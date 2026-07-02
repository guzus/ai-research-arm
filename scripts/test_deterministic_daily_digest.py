#!/usr/bin/env python3
"""Tests for the deterministic daily-digest fallback composer (no network)."""

from __future__ import annotations

import datetime as dt
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

import deterministic_daily_digest as digest  # noqa: E402

NOW = dt.datetime(2026, 7, 2, 0, 5, tzinfo=dt.timezone.utc)


class ExtractorTest(unittest.TestCase):
    def test_extract_bullets_takes_top_level_dash_and_dot_bullets(self):
        text = (
            "# Title\n"
            "- first item\n"
            "  > indented quote is skipped\n"
            "• second item\n"
            "not a bullet\n"
            "- third item\n"
        )
        self.assertEqual(
            digest.extract_bullets(text, cap=8),
            ["- first item", "- second item", "- third item"],
        )

    def test_extract_bullets_respects_cap(self):
        text = "\n".join(f"- item {i}" for i in range(20))
        self.assertEqual(len(digest.extract_bullets(text, cap=8)), 8)

    def test_extract_bullets_clamps_very_long_lines(self):
        text = "- " + "x" * 1000
        (line,) = digest.extract_bullets(text, cap=8)
        self.assertLessEqual(len(line), digest.MAX_LINE_CHARS)
        self.assertTrue(line.endswith("…"))

    def test_extract_headings_takes_h3_lines(self):
        text = "## Section\n### [Post One](https://x)\nbody\n### Post Two\n#### h4 skipped\n"
        self.assertEqual(
            digest.extract_headings(text, cap=8),
            ["- [Post One](https://x)", "- Post Two"],
        )

    def test_extract_table_drops_header_and_separator_rows(self):
        text = (
            "| Title | Score | Link |\n"
            "|-------|-------|------|\n"
            "| Story A | 42 | https://a |\n"
            "| Story B | 7 | https://b |\n"
        )
        self.assertEqual(
            digest.extract_table(text, cap=8),
            ["- Story A — https://a", "- Story B — https://b"],
        )


class ComposeTest(unittest.TestCase):
    def _make_research_dir(self, root: Path) -> Path:
        research = root / "research"
        (research / "summaries").mkdir(parents=True)
        (research / "rss").mkdir()
        (research / "blogs").mkdir()
        # Two twitter cycles for today — the latest hour must win.
        (research / "summaries" / "2026-07-02-twitter-01h-summary.txt").write_text(
            "TOP STORIES:\n• early cycle story\n", encoding="utf-8"
        )
        (research / "summaries" / "2026-07-02-twitter-10h-summary.txt").write_text(
            "TOP STORIES:\n• Meta building Meta Compute [✓]\n• Karp attacks tokenmaxxing [⚠]\n",
            encoding="utf-8",
        )
        # Comparison-lane summary sorts lexically after the primary one and
        # must be excluded by the [0-9][0-9]h glob class.
        (research / "summaries" / "2026-07-02-twitter-deepseek-22h-summary.txt").write_text(
            "TOP STORIES:\n• deepseek comparison story must not appear\n",
            encoding="utf-8",
        )
        # RSS only exists for yesterday — the window must fall back to it.
        (research / "rss" / "2026-07-01.md").write_text(
            "# Official AI News - 2026-07-01\n\n"
            "- [Venice AI becomes a unicorn](https://tc/venice) - 2026-07-01\n"
            "  > run-rate revenue detail\n"
            "- [Gemini Spark on Mac](https://tc/spark) - 2026-07-01\n",
            encoding="utf-8",
        )
        (research / "blogs" / "2026-07-02.md").write_text(
            "# AI Expert Blog Watch - 2026-07-02\n\n## P0 Watch Items\n\n"
            "### [Software factories](https://latent.space/p/sf)\n- Source: Latent Space\n",
            encoding="utf-8",
        )
        return research

    def test_compose_writes_digest_and_summary_with_lane_sections(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            research = self._make_research_dir(root)
            out = root / "out" / "2026-07-02-digest.md"
            summary = root / "out" / "2026-07-02-digest-summary.txt"

            extracts = digest.compose(research, "2026-07-02", out, summary, now=NOW)

            text = out.read_text(encoding="utf-8")
            self.assertIn("# AI Daily Digest - 2026-07-02", text)
            self.assertIn("Deterministic fallback digest", text)
            # Latest PRIMARY twitter cycle won, verbatim; the comparison
            # lane's file (lexically later) was excluded.
            self.assertIn("- Meta building Meta Compute [✓]", text)
            self.assertNotIn("early cycle story", text)
            self.assertNotIn("deepseek comparison story", text)
            self.assertIn("2026-07-02-twitter-10h-summary.txt", text)
            # RSS fell back to yesterday's artifact.
            self.assertIn("- [Venice AI becomes a unicorn](https://tc/venice) - 2026-07-01", text)
            # Blogs extracted via headings.
            self.assertIn("- [Software factories](https://latent.space/p/sf)", text)
            # Missing lanes are noted explicitly, not silently dropped.
            self.assertIn("- Hacker News: no artifact for 2026-07-02 or 2026-07-01", text)
            self.assertIn("## Sources Consulted", text)

            summary_text = summary.read_text(encoding="utf-8")
            self.assertIn("deterministic fallback", summary_text)
            self.assertIn("[Twitter/X] Meta building Meta Compute", summary_text)
            self.assertLessEqual(len(summary_text), digest.SUMMARY_MAX_CHARS + 1)

            covered = [e.lane.key for e in extracts if e.lines]
            self.assertEqual(covered, ["twitter", "rss", "blogs"])

    def test_compose_with_empty_research_dir_still_writes_honest_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            research = root / "research"
            research.mkdir()
            out = root / "digest.md"

            extracts = digest.compose(research, "2026-07-02", out, None, now=NOW)

            text = out.read_text(encoding="utf-8")
            self.assertIn("no artifact for 2026-07-02 or 2026-07-01", text)
            self.assertEqual([e for e in extracts if e.lines], [])

    def test_candidate_dates_is_today_then_yesterday(self):
        self.assertEqual(digest.candidate_dates("2026-07-02"), ["2026-07-02", "2026-07-01"])

    def test_empty_today_artifact_falls_through_to_yesterday(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            research = root / "research"
            (research / "blogs").mkdir(parents=True)
            # Today's blogs file exists but has no post headings ("0 posts").
            (research / "blogs" / "2026-07-02.md").write_text(
                "# AI Expert Blog Watch - 2026-07-02\n\n"
                "_No new expert blog posts found for this date._\n",
                encoding="utf-8",
            )
            (research / "blogs" / "2026-07-01.md").write_text(
                "# AI Expert Blog Watch - 2026-07-01\n\n"
                "### [Yesterday's post](https://blog/x)\n",
                encoding="utf-8",
            )

            lane = next(l for l in digest.LANES if l.key == "blogs")
            extract = digest.extract_lane(
                research, lane, ["2026-07-02", "2026-07-01"], cap=8
            )

            self.assertEqual(extract.artifact, "blogs/2026-07-01.md")
            self.assertEqual(extract.lines, ("- [Yesterday's post](https://blog/x)",))

    def test_strip_markdown_flattens_links_and_bold(self):
        self.assertEqual(
            digest.strip_markdown("- **[Venice AI](https://tc)** raised money"),
            "Venice AI raised money",
        )


if __name__ == "__main__":
    unittest.main()
