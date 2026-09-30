#!/usr/bin/env python3
"""Exercise the model lane's input isolation and fail-closed publication gate."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
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
            workspace = root / "workspace"
            workspace.mkdir()
            (workspace / ".gitignore").write_text((ROOT / ".gitignore").read_text())
            subprocess.run(["git", "init", "-q"], cwd=workspace, check=True)
            output = root / "outputs"
            stale = root / "all.json"
            stale.write_text('[{"text":"unrelated hourly-twitter input"}]')
            # The fetch CLI is stubbed; execute the workflow's real shell blocks.
            birdy = root / "birdy"
            birdy.write_text('#!/bin/sh\nprintf \'[{"text":"fresh model signal"}]\\n\'\n')
            birdy.chmod(0o755)
            env = {"RUNNER_TEMP": str(root / "runner-temp"),
                   "GITHUB_WORKSPACE": str(workspace), "GITHUB_OUTPUT": str(output),
                   "PATH": str(root) + os.pathsep + os.environ["PATH"]}
            directories = []
            for _ in range(2):
                result = self.run_step("Prepare model signal directory", env, workspace)
                self.assertEqual(result.returncode, 0, result.stderr)
                directory = Path(output.read_text().splitlines()[-1].split("=", 1)[1])
                directories.append(directory)
                # Bash's semantic working-directory boundary is the checkout,
                # not RUNNER_TEMP (Read being able to open a file is insufficient).
                self.assertEqual(directory.parent, workspace / ".model-timeline-inputs")
                self.assertEqual(list(directory.iterdir()), [])
                for name in ("Fetch tweets from company accounts", "Fetch tweets from key execs",
                             "Search for model release tweets"):
                    step = self.steps[name]
                    self.assertEqual(step["env"]["MODEL_SIGNAL_DIR"],
                                     "${{ steps.model-signal.outputs.directory }}")
                    result = self.run_step(name, {**env, "MODEL_SIGNAL_DIR": str(directory)}, workspace)
                    self.assertEqual(result.returncode, 0, result.stderr)
                files = list(directory.glob("*.json"))
                self.assertEqual(len(files), 24)
                self.assertTrue(all(json.loads(path.read_text()) ==
                                    [{"text": "fresh model signal"}] for path in files))
            self.assertNotEqual(*directories)
            self.assertEqual(json.loads(stale.read_text())[0]["text"],
                             "unrelated hourly-twitter input")
            # Even broad staging must never include runtime source material.
            subprocess.run(["git", "add", "-A"], cwd=workspace, check=True)
            staged = subprocess.run(["git", "diff", "--cached", "--name-only"],
                                    cwd=workspace, check=True, text=True, capture_output=True)
            self.assertEqual(staged.stdout.splitlines(), [".gitignore"])
            result = self.run_step("Clean model signal directory",
                                   {**env, "MODEL_SIGNAL_DIR": str(directories[0])}, workspace)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(directories[0].exists())
            self.assertEqual(len(list(directories[1].glob("*.json"))), 24)
            self.assertTrue(stale.exists())
            prompt = self.steps["CRUD model tickets via Claude"]["with"]["prompt"]
            self.assertIn("${{ steps.model-signal.outputs.directory }}/*.json", prompt)
            self.assertIn("${{ steps.model-signal.outputs.directory }}/prepared/manifest.json", prompt)
            self.assertIn("Read every signal_pages file", prompt)
            self.assertIn("every active_ticket_pages", prompt)
            self.assertIn("closed_ticket_pages", prompt)
            self.assertIn("reserve the final 25 turns", prompt)
            self.assertIn("--max-turns 100", self.steps["CRUD model tickets via Claude"]["with"]["claude-args"])
            self.assertIn("--as-of \"$AS_OF\"", self.steps["Prepare model working set"]["run"])

    def test_cleanup_rejects_paths_outside_its_run_scope(self) -> None:
        cleanup = self.steps["Clean model signal directory"]
        self.assertEqual(cleanup["if"], "always() && steps.model-signal.outcome == 'success'")
        self.assertEqual(cleanup["env"]["MODEL_SIGNAL_DIR"],
                         "${{ steps.model-signal.outputs.directory }}")
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp)
            input_root = workspace / ".model-timeline-inputs"
            input_root.mkdir()
            sentinel = input_root / "keep.json"
            sentinel.write_text("must survive cleanup")
            env = {"GITHUB_WORKSPACE": str(workspace),
                   "GITHUB_OUTPUT": str(workspace / "outputs")}
            for unexpected in (workspace, input_root, sentinel,
                               input_root / "run.other" / "nested", Path(temp + "-outside")):
                with self.subTest(path=unexpected):
                    result = self.run_step("Clean model signal directory",
                                           {**env, "MODEL_SIGNAL_DIR": str(unexpected)}, workspace)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(sentinel.read_text(), "must survive cleanup")
            # A pre-existing symlink cannot redirect preparation or cleanup
            # to another directory on the persistent self-hosted runner.
            input_root.rename(workspace / "elsewhere")
            input_root.symlink_to(workspace / "elsewhere", target_is_directory=True)
            result = self.run_step("Prepare model signal directory", env, workspace)
            self.assertNotEqual(result.returncode, 0)
            result = self.run_step("Clean model signal directory",
                                   {**env, "MODEL_SIGNAL_DIR": str(input_root / "run.other")}, workspace)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(sentinel.read_text(), "must survive cleanup")

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

    def test_trusted_schema_check_rejects_malformed_author_output(self) -> None:
        validation = self.steps["Validate completed model tickets"]
        self.assertEqual(validation["run"], "uv run python scripts/check_model_tickets.py")
        self.assertEqual(validation["if"], "success() && steps.crud.outcome == 'success'")
        names = list(self.steps)
        self.assertLess(names.index("Validate completed model tickets"), names.index("Push changes"))
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "invalid-ticket.md"
            path.write_text("---\nslug: invalid-ticket\nstatus: invented-state\n---\nPartial output\n")
            result = subprocess.run([sys.executable, str(ROOT / "scripts/check_model_tickets.py"), path.name],
                                    cwd=path.parent, text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("status", result.stderr)

    def test_partial_ticket_commit_cannot_satisfy_completion_guard(self) -> None:
        expected = "research/models/${{ steps.datetime.outputs.date }}-timeline.md"
        author = self.steps["CRUD model tickets via Claude"]["with"]
        self.assertEqual(author["expected-paths"].strip(), expected)
        self.assertEqual(author["allowed-paths"].strip(), "research/models/")
        self.assertEqual(self.steps["Require model output"]["with"]["expected-paths"].strip(), expected)
        action = yaml.load((ROOT / ".github/actions/require-output/action.yml").read_text(),
                           Loader=yaml.BaseLoader)
        guard = action["runs"]["steps"][0]["run"]
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            env = {**os.environ, "GIT_AUTHOR_NAME": "Test", "GIT_AUTHOR_EMAIL": "test@example.org",
                   "GIT_COMMITTER_NAME": "Test", "GIT_COMMITTER_EMAIL": "test@example.org"}

            def git(*args):
                return subprocess.run(["git", *args], cwd=root, env=env, check=True,
                                      text=True, capture_output=True).stdout.strip()

            git("init", "-q")
            git("commit", "--allow-empty", "-qm", "baseline")
            base = git("rev-parse", "HEAD")
            ticket = root / "research/models/tickets/partial.md"
            ticket.parent.mkdir(parents=True)
            ticket.write_text("A partial ticket edit auto-committed by agent-run")
            git("add", "research")
            git("commit", "-qm", "partial author output")
            env.update(BASE_SHA=base, EXPECTED_PATHS="research/models/2026-09-30-timeline.md",
                       LABEL="model completion", GITHUB_OUTPUT=str(root / "outputs"))
            result = subprocess.run(["bash", "-c", guard], cwd=root, env=env,
                                    text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing: research/models/2026-09-30-timeline.md", result.stdout)
            (root / env["EXPECTED_PATHS"]).write_text("Completed daily diff")
            git("add", "research")
            git("commit", "-qm", "completed author output")
            result = subprocess.run(["bash", "-c", guard], cwd=root, env=env,
                                    text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
