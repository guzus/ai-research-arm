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
                            "text": "OpenAI ships GPT-5.7 Mini with a new AI systems card.",
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
                                    "text": "OpenAI publishes the GPT-5.7 Mini AI safety system card.",
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
            self.assertNotIn("Quiet period", digest)
            self.assertIn("Twitter/X AI Pulse - 2026-07-09 07:14 UTC", summary)
            status = json.loads((out_dir / "status" / "2026-07-09-07h.json").read_text(encoding="utf-8"))
            self.assertEqual(status["status"], "published")
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
                                    "text": "OpenAI publishes GPT-5.7 Mini API safety guidance.",
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

    def test_suppresses_prior_same_day_story_families(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_dir = root / "bird"
            out_dir = root / "research" / "twitter"
            summaries_dir = root / "research" / "summaries"
            headlines_file = summaries_dir / "2026-07-09-twitter-13h-headlines.json"
            input_dir.mkdir()
            out_dir.mkdir(parents=True)
            (out_dir / "2026-07-09.md").write_text(
                "# Twitter/X AI Pulse - 2026-07-09\n\n"
                "## 12:00 UTC\n\n"
                "**Cycle summary**: Fresh primary-source AI product movement cleared the bar this window: "
                "OpenAI gives GPT-5.6 Sol/Terra/Luna a public launch window; "
                "OpenAI rolls out GPT-Live voice models in ChatGPT.\n\n"
                "### Top stories\n\n"
                '<a class="twitter-source-chip" href="https://x.com/OpenAI/status/2074704958419792299">@OpenAI</a>\n'
                '<a class="twitter-source-chip" href="https://x.com/OpenAI/status/2074907025537224840">@OpenAI</a>\n',
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
                                    "createdAt": "Thu Jul 09 12:15:00 +0000 2026",
                                    "likeCount": 45189,
                                    "retweetCount": 6571,
                                    "replyCount": 2308,
                                },
                                {
                                    "id": "2074907025537224840",
                                    "author": {"username": "OpenAI"},
                                    "text": "Introducing GPT-Live, a new generation of voice models for natural human-AI interaction. Rolling out in ChatGPT starting today.",
                                    "createdAt": "Thu Jul 09 12:45:00 +0000 2026",
                                    "likeCount": 18295,
                                    "retweetCount": 1631,
                                    "replyCount": 926,
                                },
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
                    "13",
                    "--timestamp",
                    "2026-07-09 13:08 UTC",
                    "--summary-slug",
                    "twitter",
                    "--headlines-file",
                    str(headlines_file),
                ]
            )

            self.assertEqual(rc, 0)
            digest = (out_dir / "2026-07-09.md").read_text(encoding="utf-8")
            summary = (summaries_dir / "2026-07-09-twitter-13h-summary.txt").read_text(encoding="utf-8")
            self.assertNotIn("## 13:00 UTC", digest)
            self.assertEqual(summary, "")
            status = json.loads((out_dir / "status" / "2026-07-09-13h.json").read_text(encoding="utf-8"))
            self.assertEqual(status["status"], "no_update")
            self.assertEqual(status["public_items"], 0)
            self.assertEqual(json.loads(headlines_file.read_text(encoding="utf-8")), [])

    def test_unseen_official_launch_drives_quick_hit_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_dir = root / "bird"
            out_dir = root / "research" / "twitter"
            summaries_dir = root / "research" / "summaries"
            headlines_file = summaries_dir / "2026-07-10-twitter-07h-headlines.json"
            input_dir.mkdir()
            out_dir.mkdir(parents=True)
            (out_dir / "2026-07-10.md").write_text(
                "# Twitter/X AI Pulse - 2026-07-10\n\n"
                "## 05:00 UTC\n\n"
                "**Cycle summary**: OpenAI gives GPT-5.6 Sol/Terra/Luna a public launch window.\n\n"
                "### Top stories\n\n"
                '<a class="twitter-source-chip" href="https://x.com/OpenAI/status/2074704958419792299">@OpenAI</a>\n',
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
                                    "text": "GPT-5.6 Sol, Terra and Luna will launch publicly this Thursday.",
                                    "createdAt": "Fri Jul 10 06:30:00 +0000 2026",
                                    "likeCount": 45000,
                                    "retweetCount": 6500,
                                    "replyCount": 2300,
                                }
                            ],
                            "AIatMeta": [
                                {
                                    "id": "2075221088821518394",
                                    "author": {"username": "AIatMeta"},
                                    "text": "We are introducing Muse Spark 1.1 and launching a public preview of the new Meta Model API.",
                                    "createdAt": "Fri Jul 10 06:45:00 +0000 2026",
                                    "likeCount": 3907,
                                    "retweetCount": 459,
                                    "replyCount": 212,
                                }
                            ],
                            "sama": [
                                {
                                    "id": "2075048072837734448",
                                    "author": {"username": "sama"},
                                    "text": "it surely doesnt",
                                    "createdAt": "Fri Jul 10 06:50:00 +0000 2026",
                                    "likeCount": 5096,
                                    "retweetCount": 110,
                                    "replyCount": 321,
                                },
                                {
                                    "id": "2075048072837734449",
                                    "author": {"username": "sama"},
                                    "text": "this is a surprisingly beautiful place and I hope everyone gets to visit someday",
                                    "createdAt": "Fri Jul 10 06:51:00 +0000 2026",
                                    "likeCount": 7000,
                                    "retweetCount": 300,
                                    "replyCount": 400,
                                }
                            ],
                        },
                        "searches": {
                            "ai": [
                                {
                                    "id": "spam-1",
                                    "author": {"username": "TokenPump"},
                                    "text": "Join the hottest AI crypto presale and whitelist now before the token sale closes.",
                                    "createdAt": "Fri Jul 10 06:52:00 +0000 2026",
                                    "likeCount": 9000,
                                    "retweetCount": 800,
                                    "replyCount": 50,
                                },
                                {
                                    "id": "travel-1",
                                    "author": {"username": "SummerTrips"},
                                    "text": "Plan your summer holiday with our experienced travel agent and save on flights.",
                                    "createdAt": "Fri Jul 10 06:53:00 +0000 2026",
                                    "likeCount": 8000,
                                    "retweetCount": 700,
                                    "replyCount": 40,
                                },
                            ]
                        },
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
                    "2026-07-10",
                    "--hour",
                    "07",
                    "--timestamp",
                    "2026-07-10 07:00 UTC",
                    "--summary-slug",
                    "twitter",
                    "--headlines-file",
                    str(headlines_file),
                ]
            )

            self.assertEqual(rc, 0)
            digest = (out_dir / "2026-07-10.md").read_text(encoding="utf-8")
            summary = (summaries_dir / "2026-07-10-twitter-07h-summary.txt").read_text(encoding="utf-8")
            seven = digest.split("## 07:00 UTC", 1)[1]
            self.assertIn("Muse Spark 1.1", seven)
            self.assertIn("Meta Model API", seven)
            self.assertNotIn("Quiet", seven)
            self.assertNotIn("no new main", seven)
            self.assertNotIn("it surely doesnt", seven)
            self.assertNotIn("beautiful place", seven)
            self.assertNotIn("crypto presale", seven)
            self.assertNotIn("travel agent", seven)
            self.assertIn("Muse Spark 1.1", summary)
            self.assertNotIn("it surely doesnt", summary)
            status = json.loads((out_dir / "status" / "2026-07-10-07h.json").read_text(encoding="utf-8"))
            self.assertEqual(status["status"], "published")

    def test_empty_snapshot_writes_heartbeat_without_public_digest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_dir = root / "bird"
            out_dir = root / "research" / "twitter"
            summaries_dir = root / "research" / "summaries"
            headlines_file = summaries_dir / "2026-07-10-twitter-10h-headlines.json"
            input_dir.mkdir()
            (input_dir / "all.json").write_text(
                json.dumps({"accounts": {}, "searches": {}, "news": []}),
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
                    "2026-07-10",
                    "--hour",
                    "10",
                    "--timestamp",
                    "2026-07-10 10:00 UTC",
                    "--summary-slug",
                    "twitter",
                    "--headlines-file",
                    str(headlines_file),
                ]
            )

            self.assertEqual(rc, 0)
            self.assertFalse((out_dir / "2026-07-10.md").exists())
            self.assertEqual(
                (summaries_dir / "2026-07-10-twitter-10h-summary.txt").read_text(encoding="utf-8"),
                "",
            )
            status = json.loads((out_dir / "status" / "2026-07-10-10h.json").read_text(encoding="utf-8"))
            self.assertEqual(status["status"], "no_update")
            self.assertEqual(json.loads(headlines_file.read_text(encoding="utf-8")), [])

            rc = main(
                [
                    "--input-dir",
                    str(input_dir),
                    "--out-dir",
                    str(out_dir),
                    "--summaries-dir",
                    str(summaries_dir),
                    "--date",
                    "2026-07-10",
                    "--hour",
                    "10",
                    "--timestamp",
                    "2026-07-10 10:05 UTC",
                    "--summary-slug",
                    "twitter",
                    "--headlines-file",
                    str(headlines_file),
                ]
            )
            self.assertEqual(rc, 0)
            rerun_status = json.loads(
                (out_dir / "status" / "2026-07-10-10h.json").read_text(encoding="utf-8")
            )
            self.assertEqual(rerun_status["generated_at"], "2026-07-10 10:05 UTC")
            self.assertFalse((out_dir / "2026-07-10.md").exists())

    def test_generic_ai_hype_is_not_publishable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_dir = root / "bird"
            out_dir = root / "research" / "twitter"
            summaries_dir = root / "research" / "summaries"
            headlines_file = summaries_dir / "2026-07-10-twitter-11h-headlines.json"
            input_dir.mkdir()
            (input_dir / "all.json").write_text(
                json.dumps(
                    {
                        "accounts": {},
                        "searches": {
                            "ai": [
                                {
                                    "id": "hype-1",
                                    "author": {"username": "HypeLab"},
                                    "text": "Our AI agent is changing everything. Follow us and join the community today!",
                                    "createdAt": "Fri Jul 10 10:30:00 +0000 2026",
                                    "likeCount": 5000,
                                    "retweetCount": 500,
                                    "replyCount": 100,
                                },
                                {
                                    "id": "hype-2",
                                    "author": {"username": "FutureAI"},
                                    "text": "AI agents are the future and everyone will use them soon.",
                                    "createdAt": "Fri Jul 10 10:31:00 +0000 2026",
                                    "likeCount": 4000,
                                    "retweetCount": 400,
                                    "replyCount": 90,
                                },
                                {
                                    "id": "hype-3",
                                    "author": {"username": "UpdateAI"},
                                    "text": "Quick AI update: AI agents are the future and everyone will use them soon.",
                                    "createdAt": "Fri Jul 10 10:32:00 +0000 2026",
                                    "likeCount": 3900,
                                    "retweetCount": 390,
                                    "replyCount": 80,
                                },
                                {
                                    "id": "hype-4",
                                    "author": {"username": "BigSoon"},
                                    "text": "Big update coming soon: our AI agent will change everything.",
                                    "createdAt": "Fri Jul 10 10:33:00 +0000 2026",
                                    "likeCount": 3800,
                                    "retweetCount": 380,
                                    "replyCount": 70,
                                },
                                {
                                    "id": "hype-5",
                                    "author": {"username": "SafeThoughts"},
                                    "text": "AI safety is important and everyone should care.",
                                    "createdAt": "Fri Jul 10 10:34:00 +0000 2026",
                                    "likeCount": 3700,
                                    "retweetCount": 370,
                                    "replyCount": 60,
                                },
                                {
                                    "id": "hype-6",
                                    "author": {"username": "ResearchVision"},
                                    "text": "Our AI research will change everything.",
                                    "createdAt": "Fri Jul 10 10:35:00 +0000 2026",
                                    "likeCount": 3600,
                                    "retweetCount": 360,
                                    "replyCount": 50,
                                },
                                {
                                    "id": "hype-7",
                                    "author": {"username": "MovementAI"},
                                    "text": "We are launching an AI agent that changes everything. Join the movement.",
                                    "createdAt": "Fri Jul 10 10:36:00 +0000 2026",
                                    "likeCount": 3500,
                                    "retweetCount": 350,
                                    "replyCount": 40,
                                },
                                {
                                    "id": "promo-1",
                                    "author": {"username": "TradeAI"},
                                    "text": "Launching our AI trading agent today. Limited offer: sign up now.",
                                    "createdAt": "Fri Jul 10 10:37:00 +0000 2026",
                                    "likeCount": 3400,
                                    "retweetCount": 340,
                                    "replyCount": 30,
                                },
                                {
                                    "id": "promo-2",
                                    "author": {"username": "OpenAI"},
                                    "text": "We are launching a limited edition hoodie today.",
                                    "createdAt": "Fri Jul 10 10:38:00 +0000 2026",
                                    "likeCount": 3300,
                                    "retweetCount": 330,
                                    "replyCount": 20,
                                },
                                {
                                    "id": "offtopic-2",
                                    "author": {"username": "AIatMeta"},
                                    "text": "We are launching a new office in Seoul today.",
                                    "createdAt": "Fri Jul 10 10:39:00 +0000 2026",
                                    "likeCount": 3200,
                                    "retweetCount": 320,
                                    "replyCount": 20,
                                },
                                {
                                    "id": "rumor-1",
                                    "author": {"username": "RumorFeed"},
                                    "text": "OpenAI announces that the future starts now.",
                                    "createdAt": "Fri Jul 10 10:40:00 +0000 2026",
                                    "likeCount": 3100,
                                    "retweetCount": 310,
                                    "replyCount": 20,
                                },
                                {
                                    "id": "promo-3",
                                    "author": {"username": "AgentShop"},
                                    "text": "Launching our OpenAI-powered AI agent today. Get yours today!",
                                    "createdAt": "Fri Jul 10 10:41:00 +0000 2026",
                                    "likeCount": 3000,
                                    "retweetCount": 300,
                                    "replyCount": 20,
                                },
                            ]
                        },
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
                    "2026-07-10",
                    "--hour",
                    "11",
                    "--timestamp",
                    "2026-07-10 11:00:00 UTC",
                    "--run-id",
                    "1234",
                    "--run-attempt",
                    "1",
                    "--summary-slug",
                    "twitter",
                    "--headlines-file",
                    str(headlines_file),
                ]
            )

            self.assertEqual(rc, 0)
            self.assertFalse((out_dir / "2026-07-10.md").exists())
            self.assertEqual(
                (summaries_dir / "2026-07-10-twitter-11h-summary.txt").read_text(encoding="utf-8"),
                "",
            )
            status = json.loads((out_dir / "status" / "2026-07-10-11h.json").read_text(encoding="utf-8"))
            self.assertEqual(status["status"], "no_update")
            self.assertEqual(status["run_id"], "1234")
            self.assertEqual(status["run_attempt"], 1)

    def test_trusted_primary_release_can_supply_product_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_dir = root / "bird"
            out_dir = root / "research" / "twitter"
            summaries_dir = root / "research" / "summaries"
            headlines_file = summaries_dir / "2026-07-10-twitter-12h-headlines.json"
            input_dir.mkdir()
            (input_dir / "all.json").write_text(
                json.dumps(
                    {
                        "accounts": {
                            "AIatMeta": [
                                {
                                    "id": "1200",
                                    "author": {"username": "AIatMeta"},
                                    "text": "Introducing Muse Spark 1.2, available today.",
                                    "createdAt": "Fri Jul 10 11:30:00 +0000 2026",
                                    "likeCount": 900,
                                    "retweetCount": 100,
                                    "replyCount": 50,
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
                    "2026-07-10",
                    "--hour",
                    "12",
                    "--timestamp",
                    "2026-07-10 12:00:00 UTC",
                    "--summary-slug",
                    "twitter",
                    "--headlines-file",
                    str(headlines_file),
                ]
            )

            self.assertEqual(rc, 0)
            digest = (out_dir / "2026-07-10.md").read_text(encoding="utf-8")
            self.assertIn("Muse Spark 1.2", digest)
            self.assertIn("https://x.com/AIatMeta/status/1200", digest)

    def test_no_update_removes_same_hour_heading_with_trailing_space(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_dir = root / "bird"
            out_dir = root / "research" / "twitter"
            summaries_dir = root / "research" / "summaries"
            headlines_file = summaries_dir / "2026-07-10-twitter-14h-headlines.json"
            input_dir.mkdir()
            out_dir.mkdir(parents=True)
            (input_dir / "all.json").write_text(
                json.dumps({"accounts": {}, "searches": {}, "news": []}),
                encoding="utf-8",
            )
            (out_dir / "2026-07-10.md").write_text(
                "# Twitter/X AI Pulse - 2026-07-10\r\n\r\n"
                "## 14:00 UTC \r\n\r\n"
                "**Cycle summary**: Quiet follow-up period.\r\n",
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
                    "2026-07-10",
                    "--hour",
                    "14",
                    "--timestamp",
                    "2026-07-10 14:00:00 UTC",
                    "--summary-slug",
                    "twitter",
                    "--headlines-file",
                    str(headlines_file),
                ]
            )

            self.assertEqual(rc, 0)
            digest = (out_dir / "2026-07-10.md").read_text(encoding="utf-8")
            self.assertNotIn("## 14:00 UTC", digest)
            self.assertNotIn("Quiet follow-up", digest)

    def test_new_url_in_seen_story_family_remains_publishable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_dir = root / "bird"
            out_dir = root / "research" / "twitter"
            summaries_dir = root / "research" / "summaries"
            headlines_file = summaries_dir / "2026-07-10-twitter-13h-headlines.json"
            input_dir.mkdir()
            out_dir.mkdir(parents=True)
            (out_dir / "2026-07-10.md").write_text(
                "# Twitter/X AI Pulse - 2026-07-10\n\n"
                "## 12:00 UTC\n\n"
                "**Cycle summary**: OpenAI gives GPT-5.6 Sol/Terra/Luna a public launch window.\n\n"
                '<a href="https://x.com/OpenAI/status/1">@OpenAI</a>\n',
                encoding="utf-8",
            )
            (input_dir / "all.json").write_text(
                json.dumps(
                    {
                        "accounts": {
                            "OpenAI": [
                                {
                                    "id": "2",
                                    "author": {"username": "OpenAI"},
                                    "text": "GPT-5.6 API pricing is now public, with lower cached-input pricing for Sol.",
                                    "createdAt": "Fri Jul 10 12:30:00 +0000 2026",
                                    "likeCount": 1200,
                                    "retweetCount": 180,
                                    "replyCount": 90,
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
                    "2026-07-10",
                    "--hour",
                    "13",
                    "--timestamp",
                    "2026-07-10 13:00 UTC",
                    "--summary-slug",
                    "twitter",
                    "--headlines-file",
                    str(headlines_file),
                ]
            )

            self.assertEqual(rc, 0)
            digest = (out_dir / "2026-07-10.md").read_text(encoding="utf-8")
            thirteen = digest.split("## 13:00 UTC", 1)[1]
            self.assertIn("API pricing is now public", thirteen)
            self.assertIn("https://x.com/OpenAI/status/2", thirteen)
            self.assertNotIn("Quiet", thirteen)
            status = json.loads((out_dir / "status" / "2026-07-10-13h.json").read_text(encoding="utf-8"))
            self.assertEqual(status["status"], "published")


if __name__ == "__main__":
    unittest.main()
