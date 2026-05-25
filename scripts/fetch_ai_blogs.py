#!/usr/bin/env python3
"""Fetch curated AI expert/blog feeds into a daily Markdown watch file.

This lane is intentionally separate from ``hourly-rss.yml`` because expert
blogs are analysis-heavy and duplicate-prone. The registry defines source
priority and tags; this script normalizes RSS/Atom entries, deduplicates URLs,
scores them, and writes a deterministic daily report.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import email.utils
import hashlib
import html
import json
import os
import re
import ssl
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = REPO_ROOT / "data" / "sources" / "ai_blogs.json"
DEFAULT_OUT_DIR = REPO_ROOT / "research" / "blogs"
USER_AGENT = "ai-research-arm/1.0 (https://github.com/guzus/ai-research-arm)"
BROWSER_UA = (
    "Mozilla/5.0 (compatible; AIResearchBot/1.0; "
    "+https://github.com/guzus/ai-research-arm)"
)
TIMEOUT_SECONDS = 25

ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}
CONTENT_NS = {"content": "http://purl.org/rss/1.0/modules/content/"}

PRIORITY_WEIGHT = {"P0": 100, "P1": 70, "P2": 40}
TYPE_WEIGHT = {
    "expert_blog": 15,
    "kol_substack": 10,
    "research_lab": 10,
    "vendor_blog": 0,
}
TAG_WEIGHT = {
    "agents": 12,
    "coding-agents": 12,
    "evals": 10,
    "evaluation": 10,
    "open-models": 10,
    "post-training": 10,
    "inference": 8,
    "llms": 8,
    "ai-engineering": 8,
    "production-ai": 8,
    "ai-security": 8,
    "frontier-research": 8,
    "policy": 5,
    "safety": 5,
}
TITLE_BONUS_PATTERNS = (
    (re.compile(r"\b(agent|agents|agentic|coding agent)\b", re.I), 12),
    (re.compile(r"\b(eval|evaluation|benchmark|reliability)\b", re.I), 10),
    (re.compile(r"\b(open[- ]?model|post[- ]?training|inference)\b", re.I), 10),
    (re.compile(r"\b(architecture|reasoning|alignment|hallucination)\b", re.I), 8),
    (re.compile(r"\b(release|launched|announced|introducing)\b", re.I), 5),
)
TITLE_PENALTY_PATTERNS = (
    (re.compile(r"\b(roundup|radar|last week|weekly recap)\b", re.I), -18),
    (re.compile(r"\b(podcast|transcript|video)\b", re.I), -8),
    (re.compile(r"\b(partner|partnership|customer story)\b", re.I), -10),
    (re.compile(r"\b(webinar|event|join us|hiring)\b", re.I), -15),
)
ROUNDUP_WORDS = {"roundup", "radar", "recap", "podcast", "transcript"}


@dataclasses.dataclass(frozen=True)
class Source:
    id: str
    name: str
    url: str
    feed_url: str
    type: str
    priority: str
    cadence: str
    tags: tuple[str, ...]
    include_in_digest: bool
    notes: str = ""


@dataclasses.dataclass(frozen=True)
class FeedItem:
    source: Source
    title: str
    url: str
    published_at: dt.datetime | None
    summary: str
    score: int
    content_hash: str

    @property
    def published_label(self) -> str:
        if not self.published_at:
            return "unknown date"
        return self.published_at.strftime("%Y-%m-%d %H:%M UTC")


def _build_ssl_context() -> ssl.SSLContext:
    cafile = os.environ.get("SSL_CERT_FILE")
    if cafile and os.path.isfile(cafile):
        return ssl.create_default_context(cafile=cafile)
    for p in (
        "/etc/ssl/cert.pem",
        "/etc/ssl/certs/ca-certificates.crt",
        "/etc/pki/tls/certs/ca-bundle.crt",
        "/opt/homebrew/etc/openssl@3/cert.pem",
        "/usr/local/etc/openssl@3/cert.pem",
    ):
        if os.path.isfile(p):
            return ssl.create_default_context(cafile=p)
    return ssl.create_default_context()


SSL_CTX = _build_ssl_context()


def clean_text(value: str | None) -> str:
    value = re.sub(r"<[^>]+>", " ", value or "")
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def canonical_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url.strip())
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    filtered = [
        (k, v)
        for k, v in query
        if not k.lower().startswith("utm_") and k.lower() not in {"fbclid", "gclid"}
    ]
    path = parsed.path
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    return urllib.parse.urlunsplit(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            path,
            urllib.parse.urlencode(filtered, doseq=True),
            "",
        )
    )


def parse_datetime(value: str | None) -> dt.datetime | None:
    value = clean_text(value)
    if not value:
        return None
    try:
        parsed = email.utils.parsedate_to_datetime(value)
    except (TypeError, ValueError):
        parsed = None
    if parsed is None:
        iso_value = value.replace("Z", "+00:00")
        try:
            parsed = dt.datetime.fromisoformat(iso_value)
        except ValueError:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def load_sources(path: Path) -> list[Source]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    sources = []
    seen_ids: set[str] = set()
    for row in raw:
        src = Source(
            id=row["id"],
            name=row["name"],
            url=row["url"],
            feed_url=row["feed_url"],
            type=row["type"],
            priority=row["priority"],
            cadence=row["cadence"],
            tags=tuple(row.get("tags", [])),
            include_in_digest=bool(row.get("include_in_digest", True)),
            notes=row.get("notes", ""),
        )
        if src.id in seen_ids:
            raise ValueError(f"duplicate source id: {src.id}")
        if src.priority not in PRIORITY_WEIGHT:
            raise ValueError(f"{src.id}: invalid priority {src.priority!r}")
        if src.type not in TYPE_WEIGHT:
            raise ValueError(f"{src.id}: invalid type {src.type!r}")
        seen_ids.add(src.id)
        sources.append(src)
    return sources


def fetch_url(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": BROWSER_UA,
            "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml",
        },
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS, context=SSL_CTX) as resp:
        return resp.read()


def find_link(entry: ET.Element, *, atom: bool, base_url: str) -> str:
    if atom:
        for link in entry.findall("atom:link", ATOM_NS) + entry.findall("link"):
            rel = link.get("rel")
            href = link.get("href")
            if href and rel in (None, "alternate"):
                return urllib.parse.urljoin(base_url, href)
        return ""
    return urllib.parse.urljoin(base_url, clean_text(entry.findtext("link")))


def parse_feed(source: Source, body: bytes) -> list[FeedItem]:
    root = ET.fromstring(body)
    atom = root.tag.endswith("feed")
    entries: Iterable[ET.Element]
    if atom:
        entries = root.findall("atom:entry", ATOM_NS) or root.findall("entry")
    else:
        channel = root.find("channel")
        entries = channel.findall("item") if channel is not None else root.findall(".//item")

    items: list[FeedItem] = []
    for entry in entries:
        if atom:
            title = clean_text(entry.findtext("atom:title", namespaces=ATOM_NS) or entry.findtext("title"))
            date_value = (
                entry.findtext("atom:published", namespaces=ATOM_NS)
                or entry.findtext("atom:updated", namespaces=ATOM_NS)
                or entry.findtext("published")
                or entry.findtext("updated")
            )
            summary = clean_text(
                entry.findtext("atom:summary", namespaces=ATOM_NS)
                or entry.findtext("atom:content", namespaces=ATOM_NS)
                or entry.findtext("summary")
                or entry.findtext("content")
            )
        else:
            title = clean_text(entry.findtext("title"))
            date_value = entry.findtext("pubDate") or entry.findtext("date")
            summary = clean_text(
                entry.findtext("description")
                or entry.findtext("content:encoded", namespaces=CONTENT_NS)
            )
        url = find_link(entry, atom=atom, base_url=source.feed_url)
        if not title or not url:
            continue
        url = canonical_url(url)
        published_at = parse_datetime(date_value)
        content_hash = hashlib.sha256(f"{source.id}\n{title}\n{url}".encode()).hexdigest()[:16]
        items.append(
            FeedItem(
                source=source,
                title=title,
                url=url,
                published_at=published_at,
                summary=summary[:320],
                score=score_item(source, title),
                content_hash=content_hash,
            )
        )
    return items


def score_item(source: Source, title: str) -> int:
    score = PRIORITY_WEIGHT[source.priority] + TYPE_WEIGHT[source.type]
    for tag in source.tags:
        score += TAG_WEIGHT.get(tag, 0)
    for pattern, weight in TITLE_BONUS_PATTERNS:
        if pattern.search(title):
            score += weight
    for pattern, weight in TITLE_PENALTY_PATTERNS:
        if pattern.search(title):
            score += weight
    if not source.include_in_digest:
        score -= 25
    return score


def in_target_window(item: FeedItem, target_date: dt.date, include_undated: bool) -> bool:
    if item.published_at is None:
        return include_undated
    return item.published_at.date() == target_date


def dedupe_items(items: Iterable[FeedItem]) -> list[FeedItem]:
    by_url: dict[str, FeedItem] = {}
    for item in items:
        prev = by_url.get(item.url)
        if prev is None or item.score > prev.score:
            by_url[item.url] = item

    def recency(item: FeedItem) -> float:
        if item.published_at is None:
            return 0.0
        return item.published_at.timestamp()

    return sorted(
        by_url.values(),
        key=lambda item: (
            -item.score,
            -recency(item),
            item.source.name,
            item.title,
        ),
    )


def signal_label(item: FeedItem) -> str:
    title_words = {w.lower() for w in re.findall(r"[A-Za-z]+", item.title)}
    if item.source.type == "vendor_blog":
        return "vendor/operator signal; require concrete release, benchmark, or implementation detail"
    if title_words & ROUNDUP_WORDS:
        return "roundup/discovery signal; dedupe before promoting to digest"
    if item.source.type == "research_lab":
        return "primary research context"
    if item.source.type in {"expert_blog", "kol_substack"}:
        return "expert analysis"
    return "watch item"


def group_items(items: list[FeedItem]) -> dict[str, list[FeedItem]]:
    grouped: dict[str, list[FeedItem]] = {}
    for item in items:
        grouped.setdefault(item.source.priority, []).append(item)
    return grouped


def render_markdown(
    *,
    target_date: dt.date,
    sources: list[Source],
    items: list[FeedItem],
    errors: list[tuple[Source, str]],
) -> str:
    grouped = group_items(items)
    active_sources = [s for s in sources if s.include_in_digest]
    lines = [
        f"# AI Expert Blog Watch - {target_date.isoformat()}",
        "",
        "## Summary",
        f"- Sources checked: {len(sources)} ({len(active_sources)} enabled for digest inclusion)",
        f"- Items published on {target_date.isoformat()}: {len(items)}",
        f"- Fetch errors: {len(errors)}",
        "",
    ]

    if not items:
        lines.extend([
            "_No new expert blog posts found for this date._",
            "",
        ])
    else:
        for priority in ("P0", "P1", "P2"):
            priority_items = grouped.get(priority, [])
            if not priority_items:
                continue
            lines.extend([f"## {priority} Watch Items", ""])
            for item in priority_items:
                tags = ", ".join(item.source.tags)
                digest_flag = "yes" if item.source.include_in_digest else "no"
                lines.extend(
                    [
                        f"### [{item.title}]({item.url})",
                        f"- Source: {item.source.name} ({item.source.type}, {item.source.priority})",
                        f"- Published: {item.published_label}",
                        f"- Score: {item.score}",
                        f"- Digest candidate: {digest_flag}",
                        f"- Tags: {tags}",
                        f"- Signal: {signal_label(item)}",
                    ]
                )
                if item.summary:
                    lines.append(f"- Summary: {item.summary}")
                lines.append("")

    lines.extend(["## Sources Checked", ""])
    for source in sources:
        digest_flag = "yes" if source.include_in_digest else "no"
        lines.append(
            f"- {source.priority} [{source.name}]({source.url}) — "
            f"{source.type}, digest={digest_flag}, feed: {source.feed_url}"
        )
    lines.append("")

    if errors:
        lines.extend(["## Fetch Errors", ""])
        for source, error in errors:
            lines.append(f"- {source.name}: {error}")
        lines.append("")

    generated_at = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines.extend(
        [
            "---",
            f"*Generated at {generated_at} by `scripts/fetch_ai_blogs.py`.*",
            "",
        ]
    )
    return "\n".join(lines)


def write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False, prefix=f".{path.name}.", suffix=".tmp"
    ) as tmp:
        tmp.write(text)
        tmp_path = Path(tmp.name)
    os.replace(tmp_path, path)


def collect_items(sources: list[Source], target_date: dt.date, include_undated: bool) -> tuple[list[FeedItem], list[tuple[Source, str]]]:
    all_items: list[FeedItem] = []
    errors: list[tuple[Source, str]] = []
    for source in sources:
        try:
            body = fetch_url(source.feed_url)
            parsed = parse_feed(source, body)
            all_items.extend(
                item for item in parsed if in_target_window(item, target_date, include_undated)
            )
        except (ET.ParseError, urllib.error.URLError, TimeoutError, OSError) as exc:
            errors.append((source, f"{type(exc).__name__}: {exc}"))
    return dedupe_items(all_items), errors


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--date", default=dt.datetime.now(dt.timezone.utc).date().isoformat())
    parser.add_argument("--include-undated", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        target_date = dt.date.fromisoformat(args.date)
    except ValueError:
        print(f"ERROR: invalid --date {args.date!r}; expected YYYY-MM-DD", file=sys.stderr)
        return 2

    sources = load_sources(args.registry)
    items, errors = collect_items(sources, target_date, args.include_undated)
    markdown = render_markdown(
        target_date=target_date,
        sources=sources,
        items=items,
        errors=errors,
    )
    out_path = args.out_dir / f"{target_date.isoformat()}.md"
    write_atomic(out_path, markdown)
    print(f"Wrote {out_path} with {len(items)} item(s), {len(errors)} fetch error(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
