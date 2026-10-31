#!/usr/bin/env python3
"""Validate a trusted per-lane Claude Code policy and materialize its run copy.

The committed `.github/claude/<lane>.json` is an ordinary Claude Code settings
file, limited to a reviewable subset:

* `permissions.allow` may only hold `Read(path)` and `Edit(path)` rules on
  clean workspace-relative paths, optionally ending in `/**`. They are the
  lane's whole capability: they decide the `--tools` list this script prints
  (Read rules expose Read; Edit rules expose Write and Edit) and the exact
  allowlist that `.github/actions/run-claude-container/tool-guard.mjs`
  enforces. Claude Code's dontAsk mode alone would still allow any read in the
  working directory.
* `permissions.deny` must keep the baseline below, so no lane file can drop a
  tool that runs code, reaches the network, delegates to a subagent, or reads
  the token's process.

The run copy adds what the adapter enforces regardless of the lane: dontAsk,
bypass and auto modes disabled, no project MCP servers, no git snapshot or
auto memory, and the fail-closed PreToolUse guard. It is written owner-read
only, for a read-only container mount. The model is selected by `--model`,
never by this file.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path


MODEL_REF = re.compile(r"^claude/claude-[a-z0-9][a-z0-9.-]*$")
# Kept identical to the RULE expression in tool-guard.mjs.
RULE = re.compile(r"^(Read|Edit)\(([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*)(/\*\*)?\)$")
TOP_LEVEL_KEYS = {"$schema", "permissions"}
PERMISSION_KEYS = {"allow", "deny"}
BASELINE_DENY = (
    "Bash",
    "Task",
    "WebFetch",
    "WebSearch",
    "NotebookEdit",
    "Skill",
    "mcp__*",
    "Read(//proc/**)",
    "Read(~/**)",
    "Read(.git/**)",
    "Edit(.git/**)",
    "Edit(.github/**)",
)
# Container paths owned by .github/actions/run-claude-container/action.yml.
CONTAINER_SETTINGS = "/tmp/claude-config/settings.json"
CONTAINER_GUARD = "/opt/ara-claude/tool-guard.mjs"
CONTAINER_WORKSPACE = "/workspace"
GUARD_COMMAND = (
    f"node {CONTAINER_GUARD} {CONTAINER_SETTINGS} {CONTAINER_WORKSPACE} || exit 2"
)


def validate(config: object) -> tuple[dict, str]:
    """Return the run-scoped settings and the comma-separated --tools list."""
    if not isinstance(config, dict):
        raise ValueError("Claude lane policy must be a JSON object")
    unknown = sorted(set(config) - TOP_LEVEL_KEYS)
    if unknown:
        raise ValueError(f"Claude lane policy has unsupported keys: {', '.join(unknown)}")
    permissions = config.get("permissions")
    if not isinstance(permissions, dict):
        raise ValueError("Claude lane policy must define a permissions object")
    unknown = sorted(set(permissions) - PERMISSION_KEYS)
    if unknown:
        raise ValueError(
            f"Claude lane permissions have unsupported keys: {', '.join(unknown)}"
        )
    allow = permissions.get("allow", [])
    deny = permissions.get("deny")
    if not isinstance(allow, list) or not all(isinstance(rule, str) for rule in allow):
        raise ValueError("permissions.allow must be a list of strings")
    if not isinstance(deny, list) or not all(isinstance(rule, str) for rule in deny):
        raise ValueError("permissions.deny must be a list of strings")

    kinds: set[str] = set()
    for rule in allow:
        match = RULE.fullmatch(rule)
        if not match:
            raise ValueError(
                f"unsupported allow rule {rule!r}: only Read(path) and Edit(path) on "
                "clean workspace-relative paths are allowed"
            )
        if any(part in {".", ".."} for part in match.group(2).split("/")):
            raise ValueError(f"allow rule {rule!r} traverses directories")
        kinds.add(match.group(1))
    if len(set(allow)) != len(allow):
        raise ValueError("permissions.allow has duplicate rules")
    missing = [rule for rule in BASELINE_DENY if rule not in deny]
    if missing:
        raise ValueError(f"permissions.deny lacks baseline rules: {', '.join(missing)}")

    tools = []
    if "Read" in kinds:
        tools.append("Read")
    if "Edit" in kinds:
        tools.extend(("Write", "Edit"))

    settings = {
        "permissions": {
            "allow": list(allow),
            "deny": list(deny),
            "defaultMode": "dontAsk",
            "disableBypassPermissionsMode": "disable",
            "disableAutoMode": "disable",
        },
        "hooks": {
            "PreToolUse": [{
                "matcher": "*",
                "hooks": [{"type": "command", "command": GUARD_COMMAND, "timeout": 30}],
            }],
        },
        "disableAllHooks": False,
        "enableAllProjectMcpServers": False,
        "includeGitInstructions": False,
        "autoMemoryEnabled": False,
    }
    return settings, ",".join(tools)


def copy_settings(source: Path, destination: Path, model_ref: str) -> str:
    if not MODEL_REF.fullmatch(model_ref):
        raise ValueError("model must be one canonical claude/<model> ref")
    settings, tools = validate(json.loads(source.read_text(encoding="utf-8")))
    temporary = destination.with_name(destination.name + ".tmp")
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(settings, handle, sort_keys=True, indent=2)
            handle.write("\n")
        os.replace(temporary, destination)
    except Exception:
        if temporary.exists():
            temporary.unlink()
        raise
    return tools


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("model_ref")
    args = parser.parse_args()
    print(copy_settings(args.source, args.destination, args.model_ref))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
