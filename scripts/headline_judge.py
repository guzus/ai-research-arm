#!/usr/bin/env python3
"""Agent-in-the-loop final gate for the Twitter headline-alert dedupe.

The deterministic check in ``dedupe_headline_alerts.py`` suppresses exact,
same-source, and high-overlap cross-source duplicates. Its one irreducible
residual is the *contested band* just below the cross-source floor: headlines
that share a lot of vocabulary with a recently-alerted story but score below
``CROSS_SOURCE_JACCARD_THRESHOLD`` (0.5). Calibration on the real ledger shows
that band (``[0.35, 0.50)`` Jaccard, >= 3 shared tokens) is roughly half true
duplicates that leaked (same event, different account, paraphrased) and half
genuinely-distinct items that merely share vocabulary -- "MICRON CROSSES $900B"
vs "SK HYNIX CROSSES $900B" (same metric, different subject), running-counter
progressions, appended-fact follow-ups. Token overlap cannot tell those apart;
that separation is a semantic judgment, which is what the LLM gate is for.

This module is the deterministic half of that gate -- two subcommands that
bracket one model call, so the nondeterminism lives only in the workflow's
Haiku step and everything here stays unit-testable:

  shortlist  to-send survivors + history -> the contested-band items, each with
             its <= 5 most-similar prior alerts, for the judge to rule on.
  apply      to-send survivors + judge verdicts -> survivors minus the items the
             judge confirmed (HIGH confidence) are duplicates, plus an audit
             record of every suppression.

Safety contract (the gate enforces immediately, with no shadow phase):
  * The judge can only turn a would-be SEND into a SUPPRESS -- never the reverse,
    and never within the deterministic layers' exact/same-URL/high-overlap calls.
  * A duplicate is dropped ONLY on an explicit HIGH-confidence "duplicate" verdict.
    Default-keep: any missing/low/medium verdict, or a missing/malformed verdicts
    file, leaves the headline in the send set (fail OPEN -- never silently eat a
    real alert on a parse bug or model hiccup).
  * Verdicts are matched to headlines by URL, not array position, so a reordered
    or partial model response can't misattribute a suppression.

Full contract + flow diagrams: docs/headline-dedupe.md
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Reuse the exact normalization / tokenization the deterministic layer uses, so
# the band the judge sees is computed identically to the floor it sits beneath.
from dedupe_headline_alerts import Keys, item_keys, load_json_list, write_json

# Contested band: suspicious enough to doubt, but below the deterministic
# cross-source suppress floor (0.5), so `filter` already let these through.
SHORTLIST_BAND_LOW = 0.35
SHORTLIST_BAND_HIGH = 0.50
SHORTLIST_MIN_OVERLAP = 3
SHORTLIST_MAX_CANDIDATES = 5


def jaccard(left: Keys, right: Keys) -> tuple[float, int]:
    """(Jaccard similarity, absolute shared-token count) of two headlines."""
    overlap = len(left.tokens & right.tokens)
    union = len(left.tokens | right.tokens)
    if not union:
        return 0.0, 0
    return overlap / union, overlap


def candidate_priors(
    item_keys_: Keys,
    history: list[dict[str, Any]],
    history_keys: list[Keys],
    *,
    band_low: float,
    band_high: float,
    min_overlap: int,
    max_candidates: int,
) -> list[dict[str, Any]]:
    """Return the in-band, different-URL prior alerts most similar to an item.

    Sorted by descending Jaccard, capped at ``max_candidates``. Empty when the
    item has no prior in the contested band (the common case -- most headlines
    are clearly new and never reach the judge).
    """
    scored: list[tuple[float, int, dict[str, Any]]] = []
    for record, record_keys in zip(history, history_keys):
        if not record_keys.url_key or record_keys.url_key == item_keys_.url_key:
            continue
        sim, overlap = jaccard(item_keys_, record_keys)
        if overlap < min_overlap:
            continue
        if not (band_low <= sim < band_high):
            continue
        scored.append(
            (
                sim,
                overlap,
                {
                    "headline": str(record.get("headline") or ""),
                    "url": str(record.get("url") or ""),
                    "delivered_at": str(record.get("delivered_at") or ""),
                    "category": str(record.get("category") or ""),
                    "jaccard": round(sim, 3),
                    "overlap": overlap,
                },
            )
        )
    scored.sort(key=lambda row: (row[0], row[1]), reverse=True)
    return [candidate for _, _, candidate in scored[:max_candidates]]


def shortlist(args: argparse.Namespace) -> int:
    incoming = load_json_list(Path(args.to_send_file), missing_ok=True)
    history_raw = load_json_list(Path(args.history_file), missing_ok=True)
    history = [record for record in history_raw if isinstance(record, dict)]
    history_keys = [item_keys(record) for record in history]

    doubtful: list[dict[str, Any]] = []
    for item in incoming:
        if not isinstance(item, dict):
            continue
        keys = item_keys(item)
        if not keys.headline_key or not keys.url_key:
            continue
        candidates = candidate_priors(
            keys,
            history,
            history_keys,
            band_low=args.band_low,
            band_high=args.band_high,
            min_overlap=args.min_overlap,
            max_candidates=args.max_candidates,
        )
        if not candidates:
            continue
        doubtful.append(
            {
                "url": str(item.get("url") or ""),
                "headline": str(item.get("headline") or ""),
                "category": str(item.get("category") or ""),
                "candidates": candidates,
            }
        )

    write_json(Path(args.out_file), doubtful)
    print(
        json.dumps(
            {"incoming": len(incoming), "doubtful": len(doubtful)}, sort_keys=True
        )
    )
    return 0


def _load_verdicts(path: Path) -> dict[str, dict[str, Any]]:
    """Map incoming-URL -> verdict. Fails OPEN: any problem yields no verdicts,
    so every headline is kept (sent). Never raises on a bad model response."""
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text() or "[]")
    except (json.JSONDecodeError, OSError):
        return {}
    if not isinstance(data, list):
        return {}
    by_url: dict[str, dict[str, Any]] = {}
    for entry in data:
        if not isinstance(entry, dict):
            continue
        url = str(entry.get("url") or "").strip()
        if url:
            by_url[url] = entry
    return by_url


def apply_verdicts(args: argparse.Namespace) -> int:
    incoming = load_json_list(Path(args.to_send_file), missing_ok=True)
    verdicts = _load_verdicts(Path(args.verdicts_file))

    kept: list[dict[str, Any]] = []
    suppressed: list[dict[str, Any]] = []
    for item in incoming:
        if not isinstance(item, dict):
            kept.append(item)
            continue
        url = str(item.get("url") or "").strip()
        verdict = verdicts.get(url) or {}
        is_dup = str(verdict.get("verdict") or "").strip().lower() == "duplicate"
        confident = str(verdict.get("confidence") or "").strip().lower() == "high"
        # Suppress ONLY on an explicit high-confidence duplicate verdict.
        if is_dup and confident:
            suppressed.append(
                {
                    "headline": str(item.get("headline") or ""),
                    "url": url,
                    "category": str(item.get("category") or ""),
                    "matched_url": str(verdict.get("matched_url") or ""),
                    "reason": str(verdict.get("reason") or ""),
                    "judged_at": args.timestamp,
                }
            )
            continue
        kept.append(item)

    write_json(Path(args.out_file), kept)

    # Per-run record of what was eaten, for the workflow's Telegram/hooker alert
    # (the durable, human-visible audit that stands in for a shadow phase).
    if args.suppressed_file:
        write_json(Path(args.suppressed_file), suppressed)

    # Optional append-only audit ledger (manual/local use; the workflow relies on
    # the Telegram alert instead, since an ephemeral runner can't durably commit it).
    if suppressed and args.audit_file:
        audit_path = Path(args.audit_file)
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        with audit_path.open("a", encoding="utf-8") as handle:
            for record in suppressed:
                handle.write(json.dumps(record, sort_keys=True) + "\n")

    summary = {
        "incoming": len(incoming),
        "kept": len(kept),
        "suppressed": len(suppressed),
        "suppressed_headlines": [record["headline"] for record in suppressed],
    }
    print(json.dumps(summary, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    short = subparsers.add_parser(
        "shortlist", help="emit contested-band survivors + their nearest priors"
    )
    short.add_argument("--to-send-file", required=True)
    short.add_argument("--history-file", required=True)
    short.add_argument("--out-file", required=True)
    short.add_argument("--band-low", type=float, default=SHORTLIST_BAND_LOW)
    short.add_argument("--band-high", type=float, default=SHORTLIST_BAND_HIGH)
    short.add_argument("--min-overlap", type=int, default=SHORTLIST_MIN_OVERLAP)
    short.add_argument("--max-candidates", type=int, default=SHORTLIST_MAX_CANDIDATES)
    short.set_defaults(func=shortlist)

    apply_parser = subparsers.add_parser(
        "apply", help="drop judge-confirmed duplicates from the send set"
    )
    apply_parser.add_argument("--to-send-file", required=True)
    apply_parser.add_argument("--verdicts-file", required=True)
    apply_parser.add_argument("--out-file", required=True)
    apply_parser.add_argument("--suppressed-file", default="")
    apply_parser.add_argument("--audit-file", default="")
    apply_parser.add_argument("--timestamp", default="")
    apply_parser.set_defaults(func=apply_verdicts)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
