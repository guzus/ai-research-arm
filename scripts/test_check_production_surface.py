#!/usr/bin/env python3

import json
import unittest

import check_production_surface as cps


class ResponseEvaluationTest(unittest.TestCase):
    def test_healthy_html_contract(self):
        probe = cps.Probe(
            "home", "/", content_type_prefix="text/html", body_contains="<title",
            required_headers=(("x-content-type-options", "nosniff"),),
        )
        response = cps.Response(200, {"content-type": "text/html; charset=utf-8", "x-content-type-options": "nosniff"}, "<title>ARA</title>")
        self.assertFalse(cps.evaluate_response(probe, response).failed)

    def test_wrong_status_fails_before_body_checks(self):
        probe = cps.Probe("home", "/", expected_status=200, body_contains="ok")
        result = cps.evaluate_response(probe, cps.Response(403, {}, "ok"))
        self.assertTrue(result.failed)
        self.assertIn("expected 200", result.detail)

    def test_content_type_marker_and_header_failures_are_visible(self):
        cases = [
            (cps.Probe("json", "/x", content_type_prefix="application/json"), cps.Response(200, {"content-type": "text/html"}, "{}"), "content-type"),
            (cps.Probe("marker", "/x", body_contains="generatedAt"), cps.Response(200, {}, "{}"), "marker"),
            (cps.Probe("header", "/x", required_headers=(("cache-control", "max-age=0"),)), cps.Response(200, {"cache-control": "max-age=60"}, ""), "header"),
        ]
        for probe, response, marker in cases:
            with self.subTest(probe=probe.name):
                result = cps.evaluate_response(probe, response)
                self.assertTrue(result.failed)
                self.assertIn(marker, result.detail)

    def test_403_is_a_healthy_explicit_policy(self):
        probe = cps.Probe("blocked", "/", expected_status=403)
        self.assertFalse(cps.evaluate_response(probe, cps.Response(403, {}, "blocked")).failed)

    def test_evidence_contract_requires_boolean_reusable_on_claim_entries(self):
        probe = cps.Probe("evidence", "/evidence.json", json_contract="evidence-search-v1")
        good = {"entries": [
            {"type": "research"},
            {"type": "claim", "id": "a#c1", "title": "A", "body": "Claim", "url": "/research/a", "reusable": False, "reuse_block": "Reverify live"},
        ]}
        self.assertFalse(cps.evaluate_response(probe, cps.Response(200, {}, json.dumps(good))).failed)

        bad = {"entries": [{"type": "claim", "id": "a#c1", "title": "A", "body": "Claim", "url": "/research/a"}]}
        result = cps.evaluate_response(probe, cps.Response(200, {}, json.dumps(bad)))
        self.assertTrue(result.failed)
        self.assertIn("$.entries[0].reusable", result.detail)

    def test_public_claim_contract_reports_exact_index_and_key(self):
        probe = cps.Probe("claims", "/claims.json", json_contract="public-claims-v1")
        good = {"claims": [{"article": "a", "claim": "Evidence", "reusable": True}]}
        self.assertFalse(cps.evaluate_response(probe, cps.Response(200, {}, json.dumps(good))).failed)

        bad = {"claims": [{"article": "a", "claim": "Evidence", "reusable": "yes"}]}
        result = cps.evaluate_response(probe, cps.Response(200, {}, json.dumps(bad)))
        self.assertTrue(result.failed)
        self.assertIn("$.claims[0].reusable", result.detail)

    def test_claim_contracts_reject_empty_collections_and_missing_reuse_reason(self):
        evidence = cps.Probe("evidence", "/evidence.json", json_contract="evidence-search-v1")
        result = cps.evaluate_response(evidence, cps.Response(200, {}, '{"entries":[]}'))
        self.assertIn("at least one claim entry", result.detail)
        no_claims = '{"entries":[{"type":"research"}]}'
        self.assertIn(
            "at least one claim entry",
            cps.evaluate_response(evidence, cps.Response(200, {}, no_claims)).detail,
        )
        missing_reason = {
            "entries": [{
                "type": "claim", "id": "a#c1", "title": "A", "body": "Claim",
                "url": "/research/a", "reusable": False, "reuse_block": "",
            }]
        }
        self.assertIn(
            "$.entries[0].reuse_block",
            cps.evaluate_response(evidence, cps.Response(200, {}, json.dumps(missing_reason))).detail,
        )

        claims = cps.Probe("claims", "/claims.json", json_contract="public-claims-v1")
        self.assertIn(
            "at least one claim",
            cps.evaluate_response(claims, cps.Response(200, {}, '{"claims":[]}')).detail,
        )
        public_missing_reason = {
            "claims": [{"article": "a", "claim": "Claim", "reusable": False}]
        }
        self.assertIn(
            "$.claims[0].reuse_block",
            cps.evaluate_response(claims, cps.Response(200, {}, json.dumps(public_missing_reason))).detail,
        )

    def test_json_contract_rejects_spa_html_and_wrong_array_key(self):
        probe = cps.Probe("evidence", "/evidence.json", json_contract="evidence-search-v1")
        invalid = cps.evaluate_response(probe, cps.Response(200, {}, "<html>app</html>"))
        self.assertIn("not valid JSON", invalid.detail)
        wrong = cps.evaluate_response(probe, cps.Response(200, {}, '{"claims":[]}'))
        self.assertIn("$.entries is missing", wrong.detail)

    def test_truncated_semantic_payload_fails_explicitly(self):
        probe = cps.Probe("evidence", "/evidence.json", json_contract="evidence-search-v1")
        result = cps.evaluate_response(probe, cps.Response(200, {}, '{"entries":[]}', True))
        self.assertTrue(result.failed)
        self.assertIn("exceeds semantic-check limit", result.detail)


class EvaluateTest(unittest.TestCase):
    def test_fetch_exception_is_a_failed_result(self):
        def explode(probe, base_url, timeout):
            raise TimeoutError("boom")

        results = cps.evaluate([cps.Probe("home", "/")], "https://example.test", fetch_fn=explode)
        self.assertEqual(results[0].state, "failed")
        self.assertIn("TimeoutError", results[0].detail)

    def test_default_matrix_covers_routes_discovery_404_and_user_agents(self):
        names = {probe.name for probe in cps.DEFAULT_PROBES}
        self.assertTrue({"home", "today", "today-kst-current", "twitter", "models", "research", "wiki", "pricing", "pricing-trailing-slash"} <= names)
        self.assertTrue({"manifest", "robots", "sitemap", "feed", "llms", "real-404"} <= names)
        self.assertTrue({"malformed-today-404", "missing-asset-404"} <= names)
        self.assertTrue({"evidence-search-contract", "public-claims-contract"} <= names)
        self.assertTrue({"ua-googlebot", "ua-perplexity", "ua-claudebot-policy", "ua-gptbot-policy", "ua-ccbot-policy"} <= names)


if __name__ == "__main__":
    unittest.main()
