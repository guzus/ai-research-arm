#!/usr/bin/env python3
"""Per-run content floor for the daily digest artifact.

Closes the hole scripts/check_lane_content.py explicitly scopes out: that
advisory watchdog inspects the *latest artifact on disk* across all lanes and
never fails a job, so "the agent committed the literal prompt template and
the run stayed green" slips straight through it. This checker is the
workflow-time HARD gate on one specific digest file — daily-digest.yml runs
it right after the synthesis agent and routes to the deterministic fallback
composer (scripts/deterministic_daily_digest.py) when it fails.

Three independent checks, all of which must pass:
  1. Byte floor (--min-bytes). Calibration: the smallest healthy agent digest
     in the full git history is 8,410 bytes (2026-02-04); the smallest in the
     last 30 days is 9,968 bytes. The default floor of 4,000 sits ~52% below
     the all-time healthy minimum (no false positives on quiet days) and
     ~2.5x above the raw unexpanded prompt template (~1.6KB), so a template
     shell can never clear it.
  2. Section floor (--min-sections, default 3 `## ` headings). Healthy agent
     digests carry 9-11; the deterministic fallback emits one per covered
     lane plus Sources Consulted.
  3. Placeholder scan: literal unexpanded template fragments from the digest
     prompt (e.g. `[3-5 bullet`, `[count]`, `[Headline 1]`). Verified against
     every committed digest in history — zero matches on healthy output.

Exit 0 = the digest clears the floor; exit 1 = fall back. Stdlib-only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SECTION_RE = re.compile(r"^## ", re.MULTILINE)

# Literal substrings that only appear in an UNexpanded digest prompt template.
# Keep these distinctive: generic bracket text (e.g. markdown links) must
# never match. Sourced from the FORMAT block in daily-digest.yml's prompts.
DEFAULT_PLACEHOLDERS: tuple[str, ...] = (
    "[3-5 bullet",
    "[Major announcements from companies]",
    "[New models, versions, capabilities]",
    "[Top papers from arXiv",
    "[What HN and Reddit are discussing]",
    "[Investment rounds, acquisitions, partnerships]",
    "[Government actions, policy changes]",
    "[New tools, frameworks, tutorials",
    "[Most insightful tweet or comment]",
    "[count]",
    "[Headline 1]",
    "[Headline 2]",
    "[Key metrics from today]",
    "[Top community topic]",
    "[Name]",
    "[names]",
)


def check_digest(
    text: str,
    *,
    min_bytes: int,
    min_sections: int,
    placeholders: tuple[str, ...] = DEFAULT_PLACEHOLDERS,
) -> list[str]:
    """Pure check over the digest text. Returns a list of failure reasons
    (empty = the digest clears the floor). IO-free for unit testing."""
    failures: list[str] = []

    size = len(text.encode("utf-8"))
    if size < min_bytes:
        failures.append(f"byte floor: {size}B < required {min_bytes}B")

    sections = len(SECTION_RE.findall(text))
    if sections < min_sections:
        failures.append(f"section floor: {sections} `## ` heading(s) < required {min_sections}")

    found = [p for p in placeholders if p in text]
    if found:
        failures.append(
            "unexpanded template placeholder(s) present: " + ", ".join(repr(p) for p in found)
        )

    return failures


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path, required=True, help="Digest file to check.")
    parser.add_argument(
        "--min-bytes",
        type=int,
        default=4000,
        help="Minimum size in bytes (default: 4000; see calibration note in the docstring).",
    )
    parser.add_argument(
        "--min-sections",
        type=int,
        default=3,
        help="Minimum number of `## ` section headings (default: 3).",
    )
    parser.add_argument(
        "--placeholder",
        action="append",
        default=[],
        help="Extra literal placeholder substring to reject (repeatable).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    if not args.file.is_file():
        print(f"FLOOR FAIL {args.file}: file does not exist", file=sys.stderr)
        return 1
    try:
        text = args.file.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"FLOOR FAIL {args.file}: unreadable: {exc}", file=sys.stderr)
        return 1

    placeholders = DEFAULT_PLACEHOLDERS + tuple(args.placeholder)
    failures = check_digest(
        text,
        min_bytes=args.min_bytes,
        min_sections=args.min_sections,
        placeholders=placeholders,
    )
    if failures:
        for failure in failures:
            print(f"FLOOR FAIL {args.file}: {failure}", file=sys.stderr)
        return 1

    size = len(text.encode("utf-8"))
    sections = len(SECTION_RE.findall(text))
    print(f"FLOOR OK {args.file}: {size}B, {sections} section(s), no placeholders")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
