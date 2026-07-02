#!/usr/bin/env python3
"""Deterministic fallback writer for the daily arXiv lane.

The model lane (arXiv MCP curator) is still the preferred path, but listing
new submissions is a structured-data problem. When the agent path fails —
provider outage, MCP server unavailable — this script keeps the lane alive by
querying the public arXiv Atom API directly and writing an *uncurated*,
per-category listing of papers submitted in the lookback window.

Contract:
  - Output: research/arxiv/<date>-papers.md (atomic write; replaces any
    unverified partial agent output in the working tree).
  - Zero qualifying papers still writes the file, with an explicit
    "no new papers in window" note — freshness must be honest, never faked.
  - Exit nonzero ONLY when the fetch itself entirely fails (all retries
    exhausted); a successfully-fetched-but-empty window is a healthy result.

Stdlib-only so it runs on both runner tiers with no dependency install.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import os
import re
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ARXIV_API_URL = "https://export.arxiv.org/api/query"
USER_AGENT = "Mozilla/5.0 (compatible; AIResearchBot/1.0; +https://ara.guzus.xyz)"

# Category order is the section order in the output file.
CATEGORIES: tuple[tuple[str, str], ...] = (
    ("cs.AI", "Artificial Intelligence"),
    ("cs.LG", "Machine Learning"),
    ("cs.CL", "Computation and Language"),
    ("cs.CV", "Computer Vision"),
    ("cs.NE", "Neural and Evolutionary Computing"),
)

MAX_AUTHORS = 3
ABSTRACT_MAX_CHARS = 320


@dataclasses.dataclass(frozen=True)
class Paper:
    arxiv_id: str
    title: str
    authors: tuple[str, ...]
    abstract: str
    category: str            # the target category this paper is grouped under
    published_at: dt.datetime | None
    updated_at: dt.datetime | None

    @property
    def abs_url(self) -> str:
        return f"https://arxiv.org/abs/{self.arxiv_id}"

    @property
    def newest_at(self) -> dt.datetime | None:
        stamps = [s for s in (self.published_at, self.updated_at) if s is not None]
        return max(stamps) if stamps else None


def clean_text(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def parse_datetime(value: str | None) -> dt.datetime | None:
    value = clean_text(value)
    if not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def build_query_url(max_results: int) -> str:
    search_query = " OR ".join(f"cat:{cat}" for cat, _ in CATEGORIES)
    params = urllib.parse.urlencode(
        {
            "search_query": search_query,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "start": 0,
            "max_results": max_results,
        }
    )
    return f"{ARXIV_API_URL}?{params}"


def fetch_feed(url: str, *, retries: int = 3, backoff_seconds: float = 5.0) -> bytes:
    """Fetch the Atom feed with bounded retries. Raises RuntimeError when the
    network boundary fails entirely — the caller turns that into exit 1."""
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read()
        except (urllib.error.URLError, urllib.error.HTTPError, OSError, TimeoutError) as exc:
            last_error = exc
            print(f"arXiv fetch attempt {attempt}/{retries} failed: {exc}", file=sys.stderr)
            if attempt < retries:
                time.sleep(backoff_seconds * attempt)
    raise RuntimeError(f"arXiv API fetch failed after {retries} attempts: {last_error}")


def entry_arxiv_id(entry: ET.Element) -> str:
    for child in list(entry):
        if local_name(child.tag) == "id":
            raw = clean_text("".join(child.itertext()))
            # http://arxiv.org/abs/2606.12345v2 -> 2606.12345v2
            return raw.rsplit("/abs/", 1)[-1] if "/abs/" in raw else raw
    return ""


def entry_categories(entry: ET.Element) -> tuple[str, list[str]]:
    """Return (primary_category, all_category_terms) for an Atom entry."""
    primary = ""
    terms: list[str] = []
    for child in list(entry):
        name = local_name(child.tag)
        if name == "primary_category":
            primary = child.get("term") or ""
        elif name == "category":
            term = child.get("term") or ""
            if term:
                terms.append(term)
    return primary, terms


def entry_authors(entry: ET.Element) -> tuple[str, ...]:
    authors: list[str] = []
    for child in list(entry):
        if local_name(child.tag) != "author":
            continue
        for grandchild in list(child):
            if local_name(grandchild.tag) == "name":
                name = clean_text("".join(grandchild.itertext()))
                if name:
                    authors.append(name)
    return tuple(authors)


def entry_child_text(entry: ET.Element, name: str) -> str:
    for child in list(entry):
        if local_name(child.tag) == name:
            return clean_text("".join(child.itertext()))
    return ""


def target_category(primary: str, terms: list[str]) -> str:
    """Group a paper under the first matching target category. The primary
    category wins when it is one of ours; a cross-list (e.g. stat.ML primary,
    cs.LG secondary) falls into the first target term it carries."""
    wanted = [cat for cat, _ in CATEGORIES]
    if primary in wanted:
        return primary
    for cat in wanted:
        if cat in terms:
            return cat
    return ""


def parse_papers(body: bytes) -> list[Paper]:
    root = ET.fromstring(body)
    papers: list[Paper] = []
    for entry in list(root):
        if local_name(entry.tag) != "entry":
            continue
        arxiv_id = entry_arxiv_id(entry)
        title = entry_child_text(entry, "title")
        if not arxiv_id or not title:
            continue
        primary, terms = entry_categories(entry)
        category = target_category(primary, terms)
        if not category:
            continue
        papers.append(
            Paper(
                arxiv_id=arxiv_id,
                title=title,
                authors=entry_authors(entry),
                abstract=entry_child_text(entry, "summary")[:ABSTRACT_MAX_CHARS],
                category=category,
                published_at=parse_datetime(entry_child_text(entry, "published")),
                updated_at=parse_datetime(entry_child_text(entry, "updated")),
            )
        )
    return papers


def filter_window(papers: list[Paper], now: dt.datetime, lookback_hours: int) -> list[Paper]:
    threshold = now - dt.timedelta(hours=lookback_hours)
    ceiling = now + dt.timedelta(minutes=10)
    kept: list[Paper] = []
    for paper in papers:
        newest = paper.newest_at
        if newest is None:
            continue
        if threshold <= newest <= ceiling:
            kept.append(paper)
    return kept


def author_label(authors: tuple[str, ...]) -> str:
    if not authors:
        return "(authors unlisted)"
    shown = ", ".join(authors[:MAX_AUTHORS])
    if len(authors) > MAX_AUTHORS:
        shown += " et al."
    return shown


def abstract_trim(abstract: str) -> str:
    """First 1-2 sentences of the abstract, bounded by ABSTRACT_MAX_CHARS."""
    abstract = clean_text(abstract)
    if not abstract:
        return ""
    sentences = re.split(r"(?<=[.!?])\s+", abstract)
    trimmed = " ".join(sentences[:2]).strip()
    if len(trimmed) > ABSTRACT_MAX_CHARS:
        trimmed = trimmed[: ABSTRACT_MAX_CHARS - 1].rstrip() + "…"
    return trimmed


def markdown_escape(value: str) -> str:
    return value.replace("|", r"\|").replace("\n", " ")


def render(
    date: str,
    now: dt.datetime,
    lookback_hours: int,
    papers: list[Paper],
    max_results: int,
    *,
    truncated: bool = False,
) -> str:
    lines = [
        f"# arXiv AI Research - {date}",
        "",
        "> **Deterministic model-free fallback.** The curator agent was",
        "> unavailable for this run, so this listing was generated mechanically",
        "> by `scripts/deterministic_arxiv_digest.py` from the arXiv Atom API:",
        "> papers in cs.AI / cs.LG / cs.CL / cs.CV / cs.NE submitted or updated",
        f"> in the last {lookback_hours}h (newest ≤{max_results} API results),",
        "> newest first. **Uncurated — no importance ranking, no significance",
        "> filtering.**",
        "",
    ]
    if truncated:
        lines.extend(
            [
                f"> ⚠ **Window truncated:** all {len(papers)} fetched results fall",
                f"> inside the {lookback_hours}h window, so older in-window papers were",
                f"> cut off by the max_results={max_results} cap. This listing covers",
                "> the newest submissions only.",
                "",
            ]
        )
    if not papers:
        lines.extend(
            [
                "_No new papers found in the lookback window. The arXiv API was_",
                "_reachable and returned results, but none were submitted or updated_",
                f"_within the last {lookback_hours} hours (arXiv pauses new listings on_",
                "_weekends and holidays)._",
                "",
            ]
        )
    else:
        by_category: dict[str, list[Paper]] = {}
        for paper in papers:
            by_category.setdefault(paper.category, []).append(paper)
        for cat, cat_label in CATEGORIES:
            cat_papers = by_category.get(cat, [])
            if not cat_papers:
                continue
            cat_papers.sort(
                key=lambda p: p.newest_at or dt.datetime.min.replace(tzinfo=dt.timezone.utc),
                reverse=True,
            )
            lines.extend([f"## {cat} — {cat_label} ({len(cat_papers)})", ""])
            for paper in cat_papers:
                lines.append(
                    f"- **[{markdown_escape(paper.title)}]({paper.abs_url})** — "
                    f"{markdown_escape(author_label(paper.authors))}"
                )
                trimmed = abstract_trim(paper.abstract)
                if trimmed:
                    lines.append(f"  > {markdown_escape(trimmed)}")
                lines.append("")
    lines.extend(
        [
            "---",
            f"*Generated at {now.strftime('%Y-%m-%d %H:%M UTC')} by the deterministic",
            f"arXiv fallback ({len(papers)} paper(s) in window).*",
            "",
        ]
    )
    return "\n".join(lines)


def write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False, prefix=f".{path.name}.", suffix=".tmp"
    ) as handle:
        handle.write(text)
        tmp_path = Path(handle.name)
    os.replace(tmp_path, path)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=Path("research/arxiv"))
    parser.add_argument("--date", required=True, help="Target date, YYYY-MM-DD.")
    parser.add_argument(
        "--lookback-hours",
        type=int,
        default=26,
        help="Keep papers submitted/updated within this many hours (default: 26).",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=400,
        help="max_results for the combined arXiv API query (default: 400 — a"
        " busy weekday exceeds 150 across the five categories, and the render"
        " flags the window as truncated when even this cap saturates).",
    )
    parser.add_argument(
        "--now",
        default=None,
        help="ISO-8601 UTC reference time (default: now). For testing.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    now = parse_datetime(args.now) if args.now else dt.datetime.now(dt.timezone.utc)
    if now is None:
        print(f"error: --now is not a valid ISO-8601 timestamp: {args.now}", file=sys.stderr)
        return 1

    url = build_query_url(args.max_results)
    print(f"Querying arXiv API: {url}")
    try:
        body = fetch_feed(url)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    try:
        papers = parse_papers(body)
    except ET.ParseError as exc:
        print(f"error: arXiv API response is not parseable XML: {exc}", file=sys.stderr)
        return 1

    in_window = filter_window(papers, now, args.lookback_hours)
    # Saturation signal: the API returned a full page AND every result is
    # inside the window — older in-window papers were cut off by the cap.
    truncated = len(papers) >= args.max_results and len(in_window) == len(papers)
    out_path = args.out_dir / f"{args.date}-papers.md"
    write_atomic(
        out_path,
        render(
            args.date,
            now,
            args.lookback_hours,
            in_window,
            args.max_results,
            truncated=truncated,
        ),
    )
    print(
        f"Wrote {out_path}: {len(in_window)} of {len(papers)} fetched paper(s) "
        f"within the {args.lookback_hours}h window"
        + (" — WINDOW TRUNCATED by max_results cap" if truncated else "")
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
