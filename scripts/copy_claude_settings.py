#!/usr/bin/env python3
"""Validate a trusted per-lane Claude Code policy and materialize its run copy.

The committed `.github/claude/<lane>.json` is an ordinary Claude Code settings
file, limited to a reviewable subset:

* `permissions.allow` is the lane's whole capability, in a closed grammar:
  - `Read(path)` / `Edit(path)` on clean workspace-relative paths, optionally
    ending in `/**`. Read rules expose Read; Edit rules expose Write only.
  - `Glob`, which exposes Glob for listing directories under a Read rule.
  - `Bash(git add <dir>/*)`, which stages paths under <dir>; the lane must
    also hold `Edit(<dir>/**)`, so it can only stage what it may write.
  - `Bash(git commit -m *)`, a plain `git commit -m "<message>"`.
  - `Bash(curl -sL "https://<host>/<path>?*)` (or `-s`), one fixed URL
    prefix; the query may not carry a shell metacharacter.
  - `Bash(uv run python scripts/<name>.py)`, the same with one fixed
    `--flag`, or with ` "*` for one quoted plain-text argument: an existing
    repository script and nothing else.
  These rules decide the `--tools` list this script prints and the exact
  allowlist that `.github/actions/run-claude-container/tool-guard.mjs`
  enforces; any Bash command not in one of these forms is refused, and
  Claude Code's dontAsk mode alone would still allow any read in the working
  directory. The Edit tool is never exposed: it checks `old_string` against
  the target file before any hook runs, so even a denied Edit answers "not
  found" or "Found N matches", a substring oracle over every readable file.
  Write carries no such pre-hook check of file contents.
* `permissions.deny` must keep the baseline below, so no lane file can drop a
  tool that runs code, reaches the network, delegates to a subagent, or reads
  the token's process. A lane with Bash rules needs the Bash tool itself, so
  its baseline is the same minus the bare `Bash` deny.

The run copy adds what the adapter enforces regardless of the lane: dontAsk,
bypass and auto modes disabled, no project MCP servers, no git snapshot or
auto memory, the PreToolUse guard, and a SessionStart liveness hook. Under
`-p`, Claude Code silently drops a settings file it cannot parse, guard and
all, so the adapter runs `claude --init-only` first and refuses to start the
model unless the liveness hook left its marker. It is written owner-read
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
# Kept identical to the RULE, GIT_ADD_RULE, CURL_RULE and UV_RULE expressions
# in tool-guard.mjs; scripts/test_claude_tool_guard.py compares them.
RULE = re.compile(r"^(Read|Edit)\(([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*)(/\*\*)?\)$")
GIT_ADD_RULE = re.compile(r"^Bash\(git add ([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*)/\*\)$")
GIT_COMMIT_RULE = "Bash(git commit -m *)"
CURL_RULE = re.compile(
    r'^Bash\(curl (-sL|-s) "(https://[a-z0-9]+(?:[.-][a-z0-9]+)*\.[a-z]{2,}'
    r'(?:/[A-Za-z0-9_.-]+)*/?\?)\*\)$'
)
UV_RULE = re.compile(r'^Bash\((uv run python scripts/([a-z0-9_]+)\.py)( --[a-z][a-z-]*| "\*)?\)$')
GLOB_RULE = "Glob"
SCRIPTS_DIR = Path(__file__).resolve().parent
TOP_LEVEL_KEYS = {"$schema", "permissions"}
PERMISSION_KEYS = {"allow", "deny"}
BASELINE_DENY = (
    "Bash",
    "Task",
    "Agent",
    "WebFetch",
    "WebSearch",
    "NotebookEdit",
    "Skill",
    "mcp__*",
    "Read(//proc/**)",
    "Read(//dev/**)",
    "Read(//tmp/**)",
    "Read(~/**)",
    "Read(.git/**)",
    "Edit(.git/**)",
    "Edit(.github/**)",
)
# A lane that runs git, curl, or uv needs the Bash tool itself; tool-guard.mjs
# then admits only the exact command forms its allow rules describe.
SHELL_BASELINE_DENY = tuple(rule for rule in BASELINE_DENY if rule != "Bash")
# Container paths owned by .github/actions/run-claude-container/action.yml.
CONTAINER_SETTINGS = "/tmp/claude-config/settings.json"
CONTAINER_GUARD = "/opt/ara-claude/tool-guard.mjs"
CONTAINER_WORKSPACE = "/workspace"
GUARD_COMMAND = (
    f"node {CONTAINER_GUARD} {CONTAINER_SETTINGS} {CONTAINER_WORKSPACE} || exit 2"
)
# Claude Code 2.1.285 lets a call PROCEED when it kills a hook that ran past
# its timeout (and when a signal kills the hook shell): `|| exit 2` only maps
# exit codes. The guard finishes in tens of milliseconds, so allow it far more
# time than it can need rather than leave a timeout an attacker could aim for.
GUARD_TIMEOUT_SECONDS = 600
# Claude Code 2.1.285 saves a Bash result longer than this to a file under
# HOME and hands the model only a preview and the path, which the guard never
# lets it read. 128000 is the CLI's ceiling; past it a lane pages (an API page
# with fewer results, a narrower query).
BASH_OUTPUT_MAX_CHARS = 128000
CONTAINER_LIVENESS_MARKER = "/tmp/claude-liveness/session-start"
LIVENESS_COMMAND = f"touch {CONTAINER_LIVENESS_MARKER}"


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
    edit_prefixes: set[str] = set()
    git_add_dirs: list[str] = []
    for rule in allow:
        if rule == GLOB_RULE or rule == GIT_COMMIT_RULE:
            kinds.add(rule)
            continue
        match = RULE.fullmatch(rule)
        git_add = GIT_ADD_RULE.fullmatch(rule)
        curl = CURL_RULE.fullmatch(rule)
        uv = UV_RULE.fullmatch(rule)
        if match:
            target = match.group(2)
            kinds.add(match.group(1))
            if match.group(1) == "Edit" and match.group(3):
                edit_prefixes.add(target)
        elif git_add:
            target = git_add.group(1)
            git_add_dirs.append(target)
            kinds.add("git add")
        elif curl:
            target = curl.group(2).removeprefix("https://").removesuffix("?")
            kinds.add("curl")
        elif uv:
            target = ""
            script = SCRIPTS_DIR / f"{uv.group(2)}.py"
            if not script.is_file() or script.is_symlink():
                raise ValueError(f"allow rule {rule!r} names no repository script")
            kinds.add("uv")
        else:
            raise ValueError(
                f"unsupported allow rule {rule!r}: see the closed grammar in this "
                "script's docstring"
            )
        if any(part in {".", ".."} for part in target.split("/")):
            raise ValueError(f"allow rule {rule!r} traverses directories")
    if len(set(allow)) != len(allow):
        raise ValueError("permissions.allow has duplicate rules")
    for directory in git_add_dirs:
        if directory not in edit_prefixes:
            raise ValueError(
                f"Bash(git add {directory}/*) needs Edit({directory}/**): a lane may "
                "only stage what it may write"
            )
    if GIT_COMMIT_RULE in kinds and "git add" not in kinds:
        raise ValueError(f"{GIT_COMMIT_RULE} needs a Bash(git add <dir>/*) rule")
    if GLOB_RULE in kinds and "Read" not in kinds:
        raise ValueError("Glob needs a Read(path) rule to list under")
    shell = bool({"git add", GIT_COMMIT_RULE, "curl", "uv"} & kinds)
    baseline = SHELL_BASELINE_DENY if shell else BASELINE_DENY
    missing = [rule for rule in baseline if rule not in deny]
    if missing:
        raise ValueError(f"permissions.deny lacks baseline rules: {', '.join(missing)}")

    tools = []
    if "Read" in kinds:
        tools.append("Read")
    if "Edit" in kinds:
        tools.append("Write")
    if GLOB_RULE in kinds:
        tools.append("Glob")
    if shell:
        tools.append("Bash")
    # A bare deny removes the tool from the session entirely.
    removed = [tool for tool in tools if tool in deny]
    if removed:
        raise ValueError(f"permissions.deny removes tools the allow rules need: {', '.join(removed)}")

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
                "hooks": [{"type": "command", "command": GUARD_COMMAND,
                           "timeout": GUARD_TIMEOUT_SECONDS}],
            }],
            # Prints nothing, so nothing reaches the model's context. The
            # marker only proves the CLI loaded this file and runs its hooks.
            "SessionStart": [{
                "matcher": "*",
                "hooks": [{"type": "command", "command": LIVENESS_COMMAND, "timeout": 30}],
            }],
        },
        "disableAllHooks": False,
        "enableAllProjectMcpServers": False,
        "includeGitInstructions": False,
        "autoMemoryEnabled": False,
    }
    if shell:
        settings["bashOutputMaxChars"] = BASH_OUTPUT_MAX_CHARS
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
