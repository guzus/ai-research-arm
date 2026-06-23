#!/usr/bin/env python3
"""Summarize Claude Code JSONL execution errors for GitHub Actions.

The Claude Code action writes a machine-readable execution transcript, but the
normal workflow log can collapse provider failures into "no article commit".
This helper extracts API statuses and short error text so retry gates can avoid
repeating non-retryable account/auth failures.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


NON_RETRYABLE_STATUSES = {400, 401, 402, 403, 404, 412}
STATUS_KEYS = {"api_error_status", "error_status"}
MAX_MESSAGE_CHARS = 500


def parse_objects(text: str) -> list[dict[str, Any]]:
    """Parse JSONL or concatenated JSON objects."""
    objects: list[dict[str, Any]] = []
    decoder = json.JSONDecoder()
    pos = 0
    while pos < len(text):
        while pos < len(text) and text[pos].isspace():
            pos += 1
        if pos >= len(text):
            break
        try:
            obj, end = decoder.raw_decode(text, pos)
        except json.JSONDecodeError:
            line_end = text.find("\n", pos)
            if line_end == -1:
                break
            pos = line_end + 1
            continue
        if isinstance(obj, dict):
            objects.append(obj)
        pos = end
    return objects


def redact(text: str) -> str:
    """Keep provider diagnostics useful without echoing credentials."""
    patterns = [
        (r"(?i)(bearer\s+)[A-Za-z0-9._~+/=-]{12,}", r"\1[redacted]"),
        (r"(?i)(api[_-]?key[\"'\s:=]+)[A-Za-z0-9._~+/=-]{12,}", r"\1[redacted]"),
        (r"fw_[A-Za-z0-9._~+/=-]{8,}", "fw_[redacted]"),
        (r"sk-[A-Za-z0-9._~+/=-]{8,}", "sk-[redacted]"),
    ]
    cleaned = text.replace("\x00", "")
    for pattern, repl in patterns:
        cleaned = re.sub(pattern, repl, cleaned)
    return " ".join(cleaned.split())


def walk(value: Any) -> list[Any]:
    found = [value]
    if isinstance(value, dict):
        for child in value.values():
            found.extend(walk(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(walk(child))
    return found


def summarize(objects: list[dict[str, Any]]) -> dict[str, Any]:
    statuses: list[int] = []
    messages: list[str] = []

    for obj in objects:
        for node in walk(obj):
            if not isinstance(node, dict):
                continue
            for key in STATUS_KEYS:
                status = node.get(key)
                if isinstance(status, int):
                    statuses.append(status)
                elif isinstance(status, str) and status.isdigit():
                    statuses.append(int(status))

            result = node.get("result")
            if node.get("is_error") is True and isinstance(result, str):
                messages.append(result)

            text = node.get("text")
            if isinstance(text, str) and "API Error:" in text:
                messages.append(text)

    for message in list(messages):
        match = re.search(r"\bAPI Error:\s*(\d{3})\b", message)
        if match:
            statuses.append(int(match.group(1)))

    primary_status = None
    for status in reversed(statuses):
        if status in NON_RETRYABLE_STATUSES:
            primary_status = status
            break
    if primary_status is None and statuses:
        primary_status = statuses[-1]

    unique_messages = []
    seen_messages = set()
    for message in messages:
        cleaned = redact(message)
        if cleaned and cleaned not in seen_messages:
            seen_messages.add(cleaned)
            unique_messages.append(cleaned)

    message = unique_messages[0] if unique_messages else ""
    if len(message) > MAX_MESSAGE_CHARS:
        message = message[: MAX_MESSAGE_CHARS - 1] + "..."

    return {
        "status": primary_status,
        "statuses": statuses,
        "message": message,
        "non_retryable": primary_status in NON_RETRYABLE_STATUSES
        if primary_status is not None
        else False,
    }


def annotation_escape(message: str) -> str:
    return (
        message.replace("%", "%25")
        .replace("\r", "%0D")
        .replace("\n", "%0A")
    )


def write_env(path: Path, summary: dict[str, Any]) -> None:
    status = summary["status"]
    path.write_text(
        "\n".join(
            [
                f"CLAUDE_ERROR_STATUS={status if status is not None else ''}",
                f"CLAUDE_NON_RETRYABLE={str(summary['non_retryable']).lower()}",
                "",
            ]
        )
    )


def write_github_output(path: Path, summary: dict[str, Any]) -> None:
    status = summary["status"]
    with path.open("a") as handle:
        handle.write(f"claude_error_status={status if status is not None else ''}\n")
        handle.write(
            f"claude_non_retryable={str(summary['non_retryable']).lower()}\n"
        )
        handle.write("claude_error_message<<__CLAUDE_ERROR__\n")
        handle.write(f"{summary['message']}\n")
        handle.write("__CLAUDE_ERROR__\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("execution_file", type=Path)
    parser.add_argument("--env-output", type=Path)
    parser.add_argument("--github-output", type=Path)
    parser.add_argument("--github-annotation", choices=["notice", "warning", "error"])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.execution_file.exists():
        print(f"execution transcript not found: {args.execution_file}", file=sys.stderr)
        return 0

    summary = summarize(parse_objects(args.execution_file.read_text(errors="replace")))

    if args.env_output:
        write_env(args.env_output, summary)
    if args.github_output:
        write_github_output(args.github_output, summary)
    if args.github_annotation and (summary["status"] or summary["message"]):
        status = summary["status"] or "unknown"
        retry_hint = "non-retryable" if summary["non_retryable"] else "retryable"
        message = summary["message"] or "Claude Code reported an API error."
        print(
            f"::{args.github_annotation}::Claude Code API status {status} "
            f"({retry_hint}): {annotation_escape(message)}"
        )
    if args.json:
        print(json.dumps(summary, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
