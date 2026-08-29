#!/usr/bin/env python3

import unittest
from pathlib import Path


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
        self.assertIn('if ! git_auth push origin "HEAD:refs/heads/${pr_branch}"', self.text)


if __name__ == "__main__":
    unittest.main()
