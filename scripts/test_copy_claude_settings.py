import copy
import json
import tempfile
import unittest
from pathlib import Path

from copy_claude_settings import (
    BASELINE_DENY,
    CONTAINER_LIVENESS_MARKER,
    GUARD_COMMAND,
    GUARD_TIMEOUT_SECONDS,
    LIVENESS_COMMAND,
    copy_settings,
    validate,
)


REPO_ROOT = Path(__file__).resolve().parent.parent
ARADIO = json.loads((REPO_ROOT / ".github/claude/aradio.json").read_text(encoding="utf-8"))
CANARY = json.loads((REPO_ROOT / ".github/claude/canary.json").read_text(encoding="utf-8"))


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
