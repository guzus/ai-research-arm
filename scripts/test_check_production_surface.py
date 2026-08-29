#!/usr/bin/env python3

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


class EvaluateTest(unittest.TestCase):
    def test_fetch_exception_is_a_failed_result(self):
        def explode(probe, base_url, timeout):
            raise TimeoutError("boom")

        results = cps.evaluate([cps.Probe("home", "/")], "https://example.test", fetch_fn=explode)
        self.assertEqual(results[0].state, "failed")
        self.assertIn("TimeoutError", results[0].detail)

    def test_default_matrix_covers_routes_discovery_404_and_user_agents(self):
        names = {probe.name for probe in cps.DEFAULT_PROBES}
        self.assertTrue({"home", "today", "twitter", "models", "research", "wiki"} <= names)
        self.assertTrue({"manifest", "robots", "sitemap", "feed", "llms", "real-404"} <= names)
        self.assertTrue({"ua-googlebot", "ua-perplexity", "ua-claudebot-policy", "ua-gptbot-policy", "ua-ccbot-policy"} <= names)


if __name__ == "__main__":
    unittest.main()
