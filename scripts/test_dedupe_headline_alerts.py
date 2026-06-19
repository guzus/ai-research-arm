#!/usr/bin/env python3

import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import dedupe_headline_alerts as dedupe


class DedupeHeadlineAlertsTest(unittest.TestCase):
    def test_normalize_url_twitter_variants(self):
        left = "http://www.twitter.com/OpenAI/status/123?s=20&utm_source=x"
        right = "https://x.com/OpenAI/status/123/"
        self.assertEqual(dedupe.normalize_url(left), dedupe.normalize_url(right))
        self.assertEqual(dedupe.external_key(left), "x:status:123")

    def test_same_source_and_similar_headline_is_duplicate(self):
        history = [
            dedupe.make_record(
                {
                    "headline": "OPENAI MODELS ARRIVING ON AWS BEDROCK IN COMING WEEKS",
                    "url": "https://x.com/testingcatalog/status/2048913264013197748",
                },
                "2026-04-28 01:00 UTC",
            )
        ]
        item = {
            "headline": "OPENAI MODELS COMING TO AWS BEDROCK — AMAZON HOSTS APRIL 28 LIVESTREAM",
            "url": "https://twitter.com/testingcatalog/status/2048913264013197748?s=20",
        }
        self.assertEqual(
            dedupe.duplicate_reason(item, history),
            "duplicate_source_similar_headline",
        )

    def test_same_source_but_distinct_rollup_story_is_not_duplicate(self):
        history = [
            dedupe.make_record(
                {
                    "headline": "OPENAI OPEN-SOURCES SYMPHONY — EVERY GITHUB ISSUE GETS ITS OWN CODEX AGENT",
                    "url": "https://x.com/maocaohu/status/2049065198649253960",
                },
                "2026-04-28 09:00 UTC",
            )
        ]
        item = {
            "headline": "DEEPSEEK CUTS API CACHE PRICING TO 1/10 ACROSS THE BOARD",
            "url": "https://x.com/maocaohu/status/2049065198649253960",
        }
        self.assertEqual(dedupe.duplicate_reason(item, history), "")

    def test_exact_headline_is_duplicate_even_with_different_url(self):
        history = [
            dedupe.make_record(
                {
                    "headline": "MUSK V ALTMAN TRIAL OPENS IN OAKLAND",
                    "url": "https://x.com/a/status/1",
                },
                "2026-04-28 01:00 UTC",
            )
        ]
        item = {
            "headline": "Musk v. Altman trial opens in Oakland!",
            "url": "https://x.com/b/status/2",
        }
        self.assertEqual(dedupe.duplicate_reason(item, history), "duplicate_headline")

    def test_corrupt_history_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "history.json"
            path.write_text("{not json")
            with self.assertRaises(SystemExit):
                dedupe.load_json_list(path)

    def test_filter_writes_only_new_items(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            history_file = root / "history.json"
            headlines_file = root / "headlines.json"
            filtered_file = root / "filtered.json"
            history_file.write_text(
                json.dumps(
                    [
                        dedupe.make_record(
                            {
                                "headline": "XIAOMI MIMO-V2.5 LANDS ON HUGGING FACE",
                                "url": "https://x.com/_akhaliq/status/2048861462991360155",
                            },
                            "2026-04-27 21:00 UTC",
                        )
                    ]
                )
            )
            headlines_file.write_text(
                json.dumps(
                    [
                        {
                            "headline": "XIAOMI OPEN-SOURCES MIMO-V2.5 ON HUGGING FACE UNDER MIT LICENSE",
                            "url": "https://x.com/_akhaliq/status/2048861462991360155",
                        },
                        {
                            "headline": "SAKANA AI LAUNCHES FUGU BETA",
                            "url": "https://x.com/hardmaru/status/2048954720761635041",
                        },
                    ]
                )
            )
            with redirect_stdout(StringIO()):
                rc = dedupe.main(
                    [
                        "filter",
                        "--headlines-file",
                        str(headlines_file),
                        "--history-file",
                        str(history_file),
                        "--filtered-file",
                        str(filtered_file),
                        "--timestamp",
                        "2026-04-28 04:00 UTC",
                    ]
                )
            self.assertEqual(rc, 0)
            self.assertEqual(
                json.loads(filtered_file.read_text()),
                [
                    {
                        "headline": "SAKANA AI LAUNCHES FUGU BETA",
                        "url": "https://x.com/hardmaru/status/2048954720761635041",
                    }
                ],
            )

    def test_record_delivered_appends_with_retention(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            history_file = root / "history.json"
            delivered_file = root / "delivered.json"
            history_file.write_text(json.dumps([{"headline": "OLD"}]))
            delivered_file.write_text(
                json.dumps(
                    [
                        {
                            "headline": "NEW ALERT",
                            "source": "@source",
                            "url": "https://x.com/source/status/123",
                            "category": "model",
                        }
                    ]
                )
            )
            with redirect_stdout(StringIO()):
                rc = dedupe.main(
                    [
                        "record-delivered",
                        "--delivered-file",
                        str(delivered_file),
                        "--history-file",
                        str(history_file),
                        "--timestamp",
                        "2026-04-28 10:00 UTC",
                        "--retention",
                        "1",
                    ]
                )
            self.assertEqual(rc, 0)
            history = json.loads(history_file.read_text())
            self.assertEqual(len(history), 1)
            self.assertEqual(history[0]["headline"], "NEW ALERT")
            # Derived keys are recomputed from headline/url at read time, so
            # they should NOT be persisted on disk.
            self.assertNotIn("headline_key", history[0])
            self.assertNotIn("url_key", history[0])
            self.assertNotIn("external_key", history[0])
            # The recomputed key still resolves correctly.
            self.assertEqual(dedupe.item_keys(history[0]).external_key, "x:status:123")

    def test_legacy_history_with_stored_keys_still_dedupes(self):
        # Old-format records (with stored *_key fields) and new-format records
        # (without) must both dedupe correctly, since item_keys() recomputes.
        legacy = {
            "headline": "OPENAI MODELS COMING TO AWS BEDROCK",
            "url": "https://x.com/testingcatalog/status/2048913264013197748",
            "headline_key": "STALE_VALUE_THAT_SHOULD_BE_IGNORED",
            "url_key": "stale://value",
            "external_key": "x:status:WRONG",
        }
        item = {
            "headline": "OpenAI models coming to AWS Bedrock",
            "url": "https://twitter.com/testingcatalog/status/2048913264013197748?s=20",
        }
        # Without precomputed keys, duplicate_reason recomputes for the legacy
        # record and detects the duplicate via headline_key.
        self.assertEqual(dedupe.duplicate_reason(item, [legacy]), "duplicate_headline")

    # ── cross-source semantic duplicate (different account/URL, paraphrased) ──

    def test_cross_source_similar_headline_is_duplicate(self):
        # The same hire reported by two different accounts with paraphrased wording —
        # different URLs, so the same-URL check can't see it. With a reference `now`
        # inside the window it is caught as a cross-source duplicate (Jaccard ~0.71).
        history = [
            dedupe.make_record(
                {
                    "headline": "OPENAI HIRES EX-WHITE HOUSE AI ADVISER DEAN BALL AS HEAD OF STRATEGIC FUTURES",
                    "url": "https://x.com/Polymarket/status/2066900000000000001",
                },
                "2026-06-18 01:00 UTC",
            )
        ]
        item = {
            "headline": "OPENAI HIRES EX-TRUMP AI POLICY ADVISER DEAN BALL AS HEAD OF STRATEGIC FUTURES",
            "url": "https://x.com/another_source/status/2066900000000000002",
        }
        now = dedupe.parse_delivered_at("2026-06-18 03:00 UTC")
        self.assertEqual(
            dedupe.duplicate_reason(item, history, now=now),
            "duplicate_cross_source_similar_headline",
        )

    def test_cross_source_append_fact_progression_is_not_duplicate(self):
        # Flash -> updated-with-details. The follow-up carries genuinely new facts and
        # must survive. Containment would score this 1.0 (the short headline is a subset);
        # Jaccard drops it to ~0.375 and the shared-token floor (3 < 4) also rejects it.
        history = [
            dedupe.make_record(
                {"headline": "META RELEASES LLAMA 5", "url": "https://x.com/a/status/1"},
                "2026-06-18 01:00 UTC",
            )
        ]
        item = {
            "headline": "META RELEASES LLAMA 5 WITH 2M TOKEN CONTEXT AND NATIVE VOICE",
            "url": "https://x.com/b/status/2",
        }
        now = dedupe.parse_delivered_at("2026-06-18 02:00 UTC")
        self.assertEqual(dedupe.duplicate_reason(item, history, now=now), "")

    def test_cross_source_short_headline_containment_is_not_duplicate(self):
        # The short-subset false positive: "ANTHROPIC RAISES $5B" is a token-subset of
        # the longer, distinct headline (containment 1.0). Jaccard (~0.43) + the overlap
        # floor (3 < 4) keep it from being suppressed.
        history = [
            dedupe.make_record(
                {"headline": "ANTHROPIC RAISES $5B", "url": "https://x.com/a/status/1"},
                "2026-06-18 01:00 UTC",
            )
        ]
        item = {
            "headline": "ANTHROPIC RAISES CONCERNS ABOUT $5B SAFETY FUND",
            "url": "https://x.com/b/status/2",
        }
        now = dedupe.parse_delivered_at("2026-06-18 02:00 UTC")
        self.assertEqual(dedupe.duplicate_reason(item, history, now=now), "")

    def test_cross_source_distinct_milestone_is_not_duplicate(self):
        # Same beat (SpaceX IPO) but genuinely different milestones (marketing-start vs
        # pricing). Jaccard ~0.31 keeps them apart.
        history = [
            dedupe.make_record(
                {
                    "headline": "SPACEX PRICES IPO: 555.6M SHARES AT $135, ~$75B RAISE, ~$1.75T VALUATION",
                    "url": "https://x.com/a/status/1",
                },
                "2026-06-18 01:00 UTC",
            )
        ]
        item = {
            "headline": "SPACEX IPO MARKETING STARTS JUNE 4 — $75B RAISE AT ~$1.75T, ON TRACK TO BE LARGEST",
            "url": "https://x.com/b/status/2",
        }
        now = dedupe.parse_delivered_at("2026-06-18 02:00 UTC")
        self.assertEqual(dedupe.duplicate_reason(item, history, now=now), "")

    def test_cross_source_inert_without_now(self):
        # No reference time -> cross-source pass is skipped entirely, preserving exact
        # 2-arg legacy behavior even for near-identical different-URL headlines.
        history = [
            dedupe.make_record(
                {"headline": "OPENAI HIRES NOAM SHAZEER FROM GOOGLE DEEPMIND", "url": "https://x.com/a/status/1"},
                "2026-06-18 01:00 UTC",
            )
        ]
        item = {
            "headline": "OPENAI HIRES NOAM SHAZEER AWAY FROM GOOGLE DEEPMIND",
            "url": "https://x.com/b/status/2",
        }
        self.assertEqual(dedupe.duplicate_reason(item, history), "")

    def test_cross_source_outside_window_is_not_duplicate(self):
        # A near-identical headline delivered well outside the recency window is treated
        # as a (rare) recurring beat, not a duplicate, and is delivered.
        history = [
            dedupe.make_record(
                {"headline": "OPENAI HIRES NOAM SHAZEER FROM GOOGLE DEEPMIND", "url": "https://x.com/a/status/1"},
                "2026-05-01 01:00 UTC",
            )
        ]
        item = {
            "headline": "OPENAI HIRES NOAM SHAZEER AWAY FROM GOOGLE DEEPMIND",
            "url": "https://x.com/b/status/2",
        }
        now = dedupe.parse_delivered_at("2026-06-18 01:00 UTC")  # ~48 days later
        self.assertEqual(dedupe.duplicate_reason(item, history, now=now), "")

    def test_cross_source_unparseable_delivered_at_fails_open(self):
        # A single record with a corrupt delivered_at must not eat a real alert: the
        # window check fails open (treats it as out-of-window) and the item is delivered.
        history = [
            dedupe.make_record(
                {"headline": "OPENAI HIRES NOAM SHAZEER FROM GOOGLE DEEPMIND", "url": "https://x.com/a/status/1"},
                "not-a-timestamp",
            )
        ]
        item = {
            "headline": "OPENAI HIRES NOAM SHAZEER AWAY FROM GOOGLE DEEPMIND",
            "url": "https://x.com/b/status/2",
        }
        now = dedupe.parse_delivered_at("2026-06-18 01:00 UTC")
        self.assertEqual(dedupe.duplicate_reason(item, history, now=now), "")

    def test_exact_headline_still_takes_priority_with_now(self):
        # Enabling the cross-source pass must not change which reason wins: the exact
        # (priority) pass still returns first.
        history = [
            dedupe.make_record(
                {"headline": "MUSK V ALTMAN TRIAL OPENS IN OAKLAND", "url": "https://x.com/a/status/1"},
                "2026-06-18 01:00 UTC",
            )
        ]
        item = {"headline": "Musk v. Altman trial opens in Oakland!", "url": "https://x.com/b/status/2"}
        now = dedupe.parse_delivered_at("2026-06-18 02:00 UTC")
        self.assertEqual(dedupe.duplicate_reason(item, history, now=now), "duplicate_headline")

    def test_filter_suppresses_in_batch_cross_source_paraphrase(self):
        # Two different-account paraphrases of the same story in ONE cycle: the first is
        # accepted (and appended to history at the run timestamp), so the second is caught
        # as a cross-source duplicate. Exactly one survives.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            history_file = root / "history.json"
            headlines_file = root / "headlines.json"
            filtered_file = root / "filtered.json"
            history_file.write_text("[]")
            headlines_file.write_text(
                json.dumps(
                    [
                        {
                            "headline": "OPENAI HIRES EX-WHITE HOUSE AI ADVISER DEAN BALL AS HEAD OF STRATEGIC FUTURES",
                            "url": "https://x.com/src1/status/1",
                        },
                        {
                            "headline": "OPENAI HIRES EX-TRUMP AI POLICY ADVISER DEAN BALL AS HEAD OF STRATEGIC FUTURES",
                            "url": "https://x.com/src2/status/2",
                        },
                    ]
                )
            )
            with redirect_stdout(StringIO()):
                rc = dedupe.main(
                    [
                        "filter",
                        "--headlines-file",
                        str(headlines_file),
                        "--history-file",
                        str(history_file),
                        "--filtered-file",
                        str(filtered_file),
                        "--timestamp",
                        "2026-06-18 04:00 UTC",
                    ]
                )
            self.assertEqual(rc, 0)
            filtered = json.loads(filtered_file.read_text())
            self.assertEqual(len(filtered), 1)


if __name__ == "__main__":
    unittest.main()
