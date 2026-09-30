#!/usr/bin/env python3
"""Check isolation, integrity, and shared Claude-action Bun wiring."""

import hashlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import yaml

import install_agent_bun as installer


class AgentBunInstallTest(unittest.TestCase):
    def archive(self, version="1.3.14"):
        output = io.BytesIO()
        with zipfile.ZipFile(output, "w") as archive:
            archive.writestr("bun-linux-x64/bun", f"#!/bin/sh\necho {version}\n")
            archive.writestr("../../must-not-extract", "unselected archive entry")
        return output.getvalue()

    def pins(self, archive):
        return {"version": "1.3.14", "sha256": {
            "linux_x64": hashlib.sha256(archive).hexdigest(), "linux_aarch64": "0" * 64,
        }}

    def install(self, root, archive, pins=None):
        with patch.object(installer.platform, "system", return_value="Linux"), \
             patch.object(installer.platform, "machine", return_value="x86_64"), \
             patch.object(installer.urllib.request, "urlopen", return_value=io.BytesIO(archive)) as download:
            binary = installer.install_bun(pins or self.pins(archive), root)
        self.assertEqual(download.call_args.args[0].full_url,
                         "https://github.com/oven-sh/bun/releases/download/bun-v1.3.14/bun-linux-x64.zip")
        return binary

    def test_verified_installs_use_distinct_directories_and_only_expected_member(self):
        with tempfile.TemporaryDirectory(prefix="agent bun ") as temp:
            root = Path(temp)
            archive = self.archive()
            first = self.install(root, archive)
            first_content = first.read_bytes()
            second = self.install(root, archive)
            self.assertNotEqual(first.parent, second.parent)
            self.assertEqual(first.parent.parent, root)
            self.assertEqual(first.read_bytes(), first_content)
            self.assertTrue(first.stat().st_mode & 0o111)
            self.assertEqual((first.parent / "bunx").resolve(), first.resolve())
            self.assertEqual({p.name for p in first.parent.iterdir()}, {"bun", "bunx"})
            self.assertFalse((root / "must-not-extract").exists())

    def test_bad_checksum_fails_before_extracting_or_executing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive = self.archive()
            pins = self.pins(archive)
            pins["sha256"]["linux_x64"] = "0" * 64
            with patch.object(installer.subprocess, "run") as execute:
                with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                    self.install(root, archive, pins)
                execute.assert_not_called()
            self.assertEqual(list(root.iterdir()), [])

    def test_runtime_version_must_match_and_failure_removes_only_its_install(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            keep = root / "another-job"
            keep.mkdir()
            with self.assertRaisesRegex(ValueError, "did not report pinned version"):
                self.install(root, self.archive("1.4.2"))
            self.assertEqual(list(root.iterdir()), [keep])

    def test_unsupported_architecture_fails_before_downloading(self):
        with patch.object(installer.platform, "system", return_value="Linux"), \
             patch.object(installer.platform, "machine", return_value="unsupported"), \
             patch.object(installer.urllib.request, "urlopen") as download:
            with self.assertRaisesRegex(ValueError, "Linux x64/aarch64"):
                installer.install_bun(self.pins(self.archive()), Path("/unused"))
            download.assert_not_called()

    def test_all_shared_claude_invocations_bypass_global_bun_setup(self):
        action = yaml.load((installer.ROOT / ".github/actions/agent-run/action.yml").read_text(),
                           Loader=yaml.BaseLoader)
        steps = action["runs"]["steps"]
        setup = next(step for step in steps if step.get("id") == "bun")
        self.assertEqual(setup["if"], "steps.select.outputs.adapter == 'agent-run'")
        self.assertEqual(setup["run"], 'python3 scripts/install_agent_bun.py --github-output "$GITHUB_OUTPUT"')
        callers = [step for step in steps
                   if step.get("uses", "").startswith("anthropics/claude-code-action@")]
        self.assertEqual({step["id"] for step in callers}, {
            "run-claude", "run-claude-bots", "run-zai", "run-zai-bots", "run-fireworks",
            "run-fireworks-bots", "run-zai-fallback", "run-zai-fallback-bots",
        })
        for step in callers:
            self.assertLess(steps.index(setup), steps.index(step))
            self.assertEqual(step["with"]["path_to_bun_executable"], "${{ steps.bun.outputs.bun-path }}")


if __name__ == "__main__":
    unittest.main()
