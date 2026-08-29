#!/usr/bin/env python3
"""Exit 0 only for an operational deterministic-fallback digest."""

from __future__ import annotations

import argparse
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
    parser.add_argument("digest", help="Digest path, or - to read stdin")
    args = parser.parse_args()
    markdown = sys.stdin.read() if args.digest == "-" else Path(args.digest).read_text(encoding="utf-8")
    return 0 if is_deterministic_fallback(markdown) else 1


if __name__ == "__main__":
    raise SystemExit(main())
