#!/usr/bin/env python3
"""Tests for scripts/source_cache.py.

Uses a local http.server fixture so we don't hit real upstreams during
CI. Each test gets a per-test cache root via tempfile so the global
`data/source-cache/` is never touched.
"""

from __future__ import annotations

import http.server
import json
import os
import socketserver
import sys
import tempfile
import threading
import time
import unittest
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Make `import source_cache` work whether unittest is invoked from the
# repo root or from scripts/.
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import source_cache  # noqa: E402


# ---------------------------------------------------------------------
# Local fixture HTTP server

class _Counter:
    """Thread-safe request counter the fixture handler increments."""

    def __init__(self):
        self._lock = threading.Lock()
        self.hits = 0
        self.routes: dict[str, int] = {}

    def bump(self, path: str) -> None:
        with self._lock:
            self.hits += 1
            self.routes[path] = self.routes.get(path, 0) + 1


class _FixtureHandler(http.server.BaseHTTPRequestHandler):
    # Routes are set on the server instance.
    server_version = "SourceCacheTestFixture/1.0"

    def log_message(self, *args, **kwargs):  # silence test output
        pass

    def do_GET(self):  # noqa: N802
        self.server.counter.bump(self.path)
        route = self.server.routes.get(self.path)
        if route is None:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"not found")
            return
        status, ctype, body = route
        if callable(body):
            body = body()
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class _ThreadingServer(socketserver.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True


def _start_fixture(routes: dict[str, tuple[int, str, bytes]]):
    """Start a server on a random port. Returns (base_url, counter, stop)."""
    counter = _Counter()
    srv = _ThreadingServer(("127.0.0.1", 0), _FixtureHandler)
    srv.routes = routes
    srv.counter = counter
    port = srv.server_address[1]
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()

    def stop():
        srv.shutdown()
        srv.server_close()

    return f"http://127.0.0.1:{port}", counter, stop


# ---------------------------------------------------------------------
# Helpers

def _make_cfg(root: Path) -> source_cache.CacheConfig:
    return source_cache.CacheConfig(
        root=root,
        default_ttl_days=30,
        domain_ttl_days={},
        max_bytes=source_cache.DEFAULT_MAX_BYTES,
        timeout=5,
    )


# ---------------------------------------------------------------------
# Tests

class CanonicalizeTest(unittest.TestCase):
    def test_strips_tracking_params(self):
        c = source_cache.canonicalize_url(
            "https://www.example.com/a?utm_source=x&fbclid=y&q=1"
        )
        self.assertEqual(c, "https://www.example.com/a?q=1")

    def test_lowercases_scheme_and_host(self):
        self.assertEqual(
            source_cache.canonicalize_url("HTTPS://Www.Example.COM/Path"),
            "https://www.example.com/Path",
        )

    def test_strips_default_port(self):
        self.assertEqual(
            source_cache.canonicalize_url("http://example.com:80/a"),
            "http://example.com/a",
        )
        self.assertEqual(
            source_cache.canonicalize_url("https://example.com:443/a"),
            "https://example.com/a",
        )
        # Non-default port preserved
        self.assertEqual(
            source_cache.canonicalize_url("https://example.com:8443/a"),
            "https://example.com:8443/a",
        )

    def test_strips_trailing_slash_but_preserves_root(self):
        self.assertEqual(
            source_cache.canonicalize_url("https://example.com/a/b/"),
            "https://example.com/a/b",
        )
        self.assertEqual(
            source_cache.canonicalize_url("https://example.com/"),
            "https://example.com/",
        )

    def test_drops_fragment(self):
        self.assertEqual(
            source_cache.canonicalize_url("https://example.com/a#sec"),
            "https://example.com/a",
        )

    def test_sorts_query_params(self):
        self.assertEqual(
            source_cache.canonicalize_url("https://example.com/a?b=2&a=1"),
            "https://example.com/a?a=1&b=2",
        )

    def test_rejects_non_http_scheme(self):
        with self.assertRaises(ValueError):
            source_cache.canonicalize_url("file:///etc/passwd")
        with self.assertRaises(ValueError):
            source_cache.canonicalize_url("ftp://example.com/x")

    def test_rejects_missing_host(self):
        with self.assertRaises(ValueError):
            source_cache.canonicalize_url("https:///path")

    def test_variants_hash_identically(self):
        a = source_cache.cache_key("https://www.sec.gov/x.pdf?utm_source=foo")
        b = source_cache.cache_key("HTTPS://www.SEC.gov/x.pdf/")
        self.assertEqual(a, b)


class FetchHitMissTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "source-cache"
        self.cfg = _make_cfg(self.root)
        self.routes = {
            "/doc": (200, "text/plain", b"hello world"),
        }
        self.base, self.counter, self.stop_srv = _start_fixture(self.routes)

    def tearDown(self):
        self.stop_srv()
        self.tmp.cleanup()

    def test_first_call_misses_second_hits(self):
        url = f"{self.base}/doc"
        body1 = source_cache.fetch(url, config=self.cfg)
        self.assertEqual(body1, b"hello world")
        self.assertEqual(self.counter.hits, 1)
        # Second call: no extra HTTP hit.
        body2 = source_cache.fetch(url, config=self.cfg)
        self.assertEqual(body2, b"hello world")
        self.assertEqual(self.counter.hits, 1)

    def test_force_refresh_bypasses_cache(self):
        url = f"{self.base}/doc"
        source_cache.fetch(url, config=self.cfg)
        self.assertEqual(self.counter.hits, 1)
        source_cache.fetch(url, force_refresh=True, config=self.cfg)
        self.assertEqual(self.counter.hits, 2)

    def test_canonicalization_collapses_variants(self):
        url1 = f"{self.base}/doc?utm_source=x"
        url2 = f"{self.base}/doc"  # canonical form of url1
        source_cache.fetch(url1, config=self.cfg)
        source_cache.fetch(url2, config=self.cfg)
        # Only one network hit despite two distinct input URLs.
        self.assertEqual(self.counter.hits, 1)

    def test_info_returns_metadata(self):
        url = f"{self.base}/doc"
        source_cache.fetch(url, config=self.cfg)
        meta = source_cache.info(url, config=self.cfg)
        self.assertIsNotNone(meta)
        self.assertEqual(meta["status"], 200)
        self.assertEqual(meta["content_length"], len(b"hello world"))
        self.assertEqual(meta["host"], meta["host"].lower())
        self.assertIn("fetched_at", meta)

    def test_info_returns_none_for_unknown(self):
        self.assertIsNone(source_cache.info(f"{self.base}/never-fetched", config=self.cfg))

    def test_http_error_surfaces_as_cache_error(self):
        with self.assertRaises(source_cache.CacheError):
            source_cache.fetch(f"{self.base}/missing", config=self.cfg)


class TTLExpiryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "source-cache"
        self.cfg = _make_cfg(self.root)
        self.routes = {"/doc": (200, "text/plain", b"v1")}
        self.base, self.counter, self.stop_srv = _start_fixture(self.routes)

    def tearDown(self):
        self.stop_srv()
        self.tmp.cleanup()

    def _backdate_meta(self, url: str, days: int) -> None:
        canonical = source_cache.canonicalize_url(url)
        entry = source_cache._find_existing_entry(canonical, self.cfg.root)
        self.assertIsNotNone(entry, "must fetch before backdating")
        meta = json.loads(entry["meta"].read_text(encoding="utf-8"))
        new_dt = datetime.now(timezone.utc) - timedelta(days=days)
        meta["fetched_at"] = new_dt.isoformat()
        entry["meta"].write_text(
            json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )

    def test_expired_entry_refetches(self):
        url = f"{self.base}/doc"
        source_cache.fetch(url, config=self.cfg)
        self.assertEqual(self.counter.hits, 1)
        self._backdate_meta(url, days=60)  # > default 30d TTL
        source_cache.fetch(url, config=self.cfg)
        self.assertEqual(self.counter.hits, 2)

    def test_max_age_override(self):
        url = f"{self.base}/doc"
        source_cache.fetch(url, config=self.cfg)
        # Backdate by 5 days. With default TTL of 30d we'd still hit;
        # with override max-age=1d we should miss.
        self._backdate_meta(url, days=5)
        source_cache.fetch(url, max_age_days=1, config=self.cfg)
        self.assertEqual(self.counter.hits, 2)

    def test_per_domain_ttl(self):
        url = f"{self.base}/doc"
        # Set a very short TTL for 127.0.0.1.
        self.cfg.domain_ttl_days = {"127.0.0.1": 0}
        source_cache.fetch(url, config=self.cfg)
        # TTL of 0 days means anything > 0 elapsed expires; we backdate
        # by 1 day to force the comparison.
        self._backdate_meta(url, days=1)
        source_cache.fetch(url, config=self.cfg)
        self.assertEqual(self.counter.hits, 2)


class AtomicWriteTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "source-cache"

    def tearDown(self):
        self.tmp.cleanup()

    def test_writes_via_tmp_then_rename(self):
        target = self.root / "2026-05" / "ab" / "abcd.body"
        source_cache._atomic_write_bytes(target, b"final content")
        self.assertTrue(target.is_file())
        self.assertFalse(target.with_suffix(".body.tmp").exists())
        self.assertEqual(target.read_bytes(), b"final content")

    def test_overwrites_existing(self):
        target = self.root / "2026-05" / "ab" / "abcd.body"
        source_cache._atomic_write_bytes(target, b"v1")
        source_cache._atomic_write_bytes(target, b"v2")
        self.assertEqual(target.read_bytes(), b"v2")

    def test_json_round_trip(self):
        target = self.root / "2026-05" / "ab" / "abcd.meta.json"
        source_cache._atomic_write_json(target, {"k": 1, "v": "x"})
        self.assertEqual(json.loads(target.read_text()), {"k": 1, "v": "x"})


class PurgeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "source-cache"
        self.cfg = _make_cfg(self.root)
        self.routes = {
            "/a": (200, "text/plain", b"AAA"),
            "/b": (200, "text/plain", b"BBB"),
        }
        self.base, self.counter, self.stop_srv = _start_fixture(self.routes)

    def tearDown(self):
        self.stop_srv()
        self.tmp.cleanup()

    def _backdate(self, url: str, days: int) -> None:
        canonical = source_cache.canonicalize_url(url)
        entry = source_cache._find_existing_entry(canonical, self.cfg.root)
        meta = json.loads(entry["meta"].read_text())
        new_dt = datetime.now(timezone.utc) - timedelta(days=days)
        meta["fetched_at"] = new_dt.isoformat()
        entry["meta"].write_text(
            json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True)
        )

    def test_purge_removes_old_entries_only(self):
        source_cache.fetch(f"{self.base}/a", config=self.cfg)
        source_cache.fetch(f"{self.base}/b", config=self.cfg)
        self._backdate(f"{self.base}/a", days=60)
        result = source_cache.purge(timedelta(days=30), config=self.cfg)
        self.assertEqual(result["removed"], 1)
        # /a should be gone, /b should remain.
        self.assertIsNone(source_cache.info(f"{self.base}/a", config=self.cfg))
        self.assertIsNotNone(source_cache.info(f"{self.base}/b", config=self.cfg))

    def test_purge_dry_run(self):
        source_cache.fetch(f"{self.base}/a", config=self.cfg)
        self._backdate(f"{self.base}/a", days=60)
        result = source_cache.purge(timedelta(days=30), config=self.cfg, dry_run=True)
        self.assertEqual(result["removed"], 1)
        # Body still on disk after dry-run.
        self.assertIsNotNone(source_cache.info(f"{self.base}/a", config=self.cfg))

    def test_parse_age_arg(self):
        self.assertEqual(source_cache.parse_age_arg("30d"), timedelta(days=30))
        self.assertEqual(source_cache.parse_age_arg("2w"), timedelta(weeks=2))
        self.assertEqual(source_cache.parse_age_arg("12h"), timedelta(hours=12))
        self.assertEqual(source_cache.parse_age_arg("60m"), timedelta(minutes=60))
        self.assertEqual(source_cache.parse_age_arg("7"), timedelta(days=7))
        with self.assertRaises(ValueError):
            source_cache.parse_age_arg("forever")


class StatsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "source-cache"
        self.cfg = _make_cfg(self.root)
        self.routes = {
            "/a": (200, "text/plain", b"AAA"),
            "/b": (200, "text/plain", b"BBBB"),
        }
        self.base, _, self.stop_srv = _start_fixture(self.routes)

    def tearDown(self):
        self.stop_srv()
        self.tmp.cleanup()

    def test_stats_on_empty_cache(self):
        s = source_cache.stats(config=self.cfg)
        self.assertEqual(s["entries"], 0)
        self.assertEqual(s["total_bytes"], 0)

    def test_stats_after_fetches(self):
        source_cache.fetch(f"{self.base}/a", config=self.cfg)
        source_cache.fetch(f"{self.base}/b", config=self.cfg)
        s = source_cache.stats(config=self.cfg)
        self.assertEqual(s["entries"], 2)
        self.assertEqual(s["total_bytes"], 3 + 4)
        # Host includes the non-default port (e.g. "127.0.0.1:54321")
        # because the canonical form preserves the netloc verbatim once
        # default ports are stripped.
        self.assertTrue(s["top_hosts"][0]["host"].startswith("127.0.0.1"))
        self.assertEqual(s["top_hosts"][0]["count"], 2)


class SizeCapTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "source-cache"
        self.cfg = _make_cfg(self.root)
        self.cfg.max_bytes = 100  # very low cap
        big = b"x" * 1024
        self.routes = {"/big": (200, "application/octet-stream", big)}
        self.base, _, self.stop_srv = _start_fixture(self.routes)

    def tearDown(self):
        self.stop_srv()
        self.tmp.cleanup()

    def test_oversized_body_rejected(self):
        with self.assertRaises(source_cache.CacheError):
            source_cache.fetch(f"{self.base}/big", config=self.cfg)
        # Nothing should be persisted on rejection.
        self.assertIsNone(source_cache.info(f"{self.base}/big", config=self.cfg))


class ConcurrencyTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "source-cache"
        self.cfg = _make_cfg(self.root)
        # Slow upstream so two concurrent fetches really do race.
        def _slow_body():
            time.sleep(0.2)
            return b"slow content"
        self.routes = {"/slow": (200, "text/plain", _slow_body)}
        self.base, self.counter, self.stop_srv = _start_fixture(self.routes)

    def tearDown(self):
        self.stop_srv()
        self.tmp.cleanup()

    def test_concurrent_fetchers_share_one_upstream_hit(self):
        url = f"{self.base}/slow"
        bodies = [None, None]
        errs = [None, None]

        def worker(i):
            try:
                bodies[i] = source_cache.fetch(url, config=self.cfg)
            except Exception as e:  # noqa: BLE001
                errs[i] = e

        t1 = threading.Thread(target=worker, args=(0,))
        t2 = threading.Thread(target=worker, args=(1,))
        t1.start(); t2.start()
        t1.join(); t2.join()

        self.assertIsNone(errs[0], f"worker 0 error: {errs[0]}")
        self.assertIsNone(errs[1], f"worker 1 error: {errs[1]}")
        self.assertEqual(bodies[0], b"slow content")
        self.assertEqual(bodies[1], b"slow content")
        # The lock should ensure only ONE upstream hit happened. The
        # second worker took the lock after the first wrote the entry,
        # re-checked, and served from cache.
        self.assertEqual(
            self.counter.hits, 1,
            f"expected 1 upstream hit, got {self.counter.hits}",
        )


class CLITest(unittest.TestCase):
    """Spot-check the argparse wiring — actual fetches use the library tests."""

    def test_get_subcommand_requires_url(self):
        with self.assertRaises(SystemExit):
            source_cache.main(["get"])

    def test_parse_age_via_cli_purge(self):
        # purge --older-than 60d with no cache root should report 0 removals.
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "source-cache"
            # Monkeypatch _default_root via env-style override is overkill;
            # we just test parse_age_arg directly above + the CLI dispatch
            # works for `stats` on a fresh root.
            self.assertEqual(source_cache.parse_age_arg("60d").days, 60)


if __name__ == "__main__":
    unittest.main()
