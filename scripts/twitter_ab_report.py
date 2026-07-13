#!/usr/bin/env python3
"""Render the Twitter model A/B eval report from metrics.json.

Used by .github/workflows/twitter-model-ab.yml after
scripts/twitter_ab_metrics.py. STDLIB ONLY. Reads the collected (and, when
the judge ran, finalized) metrics.json and writes the human report
`research/eval/twitter-ab/<date>-report.md` plus an optional one-line
telemetry summary. Missing/partial legs and a skipped judge render honestly
instead of crashing.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from twitter_ab_metrics import atomic_write_text  # noqa: E402

MECHANICAL_ROWS = (
    ("outcome", ("outcome",)),
    ("effective backend", ("backend", "effective")),
    ("served model", ("backend", "served_model")),
    ("is_error", ("agent", "is_error")),
    ("turns", ("agent", "num_turns")),
    ("permission denials", ("agent", "permission_denials_count")),
    ("cost (USD)", ("agent", "total_cost_usd")),
    ("wall time (s)", ("wall_time_seconds",)),
    ("required files written", ("artifacts", "required_written")),
    ("digest written", ("artifacts", "digest")),
    ("format valid", ("format", "valid")),
    ("status", ("format", "status")),
    ("public_items (status)", ("format", "public_items")),
    ("counted public items", ("format", "counted_public_items")),
    ("story cards", ("format", "story_cards")),
    ("headline alerts", ("format", "headline_count")),
    ("input sha matches snapshot", ("input_integrity", "matches_snapshot")),
    ("input unchanged during leg", ("input_integrity", "unchanged_during_leg")),
    ("committed output", ("commits", "committed")),
)


def dig(data: dict, path: tuple[str, ...]):
    node = data
    for key in path:
        if not isinstance(node, dict):
            return None
        node = node.get(key)
    return node


def fmt(value) -> str:
    if value is None:
        return "—"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, float):
        return f"{value:.4f}".rstrip("0").rstrip(".")
    return str(value)


def short_model(leg_data: dict) -> str:
    model = dig(leg_data, ("backend", "served_model")) or "?"
    return str(model)


def render(metrics: dict) -> str:
    legs: dict = metrics.get("legs") or {}
    leg_names = list(legs)
    contamination = metrics.get("contamination") or {}
    judge = metrics.get("judge")

    lines: list[str] = []
    lines.append(f"# Twitter Model A/B Eval — {metrics.get('date', '?')}")
    lines.append("")
    lines.append(
        f"Run `{metrics.get('run_id', '?')}` (attempt {metrics.get('run_attempt', '?')}), "
        f"cycle `{metrics.get('hour', '?')}`, generated {metrics.get('generated_at', '?')}. "
        "Design + how to read this report: `docs/twitter-model-ab.md`."
    )
    lines.append("")

    # ── contamination banner ──
    if contamination.get("contaminated"):
        lines.append("> [!CAUTION]")
        lines.append(
            "> **CONTAMINATED RUN — a parity guard tripped; do not read this as a model comparison.**"
        )
        for reason in contamination.get("reasons", []):
            lines.append(f"> - `{reason}`")
        lines.append("")
    if contamination.get("sandbox_suspect"):
        lines.append("> [!WARNING]")
        lines.append(
            "> **sandbox-suspect** — at least one leg hit permission denials; "
            "tool friction may have depressed that leg's output independently of model quality."
        )
        lines.append("")
    if not contamination.get("contaminated") and not contamination.get("sandbox_suspect"):
        lines.append("Parity guards: clean (no backend/model/input mismatch, no permission denials).")
        lines.append("")

    # ── shared input ──
    input_block = metrics.get("input") or {}
    lines.append("## Shared input snapshot")
    lines.append("")
    lines.append(f"- `all.json` sha256: `{input_block.get('all_json_sha256') or '?'}`")
    lines.append(f"- staged-input manifest sha256: `{input_block.get('manifest_sha256') or '?'}`")
    lines.append(f"- total tweets: {fmt(input_block.get('total_tweets'))}")
    parity = metrics.get("parity") or {}
    if parity.get("normalized_prompt_sha256"):
        lines.append(
            "- normalized prompt sha256 (identical across legs after leg-dir "
            f"substitution): `{parity['normalized_prompt_sha256']}`"
        )
    lines.append("")

    # ── mechanical table ──
    lines.append("## Mechanical metrics")
    lines.append("")
    if leg_names:
        header = "| metric | " + " | ".join(
            f"`{leg}` ({short_model(legs[leg])})" for leg in leg_names
        ) + " |"
        lines.append(header)
        lines.append("|---|" + "---|" * len(leg_names))
        for label, path in MECHANICAL_ROWS:
            row = [fmt(dig(legs[leg], path)) for leg in leg_names]
            lines.append(f"| {label} | " + " | ".join(row) + " |")
        lines.append("")
        for leg in leg_names:
            flags = legs[leg].get("flags") or []
            if flags:
                lines.append(f"- `{leg}` flags: " + ", ".join(f"`{f}`" for f in flags))
            error = dig(legs[leg], ("format", "error"))
            if error:
                lines.append(f"- `{leg}` format error: {error}")
        lines.append("")
    else:
        lines.append("_No legs ran._")
        lines.append("")

    # ── judge ──
    lines.append("## Blinded judge (claude-opus-4-8, position-swapped x2)")
    lines.append("")
    if judge and judge.get("passes_parsed", 0) > 0:
        per_leg = judge.get("per_leg") or {}
        criteria = sorted(
            {c for scores in per_leg.values() for c in (scores.get("criteria_avg") or {})}
        )
        lines.append("| leg | " + " | ".join(criteria + ["overall"]) + " |")
        lines.append("|---|" + "---|" * (len(criteria) + 1))
        for leg, scores in per_leg.items():
            criteria_avg = scores.get("criteria_avg") or {}
            row = [fmt(criteria_avg.get(c)) for c in criteria]
            row.append(fmt(scores.get("overall_avg")))
            lines.append(f"| `{leg}` | " + " | ".join(row) + " |")
        lines.append("")
        lines.append(
            f"- passes parsed: {judge.get('passes_parsed')}/2 "
            "(pass 2 sees the same briefs with A/B positions swapped)"
        )
        lines.append(f"- **final preference: `{judge.get('final_preference')}`**")
        if judge.get("final_preference") == "split":
            lines.append(
                "- `split` = the two position-swapped passes disagreed; treat this run as no-decision."
            )
        lines.append(f"- de-blinded verdict detail: `{judge.get('verdict_file')}`")
    else:
        reason = metrics.get("judge_skip_reason") or "verdicts missing/unparseable"
        lines.append(f"_Judge did not score this run: {reason}._")
    lines.append("")

    # ── allowed asymmetries ──
    asymmetries = parity.get("allowed_asymmetries") or []
    if asymmetries:
        lines.append("## Allowed config asymmetries")
        lines.append("")
        for item in asymmetries:
            lines.append(f"- {item}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def summary_line(metrics: dict) -> str:
    legs: dict = metrics.get("legs") or {}
    judge = metrics.get("judge") or {}
    contamination = metrics.get("contamination") or {}
    per_leg = judge.get("per_leg") or {}

    def leg_bit(leg: str) -> str:
        overall = (per_leg.get(leg) or {}).get("overall_avg")
        model = short_model(legs.get(leg, {}))
        return f"{model} {overall if overall is not None else 'n/a'}"

    score_part = " vs ".join(leg_bit(leg) for leg in legs) if legs else "no legs"
    pref = judge.get("final_preference") or "none"
    if contamination.get("contaminated"):
        health = "CONTAMINATED"
    elif contamination.get("sandbox_suspect"):
        health = "sandbox-suspect"
    else:
        health = "clean"
    return f"AB {metrics.get('date', '?')}: {score_part}, pref={pref}, {health}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metrics", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--summary-out", default="",
                        help="optional file for the one-line hooker summary")
    args = parser.parse_args(argv)

    try:
        metrics = json.loads(Path(args.metrics).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"::error::cannot read metrics {args.metrics}: {exc}", file=sys.stderr)
        return 1

    atomic_write_text(Path(args.out), render(metrics))
    line = summary_line(metrics)
    if args.summary_out:
        atomic_write_text(Path(args.summary_out), line + "\n")
    print(f"report written: {args.out}")
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
