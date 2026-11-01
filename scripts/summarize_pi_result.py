#!/usr/bin/env python3
"""Print a sanitized one-line summary of a run-pi-container `pi -p` run.

`pi -p` prints the model's final reply to stdout, or the provider's error
(`assistantMsg.errorMessage`) or pi's own `Error: ...` text to stderr, and
nothing else. The container sends both to .pi-result.txt in its disposable
clone, never to the job log: Actions logs are public, and the reply is built
from untrusted tweets. The model has a shell in that container, so the file
is untrusted data too. The one summary line carries typed fields only:

  status        the exit status the trusted host observed (--status), never
                anything read from the file.
  reply_sha256  SHA-256 of the stripped reply, the reply_sha256 convention of
                summarize_claude_result.py and summarize_cursor_result.py.
  reply_bytes   the file size; reply_lines its newline-delimited lines.
  cli_error     none on exit 0. Otherwise the class of known provider or pi
                error text, one of auth, usage_limit, rate_limit, model,
                network, or other.

A missing, linked, non-regular, oversized, or unreadable file becomes "-"
fields. The summary is diagnostic only and never decides the run: it exits 0
once it has printed its line, and 2 (argparse) only on malformed arguments.
run-pi-container runs this file from the real checkout, which the container
never mounts.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import stat
from pathlib import Path


SUMMARY_PREFIX = "::notice title=pi result::"
MAX_RESULT_BYTES = 1048576
# The first class whose text appears wins. pi prints a failed request's
# provider message as is: Fireworks answers a suspended account with
# "412 ... Account ... is suspended" (CLAUDE.md, FIREWORKS_API_KEY), and its
# OpenAI-compatible API uses the usual 401/402/404/429 wording. The rest is
# pi's own text (formatNoModelsAvailableMessage) and Node's network errors.
CLI_ERROR_CLASSES = (
    ("auth", re.compile(
        r"\b40[13]\b|Unauthorized|Unauthenticated|Forbidden|Invalid API key|invalid_api_key"
        r"|API key is invalid|authentication failed|No API key", re.IGNORECASE)),
    ("usage_limit", re.compile(
        r"\b402\b|\b412\b|suspended|spending limit|Insufficient (?:balance|credits|quota)"
        r"|quota exceeded|exceeded your current quota|usage limit", re.IGNORECASE)),
    ("rate_limit", re.compile(r"\b429\b|rate limit|Too Many Requests", re.IGNORECASE)),
    ("model", re.compile(
        r"No models available|model not found|Unknown model|model .{0,80} does not exist"
        r"|\b404\b", re.IGNORECASE)),
    ("network", re.compile(
        r"\b(?:ECONNREFUSED|ECONNRESET|ECONNABORTED|ETIMEDOUT|ENOTFOUND|EAI_AGAIN"
        r"|EHOSTUNREACH|ENETUNREACH|EPIPE|UND_ERR_[A-Z_]+)\b"
        r"|fetch failed|socket hang up|network error", re.IGNORECASE)),
)
CLI_ERRORS = ("none",) + tuple(name for name, _ in CLI_ERROR_CLASSES) + ("other",)


def reply_sha256(reply: str) -> str:
    """The reply digest convention shared with the Claude and Cursor summaries.

    A copy, not an import: the host runs this file under `python3 -I`, which
    puts no sibling module on sys.path.
    """
    return hashlib.sha256(reply.strip().encode("utf-8")).hexdigest()


def cli_error(status: int, text: str | None) -> str:
    """none on exit 0 (the file is then the model reply, so its words prove
    nothing), else the first known error class in the text, else other."""
    if status == 0:
        return "none"
    for name, pattern in CLI_ERROR_CLASSES:
        if text and pattern.search(text):
            return name
    return "other"


def summarize(status: int, raw: bytes | None) -> str:
    """The summary line for a host-observed status and the result bytes, if any."""
    text = None
    digest = size = lines = "-"
    if raw is not None:
        text = raw.decode("utf-8", errors="replace")
        digest = reply_sha256(text)
        size = str(len(raw))
        lines = str(raw.count(b"\n") + (1 if raw and not raw.endswith(b"\n") else 0))
    return (f"{SUMMARY_PREFIX}status={status} reply_sha256={digest} reply_bytes={size} "
            f"reply_lines={lines} cli_error={cli_error(status, text)}")


def read_result(path: Path) -> bytes | None:
    """The file's bytes, or None unless it is a regular, unlinked file within the cap.

    O_NOFOLLOW refuses a symlink, and O_NONBLOCK keeps a FIFO from blocking
    the open, which fstat then rejects.
    """
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    try:
        fd = os.open(path, flags)
    except OSError:
        return None
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_RESULT_BYTES:
            return None
        chunks = []
        remaining = MAX_RESULT_BYTES + 1
        while remaining > 0:
            chunk = os.read(fd, min(remaining, 65536))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
    except OSError:
        return None
    finally:
        os.close(fd)
    data = b"".join(chunks)
    return data if len(data) <= MAX_RESULT_BYTES else None


def exit_status(value: str) -> int:
    if not re.fullmatch(r"[0-9]{1,3}", value) or int(value) > 255:
        raise argparse.ArgumentTypeError("must be an exit status from 0 through 255")
    return int(value)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--status", required=True, type=exit_status,
                        help="the container exit status the trusted host observed")
    parser.add_argument("--result-file", type=Path, default=None,
                        help="pi's output file; omitted when the host rejected it")
    args = parser.parse_args(argv)
    raw = read_result(args.result_file) if args.result_file is not None else None
    print(summarize(args.status, raw))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
