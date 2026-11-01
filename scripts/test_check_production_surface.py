#!/usr/bin/env python3

import contextlib
import io
import json
import os
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

import yaml

import check_production_surface as cps

ROOT = Path(__file__).resolve().parent.parent


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
        self.assertTrue({"aradio", "aradio-trailing-slash", "aradio-feed"} <= names)
        self.assertTrue({"manifest", "robots", "sitemap", "feed", "llms", "real-404"} <= names)
        self.assertTrue({"malformed-today-404", "missing-asset-404"} <= names)
        self.assertTrue({"evidence-search-contract", "public-claims-contract"} <= names)
        self.assertTrue({"ua-googlebot", "ua-perplexity", "ua-claudebot-policy", "ua-gptbot-policy", "ua-ccbot-policy"} <= names)


NOW = datetime(2026, 10, 31, 4, 17, tzinfo=timezone.utc)
ROUTE = cps.Probe("aradio", "/aradio", content_type_prefix="text/html", body_contains="<title>ARA AI News")
NOT_DEPLOYED = cps.Response(404, {"content-type": "text/html"}, "Not Found")
DEPLOYED = cps.Response(200, {"content-type": "text/html"}, "<title>ARA AI News -- ara</title>")
BROKEN = cps.Response(500, {"content-type": "text/html"}, "boom")
HOME_OK = cps.Response(
    200,
    {"content-type": "text/html", "x-content-type-options": "nosniff",
     "cache-control": "public, max-age=0, must-revalidate"},
    "<title>ARA</title>",
)


class DeployRaceTest(unittest.TestCase):
    """A just-merged probe may run before Railway deploys its route."""

    def setUp(self):
        self.clock = 0.0
        self.sleeps = []

    def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.clock += seconds

    def settle(self, answers, committed_at, probe=ROUTE, eligible=None, home=HOME_OK):
        """Initial pass plus settle for `probe` beside the home-page canary.

        `answers` are served to `probe` in order, the last one repeating.
        """
        queue = list(answers)

        def fetch(target, base_url, timeout):
            if target == cps.HOME_PROBE:
                return home
            answer = queue.pop(0) if len(queue) > 1 else queue[0]
            if isinstance(answer, Exception):
                raise answer
            return answer

        probes = [cps.HOME_PROBE, probe]
        results = cps.evaluate(probes, "https://example.test", fetch_fn=fetch)
        self.assertEqual(home is not HOME_OK, results[0].failed)
        with contextlib.redirect_stderr(io.StringIO()):
            return cps.settle_deploy_race(
                probes, results, "https://example.test", 1.0, committed_at, NOW,
                eligible=[probe] if eligible is None else eligible,
                fetch_fn=fetch, sleep_fn=self.sleep, clock=lambda: self.clock,
            )[1]

    def test_new_route_passes_once_the_deploy_lands(self):
        result = self.settle([NOT_DEPLOYED, NOT_DEPLOYED, NOT_DEPLOYED, DEPLOYED],
                             NOW - timedelta(minutes=10))
        self.assertFalse(result.failed)
        self.assertEqual([60.0, 60.0, 60.0], self.sleeps)
        self.assertIn("after 180s of deploy-race retry", result.detail)

    def test_persistent_404_fails_after_a_bounded_wait(self):
        result = self.settle([NOT_DEPLOYED], NOW - timedelta(minutes=5))
        self.assertTrue(result.failed)
        self.assertEqual(404, result.status)
        self.assertEqual(15, len(self.sleeps))
        self.assertLessEqual(sum(self.sleeps), cps.DEPLOY_RACE_RETRY_BUDGET_SECONDS)
        self.assertIn("still failing after 900s", result.detail)

    def test_404_pages_at_once_when_the_probe_code_is_older_than_the_window(self):
        result = self.settle([NOT_DEPLOYED, DEPLOYED], NOW - timedelta(minutes=31))
        self.assertTrue(result.failed)
        self.assertEqual([], self.sleeps)

    def test_other_failures_never_wait(self):
        recent = NOW - timedelta(minutes=2)
        wrong_marker = cps.Response(200, {"content-type": "text/html"}, "<title>ARA</title>")
        for name, answer in (("5xx", BROKEN), ("fetch error", TimeoutError("boom")),
                             ("marker", wrong_marker)):
            with self.subTest(name):
                self.sleeps = []
                result = self.settle([answer, DEPLOYED], recent)
                self.assertTrue(result.failed)
                self.assertEqual([], self.sleeps)

    def test_a_site_whose_home_page_fails_is_down_not_mid_deploy(self):
        for home in (NOT_DEPLOYED, BROKEN):
            with self.subTest(home=home.status):
                result = self.settle([NOT_DEPLOYED, DEPLOYED], NOW - timedelta(minutes=2), home=home)
                self.assertTrue(result.failed)
                self.assertEqual([], self.sleeps)

    def test_a_deployed_route_that_breaks_stops_waiting(self):
        # Not a 404 any more: the image has the route, so the failure is real.
        result = self.settle([NOT_DEPLOYED, BROKEN, DEPLOYED], NOW - timedelta(minutes=2))
        self.assertTrue(result.failed)
        self.assertEqual(500, result.status)
        self.assertEqual([60.0], self.sleeps)

    def test_expected_404_and_user_agent_probes_never_wait(self):
        recent = NOW - timedelta(minutes=2)
        missing = cps.Probe("real-404", "/__missing__", expected_status=404)
        self.assertTrue(self.settle([DEPLOYED, NOT_DEPLOYED], recent, probe=missing).failed)
        googlebot = next(p for p in cps.USER_AGENT_PROBES if p.name == "ua-googlebot")
        # Default eligibility is the route table: zone policy is never a deploy.
        self.assertTrue(self.settle([NOT_DEPLOYED, DEPLOYED], recent, probe=googlebot,
                                    eligible=cps.ROUTE_PROBES).failed)
        self.assertEqual([], self.sleeps)
        self.assertNotIn(googlebot, set(cps.ROUTE_PROBES))

    def test_missing_unparseable_naive_or_future_timestamps_disable_the_retry(self):
        for value in ("", "   ", "not-a-date", "2026-10-31T04:10:00",
                      (NOW + timedelta(minutes=10)).isoformat()):
            with self.subTest(value=value):
                self.sleeps = []
                result = self.settle([NOT_DEPLOYED, DEPLOYED], cps.parse_committed_at(value))
                self.assertTrue(result.failed)
                self.assertEqual([], self.sleeps)
        # Within the clock-skew slack a future stamp still counts as fresh.
        self.assertFalse(self.settle([NOT_DEPLOYED, DEPLOYED], NOW + timedelta(minutes=2)).failed)

    def test_git_committer_dates_parse_with_any_offset(self):
        expected = datetime(2026, 10, 31, 3, 56, 13, tzinfo=timezone.utc)
        self.assertEqual(expected, cps.parse_committed_at("2026-10-31T12:56:13+09:00"))
        self.assertEqual(expected, cps.parse_committed_at("2026-10-31T03:56:13Z"))

    def test_main_passes_the_parsed_commit_time(self):
        failed = [cps.Result("aradio", "/aradio", "failed", "HTTP 404, expected 200", 404)]
        # CI sets both: keep this fixture's red report out of the test job's outputs.
        with mock.patch.dict(os.environ, {"GITHUB_OUTPUT": "", "GITHUB_STEP_SUMMARY": ""}), \
                mock.patch.object(cps, "evaluate", return_value=failed), \
                mock.patch.object(cps, "settle_deploy_race", return_value=failed) as settle, \
                contextlib.redirect_stdout(io.StringIO()):
            code = cps.main(["--exit-code", "--probe-code-committed-at", "2026-10-31T12:56:13+09:00"])
        self.assertEqual(2, code)
        args = settle.call_args.args
        self.assertEqual(cps.DEFAULT_PROBES, args[0])
        self.assertEqual(datetime(2026, 10, 31, 3, 56, 13, tzinfo=timezone.utc), args[4])

    def test_workflow_gives_the_probe_real_history(self):
        action = yaml.safe_load((ROOT / ".github/actions/production-surface-alert/action.yml").read_text())
        check = next(step for step in action["runs"]["steps"] if step.get("id") == "check")
        self.assertIn("--probe-code-committed-at", check["run"])
        self.assertIn("git log -1 --format=%cI -- scripts/check_production_surface.py", check["run"])
        self.assertIn("--is-shallow-repository", check["run"])
        self.assertTrue(check.get("continue-on-error"))
        workflow = yaml.safe_load((ROOT / ".github/workflows/production-synthetic.yml").read_text())
        job = workflow["jobs"]["probe"]
        checkout = next(step for step in job["steps"]
                        if str(step.get("uses", "")).startswith("actions/checkout@"))
        self.assertEqual(0, checkout["with"]["fetch-depth"])
        self.assertEqual("blob:none", checkout["with"]["filter"])
        self.assertGreater(job["timeout-minutes"] * 60, cps.DEPLOY_RACE_RETRY_BUDGET_SECONDS)


if __name__ == "__main__":
    unittest.main()
