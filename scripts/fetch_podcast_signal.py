#!/usr/bin/env python3
"""Fetch spoken-media AI signal (podcasts, lab videos, earnings calls) via tuber.

The Aradio source lane (docs/aradio.md, "Sources come through tuber"). Every
source in data/sources/podcasts.json is read through tuber-api and merged into
a rolling 30-day index, ``research/podcasts/index.json``, plus a human-readable
``research/podcasts/YYYY-MM-DD.md`` for the current UTC day.

Read-only by construction: every request goes through ``TuberClient.get``,
which refuses tuber's generation endpoints (``/summarize``, ``/acp/jobs``,
``POST /podcast/episode/summarize`` -- they spend model budget on tuber's
side) and anything outside an allowlist of read paths, BEFORE a request is
made. Only GET is ever sent.

Transcript text is never written to disk. An episode carries at most
``MAX_EXCERPTS`` excerpts of at most ``MAX_EXCERPT_WORDS`` words -- the earnings
lane's quote policy -- chosen by ``select_windows``, which the Aradio inbox
builder imports. Everything under research/ is public, so committing a
transcript would be republishing it.

Every published URL is either built from a validated id (YouTube watch and
deep links) or passes ``safe_url`` (RSS enclosures relayed by tuber, the
registry's feed URLs); an unsafe one is dropped, never repaired. Reloaded
records are re-sanitized, and the Markdown uses angle-bracket link
destinations with escaped, single-line text. ``safe_url`` is public: the
Aradio inbox builder applies the same check.

State rules (the contract in docs/aradio.md):
  - ``first_seen_at`` is set once and never changes; ``published_at`` is
    derived once at first sight (exact for RSS; for YouTube, approximate:
    the midpoint of the interval tuber's floored relative label denotes, so
    "15h ago" at first sight becomes 15.5 h before it).
  - an episode without a transcript is retried on later runs while it is
    < 3 days old; ``attempts`` counts tries.
  - ``updated_at`` changes only when the content changes, so a quiet run
    rewrites nothing and commits nothing. The first run of each UTC day does
    write that day's (possibly empty) Markdown file, which is what keeps the
    lane's freshness SLO meaningful on a day without new episodes.
  - a registry source with ``include_in_aradio: false`` is not fetched, and
    its episodes leave the index (the registry is the source of truth).
  - a video found by two sources (a lab's channel and its livestream search)
    becomes one episode, owned by the source listed first in the registry.

Exit codes:
  0  ok, including partial source failure (``degraded`` is true in the index
     when more than half of the sources failed)
  2  bad arguments, an invalid registry, or an unreadable existing index
  3  total fetch failure: every source failed; nothing is written, so the
     outage stays visible to the git-recency freshness watchdog
  4  publish-age format drift: not one tuber relative-age label parsed;
     nothing is written (fetch_youtube_signal.py's 2026-09-29 failure mode,
     which otherwise silently drops every video)
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import email.utils
import html
import http.client
import json
import os
import re
import sys
import tempfile
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable

import fetch_youtube_signal as youtube  # shared tuber client pieces + age parser

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = REPO_ROOT / "data" / "sources" / "podcasts.json"
DEFAULT_OUT_DIR = REPO_ROOT / "research" / "podcasts"
INDEX_NAME = "index.json"
LANE = "podcasts"
SCHEMA = 1

EXIT_BAD_INPUT = 2
EXIT_TOTAL_FETCH_FAILURE = 3
EXIT_PUBLISH_AGE_DRIFT = 4
# Below this many relative-age labels an all-unparsed batch is too small to
# call drift (same threshold as the YouTube lane).
PUBLISH_AGE_DRIFT_MIN_LABELS = youtube.PUBLISH_AGE_DRIFT_MIN_CANDIDATES

KINDS = ("channel", "search", "podcast")
PRIORITY_RANK = {"P0": 0, "P1": 1, "P2": 2}
DEFAULT_COUNT = {"channel": 15, "search": 20, "podcast": 15}
SHOW_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CHANNEL_ID_RE = re.compile(r"^UC[A-Za-z0-9_-]{22}$")
VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
POD_ID_RE = re.compile(r"^pod-[A-Za-z0-9_-]{1,80}$")
SHOW_KEYS = {
    "id", "name", "kind", "channel_id", "query", "rss", "priority", "tags",
    "ai_filter", "min_duration_s", "include_in_aradio", "count", "notes",
}
KIND_ONLY_KEYS = {"channel_id": {"channel", "search"}, "query": {"search"}, "rss": {"podcast"}}

# Earnings-lane quote policy: never more than this much verbatim speech.
MAX_EXCERPTS = 6
MAX_EXCERPT_WORDS = 60
MAX_DESCRIPTION_WORDS = 80

FIRST_SIGHT_MAX_AGE_DAYS = 14
RETENTION = dt.timedelta(days=30)
TRANSCRIPT_RETRY_WINDOW = dt.timedelta(days=3)
# Every run while the episode is fresh (the inbox builder airs an episode
# without a transcript once it is 6 h old), then every 6 h until 3 days.
TRANSCRIPT_FAST_ATTEMPTS = 4
TRANSCRIPT_FAST_INTERVAL = dt.timedelta(minutes=110)
TRANSCRIPT_SLOW_INTERVAL = dt.timedelta(hours=6)
# A caption track whose last segment starts before this share of the video's
# duration is a fragment (seen live: 161 words for a 63-minute episode).
MIN_TRANSCRIPT_COVERAGE = 0.5
COVERAGE_CHECK_MIN_DURATION_S = 300

# YouTube rate-limits tuber's transcript fetches in bursts (HTTP 500
# "temporarily rate-limited transcript access"), so the transcript phase is
# spaced, retried once, capped per run, time-boxed, and stops early after
# consecutive rate limits; whatever is left is retried on the next run.
DEFAULT_MAX_TRANSCRIPT_FETCHES = 12
TRANSCRIPT_SPACING_S = 2.5
TRANSCRIPT_RETRY_BACKOFF_S = 8.0
TRANSCRIPT_TIMEOUT_S = 45.0
TRANSCRIPT_PHASE_BUDGET_S = 480.0
RATE_LIMIT_BREAKER = 4
DEFAULT_MAX_DETAIL_FETCHES = 60
DETAIL_SPACING_S = 0.3
REQUEST_TIMEOUT_S = 25.0

FORBIDDEN_GENERATION_PATH_PARTS = (
    *youtube.FORBIDDEN_GENERATION_PATH_PARTS,  # "/summarize", "/acp/jobs"
    "/podcast/episode/summarize",
)
READ_ONLY_PATH_RE = re.compile(
    r"^/(?:channel/UC[A-Za-z0-9_-]{22}|search|podcast/episodes"
    r"|video/[A-Za-z0-9_-]{11}(?:/transcript)?)$"
)


class RegistryError(ValueError):
    """The registry is malformed; the run must not proceed (exit 2)."""


class IndexStateError(ValueError):
    """The existing index is unreadable; refusing to overwrite state (exit 2)."""


class TuberError(Exception):
    def __init__(self, message: str, *, status: int | None = None, rate_limited: bool = False):
        super().__init__(message)
        self.status = status
        self.rate_limited = rate_limited


# What one tuber request may raise. A truncated or malformed response
# (http.client.IncompleteRead, BadStatusLine, LineTooLong) is an
# http.client.HTTPException, which is NOT an OSError: unnamed, one cut-off
# response escapes every per-source boundary and kills the whole run instead
# of failing that one source. ValueError is the read-only guard's refusal.
FETCH_ERRORS = (TuberError, ValueError, http.client.HTTPException)


# ---------------------------------------------------------------------------
# Registry


@dataclasses.dataclass(frozen=True)
class Show:
    id: str
    name: str
    kind: str
    priority: str
    tags: tuple[str, ...]
    ai_filter: bool
    min_duration_s: int
    include_in_aradio: bool
    count: int
    channel_id: str = ""
    query: str = ""
    rss: str = ""

    @property
    def listener_kind(self) -> str:
        # earnings-call wins: those shows are ALSO tagged official, and the
        # gate treats earnings-call episodes as priority items.
        if "earnings-call" in self.tags:
            return "earnings-call"
        if "official" in self.tags:
            return "video"
        return "podcast"


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RegistryError(message)


def load_registry(path: Path) -> list[Show]:
    try:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RegistryError(f"{path}: cannot read registry: {exc}") from exc
    _require(isinstance(raw, dict), "registry must be a JSON object")
    _require(raw.get("schema") == 1, "registry schema must be 1")
    unknown_top = set(raw) - {"schema", "shows", "_comment"}
    _require(not unknown_top, f"unknown registry keys: {sorted(unknown_top)}")
    rows = raw.get("shows")
    _require(isinstance(rows, list) and rows, "registry needs a non-empty shows[]")
    shows: list[Show] = []
    seen: set[str] = set()
    for position, row in enumerate(rows):
        _require(isinstance(row, dict), f"shows[{position}] must be an object")
        sid = row.get("id")
        _require(isinstance(sid, str) and bool(SHOW_ID_RE.fullmatch(sid)),
                 f"shows[{position}]: id must be lowercase kebab-case, got {sid!r}")
        _require(sid not in seen, f"duplicate show id: {sid}")
        seen.add(sid)
        unknown = set(row) - SHOW_KEYS
        _require(not unknown, f"{sid}: unknown keys {sorted(unknown)}")
        kind = row.get("kind")
        _require(kind in KINDS, f"{sid}: kind must be one of {KINDS}, got {kind!r}")
        for key, kinds in KIND_ONLY_KEYS.items():
            _require(key not in row or kind in kinds, f"{sid}: {key!r} is not valid for kind {kind}")
        name = row.get("name")
        _require(isinstance(name, str) and bool(name.strip()), f"{sid}: name required")
        priority = row.get("priority")
        _require(priority in PRIORITY_RANK, f"{sid}: priority must be P0-P2, got {priority!r}")
        tags = row.get("tags", [])
        _require(isinstance(tags, list) and all(isinstance(t, str) and t for t in tags),
                 f"{sid}: tags must be a list of non-empty strings")
        for flag in ("ai_filter", "include_in_aradio"):
            _require(isinstance(row.get(flag), bool), f"{sid}: {flag} must be a boolean")
        min_duration = row.get("min_duration_s")
        _require(isinstance(min_duration, int) and not isinstance(min_duration, bool)
                 and min_duration >= 0, f"{sid}: min_duration_s must be a non-negative integer")
        count = row.get("count", DEFAULT_COUNT[kind])
        _require(isinstance(count, int) and not isinstance(count, bool) and 1 <= count <= 50,
                 f"{sid}: count must be an integer in 1..50")
        channel_id = row.get("channel_id", "")
        query = row.get("query", "")
        rss = row.get("rss", "")
        if kind in ("channel", "search"):
            _require(isinstance(channel_id, str) and bool(CHANNEL_ID_RE.fullmatch(channel_id)),
                     f"{sid}: {kind} source requires a UC… channel_id")
        if kind == "search":
            # The channel constraint is what keeps third-party re-streams out.
            _require(isinstance(query, str) and bool(query.strip()), f"{sid}: search source requires query")
        if kind == "podcast":
            # The feed URL is also the published fallback `url` of an episode
            # without a usable enclosure, so it must pass the same check.
            _require(isinstance(rss, str) and rss.startswith("https://") and safe_url(rss) == rss,
                     f"{sid}: podcast source requires a safe https rss URL")
        shows.append(Show(
            id=sid, name=name.strip(), kind=kind, priority=priority, tags=tuple(tags),
            ai_filter=row["ai_filter"], min_duration_s=min_duration,
            include_in_aradio=row["include_in_aradio"], count=count,
            channel_id=channel_id, query=query.strip(), rss=rss,
        ))
    return shows


# ---------------------------------------------------------------------------
# Published URLs

SAFE_URL_MAX_LENGTH = 2048
# Characters that can end or restructure a Markdown link or an HTML attribute.
_URL_FORBIDDEN_CHARS = frozenset("<>\"'()[]{}|\\^`")


def safe_url(url: str) -> str | None:
    """Return ``url`` unchanged when it is safe to publish, else None.

    Every URL that reaches research/ (the index, the daily Markdown, and from
    there the Aradio inbox and board) passes through here or is built from a
    validated id. Third-party URLs -- RSS enclosures relayed by tuber -- are
    attacker-controllable, and one carrying ``)``, ``]``, ``<``, quotes,
    whitespace or control characters could break out of a Markdown link.
    Safe means: http(s) scheme, a host, no userinfo, at most 2048 characters,
    and none of ``<>"'()[]{}|\\^``, backtick, whitespace, or control/format
    characters (which also covers bidi overrides). Nothing is repaired or
    re-encoded: a URL is either published byte-for-byte or dropped.
    """
    if not isinstance(url, str) or not url or len(url) > SAFE_URL_MAX_LENGTH:
        return None
    for char in url:
        if char in _URL_FORBIDDEN_CHARS or char.isspace() or unicodedata.category(char)[0] == "C":
            return None
    try:
        parts = urllib.parse.urlsplit(url)
        parts.port  # raises ValueError on a malformed port
    except ValueError:
        return None
    if parts.scheme not in ("https", "http") or not parts.netloc or not parts.hostname:
        return None
    if "@" in parts.netloc:  # credentials in a URL are never published
        return None
    return url


def youtube_watch_url(video_id: str, at_s: int | None = None) -> str:
    """Canonical YouTube URL, built only from a validated 11-character id."""
    if not isinstance(video_id, str) or not VIDEO_ID_RE.fullmatch(video_id):
        raise ValueError(f"not a YouTube video id: {video_id!r}")
    url = f"https://www.youtube.com/watch?v={video_id}"
    if at_s is not None:
        if isinstance(at_s, bool) or not isinstance(at_s, int) or at_s < 0:
            raise ValueError(f"not a timestamp: {at_s!r}")
        url += f"&t={at_s}s"
    return url


# ---------------------------------------------------------------------------
# tuber client (read-only)


def check_read_only_path(path: str) -> None:
    lowered = path.lower()
    if any(part in lowered for part in FORBIDDEN_GENERATION_PATH_PARTS):
        raise ValueError(f"refusing tuber generation endpoint: {path}")
    if not READ_ONLY_PATH_RE.fullmatch(path):
        raise ValueError(f"refusing non-allowlisted tuber path: {path}")


# YouTube throttling as relayed by tuber (HTTP 500), both seen live on
# 2026-10-30: "YouTube temporarily rate-limited transcript access" and
# "YouTube temporarily blocked transcript access".
_THROTTLED_RE = re.compile(r"rate.?limit|temporarily blocked|too many requests|throttl", re.I)


def _error_message(body: bytes) -> str:
    text = body[:2048].decode("utf-8", "replace")
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return youtube.clean_text(text)[:200]
    if isinstance(payload, dict) and isinstance(payload.get("error"), str):
        return youtube.clean_text(payload["error"])[:200]
    return youtube.clean_text(text)[:200]


def http_get_json(base_url: str, path: str, params: dict[str, Any] | None, timeout: float) -> Any:
    check_read_only_path(path)
    url = youtube.build_api_url(base_url, path, params)
    request = urllib.request.Request(
        url, headers={"Accept": "application/json", "User-Agent": youtube.USER_AGENT}, method="GET"
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=youtube.SSL_CTX) as response:
            body = response.read()
    except urllib.error.HTTPError as exc:
        try:
            message = _error_message(exc.read())
        except (OSError, http.client.HTTPException):
            message = ""
        rate_limited = exc.code == 429 or (exc.code >= 500 and bool(_THROTTLED_RE.search(message)))
        raise TuberError(f"HTTP {exc.code}: {message or exc.reason}", status=exc.code,
                         rate_limited=rate_limited) from exc
    except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException) as exc:
        raise TuberError(f"{type(exc).__name__}: {exc}") from exc
    try:
        return json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TuberError(f"invalid JSON from {path}: {exc}") from exc


Transport = Callable[[str, str, "dict[str, Any] | None", float], Any]


class TuberClient:
    """Every tuber request passes through ``get``, which enforces the guard."""

    def __init__(self, base_url: str, *, transport: Transport | None = None,
                 sleep: Callable[[float], None] | None = None,
                 monotonic: Callable[[], float] | None = None):
        self.base_url = base_url
        self.transport = transport or http_get_json
        self.sleep = sleep or time.sleep
        self.monotonic = monotonic or time.monotonic
        self.requests = 0

    def get(self, path: str, params: dict[str, Any] | None = None, *,
            timeout: float = REQUEST_TIMEOUT_S) -> Any:
        check_read_only_path(path)
        self.requests += 1
        return self.transport(self.base_url, path, params, timeout)


# ---------------------------------------------------------------------------
# Time helpers

AGE_UNIT_SECONDS = {
    "s": 1, "sec": 1, "second": 1,
    "m": 60, "min": 60, "minute": 60,
    "h": 3600, "hr": 3600, "hour": 3600,
    "d": 86400, "day": 86400,
    "w": 7 * 86400, "wk": 7 * 86400, "week": 7 * 86400,
    "mo": 30 * 86400, "month": 30 * 86400,
    "y": 365 * 86400, "yr": 365 * 86400, "year": 365 * 86400,
}


def _parse_age_label(label: str) -> tuple[int, int] | None:
    """(count, unit seconds) of a tuber relative label, or None."""
    text = youtube.clean_text(label).lower()
    if not text:
        return None
    if "today" in text or "just now" in text:
        return 0, 0
    if "yesterday" in text:
        return 1, 86400
    match = youtube.AGE_PATTERN.search(text)
    if not match:
        return None
    unit = match.group(2)
    if unit not in AGE_UNIT_SECONDS:
        unit = unit[:-1]
    return int(match.group(1)), AGE_UNIT_SECONDS[unit]


def label_age_seconds(label: str) -> int | None:
    """Seconds stated by a tuber relative label ("15h ago", "Streamed 1d ago").

    Same grammar as ``fetch_youtube_signal.approximate_age_days`` (shared
    pattern and unit table), at second resolution.
    """
    parsed = _parse_age_label(label)
    return None if parsed is None else parsed[0] * parsed[1]


def estimated_age_seconds(label: str) -> int | None:
    """Best estimate of a video's age from its relative label.

    YouTube floors these labels (live: a call streamed ~36.7 h earlier read
    "Streamed 1d ago"), so "15h ago" means 15-16 h and the midpoint is the
    unbiased estimate: at most half a unit off, instead of up to a whole unit
    with a systematic lean toward "too recent". In steady state an upload is
    first seen within ~2 h, under an hour-or-finer label, so the error is
    <= 30 min; day/week labels appear only while catching up a backlog.
    """
    parsed = _parse_age_label(label)
    if parsed is None:
        return None
    count, unit = parsed
    return count * unit + unit // 2


def utc_minute(value: dt.datetime) -> dt.datetime:
    return value.astimezone(dt.timezone.utc).replace(second=0, microsecond=0)


def iso(value: dt.datetime | None) -> str | None:
    if value is None:
        return None
    return value.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(value: Any) -> dt.datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def _timestamp(value: Any) -> float:
    parsed = parse_iso(value)
    return parsed.timestamp() if parsed else 0.0


def parse_rss_date(value: Any) -> dt.datetime | None:
    text = youtube.clean_text(value)
    if not text:
        return None
    try:
        parsed = email.utils.parsedate_to_datetime(text)
    except (TypeError, ValueError):
        parsed = parse_iso(text)
    if parsed is None:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def parse_duration(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value if value >= 0 else None
    if isinstance(value, float):
        return int(value) if value >= 0 and value == value else None
    text = youtube.clean_text(value)
    if re.fullmatch(r"\d+", text):
        return int(text)
    match = re.fullmatch(r"(?:(\d+):)?(\d{1,2}):(\d{2})", text)
    if match:
        hours, minutes, seconds = (int(part or 0) for part in match.groups())
        return hours * 3600 + minutes * 60 + seconds
    return None


# ---------------------------------------------------------------------------
# AI topicality (registry ai_filter) and show-note cleaning

# Case-sensitive: acronyms and proper names, so "ai" inside words and
# lowercase homographs never match.
_AI_CASED = re.compile(
    r"\b(?:A\.I\.|AI|AGI|ASI|LLMs?|GPUs?|TPUs?|HBM|GenAI|RLHF"
    r"|OpenAI|ChatGPT|GPT-?\d[\w.]*|Codex|Anthropic|Claude|DeepMind|Gemini|Llama|Grok|xAI"
    r"|Mistral|Hugging ?Face|Nvidia|NVIDIA|TSMC|ASML|CoreWeave|Cerebras|Copilot|Midjourney"
    r"|Stargate|Blackwell|Waymo|SemiAnalysis"
    r"|Sam Altman|Dario Amodei|Demis Hassabis|Jensen Huang|Ilya Sutskever|Andrej Karpathy"
    r"|Yann LeCun|Geoffrey Hinton|Mustafa Suleyman|Satya Nadella|Sundar Pichai)(?!\w)"
)
_AI_PHRASES = re.compile(
    r"\b(?:artificial intelligence|machine learning|deep learning|neural net(?:work)?s?"
    r"|(?:large )?language models?|foundation models?|frontier (?:ai|labs?|models?)"
    r"|reasoning models?|world models?|diffusion models?|open[- ]weights?"
    r"|open[- ]source (?:ai|models?)|superintelligen\w*|chatbots?|agentic|ai agents?"
    r"|coding agents?|computer use|inference|pre-?training|post-?training|fine-?tun(?:e|ed|ing)"
    r"|reinforcement learning|interpretability|data ?cent(?:er|re)s?|hyperscalers?"
    r"|semiconductors?|chipmakers?|chips?|robot(?:s|ic|ics)?|humanoids?|self-driving"
    r"|autonomous (?:vehicles?|driving|agents?)|compute|capex)\b",
    re.I,
)


def ai_hits(text: str) -> int:
    """Number of AI-topicality matches (acronyms/names cased, phrases not)."""
    return len(_AI_CASED.findall(text)) + len(_AI_PHRASES.findall(text))


def is_ai_topical(title: str, description: str) -> bool | None:
    """True/False for an ``ai_filter`` show, or None when undecidable.

    One hit in the title suffices. Show notes need two hits AFTER boilerplate
    removal: one stray "AI" in a guest bio is weak evidence. With no title hit
    and no notes the answer is unknown (the caller retries on a later run).
    """
    if ai_hits(title) >= 1:
        return True
    if not description:
        return None
    return ai_hits(description) >= 2


_URL_RE = re.compile(r"https?://\S+|www\.\S+|\b[\w-]+\.(?:com|ai|io|co|org|net|fm|ly|me|gg)/\S*", re.I)
_TIMESTAMP_RE = re.compile(r"\(?\b\d{1,2}:\d{2}(?::\d{2})?\b\)?\s*[-–—:]?\s*")
_NOTES_STOP_RE = re.compile(
    r"^(?:additional reading|resources|links?|sponsors?|sponsored by|stay updated|legal disclaimer"
    r"|disclaimer|credits|related(?: episodes)?|references|mentioned in (?:this|the) episode"
    r"|follow (?:us|the show)|subscribe|connect with us|where to find us|find us"
    r"|thanks to (?:our|today'?s) (?:partners|sponsors)|(?:our|today'?s) sponsors?"
    r"|this episode is (?:sponsored|brought to you))\b[^\n]{0,40}$",
    re.I,
)
_NOTES_BOILERPLATE_RE = re.compile(
    r"^(?:follow|subscribe)\b|\b(?:listen|watch) on\b|\bconnect with\b|\bcredits?:"
    r"|thanks to our (?:partners|sponsors)"
    r"|\b(?:subscribe|follow (?:us|me|him|her|them|our)|sponsor\w*|brought to you by|promo|"
    r"discount code|use code|patreon|newsletter|merch|affiliate|commission|"
    r"informational purposes|not (?:financial|investment|legal) advice|all rights reserved|"
    r"ethics policy|join the discussion|leave (?:us )?a review|rate (?:us|the show))\b",
    re.I,
)
_NOTES_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=\S)")


def clean_show_notes(text: Any) -> str:
    """Show notes without links, hashtags, sponsor or follow/subscribe text.

    Multi-line notes (YouTube descriptions) are filtered per line: a line
    carrying a link is a sponsor blurb, a follow/subscribe line, or a
    reading-list entry, and sponsor blurbs are dense in exactly the AI words
    the topicality check counts (live: an All-In episode about Theranos read
    as AI through "IREN is a vertically integrated AI Cloud…"). Single-line
    notes (tuber flattens RSS show notes) are filtered per sentence instead,
    so one link does not take the summary with it. A section header
    ("Additional Reading:", "Thanks to our partners") ends the notes.
    """
    raw = html.unescape(str(text or "")).replace("\r", "\n")
    raw = re.sub(r"<[^>]+>", " ", raw)
    lines = [line.strip() for line in raw.split("\n") if line.strip()]
    pieces_per_line = (
        [_NOTES_SENTENCE_SPLIT_RE.split(lines[0])] if len(lines) == 1 else [[line] for line in lines]
    )
    kept: list[str] = []
    for pieces in pieces_per_line:
        for piece in pieces:
            piece = piece.strip()
            if _NOTES_STOP_RE.match(piece):
                return re.sub(r"\s+", " ", " ".join(kept)).strip()
            if not piece or _URL_RE.search(piece) or _NOTES_BOILERPLATE_RE.search(piece):
                continue
            if all(token.startswith("#") for token in piece.split()):
                continue
            if set(piece) <= set("-–—=_*~|• "):
                continue
            kept.append(_TIMESTAMP_RE.sub(" ", piece))
    return re.sub(r"\s+", " ", " ".join(kept)).strip()


def first_words(text: str, limit: int) -> str:
    return " ".join(text.split()[:limit])


# ---------------------------------------------------------------------------
# Transcript windows (shared with the Aradio inbox builder)

_ANNOTATION_RE = re.compile(
    r"\[[^\]]{0,40}\]|\(\s*(?:music|applause|laughter|laughs|inaudible|crosstalk)\s*\)|>>+|♪+", re.I
)
_SENTENCE_END_STRIP = "\"'”’)]"
_ABBREVIATIONS = {"mr.", "mrs.", "ms.", "dr.", "st.", "vs.", "e.g.", "i.e.", "u.s.", "inc.", "jr.", "sr.", "no."}
_DIGIT_RE = re.compile(r"\d")
_MONEY_RE = re.compile(
    r"[$€£¥]\s?\d|\b\d+(?:\.\d+)?\s?(?:bn|tn|trn)\b|\b(?:billion|million|trillion|dollars?|revenue)\b", re.I
)
_PERCENT_RE = re.compile(r"\d\s?%|\bpercent(?:age)?\b|\bbasis points?\b", re.I)
_DOMAIN_RE = re.compile(
    r"\b(?:ai|agi|models?|llms?|gpus?|tpus?|compute|inference|training|pre-?training|post-?training"
    r"|fine-?tun\w*|reinforcement|reasoning|agents?|agentic|tokens?|benchmarks?|evals?|parameters?"
    r"|data ?cent(?:er|re)s?|chips?|semiconductor\w*|hbm|memory|gigawatts?|megawatts?|energy|power"
    r"|capex|margins?|profit\w*|growth|customers?|enterprise|pricing|prices?|costs?|valuation|ipo"
    r"|funding|quarter|demand|supply|capacity|cloud|api|open[- ]source|open[- ]weights?|safety"
    r"|regulation|export controls?|china|robot\w*|startups?|market share|users)\b"
)
_FORWARD_RE = re.compile(
    r"\b(?:will|won't|going to|gonna|expect(?:s|ed|ing)?|plan(?:s|ned|ning)? to"
    r"|next (?:year|quarter|month|generation|decade)|by (?:the end of )?20\d\d|forecast\w*|outlook"
    r"|guidance|roadmap|launch\w*|shipping|predict\w*)\b"
)
_FILLER_RE = re.compile(r"\b(?:um+|uh+|you know|i mean|sort of|kind of)\b")
_INTRO_OUTRO_RE = re.compile(
    r"\b(?:welcome (?:back )?to|my guests? (?:today|this week)|today'?s guests?"
    r"|thanks? (?:you )?(?:so much )?for (?:having me|joining|coming on|listening|watching|tuning in)"
    r"|see you (?:next time|next week)|leave (?:us )?a review|rate (?:the show|us)|hit the bell"
    r"|like and subscribe|subscribe to)\b"
)
_CALL_BOILERPLATE_RE = re.compile(
    r"\b(?:forward-looking statements?|safe harbor|risks and uncertainties|listen-only mode"
    r"|question-and-answer session|press star|star (?:one|1) on|next question (?:comes )?from"
    r"|your line is (?:now )?open|please go ahead|that concludes|reconciliation"
    r"|non-gaap (?:financial )?measures)\b"
)
_SPONSOR_RE = re.compile(
    r"\b(?:sponsored by|brought to you by|(?:our|today'?s|this (?:episode|week)'?s?) sponsors?"
    r"|word from (?:our|the|ours) sponsors?|support for (?:this|the) (?:show|podcast|episode)"
    r"|(?:promo|discount|coupon) code|use (?:the )?code|free trial"
    r"|(?:go|head|visit|check out)(?: over)?(?: to)? [a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:com|ai|io|co|org|net|dev|app|fm)"
    r"|(?:go|head)(?: over)? to [a-z0-9-]+ dot com"
    r"|\b[a-z0-9-]+\.(?:com|ai|io|co|org|net|dev|app|fm)/[a-z0-9-]+)",
    re.I,
)
SPONSOR_ZONE_MS = 60_000
_CAPS_STOPWORDS = {
    "i", "i'm", "i've", "i'll", "i'd", "ok", "okay", "so", "and", "but", "yeah", "yes", "no", "well",
    "now", "right", "oh", "um", "uh", "the", "a", "an", "it", "it's", "that", "this", "we", "you",
    "he", "she", "they", "like", "because", "if", "when", "what", "why", "how", "or", "mm", "hmm",
    "speaker", "operator",
}
# Integer weights (quarter points) keep scoring exactly reproducible.
_W_DIGIT, _W_MONEY, _W_PERCENT, _W_DOMAIN, _W_ENTITY, _W_FORWARD = 8, 12, 12, 6, 4, 6
_W_FILLER, _W_INTRO, _W_BOILERPLATE, _W_SHORT, _W_EDGE, _W_SPONSOR = -3, -24, -32, -16, -40, -240
# A window that opens with small talk before its substance loses to the one
# that opens on the substance (otherwise equal windows tie toward the earlier).
_W_WEAK_LEAD = -8
_EDGE_FRACTION = 0.04


def _ends_sentence(word: str) -> bool:
    core = word.rstrip(_SENTENCE_END_STRIP)
    if not core or core[-1] not in ".?!…":
        return False
    if core.lower() in _ABBREVIATIONS:
        return False
    # Initials and dotted acronyms ("J.", "U.S.", "A.I.") rarely end a
    # sentence; merging one into the next sentence is harmless.
    return not re.fullmatch(r"(?:[A-Za-z]\.)+", core)


def _segment_tokens(text: str) -> list[str | None]:
    """One caption segment's words, with None where a ">>" speaker change
    stood. Words are exactly ``_ANNOTATION_RE.sub(" ", text).split()``."""
    tokens: list[str | None] = []
    last = 0
    for match in _ANNOTATION_RE.finditer(text):
        tokens.extend(text[last:match.start()].split())
        if match.group(0).startswith(">"):
            tokens.append(None)
        last = match.end()
    tokens.extend(text[last:].split())
    return tokens


def _word_stream_turns(segments: Any) -> tuple[list[str], list[int], set[int]]:
    """(words, start ms of each word's segment, indexes of words that open a
    new speaker turn, i.e. follow a ">>" marker)."""
    rows: list[tuple[int, int, list[str | None]]] = []
    if not isinstance(segments, list):
        return [], [], set()
    for position, segment in enumerate(segments):
        if not isinstance(segment, dict):
            continue
        start = segment.get("startMs")
        if isinstance(start, bool) or not isinstance(start, (int, float)) or start != start or start < 0:
            continue
        text = segment.get("text")
        if not isinstance(text, str):
            continue
        tokens = _segment_tokens(html.unescape(text))
        if tokens:
            rows.append((int(start), position, tokens))
    rows.sort(key=lambda row: (row[0], row[1]))
    words_out: list[str] = []
    starts: list[int] = []
    turns: set[int] = set()
    pending = False
    for start, _, tokens in rows:
        for token in tokens:
            if token is None:
                pending = True
                continue
            if pending:
                turns.add(len(words_out))
                pending = False
            words_out.append(token)
            starts.append(start)
    return words_out, starts, turns


def _word_stream(segments: Any) -> tuple[list[str], list[int]]:
    words, starts, _ = _word_stream_turns(segments)
    return words, starts


def transcript_word_count(segments: Any) -> int:
    return len(_word_stream(segments)[0])


def _candidate_spans(words: list[str], max_words: int) -> tuple[list[tuple[int, int]], list[tuple[int, int]], bool]:
    """Return (candidate windows, scan units, sentence_mode).

    Scan units are sentences when the captions are punctuated (at least one
    terminator per 40 words; live captions run 1 per 11-33) and short fixed
    chunks otherwise; sponsor markers are located per unit.
    """
    total = len(words)
    terminators = sum(1 for word in words if _ends_sentence(word))
    if terminators * 40 >= total:
        sentences: list[tuple[int, int]] = []
        begin = 0
        for position, word in enumerate(words):
            if _ends_sentence(word):
                sentences.append((begin, position + 1))
                begin = position + 1
        if begin < total:
            sentences.append((begin, total))
        spans = []
        for first, (begin, end) in enumerate(sentences):
            if end - begin > max_words:
                spans.append((begin, begin + max_words))
                continue
            last = end
            for later in range(first + 1, len(sentences)):
                if sentences[later][1] - begin > max_words:
                    break
                last = sentences[later][1]
            spans.append((begin, last))
        return spans, sentences, True
    # Captions without punctuation: fixed-size word windows, half overlapping
    # so the selector can still align a window with dense content.
    stride = max(1, max_words // 2)
    spans = [(begin, min(begin + max_words, total)) for begin in range(0, total, stride)]
    units = [(begin, min(begin + 20, total)) for begin in range(0, total, 10)]
    return spans, units, False


def _entities(chunk: list[str], sentence_mode: bool) -> set[str]:
    """Capitalized tokens that are not sentence-initial or common words."""
    found = set()
    for offset, word in enumerate(chunk):
        token = word.strip(".,;:!?\"'()[]“”‘’…-—")
        if not token or not token[0].isupper() or token.lower() in _CAPS_STOPWORDS:
            continue
        if offset == 0 or (sentence_mode and _ends_sentence(chunk[offset - 1])):
            continue
        found.add(token.lower())
    return found


def _has_signal(chunk: list[str], sentence_mode: bool) -> bool:
    text = " ".join(chunk)
    return bool(_DIGIT_RE.search(text) or _MONEY_RE.search(text) or _PERCENT_RE.search(text)
                or _DOMAIN_RE.search(text.lower()) or _entities(chunk, sentence_mode))


def _score_span(words: list[str], begin: int, end: int, *, sentence_mode: bool, max_words: int,
                edge: bool, sponsor: bool) -> int:
    chunk = words[begin:end]
    text = " ".join(chunk)
    lower = text.lower()
    score = _W_DIGIT * min(sum(1 for word in chunk if _DIGIT_RE.search(word)), 6)
    score += _W_MONEY * min(len(_MONEY_RE.findall(text)), 3)
    score += _W_PERCENT * min(len(_PERCENT_RE.findall(text)), 3)
    score += _W_DOMAIN * min(len(_DOMAIN_RE.findall(lower)), 8)
    score += _W_ENTITY * min(len(_entities(chunk, sentence_mode)), 6)
    if sentence_mode:
        lead_end = next((i + 1 for i, word in enumerate(chunk) if _ends_sentence(word)), len(chunk))
        if lead_end < len(chunk) and not _has_signal(chunk[:lead_end], sentence_mode):
            score += _W_WEAK_LEAD
    score += _W_FORWARD * min(len(_FORWARD_RE.findall(lower)), 3)
    score += _W_FILLER * min(len(_FILLER_RE.findall(lower)), 8)
    score += _W_INTRO * len(_INTRO_OUTRO_RE.findall(lower))
    score += _W_BOILERPLATE * len(_CALL_BOILERPLATE_RE.findall(lower))
    if len(chunk) < max(8, (max_words * 2) // 5):
        score += _W_SHORT
    if edge:
        score += _W_EDGE
    if sponsor:
        score += _W_SPONSOR
    return score


def select_windows(segments: list[dict], *, max_windows: int, max_words: int,
                   min_gap_s: int = 120,
                   sentence_end: Callable[[str, str | None], bool] | None = None) -> list[dict]:
    """segments = tuber transcript segments [{"startMs": int, "text": str}].
    Returns ≤ max_windows non-overlapping windows [{"text": str, "at_s": int}]
    of ≤ max_words words each, highest-information first by score, then
    re-sorted by at_s. Deterministic; sponsor reads and intros/outros score low.

    ``sentence_end`` (the Aradio inbox passes check_aradio.sentence_end)
    only changes how the chosen windows are written, never which are chosen:
    the text keeps each caption ">>" speaker change as a " >> " token, and
    gets "…" glued to its first/last word where the window starts/ends inside
    a sentence (judged by ``sentence_end(word, next_word)``; a speaker change
    or the transcript's own start/end is never a cut). Aradio quotes only
    whole sentences, so it must see both. Without it (this lane's committed
    excerpts) the text is the plain words, as before.

    Windows follow sentence boundaries when the captions are punctuated and
    fall back to fixed-size word windows when they are not. Words are verbatim
    (caption annotations such as "[Music]" and ">>" are not speech and are
    dropped); ``at_s`` is the start of the caption segment holding the
    window's first word, so a deep link lands at or just before it. Scoring
    rewards numbers, money, percentages, AI/compute/business terms, named
    entities and forward-looking language; it penalizes filler, intro/outro
    and earnings-call boilerplate, the first/last 4% of the episode, and any
    window within 60 s of a sponsor-read marker ("sponsored by", "use code",
    "go to example.com/show"), because ad reads are dense in exactly the
    numbers and business terms the rest of the score rewards.
    """
    if isinstance(max_windows, bool) or isinstance(max_words, bool):
        return []
    if not isinstance(max_windows, int) or not isinstance(max_words, int):
        return []
    if max_windows < 1 or max_words < 1:
        return []
    min_gap_s = max(0, int(min_gap_s))
    words, starts, turns = _word_stream_turns(segments)
    if not words:
        return []
    spans, units, sentence_mode = _candidate_spans(words, max_words)
    first_ms, last_ms = starts[0], starts[-1]
    extent = max(1, last_ms - first_ms)
    sponsor_marks = [
        (starts[begin], starts[end - 1])
        for begin, end in units
        if _SPONSOR_RE.search(" ".join(words[begin:end]))
    ]
    scored = []
    for begin, end in spans:
        span_start, span_end = starts[begin], starts[end - 1]
        fraction = (span_start - first_ms) / extent
        edge = fraction < _EDGE_FRACTION or fraction > 1 - _EDGE_FRACTION
        sponsor = any(
            span_start <= mark_end + SPONSOR_ZONE_MS and span_end >= mark_start - SPONSOR_ZONE_MS
            for mark_start, mark_end in sponsor_marks
        )
        score = _score_span(words, begin, end, sentence_mode=sentence_mode, max_words=max_words,
                            edge=edge, sponsor=sponsor)
        scored.append((score, begin, end))
    scored.sort(key=lambda row: (-row[0], row[1], row[2]))
    chosen: list[tuple[int, int, int]] = []
    for _, begin, end in scored:
        if len(chosen) >= max_windows:
            break
        at_s = starts[begin] // 1000
        if any(begin < other_end and end > other_begin for other_begin, other_end, _ in chosen):
            continue
        if any(abs(at_s - other_at) < min_gap_s for _, _, other_at in chosen):
            continue
        chosen.append((begin, end, at_s))
    chosen.sort(key=lambda row: (row[2], row[0]))
    if sentence_end is None:
        return [{"text": " ".join(words[begin:end]), "at_s": at_s} for begin, end, at_s in chosen]
    return [{"text": _marked_text(words, turns, begin, end, sentence_end), "at_s": at_s}
            for begin, end, at_s in chosen]


def _marked_text(words: list[str], turns: set[int], begin: int, end: int,
                 sentence_end: Callable[[str, str | None], bool]) -> str:
    """words[begin:end] with " >> " speaker changes and "…" at cut edges."""
    out: list[str] = []
    for index in range(begin, end):
        if index in turns:
            out.append(">>")
        out.append(words[index])
    if begin > 0 and begin not in turns and not sentence_end(words[begin - 1], words[begin]):
        out[0] = "…" + out[0]  # words[begin]: no ">>" precedes a non-turn word
    if end < len(words) and end not in turns and not sentence_end(words[end - 1], words[end]):
        out[-1] = out[-1] + "…"
    return " ".join(out)


# ---------------------------------------------------------------------------
# Discovery


@dataclasses.dataclass
class Candidate:
    show: Show
    native_id: str
    title: str
    url: str
    video_id: str | None
    audio_url: str | None
    duration_s: int | None
    label: str
    published_at: dt.datetime | None
    precision: str
    description: str = ""
    is_live: bool = False
    channel_id: str = ""
    order: int = 0

    @property
    def episode_id(self) -> str:
        return f"{self.show.id}:{self.native_id}"


def _rows(payload: Any, key: str) -> list[dict]:
    if not isinstance(payload, dict) or not isinstance(payload.get(key), list):
        raise TuberError(f"unexpected payload shape (no {key}[])")
    return [row for row in payload[key] if isinstance(row, dict)]


def normalize_video(show: Show, row: dict, now: dt.datetime) -> Candidate | None:
    video_id = youtube.clean_text(row.get("id"))
    title = youtube.clean_text(row.get("title"))
    if not VIDEO_ID_RE.fullmatch(video_id) or not title:
        return None
    label = youtube.clean_text(row.get("publishedAt"))
    age = estimated_age_seconds(label)
    published = None if age is None else min(now, utc_minute(now - dt.timedelta(seconds=age)))
    return Candidate(
        show=show, native_id=video_id, title=title,
        url=youtube_watch_url(video_id), video_id=video_id, audio_url=None,
        duration_s=parse_duration(row.get("duration")), label=label, published_at=published,
        precision="approximate", is_live=row.get("isLive") is True,
        channel_id=youtube.clean_text(row.get("channelId")),
    )


def normalize_podcast(show: Show, row: dict) -> Candidate | None:
    pod_id = youtube.clean_text(row.get("id"))
    title = youtube.clean_text(row.get("title"))
    if not POD_ID_RE.fullmatch(pod_id) or not title:
        return None
    published = parse_rss_date(row.get("publishedAt"))
    if published is None:
        return None
    # The enclosure URL is third-party data relayed by tuber: validated as
    # received (no whitespace cleanup that could normalise a crafted value
    # into something else) and dropped when unsafe; the episode then links
    # to the registry's feed URL instead.
    audio_url = safe_url(row.get("audioUrl"))
    return Candidate(
        show=show, native_id=pod_id, title=title, url=audio_url or show.rss, video_id=None,
        audio_url=audio_url, duration_s=parse_duration(row.get("duration")),
        label=youtube.clean_text(row.get("publishedAt")), published_at=utc_minute(published),
        precision="exact", description=clean_show_notes(row.get("description")),
    )


@dataclasses.dataclass
class Discovery:
    candidates: list[Candidate]
    errors: list[tuple[Show, str]]
    relative_labels: int = 0
    parsed_labels: int = 0
    unparsed_samples: list[str] = dataclasses.field(default_factory=list)
    third_party_dropped: int = 0


def discover(shows: list[Show], client: TuberClient, now: dt.datetime) -> Discovery:
    result = Discovery(candidates=[], errors=[])
    for order, show in enumerate(shows):
        try:
            if show.kind == "channel":
                rows = _rows(client.get(f"/channel/{show.channel_id}", {"count": show.count}), "videos")
            elif show.kind == "search":
                rows = _rows(client.get("/search", {"q": show.query, "count": show.count}), "videos")
            else:
                rows = _rows(client.get("/podcast/episodes", {"rss": show.rss, "count": show.count}), "episodes")
            # Every curated channel has uploads and search always answers
            # something, so an empty list is an outage shape, never "no news".
            if not rows:
                raise TuberError("empty listing")
            found: list[Candidate] = []
            for row in rows:
                if show.kind == "podcast":
                    candidate = normalize_podcast(show, row)
                else:
                    candidate = normalize_video(show, row, now)
                    if candidate is not None and show.kind == "search" and candidate.channel_id != show.channel_id:
                        # Mandatory channel constraint: third-party re-streams never enter.
                        result.third_party_dropped += 1
                        continue
                    if candidate is not None:
                        result.relative_labels += 1
                        if candidate.published_at is not None:
                            result.parsed_labels += 1
                        elif len(result.unparsed_samples) < 5:
                            result.unparsed_samples.append(candidate.label or "<empty>")
                if candidate is not None:
                    candidate.order = order
                    found.append(candidate)
            if not found and show.kind != "search":
                raise TuberError("no usable rows in listing")
            result.candidates.extend(found)
        except FETCH_ERRORS as exc:  # this source failed; the others still publish
            result.errors.append((show, f"{type(exc).__name__}: {exc}"))
    return result


def first_sight_rejection(candidate: Candidate, now: dt.datetime) -> str | None:
    if candidate.is_live:
        return "live now"
    if candidate.published_at is None:
        return "unparseable publish age"
    if candidate.show.kind == "podcast":
        age_days = (now - candidate.published_at).days
    else:
        age_days = youtube.approximate_age_days(candidate.label)
        if age_days is None:
            return "unparseable publish age"
    if age_days > FIRST_SIGHT_MAX_AGE_DAYS:
        return "older than the first-sight window"
    if candidate.duration_s is None:
        if candidate.show.kind != "podcast":
            return "unknown duration"
    elif candidate.duration_s < candidate.show.min_duration_s:
        return "shorter than min_duration_s"
    return None


# ---------------------------------------------------------------------------
# Index


def empty_transcript() -> dict:
    return {"available": False, "source": None, "words": 0, "checked_at": None, "attempts": 0}


def build_episode(candidate: Candidate, now: dt.datetime) -> dict:
    show = candidate.show
    return {
        "id": candidate.episode_id,
        "show_id": show.id,
        "show": show.name,
        "kind": show.listener_kind,
        "priority": show.priority,
        "tags": list(show.tags),
        "title": candidate.title,
        "url": candidate.url,
        "video_id": candidate.video_id,
        "audio_url": candidate.audio_url,
        "published_at": iso(candidate.published_at),
        "published_precision": candidate.precision,
        "first_seen_at": iso(now),
        "duration_s": candidate.duration_s,
        "transcript": empty_transcript(),
        "excerpts": [],
        "description": first_words(candidate.description, MAX_DESCRIPTION_WORDS),
    }


def load_index(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise IndexStateError(f"{path}: cannot parse existing index ({exc}); refusing to reset its state") from exc
    if not isinstance(payload, dict) or payload.get("lane") != LANE or payload.get("schema") != SCHEMA \
            or not isinstance(payload.get("episodes"), list):
        raise IndexStateError(f"{path}: not a schema-{SCHEMA} {LANE} index; refusing to overwrite it")
    return payload


def _episode_is_well_formed(episode: Any) -> bool:
    if not isinstance(episode, dict):
        return False
    show_id, video_id, episode_id = episode.get("show_id"), episode.get("video_id"), episode.get("id")
    if not isinstance(show_id, str) or not SHOW_ID_RE.fullmatch(show_id) or not isinstance(episode_id, str):
        return False
    if video_id is None:
        native = episode_id.removeprefix(f"{show_id}:")
        id_ok = episode_id.startswith(f"{show_id}:") and bool(POD_ID_RE.fullmatch(native))
    else:
        id_ok = isinstance(video_id, str) and bool(VIDEO_ID_RE.fullmatch(video_id)) \
            and episode_id == f"{show_id}:{video_id}"
    return (
        id_ok
        and parse_iso(episode.get("first_seen_at")) is not None
        and parse_iso(episode.get("published_at")) is not None
        and isinstance(episode.get("transcript"), dict)
    )


def sanitize_reloaded(episode: dict, show: Show) -> None:
    """Re-derive every published URL of a reloaded record and re-apply the
    excerpt caps, so a hand-edited (or older) index can never re-publish an
    unsafe URL or more transcript text than the quote policy allows. For
    records this script wrote, every step is the identity (no diff)."""
    video_id = episode.get("video_id")
    if video_id:
        episode["url"] = youtube_watch_url(video_id)
        episode["audio_url"] = None
        kept = []
        for excerpt in episode.get("excerpts") or []:
            if not isinstance(excerpt, dict) or not isinstance(excerpt.get("text"), str):
                continue
            at_s = excerpt.get("at_s")
            if isinstance(at_s, bool) or not isinstance(at_s, int) or at_s < 0:
                continue
            kept.append({"text": first_words(excerpt["text"], MAX_EXCERPT_WORDS), "at_s": at_s,
                         "url": youtube_watch_url(video_id, at_s)})
        episode["excerpts"] = kept[:MAX_EXCERPTS]
    else:
        episode["audio_url"] = safe_url(episode.get("audio_url"))
        episode["url"] = safe_url(episode.get("url")) or episode["audio_url"] or show.rss
        episode["excerpts"] = []


def resync_show_fields(episode: dict, show: Show) -> None:
    """Show-level fields follow the registry; episode-level facts never change."""
    episode["show"] = show.name
    episode["kind"] = show.listener_kind
    episode["priority"] = show.priority
    episode["tags"] = list(show.tags)


def _sort_key(episode: dict) -> tuple:
    return (episode["published_at"], episode["first_seen_at"], episode["id"])


# ---------------------------------------------------------------------------
# Transcripts


@dataclasses.dataclass
class TranscriptOutcome:
    status: str  # ok | empty | incomplete | non-english | rate_limited | error
    segments: list[dict] = dataclasses.field(default_factory=list)
    source: str | None = None
    detail: str = ""


def fetch_transcript(client: TuberClient, video_id: str, duration_s: int | None) -> TranscriptOutcome:
    payload: Any = None
    last: TuberError | None = None
    for attempt in range(2):  # one retry with backoff
        if attempt:
            client.sleep(TRANSCRIPT_RETRY_BACKOFF_S)
        try:
            payload = client.get(f"/video/{video_id}/transcript", timeout=TRANSCRIPT_TIMEOUT_S)
            last = None
            break
        except ValueError as exc:  # refused by the read-only guard
            return TranscriptOutcome("error", detail=str(exc))
        except http.client.HTTPException as exc:  # a truncated response: a failed attempt
            last = TuberError(f"{type(exc).__name__}: {exc}")
        except TuberError as exc:
            last = exc
            if exc.status is not None and 400 <= exc.status < 500 and exc.status != 429:
                break  # a 4xx other than 429 will not change on retry
    if last is not None:
        return TranscriptOutcome("rate_limited" if last.rate_limited else "error", detail=str(last))
    if not isinstance(payload, dict) or not isinstance(payload.get("segments"), list):
        return TranscriptOutcome("error", detail="unexpected transcript payload")
    segments = [row for row in payload["segments"] if isinstance(row, dict)]
    if not segments or transcript_word_count(segments) == 0:
        return TranscriptOutcome("empty")
    language = payload.get("language")
    if isinstance(language, str) and language and not language.lower().startswith("en"):
        return TranscriptOutcome("non-english", detail=language)
    # Long-form only: a short launch video may legitimately end in music.
    if duration_s and duration_s >= COVERAGE_CHECK_MIN_DURATION_S:
        starts = [row["startMs"] for row in segments
                  if isinstance(row.get("startMs"), (int, float)) and not isinstance(row.get("startMs"), bool)]
        if not starts or max(starts) / 1000 < MIN_TRANSCRIPT_COVERAGE * duration_s:
            return TranscriptOutcome("incomplete", detail=f"covers {int(max(starts or [0])) // 1000}s of {duration_s}s")
    source = payload.get("source")
    return TranscriptOutcome("ok", segments=segments, source=source if isinstance(source, str) and source else None)


def transcript_bucket(episode: dict, now: dt.datetime) -> int | None:
    """None = not due. 0 = fresh, never tried; 1 = retry due; 2 = backlog."""
    video_id = episode.get("video_id")
    if not isinstance(video_id, str) or not VIDEO_ID_RE.fullmatch(video_id):
        return None  # RSS audio (tuber does not transcribe it) or a damaged record
    state = episode["transcript"]
    if state.get("available"):
        return None
    attempts = state.get("attempts") or 0
    published = parse_iso(episode["published_at"]) or now
    fresh = now - published < TRANSCRIPT_RETRY_WINDOW
    if attempts == 0:
        return 0 if fresh else 2
    if not fresh:
        return None
    checked = parse_iso(state.get("checked_at"))
    interval = TRANSCRIPT_FAST_INTERVAL if attempts < TRANSCRIPT_FAST_ATTEMPTS else TRANSCRIPT_SLOW_INTERVAL
    if checked is not None and now - checked < interval:
        return None
    return 1


@dataclasses.dataclass
class TranscriptStats:
    fetched: int = 0
    ok: int = 0
    empty: int = 0
    rate_limited: int = 0
    errors: int = 0
    stopped: str = ""


def update_transcripts(episodes: list[dict], client: TuberClient, now: dt.datetime, *,
                       max_fetches: int, spacing_s: float = TRANSCRIPT_SPACING_S,
                       budget_s: float = TRANSCRIPT_PHASE_BUDGET_S) -> TranscriptStats:
    stats = TranscriptStats()
    due = []
    for episode in episodes:
        bucket = transcript_bucket(episode, now)
        if bucket is not None:
            published = parse_iso(episode["published_at"]) or now
            due.append(((bucket, -published.timestamp(), PRIORITY_RANK.get(episode.get("priority"), 9),
                         episode["id"]), episode))
    due.sort(key=lambda row: row[0])
    started = client.monotonic()
    consecutive_limits = 0
    for _, episode in due:
        if stats.fetched >= max_fetches:
            stats.stopped = "per-run cap"
            break
        if client.monotonic() - started > budget_s:
            stats.stopped = "time budget"
            break
        if consecutive_limits >= RATE_LIMIT_BREAKER:
            stats.stopped = "rate-limit breaker"
            break
        if stats.fetched:
            client.sleep(spacing_s)
        outcome = fetch_transcript(client, episode["video_id"], episode.get("duration_s"))
        stats.fetched += 1
        state = dict(episode["transcript"])
        state["attempts"] = (state.get("attempts") or 0) + 1
        state["checked_at"] = iso(now)
        if outcome.status == "ok":
            consecutive_limits = 0
            stats.ok += 1
            state.update(available=True, source=outcome.source,
                         words=transcript_word_count(outcome.segments))
            windows = select_windows(outcome.segments, max_windows=MAX_EXCERPTS, max_words=MAX_EXCERPT_WORDS)
            episode["excerpts"] = [
                {"text": window["text"], "at_s": window["at_s"],
                 "url": youtube_watch_url(episode["video_id"], window["at_s"])}
                for window in windows
            ]
        elif outcome.status == "rate_limited":
            consecutive_limits += 1
            stats.rate_limited += 1
        else:
            consecutive_limits = 0
            if outcome.status == "error":
                stats.errors += 1
            else:
                stats.empty += 1
        episode["transcript"] = state
    return stats


# ---------------------------------------------------------------------------
# Rendering


def duration_label(seconds: Any) -> str:
    if not isinstance(seconds, int) or isinstance(seconds, bool):
        return "unknown"
    hours, rest = divmod(seconds, 3600)
    minutes = rest // 60
    return f"{hours}h {minutes:02d}m" if hours else f"{minutes}m {rest % 60:02d}s"


def clock_label(seconds: int) -> str:
    hours, rest = divmod(max(0, seconds), 3600)
    minutes, secs = divmod(rest, 60)
    return f"{hours}:{minutes:02d}:{secs:02d}" if hours else f"{minutes}:{secs:02d}"


def _md_escape(text: str) -> str:
    """One line of inert Markdown text: no link, HTML or code syntax, and no
    line break or control character that could start a new block."""
    text = "".join(" " if unicodedata.category(char)[0] == "C" else char for char in str(text))
    return re.sub(r"([\[\]\\`<>])", r"\\\1", " ".join(text.split()))


def transcript_label(episode: dict) -> str:
    state = episode["transcript"]
    if not episode.get("video_id"):
        return "not applicable (RSS audio; show notes only)"
    if state.get("available"):
        return f"available ({state.get('source') or 'unknown source'}, {state.get('words', 0):,} words)"
    attempts = state.get("attempts") or 0
    if attempts == 0:
        return "not checked yet"
    return f"not available yet ({attempts} attempt{'s' if attempts != 1 else ''})"


def render_markdown(*, day: dt.date, index: dict, shows: list[Show],
                    errors: list[tuple[Show, str]], base_url: str) -> str:
    todays = [
        episode for episode in index["episodes"]
        if (parse_iso(episode["first_seen_at"]) or dt.datetime.min.replace(tzinfo=dt.timezone.utc)).date() == day
    ]
    todays.sort(key=lambda e: (PRIORITY_RANK.get(e["priority"], 9), -_timestamp(e["published_at"]), e["id"]))
    with_transcript = sum(1 for episode in todays if episode["transcript"].get("available"))
    lines = [
        f"# Podcast Signal - {day.isoformat()}",
        "",
        f"Source: tuber-api ({base_url.rstrip('/')}), read-only. Aradio source lane; contract in `docs/aradio.md`.",
        "",
        "## Summary",
        f"- Sources checked: {len(shows)}",
        f"- Fetch errors: {len(errors)}",
        f"- Degraded: {'yes' if index['degraded'] else 'no'}",
        f"- Episodes first seen today: {len(todays)}",
        f"- With transcript: {with_transcript}",
        f"- Episodes in the rolling 30-day index: {len(index['episodes'])}",
        "- Generation endpoints called: 0",
        "",
        f"## Episodes first seen {day.isoformat()}",
        "",
    ]
    if not todays:
        lines.extend(["_No new episodes first seen today._", ""])
    for episode in todays:
        published = parse_iso(episode["published_at"])
        first_seen = parse_iso(episode["first_seen_at"])
        lines.extend([
            f"### [{_md_escape(episode['title'])}](<{episode['url']}>)",
            f"- Show: {episode['show']} ({episode['priority']}; {episode['kind']})",
            f"- Published: {published.strftime('%Y-%m-%d %H:%M UTC') if published else 'unknown'}"
            f" ({episode['published_precision']})",
            f"- First seen: {first_seen.strftime('%Y-%m-%d %H:%M UTC') if first_seen else 'unknown'}",
            f"- Duration: {duration_label(episode.get('duration_s'))}",
            f"- Transcript: {transcript_label(episode)}",
        ])
        if episode.get("description"):
            lines.append(f"- Notes: {_md_escape(episode['description'])}")
        if episode.get("excerpts"):
            lines.append("- Excerpts:")
            for excerpt in episode["excerpts"]:
                lines.append(f"  - [{clock_label(excerpt['at_s'])}](<{excerpt['url']}>) {_md_escape(excerpt['text'])}")
        lines.append("")
    if errors:
        lines.extend(["## Fetch errors", ""])
        for show, error in sorted(errors, key=lambda row: row[0].id):
            lines.append(f"- {show.name} (`{show.id}`): {_md_escape(error[:160])}")
        lines.append("")
    lines.extend(["---", "*Generated by `scripts/fetch_podcast_signal.py`.*", ""])
    return "\n".join(lines)


def write_if_changed(path: Path, text: str) -> bool:
    """Atomic write (temp file in the same directory + os.replace), skipped
    when the bytes would not change so a quiet run leaves no diff."""
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False,
                                     prefix=f".{path.name}.", suffix=".tmp") as handle:
        handle.write(text)
        temp_path = Path(handle.name)
    os.chmod(temp_path, 0o644)
    os.replace(temp_path, path)
    return True


def index_text(index: dict) -> str:
    return json.dumps(index, indent=2, ensure_ascii=False) + "\n"


# ---------------------------------------------------------------------------
# Run


@dataclasses.dataclass
class RunResult:
    exit_code: int
    summary: str
    wrote: list[str] = dataclasses.field(default_factory=list)


def run(*, registry: Path, out_dir: Path, base_url: str, now: dt.datetime, client: TuberClient,
        max_transcript_fetches: int = DEFAULT_MAX_TRANSCRIPT_FETCHES,
        max_detail_fetches: int = DEFAULT_MAX_DETAIL_FETCHES,
        transcript_spacing_s: float = TRANSCRIPT_SPACING_S) -> RunResult:
    now = utc_minute(now)
    try:
        all_shows = load_registry(registry)
    except RegistryError as exc:
        return RunResult(EXIT_BAD_INPUT, f"ERROR: invalid registry: {exc}")
    shows = [show for show in all_shows if show.include_in_aradio]
    if not shows:
        return RunResult(EXIT_BAD_INPUT, "ERROR: no registry source has include_in_aradio=true")
    index_path = out_dir / INDEX_NAME
    try:
        previous = load_index(index_path)
    except IndexStateError as exc:
        return RunResult(EXIT_BAD_INPUT, f"ERROR: {exc}")

    found = discover(shows, client, now)
    if len(found.errors) == len(shows):
        detail = "; ".join(f"{show.id}: {error}" for show, error in found.errors[:5])
        return RunResult(
            EXIT_TOTAL_FETCH_FAILURE,
            f"ERROR: total tuber-api fetch failure: all {len(shows)} source(s) failed against {base_url}; "
            f"refusing to write {out_dir} so the outage stays visible to the freshness watchdog ({detail})",
        )
    if found.relative_labels >= PUBLISH_AGE_DRIFT_MIN_LABELS and found.parsed_labels == 0:
        return RunResult(
            EXIT_PUBLISH_AGE_DRIFT,
            f"ERROR: publish-age format drift: none of {found.relative_labels} tuber relative-age label(s) "
            f"parsed (samples: {found.unparsed_samples}); refusing to write {out_dir}. Extend "
            "fetch_youtube_signal.AGE_PATTERN for the new label format",
        )

    shows_by_id = {show.id: show for show in shows}
    episodes: dict[str, dict] = {}
    for episode in (previous or {}).get("episodes", []):
        if not _episode_is_well_formed(episode) or episode["show_id"] not in shows_by_id:
            continue  # orphaned (show removed or disabled) or damaged record
        if now - parse_iso(episode["published_at"]) > RETENTION:
            continue
        record = json.loads(json.dumps(episode))
        resync_show_fields(record, shows_by_id[record["show_id"]])
        sanitize_reloaded(record, shows_by_id[record["show_id"]])
        episodes[record["id"]] = record
    known_videos = {episode["video_id"] for episode in episodes.values() if episode.get("video_id")}

    # New candidates, newest first; registry order breaks ties so the first
    # claimant of a video found by two sources is deterministic.
    fresh = [c for c in found.candidates if c.episode_id not in episodes]
    fresh.sort(key=lambda c: (-(c.published_at.timestamp() if c.published_at else 0), c.order, c.native_id))
    detail_fetches = 0
    added: list[dict] = []
    deferred = rejected = 0
    for candidate in fresh:
        if first_sight_rejection(candidate, now):
            continue
        if candidate.video_id and candidate.video_id in known_videos:
            continue
        if candidate.video_id and detail_fetches < max_detail_fetches:
            if detail_fetches:
                client.sleep(DETAIL_SPACING_S)
            detail_fetches += 1
            try:
                details = client.get(f"/video/{candidate.video_id}")
            except FETCH_ERRORS:
                details = None
            # Only the notes are read from /api/video/{id}: its isLive is true
            # for any PAST stream ("Streamed live on Oct 28") -- it silently
            # dropped the Alphabet Q3 call in a live run -- and its relative
            # publishDate can be a stale cached label ("Streamed 7d ago" on a
            # month-old stream). Liveness and age come from the listing.
            if isinstance(details, dict):
                candidate.description = clean_show_notes(details.get("description"))
        if candidate.show.ai_filter:
            verdict = is_ai_topical(candidate.title, candidate.description)
            if verdict is None:
                deferred += 1
                continue  # no notes yet: decide on a later run
            if not verdict:
                rejected += 1
                continue
        episode = build_episode(candidate, now)
        episodes[episode["id"]] = episode
        added.append(episode)
        if candidate.video_id:
            known_videos.add(candidate.video_id)

    # Fill show notes that were missing at first sight (tuber sometimes serves
    # a light cached record without a description), while still fresh.
    added_ids = {episode["id"] for episode in added}
    for episode in sorted(episodes.values(), key=_sort_key, reverse=True):
        if detail_fetches >= max_detail_fetches:
            break
        video_id = episode.get("video_id")
        if episode.get("description") or episode["id"] in added_ids:
            continue
        if not isinstance(video_id, str) or not VIDEO_ID_RE.fullmatch(video_id):
            continue
        if now - parse_iso(episode["published_at"]) >= TRANSCRIPT_RETRY_WINDOW:
            continue
        detail_fetches += 1
        client.sleep(DETAIL_SPACING_S)
        try:
            details = client.get(f"/video/{episode['video_id']}")
        except FETCH_ERRORS:
            continue
        if isinstance(details, dict):
            notes = first_words(clean_show_notes(details.get("description")), MAX_DESCRIPTION_WORDS)
            if notes:
                episode["description"] = notes

    ordered = sorted(episodes.values(), key=_sort_key, reverse=True)
    stats = update_transcripts(ordered, client, now, max_fetches=max_transcript_fetches,
                               spacing_s=transcript_spacing_s)
    degraded = len(found.errors) * 2 > len(shows)
    content = {"degraded": degraded, "episodes": ordered}
    unchanged = previous is not None and {
        "degraded": previous.get("degraded"), "episodes": previous.get("episodes")
    } == content
    index = {
        "lane": LANE,
        "schema": SCHEMA,
        "updated_at": (previous.get("updated_at") if unchanged else None) or iso(now),
        "degraded": degraded,
        "episodes": ordered,
    }
    wrote = []
    if write_if_changed(index_path, index_text(index)):
        wrote.append(INDEX_NAME)
    day_name = f"{now.date().isoformat()}.md"
    markdown = render_markdown(day=now.date(), index=index, shows=shows, errors=found.errors, base_url=base_url)
    if write_if_changed(out_dir / day_name, markdown):
        wrote.append(day_name)

    by_kind: dict[str, int] = {}
    for episode in added:
        by_kind[episode["kind"]] = by_kind.get(episode["kind"], 0) + 1
    kinds = ", ".join(f"{kind} {count}" for kind, count in sorted(by_kind.items())) or "none"
    summary = (
        f"podcasts: {len(shows) - len(found.errors)}/{len(shows)} sources ok; new {len(added)} ({kinds}); "
        f"ai-filter rejected {rejected}, deferred {deferred}; third-party search results dropped "
        f"{found.third_party_dropped}; transcripts fetched {stats.fetched} (ok {stats.ok}, none {stats.empty}, "
        f"rate-limited {stats.rate_limited}, errors {stats.errors}{'; stopped: ' + stats.stopped if stats.stopped else ''}); "
        f"index {len(ordered)}; degraded={'true' if degraded else 'false'}; tuber requests {client.requests}; "
        f"wrote {', '.join(wrote) if wrote else 'nothing (no change)'}"
    )
    return RunResult(0, summary, wrote)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--tuber-api-base", default=os.environ.get("TUBER_API_BASE") or youtube.DEFAULT_TUBER_API_BASE)
    parser.add_argument("--max-transcript-fetches", type=int, default=DEFAULT_MAX_TRANSCRIPT_FETCHES)
    parser.add_argument("--max-detail-fetches", type=int, default=DEFAULT_MAX_DETAIL_FETCHES)
    parser.add_argument("--now", help="UTC run time (ISO 8601) for replays and tests; default: now")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(sys.argv[1:] if argv is None else argv)
    except SystemExit as exc:  # argparse already printed the reason
        return EXIT_BAD_INPUT if exc.code else 0
    if args.max_transcript_fetches < 0 or args.max_detail_fetches < 0:
        print("ERROR: fetch caps must be >= 0", file=sys.stderr)
        return EXIT_BAD_INPUT
    if args.now:
        now = parse_iso(args.now)
        if now is None:
            print(f"ERROR: invalid --now {args.now!r}; expected ISO 8601", file=sys.stderr)
            return EXIT_BAD_INPUT
    else:
        now = dt.datetime.now(dt.timezone.utc)
    result = run(
        registry=args.registry, out_dir=args.out_dir, base_url=args.tuber_api_base, now=now,
        client=TuberClient(args.tuber_api_base, transport=http_get_json),
        max_transcript_fetches=args.max_transcript_fetches, max_detail_fetches=args.max_detail_fetches,
    )
    print(result.summary, file=sys.stderr if result.exit_code else sys.stdout)
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
