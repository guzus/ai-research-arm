#!/usr/bin/env python3
"""Reframe "viral" as OVER-PERFORMANCE relative to each author's own baseline.

Raw ">=100 likes" is dominated by follower count — author identity alone
predicts high/low at AUC ~0.82 (see analyst_review.md). To ask the question a
writer actually cares about — *"which of MY tweets pop, and why?"* — we take
each author's recent TIMELINE tweets (a **uniform source**, so no X "Top"-search
selection bias), compute their median likes, and label every tweet by how far
it beats that median:

    overperformance_ratio = like_count / max(author_median_likes, floor)
    overperformer         = ratio >= --overperform-ratio (default 3x)

This removes reach *by construction* (every comparison is within one author) and
fixes the same-source critique. A 40-like tweet from a small account can be an
over-performer; a 200-like tweet from a huge account can be a flop.

Data source: by default reuses the timeline tweets already persisted in
``viral_tweets.jsonl`` (``source == "user-tweets"``) — no network, so it can't
be rate-limited. Pass ``--refresh`` to pull fresh, deeper timelines via bird
(``collect_viral_tweets.run_bird``/``flatten``, which degrade to [] on failure).
Output feeds ``analyze_overperformance.py``.
"""
from __future__ import annotations

import argparse
import json
import os
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import median

from collect_viral_tweets import OUT_DIR, REPO_ROOT, flatten, run_bird

SRC = OUT_DIR / "viral_tweets.jsonl"
OUT_TWEETS = OUT_DIR / "overperformance_tweets.jsonl"
OUT_BASE = OUT_DIR / "author_baselines.json"


def load_existing_timeline() -> dict[str, list[dict]]:
    """Group already-persisted timeline tweets (uniform source) by author."""
    by_author: dict[str, list[dict]] = defaultdict(list)
    if not SRC.exists():
        return by_author
    with open(SRC, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if r.get("source") != "user-tweets":
                continue  # exclude X "Top"-search hits -> uniform source
            user = r.get("author_username")
            if user:
                by_author[user].append(r)
    return by_author


def fetch_timelines(authors: list[str], per_author: int, window_days: int,
                    sleep: float) -> dict[str, list[dict]]:
    """Pull fresh, deeper timelines via bird (rate-limit prone)."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=window_days)
    by_author: dict[str, list[dict]] = {}
    for i, user in enumerate(authors, 1):
        rows = run_bird(["user-tweets", user, "-n", str(per_author)], timeout=90)
        recs: list[dict] = []
        for row in rows:
            rec = flatten(row)
            if not rec or rec["text"].startswith("RT @"):
                continue
            if rec["created_at"] and datetime.fromisoformat(rec["created_at"]) < cutoff:
                continue
            rec["source"] = "user-tweets"
            recs.append(rec)
        by_author[user] = recs
        print(f"  [{i:>3}/{len(authors)}] @{user:<22} {len(recs):>3} original tweets")
        time.sleep(sleep)
    return by_author


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
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--refresh", action="store_true",
                    help="pull fresh timelines via bird instead of reusing persisted data")
    ap.add_argument("--per-author", type=int, default=80, help="(--refresh) tweets per timeline")
    ap.add_argument("--window-days", type=int, default=30, help="(--refresh) recency window")
    ap.add_argument("--min-tweets", type=int, default=8,
                    help="min original tweets to trust an author's median")
    ap.add_argument("--floor", type=float, default=5.0,
                    help="floor on the median so tiny baselines don't explode the ratio")
    ap.add_argument("--overperform-ratio", type=float, default=3.0,
                    help="ratio over author median to count as an over-performer")
    ap.add_argument("--max-authors", type=int, default=200)
    ap.add_argument("--sleep", type=float, default=1.5)
    args = ap.parse_args()

    if args.refresh:
        authors = sorted(load_existing_timeline().keys())[: args.max_authors]
        print(f"[+] refreshing {len(authors)} authors via bird")
        by_author = fetch_timelines(authors, args.per_author, args.window_days, args.sleep)
    else:
        by_author = load_existing_timeline()
        print(f"[+] using persisted timeline tweets for {len(by_author)} authors (no network)")

    baselines: dict[str, dict] = {}
    enriched: list[dict] = []
    seen: set[str] = set()
    for user, recs in by_author.items():
        if len(recs) < args.min_tweets:
            continue  # too few tweets for a trustworthy median
        likes = [r["like_count"] for r in recs]
        med = median(likes)
        base = max(med, args.floor)
        baselines[user] = {
            "median_likes": med, "n_tweets": len(recs),
            "max_likes": max(likes), "min_likes": min(likes),
        }
        for r in recs:
            if r["id"] in seen:
                continue
            seen.add(r["id"])
            ratio = r["like_count"] / base
            rec = dict(r)
            rec["author_median_likes"] = med
            rec["overperformance_ratio"] = round(ratio, 3)
            rec["overperformer"] = ratio >= args.overperform_ratio
            enriched.append(rec)

    over = sum(1 for r in enriched if r["overperformer"])
    # Authors that have BOTH an over-performer and a non-over-performer.
    by_lbl: dict[str, set] = defaultdict(set)
    for r in enriched:
        by_lbl[r["author_username"]].add(r["overperformer"])
    dual = sum(1 for s in by_lbl.values() if len(s) == 2)

    print(f"\n[=] {len(enriched)} tweets from {len(baselines)} authors with reliable baselines")
    print(f"    {over} over-performers (>= {args.overperform_ratio}x median) / "
          f"{len(enriched) - over} normal; {dual} authors have both classes")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    _write_jsonl(OUT_TWEETS, enriched)
    _write_json(OUT_BASE, {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "bird-refresh" if args.refresh else "persisted-timeline",
        "params": {
            "min_tweets": args.min_tweets, "floor": args.floor,
            "overperform_ratio": args.overperform_ratio,
            "window_days": args.window_days if args.refresh else 7,
        },
        "n_authors": len(baselines), "n_tweets": len(enriched),
        "n_overperformers": over, "n_dual_authors": dual,
        "authors": baselines,
    })
    print(f"[ok] wrote {OUT_TWEETS.relative_to(REPO_ROOT)} and {OUT_BASE.name}")


if __name__ == "__main__":
    main()
