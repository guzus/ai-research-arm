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
        self.assertEqual(c.refs_with_urls, 2)
        self.assertIn("https://arxiv.org/abs/123", c.ref_urls)
        self.assertIn("https://sec.gov/edgar/x", c.ref_urls)
        self.assertNotIn("https://techcrunch.com/article", c.ref_urls)

    def test_refs_with_urls_excludes_title_only_entries(self):
        """Title-only refs (no <a>) must not count toward refs_with_urls.
        Stops the '20 title-only refs' attack on refs-min gate."""
        body = (
            '<article>'
            '<ol class="ara-refs">'
            '<li id="ref-1"><a href="https://arxiv.org/abs/1">paper 1</a></li>'
            # title-only entry
            '<li id="ref-2">Personal communication, Smith 2024</li>'
            # entry with non-http anchor (e.g. internal hash) — also excluded
            '<li id="ref-3"><a href="#footnote">footnote</a></li>'
            '<li id="ref-4"><a href="https://sec.gov/x">filing</a></li>'
            '</ol>'
            '</article>'
        )
        c = chk._ReferenceHrefCollector()
        c.feed(body)
        # 2 URL-bearing refs, 4 total ref-li elements
        self.assertEqual(c.refs_with_urls, 2)
        self.assertEqual(len(c.ref_urls), 2)

    def test_count_references_uses_url_bearing_count(self):
        """20 title-only refs must NOT pass --refs-min 20."""
        title_only = "".join(
            f'<li id="ref-{i + 1}">Just a title, no link.</li>'
            for i in range(20)
        )
        body = (
            '<article class="ara-doc"><p>Body.</p>'
            f'<ol class="ara-refs">{title_only}</ol>'
            '</article>'
        )
        # Old behavior: count_references returns 20 (would pass refs-min 20).
        # New behavior: returns 0 (no URL-bearing entries).
        self.assertEqual(chk.count_references(body), 0)
        errs = chk.enforce_quality(body, _ns(refs_min=20))
        self.assertEqual(len(errs), 1)
        self.assertIn("reference entries", errs[0])


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


class VerifierFindingsAuditTest(unittest.TestCase):
    """The audit makes bounded-revision (step 7 of the agent prompt)
    deterministically observable. Without it, "the verifier said X
    was unsupported and we addressed it" was faith-based."""

    def _write_findings(self, tmpdir: Path, claims: list[dict]) -> Path:
        import json
        path = tmpdir / "findings.json"
        path.write_text(json.dumps({"claims": claims}), encoding="utf-8")
        return path

    def test_unsupported_claim_left_in_body_fails(self):
        import tempfile
        body = (
            '<article class="ara-doc">'
            '<p>Nvidia hit 75 percent margin in Q4 2026 due to GPU demand.</p>'
            '</article>'
        )
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            findings = self._write_findings(tmpdir, [{
                "id": "c1",
                "text": "Nvidia hit 75 percent margin in Q4 2026 due to GPU demand.",
                "verdict": "unsupported",
                "citation": None,
            }])
            total, surviving = chk.audit_verifier_findings(findings, body)
            self.assertEqual(total, 1)
            self.assertEqual(len(surviving), 1)
            self.assertEqual(surviving[0]["id"], "c1")

    def test_unsupported_claim_demoted_inside_mark_passes(self):
        import tempfile
        body = (
            '<article class="ara-doc">'
            '<p><mark class="ara-mark">Nvidia hit 75 percent margin in Q4 2026 due to GPU demand.</mark></p>'
            '</article>'
        )
        with tempfile.TemporaryDirectory() as tmp:
            findings = self._write_findings(Path(tmp), [{
                "id": "c1",
                "text": "Nvidia hit 75 percent margin in Q4 2026 due to GPU demand.",
                "verdict": "unsupported",
                "citation": None,
            }])
            total, surviving = chk.audit_verifier_findings(findings, body)
            self.assertEqual(total, 1)
            self.assertEqual(surviving, [])

    def test_unsupported_claim_removed_passes(self):
        import tempfile
        body = (
            '<article class="ara-doc">'
            '<p>Different, supported claim about Nvidia revenue.</p>'
            '</article>'
        )
        with tempfile.TemporaryDirectory() as tmp:
            findings = self._write_findings(Path(tmp), [{
                "id": "c1",
                "text": "Nvidia hit 75 percent margin in Q4 2026 due to GPU demand.",
                "verdict": "unsupported",
                "citation": None,
            }])
            total, surviving = chk.audit_verifier_findings(findings, body)
            self.assertEqual(total, 1)
            self.assertEqual(surviving, [])

    def test_supported_claims_ignored(self):
        import tempfile
        body = '<article><p>This claim is fine.</p></article>'
        with tempfile.TemporaryDirectory() as tmp:
            findings = self._write_findings(Path(tmp), [
                {"id": "c1", "text": "This claim is fine.", "verdict": "supported", "citation": "https://x.gov/y"},
                {"id": "c2", "text": "Something else.", "verdict": "weak", "citation": None},
            ])
            total, surviving = chk.audit_verifier_findings(findings, body)
            # 0 unsupported → audit passes vacuously
            self.assertEqual(total, 0)
            self.assertEqual(surviving, [])

    def test_whitespace_and_case_tolerant(self):
        import tempfile
        body = (
            '<article><p>nvidia hit 75 PERCENT margin in q4 2026 due to gpu demand.</p></article>'
        )
        with tempfile.TemporaryDirectory() as tmp:
            findings = self._write_findings(Path(tmp), [{
                "id": "c1",
                "text": "Nvidia hit 75 percent margin in Q4 2026 due to GPU demand.",
                "verdict": "unsupported",
                "citation": None,
            }])
            total, surviving = chk.audit_verifier_findings(findings, body)
            # case-insensitive match → claim still present, must FAIL
            self.assertEqual(len(surviving), 1)

    def test_malformed_json_raises(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text("{not json")
            with self.assertRaises(ValueError):
                chk.audit_verifier_findings(path, "<article></article>")

    def test_top_level_not_object_raises(self):
        import tempfile, json
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text(json.dumps([1, 2, 3]))
            with self.assertRaises(ValueError):
                chk.audit_verifier_findings(path, "<article></article>")

    def test_missing_claims_key_raises(self):
        import tempfile, json
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text(json.dumps({"findings": []}))
            with self.assertRaises(ValueError):
                chk.audit_verifier_findings(path, "<article></article>")

    def test_probe_matches_through_dsl_cite_marker(self):
        """Verifier text uses [^N] (DSL form), body has rendered cite.
        Without stripping, probe never matches → false pass.
        With stripping, probe matches → correctly FAIL."""
        import tempfile
        body = (
            '<article class="ara-doc">'
            '<p>Nvidia hit 75 percent margin in Q4 2026'
            '<sup><a class="ara-cite" href="#ref-12">12</a></sup>.</p>'
            '</article>'
        )
        with tempfile.TemporaryDirectory() as tmp:
            findings = self._write_findings(Path(tmp), [{
                "id": "c1",
                # DSL-shape: how the verifier reads it from .ara.md
                "text": "Nvidia hit 75 percent margin in Q4 2026[^12].",
                "verdict": "unsupported",
                "citation": "https://...",
            }])
            total, surviving = chk.audit_verifier_findings(findings, body)
            self.assertEqual(total, 1)
            self.assertEqual(
                len(surviving), 1,
                "Cite-stripped probe should match cite-stripped body and "
                "FAIL the audit. Without P2 fix, this returns surviving=[] "
                "(false pass).",
            )

    def test_demoted_claim_with_inline_markup_passes(self):
        """When the demoted sentence contains inline markup like <em>,
        <strong>, <a>, the mark blob carries those tags but the
        tag-stripped body does not. Without symmetric tag-stripping
        on mark regions, a valid demotion fails the audit."""
        import tempfile
        body = (
            '<article class="ara-doc">'
            '<p><mark class="ara-mark">OpenAI raised <strong>$40 billion</strong> in <em>2026</em>.</mark></p>'
            '</article>'
        )
        with tempfile.TemporaryDirectory() as tmp:
            findings = self._write_findings(Path(tmp), [{
                "id": "c1",
                "text": "OpenAI raised $40 billion in 2026.",
                "verdict": "unsupported",
                "citation": None,
            }])
            total, surviving = chk.audit_verifier_findings(findings, body)
            self.assertEqual(total, 1)
            self.assertEqual(
                len(surviving), 0,
                "demoted claim with inline markup must be detected as "
                "demoted (was falsely flagged surviving without the "
                "mark-region tag-strip fix)",
            )

    def test_probe_matches_through_multi_cite_marker(self):
        """Multi-cite `[^1,2,3]` form must also strip cleanly."""
        import tempfile
        body = (
            '<article class="ara-doc">'
            '<p>OpenAI raised $40 billion in 2026'
            '<sup><a class="ara-cite" href="#ref-1">1</a></sup>'
            '<sup><a class="ara-cite" href="#ref-2">2</a></sup>.</p>'
            '</article>'
        )
        with tempfile.TemporaryDirectory() as tmp:
            findings = self._write_findings(Path(tmp), [{
                "id": "c2",
                "text": "OpenAI raised $40 billion in 2026[^1,2].",
                "verdict": "unsupported",
                "citation": None,
            }])
            total, surviving = chk.audit_verifier_findings(findings, body)
            self.assertEqual(len(surviving), 1, "multi-cite must strip too")

    def test_strip_cite_markers_helper(self):
        import re as _re
        def collapse(s): return _re.sub(r"\s+", " ", s).strip()
        # DSL form
        self.assertEqual(
            collapse(chk._strip_cite_markers("Claim with [^1] cite.")),
            "Claim with cite.",
        )
        # Multi-cite
        self.assertEqual(
            collapse(chk._strip_cite_markers("Claim [^1,2,3] here.")),
            "Claim here.",
        )
        # Rendered form
        self.assertEqual(
            collapse(chk._strip_cite_markers(
                'Claim<sup><a class="ara-cite" href="#ref-9">9</a></sup> end.'
            )),
            "Claim end.",
        )

    def test_empty_text_skipped_not_failed(self):
        import tempfile
        body = '<article><p>Something here.</p></article>'
        with tempfile.TemporaryDirectory() as tmp:
            findings = self._write_findings(Path(tmp), [{
                "id": "c1",
                "text": "",
                "verdict": "unsupported",
                "citation": None,
            }])
            total, surviving = chk.audit_verifier_findings(findings, body)
            # Empty text → can't audit → not added to surviving
            self.assertEqual(total, 1)
            self.assertEqual(surviving, [])


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
