#!/usr/bin/env python3

import os
import tempfile
import unittest
from datetime import datetime, timezone

import check_lane_content as clc


def _spec(min_bytes=400, drop_ratio=0.10, soft_floor_mult=3.0, glob="research/x/[0-9]*.md"):
    return clc.LaneSpec(
        glob=glob,
        min_bytes=min_bytes,
        drop_ratio=drop_ratio,
        soft_floor_mult=soft_floor_mult,
    )


def _series(sizes, prefix="2026-01-"):
    """Build an oldest->newest (name, size) list from a list of byte sizes."""
    return [(f"{prefix}{i + 1:02d}.md", s) for i, s in enumerate(sizes)]


class ClassifyTest(unittest.TestCase):
    def test_no_artifact_is_missing(self):
        status = clc.classify([], _spec(), history_min=4, trailing_n=8)
        self.assertEqual(status.state, clc.MISSING)
        self.assertTrue(status.anomalous)

    def test_empty_artifact_below_floor_is_flagged(self):
        # Plenty of healthy history, then a near-empty latest file.
        sizes = _series([10000, 11000, 9000, 12000, 10500, 9800, 11200, 50])
        status = clc.classify(sizes, _spec(min_bytes=400), history_min=4, trailing_n=8)
        self.assertEqual(status.state, clc.EMPTY)
        self.assertTrue(status.anomalous)
        self.assertEqual(status.size, 50)

    def test_empty_floor_fires_even_without_history(self):
        # A floor breach is independent of history — no prior samples needed.
        status = clc.classify(_series([20]), _spec(min_bytes=400), history_min=4, trailing_n=8)
        self.assertEqual(status.state, clc.EMPTY)
        self.assertTrue(status.anomalous)

    def test_healthy_artifact_not_flagged(self):
        sizes = _series([10000, 11000, 9000, 12000, 10500, 9800, 11200, 10300])
        status = clc.classify(sizes, _spec(min_bytes=400), history_min=4, trailing_n=8)
        self.assertEqual(status.state, clc.HEALTHY)
        self.assertFalse(status.anomalous)

    def test_sudden_drop_flagged(self):
        # ~10KB typical, latest collapses to 900B: ABOVE the 400B floor (so it
        # is not caught as EMPTY) but only ~9% of the median AND below the soft
        # floor (400 * 3 = 1200). This is the "lane still committed something,
        # but it's a near-dead husk" shape the relative arm exists to catch.
        sizes = _series([10000, 11000, 9000, 12000, 10500, 9800, 11200, 900])
        status = clc.classify(sizes, _spec(min_bytes=400), history_min=4, trailing_n=8)
        self.assertEqual(status.state, clc.DROP)
        self.assertTrue(status.anomalous)
        self.assertLess(status.size, status.median)

    def test_floor_takes_precedence_over_drop(self):
        # When a collapse is severe enough to breach the floor too, the
        # stronger EMPTY signal wins (floor is checked first).
        sizes = _series([10000, 11000, 9000, 12000, 10500, 9800, 11200, 100])
        status = clc.classify(sizes, _spec(min_bytes=400), history_min=4, trailing_n=8)
        self.assertEqual(status.state, clc.EMPTY)
        self.assertTrue(status.anomalous)

    def test_quiet_but_normal_day_not_flagged(self):
        # bluesky-shaped: median ~8KB, latest drops to ~1.3KB (a real quiet
        # day). That is 16% of median — above the 10% drop ratio — AND well
        # above the soft floor, so it must NOT page.
        sizes = _series([8686, 4814, 2928, 2776, 2616, 9000, 8000, 1276])
        status = clc.classify(sizes, _spec(min_bytes=80), history_min=4, trailing_n=8)
        self.assertEqual(status.state, clc.HEALTHY)
        self.assertFalse(status.anomalous)

    def test_big_lane_halving_not_flagged(self):
        # A large, bursty lane (twitter-shaped) halving from its median is
        # normal variance — clears the soft floor, so not flagged.
        sizes = _series([286736, 90434, 120884, 38290, 78832, 100000, 95000, 47000])
        status = clc.classify(sizes, _spec(min_bytes=600), history_min=4, trailing_n=8)
        self.assertEqual(status.state, clc.HEALTHY)
        self.assertFalse(status.anomalous)

    def test_drop_requires_below_soft_floor(self):
        # Latest is < 10% of a huge median but ABOVE the soft floor: the AND
        # condition is not met, so it is NOT a drop. (Guards against paging a
        # big lane that merely shrank a lot but still produced real content.)
        sizes = _series([100000, 100000, 100000, 100000, 100000, 100000, 100000, 2000])
        status = clc.classify(sizes, _spec(min_bytes=400, soft_floor_mult=3.0),
                              history_min=4, trailing_n=8)
        # 2000 < 0.10*100000 (=10000) but 2000 > soft floor (1200) -> healthy.
        self.assertEqual(status.state, clc.HEALTHY)
        self.assertFalse(status.anomalous)

    def test_insufficient_history_skips_drop(self):
        # Only 2 prior samples (< history_min) and latest small-but-above-floor:
        # we must not call it a drop on thin data.
        sizes = _series([10000, 12000, 500])
        status = clc.classify(sizes, _spec(min_bytes=400), history_min=4, trailing_n=8)
        self.assertEqual(status.state, clc.INSUFFICIENT)
        self.assertFalse(status.anomalous)

    def test_insufficient_history_still_flags_floor(self):
        # Thin history does not suppress the absolute floor.
        sizes = _series([10000, 12000, 50])
        status = clc.classify(sizes, _spec(min_bytes=400), history_min=4, trailing_n=8)
        self.assertEqual(status.state, clc.EMPTY)
        self.assertTrue(status.anomalous)

    def test_drop_ratio_zero_disables_drop_arm(self):
        # wiki-shaped: drop_ratio=0 means only the floor applies. A small but
        # above-floor latest is healthy even if it collapsed vs history.
        sizes = _series([10000, 11000, 9000, 12000, 10500, 9800, 11200, 400])
        status = clc.classify(sizes, _spec(min_bytes=300, drop_ratio=0.0),
                              history_min=4, trailing_n=8)
        self.assertEqual(status.state, clc.HEALTHY)
        self.assertFalse(status.anomalous)


class EvaluateTest(unittest.TestCase):
    def _evaluate_with(self, series_by_lane, specs=None):
        specs = specs or {
            "rss": _spec(min_bytes=400, glob="research/rss/[0-9]*.md"),
            "twitter": _spec(min_bytes=600, glob="research/twitter/[0-9]*.md"),
            "wiki": _spec(min_bytes=300, drop_ratio=0.0, glob="research/wiki/log.md"),
            "gone": _spec(min_bytes=400, glob="research/gone/[0-9]*.md"),
        }

        def sizes_fn(spec, repo_root):
            return series_by_lane.get(spec.glob, [])

        return clc.evaluate(
            specs,
            repo_root="/nonexistent",
            history_min=4,
            trailing_n=8,
            sizes_fn=sizes_fn,
        )

    def test_mixed_states(self):
        statuses = self._evaluate_with(
            {
                # healthy
                "research/rss/[0-9]*.md": _series(
                    [10000, 11000, 9000, 12000, 10500, 9800, 11200, 10300]
                ),
                # sudden drop: still above the 600B floor but a husk (~900B
                # vs ~100KB median) -> DROP, not EMPTY.
                "research/twitter/[0-9]*.md": _series(
                    [100000, 90000, 110000, 95000, 105000, 98000, 102000, 900]
                ),
                # wiki present and healthy
                "research/wiki/log.md": [("log.md", 5000)],
                # "gone" returns no files -> missing
            }
        )
        by_lane = {s.lane: s for s in statuses}
        self.assertEqual(by_lane["rss"].state, clc.HEALTHY)
        self.assertEqual(by_lane["twitter"].state, clc.DROP)
        self.assertEqual(by_lane["wiki"].state, clc.HEALTHY)
        self.assertEqual(by_lane["gone"].state, clc.MISSING)

        anomalous = sorted(s.lane for s in statuses if s.anomalous)
        self.assertEqual(anomalous, ["gone", "twitter"])

    def test_all_healthy(self):
        statuses = self._evaluate_with(
            {
                "research/rss/[0-9]*.md": _series([10000] * 8),
                "research/twitter/[0-9]*.md": _series([50000] * 8),
                "research/wiki/log.md": [("log.md", 5000)],
                "research/gone/[0-9]*.md": _series([10000] * 8),
            }
        )
        self.assertEqual([s for s in statuses if s.anomalous], [])

    def test_lane_label_is_attached(self):
        statuses = self._evaluate_with(
            {"research/rss/[0-9]*.md": _series([10000] * 8)}
        )
        # every status carries its configured lane key
        self.assertEqual({s.lane for s in statuses}, {"rss", "twitter", "wiki", "gone"})


class IdempotencyKeyTest(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 6, 10, 6, 0, tzinfo=timezone.utc)

    def test_order_independent(self):
        a = clc.idempotency_key(["twitter", "rss"], self.now)
        b = clc.idempotency_key(["rss", "twitter"], self.now)
        self.assertEqual(a, b)

    def test_includes_date_and_set(self):
        self.assertEqual(
            clc.idempotency_key(["rss", "twitter"], self.now),
            "lane-content-2026-06-10-rss-twitter",
        )

    def test_empty_set(self):
        self.assertEqual(
            clc.idempotency_key([], self.now),
            "lane-content-2026-06-10-none",
        )

    def test_prefix_distinct_from_freshness(self):
        # Content and freshness alerts must never collide on the dedup key.
        self.assertTrue(clc.idempotency_key(["rss"], self.now).startswith("lane-content-"))


class FilesystemIntegrationTest(unittest.TestCase):
    """Exercises the real glob/stat IO path against a temp tree."""

    def setUp(self):
        self.repo = tempfile.mkdtemp(prefix="lane-content-")

    def tearDown(self):
        import shutil

        shutil.rmtree(self.repo, ignore_errors=True)

    def _write(self, rel, content):
        path = os.path.join(self.repo, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)

    def test_picks_most_recent_and_measures_real_bytes(self):
        # Two dated files; lexical max is the "latest".
        self._write("research/rss/2026-06-08.md", "x" * 5000)
        self._write("research/rss/2026-06-09.md", "y" * 4800)
        spec = _spec(min_bytes=400, glob="research/rss/[0-9]*.md")
        sizes = clc.lane_artifact_sizes(spec, self.repo)
        self.assertEqual([n for n, _ in sizes], ["2026-06-08.md", "2026-06-09.md"])
        self.assertEqual(sizes[-1], ("2026-06-09.md", 4800))

    def test_empty_file_on_disk_flags_via_evaluate(self):
        # Healthy history then an empty newest file -> EMPTY end to end.
        for i in range(1, 9):
            self._write(f"research/rss/2026-06-{i:02d}.md", "x" * 5000)
        self._write("research/rss/2026-06-09.md", "")  # 0 bytes, newest
        specs = {"rss": _spec(min_bytes=400, glob="research/rss/[0-9]*.md")}
        statuses = clc.evaluate(specs, self.repo, history_min=4, trailing_n=8)
        self.assertEqual(statuses[0].state, clc.EMPTY)

    def test_no_dir_is_missing(self):
        specs = {"bluesky": _spec(min_bytes=80, glob="research/bluesky/[0-9]*.md")}
        statuses = clc.evaluate(specs, self.repo, history_min=4, trailing_n=8)
        self.assertEqual(statuses[0].state, clc.MISSING)


class RealRepoSmokeTest(unittest.TestCase):
    """Print-only diagnostic against the live history.

    Deliberately makes NO assertion on the live data. The content gate is
    ADVISORY by contract — a genuinely near-empty lane day (e.g. an upstream
    outage) is exactly when a real anomaly should surface, and this test runs
    inside `unittest discover` on the self-hosted CI runner where research/ IS
    present. Asserting `anomalous == []` here would turn the advisory gate into
    a hard CI gate that fails every open PR on such a day — the opposite of the
    design. Threshold validation lives in the offline dry-run
    (`python scripts/check_lane_content.py`), not in CI. We only print the live
    verdict so a human reading CI logs can eyeball it."""

    def test_live_lanes_diagnostic_only(self):
        import subprocess

        try:
            repo = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True, text=True, check=True,
            ).stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.skipTest("not in a git repo")

        if not os.path.isdir(os.path.join(repo, "research", "rss")):
            self.skipTest("research/ tree not present in this checkout")

        statuses = clc.evaluate(clc.LANE_SPECS, repo)
        anomalous = [f"{s.lane}:{s.state}" for s in statuses if s.anomalous]
        # Print, never assert. (No failure, no flakiness gating CI on data.)
        print(
            "\n[lane-content live diagnostic] "
            + ("all healthy" if not anomalous else "advisory anomalies: " + ", ".join(anomalous))
        )


if __name__ == "__main__":
    unittest.main()
