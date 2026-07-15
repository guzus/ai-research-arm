#!/usr/bin/env python3
"""Poll configured RSS blog subscriptions and build Hooker notifications.

The command is deliberately two-phase:

* ``poll`` fetches feeds and writes pending notifications without marking them
  seen. A source absent from the state file is seeded with its current GUIDs
  and produces no notifications.
* ``ack`` records a pending GUID immediately after Hooker accepts that item.

Hooker receives a stable per-GUID idempotency key, so a delivery followed by a
failed state commit is safe to retry.
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
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Callable


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = REPO_ROOT / "data" / "sources" / "ai_blogs.json"
DEFAULT_STATE = REPO_ROOT / "research" / "summaries" / "blog-subscriptions.json"
DEFAULT_PENDING = REPO_ROOT / ".tmp" / "blog-subscriptions-pending.json"
USER_AGENT = "ai-research-arm/1.0 (https://github.com/guzus/ai-research-arm)"
TIMEOUT_SECONDS = 25
MAX_FEED_BYTES = 5_000_000
STATE_VERSION = 1
PENDING_VERSION = 1
# Keep this identical to Hooker's server-side topic contract.
TOPIC_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")


class SubscriptionError(ValueError):
    """Raised when configuration, feed, or persistent state is invalid."""


@dataclasses.dataclass(frozen=True)
class SubscriptionSource:
    id: str
    name: str
    url: str
    feed_url: str
    hooker_topic: str
    priority: int


@dataclasses.dataclass(frozen=True)
class FeedItem:
    guid: str
    title: str
    url: str
    published_at: dt.datetime | None


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def timestamp(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def clean_text(value: str | None) -> str:
    value = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def parse_datetime(value: str | None) -> dt.datetime | None:
    value = clean_text(value)
    if not value:
        return None
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


def canonical_url(value: str, *, base_url: str) -> str:
    absolute = urllib.parse.urljoin(base_url, clean_text(value))
    parsed = urllib.parse.urlsplit(absolute)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        raise SubscriptionError(f"invalid post URL: {absolute!r}")
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    filtered = [
        (key, val)
        for key, val in query
        if not key.lower().startswith("utm_")
        and key.lower() not in {"fbclid", "gclid", "fromrss", "trackingcode"}
    ]
    return urllib.parse.urlunsplit(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path,
            urllib.parse.urlencode(filtered, doseq=True),
            "",
        )
    )


def validate_post_url(source: SubscriptionSource, value: str) -> str:
    """Require a post link to remain under the configured blog URL."""
    url = canonical_url(value, base_url=source.feed_url)
    post = urllib.parse.urlsplit(url)
    blog = urllib.parse.urlsplit(canonical_url(source.url, base_url=source.url))
    blog_path = blog.path.rstrip("/")
    path_matches = not blog_path or blog_path == "/" or post.path == blog_path or post.path.startswith(
        f"{blog_path}/"
    )
    if post.netloc != blog.netloc or not path_matches:
        raise SubscriptionError(
            f"{source.id}: post URL escapes configured blog path {source.url!r}: {url!r}"
        )
    return url


def item_identity(source: SubscriptionSource, guid: str, link: str) -> str:
    """Return a stable item identity, preferring the feed GUID.

    URL-shaped GUIDs are canonicalized so Naver tracking-query variants do
    not replay. A missing GUID falls back to the already host/path-constrained
    canonical post link; channel metadata is never used as identity.
    """
    guid = clean_text(guid)
    if not guid:
        return validate_post_url(source, link)
    parsed = urllib.parse.urlsplit(guid)
    if parsed.scheme.lower() in {"http", "https"}:
        return validate_post_url(source, guid)
    return guid


def _ssl_context() -> ssl.SSLContext:
    cafile = os.environ.get("SSL_CERT_FILE")
    if cafile and os.path.isfile(cafile):
        return ssl.create_default_context(cafile=cafile)
    return ssl.create_default_context()


def fetch_url(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/rss+xml, application/xml, text/xml",
        },
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS, context=_ssl_context()) as response:
        body = response.read(MAX_FEED_BYTES + 1)
    if len(body) > MAX_FEED_BYTES:
        raise SubscriptionError(f"feed exceeds {MAX_FEED_BYTES} bytes: {url}")
    return body


def load_sources(path: Path) -> list[SubscriptionSource]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SubscriptionError(f"cannot read subscription registry {path}: {exc}") from exc
    if not isinstance(raw, list):
        raise SubscriptionError("blog registry must be a JSON array")

    sources: list[SubscriptionSource] = []
    seen_ids: set[str] = set()
    for row in raw:
        if not isinstance(row, dict):
            raise SubscriptionError("each blog registry entry must be an object")
        subscription = row.get("subscription")
        if subscription is None:
            continue
        if not isinstance(subscription, dict):
            raise SubscriptionError(f"{row.get('id', '<unknown>')}: subscription must be an object")
        source_id = row.get("id")
        if not isinstance(source_id, str) or not source_id:
            raise SubscriptionError("subscribed source has an invalid id")
        if source_id in seen_ids:
            raise SubscriptionError(f"duplicate subscribed source id: {source_id}")
        topic = subscription.get("hooker_topic")
        if not isinstance(topic, str) or not TOPIC_RE.fullmatch(topic):
            raise SubscriptionError(f"{source_id}: invalid Hooker topic {topic!r}")
        priority = subscription.get("priority", 3)
        if isinstance(priority, bool) or not isinstance(priority, int) or not 0 <= priority <= 5:
            raise SubscriptionError(f"{source_id}: priority must be an integer from 0 to 5")
        try:
            source = SubscriptionSource(
                id=source_id,
                name=str(row["name"]),
                url=str(row["url"]),
                feed_url=str(row["feed_url"]),
                hooker_topic=topic,
                priority=priority,
            )
        except KeyError as exc:
            raise SubscriptionError(f"{source_id}: missing registry field {exc.args[0]}") from exc
        canonical_url(source.url, base_url=source.url)
        canonical_url(source.feed_url, base_url=source.feed_url)
        seen_ids.add(source_id)
        sources.append(source)

    if not sources:
        raise SubscriptionError("blog registry has no configured subscriptions")
    return sorted(sources, key=lambda source: source.id)


def parse_rss(source: SubscriptionSource, body: bytes) -> list[FeedItem]:
    try:
        root = ET.fromstring(body)
    except ET.ParseError as exc:
        raise SubscriptionError(f"{source.id}: invalid RSS XML: {exc}") from exc
    channel = root.find("channel")
    if channel is None:
        raise SubscriptionError(f"{source.id}: RSS channel is missing")

    by_guid: dict[str, FeedItem] = {}
    for index, entry in enumerate(channel.findall("item"), start=1):
        raw_guid = clean_text(entry.findtext("guid"))
        title = clean_text(entry.findtext("title"))
        link = clean_text(entry.findtext("link"))
        if not title:
            raise SubscriptionError(f"{source.id}: item {index} has no title")
        if not link:
            raise SubscriptionError(f"{source.id}: item {index} has no link")
        url = validate_post_url(source, link)
        guid = item_identity(source, raw_guid, url)
        item = FeedItem(
            guid=guid,
            title=title,
            url=url,
            published_at=parse_datetime(entry.findtext("pubDate")),
        )
        previous = by_guid.get(guid)
        if previous is not None and previous != item:
            raise SubscriptionError(f"{source.id}: GUID {guid!r} identifies conflicting items")
        by_guid[guid] = item
    if not by_guid:
        raise SubscriptionError(f"{source.id}: RSS feed contains no items")
    return list(by_guid.values())


def empty_state() -> dict[str, Any]:
    return {"version": STATE_VERSION, "sources": {}}


def load_state(path: Path, *, allow_missing: bool = True) -> dict[str, Any]:
    if not path.exists():
        if allow_missing:
            return empty_state()
        raise SubscriptionError(f"subscription state does not exist: {path}")
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SubscriptionError(f"cannot read subscription state {path}: {exc}") from exc
    if not isinstance(state, dict) or state.get("version") != STATE_VERSION:
        raise SubscriptionError(f"unsupported or malformed subscription state: {path}")
    sources = state.get("sources")
    if not isinstance(sources, dict):
        raise SubscriptionError(f"subscription state sources must be an object: {path}")
    for source_id, source_state in sources.items():
        if not isinstance(source_id, str) or not isinstance(source_state, dict):
            raise SubscriptionError(f"malformed source record in subscription state: {source_id!r}")
        guids = source_state.get("seen_guids")
        if not isinstance(guids, list) or not all(isinstance(guid, str) and guid for guid in guids):
            raise SubscriptionError(f"{source_id}: seen_guids must be a list of non-empty strings")
        if len(set(guids)) != len(guids):
            raise SubscriptionError(f"{source_id}: seen_guids contains duplicates")
        updated_at = source_state.get("updated_at")
        if not isinstance(updated_at, str) or parse_datetime(updated_at) is None:
            raise SubscriptionError(f"{source_id}: updated_at must be a timestamp string")
    return state


def write_json_atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
        temp_path = Path(handle.name)
    os.replace(temp_path, path)


def notification_for(source: SubscriptionSource, item: FeedItem) -> dict[str, Any]:
    date_label = ""
    if item.published_at is not None:
        date_label = item.published_at.astimezone(dt.timezone(dt.timedelta(hours=9))).strftime(
            "%Y-%m-%d %H:%M KST"
        )
    text_parts = [item.title]
    if date_label:
        text_parts.extend(["", date_label])
    text_parts.extend(["", item.url])
    guid_hash = hashlib.sha256(item.guid.encode("utf-8")).hexdigest()[:32]
    return {
        "source_id": source.id,
        "guid": item.guid,
        "published_at": timestamp(item.published_at) if item.published_at else None,
        "topic": source.hooker_topic,
        "idempotency_key": f"blog-subscription-{source.id}-{guid_hash}",
        "payload": {
            "title": f"새 글 · {source.name}",
            "text": "\n".join(text_parts),
            "priority": source.priority,
            "tags": ["blog-subscription", source.id],
            "reply_markup": {
                "inline_keyboard": [[{"text": "블로그에서 읽기", "url": item.url}]]
            },
        },
    }


def poll_subscriptions(
    *,
    sources: list[SubscriptionSource],
    state_path: Path,
    pending_path: Path,
    fetcher: Callable[[str], bytes] = fetch_url,
    now: dt.datetime | None = None,
) -> dict[str, Any]:
    current_time = now or utc_now()
    state = load_state(state_path)
    fetched = {source.id: parse_rss(source, fetcher(source.feed_url)) for source in sources}

    seeded_sources: list[str] = []
    notifications: list[dict[str, Any]] = []
    for source in sources:
        items = fetched[source.id]
        source_state = state["sources"].get(source.id)
        if source_state is None:
            state["sources"][source.id] = {
                "seen_guids": sorted(item.guid for item in items),
                "updated_at": timestamp(current_time),
            }
            seeded_sources.append(source.id)
            continue
        seen = set(source_state["seen_guids"])
        unseen = [item for item in items if item.guid not in seen]
        unseen.sort(
            key=lambda item: (
                item.published_at or dt.datetime.min.replace(tzinfo=dt.timezone.utc),
                item.guid,
            )
        )
        notifications.extend(notification_for(source, item) for item in unseen)

    if seeded_sources:
        write_json_atomic(state_path, state)
    pending = {
        "version": PENDING_VERSION,
        "generated_at": timestamp(current_time),
        "seeded_sources": seeded_sources,
        "notifications": notifications,
    }
    write_json_atomic(pending_path, pending)
    return pending


def ack_pending(
    *,
    state_path: Path,
    pending_path: Path,
    source_id: str | None = None,
    guid: str | None = None,
    now: dt.datetime | None = None,
) -> int:
    if (source_id is None) != (guid is None):
        raise SubscriptionError("source_id and guid must be provided together")
    state = load_state(state_path, allow_missing=False)
    try:
        pending = json.loads(pending_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SubscriptionError(f"cannot read pending notifications {pending_path}: {exc}") from exc
    if not isinstance(pending, dict) or pending.get("version") != PENDING_VERSION:
        raise SubscriptionError(f"unsupported or malformed pending notifications: {pending_path}")
    notifications = pending.get("notifications")
    if not isinstance(notifications, list):
        raise SubscriptionError("pending notifications must be a list")

    selected = notifications
    if source_id is not None and guid is not None:
        selected = [
            notification
            for notification in notifications
            if isinstance(notification, dict)
            and notification.get("source_id") == source_id
            and notification.get("guid") == guid
        ]
        if len(selected) != 1:
            raise SubscriptionError(
                f"pending notifications contain {len(selected)} matches for {source_id!r} / {guid!r}"
            )

    current_time = now or utc_now()
    acknowledged = 0
    touched: set[str] = set()
    for notification in selected:
        if not isinstance(notification, dict):
            raise SubscriptionError("pending notification must be an object")
        source_id = notification.get("source_id")
        guid = notification.get("guid")
        if not isinstance(source_id, str) or not isinstance(guid, str) or not guid:
            raise SubscriptionError("pending notification has invalid source_id or guid")
        source_state = state["sources"].get(source_id)
        if not isinstance(source_state, dict):
            raise SubscriptionError(f"pending notification references unseeded source {source_id!r}")
        seen = set(source_state["seen_guids"])
        if guid not in seen:
            seen.add(guid)
            source_state["seen_guids"] = sorted(seen)
            acknowledged += 1
            touched.add(source_id)
    for source_id in touched:
        state["sources"][source_id]["updated_at"] = timestamp(current_time)
    if acknowledged:
        write_json_atomic(state_path, state)
    return acknowledged


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    poll = subparsers.add_parser("poll", help="Fetch feeds and write pending notifications")
    poll.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    poll.add_argument("--state", type=Path, default=DEFAULT_STATE)
    poll.add_argument("--pending", type=Path, default=DEFAULT_PENDING)
    ack = subparsers.add_parser("ack", help="Record successfully delivered pending GUIDs")
    ack.add_argument("--state", type=Path, default=DEFAULT_STATE)
    ack.add_argument("--pending", type=Path, default=DEFAULT_PENDING)
    ack.add_argument("--source-id", help="Acknowledge one pending item from this source")
    ack.add_argument("--guid", help="Acknowledge one pending item with this exact GUID")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv or sys.argv[1:])
    try:
        if args.command == "poll":
            sources = load_sources(args.registry)
            pending = poll_subscriptions(
                sources=sources,
                state_path=args.state,
                pending_path=args.pending,
            )
            print(
                f"Polled {len(sources)} subscription(s): "
                f"seeded={len(pending['seeded_sources'])}, new={len(pending['notifications'])}"
            )
        else:
            acknowledged = ack_pending(
                state_path=args.state,
                pending_path=args.pending,
                source_id=args.source_id,
                guid=args.guid,
            )
            print(f"Acknowledged {acknowledged} delivered blog post(s)")
    except (SubscriptionError, OSError, TimeoutError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
