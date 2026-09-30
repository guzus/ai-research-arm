#!/usr/bin/env python3
"""Preserve evidence while removing repeated model-lane input work."""

from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile
import unittest

import prepare_model_timeline_inputs as inputs


AS_OF = datetime(2026, 9, 30, 3, 22, 57, tzinfo=timezone.utc)


def tweet(identifier, timestamp="2026-09-30T01:00:00Z", **extra):
    return {"id": identifier, "createdAt": timestamp, "text": "Complete source text",
            "author": {"username": "example"}, **extra}


def write_json(path, data):
    path.write_text(json.dumps(data), encoding="utf-8")


class PrepareModelTimelineInputsTest(unittest.TestCase):
    def test_inclusive_utc_cutoff_and_unknown_dates_are_visible(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            rows = [tweet("at", "2026-09-29T03:22:57Z"),
                    tweet("before", "2026-09-29T03:22:56Z"),
                    tweet("offset", "2026-09-29T12:22:57+09:00"),
                    tweet("rfc", "Tue Sep 29 03:22:57 +0000 2026"),
                    tweet("unknown", "bad date"), tweet("missing", None),
                    tweet("naive", "2026-09-30T01:00:00"),
                    tweet("future", "2026-10-01T01:00:00Z")]
            write_json(root / "account.json", rows)
            records, stats = inputs.prepare_signal(root, AS_OF)
            by_id = {row["key"]: row for row in records}
            self.assertNotIn("id:before", by_id)
            self.assertEqual(stats["excluded_old_groups"], 1)
            for name in ("at", "offset", "rfc"):
                self.assertEqual(by_id["id:" + name]["variants"][0]["timestamp_status"], "within_window")
            for name in ("unknown", "missing", "naive"):
                self.assertEqual(by_id["id:" + name]["variants"][0]["timestamp_status"], "unknown")
            self.assertEqual(by_id["id:future"]["variants"][0]["timestamp_status"], "future")

    def test_dedup_merges_provenance_without_losing_richer_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            basic = tweet("123", urls=["https://example.org/source"])
            rich = {**basic, "quotedTweet": tweet("old", "2026-07-01T00:00:00Z",
                        text="Quoted evidence remains complete"),
                    "retweetedTweet": {"id": "r", "text": "Reposted text"},
                    "media": [{"type": "photo", "url": "https://example.org/media"}],
                    "full_text": "Full untruncated source text"}
            write_json(root / "company.json", [basic, rich])
            write_json(root / "search.json", [rich])
            records, stats = inputs.prepare_signal(root, AS_OF)
            self.assertEqual(stats["raw_observations"], 3)
            self.assertEqual(len(records), 1)
            variants = records[0]["variants"]
            self.assertEqual([v["payload"] for v in variants], [basic, rich])
            self.assertEqual(variants[1]["provenance"], [
                {"path": str((root / "company.json").resolve()), "index": 1},
                {"path": str((root / "search.json").resolve()), "index": 0}])

    def test_conflicting_dates_keep_every_variant_of_retained_id(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            rows = [tweet("same", "2026-07-01T00:00:00Z", text="Older richer account evidence"),
                    tweet("same"), tweet(None), tweet(None, text="Different unidentified tweet")]
            write_json(root / "account.json", rows)
            records, _ = inputs.prepare_signal(root, AS_OF)
            self.assertEqual(len(records), 3)
            self.assertEqual([v["payload"] for v in records[0]["variants"]], rows[:2])

    def test_malformed_inputs_fail_instead_of_silently_disappearing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "account.json"
            for text in ("{broken", '{"unexpected":"shape"}', '["not a tweet object"]'):
                with self.subTest(text=text):
                    path.write_text(text)
                    with self.assertRaises(ValueError):
                        inputs.prepare_signal(root, AS_OF)

    def test_inventory_includes_closed_dedup_and_cautious_closure_facts(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for slug, status in (("closed", "closed"), ("shipped", "released"), ("rumor", "rumored")):
                (root / f"{slug}.md").write_text(f"""---
slug: {slug}
title: Full title for {slug}
company: Example
model: Model
status: {status}
verification: unverified
created_at: 2026-07-01
updated_at: 2026-09-01
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-01
    change: Hypothetical release mentioned here is not a structured release date.
---
Long narrative that must not be bulk-copied.
""")
            rows = inputs.ticket_inventory(root, AS_OF)
            self.assertEqual(len(rows), 3)
            by_slug = {row["slug"]: row for row in rows}
            self.assertEqual(by_slug["closed"]["status"], "closed")
            self.assertNotIn("closure_review", by_slug["closed"])
            self.assertIn("actual release date", by_slug["shipped"]["closure_review"])
            self.assertEqual(str(by_slug["rumor"]["last_history_at"]), "2026-09-01")
            self.assertIn("fresh signal", by_slug["rumor"]["closure_review"])
            self.assertNotIn("released_at", by_slug["shipped"])
            self.assertNotIn("Long narrative", inputs.json_text(rows))
            self.assertTrue(all(Path(row["path"]).is_file() for row in rows))

    def test_pages_never_truncate_large_evidence_or_cap_records(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            rows = [{"text": "완전한 증거 " * 6000}, *[{"index": n} for n in range(1500)]]
            pages = inputs.write_pages(root, "signal", rows)
            recovered = [json.loads(line) for page in pages
                         for line in Path(page["path"]).read_text().splitlines()]
            self.assertEqual(recovered, rows)
            self.assertGreater(pages[0]["bytes"], inputs.PAGE_BYTES)
            self.assertEqual(pages[0]["records"], 1)
            self.assertTrue(all(page["bytes"] <= inputs.PAGE_BYTES for page in pages[1:]))


if __name__ == "__main__":
    unittest.main()
