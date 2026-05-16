#!/usr/bin/env python3
"""Compile-check a generative research article body without committing.

Runs the same validation rules write_generative_research.py enforces at
commit time — tag allowlist, ara-* exact-match class allowlist parsed
from COMPONENTS.md (modifier suffixes allowed), size cap, no inline
style/script/JS handlers, opening/closing <article> structure.

Optional design-system enforcement flags (off by default so check
stays additive):
  --diversity-min N   fail if fewer than N distinct visualization
                      primitives are used. Counts ara-line-chart,
                      ara-donut, ara-slope, ara-stack-bar,
                      ara-stack-rows, ara-bars, ara-rank-list,
                      ara-compare, ara-iso, ara-sparkline,
                      ara-timeline, ara-kv. ara-table and ara-callout
                      are NOT counted — they're the safe defaults.
  --callout-max M     fail if more than M ara-callout blocks. Use to
                      stop agents from reaching for callouts as
                      cosmetic emphasis (a common failure mode).
  --strict-shape      WARN (not fail) when the article has 5+
                      standalone percentages in prose but no
                      distribution viz (donut, stack-bar, bars,
                      rank-list). This catches the "179 percentages,
                      zero donuts" pattern the corpus audit surfaced.

Exit status:
  0  — body is valid; safe to commit
  1  — body fails validation; the error is printed to stderr with
        specific fixes (e.g. "undocumented class ara-references → did
        you mean: ara-eyebrow")
  2  — argv error / file missing

Usage:
  python3 scripts/check_generative_research.py /tmp/gen-research-body.html
  python3 scripts/check_generative_research.py - < body.html     # stdin
  python3 scripts/check_generative_research.py path --kind standalone
  python3 scripts/check_generative_research.py path --diversity-min 3 --callout-max 5

The agent loop in the workflow / local skill: write the body, run this
check, fix anything it reports, re-check, and only then call the real
writer to commit. Deterministic — no agent self-validation needed.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Reuse the writer's validator so this script and the commit-time check
# stay in lockstep — if one accepts a body, so does the other.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from write_generative_research import (  # noqa: E402
    KIND_FRAGMENT,
    KINDS,
    detect_dsl,
    read_body,
    validate_body,
)
from compile_ara import AraSyntaxError, compile_source  # noqa: E402

# Component classification, keep in lockstep with ARA_DSL.md / COMPONENTS.md.
VIZ_PRIMITIVES = frozenset([
    "ara-line-chart", "ara-donut", "ara-slope",
    "ara-stack-bar", "ara-stack-rows",
    "ara-bars", "ara-rank-list", "ara-compare",
    "ara-iso", "ara-sparkline", "ara-timeline", "ara-kv",
])
DISTRIBUTION_VIZ = frozenset([
    "ara-donut", "ara-stack-bar", "ara-stack-rows",
    "ara-bars", "ara-rank-list",
])
FALLBACK_PRIMITIVES = frozenset(["ara-table", "ara-callout", "ara-quote"])


def count_classes(body_html: str) -> dict[str, int]:
    """Return a {class_name: count} map of every ara-* class in the
    article's HTML output, after compile."""
    counts: dict[str, int] = {}
    for cls in re.findall(r'class="(ara-[a-z0-9-]+(?:--[a-z0-9-]+)?)', body_html):
        counts[cls] = counts.get(cls, 0) + 1
    return counts


def count_standalone_percentages(body_html: str) -> int:
    """How many `\\d+%` tokens appear in flow text (not inside an
    `ara-bar-value` or `ara-stat-value`, where they're already
    visualized)."""
    text = re.sub(r'<(span|div)[^>]*class="ara-(bar-value|stat-value|rank-value|compare-value)"[^>]*>.*?</\1>',
                  ' ', body_html, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    return len(re.findall(r"\b\d+(?:\.\d+)?\s?%", text))


def enforce_design(body_html: str, args: argparse.Namespace) -> list[str]:
    """Return a list of error messages. Empty list = pass."""
    errors: list[str] = []
    counts = count_classes(body_html)

    viz_used = {c for c in counts if c in VIZ_PRIMITIVES}
    if args.diversity_min is not None and len(viz_used) < args.diversity_min:
        sample = sorted(VIZ_PRIMITIVES - viz_used)[:6]
        errors.append(
            f"design: only {len(viz_used)} distinct viz primitive(s) used "
            f"({sorted(viz_used) or 'none'}), need ≥ {args.diversity_min}. "
            f"Reach for one of: {', '.join(sample)}."
        )

    callout_count = counts.get("ara-callout", 0)
    if args.callout_max is not None and callout_count > args.callout_max:
        errors.append(
            f"design: {callout_count} ara-callout blocks, max is "
            f"{args.callout_max}. Callouts are for thesis breaks / risk "
            f"flags only — most of these belong as inline prose or as "
            f"a structured viz (donut, stack-bar, kv)."
        )
    return errors


def soft_warnings(body_html: str) -> list[str]:
    """Non-fatal heuristics that nag at common design-system anti-
    patterns surfaced by the corpus audit. Printed to stderr but
    don't change exit status."""
    warns: list[str] = []
    counts = count_classes(body_html)
    pct = count_standalone_percentages(body_html)
    distribution_used = any(counts.get(c, 0) > 0 for c in DISTRIBUTION_VIZ)
    if pct >= 5 and not distribution_used:
        warns.append(
            f"warn: article cites {pct} standalone percentages in prose "
            f"but uses ZERO distribution viz (donut / stack-bar / bars / "
            f"rank-list). The data shape supports a viz; consider whether "
            f"a `:::donut` or `:::stack-bar` would replace prose."
        )
    callout_count = counts.get("ara-callout", 0)
    viz_count = sum(counts.get(c, 0) for c in VIZ_PRIMITIVES)
    if callout_count >= 5 and viz_count <= 1:
        warns.append(
            f"warn: {callout_count} callouts but only {viz_count} viz "
            f"primitive(s) — callouts are doing the visual heavy lifting. "
            f"That usually means a few of them want to be `:::kv` or `:::stats`."
        )
    return warns


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "body_path",
        help="path to the article body (use '-' to read from stdin)",
    )
    p.add_argument(
        "--kind",
        default=KIND_FRAGMENT,
        choices=KINDS,
        help="fragment (default) or standalone",
    )
    p.add_argument(
        "--diversity-min",
        type=int,
        default=None,
        help="fail if fewer than N distinct viz primitives are used",
    )
    p.add_argument(
        "--callout-max",
        type=int,
        default=None,
        help="fail if more than M ara-callout blocks are used",
    )
    p.add_argument(
        "--strict-shape",
        action="store_true",
        help="enable soft-warning heuristics (percentages-without-donut, etc.)",
    )
    args = p.parse_args(argv)

    if args.body_path != "-" and not Path(args.body_path).exists():
        print(f"check: body file not found: {args.body_path}", file=sys.stderr)
        return 2

    try:
        raw = read_body(args.body_path)
    except OSError as e:
        print(f"check: read failed: {e}", file=sys.stderr)
        return 2

    is_dsl = detect_dsl(args.body_path, raw)
    if is_dsl:
        try:
            body = compile_source(raw)
        except AraSyntaxError as e:
            print(f"check: DSL compile failed: {e}", file=sys.stderr)
            return 1
    else:
        body = raw

    try:
        validate_body(body, args.kind)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 1

    # Design-system gates (only active when explicitly opted in).
    if args.kind == KIND_FRAGMENT and (
        args.diversity_min is not None or args.callout_max is not None
    ):
        errors = enforce_design(body, args)
        if errors:
            for line in errors:
                print(line, file=sys.stderr)
            print(
                "Design gates failed. Either restructure the article to "
                "use more primitives, or relax the threshold for this run.",
                file=sys.stderr,
            )
            return 1

    # Soft warnings (don't change exit status; nudge the agent toward
    # the design system without blocking commits).
    if args.kind == KIND_FRAGMENT and args.strict_shape:
        for line in soft_warnings(body):
            print(line, file=sys.stderr)

    size = len(body.encode("utf-8"))
    src = "compiled from DSL" if is_dsl else "raw HTML"
    print(
        f"check: OK ({size:,} bytes, kind={args.kind}, {src}). Safe to commit.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
