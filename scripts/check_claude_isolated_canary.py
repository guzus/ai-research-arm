#!/usr/bin/env python3
"""Fail closed unless the isolated Claude Code canary proves auth, quota, and model.

The canary runs `claude -p --output-format json` inside run-claude-container
with no tools at all. Its host-tee'd stdout holds container log lines plus
the CLI's one-line JSON result; this checks the last result object: a
successful, error-free turn, no permission denials, the exact canary token as
the whole reply, and output usage billed to the requested model (the same
served-model rule as scripts/check_claude_canary.py).
"""

import argparse
from pathlib import Path

from summarize_claude_execution import parse_objects


def validate(objects: list[dict], model: str, token: str) -> None:
    results = [obj for obj in objects if obj.get("type") == "result"]
    if not results:
        raise ValueError("canary output has no Claude result object")
    result = results[-1]
    if result.get("is_error") is not False or result.get("subtype") != "success":
        raise ValueError("canary result is an error; check auth, quota, and model access")
    if result.get("permission_denials"):
        raise ValueError("canary encountered permission denials")
    usage = result.get("modelUsage")
    served = usage.get(model) if isinstance(usage, dict) else None
    output_tokens = served.get("outputTokens") if isinstance(served, dict) else None
    if not isinstance(output_tokens, int) or output_tokens <= 0:
        raise ValueError(f"requested model {model} has no observed output usage")
    if str(result.get("result", "")).strip() != token:
        raise ValueError("canary reply is not exactly the canary token")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_file", type=Path)
    parser.add_argument("--model", required=True)
    parser.add_argument("--token", required=True)
    args = parser.parse_args()
    validate(parse_objects(args.output_file.read_text(encoding="utf-8", errors="replace")),
             args.model, args.token)
    print(f"Verified isolated Claude Code canary on {args.model}: OAuth token, "
          "quota, and served model OK; no tools, no publication")


if __name__ == "__main__":
    main()
