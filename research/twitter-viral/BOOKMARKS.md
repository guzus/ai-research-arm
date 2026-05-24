# What predicts bookmarks (saves) — and why it beats likes

The likes study (`SYNTHESIS.md`) concluded the *text barely matters* — engagement
is mostly reach + timing + luck. Bookmarks are different. **Re-running the exact
same machinery on bookmark counts gives the first genuinely positive result: the
wording/format of a tweet really does predict whether it gets saved.**

## TL;DR

People **like** for social reasons (who you are, the moment) but **bookmark**
deliberately — "I'll want this later." So saves reward *useful, reference-grade*
content, and that's legible in the text.

Same method as the likes study — over-performance vs each author's own median,
controlled for reach, validated leave-one-author-out (a model that never sees the
author). Head-to-head, out-of-sample, within-author (the honest writer number):

| | **likes** | **bookmarks** |
|---|--:|--:|
| LOO within-author AUC (form) | 0.55 (≈ chance) | **0.62** |
| LOO within-author AUC (all features) | 0.60 | 0.61 |
| robust features (survive within-author check) | **0** | **5** |
| what they are | — | length, numbers, media, caps |
| within-author vs global | global higher (reach) | **within higher (content)** |

Two things make the bookmark result real where likes wasn't:

1. **Form holds out-of-sample** (0.62, didn't collapse like likes' 0.55), and
   **form ≥ all-features** (by a hair, ~0.008) — content/rhetorical moves add
   essentially nothing on top of form for saves.
2. **Within-author AUC (0.62) > global (0.59).** The signal lives *inside* an
   author's own feed (which of my tweets gets saved), not across accounts — i.e.
   it's genuine content, not "this is a big account." Likes were the opposite.

## What gets saved: information density

The 5 features that survive the within-author paired check (46 authors), all
pointing the same way — over-performers have *more* of each:

| feature | over-performers | normal | within-author agreement |
|---|--:|--:|--:|
| `char_len` (length) | avg 502 chars | 359 | 83% |
| `has_numbers` (data/stats) | 61% | 47% | 76% |
| `has_media` (image/chart/video) | 71% | 60% | 76% |
| `has_allcaps` (acronyms / hype caps) | 64% | 50% | 70% |
| `allcaps_words` | avg 3.8 | 2.4 | 63% |

Read together, these are one thing: **substantive, data-rich, visual posts** —
the stuff you save to refer back to. A chart with numbers and a real explanation
gets bookmarked; a one-liner gets liked and scrolled past.

Notably, the *rhetorical* features that folk wisdom loves — questions, hot-takes,
curiosity gaps, "stance" — do **not** survive (content composite ~0.55, ≈ chance).
Saves are about substance, not hooks.

## Actionable take

- **To get saved:** write a substantive, multi-line post with concrete numbers/
  data and a visual (chart / screenshot / diagram). That's reference content.
- **To get liked:** mostly, have followers. Wording barely moves likes.
- The bookmark lever is **real but modest** (AUC ~0.62, not 0.9) — it shifts the
  odds, it doesn't guarantee a save. Reach and timing still matter.

**Score a draft:** `python3 scripts/tweet_virality_verifier.py "your draft" --saveability [--media]`
— the `assess_saveability()` verifier scores info density (length / numbers / media;
caps are scored but never advised), and empirically separates bookmark over-performers
at AUC ~0.60 on this corpus. Unlike the likes scorers, it's backed by a real signal.

## Honest caveats

- **`has_allcaps` is the least-clean of the five.** The ALL-CAPS tokens are a
  mix of acronyms/tickers (API, LLM, $NVDA — legit info-density) *and* all-caps
  hype/shouting openers ("BREAKING", "INSTEAD OF WATCHING NETFLIX TONIGHT") — so
  it's part substance, part attention-grab, and topic-tinged. **Length, numbers,
  and media are the clean levers — lead with those.**
- **Bookmarks are sparse** (median 1 per tweet vs 108 likes), so the
  over-performance ratio is noisier for low-baseline authors (floor=2 mitigates).
- **Correlation, not causation.** "Add a number" won't *cause* saves; substantive
  data-rich posts simply get saved more. Don't cargo-cult the features.
- **Population** is AI-focused but spans markets/news/crypto (53 authors); the
  *direction* is robust, the exact magnitudes are corpus-specific.
- Only `bookmark_count` is modeled; views are captured too (`bookmarks_per_1k_views`)
  for a future "save-rate per impression" cut.

## Reproduce

```bash
python3 scripts/enrich_bookmarks.py --discover            # -> bookmark_tweets.jsonl (birdy, --json-full)
python3 scripts/analyze_overperformance.py \
  --data research/twitter-viral/bookmark_tweets.jsonl --label bookmark_overperformer \
  --out-md research/twitter-viral/bookmark_analysis.md \
  --out-weights research/twitter-viral/bookmark_weights.json
python3 scripts/experiment_overperf_cv.py \
  --data research/twitter-viral/bookmark_tweets.jsonl --label bookmark_overperformer \
  --out-md research/twitter-viral/bookmark_experiment_cv.md
```

Files: `bookmark_tweets.jsonl` (3644 tweets, 53 authors, + `views_count`,
`save_rate`, `bookmarks_per_1k_views`) · `bookmark_baselines.json` ·
`bookmark_analysis.md` · `bookmark_weights.json` · `bookmark_experiment_cv.md`.
