#!/usr/bin/env python3
"""Deterministic fallback writer for the hourly RSS lane.

The model lane is still the preferred curator, but RSS extraction itself is a
structured-data problem. This script keeps the workflow useful when the model
provider is unavailable by parsing the already-fetched XML files and appending
a timestamped daily section.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import email.utils
import html
import os
import re
import sys
import tempfile
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable


SOURCE_GROUPS = {
    "company": ("Company Announcements", ("openai", "anthropic", "google_deepmind", "huggingface")),
    "tech": (
        "Tech News",
        (
            "techcrunch",
            "the_verge",
            "venturebeat",
            "ars_technica",
            "mit_technology_review",
            "the_decoder",
            "marktechpost",
        ),
    ),
    "expert": (
        "Expert Commentary",
        ("simon_willison", "interconnects", "import_ai", "one_useful_thing"),
    ),
    "papers": ("New arXiv Papers", ("arxiv_cs_ai", "arxiv_cs_lg")),
}


@dataclasses.dataclass(frozen=True)
class Source:
    key: str
    filename: str
    label: str
    group: str
    ai_filter: bool = False


SOURCES = (
    Source("openai", "openai.xml", "OpenAI", "company"),
    Source("anthropic", "anthropic.xml", "Anthropic", "company"),
    Source("google_deepmind", "google_ai.xml", "Google/DeepMind", "company"),
    Source("google_deepmind", "deepmind.xml", "Google/DeepMind", "company"),
    Source("huggingface", "huggingface.xml", "Hugging Face", "company"),
    Source("arxiv_cs_ai", "arxiv_ai.xml", "CS.AI", "papers"),
    Source("arxiv_cs_lg", "arxiv_lg.xml", "CS.LG", "papers"),
    Source("techcrunch", "techcrunch_ai.xml", "TechCrunch", "tech"),
    Source("the_verge", "verge_ai.xml", "The Verge", "tech"),
    Source("venturebeat", "venturebeat_ai.xml", "VentureBeat", "tech"),
    Source("ars_technica", "arstechnica_ai.xml", "Ars Technica", "tech"),
    Source("mit_technology_review", "mit_tech_review_ai.xml", "MIT Technology Review", "tech"),
    Source("the_decoder", "the_decoder.xml", "The Decoder", "tech"),
    Source("marktechpost", "marktechpost.xml", "MarkTechPost", "tech"),
    Source("simon_willison", "simonwillison.xml", "Simon Willison", "expert", True),
    Source("interconnects", "interconnects.xml", "Interconnects (Nathan Lambert)", "expert"),
    Source("import_ai", "import_ai.xml", "Import AI (Jack Clark)", "expert"),
    Source("one_useful_thing", "one_useful_thing.xml", "One Useful Thing", "expert"),
)


AI_TERMS = re.compile(
    r"\b(ai|agent|agents|agentic|alignment|anthropic|benchmark|claude|codex|"
    r"deepseek|diffusion|eval|evaluation|frontier|gpt|gpu|inference|llama|llm|"
    r"machine learning|model|openai|post-training|prompt|reasoning|robot|"
    r"safety|synthetic data|transformer)\b",
    re.I,
)


@dataclasses.dataclass(frozen=True)
class FeedItem:
    source: Source
    title: str
    url: str
    published_at: dt.datetime | None
    summary: str


def clean_text(value: str | None) -> str:
    value = re.sub(r"<[^>]+>", " ", value or "")
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


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


def parse_timestamp(value: str) -> dt.datetime:
    parsed = parse_datetime(value)
    if parsed is not None:
        return parsed
    try:
        parsed = dt.datetime.strptime(value, "%Y-%m-%d %H:%M UTC")
    except ValueError as exc:
        raise ValueError(f"invalid timestamp {value!r}") from exc
    return parsed.replace(tzinfo=dt.timezone.utc)


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


def find_link(entry: ET.Element, *, atom: bool, base_url: str) -> str:
    if atom:
        for child in list(entry):
            if local_name(child.tag) != "link":
                continue
            rel = child.get("rel")
            href = child.get("href")
            if href and rel in (None, "alternate"):
                return urllib.parse.urljoin(base_url, href)
        return ""
    return urllib.parse.urljoin(base_url, child_text(entry, "link"))


def iter_entries(root: ET.Element) -> tuple[bool, Iterable[ET.Element]]:
    atom = local_name(root.tag) == "feed"
    if atom:
        return True, [child for child in list(root) if local_name(child.tag) == "entry"]
    channel = next((child for child in list(root) if local_name(child.tag) == "channel"), None)
    parent = channel if channel is not None else root
    return False, [child for child in list(parent) if local_name(child.tag) == "item"]


# Common feed namespace prefixes that show up *inside* <item>/<entry> bodies
# (content:encoded, dc:date, media:*, ...). When we salvage an entry in
# isolation we re-declare them on a synthetic wrapper so those prefixed
# children don't trip an "unbound prefix" parse error.
_FEED_NAMESPACES = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "atom": "http://www.w3.org/2005/Atom",
    "media": "http://search.yahoo.com/mrss/",
    "slash": "http://purl.org/rss/1.0/modules/slash/",
    "wfw": "http://wellformedness.net/wfw/",
}

# Bytes that XML 1.0 forbids — a single stray one yields "not well-formed
# (invalid token)" and (with strict parsing) drops the entire feed.
_CONTROL_CHARS_RE = re.compile(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]")
# A bare '&' that is not the start of a numeric or named entity.
_BARE_AMP_RE = re.compile(rb"&(?!#[0-9]+;|#x[0-9a-fA-F]+;|[A-Za-z][A-Za-z0-9]*;)")
# Individual entry blocks, used for last-resort per-entry salvage.
_ENTRY_BLOCK_RE = re.compile(rb"<(item|entry)\b[^>]*>.*?</\1\s*>", re.DOTALL | re.IGNORECASE)


def _sanitize_xml(body: bytes) -> bytes:
    """Repair the two malformations that most often break otherwise-valid feeds:
    invalid XML control bytes and bare ampersands."""
    body = _CONTROL_CHARS_RE.sub(b"", body)
    return _BARE_AMP_RE.sub(b"&amp;", body)


def _salvage_entries(body: bytes) -> list[ET.Element]:
    """Recover whatever <item>/<entry> blocks still parse on their own.

    A single mismatched tag (or a truncated download) makes strict
    ``ET.fromstring`` reject the *whole* feed, throwing away every good entry.
    Here we extract each entry block and parse it in isolation under a wrapper
    that re-declares the common feed namespaces, keeping the survivors.
    """
    ns_decl = " ".join(
        f'xmlns:{prefix}="{uri}"' for prefix, uri in _FEED_NAMESPACES.items()
    ).encode()
    recovered: list[ET.Element] = []
    for match in _ENTRY_BLOCK_RE.finditer(body):
        wrapped = b"<__salvage__ " + ns_decl + b">" + _sanitize_xml(match.group(0)) + b"</__salvage__>"
        try:
            node = ET.fromstring(wrapped)
        except ET.ParseError:
            continue
        recovered.extend(list(node))
    return recovered


def resilient_entries(body: bytes) -> tuple[bool, list[ET.Element]]:
    """Parse a feed body into (is_atom, entry_elements), tolerating malformed XML.

    Fast path is strict parsing; on failure we retry after sanitizing, then fall
    back to per-entry salvage. Only when nothing at all is recoverable does the
    original ``ET.ParseError`` propagate (so a genuinely non-feed body — e.g. an
    HTML error page from a proxy — still surfaces as a Feed Note)."""
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        try:
            root = ET.fromstring(_sanitize_xml(body))
        except ET.ParseError:
            entries = _salvage_entries(body)
            if not entries:
                raise
            atom = any(local_name(entry.tag) == "entry" for entry in entries)
            return atom, entries
    atom, entries = iter_entries(root)
    return atom, list(entries)


def parse_feed(source: Source, body: bytes) -> list[FeedItem]:
    atom, entries = resilient_entries(body)
    items: list[FeedItem] = []
    for entry in entries:
        title = child_text(entry, "title")
        url = find_link(entry, atom=atom, base_url=source.filename)
        if atom:
            date_value = child_text(entry, "published") or child_text(entry, "updated")
            summary = child_text(entry, "summary") or child_text(entry, "content")
        else:
            date_value = child_text(entry, "pubDate", "published", "updated", "date")
            summary = child_text(entry, "description", "summary", "encoded", "content")
        if not title or not url:
            continue
        summary = summary[:320]
        text_for_filter = f"{title} {summary}"
        if source.ai_filter and not AI_TERMS.search(text_for_filter):
            continue
        items.append(
            FeedItem(
                source=source,
                title=title,
                url=canonical_url(url),
                published_at=parse_datetime(date_value),
                summary=summary,
            )
        )
    return items


def collect_items(input_dir: Path, now: dt.datetime, lookback_hours: int) -> tuple[list[FeedItem], list[str]]:
    threshold = now - dt.timedelta(hours=lookback_hours)
    items: list[FeedItem] = []
    errors: list[str] = []
    for source in SOURCES:
        path = input_dir / source.filename
        if not path.exists():
            errors.append(f"{source.filename}: missing")
            continue
        try:
            parsed = parse_feed(source, path.read_bytes())
        except ET.ParseError as exc:
            errors.append(f"{source.filename}: parse error: {exc}")
            continue
        except OSError as exc:
            errors.append(f"{source.filename}: read error: {exc}")
            continue
        for item in parsed:
            if item.published_at is None:
                continue
            if threshold <= item.published_at <= now + dt.timedelta(minutes=10):
                items.append(item)
    return dedupe_items(items), errors


def dedupe_items(items: Iterable[FeedItem]) -> list[FeedItem]:
    by_url: dict[str, FeedItem] = {}
    for item in items:
        previous = by_url.get(item.url)
        if previous is None or (
            item.published_at is not None
            and (previous.published_at is None or item.published_at > previous.published_at)
        ):
            by_url[item.url] = item
    return sorted(
        by_url.values(),
        key=lambda item: (
            item.source.group,
            item.source.label,
            -(item.published_at.timestamp() if item.published_at else 0),
            item.title,
        ),
    )


def markdown_escape(value: str) -> str:
    return value.replace("|", r"\|").replace("\n", " ")


def published_label(item: FeedItem) -> str:
    if item.published_at is None:
        return "unknown date"
    return item.published_at.strftime("%b %-d")


def existing_urls(markdown: str) -> set[str]:
    return {canonical_url(match) for match in re.findall(r"\]\((https?://[^)\s]+)\)", markdown)}


def render_section(timestamp: str, items: list[FeedItem], errors: list[str], existing: str) -> str:
    seen_urls = existing_urls(existing)
    fresh = [item for item in items if item.url not in seen_urls]
    grouped: dict[str, dict[str, list[FeedItem]]] = {}
    for item in fresh:
        grouped.setdefault(item.source.group, {}).setdefault(item.source.label, []).append(item)

    lines = [f"## {timestamp} Update", ""]
    if not fresh:
        lines.extend(["_No new updates this hour._", ""])
    else:
        for group_key, (group_label, source_order) in SOURCE_GROUPS.items():
            group = grouped.get(group_key, {})
            if not group:
                continue
            lines.extend([f"### {group_label}", ""])
            ordered_labels = [
                source.label
                for source_key in source_order
                for source in SOURCES
                if source.key == source_key
            ]
            for label in dict.fromkeys(ordered_labels):
                label_items = group.get(label, [])
                if not label_items:
                    continue
                lines.extend([f"#### {label}", ""])
                for item in label_items[:8]:
                    lines.append(
                        f"- [{markdown_escape(item.title)}]({item.url}) - {published_label(item)}"
                    )
                    if item.summary:
                        lines.append(f"  > {markdown_escape(item.summary)}")
                    lines.append("")

    if errors:
        lines.extend(["### Feed Notes", ""])
        for error in errors:
            lines.append(f"- {markdown_escape(error)}")
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


def update_digest(input_dir: Path, out_dir: Path, target_date: str, timestamp: str, lookback_hours: int) -> Path:
    now = parse_timestamp(timestamp)
    out_path = out_dir / f"{target_date}.md"
    existing = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
    heading = f"# Official AI News - {target_date}\n\n"
    if f"## {timestamp} Update" in existing:
        print(f"{out_path} already has section {timestamp}; no write needed")
        return out_path
    items, errors = collect_items(input_dir, now, lookback_hours)
    section = render_section(timestamp, items, errors, existing)
    body = existing.rstrip() + "\n\n" + section if existing else heading + section
    write_atomic(out_path, body)
    print(f"Wrote {out_path} with {len(items)} candidate item(s) and {len(errors)} feed note(s)")
    return out_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=Path("/tmp/rss"))
    parser.add_argument("--out-dir", type=Path, default=Path("research/rss"))
    parser.add_argument("--date", required=True)
    parser.add_argument("--timestamp", required=True)
    parser.add_argument("--lookback-hours", type=int, default=24)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    update_digest(args.input_dir, args.out_dir, args.date, args.timestamp, args.lookback_hours)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
