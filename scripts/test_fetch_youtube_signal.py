#!/usr/bin/env python3
"""Tests for the tuber-backed YouTube signal lane."""

from __future__ import annotations

import datetime as dt
import json
import os
import sys
import tempfile
import unittest
import urllib.error
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock

sys.path.insert(0, os.path.dirname(__file__))

import fetch_youtube_signal as youtube  # noqa: E402


SOURCE = youtube.Source(
    id="ai-podcasts",
    name="AI Podcasts",
    kind="trending",
    priority="P1",
    tags=("interviews", "podcasts"),
    include_in_digest=True,
    count=3,
    topic="ai-podcasts",
    range="1w",
)


class SourceRegistryTest(unittest.TestCase):
    def test_load_sources_validates_shape(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "sources.json"
            path.write_text(
                """
                [{
                  "id": "ai-agents",
                  "name": "AI Agents",
                  "kind": "trending",
                  "topic": "ai-agents",
                  "priority": "P1",
                  "count": 5,
                  "tags": ["agents"],
                  "include_in_digest": true
                }]
                """,
                encoding="utf-8",
            )

            sources = youtube.load_sources(path)

        self.assertEqual(len(sources), 1)
        self.assertEqual(sources[0].topic, "ai-agents")
        self.assertEqual(sources[0].range, "1w")

    def test_duplicate_source_id_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "sources.json"
            path.write_text(
                """
                [
                  {"id":"x","name":"X","kind":"search","query":"x","priority":"P1","count":1},
                  {"id":"x","name":"Y","kind":"search","query":"y","priority":"P1","count":1}
                ]
                """,
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "duplicate source id"):
                youtube.load_sources(path)


class CandidateTest(unittest.TestCase):
    def test_normalize_trending_video_uses_existing_summary(self):
        candidate = youtube.normalize_video(
            SOURCE,
            {
                "id": "gH4FTjDm9FQ",
                "title": "Anthropic model release interview",
                "channel": "All-In Podcast",
                "publishedAt": "3 days ago",
                "views": "381K views",
                "duration": 6120,
                "isSummarized": True,
                "titleAnswer": "The hosts discuss a concrete Anthropic release.",
                "videoScore": {"score": 68, "band": "skim"},
            },
        )

        self.assertIsNotNone(candidate)
        assert candidate is not None
        self.assertEqual(candidate.id, "gH4FTjDm9FQ")
        self.assertEqual(candidate.evidence, "summary")
        self.assertGreater(candidate.score, 70)

    def test_dedupe_keeps_highest_score(self):
        low = youtube.VideoCandidate("dQw4w9WgXcQ", "Low", "https://youtu.be/dQw4w9WgXcQ", SOURCE, score=1)
        high = youtube.VideoCandidate("dQw4w9WgXcQ", "High", "https://youtu.be/dQw4w9WgXcQ", SOURCE, score=2)

        self.assertEqual(youtube.dedupe_candidates([low, high]), [high])

    def test_relative_publish_age_is_parsed(self):
        self.assertEqual(youtube.approximate_age_days("3 days ago"), 3)
        self.assertEqual(youtube.approximate_age_days("Streamed 2 weeks ago"), 14)
        self.assertEqual(youtube.approximate_age_days("1 month ago"), 30)
        self.assertIsNone(youtube.approximate_age_days("unknown"))

    def test_selection_skips_old_daily_candidates(self):
        old = youtube.VideoCandidate(
            "dQw4w9WgXcQ",
            "Old release",
            "https://youtu.be/dQw4w9WgXcQ",
            SOURCE,
            published="1 year ago",
            score=500,
        )
        recent = youtube.VideoCandidate(
            "gH4FTjDm9FQ",
            "Recent release",
            "https://youtu.be/gH4FTjDm9FQ",
            SOURCE,
            published="3 days ago",
            score=100,
            evidence="summary",
        )

        selected, skipped = youtube.select_high_signal([old, recent], max_items=5, min_score=80, max_age_days=14)

        self.assertEqual([item.id for item in selected], ["gH4FTjDm9FQ"])
        self.assertEqual(skipped[0].skipped_reason, "older than recency window (1 year ago)")

    def test_selection_skips_unknown_publish_age(self):
        unknown = youtube.VideoCandidate(
            "dQw4w9WgXcQ",
            "Unknown age release",
            "https://youtu.be/dQw4w9WgXcQ",
            SOURCE,
            published="Jun 1, 2025",
            score=500,
            evidence="summary",
        )

        selected, skipped = youtube.select_high_signal([unknown], max_items=5, min_score=80, max_age_days=14)

        self.assertEqual(selected, [])
        self.assertEqual(skipped[0].skipped_reason, "unknown publish age")

    def test_collect_records_per_source_error(self):
        def fake_fetch(_base, _path, _params):
            raise OSError("network down")

        candidates, errors = youtube.collect_candidates([SOURCE], base_url="https://tuber.example", fetch_json_fn=fake_fetch)

        self.assertEqual(candidates, [])
        self.assertEqual(len(errors), 1)
        self.assertIn("network down", errors[0][1])

    def test_enrich_promotes_summary_preview_without_paid_generation(self):
        candidate = youtube.VideoCandidate("dQw4w9WgXcQ", "Demo", "https://youtu.be/dQw4w9WgXcQ", SOURCE, score=80)
        calls = []

        def fake_fetch(_base, path, _params):
            calls.append(path)
            return {"available": True, "titleAnswer": "Existing generated summary from cache."}

        errors = youtube.enrich_candidates(
            [candidate],
            base_url="https://tuber.example",
            max_preview_checks=1,
            max_transcript_checks=0,
            fetch_json_fn=fake_fetch,
        )

        self.assertEqual(errors, [])
        self.assertEqual(candidate.evidence, "summary")
        self.assertIn("/summary-preview", calls[0])
        self.assertNotIn("summarize", calls[0])

    def test_fetch_json_refuses_generation_endpoints(self):
        with self.assertRaisesRegex(ValueError, "refusing non-read-only"):
            youtube.fetch_json("https://tuber.example", "/video/dQw4w9WgXcQ/summarize", None)
        with self.assertRaisesRegex(ValueError, "refusing non-read-only"):
            youtube.fetch_json("https://tuber.example", "/acp/jobs/youtube-summary", None)

    def test_key_claims_avoid_single_sentence_summary_duplication(self):
        candidate = youtube.VideoCandidate(
            "dQw4w9WgXcQ",
            "Official model demo",
            "https://youtu.be/dQw4w9WgXcQ",
            SOURCE,
            title_answer="This is the single sentence used for why it matters.",
        )

        self.assertEqual(youtube.key_claims(candidate), ["Official model demo"])

    def test_key_claims_filter_incomplete_transcript_fragments(self):
        candidate = youtube.VideoCandidate(
            "dQw4w9WgXcQ",
            "Fallback title",
            "https://youtu.be/dQw4w9WgXcQ",
            SOURCE,
            transcript_snippet="Fable 5 is a",
        )

        self.assertEqual(youtube.key_claims(candidate), ["Fallback title"])

    def test_key_claims_require_sentence_end(self):
        candidate = youtube.VideoCandidate(
            "dQw4w9WgXcQ",
            "Fallback title",
            "https://youtu.be/dQw4w9WgXcQ",
            SOURCE,
            transcript_snippet="This complete sentence should stay. This fragment should",
        )

        self.assertEqual(youtube.key_claims(candidate), ["This complete sentence should stay."])

    def test_why_it_matters_falls_back_for_non_english_summary(self):
        candidate = youtube.VideoCandidate(
            "dQw4w9WgXcQ",
            "English title",
            "https://youtu.be/dQw4w9WgXcQ",
            SOURCE,
            title_answer="한국어 요약입니다. 영어가 아닙니다.",
        )

        self.assertIn("not English", youtube.why_it_matters(candidate))


class RenderAndMainTest(unittest.TestCase):
    def test_render_markdown_matches_lane_contract(self):
        candidate = youtube.VideoCandidate(
            id="dQw4w9WgXcQ",
            title="Official agent demo",
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            source=SOURCE,
            channel="Example",
            published="1 day ago",
            views="10K views",
            score=120,
            evidence="summary",
            title_answer="An official demo shows agent workflow improvements.",
        )
        text = youtube.render_markdown(
            target_date=dt.date(2026, 6, 17),
            sources=[SOURCE],
            candidates=[candidate],
            selected=[candidate],
            skipped=[],
            fetch_errors=[],
            enrich_errors=[],
            base_url="https://tuber.example",
        )

        self.assertIn("# YouTube AI Signal - 2026-06-17", text)
        self.assertIn("- Evidence: summary", text)
        self.assertIn("- Paid/generated summaries requested: 0", text)
        self.assertIn("## Watchlist / Skipped", text)

    def test_main_writes_markdown(self):
        with tempfile.TemporaryDirectory() as td:
            registry = Path(td) / "sources.json"
            out_dir = Path(td) / "out"
            registry.write_text(
                """
                [{
                  "id":"example",
                  "name":"Example Search",
                  "kind":"search",
                  "query":"example",
                  "priority":"P1",
                  "count":1,
                  "tags":["official"],
                  "include_in_digest":true
                }]
                """,
                encoding="utf-8",
            )

            original_collect = youtube.collect_candidates
            original_enrich = youtube.enrich_candidates
            try:
                source = youtube.load_sources(registry)[0]
                candidate = youtube.VideoCandidate(
                    id="dQw4w9WgXcQ",
                    title="Example model release",
                    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    source=source,
                    published="1 day ago",
                    score=120,
                    evidence="summary",
                    title_answer="A release summary exists.",
                )
                youtube.collect_candidates = lambda sources, base_url: ([candidate], [])
                youtube.enrich_candidates = lambda candidates, **kwargs: []
                rc = youtube.main([
                    "--registry", str(registry),
                    "--out-dir", str(out_dir),
                    "--date", "2026-06-17",
                    "--tuber-api-base", "https://tuber.example",
                ])
                text = (out_dir / "2026-06-17.md").read_text(encoding="utf-8")
            finally:
                youtube.collect_candidates = original_collect
                youtube.enrich_candidates = original_enrich

        self.assertEqual(rc, 0)
        self.assertIn("Example model release", text)


GUARD_REGISTRY = [
    {
        "id": "down-channel",
        "name": "Down Channel",
        "kind": "channel",
        "channel": "@downchannel",
        "priority": "P0",
        "count": 5,
        "tags": ["official"],
        "include_in_digest": True,
    },
    {
        "id": "up-search",
        "name": "Up Search",
        "kind": "search",
        "query": "ai news",
        "priority": "P1",
        "count": 5,
        "tags": ["research"],
        "include_in_digest": True,
    },
]


class TotalFetchFailureGuardTest(unittest.TestCase):
    """Total signal loss must fail loudly, not commit an empty artifact.

    2026-07-12 incident: tuber-api returned HTTP 502 for all 10 sources and
    the lane still committed a fresh-dated file ("Unique videos collected: 0
    / Fetch errors: 10") with exit 0. The git-recency freshness watchdog
    (scripts/check_lane_freshness.py) can never catch that shape because the
    file exists and is dated today. main() must instead exit
    EXIT_TOTAL_FETCH_FAILURE (3) and write nothing when EVERY checked source
    produced a fetch error and zero candidates were collected, while partial
    failures keep the current always-write behavior.
    """

    API_BASE = "https://tuber-api.test.invalid"

    def run_main(self, td, fake_fetch, registry_rows=None):
        """Run main() with the per-source network boundary stubbed out.

        fetch_source_candidates is resolved as a module global inside
        collect_candidates, so patching it exercises the real per-source
        error accumulation. Enrichment budgets are zeroed so
        enrich_candidates makes no network calls of its own.
        """
        registry = Path(td) / "sources.json"
        registry.write_text(
            json.dumps(GUARD_REGISTRY if registry_rows is None else registry_rows),
            encoding="utf-8",
        )
        out_dir = Path(td) / "out"
        stdout, stderr = StringIO(), StringIO()
        with mock.patch.object(youtube, "fetch_source_candidates", fake_fetch):
            with redirect_stdout(stdout), redirect_stderr(stderr):
                rc = youtube.main(
                    [
                        "--registry", str(registry),
                        "--out-dir", str(out_dir),
                        "--date", "2026-07-12",
                        "--tuber-api-base", self.API_BASE,
                        "--max-preview-checks", "0",
                        "--max-transcript-checks", "0",
                    ]
                )
        return rc, stdout.getvalue(), stderr.getvalue(), out_dir / "2026-07-12.md"

    @staticmethod
    def all_sources_down(source, *, base_url, fetch_json_fn=None):
        raise urllib.error.URLError("tuber-api unreachable (HTTP 502)")

    def test_total_failure_exits_3_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as td:
            rc, out, err, out_path = self.run_main(td, self.all_sources_down)

            self.assertEqual(rc, youtube.EXIT_TOTAL_FETCH_FAILURE)
            self.assertEqual(rc, 3)  # distinct from 2 (argument validation)
            self.assertFalse(out_path.exists())
            self.assertFalse(out_path.parent.exists())  # no partial output either
            self.assertNotIn("Wrote", out)
            self.assertIn("ERROR:", err)
            self.assertIn(self.API_BASE, err)
            # Per-source error summary names every failed source.
            self.assertIn("Down Channel", err)
            self.assertIn("Up Search", err)
            self.assertIn("URLError", err)

    def test_partial_failure_still_writes_daily_file(self):
        def one_source_up(source, *, base_url, fetch_json_fn=None):
            if source.id == "down-channel":
                raise urllib.error.URLError("tuber-api unreachable (HTTP 502)")
            candidate = youtube.normalize_video(
                source,
                {
                    "id": "gH4FTjDm9FQ",
                    "title": "OpenAI announces a new reasoning model",
                    "publishedAt": "2 days ago",
                    "channel": "Up Search Channel",
                },
            )
            assert candidate is not None
            return [candidate]

        with tempfile.TemporaryDirectory() as td:
            rc, out, err, out_path = self.run_main(td, one_source_up)

            self.assertEqual(rc, 0)
            self.assertTrue(out_path.exists())
            text = out_path.read_text(encoding="utf-8")
            self.assertIn("Unique videos collected: 1", text)
            self.assertIn("Fetch errors: 1", text)
            self.assertIn("Wrote", out)

    def test_empty_registry_keeps_current_write_behavior(self):
        # The guard requires at least one checked source: an empty registry
        # is a configuration state, not a fetch outage, and keeps writing.
        with tempfile.TemporaryDirectory() as td:
            rc, _out, _err, out_path = self.run_main(td, self.all_sources_down, registry_rows=[])

            self.assertEqual(rc, 0)
            self.assertTrue(out_path.exists())
            self.assertIn("Sources checked: 0", out_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
