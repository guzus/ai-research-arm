#!/usr/bin/env python3
"""Deterministic fallback composer for the Bluesky expert-commentary lane.

The model lane is still the preferred curator (it judges signal, not just
engagement). When the agent fails to produce `.tmp/bluesky-section.md`,
2h-bluesky.yml runs this script to compose the per-run section mechanically
from the staged per-account JSON files (`data/bluesky/*.json`, the
`app.bsky.feed.getAuthorFeed` responses fetched deterministically earlier in
the workflow).

Selection contract (mirrors the documented lane rules):
  - Skip reposts (`feed[].reason` set) — only original posts qualify.
  - Window: posts created in the last 48 hours.
  - Engagement floor: >=2 likes OR >=1 repost.
  - Rank by likes + 2*reposts, descending.
  - Caps: at most 8 bullets total, at most 3 per author (the lane's
    documented output budget — see the 2026-06-15 improvement log).

Output format matches the agent contract the workflow's append step expects:
a `## <timestamp>` heading, then one `### Highlights` subsection of
`- **@handle**: "excerpt..." - [link](...) (❤️ N, 🔄 M)` bullets. The append
step's parser keeps only `### ` headings and `- ` bullets, so the fallback
provenance marker rides in the `### ` heading text (a standalone note line
would be stripped before commit). Zero qualifying posts still writes the
heading plus `_No qualifying posts this cycle._` — same as the agent.

Malformed or missing per-account JSON is boundary-handled: that account is
skipped with a stderr note and the run continues. Stdlib-only; atomic write.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import json
import os
import re
import sys
import tempfile
from pathlib import Path

WINDOW_HOURS = 48
MIN_LIKES = 2
MIN_REPOSTS = 1
MAX_TOTAL = 8
MAX_PER_AUTHOR = 3
EXCERPT_MAX_CHARS = 180

FALLBACK_HEADING = "### Highlights — deterministic engagement-ranked fallback"
FALLBACK_NOTE = (
    "_Deterministic engagement-ranked fallback: the model curator was"
    " unavailable this cycle, so posts below are ranked by likes + 2×reposts"
    " only (no signal judgment)._"
)


@dataclasses.dataclass(frozen=True)
class BlueskyPost:
    handle: str
    text: str
    created_at: dt.datetime
    likes: int
    reposts: int
    uri: str

    @property
    def score(self) -> int:
        return self.likes + 2 * self.reposts

    @property
    def rkey(self) -> str:
        return self.uri.rsplit("/", 1)[-1]

    @property
    def link(self) -> str:
        return f"https://bsky.app/profile/{self.handle}/post/{self.rkey}"


def parse_datetime(value: str | None) -> dt.datetime | None:
    if not value or not isinstance(value, str):
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def parse_timestamp(value: str) -> dt.datetime:
    """Accept ISO-8601 or the workflow's `YYYY-MM-DD HH:MM UTC` format."""
    parsed = parse_datetime(value)
    if parsed is not None:
        return parsed
    try:
        parsed = dt.datetime.strptime(value, "%Y-%m-%d %H:%M UTC")
    except ValueError as exc:
        raise ValueError(f"invalid timestamp {value!r}") from exc
    return parsed.replace(tzinfo=dt.timezone.utc)


def excerpt(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > EXCERPT_MAX_CHARS:
        text = text[: EXCERPT_MAX_CHARS - 1].rstrip() + "…"
    return text


def coerce_count(value: object) -> int:
    return value if isinstance(value, int) and value >= 0 else 0


def extract_posts(payload: object, source_name: str) -> list[BlueskyPost]:
    """Posts from one getAuthorFeed response. Repost entries (feed[].reason
    set) are skipped; structurally-broken entries are skipped item-by-item."""
    if not isinstance(payload, dict) or not isinstance(payload.get("feed"), list):
        print(f"{source_name}: unexpected JSON shape (no feed[]); skipping", file=sys.stderr)
        return []
    posts: list[BlueskyPost] = []
    for item in payload["feed"]:
        if not isinstance(item, dict):
            continue
        if item.get("reason"):
            continue  # repost of someone else's post
        post = item.get("post")
        if not isinstance(post, dict):
            continue
        author = post.get("author") or {}
        record = post.get("record") or {}
        handle = author.get("handle") if isinstance(author, dict) else None
        text = record.get("text") if isinstance(record, dict) else None
        created_at = parse_datetime(record.get("createdAt") if isinstance(record, dict) else None)
        uri = post.get("uri")
        if not handle or not isinstance(text, str) or created_at is None or not isinstance(uri, str) or not uri:
            continue
        posts.append(
            BlueskyPost(
                handle=handle,
                text=text,
                created_at=created_at,
                likes=coerce_count(post.get("likeCount")),
                reposts=coerce_count(post.get("repostCount")),
                uri=uri,
            )
        )
    return posts


def load_posts(input_dir: Path) -> list[BlueskyPost]:
    posts: list[BlueskyPost] = []
    for path in sorted(input_dir.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"{path.name}: unreadable/malformed JSON ({exc}); skipping account", file=sys.stderr)
            continue
        posts.extend(extract_posts(payload, path.name))
    return posts


def select_posts(posts: list[BlueskyPost], now: dt.datetime) -> list[BlueskyPost]:
    threshold = now - dt.timedelta(hours=WINDOW_HOURS)
    ceiling = now + dt.timedelta(minutes=10)
    qualifying = [
        post
        for post in posts
        if threshold <= post.created_at <= ceiling
        and (post.likes >= MIN_LIKES or post.reposts >= MIN_REPOSTS)
    ]
    qualifying.sort(key=lambda post: (-post.score, post.created_at, post.uri))
    selected: list[BlueskyPost] = []
    per_author: dict[str, int] = {}
    seen_uris: set[str] = set()
    for post in qualifying:
        if len(selected) >= MAX_TOTAL:
            break
        if post.uri in seen_uris:
            continue
        if per_author.get(post.handle, 0) >= MAX_PER_AUTHOR:
            continue
        selected.append(post)
        seen_uris.add(post.uri)
        per_author[post.handle] = per_author.get(post.handle, 0) + 1
    return selected


def render_section(timestamp: str, posts: list[BlueskyPost]) -> str:
    lines = [f"## {timestamp}", ""]
    if not posts:
        lines.extend(["_No qualifying posts this cycle._", ""])
        return "\n".join(lines).rstrip() + "\n"
    lines.extend([FALLBACK_NOTE, "", FALLBACK_HEADING])
    for post in posts:
        lines.append(
            f'- **@{post.handle}**: "{excerpt(post.text)}" - '
            f"[link]({post.link}) (❤️ {post.likes}, 🔄 {post.reposts})"
        )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False, prefix=f".{path.name}.", suffix=".tmp"
    ) as handle:
        handle.write(text)
        tmp_path = Path(handle.name)
    os.replace(tmp_path, path)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=Path("data/bluesky"))
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(".tmp/bluesky-section.md"),
        help="Section output path (the workflow's append step reads this).",
    )
    parser.add_argument(
        "--timestamp",
        required=True,
        help="Section heading timestamp, e.g. '2026-07-02 10:15 UTC'. Also the"
        " reference time for the 48h window.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        now = parse_timestamp(args.timestamp)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if not args.input_dir.is_dir():
        print(f"error: input dir {args.input_dir} does not exist", file=sys.stderr)
        return 1

    posts = load_posts(args.input_dir)
    selected = select_posts(posts, now)
    write_atomic(args.out, render_section(args.timestamp, selected))
    print(
        f"Wrote {args.out}: {len(selected)} post(s) selected from "
        f"{len(posts)} fetched (window {WINDOW_HOURS}h, caps {MAX_TOTAL}/{MAX_PER_AUTHOR})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
