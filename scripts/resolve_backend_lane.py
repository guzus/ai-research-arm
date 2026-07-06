#!/usr/bin/env python3
"""Resolve a lane's backend routing from data/agent-backends.json.

Field resolver for the backend SSOT: generative-research's params step calls
it on the runner for its SSOT default backend (agent-run lanes use the richer
scripts/select_backend.py). Editing data/agent-backends.json re-routes with
no workflow change. STDLIB ONLY — it must run on bare python3 on both runner
tiers.

Usage:
    python3 scripts/resolve_backend_lane.py <lane>                 # prints the lane's backend
    python3 scripts/resolve_backend_lane.py <lane> --field model   # any lane field
    python3 scripts/resolve_backend_lane.py --top fallback.native_model  # dotted path

Exit codes: 0 ok; 2 unknown lane / missing field / bad file (fail fast —
a typo'd lane must fail the run loudly, not fall back silently).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DEFAULT_FILE = Path(__file__).resolve().parent.parent / "data" / "agent-backends.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lane", nargs="?", help="lane key in data/agent-backends.json")
    parser.add_argument("--field", default="backend",
                        help="lane field to print (default: backend)")
    parser.add_argument("--top", default=None,
                        help="print a top-level key instead of a lane field; "
                             "dotted paths descend into objects (e.g. fallback.backend)")
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE,
                        help="override the routing file path (tests)")
    args = parser.parse_args()

    try:
        data = json.loads(args.file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read {args.file}: {exc}", file=sys.stderr)
        return 2

    if args.top is not None:
        value = data
        for part in args.top.split("."):
            value = value.get(part) if isinstance(value, dict) else None
        if not isinstance(value, str) or not value:
            print(f"ERROR: top-level path '{args.top}' missing or not a string in {args.file}",
                  file=sys.stderr)
            return 2
        print(value)
        return 0

    if not args.lane:
        print("ERROR: a lane argument (or --top) is required", file=sys.stderr)
        return 2

    lanes = data.get("lanes")
    if not isinstance(lanes, dict):
        print(f"ERROR: {args.file} has no 'lanes' mapping", file=sys.stderr)
        return 2

    lane = lanes.get(args.lane)
    if lane is None:
        known = ", ".join(sorted(lanes))
        print(f"ERROR: unknown lane '{args.lane}'. Known lanes: {known}", file=sys.stderr)
        return 2

    value = lane.get(args.field)
    if not isinstance(value, str) or not value:
        print(f"ERROR: lane '{args.lane}' has no '{args.field}' field", file=sys.stderr)
        return 2

    print(value)
    return 0


if __name__ == "__main__":
    sys.exit(main())
