#!/usr/bin/env python3
"""Fail closed unless the isolated Cursor CLI canary proves key, quota, and model.

The canary runs one tool-denied `agent -p --mode ask` turn inside
run-cursor-container. The adapter never prints the CLI reply. Its output file
holds the container's own log lines, then the typed summary line of
scripts/summarize_cursor_result.py, which the host appends after the container
exits. So the summary must be the final line: one anywhere else is container
output and proves nothing. This checks that line's exit status (observed by
the host, not read from the reply) is 0 and its reply SHA-256 is that of the
exact canary token.

Exact, not "contains": text mode prints only the final message, and every
successful canary on record (runs 31998732492, 32008228660, 33592443213,
33610325290, 40136175298) printed exactly the token and nothing else. A
rejected key, an exhausted quota, or an unusable model makes the CLI exit
nonzero, so status 0 proves all three. Text mode reports no served model to
check.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from summarize_cursor_result import CLI_ERRORS, SUMMARY_PREFIX, reply_sha256


FIELDS = {
    "status": re.compile(r"[0-9]{1,3}"),
    "reply_sha256": re.compile(r"[0-9a-f]{64}|-"),
    "reply_bytes": re.compile(r"[0-9]+|-"),
    "reply_lines": re.compile(r"[0-9]+|-"),
    "cli_error": re.compile("|".join(CLI_ERRORS)),
}


def final_summary(text: str) -> dict[str, str]:
    """The typed fields of the summary line that ends the output."""
    lines = [line.rstrip("\r") for line in text.split("\n")]
    while lines and not lines[-1].strip():
        lines.pop()
    if not any(line.startswith(SUMMARY_PREFIX) for line in lines):
        raise ValueError("canary output has no Cursor result summary")
    if not lines[-1].startswith(SUMMARY_PREFIX):
        raise ValueError("the Cursor result summary is not the final line of the output")
    fields: dict[str, str] = {}
    for part in lines[-1][len(SUMMARY_PREFIX):].split(" "):
        key, separator, value = part.partition("=")
        if (not separator or key in fields or key not in FIELDS
                or not FIELDS[key].fullmatch(value)):
            raise ValueError("canary result summary is malformed")
        fields[key] = value
    if set(fields) != set(FIELDS):
        raise ValueError("canary result summary is malformed")
    return fields


def validate(text: str, token: str) -> None:
    summary = final_summary(text)
    if summary["status"] != "0":
        raise ValueError(
            f"canary Cursor run exited {summary['status']} (cli_error={summary['cli_error']}); "
            "check the API key, quota, and model")
    if summary["reply_sha256"] != reply_sha256(token):
        raise ValueError("canary reply is not exactly the canary token")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("output_file", type=Path)
    parser.add_argument("--token", required=True)
    args = parser.parse_args(argv)
    try:
        text = args.output_file.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"::error::Cursor CLI canary output is unreadable ({type(exc).__name__}).")
        return 1
    try:
        validate(text, args.token)
    except ValueError as exc:
        print(f"::error::Cursor CLI canary failed: {exc}.")
        return 1
    print("Verified isolated Cursor CLI canary: API key, quota, and model OK; "
          "exact token reply; tool-denied, no publication.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
