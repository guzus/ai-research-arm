#!/usr/bin/env python3
"""Resolve a runtime-dispatched lane through lane -> route -> backend.

The routing SSOT deliberately separates four concerns:

* a lane owns workflow identity and points at a route;
* a route owns the requested backend and fallback policy;
* a backend profile owns adapter, provider, and model;
* backend capabilities say whether that adapter is safe for untrusted
  editorial inputs.

That split makes a registered harness/model change a data edit.  The workflow
continues to own its prompt, dated paths, staged inputs, timeout, and trusted
post-processing because those are lane I/O, not provider routing.

Only isolated adapters implemented by agent-dispatch are accepted here.
OpenCode and Cursor CLI routes fail closed: cross-adapter fallback would
require a second containment boundary and is not silently inferred from the
global agent-run chain.  The host-checkout agent-run adapter is deliberately
incompatible.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FILE = REPO_ROOT / "data" / "agent-backends.json"
SUPPORTED_ADAPTERS = {"opencode", "cursor"}
SUPPORTED_FALLBACKS = {"global", "none"}


class RouteError(ValueError):
    """The SSOT cannot produce a safe executable route."""


@dataclass(frozen=True)
class RouteSelection:
    lane: str
    route: str
    contract: str
    backend: str
    adapter: str
    provider: str
    credential: str
    model: str
    model_ref: str
    fallback: str
    strict: bool


def load_config(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RouteError(f"cannot read {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise RouteError(f"{path} must contain a JSON object")
    return data


def resolve_route(data: dict, lane_key: str) -> RouteSelection:
    lanes = data.get("lanes")
    routes = data.get("routes")
    backends = data.get("backends")
    adapters = data.get("adapters")
    if not isinstance(lanes, dict):
        raise RouteError("routing file has no 'lanes' mapping")
    if not isinstance(routes, dict):
        raise RouteError("routing file has no 'routes' mapping")
    if not isinstance(backends, dict):
        raise RouteError("routing file has no 'backends' mapping")
    if not isinstance(adapters, dict):
        raise RouteError("routing file has no 'adapters' mapping")

    lane = lanes.get(lane_key)
    if not isinstance(lane, dict):
        raise RouteError(f"unknown lane '{lane_key}'")
    route_key = lane.get("route")
    if not isinstance(route_key, str) or not route_key:
        raise RouteError(f"lane '{lane_key}' has no non-empty route reference")

    route = routes.get(route_key)
    if not isinstance(route, dict):
        raise RouteError(f"lane '{lane_key}' references unknown route '{route_key}'")
    backend_key = route.get("backend")
    if not isinstance(backend_key, str) or not backend_key:
        raise RouteError(f"route '{route_key}' has no non-empty backend reference")
    contract = route.get("contract")
    if contract != "research-editorial":
        raise RouteError(
            f"route '{route_key}' contract must be 'research-editorial'"
        )
    fallback = route.get("fallback")
    if fallback not in SUPPORTED_FALLBACKS:
        raise RouteError(
            f"route '{route_key}' fallback must be one of {sorted(SUPPORTED_FALLBACKS)}"
        )

    backend = backends.get(backend_key)
    if not isinstance(backend, dict):
        raise RouteError(f"route '{route_key}' references unknown backend '{backend_key}'")
    adapter = backend.get("adapter")
    capabilities = adapters.get(adapter)
    if not isinstance(capabilities, dict):
        raise RouteError(
            f"backend '{backend_key}' references unknown adapter '{adapter}'"
        )
    for capability in ("isolated_workspace", "editorial_contract"):
        if capabilities.get(capability) is not True:
            raise RouteError(
                f"backend '{backend_key}' is incompatible with research-editorial: "
                f"capability '{capability}' must be true"
            )
    if adapter not in SUPPORTED_ADAPTERS:
        raise RouteError(
            f"backend '{backend_key}' adapter '{adapter}' is not supported by agent-dispatch"
        )
    provider = backend.get("provider")
    if not isinstance(provider, str) or not provider:
        raise RouteError(f"backend '{backend_key}' has no provider")
    provider_credentials = capabilities.get("provider_credentials")
    if not isinstance(provider_credentials, dict):
        raise RouteError(f"adapter '{adapter}' has no provider_credentials mapping")
    credential = provider_credentials.get(provider)
    if not isinstance(credential, str) or not credential:
        raise RouteError(
            f"adapter '{adapter}' does not bind provider '{provider}' to a credential input"
        )
    model = backend.get("model")
    if not isinstance(model, str):
        raise RouteError(f"backend '{backend_key}' model must be a string")
    model_ref = f"{provider}/{model}" if provider and model else ""

    strict = fallback == "none"
    if adapter == "opencode":
        if not strict:
            raise RouteError(
                f"route '{route_key}' uses opencode but fallback is '{fallback}'; "
                "cross-adapter fallback is unsupported, so opencode routes must use 'none'"
            )
        if provider != "opencode-go" or not model:
            raise RouteError(
                f"backend '{backend_key}' must declare provider 'opencode-go' and a "
                "non-empty model; model_ref is derived as provider/model"
            )
        if credential != "opencode-api-key":
            raise RouteError(
                "opencode-go must bind exactly to dispatcher input opencode-api-key"
            )
    if adapter == "cursor":
        if not strict:
            raise RouteError(
                f"route '{route_key}' uses cursor but fallback is '{fallback}'; "
                "cross-adapter fallback is unsupported, so cursor routes must use 'none'"
            )
        if provider != "cursor" or not model:
            raise RouteError(
                f"backend '{backend_key}' must declare provider 'cursor' and a "
                "non-empty model; model_ref is derived as provider/model"
            )
        if credential != "cursor-api-key":
            raise RouteError(
                "cursor must bind exactly to dispatcher input cursor-api-key"
            )
    return RouteSelection(
        lane=lane_key,
        route=route_key,
        contract=contract,
        backend=backend_key,
        adapter=adapter,
        provider=provider,
        credential=credential,
        model=model,
        model_ref=model_ref,
        fallback=fallback,
        strict=strict,
    )


def write_github_outputs(path: Path, selection: RouteSelection) -> None:
    outputs = {
        **asdict(selection),
        "strict": str(selection.strict).lower(),
    }
    with path.open("a", encoding="utf-8") as handle:
        for key, value in outputs.items():
            handle.write(f"{key}={' '.join(str(value).splitlines())}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lane", help="lane key in data/agent-backends.json")
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE)
    parser.add_argument("--field", choices=[
        "lane", "route", "contract", "backend", "adapter", "provider", "credential", "model",
        "model_ref", "fallback", "strict",
    ])
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args(argv)

    try:
        selection = resolve_route(load_config(args.file), args.lane)
    except RouteError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.github_output:
        write_github_outputs(args.github_output, selection)
    if args.field:
        value = getattr(selection, args.field)
        print(str(value).lower() if isinstance(value, bool) else value)
    elif not args.github_output:
        print(json.dumps(asdict(selection), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
