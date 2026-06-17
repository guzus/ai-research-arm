#!/usr/bin/env python3
"""Export research/wiki as an Open Knowledge Format bundle.

The maintained ARA wiki is stricter than baseline OKF and uses ARA-specific
fields plus [[wikilinks]]. This exporter validates that source bundle, then
writes a portable Markdown/YAML bundle whose concept files expose the OKF
frontmatter fields and standard Markdown links.

Usage:
    uv run python scripts/export_wiki_okf.py --out /tmp/ara-okf
    uv run python scripts/export_wiki_okf.py --root research/wiki --out /tmp/ara-okf
"""

from __future__ import annotations

import argparse
import posixpath
import re
import shutil
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import yaml

import check_wiki as cw

SECTION_FOR_TYPE = {
    "entity": "Entities",
    "concept": "Concepts",
    "theme": "Themes",
}


def _split_page(path: Path) -> tuple[dict[str, Any], str]:
    report = cw.Report()
    data, body = cw._split_frontmatter(path.read_text(encoding="utf-8"), path, report)
    if data is None:
        raise ValueError(f"{path} did not parse after validation")
    return data, body


def _date_to_timestamp(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.isoformat()
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    if isinstance(value, date):
        return f"{value.isoformat()}T00:00:00Z"
    if isinstance(value, str):
        # The source contract uses YYYY-MM-DD. Preserve already-expanded
        # timestamps if a caller feeds a custom bundle.
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            return f"{value}T00:00:00Z"
        return value
    return str(value)


def rewrite_wikilinks(
    body: str,
    pages: list[cw.Page],
    resolver: dict[str, str],
    wiki_dir: Path,
    current_path: Path,
) -> str:
    """Convert ARA [[wikilinks]] to OKF-friendly Markdown links.

    Fenced code blocks are preserved verbatim, matching check_wiki's extraction
    behavior so examples do not become links.
    """
    page_by_slug = {p.slug: p for p in pages}

    def replacement(match: re.Match[str]) -> str:
        raw = match.group(1)
        target, _, label = raw.partition("|")
        target = target.strip()
        slug = resolver.get(target.lower())
        if not slug or slug not in page_by_slug:
            return match.group(0)
        page = page_by_slug[slug]
        display = label.strip() or page.title
        target = page.path.relative_to(wiki_dir).as_posix()
        start = current_path.relative_to(wiki_dir).parent.as_posix()
        href = posixpath.relpath(target, start=start)
        return f"[{display}]({href})"

    out: list[str] = []
    fence: str | None = None
    fence_indent = ""
    for line in body.splitlines(keepends=True):
        line_without_newline = line.rstrip("\n")
        m = cw.FENCE_RE.match(line_without_newline)
        if fence is None:
            if m:
                fence = m.group(2)
                fence_indent = m.group(1)
                out.append(line)
                continue
            out.append(cw.WIKILINK_RE.sub(replacement, line))
            continue

        out.append(line)
        if (
            m
            and m.group(2)[0] == fence[0]
            and len(m.group(2)) >= len(fence)
            and m.group(1) == fence_indent
            and not line_without_newline[m.end() :].strip()
        ):
            fence = None

    return "".join(out)


def okf_frontmatter(data: dict[str, Any]) -> dict[str, Any]:
    """Preserve OKF-native ARA wiki frontmatter with local extension fields."""
    out: dict[str, Any] = {
        "type": str(data["type"]),
        "title": data["title"],
        "description": data["description"],
        "ara_slug": data["slug"],
        "created_at": str(data["created_at"]),
        "timestamp": _date_to_timestamp(data["timestamp"]),
    }
    for key in ("aliases", "tags", "sources", "images"):
        if key in data and data[key]:
            out[key] = data[key]
    return out


def render_concept(data: dict[str, Any], body: str) -> str:
    header = yaml.safe_dump(okf_frontmatter(data), sort_keys=False, allow_unicode=True).strip()
    return f"---\n{header}\n---\n\n{body.strip()}\n"


def render_index(pages: list[cw.Page], wiki_dir: Path) -> str:
    lines = [
        "# ARA Open Knowledge Format Bundle",
        "",
        "Generated from `research/wiki/`. Each listed file is an OKF concept document.",
        "",
    ]
    for type_ in ("entity", "concept", "theme"):
        lines.append(f"## {SECTION_FOR_TYPE[type_]}")
        lines.append("")
        for page in sorted((p for p in pages if p.type == type_), key=lambda p: p.title.lower()):
            href = str(page.path.relative_to(wiki_dir))
            data, _ = _split_page(page.path)
            preview = str(data.get("description") or "").strip()
            lines.append(f"* [{page.title}]({href}) - {preview}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def load_valid_wiki(wiki_dir: Path) -> tuple[list[cw.Page], dict[str, str]]:
    report = cw.Report()
    targets = cw.gather_pages(wiki_dir)
    cw.validate(targets, wiki_dir, report, lint=False)
    if not report.ok():
        for failure in report.failures:
            print(f"FAIL {failure.path}: {failure.field}: {failure.msg}", file=sys.stderr)
        raise SystemExit(1)

    pages: list[cw.Page] = []
    load_report = cw.Report()
    for path in targets:
        page = cw.load_page(path, load_report)
        if page is not None:
            pages.append(page)
    resolver = cw.build_resolver(pages, load_report)
    if not load_report.ok():
        for failure in load_report.failures:
            print(f"FAIL {failure.path}: {failure.field}: {failure.msg}", file=sys.stderr)
        raise SystemExit(1)
    return pages, resolver


def export_okf(wiki_dir: Path, out_dir: Path, *, clean: bool) -> None:
    pages, resolver = load_valid_wiki(wiki_dir)

    if out_dir.exists():
        if not clean:
            raise SystemExit(f"{out_dir} already exists; pass --clean to replace it")
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "index.md").write_text(render_index(pages, wiki_dir), encoding="utf-8")

    for page in pages:
        data, body = _split_page(page.path)
        converted = rewrite_wikilinks(body, pages, resolver, wiki_dir, page.path)
        rel = page.path.relative_to(wiki_dir)
        dest = out_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(render_concept(data, converted), encoding="utf-8")

    print(f"wrote OKF bundle to {out_dir} ({len(pages)} concept document(s))")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=None, help="wiki root dir (default research/wiki)")
    parser.add_argument("--out", required=True, help="output directory for the OKF bundle")
    parser.add_argument("--clean", action="store_true", help="replace the output directory if it already exists")
    args = parser.parse_args(argv)

    wiki_dir = Path(args.root) if args.root else cw.WIKI_DIR
    out_dir = Path(args.out)
    export_okf(wiki_dir, out_dir, clean=args.clean)
    return 0


if __name__ == "__main__":
    sys.exit(main())
