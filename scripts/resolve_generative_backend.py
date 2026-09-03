#!/usr/bin/env python3
"""Resolve a generative-research selector from the backend registry.

This is deliberately a data resolver, not a provider plug-in system. A new
model on an existing adapter/provider can be exposed by one backend entry;
new adapters or providers still need explicit credentials and runner code.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FILE = REPO_ROOT / "data" / "agent-backends.json"
SAFE_KEY = re.compile(r"^[a-z0-9][a-z0-9._-]{0,127}$")
SAFE_PROVIDER = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
SAFE_MODEL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]{0,255}$")
PROTOCOLS = {
    ("agent-run", "claude"): {"native-claude": "harness"},
    ("agent-run", "fireworks"): {
        "anthropic-compatible": "scripts/check_fireworks_backend.py"
    },
    ("dispatch-default", "claude"): {"native-claude": "harness"},
    ("dispatch-default", "openai"): {"codex-cli": "harness"},
    ("opencode", "opencode-go"): {
        "openai-chat-completions": "chat/completions",
        "openai-responses": "responses",
    },
    ("cursor", "cursor"): {"cursor-cli": "harness"},
}


class ResolutionError(ValueError):
    pass


@dataclass(frozen=True)
class Selection:
    backend: str
    selector: str
    adapter: str
    provider: str
    model: str
    model_ref: str
    provenance_model: str
    protocol: str
    preflight_path: str
    display_name: str
    production_eligible: bool


def load_config(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ResolutionError(f"cannot read {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ResolutionError(f"{path} must contain a JSON object")
    return data


def _safe_model(value: object, field: str, *, allow_empty: bool = False) -> str:
    if value == "" and allow_empty:
        return ""
    if not isinstance(value, str) or not SAFE_MODEL.fullmatch(value):
        raise ResolutionError(f"{field} is not a safe model identifier")
    if "//" in value or any(part in {"", ".", ".."} for part in value.split("/")):
        raise ResolutionError(f"{field} contains an unsafe path segment")
    return value


def _production_restrictions(backend: dict, backend_key: str) -> list[str]:
    restrictions = backend.get("restrictions", {})
    if not isinstance(restrictions, dict):
        raise ResolutionError(f"backend '{backend_key}' restrictions must be an object")
    active: list[str] = []
    for key, value in restrictions.items():
        if not isinstance(key, str) or not SAFE_KEY.fullmatch(key):
            raise ResolutionError(f"backend '{backend_key}' has an unsafe restriction key")
        if not isinstance(value, bool):
            raise ResolutionError(
                f"backend '{backend_key}' restriction '{key}' must be boolean"
            )
        if value:
            active.append(key)
    return active


def exposed_profiles(data: dict) -> tuple[dict[str, Selection], dict[str, str]]:
    backends = data.get("backends")
    adapters = data.get("adapters")
    if not isinstance(backends, dict):
        raise ResolutionError("routing file has no 'backends' mapping")
    if not isinstance(adapters, dict):
        raise ResolutionError("routing file has no 'adapters' mapping")
    result: dict[str, Selection] = {}
    aliases: dict[str, str] = {}
    for backend_key, backend in backends.items():
        if not isinstance(backend_key, str) or not SAFE_KEY.fullmatch(backend_key):
            raise ResolutionError(f"unsafe backend key {backend_key!r}")
        if not isinstance(backend, dict):
            raise ResolutionError(f"backend '{backend_key}' must be an object")
        generative = backend.get("generative")
        if generative is None:
            continue
        if not isinstance(generative, dict) or generative.get("exposed") is not True:
            raise ResolutionError(
                f"backend '{backend_key}' generative metadata must be exposed=true"
            )
        selector = generative.get("selector")
        adapter = backend.get("adapter")
        provider = backend.get("provider")
        if not isinstance(selector, str) or not SAFE_KEY.fullmatch(selector):
            raise ResolutionError(f"backend '{backend_key}' has unsafe generative selector")
        if not isinstance(adapter, str) or not SAFE_KEY.fullmatch(adapter):
            raise ResolutionError(f"backend '{backend_key}' has unsafe adapter")
        if not isinstance(provider, str) or not SAFE_PROVIDER.fullmatch(provider):
            raise ResolutionError(f"backend '{backend_key}' has unsafe provider")
        adapter_spec = adapters.get(adapter)
        if not isinstance(adapter_spec, dict):
            raise ResolutionError(f"backend '{backend_key}' uses an unregistered adapter")
        implementation = adapter_spec.get("implementation")
        if not isinstance(implementation, str) or not implementation or "\n" in implementation:
            raise ResolutionError(f"adapter '{adapter}' has no safe implementation")
        credentials = adapter_spec.get("provider_credentials")
        if not isinstance(credentials, dict):
            raise ResolutionError(f"adapter '{adapter}' has no provider credential registry")
        if adapter != "dispatch-default" and not isinstance(credentials.get(provider), str):
            raise ResolutionError(
                f"adapter '{adapter}' has no credential binding for provider '{provider}'"
            )
        model = _safe_model(backend.get("model"), f"backend '{backend_key}' model", allow_empty=True)
        provenance = _safe_model(
            generative.get("provenance_model"),
            f"backend '{backend_key}' provenance_model",
        )
        protocol = generative.get("protocol")
        preflight = generative.get("preflight_path")
        allowed = PROTOCOLS.get((adapter, provider))
        if not allowed or protocol not in allowed or preflight != allowed[protocol]:
            raise ResolutionError(
                f"backend '{backend_key}' has unsupported adapter/provider/protocol/preflight"
            )
        display_name = backend.get("display_name")
        if not isinstance(display_name, str) or not display_name or "\n" in display_name:
            raise ResolutionError(f"backend '{backend_key}' has unsafe display_name")
        if not isinstance(backend.get("production_eligible"), bool):
            raise ResolutionError(
                f"backend '{backend_key}' production_eligible must be boolean"
            )
        restrictions = _production_restrictions(backend, backend_key)
        if backend.get("production_eligible") is True and restrictions:
            raise ResolutionError(
                f"backend '{backend_key}' cannot be production-eligible while restrictions "
                f"are active: {', '.join(restrictions)}"
            )
        if adapter == "cursor" and "/" in model:
            raise ResolutionError(
                f"backend '{backend_key}' Cursor model must be one CLI model id"
            )
        if adapter in {"opencode", "cursor"} and provenance != model:
            raise ResolutionError(
                f"backend '{backend_key}' provenance_model must equal the served model "
                f"for adapter '{adapter}'"
            )
        selection = Selection(
            backend=backend_key,
            selector=selector,
            adapter=adapter,
            provider=provider,
            model=model,
            model_ref=f"{provider}/{model}" if model else "",
            provenance_model=provenance,
            protocol=protocol,
            preflight_path=preflight,
            display_name=display_name,
            production_eligible=backend.get("production_eligible") is True,
        )
        result[backend_key] = selection
        candidates = [backend_key, selector]
        candidates.extend(backend.get("aliases") or [])
        candidates.extend(generative.get("aliases") or [])
        for candidate in candidates:
            if not isinstance(candidate, str) or not SAFE_KEY.fullmatch(candidate):
                raise ResolutionError(f"backend '{backend_key}' has unsafe selector alias")
            owner = aliases.setdefault(candidate, backend_key)
            if owner != backend_key:
                raise ResolutionError(
                    f"selector '{candidate}' is ambiguous between '{owner}' and '{backend_key}'"
                )
    return result, aliases


def resolve(data: dict, requested: str) -> Selection:
    is_default = requested == "default"
    if is_default:
        lanes = data.get("lanes") or {}
        lane = lanes.get("generative-research-default") or {}
        requested = lane.get("backend")
    if not isinstance(requested, str) or not SAFE_KEY.fullmatch(requested):
        raise ResolutionError("selector is empty or contains unsafe characters")
    profiles, aliases = exposed_profiles(data)
    backend_key = aliases.get(requested)
    if backend_key is None:
        raise ResolutionError(f"unknown or non-exposed generative backend '{requested}'")
    selection = profiles[backend_key]
    if is_default and not selection.production_eligible:
        raise ResolutionError(
            f"default generative backend '{backend_key}' is not production-eligible"
        )
    return selection


def write_outputs(path: Path, selection: Selection) -> None:
    values = asdict(selection)
    values["production_eligible"] = str(selection.production_eligible).lower()
    with path.open("a", encoding="utf-8") as handle:
        for key, value in values.items():
            handle.write(f"{key}={' '.join(str(value).splitlines())}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("selector")
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE)
    parser.add_argument("--field", choices=list(Selection.__dataclass_fields__))
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args(argv)
    try:
        selection = resolve(load_config(args.file), args.selector)
    except ResolutionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.github_output:
        write_outputs(args.github_output, selection)
    if args.field:
        value = getattr(selection, args.field)
        print(str(value).lower() if isinstance(value, bool) else value)
    elif not args.github_output:
        print(json.dumps(asdict(selection), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
