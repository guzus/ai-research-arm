"""Behavioral tests for run-claude-container's PreToolUse path guard.

The guard is the only layer that narrows Claude Code's dontAsk default of
"any read inside the working directory", so these tests run the real script
with node against a real workspace. They fail, never skip, when node is
missing: a skipped containment test is a silent hole.
"""

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from copy_claude_settings import GUARD_COMMAND, RULE


REPO_ROOT = Path(__file__).resolve().parent.parent
GUARD = REPO_ROOT / ".github/actions/run-claude-container/tool-guard.mjs"
ALLOW = ["Read(.agent-input/aradio/**)", "Edit(.tmp/aradio/edit.json)"]


class ClaudeToolGuardTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.node = shutil.which("node")
        if cls.node is None:
            raise AssertionError("node is required to test the Claude tool guard")

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(os.path.realpath(self.tmp.name))
        self.workspace = root / "workspace"
        inbox = self.workspace / ".agent-input" / "aradio"
        (inbox / "transcripts").mkdir(parents=True)
        (inbox / "inbox.md").write_text("inbox\n", encoding="utf-8")
        (inbox / "transcripts" / "t1.txt").write_text("said\n", encoding="utf-8")
        (self.workspace / ".agent-input" / "aradio-evil").mkdir()
        (self.workspace / ".agent-input" / "aradio-evil" / "x").write_text("x", encoding="utf-8")
        (self.workspace / ".tmp").mkdir()
        (self.workspace / "CLAUDE.md").write_text("repo\n", encoding="utf-8")
        outside = root / "outside.txt"
        outside.write_text("secret\n", encoding="utf-8")
        os.symlink(outside, inbox / "link.txt")
        self.settings = root / "settings.json"
        self.write_settings(ALLOW)

    def write_settings(self, allow):
        self.settings.write_text(json.dumps({"permissions": {"allow": allow, "deny": []}}),
                                 encoding="utf-8")

    def run_guard(self, tool, tool_input=None, raw=None, workspace=None):
        payload = raw if raw is not None else json.dumps({
            "hook_event_name": "PreToolUse", "tool_name": tool,
            "tool_input": {} if tool_input is None else tool_input,
        })
        return subprocess.run(
            [self.node, str(GUARD), str(self.settings), str(workspace or self.workspace)],
            input=payload, text=True, capture_output=True, check=False)

    def assert_allowed(self, tool, file_path):
        result = self.run_guard(tool, {"file_path": file_path})
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("", result.stdout)

    def assert_denied(self, tool, tool_input=None, **kwargs):
        result = self.run_guard(tool, tool_input, **kwargs)
        self.assertEqual(2, result.returncode, (tool, tool_input, result.stderr))
        self.assertIn("ARA tool guard denied this call", result.stderr)

    def test_reads_only_inside_the_inbox(self):
        ws = self.workspace
        self.assert_allowed("Read", str(ws / ".agent-input/aradio/inbox.md"))
        self.assert_allowed("Read", str(ws / ".agent-input/aradio/transcripts/t1.txt"))
        self.assert_allowed("Read", ".agent-input/aradio/inbox.md")
        for path in (str(ws / "CLAUDE.md"), "/proc/self/environ", "/proc/1/environ",
                     "/etc/passwd", str(ws / ".agent-input/aradio/../../CLAUDE.md"),
                     str(ws / ".agent-input/aradio-evil/x"), str(ws / ".agent-input/aradio"),
                     str(ws / ".agent-input/aradio/missing.md"), str(ws / ".tmp/aradio/edit.json")):
            with self.subTest(path=path):
                self.assert_denied("Read", {"file_path": path})

    def test_symlinks_never_cross_the_allowlist(self):
        self.assert_denied("Read", {"file_path": str(self.workspace / ".agent-input/aradio/link.txt")})
        linked_root = Path(self.tmp.name) / "workspace-link"
        os.symlink(self.workspace, linked_root)
        self.assert_denied("Read", {"file_path": str(linked_root / ".agent-input/aradio/inbox.md")})
        self.assert_denied("Read", {"file_path": ".agent-input/aradio/inbox.md"},
                           workspace=linked_root)

    def test_writes_only_the_declared_artifact(self):
        ws = self.workspace
        # The parent directory does not exist yet; the Write tool creates it.
        self.assert_allowed("Write", str(ws / ".tmp/aradio/edit.json"))
        self.assert_allowed("Edit", str(ws / ".tmp/aradio/edit.json"))
        for path in (str(ws / ".tmp/aradio/other.json"), str(ws / ".tmp/edit.json"),
                     str(ws / "research/aradio/state.json"), str(ws / ".agent-input/aradio/inbox.md"),
                     str(ws / ".git/config"), str(ws / ".tmp/aradio/edit.json/x"),
                     str(ws / ".tmp/aradio/../aradio/../../CLAUDE.md"), "/tmp/edit.json"):
            with self.subTest(path=path):
                self.assert_denied("Write", {"file_path": path, "content": "{}"})

    def test_writes_refuse_links_and_non_files(self):
        artifact_dir = self.workspace / ".tmp" / "aradio"
        artifact_dir.mkdir()
        target = Path(self.tmp.name) / "elsewhere.json"
        os.symlink(target, artifact_dir / "edit.json")
        self.assert_denied("Write", {"file_path": str(artifact_dir / "edit.json")})
        (artifact_dir / "edit.json").unlink()
        (artifact_dir / "edit.json").mkdir()
        self.assert_denied("Write", {"file_path": str(artifact_dir / "edit.json")})
        (artifact_dir / "edit.json").rmdir()
        shutil.rmtree(self.workspace / ".tmp")
        os.symlink(Path(self.tmp.name), self.workspace / ".tmp")
        self.assert_denied("Write", {"file_path": str(self.workspace / ".tmp/aradio/edit.json")})

    def test_every_other_tool_is_refused(self):
        for tool, tool_input in (("Bash", {"command": "env"}), ("WebFetch", {"url": "https://x"}),
                                 ("WebSearch", {"query": "x"}), ("Task", {"prompt": "x"}),
                                 ("Glob", {"pattern": "**"}), ("Grep", {"pattern": "x"}),
                                 ("NotebookEdit", {"notebook_path": "x"}),
                                 ("mcp__evil__steal", {}), ("constructor", {}),
                                 ("__proto__", {}), ("", {})):
            with self.subTest(tool=tool):
                self.assert_denied(tool, tool_input)

    def test_malformed_input_and_policy_fail_closed(self):
        self.assert_denied("Read", raw="not json")
        self.assert_denied("Read", raw=json.dumps({"tool_name": "Read"}))
        self.assert_denied("Read", {"file_path": 7})
        self.assert_denied("Read", {"file_path": ""})
        self.assert_denied("Read", {"file_path": "inbox\u0000.md"})
        for allow in (["Bash(env)"], ["Read(//proc/**)"], ["Read(.agent-input/../x/**)"], "x"):
            with self.subTest(allow=allow):
                self.write_settings(allow)
                self.assert_denied("Read", {"file_path": str(self.workspace / ".agent-input/aradio/inbox.md")})
        self.settings.write_text("{", encoding="utf-8")
        self.assert_denied("Read", {"file_path": str(self.workspace / ".agent-input/aradio/inbox.md")})

    def test_hook_command_blocks_when_the_guard_cannot_run(self):
        command = GUARD_COMMAND.replace("node ", "/nonexistent/node ", 1)
        result = subprocess.run(["sh", "-c", command], input="{}", text=True,
                                capture_output=True, check=False)
        self.assertEqual(2, result.returncode)

    def test_rule_grammar_matches_the_settings_copier(self):
        source = GUARD.read_text(encoding="utf-8")
        match = re.search(r"^const RULE = /(.*)/;$", source, re.MULTILINE)
        self.assertIsNotNone(match)
        self.assertEqual(RULE.pattern, match.group(1).replace("\\/", "/"))


if __name__ == "__main__":
    unittest.main()
