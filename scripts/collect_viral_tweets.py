#!/usr/bin/env python3
"""Collect viral (>=100-like) AI/tech tweets from the last 7 days plus
author-controlled low-engagement baselines, and persist them to
``research/twitter-viral/`` as JSONL for downstream analysis.

Why author-controlled negatives
--------------------------------
Tweets that already have >=100 likes are all "positives". If we only look at
positives we can describe what viral tweets look like, but we cannot say what
*distinguishes* them from flops -- and the single biggest confounder of raw
like counts is author follower count, not content. So we also pull the SAME
authors' other recent tweets and label each high/low by like count. Holding the
author ~constant controls for follower count, so the high-vs-low difference
isolates *content/form* effects -- the part a writer can actually act on.

Network boundary
----------------
This is the only networked script in the set: it shells out to ``birdy`` when
present (a multi-account proxy that rotates X accounts to cut rate-limit risk),
else plain ``bird`` (override via ``ARA_BIRD_CMD``). All calls degrade gracefully
to empty results, per repo convention (``--json`` + fallback). Offline analysis
lives in ``analyze_viral_tweets.py``; the verifier (``tweet_virality_verifier.py``)
is pure and never touches the network.

Usage
-----
    python scripts/collect_viral_tweets.py            # defaults (last 7 days)
    python scripts/collect_viral_tweets.py --min-faves 200 --max-authors 30
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "research" / "twitter-viral"

# Prefer birdy (rotates across multiple X accounts -> ~Nx the rate-limit
# headroom) when it's on PATH; fall back to plain bird. Override with ARA_BIRD_CMD.
BIRD_CMD = os.environ.get("ARA_BIRD_CMD") or ("birdy" if shutil.which("birdy") else "bird")

# AI/tech topic queries. Deliberately broad: we want variance in *how* viral
# AI-adjacent tweets are written, not a narrow keyword slice. Each is formatted
# with --min-faves / --since at runtime.
POSITIVE_QUERIES = [
    '(AI OR LLM OR "language model" OR AGI) min_faves:{min_faves} since:{since} -filter:replies lang:en',
    '(GPT OR Claude OR OpenAI OR Anthropic OR Gemini OR DeepSeek) min_faves:{min_faves} since:{since} -filter:replies lang:en',
    '("machine learning" OR "deep learning" OR "AI agent" OR robotics OR "neural network") '
    'min_faves:{min_faves} since:{since} -filter:replies lang:en',
]

HIGH_LIKE_THRESHOLD = 100


def _extract_json(stdout: str):
    """Parse bird's stdout into a Python object, tolerating stray prefix/suffix
    lines some subcommands print around the JSON payload."""
    out = stdout.strip()
    if not out:
        return None
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        pass
    # Fall back to the outermost array/object span.
    for opener, closer in (("[", "]"), ("{", "}")):
        start = out.find(opener)
        end = out.rfind(closer)
        if start != -1 and end > start:
            try:
                return json.loads(out[start : end + 1])
            except json.JSONDecodeError:
                continue
    return None


def run_bird(args: list[str], timeout: int = 90, full: bool = False) -> list[dict]:
    """Call ``bird <args> --json[-full] --plain`` and return a list of tweet dicts.

    ``full=True`` uses ``--json-full`` so each tweet carries a ``_raw`` field with
    the full GraphQL node — needed for ``bookmark_count`` / ``views`` which the
    flattened ``--json`` output omits. Returns ``[]`` on any failure (missing
    binary, non-zero exit, bad JSON, expired cookies) so callers degrade safely.
    """
    cmd = [BIRD_CMD, *args, "--json-full" if full else "--json", "--plain"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
        print(f"  ! {BIRD_CMD} error: {exc}", file=sys.stderr)
        return []
    if proc.returncode != 0:
        print(f"  ! bird rc={proc.returncode}: {proc.stderr.strip()[:200]}", file=sys.stderr)
        return []
    data = _extract_json(proc.stdout)
    if isinstance(data, list):
        return [t for t in data if isinstance(t, dict)]
    if isinstance(data, dict):
        for key in ("tweets", "data", "results"):
            if isinstance(data.get(key), list):
                return [t for t in data[key] if isinstance(t, dict)]
        return [data]
    return []


def parse_created_at(value: str):
    """Twitter format: 'Sun May 24 03:20:08 +0000 2026' -> aware datetime."""
    try:
        return datetime.strptime(value, "%a %b %d %H:%M:%S %z %Y")
    except (ValueError, TypeError):
        return None


def _bookmark_from_raw(raw) -> "int | None":
    """Top-level tweet's bookmark_count from a --json-full ``_raw`` blob.

    The tweet's own count is at ``_raw.legacy.bookmark_count``; quoted/retweeted
    tweets nest theirs deeper, so prefer ``legacy`` then fall back to the
    shallowest ``bookmark_count`` found anywhere.
    """
    if not isinstance(raw, dict):
        return None
    leg = raw.get("legacy")
    if isinstance(leg, dict) and leg.get("bookmark_count") is not None:
        try:
            return int(leg["bookmark_count"])
        except (TypeError, ValueError):
            pass
    best = None  # (depth, value)
    stack = [(raw, 0)]
    while stack:
        obj, depth = stack.pop()
        if isinstance(obj, dict):
            bc = obj.get("bookmark_count")
            if bc is not None and (best is None or depth < best[0]):
                try:
                    best = (depth, int(bc))
                except (TypeError, ValueError):
                    pass
            for v in obj.values():
                stack.append((v, depth + 1))
        elif isinstance(obj, list):
            for v in obj:
                stack.append((v, depth + 1))
    return best[1] if best else None


def _views_from_raw(raw) -> "int | None":
    """Impression count from ``_raw.views.count`` (string -> int), if present."""
    if not isinstance(raw, dict):
        return None
    views = raw.get("views")
    if isinstance(views, dict):
        try:
            return int(views.get("count"))
        except (TypeError, ValueError):
            return None
    return None


def flatten(tweet: dict, label: str | None = None) -> dict | None:
    """Project a bird tweet object onto the flat record we persist.

    When the tweet came from ``--json-full`` (carries ``_raw``), also captures
    ``bookmark_count`` and ``views_count``; both are ``None`` for plain ``--json``.
    The bulky ``_raw`` itself is never persisted.
    """
    tid = str(tweet.get("id") or "")
    text = tweet.get("text") or ""
    if not tid or not text:
        return None
    # Normalize Unicode line separators (U+2028/U+2029) to "\n". json.dumps
    # leaves them raw in the JSONL otherwise, and naive consumers that use
    # str.splitlines() would silently splinter the record onto multiple lines.
    text = text.translate({0x2028: "\n", 0x2029: "\n"})
    created = parse_created_at(tweet.get("createdAt", ""))
    like = int(tweet.get("likeCount") or 0)
    author = tweet.get("author") or {}
    media = [m for m in (tweet.get("media") or []) if isinstance(m, dict)]
    username = author.get("username") or "i"
    return {
        "id": tid,
        "url": f"https://x.com/{username}/status/{tid}",
        "text": text,
        "created_at": created.astimezone(timezone.utc).isoformat() if created else None,
        "like_count": like,
        "retweet_count": int(tweet.get("retweetCount") or 0),
        "reply_count": int(tweet.get("replyCount") or 0),
        "author_username": author.get("username"),
        "author_name": author.get("name"),
        "author_id": str(tweet.get("authorId") or ""),
        "has_media": bool(media),
        "media_types": sorted({m.get("type") for m in media if m.get("type")}),
        "is_quote": bool(tweet.get("quotedTweet")),
        "bookmark_count": _bookmark_from_raw(tweet.get("_raw")),
        "views_count": _views_from_raw(tweet.get("_raw")),
        "label": label if label is not None else ("high" if like >= HIGH_LIKE_THRESHOLD else "low"),
    }


def collect(args) -> None:
    since = args.since
    seen: dict[str, dict] = {}

    # 1) Positives: viral AI/tech tweets from the search index.
    for query_tmpl in POSITIVE_QUERIES:
        query = query_tmpl.format(min_faves=args.min_faves, since=since)
        print(f"[+] search: {query}")
        rows = run_bird(["search", query, "--all", "--max-pages", str(args.max_pages)], timeout=180)
        added = 0
        for row in rows:
            rec = flatten(row, label="high")
            if rec and rec["id"] not in seen:
                rec["source"] = "search"
                seen[rec["id"]] = rec
                added += 1
        print(f"    +{added} (running unique total {len(seen)})")
        time.sleep(args.sleep)

    positives = list(seen.values())
    print(f"[=] {len(positives)} positive (>= {args.min_faves} likes) tweets\n")

    # 2) Author-controlled negatives: same authors' other recent tweets.
    author_counts: dict[str, int] = {}
    for rec in positives:
        user = rec.get("author_username")
        if user:
            author_counts[user] = author_counts.get(user, 0) + 1
    # Most-prolific viral authors first -> richest high/low contrast per author.
    authors = [u for u, _ in sorted(author_counts.items(), key=lambda kv: -kv[1])][: args.max_authors]
    cutoff = datetime.now(timezone.utc) - timedelta(days=args.neg_window_days)
    print(f"[+] pulling timelines for {len(authors)} authors "
          f"(window {args.neg_window_days}d) for baselines")

    base_added = 0
    for i, user in enumerate(authors, 1):
        rows = run_bird(["user-tweets", user, "-n", str(args.per_author)], timeout=90)
        kept = 0
        for row in rows:
            rec = flatten(row)  # auto-label by 100-like threshold
            if not rec or rec["id"] in seen:
                continue
            if rec["text"].startswith("RT @"):  # retweets aren't the author's writing
                continue
            if rec["created_at"]:
                when = datetime.fromisoformat(rec["created_at"])
                if when < cutoff:
                    continue
            rec["source"] = "user-tweets"
            seen[rec["id"]] = rec
            kept += 1
            base_added += 1
        print(f"  [{i:>2}/{len(authors)}] @{user:<20} +{kept}")
        time.sleep(args.sleep)

    records = list(seen.values())
    highs = [r for r in records if r["label"] == "high"]
    lows = [r for r in records if r["label"] == "low"]
    print(f"\n[=] total {len(records)} tweets: {len(highs)} high / {len(lows)} low "
          f"(+{base_added} from timelines)")

    # 3) Persist atomically (temp file in same dir -> os.replace).
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    data_path = OUT_DIR / "viral_tweets.jsonl"
    _write_jsonl(data_path, records)

    meta = {
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "min_faves": args.min_faves,
        "since": since,
        "neg_window_days": args.neg_window_days,
        "high_like_threshold": HIGH_LIKE_THRESHOLD,
        "queries": [q.format(min_faves=args.min_faves, since=since) for q in POSITIVE_QUERIES],
        "counts": {
            "total": len(records),
            "high": len(highs),
            "low": len(lows),
            "from_search": sum(1 for r in records if r.get("source") == "search"),
            "from_user_tweets": sum(1 for r in records if r.get("source") == "user-tweets"),
            "unique_authors": len({r["author_username"] for r in records if r.get("author_username")}),
        },
    }
    _write_json(OUT_DIR / "meta.json", meta)
    print(f"[ok] wrote {data_path.relative_to(REPO_ROOT)} and meta.json")
    print(json.dumps(meta["counts"], indent=2))


def _write_jsonl(path: Path, records: list[dict]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    os.replace(tmp, path)


def _write_json(path: Path, obj) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def main() -> None:
    default_since = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min-faves", type=int, default=HIGH_LIKE_THRESHOLD,
                    help="minimum likes for the positive (viral) set")
    ap.add_argument("--since", default=default_since,
                    help="positives lower date bound YYYY-MM-DD (default: 7 days ago)")
    ap.add_argument("--max-pages", type=int, default=3,
                    help="pages per positive search query (~20 tweets/page)")
    ap.add_argument("--max-authors", type=int, default=25,
                    help="number of viral authors to pull baselines from")
    ap.add_argument("--per-author", type=int, default=40,
                    help="tweets to fetch per author timeline")
    ap.add_argument("--neg-window-days", type=int, default=7,
                    help="recency window (days) for the baseline/negative set")
    ap.add_argument("--sleep", type=float, default=1.2,
                    help="seconds to sleep between bird calls")
    collect(ap.parse_args())


if __name__ == "__main__":
    main()
