#!/usr/bin/env python3
"""Filter and record delivered Twitter headline alerts.

This is intentionally an alert-send ledger, not a global news/event store. The
workflow already has a structured boundary at `*-headlines.json`; this script
keeps Telegram/Hooker sends from repeating previously delivered alert items.
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit


RETENTION_DEFAULT = 3000
URL_SIMILARITY_THRESHOLD = 0.62
STOPWORDS = {
    "A",
    "AN",
    "AND",
    "ARE",
    "AS",
    "AT",
    "BY",
    "FOR",
    "FROM",
    "IN",
    "INTO",
    "IS",
    "NEW",
    "NOW",
    "OF",
    "ON",
    "OR",
    "OVER",
    "THE",
    "TO",
    "VIA",
    "WITH",
}
TRACKING_PARAMS = {
    "cmpid",
    "fbclid",
    "gclid",
    "igshid",
    "mc_cid",
    "mc_eid",
    "ref",
    "s",
    "si",
}


@dataclass(frozen=True)
class Keys:
    headline_key: str
    url_key: str
    external_key: str
    story_key: str


def load_json_list(path: Path, *, missing_ok: bool = False) -> list[Any]:
    if missing_ok and not path.exists():
        return []
    try:
        data = json.loads(path.read_text() or "[]")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(data, list):
        raise SystemExit(f"{path}: expected a JSON array")
    return data


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    tmp.replace(path)


def normalize_headline(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "").upper()
    text = re.sub(r"HTTPS?://\S+", " ", text)
    text = re.sub(r"(?<!\d)\.(?!\d)", " ", text)
    text = re.sub(r"[^A-Z0-9.$]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def headline_tokens(text: str) -> set[str]:
    return {
        token
        for token in normalize_headline(text).split()
        if len(token) > 1 and token not in STOPWORDS
    }


def headline_similarity(left: str, right: str) -> float:
    left_tokens = headline_tokens(left)
    right_tokens = headline_tokens(right)
    if not left_tokens or not right_tokens:
        return 0.0
    overlap = len(left_tokens & right_tokens)
    containment = overlap / min(len(left_tokens), len(right_tokens))
    jaccard = overlap / len(left_tokens | right_tokens)
    return max(containment, jaccard)


def _clean_query(query: str) -> str:
    pairs: list[tuple[str, str]] = []
    for key, values in parse_qs(query, keep_blank_values=False).items():
        lower = key.lower()
        if lower.startswith("utm_") or lower in TRACKING_PARAMS:
            continue
        for value in values:
            pairs.append((lower, value))
    return urlencode(sorted(pairs), doseq=True)


def normalize_url(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return ""
    if url.startswith("//"):
        url = "https:" + url
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", url):
        url = "https://" + url

    parts = urlsplit(url)
    scheme = "https" if parts.scheme in {"http", "https"} else parts.scheme.lower()
    host = parts.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    if host in {"twitter.com", "mobile.twitter.com"}:
        host = "x.com"
    path = re.sub(r"/+", "/", parts.path).rstrip("/")
    query = _clean_query(parts.query)
    return urlunsplit((scheme, host, path, query, ""))


def external_key(url: str) -> str:
    normalized = normalize_url(url)
    if not normalized:
        return ""
    parts = urlsplit(normalized)
    if parts.netloc == "x.com":
        status = re.match(r"^/([^/]+)/status/(\d+)$", parts.path)
        if status:
            return f"x:status:{status.group(2)}"
        trend = re.match(r"^/i/trending/(\d+)$", parts.path)
        if trend:
            return f"x:trend:{trend.group(1)}"
        if parts.path == "/search":
            query = parse_qs(parts.query).get("q", [""])[0].strip().lower()
            if query:
                digest = hashlib.sha256(query.encode()).hexdigest()[:16]
                return f"x:search:{digest}"
    digest = hashlib.sha256(normalized.encode()).hexdigest()[:24]
    return f"url:{digest}"


def item_keys(item: dict[str, Any]) -> Keys:
    headline = str(item.get("headline") or "")
    url = str(item.get("url") or "")
    story = normalize_headline(str(item.get("story_key") or ""))
    return Keys(
        headline_key=normalize_headline(headline),
        url_key=normalize_url(url),
        external_key=external_key(url),
        story_key=story,
    )


def make_record(item: dict[str, Any], delivered_at: str, *, source_file: str = "") -> dict[str, Any]:
    keys = item_keys(item)
    record = {
        "headline": item.get("headline", ""),
        "source": item.get("source", ""),
        "url": item.get("url", ""),
        "category": item.get("category", ""),
        "delivered_at": delivered_at,
        "headline_key": keys.headline_key,
        "url_key": keys.url_key,
        "external_key": keys.external_key,
    }
    if keys.story_key:
        record["story_key"] = keys.story_key
    if source_file:
        record["source_file"] = source_file
        record["backfilled"] = True
    return record


def duplicate_reason(item: dict[str, Any], history: list[dict[str, Any]]) -> str:
    keys = item_keys(item)
    if not keys.headline_key:
        return "invalid_headline"
    if not keys.url_key:
        return "invalid_url"

    headline = str(item.get("headline") or "")
    for record in history:
        record_headline = str(record.get("headline") or "")
        if keys.story_key and keys.story_key == record.get("story_key"):
            return "duplicate_story_key"
        if keys.headline_key == record.get("headline_key"):
            return "duplicate_headline"
        same_external = keys.external_key and keys.external_key == record.get("external_key")
        same_url = keys.url_key and keys.url_key == record.get("url_key")
        if same_external or same_url:
            similarity = headline_similarity(headline, record_headline)
            if similarity >= URL_SIMILARITY_THRESHOLD:
                return "duplicate_source_similar_headline"
    return ""


def filter_headlines(args: argparse.Namespace) -> int:
    incoming_raw = load_json_list(Path(args.headlines_file), missing_ok=True)
    history_raw = load_json_list(Path(args.history_file), missing_ok=True)
    history = [item for item in history_raw if isinstance(item, dict)]
    accepted: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()

    for item in incoming_raw:
        if not isinstance(item, dict):
            counts["invalid_item"] += 1
            continue
        reason = duplicate_reason(item, history)
        if reason:
            counts[reason] += 1
            continue
        accepted.append(item)
        history.append(make_record(item, args.timestamp))
        counts["new"] += 1

    write_json(Path(args.filtered_file), accepted)
    summary = {
        "incoming": len(incoming_raw),
        "new": len(accepted),
        "suppressed": len(incoming_raw) - len(accepted),
        "reason_counts": dict(sorted(counts.items())),
        "history_size": len(history_raw),
    }
    print(json.dumps(summary, sort_keys=True))
    return 0


def record_delivered(args: argparse.Namespace) -> int:
    delivered_raw = load_json_list(Path(args.delivered_file), missing_ok=True)
    history_raw = load_json_list(Path(args.history_file), missing_ok=True)
    history = [item for item in history_raw if isinstance(item, dict)]

    for item in delivered_raw:
        if not isinstance(item, dict):
            continue
        history.append(make_record(item, args.timestamp))

    retained = history[-args.retention :]
    write_json(Path(args.history_file), retained)
    print(
        json.dumps(
            {
                "recorded": len([i for i in delivered_raw if isinstance(i, dict)]),
                "history_size_before": len(history_raw),
                "history_size_after": len(retained),
            },
            sort_keys=True,
        )
    )
    return 0


def timestamp_from_headline_file(path: Path) -> str:
    match = re.match(r"^(\d{4}-\d{2}-\d{2})-twitter-(\d{2})h-headlines\.json$", path.name)
    if match:
        return f"{match.group(1)} {match.group(2)}:00 UTC"
    return ""


def backfill(args: argparse.Namespace) -> int:
    records: list[dict[str, Any]] = []
    for filename in sorted(glob.glob(args.glob)):
        path = Path(filename)
        delivered_at = timestamp_from_headline_file(path) or args.timestamp
        for item in load_json_list(path, missing_ok=False):
            if isinstance(item, dict):
                records.append(make_record(item, delivered_at, source_file=str(path)))
    retained = records[-args.retention :]
    write_json(Path(args.history_file), retained)
    print(json.dumps({"backfilled": len(records), "history_size": len(retained)}, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    filter_parser = subparsers.add_parser("filter")
    filter_parser.add_argument("--headlines-file", required=True)
    filter_parser.add_argument("--history-file", required=True)
    filter_parser.add_argument("--filtered-file", required=True)
    filter_parser.add_argument("--timestamp", required=True)
    filter_parser.set_defaults(func=filter_headlines)

    record_parser = subparsers.add_parser("record-delivered")
    record_parser.add_argument("--delivered-file", required=True)
    record_parser.add_argument("--history-file", required=True)
    record_parser.add_argument("--timestamp", required=True)
    record_parser.add_argument("--retention", type=int, default=RETENTION_DEFAULT)
    record_parser.set_defaults(func=record_delivered)

    backfill_parser = subparsers.add_parser("backfill")
    backfill_parser.add_argument("--glob", required=True)
    backfill_parser.add_argument("--history-file", required=True)
    backfill_parser.add_argument("--timestamp", default="")
    backfill_parser.add_argument("--retention", type=int, default=RETENTION_DEFAULT)
    backfill_parser.set_defaults(func=backfill)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
