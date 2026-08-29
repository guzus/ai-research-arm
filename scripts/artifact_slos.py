#!/usr/bin/env python3
"""Load and validate the machine-readable artifact/SLO registry."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = REPO_ROOT / "data" / "artifact-slos.json"
CADENCE_KINDS = {"interval", "daily", "event", "on_demand"}


def load_registry(path: Path | str = DEFAULT_REGISTRY) -> list[dict[str, Any]]:
    source = Path(path)
    payload = json.loads(source.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1 or not isinstance(payload.get("artifacts"), list):
        raise ValueError(f"{source}: expected schema_version=1 and artifacts[]")
    seen: set[str] = set()
    for entry in payload["artifacts"]:
        if not isinstance(entry, dict):
            raise ValueError(f"{source}: every artifacts[] entry must be an object")
        artifact_id = entry.get("id")
        if not isinstance(artifact_id, str) or not artifact_id or artifact_id in seen:
            raise ValueError(f"{source}: artifact id is missing or duplicated: {artifact_id!r}")
        seen.add(artifact_id)
        for field in ("producer", "artifacts", "freshness_paths", "validators", "degraded_policy"):
            if field not in entry:
                raise ValueError(f"{source}: {artifact_id} missing {field}")
        if not isinstance(entry["producer"], str) or not entry["producer"]:
            raise ValueError(f"{source}: {artifact_id} producer must be a non-empty string")
        for field in ("artifacts", "freshness_paths", "validators"):
            if not isinstance(entry[field], list) or not all(
                isinstance(value, str) and value for value in entry[field]
            ):
                raise ValueError(f"{source}: {artifact_id} {field} must be a string list")
        if not isinstance(entry["degraded_policy"], str) or not entry["degraded_policy"]:
            raise ValueError(f"{source}: {artifact_id} degraded_policy must be a non-empty string")
        cadence = entry.get("cadence")
        if not isinstance(cadence, dict) or cadence.get("kind") not in CADENCE_KINDS:
            raise ValueError(f"{source}: {artifact_id} has invalid cadence")
        threshold = cadence.get("freshness_slo_hours")
        if cadence["kind"] in {"interval", "daily"} and not isinstance(threshold, (int, float)):
            raise ValueError(f"{source}: {artifact_id} fixed cadence needs freshness_slo_hours")
        if cadence["kind"] in {"event", "on_demand"} and threshold is not None:
            raise ValueError(f"{source}: {artifact_id} non-fixed cadence must not define freshness SLO")
        content = entry.get("content")
        if content is not None:
            if not isinstance(content, dict) or not isinstance(content.get("primary_glob"), str):
                raise ValueError(f"{source}: {artifact_id} content needs primary_glob")
            if not isinstance(content.get("min_bytes"), int) or content["min_bytes"] < 0:
                raise ValueError(f"{source}: {artifact_id} content needs non-negative integer min_bytes")
            patterns = content.get("reject_patterns", [])
            if not isinstance(patterns, list) or not all(isinstance(value, str) for value in patterns):
                raise ValueError(f"{source}: {artifact_id} reject_patterns must be a string list")
    return payload["artifacts"]


def freshness_entries(path: Path | str = DEFAULT_REGISTRY) -> list[dict[str, Any]]:
    return [e for e in load_registry(path) if "freshness_slo_hours" in e["cadence"]]


def content_entries(path: Path | str = DEFAULT_REGISTRY) -> list[dict[str, Any]]:
    return [e for e in load_registry(path) if isinstance(e.get("content"), dict)]
