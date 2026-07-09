#!/usr/bin/env python3
"""Deterministic fallback writer for scheduled Twitter/X lanes.

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
DEFAULT_MAX_AGE_HOURS = 36
FUTURE_SKEW = dt.timedelta(minutes=15)


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


def parse_timestamp(value: str) -> dt.datetime | None:
    text = clean_text(value)
    for fmt in ("%Y-%m-%d %H:%M UTC", "%Y-%m-%d %H:%M:%S UTC"):
        try:
            return dt.datetime.strptime(text, fmt).replace(tzinfo=dt.timezone.utc)
        except ValueError:
            pass
    return parse_datetime(text)


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


def iter_all_rows(path: Path) -> list[tuple[str, dict[str, Any]]]:
    """Return tweet-like rows from birdy's aggregate all.json snapshot."""
    try:
        payload = json.loads(path.read_text(encoding="utf-8") or "{}")
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(payload, dict):
        return []

    rows: list[tuple[str, dict[str, Any]]] = []
    for group in ("accounts", "searches"):
        values = payload.get(group)
        if not isinstance(values, dict):
            continue
        for name, items in values.items():
            if not isinstance(items, list):
                continue
            source = f"{group[:-1]}-{clean_text(name) or 'unknown'}"
            rows.extend((source, row) for row in items if isinstance(row, dict))

    news = payload.get("news")
    if isinstance(news, list):
        rows.extend(("news", row) for row in news if isinstance(row, dict))
    return rows


def is_fresh(created_at: dt.datetime | None, end_time: dt.datetime, max_age: dt.timedelta) -> bool:
    if created_at is None:
        return False
    return end_time - max_age <= created_at <= end_time + FUTURE_SKEW


def add_tweet(
    tweets: dict[str, Tweet],
    row: dict[str, Any],
    source: str,
    end_time: dt.datetime,
    max_age: dt.timedelta,
) -> None:
    author = author_handle(row)
    tid = tweet_id(row)
    text = tweet_text(row)
    url = tweet_url(row, author, tid)
    created_at = parse_datetime(row.get("createdAt") or nested(row, "legacy", "created_at"))
    if not text or not url or not is_fresh(created_at, end_time, max_age):
        return
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
        created_at=created_at,
    )
    existing = tweets.get(key)
    if existing is None or tweet.score > existing.score:
        tweets[key] = tweet


def collect_tweets(input_dir: Path, limit: int, end_time: dt.datetime, max_age_hours: int) -> list[Tweet]:
    tweets: dict[str, Tweet] = {}
    max_age = dt.timedelta(hours=max_age_hours)

    # The production Claude lane fetches an aggregate all.json. Prefer it when
    # present so fallback recovery uses the same raw snapshot the agent prompt
    # referenced; otherwise use the comparison lane's per-source JSON files.
    for source, row in iter_all_rows(input_dir / "all.json"):
        add_tweet(tweets, row, source, end_time, max_age)

    if tweets:
        return rank_tweets(tweets, limit)

    for path in sorted(input_dir.glob("*.json")):
        if path.name in {"all.json", "manifest.json"}:
            continue
        source = path.stem
        for row in iter_rows(path):
            add_tweet(tweets, row, source, end_time, max_age)

    return rank_tweets(tweets, limit)


def rank_tweets(tweets: dict[str, Tweet], limit: int) -> list[Tweet]:
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
            "- Next scheduled Twitter/X AI monitor run.",
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
            "WATCH: Next scheduled Twitter/X AI monitor run.\n\n"
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
    parser.add_argument("--headlines-file", type=Path)
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--max-age-hours", type=int, default=DEFAULT_MAX_AGE_HOURS)
    args = parser.parse_args(argv)

    end_time = parse_timestamp(args.timestamp)
    if end_time is None:
        raise SystemExit(f"Could not parse --timestamp as UTC time: {args.timestamp!r}")

    tweets = collect_tweets(args.input_dir, args.limit, end_time, args.max_age_hours)
    digest_path = args.out_dir / f"{args.date}.md"
    summary_path = args.summaries_dir / f"{args.date}-{args.summary_slug}-{args.hour}h-summary.txt"

    header, digest = render_digest(args.date, args.hour, args.title_suffix, tweets)
    changed = append_if_missing(digest_path, header, digest)
    atomic_write(summary_path, render_summary(args.timestamp, args.title_suffix, tweets))
    if args.headlines_file is not None:
        atomic_write(args.headlines_file, "[]\n")

    print(f"wrote {digest_path} ({'changed' if changed else 'already had section'})")
    print(f"wrote {summary_path}")
    if args.headlines_file is not None:
        print(f"wrote {args.headlines_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
