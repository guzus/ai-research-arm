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
        min_corroborating_sources=None,
    )
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def _article(refs_count=0, cites_count=0, body_words=100, primary_hosts=None):
    """Build a minimal synthetic article body. By default zero refs
    and zero cites; pass counts to populate.

    Each ref gets a DISTINCT URL path so count_references()'s distinct-
    URL counting works as the test expects. To inject duplicates,
    pass primary_hosts with repeated entries (the path-suffix is what
    makes them distinct, so passing the same host N times still yields
    N distinct URLs in the synthetic article)."""
    body_text = " ".join(["Lorem"] * body_words)
    sup_block = "".join(
        f'<sup><a class="ara-cite" href="#ref-{i + 1}">{i + 1}</a></sup>'
        for i in range(cites_count)
    )
    if primary_hosts is None:
        primary_hosts = ["example.com"] * refs_count
    # Add /{i} to each URL so the helper yields refs_count distinct URLs
    # by default; tests that want to verify duplicate-handling should
    # construct their own bodies inline.
    refs_lis = "".join(
        f'<li id="ref-{i + 1}"><a href="https://{primary_hosts[i]}/x/{i + 1}">src</a></li>'
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
        self.assertEqual(chk.count_references(body), 0)
        errs = chk.enforce_quality(body, _ns(refs_min=20))
        self.assertEqual(len(errs), 1)
        self.assertIn("reference entries", errs[0])

    def test_count_references_counts_distinct_urls(self):
        """20 refs all pointing to the same URL must NOT pass --refs-min 20.
        Workflow target is '20 DISTINCT source URLs', so duplicates can't
        satisfy the gate."""
        same_url = "".join(
            f'<li id="ref-{i + 1}"><a href="https://arxiv.org/abs/2401.00001">paper</a></li>'
            for i in range(20)
        )
        body = (
            '<article class="ara-doc"><p>Body.</p>'
            f'<ol class="ara-refs">{same_url}</ol>'
            '</article>'
        )
        # All 20 li elements have URLs but only 1 distinct URL → count = 1.
        self.assertEqual(chk.count_references(body), 1)
        errs = chk.enforce_quality(body, _ns(refs_min=20))
        self.assertEqual(len(errs), 1, "duplicate URL spam must fail refs-min")

    def test_url_normalization_for_distinct_counting(self):
        """www prefix, trailing slash, default port, case → normalized.
        Scheme (http vs https) is intentionally kept distinct."""
        self.assertEqual(
            chk._normalize_url("https://www.example.com/x"),
            chk._normalize_url("https://EXAMPLE.com/x/"),
        )
        self.assertEqual(
            chk._normalize_url("https://example.com:443/x"),
            chk._normalize_url("https://example.com/x"),
        )
        # Different paths remain distinct
        self.assertNotEqual(
            chk._normalize_url("https://example.com/a"),
            chk._normalize_url("https://example.com/b"),
        )


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

    def test_duplicate_occurrences_partial_demotion_fails(self):
        """When the same unsupported claim appears N times and only 1
        copy is wrapped in <mark>, the OTHER copies still survive
        outside a mark region — audit must fail. The pre-fix
        `probe in mark_norm` test would pass because the probe exists
        somewhere in the mark blob."""
        import tempfile
        body = (
            '<article class="ara-doc">'
            # First occurrence wrapped in mark (demoted)
            '<p><mark class="ara-mark">Nvidia hit 75 percent margin in Q4 2026.</mark></p>'
            # Second occurrence unwrapped (still surviving — should fail)
            '<p>Nvidia hit 75 percent margin in Q4 2026.</p>'
            '</article>'
        )
        with tempfile.TemporaryDirectory() as tmp:
            findings = self._write_findings(Path(tmp), [{
                "id": "c1",
                "text": "Nvidia hit 75 percent margin in Q4 2026.",
                "verdict": "unsupported",
                "citation": None,
            }])
            total, surviving = chk.audit_verifier_findings(findings, body)
            self.assertEqual(total, 1)
            self.assertEqual(
                len(surviving), 1,
                "When 2 occurrences exist and only 1 is demoted, the "
                "other survives — audit must fail. Without the count-"
                "based fix, the old `probe in mark_norm` returned True "
                "and the audit would falsely pass.",
            )
            self.assertEqual(surviving[0]['body_occurrences'], 2)
            self.assertEqual(surviving[0]['mark_occurrences'], 1)

    def test_duplicate_occurrences_all_demoted_passes(self):
        """When the same claim appears N times and ALL N are demoted,
        the audit correctly passes."""
        import tempfile
        body = (
            '<article class="ara-doc">'
            '<p><mark class="ara-mark">Nvidia hit 75 percent margin in Q4 2026.</mark></p>'
            '<p><mark class="ara-mark">Nvidia hit 75 percent margin in Q4 2026.</mark></p>'
            '</article>'
        )
        with tempfile.TemporaryDirectory() as tmp:
            findings = self._write_findings(Path(tmp), [{
                "id": "c1",
                "text": "Nvidia hit 75 percent margin in Q4 2026.",
                "verdict": "unsupported",
                "citation": None,
            }])
            total, surviving = chk.audit_verifier_findings(findings, body)
            self.assertEqual(surviving, [])

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


class CorroborationGateTest(unittest.TestCase):
    """Gate 1: --min-corroborating-sources. Each substantive cited claim
    needs N distinct source hosts unless explicitly wrapped in
    `==single-source: ...==`.

    The corpus calibration (PR body) shows N=2 default would fail 84%
    of historical claims, so the gate ships opt-in only. Tests assert
    correctness, not the default-on policy."""

    def _article_with_refs(self, body_inner: str, refs: list[tuple[int, str]]) -> str:
        """Build an article with explicit (ref_num, host) ref entries.
        Each ref gets a distinct URL path so URL-normalization can't
        collapse them."""
        ref_lis = "".join(
            f'<li id="ref-{n}"><a href="https://{host}/path/{n}">src</a></li>'
            for n, host in refs
        )
        return (
            '<article class="ara-doc">'
            f"<p>{body_inner}</p>"
            f'<ol class="ara-refs">{ref_lis}</ol>'
            "</article>"
        )

    def test_claim_with_two_distinct_hosts_passes(self):
        body = self._article_with_refs(
            'OpenAI raised $40 billion in 2026'
            '<sup><a class="ara-cite" href="#ref-1">1</a></sup>'
            '<sup><a class="ara-cite" href="#ref-2">2</a></sup>.',
            [(1, "anthropic.com"), (2, "openai.com")],
        )
        failing, total = chk.corroboration_audit(body, 2)
        self.assertEqual(total, 1)
        self.assertEqual(failing, [])

    def test_claim_with_two_cites_same_host_fails(self):
        """Two cites both to the same host (different URLs on same
        host) count as 1 distinct host — claim fails @ N=2."""
        body = self._article_with_refs(
            'Cerebras shipped 142x speedup'
            '<sup><a class="ara-cite" href="#ref-1">1</a></sup>'
            '<sup><a class="ara-cite" href="#ref-2">2</a></sup>.',
            [(1, "cerebras.ai"), (2, "cerebras.ai")],
        )
        failing, total = chk.corroboration_audit(body, 2)
        self.assertEqual(total, 1)
        self.assertEqual(len(failing), 1)
        self.assertEqual(failing[0]["distinct_hosts"], 1)
        self.assertEqual(failing[0]["hosts"], ["cerebras.ai"])

    def test_single_source_wrapping_exempts_claim(self):
        """A failing-by-host-count claim wrapped in <mark> whose inner
        text begins with `single-source:` is exempt — that's the
        agent's explicit acknowledgment."""
        body = self._article_with_refs(
            '<mark class="ara-mark">single-source: Cerebras posted '
            '21 PB/s aggregate bandwidth'
            '<sup><a class="ara-cite" href="#ref-1">1</a></sup>.</mark>',
            [(1, "cerebras.ai")],
        )
        failing, total = chk.corroboration_audit(body, 2)
        self.assertEqual(total, 1)
        self.assertEqual(failing, [],
                         "single-source: wrapping must exempt the claim")

    def test_single_source_exemption_via_dsl_compile(self):
        """Wraps the claim via DSL `==single-source: ...==` (the
        intended author-facing syntax) and confirms the compiled
        HTML survives the corroboration audit. Guards against the
        compile output shape changing under us."""
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from compile_ara import parse_inline
        sentence = (
            '==single-source: Cerebras posted 21 PB/s bandwidth[^1].=='
        )
        compiled = parse_inline(sentence)
        body = (
            '<article class="ara-doc">'
            f'<p>{compiled}</p>'
            '<ol class="ara-refs">'
            '<li id="ref-1"><a href="https://cerebras.ai/x">src</a></li>'
            '</ol></article>'
        )
        failing, total = chk.corroboration_audit(body, 2)
        self.assertEqual(failing, [],
                         "DSL-compiled single-source wrap must exempt")

    def test_no_cited_claims_passes_trivially(self):
        """An article with no cited substantive sentences (e.g. a
        methodology piece) passes the gate vacuously."""
        body = (
            '<article class="ara-doc">'
            '<p>This is a methodology piece with no factual claims.</p>'
            '<p>It explains an approach without numbers or attributions.</p>'
            '</article>'
        )
        failing, total = chk.corroboration_audit(body, 2)
        self.assertEqual(total, 0)
        self.assertEqual(failing, [])

    def test_non_substantive_cited_sentence_ignored(self):
        """A cited sentence with no number/percent/dollar/name-entity
        proxy isn't a 'substantive claim' — gate ignores it."""
        body = self._article_with_refs(
            'see this related work'
            '<sup><a class="ara-cite" href="#ref-1">1</a></sup>.',
            [(1, "arxiv.org")],
        )
        # No digits, no $, no %, no multi-word capitalized phrase →
        # not substantive, not counted.
        failing, total = chk.corroboration_audit(body, 2)
        self.assertEqual(total, 0)

    def test_headings_excluded_from_substantive_count(self):
        """Headings often look substantive (multi-word capitalized)
        but rarely carry meaningful claims. The pre-strip step removes
        them so they can't contribute false positives."""
        body = (
            '<article class="ara-doc">'
            '<h2>Cerebras WSE-3 Architecture'
            '<sup><a class="ara-cite" href="#ref-1">1</a></sup></h2>'
            '<p>A non-substantive cited sentence is here too.</p>'
            '<ol class="ara-refs">'
            '<li id="ref-1"><a href="https://cerebras.ai/x">src</a></li>'
            '</ol></article>'
        )
        failing, total = chk.corroboration_audit(body, 2)
        # Heading-cited claim is stripped; body claim has no cite → 0 total
        self.assertEqual(total, 0)

    def test_multi_cite_one_resolvable_one_orphan(self):
        """A cite to a ref-num that doesn't exist in the references
        list (orphan citation) doesn't contribute a host. If the only
        OTHER cite is a duplicate host, claim fails."""
        body = self._article_with_refs(
            'Nvidia hit $62B revenue'
            '<sup><a class="ara-cite" href="#ref-1">1</a></sup>'
            '<sup><a class="ara-cite" href="#ref-99">99</a></sup>.',
            [(1, "nvidia.com")],  # ref-99 is orphan
        )
        failing, total = chk.corroboration_audit(body, 2)
        self.assertEqual(total, 1)
        self.assertEqual(len(failing), 1)
        self.assertEqual(failing[0]["distinct_hosts"], 1)
        self.assertEqual(failing[0]["hosts"], ["nvidia.com"])

    def test_enforce_quality_threading(self):
        """Gate 1 plumbs through enforce_quality()."""
        body = self._article_with_refs(
            'Nvidia hit $62B in Q4 2026'
            '<sup><a class="ara-cite" href="#ref-1">1</a></sup>.',
            [(1, "nvidia.com")],
        )
        errs = chk.enforce_quality(body, _ns(min_corroborating_sources=2))
        self.assertEqual(len(errs), 1)
        self.assertIn("distinct source host", errs[0])
        self.assertIn("single-source", errs[0])

    def test_enforce_quality_threshold_one_passes(self):
        """At N=1 the gate degenerates to 'every cited claim has a
        resolvable host' which is the existing cited-claims-min gate.
        Still useful as a smoke test."""
        body = self._article_with_refs(
            'Nvidia hit $62B revenue'
            '<sup><a class="ara-cite" href="#ref-1">1</a></sup>.',
            [(1, "nvidia.com")],
        )
        errs = chk.enforce_quality(body, _ns(min_corroborating_sources=1))
        self.assertEqual(errs, [])

    def test_ref_host_map_skips_title_only_refs(self):
        """Refs without an http(s) URL don't get added to the host map
        — a cite pointing at them resolves to no host (treated as not
        contributing to the distinct-host count)."""
        body = (
            '<article class="ara-doc"><p>Claim with cite.</p>'
            '<ol class="ara-refs">'
            '<li id="ref-1">Personal communication.</li>'
            '<li id="ref-2"><a href="https://arxiv.org/x">paper</a></li>'
            '</ol></article>'
        )
        m = chk.build_ref_host_map(body)
        self.assertNotIn(1, m)
        self.assertEqual(m.get(2), "arxiv.org")

    def test_www_prefix_normalized_in_host_map(self):
        """Hosts in the map are normalized (lowercase, www stripped)
        so duplicate-host detection treats www.example.com and
        example.com as the same source."""
        body = (
            '<article class="ara-doc"><p>x</p>'
            '<ol class="ara-refs">'
            '<li id="ref-1"><a href="https://www.Cerebras.ai/x">a</a></li>'
            '<li id="ref-2"><a href="https://CEREBRAS.AI/y">b</a></li>'
            '</ol></article>'
        )
        m = chk.build_ref_host_map(body)
        self.assertEqual(m.get(1), "cerebras.ai")
        self.assertEqual(m.get(2), "cerebras.ai")

    def test_first_url_per_ref_li_is_canonical(self):
        """A ref entry with multiple URLs uses ONLY the first http URL
        for host classification — bibliographic convention is primary
        source first."""
        body = (
            '<article class="ara-doc"><p>x</p>'
            '<ol class="ara-refs">'
            '<li id="ref-1">'
            '<a href="https://arxiv.org/abs/2024.001">paper</a>'
            ' (also at <a href="https://medium.com/repost">medium</a>)'
            '</li></ol></article>'
        )
        m = chk.build_ref_host_map(body)
        # First URL is arxiv; medium does NOT register as the ref host
        self.assertEqual(m.get(1), "arxiv.org")

    def test_corroboration_invalid_min(self):
        """N must be >= 1."""
        body = '<article><p>x</p></article>'
        with self.assertRaises(ValueError):
            chk.corroboration_audit(body, 0)


class QSanityGateTest(unittest.TestCase):
    """Gate 2: --qsanity. Warn-only in v1 — qsanity_scan returns the
    list of warning lines; the CLI prints to stderr but doesn't fail
    the build. Tests assert pattern correctness."""

    def test_donut_summing_over_100_warns(self):
        """A :::donut block with data-pct values summing > 105% is flagged.
        Per the qsanity rationale: donut slices are slices of one
        whole — if they overlap, the chart is wrong."""
        body = (
            '<article class="ara-doc">'
            '<ul class="ara-donut" data-title="x">'
            '<li data-pct="80">A</li>'
            '<li data-pct="50">B</li>'
            '<li data-pct="45">C</li>'
            '</ul></article>'
        )
        warns = chk.qsanity_scan(body, 2026)
        self.assertEqual(len(warns), 1)
        self.assertIn("175", warns[0])  # the sum
        self.assertIn("donut", warns[0].lower())

    def test_donut_summing_under_limit_silent(self):
        """Donut summing to 100% (or 105% with rounding tolerance) is silent."""
        body = (
            '<article class="ara-doc">'
            '<ul class="ara-donut" data-title="x">'
            '<li data-pct="40">A</li>'
            '<li data-pct="35">B</li>'
            '<li data-pct="25">C</li>'
            '</ul></article>'
        )
        warns = chk.qsanity_scan(body, 2026)
        self.assertEqual([w for w in warns if "donut" in w.lower()], [])

    def test_donut_rounding_tolerance(self):
        """Sum of 103% is within the 105% tolerance — should NOT warn."""
        body = (
            '<article class="ara-doc">'
            '<ul class="ara-donut" data-title="x">'
            '<li data-pct="34">A</li>'
            '<li data-pct="35">B</li>'
            '<li data-pct="34">C</li>'
            '</ul></article>'
        )
        warns = chk.qsanity_scan(body, 2026)
        self.assertEqual([w for w in warns if "donut" in w.lower()], [])

    def test_market_share_over_100_warns(self):
        body = (
            '<article class="ara-doc">'
            '<p>Cerebras commands a 175% market share in wafer-scale chips.</p>'
            '</article>'
        )
        warns = chk.qsanity_scan(body, 2026)
        self.assertTrue(any("175" in w and "market share" in w for w in warns))

    def test_market_share_at_99_silent(self):
        body = (
            '<article class="ara-doc">'
            '<p>Cerebras commands a 99% market share in wafer-scale chips.</p>'
            '</article>'
        )
        warns = chk.qsanity_scan(body, 2026)
        self.assertEqual([w for w in warns if "market share" in w], [])

    def test_yoy_growth_over_1000_warns(self):
        body = (
            '<article class="ara-doc">'
            '<p>Revenue grew 2500% YoY in Q4 2026.</p>'
            '</article>'
        )
        warns = chk.qsanity_scan(body, 2026)
        self.assertTrue(any("2500" in w and "YoY" in w for w in warns))

    def test_yoy_growth_at_500_silent(self):
        body = (
            '<article class="ara-doc">'
            '<p>Revenue grew 500% YoY in Q4 2026.</p>'
            '</article>'
        )
        warns = chk.qsanity_scan(body, 2026)
        self.assertEqual([w for w in warns if "YoY" in w], [])

    def test_future_date_over_horizon_warns(self):
        body = (
            '<article class="ara-doc">'
            '<p>The forecast projects a peak in 2055 based on current rates.</p>'
            '</article>'
        )
        warns = chk.qsanity_scan(body, 2026)
        # 2055 > 2026+10 → warn
        self.assertTrue(any("2055" in w for w in warns))

    def test_future_date_in_horizon_silent(self):
        """2032 is within 10y horizon of 2026 — silent."""
        body = (
            '<article class="ara-doc">'
            '<p>By 2032 the market is expected to mature.</p>'
            '</article>'
        )
        warns = chk.qsanity_scan(body, 2026)
        self.assertEqual([w for w in warns if "2032" in w], [])

    def test_past_year_silent(self):
        """Historical references aren't flagged."""
        body = (
            '<article class="ara-doc">'
            '<p>The IPO was filed in 2024 and priced in 2026.</p>'
            '</article>'
        )
        warns = chk.qsanity_scan(body, 2026)
        self.assertEqual(warns, [])

    def test_future_date_deduped(self):
        """The same year mentioned twice should only warn once."""
        body = (
            '<article class="ara-doc">'
            '<p>The 2055 forecast vs the 2055 actual is informative.</p>'
            '</article>'
        )
        warns = chk.qsanity_scan(body, 2026)
        self.assertEqual(len([w for w in warns if "2055" in w]), 1)

    def test_clean_article_no_warnings(self):
        body = (
            '<article class="ara-doc">'
            '<p>Revenue was $5.55 billion in Q4 2026, with 75% gross margin.</p>'
            '</article>'
        )
        warns = chk.qsanity_scan(body, 2026)
        self.assertEqual(warns, [])

    def test_nbis_class_pattern_revenue_per_employee(self):
        """Documents that the original NBIS-class failure (e.g.
        '1000 employees, $5T revenue' = $5B per employee, implausible)
        is NOT caught by v1's pattern set. This is intentional — the
        revenue/employee pairing pattern requires reliable proximity
        matching which has high false-positive rates on early-stage
        SaaS. Documented in PR body and the --qsanity CLI help.

        If a future iteration wants to add this pattern, build it
        with a tight (<80 char) proximity window and start warn-only.
        """
        body = (
            '<article class="ara-doc">'
            '<p>NBIS had $5T revenue with 1000 employees.</p>'
            '</article>'
        )
        warns = chk.qsanity_scan(body, 2026)
        # This pattern is documented as out-of-scope for v1.
        # When/if added, update this test.
        self.assertEqual(warns, [])


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
