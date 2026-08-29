#!/usr/bin/env python3
"""Detect open automation/safe-push PRs whose publication is stranded."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed


def stranded(rows: list[dict], now: datetime, min_age_hours: float) -> list[dict]:
    result = []
    for row in rows:
        head = str(row.get("headRefName") or "")
        if not head.startswith("automation/safe-push/"):
            continue
        try:
            age = (now - parse_time(str(row["createdAt"]))).total_seconds() / 3600
        except (KeyError, TypeError, ValueError):
            continue
        if age >= min_age_hours:
            result.append({**row, "age_hours": round(age, 1)})
    return sorted(result, key=lambda row: (row["createdAt"], row.get("number", 0)))


def _outputs(rows: list[dict], now: datetime) -> None:
    output = os.environ.get("GITHUB_OUTPUT")
    if not output:
        return
    ids = "-".join(str(row.get("number")) for row in rows) or "none"
    summary = "\n".join(
        f"- #{row.get('number')} ({row['age_hours']}h): {row.get('url', '')}" for row in rows
    )
    with open(output, "a", encoding="utf-8") as fh:
        fh.write(f"stranded={'true' if rows else 'false'}\n")
        fh.write(f"count={len(rows)}\n")
        fh.write(f"idempotency_key=stranded-publications-{now:%Y-%m-%d}-{ids}\n")
        fh.write(f"summary<<__STRANDED__\n{summary}\n__STRANDED__\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", help="fixture JSON; default queries gh pr list")
    parser.add_argument("--now", help="ISO-8601 timestamp; default now")
    parser.add_argument("--min-age-hours", type=float, default=1.0)
    args = parser.parse_args(argv)
    now = parse_time(args.now) if args.now else datetime.now(timezone.utc)
    if args.input:
        rows = json.loads(Path(args.input).read_text(encoding="utf-8"))
    else:
        try:
            raw = subprocess.run(
                ["gh", "pr", "list", "--state", "open", "--limit", "100", "--json", "number,url,title,headRefName,createdAt"],
                check=True, capture_output=True, text=True,
            ).stdout
        except (FileNotFoundError, subprocess.CalledProcessError) as exc:
            print(f"error: cannot query open publication PRs: {exc}", file=sys.stderr)
            return 1
        rows = json.loads(raw)
    found = stranded(rows, now, args.min_age_hours)
    _outputs(found, now)
    print(json.dumps({"stranded": found}, indent=2))
    return 2 if found else 0


if __name__ == "__main__":
    raise SystemExit(main())
