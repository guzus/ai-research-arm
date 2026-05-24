#!/usr/bin/env python3
"""Validate LLM Wiki pages against the schema in docs/wiki-schema.md.

Usage:
    uv run python scripts/check_wiki.py
    uv run python scripts/check_wiki.py path/to/page.md ...
    uv run python scripts/check_wiki.py --root path/to/wiki
    uv run python scripts/check_wiki.py --lint     # advisory, always exit 0

Exit 0 when every page is valid (and index/log are consistent). Exit 1 with a
list of failures. The `--lint` mode is advisory: it prints warnings (orphans,
stale pages, missing reciprocal links) and ALWAYS exits 0.

The schema is intentionally strict: every field listed under "Frontmatter
schema" in docs/wiki-schema.md is enforced here. Keep this script and the doc
in lockstep.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = REPO_ROOT / "research" / "wiki"
PAGE_SUBDIRS = ("entities", "concepts", "themes")

CANONICAL_TYPES = {"entity", "concept", "theme"}
TYPE_TO_SUBDIR = {"entity": "entities", "concept": "concepts", "theme": "themes"}
CANONICAL_LOG_OPS = {"seed", "ingest", "query", "lint"}
STALE_AFTER_DAYS = 30

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
URL_RE = re.compile(r"^https?://\S+$")
# [[slug]] or [[slug|Display Label]]. The target is everything up to an
# optional '|'. We capture the raw target and strip/validate it afterwards.
WIKILINK_RE = re.compile(r"\[\[([^\[\]]+?)\]\]")
# Fence openers/closers: ``` or ~~~ (3+), capturing indent so we close at the
# same indent level. Mirrors the CommonMark fenced-code-block rule closely
# enough for our purposes.
FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})")
LOG_LINE_RE = re.compile(r"^## \[(\d{4}-\d{2}-\d{2})\] (\S+) \| (.+)$")
INDEX_ITEM_RE = re.compile(r"^- \[\[([^\[\]|]+)\]\] — (.+)$")


@dataclass
class Failure:
    path: Path
    field: str
    msg: str


@dataclass
class Warning_:
    path: Path
    kind: str
    msg: str


@dataclass
class Page:
    path: Path
    slug: str
    type: str
    aliases: list[str]
    title: str
    body: str
    updated_at: date | None
    links: list[str]  # resolved-target slugs of outbound wikilinks


@dataclass
class Report:
    failures: list[Failure] = field(default_factory=list)
    warnings: list[Warning_] = field(default_factory=list)
    files_checked: int = 0

    def fail(self, path: Path, field_name: str, msg: str) -> None:
        self.failures.append(Failure(path, field_name, msg))

    def warn(self, path: Path, kind: str, msg: str) -> None:
        self.warnings.append(Warning_(path, kind, msg))

    def ok(self) -> bool:
        return not self.failures


def _split_frontmatter(text: str, path: Path, report: Report) -> tuple[dict[str, Any] | None, str]:
    """Return (frontmatter_dict, body). Returns (None, '') on parse failure.

    Hand-rolled (not imported from compile_ara) so the validator stays
    self-contained, matching check_model_tickets.py.
    """
    if not text.startswith("---\n"):
        report.fail(path, "frontmatter", "file must start with '---' on line 1")
        return None, ""
    parts = text.split("\n---\n", 1)
    if len(parts) < 2:
        report.fail(path, "frontmatter", "missing closing '---' delimiter")
        return None, ""
    header = parts[0][4:]  # drop leading '---\n'
    body = parts[1].lstrip("\n")
    try:
        data = yaml.safe_load(header)
    except yaml.YAMLError as e:
        report.fail(path, "frontmatter", f"YAML parse error: {e}")
        return None, ""
    if not isinstance(data, dict):
        report.fail(path, "frontmatter", "frontmatter must be a mapping")
        return None, ""
    return data, body


def _check_str(data: dict, key: str, path: Path, report: Report, *, required: bool = True) -> str | None:
    val = data.get(key)
    if val is None:
        if required:
            report.fail(path, key, "required field missing or null")
        return None
    if not isinstance(val, str):
        report.fail(path, key, f"must be a string, got {type(val).__name__}")
        return None
    if not val.strip():
        report.fail(path, key, "must not be empty")
        return None
    return val


def _check_date(data: dict, key: str, path: Path, report: Report) -> date | None:
    val = data.get(key)
    if val is None:
        report.fail(path, key, "required date missing or null")
        return None
    if isinstance(val, date):
        return val
    if isinstance(val, str):
        try:
            return date.fromisoformat(val)
        except ValueError:
            report.fail(path, key, f"not a valid ISO date (YYYY-MM-DD): {val!r}")
            return None
    report.fail(path, key, f"must be a date, got {type(val).__name__}")
    return None


def _check_str_list(data: dict, key: str, path: Path, report: Report) -> list[str]:
    """Optional list[str]. Returns [] when absent; reports on type errors."""
    if key not in data or data[key] is None:
        return []
    val = data[key]
    if not isinstance(val, list):
        report.fail(path, key, "must be a list")
        return []
    out: list[str] = []
    for i, item in enumerate(val):
        if not isinstance(item, str) or not item.strip():
            report.fail(path, key, f"item {i} must be a non-empty string")
            continue
        out.append(item)
    return out


def _check_sources(val: Any, path: Path, report: Report) -> None:
    """Optional list of mappings; each has `title` (req) + optional url/path/date."""
    if not isinstance(val, list):
        report.fail(path, "sources", "must be a list of mappings")
        return
    if not val:
        report.fail(path, "sources", "must be omitted entirely rather than an empty list")
        return
    for i, src in enumerate(val):
        if not isinstance(src, dict):
            report.fail(path, "sources", f"item {i} must be a mapping (got {type(src).__name__})")
            continue
        title = src.get("title")
        if not isinstance(title, str) or not title.strip():
            report.fail(path, "sources", f"item {i} requires a non-empty 'title'")
        if "url" in src and src["url"] is not None:
            if not isinstance(src["url"], str) or not URL_RE.match(src["url"]):
                report.fail(path, "sources", f"item {i} url must be http(s)://… ({src.get('url')!r})")
        if "path" in src and src["path"] is not None and not isinstance(src["path"], str):
            report.fail(path, "sources", f"item {i} path must be a string")
        if "date" in src and src["date"] is not None:
            d = src["date"]
            if isinstance(d, date):
                pass
            elif isinstance(d, str):
                try:
                    date.fromisoformat(d)
                except ValueError:
                    report.fail(path, "sources", f"item {i} date not ISO (YYYY-MM-DD): {d!r}")
            else:
                report.fail(path, "sources", f"item {i} date must be a date or ISO string")
        allowed = {"title", "url", "path", "date"}
        extra = set(src) - allowed
        if extra:
            report.fail(path, "sources", f"item {i} has unknown keys {sorted(extra)} (allowed: {sorted(allowed)})")


def extract_wikilinks(body: str) -> list[str]:
    """Return raw link targets from [[...]] in `body`, skipping fenced code.

    A wikilink target is the text before an optional '|'. Lines inside fenced
    code blocks (``` or ~~~) are ignored so that documentation examples don't
    register as real links. Inline single-backtick spans are a known v1
    limitation (not stripped) — keep code examples in fences.
    """
    targets: list[str] = []
    fence: str | None = None  # the active fence marker char-run, e.g. '```'
    fence_indent = ""
    for line in body.splitlines():
        m = FENCE_RE.match(line)
        if fence is None:
            if m:
                fence = m.group(2)
                fence_indent = m.group(1)
            continue  # opener line itself carries no links we care about
        else:
            # Inside a fence: a closer is a fence marker of the same type,
            # >= length, at the same indent, with nothing meaningful after it.
            if m and m.group(2)[0] == fence[0] and len(m.group(2)) >= len(fence) and m.group(1) == fence_indent:
                rest = line[m.end():].strip()
                if not rest:
                    fence = None
            continue  # never extract links from inside a fence
    # Re-walk for links on non-fenced lines (cleaner than interleaving).
    fence = None
    fence_indent = ""
    for line in body.splitlines():
        m = FENCE_RE.match(line)
        if fence is None:
            if m:
                fence = m.group(2)
                fence_indent = m.group(1)
                continue
            for raw in WIKILINK_RE.findall(line):
                target = raw.split("|", 1)[0].strip()
                if target:
                    targets.append(target)
        else:
            if m and m.group(2)[0] == fence[0] and len(m.group(2)) >= len(fence) and m.group(1) == fence_indent:
                if not line[m.end():].strip():
                    fence = None
    return targets


def load_page(path: Path, report: Report) -> Page | None:
    """Validate one page file's frontmatter + body. Returns a Page on success.

    Per-file checks only. Cross-file checks (uniqueness, link resolution,
    index/log consistency) happen in the corpus pass.
    """
    report.files_checked += 1
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        report.fail(path, "io", f"cannot read file: {e}")
        return None

    data, body = _split_frontmatter(text, path, report)
    if data is None:
        return None

    slug = _check_str(data, "slug", path, report)
    if slug and not SLUG_RE.match(slug):
        report.fail(path, "slug", f"must match {SLUG_RE.pattern}, got {slug!r}")
        slug = None
    if slug:
        expected_filename = f"{slug}.md"
        if path.name != expected_filename:
            report.fail(path, "slug", f"filename {path.name!r} must match slug + '.md' ({expected_filename!r})")

    title = _check_str(data, "title", path, report)

    type_ = _check_str(data, "type", path, report)
    if type_ and type_ not in CANONICAL_TYPES:
        report.fail(path, "type", f"must be one of {sorted(CANONICAL_TYPES)}, got {type_!r}")
        type_ = None
    # Page must live in the subdir that matches its type.
    if type_:
        expected_subdir = TYPE_TO_SUBDIR[type_]
        if path.parent.name != expected_subdir:
            report.fail(
                path,
                "type",
                f"type={type_!r} pages live in {expected_subdir}/, but file is in {path.parent.name}/",
            )

    aliases = _check_str_list(data, "aliases", path, report)
    _check_str_list(data, "tags", path, report)
    _check_str(data, "summary", path, report)
    # summary must be a single line (one-liner contract).
    summary_val = data.get("summary")
    if isinstance(summary_val, str) and "\n" in summary_val.strip():
        report.fail(path, "summary", "must be a single line (no embedded newlines)")

    created_at = _check_date(data, "created_at", path, report)
    updated_at = _check_date(data, "updated_at", path, report)
    if created_at and updated_at and updated_at < created_at:
        report.fail(path, "updated_at", f"updated_at {updated_at} < created_at {created_at}")

    if "sources" in data and data["sources"] is not None:
        _check_sources(data["sources"], path, report)

    if not body.strip():
        report.fail(path, "body", "body must not be empty — write markdown under the frontmatter")

    links = extract_wikilinks(body)

    if slug is None or type_ is None:
        return None  # too broken to participate in the corpus pass
    return Page(
        path=path,
        slug=slug,
        type=type_,
        aliases=aliases,
        title=title or slug,
        body=body,
        updated_at=updated_at,
        links=links,
    )


def build_resolver(pages: list[Page], report: Report) -> dict[str, str]:
    """Map every slug AND alias (lowercased) → owning slug. Fail on collisions.

    The wikilink namespace is slugs ∪ aliases; a link resolves if its
    lowercased target is a key here. Collisions (two pages claiming the same
    name) are hard failures because they make resolution ambiguous.
    """
    resolver: dict[str, str] = {}
    owner: dict[str, Page] = {}

    def claim(name: str, page: Page, kind: str) -> None:
        # Collision is keyed on the OWNING PAGE (by path), not the slug string:
        # two distinct files sharing a slug must collide even though their slug
        # values are equal. This is what enforces filename-stem uniqueness
        # across subdirs (the global-identity contract).
        key = name.lower()
        if key in resolver and owner[key].path != page.path:
            prev = owner[key]
            report.fail(
                page.path,
                kind,
                f"{kind} {name!r} collides with {prev.path.name} (already maps to slug {resolver[key]!r})",
            )
            return
        resolver[key] = page.slug
        owner[key] = page

    # Claim slugs first so an alias colliding with a slug is reported against
    # the alias-owner (more actionable).
    for page in pages:
        claim(page.slug, page, "slug")
    for page in pages:
        for alias in page.aliases:
            if alias.lower() == page.slug.lower():
                continue  # alias == own slug: harmless, skip
            claim(alias, page, "aliases")
    return resolver


def check_corpus(pages: list[Page], report: Report) -> dict[str, str]:
    """Cross-file checks: slug uniqueness, link resolution. Returns resolver."""
    resolver = build_resolver(pages, report)
    for page in pages:
        for target in page.links:
            if target.lower() not in resolver:
                report.fail(
                    page.path,
                    "links",
                    f"[[{target}]] does not resolve to any page slug or alias",
                )
    return resolver


def _read_optional(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def check_index(wiki_dir: Path, pages: list[Page], report: Report) -> None:
    """index.md ↔ pages: every page listed once; every listed slug exists."""
    index_path = wiki_dir / "index.md"
    text = _read_optional(index_path)
    if text is None:
        report.fail(index_path, "index", "research/wiki/index.md is missing")
        return

    lines = text.splitlines()
    if not lines or lines[0].strip() != "# Wiki Index":
        report.fail(index_path, "index", "first line must be '# Wiki Index'")

    listed: list[str] = []
    current_section: str | None = None
    section_for_type = {"entity": "Entities", "concept": "Concepts", "theme": "Themes"}
    type_for_section = {v: k for k, v in section_for_type.items()}
    listed_section: dict[str, str] = {}
    for line in lines:
        s = line.strip()
        if s.startswith("## "):
            current_section = s[3:].strip()
            continue
        m = INDEX_ITEM_RE.match(line)
        if m:
            slug = m.group(1).strip()
            listed.append(slug)
            if current_section:
                listed_section[slug] = current_section

    page_slugs = {p.slug: p for p in pages}
    dupes = {s for s in listed if listed.count(s) > 1}
    for s in sorted(dupes):
        report.fail(index_path, "index", f"slug {s!r} listed more than once")

    for slug in listed:
        if slug not in page_slugs:
            report.fail(index_path, "index", f"listed slug {slug!r} has no page file")
            continue
        # Section must match the page's type.
        sect = listed_section.get(slug)
        page = page_slugs[slug]
        expected_section = section_for_type[page.type]
        if sect is not None and sect in type_for_section and sect != expected_section:
            report.fail(
                index_path,
                "index",
                f"{slug!r} is under '## {sect}' but type={page.type} → belongs under '## {expected_section}'",
            )

    listed_set = set(listed)
    for slug in page_slugs:
        if slug not in listed_set:
            report.fail(index_path, "index", f"page {slug!r} is not listed in the index")


def check_log(wiki_dir: Path, report: Report) -> None:
    """log.md: lines '## [YYYY-MM-DD] <op> | <summary>', dates non-decreasing."""
    log_path = wiki_dir / "log.md"
    text = _read_optional(log_path)
    if text is None:
        report.fail(log_path, "log", "research/wiki/log.md is missing")
        return

    prev: date | None = None
    saw_entry = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        if not line.startswith("## "):
            continue  # headings/prose allowed between entries; only validate '## ' lines
        m = LOG_LINE_RE.match(line)
        if not m:
            report.fail(log_path, "log", f"line {lineno}: malformed entry (want '## [YYYY-MM-DD] <op> | <summary>'): {line!r}")
            continue
        saw_entry = True
        ds, op, summary = m.group(1), m.group(2), m.group(3)
        try:
            d = date.fromisoformat(ds)
        except ValueError:
            report.fail(log_path, "log", f"line {lineno}: bad date {ds!r}")
            continue
        if op not in CANONICAL_LOG_OPS:
            report.fail(log_path, "log", f"line {lineno}: op {op!r} must be one of {sorted(CANONICAL_LOG_OPS)}")
        if not summary.strip():
            report.fail(log_path, "log", f"line {lineno}: summary must be non-empty")
        if prev is not None and d < prev:
            report.fail(log_path, "log", f"line {lineno}: date {d} is out of order (previous was {prev})")
        prev = d
    if not saw_entry:
        report.fail(log_path, "log", "log.md has no '## [date] op | summary' entries")


def run_lint(pages: list[Page], resolver: dict[str, str], report: Report, *, today: date | None = None) -> None:
    """Advisory checks. Populate report.warnings; never report.fail()."""
    today = today or date.today()
    slug_set = {p.slug for p in pages}
    by_slug = {p.slug: p for p in pages}

    # Inbound link map: slug -> set of slugs that link to it.
    inbound: dict[str, set[str]] = {p.slug: set() for p in pages}
    outbound: dict[str, set[str]] = {p.slug: set() for p in pages}
    for page in pages:
        for target in page.links:
            tgt_slug = resolver.get(target.lower())
            if tgt_slug and tgt_slug != page.slug:
                inbound[tgt_slug].add(page.slug)
                outbound[page.slug].add(tgt_slug)

    for page in pages:
        if not inbound[page.slug]:
            report.warn(page.path, "orphan", f"{page.slug!r} has no inbound links from other pages")
        if page.updated_at is not None:
            age = (today - page.updated_at).days
            if age > STALE_AFTER_DAYS:
                report.warn(page.path, "stale", f"{page.slug!r} updated_at {page.updated_at} is {age}d old (> {STALE_AFTER_DAYS}d)")
        # Missing reciprocal: A links B but B does not link back to A.
        for tgt in sorted(outbound[page.slug]):
            if tgt in by_slug and page.slug not in outbound.get(tgt, set()):
                report.warn(page.path, "reciprocal", f"{page.slug!r} → {tgt!r} but {tgt!r} does not link back")


def gather_pages(root: Path) -> list[Path]:
    out: list[Path] = []
    for sub in PAGE_SUBDIRS:
        d = root / sub
        if d.is_dir():
            out.extend(sorted(d.glob("*.md")))
    return out


def validate(targets: list[Path], wiki_dir: Path, report: Report, *, lint: bool, today: date | None = None) -> None:
    """Core entry used by both the CLI and tests."""
    pages: list[Page] = []
    for path in targets:
        if not path.is_file():
            report.fail(path, "io", "not a regular file")
            continue
        page = load_page(path, report)
        if page is not None:
            pages.append(page)

    resolver = check_corpus(pages, report)
    check_index(wiki_dir, pages, report)
    check_log(wiki_dir, report)
    if lint:
        run_lint(pages, resolver, report, today=today)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", help="page files; defaults to research/wiki/{entities,concepts,themes}/*.md")
    parser.add_argument("--root", default=None, help="wiki root dir (default research/wiki); used for index.md/log.md and default page glob")
    parser.add_argument("--lint", action="store_true", help="advisory mode: print warnings (orphan/stale/reciprocal) and always exit 0")
    args = parser.parse_args(argv)

    wiki_dir = Path(args.root) if args.root else WIKI_DIR

    if args.paths:
        targets = [Path(p) for p in args.paths]
    else:
        if not wiki_dir.is_dir():
            print(f"no wiki dir at {wiki_dir} — nothing to validate", file=sys.stderr)
            return 0
        targets = gather_pages(wiki_dir)

    report = Report()
    validate(targets, wiki_dir, report, lint=args.lint)

    if args.lint:
        # Advisory mode: print warnings AND any hard failures (so the user sees
        # both), but ALWAYS exit 0. Hard validation is the default (non-lint) mode.
        for w in report.warnings:
            rel = w.path.relative_to(REPO_ROOT) if w.path.is_absolute() and _under(w.path, REPO_ROOT) else w.path
            print(f"LINT {rel}: {w.kind}: {w.msg}")
        if report.failures:
            print(f"\n(note: {len(report.failures)} hard validation issue(s) also present — run without --lint)")
        print(f"lint complete — {len(report.warnings)} advisory warning(s) across {report.files_checked} page(s)")
        return 0

    if report.ok():
        print(f"OK — {report.files_checked} page(s) valid")
        return 0

    for f in report.failures:
        rel = f.path.relative_to(REPO_ROOT) if f.path.is_absolute() and _under(f.path, REPO_ROOT) else f.path
        print(f"FAIL {rel}: {f.field}: {f.msg}", file=sys.stderr)
    print(f"\n{len(report.failures)} failure(s) across {report.files_checked} page(s)", file=sys.stderr)
    return 1


def _under(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    sys.exit(main())
