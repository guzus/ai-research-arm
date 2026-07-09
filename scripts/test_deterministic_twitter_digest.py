import json
import tempfile
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from deterministic_twitter_digest import main


class DeterministicTwitterDigestTest(unittest.TestCase):
    def test_writes_digest_and_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_dir = root / "bird"
            out_dir = root / "research" / "twitter-deepseek"
            summaries_dir = root / "research" / "summaries"
            headlines_file = summaries_dir / "2026-06-29-twitter-deepseek-10h-headlines.json"
            input_dir.mkdir()
            (input_dir / "search-ai.json").write_text(
                json.dumps(
                    [
                        {
                            "id": "123",
                            "author": {"username": "openai"},
                            "text": "OpenAI ships a small but relevant AI systems update.",
                            "createdAt": "Mon Jun 29 10:01:00 +0000 2026",
                            "likeCount": 42,
                            "retweetCount": 5,
                            "replyCount": 2,
                        }
                    ]
                ),
                encoding="utf-8",
            )

            rc = main(
                [
                    "--input-dir",
                    str(input_dir),
                    "--out-dir",
                    str(out_dir),
                    "--summaries-dir",
                    str(summaries_dir),
                    "--date",
                    "2026-06-29",
                    "--hour",
                    "10",
                    "--timestamp",
                    "2026-06-29 10:53 UTC",
                    "--title-suffix",
                    " (DeepSeek v4 Flash)",
                    "--summary-slug",
                    "twitter-deepseek",
                    "--headlines-file",
                    str(headlines_file),
                ]
            )

            self.assertEqual(rc, 0)
            digest = (out_dir / "2026-06-29.md").read_text(encoding="utf-8")
            summary = (summaries_dir / "2026-06-29-twitter-deepseek-10h-summary.txt").read_text(encoding="utf-8")
            self.assertIn("## 10:00 UTC", digest)
            self.assertIn("@openai", digest)
            self.assertIn("https://x.com/openai/status/123", digest)
            self.assertIn("Twitter/X AI Pulse (DeepSeek v4 Flash)", summary)
            self.assertEqual(json.loads(headlines_file.read_text(encoding="utf-8")), [])

    def test_reads_aggregate_all_json_for_primary_lane(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_dir = root / "bird"
            out_dir = root / "research" / "twitter"
            summaries_dir = root / "research" / "summaries"
            headlines_file = summaries_dir / "2026-07-09-twitter-07h-headlines.json"
            input_dir.mkdir()
            (input_dir / "all.json").write_text(
                json.dumps(
                    {
                        "accounts": {
                            "OpenAI": [
                                {
                                    "id": "456",
                                    "author": {"username": "openai"},
                                    "text": "OpenAI publishes a new AI safety systems note.",
                                    "createdAt": "Thu Jul 09 07:02:00 +0000 2026",
                                    "likeCount": 10,
                                    "retweetCount": 2,
                                    "replyCount": 1,
                                }
                            ]
                        },
                        "searches": {},
                        "news": [],
                    }
                ),
                encoding="utf-8",
            )

            rc = main(
                [
                    "--input-dir",
                    str(input_dir),
                    "--out-dir",
                    str(out_dir),
                    "--summaries-dir",
                    str(summaries_dir),
                    "--date",
                    "2026-07-09",
                    "--hour",
                    "07",
                    "--timestamp",
                    "2026-07-09 07:14 UTC",
                    "--summary-slug",
                    "twitter",
                    "--headlines-file",
                    str(headlines_file),
                ]
            )

            self.assertEqual(rc, 0)
            digest = (out_dir / "2026-07-09.md").read_text(encoding="utf-8")
            summary = (summaries_dir / "2026-07-09-twitter-07h-summary.txt").read_text(encoding="utf-8")
            self.assertIn("## 07:00 UTC", digest)
            self.assertIn("@openai", digest)
            self.assertIn("https://x.com/openai/status/456", digest)
            self.assertIn("Next scheduled Twitter/X AI monitor run", digest)
            self.assertIn("Twitter/X AI Pulse - 2026-07-09 07:14 UTC", summary)
            self.assertEqual(json.loads(headlines_file.read_text(encoding="utf-8")), [])

    def test_excludes_stale_high_engagement_rows_from_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_dir = root / "bird"
            out_dir = root / "research" / "twitter"
            summaries_dir = root / "research" / "summaries"
            headlines_file = summaries_dir / "2026-07-09-twitter-11h-headlines.json"
            input_dir.mkdir()
            (input_dir / "all.json").write_text(
                json.dumps(
                    {
                        "accounts": {
                            "karpathy": [
                                {
                                    "id": "2056753169888334312",
                                    "author": {"username": "karpathy"},
                                    "text": "Personal update: I've joined Anthropic.",
                                    "createdAt": "Wed May 20 11:00:00 +0000 2026",
                                    "likeCount": 150161,
                                    "retweetCount": 11096,
                                    "replyCount": 7974,
                                }
                            ],
                            "OpenAI": [
                                {
                                    "id": "999",
                                    "author": {"username": "openai"},
                                    "text": "Fresh AI systems note for the current monitoring window.",
                                    "createdAt": "Thu Jul 09 11:05:00 +0000 2026",
                                    "likeCount": 7,
                                    "retweetCount": 1,
                                    "replyCount": 0,
                                }
                            ],
                        },
                        "searches": {},
                        "news": [],
                    }
                ),
                encoding="utf-8",
            )

            rc = main(
                [
                    "--input-dir",
                    str(input_dir),
                    "--out-dir",
                    str(out_dir),
                    "--summaries-dir",
                    str(summaries_dir),
                    "--date",
                    "2026-07-09",
                    "--hour",
                    "11",
                    "--timestamp",
                    "2026-07-09 11:36 UTC",
                    "--summary-slug",
                    "twitter",
                    "--headlines-file",
                    str(headlines_file),
                ]
            )

            self.assertEqual(rc, 0)
            digest = (out_dir / "2026-07-09.md").read_text(encoding="utf-8")
            summary = (summaries_dir / "2026-07-09-twitter-11h-summary.txt").read_text(encoding="utf-8")
            self.assertIn("@openai", digest)
            self.assertIn("https://x.com/openai/status/999", digest)
            self.assertNotIn("@karpathy", digest)
            self.assertNotIn("2056753169888334312", digest)
            self.assertNotIn("joined Anthropic", summary)


if __name__ == "__main__":
    unittest.main()
