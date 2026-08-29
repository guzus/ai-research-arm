#!/usr/bin/env python3

import unittest
from datetime import datetime, timezone

import check_stranded_publications as check


class StrandedPublicationTest(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 8, 29, 12, tzinfo=timezone.utc)

    def test_only_old_safe_push_prs_alert(self):
        rows = [
            {"number": 1, "headRefName": "automation/safe-push/main/rss", "createdAt": "2026-08-29T09:00:00Z", "url": "u1"},
            {"number": 2, "headRefName": "automation/safe-push/main/new", "createdAt": "2026-08-29T11:30:00Z", "url": "u2"},
            {"number": 3, "headRefName": "feature/not-publication", "createdAt": "2026-08-20T00:00:00Z", "url": "u3"},
        ]
        found = check.stranded(rows, self.now, 1.0)
        self.assertEqual([row["number"] for row in found], [1])

    def test_exact_threshold_is_stranded(self):
        rows = [{"number": 4, "headRefName": "automation/safe-push/main/x", "createdAt": "2026-08-29T11:00:00Z"}]
        self.assertEqual(check.stranded(rows, self.now, 1.0)[0]["age_hours"], 1.0)

    def test_naive_fixture_timestamp_is_interpreted_as_utc(self):
        rows = [{"number": 8, "headRefName": "automation/safe-push/main/x", "createdAt": "2026-08-29T10:00:00"}]
        self.assertEqual([row["number"] for row in check.stranded(rows, self.now, 1.0)], [8])


if __name__ == "__main__":
    unittest.main()
