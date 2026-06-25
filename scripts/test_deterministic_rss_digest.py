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
