#!/usr/bin/env python3
"""External production-surface synthetic checks for ara.guzus.xyz.

Unlike ``check_deploy_health.py`` (one manifest freshness probe), this checks
the public contract users and crawlers actually see: canonical HTML routes,
machine-readable discovery files, a real 404, security/cache headers, and the
Cloudflare user-agent policy.  Defaults describe the intentional production
policy.  A policy change must update this file and its tests in the same PR.

The checker is stdlib-only so a scheduled GitHub-hosted watchdog can run it
without executing anything on the self-hosted production runner.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Callable, Iterable, Optional


DEFAULT_BASE_URL = "https://ara.guzus.xyz"
DEFAULT_TIMEOUT_SECONDS = 15.0
# evidence-search.json is intentionally a lazy-loaded full-text corpus. Read
# the whole semantic contract (rather than validating a truncated prefix).
MAX_BODY_BYTES = 16_000_000

BROWSER_UA = "ara-production-synthetic/1.0 (+https://github.com/guzus/ai-research-arm)"


@dataclass(frozen=True)
class Probe:
    name: str
    path: str
    user_agent: str = BROWSER_UA
    expected_status: int = 200
    content_type_prefix: str = ""
    body_contains: str = ""
    json_contract: str = ""
    required_headers: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class Response:
    status: int
    headers: dict[str, str]
    body: str
    truncated: bool = False


@dataclass
class Result:
    name: str
    path: str
    state: str
    detail: str
    status: Optional[int] = None

    @property
    def failed(self) -> bool:
        return self.state != "healthy"


HTML_HEADERS = (
    ("x-content-type-options", "nosniff"),
    ("cache-control", "max-age=0"),
)

ROUTE_PROBES: tuple[Probe, ...] = (
    Probe("home", "/", content_type_prefix="text/html", body_contains="<title", required_headers=HTML_HEADERS),
    Probe("today", "/today", content_type_prefix="text/html", body_contains="<title", required_headers=HTML_HEADERS),
    Probe("twitter", "/twitter", content_type_prefix="text/html", body_contains="<title", required_headers=HTML_HEADERS),
    Probe("models", "/models", content_type_prefix="text/html", body_contains="<title", required_headers=HTML_HEADERS),
    Probe("research", "/research", content_type_prefix="text/html", body_contains="<title", required_headers=HTML_HEADERS),
    Probe("wiki", "/wiki", content_type_prefix="text/html", body_contains="<title", required_headers=HTML_HEADERS),
    Probe("manifest", "/research/manifest.json", content_type_prefix="application/json", body_contains='"generatedAt"'),
    Probe(
        "evidence-search-contract",
        "/research/evidence-search.json",
        content_type_prefix="application/json",
        json_contract="evidence-search-v1",
    ),
    Probe(
        "public-claims-contract",
        "/research/claims/public.json",
        content_type_prefix="application/json",
        json_contract="public-claims-v1",
    ),
    Probe("robots", "/robots.txt", content_type_prefix="text/plain", body_contains="User-agent:"),
    # Caddy currently serves both generated XML artifacts as text/xml. Pin the
    # observed edge contract so a type change is reviewed rather than ignored.
    Probe("sitemap", "/sitemap.xml", content_type_prefix="text/xml", body_contains="<urlset"),
    Probe("feed", "/feed.xml", content_type_prefix="text/xml", body_contains="<rss"),
    Probe("llms", "/llms.txt", content_type_prefix="text/plain", body_contains="#"),
    Probe("real-404", "/__ara_synthetic_missing__", expected_status=404),
)

# Cloudflare policy observed and documented in CLAUDE.md rule 3.  These are
# exact expectations, not a permissive {200,403}: an unnoticed zone-policy
# flip is operationally significant in either direction.
USER_AGENT_PROBES: tuple[Probe, ...] = (
    Probe("ua-googlebot", "/", user_agent="Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"),
    Probe("ua-perplexity", "/", user_agent="PerplexityBot/1.0 (+https://perplexity.ai/perplexitybot)"),
    Probe("ua-claudebot-policy", "/", user_agent="ClaudeBot/1.0", expected_status=403),
    Probe("ua-gptbot-policy", "/", user_agent="GPTBot/1.2", expected_status=403),
    Probe("ua-ccbot-policy", "/", user_agent="CCBot/2.0", expected_status=403),
)

DEFAULT_PROBES = ROUTE_PROBES + USER_AGENT_PROBES


def fetch(probe: Probe, base_url: str, timeout: float = DEFAULT_TIMEOUT_SECONDS) -> Response:
    url = urllib.parse.urljoin(base_url.rstrip("/") + "/", probe.path.lstrip("/"))
    # Unique query defeats accidental edge-cache reuse without changing route.
    sep = "&" if "?" in url else "?"
    url = f"{url}{sep}synthetic={int(time.time() * 1000)}"
    request = urllib.request.Request(
        url,
        headers={"User-Agent": probe.user_agent, "Cache-Control": "no-cache"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read(MAX_BODY_BYTES + 1)
            body = raw[:MAX_BODY_BYTES].decode("utf-8", "replace")
            headers = {str(k).lower(): str(v) for k, v in response.headers.items()}
            return Response(int(response.status), headers, body, len(raw) > MAX_BODY_BYTES)
    except urllib.error.HTTPError as exc:
        raw = exc.read(MAX_BODY_BYTES + 1)
        body = raw[:MAX_BODY_BYTES].decode("utf-8", "replace")
        headers = {str(k).lower(): str(v) for k, v in exc.headers.items()}
        return Response(int(exc.code), headers, body, len(raw) > MAX_BODY_BYTES)


def evaluate_response(probe: Probe, response: Response) -> Result:
    if response.status != probe.expected_status:
        return Result(probe.name, probe.path, "failed", f"HTTP {response.status}, expected {probe.expected_status}", response.status)
    if probe.content_type_prefix:
        actual = response.headers.get("content-type", "")
        if not actual.lower().startswith(probe.content_type_prefix.lower()):
            return Result(probe.name, probe.path, "failed", f"content-type {actual!r}, expected prefix {probe.content_type_prefix!r}", response.status)
    if response.truncated:
        return Result(
            probe.name,
            probe.path,
            "failed",
            f"body exceeds semantic-check limit of {MAX_BODY_BYTES} bytes",
            response.status,
        )
    if probe.body_contains and probe.body_contains.lower() not in response.body.lower():
        return Result(probe.name, probe.path, "failed", f"body missing marker {probe.body_contains!r}", response.status)
    if probe.json_contract:
        problem = validate_json_contract(probe.json_contract, response.body)
        if problem:
            return Result(
                probe.name,
                probe.path,
                "failed",
                f"JSON contract {probe.json_contract}: {problem}",
                response.status,
            )
    for header, marker in probe.required_headers:
        actual = response.headers.get(header, "")
        if marker.lower() not in actual.lower():
            return Result(probe.name, probe.path, "failed", f"header {header}={actual!r} missing {marker!r}", response.status)
    return Result(probe.name, probe.path, "healthy", f"HTTP {response.status}", response.status)


def _object_array(payload: object, key: str) -> tuple[Optional[list[object]], Optional[str]]:
    if not isinstance(payload, dict):
        return None, "$ must be an object"
    if key not in payload:
        return None, f"$.{key} is missing"
    values = payload[key]
    if not isinstance(values, list):
        return None, f"$.{key} must be an array"
    return values, None


def validate_json_contract(contract: str, body: str) -> Optional[str]:
    """Return a precise schema violation, or None for a valid payload.

    These checks pin stable public semantics, not generated counts, copy, or
    ordering. That catches a SPA fallback or provenance regression without
    paging when editorial content naturally changes.
    """
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        return f"$ is not valid JSON ({exc.msg} at line {exc.lineno} column {exc.colno})"

    if contract == "evidence-search-v1":
        entries, problem = _object_array(payload, "entries")
        if problem:
            return problem
        for index, entry in enumerate(entries or []):
            path = f"$.entries[{index}]"
            if not isinstance(entry, dict):
                return f"{path} must be an object"
            if not isinstance(entry.get("type"), str) or not entry["type"]:
                return f"{path}.type must be a non-empty string"
            if entry["type"] == "claim":
                if not isinstance(entry.get("reusable"), bool):
                    return f"{path}.reusable must be a boolean for claim entries"
                for key in ("id", "title", "body", "url"):
                    if not isinstance(entry.get(key), str) or not entry[key]:
                        return f"{path}.{key} must be a non-empty string for claim entries"
        return None

    if contract == "public-claims-v1":
        claims, problem = _object_array(payload, "claims")
        if problem:
            return problem
        for index, claim in enumerate(claims or []):
            path = f"$.claims[{index}]"
            if not isinstance(claim, dict):
                return f"{path} must be an object"
            if not isinstance(claim.get("reusable"), bool):
                return f"{path}.reusable must be a boolean"
            for key in ("article", "claim"):
                if not isinstance(claim.get(key), str) or not claim[key]:
                    return f"{path}.{key} must be a non-empty string"
        return None

    return f"unsupported contract {contract!r}"


def run_probe(
    probe: Probe,
    base_url: str,
    timeout: float,
    fetch_fn: Callable[[Probe, str, float], Response] = fetch,
) -> Result:
    try:
        return evaluate_response(probe, fetch_fn(probe, base_url, timeout))
    except Exception as exc:
        return Result(probe.name, probe.path, "failed", f"fetch error: {type(exc).__name__}: {exc}")


def evaluate(
    probes: Iterable[Probe],
    base_url: str,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    fetch_fn: Callable[[Probe, str, float], Response] = fetch,
) -> list[Result]:
    probe_list = list(probes)
    if fetch_fn is not fetch:  # deterministic tests should remain serial
        return [run_probe(p, base_url, timeout, fetch_fn) for p in probe_list]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futures = [pool.submit(run_probe, p, base_url, timeout, fetch_fn) for p in probe_list]
        return [future.result() for future in futures]


def format_report(results: list[Result]) -> str:
    rows = sorted(results, key=lambda r: (not r.failed, r.name))
    lines = ["| probe | path | state | detail |", "|---|---|---|---|"]
    for result in rows:
        icon = "🔴" if result.failed else "✅"
        lines.append(f"| `{result.name}` | `{result.path}` | {icon} {result.state} | {result.detail} |")
    return "\n".join(lines)


def emit_github_outputs(results: list[Result], report: str, now: datetime) -> None:
    output_path = os.environ.get("GITHUB_OUTPUT")
    if not output_path:
        return
    failures = sorted(r.name for r in results if r.failed)
    delimiter = "__ARA_SYNTHETIC_REPORT__"
    with open(output_path, "a", encoding="utf-8") as handle:
        handle.write(f"alert={'true' if failures else 'false'}\n")
        handle.write(f"failed_probes={','.join(failures)}\n")
        handle.write(f"idempotency_key=production-surface-{now:%Y-%m-%d-%H}-{'-'.join(failures) or 'healthy'}\n")
        handle.write(f"report<<{delimiter}\n{report}\n{delimiter}\n")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--exit-code", action="store_true", help="exit 2 when any probe fails")
    args = parser.parse_args(argv)

    results = evaluate(DEFAULT_PROBES, args.base_url, args.timeout)
    report = format_report(results)
    failures = [result for result in results if result.failed]
    now = datetime.now(timezone.utc)
    emit_github_outputs(results, report, now)
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as handle:
            handle.write(("### 🔴" if failures else "### ✅") + " Production surface\n\n" + report + "\n")
    if args.json:
        print(json.dumps({"base_url": args.base_url, "failed_probes": [r.name for r in failures], "results": [asdict(r) for r in results]}, indent=2))
    else:
        print(report)
    return 2 if failures and args.exit_code else 0


if __name__ == "__main__":
    raise SystemExit(main())
