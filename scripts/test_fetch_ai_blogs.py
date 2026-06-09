#!/usr/bin/env python3
"""Tests for the curated AI blog feed fetcher."""

from __future__ import annotations

import datetime as dt
import os
import sys
import tempfile
import unittest
import unittest.mock
import urllib.error
import xml.etree.ElementTree as ET
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


class CollectItemsResilienceTest(unittest.TestCase):
    """The hourly lane must survive a single bad feed: collect_items catches
    per-feed fetch/parse failures, records them, and keeps going so one dead
    upstream can't crash the whole run. test_main_writes_markdown mocks
    collect_items wholesale, so the real per-feed except handler
    (fetch_ai_blogs.py: collect_items + fetch_url) would otherwise be untested.
    """

    def test_url_error_recorded_not_raised(self):
        # A feed whose fetch raises urllib.error.URLError (e.g. DNS failure,
        # connection refused) must be recorded in `errors`, not propagated.
        with unittest.mock.patch.object(
            blogs, "fetch_url", side_effect=urllib.error.URLError("name resolution failed")
        ):
            items, errors = blogs.collect_items([SOURCE], dt.date(2026, 5, 25), False)

        self.assertEqual(items, [])
        self.assertEqual(len(errors), 1)
        err_source, err_text = errors[0]
        self.assertIs(err_source, SOURCE)
        self.assertTrue(err_text.startswith("URLError:"), err_text)
        self.assertIn("name resolution failed", err_text)

    def test_parse_error_recorded_not_raised(self):
        # A feed that returns malformed XML must surface as a recorded error
        # via the real parse_feed -> ET.fromstring path, not crash the run.
        with unittest.mock.patch.object(blogs, "fetch_url", return_value=b"<not-valid-xml"):
            items, errors = blogs.collect_items([SOURCE], dt.date(2026, 5, 25), False)

        self.assertEqual(items, [])
        self.assertEqual(len(errors), 1)
        err_source, err_text = errors[0]
        self.assertIs(err_source, SOURCE)
        self.assertTrue(err_text.startswith("ParseError:"), err_text)
        # Sanity: a real ET.ParseError is what we're exercising here.
        with self.assertRaises(ET.ParseError):
            blogs.parse_feed(SOURCE, b"<not-valid-xml")

    def test_one_bad_feed_does_not_drop_a_healthy_one(self):
        # Two sources: one fetches fine, one raises. The healthy item must
        # still come through and the bad feed must be recorded as an error.
        good = blogs.Source(
            id="good",
            name="Good Blog",
            url="https://good.example/",
            feed_url="https://good.example/feed.xml",
            type="expert_blog",
            priority="P0",
            cadence="daily",
            tags=("agents",),
            include_in_digest=True,
            notes="",
        )
        good_feed = b"""<?xml version="1.0"?>
        <rss version="2.0">
          <channel>
            <item>
              <title>Healthy post</title>
              <link>https://good.example/post</link>
              <pubDate>Mon, 25 May 2026 08:00:00 GMT</pubDate>
              <description>Body.</description>
            </item>
          </channel>
        </rss>"""

        def fake_fetch(url: str) -> bytes:
            if url == good.feed_url:
                return good_feed
            raise urllib.error.URLError("boom")

        with unittest.mock.patch.object(blogs, "fetch_url", side_effect=fake_fetch):
            items, errors = blogs.collect_items([good, SOURCE], dt.date(2026, 5, 25), False)

        self.assertEqual([i.title for i in items], ["Healthy post"])
        self.assertEqual([s.id for s, _ in errors], ["example"])

    def test_render_markdown_emits_fetch_errors_section(self):
        # The recorded errors must surface in the report so a silent stream of
        # empty digests is visible. render_markdown owns the "## Fetch Errors"
        # section.
        with unittest.mock.patch.object(
            blogs, "fetch_url", side_effect=urllib.error.URLError("connection refused")
        ):
            items, errors = blogs.collect_items([SOURCE], dt.date(2026, 5, 25), False)

        markdown = blogs.render_markdown(
            target_date=dt.date(2026, 5, 25),
            sources=[SOURCE],
            items=items,
            errors=errors,
        )
        self.assertIn("## Fetch Errors", markdown)
        self.assertIn("- Fetch errors: 1", markdown)
        self.assertIn(SOURCE.name, markdown)
        self.assertIn("connection refused", markdown)


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
