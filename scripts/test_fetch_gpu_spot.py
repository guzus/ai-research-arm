#!/usr/bin/env python3
"""Offline tests for scripts/fetch_gpu_spot.py.

FULLY OFFLINE by construction: every test drives `run()`/`collect_model()`
through an injected `fetch` callable backed by fixture payloads. Nothing here
opens a socket, so the suite is deterministic in CI and cannot be broken by
the live marketplace moving.

Written as unittest.TestCase because the repo's CI gate is
`uv run python -m unittest discover -s scripts -p 'test_*.py'` (ci.yml), not
pytest. TestCase classes are collected by both runners.
"""

from __future__ import annotations

import json
import unittest
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import fetch_gpu_spot as gs

NOW = datetime(2026, 8, 2, 5, 12, 0, tzinfo=timezone.utc)
LATER = datetime(2026, 8, 2, 11, 12, 0, tzinfo=timezone.utc)


def offer(
    offer_id: int,
    gpu_name: str = "H100 SXM",
    num_gpus: int = 1,
    dph_total: float = 2.0,
    **extra: Any,
) -> dict[str, Any]:
    base = {"id": offer_id, "gpu_name": gpu_name, "num_gpus": num_gpus, "dph_total": dph_total}
    base.update(extra)
    return base


class FakeAPI:
    """Fixture-backed stand-in for the marketplace endpoint.

    `books` maps (gpu_name, key) -> list of raw offer dicts, so a test can
    express "unpartitioned returns a capped page, bucket queries return the
    real book" exactly as the live API behaves. `key` is None for the
    unpartitioned page, an int for an exact num_gpus bucket, and the tuple
    ("gte", N) for the tail sweep.

    Keying the tail sweep separately is load-bearing: `{"gte": 17}` has no
    "eq" member, so a `.get("eq")` lookup would silently return None and
    re-serve the UNPARTITIONED page as if it were the tail — making a test
    pass on data the real endpoint would never return.
    """

    def __init__(self, books: dict[tuple[str, Any], list[dict[str, Any]]],
                 fail_for: set[str] | None = None) -> None:
        self.books = books
        self.fail_for = fail_for or set()
        self.calls: list[dict[str, Any]] = []

    @staticmethod
    def key_for(query: dict[str, Any]) -> Any:
        spec = query.get("num_gpus")
        if not spec:
            return None
        if "eq" in spec:
            return spec["eq"]
        for op in ("gte", "gt"):
            if op in spec:
                return (op, spec[op])
        raise AssertionError(f"unsupported num_gpus spec in query: {spec!r}")

    def __call__(self, query: dict[str, Any]) -> list[Any]:
        self.calls.append(query)
        name = query["gpu_name"]["eq"]
        if name in self.fail_for:
            raise OSError(f"simulated network failure for {name}")
        return list(self.books.get((name, self.key_for(query)), []))


# ---------------------------------------------------------------------------
# per-GPU normalisation — the single most important correctness detail
# ---------------------------------------------------------------------------

class TestPerGpuNormalisation(unittest.TestCase):
    def test_divides_whole_machine_price_by_num_gpus(self):
        """dph_total is the whole machine; an 8x box at 19.2016 is $2.40/GPU."""
        self.assertAlmostEqual(
            gs.per_gpu_price(offer(1, num_gpus=8, dph_total=19.20156681481481)),
            2.4001958518518512,
            places=9,
        )

    def test_single_gpu_price_is_unchanged(self):
        self.assertAlmostEqual(gs.per_gpu_price(offer(1, num_gpus=1, dph_total=1.4911)), 1.4911)

    def test_aggregate_uses_per_gpu_not_whole_machine(self):
        """Regression guard for an off-by-num_gpus error.

        Three 8x machines at $16/hr are $2.00/GPU/hr. If the division were
        dropped, every statistic would read 16.0 and silently multiply every
        downstream article's price by 8.
        """
        api = FakeAPI({("H100 SXM", None): [
            offer(1, num_gpus=8, dph_total=16.0),
            offer(2, num_gpus=8, dph_total=16.0),
            offer(3, num_gpus=8, dph_total=16.0),
        ]})
        stats = gs.collect_model("H100 SXM", api, cap=64)
        self.assertEqual(stats["samples"], 3)
        self.assertAlmostEqual(stats["min"], 2.0)
        self.assertAlmostEqual(stats["median"], 2.0)
        self.assertAlmostEqual(stats["max"], 2.0)

    def test_mixed_gpu_counts_rank_by_per_gpu_price(self):
        """A cheap-per-GPU 8x box must beat an expensive 1x box.

        This is the case the API's own dph_total ordering gets wrong (19.2
        sorts after 3.0), which is why prices are sorted locally after
        normalisation rather than trusting response order.
        """
        api = FakeAPI({("H100 SXM", None): [
            offer(1, num_gpus=1, dph_total=3.0),      # $3.00/GPU
            offer(2, num_gpus=8, dph_total=19.2),     # $2.40/GPU
        ]})
        stats = gs.collect_model("H100 SXM", api, cap=64)
        self.assertAlmostEqual(stats["min"], 2.4)
        self.assertAlmostEqual(stats["max"], 3.0)
        self.assertEqual(stats["by_num_gpus"], {"1": 1, "8": 1})


# ---------------------------------------------------------------------------
# filtering
# ---------------------------------------------------------------------------

class TestFiltering(unittest.TestCase):
    def _drops(self, offers: list[Any], name: str = "H100 SXM"):
        drops: dict[str, int] = {}
        kept = gs.clean_offers(offers, name, set(), drops)
        return kept, drops

    def test_drops_interruptible_bid_offers(self):
        """`sample_basis` promises ask-only; that must be enforced, not just
        asserted. A bid offer's much lower price would drag `min` toward the
        bid floor while the artifact still claimed it excluded them."""
        kept, drops = self._drops([
            offer(1, dph_total=2.0),                       # on-demand ask
            offer(2, dph_total=2.0, is_bid=False),         # explicit ask
            offer(3, dph_total=0.4, is_bid=True),          # interruptible bid
        ])
        self.assertEqual(len(kept), 2)
        self.assertEqual(drops["is_bid"], 1)
        self.assertNotIn(0.4, [price for price, _count in kept])

    def test_drops_nonpositive_and_missing_fields(self):
        kept, drops = self._drops([
            offer(1, dph_total=2.0),                       # good
            offer(2, dph_total=0.0),                       # zero price
            offer(3, dph_total=-1.0),                      # negative price
            offer(4, num_gpus=0, dph_total=2.0),           # zero gpus
            offer(5, num_gpus=-2, dph_total=2.0),          # negative gpus
            {"id": 6, "gpu_name": "H100 SXM", "num_gpus": 1},            # no price
            {"id": 7, "gpu_name": "H100 SXM", "dph_total": 2.0},         # no num_gpus
            {"id": 8, "gpu_name": "H100 SXM", "num_gpus": 1, "dph_total": "2.0"},  # string
            "not-a-dict",
        ])
        self.assertEqual(len(kept), 1)
        self.assertEqual(drops["nonpositive_price"], 2)
        self.assertEqual(drops["nonpositive_num_gpus"], 2)
        self.assertEqual(drops["missing_price"], 2)  # absent + non-numeric string
        self.assertEqual(drops["missing_num_gpus"], 1)
        self.assertEqual(drops["malformed_offer"], 1)

    def test_drops_absurd_outliers_outside_absolute_band(self):
        kept, drops = self._drops([
            offer(1, dph_total=2.0),
            offer(2, dph_total=1e9),        # $1B/hr
            offer(3, dph_total=0.0000001),  # sub-mil
        ])
        self.assertEqual(len(kept), 1)
        self.assertEqual(drops["price_out_of_band"], 2)

    def test_keeps_genuine_price_spike(self):
        """A real spike is the most newsworthy thing this series can capture.

        The band is absolute, never relative, so a 10x move against the rest of
        the book survives rather than being filtered as an 'outlier'.
        """
        kept, drops = self._drops([
            offer(1, dph_total=2.0), offer(2, dph_total=2.1),
            offer(3, dph_total=2.2), offer(4, dph_total=25.0),
        ])
        self.assertEqual(len(kept), 4)
        self.assertNotIn("price_out_of_band", drops)

    def test_drops_wrong_model_and_duplicate_ids(self):
        seen: set[Any] = set()
        drops: dict[str, int] = {}
        first = gs.clean_offers([offer(1), offer(2)], "H100 SXM", seen, drops)
        second = gs.clean_offers(
            [offer(2), offer(3), offer(4, gpu_name="B200")], "H100 SXM", seen, drops
        )
        self.assertEqual(len(first), 2)
        self.assertEqual(len(second), 1)          # id 2 deduped, B200 rejected
        self.assertEqual(drops["duplicate_id"], 1)
        self.assertEqual(drops["gpu_name_mismatch"], 1)

    def test_rejects_fractional_num_gpus_instead_of_truncating(self):
        """int(2.7) == 2 would divide by the wrong count and understate price.

        A whole-machine price of $8.10 over a claimed 2.7 GPUs must be rejected
        outright, not silently booked as $4.05/GPU.
        """
        kept, drops = self._drops([offer(1, num_gpus=2.7, dph_total=8.1)])
        self.assertEqual(kept, [])
        self.assertEqual(drops["fractional_num_gpus"], 1)

    def test_integral_float_num_gpus_is_accepted(self):
        kept, _drops = self._drops([offer(1, num_gpus=2.0, dph_total=8.0)])
        self.assertEqual(len(kept), 1)
        self.assertAlmostEqual(kept[0][0], 4.0)

    def test_rejects_bool_as_numeric(self):
        _kept, drops = self._drops([{"id": 1, "gpu_name": "H100 SXM", "num_gpus": True,
                                     "dph_total": 2.0}])
        self.assertEqual(drops["missing_num_gpus"], 1)

    def test_dropped_counts_are_reported_in_output(self):
        api = FakeAPI({("H100 SXM", None): [offer(1, dph_total=2.0), offer(2, dph_total=0.0)]})
        payload, code = gs.run(["H100 SXM"], api, {}, NOW)
        self.assertEqual(code, 0)
        self.assertEqual(payload["snapshot"]["dropped"]["total"], 1)
        self.assertEqual(payload["snapshot"]["dropped"]["by_reason"]["nonpositive_price"], 1)


# ---------------------------------------------------------------------------
# statistics
# ---------------------------------------------------------------------------

class TestAggregation(unittest.TestCase):
    def test_percentiles_linear_interpolation(self):
        values = [1.0, 2.0, 3.0, 4.0]
        self.assertAlmostEqual(gs.percentile(values, 0.0), 1.0)
        self.assertAlmostEqual(gs.percentile(values, 0.25), 1.75)
        self.assertAlmostEqual(gs.percentile(values, 0.5), 2.5)
        self.assertAlmostEqual(gs.percentile(values, 1.0), 4.0)

    def test_single_sample_collapses_all_quantiles(self):
        stats = gs.aggregate_prices([2.5])
        self.assertEqual(
            (stats["samples"], stats["min"], stats["p25"], stats["median"], stats["max"]),
            (1, 2.5, 2.5, 2.5, 2.5),
        )

    def test_empty_aggregate_fails_fast(self):
        with self.assertRaises(ValueError):
            gs.aggregate_prices([])


# ---------------------------------------------------------------------------
# adaptive partitioning + truncation
# ---------------------------------------------------------------------------

class TestPartitioning(unittest.TestCase):
    def test_no_partition_when_under_cap(self):
        api = FakeAPI({("H100 SXM", None): [offer(i, dph_total=2.0) for i in range(10)]})
        stats = gs.collect_model("H100 SXM", api, cap=64)
        self.assertEqual(len(api.calls), 1)
        self.assertFalse(stats["partitioned"])
        self.assertFalse(stats["truncated"])

    def test_partitions_and_unions_when_capped(self):
        """A capped unpartitioned page is re-queried per bucket and unioned.

        Offer ids overlap between the two passes, so the union must dedupe —
        otherwise popular models would double-count their cheapest offers.
        """
        capped = [offer(i, num_gpus=1, dph_total=1.0) for i in range(4)]
        api = FakeAPI({
            ("H100 SXM", None): capped,
            ("H100 SXM", 1): capped + [offer(100, num_gpus=1, dph_total=1.5)],
            ("H100 SXM", 2): [offer(200, num_gpus=2, dph_total=4.0)],
        })
        stats = gs.collect_model("H100 SXM", api, cap=4, buckets=(1, 2))
        self.assertTrue(stats["partitioned"])
        self.assertEqual(stats["samples"], 6)  # 4 + 1 new 1x + 1 2x, ids deduped
        self.assertEqual(stats["by_num_gpus"], {"1": 5, "2": 1})

    def test_truncated_flag_set_when_a_bucket_still_caps(self):
        capped = [offer(i, num_gpus=1, dph_total=1.0) for i in range(4)]
        api = FakeAPI({("H100 SXM", None): capped, ("H100 SXM", 1): capped})
        stats = gs.collect_model("H100 SXM", api, cap=4, buckets=(1,))
        self.assertTrue(stats["truncated"])

    def test_not_truncated_when_partitioning_resolves_under_cap(self):
        """`truncated: false` requires EXHAUSTIVE coverage, not just no cap.

        buckets=(1,) with tail_min=2 covers num_gpus 1 exactly plus everything
        >= 2, so the union provably sees the whole book.
        """
        api = FakeAPI({
            ("H100 SXM", None): [offer(i, num_gpus=1, dph_total=1.0) for i in range(4)],
            ("H100 SXM", 1): [offer(i, num_gpus=1, dph_total=1.0) for i in range(3)],
            ("H100 SXM", ("gte", 2)): [],
        })
        stats = gs.collect_model("H100 SXM", api, cap=4, buckets=(1,), tail_min=2)
        self.assertFalse(stats["truncated"])

    def test_truncated_when_bucket_coverage_is_not_exhaustive(self):
        """A gap in the bucket specs is itself incompleteness.

        buckets=(1,) with tail_min=3 never asks about num_gpus 2, so no answer
        about the book can be complete — regardless of whether any single
        query capped. Publishing `truncated: false` here would assert a
        complete book over a sample with a hole in it.
        """
        api = FakeAPI({
            ("H100 SXM", None): [offer(i, num_gpus=1, dph_total=1.0) for i in range(4)],
            ("H100 SXM", 1): [offer(i, num_gpus=1, dph_total=1.0) for i in range(3)],
            ("H100 SXM", ("gte", 3)): [],
        })
        stats = gs.collect_model("H100 SXM", api, cap=4, buckets=(1,), tail_min=3)
        self.assertTrue(stats["truncated"])

    def test_out_of_bucket_tier_beyond_the_cap_is_still_collected(self):
        """REGRESSION: the out-of-bucket tier must survive when it is beyond
        the cap, which is the only case where truncation matters.

        The previous version of this test put the 5-GPU offer INSIDE the
        capped page, so it survived by construction and the assertion passed
        even while whole tiers were being lost. Here the 5-GPU offer sorts
        BEYOND the cap in ascending dph_total and never appears on the
        unpartitioned page — exactly the live shape, since
        dph_total ~= num_gpus x per-GPU price makes ascending truncation drop
        high-num_gpus offers first. The 5-GPU tier is also the CHEAPEST per
        GPU ($10.0 / 5 = $2.00, vs $3.00 for 1x and $4.00 for 2x), so losing
        it corrupts `min` — the field stamped into every history record.
        """
        ones = [offer(i, num_gpus=1, dph_total=3.0) for i in range(2)]
        twos = [offer(50, num_gpus=2, dph_total=8.0)]
        fives = [offer(99, num_gpus=5, dph_total=10.0)]
        api = FakeAPI({
            # Capped at 3 in ascending dph_total: 3.0, 3.0, 8.0. The 10.0
            # five-GPU row is the truncated tail.
            ("H100 SXM", None): ones + twos,
            ("H100 SXM", 1): ones,
            ("H100 SXM", 2): twos,
            ("H100 SXM", ("gte", 3)): fives,
        })
        stats = gs.collect_model("H100 SXM", api, cap=3, buckets=(1, 2), tail_min=3)
        self.assertIn("5", stats["by_num_gpus"])
        self.assertAlmostEqual(stats["min"], 2.0)
        # Coverage is exhaustive and no individual query capped, so the
        # completeness claim is honest here.
        self.assertFalse(stats["truncated"])

    def test_production_bucket_list_is_exhaustive(self):
        """The shipped specs must leave no num_gpus unasked.

        This is the invariant the sparse hand-picked list violated: every
        integer below the tail must have its own bucket, or the union has a
        hole that `truncated: false` would deny.
        """
        self.assertEqual(
            set(gs.NUM_GPU_BUCKETS), set(range(1, gs.NUM_GPU_TAIL_MIN))
        )

    def test_tail_sweep_is_issued_as_a_range_query(self):
        """The catch-all must be a range operator, not another `eq`."""
        capped = [offer(i, num_gpus=1, dph_total=1.0) for i in range(3)]
        api = FakeAPI({("H100 SXM", None): capped, ("H100 SXM", 1): capped})
        gs.collect_model("H100 SXM", api, cap=3, buckets=(1,), tail_min=2)
        specs = [q.get("num_gpus") for q in api.calls]
        self.assertIn({"gte": 2}, specs)

    def test_truncated_flag_reaches_every_history_record(self):
        """A methodology-visible flag must live in history, not only the snapshot.

        Without it, a model that truncates one day and not the next shows a
        median move that is an artifact, indistinguishable from a market move.
        """
        capped = [offer(i, num_gpus=1, dph_total=1.0) for i in range(4)]
        api = FakeAPI({("H100 SXM", None): capped, ("H100 SXM", 1): capped})
        payload, _ = gs.run(["H100 SXM"], api, {}, NOW, cap=4)
        record = payload["history"][-1]
        idx = payload["history_fields"].index("truncated")
        self.assertTrue(record["models"]["H100 SXM"][idx])
        self.assertEqual(record["method_version"], gs.METHOD_VERSION)


# ---------------------------------------------------------------------------
# history accumulation
# ---------------------------------------------------------------------------

class TestHistory(unittest.TestCase):
    def test_history_appends_across_two_runs(self):
        api1 = FakeAPI({("H100 SXM", None): [offer(1, dph_total=2.0)]})
        first, _ = gs.run(["H100 SXM"], api1, {}, NOW)
        self.assertEqual(len(first["history"]), 1)

        api2 = FakeAPI({("H100 SXM", None): [offer(1, dph_total=3.0)]})
        second, _ = gs.run(["H100 SXM"], api2, first, LATER)
        self.assertEqual(len(second["history"]), 2)
        self.assertEqual([r["t"] for r in second["history"]], [gs._iso(NOW), gs._iso(LATER)])

        idx = second["history_fields"].index("min")
        self.assertAlmostEqual(second["history"][0]["models"]["H100 SXM"][idx], 2.0)
        self.assertAlmostEqual(second["history"][1]["models"]["H100 SXM"][idx], 3.0)

    def test_history_record_matches_declared_field_order(self):
        api = FakeAPI({("H100 SXM", None): [offer(1, num_gpus=1, dph_total=2.0),
                                            offer(2, num_gpus=1, dph_total=4.0)]})
        payload, _ = gs.run(["H100 SXM"], api, {}, NOW)
        row = dict(zip(payload["history_fields"], payload["history"][-1]["models"]["H100 SXM"]))
        snap = payload["snapshot"]["models"]["H100 SXM"]
        for field in ("samples", "min", "p25", "median", "mean", "max", "truncated"):
            self.assertEqual(row[field], snap[field], field)

    def test_retention_keeps_most_recent_records(self):
        seeded = {"history": [{"t": f"2026-07-{d:02d}T00:00:00Z", "method_version": 1,
                               "models": {}} for d in range(1, 6)]}
        api = FakeAPI({("H100 SXM", None): [offer(1, dph_total=2.0)]})
        payload, _ = gs.run(["H100 SXM"], api, seeded, NOW, history_max=3)
        self.assertEqual(len(payload["history"]), 3)
        self.assertEqual(payload["history"][-1]["t"], gs._iso(NOW))
        self.assertEqual(payload["history"][0]["t"], "2026-07-04T00:00:00Z")

    def test_corrupt_previous_history_does_not_wedge_the_lane(self):
        api = FakeAPI({("H100 SXM", None): [offer(1, dph_total=2.0)]})
        payload, code = gs.run(["H100 SXM"], api, {"history": "not-a-list"}, NOW)
        self.assertEqual(code, 0)
        self.assertEqual(len(payload["history"]), 1)


# ---------------------------------------------------------------------------
# fail-soft / fail-loud
# ---------------------------------------------------------------------------

class TestFailureModes(unittest.TestCase):
    def _previous(self) -> dict[str, Any]:
        api = FakeAPI({("H100 SXM", None): [offer(1, dph_total=2.0)],
                       ("B200", None): [offer(2, gpu_name="B200", dph_total=5.0)]})
        payload, _ = gs.run(["H100 SXM", "B200"], api, {}, NOW)
        return payload

    def test_stale_carry_forward_for_a_failing_model(self):
        previous = self._previous()
        api = FakeAPI({("B200", None): [offer(9, gpu_name="B200", dph_total=6.0)]},
                      fail_for={"H100 SXM"})
        payload, code = gs.run(["H100 SXM", "B200"], api, previous, LATER)

        self.assertEqual(code, 0)  # one fresh model is enough
        h100 = payload["snapshot"]["models"]["H100 SXM"]
        self.assertTrue(h100["stale"])
        self.assertAlmostEqual(h100["min"], 2.0)          # previous value preserved
        self.assertEqual(h100["as_of"], gs._iso(NOW))     # honest original timestamp
        self.assertFalse(payload["snapshot"]["models"]["B200"]["stale"])

    def test_stale_value_is_never_appended_to_history(self):
        """Carrying a stale price into the series would fabricate an observation."""
        previous = self._previous()
        api = FakeAPI({("B200", None): [offer(9, gpu_name="B200", dph_total=6.0)]},
                      fail_for={"H100 SXM"})
        payload, _ = gs.run(["H100 SXM", "B200"], api, previous, LATER)
        latest = payload["history"][-1]["models"]
        self.assertIn("B200", latest)
        self.assertNotIn("H100 SXM", latest)

    def test_total_failure_exits_nonzero_and_preserves_history(self):
        previous = self._previous()
        api = FakeAPI({}, fail_for={"H100 SXM", "B200"})
        payload, code = gs.run(["H100 SXM", "B200"], api, previous, LATER)

        self.assertEqual(code, 1)
        self.assertTrue(payload["stale"])
        self.assertEqual(len(payload["history"]), len(previous["history"]))  # no new record
        self.assertTrue(all(m["stale"] for m in payload["snapshot"]["models"].values()))
        self.assertAlmostEqual(payload["snapshot"]["models"]["H100 SXM"]["min"], 2.0)

    def test_empty_book_is_zero_supply_not_a_stale_price(self):
        """HTTP 200 with no offers is a real observation, and must be visible.

        A curated gpu_name list fails silently when upstream renames a model;
        surfacing the zero is the only way that becomes noticeable.
        """
        previous = self._previous()
        api = FakeAPI({("H100 SXM", None): [], ("B200", None): [offer(9, gpu_name="B200", dph_total=6.0)]})
        payload, code = gs.run(["H100 SXM", "B200"], api, previous, LATER)

        self.assertEqual(code, 0)  # B200 is fresh, so the run is not a total failure
        self.assertIn("H100 SXM", payload["snapshot"]["zero_offer_models"])
        self.assertNotIn("H100 SXM", payload["snapshot"]["models"])
        self.assertNotIn("H100 SXM", payload["history"][-1]["models"])

    def test_all_offers_rejected_is_a_failure_not_zero_supply(self):
        """An upstream schema change must not publish as "no supply".

        `zero_offer_models` is documented as the detector for a renamed
        model, so a model whose offers all fail the cleaning filters must NOT
        land in the same bucket — that would assert a live rental market has
        no machines, on a green run, with the only trace buried in
        dropped.by_reason. Here num_gpus arrives as the STRING "1", a
        plausible serialization change.
        """
        previous = self._previous()
        api = FakeAPI({
            ("H100 SXM", None): [offer(i, num_gpus="1", dph_total=1.0) for i in range(5)],
            ("B200", None): [offer(9, gpu_name="B200", dph_total=6.0)],
        })
        payload, code = gs.run(["H100 SXM", "B200"], api, previous, LATER)

        self.assertEqual(code, 0)  # B200 is fresh, so not a total failure
        self.assertNotIn("H100 SXM", payload["snapshot"]["zero_offer_models"])
        self.assertEqual(payload["snapshot"]["requests"]["failed"], 1)
        # Fail-soft: the prior value is carried forward, marked stale, rather
        # than the row silently disappearing.
        self.assertTrue(payload["snapshot"]["models"]["H100 SXM"]["stale"])
        # A stale carry must never be appended to the append-only series.
        self.assertNotIn("H100 SXM", payload["history"][-1]["models"])

    def test_genuinely_empty_book_is_still_zero_supply(self):
        """Control for the test above: 0 offers in means zero supply out."""
        api = FakeAPI({("H100 SXM", None): [],
                       ("B200", None): [offer(9, gpu_name="B200", dph_total=6.0)]})
        payload, code = gs.run(["H100 SXM", "B200"], api, {}, NOW)
        self.assertEqual(code, 0)
        self.assertIn("H100 SXM", payload["snapshot"]["zero_offer_models"])
        self.assertEqual(payload["snapshot"]["requests"]["failed"], 0)

    def test_no_previous_data_means_failing_model_is_simply_absent(self):
        api = FakeAPI({("B200", None): [offer(1, gpu_name="B200", dph_total=5.0)]},
                      fail_for={"H100 SXM"})
        payload, code = gs.run(["H100 SXM", "B200"], api, {}, NOW)
        self.assertEqual(code, 0)
        self.assertNotIn("H100 SXM", payload["snapshot"]["models"])
        self.assertEqual(payload["snapshot"]["requests"]["failed"], 1)


# ---------------------------------------------------------------------------
# atomic write (load-bearing rule 8)
# ---------------------------------------------------------------------------

class TestAtomicWrite(unittest.TestCase):
    def test_writes_and_reads_back(self):
        with TemporaryDirectory() as tmp:
            out = Path(tmp) / "gpu-spot.json"
            gs.write_atomic(out, {"generated_at": "2026-08-02T05:12:00Z"})
            self.assertEqual(json.loads(out.read_text())["generated_at"], "2026-08-02T05:12:00Z")

    def test_unserializable_payload_never_opens_a_temp_file(self):
        """Serialization runs before the temp file is created.

        The live artifact is untouched and no .tmp is left behind, because the
        failure happens before any file is opened.
        """
        with TemporaryDirectory() as tmp:
            out = Path(tmp) / "gpu-spot.json"
            gs.write_atomic(out, {"ok": True})
            original = out.read_text()

            with self.assertRaises(TypeError):
                gs.write_atomic(out, {"bad": {1, 2, 3}})  # sets are not JSON

            self.assertEqual(out.read_text(), original)
            self.assertEqual(list(Path(tmp).iterdir()), [out])  # no stray .tmp

    def test_failure_mid_write_leaves_previous_file_intact(self):
        """The real mid-write branch: os.replace fails AFTER the temp exists.

        This is the case the atomic-write rule exists for. The dashboard
        prebuild copies this file straight into the deployed image (verified:
        research/market/ is in prebuild's COPY_DIRS), so a truncated or
        half-swapped JSON would ship broken data to production. The previous
        artifact must survive byte-for-byte and the temp must be cleaned up.
        """
        with TemporaryDirectory() as tmp:
            out = Path(tmp) / "gpu-spot.json"
            gs.write_atomic(out, {"ok": True, "history": [{"t": "a"}]})
            original = out.read_bytes()

            real_replace = gs.os.replace
            saw_temp: list[bool] = []

            def exploding_replace(src, dst):  # noqa: ANN001
                # The temp file must already exist and hold the NEW content at
                # this point — that is what makes the swap atomic.
                saw_temp.append(Path(src).exists())
                raise OSError("simulated failure during rename")

            gs.os.replace = exploding_replace
            try:
                with self.assertRaises(OSError):
                    gs.write_atomic(out, {"ok": False, "history": [{"t": "b"}]})
            finally:
                gs.os.replace = real_replace

            self.assertEqual(saw_temp, [True])                  # temp was fully written
            self.assertEqual(out.read_bytes(), original)        # original untouched
            self.assertEqual(list(Path(tmp).iterdir()), [out])  # temp cleaned up

    def test_keyboard_interrupt_mid_write_also_cleans_up(self):
        """Cleanup catches BaseException, not just Exception — a Ctrl-C or a
        job timeout between write and rename must not strand a .tmp."""
        with TemporaryDirectory() as tmp:
            out = Path(tmp) / "gpu-spot.json"
            real_replace = gs.os.replace

            def interrupting_replace(src, dst):  # noqa: ANN001
                raise KeyboardInterrupt

            gs.os.replace = interrupting_replace
            try:
                with self.assertRaises(KeyboardInterrupt):
                    gs.write_atomic(out, {"ok": True})
            finally:
                gs.os.replace = real_replace

            self.assertEqual(list(Path(tmp).iterdir()), [])  # nothing stranded

    def test_temp_file_is_in_the_same_directory(self):
        """os.replace is only atomic within a filesystem — a /tmp staging file
        would degrade to a non-atomic cross-device copy."""
        with TemporaryDirectory() as tmp:
            out = Path(tmp) / "sub" / "gpu-spot.json"
            captured: list[Path] = []
            real_write_text = Path.write_text

            def spy(self, *args, **kwargs):  # noqa: ANN001
                captured.append(Path(self))
                return real_write_text(self, *args, **kwargs)

            Path.write_text = spy  # type: ignore[method-assign]
            try:
                gs.write_atomic(out, {"ok": True})
            finally:
                Path.write_text = real_write_text  # type: ignore[method-assign]

            self.assertTrue(captured)
            self.assertEqual(captured[0].parent, out.parent)

    def test_run_output_is_json_serializable(self):
        api = FakeAPI({("H100 SXM", None): [offer(1, dph_total=2.0)]})
        payload, _ = gs.run(["H100 SXM"], api, {}, NOW)
        json.dumps(payload)  # would raise on a set/tuple-keyed leak


# ---------------------------------------------------------------------------
# serialization: compact history records inside an indented document
# ---------------------------------------------------------------------------

class TestSerialization(unittest.TestCase):
    def _payload(self, runs: int = 3) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        for i in range(runs):
            api = FakeAPI({("H100 SXM", None): [offer(1, dph_total=2.0 + i)],
                           ("B200", None): [offer(2, gpu_name="B200", dph_total=5.0 + i)]})
            stamp = datetime(2026, 8, 2, 5 + i, 0, 0, tzinfo=timezone.utc)
            payload, _ = gs.run(["H100 SXM", "B200"], api, payload, stamp)
        return payload

    def test_round_trip_is_the_identity(self):
        """The whole compact-record trick is only safe if this holds."""
        payload = self._payload()
        self.assertEqual(json.loads(gs.serialize(payload)), payload)

    def test_each_history_record_is_one_line(self):
        payload = self._payload(runs=3)
        # A compact history record is the only line carrying all three keys;
        # the top-level "method_version" sits on its own indented line.
        lines = [
            ln for ln in gs.serialize(payload).splitlines()
            if '"t":' in ln and '"method_version":' in ln and '"models":' in ln
        ]
        self.assertEqual(len(lines), 3)
        for line in lines:
            self.assertIn('"H100 SXM":', line)  # entire record inline, not split

    def test_document_outside_history_stays_indented(self):
        text = gs.serialize(self._payload(runs=1))
        self.assertIn('\n  "snapshot": {\n', text)
        self.assertIn('\n      "H100 SXM": {\n', text)

    def test_round_trip_survives_quotes_in_model_names(self):
        """The marker is unwrapped via json.loads, so escapes must round-trip."""
        payload = {"history": [{"t": "x", "models": {'weird "quoted" \\ name': [1, 2.0, False]}}]}
        self.assertEqual(json.loads(gs.serialize(payload)), payload)

    def test_serialize_is_what_write_atomic_writes(self):
        payload = self._payload(runs=2)
        with TemporaryDirectory() as tmp:
            out = Path(tmp) / "gpu-spot.json"
            gs.write_atomic(out, payload)
            self.assertEqual(out.read_text(encoding="utf-8"), gs.serialize(payload))
            self.assertEqual(json.loads(out.read_text(encoding="utf-8")), payload)

    def test_empty_history_serializes_cleanly(self):
        payload = {"history": [], "generated_at": "2026-08-02T05:12:00Z"}
        self.assertEqual(json.loads(gs.serialize(payload)), payload)


# ---------------------------------------------------------------------------
# contract shape
# ---------------------------------------------------------------------------

class TestContract(unittest.TestCase):
    def test_top_level_shape_and_timestamps(self):
        api = FakeAPI({("H100 SXM", None): [offer(1, dph_total=2.0)]})
        payload, _ = gs.run(["H100 SXM"], api, {}, NOW)
        for key in ("generated_at", "method_version", "source", "metric", "price_basis",
                    "sample_basis", "stale", "history_fields", "snapshot", "history"):
            self.assertIn(key, payload)
        self.assertEqual(payload["generated_at"], "2026-08-02T05:12:00Z")
        self.assertEqual(payload["metric"], "usd_per_gpu_hour")
        self.assertEqual(payload["price_basis"], "dph_total / num_gpus")
        # The series must say it is on-demand asks, not the interruptible bid
        # tier, or an article can cite it as "spot" and mean the wrong market.
        self.assertIn("on-demand", payload["sample_basis"])
        self.assertIn("bid", payload["sample_basis"])
        self.assertEqual(payload["history_fields"], list(gs.HISTORY_FIELDS))

    def test_query_orders_ascending_and_filters_rentable(self):
        """Ascending order is load-bearing: it is what keeps `min` exact under
        truncation. Losing it would silently bias the headline number."""
        query = gs.build_query("H100 SXM", 8, 64)
        self.assertEqual(query["order"], [["dph_total", "asc"]])
        self.assertEqual(query["rentable"], {"eq": True})
        self.assertEqual(query["gpu_name"], {"eq": "H100 SXM"})
        self.assertEqual(query["num_gpus"], {"eq": 8})

    def test_curated_model_list_has_no_duplicates(self):
        self.assertEqual(len(gs.GPU_MODELS), len(set(gs.GPU_MODELS)))

    def test_models_are_sorted_deterministically(self):
        api = FakeAPI({("B200", None): [offer(1, gpu_name="B200", dph_total=5.0)],
                       ("H100 SXM", None): [offer(2, dph_total=2.0)]})
        payload, _ = gs.run(["H100 SXM", "B200"], api, {}, NOW)
        self.assertEqual(list(payload["snapshot"]["models"]), ["B200", "H100 SXM"])


if __name__ == "__main__":
    unittest.main()
