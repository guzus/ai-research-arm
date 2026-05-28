#!/usr/bin/env python3

import os
import shutil
import subprocess
import tempfile
import unittest
from datetime import datetime, timezone

import check_lane_freshness as clf


class ClassifyTest(unittest.TestCase):
    def test_missing_dir_is_missing_regardless_of_age(self):
        self.assertEqual(clf.classify(None, 30, dir_exists=False), clf.MISSING)
        self.assertEqual(clf.classify(1.0, 30, dir_exists=False), clf.MISSING)

    def test_no_commits_is_unknown(self):
        # dir exists but git returned no commit (e.g. shallow clone)
        self.assertEqual(clf.classify(None, 30, dir_exists=True), clf.UNKNOWN)

    def test_within_threshold_is_fresh(self):
        self.assertEqual(clf.classify(3.9, 4, dir_exists=True), clf.FRESH)

    def test_over_threshold_is_stale(self):
        self.assertEqual(clf.classify(4.1, 4, dir_exists=True), clf.STALE)

    def test_exactly_at_threshold_is_fresh(self):
        # boundary: equal age is not yet stale
        self.assertEqual(clf.classify(30.0, 30, dir_exists=True), clf.FRESH)


class EvaluateTest(unittest.TestCase):
    def _evaluate_with(self, ages, present):
        thresholds = {"rss": 4, "twitter": 9, "wiki": 30, "gone": 30}

        def age_fn(lane, now_epoch, repo_root):
            return ages.get(lane)

        def dir_exists_fn(lane, repo_root):
            return lane in present

        return clf.evaluate(
            thresholds,
            now_epoch=0,
            repo_root="/nonexistent",
            age_fn=age_fn,
            dir_exists_fn=dir_exists_fn,
        )

    def test_mixed_states(self):
        statuses = self._evaluate_with(
            ages={"rss": 12.0, "twitter": 1.0, "wiki": 200.0},
            present={"rss", "twitter", "wiki"},  # "gone" absent
        )
        by_lane = {s.lane: s for s in statuses}
        self.assertEqual(by_lane["rss"].state, clf.STALE)      # 12h > 4h
        self.assertEqual(by_lane["twitter"].state, clf.FRESH)  # 1h <= 9h
        self.assertEqual(by_lane["wiki"].state, clf.STALE)     # 200h > 30h
        self.assertEqual(by_lane["gone"].state, clf.MISSING)   # dir absent

        alerting = sorted(s.lane for s in statuses if s.alerting)
        self.assertEqual(alerting, ["gone", "rss", "wiki"])

    def test_all_fresh(self):
        statuses = self._evaluate_with(
            ages={"rss": 0.5, "twitter": 0.5, "wiki": 0.5, "gone": 0.5},
            present={"rss", "twitter", "wiki", "gone"},
        )
        self.assertEqual([s for s in statuses if s.alerting], [])


class IdempotencyKeyTest(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 5, 28, 6, 0, tzinfo=timezone.utc)

    def test_order_independent(self):
        a = clf.idempotency_key(["twitter", "rss"], self.now)
        b = clf.idempotency_key(["rss", "twitter"], self.now)
        self.assertEqual(a, b)

    def test_includes_date_and_set(self):
        self.assertEqual(
            clf.idempotency_key(["rss", "twitter"], self.now),
            "lane-freshness-2026-05-28-rss-twitter",
        )

    def test_empty_set(self):
        self.assertEqual(
            clf.idempotency_key([], self.now),
            "lane-freshness-2026-05-28-none",
        )

    def test_different_set_different_key(self):
        a = clf.idempotency_key(["rss"], self.now)
        b = clf.idempotency_key(["rss", "twitter"], self.now)
        self.assertNotEqual(a, b)


@unittest.skipIf(shutil.which("git") is None, "git not available")
class GitIntegrationTest(unittest.TestCase):
    """Exercises the real `git log` path with deterministic backdated commits."""

    def setUp(self):
        self.repo = tempfile.mkdtemp(prefix="lane-fresh-")
        self._git("init", "-q")
        self._git("config", "user.email", "test@example.com")
        self._git("config", "user.name", "Test")

    def tearDown(self):
        shutil.rmtree(self.repo, ignore_errors=True)

    def _git(self, *args, env_extra=None):
        env = os.environ.copy()
        if env_extra:
            env.update(env_extra)
        subprocess.run(["git", *args], cwd=self.repo, check=True,
                       capture_output=True, text=True, env=env)

    def _commit_lane(self, lane, iso_date):
        d = os.path.join(self.repo, "research", lane)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "2026-01-01.md"), "a", encoding="utf-8") as fh:
            fh.write("x\n")
        self._git("add", "-A")
        # Pin both author and committer date so %ct is deterministic.
        self._git(
            "commit", "-q", "-m", f"{lane} {iso_date}",
            env_extra={"GIT_AUTHOR_DATE": iso_date, "GIT_COMMITTER_DATE": iso_date},
        )

    def test_age_reflects_last_commit_time(self):
        # rss last written 10 days ago; twitter 1 hour ago.
        self._commit_lane("rss", "2026-05-18T00:00:00Z")
        self._commit_lane("twitter", "2026-05-28T05:00:00Z")

        now_epoch = int(datetime(2026, 5, 28, 6, 0, tzinfo=timezone.utc).timestamp())
        rss_age = clf.lane_age_hours("rss", now_epoch, self.repo)
        tw_age = clf.lane_age_hours("twitter", now_epoch, self.repo)

        self.assertIsNotNone(rss_age)
        self.assertIsNotNone(tw_age)
        self.assertAlmostEqual(rss_age, 10 * 24 + 6, delta=0.5)  # 246h
        self.assertAlmostEqual(tw_age, 1.0, delta=0.5)

        # And end-to-end classification with the real thresholds.
        statuses = clf.evaluate(
            {"rss": clf.LANE_THRESHOLDS_HOURS["rss"],
             "twitter": clf.LANE_THRESHOLDS_HOURS["twitter"]},
            now_epoch, self.repo,
        )
        by_lane = {s.lane: s.state for s in statuses}
        self.assertEqual(by_lane["rss"], clf.STALE)
        self.assertEqual(by_lane["twitter"], clf.FRESH)

    def test_absent_lane_dir_is_missing(self):
        self._commit_lane("rss", "2026-05-28T05:00:00Z")
        now_epoch = int(datetime(2026, 5, 28, 6, 0, tzinfo=timezone.utc).timestamp())
        statuses = clf.evaluate({"bluesky": 30}, now_epoch, self.repo)
        self.assertEqual(statuses[0].state, clf.MISSING)


if __name__ == "__main__":
    unittest.main()
