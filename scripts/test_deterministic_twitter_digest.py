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
                ]
            )

            self.assertEqual(rc, 0)
            digest = (out_dir / "2026-06-29.md").read_text(encoding="utf-8")
            summary = (summaries_dir / "2026-06-29-twitter-deepseek-10h-summary.txt").read_text(encoding="utf-8")
            self.assertIn("## 10:00 UTC", digest)
            self.assertIn("@openai", digest)
            self.assertIn("https://x.com/openai/status/123", digest)
            self.assertIn("Twitter/X AI Pulse (DeepSeek v4 Flash)", summary)


if __name__ == "__main__":
    unittest.main()
