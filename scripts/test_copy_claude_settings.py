import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import copy_claude_settings
from copy_claude_settings import (
    BASELINE_DENY,
    BASH_OUTPUT_MAX_CHARS,
    CONTAINER_LIVENESS_MARKER,
    GUARD_COMMAND,
    GUARD_TIMEOUT_SECONDS,
    LIVENESS_COMMAND,
    SHELL_BASELINE_DENY,
    copy_settings,
    validate,
)


REPO_ROOT = Path(__file__).resolve().parent.parent


def load(name):
    return json.loads((REPO_ROOT / f".github/claude/{name}.json").read_text(encoding="utf-8"))


ARADIO = load("aradio")
CANARY = load("canary")


class CopyClaudeSettingsTest(unittest.TestCase):
    def test_aradio_policy_is_read_inbox_write_one_file(self):
        settings, tools = validate(ARADIO)
        # Edit rules expose Write only: the Edit tool checks old_string
        # against its target before any hook runs (a substring oracle).
        self.assertEqual("Read,Write", tools)
        self.assertEqual(["Read(.agent-input/aradio/**)", "Edit(.tmp/aradio/edit.json)"],
                         settings["permissions"]["allow"])
        for rule in BASELINE_DENY:
            self.assertIn(rule, settings["permissions"]["deny"])
        # Write(path) rules never match in Claude Code; Edit rules govern Write.
        self.assertFalse(any(rule.startswith("Write(") for rule in
                             settings["permissions"]["allow"] + settings["permissions"]["deny"]))

    def test_canary_policy_exposes_no_tools(self):
        settings, tools = validate(CANARY)
        self.assertEqual("", tools)
        self.assertEqual([], settings["permissions"]["allow"])

    def test_run_copy_adds_the_adapter_enforcement(self):
        settings, _ = validate(ARADIO)
        permissions = settings["permissions"]
        self.assertEqual("dontAsk", permissions["defaultMode"])
        self.assertEqual("disable", permissions["disableBypassPermissionsMode"])
        self.assertEqual("disable", permissions["disableAutoMode"])
        self.assertIs(False, settings["disableAllHooks"])
        self.assertIs(False, settings["enableAllProjectMcpServers"])
        self.assertIs(False, settings["includeGitInstructions"])
        self.assertIs(False, settings["autoMemoryEnabled"])
        self.assertNotIn("env", settings)
        self.assertNotIn("apiKeyHelper", settings)
        self.assertEqual({"PreToolUse", "SessionStart"}, set(settings["hooks"]))
        hooks = settings["hooks"]["PreToolUse"]
        self.assertEqual(1, len(hooks))
        self.assertEqual("*", hooks[0]["matcher"])
        self.assertEqual([{"type": "command", "command": GUARD_COMMAND,
                           "timeout": GUARD_TIMEOUT_SECONDS}], hooks[0]["hooks"])
        # A crash or a missing interpreter must block, never allow; a killed
        # or timed-out hook lets the call proceed on 2.1.285, so the timeout
        # must dwarf the guard's runtime.
        self.assertTrue(GUARD_COMMAND.endswith("|| exit 2"))
        self.assertGreaterEqual(GUARD_TIMEOUT_SECONDS, 600)
        liveness = settings["hooks"]["SessionStart"]
        self.assertEqual([{"matcher": "*", "hooks": [
            {"type": "command", "command": LIVENESS_COMMAND, "timeout": 30}]}], liveness)
        self.assertEqual(f"touch {CONTAINER_LIVENESS_MARKER}", LIVENESS_COMMAND)

    def test_writes_owner_read_only_copy_and_prints_tools(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "aradio.json"
            destination = Path(tmp) / "settings.json"
            source.write_text(json.dumps(ARADIO), encoding="utf-8")
            tools = copy_settings(source, destination, "claude/claude-sonnet-5-5")
            self.assertEqual("Read,Write", tools)
            self.assertEqual(0o400, destination.stat().st_mode & 0o777)
            generated = json.loads(destination.read_text(encoding="utf-8"))
            self.assertNotIn("model", generated)
            self.assertEqual("dontAsk", generated["permissions"]["defaultMode"])

    def test_rejects_noncanonical_or_alias_model_refs(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "aradio.json"
            source.write_text(json.dumps(ARADIO), encoding="utf-8")
            for model_ref in ("claude-sonnet-5-5", "claude/sonnet", "cursor/claude-x",
                              "claude/claude-sonnet-5-5[1m]", "claude/../x", "claude/ x"):
                with self.subTest(model_ref=model_ref), self.assertRaises(ValueError):
                    copy_settings(source, Path(tmp) / "out.json", model_ref)

    def test_rejects_capabilities_outside_the_reviewable_subset(self):
        cases = {
            "bash allow": ("allow", "Bash(uv run *)"),
            "web allow": ("allow", "WebFetch(domain:example.com)"),
            "mcp allow": ("allow", "mcp__server__tool"),
            "write rule never matches": ("allow", "Write(.tmp/aradio/edit.json)"),
            "absolute path": ("allow", "Read(//proc/**)"),
            "settings-anchored path": ("allow", "Read(/.agent-input/**)"),
            "home path": ("allow", "Read(~/notes)"),
            "traversal": ("allow", "Read(.agent-input/../scripts/**)"),
            "dot segment": ("allow", "Read(./.agent-input/**)"),
            "inner glob": ("allow", "Read(.agent-input/*/inbox.md)"),
            "negation": ("allow", "Read(!.agent-input/**)"),
            "bare tool": ("allow", "Read"),
        }
        for name, (field, rule) in cases.items():
            policy = copy.deepcopy(ARADIO)
            policy["permissions"][field].append(rule)
            with self.subTest(name), self.assertRaises(ValueError):
                validate(policy)

    def test_baseline_closes_the_tmp_dev_and_subagent_gaps(self):
        # `~/...` targets land in /tmp, fd 3 lives under /dev, and newer CLIs
        # name the subagent tool Agent instead of Task.
        for rule in ("Read(//tmp/**)", "Read(//dev/**)", "Agent", "Task"):
            self.assertIn(rule, BASELINE_DENY)
        for policy in (ARADIO, CANARY):
            for rule in BASELINE_DENY:
                self.assertIn(rule, policy["permissions"]["deny"])

    def test_every_baseline_deny_is_required(self):
        for rule in BASELINE_DENY:
            policy = copy.deepcopy(ARADIO)
            policy["permissions"]["deny"].remove(rule)
            with self.subTest(rule=rule), self.assertRaisesRegex(ValueError, "baseline"):
                validate(policy)

    def test_rejects_unknown_keys_that_could_add_capability(self):
        for key, value in (("env", {"X": "1"}), ("hooks", {}), ("apiKeyHelper", "x"),
                           ("mcpServers", {}), ("enabledPlugins", {}), ("sandbox", {})):
            policy = copy.deepcopy(ARADIO)
            policy[key] = value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "unsupported keys"):
                validate(policy)
        for key, value in (("defaultMode", "bypassPermissions"), ("additionalDirectories", ["/"]),
                           ("ask", ["Read"])):
            policy = copy.deepcopy(ARADIO)
            policy["permissions"][key] = value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "unsupported keys"):
                validate(policy)

    def test_every_lane_policy_exposes_the_tools_its_rules_imply(self):
        expected = {"aradio": "Read,Write", "canary": "", "translation": "Read,Write",
                    "bluesky": "Read,Write,Glob", "rss": "Read,Write,Bash",
                    "community": "Read,Write,Bash", "arxiv": "Read,Write,Bash",
                    "wiki": "Read,Write,Glob,Bash"}
        self.assertEqual(set(expected),
                         {path.stem for path in (REPO_ROOT / ".github/claude").glob("*.json")})
        for name, tools in expected.items():
            with self.subTest(lane=name):
                settings, exposed = validate(load(name))
                self.assertEqual(tools, exposed)
                deny = settings["permissions"]["deny"]
                shell = "Bash" in tools.split(",")
                for rule in SHELL_BASELINE_DENY if shell else BASELINE_DENY:
                    self.assertIn(rule, deny)
                for tool in tools.split(",") if tools else []:
                    self.assertNotIn(tool, deny)
                if shell:
                    self.assertEqual(BASH_OUTPUT_MAX_CHARS, settings["bashOutputMaxChars"])
                else:
                    self.assertNotIn("bashOutputMaxChars", settings)
        self.assertEqual(128000, BASH_OUTPUT_MAX_CHARS)
        self.assertEqual([rule for rule in BASELINE_DENY if rule != "Bash"],
                         list(SHELL_BASELINE_DENY))

    def test_shell_rules_follow_the_closed_grammar(self):
        cases = {
            "git add anything": "Bash(git add *)",
            "git add of the root": "Bash(git add ./*)",
            "git add one file": "Bash(git add research/arxiv)",
            "git add traversal": "Bash(git add research/../scripts/*)",
            "git add option": "Bash(git add -f research/arxiv/*)",
            "git commit variant": "Bash(git commit *)",
            "git push": "Bash(git push *)",
            "git anything": "Bash(git *)",
            "curl over http": 'Bash(curl -sL "http://export.arxiv.org/api/query?*)',
            "curl without query": 'Bash(curl -sL "https://export.arxiv.org/api/query*)',
            "curl unquoted": "Bash(curl -sL https://export.arxiv.org/api/query?*)",
            "curl other flags": 'Bash(curl -sSL "https://export.arxiv.org/api/query?*)',
            "curl output flag": 'Bash(curl -o x "https://export.arxiv.org/api/query?*)',
            "curl ip host": 'Bash(curl -sL "https://127.0.0.1/api?*)',
            "curl userinfo": 'Bash(curl -sL "https://user@export.arxiv.org/api?*)',
            "curl port": 'Bash(curl -sL "https://export.arxiv.org:8443/api?*)',
            "curl traversal": 'Bash(curl -sL "https://export.arxiv.org/api/../x?*)',
            "curl any url": "Bash(curl *)",
            "uv anything": "Bash(uv run *)",
            "uv inline code": "Bash(uv run python -c *)",
            "uv free arguments": "Bash(uv run python scripts/check_wiki.py *)",
            "uv two flags": "Bash(uv run python scripts/check_wiki.py --lint --root)",
            "uv traversal": "Bash(uv run python scripts/../x.py)",
            "uv with": "Bash(uv run --with x python scripts/check_wiki.py)",
            "uvx": "Bash(uvx *)",
            "scoped glob": "Glob(.agent-input/**)",
            "grep": "Grep",
        }
        for name, rule in cases.items():
            policy = load("arxiv")
            policy["permissions"]["allow"].append(rule)
            with self.subTest(name), self.assertRaises(ValueError):
                validate(policy)
        policy = load("wiki")
        policy["permissions"]["allow"].append("Bash(uv run python scripts/no_such_script.py)")
        with self.assertRaisesRegex(ValueError, "names no repository script"):
            validate(policy)

    def test_uv_rules_name_only_regular_repository_scripts(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp)
            (scripts / "real.py").write_text("print(1)\n", encoding="utf-8")
            os.symlink(scripts / "real.py", scripts / "link.py")
            (scripts / "folder.py").mkdir()
            policy = load("wiki")
            with mock.patch.object(copy_claude_settings, "SCRIPTS_DIR", scripts):
                policy["permissions"]["allow"] = [
                    rule for rule in policy["permissions"]["allow"] if "uv run" not in rule
                ] + ["Bash(uv run python scripts/real.py)"]
                validate(policy)
                for name in ("link", "folder", "missing"):
                    bad = copy.deepcopy(policy)
                    bad["permissions"]["allow"].append(f"Bash(uv run python scripts/{name}.py)")
                    with self.subTest(name), self.assertRaisesRegex(ValueError, "no repository"):
                        validate(bad)

    def test_shell_and_listing_rules_need_their_file_rules(self):
        cases = (
            ("rss", "Edit(research/rss/**)", "needs Edit\\(research/rss/\\*\\*\\)"),
            ("rss", "Bash(git add research/rss/*)", "needs a Bash\\(git add"),
            ("arxiv", "Edit(research/summaries/**)", "needs Edit\\(research/summaries"),
            ("bluesky", "Read(.agent-input/bluesky/**)", "Glob needs a Read"),
        )
        for name, removed, message in cases:
            policy = load(name)
            policy["permissions"]["allow"].remove(removed)
            with self.subTest(lane=name, removed=removed), self.assertRaisesRegex(ValueError, message):
                validate(policy)
        # Staging needs the whole directory writable, not one file in it.
        policy = load("rss")
        allow = policy["permissions"]["allow"]
        allow[allow.index("Edit(research/rss/**)")] = "Edit(research/rss/2026-10-31.md)"
        with self.assertRaisesRegex(ValueError, "needs Edit"):
            validate(policy)

    def test_shell_lanes_keep_the_baseline_and_their_tools(self):
        for rule in SHELL_BASELINE_DENY:
            policy = load("rss")
            policy["permissions"]["deny"].remove(rule)
            with self.subTest(rule=rule), self.assertRaisesRegex(ValueError, "baseline"):
                validate(policy)
        for name, tool in (("rss", "Bash"), ("wiki", "Bash"), ("wiki", "Glob"),
                           ("bluesky", "Glob")):
            policy = load(name)
            policy["permissions"]["deny"].append(tool)
            with self.subTest(lane=name, tool=tool), self.assertRaisesRegex(ValueError, "removes tools"):
                validate(policy)

    def test_rejects_malformed_documents(self):
        for document in ([], "x", {"permissions": []}, {"permissions": {"allow": "Read(x)"}},
                         {"permissions": {"allow": [], "deny": "Bash"}},
                         {"permissions": {"allow": [1], "deny": list(BASELINE_DENY)}}):
            with self.subTest(document=document), self.assertRaises(ValueError):
                validate(document)
        policy = copy.deepcopy(ARADIO)
        policy["permissions"]["allow"].append(policy["permissions"]["allow"][0])
        with self.assertRaisesRegex(ValueError, "duplicate"):
            validate(policy)


if __name__ == "__main__":
    unittest.main()
