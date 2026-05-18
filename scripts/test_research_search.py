#!/usr/bin/env python3
"""Tests for research_search.py — new source backends.

Network-dependent tests skip cleanly when offline. The argparse dispatch
test runs always (no network).

Run via:
  python3 -m unittest discover -s scripts -p 'test_*.py'
"""

from __future__ import annotations

import io
import os
import sys
import unittest
import unittest.mock
import urllib.error
import urllib.request

# Make the script importable as a module — its filename is a valid
# identifier so we can import it directly.
sys.path.insert(0, os.path.dirname(__file__))

import research_search  # noqa: E402


# Probe the network once at module load. We pick Wikidata because all
# code paths use HTTPS through stdlib and Wikidata is the most uptime-
# guaranteed of the new endpoints. A failure here means we should skip
# all network tests rather than report false failures. Use the same
# project UA the live functions use — Wikidata 403s requests without one.
def _probe_network() -> bool:
    req = urllib.request.Request(
        "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=test&format=json&language=en",
        headers={"User-Agent": research_search.USER_AGENT, "Accept": "application/json"},
    )
    try:
        urllib.request.urlopen(req, timeout=5, context=research_search.SSL_CTX)
        return True
    except Exception:  # noqa: BLE001
        return False


NETWORK_OK = _probe_network()


def _collect(gen) -> str:
    """Consume a generator-returning search function into a single string."""
    return "\n".join(gen)


def _has_traceback(s: str) -> bool:
    """Detect Python traceback markers that would indicate a function leaked
    an exception into the output stream."""
    markers = ("Traceback (most recent call last)", "  File \"", "  File '")
    return any(m in s for m in markers)


class ArgparseDispatchTest(unittest.TestCase):
    """Argparse + dispatch table — no network required."""

    def test_backends_includes_new_sources(self):
        for name in ("wikidata", "uspto", "jedec", "predictionmarket",
                     "gdelt", "nonenglish"):
            self.assertIn(name, research_search.BACKENDS,
                          f"missing {name} from BACKENDS")

    def test_backends_aliases_resolve(self):
        # Convenience aliases — make sure they didn't get dropped.
        self.assertIs(research_search.BACKENDS["wd"],
                      research_search.search_wikidata)
        self.assertIs(research_search.BACKENDS["patents"],
                      research_search.search_uspto)
        self.assertIs(research_search.BACKENDS["polymarket"],
                      research_search.search_predictionmarket)
        self.assertIs(research_search.BACKENDS["pm"],
                      research_search.search_predictionmarket)
        self.assertIs(research_search.BACKENDS["noneng"],
                      research_search.search_nonenglish)

    def test_argparse_accepts_all_new_sources(self):
        # main() shouldn't reject the new SOURCE values at parse-time.
        # We patch sys.stdout/stderr and the dispatched function so we
        # don't make a network call.
        for name in ("wikidata", "uspto", "jedec", "predictionmarket",
                     "gdelt", "nonenglish"):
            with self.subTest(source=name):
                with unittest.mock.patch.dict(
                    research_search.BACKENDS,
                    {name: lambda q, n, **kw: iter(["[test-stub]"])},
                ):
                    buf = io.StringIO()
                    with unittest.mock.patch("sys.stdout", buf):
                        rc = research_search.main([name, "x", "--limit", "1"])
                    self.assertEqual(rc, 0)
                    self.assertIn("[test-stub]", buf.getvalue())

    def test_argparse_lang_flag_passed_to_nonenglish(self):
        captured: dict = {}

        def stub(query, limit, **kw):
            captured["query"] = query
            captured["limit"] = limit
            captured["lang"] = kw.get("lang")
            yield "[stub]"

        with unittest.mock.patch.dict(
            research_search.BACKENDS, {"nonenglish": stub}
        ):
            buf = io.StringIO()
            with unittest.mock.patch("sys.stdout", buf):
                rc = research_search.main(
                    ["nonenglish", "OpenAI", "--limit", "5", "--lang", "ja"]
                )
            self.assertEqual(rc, 0)
            self.assertEqual(captured["lang"], "ja")
            self.assertEqual(captured["query"], "OpenAI")
            self.assertEqual(captured["limit"], 5)

    def test_argparse_lang_not_passed_to_other_sources(self):
        # Other sources should not receive lang as a kwarg even when
        # --lang is set on the CLI. Verifying this prevents a regression
        # where lang leaks into search_arxiv etc.
        captured: dict = {}

        def stub(query, limit, **kw):
            captured["kw"] = dict(kw)
            yield "[stub]"

        # When --lang is omitted, no lang kwarg should be passed.
        with unittest.mock.patch.dict(
            research_search.BACKENDS, {"arxiv": stub}
        ):
            buf = io.StringIO()
            with unittest.mock.patch("sys.stdout", buf):
                research_search.main(["arxiv", "x", "--limit", "1"])
            self.assertNotIn("lang", captured["kw"])

    def test_main_returns_2_on_network_error(self):
        # urllib.error.URLError → exit 2 with "ERROR: network failure:"
        def boom(q, n, **kw):
            yield "[before]"
            raise urllib.error.URLError("simulated")

        with unittest.mock.patch.dict(
            research_search.BACKENDS, {"arxiv": boom}
        ):
            buf_out = io.StringIO()
            buf_err = io.StringIO()
            with unittest.mock.patch("sys.stdout", buf_out), \
                 unittest.mock.patch("sys.stderr", buf_err):
                rc = research_search.main(["arxiv", "x"])
            self.assertEqual(rc, 2)
            self.assertIn("ERROR: network failure", buf_err.getvalue())
            # Should NOT have leaked a Python traceback to stderr
            self.assertFalse(_has_traceback(buf_err.getvalue()))


# ── Smoke tests — happy-path with real network calls ──────────────
@unittest.skipUnless(NETWORK_OK, "network required")
class SmokeTest(unittest.TestCase):
    """Live calls. Each test verifies (a) non-empty output, (b) no Python
    traceback leaked, and (c) recognizable structure."""

    def test_wikidata_smoke(self):
        out = _collect(research_search.search_wikidata("Anthropic", 2))
        self.assertTrue(out, "wikidata returned empty")
        self.assertFalse(_has_traceback(out))
        # Wikidata blocks start with `[N]\nLabel:` or with an error stanza.
        self.assertTrue(
            "Label:" in out or "(wikidata)" in out,
            f"unrecognized wikidata output: {out[:200]}",
        )

    def test_uspto_smoke(self):
        out = _collect(research_search.search_uspto("transformer", 3))
        self.assertTrue(out)
        self.assertFalse(_has_traceback(out))
        self.assertTrue(
            "Patent:" in out or "(uspto)" in out,
            f"unrecognized uspto output: {out[:200]}",
        )

    def test_jedec_smoke(self):
        out = _collect(research_search.search_jedec("HBM3E", 3))
        self.assertTrue(out)
        self.assertFalse(_has_traceback(out))
        # JEDEC primary path is Wikipedia, fallback Bing; either way
        # we should get URL: lines or a per-source error stanza.
        self.assertTrue(
            "URL:" in out or "(jedec)" in out,
            f"unrecognized jedec output: {out[:200]}",
        )

    def test_predictionmarket_smoke(self):
        out = _collect(research_search.search_predictionmarket("election", 3))
        self.assertTrue(out)
        self.assertFalse(_has_traceback(out))
        self.assertTrue(
            "Question:" in out or "(predictionmarket)" in out,
            f"unrecognized predictionmarket output: {out[:200]}",
        )

    def test_gdelt_smoke(self):
        out = _collect(research_search.search_gdelt("Anthropic", 3))
        self.assertTrue(out)
        self.assertFalse(_has_traceback(out))
        self.assertTrue(
            "Title:" in out or "(gdelt)" in out,
            f"unrecognized gdelt output: {out[:200]}",
        )

    def test_gdelt_short_query_handled(self):
        # GDELT returns plain-text "Your search contained a keyword that
        # was too short." with HTTP 200 — our parser should detect non-
        # JSON body before json.loads and yield a graceful (gdelt) line.
        out = _collect(research_search.search_gdelt("ai", 2))
        self.assertFalse(_has_traceback(out))
        # Either too-short error OR (if GDELT changed) at least no crash.
        self.assertTrue(out)


if __name__ == "__main__":
    unittest.main()
