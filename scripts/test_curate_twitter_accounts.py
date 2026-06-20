from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from curate_twitter_accounts import (
    DEFAULT_MANIFEST,
    apply_changes,
    build_fetch_manifest,
    propose_changes,
    validate_manifest,
)


def load_manifest():
    return json.loads(DEFAULT_MANIFEST.read_text(encoding="utf-8"))


class TwitterAccountCurationTests(unittest.TestCase):
    def test_manifest_validates_with_expected_counts(self):
        stats = validate_manifest(load_manifest())

        self.assertEqual(stats["handles"], 75)
        self.assertEqual(stats["searches"], 7)
        self.assertEqual(stats["tweets_per_account"], 20)

    def test_build_fetch_manifest_preserves_bird_contract(self):
        fetch = build_fetch_manifest(load_manifest(), concurrency=6)

        self.assertEqual(fetch["concurrency"], 6)
        self.assertEqual(len(fetch["operations"]), 83)
        self.assertEqual(
            fetch["operations"][0],
            {
                "id": "OpenAI",
                "args": ["user-tweets", "@OpenAI", "-n", "20", "--json", "--plain"],
            },
        )
        self.assertEqual(
            fetch["operations"][-1],
            {
                "id": "news",
                "args": ["news", "--ai-only", "-n", "40", "--json", "--plain"],
            },
        )

    def test_propose_and_apply_add_remove_round_trip(self):
        manifest = load_manifest()
        candidates = [
            {
                "action": "add",
                "handle": "@new_ai_signal",
                "category": "others",
                "score": 3,
                "reason": "Repeated primary launch evidence.",
                "evidence": ["https://x.com/new_ai_signal/status/1"],
            },
            {
                "action": "remove",
                "handle": "MetaAI",
                "reason": "Inactive compared with AIatMeta.",
                "evidence": ["research/twitter/example.md"],
            },
            {
                "action": "add",
                "handle": "OpenAI",
                "score": 5,
                "reason": "Already monitored.",
            },
        ]

        changes = propose_changes(manifest, candidates, min_score=2, default_category="others")
        self.assertEqual([item["handle"] for item in changes["additions"]], ["new_ai_signal"])
        self.assertEqual([item["handle"] for item in changes["removals"]], ["MetaAI"])
        self.assertEqual(changes["ignored"][0]["why"], "already monitored in labs")

        updated = apply_changes(manifest, changes)
        handles = {
            (entry if isinstance(entry, str) else entry["handle"]).lower()
            for category in updated["categories"]
            for entry in category["handles"]
        }
        self.assertIn("new_ai_signal", handles)
        self.assertNotIn("metaai", handles)
        self.assertEqual(validate_manifest(updated)["handles"], 75)


if __name__ == "__main__":
    unittest.main()
