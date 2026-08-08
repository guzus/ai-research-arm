#!/usr/bin/env python3
"""Offline tests for scripts/fetch_model_pricing.py.

FULLY OFFLINE by construction: `run()` takes both sources as injected
callables, so nothing here opens a socket. The suite cannot be reddened by
OpenRouter repricing a model or Epoch publishing a new benchmark run.

unittest.TestCase because the repo's CI gate is
`uv run python -m unittest discover -s scripts -p 'test_*.py'` (ci.yml).
"""

from __future__ import annotations

import json
import unittest
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import fetch_model_pricing as mp

NOW = datetime(2026, 8, 7, 4, 0, 0, tzinfo=timezone.utc)
LATER = datetime(2026, 8, 7, 10, 0, 0, tzinfo=timezone.utc)


def or_model(name: str, out_per_mtok: float, in_per_mtok: float = 1.0, **extra: Any) -> dict[str, Any]:
    """An OpenRouter row. Prices are given per Mtok and converted to per-token."""
    row = {
        "id": extra.pop("id", "vendor/" + name.lower().replace(" ", "-")),
        "name": name,
        "context_length": extra.pop("context_length", 128000),
        "pricing": {"prompt": str(in_per_mtok / 1e6), "completion": str(out_per_mtok / 1e6)},
    }
    row.update(extra)
    return row


def epoch_row(model: str, score: float, task: str = "GPQA diamond", **extra: Any) -> dict[str, str]:
    row = {
        "task": task,
        "Model": model,
        "mean_score": str(score),
        "stderr": extra.pop("stderr", "0.01"),
        "id_model_version": extra.pop("variant", model.lower().replace(" ", "-")),
        "Version release date": extra.pop("released", "2026-01-01"),
        "Organization": extra.pop("org", "TestOrg"),
    }
    row.update({k: str(v) for k, v in extra.items()})
    return row


# ---------------------------------------------------------------- normalization

class NormalizationTests(unittest.TestCase):
    def test_drops_vendor_prefix_and_variant(self) -> None:
        self.assertEqual(mp.norm_key("Anthropic: Claude Opus 4.7 (Fast)"), "claudeopus4.7")
        self.assertEqual(mp.norm_key("Claude Opus 4.7"), "claudeopus4.7")

    def test_version_dots_are_preserved(self) -> None:
        """'4.5' must not collapse into '45' and collide with a hypothetical v45."""
        self.assertNotEqual(mp.norm_key("Claude Opus 4.5"), mp.norm_key("Claude Opus 45"))

    def test_distinct_products_do_not_collide(self) -> None:
        self.assertNotEqual(mp.norm_key("GPT-5.6 Luna"), mp.norm_key("GPT-5.6 Luna Pro"))

    def test_variant_extraction(self) -> None:
        self.assertEqual(mp.variant_of("Claude Opus 5 (batch)"), "batch")
        self.assertIsNone(mp.variant_of("Claude Opus 5"))


# ---------------------------------------------------------------- price index

class PriceIndexTests(unittest.TestCase):
    def test_converts_per_token_to_per_mtok(self) -> None:
        index = mp.build_price_index([or_model("Solo", out_per_mtok=25.0, in_per_mtok=5.0)])
        row = index["solo"]
        self.assertAlmostEqual(row["output_usd_per_mtok"], 25.0)
        self.assertAlmostEqual(row["input_usd_per_mtok"], 5.0)

    def test_base_tier_beats_cheaper_batch_and_dearer_fast(self) -> None:
        """THE load-bearing case: the frontier must price the standard tier.

        Picking `min(price)` naively would select the batch tier; picking the
        first row could select Fast at 6x. Either silently misplaces the point.
        """
        index = mp.build_price_index([
            or_model("Claude Opus 4.7 (Fast)", 150.0),
            or_model("Claude Opus 4.7", 25.0),
            or_model("Claude Opus 4.7 (batch)", 12.5),
        ])
        row = index["claudeopus4.7"]
        self.assertAlmostEqual(row["output_usd_per_mtok"], 25.0)
        self.assertIsNone(row["price_variant"])
        self.assertEqual(row["variants_seen"], 3)

    def test_falls_back_to_cheapest_variant_when_no_base_tier(self) -> None:
        index = mp.build_price_index([
            or_model("Ghost (Fast)", 90.0),
            or_model("Ghost (batch)", 30.0),
        ])
        row = index["ghost"]
        self.assertAlmostEqual(row["output_usd_per_mtok"], 30.0)
        self.assertEqual(row["price_variant"], "batch")

    def test_free_tier_is_excluded(self) -> None:
        """A $0 promo row would dominate every capability tier and void the chart."""
        index = mp.build_price_index([
            or_model("Freebie (free)", 0.0),
            or_model("Freebie", 4.0),
        ])
        self.assertAlmostEqual(index["freebie"]["output_usd_per_mtok"], 4.0)

    def test_model_priced_only_free_is_dropped_entirely(self) -> None:
        self.assertEqual(mp.build_price_index([or_model("OnlyFree", 0.0)]), {})

    def test_blended_price_uses_declared_ratio(self) -> None:
        index = mp.build_price_index([or_model("Blend", out_per_mtok=10.0, in_per_mtok=2.0)])
        # (2*3 + 10) / 4 == 4.0
        self.assertAlmostEqual(index["blend"]["blended_usd_per_mtok"], 4.0)


# ---------------------------------------------------------------- capability

class CapabilityIndexTests(unittest.TestCase):
    def test_keeps_best_score_across_effort_variants(self) -> None:
        index = mp.build_capability_index([
            epoch_row("Gemini 3.6 Flash", 0.71, variant="g36_low", stderr="0.05"),
            epoch_row("Gemini 3.6 Flash", 0.94, variant="g36_high", stderr="0.02"),
        ], "GPQA diamond")
        entry = index["gemini3.6flash"]
        self.assertAlmostEqual(entry["score"], 0.94)
        self.assertEqual(entry["score_variant"], "g36_high")
        self.assertAlmostEqual(entry["stderr"], 0.02, msg="stderr must follow the winning run")
        self.assertEqual(entry["runs"], 2)

    def test_other_benchmarks_are_ignored(self) -> None:
        index = mp.build_capability_index([
            epoch_row("A", 0.9, task="SWE-Bench verified"),
            epoch_row("A", 0.4, task="GPQA diamond"),
        ], "GPQA diamond")
        self.assertAlmostEqual(index["a"]["score"], 0.4)

    def test_unparseable_score_is_skipped(self) -> None:
        rows = [epoch_row("A", 0.5)]
        rows.append({**epoch_row("B", 0.0), "mean_score": ""})
        index = mp.build_capability_index(rows, "GPQA diamond")
        self.assertIn("a", index)
        self.assertNotIn("b", index)

    def test_benchmark_counts_are_distinct_models(self) -> None:
        counts = mp.benchmark_counts([
            epoch_row("A", 0.5), epoch_row("A", 0.6), epoch_row("B", 0.7),
            epoch_row("C", 0.8, task="MATH level 5"),
        ])
        self.assertEqual(counts["GPQA diamond"], 2)
        self.assertEqual(counts["MATH level 5"], 1)


# ---------------------------------------------------------------- pareto

def plot(score: float, price: float, name: str = "m") -> dict[str, Any]:
    return {"name": name, "score": score, "output_usd_per_mtok": price}


class ParetoTests(unittest.TestCase):
    def test_dominated_model_is_excluded(self) -> None:
        cheap_good = plot(0.9, 1.0, "cheap-good")
        dear_bad = plot(0.5, 10.0, "dear-bad")
        mp.mark_pareto([cheap_good, dear_bad])
        self.assertTrue(cheap_good["pareto"])
        self.assertFalse(dear_bad["pareto"])

    def test_tradeoff_models_both_survive(self) -> None:
        cheap_weak = plot(0.5, 1.0)
        dear_strong = plot(0.9, 10.0)
        mp.mark_pareto([cheap_weak, dear_strong])
        self.assertTrue(cheap_weak["pareto"])
        self.assertTrue(dear_strong["pareto"])

    def test_exact_ties_both_stay_on_the_frontier(self) -> None:
        """Identical (score, price) pairs must not dominate each other.

        Dropping one arbitrarily would hide a real choice between two models
        that are genuinely equivalent on both axes.
        """
        a, b = plot(0.8, 5.0, "a"), plot(0.8, 5.0, "b")
        count = mp.mark_pareto([a, b])
        self.assertTrue(a["pareto"] and b["pareto"])
        self.assertEqual(count, 2)

    def test_equal_score_cheaper_price_dominates(self) -> None:
        cheaper, dearer = plot(0.8, 2.0, "cheaper"), plot(0.8, 9.0, "dearer")
        mp.mark_pareto([cheaper, dearer])
        self.assertTrue(cheaper["pareto"])
        self.assertFalse(dearer["pareto"])

    def test_equal_price_better_score_dominates(self) -> None:
        better, worse = plot(0.9, 3.0, "better"), plot(0.4, 3.0, "worse")
        mp.mark_pareto([better, worse])
        self.assertTrue(better["pareto"])
        self.assertFalse(worse["pareto"])

    def test_single_model_is_trivially_on_the_frontier(self) -> None:
        only = plot(0.3, 99.0)
        self.assertEqual(mp.mark_pareto([only]), 1)


class FrontierPriceTests(unittest.TestCase):
    def test_reports_cheapest_price_meeting_each_tier(self) -> None:
        models = [plot(0.95, 50.0), plot(0.91, 0.2), plot(0.55, 0.05)]
        out = mp.frontier_price_at(models, (0.5, 0.9))
        self.assertAlmostEqual(out["0.5"], 0.05)
        self.assertAlmostEqual(out["0.9"], 0.2)

    def test_unreachable_tier_is_null_not_omitted(self) -> None:
        """`null` is the datable fact 'not purchasable at any price yet'."""
        out = mp.frontier_price_at([plot(0.4, 1.0)], (0.9,))
        self.assertIn("0.9", out)
        self.assertIsNone(out["0.9"])


# ---------------------------------------------------------------- join

class JoinTests(unittest.TestCase):
    def test_scored_and_priced_models_are_plotted(self) -> None:
        prices = mp.build_price_index([or_model("Claude Opus 5", 25.0)])
        caps = mp.build_capability_index([epoch_row("Claude Opus 5", 0.89)], "GPQA diamond")
        plotted, unscored = mp.join_models(prices, caps, {})
        self.assertEqual(len(plotted), 1)
        self.assertEqual(unscored, [])
        self.assertAlmostEqual(plotted[0]["score"], 0.89)
        self.assertAlmostEqual(plotted[0]["output_usd_per_mtok"], 25.0)

    def test_priced_but_unscored_goes_to_unscored(self) -> None:
        prices = mp.build_price_index([or_model("Obscure Model", 3.0)])
        plotted, unscored = mp.join_models(prices, {}, {})
        self.assertEqual(plotted, [])
        self.assertEqual(len(unscored), 1)

    def test_scored_but_unpriced_is_simply_absent(self) -> None:
        caps = mp.build_capability_index([epoch_row("Research Only", 0.7)], "GPQA diamond")
        plotted, unscored = mp.join_models({}, caps, {})
        self.assertEqual((plotted, unscored), ([], []))

    def test_alias_rescues_a_name_mismatch(self) -> None:
        prices = mp.build_price_index([or_model("Gemini 3 Pro Preview", 12.0)])
        caps = mp.build_capability_index([epoch_row("Gemini 3 Pro", 0.85)], "GPQA diamond")
        self.assertEqual(mp.join_models(prices, caps, {})[0], [], "control: should not match")
        aliases = {mp.norm_key("Gemini 3 Pro"): mp.norm_key("Gemini 3 Pro Preview")}
        plotted, _ = mp.join_models(prices, caps, aliases)
        self.assertEqual(len(plotted), 1)


# ---------------------------------------------------------------- run / failure policy

def healthy_prices() -> list[dict[str, Any]]:
    return [or_model("Alpha", 25.0), or_model("Beta", 0.5), or_model("Unscored One", 7.0)]


def healthy_caps() -> list[dict[str, str]]:
    return [epoch_row("Alpha", 0.90), epoch_row("Beta", 0.80)]


def boom(*_: Any) -> Any:
    raise OSError("network down")


class RunTests(unittest.TestCase):
    def test_healthy_run_appends_exactly_one_history_record(self) -> None:
        payload, code = mp.run(healthy_prices, healthy_caps, {}, NOW)
        self.assertEqual(code, 0)
        self.assertFalse(payload["stale"])
        self.assertFalse(payload["capability_stale"])
        self.assertEqual(len(payload["history"]), 1)
        self.assertEqual(payload["snapshot"]["counts"]["plotted"], 2)
        self.assertEqual(payload["snapshot"]["counts"]["unscored"], 1)

    def test_price_failure_carries_previous_forward_and_never_appends(self) -> None:
        previous, _ = mp.run(healthy_prices, healthy_caps, {}, NOW)
        payload, code = mp.run(boom, healthy_caps, previous, LATER)
        self.assertEqual(code, 1, "price failure must fail loud")
        self.assertTrue(payload["stale"])
        self.assertEqual(len(payload["history"]), 1, "a stale price must not enter the series")
        self.assertEqual(payload["generated_at"], mp._iso(LATER))
        self.assertEqual(
            payload["snapshot"]["models"], previous["snapshot"]["models"],
            "carried-forward snapshot must be byte-identical to the last good one",
        )

    def test_price_failure_with_no_previous_still_fails_loud(self) -> None:
        payload, code = mp.run(boom, healthy_caps, {}, NOW)
        self.assertEqual(code, 1)
        self.assertTrue(payload["stale"])
        self.assertEqual(payload["history"], [])

    def test_capability_failure_is_soft_but_visible(self) -> None:
        payload, code = mp.run(healthy_prices, boom, {}, NOW)
        self.assertEqual(code, 3, "degraded, not failed: prices are still good")
        self.assertFalse(payload["stale"])
        self.assertTrue(payload["capability_stale"])
        self.assertEqual(payload["history"], [], "no frontier without scores -> no record")
        self.assertEqual(payload["snapshot"]["counts"]["plotted"], 0)
        self.assertEqual(payload["snapshot"]["counts"]["unscored"], 3,
                         "every priced model should still publish")

    def test_history_accumulates_across_runs(self) -> None:
        first, _ = mp.run(healthy_prices, healthy_caps, {}, NOW)
        second, _ = mp.run(healthy_prices, healthy_caps, first, LATER)
        self.assertEqual(len(second["history"]), 2)
        self.assertEqual([r["ts"] for r in second["history"]], [mp._iso(NOW), mp._iso(LATER)])

    def test_history_is_trimmed_to_max(self) -> None:
        payload: dict[str, Any] = {}
        for hour in range(5):
            moment = datetime(2026, 8, 7, hour, 0, 0, tzinfo=timezone.utc)
            payload, _ = mp.run(healthy_prices, healthy_caps, payload, moment, history_max=3)
        self.assertEqual(len(payload["history"]), 3)
        self.assertEqual(payload["history"][-1]["ts"], mp._iso(datetime(2026, 8, 7, 4, 0, 0, tzinfo=timezone.utc)))

    def test_attribution_is_always_stamped(self) -> None:
        payload, _ = mp.run(healthy_prices, healthy_caps, {}, NOW)
        self.assertEqual(payload["capability_license"], "CC-BY")
        self.assertIn("Epoch AI", payload["capability_attribution"])


# ---------------------------------------------------------------- serialize / write

class SerializeTests(unittest.TestCase):
    def test_round_trip_is_the_identity(self) -> None:
        payload, _ = mp.run(healthy_prices, healthy_caps, {}, NOW)
        self.assertEqual(json.loads(mp.serialize(payload)), json.loads(json.dumps(payload)))

    def test_history_records_are_one_line_each(self) -> None:
        payload, _ = mp.run(healthy_prices, healthy_caps, {}, NOW)
        payload, _ = mp.run(healthy_prices, healthy_caps, payload, LATER)
        body = mp.serialize(payload)
        # Match whole records, not the bare "frontier_price_at" token — that
        # string also appears as an element of the history_fields array.
        record_lines = [
            ln for ln in body.splitlines()
            if '"ts":' in ln and '"frontier_price_at":' in ln
        ]
        self.assertEqual(len(record_lines), 2, "each history record must occupy exactly one line")

    def test_write_atomic_leaves_no_temp_file(self) -> None:
        payload, _ = mp.run(healthy_prices, healthy_caps, {}, NOW)
        with TemporaryDirectory() as tmp:
            out = Path(tmp) / "model-pricing.json"
            mp.write_atomic(out, payload)
            self.assertEqual(json.loads(out.read_text())["benchmark"], mp.DEFAULT_BENCHMARK)
            self.assertEqual([p.name for p in Path(tmp).iterdir()], ["model-pricing.json"])

    def test_unserializable_payload_leaves_previous_file_intact(self) -> None:
        with TemporaryDirectory() as tmp:
            out = Path(tmp) / "model-pricing.json"
            mp.write_atomic(out, {"ok": True})
            before = out.read_text()
            with self.assertRaises(TypeError):
                mp.write_atomic(out, {"bad": {1, 2, 3}})  # a set is not JSON
            self.assertEqual(out.read_text(), before)
            self.assertEqual([p.name for p in Path(tmp).iterdir()], ["model-pricing.json"])

    def test_load_previous_tolerates_corrupt_file(self) -> None:
        with TemporaryDirectory() as tmp:
            out = Path(tmp) / "model-pricing.json"
            out.write_text("{not json", encoding="utf-8")
            self.assertEqual(mp.load_previous(out), {})


class AliasFileTests(unittest.TestCase):
    def test_missing_alias_file_is_not_an_error(self) -> None:
        self.assertEqual(mp.load_aliases(Path("/nonexistent/aliases.json")), {})

    def test_aliases_are_normalized_on_load(self) -> None:
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "aliases.json"
            path.write_text(json.dumps({"aliases": {"Gemini 3 Pro": "Gemini 3 Pro Preview"}}), encoding="utf-8")
            self.assertEqual(mp.load_aliases(path), {"gemini3pro": "gemini3propreview"})


if __name__ == "__main__":
    unittest.main()
