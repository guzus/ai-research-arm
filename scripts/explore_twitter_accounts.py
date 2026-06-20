#!/usr/bin/env python3
"""Discover candidate Twitter/X accounts for the ARA monitor.

This script is intentionally a scout, not a mutator. It gathers candidate
authors from broad X searches, scores them from observable tweet evidence, and
writes JSON that `curate_twitter_accounts.py propose` can review.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from curate_twitter_accounts import DEFAULT_MANIFEST, ManifestError, iter_handle_entries, normalize_handle

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = Path("/tmp/twitter-account-candidates.json")
DEFAULT_REPORT = Path("/tmp/twitter-account-explorer-report.md")
BIRD_CMD = os.environ.get("ARA_BIRD_CMD") or ("birdy" if shutil.which("birdy") else "bird")
MENTION_RE = re.compile(r"(?<![A-Za-z0-9_])@([A-Za-z0-9_]{1,15})")

# AI-topicality vocabulary. A candidate earns a bonus for each DISTINCT term
# that actually appears in its evidence text, so an account that merely tripped
# a broad keyword search on raw engagement (viral politics, crypto, astrology
# "Gemini") cannot outrank a genuine AI source. Bare "ai"/"ml" are intentionally
# omitted — too noisy to match on their own.
AI_TERM_RE = re.compile(
    r"\b("
    r"llms?|gpt-?[345]\w*|transformers?|inference|fine-?tun\w+|open[- ]?weights?|"
    r"rlhf|rlvr|benchmarks?|sota|multimodal|diffusion|quantiz\w+|pre-?train\w+|"
    r"tokeniz\w+|embeddings?|context window|agentic|coding agent|"
    r"machine learning|deep learning|neural net\w*|foundation model|"
    r"anthropic|openai|deepmind|mistral|qwen|deepseek|llama|claude|gemini"
    r")\b",
    re.IGNORECASE,
)


def _ai_terms(text: str) -> set[str]:
    return {match.lower() for match in AI_TERM_RE.findall(text or "")}


DISCOVERY_QUERIES = [
    '("new model" OR "model release" OR "open weights" OR "AI launch") min_faves:40 -filter:replies lang:en',
    '(OpenAI OR Anthropic OR Claude OR GPT OR Gemini OR Llama OR Mistral OR DeepSeek) min_faves:40 -filter:replies lang:en',
    '("AI agent" OR "coding agent" OR "AI infrastructure" OR "inference") min_faves:40 -filter:replies lang:en',
    '("AI benchmark" OR "machine learning research" OR "state of the art" OR SOTA) min_faves:30 -filter:replies lang:en',
]


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json_atomic(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _extract_json(stdout: str) -> Any:
    out = stdout.strip()
    if not out:
        return []
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        pass
    start = out.find("[")
    end = out.rfind("]")
    if start != -1 and end > start:
        try:
            return json.loads(out[start : end + 1])
        except json.JSONDecodeError:
            return []
    return []


def run_bird_search(query: str, limit: int, timeout: int = 120) -> list[dict[str, Any]]:
    cmd = [BIRD_CMD, "search", query, "-n", str(limit), "--json", "--plain"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        print(f"warning: {BIRD_CMD} search failed: {exc}", file=sys.stderr)
        return []
    if proc.returncode != 0:
        print(f"warning: {BIRD_CMD} rc={proc.returncode}: {proc.stderr.strip()[:240]}", file=sys.stderr)
        return []
    data = _extract_json(proc.stdout)
    return [item for item in data if isinstance(item, dict)] if isinstance(data, list) else []


def current_handles(manifest: dict[str, Any]) -> set[str]:
    return {normalize_handle(entry["handle"]).lower() for _category_id, entry in iter_handle_entries(manifest)}


def _author_username(tweet: dict[str, Any]) -> str | None:
    author = tweet.get("author")
    if isinstance(author, dict):
        username = author.get("username") or author.get("screen_name")
        if username:
            return normalize_handle(str(username))
    for key in ("username", "screen_name", "handle"):
        if tweet.get(key):
            return normalize_handle(str(tweet[key]))
    return None


def _tweet_url(tweet: dict[str, Any], handle: str) -> str | None:
    if isinstance(tweet.get("url"), str) and tweet["url"].startswith(("https://x.com/", "https://twitter.com/")):
        return tweet["url"]
    tid = tweet.get("id") or tweet.get("id_str")
    if tid:
        return f"https://x.com/{handle}/status/{tid}"
    return None


def _count(tweet: dict[str, Any], key: str) -> int:
    try:
        return int(tweet.get(key) or 0)
    except (TypeError, ValueError):
        return 0


def candidates_from_tweets(
    tweets: list[dict[str, Any]],
    monitored_handles: set[str],
    *,
    min_score: float,
    max_candidates: int,
) -> list[dict[str, Any]]:
    by_handle: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "handle": "",
            "tweet_count": 0,
            "likes": 0,
            "retweets": 0,
            "replies": 0,
            "examples": [],
            "source": "author",
            "cited_by": set(),
            "mention_count": 0,
            "citation_examples": [],
            "ai_terms": set(),
        }
    )

    for tweet in tweets:
        url = None
        try:
            handle = _author_username(tweet)
        except ManifestError:
            continue
        if not handle:
            continue
        text = tweet.get("text") or tweet.get("fullText") or ""
        terms = _ai_terms(text)
        if handle.lower() not in monitored_handles:
            bucket = by_handle[handle.lower()]
            bucket["handle"] = handle
            bucket["tweet_count"] += 1
            bucket["likes"] += _count(tweet, "likeCount")
            bucket["retweets"] += _count(tweet, "retweetCount")
            bucket["replies"] += _count(tweet, "replyCount")
            bucket["ai_terms"].update(terms)
            url = _tweet_url(tweet, handle)
            if url and len(bucket["examples"]) < 3:
                bucket["examples"].append(url)
        for mentioned in MENTION_RE.findall(text):
            try:
                mentioned_handle = normalize_handle(mentioned)
            except ManifestError:
                continue
            mentioned_key = mentioned_handle.lower()
            if mentioned_key == handle.lower() or mentioned_key in monitored_handles:
                continue
            mentioned_bucket = by_handle[mentioned_key]
            mentioned_bucket["handle"] = mentioned_handle
            mentioned_bucket["source"] = "mention_graph"
            mentioned_bucket["mention_count"] += 1
            mentioned_bucket["cited_by"].add(handle)
            mentioned_bucket["ai_terms"].update(terms)
            url = url or _tweet_url(tweet, handle)
            if url and len(mentioned_bucket["citation_examples"]) < 3:
                mentioned_bucket["citation_examples"].append(f"cited in: {url}")

    candidates = []
    for bucket in by_handle.values():
        # First-principles scoring. Three bounded signals, so no single one can
        # carry a candidate:
        #   1. Trust-weighted mentions. The strongest discovery signal is being
        #      mentioned by accounts WE ALREADY TRUST (the monitored manifest),
        #      not by whoever happened to trip a broad keyword search. A
        #      mention-graph candidate must have >= 1 monitored citer; unverified
        #      citers (which include crypto/spam rings) add only capped, minor
        #      weight. This is goodtweet's lesson applied to a trusted seed set.
        #   2. AI topicality. A bonus per DISTINCT AI term actually present in
        #      the evidence text, so engagement on an off-topic viral post
        #      (politics, astrology) cannot outrank a genuine AI source.
        #   3. Engagement, logarithmic AND halved, so it nudges, never dominates.
        engagement = bucket["likes"] + (2 * bucket["retweets"]) + bucket["replies"]
        engagement_bonus = min(2.0, math.log10(max(engagement, 1)) / 2.0)
        topicality = float(min(3, len(bucket["ai_terms"])))
        cited_by = sorted(bucket["cited_by"])
        trusted = [handle for handle in cited_by if handle.lower() in monitored_handles]
        unverified = [handle for handle in cited_by if handle.lower() not in monitored_handles]

        if bucket["source"] == "mention_graph":
            # Require a trusted voucher; ignore spam rings of unknown citers.
            if not trusted:
                continue
            mention_score = (3.0 * len(trusted)) + min(1.0, 0.5 * len(unverified))
            score = mention_score + topicality + engagement_bonus
            examples = bucket["citation_examples"]
            extra = f" (+{len(unverified)} unverified mention(s))" if unverified else ""
            reason = (
                f"Mention-graph candidate vouched by {len(trusted)} monitored "
                f"account(s): {', '.join('@' + h for h in trusted[:5])}{extra}. "
                f"Matched {len(bucket['ai_terms'])} AI term(s)."
            )
        else:
            score = bucket["tweet_count"] + topicality + engagement_bonus
            examples = bucket["examples"]
            reason = (
                f"Surfaced {bucket['tweet_count']} time(s) as an author in AI "
                f"discovery searches (engagement {engagement}, "
                f"{len(bucket['ai_terms'])} AI term(s) matched)."
            )
        if score < min_score:
            continue
        candidates.append(
            {
                "action": "add",
                "handle": bucket["handle"],
                "category": "others",
                "score": round(score, 2),
                "reason": reason,
                "evidence": examples,
                "source": bucket["source"],
            }
        )

    candidates.sort(key=lambda item: (-item["score"], item["handle"].lower()))
    return candidates[:max_candidates]


def write_report(path: Path, candidates: list[dict[str, Any]], query_counts: list[tuple[str, int]]) -> None:
    lines = [
        "# Twitter Account Explorer Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Discovery command: `{BIRD_CMD}`",
        "",
        "## Query Coverage",
        "",
    ]
    for query, count in query_counts:
        lines.append(f"- `{query}` -> {count} tweet(s)")
    lines.extend(["", "## Candidate Additions", ""])
    if candidates:
        for item in candidates:
            evidence = ", ".join(item["evidence"]) if item["evidence"] else "no URL evidence"
            lines.append(f"- `@{item['handle']}` score {item['score']}: {item['reason']} Evidence: {evidence}")
    else:
        lines.append("- None")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def discover(args: argparse.Namespace) -> int:
    try:
        manifest = _load_json(args.manifest)
        monitored = current_handles(manifest)
    except (FileNotFoundError, json.JSONDecodeError, ManifestError) as exc:
        print(f"error: cannot load manifest: {exc}", file=sys.stderr)
        return 2

    tweets: list[dict[str, Any]] = []
    query_counts: list[tuple[str, int]] = []
    for query in args.query:
        rows = run_bird_search(query, args.per_query)
        query_counts.append((query, len(rows)))
        tweets.extend(rows)

    candidates = candidates_from_tweets(
        tweets,
        monitored,
        min_score=args.min_score,
        max_candidates=args.max_candidates,
    )
    _write_json_atomic(args.output, candidates)
    write_report(args.report, candidates, query_counts)
    print(f"wrote {len(candidates)} candidate(s) to {args.output}")
    print(f"wrote report to {args.report}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--query", action="append", default=list(DISCOVERY_QUERIES))
    parser.add_argument("--per-query", type=int, default=50)
    parser.add_argument("--min-score", type=float, default=4)
    parser.add_argument("--max-candidates", type=int, default=25)
    return parser


def main(argv: list[str] | None = None) -> int:
    return discover(build_parser().parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
