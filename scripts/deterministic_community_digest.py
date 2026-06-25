#!/usr/bin/env python3
"""Deterministic fallback writer for the HN/Reddit community lane."""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import email.utils
import html
import json
import os
import re
import sys
import tempfile
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


AI_TERMS = re.compile(
    r"\b(ai|agent|agents|agentic|alignment|anthropic|benchmark|claude|codex|"
    r"deepseek|diffusion|eval|evaluation|frontier|gpt|gpu|inference|llama|llm|"
    r"machine learning|model|neural|openai|post-training|prompt|rag|reasoning|"
    r"robot|safety|synthetic data|transformer|vibe coding)\b",
    re.I,
)
LOW_SIGNAL_TERMS = re.compile(r"\b(beginner|homework|meme|shitpost|wallpaper)\b", re.I)


@dataclasses.dataclass(frozen=True)
class HNItem:
    title: str
    url: str
    points: int
    comments: int
    object_id: str

    @property
    def discuss_url(self) -> str:
        return f"https://news.ycombinator.com/item?id={self.object_id}"


@dataclasses.dataclass(frozen=True)
class RedditItem:
    subreddit: str
    title: str
    url: str
    updated_at: dt.datetime | None


def clean_text(value: str | None) -> str:
    value = re.sub(r"<[^>]+>", " ", value or "")
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def markdown_escape(value: str) -> str:
    return value.replace("|", r"\|").replace("\n", " ")


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def child_text(element: ET.Element, *names: str) -> str:
    wanted = set(names)
    for child in list(element):
        if local_name(child.tag) in wanted:
            return clean_text("".join(child.itertext()))
    return ""


def parse_datetime(value: str | None) -> dt.datetime | None:
    value = clean_text(value)
    if not value:
        return None
    parsed: dt.datetime | None
    try:
        parsed = email.utils.parsedate_to_datetime(value)
    except (TypeError, ValueError):
        parsed = None
    if parsed is None:
        try:
            parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def canonical_url(url: str) -> str:
    parts = urllib.parse.urlsplit(url.strip())
    query = [
        (key, value)
        for key, value in urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
        if not key.lower().startswith("utm_") and key.lower() not in {"fbclid", "gclid"}
    ]
    path = parts.path
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    return urllib.parse.urlunsplit(
        (parts.scheme.lower(), parts.netloc.lower(), path, urllib.parse.urlencode(query, doseq=True), "")
    )


def is_relevant(text: str) -> bool:
    return bool(AI_TERMS.search(text)) and not LOW_SIGNAL_TERMS.search(text)


def load_hn_items(path: Path, limit: int) -> list[HNItem]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        payload = {"hits": []}
    items: list[HNItem] = []
    for row in payload.get("hits", []):
        if not isinstance(row, dict):
            continue
        title = clean_text(row.get("title") or row.get("story_title"))
        object_id = clean_text(str(row.get("objectID") or ""))
        if not title or not object_id:
            continue
        text = " ".join(
            clean_text(str(row.get(key) or ""))
            for key in ("title", "story_title", "url", "story_text", "comment_text")
        )
        if not is_relevant(text):
            continue
        url = clean_text(row.get("url") or row.get("story_url")) or f"https://news.ycombinator.com/item?id={object_id}"
        try:
            points = int(row.get("points") or 0)
        except (TypeError, ValueError):
            points = 0
        try:
            comments = int(row.get("num_comments") or 0)
        except (TypeError, ValueError):
            comments = 0
        items.append(HNItem(title=title, url=canonical_url(url), points=points, comments=comments, object_id=object_id))
    items.sort(key=lambda item: (-item.points, -item.comments, item.title))
    return items[:limit]


def reddit_link(entry: ET.Element) -> str:
    for child in list(entry):
        if local_name(child.tag) != "link":
            continue
        href = child.get("href")
        if href:
            return href
    return child_text(entry, "link")


def parse_reddit_feed(path: Path, subreddit: str, limit: int) -> tuple[list[RedditItem], str | None]:
    try:
        root = ET.fromstring(path.read_bytes())
    except FileNotFoundError:
        return [], f"{path}: missing"
    except ET.ParseError as exc:
        return [], f"{path}: parse error: {exc}"
    except OSError as exc:
        return [], f"{path}: read error: {exc}"

    entries = [child for child in list(root) if local_name(child.tag) == "entry"]
    parsed: list[RedditItem] = []
    fallback: list[RedditItem] = []
    for entry in entries:
        title = child_text(entry, "title")
        url = reddit_link(entry)
        content = child_text(entry, "content", "summary")
        if not title or not url:
            continue
        item = RedditItem(
            subreddit=subreddit,
            title=title,
            url=canonical_url(url),
            updated_at=parse_datetime(child_text(entry, "updated", "published")),
        )
        if LOW_SIGNAL_TERMS.search(f"{title} {content}"):
            continue
        fallback.append(item)
        if is_relevant(f"{title} {content}"):
            parsed.append(item)
    selected = parsed or fallback
    selected.sort(key=lambda item: (-(item.updated_at.timestamp() if item.updated_at else 0), item.title))
    return selected[:limit], None


def existing_section(markdown: str, timestamp: str) -> bool:
    return f"## {timestamp}" in markdown


def section_body(timestamp: str, lines: list[str]) -> str:
    return "\n".join([f"## {timestamp}", "", *lines]).rstrip() + "\n"


def render_hn_section(timestamp: str, items: list[HNItem]) -> str:
    lines = ["### Top Stories", "", "| Title | Points | Comments | Link |", "|-------|--------|----------|------|"]
    if not items:
        lines.append("| _No AI-related HN front-page stories matched deterministic filters._ | - | - | - |")
    else:
        for item in items:
            lines.append(
                f"| [{markdown_escape(item.title)}]({item.url}) | {item.points} | {item.comments} | "
                f"[discuss]({item.discuss_url}) |"
            )
    lines.extend(["", "### Notable Discussions", ""])
    if not items:
        lines.append("- No deterministic HN discussion candidates this run.")
    else:
        for item in items[:8]:
            lines.append(
                f"- **{markdown_escape(item.title)}**: {item.points} points, "
                f"{item.comments} comments - [discuss]({item.discuss_url})"
            )
    return section_body(timestamp, lines)


def render_reddit_section(timestamp: str, by_subreddit: dict[str, list[RedditItem]], notes: list[str]) -> str:
    lines: list[str] = []
    for subreddit in ("MachineLearning", "LocalLLaMA", "artificial"):
        lines.extend(
            [
                f"### r/{subreddit} (Hot)",
                "",
                "| Title | Score | Comments | Link |",
                "|-------|-------|----------|------|",
            ]
        )
        items = by_subreddit.get(subreddit, [])
        if not items:
            lines.append("| _No matching RSS entries._ | N/A | - | - |")
        else:
            for item in items:
                lines.append(
                    f"| [{markdown_escape(item.title)}]({item.url}) | N/A | - | [link]({item.url}) |"
                )
        lines.append("")
    lines.extend(
        [
            "> Note: Reddit RSS does not expose score/comment counts; N/A reflects the source limitation.",
            "",
        ]
    )
    if notes:
        lines.extend(["### Feed Notes", ""])
        for note in notes:
            lines.append(f"- {markdown_escape(note)}")
    return section_body(timestamp, lines)


def write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False, prefix=f".{path.name}.", suffix=".tmp"
    ) as handle:
        handle.write(text)
        tmp_path = Path(handle.name)
    os.replace(tmp_path, path)


def append_daily_section(path: Path, title: str, timestamp: str, body: str) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if existing_section(existing, timestamp):
        print(f"{path} already has section {timestamp}; no write needed")
        return
    full = existing.rstrip() + "\n\n" + body if existing else f"# {title}\n\n{body}"
    write_atomic(path, full)
    print(f"Wrote {path}")


def update_digest(hn_path: Path, reddit_dir: Path, out_dir: Path, target_date: str, timestamp: str) -> tuple[Path, Path]:
    hn_items = load_hn_items(hn_path, limit=15)
    hn_out = out_dir / f"{target_date}-hn.md"
    append_daily_section(
        hn_out,
        f"Hacker News AI Digest - {target_date}",
        timestamp,
        render_hn_section(timestamp, hn_items),
    )

    reddit_specs = {
        "MachineLearning": "ml.rss",
        "LocalLLaMA": "localllama.rss",
        "artificial": "artificial.rss",
    }
    reddit_items: dict[str, list[RedditItem]] = {}
    notes: list[str] = []
    for subreddit, filename in reddit_specs.items():
        items, note = parse_reddit_feed(reddit_dir / filename, subreddit, limit=12)
        reddit_items[subreddit] = items
        if note:
            notes.append(note)
    reddit_out = out_dir / f"{target_date}-reddit.md"
    append_daily_section(
        reddit_out,
        f"Reddit AI Digest - {target_date}",
        timestamp,
        render_reddit_section(timestamp, reddit_items, notes),
    )
    return hn_out, reddit_out


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hn-json", type=Path, default=Path("data/hn/frontpage.json"))
    parser.add_argument("--reddit-dir", type=Path, default=Path("data/reddit"))
    parser.add_argument("--out-dir", type=Path, default=Path("research/community"))
    parser.add_argument("--date", required=True)
    parser.add_argument("--timestamp", required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    update_digest(args.hn_json, args.reddit_dir, args.out_dir, args.date, args.timestamp)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
