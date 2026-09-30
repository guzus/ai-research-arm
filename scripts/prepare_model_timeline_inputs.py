#!/usr/bin/env python3
"""Prepare lossless, paged signal and compact ticket metadata for model CRUD.

This is input preparation, not editorial synthesis. It never changes tickets,
ranks/drops candidates, infers release dates, or truncates source evidence.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parent.parent
TICKET_FIELDS = (
    "slug", "title", "company", "model", "status", "verification",
    "created_at", "updated_at", "closed_at", "closed_reason",
)
PAGE_BYTES = 16000


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)


def parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        try:
            parsed = parsedate_to_datetime(value)
        except (ValueError, TypeError, OverflowError):
            return None
    # Never silently apply the host timezone to ambiguous source timestamps.
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def ticket_inventory(tickets_dir: Path, as_of: datetime) -> list[dict[str, Any]]:
    rows = []
    for path in sorted(tickets_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n") or "\n---\n" not in text:
            raise ValueError(f"{path}: missing ticket frontmatter")
        data = yaml.safe_load(text[4:].split("\n---\n", 1)[0])
        if not isinstance(data, dict) or not all(key in data for key in ("slug", "status", "history")):
            raise ValueError(f"{path}: invalid ticket metadata")
        history = data["history"]
        if not isinstance(history, list):
            raise ValueError(f"{path}: history must be a list")
        dates = [date.fromisoformat(str(entry["ts"])) for entry in history]
        latest = max(dates) if dates else None
        row = {key: data.get(key) for key in TICKET_FIELDS}
        row.update(path=str(path.resolve()), last_history_at=latest, history_count=len(history))
        # History contains only ts/change, not a structured release timestamp.
        # These are review hints, never automatic closure decisions.
        if data["status"] == "released":
            row["closure_review"] = "Read original history to establish actual release date."
        elif (data["status"] != "closed" and data.get("verification") == "unverified"
              and latest is not None and (as_of.date() - latest).days >= 15):
            row["closure_review"] = "No history in 15+ days; check fresh signal before closing."
        rows.append(row)
    if not rows:
        raise ValueError(f"{tickets_dir}: no ticket files")
    return rows


def prepare_signal(raw_dir: Path, as_of: datetime) -> tuple[list[dict[str, Any]], dict[str, int]]:
    cutoff = as_of - timedelta(hours=24)
    groups: dict[str, dict[str, Any]] = {}
    files = sorted(raw_dir.glob("*.json"))
    if not files:
        raise ValueError(f"{raw_dir}: no raw JSON inputs")
    observed = 0
    for path in files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, list) or any(not isinstance(item, dict) for item in payload):
            raise ValueError(f"{path}: expected a JSON array of tweet objects")
        for index, tweet in enumerate(payload):
            observed += 1
            encoded = json.dumps(tweet, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
            tweet_id = tweet.get("id") or tweet.get("id_str")
            key = f"id:{tweet_id}" if tweet_id else "payload:" + hashlib.sha256(encoded.encode()).hexdigest()
            group = groups.setdefault(key, {"key": key, "variants": {}, "keep": False})
            variant = group["variants"].get(encoded)
            if variant is None:
                raw_time = tweet.get("createdAt") or tweet.get("created_at")
                timestamp = parse_timestamp(raw_time)
                status = ("unknown" if timestamp is None else "before_window" if timestamp < cutoff
                          else "future" if timestamp > as_of else "within_window")
                variant = {"timestamp_status": status, "timestamp_utc": timestamp.isoformat() if timestamp else None,
                           "payload": tweet, "provenance": []}
                group["variants"][encoded] = variant
                group["keep"] |= status != "before_window"
            variant["provenance"].append({"path": str(path.resolve()), "index": index})
    # Keep every distinct payload version of a retained ID, even if one version
    # has an old/conflicting date or richer quoted/media evidence. Raw files stay
    # untouched and every observation can be traced back to its array index.
    records = [{"key": group["key"], "variants": list(group["variants"].values())}
               for group in groups.values() if group["keep"]]
    return records, {"raw_files": len(files), "raw_observations": observed,
                     "unique_groups": len(groups), "retained_groups": len(records),
                     "excluded_old_groups": len(groups) - len(records)}


def write_pages(output_dir: Path, prefix: str, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pages = []
    current: list[str] = []
    size = 0

    def flush() -> None:
        nonlocal current, size
        if not current:
            return
        path = output_dir / f"{prefix}-{len(pages) + 1:03d}.jsonl"
        path.write_text("".join(current), encoding="utf-8")
        pages.append({"path": str(path.resolve()), "records": len(current), "bytes": size})
        current, size = [], 0

    for record in records:
        line = json_text(record) + "\n"
        length = len(line.encode())
        if current and size + length > PAGE_BYTES:
            flush()
        current.append(line)
        size += length
        # Oversized individual evidence is preserved in its own page, never
        # shortened. The manifest exposes its size for chunked/targeted reads.
        if size >= PAGE_BYTES:
            flush()
    flush()
    return pages


def prepare(raw_dir: Path, tickets_dir: Path, output_dir: Path, as_of: datetime) -> dict[str, Any]:
    inventory = ticket_inventory(tickets_dir, as_of)
    signal, stats = prepare_signal(raw_dir, as_of)
    output_dir.mkdir(parents=True, exist_ok=False)
    active = [row for row in inventory if row["status"] != "closed"]
    closed = [row for row in inventory if row["status"] == "closed"]
    manifest = {
        "as_of_utc": as_of.isoformat(), "cutoff_utc": (as_of - timedelta(hours=24)).isoformat(),
        "raw_signal_directory": str(raw_dir.resolve()), "signal_counts": stats,
        "ticket_counts": {"total": len(inventory), **dict(Counter(row["status"] for row in inventory))},
        "active_ticket_pages": write_pages(output_dir, "tickets-active", active),
        "closed_ticket_pages": write_pages(output_dir, "tickets-closed", closed),
        "signal_pages": write_pages(output_dir, "signal", signal),
        "contract": [
            "Read every listed ticket and signal page with Bash(cat <exact page path>), not Read (long JSON lines can truncate).",
            "There is no candidate cap or ranking; never accept truncated tool output as full evidence.",
            "All closed tickets remain visible for dedup, but cannot be edited.",
            "Each signal variant retains the complete original payload and raw file/index provenance.",
            "Only groups with exclusively known timestamps before cutoff are excluded.",
            "Unknown/future timestamps require review; they are not proof of freshness.",
            "Metadata omits ticket bodies/history text. Read original matched tickets before editing.",
            "Closure hints are not decisions; release date must be checked in original history.",
            "Oversized individual records are preserved intact; use jq to read their variants/fields in parts.",
        ],
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", type=Path, required=True)
    parser.add_argument("--tickets-dir", type=Path, default=ROOT / "research/models/tickets")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--as-of", required=True, help="Explicit timezone-aware UTC timestamp")
    args = parser.parse_args()
    as_of = parse_timestamp(args.as_of)
    if as_of is None or not args.as_of.endswith(("Z", "+00:00")):
        parser.error("--as-of must be an explicit UTC timestamp (Z or +00:00)")
    try:
        manifest = prepare(args.raw_dir, args.tickets_dir, args.output_dir, as_of)
    except (ValueError, OSError, KeyError, TypeError, yaml.YAMLError) as exc:
        parser.exit(1, f"Model input preparation failed: {exc}\n")
    print(json.dumps({"manifest": str((args.output_dir / "manifest.json").resolve()),
                      "signal_counts": manifest["signal_counts"], "ticket_counts": manifest["ticket_counts"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
