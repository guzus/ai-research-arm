#!/usr/bin/env python3
"""Write a generative research HTML fragment into research/generative/.

Used by all three trigger paths (local slash command, GitHub issue label,
workflow_dispatch). Pure I/O — never calls an LLM. The contract:

  * Body must be a single <article>...</article> fragment.
  * No <script>, <style>, or inline style= attributes.
  * The file is named <YYYY-MM-DDTHHMMSS>--<slug>.html (UTC).
  * research/generative/index.json holds the canonical list (ascending).

The dashboard reads index.json via the deploy manifest and renders the
list newest-first.
"""

from __future__ import annotations

import argparse
import difflib
import fcntl
import html.parser
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

# Local import — the compiler lives next door in scripts/.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ara_catalog import catalog_classes, load_catalog  # noqa: E402
from compile_ara import AraSyntaxError, compile_source, is_safe_image_src  # noqa: E402

MAX_BODY_BYTES = 200_000
MAX_STANDALONE_BYTES = 2_000_000
SLUG_MAX = 60
KIND_FRAGMENT = "fragment"
KIND_STANDALONE = "standalone"
KINDS = (KIND_FRAGMENT, KIND_STANDALONE)
DEFAULT_LANGUAGE = "en"
SUPPORTED_TRANSLATION_LANGUAGES = ("ko",)
LANGUAGES = (DEFAULT_LANGUAGE, *SUPPORTED_TRANSLATION_LANGUAGES)
DISALLOWED_PATTERNS = [
    re.compile(r"\sstyle\s*=", re.IGNORECASE),
    re.compile(r"\son\w+\s*=", re.IGNORECASE),  # onclick=, onload=, etc.
    re.compile(r"javascript:", re.IGNORECASE),
]
# Fragment articles must compose from this fixed tag set + the ara-* class
# vocabulary defined in ARA_CATALOG.json. See COMPONENTS.md for the
# human-readable reference.
FRAGMENT_ALLOWED_TAGS = frozenset([
    "article", "section", "div", "header", "footer",
    "h2", "h3", "h4",
    "p", "span", "em", "strong", "code", "mark", "sup", "sub", "abbr", "time",
    "ul", "ol", "li", "dl", "dt", "dd",
    "a", "img", "figure", "figcaption",
    "table", "thead", "tbody", "tr", "th", "td",
    "blockquote", "pre",
    "br", "hr",
])
FRAGMENT_CLASS_PREFIX = "ara-"
# Canonical class vocabulary lives in ARA_CATALOG.json at repo root. Loaded
# lazily on first validation so the test/CI paths can override the path.
_VALID_CLASSES_CACHE: set[str] | None = None
_ARA_CATALOG_PATH: Path | None = None
_COMPONENTS_MD_PATH: Path | None = None


def _components_md_path() -> Path:
    if _COMPONENTS_MD_PATH is not None:
        return _COMPONENTS_MD_PATH
    # The writer lives at scripts/write_generative_research.py — COMPONENTS.md
    # sits at the repo root one level up.
    return Path(__file__).resolve().parent.parent / "COMPONENTS.md"


def _ara_catalog_path() -> Path:
    if _ARA_CATALOG_PATH is not None:
        return _ARA_CATALOG_PATH
    return Path(__file__).resolve().parent.parent / "ARA_CATALOG.json"


def load_valid_classes() -> set[str]:
    """Load every cataloged ara-* base class. Cached after first call so
    we don't re-read the file for every validated article in a batch.

    Raises loudly if the file is missing or no classes can be parsed.
    COMPONENTS.md remains a fallback because some tests may override that
    path directly, but the normal source of truth is ARA_CATALOG.json.
    """
    global _VALID_CLASSES_CACHE
    if _VALID_CLASSES_CACHE is not None:
        return _VALID_CLASSES_CACHE
    catalog_path = _ara_catalog_path()
    if catalog_path.exists():
        _VALID_CLASSES_CACHE = catalog_classes(load_catalog(catalog_path))
        return _VALID_CLASSES_CACHE

    md_path = _components_md_path()
    if not md_path.exists():
        raise RuntimeError(
            f"ARA_CATALOG.json not found at {catalog_path} and COMPONENTS.md "
            f"not found at {md_path}. The fragment validator needs the ara-* "
            f"class vocabulary; without it "
            f"every article would be rejected as 'undocumented class'. "
            f"Restore the catalog/reference or set _ARA_CATALOG_PATH/_COMPONENTS_MD_PATH for tests."
        )
    text = md_path.read_text(encoding="utf-8")
    # Only the component vocabulary table is authoritative. COMPONENTS.md
    # also contains explicit anti-examples like `ara-grid`; scraping every
    # backticked ara-* token would incorrectly make those valid classes.
    found = set()
    for line in text.splitlines():
        m = re.match(r"\|\s*`(ara-[a-z0-9-]+)`\s*\|", line)
        if m:
            found.add(m.group(1))
    if not found:
        raise RuntimeError(
            f"COMPONENTS.md at {md_path} parsed to ZERO ara-* classes. "
            f"The vocabulary table format may have changed (expected lines "
            f"like '| `ara-foo` | ...'). Without classes loaded, every "
            f"article would be silently rejected."
        )
    _VALID_CLASSES_CACHE = found
    return found


def is_valid_ara_class(token: str, valid: set[str]) -> bool:
    """A class is valid if it's documented, OR it's a modifier of a
    documented base (e.g. `ara-callout--info` when `ara-callout` is
    documented)."""
    if not token.startswith(FRAGMENT_CLASS_PREFIX):
        return False
    if token in valid:
        return True
    if "--" in token:
        base = token.split("--", 1)[0]
        if base in valid:
            return True
    return False


def _valid_number(value: str, lo: float | None = None, hi: float | None = None) -> bool:
    try:
        n = float(value.strip())
    except ValueError:
        return False
    if not math.isfinite(n):
        return False
    if lo is not None and n < lo:
        return False
    if hi is not None and n > hi:
        return False
    return True


def _valid_int(value: str, lo: int | None = None, hi: int | None = None) -> bool:
    try:
        n = float(value.strip())
    except ValueError:
        return False
    if not math.isfinite(n) or not n.is_integer():
        return False
    i = int(n)
    if lo is not None and i < lo:
        return False
    if hi is not None and i > hi:
        return False
    return True


def _valid_number_list(value: str) -> bool:
    parts = [p.strip() for p in value.split(",") if p.strip()]
    return bool(parts) and all(_valid_number(p) for p in parts)


ARTICLE_OPEN = re.compile(r"<article\b[^>]*>", re.IGNORECASE)
ARTICLE_CLOSE = re.compile(r"</article\s*>", re.IGNORECASE)
H2_TEXT = re.compile(r"<h2\b[^>]*>(.*?)</h2>", re.IGNORECASE | re.DOTALL)
HTML_TITLE = re.compile(r"<title\b[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
H1_TEXT = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)
TAG_STRIP = re.compile(r"<[^>]+>")


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    if len(text) > SLUG_MAX:
        text = text[:SLUG_MAX].rstrip("-")
    return text or "untitled"


def read_body(source: str) -> str:
    if source == "-":
        return sys.stdin.read()
    return Path(source).read_text(encoding="utf-8")


def detect_dsl(path_or_stdin: str, body: str) -> bool:
    """`.ara.md` extension is the canonical signal. If reading from stdin
    we sniff for `---\n` frontmatter — but only count it as DSL if we
    also see a known marker like `:::` or `## ` near the top, so a stray
    HTML comment doesn't trigger compile."""
    if path_or_stdin != "-" and path_or_stdin.endswith(".ara.md"):
        return True
    head = body[:4096]
    if head.startswith("---\n") and ("\n:::" in head or "\n## " in head or "\n# " in head):
        return True
    return False


class _FragmentValidator(html.parser.HTMLParser):
    """Parse-aware check: every tag must be in FRAGMENT_ALLOWED_TAGS,
    every class= token must be a documented ara-* class (or a modifier
    of one)."""

    def __init__(self, valid_classes: set[str]):
        super().__init__(convert_charrefs=True)
        self.valid_classes = valid_classes
        self.bad_tags: list[str] = []
        self.bad_classes: list[tuple[str, str]] = []  # (tag, non-ara token)
        self.unknown_ara: list[tuple[str, str]] = []  # (tag, ara-* token not in vocab)
        self.bad_attrs: list[tuple[str, str, str | None]] = []

    def _check(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() not in FRAGMENT_ALLOWED_TAGS:
            self.bad_tags.append(tag.lower())
            return
        for name, value in attrs:
            attr = name.lower()
            if attr == "class":
                if not value:
                    continue
                for tok in value.split():
                    if not tok.startswith(FRAGMENT_CLASS_PREFIX):
                        self.bad_classes.append((tag.lower(), tok))
                    elif not is_valid_ara_class(tok, self.valid_classes):
                        self.unknown_ara.append((tag.lower(), tok))
                continue
            if not self._attr_allowed(tag.lower(), attr, value):
                self.bad_attrs.append((tag.lower(), attr, value))

    def _attr_allowed(self, tag: str, attr: str, value: str | None) -> bool:
        if attr.startswith("data-"):
            return bool(re.match(r"^data-[a-z0-9-]+$", attr)) and self._data_attr_allowed(attr, value)
        if attr == "id":
            return tag == "li" and bool(value and re.match(r"^ref-[0-9]+$", value))
        if attr == "href":
            return tag == "a" and bool(value and re.match(r"^(https?://|/|#ref-[0-9]+$)", value))
        if attr == "src":
            return tag == "img" and bool(value and is_safe_image_src(value))
        if attr == "alt":
            return tag == "img"
        if attr == "loading":
            return tag == "img" and value in {"lazy", "eager"}
        if attr == "decoding":
            return tag == "img" and value in {"async", "sync", "auto"}
        if attr == "referrerpolicy":
            return tag == "img" and value in {
                "no-referrer",
                "no-referrer-when-downgrade",
                "origin",
                "origin-when-cross-origin",
                "same-origin",
                "strict-origin",
                "strict-origin-when-cross-origin",
                "unsafe-url",
            }
        return False

    def _data_attr_allowed(self, attr: str, value: str | None) -> bool:
        if value is None:
            return False
        free_text = {
            "data-x-labels",
            "data-title",
            "data-subtitle",
            "data-y-unit",
            "data-series-1-label",
            "data-series-2-label",
            "data-series-3-label",
            "data-series-4-label",
            "data-series-5-label",
            "data-series-6-label",
            "data-labels",
            "data-center-label",
            "data-items",
            "data-left-label",
            "data-right-label",
            "data-unit",
            "data-glyph",
            # bar-chart
            "data-categories",
            "data-orientation",
            "data-mode",
            "data-value-suffix",
        }
        if attr in free_text:
            return True
        if attr == "data-pct":
            return _valid_number(value, lo=0, hi=100)
        if attr == "data-count":
            return _valid_int(value, lo=0, hi=200)
        if attr in {
            "data-points",
            "data-values",
            "data-left-values",
            "data-right-values",
            "data-series-1",
            "data-series-2",
            "data-series-3",
            "data-series-4",
            "data-series-5",
            "data-series-6",
        }:
            return _valid_number_list(value)
        # ara-tradingview: config for the dashboard-injected widget. Strict
        # charset on the symbol (it reaches a third-party widget + a URL);
        # interval/range are charset-gated, theme is an enum.
        # \Z (not $): Python's $ matches before a trailing newline, which would
        # let data-symbol="X\n" slip the gate. \Z anchors the true end and keeps
        # this mirror byte-identical to the compiler's _TV_*_RE patterns.
        if attr == "data-symbol":
            return bool(re.match(r"^[A-Za-z0-9:._-]{1,32}\Z", value))
        if attr == "data-interval":
            return bool(re.match(r"^[A-Za-z0-9]{1,5}\Z", value))
        if attr == "data-range":
            return bool(re.match(r"^[A-Za-z0-9]{1,4}\Z", value))
        if attr == "data-theme":
            return value in {"dark", "light"}
        return False

    def handle_starttag(self, tag, attrs):
        self._check(tag, attrs)

    def handle_startendtag(self, tag, attrs):
        self._check(tag, attrs)


def validate_body(body: str, kind: str) -> None:
    if kind == KIND_FRAGMENT:
        if len(body.encode("utf-8")) > MAX_BODY_BYTES:
            raise ValueError(f"fragment body exceeds {MAX_BODY_BYTES} bytes")
        if not ARTICLE_OPEN.search(body):
            raise ValueError("fragment body must contain an opening <article> tag")
        if not ARTICLE_CLOSE.search(body):
            raise ValueError("fragment body must contain a closing </article> tag")
        for pat in DISALLOWED_PATTERNS:
            m = pat.search(body)
            if m:
                raise ValueError(f"fragment body contains disallowed pattern: {m.group(0)!r}")
        valid_classes = load_valid_classes()
        parser = _FragmentValidator(valid_classes)
        parser.feed(body)
        if parser.bad_tags:
            uniq = sorted(set(parser.bad_tags))
            raise ValueError(
                f"fragment uses disallowed tags: {uniq}. "
                f"Allowed: {sorted(FRAGMENT_ALLOWED_TAGS)}. See ARA_CATALOG.json and COMPONENTS.md."
            )
        if parser.bad_classes:
            preview = ", ".join(f"<{t}> class={c!r}" for t, c in parser.bad_classes[:5])
            raise ValueError(
                f"fragment uses non-{FRAGMENT_CLASS_PREFIX}* classes: {preview}. "
                f"All class tokens must start with {FRAGMENT_CLASS_PREFIX!r}. "
                f"See ARA_CATALOG.json for the vocabulary."
            )
        if parser.unknown_ara:
            # Group by class so a single repeated mistake doesn't spam.
            uniq = sorted(set(c for _, c in parser.unknown_ara))
            sample = sorted(valid_classes)
            lines = [
                f"fragment uses {len(uniq)} undocumented ara-* class"
                f"{'es' if len(uniq) != 1 else ''} (these have no CSS so "
                f"they render with NO STYLING — silent design-system "
                f"failure):",
                "",
            ]
            for tok in uniq:
                suggestions = difflib.get_close_matches(tok, sample, n=3, cutoff=0.5)
                hint = f"  → did you mean: {', '.join(suggestions)}" if suggestions else ""
                lines.append(f"  - {tok}{hint}")
            lines.extend([
                "",
                "Every ara-* class must be cataloged in ARA_CATALOG.json (or "
                "be a modifier like ara-callout--info of a cataloged base).",
                "Fix the body and re-run.",
            ])
            raise ValueError("\n".join(lines))
        if parser.bad_attrs:
            preview = ", ".join(
                f"<{t}> {a}={v!r}" if v is not None else f"<{t}> {a}"
                for t, a, v in parser.bad_attrs[:5]
            )
            raise ValueError(
                f"fragment uses disallowed attributes: {preview}. "
                "Allowed attributes are class, data-*, reference ids, safe href/src, and safe img metadata."
            )
    elif kind == KIND_STANDALONE:
        # Standalone docs are full HTML pages rendered inside a sandboxed
        # iframe. The sandbox is the security boundary, not regex on the body.
        if len(body.encode("utf-8")) > MAX_STANDALONE_BYTES:
            raise ValueError(f"standalone body exceeds {MAX_STANDALONE_BYTES} bytes")
        if "<html" not in body.lower() and "<!doctype" not in body.lower():
            raise ValueError("standalone body should start with <!doctype html> or <html>")
    else:
        raise ValueError(f"unknown kind: {kind!r}")


def derive_title(body: str, kind: str, fallback: str) -> str:
    if kind == KIND_STANDALONE:
        for pat in (HTML_TITLE, H1_TEXT, H2_TEXT):
            m = pat.search(body)
            if m:
                text = TAG_STRIP.sub("", m.group(1)).strip()
                if text:
                    return text
    else:
        m = H2_TEXT.search(body)
        if m:
            text = TAG_STRIP.sub("", m.group(1)).strip()
            if text:
                return text
    return fallback.strip() or "Untitled"


def atomic_write_json(path: Path, data) -> None:
    fd, tmp = tempfile.mkstemp(prefix=".idx-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def load_index(path: Path) -> list:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    data = json.loads(text)
    if not isinstance(data, list):
        raise ValueError(f"{path} is not a JSON array")
    return data


def _parse_index_text(text: str, path: Path) -> list:
    """Parse JSON-array index text. Empty/whitespace-only treated as []."""
    text = text.strip()
    if not text:
        return []
    data = json.loads(text)
    if not isinstance(data, list):
        raise ValueError(f"{path} is not a JSON array")
    return data


def append_index_atomically(index_path: Path, base_slug: str, row_builder) -> tuple[str, list]:
    """Read-modify-write `index.json` under an exclusive file lock.

    Two concurrent invocations of write_generative_research.py on the same
    machine used to race here: each read a snapshot, derived a unique slug
    against that snapshot, and both wrote back the full array. The second
    writer's write-back wiped the first writer's appended row. The workflow's
    post-push union-by-slug merge only repairs damage that survives to the
    push step.

    Locking strategy:
      * fcntl.flock(LOCK_EX) on a SEPARATE lockfile next to index.json.
        Locking on index.json itself would not work: os.replace() rotates
        the file to a fresh inode, so subsequent writers would open the
        new inode (no lock) and miss the critical section. The lockfile
        is created once and never renamed.
      * Inside the locked region we re-read index.json — any earlier
        in-memory snapshot is stale by definition.
      * Slug uniqueness is decided against the LIVE on-disk index, then
        the row is appended and the file is rewritten via
        atomic_write_json (os.replace).

    Args:
      index_path: research/generative/index.json
      base_slug:  slug stem; we append `-2`, `-3`, ... if the locked snapshot
                  already contains it.
      row_builder: callable(final_slug: str) -> dict — builds the index row
                   once we've allocated a unique slug under the lock. Any
                   side effects (writing the HTML/DSL files) should happen
                   INSIDE the builder so they are also serialized.

    Returns: (final_slug, updated_index)
    """
    index_path.parent.mkdir(parents=True, exist_ok=True)
    if not index_path.exists():
        index_path.write_text("[]\n", encoding="utf-8")
    lock_path = index_path.with_suffix(index_path.suffix + ".lock")
    # Open the lockfile with O_CREAT — multiple processes share the same
    # underlying inode. flock is advisory and POSIX-only (Linux runner +
    # macOS dev). Windows would need msvcrt.locking; not supported here.
    lock_fd = os.open(str(lock_path), os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        # Re-read inside the lock — sibling writers may have appended
        # since the caller looked at the file.
        current = _parse_index_text(
            index_path.read_text(encoding="utf-8"), index_path
        )
        existing_slugs = {
            row.get("slug") for row in current if isinstance(row, dict)
        }
        slug = base_slug
        n = 2
        while slug in existing_slugs:
            slug = f"{base_slug}-{n}"
            n += 1
        row = row_builder(slug)
        current.append(row)
        atomic_write_json(index_path, current)
    finally:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
        finally:
            os.close(lock_fd)
    return slug, current


def update_translation_atomically(
    index_path: Path,
    target_slug: str,
    language: str,
    row_builder,
) -> tuple[str, list]:
    """Attach a translated artifact to an existing generative article row.

    The dashboard cannot discover pushed files by directory listing, so a
    backfilled translation must be represented in index.json. This mutates the
    existing row instead of appending a new article, keeping `/research/<slug>`
    as the canonical article URL while allowing the UI to fetch a language
    variant when present.
    """
    index_path.parent.mkdir(parents=True, exist_ok=True)
    if not index_path.exists():
        raise ValueError(f"{index_path} does not exist; cannot backfill translation")
    lock_path = index_path.with_suffix(index_path.suffix + ".lock")
    lock_fd = os.open(str(lock_path), os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        current = _parse_index_text(
            index_path.read_text(encoding="utf-8"), index_path
        )
        for row in current:
            if not isinstance(row, dict) or row.get("slug") != target_slug:
                continue
            translations = row.get("translations")
            if not isinstance(translations, dict):
                translations = {}
                row["translations"] = translations
            translations[language] = row_builder(target_slug)
            atomic_write_json(index_path, current)
            return target_slug, current
        raise ValueError(
            f"translation target slug {target_slug!r} not found in {index_path}"
        )
    finally:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
        finally:
            os.close(lock_fd)


def git_commit(repo: Path, files: list[Path], message: str) -> None:
    rels = [str(p.relative_to(repo)) for p in files]
    subprocess.run(["git", "-C", str(repo), "add", "--", *rels], check=True)
    diff = subprocess.run(
        ["git", "-C", str(repo), "diff", "--cached", "--quiet"],
    )
    if diff.returncode == 0:
        print("write_generative_research: no staged changes; skipping commit", file=sys.stderr)
        return
    subprocess.run(
        ["git", "-C", str(repo), "commit", "-m", message],
        check=True,
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--topic", required=True, help="user-supplied topic; default title source")
    p.add_argument("--html-body", required=True, help="path to <article> fragment, or '-' for stdin")
    p.add_argument("--model", required=True, help="model identifier, e.g. claude-opus-4-7")
    p.add_argument("--title", default=None, help="explicit title; falls back to first <h2> then topic")
    p.add_argument("--slug", default=None, help="url slug; falls back to slugify(topic)")
    p.add_argument("--prompt", default=None, help="original user prompt (stored in index)")
    p.add_argument("--tags", default="", help="comma-separated tags")
    p.add_argument("--source", default="local", help="trigger source: local, workflow_dispatch, issue, import")
    p.add_argument(
        "--language",
        default=DEFAULT_LANGUAGE,
        choices=LANGUAGES,
        help="article language; non-English values backfill an existing row",
    )
    p.add_argument(
        "--translation-of",
        default=None,
        help="existing article slug to attach this translated artifact to",
    )
    p.add_argument(
        "--kind",
        default=KIND_FRAGMENT,
        choices=KINDS,
        help=(
            "fragment (default) = single <article> rendered with dashboard styles; "
            "standalone = full HTML page rendered inside a sandboxed iframe"
        ),
    )
    p.add_argument("--no-commit", action="store_true", help="skip git commit")
    p.add_argument(
        "--repo-root",
        default=str(Path(__file__).resolve().parent.parent),
        help="repo root (default: parent of scripts/)",
    )
    # Research-quality gates — same flags as scripts/check_generative_research.py.
    # When set, the writer re-validates the compiled body AFTER validate_body()
    # and BEFORE allocating the slug + writing files. A failure here aborts
    # before any disk state changes so retries start clean. The workflow passes
    # the same flags to both check_generative_research and write_generative_research
    # to guarantee local-vs-CI behavior matches.
    p.add_argument(
        "--cite-density-min",
        type=float,
        default=None,
        metavar="FLOAT",
        help="fail commit if cite density < N citations per 1,000 words",
    )
    p.add_argument(
        "--refs-min",
        type=int,
        default=None,
        metavar="INT",
        help="fail commit if references list has < N entries",
    )
    p.add_argument(
        "--primary-share-min",
        type=float,
        default=None,
        metavar="FLOAT",
        help="fail commit if < FLOAT (0-1) of references are primary sources",
    )
    p.add_argument(
        "--cited-claims-min",
        type=float,
        default=None,
        metavar="FLOAT",
        help="fail commit if < FLOAT (0-1) of substantive sentences carry a cite",
    )
    # Corroboration gate (--min-corroborating-sources). Mirrors the same flag
    # in scripts/check_generative_research.py. Opt-in only — corpus calibration
    # showed default N=2 would block legitimate articles, so workflow default
    # does NOT pass this flag. Provided here so local invocations / future
    # workflow tightening can use it.
    p.add_argument(
        "--min-corroborating-sources",
        type=int,
        default=None,
        metavar="INT",
        help=(
            "fail commit if any substantive cited claim is supported by "
            "fewer than INT distinct source hosts. Single-source claims "
            "may opt out via `==single-source: claim text==` wrapping "
            "in the DSL. Opt-in only — not yet on by default."
        ),
    )
    # qsanity scan (--qsanity). Mirrors the same flag in
    # scripts/check_generative_research.py. Warn-only in v1; passes through
    # to the check at validation time so the commit reflects the same
    # warnings the agent would have seen.
    p.add_argument(
        "--qsanity",
        action="store_true",
        help=(
            "warn-only quantitative-sanity scan; prints to stderr "
            "without failing the commit. See scripts/check_generative_research.py."
        ),
    )
    args = p.parse_args(argv)

    repo = Path(args.repo_root).resolve()
    gen_dir = repo / "research" / "generative"
    if not gen_dir.exists():
        raise SystemExit(f"missing dir: {gen_dir}")

    raw = read_body(args.html_body)
    is_dsl = detect_dsl(args.html_body, raw)
    if is_dsl:
        try:
            body = compile_source(raw)
        except AraSyntaxError as e:
            raise SystemExit(f"write_generative_research: DSL compile failed: {e}")
    else:
        body = raw
    validate_body(body, args.kind)

    # Research-quality gates (mirror check_generative_research.py flags).
    # Only fires when at least one threshold is explicitly set. The check
    # script is the source of truth for the heuristics; we import it here
    # rather than reimplement so behavior cannot drift between local-check
    # and commit-time enforcement.
    if args.kind == KIND_FRAGMENT and any(
        v is not None for v in (
            args.cite_density_min,
            args.refs_min,
            args.primary_share_min,
            args.cited_claims_min,
            args.min_corroborating_sources,
        )
    ):
        # Defer import so the writer has no hard dependency on the check
        # module unless quality gates are requested.
        from check_generative_research import enforce_quality  # noqa: E402
        errs = enforce_quality(body, args)
        if errs:
            print(
                "write_generative_research: quality gate(s) failed; "
                "REFUSING to commit. Fix the article and retry.",
                file=sys.stderr,
            )
            for line in errs:
                print(f"  - {line}", file=sys.stderr)
            raise SystemExit(1)

    # qsanity warn-only scan. Same opt-in flag as check_generative_research.
    # Printed at commit time so authors see exactly the warnings the
    # check would have emitted, even if the agent skipped the local
    # compile-check step. Never fails the commit in v1.
    if args.kind == KIND_FRAGMENT and args.qsanity:
        from check_generative_research import qsanity_scan  # noqa: E402
        cy = datetime.now(timezone.utc).year
        for line in qsanity_scan(body, cy):
            print(f"  - {line}", file=sys.stderr)

    if not body.endswith("\n"):
        body += "\n"

    title = (args.title or derive_title(body, args.kind, args.topic)).strip()
    base_slug = (args.slug or slugify(args.topic)).strip("-") or "untitled"
    language = args.language
    translation_target = (args.translation_of or "").strip()
    if language != DEFAULT_LANGUAGE and not translation_target:
        translation_target = (args.slug or "").strip()
    if language != DEFAULT_LANGUAGE and not translation_target:
        raise SystemExit(
            "write_generative_research: --language "
            f"{language!r} requires --translation-of <existing-slug> "
            "(or --slug set to that existing slug)"
        )
    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    now = datetime.now(timezone.utc).replace(microsecond=0)
    stamp = now.strftime("%Y-%m-%dT%H%M%S")
    iso = now.isoformat().replace("+00:00", "Z")

    index_path = gen_dir / "index.json"

    # Slug uniqueness + index-array mutation happen under fcntl.LOCK_EX so
    # two concurrent writers cannot both observe slug `foo`, write `foo.html`,
    # and clobber each other's index entry. The lock-and-mutate helper also
    # picks the final slug (appending `-2`, `-3`, ... if taken) inside the
    # critical section, so the slug is guaranteed unique against the file's
    # state at write time. See append_index_atomically().
    #
    # Track the actual paths we wrote (with the FINAL allocated slug, which
    # may be base_slug-2 / -3 / ...). If the index rewrite fails after the
    # HTML/DSL files were written, the except branch removes the orphans —
    # so the cleanup must reference the real paths, not derive them from
    # base_slug (which would miss `foo-2.html`).
    written_html_path: Path | None = None
    written_source_path: Path | None = None
    try:
        def _write_artifacts(final_slug: str, lang: str) -> tuple[str, Path, Path | None]:
            nonlocal written_html_path, written_source_path
            suffix = "" if lang == DEFAULT_LANGUAGE else f".{lang}"
            filename = f"{stamp}--{final_slug}{suffix}.html"
            html_path = gen_dir / filename
            if html_path.exists():
                # Extremely unlikely now that slug uniqueness is locked,
                # but stamp+slug collision is still theoretically possible
                # if two runs in the same second pick the same slug. Bail.
                raise SystemExit(
                    f"refusing to overwrite existing file: {html_path}"
                )
            html_path.write_text(body, encoding="utf-8")
            written_html_path = html_path
            if is_dsl:
                source_path = gen_dir / f"{stamp}--{final_slug}{suffix}.ara.md"
                source_path.write_text(
                    raw if raw.endswith("\n") else raw + "\n",
                    encoding="utf-8",
                )
                written_source_path = source_path
            return filename, html_path, written_source_path

        def _build_row(final_slug: str) -> dict:
            filename, _, _ = _write_artifacts(final_slug, DEFAULT_LANGUAGE)
            return {
                "slug": final_slug,
                "file": filename,
                "kind": args.kind,
                "language": DEFAULT_LANGUAGE,
                "title": title,
                "model": args.model,
                "created_at": iso,
                "source": args.source,
                "prompt": args.prompt or args.topic,
                "tags": tags,
            }

        def _build_translation(final_slug: str) -> dict:
            filename, _, _ = _write_artifacts(final_slug, language)
            return {
                "file": filename,
                "kind": args.kind,
                "language": language,
                "title": title,
                "model": args.model,
                "created_at": iso,
                "source": args.source,
                "prompt": args.prompt or args.topic,
                "tags": tags,
            }

        if language == DEFAULT_LANGUAGE:
            slug, index = append_index_atomically(index_path, base_slug, _build_row)
        else:
            slug, index = update_translation_atomically(
                index_path,
                translation_target,
                language,
                _build_translation,
            )
    except BaseException:
        # If the locked append failed AFTER we wrote the HTML / DSL source,
        # remove the orphans so a retry starts clean. We use the ACTUAL
        # written paths captured by _build_row, not paths derived from
        # base_slug — the allocated slug may be `base_slug-2`/`-3`/... so
        # deriving from base_slug would miss the real orphan and leave it
        # in the worktree forever.
        if written_html_path is not None:
            try:
                written_html_path.unlink(missing_ok=True)
            except OSError:
                pass
        if written_source_path is not None:
            try:
                written_source_path.unlink(missing_ok=True)
            except OSError:
                pass
        raise

    html_path = written_html_path or gen_dir / f"{stamp}--{slug}.html"
    print(f"wrote {html_path.relative_to(repo)}")
    print(f"updated {index_path.relative_to(repo)} ({len(index)} entries)")

    files_to_commit = [html_path, index_path]
    if written_source_path is not None:
        print(f"wrote {written_source_path.relative_to(repo)} (DSL source)")
        files_to_commit.insert(1, written_source_path)

    if not args.no_commit:
        git_commit(
            repo,
            files_to_commit,
            (
                f"Generative research translation ({language}): {title}"
                if language != DEFAULT_LANGUAGE
                else f"Generative research: {title}"
            ),
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
