#!/usr/bin/env python3
"""Validate and curate the Twitter/X account manifest used by hourly fetches."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = REPO_ROOT / "data" / "sources" / "twitter_accounts.json"
HANDLE_RE = re.compile(r"^[A-Za-z0-9_]{1,15}$")
SEARCH_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


class ManifestError(ValueError):
    pass


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ManifestError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ManifestError(f"{path}: invalid JSON: {exc}") from exc


def _write_json_atomic(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def normalize_handle(handle: str) -> str:
    value = str(handle or "").strip().lstrip("@")
    if not HANDLE_RE.fullmatch(value):
        raise ManifestError(f"invalid X/Twitter handle: {handle!r}")
    return value


def validate_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(manifest, dict):
        raise ManifestError("manifest must be a JSON object")
    if manifest.get("version") != 1:
        raise ManifestError("manifest version must be 1")

    tweets_per_account = manifest.get("tweets_per_account")
    if not isinstance(tweets_per_account, int) or tweets_per_account <= 0:
        raise ManifestError("tweets_per_account must be a positive integer")

    categories = manifest.get("categories")
    if not isinstance(categories, list) or not categories:
        raise ManifestError("categories must be a non-empty list")

    category_ids: set[str] = set()
    seen_handles: dict[str, str] = {}
    total_handles = 0
    for category in categories:
        if not isinstance(category, dict):
            raise ManifestError("each category must be an object")
        category_id = category.get("id")
        if not isinstance(category_id, str) or not SEARCH_ID_RE.fullmatch(category_id):
            raise ManifestError(f"invalid category id: {category_id!r}")
        if category_id in category_ids:
            raise ManifestError(f"duplicate category id: {category_id}")
        category_ids.add(category_id)
        if not isinstance(category.get("label"), str) or not category["label"].strip():
            raise ManifestError(f"category {category_id} must have a label")
        handles = category.get("handles")
        if not isinstance(handles, list):
            raise ManifestError(f"category {category_id} handles must be a list")
        for entry in handles:
            if isinstance(entry, str):
                handle = normalize_handle(entry)
            elif isinstance(entry, dict):
                handle = normalize_handle(entry.get("handle", ""))
                if "name" in entry and not isinstance(entry["name"], str):
                    raise ManifestError(f"@{handle} name must be a string")
                if "notes" in entry and not isinstance(entry["notes"], str):
                    raise ManifestError(f"@{handle} notes must be a string")
            else:
                raise ManifestError(f"invalid handle entry in {category_id}: {entry!r}")
            key = handle.lower()
            if key in seen_handles:
                raise ManifestError(f"duplicate handle @{handle} in {category_id}; first seen in {seen_handles[key]}")
            seen_handles[key] = category_id
            total_handles += 1

    searches = manifest.get("searches")
    if not isinstance(searches, list):
        raise ManifestError("searches must be a list")
    seen_searches: set[str] = set()
    for search in searches:
        if not isinstance(search, dict):
            raise ManifestError("each search must be an object")
        search_id = search.get("id")
        if not isinstance(search_id, str) or not SEARCH_ID_RE.fullmatch(search_id):
            raise ManifestError(f"invalid search id: {search_id!r}")
        if search_id in seen_searches:
            raise ManifestError(f"duplicate search id: {search_id}")
        seen_searches.add(search_id)
        if not isinstance(search.get("query"), str) or not search["query"].strip():
            raise ManifestError(f"search {search_id} must have a query")
        if not isinstance(search.get("limit"), int) or search["limit"] <= 0:
            raise ManifestError(f"search {search_id} limit must be a positive integer")

    news = manifest.get("news")
    if not isinstance(news, dict):
        raise ManifestError("news must be an object")
    news_id = news.get("id")
    if not isinstance(news_id, str) or not SEARCH_ID_RE.fullmatch(news_id):
        raise ManifestError(f"invalid news id: {news_id!r}")
    if not isinstance(news.get("limit"), int) or news["limit"] <= 0:
        raise ManifestError("news limit must be a positive integer")

    return {
        "categories": len(categories),
        "handles": total_handles,
        "searches": len(searches),
        "news_id": news_id,
        "tweets_per_account": tweets_per_account,
    }


def iter_handle_entries(manifest: dict[str, Any]):
    for category in manifest["categories"]:
        for entry in category["handles"]:
            if isinstance(entry, str):
                yield category["id"], {"handle": entry}
            else:
                yield category["id"], entry


def build_fetch_manifest(manifest: dict[str, Any], concurrency: int) -> dict[str, Any]:
    stats = validate_manifest(manifest)
    ops = []
    for _category_id, entry in iter_handle_entries(manifest):
        handle = normalize_handle(entry["handle"])
        ops.append(
            {
                "id": handle,
                "args": [
                    "user-tweets",
                    f"@{handle}",
                    "-n",
                    str(stats["tweets_per_account"]),
                    "--json",
                    "--plain",
                ],
            }
        )
    for search in manifest["searches"]:
        ops.append(
            {
                "id": search["id"],
                "args": ["search", search["query"], "-n", str(search["limit"]), "--json", "--plain"],
            }
        )
    news = manifest["news"]
    news_args = ["news"]
    if news.get("ai_only", True):
        news_args.append("--ai-only")
    news_args.extend(["-n", str(news["limit"]), "--json", "--plain"])
    ops.append({"id": news["id"], "args": news_args})
    return {"operations": ops, "concurrency": concurrency}


def _read_candidates(path: Path) -> list[dict[str, Any]]:
    raw = _load_json(path)
    if isinstance(raw, dict) and isinstance(raw.get("candidates"), list):
        raw = raw["candidates"]
    if not isinstance(raw, list):
        raise ManifestError("candidate file must be a list or an object with a candidates list")
    candidates = []
    for index, item in enumerate(raw, 1):
        if not isinstance(item, dict):
            raise ManifestError(f"candidate {index} must be an object")
        handle = normalize_handle(item.get("handle", ""))
        action = str(item.get("action", "add")).strip().lower()
        if action not in {"add", "remove"}:
            raise ManifestError(f"candidate @{handle} has invalid action {action!r}")
        evidence = item.get("evidence", [])
        if isinstance(evidence, str):
            evidence = [evidence]
        if not isinstance(evidence, list) or not all(isinstance(v, str) and v.strip() for v in evidence):
            raise ManifestError(f"candidate @{handle} evidence must be a string or list of strings")
        category = item.get("category")
        if category is not None and (not isinstance(category, str) or not SEARCH_ID_RE.fullmatch(category)):
            raise ManifestError(f"candidate @{handle} has invalid category {category!r}")
        score = item.get("score", 1)
        if not isinstance(score, (int, float)):
            raise ManifestError(f"candidate @{handle} score must be numeric")
        candidates.append(
            {
                "action": action,
                "handle": handle,
                "category": category,
                "score": score,
                "reason": str(item.get("reason", "")).strip(),
                "evidence": [v.strip() for v in evidence],
            }
        )
    return candidates


def _handle_index(manifest: dict[str, Any]) -> dict[str, str]:
    return {entry["handle"].lower(): category_id for category_id, entry in iter_handle_entries(manifest)}


def propose_changes(
    manifest: dict[str, Any],
    candidates: list[dict[str, Any]],
    min_score: float,
    default_category: str,
) -> dict[str, Any]:
    validate_manifest(manifest)
    categories = {category["id"] for category in manifest["categories"]}
    if default_category not in categories:
        raise ManifestError(f"default category {default_category!r} does not exist")
    current = _handle_index(manifest)
    additions = []
    removals = []
    ignored = []
    emitted: set[tuple[str, str]] = set()

    for candidate in candidates:
        handle = normalize_handle(candidate["handle"])
        candidate = {**candidate, "handle": handle}
        key = handle.lower()
        action = candidate["action"]
        dedupe_key = (action, key)
        if dedupe_key in emitted:
            ignored.append({**candidate, "why": "duplicate candidate"})
            continue
        emitted.add(dedupe_key)

        if action == "add":
            if key in current:
                ignored.append({**candidate, "why": f"already monitored in {current[key]}"})
                continue
            if candidate["score"] < min_score:
                ignored.append({**candidate, "why": f"score below threshold {min_score:g}"})
                continue
            category = candidate["category"] or default_category
            if category not in categories:
                ignored.append({**candidate, "why": f"unknown category {category!r}"})
                continue
            additions.append({**candidate, "category": category})
        else:
            if key not in current:
                ignored.append({**candidate, "why": "not currently monitored"})
                continue
            removals.append({**candidate, "category": current[key]})

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "manifest": str(DEFAULT_MANIFEST.relative_to(REPO_ROOT)),
        "additions": additions,
        "removals": removals,
        "ignored": ignored,
    }


def write_proposal_markdown(path: Path, changes: dict[str, Any]) -> None:
    lines = [
        "# Twitter Account Curation Proposal",
        "",
        f"Generated: {changes['generated_at']}",
        "",
        "## Proposed Additions",
        "",
    ]
    if changes["additions"]:
        for item in changes["additions"]:
            lines.append(f"- `@{item['handle']}` -> `{item['category']}` (score {item['score']})")
            lines.append(f"  Reason: {item['reason'] or 'No reason supplied.'}")
            if item["evidence"]:
                lines.append("  Evidence: " + ", ".join(item["evidence"]))
    else:
        lines.append("- None")

    lines.extend(["", "## Proposed Removals", ""])
    if changes["removals"]:
        for item in changes["removals"]:
            lines.append(f"- `@{item['handle']}` from `{item['category']}` (score {item['score']})")
            lines.append(f"  Reason: {item['reason'] or 'No reason supplied.'}")
            if item["evidence"]:
                lines.append("  Evidence: " + ", ".join(item["evidence"]))
    else:
        lines.append("- None")

    lines.extend(["", "## Ignored Candidates", ""])
    if changes["ignored"]:
        for item in changes["ignored"]:
            lines.append(f"- `@{item['handle']}` `{item['action']}`: {item['why']}")
    else:
        lines.append("- None")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def apply_changes(manifest: dict[str, Any], changes: dict[str, Any]) -> dict[str, Any]:
    validate_manifest(manifest)
    out = deepcopy(manifest)
    category_by_id = {category["id"]: category for category in out["categories"]}

    remove_keys = {normalize_handle(item["handle"]).lower() for item in changes.get("removals", [])}
    for category in out["categories"]:
        category["handles"] = [
            entry for entry in category["handles"]
            if normalize_handle(entry if isinstance(entry, str) else entry["handle"]).lower() not in remove_keys
        ]

    existing = _handle_index(out)
    for item in changes.get("additions", []):
        handle = normalize_handle(item["handle"])
        key = handle.lower()
        if key in existing:
            continue
        category_id = item.get("category")
        if category_id not in category_by_id:
            raise ManifestError(f"cannot add @{handle}: category {category_id!r} does not exist")
        entry = {"handle": handle}
        if item.get("reason"):
            entry["notes"] = item["reason"]
        if item.get("evidence"):
            entry["evidence"] = item["evidence"]
        category_by_id[category_id]["handles"].append(entry)
        existing[key] = category_id

    validate_manifest(out)
    return out


def cmd_validate(args: argparse.Namespace) -> int:
    manifest = _load_json(args.manifest)
    stats = validate_manifest(manifest)
    print(
        f"OK: {stats['handles']} handles, {stats['searches']} searches, "
        f"news={stats['news_id']}, tweets_per_account={stats['tweets_per_account']}"
    )
    return 0


def cmd_build_fetch_manifest(args: argparse.Namespace) -> int:
    if args.concurrency <= 0:
        raise ManifestError("--concurrency must be positive")
    manifest = _load_json(args.manifest)
    fetch_manifest = build_fetch_manifest(manifest, args.concurrency)
    _write_json_atomic(args.output, fetch_manifest)
    print(f"wrote {len(fetch_manifest['operations'])} operations to {args.output}")
    return 0


def cmd_propose(args: argparse.Namespace) -> int:
    manifest = _load_json(args.manifest)
    candidates = _read_candidates(args.candidates)
    changes = propose_changes(manifest, candidates, args.min_score, args.default_category)
    write_proposal_markdown(args.output, changes)
    if args.changes_output:
        _write_json_atomic(args.changes_output, changes)
    print(
        f"proposal: {len(changes['additions'])} additions, "
        f"{len(changes['removals'])} removals, {len(changes['ignored'])} ignored"
    )
    return 0


def cmd_apply(args: argparse.Namespace) -> int:
    manifest = _load_json(args.manifest)
    changes = _load_json(args.changes)
    updated = apply_changes(manifest, changes)
    _write_json_atomic(args.manifest, updated)
    stats = validate_manifest(updated)
    print(f"updated {args.manifest}: {stats['handles']} handles")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="validate the Twitter account manifest")
    validate.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    validate.set_defaults(func=cmd_validate)

    build = sub.add_parser("build-fetch-manifest", help="build a birdy multi-fetch manifest")
    build.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    build.add_argument("--output", type=Path, required=True)
    build.add_argument("--concurrency", type=int, default=8)
    build.set_defaults(func=cmd_build_fetch_manifest)

    propose = sub.add_parser("propose", help="write a reviewable add/remove proposal")
    propose.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    propose.add_argument("--candidates", type=Path, required=True)
    propose.add_argument("--output", type=Path, required=True)
    propose.add_argument("--changes-output", type=Path)
    propose.add_argument("--min-score", type=float, default=1)
    propose.add_argument("--default-category", default="others")
    propose.set_defaults(func=cmd_propose)

    apply = sub.add_parser("apply", help="apply reviewed proposal changes to the manifest")
    apply.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    apply.add_argument("--changes", type=Path, required=True)
    apply.set_defaults(func=cmd_apply)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ManifestError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
