#!/usr/bin/env python3
"""Validate model-release tickets against the schema in docs/model-tickets.md.

Usage:
    uv run python scripts/check_model_tickets.py
    uv run python scripts/check_model_tickets.py path/to/ticket.md ...

Exit 0 when every ticket is valid. Exit 1 with a list of failures.

The schema is intentionally strict: every field listed under "Frontmatter
schema" in docs/model-tickets.md is enforced here. Keep this script and
the doc in lockstep.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
TICKETS_DIR = REPO_ROOT / "research" / "models" / "tickets"

CANONICAL_STATUSES = {"rumored", "in-testing", "confirmed", "released", "closed"}
CANONICAL_VERIFICATION = {"confirmed", "partial", "unverified"}
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
HANDLE_RE = re.compile(r"^@[A-Za-z0-9_]{1,30}$")
URL_RE = re.compile(r"^https?://\S+$")


@dataclass
class Failure:
    path: Path
    field: str
    msg: str


@dataclass
class Report:
    failures: list[Failure] = field(default_factory=list)
    files_checked: int = 0

    def fail(self, path: Path, field_name: str, msg: str) -> None:
        self.failures.append(Failure(path, field_name, msg))

    def ok(self) -> bool:
        return not self.failures


def _split_frontmatter(text: str, path: Path, report: Report) -> tuple[dict[str, Any] | None, str]:
    """Return (frontmatter_dict, body). Returns (None, '') on parse failure."""
    if not text.startswith("---\n"):
        report.fail(path, "frontmatter", "file must start with '---' on line 1")
        return None, ""
    parts = text.split("\n---\n", 1)
    if len(parts) < 2:
        report.fail(path, "frontmatter", "missing closing '---' delimiter")
        return None, ""
    header = parts[0][4:]  # drop leading '---\n'
    body = parts[1].lstrip("\n")
    try:
        data = yaml.safe_load(header)
    except yaml.YAMLError as e:
        report.fail(path, "frontmatter", f"YAML parse error: {e}")
        return None, ""
    if not isinstance(data, dict):
        report.fail(path, "frontmatter", "frontmatter must be a mapping")
        return None, ""
    return data, body


def _check_str(data: dict, key: str, path: Path, report: Report, *, required: bool = True) -> str | None:
    val = data.get(key)
    if val is None:
        if required:
            report.fail(path, key, "required field missing or null")
        return None
    if not isinstance(val, str):
        report.fail(path, key, f"must be a string, got {type(val).__name__}")
        return None
    if not val.strip():
        report.fail(path, key, "must not be empty")
        return None
    return val


def _check_date(data: dict, key: str, path: Path, report: Report, *, allow_null: bool = False) -> date | None:
    val = data.get(key)
    if val is None:
        if allow_null:
            return None
        report.fail(path, key, "required date missing or null")
        return None
    if isinstance(val, date):
        return val
    if isinstance(val, str):
        try:
            return date.fromisoformat(val)
        except ValueError:
            report.fail(path, key, f"not a valid ISO date (YYYY-MM-DD): {val!r}")
            return None
    report.fail(path, key, f"must be a date, got {type(val).__name__}")
    return None


def _check_sources(val: Any, path: Path, report: Report) -> None:
    if not isinstance(val, list):
        report.fail(path, "sources", "must be a list")
        return
    if not val:
        report.fail(path, "sources", "must have at least one source")
        return
    for i, src in enumerate(val):
        if not isinstance(src, str):
            report.fail(path, "sources", f"item {i} must be a string, got {type(src).__name__}")
            continue
        if not (URL_RE.match(src) or HANDLE_RE.match(src)):
            report.fail(path, "sources", f"item {i} must be a URL (http(s)://) or handle (@name): {src!r}")


def _check_history(val: Any, path: Path, report: Report, created_at: date | None, updated_at: date | None) -> None:
    if not isinstance(val, list):
        report.fail(path, "history", "must be a list")
        return
    if not val:
        report.fail(path, "history", "must have at least one entry (the 'Created' entry)")
        return
    prev_ts: date | None = None
    for i, entry in enumerate(val):
        if not isinstance(entry, dict):
            report.fail(path, "history", f"entry {i} must be a mapping with ts + change keys")
            continue
        ts = entry.get("ts")
        change = entry.get("change")
        if isinstance(ts, str):
            try:
                ts = date.fromisoformat(ts)
            except ValueError:
                report.fail(path, "history", f"entry {i} ts not a valid ISO date: {entry.get('ts')!r}")
                ts = None
        elif not isinstance(ts, date):
            report.fail(path, "history", f"entry {i} ts must be a date, got {type(ts).__name__}")
            ts = None
        if not isinstance(change, str) or not change.strip():
            report.fail(path, "history", f"entry {i} change must be a non-empty string")
        if ts is not None:
            if created_at and ts < created_at:
                report.fail(path, "history", f"entry {i} ts {ts} predates created_at {created_at}")
            if updated_at and ts > updated_at:
                report.fail(path, "history", f"entry {i} ts {ts} is after updated_at {updated_at}")
            if prev_ts and ts < prev_ts:
                report.fail(path, "history", f"entry {i} ts {ts} is out of order (previous was {prev_ts})")
            prev_ts = ts


def check_ticket(path: Path, report: Report) -> None:
    report.files_checked += 1
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        report.fail(path, "io", f"cannot read file: {e}")
        return

    data, body = _split_frontmatter(text, path, report)
    if data is None:
        return

    slug = _check_str(data, "slug", path, report)
    if slug and not SLUG_RE.match(slug):
        report.fail(path, "slug", f"must match {SLUG_RE.pattern}, got {slug!r}")
    expected_filename = f"{slug}.md" if slug else None
    if expected_filename and path.name != expected_filename:
        report.fail(path, "slug", f"filename {path.name!r} must match slug + '.md' ({expected_filename!r})")

    _check_str(data, "title", path, report)
    _check_str(data, "company", path, report)

    status = _check_str(data, "status", path, report)
    if status and status not in CANONICAL_STATUSES:
        report.fail(path, "status", f"must be one of {sorted(CANONICAL_STATUSES)}, got {status!r}")

    verification = _check_str(data, "verification", path, report)
    if verification and verification not in CANONICAL_VERIFICATION:
        report.fail(path, "verification", f"must be one of {sorted(CANONICAL_VERIFICATION)}, got {verification!r}")

    if "sources" not in data:
        report.fail(path, "sources", "required field missing")
    else:
        _check_sources(data["sources"], path, report)

    created_at = _check_date(data, "created_at", path, report)
    updated_at = _check_date(data, "updated_at", path, report)
    closed_at = _check_date(data, "closed_at", path, report, allow_null=True)

    if created_at and updated_at and updated_at < created_at:
        report.fail(path, "updated_at", f"updated_at {updated_at} < created_at {created_at}")

    closed_reason = data.get("closed_reason")
    if status == "closed":
        if closed_at is None:
            report.fail(path, "closed_at", "status=closed requires closed_at (YYYY-MM-DD)")
        if closed_reason is None or not str(closed_reason).strip():
            report.fail(path, "closed_reason", "status=closed requires closed_reason")
    else:
        if closed_at is not None:
            report.fail(path, "closed_at", f"closed_at must be null when status != closed (got {closed_at})")
        if closed_reason not in (None, ""):
            report.fail(path, "closed_reason", "closed_reason must be null when status != closed")

    if "history" not in data:
        report.fail(path, "history", "required field missing")
    else:
        _check_history(data["history"], path, report, created_at, updated_at)

    if "model" in data and data["model"] is not None and not isinstance(data["model"], str):
        report.fail(path, "model", "must be a string or null")
    if "expected" in data and data["expected"] is not None and not isinstance(data["expected"], str):
        report.fail(path, "expected", "must be a string or null")
    if "status_note" in data and data["status_note"] is not None and not isinstance(data["status_note"], str):
        report.fail(path, "status_note", "must be a string or null")

    if "labels" in data and data["labels"] is not None:
        if not isinstance(data["labels"], list) or not all(isinstance(l, str) for l in data["labels"]):
            report.fail(path, "labels", "must be a list of strings or null")

    body_stripped = body.strip()
    if not body_stripped:
        report.fail(path, "body", "body must not be empty — write a narrative under the frontmatter")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", help="ticket files; defaults to research/models/tickets/*.md")
    args = parser.parse_args(argv)

    if args.paths:
        targets = [Path(p) for p in args.paths]
    else:
        if not TICKETS_DIR.is_dir():
            print(f"no tickets dir at {TICKETS_DIR.relative_to(REPO_ROOT)} — nothing to validate", file=sys.stderr)
            return 0
        targets = sorted(TICKETS_DIR.glob("*.md"))

    report = Report()
    for path in targets:
        if not path.is_file():
            report.fail(path, "io", "not a regular file")
            continue
        check_ticket(path, report)

    if report.ok():
        print(f"OK — {report.files_checked} ticket(s) valid")
        return 0

    for f in report.failures:
        rel = f.path.relative_to(REPO_ROOT) if f.path.is_absolute() else f.path
        print(f"FAIL {rel}: {f.field}: {f.msg}", file=sys.stderr)
    print(f"\n{len(report.failures)} failure(s) across {report.files_checked} ticket(s)", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
