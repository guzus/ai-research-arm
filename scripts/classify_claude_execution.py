#!/usr/bin/env python3
"""Classify how a native Claude Code agent step ended, for post-agent fallback.

`.github/actions/agent-run` cannot learn from the pre-agent OAuth probe
whether Claude can serve a run: a healthy Claude Code OAuth token answers
the raw 1-token ping with HTTP 429 unconditionally, so 429 there carries no
information (see scripts/select_backend.py). The reliable signal is the
agent step itself. This helper reads the claude-code-action execution
transcript and answers one question: did Claude die BEFORE doing any work?

Outcomes
  success    a `result` object with is_error false.
  dead-start is_error true AND num_turns <= 1 AND total_cost_usd == 0 —
             the signature of a throttled or rejected credential (the
             2026-07-24 expired-token outage and the 2026-08-28 usage-limit
             hits both look exactly like this). Nothing was written, so the
             caller may hand the SAME prompt to the next backend in the
             chain from a clean checkout.
  failed     is_error true after real work (turns > 1 or cost > 0). The
             checkout may hold partial edits; NOT safe to re-run elsewhere.
  unknown    no `result` object (transcript missing/empty/truncated).

Only `dead-start` is a fallback trigger. `failed` and `unknown` are surfaced
as errors so a real agent failure stays red instead of being papered over
by a fallback that would double-spend and could mix two models' output.

STDLIB ONLY — runs on bare python3 on the runner. Exit code is always 0
(classification is data; the action decides), except 2 for bad arguments.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from summarize_claude_execution import parse_objects, redact, summarize  # noqa: E402

DEAD_START_MAX_TURNS = 1
MAX_REASON_CHARS = 400


def _as_int(value: Any, default: int) -> int:
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return default


def _as_float(value: Any, default: float) -> float:
    if isinstance(value, bool):
        return default
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            return default
    return default


def classify(objects: list[dict[str, Any]]) -> dict[str, Any]:
    result_obj = None
    for obj in objects:
        if obj.get("type") == "result":
            result_obj = obj  # keep the LAST result object
    if result_obj is None:
        return {"outcome": "unknown", "reason": "no result object in transcript",
                "num_turns": None, "total_cost_usd": None, "error_status": None}

    is_error = result_obj.get("is_error") is True
    num_turns = _as_int(result_obj.get("num_turns"), default=0)
    cost = _as_float(result_obj.get("total_cost_usd"), default=0.0)
    summary = summarize(objects)
    status = summary.get("status")
    message = summary.get("message") or ""
    if not message and isinstance(result_obj.get("result"), str):
        message = redact(result_obj["result"])
    if len(message) > MAX_REASON_CHARS:
        message = message[: MAX_REASON_CHARS - 1] + "..."

    if not is_error:
        outcome, reason = "success", f"{num_turns} turn(s), ${cost:.4f}"
    elif num_turns <= DEAD_START_MAX_TURNS and cost == 0:
        outcome = "dead-start"
        reason = (f"Claude died before doing work (is_error, {num_turns} turn(s), $0"
                  + (f", API status {status}" if status else "") + ")"
                  + (f": {message}" if message else ""))
    else:
        outcome = "failed"
        reason = (f"Claude failed after real work ({num_turns} turn(s), ${cost:.4f}"
                  + (f", API status {status}" if status else "") + ")"
                  + (f": {message}" if message else ""))
    return {"outcome": outcome, "reason": reason, "num_turns": num_turns,
            "total_cost_usd": cost, "error_status": status}


def classify_file(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"outcome": "unknown", "reason": f"execution transcript not found: {path}",
                "num_turns": None, "total_cost_usd": None, "error_status": None}
    try:
        text = path.read_text(errors="replace")
    except OSError as exc:
        return {"outcome": "unknown", "reason": f"cannot read transcript: {exc}",
                "num_turns": None, "total_cost_usd": None, "error_status": None}
    return classify(parse_objects(text))


def write_github_output(path: Path, verdict: dict[str, Any]) -> None:
    def one_line(value: Any) -> str:
        return " ".join(str(value if value is not None else "").splitlines())
    with path.open("a") as handle:
        handle.write(f"outcome={one_line(verdict['outcome'])}\n")
        handle.write(f"reason={one_line(verdict['reason'])}\n")
        handle.write(f"num_turns={one_line(verdict['num_turns'])}\n")
        handle.write(f"total_cost_usd={one_line(verdict['total_cost_usd'])}\n")
        handle.write(f"error_status={one_line(verdict['error_status'])}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("execution_file", type=Path, nargs="?",
                        help="claude-code-action execution transcript (JSONL / JSON)")
    parser.add_argument("--github-output", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.execution_file is None:
        verdict = {"outcome": "unknown", "reason": "no execution transcript path given",
                   "num_turns": None, "total_cost_usd": None, "error_status": None}
    else:
        verdict = classify_file(args.execution_file)

    if args.github_output:
        write_github_output(args.github_output, verdict)
    if args.json:
        print(json.dumps(verdict, separators=(",", ":")))
    else:
        print(f"claude outcome: {verdict['outcome']} — {verdict['reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
