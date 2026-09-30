#!/usr/bin/env python3

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml


class SafePushStrictPublicationContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (Path(__file__).resolve().parent.parent / ".github/actions/safe-push/action.yml").read_text()

    def test_schedules_are_strict_by_default(self):
        self.assertIn('auto) [ "${SAFE_PUSH_EVENT_NAME}" = "schedule" ]', self.text)
        self.assertIn("STRICT_PUBLICATION=true", self.text)

    def test_noop_exits_successfully_before_strict_failure_paths(self):
        start = self.text.index('if [ -n "$UPSTREAM_HEAD" ] && [ "$CURRENT_HEAD" = "$UPSTREAM_HEAD" ]')
        end = self.text.index('PUSH_LOG="$(mktemp)"', start)
        noop_block = self.text[start:end]
        self.assertIn("publication-mode=noop", noop_block)
        self.assertIn("exit 0", noop_block)
        self.assertNotIn("STRICT_PUBLICATION", noop_block)

    def test_every_non_landed_fallback_has_strict_failure(self):
        self.assertIn("generated branch ${pr_branch} did not land", self.text)
        self.assertIn("did not become a pull request", self.text)
        self.assertIn("remains open, so output is stranded", self.text)

    def test_concurrent_claim_index_is_rebuilt_not_side_selected(self):
        self.assertIn('"research/claims/index.json"', self.text)
        self.assertIn("rebuild_claim_index", self.text)
        self.assertIn("Rebuilt claim index after incorporating concurrent ledgers", self.text)

    def test_failed_fallback_branch_push_is_not_reported_as_publication(self):
        self.assertIn('if ! push_fallback_branch "$pr_branch"; then\n            return 1', self.text)


class SafePushBranchRetryTest(unittest.TestCase):
    """Execute the action's retry function with a failing Git transport."""

    @classmethod
    def setUpClass(cls):
        action = Path(__file__).resolve().parent.parent / ".github/actions/safe-push/action.yml"
        script = yaml.safe_load(action.read_text())["runs"]["steps"][0]["run"]
        start = script.index("push_fallback_branch() {")
        cls.function = script[start:script.index("sanitize_branch_part() {", start)]

    def run_push(self, failures, error):
        with tempfile.TemporaryDirectory() as directory:
            env = dict(os.environ, PUSH_STATE=directory, FAILURES=str(failures), PUSH_ERROR=error)
            script = r'''
set -euo pipefail
MAX_ATTEMPTS=3
git_auth() {
  printf '%s\n' "$*" >> "$PUSH_STATE/calls"
  local count
  count=$(wc -l < "$PUSH_STATE/calls")
  if [ "$count" -le "$FAILURES" ]; then
    printf '%s\n' "$PUSH_ERROR" >&2
    return 1
  fi
}
sleep() { :; }
'''
            result = subprocess.run(
                ["bash", "-c", script + self.function + '\npush_fallback_branch "automation/safe-push/test"'],
                env=env, capture_output=True, text=True, timeout=10,
            )
            calls = (Path(directory) / "calls").read_text().splitlines()
            return result, calls

    def test_transient_failure_retries_same_branch_without_force(self):
        result, calls = self.run_push(1, "remote: Internal Server Error")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(calls, ["push origin HEAD:refs/heads/automation/safe-push/test"] * 2)

    def test_retry_exhaustion_fails(self):
        result, calls = self.run_push(10, "fatal: unable to access URL: The requested URL returned error: 503")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(len(calls), 3)
        self.assertIn("::error::Failed to publish fallback branch", result.stdout)

    def test_permanent_failures_are_not_retried(self):
        for error in ("Authentication failed", "remote: error: GH013: Repository rule violations", "! [rejected] (non-fast-forward)"):
            with self.subTest(error=error):
                result, calls = self.run_push(10, error)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(len(calls), 1)

    def test_success_does_not_retry(self):
        result, calls = self.run_push(0, "")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(len(calls), 1)


if __name__ == "__main__":
    unittest.main()
