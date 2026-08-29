#!/usr/bin/env python3
"""Tests for the cross-article claim store (build_claim_index + claim_search).

Run: uv run python -m unittest scripts.test_claim_store
     uv run --with pytest pytest scripts/test_claim_store.py -q

Fixtures are synthetic so the suite never depends on the committed corpus
drifting. Two behaviours carry most of the weight and get the most tests:

  1. The REUSE CONTRACT. The store's value is "reuse instead of re-verify",
     which is also exactly how a stale volatile metric gets laundered into a
     new article. Every gate on `reusable` is pinned here.

  2. CANDIDATE PRECISION. `--candidates` shortlists possible contradictions
     for an agent to adjudicate. A false positive is worse than silence, so
     the identical-claim case is asserted to return ZERO — that is a
     regression test for a real defect: the first implementation
     cross-produced every same-unit number and "found" a conflict between
     the 65% and 68% of an identical sentence.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_claim_index as bci  # noqa: E402
import claim_search as cs  # noqa: E402


def _claim(cid, text, **over):
    row = {
        "id": cid,
        "claim": text,
        "type": "metric",
        "source_urls": ["https://www.sec.gov/a"],
        "source_tiers": ["primary"],
        "as_of": "2026-06-30",
        "confidence": "high",
        "risk": "stable",
    }
    row.update(over)
    return row


class ReuseContractTests(unittest.TestCase):
    """A claim is reusable ONLY when stable + dated + not low-confidence."""

    def test_stable_dated_high_is_reusable(self):
        ok, block = bci._reuse_verdict(_claim("c1", "x"))
        self.assertTrue(ok)
        self.assertIsNone(block)

    def test_each_risk_other_than_stable_blocks_reuse(self):
        for risk in ("volatile", "contested", "single-source"):
            with self.subTest(risk=risk):
                ok, block = bci._reuse_verdict(_claim("c1", "x", risk=risk))
                self.assertFalse(ok, f"{risk} must not be directly reusable")
                self.assertEqual(block, risk)

    def test_missing_as_of_blocks_reuse(self):
        for missing in ("", "   ", None):
            with self.subTest(as_of=missing):
                ok, block = bci._reuse_verdict(_claim("c1", "x", as_of=missing))
                self.assertFalse(ok)
                self.assertEqual(block, "no-as-of")

    def test_low_confidence_blocks_reuse(self):
        ok, block = bci._reuse_verdict(_claim("c1", "x", confidence="low"))
        self.assertFalse(ok)
        self.assertEqual(block, "low-confidence")

    def test_medium_confidence_still_reusable(self):
        ok, _ = bci._reuse_verdict(_claim("c1", "x", confidence="medium"))
        self.assertTrue(ok)


class NumericExtractionTests(unittest.TestCase):
    def test_scales_and_currency(self):
        vals = {n["raw"]: n for n in bci.extract_numerics("$1.8 trillion and 43,785 million and 60B")}
        self.assertAlmostEqual(vals["$1.8 trillion"]["value"], 1.8e12)
        self.assertEqual(vals["$1.8 trillion"]["unit"], "currency")
        self.assertAlmostEqual(vals["43,785 million"]["value"], 43785e6)
        self.assertAlmostEqual(vals["60B"]["value"], 60e9)

    def test_percent_and_bps_keep_their_own_units(self):
        nums = bci.extract_numerics("grew 65% while spreads widened 40 bps")
        units = {n["unit"] for n in nums}
        self.assertIn("percent", units)
        self.assertIn("bps", units)

    def test_percent_is_never_scaled_like_a_magnitude(self):
        (n,) = [x for x in bci.extract_numerics("up 50%") if x["unit"] == "percent"]
        self.assertEqual(n["value"], 50.0)


class IndexBuildTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.gen = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def _write(self, stem, claims, meta=True):
        (self.gen / f"{stem}.claims.json").write_text(json.dumps({"claims": claims}), encoding="utf-8")
        if meta:
            path = self.gen / "index.json"
            rows = json.loads(path.read_text()) if path.is_file() else []
            rows.append({"file": f"{stem}.html", "slug": stem, "title": f"T {stem}", "created_at": "2026-01-01T00:00:00Z", "tags": ["x"]})
            path.write_text(json.dumps(rows), encoding="utf-8")

    def test_claim_ids_collide_across_articles_so_keys_are_composite(self):
        # c1 exists in BOTH ledgers; a non-composite key would drop one.
        self._write("art-a", [_claim("c1", "alpha claim")])
        self._write("art-b", [_claim("c1", "beta claim")])
        idx = bci.build_index(self.gen)
        keys = {c["key"] for c in idx["claims"]}
        self.assertEqual(keys, {"art-a#c1", "art-b#c1"})
        self.assertEqual(idx["claim_count"], 2)

    def test_id_less_row_is_indexed_not_dropped(self):
        row = _claim("c1", "has id")
        noid = _claim("", "no id at all")
        del noid["id"]
        self._write("art-a", [row, noid])
        idx = bci.build_index(self.gen)
        self.assertEqual(idx["claim_count"], 2)
        self.assertIn("art-a#idx1", {c["key"] for c in idx["claims"]})

    def test_empty_claim_text_is_skipped(self):
        self._write("art-a", [_claim("c1", "real"), _claim("c2", "   ")])
        self.assertEqual(bci.build_index(self.gen)["claim_count"], 1)

    def test_article_without_metadata_is_still_indexed(self):
        self._write("orphan", [_claim("c1", "still counts")], meta=False)
        idx = bci.build_index(self.gen)
        self.assertEqual(idx["claim_count"], 1)
        self.assertEqual(idx["claims"][0]["article_title"], "")

    def test_unreadable_ledger_is_skipped_not_fatal(self):
        self._write("good", [_claim("c1", "fine")])
        (self.gen / "bad.claims.json").write_text("{not json", encoding="utf-8")
        idx = bci.build_index(self.gen)
        self.assertEqual(idx["claim_count"], 1)

    def test_output_is_deterministic(self):
        self._write("art-a", [_claim("c2", "second"), _claim("c1", "first")])
        self.assertEqual(bci.render(bci.build_index(self.gen)), bci.render(bci.build_index(self.gen)))

    def test_check_flags_a_stale_index(self):
        self._write("art-a", [_claim("c1", "one")])
        out = self.gen / "index-out.json"
        self.assertEqual(bci.main(["--root", str(self.gen), "--out", str(out)]), 0)
        self.assertEqual(bci.main(["--root", str(self.gen), "--out", str(out), "--check"]), 0)
        self._write("art-b", [_claim("c1", "two")])
        self.assertEqual(
            bci.main(["--root", str(self.gen), "--out", str(out), "--check"]),
            1,
            "adding a ledger must make --check fail",
        )

    def test_check_fails_when_index_absent(self):
        self._write("art-a", [_claim("c1", "one")])
        self.assertEqual(
            bci.main(["--root", str(self.gen), "--out", str(self.gen / "nope.json"), "--check"]), 1
        )

    def test_write_is_atomic_no_partial_file_on_failure(self):
        self._write("art-a", [_claim("c1", "one")])
        out = self.gen / "sub" / "index-out.json"
        bci.main(["--root", str(self.gen), "--out", str(out)])
        self.assertTrue(out.is_file())
        # No stray temp files left behind in the target directory.
        self.assertEqual([p.name for p in out.parent.glob(".claim-index-*")], [])

    def test_url_canonicalization_groups_cosmetic_variants(self):
        self._write("art-a", [_claim("c1", "one", source_urls=["https://a.com/x#frag"])])
        self._write("art-b", [_claim("c1", "two", source_urls=["https://a.com/x"])])
        idx = bci.build_index(self.gen)
        self.assertEqual(len(idx["by_url"]["https://a.com/x"]), 2)


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.index = {
            "claims": [
                {
                    "key": "art-a#c1",
                    "article": "art-a",
                    "article_title": "Nvidia results",
                    "id": "c1",
                    "claim": "NVIDIA reported fiscal 2026 revenue of $215.9 billion, up 65%, with Data Center revenue up 68%.",
                    "type": "metric",
                    "source_urls": ["https://www.sec.gov/nvda"],
                    "source_tiers": ["primary"],
                    "hosts": ["sec.gov"],
                    "as_of": "2026-01-25",
                    "confidence": "high",
                    "risk": "stable",
                    "reusable": True,
                    "reuse_block": None,
                },
                {
                    "key": "art-b#c1",
                    "article": "art-b",
                    "article_title": "Cooling supply chain",
                    "id": "c1",
                    "claim": "Liquid cooling attach rates rose sharply across hyperscale data centers.",
                    "type": "event",
                    "source_urls": ["https://example.com/cool"],
                    "source_tiers": ["secondary"],
                    "hosts": ["example.com"],
                    "as_of": "",
                    "confidence": "medium",
                    "risk": "volatile",
                    "reusable": False,
                    "reuse_block": "volatile",
                },
            ],
            "by_host": {"sec.gov": ["art-a#c1"], "example.com": ["art-b#c1"]},
            "by_url": {"https://www.sec.gov/nvda": ["art-a#c1"]},
        }
        self.nvda = self.index["claims"][0]["claim"]

    def test_bm25_finds_the_right_claim(self):
        hits = cs.bm25("nvidia data center revenue", self.index["claims"])
        self.assertTrue(hits)
        self.assertEqual(hits[0][1]["key"], "art-a#c1")

    def test_bm25_empty_query_returns_nothing(self):
        self.assertEqual(cs.bm25("", self.index["claims"]), [])

    # --- candidate precision: the load-bearing behaviour -------------------

    def test_identical_claim_yields_zero_candidates(self):
        """REGRESSION: cross-producting same-unit numbers made 65% "conflict"
        with 68% inside an identical sentence. Identical must mean silent."""
        self.assertEqual(cs.find_candidates(self.nvda, self.index), [])

    def test_genuine_disagreement_flags_only_the_differing_figure(self):
        q = self.nvda.replace("$215.9 billion", "$189.0 billion")
        cands = cs.find_candidates(q, self.index)
        self.assertEqual(len(cands), 1)
        diffs = cands[0]["numeric_differences"]
        self.assertEqual(len(diffs), 1, f"expected only the revenue figure, got {diffs}")
        self.assertEqual(diffs[0]["unit"], "currency")

    def test_rounding_is_not_a_disagreement(self):
        q = self.nvda.replace("$215.9 billion", "$216.0 billion")
        self.assertEqual(cs.find_candidates(q, self.index), [])

    def test_low_token_overlap_never_shortlists_however_different_the_numbers(self):
        q = "Completely unrelated subject matter involving $999.9 billion of something else entirely."
        self.assertEqual(cs.find_candidates(q, self.index), [])

    def test_units_are_never_compared_across_kinds(self):
        # 65 percent vs 65 billion must not pair, and must not conflict.
        a = [{"value": 65.0, "unit": "percent", "raw": "65%"}]
        b = [{"value": 65e9, "unit": "currency", "raw": "$65 billion"}]
        self.assertEqual(cs._numeric_conflicts(a, b), [])

    def test_query_figure_with_no_comparable_counterpart_is_not_a_conflict(self):
        a = [{"value": 40.0, "unit": "bps", "raw": "40 bps"}]
        b = [{"value": 215.9e9, "unit": "currency", "raw": "$215.9 billion"}]
        self.assertEqual(cs._numeric_conflicts(a, b), [])

    def test_candidate_output_is_labelled_as_non_verdict(self):
        q = self.nvda.replace("$215.9 billion", "$189.0 billion")
        (cand,) = cs.find_candidates(q, self.index)
        self.assertIn("CANDIDATE ONLY", cand["note"])

    # --- reuse flags survive into search output ---------------------------

    def test_reusable_only_filters_out_reverify_claims(self):
        claims = self.index["claims"]
        self.assertEqual([c["key"] for c in claims if c["reusable"]], ["art-a#c1"])

    def test_reverify_claim_carries_its_reason(self):
        volatile = self.index["claims"][1]
        self.assertFalse(volatile["reusable"])
        self.assertEqual(volatile["reuse_block"], "volatile")

    def test_formatter_surfaces_the_reuse_verdict(self):
        self.assertIn("REUSABLE", cs._fmt(self.index["claims"][0]))
        self.assertIn("RE-VERIFY", cs._fmt(self.index["claims"][1]))


class DerivableDataTests(unittest.TestCase):
    """Figures are derivable from claim text and must not be committed.

    Storing them cost ~0.5 MB of git and, worse, gave the numbers a second
    home free to drift from the sentence they describe. These pin both
    halves: the index stays clean, and search still works without them.
    """

    def test_index_records_do_not_carry_stored_figures(self):
        import tempfile as _tf

        with _tf.TemporaryDirectory() as td:
            gen = Path(td)
            (gen / "art-a.claims.json").write_text(
                json.dumps({"claims": [_claim("c1", "Revenue was $215.9 billion, up 65%.")]}),
                encoding="utf-8",
            )
            (record,) = bci.build_index(gen)["claims"]
        self.assertNotIn("numerics", record, "figures are derivable; do not commit them")

    def test_candidates_still_work_with_no_stored_figures(self):
        index = {
            "claims": [
                {
                    "key": "art-a#c1",
                    "article": "art-a",
                    "article_title": "T",
                    "id": "c1",
                    "claim": "Revenue was $215.9 billion, up 65%.",
                    "type": "metric",
                    "source_urls": [],
                    "source_tiers": [],
                    "hosts": [],
                    "as_of": "2026-01-25",
                    "confidence": "high",
                    "risk": "stable",
                    "reusable": True,
                    "reuse_block": None,
                }
            ]
        }
        (cand,) = cs.find_candidates("Revenue was $189.0 billion, up 65%.", index)
        self.assertEqual(cand["numeric_differences"][0]["unit"], "currency")
        self.assertEqual(cs.find_candidates("Revenue was $215.9 billion, up 65%.", index), [])


class CommittedIndexTests(unittest.TestCase):
    """The real index must exist and be in sync with the committed ledgers."""

    def test_committed_index_is_not_stale(self):
        if not bci.OUT_PATH.is_file():
            self.skipTest("claim index not built yet")
        self.assertEqual(
            bci.main(["--check"]), 0, "research/claims/index.json is stale — rebuild it"
        )


if __name__ == "__main__":
    unittest.main()
