#!/usr/bin/env python3
"""Print a sanitized summary of an isolated `claude -p --output-format json` result.

run-claude-container calls this on the host after the container exits. The
file was written inside the disposable container, so it is untrusted data:
only typed fields that match strict patterns are echoed. The reply text and
the input of denied calls (a denied Write keeps its whole content) never
reach the public log; a SHA-256 of the stripped reply stands in for it, which
is how the canary proves its exact token reply. Denials are counted by tool
and reason, never shown with an input or a path: the guard's own refusals
carry its reason code (tool-guard.mjs writes them to --guard-denials), and
the rest of the CLI's permission_denials count as `cli_rule`, refused by
Claude Code's own rules before the guard ran. The exit status is the
contract: 0 = summarized, 3 = the CLI reported is_error (the caller fails
closed even when the CLI exited 0), 2 = unreadable.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path


SAFE_TOKEN = re.compile(r"^[A-Za-z0-9_.-]{1,64}$")
# Kept identical to REASONS and LOGGED_TOOLS in
# .github/actions/run-claude-container/tool-guard.mjs.
GUARD_REASONS = frozenset({
    "policy_invalid", "workspace_invalid", "input_invalid", "tool_not_allowed",
    "path_invalid", "path_tilde", "path_missing", "path_type", "path_symlink", "path_outside",
    "path_not_allowed", "git_metadata", "glob_pattern", "shell_multiline", "shell_background",
    "shell_metachar", "command_not_allowed", "curl_flag", "curl_form", "curl_url",
    "curl_query", "uv_form", "uv_argument", "git_form", "commit_form",
})
GUARD_TOOLS = frozenset({
    "Read", "Write", "Edit", "MultiEdit", "Glob", "Grep", "Bash", "WebFetch", "WebSearch",
    "Task", "Agent", "NotebookEdit", "TodoWrite", "Skill", "mcp", "other", "-",
})
MAX_GUARD_LINES = 4096


def _token(value: object) -> str:
    return value if isinstance(value, str) and SAFE_TOKEN.fullmatch(value) else "?"


def _count(value: object) -> str:
    return str(value) if isinstance(value, int) and not isinstance(value, bool) else "?"


def reply_sha256(reply: str) -> str:
    """The digest the canary compares against its expected token."""
    return hashlib.sha256(reply.strip().encode("utf-8")).hexdigest()


def guard_denials(text: str) -> list[tuple[str, str]]:
    """The well-formed "<tool>\t<reason>" lines of the guard's denial log."""
    entries = []
    for line in text.splitlines()[:MAX_GUARD_LINES]:
        tool, separator, reason = line.partition("\t")
        if separator and tool in GUARD_TOOLS and reason in GUARD_REASONS:
            entries.append((tool, reason))
    return entries


def summarize(data: object, guard: list[tuple[str, str]] = ()) -> tuple[list[str], bool]:
    """Return log lines and whether the CLI reported an error."""
    if not isinstance(data, dict):
        raise ValueError("Claude result must be a JSON object")
    is_error = data.get("is_error")
    if not isinstance(is_error, bool):
        raise ValueError("Claude result has no boolean is_error")
    cost = data.get("total_cost_usd")
    cost_text = (f"{cost:.4f}" if isinstance(cost, (int, float))
                 and not isinstance(cost, bool) else "?")
    usage = data.get("modelUsage")
    usage = usage if isinstance(usage, dict) else {}
    models = sorted(_token(model) for model in usage)
    output_tokens = sorted(
        f"{_token(model)}:{_count(spec.get('outputTokens') if isinstance(spec, dict) else None)}"
        for model, spec in usage.items())
    api_error_status = data.get("api_error_status")
    denials = data.get("permission_denials")
    denials = denials if isinstance(denials, list) else []
    reply = data.get("result")
    lines = [
        "::notice title=Claude result::"
        f"is_error={str(is_error).lower()} subtype={_token(data.get('subtype'))} "
        f"terminal_reason={_token(data.get('terminal_reason'))} "
        f"turns={_count(data.get('num_turns'))} cost_usd={cost_text} "
        f"models={','.join(models) or 'none'} "
        f"output_tokens={','.join(output_tokens) or 'none'} "
        f"api_error_status={_count(api_error_status) if api_error_status is not None else '-'} "
        f"permission_denials={len(denials)} "
        f"reply_sha256={reply_sha256(reply) if isinstance(reply, str) else '-'}"
    ]
    counts: Counter[tuple[str, str]] = Counter(guard)
    by_tool = Counter(_token(denial.get("tool_name")) if isinstance(denial, dict) else "?"
                      for denial in denials)
    for tool, total in by_tool.items():
        rest = total - sum(count for (name, _), count in counts.items() if name == tool)
        if rest > 0:
            counts[(tool, "cli_rule")] += rest
    if counts:
        lines.append("::notice title=Claude denials::" + " ".join(
            f"{tool}:{reason}={count}" for (tool, reason), count in sorted(counts.items())))
    return lines, is_error


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result_file", type=Path)
    parser.add_argument("--guard-denials", type=Path, default=None)
    args = parser.parse_args(argv)
    guard: list[tuple[str, str]] = []
    if args.guard_denials is not None:
        try:
            guard = guard_denials(args.guard_denials.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            guard = []
    try:
        lines, is_error = summarize(json.loads(args.result_file.read_text(encoding="utf-8")),
                                    guard)
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        print(f"Could not summarize the Claude result: {type(exc).__name__}", file=sys.stderr)
        return 2
    for line in lines:
        print(line)
    return 3 if is_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
