#!/usr/bin/env python3
"""Unit tests for the research-quality gates added to
scripts/check_generative_research.py.

These tests cover the heuristics themselves (not the validate_body
plumbing — that has its own tests in test_ara_dsl.py). For each gate
we assert behavior on a hand-built synthetic article plus a sanity
check against a known-good article in research/generative/."""

from __future__ import annotations

import argparse
import sys
import unittest
from pathlib import Path

# Reuse the same sys.path bootstrap the script itself uses.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_generative_research as chk  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
SANITY_GOOD = (
    REPO_ROOT
    / "research"
    / "generative"
    / "2026-05-16T085517--cerebras-wse-3-vs-nvidia-gb200-cost-per-token-economics.html"
)


def _ns(**overrides):
    """Build an argparse.Namespace with all gate flags = None, then
    apply overrides. Lets each test focus on a single gate."""
    defaults = dict(
        cite_density_min=None,
        refs_min=None,
        primary_share_min=None,
        cited_claims_min=None,
    )
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def _article(refs_count=0, cites_count=0, body_words=100, primary_hosts=None):
    """Build a minimal synthetic article body. By default zero refs
    and zero cites; pass counts to populate."""
    body_text = " ".join(["Lorem"] * body_words)
    sup_block = "".join(
        f'<sup><a class="ara-cite" href="#ref-{i + 1}">{i + 1}</a></sup>'
        for i in range(cites_count)
    )
    if primary_hosts is None:
        primary_hosts = ["example.com"] * refs_count
    refs_lis = "".join(
        f'<li id="ref-{i + 1}"><a href="https://{primary_hosts[i]}/x">src</a></li>'
        for i in range(refs_count)
    )
    refs_block = (
        f'<ol class="ara-refs">{refs_lis}</ol>' if refs_count else ""
    )
    return (
        '<article class="ara-doc">'
        f"<h2>Test</h2><p>{body_text}{sup_block}</p>"
        f"{refs_block}"
        "</article>"
    )


class PrimarySourceClassificationTest(unittest.TestCase):
    def test_government_suffix_is_primary(self):
        self.assertTrue(chk.is_primary_source("data.gov"))
        self.assertTrue(chk.is_primary_source("sec.gov"))
        self.assertTrue(chk.is_primary_source("emp.lbl.gov"))

    def test_education_suffix_is_primary(self):
        self.assertTrue(chk.is_primary_source("stanford.edu"))
        self.assertTrue(chk.is_primary_source("ox.ac.uk"))

    def test_arxiv_and_research_repos_primary(self):
        self.assertTrue(chk.is_primary_source("arxiv.org"))
        self.assertTrue(chk.is_primary_source("openreview.net"))
        self.assertTrue(chk.is_primary_source("biorxiv.org"))

    def test_first_party_corp_blogs_primary(self):
        self.assertTrue(chk.is_primary_source("anthropic.com"))
        self.assertTrue(chk.is_primary_source("blog.google"))
        self.assertTrue(chk.is_primary_source("developer.nvidia.com"))
        self.assertTrue(chk.is_primary_source("cerebras.ai"))

    def test_subdomain_inherits_primary(self):
        # subdomain of a registered primary suffix
        self.assertTrue(chk.is_primary_source("investor.bloomenergy.com"))
        # bloomenergy.com is in EXACT list via investor. — confirm the bare host
        self.assertTrue(chk.is_primary_source("investor.natera.com"))

    def test_typical_secondary_press_not_primary(self):
        self.assertFalse(chk.is_primary_source("techcrunch.com"))
        self.assertFalse(chk.is_primary_source("theinformation.com"))
        self.assertFalse(chk.is_primary_source("bloomberg.com"))
        self.assertFalse(chk.is_primary_source("cnbc.com"))

    def test_www_prefix_normalized(self):
        self.assertTrue(chk.is_primary_source("www.sec.gov"))
        self.assertTrue(chk.is_primary_source("www.arxiv.org"))

    def test_none_or_empty_not_primary(self):
        self.assertFalse(chk.is_primary_source(None))
        self.assertFalse(chk.is_primary_source(""))


class CiteDensityTest(unittest.TestCase):
    def test_zero_cites_density_zero(self):
        body = _article(cites_count=0, body_words=500)
        density, cites, words = chk.cite_density(body)
        self.assertEqual(cites, 0)
        self.assertEqual(density, 0.0)
        self.assertGreater(words, 0)

    def test_density_proportional_to_cites(self):
        body = _article(cites_count=15, body_words=1500)
        density, cites, _ = chk.cite_density(body)
        self.assertEqual(cites, 15)
        self.assertAlmostEqual(density, 10.0, delta=0.5)

    def test_gate_below_threshold_fails(self):
        # 5 cites in 1000 words = density 5.0; gate at 10 fails
        body = _article(cites_count=5, body_words=1000)
        errs = chk.enforce_quality(body, _ns(cite_density_min=10.0))
        self.assertEqual(len(errs), 1)
        self.assertIn("cite density", errs[0])

    def test_gate_above_threshold_passes(self):
        body = _article(cites_count=20, body_words=1000)
        errs = chk.enforce_quality(body, _ns(cite_density_min=10.0))
        self.assertEqual(errs, [])


class RefsMinTest(unittest.TestCase):
    def test_zero_refs_below_threshold(self):
        body = _article(refs_count=0)
        errs = chk.enforce_quality(body, _ns(refs_min=20))
        self.assertEqual(len(errs), 1)
        self.assertIn("reference entries", errs[0])

    def test_meets_threshold_passes(self):
        body = _article(refs_count=20)
        errs = chk.enforce_quality(body, _ns(refs_min=20))
        self.assertEqual(errs, [])


class PrimaryShareTest(unittest.TestCase):
    def test_all_secondary_fails(self):
        body = _article(
            refs_count=10,
            primary_hosts=["techcrunch.com"] * 10,
        )
        share, prim, total = chk.primary_share(body)
        self.assertEqual(prim, 0)
        self.assertEqual(total, 10)
        self.assertEqual(share, 0.0)

    def test_all_primary_passes(self):
        body = _article(
            refs_count=10,
            primary_hosts=["arxiv.org", "sec.gov", "anthropic.com"] * 4,
        )
        share, prim, total = chk.primary_share(body)
        self.assertEqual(total, 10)
        self.assertEqual(prim, 10)
        self.assertEqual(share, 1.0)
        errs = chk.enforce_quality(body, _ns(primary_share_min=0.5))
        self.assertEqual(errs, [])

    def test_below_threshold_fails(self):
        body = _article(
            refs_count=10,
            primary_hosts=(["arxiv.org"] * 3 + ["techcrunch.com"] * 7),
        )
        errs = chk.enforce_quality(body, _ns(primary_share_min=0.5))
        self.assertEqual(len(errs), 1)
        self.assertIn("primary-source share", errs[0])

    def test_no_refs_fails_with_message(self):
        body = _article(refs_count=0)
        errs = chk.enforce_quality(body, _ns(primary_share_min=0.5))
        self.assertEqual(len(errs), 1)
        self.assertIn("no reference URLs", errs[0])


class CitedClaimShareTest(unittest.TestCase):
    def test_all_substantive_uncited_zero_share(self):
        body = (
            '<article class="ara-doc">'
            "<p>Cerebras posted $5.55 billion in 2026. "
            "Nvidia reported 75 percent margin. "
            "OpenAI raised funding rounds.</p>"
            "</article>"
        )
        share, cited, total = chk.cited_claim_share(body)
        self.assertGreater(total, 0)
        self.assertEqual(cited, 0)
        self.assertEqual(share, 0.0)

    def test_cited_substantive_counted(self):
        body = (
            '<article class="ara-doc">'
            '<p>Cerebras posted $5.55 billion in 2026'
            '<sup><a class="ara-cite" href="#ref-1">1</a></sup>. '
            'Nvidia reported 75 percent margin'
            '<sup><a class="ara-cite" href="#ref-2">2</a></sup>.</p>'
            "</article>"
        )
        share, cited, total = chk.cited_claim_share(body)
        self.assertEqual(cited, total)
        self.assertEqual(share, 1.0)

    def test_gate_threshold_enforced(self):
        # Two substantive sentences, only one cited → 0.5 share
        body = (
            '<article class="ara-doc"><p>'
            "Cerebras posted $5.55 billion in 2026"
            '<sup><a class="ara-cite" href="#ref-1">1</a></sup>. '
            "Nvidia reported 75 percent margin."
            "</p></article>"
        )
        errs = chk.enforce_quality(body, _ns(cited_claims_min=0.8))
        self.assertEqual(len(errs), 1)
        self.assertIn("cited-claim share", errs[0])
        # Same body at threshold 0.4 → passes
        errs = chk.enforce_quality(body, _ns(cited_claims_min=0.4))
        self.assertEqual(errs, [])


class ReferenceHrefCollectorTest(unittest.TestCase):
    def test_only_ref_li_hrefs_counted(self):
        body = (
            '<article>'
            # In-body link to another section — should NOT count
            '<p>See <a href="https://techcrunch.com/article">this</a>.</p>'
            '<ol class="ara-refs">'
            '<li id="ref-1"><a href="https://arxiv.org/abs/123">paper</a></li>'
            '<li id="ref-2"><a href="https://sec.gov/edgar/x">filing</a></li>'
            '</ol>'
            '</article>'
        )
        c = chk._ReferenceHrefCollector()
        c.feed(body)
        self.assertEqual(len(c.ref_urls), 2)
        self.assertIn("https://arxiv.org/abs/123", c.ref_urls)
        self.assertIn("https://sec.gov/edgar/x", c.ref_urls)
        self.assertNotIn("https://techcrunch.com/article", c.ref_urls)


class EnforceQualityCompositionTest(unittest.TestCase):
    def test_multiple_failures_all_reported(self):
        body = _article(
            cites_count=2, refs_count=2, body_words=500,
            primary_hosts=["techcrunch.com", "cnbc.com"],
        )
        errs = chk.enforce_quality(
            body,
            _ns(cite_density_min=10.0, refs_min=20, primary_share_min=0.5),
        )
        # All three should fail
        self.assertEqual(len(errs), 3)
        self.assertTrue(any("cite density" in e for e in errs))
        self.assertTrue(any("reference entries" in e for e in errs))
        self.assertTrue(any("primary-source share" in e for e in errs))


class SanityAgainstKnownGoodArticleTest(unittest.TestCase):
    """The task explicitly named this file as a high-quality article
    that the gates must accept. If we ever ratchet defaults up and
    this article fails, that's a signal to recalibrate, not to ratchet."""

    @unittest.skipUnless(SANITY_GOOD.exists(), "fixture article not present")
    def test_cerebras_wse_passes_workflow_gates(self):
        body = SANITY_GOOD.read_text(encoding="utf-8")
        errs = chk.enforce_quality(
            body,
            _ns(cite_density_min=10.0, refs_min=20),
        )
        self.assertEqual(
            errs, [],
            "cerebras-wse-3 article must pass the workflow gates "
            "(--cite-density-min 10 --refs-min 20). Errors: " + "; ".join(errs),
        )


if __name__ == "__main__":
    unittest.main()
