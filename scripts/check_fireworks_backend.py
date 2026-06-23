#!/usr/bin/env python3
"""Preflight Fireworks' Anthropic-compatible Messages endpoint.

Claude Code hides provider error bodies when `show_full_output` is false, which
is the safe default for research runs. This script performs a tiny direct
request before the expensive agent step so account/auth/model failures stop
before the workflow enters its retry loop.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


NON_RETRYABLE_STATUSES = {400, 401, 402, 403, 404, 412}
MAX_MESSAGE_CHARS = 500


def redact(text: str) -> str:
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


def annotation_escape(message: str) -> str:
    return (
        message.replace("%", "%25")
        .replace("\r", "%0D")
        .replace("\n", "%0A")
    )


def extract_message(status: int | None, body: str) -> str:
    body = body.strip()
    if not body:
        return f"HTTP {status}" if status else "no response body"
    try:
        parsed: Any = json.loads(body)
    except json.JSONDecodeError:
        message = body
    else:
        error = parsed.get("error") if isinstance(parsed, dict) else None
        if isinstance(error, dict):
            message = str(
                error.get("message")
                or error.get("detail")
                or error.get("type")
                or json.dumps(error, separators=(",", ":"))
            )
        elif isinstance(error, str):
            message = error
        elif isinstance(parsed, dict):
            message = str(
                parsed.get("message")
                or parsed.get("detail")
                or json.dumps(parsed, separators=(",", ":"))
            )
        else:
            message = str(parsed)
    message = redact(message)
    if len(message) > MAX_MESSAGE_CHARS:
        message = message[: MAX_MESSAGE_CHARS - 1] + "..."
    return message


def write_outputs(
    path: Path | None,
    *,
    status: int | None,
    non_retryable: bool,
    available: bool,
    message: str,
) -> None:
    if not path:
        return
    with path.open("a") as handle:
        handle.write(f"status={status if status is not None else ''}\n")
        handle.write(f"non_retryable={str(non_retryable).lower()}\n")
        handle.write(f"available={str(available).lower()}\n")
        handle.write("message<<__FIREWORKS_PREFLIGHT__\n")
        handle.write(f"{message}\n")
        handle.write("__FIREWORKS_PREFLIGHT__\n")


def request_preflight(endpoint: str, api_key: str, model: str) -> tuple[int, str]:
    payload = json.dumps(
        {
            "model": model,
            "max_tokens": 1,
            "messages": [{"role": "user", "content": "ping"}],
        }
    ).encode()
    request = urllib.request.Request(
        endpoint.rstrip("/") + "/v1/messages",
        data=payload,
        method="POST",
        headers={
            "anthropic-version": "2023-06-01",
            "authorization": f"Bearer {api_key}",
            "content-type": "application/json",
            "x-api-key": api_key,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.status, response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode("utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument(
        "--endpoint",
        default="https://api.fireworks.ai/inference",
        help="Fireworks Anthropic-compatible base URL without /v1.",
    )
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()

    api_key = os.environ.get("FIREWORKS_API_KEY", "").strip()
    if not api_key:
        message = "FIREWORKS_API_KEY is not configured"
        write_outputs(
            args.github_output,
            status=None,
            non_retryable=True,
            available=False,
            message=message,
        )
        print(f"::error::{annotation_escape(message)}")
        return 1

    try:
        status, body = request_preflight(args.endpoint, api_key, args.model)
    except Exception as exc:  # noqa: BLE001 - network preflight should not crash.
        message = redact(str(exc))
        write_outputs(
            args.github_output,
            status=None,
            non_retryable=False,
            available=False,
            message=message,
        )
        print(
            "::warning::Fireworks preflight request failed before HTTP status; "
            f"continuing to Claude Code retry policy: {annotation_escape(message)}"
        )
        return 0

    message = extract_message(status, body)
    non_retryable = status in NON_RETRYABLE_STATUSES
    available = 200 <= status < 300
    write_outputs(
        args.github_output,
        status=status,
        non_retryable=non_retryable,
        available=available,
        message=message,
    )

    if available:
        print(f"Fireworks preflight OK for {args.model}")
        return 0
    if non_retryable:
        print(
            f"::error::Fireworks preflight API status {status} "
            f"(non-retryable): {annotation_escape(message)}"
        )
        return 1
    print(
        f"::warning::Fireworks preflight API status {status} "
        f"(retryable): {annotation_escape(message)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
