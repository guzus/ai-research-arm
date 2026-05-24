# What actually makes a tweet pop — the honest answer

Capstone for the `twitter-viral` study. Read this first.

## TL;DR

We asked "what's the secret ingredient of a tweet that pops?" across two rounds
and a cross-validated experiment. The honest answer:

1. **Raw likes are mostly reach.** Who tweets predicts a >=100-like tweet at
   **AUC ~0.82**; the entire text tops out far lower. The biggest "ingredient"
   is having followers.
2. **Round 1's text levers were artifacts.** "Longer + an ALL-CAPS word" did not
   survive controlling for the author — ALL-CAPS was ~97% tickers/acronyms (AI,
   BTC, NVDA), not emphasis, and length tracked *which account* tweeted.
3. **The one lever that holds up is attaching MEDIA.** On a larger, AI-focused,
   reach-controlled corpus (1831 tweets, 28 authors), tweets with an
   image/chart/video beat the author's own median far more often: **73% of
   over-performers carry media vs 60% of normal tweets, and this holds for 22 of
   24 authors.** Modest (lift ~1.2×) but the only feature that clears the bar.
4. **Wording barely matters; reach + timing + luck dominate.** Out-of-sample
   (leave-one-author-out) a full text model predicts over-performance at only
   ~0.54 within-author. Stance, questions, length, caps — all ~chance.

So the actionable "secret ingredient" is small but real: **post a visual, and
have an audience.** The exact words are mostly noise.

## How we got here

| Round | Question | Data | Result |
|---|---|---|---|
| **1** | What separates a >=100-**raw-like** tweet from a flop? | 677 tweets (search + timelines), mixed topics | Length/ALL-CAPS look like levers but are author/topic artifacts; identity dominates (AUC ~0.82). `score_tweet` validated at AUC ~0.67 for the raw-likes question. |
| **2** | What makes a tweet beat its **own author's median** (reach removed)? | 1831 timeline tweets, 28 AI-focused authors (24 with both classes), pulled via **birdy** account rotation | Within author, **`has_media` is the one robust lever** (73% vs 60%, 22/24 authors). Text form/content otherwise ~chance. |
| **exp** | Honest ceiling on text-only prediction? | same, leave-one-author-out CV | Full model LOO within-author **~0.54** (weak but real); in-sample 0.75 was mostly memorizing the author. |

The key move in round 2: **reframe "viral" as over-performance vs the author's
own baseline** — every comparison within one person, so follower count cancels
out — and pull timelines via **birdy** (rotates 3 X accounts), which beat the
rate-limiting that had truncated the first attempt and let the corpus grow ~3×.

> **A note on sample size.** An earlier 562-tweet cut of round 2 suggested form
> features *anti*-generalized (LOO within-author 0.31) and that "nothing in the
> text works." Tripling the data with birdy showed that was small-sample noise:
> form is simply ~chance within author (0.51), and `has_media` emerges as a real,
> if modest, lever. More data corrected an over-dramatic conclusion — the reason
> it was worth re-pulling.

## The honest ceiling (leave-one-author-out CV)

A logistic regression cross-validated leave-one-author-out — every tweet scored
by a model that never saw its author (`experiment_cv.md`). Out-of-sample:

| feature set | in-sample AUC | LOO global | LOO within-author |
|---|--:|--:|--:|
| form | 0.71 | 0.58 | 0.51 |
| content | 0.62 | 0.52 | 0.55 |
| all | 0.75 | 0.63 | **0.54** |

The in-sample 0.75 collapses to ~chance within-author out-of-sample — it was
mostly memorizing *which account* tweeted. The honest within-author ceiling for
text is **~0.54**: weak but real, and much of it is the media signal.

## What over-performs (reach-controlled, `overperformance_analysis.md`)

- **Attach media — the one robust lever.** `has_media`: 73% of over-performers
  vs 60% of normal tweets, agrees for 22/24 authors, lift 1.21. A chart,
  screenshot, or short demo clip is the most reliable (still modest) move.
- Everything else is ~chance within author: length, ALL-CAPS, questions, lists,
  news framing, and **stance** (round 2's earlier "best content lever" — lift
  ~1.5× pooled but AUC ~0.51 within author; it did not survive the bigger sample).

The qualitative read (`overperformance_qualitative.md`) still describes the
recurring *flavor* of hits — stake-planting opinion, identity call-outs,
underdog-beats-giant — but those are weak/topic-shaped quantitatively; media is
the only one that holds up.

## The verifier (`scripts/tweet_virality_verifier.py`)

- `score_tweet(text, ...)` — **raw-likes conformance** (round 1), AUC ~0.67. A
  high score mostly means "you write like a high-follower account."
- `assess_overperformance(text, has_media=..., ...)` — **round-2 guidance**: leads
  with the media lever, refuses to credit length/caps/stance, and states the
  ceiling honestly.

```bash
python3 scripts/tweet_virality_verifier.py "draft" --overperformance --media
python3 scripts/tweet_virality_verifier.py "draft"            # raw-likes score
```

## What this is NOT

- **Not an impressions/reach model** — only `like_count` is used; bookmarks,
  reposts, and quote-driven exposure are invisible (so the media effect on
  bookmark-heavy "data drop" tweets is probably *under*-counted).
- **Not causal, and not timing-aware** — news cycles and "tweeted into a hot
  thread" are uncontrolled. The biggest single over-performer was a news headline
  that popped for two accounts at once.
- **Still small-N** — 24 authors with both classes; treat the media lift (1.21)
  as directional. The most robust finding remains the *negative* one: wording
  barely predicts whether a tweet beats its own author's baseline.

## Files

Round 1: `viral_tweets.jsonl` · `analysis.md` · `analyst_review.md` ·
`verifier_validation.md`. Round 2: `overperformance_tweets.jsonl` ·
`author_baselines.json` · `overperformance_analysis.md` ·
`overperformance_qualitative.md` · `overperformance_weights.json` ·
`experiment_cv.md`. Pipeline + reproduce in `README.md`.
