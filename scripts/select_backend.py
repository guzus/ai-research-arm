#!/usr/bin/env python3
"""Select the effective backend for an agent-run lane by walking the SSOT
fallback chain in order.

Reads data/agent-backends.json (lanes + backends profile table + ordered
fallback chain), probes each candidate's provider for availability, and
emits the first available candidate to $GITHUB_OUTPUT. Called by
`.github/actions/agent-run` as the single backend-selection step.

Candidate order: [requested backend] + fallback.chain, deduplicated (a
zai-primary lane whose chain starts with the same zai backend skips it).
Probes: fireworks → tiny /v1/messages preflight (reuses
check_fireworks_backend); zai → same-shape probe against the Z.ai
Anthropic-compatible endpoint; claude → always available (the OAuth token
is a hard requirement of the action schema).

Strictness: `--fallback-policy none` or a lane with `"strict": true`
disables the chain — the requested backend is the only candidate and its
unavailability fails the run (zai-canary relies on this to stay a
meaningful Z.ai diagnostic).

STDLIB ONLY (plus sibling script imports) — runs on bare python3 on the
runner. Exit codes: 0 selected; 1 no candidate available; 2 config error.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_fireworks_backend import extract_message, redact, request_preflight  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FILE = REPO_ROOT / "data" / "agent-backends.json"

FIREWORKS_ENDPOINT = "https://api.fireworks.ai/inference"
ZAI_ENDPOINT = "https://api.z.ai/api/anthropic"


def config_error(msg: str) -> int:
    print(f"::error::{msg}", file=sys.stderr)
    return 2


def probe_fireworks(model: str) -> tuple[bool, str]:
    api_key = os.environ.get("FIREWORKS_API_KEY", "").strip()
    if not api_key:
        return False, "FIREWORKS_API_KEY is not configured"
    try:
        status, body = request_preflight(FIREWORKS_ENDPOINT, api_key, model)
    except Exception as exc:  # noqa: BLE001 - a probe must not crash selection
        return False, f"preflight request failed: {redact(str(exc))}"
    if 200 <= status < 300:
        return True, f"HTTP {status}"
    return False, f"HTTP {status}: {extract_message(status, body)}"


def probe_zai(model: str) -> tuple[bool, str]:
    api_key = os.environ.get("ZAI_API_KEY", "").strip()
    if not api_key:
        return False, "ZAI_API_KEY is not configured"
    try:
        status, body = request_preflight(ZAI_ENDPOINT, api_key, model)
    except Exception as exc:  # noqa: BLE001
        return False, f"preflight request failed: {redact(str(exc))}"
    if 200 <= status < 300:
        return True, f"HTTP {status}"
    return False, f"HTTP {status}: {extract_message(status, body)}"


def probe_claude(model: str) -> tuple[bool, str]:
    return True, "native path (claude-code-action OAuth)"


PROBES = {
    "fireworks": probe_fireworks,
    "zai": probe_zai,
    "claude": probe_claude,
}


def normalize(selector: str, backends: dict[str, dict]) -> str | None:
    selector = selector.strip()
    if selector in backends:
        return selector
    for key, spec in backends.items():
        if selector in (spec.get("aliases") or []):
            return key
    return None


def write_outputs(path: Path | None, outputs: dict[str, str]) -> None:
    if not path:
        return
    with path.open("a") as handle:
        for key, value in outputs.items():
            # single-line sanitization: a newline in a JSON-sourced value must
            # not be able to inject extra output keys
            handle.write(f"{key}={' '.join(str(value).splitlines())}\n")


def main_with_args(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lane", default="", help="lane key in data/agent-backends.json")
    parser.add_argument("--backend", default="",
                        help="explicit backend selector (bypasses lane lookup)")
    parser.add_argument("--fallback-policy", default="claude",
                        choices=["claude", "none"],
                        help="claude = walk the SSOT fallback chain; none = strict")
    parser.add_argument("--native-model-override", default="")
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE)
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args(argv)

    try:
        data = json.loads(args.file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return config_error(f"cannot read {args.file}: {exc}")

    backends = data.get("backends") or {}
    fallback = data.get("fallback") or {}
    lanes = data.get("lanes") or {}
    if not backends:
        return config_error(f"{args.file} has no 'backends' profile table")

    strict = args.fallback_policy == "none"
    if args.backend:
        requested = normalize(args.backend, backends)
        if requested is None:
            return config_error(f"unknown backend selector '{args.backend}'")
    elif args.lane:
        lane = lanes.get(args.lane)
        if lane is None:
            known = ", ".join(sorted(k for k, l in lanes.items()
                                     if l.get("harness") == "agent-run"))
            return config_error(f"unknown lane '{args.lane}'. Known agent-run lanes: {known}")
        if lane.get("harness") != "agent-run":
            return config_error(f"lane '{args.lane}' has harness '{lane.get('harness')}' — "
                                "only agent-run lanes are runtime-selected")
        requested = normalize(str(lane.get("backend", "")), backends)
        if requested is None:
            return config_error(f"lane '{args.lane}' backend '{lane.get('backend')}' is not "
                                "in the backends table")
        if lane.get("strict"):
            strict = True
    else:
        return config_error("one of --lane or --backend is required")

    chain: list[str] = [] if strict else list(fallback.get("chain") or [])
    candidates: list[str] = []
    for selector in [requested, *chain]:
        key = normalize(str(selector), backends)
        if key is None:
            return config_error(f"fallback chain entry '{selector}' is not in the backends table")
        if key not in candidates:
            candidates.append(key)

    chosen = None
    for key in candidates:
        spec = backends[key]
        provider = str(spec.get("provider", ""))
        probe = PROBES.get(provider)
        if probe is None:
            return config_error(f"backend '{key}' has unknown provider '{provider}'")
        available, reason = probe(str(spec.get("model", "")))
        marker = "available" if available else "UNAVAILABLE"
        print(f"candidate {key} ({provider}): {marker} — {reason}")
        if available:
            chosen = key
            break

    if chosen is None:
        print(f"::error::no available backend: walked {len(candidates)} candidate(s) "
              f"({', '.join(candidates)}) and every provider probe failed. "
              "Fix the providers or extend fallback.chain in data/agent-backends.json.",
              file=sys.stderr)
        return 1

    spec = backends[chosen]
    native_model = args.native_model_override or str(fallback.get("native_model", ""))
    if not native_model:
        return config_error("fallback.native_model is not set in data/agent-backends.json")
    used_fallback = chosen != requested
    if used_fallback:
        print(f"::warning::requested backend '{requested}' unavailable; "
              f"selected '{chosen}' from the SSOT fallback chain.")

    write_outputs(args.github_output, {
        "requested-backend": requested,
        "backend": chosen,
        "provider": str(spec.get("provider", "")),
        "model-id": str(spec.get("model", "")),
        "display-name": str(spec.get("display_name", chosen)),
        "native-model": native_model,
        "used-fallback": str(used_fallback).lower(),
    })
    print(f"Selected backend: {spec.get('display_name', chosen)} "
          f"(requested {requested}{', fell back' if used_fallback else ''})")
    return 0


def main() -> int:
    return main_with_args()


if __name__ == "__main__":
    sys.exit(main())
