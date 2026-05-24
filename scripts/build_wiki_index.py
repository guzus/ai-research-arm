#!/usr/bin/env python3
"""Generate research/wiki/index.json from the wiki pages + log.

The dashboard's Wiki tab reads this committed JSON instead of parsing pages in
the browser. Generating it in Python — reusing check_wiki's loader, resolver,
and fence-aware link extraction — means there is exactly ONE wikilink language
(slug ∪ aliases, fenced code skipped), not a second, subtly-different parser in
prebuild.mjs. It also keeps the Vercel/prebuild build free of any Python
dependency: prebuild just copies the committed index.json into public/.

Usage:
    uv run python scripts/build_wiki_index.py            # write research/wiki/index.json
    uv run python scripts/build_wiki_index.py --check    # fail (exit 1) if the
                                                         # committed file is stale
    uv run python scripts/build_wiki_index.py --out PATH --root DIR

The output is a pure function of the wiki inputs (no timestamps), so --check is
a deterministic drift gate that CI runs to keep index.json in lockstep with the
pages. The ingest agent regenerates it every run; CI rejects a stale commit.

index.json shape:
    {
      "pages": [
        {slug, title, type, tags, summary, created_at, updated_at,
         file, aliases, outbound, inbound}
      ],
      "resolver": { "<name-or-alias lowercased>": "<slug>" },
      "recent_log": [ {date, op, summary} ]   # newest first
    }
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

import check_wiki as cw

RECENT_LOG_LIMIT = 20


def _isoformat(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, date):
        return value.isoformat()
    return str(value)


def _page_extra_fields(path: Path) -> dict[str, Any]:
    """Re-read a page's frontmatter for fields check_wiki's Page doesn't carry
    (tags, summary, created_at). check_wiki already validated the page, so this
    is a thin metadata read, not a re-validation."""
    text = path.read_text(encoding="utf-8")
    throwaway = cw.Report()
    data, _ = cw._split_frontmatter(text, path, throwaway)
    data = data or {}
    tags = data.get("tags") or []
    if not isinstance(tags, list):
        tags = []
    return {
        "tags": [str(t) for t in tags],
        "summary": str(data.get("summary") or ""),
        "created_at": _isoformat(data.get("created_at")),
    }


def build_index(wiki_dir: Path) -> dict[str, Any]:
    """Load + validate the wiki, then assemble the index document. Raises
    SystemExit(1) loudly if any page fails to load — build_wiki_index runs
    AFTER check_wiki, so an invalid page here is a real (gating) problem."""
    report = cw.Report()
    page_paths = cw.gather_pages(wiki_dir)
    pages: list[cw.Page] = []
    for p in page_paths:
        page = cw.load_page(p, report)
        if page is not None:
            pages.append(page)

    if not report.ok():
        for f in report.failures:
            print(f"FAIL {f.path}: {f.field}: {f.msg}", file=sys.stderr)
        print(
            "\nbuild_wiki_index: pages do not pass validation — run "
            "`uv run python scripts/check_wiki.py` first",
            file=sys.stderr,
        )
        raise SystemExit(1)

    resolver = cw.build_resolver(pages, report)
    if not report.ok():  # resolver collisions
        for f in report.failures:
            print(f"FAIL {f.path}: {f.field}: {f.msg}", file=sys.stderr)
        raise SystemExit(1)

    # Outbound (resolved, deduped, excluding self) + inbound graph.
    by_slug = {p.slug: p for p in pages}
    outbound: dict[str, set[str]] = {p.slug: set() for p in pages}
    inbound: dict[str, set[str]] = {p.slug: set() for p in pages}
    for page in pages:
        for target in page.links:
            tgt = resolver.get(target.lower())
            if tgt and tgt != page.slug and tgt in by_slug:
                outbound[page.slug].add(tgt)
                inbound[tgt].add(page.slug)

    page_docs: list[dict[str, Any]] = []
    for page in sorted(pages, key=lambda p: p.slug):
        extra = _page_extra_fields(page.path)
        page_docs.append(
            {
                "slug": page.slug,
                "title": page.title,
                "type": page.type,
                "tags": extra["tags"],
                "summary": extra["summary"],
                "created_at": extra["created_at"],
                "updated_at": _isoformat(page.updated_at),
                "file": str(page.path.relative_to(wiki_dir)),
                "aliases": list(page.aliases),
                "outbound": sorted(outbound[page.slug]),
                "inbound": sorted(inbound[page.slug]),
            }
        )

    return {
        "pages": page_docs,
        "resolver": {k: resolver[k] for k in sorted(resolver)},
        "recent_log": _recent_log(wiki_dir),
    }


def _recent_log(wiki_dir: Path) -> list[dict[str, str]]:
    """Parse log.md's `## [date] op | summary` entries, newest first, capped."""
    log_path = wiki_dir / "log.md"
    try:
        text = log_path.read_text(encoding="utf-8")
    except OSError:
        return []
    entries: list[dict[str, str]] = []
    for line in text.splitlines():
        m = cw.LOG_LINE_RE.match(line)
        if m:
            entries.append({"date": m.group(1), "op": m.group(2), "summary": m.group(3)})
    entries.reverse()  # log.md is oldest→newest; surface newest first
    return entries[:RECENT_LOG_LIMIT]


def render(index: dict[str, Any]) -> str:
    """Stable serialization: deterministic so --check is a real drift gate."""
    return json.dumps(index, indent=2, ensure_ascii=False) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=None, help="wiki root (default research/wiki)")
    parser.add_argument("--out", default=None, help="output path (default <root>/index.json)")
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if the committed index.json differs from a fresh build (CI drift gate)",
    )
    args = parser.parse_args(argv)

    wiki_dir = Path(args.root) if args.root else cw.WIKI_DIR
    out_path = Path(args.out) if args.out else wiki_dir / "index.json"

    if not wiki_dir.is_dir():
        print(f"no wiki dir at {wiki_dir} — nothing to index", file=sys.stderr)
        return 0

    index = build_index(wiki_dir)
    content = render(index)

    if args.check:
        try:
            existing = out_path.read_text(encoding="utf-8")
        except OSError:
            print(f"FAIL: {out_path} is missing — run `uv run python scripts/build_wiki_index.py`", file=sys.stderr)
            return 1
        if existing != content:
            print(
                f"FAIL: {out_path} is stale — regenerate with "
                f"`uv run python scripts/build_wiki_index.py`",
                file=sys.stderr,
            )
            return 1
        print(f"OK — {out_path} is up to date ({len(index['pages'])} page(s))")
        return 0

    out_path.write_text(content, encoding="utf-8")
    print(f"wrote {out_path} ({len(index['pages'])} page(s), {len(index['resolver'])} resolver keys)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
