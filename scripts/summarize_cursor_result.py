#!/usr/bin/env python3
"""Print a sanitized one-line summary of an isolated Cursor CLI text-mode run.

run-cursor-container runs `agent -p --output-format text`, which prints the
model's final reply once at exit, or the CLI's own error text, and nothing
else. The container copies that last attempt log into the disposable
workspace as .cursor-result.txt. It is untrusted data and Actions logs are
public, so it is never echoed. The one summary line carries typed fields only:

  status        the exit status the trusted host observed (--status). Text
                mode has no structured status, so nothing in the file can
                claim success.
  reply_sha256  SHA-256 of the stripped reply, the reply_sha256 convention of
                summarize_claude_result.py. The canary compares it with the
                hash of its exact token.
  reply_bytes   the file size; reply_lines its newline-delimited lines.
  cli_error     none on exit 0. Otherwise the class of known CLI error text,
                one of auth, usage_limit, model, network, or other.

A missing, linked, non-regular, oversized, or unreadable file becomes "-"
fields. The summary is diagnostic only and never decides the run: it exits 0
once it has printed its line, and 2 (argparse) only on malformed arguments.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import stat
from pathlib import Path


SUMMARY_PREFIX = "::notice title=Cursor result::"
# Same cap as the host check in run-cursor-container; the container copy is
# truncated to it.
MAX_RESULT_BYTES = 1048576
# The first class whose text appears wins. auth and usage_limit extend the
# attempt loop's cursor_fatal_pattern. The rest is the CLI's own wording: the
# errors real canary runs printed (41160732509 "ActionRequiredError: Weekly
# usage limit reached...", 32004994067 "Cannot use this model: ..."), and from
# the CLI bundle its print-mode auth errors, the words it tests to detect an
# auth failure, and the codes and messages it treats as network failures.
CLI_ERROR_CLASSES = (
    ("auth", re.compile(
        r"Invalid API key|API key is invalid|Unauthorized|Unauthenticated"
        r"|authentication failed|authentication is invalid|Authentication required"
        r"|invalid token|token expired|Not logged in", re.IGNORECASE)),
    ("usage_limit", re.compile(
        r"usage limit|Insufficient (?:balance|credits)|402 Payment", re.IGNORECASE)),
    ("model", re.compile(
        r"Cannot use this model|Model not found|No model found|No models available",
        re.IGNORECASE)),
    ("network", re.compile(
        r"\b(?:ECONNREFUSED|ECONNRESET|ECONNABORTED|ETIMEDOUT|ENOTFOUND|EAI_AGAIN"
        r"|EHOSTUNREACH|ENETUNREACH|ENETDOWN|EPIPE|UND_ERR_[A-Z_]+)\b"
        r"|connection reset|fetch failed|network error|other side closed|socket hang up",
        re.IGNORECASE)),
)
CLI_ERRORS = ("none",) + tuple(name for name, _ in CLI_ERROR_CLASSES) + ("other",)


def reply_sha256(reply: str) -> str:
    """The digest the canary compares against its expected token.

    The same convention as summarize_claude_result.reply_sha256, which a test
    pins. It is a copy, not an import: the host runs this file under
    `python3 -I`, which keeps the script directory off sys.path.
    """
    return hashlib.sha256(reply.strip().encode("utf-8")).hexdigest()


def cli_error(status: int, text: str | None) -> str:
    """none on exit 0 (the file is then the model reply, so its words prove
    nothing), else the first known CLI error class in the text, else other."""
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

    The host checks the same before calling; this holds even when it did not.
    O_NOFOLLOW refuses a symlink and O_NONBLOCK keeps a FIFO from blocking the
    open, which fstat then rejects.
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
                        help="the agent exit status the trusted host observed")
    parser.add_argument("--result-file", type=Path, default=None,
                        help="the copied attempt log; omitted when the host rejected it")
    args = parser.parse_args(argv)
    raw = read_result(args.result_file) if args.result_file is not None else None
    print(summarize(args.status, raw))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
