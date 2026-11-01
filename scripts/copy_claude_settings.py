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
  - `Bash(curl -q -s "https://<host>/<path>?*)`, one fixed URL prefix on a
    host in CURL_HOSTS; the query may not carry a shell metacharacter. `-q`
    comes first, so curl reads no curlrc, and there is no `-L`: curl never
    follows a redirect off that host.
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

With `--addendum PATH` it also writes the prompt addendum: the admitted forms
as text, which the adapter appends to the lane prompt so the commands a model
is told to run come from the same rules the guard enforces.
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
    r'^Bash\(curl -q -s "(https://[a-z0-9]+(?:[.-][a-z0-9]+)*\.[a-z]{2,}'
    r'(?:/[A-Za-z0-9_.-]+)*/?\?)\*\)$'
)
UV_RULE = re.compile(r'^Bash\((uv run python scripts/([a-z0-9_]+)\.py)( --[a-z][a-z-]*| "\*)?\)$')
# The only hosts a curl rule may name, kept identical to CURL_HOSTS in
# tool-guard.mjs: reaching a new host is a reviewed code change, never a
# policy edit alone.
CURL_HOSTS = ("export.arxiv.org",)
# The page-size and offset parameters that keep a pinned host's reply under
# BASH_OUTPUT_MAX_CHARS, and the largest page that fits: about 2.5 KB per arXiv
# entry, so 40 fit (measured 2026-10-31: 100 entries came to 248.6 KB).
CURL_PAGE_LIMITS = {"export.arxiv.org": ("max_results", "start", 40)}
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
# The guard appends one "<tool>\t<reason code>" line per refusal here, never an
# input or a path; the host prints the counts in its typed result summary.
CONTAINER_GUARD_DENIALS = "/workspace/.claude-guard-denials.tsv"
GUARD_COMMAND = (
    f"node {CONTAINER_GUARD} {CONTAINER_SETTINGS} {CONTAINER_WORKSPACE} "
    f"{CONTAINER_GUARD_DENIALS} || exit 2"
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
    read_prefixes: set[str] = set()
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
            if match.group(1) == "Read" and match.group(3):
                read_prefixes.add(target)
        elif git_add:
            target = git_add.group(1)
            git_add_dirs.append(target)
            kinds.add("git add")
        elif curl:
            target = curl.group(1).removeprefix("https://").removesuffix("?")
            host = target.split("/", 1)[0]
            if host not in CURL_HOSTS:
                raise ValueError(f"allow rule {rule!r} names curl host {host!r}, which is not "
                                 "in CURL_HOSTS")
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
    if GLOB_RULE in kinds and not read_prefixes:
        raise ValueError("Glob needs a Read(<dir>/**) rule to list under: the guard lists "
                         "only directories under a Read prefix")
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


def addendum(allow: list[str]) -> str:
    """The exact forms a validated policy admits, as text for the lane prompt.

    The adapter appends it to every prompt, so the commands a model is told to
    run come from the same rules the guard enforces and cannot drift from them.
    A policy without tools gets no text.
    """
    reads: list[str] = []
    writes: list[str] = []
    stage_dirs: list[str] = []
    fetches: list[str] = []
    runs: list[str] = []
    glob = commit = False
    for rule in allow:
        if rule == GLOB_RULE:
            glob = True
        elif rule == GIT_COMMIT_RULE:
            commit = True
        elif match := RULE.fullmatch(rule):
            shown = match.group(2) + ("/" if match.group(3) else "")
            (reads if match.group(1) == "Read" else writes).append(shown)
        elif match := GIT_ADD_RULE.fullmatch(rule):
            stage_dirs.append(match.group(1) + "/")
        elif match := CURL_RULE.fullmatch(rule):
            fetches.append(match.group(1))
        elif match := UV_RULE.fullmatch(rule):
            suffix = match.group(3) or ""
            runs.append(match.group(1) + (' "<text>"' if suffix == ' "*' else suffix))
    if not (reads or writes or glob or stage_dirs or commit or fetches or runs):
        return ""

    def paths(items: list[str]) -> str:
        return ", ".join(f"`{item}`" for item in items)

    lines = ["## Sandbox tools", "",
             "This run is sandboxed. A guard refuses every tool call outside these forms, "
             "so use them exactly.", ""]
    if reads:
        lines.append(f"- Read files only at or under: {paths(reads)}.")
    if writes:
        lines.append(f"- Write files only at or under: {paths(writes)}. Read an existing "
                     "file before you replace it.")
    if glob:
        # validate() requires a Read directory for Glob; an unvalidated list
        # without one still gets the rule, just no example directory.
        example = next((item.rstrip("/") for item in reads if item.endswith("/")), None)
        lines.append("- Glob lists a directory under a Read path; use it instead of `ls` or "
                     "`find`. Give `path`" + (f" (for example `{example}`)" if example else "")
                     + " and a plain `pattern` such as `*` or `*.md`; no braces, `[...]` "
                     "classes or `..`.")
    shell = stage_dirs or commit or fetches or runs
    if shell:
        lines.append("- Bash runs one command per call, on one line, in the foreground, and "
                     "only these forms:")
        if stage_dirs:
            lines.append(f"  - `git add <path>`, with one or more paths, each under "
                         f"{' or '.join(f'`{item}`' for item in stage_dirs)}")
        if commit:
            lines.append('  - `git commit -m "<message>"`, optionally followed by '
                         '`|| echo "No changes"`; the message may use only letters, digits, '
                         "spaces and `:._,()#+/@-`")
            if stage_dirs:
                lines.append('  - `git add <path> && git commit -m "<message>"`')
        for prefix in fetches:
            lines.append(f'  - `curl -q -s "{prefix}<query>"`; the query may use only letters, '
                         "digits and `_=&+:.%,()/@-`, and nothing may follow the closing quote")
        for run in runs:
            lines.append(f"  - `{run}`" + ("; the text may use only letters, digits, spaces "
                                          "and `._,:()/+'-`" if run.endswith('"<text>"') else ""))
        lines.append("- Nothing else runs in Bash: no pipes, redirects, `;`, `$(...)`, "
                     "backticks, `cd`, `ls`, `cat`, `python` or other programs.")
        hints = []
        for host, (size, offset, limit) in CURL_PAGE_LIMITS.items():
            if any(prefix.startswith(f"https://{host}/") for prefix in fetches):
                hints.append(f"For `{host}` ask for `{size}={limit}` or fewer and page with "
                             f"`{offset}=0`, `{offset}={limit}`, `{offset}={2 * limit}`.")
        lines.append(f"- Bash output over {BASH_OUTPUT_MAX_CHARS} characters is not shown; it "
                     "is saved where you cannot read it. Ask for less per call."
                     + "".join(f" {hint}" for hint in hints))
    missing = ["Edit", "WebFetch", "WebSearch", "Grep"] + ([] if glob else ["Glob"])
    lines.append(f"- There is no {', '.join(missing)} or subagent tool"
                 + ("." if shell else ", and no Bash: no `ls`, `git`, `curl` or other "
                    "commands."))
    return "\n".join(lines) + "\n"


def write_once(path: Path, text: str) -> None:
    """Write an owner-read-only file through a fresh sibling, then rename it."""
    temporary = path.with_name(path.name + ".tmp")
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
        os.replace(temporary, path)
    except Exception:
        if temporary.exists():
            temporary.unlink()
        raise


def copy_settings(source: Path, destination: Path, model_ref: str,
                  addendum_path: Path | None = None) -> str:
    if not MODEL_REF.fullmatch(model_ref):
        raise ValueError("model must be one canonical claude/<model> ref")
    policy = json.loads(source.read_text(encoding="utf-8"))
    settings, tools = validate(policy)
    write_once(destination, json.dumps(settings, sort_keys=True, indent=2) + "\n")
    if addendum_path is not None:
        write_once(addendum_path, addendum(policy["permissions"].get("allow", [])))
    return tools


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("model_ref")
    parser.add_argument("--addendum", type=Path, default=None,
                        help="also write the prompt addendum that lists the admitted forms")
    args = parser.parse_args()
    print(copy_settings(args.source, args.destination, args.model_ref, args.addendum))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
