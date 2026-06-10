#!/usr/bin/env python3
"""Deploy-health watchdog (advisory): is the artifact users see current?

The other two watchdogs measure the REPOSITORY: check_lane_freshness.py
asks "did each lane commit recently?", check_lane_content.py asks "was the
latest artifact non-empty?". Neither can see the failure mode that actually
happened (2026-06-09→10): the Railway Docker build broke on every push
after #102, so ara.guzus.xyz silently served a day-old build while the repo
stayed perfectly fresh and green. Repo healthy, deploy dead, zero alarms.

This script closes that gap by reading the LIVE site, not the repo:
dashboard/scripts/prebuild.mjs stamps the manifest it emits with
`generatedAt` (build wall-clock, ISO-8601 UTC). We fetch the deployed
manifest and compute `lag = now - generatedAt`.

Why the lag threshold works for THIS repo (no false positives in quiet
periods): the pipeline pushes to main around the clock — over the trailing
10 days, 367 commits with a MAXIMUM gap of ~3.4h between pushes (hourly
RSS is the floor; lane-freshness pages rss at 4h idle anyway). Railway
rebuilds on every push, so on a healthy system lag stays under ~1h and can
never legitimately reach the default 8h threshold (>2x the worst observed
push gap) without something being wrong.

Distinguishing deploy-stale from pipeline-dead (don't double-page): if the
whole pipeline froze, lag grows too — but lane-freshness already owns that
page. So the page-worthy finding requires the repo to be DEMONSTRABLY
alive: `deploy-stale` fires only when lag > threshold AND the last commit
in the checkout is < 2h old (`git log -1 --format=%ct`; the liveness-check
checkout always exists). Big lag + idle repo is reported as
`pipeline-idle (deferring to lane-freshness)` and does not alert.

Defeating the CDN cache (the read must be the ORIGIN's manifest):
Cloudflare fronts the site. Every request appends a unique `cb=<epoch>`
query param (CF's cache key includes the query string by default) and
sends Cache-Control: no-cache; the response's `cf-cache-status` / `age`
headers are captured and reported so a cached read is visible in the
diagnostics (a `HIT` despite the buster gets an explicit warning).
Observed live (2026-06-10): `cf-cache-status: DYNAMIC` — the JSON is not
edge-cached today, but the busting keeps the check correct if a cache rule
ever changes that.

URL choice (verified live, 2026-06-10): the manifest users' dashboards
consume is `/research/manifest.json` (main.ts fetches `${DATA_BASE}/
manifest.json`). The root `/manifest.json` is a trap: the Caddyfile's
`try_files {path} /index.html` SPA fallback serves it as index.html with
HTTP 200, which would JSON-parse-fail forever. Default accordingly;
`--url` overrides.

Findings (state machine):
  healthy                 lag <= threshold (or generatedAt in the future —
                          clock skew is not an outage).
  deploy-stale            ALERT. lag > threshold AND repo alive (< 2h since
                          last commit). The incident this watchdog exists
                          for: pushes flow, builds don't.
  site-unreachable        ALERT. Fetch failed after one retry, or non-200.
  manifest-unparseable    ALERT. Body is not a JSON object (e.g. the SPA
                          fallback served HTML for the manifest path) or
                          `generatedAt` is present but not a timestamp.
  legacy-build            note, NOT a page. Manifest parses but has no
                          `generatedAt` — the live build predates the
                          stamping feature. Disappears after the first
                          successful post-feature deploy.
  pipeline-idle           note, NOT a page. lag > threshold but the repo is
                          idle too — lane-freshness owns that page.

Stdlib-only (urllib.request/json/argparse/datetime) so it runs identically
on both watchdog tiers. All external effects (fetch, git, clock) are
injectable for tests, mirroring check_lane_freshness/check_lane_content.

Exit codes:
  0  default — even on findings (advisory). Findings still surface via
     $GITHUB_OUTPUT (`alert=true`) and the step summary.
  2  an ALERT-class finding, AND --exit-code was passed.
  1  internal error (e.g. malformed --now).
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Optional

# The manifest the dashboard actually consumes (see docstring: root
# /manifest.json is the SPA fallback and serves HTML with HTTP 200).
DEFAULT_URL = "https://ara.guzus.xyz/research/manifest.json"

# lag > this is anomalous. Calibrated to the repo's real push cadence:
# max observed push gap over 10 days is ~3.4h, builds finish in minutes,
# so 8h is >2x the worst legitimate quiet period.
DEFAULT_MAX_LAG_HOURS = 8.0

# The repo counts as "demonstrably alive and pushing" when its last commit
# is younger than this. Under that bound, a healthy deploy chain MUST have
# produced a recent build (pushes flow hourly), so big lag = broken deploys.
DEFAULT_REPO_ALIVE_HOURS = 2.0

DEFAULT_TIMEOUT_SECONDS = 15.0
RETRY_DELAY_SECONDS = 5.0
MAX_BODY_BYTES = 5_000_000  # manifest is ~50KB; cap pathological responses
USER_AGENT = "ara-deploy-health/1.0 (+https://github.com/guzus/ai-research-arm)"

HEALTHY = "healthy"
DEPLOY_STALE = "deploy-stale"
SITE_UNREACHABLE = "site-unreachable"
MANIFEST_UNPARSEABLE = "manifest-unparseable"
LEGACY_BUILD = "legacy-build"
PIPELINE_IDLE = "pipeline-idle"

# Findings that should route an alert. legacy-build and pipeline-idle are
# diagnostic notes by design (see docstring).
ALERTING_STATES = frozenset({DEPLOY_STALE, SITE_UNREACHABLE, MANIFEST_UNPARSEABLE})


class FetchError(Exception):
    """Total fetch failure (after retries). Message carries the last error."""


@dataclass
class FetchResult:
    """A completed HTTP exchange. Header keys are lower-cased."""

    status: int
    headers: dict[str, str]
    body: str


@dataclass
class DeployHealth:
    state: str
    detail: str                              # single line, alert-body ready
    lag_hours: Optional[float] = None
    repo_idle_hours: Optional[float] = None
    generated_at: Optional[str] = None
    git_sha: Optional[str] = None
    cache_status: Optional[str] = None       # cf-cache-status header (or None)
    age: Optional[str] = None                # age header (or None)
    http_status: Optional[int] = None
    url: str = ""

    @property
    def alerting(self) -> bool:
        return self.state in ALERTING_STATES


def with_cache_buster(url: str, epoch: int) -> str:
    """Append a unique cb=<epoch> param (CF's cache key includes the query)."""
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}cb={epoch}"


def fetch_manifest(
    url: str,
    *,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    retries: int = 1,
    opener_fn: Callable = urllib.request.urlopen,
    sleep_fn: Callable[[float], None] = time.sleep,
    epoch_fn: Callable[[], float] = time.time,
) -> FetchResult:
    """Fetch the live manifest with a cache-busting param. One retry.

    Returns a FetchResult on HTTP success; raises FetchError once every
    attempt (initial + `retries`) has failed. HTTP error statuses (urlopen
    raises HTTPError for non-2xx) are retried like network errors — a 502
    from a mid-restart edge is transient — and the final error message
    carries the status code so the finding's detail is diagnosable.
    """
    target = with_cache_buster(url, int(epoch_fn()))
    request = urllib.request.Request(
        target,
        headers={
            "User-Agent": USER_AGENT,
            # CF mostly ignores client cache-control, but it is free and
            # correct to ask; the cb param is the real cache defeat.
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )
    last_error: Optional[BaseException] = None
    for attempt in range(retries + 1):
        if attempt > 0:
            sleep_fn(RETRY_DELAY_SECONDS)
        try:
            with opener_fn(request, timeout=timeout) as resp:
                body = resp.read(MAX_BODY_BYTES).decode("utf-8", "replace")
                headers = {str(k).lower(): str(v) for k, v in resp.headers.items()}
                status = getattr(resp, "status", None)
                if status is None:  # pre-3.9 compat shim; harmless elsewhere
                    status = resp.getcode()
                return FetchResult(status=int(status), headers=headers, body=body)
        except urllib.error.HTTPError as exc:  # non-2xx IS a response; keep code
            last_error = exc
        except Exception as exc:  # URLError, socket timeout, DNS, TLS, ...
            last_error = exc
    attempts = retries + 1
    if isinstance(last_error, urllib.error.HTTPError):
        raise FetchError(
            f"HTTP {last_error.code} after {attempts} attempt(s) for {target}"
        ) from last_error
    raise FetchError(
        f"fetch failed after {attempts} attempt(s) for {target}: {last_error}"
    ) from last_error


def repo_last_commit_epoch(repo_root: str) -> Optional[int]:
    """Epoch of the last commit in the checkout, or None when unavailable.

    `git log -1 --format=%ct` works even on a depth-1 checkout (it only
    needs the tip), so this is robust on both watchdog tiers.
    """
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%ct"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None
    raw = out.stdout.strip()
    try:
        return int(raw)
    except ValueError:
        return None


def parse_iso8601(value: str) -> Optional[datetime]:
    """Parse an ISO-8601 timestamp; tolerate the trailing 'Z' that
    `Date.prototype.toISOString()` emits (Python <3.11 fromisoformat
    rejects it). Naive values are assumed UTC."""
    if not isinstance(value, str) or not value:
        return None
    raw = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _fmt_hours(hours: Optional[float]) -> str:
    if hours is None:
        return "?"
    if hours < 48:
        return f"{hours:.1f}h"
    return f"{hours / 24:.1f}d"


def cache_note(headers: dict[str, str]) -> str:
    """Single-line CDN-cache diagnostic. Must not crash on absent headers."""
    status = headers.get("cf-cache-status", "absent")
    age = headers.get("age", "absent")
    note = f"cf-cache-status={status} age={age}"
    if status.upper() == "HIT":
        note += (
            " (WARNING: cache HIT despite the cb cache-buster — this read may"
            " be a stale edge copy; check Cloudflare cache rules)"
        )
    return note


def evaluate(
    *,
    url: str = DEFAULT_URL,
    max_lag_hours: float = DEFAULT_MAX_LAG_HOURS,
    repo_alive_hours: float = DEFAULT_REPO_ALIVE_HOURS,
    now: Optional[datetime] = None,
    fetch_fn: Callable[[str], FetchResult],
    git_time_fn: Callable[[], Optional[int]],
) -> DeployHealth:
    """Classify the live deploy. fetch_fn/git_time_fn/now are injectable so
    the logic is unit-testable without network or a repository (mirrors the
    age_fn/sizes_fn seams in the sibling watchdogs)."""
    now = now or datetime.now(timezone.utc)

    # 1) Reach the site. Any exception out of the fetch seam (the real
    #    impl already retried) means users may not be reaching it either.
    try:
        result = fetch_fn(url)
    except Exception as exc:
        return DeployHealth(
            state=SITE_UNREACHABLE,
            detail=f"could not fetch live manifest: {exc}",
            url=url,
        )

    cache_status = result.headers.get("cf-cache-status")
    age = result.headers.get("age")
    base = dict(cache_status=cache_status, age=age, http_status=result.status, url=url)

    if result.status != 200:
        return DeployHealth(
            state=SITE_UNREACHABLE,
            detail=f"live manifest returned HTTP {result.status} (expected 200)",
            **base,
        )

    # 2) Parse. The SPA fallback serves index.html with HTTP 200 for missing
    #    paths (Caddyfile try_files), so "200 but HTML" is a real deployed-
    #    artifact failure shape, not a transport error.
    try:
        manifest = json.loads(result.body)
    except ValueError:
        snippet = result.body[:60].replace("\n", " ")
        content_type = result.headers.get("content-type", "absent")
        return DeployHealth(
            state=MANIFEST_UNPARSEABLE,
            detail=(
                f"live manifest is not JSON (content-type={content_type}; "
                f"body starts {snippet!r}) — is the static file route broken?"
            ),
            **base,
        )
    if not isinstance(manifest, dict):
        return DeployHealth(
            state=MANIFEST_UNPARSEABLE,
            detail=f"live manifest is JSON but not an object (got {type(manifest).__name__})",
            **base,
        )

    git_sha = manifest.get("gitSha")
    base["git_sha"] = git_sha if isinstance(git_sha, str) else None

    # 3) The stamp. Absent => the live build predates this feature: an
    #    expected, self-resolving state right after this PR ships — note it,
    #    never page on it.
    if "generatedAt" not in manifest:
        return DeployHealth(
            state=LEGACY_BUILD,
            detail=(
                "live manifest has no generatedAt — the deployed build predates "
                "the deploy-health stamp; this resolves on the first successful "
                "post-feature deploy (advisory note, not a page)"
            ),
            **base,
        )

    raw_generated_at = manifest.get("generatedAt")
    generated_at = parse_iso8601(raw_generated_at)
    if generated_at is None:
        return DeployHealth(
            state=MANIFEST_UNPARSEABLE,
            detail=(
                f"live manifest generatedAt is not a parseable ISO-8601 "
                f"timestamp: {raw_generated_at!r}"
            ),
            **base,
        )
    base["generated_at"] = generated_at.isoformat()

    # 4) The signal: how old is the artifact users see?
    lag_hours = (now - generated_at).total_seconds() / 3600.0
    base["lag_hours"] = lag_hours

    if lag_hours < 0:
        return DeployHealth(
            state=HEALTHY,
            detail=(
                f"live build generatedAt is {_fmt_hours(-lag_hours)} in the "
                "future (clock skew between builder and checker) — treating as fresh"
            ),
            **base,
        )
    if lag_hours <= max_lag_hours:
        return DeployHealth(
            state=HEALTHY,
            detail=(
                f"live build is {_fmt_hours(lag_hours)} old "
                f"(within the {max_lag_hours:g}h threshold)"
            ),
            **base,
        )

    # 5) lag is anomalous. Page only when the repo is demonstrably pushing —
    #    otherwise lane-freshness owns the page (premise c: don't double-page).
    last_commit_epoch = git_time_fn()
    repo_idle_hours: Optional[float] = None
    if last_commit_epoch is not None:
        repo_idle_hours = (now.timestamp() - last_commit_epoch) / 3600.0
    base["repo_idle_hours"] = repo_idle_hours

    if repo_idle_hours is None:
        # Only reachable outside the wired environment (liveness-check always
        # has a checkout). The lag is real; surface it with the caveat rather
        # than swallowing a genuine deploy outage.
        return DeployHealth(
            state=DEPLOY_STALE,
            detail=(
                f"live build is {_fmt_hours(lag_hours)} old (> {max_lag_hours:g}h) "
                "and repo liveness is UNKNOWN (git unavailable) — cannot apply "
                "the pipeline-idle deferral; treat as deploy-stale"
            ),
            **base,
        )
    if repo_idle_hours < repo_alive_hours:
        return DeployHealth(
            state=DEPLOY_STALE,
            detail=(
                f"live build is {_fmt_hours(lag_hours)} old (> {max_lag_hours:g}h) "
                f"while the repo pushed {_fmt_hours(repo_idle_hours)} ago — "
                "pushes are flowing but deploys are not (check the Railway "
                "build: Dockerfile / bun build / Caddy image)"
            ),
            **base,
        )
    return DeployHealth(
        state=PIPELINE_IDLE,
        detail=(
            f"live build is {_fmt_hours(lag_hours)} old but the repo has also "
            f"been idle {_fmt_hours(repo_idle_hours)} (>= {repo_alive_hours:g}h) "
            "— pipeline-idle (deferring to lane-freshness, which owns that page)"
        ),
        **base,
    )


def format_report(health: DeployHealth) -> str:
    """Multi-line diagnostics block for the step summary / alert context."""
    icon = {
        HEALTHY: "✅",
        DEPLOY_STALE: "🔴",
        SITE_UNREACHABLE: "🔴",
        MANIFEST_UNPARSEABLE: "🔴",
        LEGACY_BUILD: "⚪",
        PIPELINE_IDLE: "🟡",
    }
    headers: dict[str, str] = {}
    if health.cache_status is not None:
        headers["cf-cache-status"] = health.cache_status
    if health.age is not None:
        headers["age"] = health.age
    lines = [
        f"{icon.get(health.state, '?')} {health.state}: {health.detail}",
        f"- url: {health.url or '?'}",
        f"- http_status: {health.http_status if health.http_status is not None else '?'}",
        f"- generatedAt: {health.generated_at or 'absent'}",
        f"- lag: {_fmt_hours(health.lag_hours)}",
        f"- repo idle: {_fmt_hours(health.repo_idle_hours)}",
        f"- gitSha: {health.git_sha or 'absent'}",
        f"- cache: {cache_note(headers)}",
    ]
    return "\n".join(lines)


def idempotency_key(state: str, now: datetime) -> str:
    """Per-day, per-finding key so both watchdog tiers (and repeat runs the
    same day) collapse to one delivered alert; a different finding the same
    day produces a new key. Distinct prefix so deploy-health alerts never
    collide with lane-freshness/lane-content keys."""
    return f"deploy-health-{now.strftime('%Y-%m-%d')}-{state}"


def _emit_github_output(health: DeployHealth, report: str, key: str) -> None:
    out_path = os.environ.get("GITHUB_OUTPUT")
    if not out_path:
        return
    delim = "__ARA_DEPLOY_HEALTH_EOF__"
    with open(out_path, "a", encoding="utf-8") as fh:
        fh.write(f"finding={health.state}\n")
        fh.write(f"alert={'true' if health.alerting else 'false'}\n")
        fh.write(f"idempotency_key={key}\n")
        fh.write(f"detail={health.detail}\n")
        fh.write(f"report<<{delim}\n{report}\n{delim}\n")


def _emit_step_summary(report: str, health: DeployHealth) -> None:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    if health.alerting:
        header = f"### 🔴 Deploy health: {health.state} (advisory)\n\n"
    elif health.state == HEALTHY:
        header = "### ✅ Deploy health: live build is current\n\n"
    else:
        header = f"### ⚪ Deploy health: {health.state} (note)\n\n"
    with open(summary_path, "a", encoding="utf-8") as fh:
        fh.write(header + report + "\n")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Deploy-health watchdog: is the live site serving a current build? (advisory)",
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help=f"Live manifest URL (default: {DEFAULT_URL}; root /manifest.json "
        "is the SPA fallback and serves HTML — do not point there).",
    )
    parser.add_argument(
        "--max-lag-hours",
        type=float,
        default=DEFAULT_MAX_LAG_HOURS,
        help=f"Max tolerated build age before the lag is anomalous (default: {DEFAULT_MAX_LAG_HOURS:g}).",
    )
    parser.add_argument(
        "--repo-alive-hours",
        type=float,
        default=DEFAULT_REPO_ALIVE_HOURS,
        help="Repo counts as alive-and-pushing when its last commit is younger "
        f"than this; gates the deploy-stale page (default: {DEFAULT_REPO_ALIVE_HOURS:g}).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"Per-attempt fetch timeout in seconds (default: {DEFAULT_TIMEOUT_SECONDS:g}).",
    )
    parser.add_argument(
        "--now",
        help="ISO-8601 UTC timestamp to evaluate against (default: now). For testing.",
    )
    parser.add_argument(
        "--repo",
        default=None,
        help="Repository root for the repo-liveness probe (default: git toplevel of CWD, else CWD).",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of the report.")
    parser.add_argument(
        "--exit-code",
        action="store_true",
        help="Exit 2 on an alert-class finding (default: always exit 0 — advisory).",
    )
    args = parser.parse_args(argv)

    if args.now:
        # Python <3.11's fromisoformat rejects a trailing 'Z'; normalize it.
        now_dt = parse_iso8601(args.now)
        if now_dt is None:
            print(f"error: --now is not a valid ISO-8601 timestamp: {args.now}", file=sys.stderr)
            return 1
    else:
        now_dt = datetime.now(timezone.utc)

    repo_root = args.repo
    if repo_root is None:
        try:
            top = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True, text=True, check=True,
            ).stdout.strip()
            repo_root = top or os.getcwd()
        except (subprocess.CalledProcessError, FileNotFoundError, OSError):
            repo_root = os.getcwd()

    health = evaluate(
        url=args.url,
        max_lag_hours=args.max_lag_hours,
        repo_alive_hours=args.repo_alive_hours,
        now=now_dt,
        fetch_fn=lambda url: fetch_manifest(url, timeout=args.timeout),
        git_time_fn=lambda: repo_last_commit_epoch(repo_root),
    )
    report = format_report(health)
    key = idempotency_key(health.state, now_dt)

    if args.json:
        print(
            json.dumps(
                {
                    "now": now_dt.isoformat(),
                    "finding": health.state,
                    "alert": health.alerting,
                    "detail": health.detail,
                    "idempotency_key": key,
                    "url": health.url,
                    "http_status": health.http_status,
                    "generated_at": health.generated_at,
                    "lag_hours": health.lag_hours,
                    "repo_idle_hours": health.repo_idle_hours,
                    "git_sha": health.git_sha,
                    "cf_cache_status": health.cache_status,
                    "age": health.age,
                },
                indent=2,
            )
        )
    else:
        print(report)

    _emit_github_output(health, report, key)
    _emit_step_summary(report, health)

    if health.alerting:
        print(
            f"\n::warning::deploy-health finding: {health.state} "
            "(advisory — does not fail the job)",
            file=sys.stderr,
        )
        return 2 if args.exit_code else 0
    if health.state in (LEGACY_BUILD, PIPELINE_IDLE):
        print(f"\ndeploy-health note: {health.state} (no alert)", file=sys.stderr)
    else:
        print("\nlive deploy is current", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
