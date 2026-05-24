#!/usr/bin/env python3
"""Collect a bookmark-labeled corpus: what makes a tweet get SAVED.

Bookmarks ("save for later") are a stronger *this is useful* signal than likes,
so plausibly more content-driven. Same reach-controlled design as the likes
study: pull each author's recent timeline via birdy with ``--json-full`` (to get
``bookmark_count`` + ``views``), compute their median bookmarks, and label each
tweet by how far it beats that median. Also records:

- ``save_rate`` = bookmarks / (likes + 1)  — "saveworthiness" vs raw popularity
- ``bookmarks_per_1k_views``               — save rate per impression (purest,
  reach-normalized — only where views are exposed)

Output feeds the generalized ``analyze_overperformance.py`` /
``experiment_overperf_cv.py`` via ``--label bookmark_overperformer``.
"""
from __future__ import annotations

import argparse
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from statistics import median

from collect_viral_tweets import BIRD_CMD, OUT_DIR, REPO_ROOT, flatten, run_bird
from enrich_overperformance import _write_json, _write_jsonl, discover_authors, load_existing_timeline

OUT_TWEETS = OUT_DIR / "bookmark_tweets.jsonl"
OUT_BASE = OUT_DIR / "bookmark_baselines.json"


def fetch_timelines_full(authors, per_author, window_days, sleep):
    """Pull timelines via ``--json-full`` so each tweet carries bookmark_count."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=window_days)
    by_author = {}
    for i, user in enumerate(authors, 1):
        rows = run_bird(["user-tweets", user, "-n", str(per_author)], timeout=150, full=True)
        recs = []
        for row in rows:
            rec = flatten(row)
            if not rec or rec["text"].startswith("RT @"):
                continue
            if rec.get("bookmark_count") is None:  # need the metric
                continue
            if rec["created_at"] and datetime.fromisoformat(rec["created_at"]) < cutoff:
                continue
            rec["source"] = "user-tweets"
            recs.append(rec)
        by_author[user] = recs
        print(f"  [{i:>3}/{len(authors)}] @{user:<22} {len(recs):>3} tweets w/ bookmarks")
        time.sleep(sleep)
    return by_author


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--discover", action="store_true", help="discover AI authors via search")
    ap.add_argument("--discover-pages", type=int, default=4)
    ap.add_argument("--per-author", type=int, default=100)
    ap.add_argument("--window-days", type=int, default=30)
    ap.add_argument("--min-tweets", type=int, default=8,
                    help="min tweets w/ bookmarks to trust an author's median")
    ap.add_argument("--floor", type=float, default=2.0,
                    help="floor on the median (bookmarks are sparser than likes)")
    ap.add_argument("--overperform-ratio", type=float, default=3.0)
    ap.add_argument("--max-authors", type=int, default=90)
    ap.add_argument("--sleep", type=float, default=0.8)
    args = ap.parse_args()

    authors = set(load_existing_timeline().keys())
    if args.discover:
        since = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")
        found = discover_authors(since, args.discover_pages)
        print(f"[+] discovered {len(found)} authors via search ({len(found - authors)} new)")
        authors |= found
    authors = sorted(authors)[: args.max_authors]
    print(f"[+] pulling {len(authors)} timelines via {BIRD_CMD} (--json-full for bookmarks)")
    by_author = fetch_timelines_full(authors, args.per_author, args.window_days, args.sleep)

    baselines = {}
    enriched = []
    seen = set()
    for user, recs in by_author.items():
        if len(recs) < args.min_tweets:
            continue
        bookmarks = [r["bookmark_count"] for r in recs]
        med = median(bookmarks)
        base = max(med, args.floor)
        baselines[user] = {
            "median_bookmarks": med, "n_tweets": len(recs), "max_bookmarks": max(bookmarks),
            "median_likes": median([r["like_count"] for r in recs]),
        }
        for r in recs:
            if r["id"] in seen:
                continue
            seen.add(r["id"])
            ratio = r["bookmark_count"] / base
            rec = dict(r)
            rec["author_median_bookmarks"] = med
            rec["bookmark_ratio"] = round(ratio, 3)
            rec["bookmark_overperformer"] = ratio >= args.overperform_ratio
            rec["save_rate"] = round(r["bookmark_count"] / (r["like_count"] + 1), 4)
            rec["bookmarks_per_1k_views"] = (
                round(1000 * r["bookmark_count"] / r["views_count"], 3) if r.get("views_count") else None
            )
            enriched.append(rec)

    over = sum(1 for r in enriched if r["bookmark_overperformer"])
    by_lbl = defaultdict(set)
    for r in enriched:
        by_lbl[r["author_username"]].add(r["bookmark_overperformer"])
    dual = sum(1 for s in by_lbl.values() if len(s) == 2)
    with_views = sum(1 for r in enriched if r.get("views_count"))

    print(f"\n[=] {len(enriched)} tweets / {len(baselines)} authors with reliable baselines")
    print(f"    {over} bookmark-overperformers (>= {args.overperform_ratio}x median); "
          f"{dual} dual authors; views on {with_views}/{len(enriched)}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    _write_jsonl(OUT_TWEETS, enriched)
    _write_json(OUT_BASE, {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "metric": "bookmarks",
        "params": {"per_author": args.per_author, "window_days": args.window_days,
                   "min_tweets": args.min_tweets, "floor": args.floor,
                   "overperform_ratio": args.overperform_ratio},
        "n_authors": len(baselines), "n_tweets": len(enriched),
        "n_overperformers": over, "n_dual_authors": dual, "n_with_views": with_views,
        "authors": baselines,
    })
    print(f"[ok] wrote {OUT_TWEETS.relative_to(REPO_ROOT)} and {OUT_BASE.name}")


if __name__ == "__main__":
    main()
