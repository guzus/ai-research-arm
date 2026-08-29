#!/usr/bin/env python3
"""Exit 0 only for an operational deterministic-fallback digest."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FALLBACK_BANNER = "> **Deterministic fallback digest.**"


def is_deterministic_fallback(markdown: str) -> bool:
    for line in markdown.splitlines()[:8]:
        normalized = line.strip()
        if normalized == FALLBACK_BANNER or normalized.startswith(FALLBACK_BANNER + " "):
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("digest", nargs="?", help="Digest path, or - to read stdin")
    parser.add_argument("--list-fallback-dates", metavar="DIR", help="Print fallback dates found in a digest directory")
    args = parser.parse_args()
    if args.list_fallback_dates:
        digest_dir = Path(args.list_fallback_dates)
        for path in sorted(digest_dir.glob("*-digest.md")):
            match = re.fullmatch(r"(\d{4}-\d{2}-\d{2})-digest\.md", path.name)
            if match and is_deterministic_fallback(path.read_text(encoding="utf-8")):
                print(match.group(1))
        return 0
    if not args.digest:
        parser.error("digest is required unless --list-fallback-dates is used")
    markdown = sys.stdin.read() if args.digest == "-" else Path(args.digest).read_text(encoding="utf-8")
    return 0 if is_deterministic_fallback(markdown) else 1


if __name__ == "__main__":
    raise SystemExit(main())
