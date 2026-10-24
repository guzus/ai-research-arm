#!/usr/bin/env python3
"""Resolve an explicit/UTC digest date and carry it to downstream renderers."""

import argparse
from datetime import date, datetime, timezone
import json
import os
from pathlib import Path
import re


def validate_date(value: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError("edition date must be YYYY-MM-DD")
    date.fromisoformat(value)
    return value


def resolve_date(requested: str, created_at: str, now: datetime) -> str:
    if requested:
        return validate_date(requested)
    if created_at:
        created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        if created.tzinfo is None:
            raise ValueError("run creation timestamp must include its timezone")
        return created.astimezone(timezone.utc).date().isoformat()
    return now.astimezone(timezone.utc).date().isoformat()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default="")
    parser.add_argument("--created-at", default="")
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.manifest:
        # A missing or malformed parent handoff must not render today's issue.
        payload = json.loads(args.manifest.read_text())
        edition = validate_date(payload["date"])
    else:
        edition = resolve_date(args.date, args.created_at, datetime.now(timezone.utc))
    if args.output:
        temporary = args.output.with_suffix(".tmp")
        temporary.write_text(json.dumps({"date": edition}) + "\n")
        os.replace(temporary, args.output)
    print(edition)


if __name__ == "__main__":
    main()
