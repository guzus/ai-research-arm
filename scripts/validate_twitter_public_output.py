#!/usr/bin/env python3
"""Validate the signal-only contract for one Twitter/X monitoring cycle."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from typing import Any


H2_RE = re.compile(r"^##[ \t]+(?P<title>.*?)[ \t]*\r?$", re.MULTILINE)
STORY_BLOCK_RE = re.compile(r"<article\b(?P<attrs>[^>]*)>(?P<body>.*?)</article>", re.IGNORECASE | re.DOTALL)
CLASS_RE = re.compile(r"\bclass=(?P<quote>['\"])(?P<classes>.*?)(?P=quote)", re.IGNORECASE)
TITLE_RE = re.compile(
    r"<h[1-6]\b[^>]*\bclass=(?P<quote>['\"])[^'\"]*\btwitter-story-title\b[^'\"]*(?P=quote)[^>]*>(?P<body>.*?)</h[1-6]>",
    re.IGNORECASE | re.DOTALL,
)
LEAD_RE = re.compile(
    r"<p\b[^>]*\bclass=(?P<quote>['\"])[^'\"]*\btwitter-story-lead\b[^'\"]*(?P=quote)[^>]*>(?P<body>.*?)</p>",
    re.IGNORECASE | re.DOTALL,
)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
SOURCE_ANCHOR_RE = re.compile(
    r"<a\b(?=[^>]*\bclass=(?P<class_quote>['\"])[^'\"]*\btwitter-source-chip\b[^'\"]*(?P=class_quote))"
    r"(?=[^>]*\bhref=(?P<href_quote>['\"])https?://(?:www\.)?(?:x|twitter)\.com/[^'\"\s<>]+/status/\d+(?P=href_quote))[^>]*>",
    re.IGNORECASE,
)
X_STATUS_RE = re.compile(
    r"https?://(?:www\.)?(?:x|twitter)\.com/[^\s)\]<>]+/status/\d+",
    re.IGNORECASE,
)
FILLER_RE = re.compile(
    r"(?:"
    r"\bquiet\b|"
    r"\bno\s+(?:(?:new|noteworthy|significant|material|major|fresh|concrete|publishable|main)\s+)*(?:ai\s+)?(?:stor(?:y|ies)|updates?|developments?|changes?|items?)\b|"
    r"\bpublication bar\b|"
    r"\bsame-day (?:twitter/x )?items\b|"
    r"\bfollow-up period\b|"
    r"\bnext scheduled (?:twitter/x )?(?:ai )?monitor run\b|"
    r"\bnothing (?:new|concrete|publishable)\b|"
    r"\bnone this cycle\b|"
    r"\bmonitor(?:ing)? (?:found|saw|surfaced|returned) no\b|"
    r"\bonly earlier .*? (?:items?|stories?) (?:repeated|remain(?:ed)?)\b|"
    r"\bno follow-ups? needed\b|"
    r"\bpre-fetched snapshot\b|"
    r"\bsource checks? (?:issued|performed|completed) this cycle\b|"
    r"^###[ \t]+Research notes[ \t]*$|"
    r"\bno_update\b"
    r")",
    re.IGNORECASE | re.MULTILINE,
)


class ContractError(ValueError):
    """Raised when a cycle violates the public-output contract."""


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ContractError(f"missing JSON artifact: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ContractError(f"invalid JSON artifact {path}: {exc}") from exc


def cycle_sections(text: str, hour: str) -> list[str]:
    """Return matching sections using the dashboard's any-H2 boundary."""
    matches = list(H2_RE.finditer(text))
    sections: list[str] = []
    expected = f"{hour}:00 UTC"
    for index, match in enumerate(matches):
        if match.group("title").strip() != expected:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append(text[match.start() : end])
    return sections


def public_item_count(section: str) -> int:
    section = HTML_COMMENT_RE.sub("", section)

    def visible_text(fragment: str) -> str:
        without_tags = re.sub(r"<[^>]+>", "", fragment)
        return html.unescape(without_tags).replace("\xa0", " ").strip()

    stories = 0
    for block in STORY_BLOCK_RE.finditer(section):
        class_match = CLASS_RE.search(block.group("attrs"))
        if class_match is None or "twitter-story" not in class_match.group("classes").split():
            continue
        body = block.group("body")
        title = TITLE_RE.search(body)
        lead = LEAD_RE.search(body)
        if title is None or not visible_text(title.group("body")):
            continue
        if lead is None or not visible_text(lead.group("body")):
            continue
        if SOURCE_ANCHOR_RE.search(body) is None:
            continue
        stories += 1
    quick_hits = 0
    in_quick_hits = False
    for line in section.splitlines():
        stripped = line.strip()
        if re.fullmatch(r"###[ \t]+Quick hits[ \t]*", stripped, re.IGNORECASE):
            in_quick_hits = True
            continue
        if in_quick_hits and stripped.startswith("#"):
            in_quick_hits = False
        if in_quick_hits and re.match(r"^[-*][ \t]+\S", stripped) and X_STATUS_RE.search(stripped):
            quick_hits += 1
    return stories + quick_hits


def validate(
    *,
    backend: str,
    status_file: Path,
    digest_file: Path,
    summary_file: Path,
    date: str,
    hour: str,
    generated_at: str,
    run_id: str,
    run_attempt: int,
    headlines_file: Path | None = None,
) -> None:
    status = load_json(status_file)
    if not isinstance(status, dict):
        raise ContractError("status must be a JSON object")

    expected = {
        "schema_version": 1,
        "date": date,
        "hour": f"{hour}:00 UTC",
        "generated_at": generated_at,
        "run_id": run_id,
        "run_attempt": run_attempt,
    }
    for key, value in expected.items():
        if status.get(key) != value:
            raise ContractError(
                f"status {key} must equal this run's {value!r}; got {status.get(key)!r}"
            )

    state = status.get("status")
    public_items = status.get("public_items")
    recovery = status.get("recovery", False)
    if state not in {"published", "no_update"}:
        raise ContractError("status must be 'published' or 'no_update'")
    if isinstance(public_items, bool) or not isinstance(public_items, int) or public_items < 0:
        raise ContractError("public_items must be a non-negative integer")
    if not isinstance(recovery, bool):
        raise ContractError("recovery must be a boolean when present")
    if not summary_file.exists():
        raise ContractError(f"missing summary artifact: {summary_file}")

    digest = digest_file.read_text(encoding="utf-8") if digest_file.exists() else ""
    sections = cycle_sections(digest, hour)
    if len(sections) > 1:
        raise ContractError(f"digest contains {len(sections)} same-hour sections")

    if backend == "claude":
        if headlines_file is None:
            raise ContractError("Claude validation requires --headlines-file")
        headlines = load_json(headlines_file)
        if not isinstance(headlines, list):
            raise ContractError("headline artifact must be a JSON array")
    else:
        headlines = None

    if state == "published":
        if recovery:
            raise ContractError("published status cannot be a recovery heartbeat")
        if public_items < 1:
            raise ContractError("published status requires public_items > 0")
        if len(sections) != 1:
            raise ContractError("published status requires exactly one same-hour public section")
        section = sections[0]
        summary_match = re.search(
            r"^\*\*Cycle summary\*\*:[ \t]*(?P<summary>\S.*)$",
            section,
            re.MULTILINE,
        )
        if summary_match is None:
            raise ContractError("published section requires a non-empty Cycle summary")
        filler = FILLER_RE.search(section)
        if filler is not None:
            raise ContractError(f"public section contains operational/no-news filler: {filler.group(0)!r}")
        actual_items = public_item_count(section)
        if actual_items < 1:
            raise ContractError("published section has no story card or linked Quick-hit bullet")
        if actual_items != public_items:
            raise ContractError(
                f"public_items says {public_items}, but the section contains {actual_items} public items"
            )
        if summary_file.stat().st_size == 0:
            raise ContractError("published status requires a non-empty notification summary")
        return

    if public_items != 0:
        raise ContractError("no_update status requires public_items == 0")
    if sections and not recovery:
        raise ContractError("no_update status must not leave a same-hour public section")
    if summary_file.stat().st_size != 0:
        raise ContractError("no_update status requires an empty notification summary")
    if backend == "claude" and headlines != []:
        raise ContractError("no_update status requires an empty Claude headline array")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", required=True)
    parser.add_argument("--status-file", type=Path, required=True)
    parser.add_argument("--digest-file", type=Path, required=True)
    parser.add_argument("--summary-file", type=Path, required=True)
    parser.add_argument("--headlines-file", type=Path)
    parser.add_argument("--date", required=True)
    parser.add_argument("--hour", required=True)
    parser.add_argument("--generated-at", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--run-attempt", type=int, required=True)
    args = parser.parse_args(argv)

    try:
        validate(
            backend=args.backend,
            status_file=args.status_file,
            digest_file=args.digest_file,
            summary_file=args.summary_file,
            headlines_file=args.headlines_file,
            date=args.date,
            hour=args.hour,
            generated_at=args.generated_at,
            run_id=args.run_id,
            run_attempt=args.run_attempt,
        )
    except ContractError as exc:
        parser.error(str(exc))
    print(f"validated Twitter public-output contract: {args.status_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
