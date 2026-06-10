#!/usr/bin/env python3

import json
import unittest
from datetime import datetime, timedelta, timezone

import check_deploy_health as cdh

NOW = datetime(2026, 6, 10, 12, 0, 0, tzinfo=timezone.utc)
URL = "https://ara.example.test/research/manifest.json"

FULL_HEADERS = {
    "content-type": "application/json",
    "cf-cache-status": "DYNAMIC",
    "age": "0",
}


def _manifest_body(generated_at=None, *, omit_stamp=False, git_sha="abc1234"):
    body = {"today": [], "twitter": [], "models": [], "frontpage": [], "audio": [], "generative": []}
    if not omit_stamp:
        body["generatedAt"] = generated_at
        body["gitSha"] = git_sha
    return json.dumps(body)


def _result(body, status=200, headers=None):
    return cdh.FetchResult(
        status=status,
        headers=dict(FULL_HEADERS if headers is None else headers),
        body=body,
    )


def _iso_hours_ago(hours):
    return (NOW - timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def _epoch_hours_ago(hours):
    return int((NOW - timedelta(hours=hours)).timestamp())


def _evaluate(fetch_fn, git_time_fn=lambda: _epoch_hours_ago(0.5), **kwargs):
    return cdh.evaluate(
        url=URL,
        max_lag_hours=8.0,
        repo_alive_hours=2.0,
        now=NOW,
        fetch_fn=fetch_fn,
        git_time_fn=git_time_fn,
        **kwargs,
    )


class EvaluateTest(unittest.TestCase):
    def test_healthy_small_lag(self):
        # Built 1h ago, repo pushing — the steady state.
        health = _evaluate(lambda url: _result(_manifest_body(_iso_hours_ago(1.0))))
        self.assertEqual(health.state, cdh.HEALTHY)
        self.assertFalse(health.alerting)
        self.assertAlmostEqual(health.lag_hours, 1.0, places=2)

    def test_deploy_stale_big_lag_repo_alive(self):
        # THE incident shape: pushes flow (repo idle 0.5h) but the live build
        # is 26h old — Railway builds are failing on every push.
        health = _evaluate(
            lambda url: _result(_manifest_body(_iso_hours_ago(26.0))),
            git_time_fn=lambda: _epoch_hours_ago(0.5),
        )
        self.assertEqual(health.state, cdh.DEPLOY_STALE)
        self.assertTrue(health.alerting)
        self.assertAlmostEqual(health.lag_hours, 26.0, places=2)
        self.assertAlmostEqual(health.repo_idle_hours, 0.5, places=2)
        self.assertIn("deploy", health.detail)

    def test_big_lag_repo_idle_defers_to_lane_freshness(self):
        # Pipeline froze 10h ago: lag is big BUT the repo is idle too —
        # lane-freshness owns that page; we must not double-page.
        health = _evaluate(
            lambda url: _result(_manifest_body(_iso_hours_ago(26.0))),
            git_time_fn=lambda: _epoch_hours_ago(10.0),
        )
        self.assertEqual(health.state, cdh.PIPELINE_IDLE)
        self.assertFalse(health.alerting)
        self.assertIn("lane-freshness", health.detail)

    def test_missing_generated_at_is_legacy_build(self):
        # The live build predates the stamping feature: note, never a page.
        health = _evaluate(lambda url: _result(_manifest_body(omit_stamp=True)))
        self.assertEqual(health.state, cdh.LEGACY_BUILD)
        self.assertFalse(health.alerting)

    def test_fetch_failure_is_site_unreachable(self):
        def boom(url):
            raise cdh.FetchError("fetch failed after 2 attempt(s): connection refused")

        health = _evaluate(boom)
        self.assertEqual(health.state, cdh.SITE_UNREACHABLE)
        self.assertTrue(health.alerting)
        self.assertIn("connection refused", health.detail)

    def test_unexpected_fetch_exception_is_site_unreachable(self):
        # The fetch seam is a network boundary: ANY exception out of it must
        # classify, not crash the watchdog.
        def boom(url):
            raise RuntimeError("totally unexpected")

        health = _evaluate(boom)
        self.assertEqual(health.state, cdh.SITE_UNREACHABLE)
        self.assertTrue(health.alerting)

    def test_non_200_is_site_unreachable(self):
        health = _evaluate(lambda url: _result("oops", status=503))
        self.assertEqual(health.state, cdh.SITE_UNREACHABLE)
        self.assertTrue(health.alerting)
        self.assertIn("503", health.detail)

    def test_html_body_is_manifest_unparseable(self):
        # Observed live: the Caddy SPA fallback serves index.html with HTTP
        # 200 for a missing path — JSON parsing fails, and that means the
        # deployed artifact users need is gone.
        health = _evaluate(
            lambda url: _result(
                "<!doctype html>\n<html>...</html>",
                headers={"content-type": "text/html; charset=utf-8"},
            )
        )
        self.assertEqual(health.state, cdh.MANIFEST_UNPARSEABLE)
        self.assertTrue(health.alerting)
        self.assertIn("text/html", health.detail)

    def test_non_object_json_is_manifest_unparseable(self):
        health = _evaluate(lambda url: _result("[]"))
        self.assertEqual(health.state, cdh.MANIFEST_UNPARSEABLE)
        self.assertTrue(health.alerting)

    def test_garbage_generated_at_is_manifest_unparseable(self):
        health = _evaluate(lambda url: _result(_manifest_body("not-a-timestamp")))
        self.assertEqual(health.state, cdh.MANIFEST_UNPARSEABLE)
        self.assertTrue(health.alerting)

    def test_threshold_boundary_exactly_at_threshold_is_healthy(self):
        # lag must be STRICTLY greater than the threshold to be anomalous.
        health = _evaluate(lambda url: _result(_manifest_body(_iso_hours_ago(8.0))))
        self.assertEqual(health.state, cdh.HEALTHY)
        self.assertFalse(health.alerting)

    def test_threshold_boundary_just_over_flags(self):
        health = _evaluate(
            lambda url: _result(_manifest_body(_iso_hours_ago(8.01))),
            git_time_fn=lambda: _epoch_hours_ago(0.1),
        )
        self.assertEqual(health.state, cdh.DEPLOY_STALE)
        self.assertTrue(health.alerting)

    def test_repo_alive_boundary_exactly_two_hours_defers(self):
        # repo_idle must be STRICTLY under repo_alive_hours to page.
        health = _evaluate(
            lambda url: _result(_manifest_body(_iso_hours_ago(26.0))),
            git_time_fn=lambda: _epoch_hours_ago(2.0),
        )
        self.assertEqual(health.state, cdh.PIPELINE_IDLE)
        self.assertFalse(health.alerting)

    def test_git_time_unavailable_still_flags_with_caveat(self):
        # Outside the wired environment (no checkout) we cannot apply the
        # deferral; surface the real lag rather than swallowing it.
        health = _evaluate(
            lambda url: _result(_manifest_body(_iso_hours_ago(26.0))),
            git_time_fn=lambda: None,
        )
        self.assertEqual(health.state, cdh.DEPLOY_STALE)
        self.assertTrue(health.alerting)
        self.assertIn("UNKNOWN", health.detail)

    def test_future_generated_at_is_healthy_clock_skew(self):
        health = _evaluate(lambda url: _result(_manifest_body(_iso_hours_ago(-0.5))))
        self.assertEqual(health.state, cdh.HEALTHY)
        self.assertFalse(health.alerting)
        self.assertIn("future", health.detail)

    def test_absent_cache_headers_do_not_crash(self):
        # The contract: diagnostics must tolerate cf-cache-status/age absence
        # (origin reads outside Cloudflare, or header changes).
        health = _evaluate(
            lambda url: _result(
                _manifest_body(_iso_hours_ago(1.0)),
                headers={"content-type": "application/json"},
            )
        )
        self.assertEqual(health.state, cdh.HEALTHY)
        self.assertIsNone(health.cache_status)
        self.assertIsNone(health.age)
        report = cdh.format_report(health)
        self.assertIn("cf-cache-status=absent", report)
        self.assertIn("age=absent", report)

    def test_cache_hit_despite_buster_is_warned(self):
        health = _evaluate(
            lambda url: _result(
                _manifest_body(_iso_hours_ago(1.0)),
                headers={"cf-cache-status": "HIT", "age": "5400"},
            )
        )
        report = cdh.format_report(health)
        self.assertIn("cf-cache-status=HIT", report)
        self.assertIn("WARNING", report)


class FetchManifestTest(unittest.TestCase):
    class _FakeResponse:
        def __init__(self, body=b"{}", status=200, headers=None):
            self._body = body
            self.status = status
            self.headers = headers or {"Content-Type": "application/json"}

        def read(self, n=-1):
            return self._body

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    def test_cache_buster_appended(self):
        seen = {}

        def opener(request, timeout):
            seen["url"] = request.full_url
            seen["timeout"] = timeout
            return self._FakeResponse()

        result = cdh.fetch_manifest(
            URL, timeout=7.0, opener_fn=opener, sleep_fn=lambda s: None,
            epoch_fn=lambda: 1781000000,
        )
        self.assertEqual(result.status, 200)
        self.assertEqual(seen["url"], URL + "?cb=1781000000")
        self.assertEqual(seen["timeout"], 7.0)

    def test_cache_buster_respects_existing_query(self):
        self.assertEqual(
            cdh.with_cache_buster("https://x.test/m.json?a=1", 42),
            "https://x.test/m.json?a=1&cb=42",
        )

    def test_retry_succeeds_on_second_attempt(self):
        calls = {"n": 0}
        sleeps = []

        def opener(request, timeout):
            calls["n"] += 1
            if calls["n"] == 1:
                raise OSError("connection reset")
            return self._FakeResponse(body=b'{"ok": true}')

        result = cdh.fetch_manifest(
            URL, retries=1, opener_fn=opener, sleep_fn=sleeps.append,
            epoch_fn=lambda: 1,
        )
        self.assertEqual(calls["n"], 2)
        self.assertEqual(sleeps, [cdh.RETRY_DELAY_SECONDS])
        self.assertEqual(result.body, '{"ok": true}')

    def test_retries_exhausted_raises_fetch_error(self):
        def opener(request, timeout):
            raise OSError("no route to host")

        with self.assertRaises(cdh.FetchError) as ctx:
            cdh.fetch_manifest(
                URL, retries=1, opener_fn=opener, sleep_fn=lambda s: None,
                epoch_fn=lambda: 1,
            )
        self.assertIn("2 attempt(s)", str(ctx.exception))
        self.assertIn("no route to host", str(ctx.exception))

    def test_header_keys_lowercased(self):
        def opener(request, timeout):
            return self._FakeResponse(
                headers={"CF-Cache-Status": "DYNAMIC", "Age": "3"},
            )

        result = cdh.fetch_manifest(URL, opener_fn=opener, sleep_fn=lambda s: None, epoch_fn=lambda: 1)
        self.assertEqual(result.headers.get("cf-cache-status"), "DYNAMIC")
        self.assertEqual(result.headers.get("age"), "3")


class HelpersTest(unittest.TestCase):
    def test_idempotency_key_format(self):
        self.assertEqual(
            cdh.idempotency_key(cdh.DEPLOY_STALE, NOW),
            "deploy-health-2026-06-10-deploy-stale",
        )
        self.assertEqual(
            cdh.idempotency_key(cdh.HEALTHY, NOW),
            "deploy-health-2026-06-10-healthy",
        )

    def test_parse_iso8601_variants(self):
        # toISOString() shape (trailing Z + millis) must parse on Python <3.11.
        parsed = cdh.parse_iso8601("2026-06-10T01:28:50.123Z")
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed.tzinfo, timezone.utc)
        # Naive timestamps are assumed UTC.
        naive = cdh.parse_iso8601("2026-06-10T01:28:50")
        self.assertIsNotNone(naive.tzinfo)
        # Garbage and non-strings are None, not exceptions.
        self.assertIsNone(cdh.parse_iso8601("yesterday-ish"))
        self.assertIsNone(cdh.parse_iso8601(""))
        self.assertIsNone(cdh.parse_iso8601(None))

    def test_alerting_states_are_exactly_the_page_worthy_set(self):
        self.assertEqual(
            cdh.ALERTING_STATES,
            {cdh.DEPLOY_STALE, cdh.SITE_UNREACHABLE, cdh.MANIFEST_UNPARSEABLE},
        )
        for state in (cdh.HEALTHY, cdh.LEGACY_BUILD, cdh.PIPELINE_IDLE):
            self.assertNotIn(state, cdh.ALERTING_STATES)


if __name__ == "__main__":
    unittest.main()
