#!/usr/bin/env python3
"""Deterministic fallback composer for the daily digest lane.

The model lane (digest synthesizer agent) is still the preferred path — it
ranks, cross-references, and writes prose. When it fails or produces
sub-floor output (see scripts/check_digest_content.py), this script keeps the
digest lane — and its workflow_run consumers (wiki-ingest, front-page) —
alive by composing the digest MECHANICALLY from the day's committed lane
artifacts.

Composition contract (deliberately dumb, never creative):
  - For each source lane, find the most recent artifact dated today or
    yesterday (the digest runs at 00:00 UTC, so yesterday's files are the
    freshest complete data).
  - Extract the top bullet / heading / table-row lines VERBATIM (capped per
    lane) and emit them under a per-source `## ` section with the source path
    attributed. NEVER invent, rewrite, or summarize content.
  - Lanes with no artifact (or no extractable items) are skipped with an
    explicit note in the Sources Consulted footer — missing coverage is
    stated, not papered over.
  - A banner marks the file as the deterministic model-free fallback.

Also writes the Telegram summary file (--summary-out) so the digest's
notification/audio steps keep working on fallback days.

Stdlib-only; atomic writes per Load-bearing rule 8.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import glob
import os
import re
import sys
import tempfile
from pathlib import Path

BULLET_RE = re.compile(r"^[-•]\s+\S")
HEADING_RE = re.compile(r"^###\s+\S")
TABLE_SEPARATOR_RE = re.compile(r"^\|[\s:|-]+\|$")
MAX_LINE_CHARS = 300
SUMMARY_MAX_CHARS = 800


@dataclasses.dataclass(frozen=True)
class LaneSource:
    key: str
    label: str
    pattern: str            # glob relative to the research dir, with {date}
    modes: tuple[str, ...]  # extractor order: "bullets" | "headings" | "table"


# Section order in the fallback digest. Patterns mirror each lane's real
# artifact naming (see CLAUDE.md "Output Locations").
LANES: tuple[LaneSource, ...] = (
    # The twitter lane's .md is an HTML-article render; the plain-text
    # Telegram summaries are the extractable artifact. Several exist per day
    # (one per 3h cycle) — the latest non-empty cycle wins. The
    # [0-9][0-9]h class pins the PRIMARY lane's `<date>-twitter-<HH>h-` files
    # and excludes the comparison lanes (`-twitter-deepseek-<HH>h-` etc.).
    LaneSource(
        "twitter",
        "Twitter/X",
        "summaries/{date}-twitter-[0-9][0-9]h-summary.txt",
        ("bullets",),
    ),
    LaneSource("rss", "RSS / Official Announcements", "rss/{date}.md", ("bullets",)),
    LaneSource("hn", "Hacker News", "community/{date}-hn.md", ("bullets", "table")),
    LaneSource("reddit", "Reddit", "community/{date}-reddit.md", ("table", "bullets")),
    LaneSource("blogs", "Expert Blogs", "blogs/{date}.md", ("headings",)),
    LaneSource("bluesky", "Bluesky", "bluesky/{date}.md", ("bullets",)),
    LaneSource("arxiv", "arXiv Papers", "arxiv/{date}-papers.md", ("headings", "bullets")),
    LaneSource("youtube", "YouTube", "youtube/{date}.md", ("headings",)),
)


@dataclasses.dataclass(frozen=True)
class LaneExtract:
    lane: LaneSource
    artifact: str | None    # path relative to the research dir
    lines: tuple[str, ...]  # rendered "- ..." excerpt lines
    note: str               # only set when artifact is missing/empty


def clamp_line(line: str) -> str:
    line = re.sub(r"\s+", " ", line).strip()
    if len(line) > MAX_LINE_CHARS:
        line = line[: MAX_LINE_CHARS - 1].rstrip() + "…"
    return line


def extract_bullets(text: str, cap: int) -> list[str]:
    """Top-level `- ` / `• ` lines, verbatim (normalized to `- `). Bullets
    that are pure italic status notes (`- _No new updates this hour._`) are
    lane bookkeeping, not content — the Sources Consulted footer already
    carries lane status, so they are skipped."""
    out: list[str] = []
    for raw in text.splitlines():
        if len(out) >= cap:
            break
        if not BULLET_RE.match(raw):
            continue
        body = raw[1:].strip()
        if re.fullmatch(r"_[^_]*_", body):
            continue
        out.append(clamp_line(f"- {body}"))
    return out


def extract_headings(text: str, cap: int) -> list[str]:
    """`### ` headings (item titles in blogs/arxiv/youtube lanes), as bullets."""
    out: list[str] = []
    for raw in text.splitlines():
        if len(out) >= cap:
            break
        if not HEADING_RE.match(raw):
            continue
        out.append(clamp_line(f"- {raw[4:].strip()}"))
    return out


def extract_table(text: str, cap: int) -> list[str]:
    """Markdown table body rows as `- first-cell — last-cell` bullets.
    Header rows (the row preceding a `|---|` separator) and separator rows
    are dropped."""
    out: list[str] = []
    previous_was_row = False
    rows: list[list[str]] = []
    for raw in text.splitlines():
        stripped = raw.strip()
        if not (stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 2):
            previous_was_row = False
            continue
        if TABLE_SEPARATOR_RE.match(stripped):
            if previous_was_row and rows:
                rows.pop()  # the row before a separator is the header
            previous_was_row = False
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        cells = [cell for cell in cells if cell]
        if len(cells) >= 2:
            rows.append(cells)
            previous_was_row = True
    for cells in rows[:cap]:
        out.append(clamp_line(f"- {cells[0]} — {cells[-1]}"))
    return out


EXTRACTORS = {
    "bullets": extract_bullets,
    "headings": extract_headings,
    "table": extract_table,
}


def candidate_dates(date: str) -> list[str]:
    """[today, yesterday] — the digest window. Most recent date wins."""
    target = dt.date.fromisoformat(date)
    return [date, (target - dt.timedelta(days=1)).isoformat()]


def extract_lane(research_dir: Path, lane: LaneSource, dates: list[str], cap: int) -> LaneExtract:
    """Walk the window newest-date-first and return the first artifact that
    yields extractable lines. An artifact that exists but has no items (e.g.
    a "0 posts today" blogs file) falls through to the previous date instead
    of shadowing it — the attribution line always names the file actually
    excerpted, so the provenance stays honest."""
    empty_artifacts: list[str] = []
    for candidate in dates:
        pattern = str(research_dir / lane.pattern.format(date=candidate))
        matches = sorted(p for p in glob.glob(pattern) if os.path.isfile(p))
        if not matches:
            continue
        # Several sub-daily artifacts can exist for one date. Walk newest to
        # oldest so a machine-only/empty no_update summary does not shadow an
        # earlier same-day cycle that contains the actual public signal.
        for match in reversed(matches):
            artifact = Path(match)
            relative = artifact.relative_to(research_dir).as_posix()
            try:
                text = artifact.read_text(encoding="utf-8")
            except OSError as exc:
                empty_artifacts.append(f"{relative} (unreadable: {exc})")
                continue
            lines: list[str] = []
            for mode in lane.modes:
                if len(lines) >= cap:
                    break
                for line in EXTRACTORS[mode](text, cap - len(lines)):
                    if line not in lines:
                        lines.append(line)
            if lines:
                return LaneExtract(lane, relative, tuple(lines), "")
            empty_artifacts.append(relative)
    if empty_artifacts:
        return LaneExtract(
            lane, None, (),
            "artifact(s) had no extractable items: " + ", ".join(empty_artifacts),
        )
    window = " or ".join(dates)
    return LaneExtract(lane, None, (), f"no artifact for {window} — lane skipped")


def lane_leads(extracts: list[LaneExtract]) -> list[tuple[str, str]]:
    """(lane label, first excerpt body) for each covered lane — the digest's
    best available stand-in for a lead-story list. Shared by the Executive
    Summary section and the Telegram summary."""
    leads: list[tuple[str, str]] = []
    for extract in extracts:
        if extract.lines:
            leads.append((extract.lane.label, extract.lines[0][2:]))
    return leads


def render_digest(date: str, now: dt.datetime, extracts: list[LaneExtract]) -> str:
    lines = [
        f"# AI Daily Digest - {date}",
        "",
        "> **Deterministic fallback digest.** The model synthesis path was",
        "> unavailable (or produced sub-floor output) for this run, so this",
        "> digest was composed mechanically by",
        "> `scripts/deterministic_daily_digest.py`: verbatim top excerpts from",
        "> each committed lane artifact — **no ranking, no cross-source",
        "> synthesis, no external search**. Treat coverage as raw and uncurated.",
        "",
    ]
    # Canonical `## Executive Summary` section: the front-page renderer
    # (scripts/render_front_page.mjs) builds its masthead lead + deck from
    # this section's bullets, and when it is absent falls back to the
    # digest's first paragraph — the raw `# ` title line. One verbatim top
    # excerpt per covered lane, lane-labelled — still zero synthesis.
    leads = lane_leads(extracts)
    if leads:
        lines.extend(
            [
                "## Executive Summary",
                "",
                "_Top verbatim excerpt from each covered lane (no editorial",
                "ranking — see the fallback banner above):_",
                "",
                *[f"- **{label}:** {body}" for label, body in leads],
                "",
            ]
        )
    for extract in extracts:
        if not extract.lines:
            continue
        lines.extend(
            [
                f"## {extract.lane.label}",
                "",
                f"_Verbatim excerpts from `research/{extract.artifact}`:_",
                "",
                *extract.lines,
                "",
            ]
        )
    lines.extend(["---", "", "## Sources Consulted", ""])
    for extract in extracts:
        if extract.lines:
            lines.append(
                f"- {extract.lane.label}: `research/{extract.artifact}` "
                f"({len(extract.lines)} excerpt(s))"
            )
        else:
            lines.append(f"- {extract.lane.label}: {extract.note}")
    lines.extend(
        [
            "",
            f"*Generated at {now.strftime('%Y-%m-%d %H:%M UTC')} by the deterministic",
            "digest fallback (`scripts/deterministic_daily_digest.py`).*",
            "",
        ]
    )
    return "\n".join(lines)


def strip_markdown(line: str) -> str:
    """De-markdown one excerpt bullet for the plain-text Telegram summary."""
    line = re.sub(r"^-\s+", "", line)
    line = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", line)  # [text](url) -> text
    line = line.replace("**", "").replace("`", "")
    return line.strip()


def render_summary(date: str, extracts: list[LaneExtract], *, max_stories: int = 5) -> str:
    stories: list[str] = []
    for label, body in lane_leads(extracts)[:max_stories]:
        headline = strip_markdown(body)
        if len(headline) > 100:
            headline = headline[:99].rstrip() + "…"
        stories.append(f"• [{label}] {headline}")
    covered = sum(1 for e in extracts if e.lines)
    missing = [e.lane.label for e in extracts if not e.lines]
    parts = [
        f"Daily AI Digest - {date} (deterministic fallback)",
        "",
        "TOP OF EACH LANE:",
        *(stories or ["• (no lane artifacts found in window)"]),
        "",
        f"SOURCES: {covered}/{len(extracts)} lanes had data"
        + (f"; missing: {', '.join(missing)}" if missing else ""),
        "",
        "Verbatim, unranked lane excerpts. Full digest on GitHub.",
    ]
    text = "\n".join(parts)
    if len(text) > SUMMARY_MAX_CHARS:
        text = text[: SUMMARY_MAX_CHARS - 1].rstrip() + "…"
    return text + "\n"


def write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False, prefix=f".{path.name}.", suffix=".tmp"
    ) as handle:
        handle.write(text)
        tmp_path = Path(handle.name)
    os.replace(tmp_path, path)


def compose(
    research_dir: Path,
    date: str,
    out_path: Path,
    summary_path: Path | None,
    *,
    max_per_lane: int = 8,
    now: dt.datetime | None = None,
) -> list[LaneExtract]:
    now = now or dt.datetime.now(dt.timezone.utc)
    dates = candidate_dates(date)
    extracts = [extract_lane(research_dir, lane, dates, max_per_lane) for lane in LANES]
    write_atomic(out_path, render_digest(date, now, extracts))
    if summary_path is not None:
        write_atomic(summary_path, render_summary(date, extracts))
    return extracts


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--research-dir", type=Path, default=Path("research"))
    parser.add_argument("--date", required=True, help="Digest date, YYYY-MM-DD.")
    parser.add_argument("--out", type=Path, required=True, help="Digest output path.")
    parser.add_argument(
        "--summary-out",
        type=Path,
        default=None,
        help="Optional Telegram summary output path.",
    )
    parser.add_argument(
        "--max-per-lane",
        type=int,
        default=8,
        help="Excerpt cap per lane (default: 8).",
    )
    parser.add_argument(
        "--now",
        default=None,
        help="ISO-8601 UTC timestamp for the footer (default: now). For testing.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    now: dt.datetime | None = None
    if args.now:
        try:
            now = dt.datetime.fromisoformat(args.now.replace("Z", "+00:00"))
        except ValueError:
            print(f"error: --now is not a valid ISO-8601 timestamp: {args.now}", file=sys.stderr)
            return 1
        if now.tzinfo is None:
            now = now.replace(tzinfo=dt.timezone.utc)
    try:
        dt.date.fromisoformat(args.date)
    except ValueError:
        print(f"error: --date is not a valid YYYY-MM-DD date: {args.date}", file=sys.stderr)
        return 1

    extracts = compose(
        args.research_dir,
        args.date,
        args.out,
        args.summary_out,
        max_per_lane=args.max_per_lane,
        now=now,
    )
    covered = sum(1 for e in extracts if e.lines)
    print(f"Wrote {args.out}: {covered}/{len(extracts)} lane(s) had extractable data")
    for extract in extracts:
        status = f"{len(extract.lines)} excerpt(s) from research/{extract.artifact}" if extract.lines else extract.note
        print(f"  - {extract.lane.label}: {status}")
    if args.summary_out is not None:
        print(f"Wrote {args.summary_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
