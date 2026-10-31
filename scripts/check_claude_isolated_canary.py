#!/usr/bin/env python3
"""Fail closed unless the isolated Claude Code canary proves auth, quota, and model.

The canary runs `claude -p --output-format json` inside run-claude-container
with no tools at all. The adapter never prints the CLI's reply: its output
file holds container log lines plus the sanitized summary line from
scripts/summarize_claude_result.py. This checks the last summary: a
successful, error-free turn, no permission denials, output usage billed to
the requested model (the served-model rule of scripts/check_claude_canary.py),
and a reply whose SHA-256 is that of the exact canary token.
"""

import argparse
import re
from pathlib import Path

from summarize_claude_result import reply_sha256


SUMMARY_PREFIX = "::notice title=Claude result::"
FIELD = re.compile(r"^([a-z0-9_]+)=(\S+)$")


def last_summary(text: str) -> dict[str, str]:
    lines = [line[len(SUMMARY_PREFIX):] for line in text.splitlines()
             if line.startswith(SUMMARY_PREFIX)]
    if not lines:
        raise ValueError("canary output has no Claude result summary")
    fields: dict[str, str] = {}
    for part in lines[-1].split():
        match = FIELD.fullmatch(part)
        if not match or match.group(1) in fields:
            raise ValueError("canary result summary is malformed")
        fields[match.group(1)] = match.group(2)
    return fields


def validate(text: str, model: str, token: str) -> None:
    summary = last_summary(text)
    if summary.get("is_error") != "false" or summary.get("subtype") != "success":
        raise ValueError("canary result is an error; check auth, quota, and model access")
    if summary.get("permission_denials") != "0":
        raise ValueError("canary encountered permission denials")
    served = {}
    for entry in summary.get("output_tokens", "none").split(","):
        name, _, count = entry.rpartition(":")
        if name and count.isdigit():
            served[name] = int(count)
    if served.get(model, 0) <= 0:
        raise ValueError(f"requested model {model} has no observed output usage")
    if summary.get("reply_sha256") != reply_sha256(token):
        raise ValueError("canary reply is not exactly the canary token")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_file", type=Path)
    parser.add_argument("--model", required=True)
    parser.add_argument("--token", required=True)
    args = parser.parse_args()
    validate(args.output_file.read_text(encoding="utf-8", errors="replace"),
             args.model, args.token)
    print(f"Verified isolated Claude Code canary on {args.model}: OAuth token, "
          "quota, and served model OK; no tools, no publication")


if __name__ == "__main__":
    main()
