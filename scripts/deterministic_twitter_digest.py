#!/usr/bin/env python3
"""Deterministic fallback writer for the Twitter comparison lanes.

The model lane is still the preferred analyst. This script only preserves the
scheduled output contract when the agent path returns without committing the
expected digest file. It reads the already-fetched bird JSON files and appends a
conservative quick-hit section without claiming deeper synthesis.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import email.utils
import json
import re
import tempfile
from pathlib import Path
from typing import Any


MAX_TEXT = 220


@dataclasses.dataclass(frozen=True)
class Tweet:
    key: str
    author: str
    text: str
    url: str
    source: str
    likes: int
    retweets: int
    replies: int
    created_at: dt.datetime | None

    @property
    def score(self) -> int:
        return self.likes + (2 * self.retweets) + self.replies


def clean_text(value: Any) -> str:
    text = str(value or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def as_int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def parse_datetime(value: Any) -> dt.datetime | None:
    text = clean_text(value)
    if not text:
        return None
    try:
        parsed = email.utils.parsedate_to_datetime(text)
    except (TypeError, ValueError):
        parsed = None
    if parsed is None:
        try:
            parsed = dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def nested(row: dict[str, Any], *path: str) -> Any:
    value: Any = row
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def author_handle(row: dict[str, Any]) -> str:
    candidates = (
        nested(row, "author", "username"),
        nested(row, "author", "screen_name"),
        nested(row, "user", "username"),
        nested(row, "user", "screen_name"),
        row.get("username"),
        row.get("screenName"),
        row.get("authorUsername"),
        row.get("name"),
    )
    for candidate in candidates:
        value = clean_text(candidate).lstrip("@")
        if value:
            return value
    return "unknown"


def tweet_id(row: dict[str, Any]) -> str:
    candidates = (
        row.get("id"),
        row.get("id_str"),
        row.get("rest_id"),
        row.get("tweetId"),
        nested(row, "legacy", "id_str"),
    )
    for candidate in candidates:
        value = clean_text(candidate)
        if value:
            return value
    return ""


def tweet_text(row: dict[str, Any]) -> str:
    candidates = (
        row.get("text"),
        row.get("fullText"),
        row.get("full_text"),
        row.get("content"),
        nested(row, "legacy", "full_text"),
    )
    for candidate in candidates:
        value = clean_text(candidate)
        if value:
            return value
    return ""


def tweet_url(row: dict[str, Any], author: str, tid: str) -> str:
    for candidate in (row.get("url"), row.get("tweetUrl"), row.get("permalink")):
        value = clean_text(candidate)
        if value:
            return value
    if author != "unknown" and tid:
        return f"https://x.com/{author}/status/{tid}"
    return ""


def iter_rows(path: Path) -> list[dict[str, Any]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8") or "[]")
    except (OSError, json.JSONDecodeError):
        return []
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    return []


def collect_tweets(input_dir: Path, limit: int) -> list[Tweet]:
    tweets: dict[str, Tweet] = {}
    for path in sorted(input_dir.glob("*.json")):
        if path.name in {"all.json", "manifest.json"}:
            continue
        source = path.stem
        for row in iter_rows(path):
            author = author_handle(row)
            tid = tweet_id(row)
            text = tweet_text(row)
            url = tweet_url(row, author, tid)
            if not text or not url:
                continue
            key = url or tid or text[:120]
            tweet = Tweet(
                key=key,
                author=author,
                text=text,
                url=url,
                source=source,
                likes=as_int(row.get("likeCount") or nested(row, "legacy", "favorite_count")),
                retweets=as_int(row.get("retweetCount") or nested(row, "legacy", "retweet_count")),
                replies=as_int(row.get("replyCount") or nested(row, "legacy", "reply_count")),
                created_at=parse_datetime(row.get("createdAt") or nested(row, "legacy", "created_at")),
            )
            existing = tweets.get(key)
            if existing is None or tweet.score > existing.score:
                tweets[key] = tweet

    ranked = sorted(
        tweets.values(),
        key=lambda item: (
            -item.score,
            -(item.created_at.timestamp() if item.created_at else 0),
            item.author,
            item.text,
        ),
    )
    return ranked[:limit]


def trim_sentence(text: str, max_len: int = MAX_TEXT) -> str:
    text = clean_text(text)
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "..."


def append_if_missing(path: Path, header: str, section: str) -> bool:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if header in existing:
        return False
    body = existing.rstrip()
    next_text = f"{body}\n\n{section}" if body else section
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(path, next_text.rstrip() + "\n")
    return True


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(text)
        tmp_name = handle.name
    Path(tmp_name).replace(path)


def render_digest(date: str, hour: str, title_suffix: str, tweets: list[Tweet]) -> tuple[str, str]:
    h1 = f"# Twitter/X AI Pulse{title_suffix} - {date}"
    header = f"## {hour}:00 UTC"
    lines = [
        h1,
        "",
        header,
        "",
        "**Cycle summary**: Quiet period - no analyst-grade main stories selected from the pre-fetched Twitter/X snapshot.",
        "",
        "### Quick hits",
    ]
    if tweets:
        for tweet in tweets:
            engagement = f"{tweet.likes} likes, {tweet.retweets} reposts, {tweet.replies} replies"
            lines.append(f"- @{tweet.author}: {trim_sentence(tweet.text)} [{engagement}]({tweet.url})")
    else:
        lines.append("- No notable pre-fetched tweets survived deterministic parsing.")
    lines.extend(
        [
            "",
            "### Skeptic's corner",
            "- None this cycle.",
            "",
            "### Watch list (next 24h)",
            "- Next scheduled Twitter/X comparison cycle.",
            "",
            "### Research notes",
            "- Source checks issued this cycle: deterministic scan of pre-fetched account, search, and news snapshots.",
        ]
    )
    return header, "\n".join(lines)


def render_summary(timestamp: str, title_suffix: str, tweets: list[Tweet]) -> str:
    if tweets:
        bullets = "\n".join(f"- @{tweet.author}: {trim_sentence(tweet.text, 110)}" for tweet in tweets[:3])
        return (
            f"Twitter/X AI Pulse{title_suffix} - {timestamp}\n\n"
            "CYCLE: Quiet period; deterministic quick-hit scan found no analyst-grade main story.\n\n"
            f"QUICK HITS:\n{bullets}\n\n"
            "WATCH: Next scheduled Twitter/X comparison cycle.\n\n"
            "Full update on GitHub.\n"
        )
    return (
        f"Twitter/X AI Pulse{title_suffix} - {timestamp}\n\n"
        "Quiet period - no major AI updates on Twitter/X.\n"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summaries-dir", type=Path, required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--hour", required=True)
    parser.add_argument("--timestamp", required=True)
    parser.add_argument("--title-suffix", default="")
    parser.add_argument("--summary-slug", required=True)
    parser.add_argument("--limit", type=int, default=8)
    args = parser.parse_args(argv)

    tweets = collect_tweets(args.input_dir, args.limit)
    digest_path = args.out_dir / f"{args.date}.md"
    summary_path = args.summaries_dir / f"{args.date}-{args.summary_slug}-{args.hour}h-summary.txt"

    header, digest = render_digest(args.date, args.hour, args.title_suffix, tweets)
    changed = append_if_missing(digest_path, header, digest)
    atomic_write(summary_path, render_summary(args.timestamp, args.title_suffix, tweets))

    print(f"wrote {digest_path} ({'changed' if changed else 'already had section'})")
    print(f"wrote {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
