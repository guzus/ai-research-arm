#!/usr/bin/env python3
"""Print a sanitized summary of an isolated `claude -p --output-format json` result.

run-claude-container calls this on the host after the container exits. The
file was written inside the disposable container, so it is untrusted data:
only typed fields that match strict patterns are echoed, never the reply
text, so a model reply cannot inject a workflow command into the log. The
exit status is the contract: 0 = summarized, 3 = the CLI reported is_error
(the caller fails closed even when the CLI exited 0), 2 = unreadable.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SAFE_TOKEN = re.compile(r"^[A-Za-z0-9_.-]{1,64}$")
SAFE_PATH = re.compile(r"^[A-Za-z0-9_./-]{1,240}$")
MAX_DENIALS = 20


def _token(value: object) -> str:
    return value if isinstance(value, str) and SAFE_TOKEN.fullmatch(value) else "?"


def summarize(data: object) -> tuple[list[str], bool]:
    """Return log lines and whether the CLI reported an error."""
    if not isinstance(data, dict):
        raise ValueError("Claude result must be a JSON object")
    is_error = data.get("is_error")
    if not isinstance(is_error, bool):
        raise ValueError("Claude result has no boolean is_error")
    turns = data.get("num_turns")
    turns_text = str(turns) if isinstance(turns, int) and not isinstance(turns, bool) else "?"
    cost = data.get("total_cost_usd")
    cost_text = (f"{cost:.4f}" if isinstance(cost, (int, float))
                 and not isinstance(cost, bool) else "?")
    usage = data.get("modelUsage")
    models = sorted(_token(model) for model in usage) if isinstance(usage, dict) else []
    denials = data.get("permission_denials")
    denials = denials if isinstance(denials, list) else []
    lines = [
        "::notice title=Claude result::"
        f"is_error={str(is_error).lower()} subtype={_token(data.get('subtype'))} "
        f"terminal_reason={_token(data.get('terminal_reason'))} turns={turns_text} "
        f"cost_usd={cost_text} models={','.join(models) or 'none'} "
        f"permission_denials={len(denials)}"
    ]
    for denial in denials[:MAX_DENIALS]:
        denial = denial if isinstance(denial, dict) else {}
        tool_input = denial.get("tool_input")
        target = tool_input.get("file_path") if isinstance(tool_input, dict) else None
        shown = target if isinstance(target, str) and SAFE_PATH.fullmatch(target) else "-"
        lines.append(f"Claude permission denial: {_token(denial.get('tool_name'))} {shown}")
    if len(denials) > MAX_DENIALS:
        lines.append(f"Claude permission denial: {len(denials) - MAX_DENIALS} more not shown")
    return lines, is_error


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result_file", type=Path)
    args = parser.parse_args(argv)
    try:
        lines, is_error = summarize(json.loads(args.result_file.read_text(encoding="utf-8")))
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        print(f"Could not summarize the Claude result: {type(exc).__name__}", file=sys.stderr)
        return 2
    for line in lines:
        print(line)
    return 3 if is_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
