#!/usr/bin/env python3
"""Tests for the curated AI blog feed fetcher."""

from __future__ import annotations

import datetime as dt
import os
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

import fetch_ai_blogs as blogs  # noqa: E402


SOURCE = blogs.Source(
    id="example",
    name="Example Blog",
    url="https://example.com/",
    feed_url="https://example.com/feed.xml",
    type="expert_blog",
    priority="P0",
    cadence="daily",
    tags=("agents", "evals"),
    include_in_digest=True,
    notes="",
)


class FeedParserTest(unittest.TestCase):
    def test_parse_rss_item(self):
        body = b"""<?xml version="1.0"?>
        <rss version="2.0">
          <channel>
            <item>
              <title>Agent evals in production</title>
              <link>https://example.com/post?utm_source=x</link>
              <pubDate>Mon, 25 May 2026 08:00:00 GMT</pubDate>
              <description><![CDATA[<p>Useful detail.</p>]]></description>
            </item>
          </channel>
        </rss>"""

        items = blogs.parse_feed(SOURCE, body)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].title, "Agent evals in production")
        self.assertEqual(items[0].url, "https://example.com/post")
        self.assertEqual(items[0].published_at, dt.datetime(2026, 5, 25, 8, tzinfo=dt.timezone.utc))
        self.assertIn("Useful detail", items[0].summary)
        self.assertGreater(items[0].score, 100)

    def test_parse_atom_item_with_relative_link(self):
        body = b"""<?xml version="1.0"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
          <entry>
            <title>Open model inference notes</title>
            <link rel="alternate" href="/posts/open-models" />
            <published>2026-05-25T09:30:00Z</published>
            <summary>Inference benchmark notes.</summary>
          </entry>
        </feed>"""

        items = blogs.parse_feed(SOURCE, body)

        self.assertEqual(items[0].url, "https://example.com/posts/open-models")
        self.assertEqual(items[0].published_label, "2026-05-25 09:30 UTC")

    def test_target_window_uses_utc_date(self):
        item = blogs.FeedItem(
            source=SOURCE,
            title="Title",
            url="https://example.com/title",
            published_at=dt.datetime(2026, 5, 25, 23, 59, tzinfo=dt.timezone.utc),
            summary="",
            score=1,
            content_hash="abc",
        )

        self.assertTrue(blogs.in_target_window(item, dt.date(2026, 5, 25), False))
        self.assertFalse(blogs.in_target_window(item, dt.date(2026, 5, 26), False))

    def test_dedupe_keeps_highest_scored_item(self):
        low = blogs.FeedItem(SOURCE, "Low", "https://example.com/a", None, "", 1, "low")
        high = blogs.FeedItem(SOURCE, "High", "https://example.com/a", None, "", 2, "high")

        self.assertEqual(blogs.dedupe_items([low, high]), [high])


class MainTest(unittest.TestCase):
    def test_main_writes_markdown(self):
        item = blogs.FeedItem(
            source=SOURCE,
            title="Agent evals in production",
            url="https://example.com/post",
            published_at=dt.datetime(2026, 5, 25, 8, tzinfo=dt.timezone.utc),
            summary="Useful detail.",
            score=150,
            content_hash="abc",
        )
        with tempfile.TemporaryDirectory() as td:
            registry = Path(td) / "sources.json"
            out_dir = Path(td) / "out"
            registry.write_text(
                """
                [{
                  "id": "example",
                  "name": "Example Blog",
                  "url": "https://example.com/",
                  "feed_url": "https://example.com/feed.xml",
                  "type": "expert_blog",
                  "priority": "P0",
                  "cadence": "daily",
                  "tags": ["agents"],
                  "include_in_digest": true
                }]
                """,
                encoding="utf-8",
            )
            with unittest.mock.patch.object(blogs, "collect_items", return_value=([item], [])):
                rc = blogs.main([
                    "--registry", str(registry),
                    "--out-dir", str(out_dir),
                    "--date", "2026-05-25",
                ])

            self.assertEqual(rc, 0)
            text = (out_dir / "2026-05-25.md").read_text(encoding="utf-8")
            self.assertIn("# AI Expert Blog Watch - 2026-05-25", text)
            self.assertIn("[Agent evals in production](https://example.com/post)", text)


if __name__ == "__main__":
    unittest.main()
