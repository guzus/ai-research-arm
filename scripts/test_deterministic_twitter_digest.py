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

    def test_promotes_fresh_launch_posts_to_top_stories(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_dir = root / "bird"
            out_dir = root / "research" / "twitter"
            summaries_dir = root / "research" / "summaries"
            headlines_file = summaries_dir / "2026-07-09-twitter-12h-headlines.json"
            input_dir.mkdir()
            (input_dir / "all.json").write_text(
                json.dumps(
                    {
                        "accounts": {
                            "OpenAI": [
                                {
                                    "id": "2074704958419792299",
                                    "author": {"username": "OpenAI"},
                                    "text": "GPT-5.6 Sol, along with Terra and Luna, will launch publicly this Thursday. We are expanding preview access globally now.",
                                    "createdAt": "Thu Jul 09 11:15:00 +0000 2026",
                                    "likeCount": 44949,
                                    "retweetCount": 6540,
                                    "replyCount": 2290,
                                },
                                {
                                    "id": "2074907025537224840",
                                    "author": {"username": "OpenAI"},
                                    "text": "Introducing GPT-Live, a new generation of voice models for natural human-AI interaction. Rolling out in ChatGPT starting today.",
                                    "createdAt": "Thu Jul 09 11:45:00 +0000 2026",
                                    "likeCount": 17791,
                                    "retweetCount": 1579,
                                    "replyCount": 895,
                                },
                            ],
                            "sama": [
                                {
                                    "id": "2074709023807664454",
                                    "author": {"username": "sama"},
                                    "text": "GPT-5.6 sol launches thursday! happy building",
                                    "createdAt": "Thu Jul 09 11:17:00 +0000 2026",
                                    "likeCount": 29513,
                                    "retweetCount": 1860,
                                    "replyCount": 1796,
                                },
                                {
                                    "id": "2074909079450050629",
                                    "author": {"username": "sama"},
                                    "text": "GPT-live (next-generation voice) launches today in ChatGPT. it feels magical and real.",
                                    "createdAt": "Thu Jul 09 11:48:00 +0000 2026",
                                    "likeCount": 8894,
                                    "retweetCount": 426,
                                    "replyCount": 804,
                                },
                            ],
                            "elonmusk": [
                                {
                                    "id": "2074912099554201969",
                                    "author": {"username": "elonmusk"},
                                    "text": "We will be releasing a new @CommunityNotes feature that sends you an X Chat message if a post you interacted with is corrected",
                                    "createdAt": "Thu Jul 09 11:49:00 +0000 2026",
                                    "likeCount": 13152,
                                    "retweetCount": 1690,
                                    "replyCount": 2802,
                                }
                            ],
                            "deedydas": [
                                {
                                    "id": "2074773187037134892",
                                    "author": {"username": "deedydas"},
                                    "text": "The Argentina come back against Egypt is one of the best matches in football history. I analyzed 50,000 games with Fable.",
                                    "createdAt": "Thu Jul 09 10:02:00 +0000 2026",
                                    "likeCount": 8941,
                                    "retweetCount": 1441,
                                    "replyCount": 252,
                                }
                            ],
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
                    "12",
                    "--timestamp",
                    "2026-07-09 12:11 UTC",
                    "--summary-slug",
                    "twitter",
                    "--headlines-file",
                    str(headlines_file),
                ]
            )

            self.assertEqual(rc, 0)
            digest = (out_dir / "2026-07-09.md").read_text(encoding="utf-8")
            summary = (summaries_dir / "2026-07-09-twitter-12h-summary.txt").read_text(encoding="utf-8")
            headlines = json.loads(headlines_file.read_text(encoding="utf-8"))
            self.assertIn("### Top stories", digest)
            self.assertIn('<article class="twitter-story" data-rank="1">', digest)
            self.assertIn("OpenAI gives GPT-5.6", digest)
            self.assertIn("OpenAI rolls out GPT-Live", digest)
            self.assertIn("TOP STORIES:", summary)
            self.assertGreaterEqual(len(headlines), 2)
            self.assertIn("GPT-5.6", headlines[0]["headline"])
            self.assertNotIn("CommunityNotes", digest)
            self.assertNotIn("football", digest)
            self.assertNotIn("@karpathy", digest)

    def test_replaces_existing_same_hour_fallback_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_dir = root / "bird"
            out_dir = root / "research" / "twitter"
            summaries_dir = root / "research" / "summaries"
            headlines_file = summaries_dir / "2026-07-09-twitter-12h-headlines.json"
            input_dir.mkdir()
            out_dir.mkdir(parents=True)
            (out_dir / "2026-07-09.md").write_text(
                "# Twitter/X AI Pulse - 2026-07-09\n\n"
                "## 12:00 UTC\n\n"
                "**Cycle summary**: Quiet period - no analyst-grade main stories selected.\n\n"
                "### Quick hits\n"
                "- @OpenAI: raw dump only\n",
                encoding="utf-8",
            )
            (input_dir / "all.json").write_text(
                json.dumps(
                    {
                        "accounts": {
                            "OpenAI": [
                                {
                                    "id": "2074704958419792299",
                                    "author": {"username": "OpenAI"},
                                    "text": "GPT-5.6 Sol, along with Terra and Luna, will launch publicly this Thursday.",
                                    "createdAt": "Thu Jul 09 11:15:00 +0000 2026",
                                    "likeCount": 44949,
                                    "retweetCount": 6540,
                                    "replyCount": 2290,
                                }
                            ],
                            "sama": [
                                {
                                    "id": "2074709023807664454",
                                    "author": {"username": "sama"},
                                    "text": "GPT-5.6 sol launches thursday! happy building",
                                    "createdAt": "Thu Jul 09 11:17:00 +0000 2026",
                                    "likeCount": 29513,
                                    "retweetCount": 1860,
                                    "replyCount": 1796,
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
                    "12",
                    "--timestamp",
                    "2026-07-09 12:11 UTC",
                    "--summary-slug",
                    "twitter",
                    "--headlines-file",
                    str(headlines_file),
                ]
            )

            self.assertEqual(rc, 0)
            digest = (out_dir / "2026-07-09.md").read_text(encoding="utf-8")
            self.assertIn("### Top stories", digest)
            self.assertIn("OpenAI gives GPT-5.6", digest)
            self.assertNotIn("raw dump only", digest)
            self.assertNotIn("no analyst-grade main stories", digest)


if __name__ == "__main__":
    unittest.main()
