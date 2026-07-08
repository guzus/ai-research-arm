#!/usr/bin/env python3
"""Tests for the deterministic daily-digest fallback composer (no network)."""

from __future__ import annotations

import datetime as dt
import os
import re
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
            # Canonical Executive Summary (the front-page renderer's lead/deck
            # source): lane-labelled first excerpt of each covered lane,
            # placed before the per-lane sections.
            self.assertIn("## Executive Summary", text)
            self.assertIn("- **Twitter/X:** Meta building Meta Compute [✓]", text)
            self.assertIn("- **RSS / Official Announcements:** [Venice AI becomes a unicorn]", text)
            self.assertLess(text.index("## Executive Summary"), text.index("## Twitter/X"))
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


class FrontPageRendererParityTest(unittest.TestCase):
    """Literal Python ports of scripts/render_front_page.mjs's extraction
    logic (`section()`, record extraction, `stripMarkdown`, and the `lead`
    selection chain). Guards the contract that both fallback and Claude-written
    digests populate the front page's masthead instead of regressing to a
    `# `-prefixed lead."""

    @staticmethod
    def _js_section(markdown: str, name: str) -> str:
        # JS: ^##\s+NAME\s*$([\s\S]*?)(?=^##\s+|(?![\s\S])) with flags mi
        pattern = re.compile(
            rf"^##\s+{name}\s*$(.*?)(?=^##\s+|\Z)", re.M | re.I | re.S
        )
        match = pattern.search(markdown)
        return match.group(1).strip() if match else ""

    @classmethod
    def _js_section_any(cls, markdown: str, names: list[str]) -> str:
        for name in names:
            value = cls._js_section(markdown, name)
            if value:
                return value
        return ""

    @staticmethod
    def _js_strip_markdown(value: str) -> str:
        value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
        value = re.sub(r"\*\*([^*]+)\*\*", r"\1", value)
        value = re.sub(r"\*([^*]+)\*", r"\1", value)
        value = re.sub(r"`([^`]+)`", r"\1", value)
        value = value.replace("**", "")
        value = re.sub(r"[*_\[\]]", "", value)
        value = re.sub(r"^[-*]\s+", "", value)
        value = re.sub(r"^\d+\.\s+", "", value)
        return re.sub(r"\s+", " ", value).strip()

    @classmethod
    def _js_bullet_records(cls, text: str, limit: int) -> list[str]:
        out = []
        for line in text.split("\n"):
            line = line.strip()
            if not re.match(r"^([-*]|\d+\.)\s+", line):
                continue
            stripped = cls._js_strip_markdown(line)
            if stripped:
                out.append(stripped)
            if len(out) >= limit:
                break
        return out

    @classmethod
    def _js_paragraph_records(cls, text: str, limit: int) -> list[str]:
        out = []
        for block in re.split(r"\n{2,}", text):
            stripped = cls._js_strip_markdown(block)
            if stripped and not stripped.startswith("#"):
                out.append(stripped)
            if len(out) >= limit:
                break
        return out

    @classmethod
    def _js_section_records(cls, text: str, limit: int) -> list[str]:
        records = cls._js_bullet_records(text, limit)
        return records or cls._js_paragraph_records(text, limit)

    @classmethod
    def _js_paragraphs(cls, text: str, limit: int) -> list[str]:
        out = []
        for block in re.split(r"\n{2,}", text):
            stripped = cls._js_strip_markdown(block)
            if stripped:
                out.append(stripped)
            if len(out) >= limit:
                break
        return out

    def _compose_fallback_digest(self, root: Path) -> str:
        research = root / "research"
        (research / "summaries").mkdir(parents=True)
        (research / "rss").mkdir()
        (research / "summaries" / "2026-07-02-twitter-10h-summary.txt").write_text(
            "TOP STORIES:\n• Meta building Meta Compute\n", encoding="utf-8"
        )
        (research / "rss" / "2026-07-02.md").write_text(
            "# Official AI News\n\n- [Venice AI raises](https://tc/v) - 2026-07-01\n",
            encoding="utf-8",
        )
        out = root / "digest.md"
        digest.compose(research, "2026-07-02", out, None, now=NOW)
        return out.read_text(encoding="utf-8")

    def test_renderer_extracts_lead_and_deck_from_fallback_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            markdown = self._compose_fallback_digest(Path(tmp))

            executive = self._js_section_records(self._js_section(markdown, "Executive Summary"), 5)
            lead = (executive or self._js_paragraphs(markdown, 1))[0]

            self.assertGreaterEqual(len(executive), 2)
            self.assertEqual(lead, executive[0])
            self.assertFalse(lead.startswith("#"))
            self.assertIn("Meta building Meta Compute", lead)
            self.assertIn("Venice AI raises", executive[1])

    def test_without_executive_summary_lead_regresses_to_hash_title(self):
        # Control experiment: strip the Executive Summary section and confirm
        # the renderer's fallback chain would produce the broken `# `-lead —
        # i.e. this suite genuinely guards the failure mode it claims to.
        with tempfile.TemporaryDirectory() as tmp:
            markdown = self._compose_fallback_digest(Path(tmp))
            gutted = re.sub(
                r"^## Executive Summary$.*?(?=^## )", "", markdown, flags=re.M | re.S
            )

            executive = self._js_section_records(self._js_section(gutted, "Executive Summary"), 5)
            lead = (executive or self._js_paragraphs(gutted, 1))[0]

            self.assertEqual(executive, [])
            self.assertTrue(lead.startswith("#"))

    def test_renderer_extracts_paragraph_lead_and_alternate_claude_headings(self):
        markdown = (
            "# AI Daily Digest - 2026-07-08\n\n"
            "## Executive Summary\n\n"
            "The day's clearest throughline is a widening gap between the US and China on model export policy. "
            "Infrastructure economics are the second-order story.\n\n"
            "## Lead Developments\n\n"
            "**GPT-5.6's Thursday launch is the best-corroborated story of the day.** OpenAI previewed Sol, Terra, and Luna.\n\n"
            "**Claude Cowork's mobile/web expansion is confirmed.** Three outlets reported it.\n\n"
            "## Model Releases & Product Updates\n\n"
            "- **OpenAI GPT-5.6 (Sol/Terra/Luna)** -- limited preview live.\n"
            "- **Claude Cowork** -- now available on mobile and web.\n\n"
            "## Policy, Safety & Market Context\n\n"
            "The US-China export-control picture cuts both ways today.\n\n"
            "On the market/infrastructure side: Microsoft is phasing external models out of Copilot-adjacent products.\n\n"
            "On safety/incidents specifically: GitLost and HalluSquatting kept agent security in focus.\n"
        )

        executive = self._js_section_records(self._js_section(markdown, "Executive Summary"), 5)
        breaking = self._js_section_records(
            self._js_section_any(markdown, ["Breaking News", "Lead Developments"]), 3
        )
        models = self._js_section_records(
            self._js_section_any(markdown, ["Model Releases & Updates", "Model Releases & Product Updates"]),
            4,
        )
        policy_context = self._js_section_any(
            markdown, ["Policy & Regulation", "Policy, Safety & Market Context"]
        )
        policy_paragraphs = self._js_paragraph_records(policy_context, 4)
        policy = [policy_paragraphs[0], *policy_paragraphs[2:3]]
        business = [policy_paragraphs[1]]
        lead = (executive or self._js_paragraphs(markdown, 1))[0]

        self.assertFalse(lead.startswith("#"))
        self.assertIn("widening gap between the US and China", lead)
        self.assertIn("GPT-5.6's Thursday launch", breaking[0])
        self.assertIn("OpenAI GPT-5.6", models[0])
        self.assertIn("US-China export-control", policy[0])
        self.assertIn("GitLost", policy[1])
        self.assertIn("Microsoft is phasing", business[0])


if __name__ == "__main__":
    unittest.main()
