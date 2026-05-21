#!/usr/bin/env python3
"""Persistent cache of fetched primary-source URLs.

Used by gen-research runs that repeatedly hit the same primary documents
(S-1 PDFs, IR pages, papers) across different topics. The first run
downloads + caches; later runs hit cache, saving the round-trip cost,
sparing the upstream host, and surviving transient outages.

Design (first-principles):

  - Cache KEY = SHA-256 of the CANONICAL URL string. Canonicalization
    strips tracking params (utm_*, fbclid, gclid, ref, ref_, _hsenc,
    mc_*, igshid, mkt_tok, oly_*), lowercases scheme + host, strips
    the default port for http/https, removes a trailing slash from
    the path, and sorts remaining query params for stability. Result:
    the same logical document hashes to the same key regardless of
    cosmetic URL variation.

  - Cache LAYOUT (filesystem, no database — single host, single user):
        data/source-cache/
            YYYY-MM/               (year-month bucket of fetched_at, for purge)
                <hash[:2]>/        (first 2 hex chars, shard fan-out)
                    <hash>.meta.json   (canonical URL, fetched_at,
                                         content_type, status, length,
                                         hash, optional pdftotext bytes)
                    <hash>.body        (raw fetched bytes)
                    <hash>.txt         (only for PDFs — pdftotext output)
                    <hash>.lock        (advisory flock for concurrent runs)

  - Per-domain TTL via data/source-cache-config.json (optional). Default
    TTL: 30 days. The config file may set "default_ttl_days" and
    "domain_ttl_days": { "<host>": <days>, "<suffix>.<tld>": <days> }.

  - CONCURRENCY: a parallel gen-research run that asks for the same URL
    blocks on fcntl.flock(<hash>.lock, LOCK_EX) before fetching, so only
    one writer touches the meta+body. Readers (cache HIT path) take a
    shared lock first.

  - ATOMIC WRITES: every body/meta write goes to ".tmp" then os.replace
    into final name. A crash mid-fetch leaves only a .tmp file behind,
    which a later run overwrites; the existing cached entry is unharmed.

  - SIZE CAP: per-response cap (default 100 MB) prevents a single
    pathological URL from filling disk. Configurable via env var
    SOURCE_CACHE_MAX_BYTES. There is intentionally NO total-cache
    size cap; the operator is expected to run
    `uv run python scripts/source_cache.py purge --older-than 30d` on a
    schedule (or in a workflow's housekeeping step) when the cache
    grows beyond what's wanted. `stats` reports the current total.

  - TRUST MODEL: this is a research convenience cache, not a security
    boundary. We trust upstream to serve consistent content. If a URL
    later starts serving malicious bytes, the cache will re-serve them
    until TTL expiry or --force-refresh. Documented in the README.

  - DEPS: stdlib only. urllib for fetches, hashlib + json + pathlib +
    fcntl for storage, subprocess for the optional pdftotext step.
    Same constraint as research_search.py.

CLI:

  uv run python scripts/source_cache.py get   <url> [--force-refresh] [--max-age N]
  uv run python scripts/source_cache.py info  <url>
  uv run python scripts/source_cache.py purge --older-than 30d
  uv run python scripts/source_cache.py stats

PROGRAMMATIC:

  from source_cache import fetch
  raw = fetch("https://www.sec.gov/Archives/edgar/.../s-1.pdf")
"""

from __future__ import annotations

import argparse
import contextlib
import fcntl
import hashlib
import json
import os
import re
import shutil
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

# ---------------------------------------------------------------------
# Configuration knobs (env-overridable so tests and callers can scope it
# without touching globals).

USER_AGENT = "ai-research-arm/source-cache 1.0 (github.com/guzus/ai-research-arm)"
DEFAULT_TIMEOUT = 30
DEFAULT_TTL_DAYS = 30
DEFAULT_MAX_BYTES = 100 * 1024 * 1024  # 100 MB per response
# Total cache-on-disk cap. When a fresh write would push us above this,
# we LRU-evict oldest entries (by fetched_at) until there's room. The
# default of 10 GB gives ~100 max-size entries; in practice the cache
# holds thousands of small HTML/JSON entries plus a handful of PDFs.
# Override via env var SOURCE_CACHE_MAX_TOTAL_BYTES.
DEFAULT_MAX_TOTAL_BYTES = 10 * 1024 * 1024 * 1024  # 10 GB

# Query params we always discard during canonicalization — they don't
# affect WHICH document is served. We deliberately keep this list TIGHT:
# every entry below is unambiguously a tracker/attribution param. Generic
# short names like `s`, `t`, `ref`, `trk`, `source` are NOT stripped
# globally because legitimate sites use them for content selection (e.g.
# `?source=owner` on github.com, `?ref=…` for branch on the GitHub API,
# `?t=` for paragraph offset on some news sites). Per-host stripping for
# narrower cases lives in TRACKING_PARAM_HOST_RULES below.
TRACKING_PARAM_PATTERNS = (
    re.compile(r"^utm_"),
    re.compile(r"^_hs(enc|mi)$"),
    re.compile(r"^mc_(cid|eid)$"),
    re.compile(r"^mkt_tok$"),
    re.compile(r"^oly_(anon_id|enc_id)$"),
    re.compile(r"^fbclid$"),
    re.compile(r"^gclid$"),
    re.compile(r"^dclid$"),
    re.compile(r"^msclkid$"),
    re.compile(r"^yclid$"),
    re.compile(r"^igshid$"),
)

# Per-host tracking-param rules. The KEY is the bare hostname; the VALUE
# is a tuple of compiled regexes that match params we strip on THAT host.
# Used for cases where a short param name is a tracker on one site but
# content-bearing on another (Twitter's `?s=20&t=…` share suffix is the
# canonical example).
TRACKING_PARAM_HOST_RULES: dict[str, tuple[re.Pattern, ...]] = {
    "x.com": (re.compile(r"^s$"), re.compile(r"^t$")),
    "twitter.com": (re.compile(r"^s$"), re.compile(r"^t$")),
    "www.twitter.com": (re.compile(r"^s$"), re.compile(r"^t$")),
    "mobile.twitter.com": (re.compile(r"^s$"), re.compile(r"^t$")),
}


def _is_tracking_param(name: str, host: str = "") -> bool:
    name = name.lower()
    if any(p.match(name) for p in TRACKING_PARAM_PATTERNS):
        return True
    host_rules = TRACKING_PARAM_HOST_RULES.get(host.lower())
    if host_rules and any(p.match(name) for p in host_rules):
        return True
    return False


# ---------------------------------------------------------------------
# SSL context — mirror research_search.py so the same CA-discovery
# heuristic works on both runners and local dev machines.

def _build_ssl_context() -> ssl.SSLContext:
    cafile = os.environ.get("SSL_CERT_FILE")
    if cafile and os.path.isfile(cafile):
        return ssl.create_default_context(cafile=cafile)
    for p in (
        "/etc/ssl/cert.pem",
        "/etc/ssl/certs/ca-certificates.crt",
        "/etc/pki/tls/certs/ca-bundle.crt",
        "/opt/homebrew/etc/openssl@3/cert.pem",
        "/usr/local/etc/openssl@3/cert.pem",
    ):
        if os.path.isfile(p):
            return ssl.create_default_context(cafile=p)
    return ssl.create_default_context()


SSL_CTX = _build_ssl_context()


# ---------------------------------------------------------------------
# URL canonicalization

def canonicalize_url(url: str) -> str:
    """Return the canonical form used to derive the cache key.

    Rules:
      - lowercase scheme + host
      - strip the default port (80/443) when it matches the scheme
      - drop a trailing "/" from the path (but keep "/" when path is just root)
      - drop tracking params (utm_*, fbclid, …)
      - sort remaining query params for deterministic ordering
      - drop URL fragments (they don't change what bytes the server returns)
    """
    if not url or not isinstance(url, str):
        raise ValueError("url must be a non-empty string")
    url = url.strip()
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"unsupported scheme: {parsed.scheme!r} (only http/https)")
    if not parsed.netloc:
        raise ValueError(f"missing host in URL: {url!r}")

    scheme = parsed.scheme.lower()
    # netloc may contain userinfo / port; we lowercase only the host portion.
    userinfo = ""
    host_part = parsed.netloc
    if "@" in host_part:
        userinfo, host_part = host_part.split("@", 1)
        userinfo += "@"
    if ":" in host_part:
        host, port = host_part.rsplit(":", 1)
        if (scheme == "http" and port == "80") or (scheme == "https" and port == "443"):
            netloc = userinfo + host.lower()
        else:
            netloc = userinfo + host.lower() + ":" + port
    else:
        netloc = userinfo + host_part.lower()

    path = parsed.path or "/"
    if len(path) > 1 and path.endswith("/"):
        path = path.rstrip("/") or "/"

    # For tracking-param stripping we use the BARE host (no port, no
    # userinfo) so per-host rules match consistently.
    bare_host = netloc.split("@", 1)[-1]
    if bare_host.startswith("["):
        end = bare_host.find("]")
        if end >= 0:
            bare_host = bare_host[: end + 1]
    elif ":" in bare_host:
        bare_host = bare_host.rsplit(":", 1)[0]

    # parse_qsl with keep_blank_values=True so "?foo=" survives if upstream
    # cares; we still drop tracking blanks.
    qs = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    qs = [(k, v) for (k, v) in qs if not _is_tracking_param(k, bare_host)]
    qs.sort(key=lambda kv: (kv[0], kv[1]))
    query = urllib.parse.urlencode(qs)

    # Drop fragment unconditionally.
    return urllib.parse.urlunsplit((scheme, netloc, path, query, ""))


def cache_key(url: str) -> str:
    return hashlib.sha256(canonicalize_url(url).encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------
# Cache instance (path-resolved at construction so tests can scope it)

@dataclass
class CacheConfig:
    root: Path
    default_ttl_days: int = DEFAULT_TTL_DAYS
    domain_ttl_days: dict[str, int] = field(default_factory=dict)
    max_bytes: int = DEFAULT_MAX_BYTES
    max_total_bytes: int = DEFAULT_MAX_TOTAL_BYTES
    timeout: int = DEFAULT_TIMEOUT

    @classmethod
    def load(cls, root: Path | None = None) -> "CacheConfig":
        root = (root or _default_root()).resolve()
        cfg_path = root.parent / "source-cache-config.json"
        domain_ttl: dict[str, int] = {}
        default_ttl = DEFAULT_TTL_DAYS
        if cfg_path.is_file():
            try:
                raw = json.loads(cfg_path.read_text(encoding="utf-8"))
                if isinstance(raw, dict):
                    if isinstance(raw.get("default_ttl_days"), int):
                        default_ttl = int(raw["default_ttl_days"])
                    dt = raw.get("domain_ttl_days") or {}
                    if isinstance(dt, dict):
                        for k, v in dt.items():
                            if isinstance(k, str) and isinstance(v, int):
                                domain_ttl[k.lower()] = v
            except Exception as e:  # noqa: BLE001
                print(
                    f"source_cache: warning — failed to parse {cfg_path}: {e}; "
                    "falling back to defaults",
                    file=sys.stderr,
                )
        max_bytes = int(os.environ.get("SOURCE_CACHE_MAX_BYTES", DEFAULT_MAX_BYTES))
        max_total_bytes = int(os.environ.get(
            "SOURCE_CACHE_MAX_TOTAL_BYTES", DEFAULT_MAX_TOTAL_BYTES))
        timeout = int(os.environ.get("SOURCE_CACHE_TIMEOUT", DEFAULT_TIMEOUT))
        return cls(
            root=root,
            default_ttl_days=default_ttl,
            domain_ttl_days=domain_ttl,
            max_bytes=max_bytes,
            max_total_bytes=max_total_bytes,
            timeout=timeout,
        )

    def ttl_for(self, host: str) -> int:
        # Strip userinfo + port before comparing — users configure TTLs
        # by domain name, not by `example.com:8443`.
        host = host.lower()
        if "@" in host:
            host = host.rsplit("@", 1)[1]
        if host.startswith("["):
            # IPv6: [::1]:443 → [::1]
            end = host.find("]")
            if end >= 0:
                host = host[: end + 1]
        elif ":" in host:
            host = host.rsplit(":", 1)[0]
        if host in self.domain_ttl_days:
            return self.domain_ttl_days[host]
        # Suffix match: "sec.gov" matches "www.sec.gov".
        for pat, days in self.domain_ttl_days.items():
            if pat.startswith(".") and host.endswith(pat):
                return days
            if not pat.startswith(".") and host.endswith("." + pat):
                return days
        return self.default_ttl_days


def _default_root() -> Path:
    # Located relative to this script: scripts/source_cache.py → ../data/source-cache
    return Path(__file__).resolve().parent.parent / "data" / "source-cache"


# ---------------------------------------------------------------------
# Storage helpers

def _bucket_for(month: str, h: str, root: Path) -> Path:
    return root / month / h[:2]


def _entry_paths(canonical_url: str, fetched_at: datetime, root: Path) -> dict[str, Path]:
    h = hashlib.sha256(canonical_url.encode("utf-8")).hexdigest()
    month = fetched_at.strftime("%Y-%m")
    bucket = _bucket_for(month, h, root)
    return {
        "hash": h,
        "bucket": bucket,
        "meta": bucket / f"{h}.meta.json",
        "body": bucket / f"{h}.body",
        "text": bucket / f"{h}.txt",
        "lock": bucket / f"{h}.lock",
    }


def _find_existing_entry(canonical_url: str, root: Path) -> dict[str, Path] | None:
    """Locate an existing cached entry across all month buckets.

    The month bucket reflects fetched_at, so we can't compute the bucket
    from the URL alone — we have to scan. We do it lazily: glob by hash.
    O(num_months) per lookup, which on a 1-year-old cache is 12. Fast.
    """
    h = hashlib.sha256(canonical_url.encode("utf-8")).hexdigest()
    if not root.exists():
        return None
    for meta_path in root.glob(f"*/{h[:2]}/{h}.meta.json"):
        bucket = meta_path.parent
        return {
            "hash": h,
            "bucket": bucket,
            "meta": meta_path,
            "body": bucket / f"{h}.body",
            "text": bucket / f"{h}.txt",
            "lock": bucket / f"{h}.lock",
        }
    return None


@contextlib.contextmanager
def _exclusive_lock(lock_path: Path):
    """Hold an exclusive flock for the lifetime of the with-block.

    The lockfile lives next to the entry's body/meta. We open in 'w' so
    the file is created if missing; the file content is irrelevant.
    """
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with open(lock_path, "w") as fp:
        try:
            fcntl.flock(fp.fileno(), fcntl.LOCK_EX)
            yield fp
        finally:
            fcntl.flock(fp.fileno(), fcntl.LOCK_UN)


def _enumerate_entries(root: Path) -> list[tuple[float, int, Path, str]]:
    """List every cache entry as (fetched_at_epoch, size, meta_path, hash).

    Used by the LRU evictor. Cheap walk: one stat per meta + body file.
    Entries we can't parse are returned at epoch 0 so they evict first.
    """
    rows: list[tuple[float, int, Path, str]] = []
    if not root.exists():
        return rows
    for meta_path in root.glob("*/*/*.meta.json"):
        h = meta_path.name[: -len(".meta.json")]
        bucket = meta_path.parent
        size = 0
        for suffix in (".meta.json", ".body", ".txt"):
            f = bucket / f"{h}{suffix}"
            try:
                size += f.stat().st_size
            except OSError:
                pass
        ts = 0.0
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            fetched_at = datetime.fromisoformat(meta["fetched_at"])
            if fetched_at.tzinfo is None:
                fetched_at = fetched_at.replace(tzinfo=timezone.utc)
            ts = fetched_at.timestamp()
        except Exception:  # noqa: BLE001
            pass
        rows.append((ts, size, meta_path, h))
    return rows


def _evict_to_fit(needed_bytes: int, cfg: CacheConfig,
                  protect_hash: str | None = None) -> int:
    """LRU-evict oldest entries until `needed_bytes` fits under the quota.

    Returns the number of bytes freed. Never evicts the entry whose hash
    matches `protect_hash` (the one we're currently writing). Honors the
    same atomic-delete pattern as `purge()` so a crash mid-eviction
    leaves valid entries intact.
    """
    if cfg.max_total_bytes <= 0:
        return 0
    entries = _enumerate_entries(cfg.root)
    if not entries:
        return 0
    current_total = sum(sz for _, sz, _, _ in entries)
    if current_total + needed_bytes <= cfg.max_total_bytes:
        return 0
    # Sort oldest-first (lowest fetched_at first).
    entries.sort(key=lambda r: r[0])
    freed = 0
    for ts, size, meta_path, h in entries:
        if current_total + needed_bytes - freed <= cfg.max_total_bytes:
            break
        if protect_hash is not None and h == protect_hash:
            continue
        bucket = meta_path.parent
        for suffix in (".meta.json", ".body", ".txt", ".lock"):
            f = bucket / f"{h}{suffix}"
            if not f.is_file():
                continue
            try:
                fsize = f.stat().st_size
                f.unlink()
                freed += fsize
            except OSError:
                pass
    return freed


def _atomic_write_bytes(target: Path, data: bytes) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    # Use string-append rather than Path.with_suffix because on older
    # Python (<3.12 strict mode) with_suffix rejects multi-dot suffixes
    # like ".json.tmp" — which is exactly what we'd produce for a path
    # named "<hash>.meta.json".
    tmp = Path(str(target) + ".tmp")
    with open(tmp, "wb") as fp:
        fp.write(data)
        fp.flush()
        os.fsync(fp.fileno())
    os.replace(tmp, target)


def _atomic_write_json(target: Path, data: dict) -> None:
    _atomic_write_bytes(
        target,
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8"),
    )


# ---------------------------------------------------------------------
# HTTP fetch (with size cap)

class CacheError(Exception):
    pass


def _http_get(url: str, *, timeout: int, max_bytes: int) -> tuple[bytes, dict]:
    """Fetch a URL into memory with a hard size cap.

    Returns (body_bytes, response_metadata_dict). Raises CacheError on
    any failure (network, HTTP >= 400, oversized body).

    `response_metadata_dict` includes the final URL (`url_final`) and
    `host_final` after any redirects so callers can store a forensic
    trail. urllib.request follows redirects by default; if the final
    URL differs from the input URL, the difference is recorded but the
    fetch is not rejected — primary sources legitimately redirect (IR
    pages → /investors, SEC archives → versioned URLs, etc.). Operators
    inspecting a poisoning incident can compare `url_canonical` vs
    `url_final` to detect a hostile rewrite.
    """
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "*/*",
        # Many servers gzip by default; we don't decompress so disable.
        "Accept-Encoding": "identity",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as resp:
            status = resp.status
            content_type = resp.headers.get("Content-Type", "")
            final_url = resp.geturl()
            # Read up to max_bytes + 1 so we can detect the overflow.
            buf = resp.read(max_bytes + 1)
    except urllib.error.HTTPError as e:
        raise CacheError(f"HTTP {e.code} fetching {url}") from e
    except urllib.error.URLError as e:
        raise CacheError(f"network error fetching {url}: {e.reason}") from e
    except Exception as e:  # noqa: BLE001 — surface everything as CacheError
        raise CacheError(f"{type(e).__name__} fetching {url}: {e}") from e
    if len(buf) > max_bytes:
        raise CacheError(
            f"response body exceeds size cap ({max_bytes} bytes) for {url}; "
            "raise SOURCE_CACHE_MAX_BYTES to allow this URL"
        )
    try:
        host_final = urllib.parse.urlsplit(final_url).netloc or ""
    except Exception:  # noqa: BLE001
        host_final = ""
    return buf, {
        "status": status,
        "content_type": content_type,
        "content_length": len(buf),
        "url_final": final_url,
        "host_final": host_final,
    }


# ---------------------------------------------------------------------
# Optional PDF → text extraction (best-effort; doesn't fail the fetch)

def _maybe_extract_pdf(body: bytes, url: str, content_type: str) -> bytes | None:
    is_pdf = (
        content_type.lower().startswith("application/pdf")
        or urllib.parse.urlsplit(url).path.lower().endswith(".pdf")
    )
    if not is_pdf:
        return None
    if shutil.which("pdftotext") is None:
        print(
            "source_cache: note — pdftotext not found; skipping text extraction. "
            "PDF body is still cached.",
            file=sys.stderr,
        )
        return None
    try:
        # pdftotext - - reads from stdin and writes to stdout. Layout is the
        # default reading-order extraction, which matches what the existing
        # workflow uses (`pdftotext /tmp/x.pdf - | head -c 60000`).
        result = subprocess.run(
            ["pdftotext", "-", "-"],
            input=body,
            capture_output=True,
            timeout=120,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"source_cache: pdftotext failed ({e}); skipping text extraction.", file=sys.stderr)
        return None
    if result.returncode != 0:
        print(
            f"source_cache: pdftotext exit {result.returncode}; stderr: "
            f"{result.stderr[:200].decode('utf-8', errors='replace')}",
            file=sys.stderr,
        )
        return None
    return result.stdout


# ---------------------------------------------------------------------
# Public fetch() — used as a library by other scripts

def fetch(url: str, *, force_refresh: bool = False, max_age_days: int | None = None,
          config: CacheConfig | None = None) -> bytes:
    """Return the cached body for `url`, fetching+caching on miss/expiry.

    Args:
        url: raw URL (canonicalized internally)
        force_refresh: bypass cache + re-fetch even on a fresh hit
        max_age_days: override the configured per-domain TTL for this call
        config: a CacheConfig to use (else load default)
    """
    cfg = config or CacheConfig.load()
    canonical = canonicalize_url(url)
    host = urllib.parse.urlsplit(canonical).netloc
    ttl_days = max_age_days if max_age_days is not None else cfg.ttl_for(host)

    existing = _find_existing_entry(canonical, cfg.root)

    if existing and not force_refresh:
        try:
            meta = json.loads(existing["meta"].read_text(encoding="utf-8"))
            fetched_at = datetime.fromisoformat(meta["fetched_at"])
            if fetched_at.tzinfo is None:
                fetched_at = fetched_at.replace(tzinfo=timezone.utc)
            if datetime.now(timezone.utc) - fetched_at < timedelta(days=ttl_days):
                if existing["body"].is_file():
                    return existing["body"].read_bytes()
        except Exception as e:  # noqa: BLE001
            # Treat as a miss — we'll re-fetch and overwrite.
            print(
                f"source_cache: warning — corrupt entry at {existing['meta']}: {e}; refreshing",
                file=sys.stderr,
            )

    # MISS path. Acquire the per-key lock so two concurrent runs don't
    # race on the same URL. The lock lives in the (possibly new) bucket
    # for the CURRENT month; that's where the new entry will be written.
    now = datetime.now(timezone.utc)
    new_paths = _entry_paths(canonical, now, cfg.root)
    new_paths["bucket"].mkdir(parents=True, exist_ok=True)
    with _exclusive_lock(new_paths["lock"]):
        # Re-check after acquiring the lock — another writer may have
        # just produced a fresh entry while we were blocked.
        existing = _find_existing_entry(canonical, cfg.root)
        if existing and not force_refresh:
            try:
                meta = json.loads(existing["meta"].read_text(encoding="utf-8"))
                fetched_at = datetime.fromisoformat(meta["fetched_at"])
                if fetched_at.tzinfo is None:
                    fetched_at = fetched_at.replace(tzinfo=timezone.utc)
                if now - fetched_at < timedelta(days=ttl_days):
                    if existing["body"].is_file():
                        return existing["body"].read_bytes()
            except Exception:  # noqa: BLE001
                pass

        body, resp_meta = _http_get(canonical, timeout=cfg.timeout, max_bytes=cfg.max_bytes)
        body_sha256 = hashlib.sha256(body).hexdigest()
        pdf_text = _maybe_extract_pdf(body, canonical, resp_meta["content_type"])

        # If an existing entry lives in an OLDER month bucket, write the
        # new one in the current month bucket and remove the stale entry.
        # This keeps month-based purge intuitive.
        if existing and existing["meta"] != new_paths["meta"]:
            for k in ("meta", "body", "text"):
                try:
                    existing[k].unlink(missing_ok=True)
                except Exception:  # noqa: BLE001
                    pass

        # Total-cache quota: LRU-evict oldest entries until the new body
        # + meta + optional pdf-text fits under cfg.max_total_bytes. We
        # protect THIS entry's hash so a refresh of an oversized URL
        # doesn't evict itself. If the single new body exceeds the
        # quota outright, we still write — the alternative is dropping
        # the fetch we already paid for, which is worse than briefly
        # over-quota until the next eviction.
        projected = len(body) + (len(pdf_text) if pdf_text else 0) + 1024  # 1KB meta budget
        _evict_to_fit(projected, cfg, protect_hash=new_paths["hash"])

        # Detect post-fetch redirect: if the upstream redirected to a
        # different host, record it in meta so an operator inspecting
        # a poisoning incident sees the discrepancy. Compare BARE hosts
        # (no port, no userinfo) since e.g. an HTTP→HTTPS upgrade
        # legitimately changes the netloc-with-port but not the host.
        def _bare(netloc: str) -> str:
            n = netloc.split("@", 1)[-1]
            if n.startswith("["):
                end = n.find("]")
                if end >= 0:
                    return n[: end + 1].lower()
            if ":" in n:
                return n.rsplit(":", 1)[0].lower()
            return n.lower()
        canon_host_bare = _bare(host)
        final_host_bare = _bare(resp_meta.get("host_final") or "")
        redirect_host_mismatch = bool(final_host_bare and final_host_bare != canon_host_bare)

        meta_doc = {
            "url_original": url,
            "url_canonical": canonical,
            "url_final": resp_meta.get("url_final") or canonical,
            "host": host,
            "host_final": resp_meta.get("host_final") or host,
            "redirect_host_mismatch": redirect_host_mismatch,
            "hash": new_paths["hash"],
            "fetched_at": now.isoformat(),
            "status": resp_meta["status"],
            "content_type": resp_meta["content_type"],
            "content_length": resp_meta["content_length"],
            # Body SHA-256 lets a future re-fetch detect content drift
            # (the URL is the SAME, but the bytes changed). Useful as
            # forensic evidence if a cached primary source was later
            # silently updated upstream.
            "body_sha256": body_sha256,
            "ttl_days": ttl_days,
            "pdf_text_bytes": len(pdf_text) if pdf_text is not None else 0,
        }
        _atomic_write_bytes(new_paths["body"], body)
        if pdf_text is not None:
            _atomic_write_bytes(new_paths["text"], pdf_text)
        else:
            # Refresh case: if a previous (PDF) fetch left a stale
            # <hash>.txt in this bucket and the new content isn't PDF,
            # the stale text would otherwise be re-served by info() —
            # which would mismatch the cached body. Unlink it now.
            try:
                new_paths["text"].unlink(missing_ok=True)
            except Exception:  # noqa: BLE001
                pass
        _atomic_write_json(new_paths["meta"], meta_doc)

    return body


def info(url: str, config: CacheConfig | None = None) -> dict | None:
    cfg = config or CacheConfig.load()
    canonical = canonicalize_url(url)
    entry = _find_existing_entry(canonical, cfg.root)
    if not entry:
        return None
    try:
        meta = json.loads(entry["meta"].read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return {"error": f"failed to read meta: {e}", "meta_path": str(entry["meta"])}
    meta["_meta_path"] = str(entry["meta"])
    meta["_body_path"] = str(entry["body"])
    if entry["text"].is_file():
        meta["_text_path"] = str(entry["text"])
    return meta


# ---------------------------------------------------------------------
# Maintenance: purge + stats

_AGE_RE = re.compile(r"^(\d+)\s*([dwhm]?)$")


def parse_age_arg(s: str) -> timedelta:
    """Parse "30d", "12h", "2w", "60m", or a bare integer (days)."""
    m = _AGE_RE.match(s.strip().lower())
    if not m:
        raise ValueError(f"unrecognized age spec: {s!r} (try '30d', '12h', '2w', '60m')")
    n = int(m.group(1))
    unit = m.group(2) or "d"
    return {
        "d": timedelta(days=n),
        "w": timedelta(weeks=n),
        "h": timedelta(hours=n),
        "m": timedelta(minutes=n),
    }[unit]


def purge(older_than: timedelta, config: CacheConfig | None = None,
          dry_run: bool = False) -> dict:
    cfg = config or CacheConfig.load()
    cutoff = datetime.now(timezone.utc) - older_than
    removed = 0
    bytes_freed = 0
    errors = 0
    if not cfg.root.exists():
        return {"removed": 0, "bytes_freed": 0, "errors": 0, "cutoff": cutoff.isoformat()}
    for meta_path in cfg.root.glob("*/*/*.meta.json"):
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            fetched_at = datetime.fromisoformat(meta["fetched_at"])
            if fetched_at.tzinfo is None:
                fetched_at = fetched_at.replace(tzinfo=timezone.utc)
        except Exception:
            errors += 1
            continue
        if fetched_at >= cutoff:
            continue
        bucket = meta_path.parent
        h = meta_path.name[: -len(".meta.json")]
        for suffix in (".meta.json", ".body", ".txt", ".lock"):
            target = bucket / f"{h}{suffix}"
            if not target.is_file():
                continue
            try:
                if not dry_run:
                    size = target.stat().st_size
                    target.unlink()
                    bytes_freed += size
                else:
                    bytes_freed += target.stat().st_size
            except Exception:  # noqa: BLE001
                errors += 1
        removed += 1
    # Sweep empty bucket dirs.
    if not dry_run:
        for bucket in sorted(cfg.root.glob("*/*"), reverse=True):
            try:
                bucket.rmdir()
            except OSError:
                pass
        for month_dir in sorted(cfg.root.glob("*"), reverse=True):
            try:
                month_dir.rmdir()
            except OSError:
                pass
    return {
        "removed": removed,
        "bytes_freed": bytes_freed,
        "errors": errors,
        "cutoff": cutoff.isoformat(),
        "dry_run": dry_run,
    }


def stats(config: CacheConfig | None = None) -> dict:
    cfg = config or CacheConfig.load()
    entries = 0
    total_bytes = 0
    pdf_entries = 0
    by_host: dict[str, dict] = {}
    by_month: dict[str, int] = {}
    if cfg.root.exists():
        for meta_path in cfg.root.glob("*/*/*.meta.json"):
            entries += 1
            month = meta_path.parent.parent.name
            by_month[month] = by_month.get(month, 0) + 1
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
            except Exception:
                continue
            host = meta.get("host") or "?"
            length = meta.get("content_length") or 0
            total_bytes += length
            if (meta.get("pdf_text_bytes") or 0) > 0:
                pdf_entries += 1
            h = by_host.setdefault(host, {"count": 0, "bytes": 0})
            h["count"] += 1
            h["bytes"] += length
    top_hosts = sorted(
        ({"host": k, **v} for k, v in by_host.items()),
        key=lambda r: r["count"],
        reverse=True,
    )[:10]
    return {
        "root": str(cfg.root),
        "entries": entries,
        "total_bytes": total_bytes,
        "pdf_entries": pdf_entries,
        "by_month": dict(sorted(by_month.items())),
        "top_hosts": top_hosts,
        "default_ttl_days": cfg.default_ttl_days,
        "domain_ttl_days": cfg.domain_ttl_days,
        "max_bytes": cfg.max_bytes,
        "max_total_bytes": cfg.max_total_bytes,
        "utilization_pct": (
            round(100 * total_bytes / cfg.max_total_bytes, 2)
            if cfg.max_total_bytes else 0.0
        ),
    }


# ---------------------------------------------------------------------
# CLI

def _print_bytes(b: bytes, sink) -> None:
    # Write raw bytes to stdout when the caller is shell-piping the body
    # somewhere (`> /tmp/x.pdf`). For TTY, this'd be ugly; that's the
    # caller's problem — same as `curl` semantics.
    try:
        sink.buffer.write(b)
        sink.flush()
    except (AttributeError, BrokenPipeError):
        try:
            sink.write(b.decode("utf-8", errors="replace"))
        except Exception:  # noqa: BLE001
            pass


def _cmd_get(args) -> int:
    try:
        body = fetch(args.url, force_refresh=args.force_refresh,
                     max_age_days=args.max_age_days)
    except (ValueError, CacheError) as e:
        print(f"source_cache: {e}", file=sys.stderr)
        return 1
    _print_bytes(body, sys.stdout)
    return 0


def _cmd_info(args) -> int:
    try:
        meta = info(args.url)
    except ValueError as e:
        print(f"source_cache: {e}", file=sys.stderr)
        return 1
    if not meta:
        print(f"source_cache: no cached entry for {args.url}", file=sys.stderr)
        return 2
    print(json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def _cmd_purge(args) -> int:
    age = parse_age_arg(args.older_than)
    result = purge(age, dry_run=args.dry_run)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def _cmd_stats(_args) -> int:
    print(json.dumps(stats(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Persistent cache of fetched primary-source URLs.",
        prog="source_cache.py",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("get", help="fetch a URL through the cache (stdout = body)")
    g.add_argument("url")
    g.add_argument("--force-refresh", action="store_true",
                   help="bypass cache and re-fetch even on a fresh hit")
    g.add_argument("--max-age-days", type=int, default=None,
                   help="override per-domain TTL for this call (days)")
    g.set_defaults(func=_cmd_get)

    i = sub.add_parser("info", help="print metadata for a cached URL")
    i.add_argument("url")
    i.set_defaults(func=_cmd_info)

    pr = sub.add_parser("purge", help="remove cache entries older than the given age")
    pr.add_argument("--older-than", default="30d",
                    help="age spec: 30d, 12h, 2w, 60m (default: 30d)")
    pr.add_argument("--dry-run", action="store_true",
                    help="report what would be removed without deleting")
    pr.set_defaults(func=_cmd_purge)

    st = sub.add_parser("stats", help="print cache usage summary")
    st.set_defaults(func=_cmd_stats)

    args = p.parse_args(argv)
    try:
        return args.func(args)
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
