#!/usr/bin/env python3
"""Fetch YouTube AI signal from tuber into a deterministic daily Markdown lane.

The lane is deliberately read-only: it uses tuber's discovery, existing summary
preview, and transcript endpoints, but it never triggers paid/generated summary
work. If a video has no existing summary or transcript, it can still appear as a
metadata-only watch item when the source/score is strong enough.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
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
from pathlib import Path
from typing import Any, Callable, Iterable

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = REPO_ROOT / "data" / "sources" / "youtube_channels.json"
DEFAULT_OUT_DIR = REPO_ROOT / "research" / "youtube"
DEFAULT_TUBER_API_BASE = "https://tuber-api.guzus.xyz"
USER_AGENT = "ai-research-arm/1.0 (https://github.com/guzus/ai-research-arm)"
TIMEOUT_SECONDS = 25
FORBIDDEN_GENERATION_PATH_PARTS = ("/summarize", "/acp/jobs")

PRIORITY_WEIGHT = {"P0": 100, "P1": 70, "P2": 40}
KIND_WEIGHT = {"channel": 24, "search": 10, "trending": 0}
TAG_WEIGHT = {
    "official": 24,
    "frontier-lab": 20,
    "model-release": 18,
    "research": 14,
    "agents": 12,
    "evals": 10,
    "open-models": 10,
    "infrastructure": 8,
    "inference": 8,
    "interviews": 6,
    "developer": 6,
    "podcasts": -8,
}
TITLE_BONUS_PATTERNS = (
    (re.compile(r"\b(announc|introduc|launch|release|preview|demo|keynote)\w*\b", re.I), 14),
    (re.compile(r"\b(model|llm|agent|agents|agentic|reasoning|benchmark|eval)\w*\b", re.I), 12),
    (re.compile(r"\b(open[- ]?weight|open[- ]?source|inference|post[- ]?training)\b", re.I), 10),
    (re.compile(r"\b(research|paper|technical|architecture|safety)\b", re.I), 8),
)
TITLE_PENALTY_PATTERNS = (
    (re.compile(r"\b(reaction|drama|shocking|insane|crazy|exposed)\b", re.I), -18),
    (re.compile(r"\b(make money|side hustle|passive income|sponsorship)\b", re.I), -20),
    (re.compile(r"\b(top \d+|news roundup|weekly recap)\b", re.I), -8),
)
LOW_EVIDENCE_WORDS = {"reaction", "drama", "rumor", "leak", "exposed"}
INCOMPLETE_TRAILING_WORDS = {"a", "an", "and", "as", "at", "by", "for", "from", "in", "of", "or", "the", "to", "with"}
RECENT_AGE_PENALTIES = (
    (365, -100),
    (180, -85),
    (90, -70),
    (30, -40),
    (21, -25),
)
ASCII_TRANSLATION = str.maketrans({
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2013": "-",
    "\u2014": "-",
    "\u2026": "...",
    "\u00a0": " ",
})


@dataclasses.dataclass(frozen=True)
class Source:
    id: str
    name: str
    kind: str
    priority: str
    tags: tuple[str, ...]
    include_in_digest: bool
    count: int
    query: str = ""
    topic: str = ""
    range: str = "1w"
    channel: str = ""
    notes: str = ""


@dataclasses.dataclass
class VideoCandidate:
    id: str
    title: str
    url: str
    source: Source
    channel: str = "Unknown"
    channel_id: str = ""
    published: str = "unknown"
    duration: int | str | None = None
    views: str = ""
    thumbnail: str = ""
    score: int = 0
    source_score: int = 0
    video_score: dict[str, Any] | None = None
    title_answer: str | None = None
    transcript_snippet: str | None = None
    evidence: str = "metadata-only"
    caveat: str = ""
    skipped_reason: str = ""


def _build_ssl_context() -> ssl.SSLContext:
    cafile = os.environ.get("SSL_CERT_FILE")
    if cafile and os.path.isfile(cafile):
        return ssl.create_default_context(cafile=cafile)
    for path in (
        "/etc/ssl/cert.pem",
        "/etc/ssl/certs/ca-certificates.crt",
        "/etc/pki/tls/certs/ca-bundle.crt",
        "/opt/homebrew/etc/openssl@3/cert.pem",
        "/usr/local/etc/openssl@3/cert.pem",
    ):
        if os.path.isfile(path):
            return ssl.create_default_context(cafile=path)
    return ssl.create_default_context()


SSL_CTX = _build_ssl_context()


def clean_text(value: Any) -> str:
    value = re.sub(r"<[^>]+>", " ", str(value or ""))
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def ascii_safe(value: str) -> str:
    value = value.translate(ASCII_TRANSLATION)
    value = value.encode("ascii", "ignore").decode("ascii")
    return "\n".join(line.rstrip() for line in value.splitlines()).strip()


def load_sources(path: Path) -> list[Source]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("YouTube source registry must be a JSON array")
    seen: set[str] = set()
    sources: list[Source] = []
    for row in raw:
        if not isinstance(row, dict):
            raise ValueError("each YouTube source must be an object")
        source = Source(
            id=clean_text(row.get("id")),
            name=clean_text(row.get("name")),
            kind=clean_text(row.get("kind")),
            priority=clean_text(row.get("priority")),
            tags=tuple(clean_text(tag) for tag in row.get("tags", [])),
            include_in_digest=bool(row.get("include_in_digest", True)),
            count=int(row.get("count", 10)),
            query=clean_text(row.get("query")),
            topic=clean_text(row.get("topic")),
            range=clean_text(row.get("range") or "1w"),
            channel=clean_text(row.get("channel")),
            notes=clean_text(row.get("notes")),
        )
        if not source.id or not source.name:
            raise ValueError("YouTube sources require id and name")
        if source.id in seen:
            raise ValueError(f"duplicate source id: {source.id}")
        if source.kind not in KIND_WEIGHT:
            raise ValueError(f"{source.id}: invalid kind {source.kind!r}")
        if source.priority not in PRIORITY_WEIGHT:
            raise ValueError(f"{source.id}: invalid priority {source.priority!r}")
        if source.count < 1 or source.count > 50:
            raise ValueError(f"{source.id}: count must be between 1 and 50")
        if source.kind == "search" and not source.query:
            raise ValueError(f"{source.id}: search source requires query")
        if source.kind == "trending" and not source.topic:
            raise ValueError(f"{source.id}: trending source requires topic")
        if source.kind == "channel" and not source.channel:
            raise ValueError(f"{source.id}: channel source requires channel")
        seen.add(source.id)
        sources.append(source)
    return sources


def build_api_url(base_url: str, path: str, params: dict[str, Any] | None = None) -> str:
    base = (base_url or DEFAULT_TUBER_API_BASE).strip().rstrip("/")
    if base.endswith("/api"):
        base = base[:-4]
    encoded = urllib.parse.urlencode(
        {key: str(value) for key, value in (params or {}).items() if value not in (None, "")}
    )
    return f"{base}/api{path}" + (f"?{encoded}" if encoded else "")


def fetch_json(base_url: str, path: str, params: dict[str, Any] | None = None) -> Any:
    if any(part in path for part in FORBIDDEN_GENERATION_PATH_PARTS):
        raise ValueError(f"refusing non-read-only tuber endpoint: {path}")
    url = build_api_url(base_url, path, params)
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS, context=SSL_CTX) as resp:
        payload = resp.read()
    return json.loads(payload.decode("utf-8"))


def _video_id(row: dict[str, Any]) -> str:
    raw = clean_text(row.get("id") or row.get("videoId") or row.get("video_id"))
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", raw):
        return raw
    match = re.search(r"(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{11})", clean_text(row.get("url")))
    return match.group(1) if match else ""


def _video_score_points(video_score: dict[str, Any] | None) -> int:
    if not video_score:
        return 0
    try:
        score = int(video_score.get("score", 0))
    except (TypeError, ValueError):
        return 0
    return max(-20, min(40, round((score - 50) / 2)))


def approximate_age_days(label: str) -> int | None:
    text = clean_text(label).lower()
    if not text:
        return None
    if "today" in text or "just now" in text:
        return 0
    if "yesterday" in text:
        return 1
    match = re.search(r"(\d+)\s+(minute|hour|day|week|month|year)s?\s+ago", text)
    if not match:
        return None
    amount = int(match.group(1))
    unit = match.group(2)
    if unit in {"minute", "hour"}:
        return 0
    if unit == "day":
        return amount
    if unit == "week":
        return amount * 7
    if unit == "month":
        return amount * 30
    if unit == "year":
        return amount * 365
    return None


def score_candidate(source: Source, row: dict[str, Any], title: str, video_score: dict[str, Any] | None) -> int:
    score = PRIORITY_WEIGHT[source.priority] + KIND_WEIGHT[source.kind]
    for tag in source.tags:
        score += TAG_WEIGHT.get(tag, 0)
    for pattern, weight in TITLE_BONUS_PATTERNS:
        if pattern.search(title):
            score += weight
    for pattern, weight in TITLE_PENALTY_PATTERNS:
        if pattern.search(title):
            score += weight
    score += _video_score_points(video_score)
    if row.get("isSummarized") or row.get("titleAnswer"):
        score += 10
    published = clean_text(row.get("publishedAt") or row.get("published") or row.get("publishedText"))
    age_days = approximate_age_days(published)
    if age_days is not None:
        for minimum_days, penalty in RECENT_AGE_PENALTIES:
            if age_days >= minimum_days:
                score += penalty
                break
    else:
        score -= 30
    if not source.include_in_digest:
        score -= 30
    return score


def normalize_video(source: Source, row: dict[str, Any]) -> VideoCandidate | None:
    video_id = _video_id(row)
    title = clean_text(row.get("title"))
    if not video_id or not title:
        return None
    video_score = row.get("videoScore") if isinstance(row.get("videoScore"), dict) else None
    title_answer = clean_text(row.get("titleAnswer")) or None
    source_score = score_candidate(source, row, title, video_score)
    evidence = "summary" if title_answer else "metadata-only"
    caveat = "metadata-only; no existing summary or transcript observed" if evidence == "metadata-only" else ""
    return VideoCandidate(
        id=video_id,
        title=title,
        url=f"https://www.youtube.com/watch?v={video_id}",
        source=source,
        channel=clean_text(row.get("channel") or row.get("author") or row.get("channelName")) or "Unknown",
        channel_id=clean_text(row.get("channelId")),
        published=clean_text(row.get("publishedAt") or row.get("published") or row.get("publishedText")) or "unknown",
        duration=row.get("duration") or row.get("durationText"),
        views=clean_text(row.get("views") or row.get("viewCountText")),
        thumbnail=clean_text(row.get("thumbnail")),
        score=source_score,
        source_score=source_score,
        video_score=video_score,
        title_answer=title_answer,
        evidence=evidence,
        caveat=caveat,
    )


def extract_videos(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if not isinstance(payload, dict):
        return []
    for key in ("videos", "items", "results"):
        rows = payload.get(key)
        if isinstance(rows, list):
            return [row for row in rows if isinstance(row, dict)]
    data = payload.get("data")
    if isinstance(data, dict):
        return extract_videos(data)
    return []


FetchJson = Callable[[str, str, dict[str, Any] | None], Any]


def fetch_source_candidates(
    source: Source,
    *,
    base_url: str,
    fetch_json_fn: FetchJson = fetch_json,
) -> list[VideoCandidate]:
    if source.kind == "trending":
        payload = fetch_json_fn(
            base_url,
            "/trending",
            {"topic": source.topic, "range": source.range, "count": source.count, "cache": "daily"},
        )
    elif source.kind == "search":
        payload = fetch_json_fn(base_url, "/search", {"q": source.query, "count": source.count})
    else:
        payload = fetch_json_fn(
            base_url,
            f"/channel/{urllib.parse.quote(source.channel, safe='')}",
            {"count": source.count},
        )
    out: list[VideoCandidate] = []
    for row in extract_videos(payload):
        candidate = normalize_video(source, row)
        if candidate:
            out.append(candidate)
    return out


def dedupe_candidates(candidates: Iterable[VideoCandidate]) -> list[VideoCandidate]:
    by_id: dict[str, VideoCandidate] = {}
    for candidate in candidates:
        previous = by_id.get(candidate.id)
        if previous is None or candidate.score > previous.score:
            by_id[candidate.id] = candidate
    return sorted(
        by_id.values(),
        key=lambda item: (
            -item.score,
            item.source.priority,
            item.source.name.lower(),
            item.title.lower(),
            item.id,
        ),
    )


def collect_candidates(
    sources: list[Source],
    *,
    base_url: str,
    fetch_json_fn: FetchJson = fetch_json,
) -> tuple[list[VideoCandidate], list[tuple[Source, str]]]:
    candidates: list[VideoCandidate] = []
    errors: list[tuple[Source, str]] = []
    for source in sources:
        try:
            candidates.extend(fetch_source_candidates(source, base_url=base_url, fetch_json_fn=fetch_json_fn))
        except (json.JSONDecodeError, urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
            errors.append((source, f"{type(exc).__name__}: {exc}"))
    return dedupe_candidates(candidates), errors


def _first_segments(payload: Any, limit: int = 3) -> list[str]:
    segments: Any = []
    if isinstance(payload, dict):
        segments = payload.get("segments") or payload.get("transcript") or payload.get("items") or []
    elif isinstance(payload, list):
        segments = payload
    out: list[str] = []
    for row in segments:
        if isinstance(row, dict):
            text = clean_text(row.get("text") or row.get("content"))
        else:
            text = clean_text(row)
        if text:
            out.append(text)
        if len(out) >= limit:
            break
    return out


def enrich_candidates(
    candidates: list[VideoCandidate],
    *,
    base_url: str,
    max_preview_checks: int,
    max_transcript_checks: int,
    fetch_json_fn: FetchJson = fetch_json,
) -> list[tuple[str, str]]:
    errors: list[tuple[str, str]] = []
    preview_checked = 0
    transcript_checked = 0
    for candidate in candidates:
        if not candidate.title_answer and preview_checked < max_preview_checks:
            preview_checked += 1
            try:
                preview = fetch_json_fn(base_url, f"/video/{candidate.id}/summary-preview", None)
                if isinstance(preview, dict) and preview.get("available"):
                    candidate.title_answer = clean_text(preview.get("titleAnswer") or preview.get("snippet")) or None
                    candidate.evidence = "summary"
                    candidate.caveat = ""
                    candidate.score += 10
            except (json.JSONDecodeError, urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
                errors.append((candidate.id, f"summary-preview {type(exc).__name__}: {exc}"))

        if candidate.evidence == "metadata-only" and transcript_checked < max_transcript_checks:
            transcript_checked += 1
            try:
                transcript = fetch_json_fn(base_url, f"/video/{candidate.id}/transcript", None)
                snippets = _first_segments(transcript)
                if snippets:
                    candidate.transcript_snippet = " ".join(snippets)[:360]
                    candidate.evidence = "transcript"
                    candidate.caveat = "transcript-backed, no generated summary"
                    candidate.score += 8
            except (json.JSONDecodeError, urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
                errors.append((candidate.id, f"transcript {type(exc).__name__}: {exc}"))
    candidates.sort(key=lambda item: (-item.score, item.source.name.lower(), item.title.lower(), item.id))
    return errors


def is_recent_enough(candidate: VideoCandidate, max_age_days: int) -> bool:
    age_days = approximate_age_days(candidate.published)
    if age_days is None:
        return False
    return age_days <= max_age_days


def has_selection_evidence(candidate: VideoCandidate) -> bool:
    if candidate.evidence != "metadata-only":
        return True
    return "official" in candidate.source.tags


def select_high_signal(
    candidates: list[VideoCandidate],
    max_items: int,
    min_score: int,
    max_age_days: int,
) -> tuple[list[VideoCandidate], list[VideoCandidate]]:
    selected = [
        candidate
        for candidate in candidates
        if candidate.score >= min_score
        and candidate.source.include_in_digest
        and is_recent_enough(candidate, max_age_days)
        and has_selection_evidence(candidate)
    ]
    if not selected and candidates:
        selected = [
            candidate
            for candidate in candidates
            if candidate.source.include_in_digest
            and is_recent_enough(candidate, max_age_days)
            and has_selection_evidence(candidate)
        ][: min(5, max_items)]
    selected = selected[:max_items]
    selected_ids = {candidate.id for candidate in selected}
    skipped = [candidate for candidate in candidates if candidate.id not in selected_ids]
    for candidate in skipped:
        if not candidate.source.include_in_digest:
            candidate.skipped_reason = "source disabled for digest inclusion"
        elif not is_recent_enough(candidate, max_age_days):
            age_days = approximate_age_days(candidate.published)
            candidate.skipped_reason = (
                "unknown publish age"
                if age_days is None
                else f"older than recency window ({candidate.published})"
            )
        elif not has_selection_evidence(candidate):
            candidate.skipped_reason = "metadata-only non-official candidate"
        elif candidate.score < min_score:
            candidate.skipped_reason = f"score below threshold ({candidate.score} < {min_score})"
        elif candidate.evidence == "metadata-only":
            candidate.skipped_reason = "metadata-only after enrichment budget"
        else:
            candidate.skipped_reason = "lower-ranked duplicate/day candidate"
    return selected, skipped


def key_claims(candidate: VideoCandidate) -> list[str]:
    text = candidate.title_answer or candidate.transcript_snippet or candidate.title
    parts = []
    for part in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])", text):
        cleaned = clean_text(part)
        words = re.findall(r"[A-Za-z0-9]+", cleaned)
        if cleaned[-1:] not in {".", "!", "?"}:
            continue
        if len(cleaned) < 30:
            continue
        if words and words[-1].lower() in INCOMPLETE_TRAILING_WORDS:
            continue
        parts.append(cleaned)
    if candidate.title_answer and len(parts) <= 1:
        return [candidate.title]
    if candidate.title_answer and len(parts) > 1:
        parts = parts[1:]
    if not parts:
        return [candidate.title]
    return parts[:2]


def why_it_matters(candidate: VideoCandidate) -> str:
    if candidate.title_answer:
        if sum(1 for ch in candidate.title_answer if ord(ch) > 127) > 10:
            return "Existing tuber summary is not English; review the source video before digest promotion."
        return candidate.title_answer
    if candidate.transcript_snippet:
        return "Transcript is available; review before promoting because no generated summary exists yet."
    if "official" in candidate.source.tags:
        return "Official-source video surfaced by tuber; metadata should be checked against other primary sources before promotion."
    return "Discovery candidate from YouTube; treat as secondary signal until transcript or summary evidence is available."


def caveat_for(candidate: VideoCandidate) -> str:
    if candidate.caveat:
        return candidate.caveat
    words = {word.lower() for word in re.findall(r"[A-Za-z]+", candidate.title)}
    if words & LOW_EVIDENCE_WORDS:
        return "sensational framing; verify against primary sources"
    if "podcasts" in candidate.source.tags:
        return "long-form commentary/interview; extract primary claims before digest promotion"
    return "single YouTube source"


def duration_label(value: int | str | None) -> str:
    if value is None or value == "":
        return "unknown"
    if isinstance(value, int):
        hours, rem = divmod(value, 3600)
        minutes, seconds = divmod(rem, 60)
        if hours:
            return f"{hours}h {minutes}m {seconds}s"
        return f"{minutes}m {seconds}s"
    return clean_text(value)


def render_markdown(
    *,
    target_date: dt.date,
    sources: list[Source],
    candidates: list[VideoCandidate],
    selected: list[VideoCandidate],
    skipped: list[VideoCandidate],
    fetch_errors: list[tuple[Source, str]],
    enrich_errors: list[tuple[str, str]],
    base_url: str,
) -> str:
    enabled_sources = [source for source in sources if source.include_in_digest]
    lines = [
        f"# YouTube AI Signal - {target_date.isoformat()}",
        "",
        f"Generated: {dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"Source: tuber-api ({base_url.rstrip('/')})",
        "",
        "## Summary",
        f"- Sources checked: {len(sources)} ({len(enabled_sources)} enabled for digest inclusion)",
        f"- Unique videos collected: {len(candidates)}",
        f"- High-signal videos selected: {len(selected)}",
        f"- Fetch errors: {len(fetch_errors)}",
        f"- Enrichment errors: {len(enrich_errors)}",
        "- Paid/generated summaries requested: 0",
        "",
    ]

    lines.extend(["## High-Signal Videos", ""])
    if not selected:
        lines.extend(["_No high-signal YouTube videos passed the current filters._", ""])
    for candidate in selected:
        score_label = str(candidate.score)
        if candidate.video_score and candidate.video_score.get("band"):
            score_label += f" / {candidate.video_score.get('band')}"
        lines.extend(
            [
                f"### {candidate.title}",
                f"- Channel: {candidate.channel}",
                f"- Video: {candidate.url}",
                f"- Published: {candidate.published}",
                f"- Duration: {duration_label(candidate.duration)}",
                f"- Views: {candidate.views or 'unknown'}",
                f"- Score: {score_label}",
                f"- Source lane: {candidate.source.name} ({candidate.source.priority}; {candidate.source.kind})",
                f"- Evidence: {candidate.evidence}",
                f"- Why it matters: {why_it_matters(candidate)}",
                "- Key claims:",
            ]
        )
        for claim in key_claims(candidate):
            lines.append(f"  - {claim}")
        lines.extend([f"- Caveats: {caveat_for(candidate)}", ""])

    lines.extend(["## Watchlist / Skipped", ""])
    if not skipped:
        lines.extend(["_No skipped candidates._", ""])
    for candidate in skipped[:20]:
        reason = candidate.skipped_reason or "below selected set"
        lines.append(f"- [{candidate.title}]({candidate.url}) - skipped because {reason}; score={candidate.score}; evidence={candidate.evidence}")
    lines.append("")

    lines.extend(["## Sources Checked", ""])
    for source in sources:
        digest_flag = "yes" if source.include_in_digest else "no"
        detail = source.query or source.topic or source.channel
        lines.append(
            f"- {source.priority} {source.name} - {source.kind} `{detail}`; "
            f"count={source.count}; digest={digest_flag}; tags={', '.join(source.tags)}"
        )
    lines.append("")

    if fetch_errors:
        lines.extend(["## Fetch Errors", ""])
        for source, error in fetch_errors:
            lines.append(f"- {source.name}: {error}")
        lines.append("")

    if enrich_errors:
        lines.extend(["## Enrichment Errors", ""])
        for video_id, error in enrich_errors[:20]:
            lines.append(f"- {video_id}: {error}")
        lines.append("")

    lines.extend(["---", "*Generated by `scripts/fetch_youtube_signal.py`.*", ""])
    return ascii_safe("\n".join(lines)) + "\n"


def write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False, prefix=f".{path.name}.", suffix=".tmp"
    ) as tmp:
        tmp.write(text)
        tmp_path = Path(tmp.name)
    os.replace(tmp_path, path)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--date", default=dt.datetime.now(dt.timezone.utc).date().isoformat())
    parser.add_argument("--tuber-api-base", default=os.environ.get("TUBER_API_BASE", DEFAULT_TUBER_API_BASE))
    parser.add_argument("--max-items", type=int, default=15)
    parser.add_argument("--min-score", type=int, default=82)
    parser.add_argument("--max-preview-checks", type=int, default=12)
    parser.add_argument("--max-transcript-checks", type=int, default=4)
    parser.add_argument("--max-age-days", type=int, default=14)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        target_date = dt.date.fromisoformat(args.date)
    except ValueError:
        print(f"ERROR: invalid --date {args.date!r}; expected YYYY-MM-DD", file=sys.stderr)
        return 2
    if args.max_items < 1:
        print("ERROR: --max-items must be >= 1", file=sys.stderr)
        return 2

    sources = load_sources(args.registry)
    candidates, fetch_errors = collect_candidates(sources, base_url=args.tuber_api_base)
    enrich_errors = enrich_candidates(
        candidates,
        base_url=args.tuber_api_base,
        max_preview_checks=max(0, args.max_preview_checks),
        max_transcript_checks=max(0, args.max_transcript_checks),
    )
    selected, skipped = select_high_signal(candidates, args.max_items, args.min_score, max(0, args.max_age_days))
    markdown = render_markdown(
        target_date=target_date,
        sources=sources,
        candidates=candidates,
        selected=selected,
        skipped=skipped,
        fetch_errors=fetch_errors,
        enrich_errors=enrich_errors,
        base_url=args.tuber_api_base,
    )
    out_path = args.out_dir / f"{target_date.isoformat()}.md"
    write_atomic(out_path, markdown)
    print(
        f"Wrote {out_path} with {len(selected)} selected video(s), "
        f"{len(candidates)} candidate(s), {len(fetch_errors)} fetch error(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
