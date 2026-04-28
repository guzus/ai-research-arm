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
            self.assertEqual(history[0]["external_key"], "x:status:123")


if __name__ == "__main__":
    unittest.main()
