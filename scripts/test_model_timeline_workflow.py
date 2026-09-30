#!/usr/bin/env python3
"""Exercise the model lane's input isolation and fail-closed publication gate."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml


ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = ROOT / ".github/workflows/24h-model-timeline.yml"


class ModelTimelineWorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        workflow = yaml.load(WORKFLOW.read_text(), Loader=yaml.BaseLoader)
        cls.steps = {step["name"]: step for step in workflow["jobs"]["model-timeline"]["steps"]}

    def run_step(self, name: str, env: dict[str, str], cwd: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["bash", "-e", "-o", "pipefail", "-c", self.steps[name]["run"]],
            env={**os.environ, **env}, cwd=cwd, text=True, capture_output=True,
        )

    def test_each_run_reads_only_its_own_fetches(self) -> None:
        with tempfile.TemporaryDirectory(prefix="model input ") as temp:
            root = Path(temp)
            output = root / "outputs"
            stale = root / "all.json"
            stale.write_text('[{"text":"unrelated hourly-twitter input"}]')
            # The fetch CLI is stubbed; execute the workflow's real shell blocks.
            birdy = root / "birdy"
            birdy.write_text('#!/bin/sh\nprintf \'[{"text":"fresh model signal"}]\\n\'\n')
            birdy.chmod(0o755)
            env = {"RUNNER_TEMP": str(root), "GITHUB_OUTPUT": str(output),
                   "PATH": str(root) + os.pathsep + os.environ["PATH"]}
            directories = []
            for _ in range(2):
                result = self.run_step("Prepare model signal directory", env, root)
                self.assertEqual(result.returncode, 0, result.stderr)
                directory = Path(output.read_text().splitlines()[-1].split("=", 1)[1])
                directories.append(directory)
                self.assertEqual(list(directory.iterdir()), [])
                for name in ("Fetch tweets from company accounts", "Fetch tweets from key execs",
                             "Search for model release tweets"):
                    step = self.steps[name]
                    self.assertEqual(step["env"]["MODEL_SIGNAL_DIR"],
                                     "${{ steps.model-signal.outputs.directory }}")
                    result = self.run_step(name, {**env, "MODEL_SIGNAL_DIR": str(directory)}, root)
                    self.assertEqual(result.returncode, 0, result.stderr)
                files = list(directory.glob("*.json"))
                self.assertEqual(len(files), 24)
                self.assertTrue(all(json.loads(path.read_text()) ==
                                    [{"text": "fresh model signal"}] for path in files))
            self.assertNotEqual(*directories)
            self.assertEqual(json.loads(stale.read_text())[0]["text"],
                             "unrelated hourly-twitter input")
            prompt = self.steps["CRUD model tickets via Claude"]["with"]["prompt"]
            self.assertIn("${{ steps.model-signal.outputs.directory }}/*.json", prompt)
            self.assertIn("Read only the JSON files in the RAW SIGNAL directory", prompt)

    def test_failed_author_cannot_become_a_no_change_publication(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            # Failures may leave real work behind; the outcome gate must not
            # transform it into an apparently fresh, successful publication.
            partial = root / "partial-ticket.md"
            partial.write_text("unvalidated model edit")
            for outcome in ("failure", "cancelled", "skipped"):
                with self.subTest(outcome=outcome):
                    result = self.run_step("Inspect Claude outcome", {"OUTCOME": outcome}, root)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("Partial output will not be published", result.stdout)
                    self.assertEqual(list(root.iterdir()), [partial])
            result = self.run_step("Inspect Claude outcome", {"OUTCOME": "success"}, root)
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("Deterministic model timeline fallback", self.steps)
        for name in ("Require model output", "Push changes"):
            self.assertEqual(self.steps[name]["if"],
                             "success() && steps.crud.outcome == 'success'")
        self.assertEqual(self.steps["Publish Hooker workflow telemetry"]["if"], "always()")


if __name__ == "__main__":
    unittest.main()
