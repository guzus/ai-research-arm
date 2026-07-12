#!/usr/bin/env python3
"""Operational fallback for scheduled Twitter/X lanes.

The fallback deliberately does not turn raw tweets into reader-facing news or
edit the public digest. The workflow restores that digest from its pre-agent
baseline; this script only writes recovery heartbeat and empty-alert artifacts.
"""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(text)
        tmp_name = handle.name
    Path(tmp_name).replace(path)


def render_status(
    date: str,
    hour: str,
    timestamp: str,
    run_id: str,
    run_attempt: int,
) -> str:
    return json.dumps(
        {
            "schema_version": 1,
            "date": date,
            "hour": f"{hour}:00 UTC",
            "generated_at": timestamp,
            "run_id": run_id,
            "run_attempt": run_attempt,
            "status": "no_update",
            "public_items": 0,
            "recovery": True,
        },
        indent=2,
        ensure_ascii=False,
    ) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    # Retain the workflow CLI contract even though an operational fallback
    # must not inspect or editorialize the staged source snapshot.
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summaries-dir", type=Path, required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--hour", required=True)
    parser.add_argument("--timestamp", required=True)
    parser.add_argument("--run-id", default="local")
    parser.add_argument("--run-attempt", type=int, default=1)
    parser.add_argument("--title-suffix", default="")
    parser.add_argument("--summary-slug", required=True)
    parser.add_argument("--headlines-file", type=Path)
    parser.add_argument("--status-file", type=Path)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--max-age-hours", type=int, default=36)
    args = parser.parse_args(argv)

    summary_path = args.summaries_dir / f"{args.date}-{args.summary_slug}-{args.hour}h-summary.txt"
    status_path = args.status_file or args.out_dir / "status" / f"{args.date}-{args.hour}h.json"

    atomic_write(summary_path, "")
    atomic_write(
        status_path,
        render_status(
            args.date,
            args.hour,
            args.timestamp,
            args.run_id,
            args.run_attempt,
        ),
    )
    if args.headlines_file is not None:
        atomic_write(args.headlines_file, "[]\n")

    print("left public digest unchanged (workflow restores its baseline)")
    print(f"wrote {summary_path}")
    print(f"wrote {status_path}")
    if args.headlines_file is not None:
        print(f"wrote {args.headlines_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
