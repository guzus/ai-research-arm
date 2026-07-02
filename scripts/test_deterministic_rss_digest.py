#!/usr/bin/env python3
"""Tests for the deterministic RSS fallback writer."""

from __future__ import annotations

import datetime as dt
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

import deterministic_rss_digest as rss  # noqa: E402


class DeterministicRssDigestTest(unittest.TestCase):
    def test_parse_rss_and_atom_items(self):
        source = rss.Source("openai", "openai.xml", "OpenAI", "company")
        rss_body = b"""<rss><channel><item>
        <title>OpenAI ships agent evals</title>
        <link>https://openai.com/post?utm_source=x</link>
        <pubDate>Thu, 25 Jun 2026 08:00:00 GMT</pubDate>
        <description><![CDATA[<p>New evaluation detail.</p>]]></description>
        </item></channel></rss>"""
        atom_source = rss.Source("simon_willison", "simon.xml", "Simon", "expert", True)
        atom_body = b"""<feed xmlns="http://www.w3.org/2005/Atom"><entry>
        <title>Notes on LLM agents</title>
        <link rel="alternate" href="https://example.com/agents" />
        <published>2026-06-25T08:30:00Z</published>
        <summary>Hands-on AI notes.</summary>
        </entry></feed>"""

        parsed = rss.parse_feed(source, rss_body) + rss.parse_feed(atom_source, atom_body)

        self.assertEqual([item.title for item in parsed], ["OpenAI ships agent evals", "Notes on LLM agents"])
        self.assertEqual(parsed[0].url, "https://openai.com/post")
        self.assertEqual(parsed[1].published_at, dt.datetime(2026, 6, 25, 8, 30, tzinfo=dt.timezone.utc))

    def test_salvages_feed_with_one_broken_item(self):
        # A single mismatched tag (here an unclosed <b> in item 2) must not
        # discard the whole feed — the good items still come through.
        source = rss.Source("marktechpost", "marktechpost.xml", "MarkTechPost", "tech", True)
        body = b"""<rss><channel>
        <item><title>New open model drops</title>
        <link>https://marktechpost.com/a</link>
        <pubDate>Sun, 28 Jun 2026 08:00:00 GMT</pubDate></item>
        <item><title>Broken <b>entry</title>
        <link>https://marktechpost.com/b</link>
        <pubDate>Sun, 28 Jun 2026 09:00:00 GMT</pubDate></item>
        <item><title>Agent benchmark released</title>
        <link>https://marktechpost.com/c</link>
        <pubDate>Sun, 28 Jun 2026 10:00:00 GMT</pubDate></item>
        </channel></rss>"""
        with self.assertRaises(rss.ET.ParseError):
            rss.ET.fromstring(body)  # strict parse drops everything
        titles = [item.title for item in rss.parse_feed(source, body)]
        self.assertIn("New open model drops", titles)
        self.assertIn("Agent benchmark released", titles)

    def test_sanitizes_bare_ampersand(self):
        source = rss.Source("openai", "openai.xml", "OpenAI", "company")
        body = b"""<rss><channel><item>
        <title>Tom & Jerry ship an agent</title>
        <link>https://openai.com/post</link>
        <pubDate>Sun, 28 Jun 2026 08:00:00 GMT</pubDate>
        </item></channel></rss>"""
        parsed = rss.parse_feed(source, body)
        self.assertEqual([item.title for item in parsed], ["Tom & Jerry ship an agent"])

    def test_salvages_truncated_feed(self):
        # Connection cut mid-download: closing tags missing. Completed <item>
        # blocks should still be recovered.
        source = rss.Source("the_decoder", "the_decoder.xml", "The Decoder", "tech", True)
        body = b"""<rss><channel>
        <item><title>First agent story</title>
        <link>https://the-decoder.com/1</link>
        <pubDate>Sun, 28 Jun 2026 08:00:00 GMT</pubDate></item>
        <item><title>Second story truncat"""
        titles = [item.title for item in rss.parse_feed(source, body)]
        self.assertEqual(titles, ["First agent story"])

    def test_non_feed_body_still_raises(self):
        # A real proxy/CDN error page (unclosed void elements like <hr>) is not
        # well-formed XML and has no entries to salvage, so it must still
        # surface as a parse error / Feed Note rather than be silently swallowed.
        source = rss.Source("anthropic", "anthropic.xml", "Anthropic", "company")
        body = (
            b"<html>\n<head><title>502 Bad Gateway</title></head>\n<body>\n"
            b"<center><h1>502 Bad Gateway</h1></center>\n<hr><center>nginx</center>\n"
            b"</body>\n</html>\n"
        )
        with self.assertRaises(rss.ET.ParseError):
            rss.parse_feed(source, body)

    def test_update_digest_appends_no_new_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_dir = root / "rss"
            out_dir = root / "out"
            input_dir.mkdir()
            (input_dir / "openai.xml").write_text("<rss></rss>", encoding="utf-8")

            out_path = rss.update_digest(
                input_dir,
                out_dir,
                "2026-06-25",
                "2026-06-25 09:00 UTC",
                24,
            )

            text = out_path.read_text(encoding="utf-8")
            self.assertIn("# Official AI News - 2026-06-25", text)
            self.assertIn("## 2026-06-25 09:00 UTC Update", text)
            self.assertIn("_No new updates this hour._", text)
            self.assertIn("anthropic.xml: missing", text)


if __name__ == "__main__":
    unittest.main()
