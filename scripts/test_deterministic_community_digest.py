#!/usr/bin/env python3
"""Tests for the deterministic community fallback writer."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

import deterministic_community_digest as community  # noqa: E402


class DeterministicCommunityDigestTest(unittest.TestCase):
    def test_load_hn_items_filters_and_sorts_ai_posts(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "frontpage.json"
            path.write_text(
                json.dumps(
                    {
                        "hits": [
                            {
                                "title": "LLM inference benchmark",
                                "url": "https://example.com/llm?utm_campaign=x",
                                "points": 42,
                                "num_comments": 7,
                                "objectID": "1",
                            },
                            {
                                "title": "Woodworking notes",
                                "url": "https://example.com/wood",
                                "points": 99,
                                "num_comments": 1,
                                "objectID": "2",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            items = community.load_hn_items(path, limit=10)

            self.assertEqual(len(items), 1)
            self.assertEqual(items[0].title, "LLM inference benchmark")
            self.assertEqual(items[0].url, "https://example.com/llm")
            self.assertEqual(items[0].discuss_url, "https://news.ycombinator.com/item?id=1")

    def test_update_digest_writes_hn_and_reddit_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            hn_path = root / "frontpage.json"
            reddit_dir = root / "reddit"
            out_dir = root / "out"
            reddit_dir.mkdir()
            hn_path.write_text(
                json.dumps(
                    {
                        "hits": [
                            {
                                "title": "Claude agents in production",
                                "url": "https://example.com/claude",
                                "points": 12,
                                "num_comments": 3,
                                "objectID": "99",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            atom = """<feed xmlns="http://www.w3.org/2005/Atom"><entry>
            <title>Open model inference thread</title>
            <link href="https://reddit.com/r/MachineLearning/comments/abc" />
            <updated>2026-06-25T08:30:00Z</updated>
            <content>LLM inference notes</content>
            </entry></feed>"""
            (reddit_dir / "ml.rss").write_text(atom, encoding="utf-8")

            hn_out, reddit_out = community.update_digest(
                hn_path,
                reddit_dir,
                out_dir,
                "2026-06-25",
                "2026-06-25 09:00 UTC",
            )

            self.assertIn("Claude agents in production", hn_out.read_text(encoding="utf-8"))
            reddit_text = reddit_out.read_text(encoding="utf-8")
            self.assertIn("Open model inference thread", reddit_text)
            self.assertIn("localllama.rss", reddit_text)


if __name__ == "__main__":
    unittest.main()
