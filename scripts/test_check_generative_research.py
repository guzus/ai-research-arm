#!/usr/bin/env python3
"""Unit tests for the research-quality gates added to
scripts/check_generative_research.py.

These tests cover the heuristics themselves (not the validate_body
plumbing — that has its own tests in test_ara_dsl.py). For each gate
we assert behavior on a hand-built synthetic article plus a sanity
check against a known-good article in research/generative/."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
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

    def test_quoted_claim_with_verifier_framing_fails(self):
        """Regression: anthropic-vs-the-pentagon (2026-07-04), claim
        c23. The ledger wrapped the quote in attribution framing
        ("CFR\u2019s Kat Duffy poses: \u2018...\u2019") with curly glyphs and a
        Unicode-ellipsis elision; the body renders the same quote with
        different framing and different quote glyphs. The old 80-char
        prefix probe never matched → the unsupported quote shipped."""
        import tempfile
        body = (
            '<article class="ara-doc">'
            "<p>The more durable finding may be about who else is exposed. "
            "CFR\u2019s Kat Duffy, in a separate interview, turned the "
            "designation into an open question for the rest of the "
            "industry: \u201cwill we also be declared supply chain risks? "
            "\u2026 Google, OpenAI and Anthropic have all been\u201d on the "
            "receiving end of some version of this pressure"
            '<sup><a class="ara-cite" href="#ref-44">44</a></sup>.</p>'
            "</article>"
        )
        with tempfile.TemporaryDirectory() as tmp:
            findings = self._write_findings(Path(tmp), [{
                "id": "c23",
                "text": (
                    "CFR\u2019s Kat Duffy poses: \u2018will we also be declared "
                    "supply chain risks?\u2026 Google, OpenAI and Anthropic "
                    "have all\u2019"
                ),
                "verdict": "unsupported",
                "citation": None,
            }])
            total, surviving = chk.audit_verifier_findings(findings, body)
            self.assertEqual(total, 1)
            self.assertEqual(
                len(surviving), 1,
                "Verbatim quote survived in the body behind ledger "
                "framing — the probe set must catch it (old prefix "
                "probe false-passed exactly this shape).",
            )
            self.assertEqual(surviving[0]["id"], "c23")

    def test_entity_encoded_body_still_caught(self):
        """Reviewer-confirmed bypass: ~10% of committed articles render
        typographic glyphs as HTML entities (&rsquo; &ldquo; &hellip;
        &mdash;) in visible text. Folding literal Unicode alone lets an
        entity-encoded body ghost an unsupported claim through — the
        audit must unescape before folding."""
        import tempfile
        body = (
            '<article class="ara-doc">'
            "<p>CFR&rsquo;s Kat Duffy, in a separate interview, asked:"
            " &ldquo;will we also be declared supply chain risks?"
            " &hellip; Google, OpenAI and Anthropic have all"
            " been&rdquo; &mdash; on the record.</p>"
            "</article>"
        )
        with tempfile.TemporaryDirectory() as tmp:
            findings = self._write_findings(Path(tmp), [{
                "id": "c23",
                "text": (
                    "CFR\u2019s Kat Duffy poses: \u2018will we also be declared "
                    "supply chain risks?\u2026 Google, OpenAI and Anthropic "
                    "have all\u2019"
                ),
                "verdict": "unsupported",
                "citation": None,
            }])
            total, surviving = chk.audit_verifier_findings(findings, body)
            self.assertEqual(total, 1)
            self.assertEqual(
                len(surviving), 1,
                "Entity-encoded body must not evade the probe set.",
            )

    def test_paraphrased_revision_still_passes(self):
        """The documented paraphrase-on-revision escape must survive
        the probe-set tightening: a genuine rewrite shares no 5-word
        segment or 8-word shingle with the ledger text."""
        import tempfile
        body = (
            '<article class="ara-doc">'
            "<p>Duffy has separately argued that other AI vendors could "
            "face comparable designations in future disputes.</p>"
            "</article>"
        )
        with tempfile.TemporaryDirectory() as tmp:
            findings = self._write_findings(Path(tmp), [{
                "id": "c23",
                "text": (
                    "CFR\u2019s Kat Duffy poses: \u2018will we also be declared "
                    "supply chain risks?\u2026 Google, OpenAI and Anthropic "
                    "have all\u2019"
                ),
                "verdict": "unsupported",
                "citation": None,
            }])
            total, surviving = chk.audit_verifier_findings(findings, body)
            self.assertEqual(total, 1)
            self.assertEqual(surviving, [])

    def test_demoted_quote_with_typography_variants_passes(self):
        """A quote demoted inside <mark> must pass even when the body
        uses curly glyphs and the ledger uses ASCII ones — the folding
        has to apply to the mark regions too."""
        import tempfile
        body = (
            '<article class="ara-doc">'
            '<p><mark class="ara-mark">\u201cwill we also be declared supply '
            "chain risks? \u2026 Google, OpenAI and Anthropic have all "
            "been\u201d</mark></p>"
            "</article>"
        )
        with tempfile.TemporaryDirectory() as tmp:
            findings = self._write_findings(Path(tmp), [{
                "id": "c1",
                "text": (
                    "'will we also be declared supply chain risks?... "
                    "Google, OpenAI and Anthropic have all been'"
                ),
                "verdict": "unsupported",
                "citation": None,
            }])
            total, surviving = chk.audit_verifier_findings(findings, body)
            self.assertEqual(total, 1)
            self.assertEqual(surviving, [])

    def test_short_verbatim_fragment_survival_fails(self):
        """A 5+ word verbatim run inside a framed claim is enough to
        flag survival via the segment probe."""
        import tempfile
        body = (
            '<article class="ara-doc">'
            "<p>Analysts note the surge pricing doubles peak output rates "
            "for all API tiers.</p></article>"
        )
        with tempfile.TemporaryDirectory() as tmp:
            findings = self._write_findings(Path(tmp), [{
                "id": "c9",
                "text": (
                    "Per one report: \u2018surge pricing doubles peak output "
                    "rates\u2019 \u2026 (unconfirmed)"
                ),
                "verdict": "unsupported",
                "citation": None,
            }])
            total, surviving = chk.audit_verifier_findings(findings, body)
            self.assertEqual(total, 1)
            self.assertEqual(len(surviving), 1)

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

    def test_donut_summing_over_100_warns_compiled_shape(self):
        """The actual compiler output for :::donut is
            <div class="ara-donut" data-labels="A,B,C" data-values="80,50,45">
        not a <ul>/<li> shape. Codex review caught the original
        implementation matching only the wrong shape — now we test
        against what the compiler actually emits, by compiling DSL
        through the real compiler instead of hand-rolling HTML."""
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from compile_ara import compile_source
        src = (
            "---\n"
            "title: T\n"
            "---\n"
            "\n"
            "## 1. Test\n"
            "\n"
            ":::donut\n"
            "- label: A\n"
            "  value: 80\n"
            "- label: B\n"
            "  value: 50\n"
            "- label: C\n"
            "  value: 45\n"
            ":::\n"
        )
        body = compile_source(src)
        # Confirm compiler shape — div with data-values, not ul/li
        self.assertIn('<div class="ara-donut"', body)
        self.assertIn('data-values="80,50,45"', body)
        # And the qsanity scan flags the over-100 sum
        warns = chk.qsanity_scan(body, 2026)
        donut_warns = [w for w in warns if "donut" in w.lower()]
        self.assertEqual(len(donut_warns), 1, f"got: {donut_warns}")
        self.assertIn("175", donut_warns[0])

    def test_donut_summing_under_limit_silent_compiled_shape(self):
        """Compiled donut summing to 100% is silent."""
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from compile_ara import compile_source
        src = (
            "---\ntitle: T\n---\n\n## 1. Test\n\n"
            ":::donut\n"
            "- label: A\n  value: 40\n"
            "- label: B\n  value: 35\n"
            "- label: C\n  value: 25\n"
            ":::\n"
        )
        body = compile_source(src)
        warns = chk.qsanity_scan(body, 2026)
        self.assertEqual([w for w in warns if "donut" in w.lower()], [])

    def test_donut_rounding_tolerance_compiled_shape(self):
        """Sum of 103% is within the 105% tolerance."""
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from compile_ara import compile_source
        src = (
            "---\ntitle: T\n---\n\n## 1. Test\n\n"
            ":::donut\n"
            "- label: A\n  value: 34\n"
            "- label: B\n  value: 35\n"
            "- label: C\n  value: 34\n"
            ":::\n"
        )
        body = compile_source(src)
        warns = chk.qsanity_scan(body, 2026)
        self.assertEqual([w for w in warns if "donut" in w.lower()], [])

    def test_donut_legacy_ul_shape_still_supported(self):
        """The pre-fix <ul>/<li data-pct> shape is also matched, in
        case anyone hand-rolled a donut via :::raw."""
        body = (
            '<article class="ara-doc">'
            '<ul class="ara-donut" data-title="x">'
            '<li data-pct="80">A</li>'
            '<li data-pct="50">B</li>'
            '<li data-pct="45">C</li>'
            '</ul></article>'
        )
        warns = chk.qsanity_scan(body, 2026)
        donut_warns = [w for w in warns if "donut" in w.lower()]
        self.assertEqual(len(donut_warns), 1)
        self.assertIn("175", donut_warns[0])

    def test_donut_legacy_ul_under_limit_silent(self):
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


class MethodologyArtifactValidationTest(unittest.TestCase):
    def _write_json(self, payload):
        tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        with tmp:
            json.dump(payload, tmp)
        return Path(tmp.name)

    def tearDown(self):
        for attr in ("path",):
            p = getattr(self, attr, None)
            if p and p.exists():
                p.unlink()

    def test_valid_claim_ledger_passes(self):
        self.path = self._write_json({
            "claims": [{
                "id": "c1",
                "claim": "Omni listed 450 live perpetual markets as of the review date.",
                "type": "metric",
                "source_urls": ["https://docs.example.com/markets"],
                "source_tiers": ["primary"],
                "as_of": "2026-05-21",
                "confidence": "high",
                "risk": "volatile",
            }]
        })
        self.assertEqual(chk.validate_claim_ledger(self.path), [])

    def test_metric_claim_requires_as_of(self):
        self.path = self._write_json({
            "claims": [{
                "id": "c1",
                "claim": "Omni listed 450 live perpetual markets.",
                "type": "metric",
                "source_urls": ["https://docs.example.com/markets"],
                "source_tiers": ["primary"],
                "as_of": "",
                "confidence": "high",
                "risk": "volatile",
            }]
        })
        errs = chk.validate_claim_ledger(self.path)
        self.assertTrue(any("as_of" in e for e in errs))

    def test_redteam_placeholder_fails(self):
        self.path = self._write_json({
            "findings": [
                {
                    "claim_id": "c1",
                    "claim_text": "This placeholder indicates the red-team pass failed.",
                    "contradicting_url": None,
                    "contradicting_quote": None,
                    "severity": None,
                    "no_contradiction_found": False,
                    "redteam_failed": True,
                },
                {
                    "claim_id": "c2",
                    "claim_text": "This placeholder indicates the red-team pass failed.",
                    "contradicting_url": None,
                    "contradicting_quote": None,
                    "severity": None,
                    "no_contradiction_found": False,
                    "redteam_failed": True,
                },
                {
                    "claim_id": "c3",
                    "claim_text": "This placeholder indicates the red-team pass failed.",
                    "contradicting_url": None,
                    "contradicting_quote": None,
                    "severity": None,
                    "no_contradiction_found": False,
                    "redteam_failed": True,
                },
            ]
        })
        errs = chk.validate_redteam_artifact(self.path)
        self.assertTrue(any("redteam_failed=true" in e for e in errs))

    def test_empty_verifier_claims_fail(self):
        self.path = self._write_json({"claims": []})
        errs = chk.validate_verifier_artifact(self.path)
        self.assertTrue(any("non-empty claims" in e for e in errs))


# ---------------------------------------------------------------------------
# Derived-claim recompute audit (--audit-derived-claims).
# ---------------------------------------------------------------------------


def _retrieval_claim(cid, claim=None, url="https://example.gov/x"):
    """A normal (non-derived) ledger claim — the thing a derived claim's
    inputs point at."""
    return {
        "id": cid,
        "claim": claim or f"Retrieval claim {cid} with enough text to be real.",
        "type": "metric",
        "source_urls": [url],
        "source_tiers": ["primary"],
        "as_of": "2026-08-01",
        "confidence": "high",
        "risk": "volatile",
    }


def _derived_claim(cid="d1", **overrides):
    """The canonical derived claim from the contract: 30 GW * $60B/GW =
    $1.8T. Override any field to make a single rule fail in isolation."""
    entry = {
        "id": cid,
        "type": "derived",
        "claim": (
            "At 30 GW of CY28 additions and $60B per GW, hyperscale+neocloud "
            "capex is about $1.8T."
        ),
        "inputs": [
            {"ref": "c3", "name": "gigawatts", "value": 30, "unit": "GW"},
            {"ref": "c7", "name": "cost_per_gw", "value": 60e9, "unit": "USD/GW"},
        ],
        "formula": "gigawatts * cost_per_gw",
        "result": 1800000000000,
        "unit": "USD",
        "assumptions": [
            "Midpoint of the 25-35 GW consensus range",
            "$60B/GW blended build cost",
        ],
        "as_of": "2026-08-01",
        "confidence": "high",
        "risk": "stable",
    }
    entry.update(overrides)
    return entry


class DerivedClaimAuditTest(unittest.TestCase):
    """Each test isolates ONE of R1-R7 so a regression names its rule.

    The premise: a derived claim carries no source URL by construction,
    so retrieval verification is structurally impossible for it. This
    audit substitutes recomputation — inputs must resolve inside the
    ledger and the arithmetic must reproduce."""

    def setUp(self):
        self._paths = []

    def tearDown(self):
        for p in self._paths:
            if p.exists():
                p.unlink()

    def _ledger(self, claims):
        tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        with tmp:
            json.dump({"claims": claims}, tmp)
        p = Path(tmp.name)
        self._paths.append(p)
        return p

    def _audit(self, claims, **kwargs):
        return chk.audit_derived_claims(self._ledger(claims), **kwargs)

    # -- identity: a derived entry must never be able to disappear -------
    #
    # Both of these were live one-key bypasses of the ENTIRE gate: the
    # audit indexed the ledger by id and then built its work list from
    # that index, so an entry with no id was never indexed and the
    # second entry sharing an id was dropped by first-id-wins. The CLI
    # reported "0 derived claim(s)" and exited 0 on a ledger whose
    # arithmetic was off by five orders of magnitude. The rest of this
    # class cannot catch them, because its helper hard-codes cid="d1".

    def test_derived_entry_without_an_id_is_audited_not_skipped(self):
        entry = _derived_claim(result=999_000_000_000_000)
        del entry["id"]
        total, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"), entry,
        ])
        self.assertEqual(total, 1, "an id-less derived entry must still be counted")
        rules = {p["rule"] for p in problems}
        self.assertIn("R1", rules, "the missing id must itself be a failure")
        self.assertIn("R5", rules, "the wrong arithmetic must still be caught")
        self.assertTrue(all(p["id"] for p in problems), "every problem needs a label")

    def test_duplicate_id_cannot_hide_a_derived_entry(self):
        total, problems = self._audit([
            _retrieval_claim("d1"),  # shadows the derived entry below
            _derived_claim(result=999_000_000_000_000),
            _retrieval_claim("c3"), _retrieval_claim("c7"),
        ])
        self.assertEqual(total, 1)
        rules = {p["rule"] for p in problems}
        self.assertIn("R1", rules, "the duplicated id must itself be a failure")
        self.assertIn("R5", rules, "the wrong arithmetic must still be caught")

    def test_every_derived_entry_is_audited_when_ids_repeat(self):
        """Two derived entries sharing an id: BOTH get recomputed."""
        total, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(result=111),
            _derived_claim(result=222),
        ])
        self.assertEqual(total, 2)
        self.assertEqual(
            len([p for p in problems if p["rule"] == "R5"]), 2,
            "first-id-wins must not silence the second entry's arithmetic",
        )

    def _rules(self, problems):
        return sorted({p["rule"] for p in problems})

    # ---- happy paths ----------------------------------------------------

    def test_valid_derived_claim_passes(self):
        total, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"), _derived_claim(),
        ])
        self.assertEqual(total, 1)
        self.assertEqual(problems, [], f"unexpected: {problems}")

    def test_ledger_without_derived_claims_passes_trivially(self):
        """Derived claims are optional; an all-retrieval ledger is a
        pass, not a "you forgot to derive anything" failure."""
        total, problems = self._audit([_retrieval_claim("c1"), _retrieval_claim("c2")])
        self.assertEqual(total, 0)
        self.assertEqual(problems, [])

    def test_derived_claim_may_reference_another_derived_claim(self):
        """R7 explicitly permits derived-on-derived; only cycles and
        over-deep chains fail."""
        total, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"), _derived_claim(),
            _derived_claim(
                cid="d2",
                inputs=[
                    {"ref": "d1", "name": "capex", "value": 1.8e12, "unit": "USD"},
                    {"ref": "c3", "name": "years", "value": 3, "unit": "years"},
                ],
                formula="capex / years",
                result=6e11,
            ),
        ])
        self.assertEqual(total, 2)
        self.assertEqual(problems, [], f"unexpected: {problems}")

    # ---- R1: inputs shape ----------------------------------------------

    def test_r1_missing_inputs_fails(self):
        _, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(inputs=[]),
        ])
        self.assertIn("R1", self._rules(problems))
        self.assertTrue(any("non-empty array" in p["message"] for p in problems))

    def test_r1_input_missing_unit_fails(self):
        _, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(inputs=[
                {"ref": "c3", "name": "gigawatts", "value": 30, "unit": ""},
                {"ref": "c7", "name": "cost_per_gw", "value": 60e9, "unit": "USD/GW"},
            ]),
        ])
        self.assertTrue(
            any(p["rule"] == "R1" and "unit" in p["message"] for p in problems),
            f"got: {problems}",
        )

    def test_r1_non_numeric_value_fails(self):
        _, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(inputs=[
                {"ref": "c3", "name": "gigawatts", "value": "30", "unit": "GW"},
                {"ref": "c7", "name": "cost_per_gw", "value": 60e9, "unit": "USD/GW"},
            ]),
        ])
        self.assertTrue(
            any(p["rule"] == "R1" and "finite number" in p["message"] for p in problems),
            f"got: {problems}",
        )

    def test_r1_boolean_value_is_not_a_number(self):
        """`True` is an int in Python; accepting it would silently
        evaluate a schema error as the number 1."""
        _, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(inputs=[
                {"ref": "c3", "name": "gigawatts", "value": True, "unit": "GW"},
                {"ref": "c7", "name": "cost_per_gw", "value": 60e9, "unit": "USD/GW"},
            ]),
        ])
        self.assertTrue(
            any(p["rule"] == "R1" and "finite number" in p["message"] for p in problems),
            f"got: {problems}",
        )

    def test_r1_non_identifier_name_reported_as_such(self):
        """"cost per gw" can never appear as an AST Name, so the error
        must say so rather than surfacing as a confusing R4 mismatch."""
        _, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(inputs=[
                {"ref": "c3", "name": "gigawatts", "value": 30, "unit": "GW"},
                {"ref": "c7", "name": "cost per gw", "value": 60e9, "unit": "USD/GW"},
            ]),
        ])
        self.assertTrue(
            any("not a valid identifier" in p["message"] for p in problems),
            f"got: {problems}",
        )

    def test_r1_duplicate_input_names_fail(self):
        _, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(inputs=[
                {"ref": "c3", "name": "gigawatts", "value": 30, "unit": "GW"},
                {"ref": "c7", "name": "gigawatts", "value": 60e9, "unit": "USD/GW"},
            ]),
        ])
        self.assertTrue(
            any("duplicates input name" in p["message"] for p in problems),
            f"got: {problems}",
        )

    def test_r1_untyped_arithmetic_claim_is_flagged(self):
        """A claim carrying `formula`/`inputs` but typed something else
        would skip this audit while still reading as arithmetic. Closes
        the accidental version of that bypass (the deliberate version —
        omitting the claim entirely — is out of reach, see the module
        docstring)."""
        _, problems = self._audit([
            _retrieval_claim("c3"),
            dict(_retrieval_claim("c9"), formula="a * b"),
        ])
        self.assertTrue(
            any("must be typed 'derived'" in p["message"] for p in problems),
            f"got: {problems}",
        )

    # ---- R2: ref resolution ---------------------------------------------

    def test_r2_dangling_ref_fails(self):
        _, problems = self._audit([
            _retrieval_claim("c3"),
            _derived_claim(),  # references c7, which is absent
        ])
        self.assertTrue(
            any(p["rule"] == "R2" and "c7" in p["message"] for p in problems),
            f"got: {problems}",
        )

    def test_r2_ambiguous_duplicate_id_ref_fails(self):
        _, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _retrieval_claim("c7", claim="A second claim reusing the id c7."),
            _derived_claim(),
        ])
        self.assertTrue(
            any(p["rule"] == "R2" and "ambiguous" in p["message"] for p in problems),
            f"got: {problems}",
        )

    # ---- R3: formula AST whitelist --------------------------------------

    def test_r3_call_node_rejected(self):
        """The formula is LLM-authored. A Call node is the whole reason
        this uses an AST walk instead of eval()."""
        _, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(formula="__import__('os').system('id')"),
        ])
        self.assertTrue(
            any(p["rule"] == "R3" and "Call" in p["message"] for p in problems),
            f"got: {problems}",
        )

    def test_r3_attribute_and_subscript_rejected(self):
        for formula in ("gigawatts.real * cost_per_gw", "gigawatts[0] * cost_per_gw"):
            with self.subTest(formula=formula):
                _, problems = self._audit([
                    _retrieval_claim("c3"), _retrieval_claim("c7"),
                    _derived_claim(formula=formula),
                ])
                self.assertIn("R3", self._rules(problems))

    def test_r3_comparison_rejected(self):
        _, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(formula="gigawatts > cost_per_gw"),
        ])
        self.assertIn("R3", self._rules(problems))

    def test_r3_syntax_error_rejected(self):
        _, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(formula="gigawatts *"),
        ])
        self.assertTrue(
            any(p["rule"] == "R3" and "does not parse" in p["message"] for p in problems),
            f"got: {problems}",
        )

    def test_r3_string_literal_rejected(self):
        _, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(formula="gigawatts * cost_per_gw * 'x'"),
        ])
        self.assertIn("R3", self._rules(problems))

    def test_parse_formula_accepts_full_operator_set(self):
        """Direct check on the helper: the allowed operators all parse
        and the name set comes back."""
        tree, names = chk._parse_formula("-(a + b) * c / d % e ** 2")
        self.assertEqual(names, {"a", "b", "c", "d", "e"})
        self.assertEqual(
            chk._eval_formula(tree, {"a": 1.0, "b": 1.0, "c": 8.0, "d": 2.0, "e": 3.0}),
            -(1 + 1) * 8 / 2 % 3 ** 2,
        )

    # ---- R4: name binding ------------------------------------------------

    def test_r4_unbound_name_in_formula_fails(self):
        _, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(formula="gigawatts * cost_per_gw * utilization"),
        ])
        self.assertTrue(
            any(p["rule"] == "R4" and "utilization" in p["message"] for p in problems),
            f"got: {problems}",
        )

    def test_r4_declared_but_unused_input_fails(self):
        _, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(formula="gigawatts * 60000000000", result=1800000000000),
        ])
        self.assertTrue(
            any(p["rule"] == "R4" and "cost_per_gw" in p["message"] for p in problems),
            f"got: {problems}",
        )

    # ---- R5: recomputation ----------------------------------------------

    def test_r5_arithmetic_mismatch_fails(self):
        """The core value of the gate: a stated result that the stated
        inputs do not produce."""
        _, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(result=18000000000000),  # 10x too big
        ])
        self.assertTrue(
            any(p["rule"] == "R5" and "mismatch" in p["message"] for p in problems),
            f"got: {problems}",
        )

    def test_r5_within_tolerance_passes(self):
        """Rounded headline figures are fine: computed 1.8e12 vs a
        declared 1.81e12 is 0.55% off, inside the 1% default."""
        _, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(result=1.81e12),
        ])
        self.assertEqual(problems, [], f"unexpected: {problems}")

    def test_r5_tolerance_boundary(self):
        """Boundary is checked with the SAME symmetric formula the code
        uses: |c-d| / max(|c|,|d|). computed = 100.
          declared 101   -> 1/101   = 0.990% -> inside 1%
          declared 102   -> 2/102   = 1.961% -> outside 1%
        """
        base = [
            _retrieval_claim("c3"), _retrieval_claim("c7"),
        ]
        inside = _derived_claim(
            inputs=[
                {"ref": "c3", "name": "a", "value": 10, "unit": "u"},
                {"ref": "c7", "name": "b", "value": 10, "unit": "u"},
            ],
            formula="a * b", result=101,
        )
        _, problems = self._audit(base + [inside])
        self.assertEqual(problems, [], f"101 should be inside 1%: {problems}")

        outside = dict(inside, result=102)
        _, problems = self._audit(base + [outside])
        self.assertTrue(
            any(p["rule"] == "R5" for p in problems),
            f"102 should be outside 1%: {problems}",
        )

    def test_r5_tolerance_is_configurable(self):
        _, problems = self._audit(
            [
                _retrieval_claim("c3"), _retrieval_claim("c7"),
                _derived_claim(result=1.9e12),  # 5.3% off
            ],
            tolerance=0.10,
        )
        self.assertEqual(problems, [], f"unexpected at tolerance=0.10: {problems}")

    def test_r5_division_by_zero_is_a_rejection_not_a_crash(self):
        _, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(
                inputs=[
                    {"ref": "c3", "name": "num", "value": 30, "unit": "GW"},
                    {"ref": "c7", "name": "den", "value": 0, "unit": "GW"},
                ],
                formula="num / den", result=0,
            ),
        ])
        self.assertTrue(
            any(p["rule"] == "R5" and "zero" in p["message"] for p in problems),
            f"got: {problems}",
        )

    def test_r5_compute_bomb_exponent_rejected(self):
        """`9**9**9` is three allowlisted nodes and would hang the
        runner. The exponent cap catches it because evaluation is
        inner-first: 9**9 = 387420489 > 64."""
        _, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(
                inputs=[{"ref": "c3", "name": "base", "value": 9, "unit": "x"}],
                formula="base ** 9 ** 9", result=1,
            ),
        ])
        self.assertTrue(
            any(p["rule"] == "R5" and "exponent" in p["message"] for p in problems),
            f"got: {problems}",
        )

    def test_r5_overflow_to_infinity_rejected(self):
        """Float multiplication overflows to inf SILENTLY in Python, so
        a finite-check on every intermediate is load-bearing."""
        _, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(
                inputs=[
                    {"ref": "c3", "name": "a", "value": 1e308, "unit": "x"},
                    {"ref": "c7", "name": "b", "value": 1e10, "unit": "x"},
                ],
                formula="a * b", result=1e318,
            ),
        ])
        self.assertTrue(
            any(p["rule"] == "R5" for p in problems), f"got: {problems}",
        )

    def test_r5_non_numeric_result_fails(self):
        _, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(result="about $1.8T"),
        ])
        self.assertTrue(
            any(p["rule"] == "R5" and "finite number" in p["message"] for p in problems),
            f"got: {problems}",
        )

    # ---- R6: assumptions + unit -----------------------------------------

    def test_r6_empty_assumptions_fails(self):
        _, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(assumptions=[]),
        ])
        self.assertTrue(
            any(p["rule"] == "R6" and "assumptions" in p["message"] for p in problems),
            f"got: {problems}",
        )

    def test_r6_blank_assumption_string_fails(self):
        _, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(assumptions=["   "]),
        ])
        self.assertTrue(
            any(p["rule"] == "R6" for p in problems), f"got: {problems}",
        )

    def test_r6_missing_unit_fails(self):
        _, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(unit=""),
        ])
        self.assertTrue(
            any(p["rule"] == "R6" and "unit" in p["message"] for p in problems),
            f"got: {problems}",
        )

    # ---- R7: cycles, depth, unsupported propagation ----------------------

    def test_r7_two_node_cycle_detected(self):
        d1 = _derived_claim(
            cid="d1",
            inputs=[
                {"ref": "c3", "name": "a", "value": 2, "unit": "u"},
                {"ref": "d2", "name": "b", "value": 3, "unit": "u"},
            ],
            formula="a * b", result=6,
        )
        d2 = _derived_claim(
            cid="d2",
            inputs=[
                {"ref": "c3", "name": "a", "value": 2, "unit": "u"},
                {"ref": "d1", "name": "b", "value": 3, "unit": "u"},
            ],
            formula="a * b", result=6,
        )
        _, problems = self._audit([_retrieval_claim("c3"), d1, d2])
        self.assertTrue(
            any(p["rule"] == "R7" and "cycle" in p["message"] for p in problems),
            f"got: {problems}",
        )

    def test_r7_self_reference_detected(self):
        _, problems = self._audit([
            _retrieval_claim("c3"),
            _derived_claim(
                cid="d1",
                inputs=[
                    {"ref": "c3", "name": "a", "value": 2, "unit": "u"},
                    {"ref": "d1", "name": "b", "value": 3, "unit": "u"},
                ],
                formula="a * b", result=6,
            ),
        ])
        self.assertTrue(
            any(p["rule"] == "R7" and "cycle" in p["message"] for p in problems),
            f"got: {problems}",
        )

    def test_r7_depth_cap_enforced(self):
        """A chain d1->d2->...->d7 exceeds the 5-edge cap."""
        claims = [_retrieval_claim("c3")]
        for i in range(1, 8):
            nxt = f"d{i + 1}"
            inputs = [{"ref": "c3", "name": "a", "value": 2, "unit": "u"}]
            if i < 7:
                inputs.append({"ref": nxt, "name": "b", "value": 3, "unit": "u"})
                formula, result = "a * b", 6
            else:
                formula, result = "a", 2
            claims.append(_derived_claim(
                cid=f"d{i}", inputs=inputs, formula=formula, result=result,
            ))
        _, problems = self._audit(claims)
        self.assertTrue(
            any(p["rule"] == "R7" and "deep" in p["message"] for p in problems),
            f"got: {problems}",
        )

    def _chain(self, n_derived):
        """d1 -> d2 -> ... -> dN, i.e. N-1 derived-to-derived edges."""
        claims = [_retrieval_claim("c3")]
        for i in range(1, n_derived + 1):
            inputs = [{"ref": "c3", "name": "a", "value": 2, "unit": "u"}]
            if i < n_derived:
                inputs.append(
                    {"ref": f"d{i + 1}", "name": "b", "value": 3, "unit": "u"}
                )
                formula, result = "a * b", 6
            else:
                formula, result = "a", 2
            claims.append(_derived_claim(
                cid=f"d{i}", inputs=inputs, formula=formula, result=result,
            ))
        return claims

    def test_r7_depth_boundary_is_exactly_max_depth_edges(self):
        """Pins the cap: 5 edges pass, 6 fail (default max_depth=5)."""
        _, ok = self._audit(self._chain(6))     # 5 edges
        self.assertEqual(ok, [], f"5 edges should pass: {ok}")
        _, bad = self._audit(self._chain(7))    # 6 edges
        self.assertTrue(
            any(p["rule"] == "R7" and "deep" in p["message"] for p in bad),
            f"6 edges should fail: {bad}",
        )

    def test_r1_unit_error_does_not_suppress_the_recompute_check(self):
        """A bad `unit` must not hide an arithmetic error behind it —
        the author would fix the unit, re-run, and only THEN discover
        the number was wrong."""
        _, problems = self._audit([
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(
                inputs=[
                    {"ref": "c3", "name": "gigawatts", "value": 30, "unit": ""},
                    {"ref": "c7", "name": "cost_per_gw", "value": 60e9,
                     "unit": "USD/GW"},
                ],
                result=42,
            ),
        ])
        rules = self._rules(problems)
        self.assertIn("R1", rules)
        self.assertIn("R5", rules)

    def test_r7_shallow_chain_within_cap_passes(self):
        claims = [_retrieval_claim("c3")]
        for i in (1, 2):
            inputs = [{"ref": "c3", "name": "a", "value": 2, "unit": "u"}]
            if i == 1:
                inputs.append({"ref": "d2", "name": "b", "value": 3, "unit": "u"})
                formula, result = "a * b", 6
            else:
                formula, result = "a", 2
            claims.append(_derived_claim(
                cid=f"d{i}", inputs=inputs, formula=formula, result=result,
            ))
        _, problems = self._audit(claims)
        self.assertEqual(problems, [], f"unexpected: {problems}")

    def test_r7_dense_graph_hits_the_traversal_budget(self):
        """A degenerate derived-on-derived ledger must fail closed in
        bounded time, not pin the runner. 24 derived claims each
        referencing the next 8 blows past the step budget."""
        width = 8
        n = 24
        claims = [_retrieval_claim("c3")]
        for i in range(1, n + 1):
            inputs = [{"ref": "c3", "name": "a", "value": 2, "unit": "u"}]
            for k in range(1, width + 1):
                j = i + k
                if j <= n:
                    inputs.append(
                        {"ref": f"d{j}", "name": f"b{k}", "value": 1, "unit": "u"}
                    )
            formula = " * ".join(inp["name"] for inp in inputs)
            claims.append(_derived_claim(
                cid=f"d{i}", inputs=inputs, formula=formula, result=2,
            ))
        _, problems = self._audit(claims)
        self.assertTrue(
            any("traversal-step budget" in p["message"] for p in problems),
            f"expected a budget failure, got rules {self._rules(problems)}",
        )

    def test_r7_unsupported_input_taints_derived_claim(self):
        _, problems = self._audit(
            [_retrieval_claim("c3"), _retrieval_claim("c7"), _derived_claim()],
            unsupported_ids={"c7"},
        )
        self.assertTrue(
            any(p["rule"] == "R7" and "unsupported" in p["message"] for p in problems),
            f"got: {problems}",
        )

    def test_r7_unsupported_taint_is_transitive(self):
        """d2 depends on d1 depends on c3; c3 unsupported taints both."""
        d1 = _derived_claim(
            cid="d1",
            inputs=[{"ref": "c3", "name": "a", "value": 2, "unit": "u"}],
            formula="a", result=2,
        )
        d2 = _derived_claim(
            cid="d2",
            inputs=[{"ref": "d1", "name": "b", "value": 2, "unit": "u"}],
            formula="b", result=2,
        )
        _, problems = self._audit(
            [_retrieval_claim("c3"), d1, d2], unsupported_ids={"c3"},
        )
        tainted = {p["id"] for p in problems if p["rule"] == "R7"}
        self.assertEqual(tainted, {"d1", "d2"}, f"got: {problems}")

    def test_r7_derived_claims_own_unsupported_verdict_is_ignored(self):
        """The verifier is EXPECTED to mark a derived sentence
        unsupported — it has no source URL, which is the whole gap this
        audit closes. Tainting a derived claim with its own verdict
        would fail every derived claim as soon as both flags are passed,
        i.e. exactly the case the feature exists for. R7 looks at
        INPUTS only."""
        _, problems = self._audit(
            [_retrieval_claim("c3"), _retrieval_claim("c7"), _derived_claim()],
            unsupported_ids={"d1"},
        )
        self.assertEqual(problems, [], f"unexpected: {problems}")

    def test_r7_no_verifier_ids_means_no_taint_check(self):
        """Documents the hole: without verifier findings, a derived
        claim resting on rejected inputs passes silently."""
        _, problems = self._audit(
            [_retrieval_claim("c3"), _retrieval_claim("c7"), _derived_claim()],
        )
        self.assertEqual(problems, [])

    # ---- artifact-level errors -------------------------------------------

    def test_malformed_json_raises(self):
        tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        with tmp:
            tmp.write("{not json")
        p = Path(tmp.name)
        self._paths.append(p)
        with self.assertRaises(ValueError):
            chk.audit_derived_claims(p)

    def test_missing_claims_array_raises(self):
        tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        with tmp:
            json.dump({"notclaims": []}, tmp)
        p = Path(tmp.name)
        self._paths.append(p)
        with self.assertRaises(ValueError):
            chk.audit_derived_claims(p)

    def test_unsupported_claim_ids_is_lenient(self):
        """A missing/malformed verifier artifact must NOT raise here —
        --audit-verifier-findings owns that error and its exit code."""
        self.assertEqual(chk.unsupported_claim_ids(Path("/nonexistent/x.json")), set())
        tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        with tmp:
            tmp.write("{broken")
        p = Path(tmp.name)
        self._paths.append(p)
        self.assertEqual(chk.unsupported_claim_ids(p), set())

    def test_unsupported_claim_ids_extracts_only_unsupported(self):
        tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        with tmp:
            json.dump({"claims": [
                {"id": "c1", "verdict": "supported"},
                {"id": "c2", "verdict": "unsupported"},
                {"id": "c3", "verdict": "weak"},
                {"id": "c4", "verdict": "UNSUPPORTED"},
            ]}, tmp)
        p = Path(tmp.name)
        self._paths.append(p)
        self.assertEqual(chk.unsupported_claim_ids(p), {"c2", "c4"})


class DerivedClaimCliTest(unittest.TestCase):
    """CLI wiring: --audit-derived-claims must mirror
    --audit-verifier-findings' exit-code contract (2 = missing file,
    1 = malformed or failing, 0 = clean) and must not disturb the
    verifier audit when both flags are passed."""

    def setUp(self):
        self._paths = []
        body = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False)
        with body:
            body.write(
                '<article class="ara-doc"><h2>T</h2>'
                "<p>Body text for the audit-mode CLI tests.</p></article>"
            )
        self.body_path = Path(body.name)
        self._paths.append(self.body_path)

    def tearDown(self):
        for p in self._paths:
            if p.exists():
                p.unlink()

    def _json_file(self, payload, suffix=".json"):
        tmp = tempfile.NamedTemporaryFile("w", suffix=suffix, delete=False)
        with tmp:
            json.dump(payload, tmp)
        p = Path(tmp.name)
        self._paths.append(p)
        return p

    def test_missing_ledger_exits_2(self):
        rc = chk.main([
            str(self.body_path),
            "--audit-derived-claims", "/nonexistent/ledger.json",
        ])
        self.assertEqual(rc, 2)

    def test_clean_ledger_exits_0(self):
        ledger = self._json_file({"claims": [
            _retrieval_claim("c3"), _retrieval_claim("c7"), _derived_claim(),
        ]})
        rc = chk.main([str(self.body_path), "--audit-derived-claims", str(ledger)])
        self.assertEqual(rc, 0)

    def test_bad_arithmetic_exits_1(self):
        ledger = self._json_file({"claims": [
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(result=42),
        ]})
        rc = chk.main([str(self.body_path), "--audit-derived-claims", str(ledger)])
        self.assertEqual(rc, 1)

    def test_malformed_ledger_exits_1(self):
        bad = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        with bad:
            bad.write("{nope")
        p = Path(bad.name)
        self._paths.append(p)
        rc = chk.main([str(self.body_path), "--audit-derived-claims", str(p)])
        self.assertEqual(rc, 1)

    def test_tolerance_flag_is_wired(self):
        ledger = self._json_file({"claims": [
            _retrieval_claim("c3"), _retrieval_claim("c7"),
            _derived_claim(result=1.9e12),  # 5.3% off
        ]})
        self.assertEqual(
            chk.main([str(self.body_path), "--audit-derived-claims", str(ledger)]), 1
        )
        self.assertEqual(
            chk.main([
                str(self.body_path), "--audit-derived-claims", str(ledger),
                "--derived-tolerance", "0.10",
            ]),
            0,
        )

    def test_both_audits_compose_verifier_still_runs(self):
        """With both flags, a clean derived audit must fall through so
        the verifier audit still gets to fail the build."""
        ledger = self._json_file({"claims": [
            _retrieval_claim("c3"), _retrieval_claim("c7"), _derived_claim(),
        ]})
        findings = self._json_file({"claims": [{
            "id": "c1",
            "text": "Body text for the audit-mode CLI tests.",
            "verdict": "unsupported",
            "citation": None,
        }]})
        rc = chk.main([
            str(self.body_path),
            "--audit-derived-claims", str(ledger),
            "--audit-verifier-findings", str(findings),
        ])
        self.assertEqual(rc, 1, "surviving unsupported claim must still fail")

    def test_co_passed_claims_ledger_still_validated(self):
        """--audit-derived-claims takes the same file as --claims-ledger,
        so co-passing them is the natural wiring. A clean derived audit
        must NOT short-circuit the ledger-schema gate the caller also
        asked for.

        A `derived` entry is now LEGAL under
        generative_methodology.validate_claim_ledger (it was rejected
        three ways before that gate learned the type, which made this
        whole feature inert end-to-end). So the schema failure is
        injected independently — a retrieval claim with an invalid
        `type` — proving the schema gate really ran rather than being
        skipped by the derived audit's early return."""
        good = self._json_file({"claims": [
            _retrieval_claim("c3"), _retrieval_claim("c7"), _derived_claim(),
        ]})
        rc = chk.main([
            str(self.body_path),
            "--audit-derived-claims", str(good),
            "--claims-ledger", str(good),
        ])
        self.assertEqual(
            rc, 0,
            "a valid derived ledger must satisfy BOTH the recompute audit "
            "and the ledger schema gate",
        )

        broken = dict(_retrieval_claim("c7"))
        broken["type"] = "not-a-real-type"
        ledger = self._json_file({"claims": [
            _retrieval_claim("c3"), broken, _derived_claim(),
        ]})
        rc = chk.main([
            str(self.body_path),
            "--audit-derived-claims", str(ledger),
            "--claims-ledger", str(ledger),
        ])
        self.assertEqual(
            rc, 1,
            "co-passed --claims-ledger must still run and fail on the "
            "schema-invalid entry rather than being skipped",
        )

    def test_co_passed_valid_claims_ledger_composes(self):
        """Same wiring, ledger with no derived entries: both checks run
        and both pass, so the fall-through is not a blanket failure."""
        ledger = self._json_file({"claims": [_retrieval_claim("c3")]})
        rc = chk.main([
            str(self.body_path),
            "--audit-derived-claims", str(ledger),
            "--claims-ledger", str(ledger),
        ])
        self.assertEqual(rc, 0)

    def test_verifier_flag_alone_is_unchanged(self):
        """Regression guard: the pre-existing single-flag path must
        behave exactly as before."""
        findings = self._json_file({"claims": [{
            "id": "c1",
            "text": "A claim that no longer appears anywhere in the body.",
            "verdict": "unsupported",
            "citation": None,
        }]})
        rc = chk.main([
            str(self.body_path), "--audit-verifier-findings", str(findings),
        ])
        self.assertEqual(rc, 0)

    def test_unsupported_input_taint_via_both_flags(self):
        """R7's propagation only activates when the verifier findings
        are supplied alongside the ledger."""
        ledger = self._json_file({"claims": [
            _retrieval_claim("c3"), _retrieval_claim("c7"), _derived_claim(),
        ]})
        findings = self._json_file({"claims": [{
            "id": "c7",
            "text": "A claim that no longer appears anywhere in the body.",
            "verdict": "unsupported",
            "citation": None,
        }]})
        rc = chk.main([
            str(self.body_path),
            "--audit-derived-claims", str(ledger),
            "--audit-verifier-findings", str(findings),
        ])
        self.assertEqual(rc, 1)


# ---------------------------------------------------------------------------
# :::position exemption.
# ---------------------------------------------------------------------------

POSITION_BLOCK = (
    '<div class="ara-position ara-position--medium">'
    '<p class="ara-position-label">Analyst position — not a sourced claim</p>'
    '<p class="ara-position-stance">Hyperscaler credit spreads compress '
    'rather than widen through Q4 2026.</p>'
    '<div class="ara-position-row">'
    '<span class="ara-position-key">Consensus</span>'
    '<span class="ara-position-val">Sell-side models a Q3 operating '
    'cash-flow deceleration and assumes the capex funding gap is '
    'debt-financed.</span>'
    "</div>"
    '<div class="ara-position-row">'
    '<span class="ara-position-key">Resolves</span>'
    '<span class="ara-position-val">Q3 2026 hyperscaler 10-Q filings — '
    'combined OCF growth vs. the 31% Q1 2026 print.</span>'
    "</div>"
    '<p class="ara-position-meta">Confidence medium · Horizon 2026-Q4</p>'
    "</div>"
)


class PositionBlockExemptionTest(unittest.TestCase):
    """A `:::position` block is labelled analyst judgment ("Analyst
    position — not a sourced claim"). It is substantive by every
    heuristic in this file and uncited by design, so the uncited-claim
    gates must not see it — otherwise using the component correctly
    would fail the gate that makes the article publishable.

    Fail-open is the invariant that matters most: any parse weirdness
    must return the body UNCHANGED, never strip to end-of-document
    (which would delete every downstream cite marker and crater the
    density of an article that should pass)."""

    def _article(self, inner):
        return f'<article class="ara-doc"><h2>Sec</h2>{inner}</article>'

    def test_no_position_class_is_identity(self):
        body = self._article("<p>Nvidia posted $30B in Q4 2026 revenue.</p>")
        self.assertIs(chk.strip_position_blocks(body), body)

    def test_oversized_position_block_is_not_exempted(self):
        """REGRESSION: the exemption removed an unbounded, author-controlled
        region from cite_density()'s denominator, which made it a bypass of
        the live production gate `--cite-density-min 10`. Relocating uncited
        prose into a `:::position` block took a measured 7.94 (FAIL) to
        166.67 (PASS) using only the sanctioned directive and allowlisted
        classes. An oversized block is now exempted NOT AT ALL, so the
        relocation buys nothing."""
        prose = " ".join(
            ["Nvidia reported material capacity growth this quarter."] * 200
        )
        cites = "".join(
            f"<p>Cited sentence {i} about Nvidia Q4 2026."
            f'<sup><a class="ara-cite" href="#ref-{i}">{i}</a></sup></p>'
            for i in range(1, 11)
        )
        plain = self._article(f"<p>{prose}</p>{cites}")
        laundered = self._article(
            '<div class="ara-position ara-position--medium">'
            '<span class="ara-position-label">'
            "Analyst position - not a sourced claim</span>"
            f'<p class="ara-position-stance">{prose}</p></div>{cites}'
        )
        plain_density = chk.cite_density(plain)[0]
        laundered_density = chk.cite_density(laundered)[0]
        self.assertLess(plain_density, 10.0)
        self.assertLess(
            laundered_density, 10.0,
            "relocating uncited prose into a position block must not turn a "
            "failing cite density into a passing one",
        )
        # The oversized block is left wholly in place.
        self.assertIn("ara-position-stance", chk.strip_position_blocks(laundered))

    def test_normal_sized_position_block_is_still_exempted(self):
        """Control for the cap: the component must remain usable."""
        stripped = chk.strip_position_blocks(self._article(POSITION_BLOCK))
        self.assertNotIn("ara-position", stripped)

    def test_position_block_removed(self):
        body = self._article(f"<p>Before.</p>{POSITION_BLOCK}<p>After.</p>")
        out = chk.strip_position_blocks(body)
        self.assertNotIn("ara-position", out)
        self.assertIn("Before.", out)
        self.assertIn("After.", out)

    def test_nested_same_tag_does_not_end_region_early(self):
        """The block root is a <div> containing <div class="…-row">
        children. A non-greedy regex would stop at the first </div> and
        leave the stance rows behind."""
        out = chk.strip_position_blocks(
            self._article(f"{POSITION_BLOCK}<p>Tail sentence.</p>")
        )
        self.assertNotIn("ara-position-row", out)
        self.assertNotIn("Sell-side models", out)
        self.assertIn("Tail sentence.", out)

    def test_variant_class_alone_still_strips(self):
        body = self._article(
            '<div class="ara-position--high"><p>Stance only.</p></div><p>Tail.</p>'
        )
        out = chk.strip_position_blocks(body)
        self.assertNotIn("Stance only.", out)
        self.assertIn("Tail.", out)

    def test_inner_position_classes_alone_do_not_strip(self):
        """`ara-position-label` is NOT a block root. Substring matching
        would treat it as one and swallow the wrong region."""
        body = self._article(
            '<p class="ara-position-label">Analyst position</p>'
            "<p>Nvidia posted $30B in Q4 2026 revenue.</p>"
        )
        out = chk.strip_position_blocks(body)
        self.assertIn("Nvidia posted", out)
        self.assertIn("ara-position-label", out)

    def test_unclosed_block_fails_open(self):
        """Missing </div> must return the body untouched rather than
        deleting everything after the block."""
        body = (
            '<article class="ara-doc">'
            '<div class="ara-position"><p>Stance.</p>'
            '<p>Later text with a cite'
            '<sup><a class="ara-cite" href="#ref-1">1</a></sup>.</p>'
            "</article>"
        )
        self.assertIs(chk.strip_position_blocks(body), body)

    def test_self_closing_position_tag_removed(self):
        body = self._article('<p>A.</p><div class="ara-position"/><p>B.</p>')
        out = chk.strip_position_blocks(body)
        self.assertNotIn("ara-position", out)
        self.assertIn("A.", out)
        self.assertIn("B.", out)

    # ---- gate-level behaviour -------------------------------------------

    def test_cited_claim_share_ignores_position_text(self):
        cited = (
            "<p>Nvidia posted $30B in Q4 2026 revenue"
            '<sup><a class="ara-cite" href="#ref-1">1</a></sup>.</p>'
        )
        without = self._article(cited)
        with_pos = self._article(cited + POSITION_BLOCK)
        self.assertEqual(
            chk.cited_claim_share(with_pos), chk.cited_claim_share(without),
            "a :::position block must not enter the cited-claim denominator",
        )
        # And the position text WOULD have counted without the exemption:
        # the raw block segments into substantive uncited sentences.
        raw_share, _, raw_total = chk.cited_claim_share(
            self._article(cited).replace("</article>", "</article>")
        )
        naive_total = chk.cited_claim_share(
            self._article(cited + POSITION_BLOCK.replace("ara-position", "ara-kv"))
        )[2]
        self.assertGreater(
            naive_total, raw_total,
            "sanity: the same markup under a non-exempt class DOES inflate "
            "the denominator, so the exemption is doing real work",
        )

    def test_cite_density_excludes_position_words(self):
        cited = (
            "<p>Nvidia posted $30B in Q4 2026 revenue"
            '<sup><a class="ara-cite" href="#ref-1">1</a></sup>.</p>'
        )
        d_without = chk.cite_density(self._article(cited))
        d_with = chk.cite_density(self._article(cited + POSITION_BLOCK))
        self.assertEqual(d_with, d_without)
        # Same markup under a counted class dilutes density — proving the
        # exclusion is not a no-op.
        d_naive = chk.cite_density(
            self._article(cited + POSITION_BLOCK.replace("ara-position", "ara-kv"))
        )
        self.assertLess(d_naive[0], d_without[0])

    def test_corroboration_audit_ignores_position_claims(self):
        cited = (
            "<p>Nvidia posted $30B in Q4 2026 revenue"
            '<sup><a class="ara-cite" href="#ref-1">1</a></sup>'
            '<sup><a class="ara-cite" href="#ref-2">2</a></sup>.</p>'
        )
        refs = (
            '<ol class="ara-refs">'
            '<li id="ref-1"><a href="https://nvidia.com/a">a</a></li>'
            '<li id="ref-2"><a href="https://sec.gov/b">b</a></li>'
            '<li id="ref-3"><a href="https://example.com/c">c</a></li>'
            "</ol>"
        )
        # A position block that carries a cite of its own would otherwise
        # register as a single-host substantive claim and fail at N=2.
        pos = POSITION_BLOCK.replace(
            "</div>",
            '<p class="ara-position-meta">Spreads tighten 40bp by Q4 2026'
            '<sup><a class="ara-cite" href="#ref-3">3</a></sup>.</p></div>',
            1,
        )
        failing, total = chk.corroboration_audit(
            self._article(cited + pos + refs), 2
        )
        self.assertEqual(failing, [], f"got: {failing}")
        self.assertEqual(total, 1)

    def test_verifier_audit_is_not_exempt(self):
        """Deliberate non-exemption: parking a claim the verifier
        rejected inside a position block is not a demotion. `<mark>` is
        the demotion channel."""
        claim = "Nvidia will hold 90% of accelerator share through 2027."
        body = self._article(
            f'<div class="ara-position"><p class="ara-position-stance">'
            f"{claim}</p></div>"
        )
        tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        with tmp:
            json.dump({"claims": [{
                "id": "c1", "text": claim,
                "verdict": "unsupported", "citation": None,
            }]}, tmp)
        p = Path(tmp.name)
        try:
            total, surviving = chk.audit_verifier_findings(p, body)
            self.assertEqual(total, 1)
            self.assertEqual(
                len(surviving), 1,
                "an unsupported claim hidden in a position block must still "
                "count as surviving",
            )
        finally:
            p.unlink()

    def test_corpus_position_blocks_strip_without_touching_others(self):
        """Corpus evidence for both sides of the position-block contract."""
        corpus = sorted((REPO_ROOT / "research" / "generative").glob("*.html"))
        if not corpus:
            self.skipTest("no committed articles to check")
        stripped_count = 0
        for path in corpus:
            body = path.read_text(encoding="utf-8")
            output = chk.strip_position_blocks(body)
            with self.subTest(article=path.name):
                if "ara-position" not in body:
                    self.assertIs(
                        output,
                        body,
                        "stripper must preserve identity when no position exists",
                    )
                else:
                    stripped_count += 1
                    self.assertNotEqual(output, body)
                    self.assertNotIn("ara-position", output)
        self.assertGreater(stripped_count, 0, "fixture corpus needs a position block")


if __name__ == "__main__":
    unittest.main()
