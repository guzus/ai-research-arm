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
3. **The most consistent edge is attaching MEDIA — but it's small.** On the
   largest, AI-focused, reach-controlled corpus (3924 tweets, 57 authors), tweets
   with an image/chart/video beat the author's own median a bit more often: **72%
   of over-performers carry media vs 65% of normal, leaning positive for ~74% of
   authors.** It's the single most consistent direction, but the effect shrank as
   the sample grew (lift 1.21 → 1.11) and **no feature clears the robustness bar**.
4. **Wording barely matters; reach + timing + luck dominate.** Out-of-sample
   (leave-one-author-out, 51 authors) a full text model predicts over-performance
   at only **~0.60** within-author — weak but real. Stance, questions, length,
   caps — all ~chance individually.

So the actionable "secret ingredient" is small but real: **post a visual, and
have an audience.** The exact words are mostly noise.

## How we got here

| Round | Question | Data | Result |
|---|---|---|---|
| **1** | What separates a >=100-**raw-like** tweet from a flop? | 677 tweets (search + timelines), mixed topics | Length/ALL-CAPS look like levers but are author/topic artifacts; identity dominates (AUC ~0.82). `score_tweet` validated at AUC ~0.67 for the raw-likes question. |
| **2** | What makes a tweet beat its **own author's median** (reach removed)? | 3924 timeline tweets, 57 AI-focused authors (51 with both classes), pulled via **birdy** account rotation | Within author, **no feature is robust**; `has_media` is the most consistent direction (72% vs 65%, ~74% of authors) but small (lift 1.11). Form/content otherwise ~chance. |
| **exp** | Honest ceiling on text-only prediction? | same, leave-one-author-out CV (51 authors) | Full model LOO within-author **~0.60** (weak but real); in-sample 0.72 was mostly memorizing the author. |

The key move in round 2: **reframe "viral" as over-performance vs the author's
own baseline** — every comparison within one person, so follower count cancels
out — and pull timelines via **birdy** (rotates 3 X accounts), which beat the
rate-limiting that had truncated the first attempt and let the corpus grow ~3×.

> **A note on sample size (the signal is weak enough to be unstable).** Round 2
> was pulled at three sizes as birdy's account pool grew: 562 → 1831 → 3924 tweets
> (18 → 24 → 51 dual authors). The "winning" feature moved each time: at 562, form
> looked to *anti*-generalize (LOO within-author 0.31) — small-sample noise; at
> 1831, `has_media` looked *robust* (lift 1.21, 22/24 authors); by 3924 media's
> effect had shrunk (lift 1.11) and **no feature clears the robustness bar**. What
> *stabilized* is the overall out-of-sample ceiling: LOO within-author ~0.55–0.60.
> Lesson: at this effect size, single-feature claims need many authors before you
> trust them.

## The honest ceiling (leave-one-author-out CV)

A logistic regression cross-validated leave-one-author-out — every tweet scored
by a model that never saw its author (`experiment_cv.md`). Out-of-sample:

| feature set | in-sample AUC | LOO global | LOO within-author |
|---|--:|--:|--:|
| form | 0.67 | 0.58 | 0.55 |
| content | 0.61 | 0.49 | 0.53 |
| all | 0.72 | 0.65 | **0.60** |

The in-sample 0.72 drops to ~0.60 within-author out-of-sample — the gap is how
much the naive fit was memorizing *which account* tweeted. The honest
within-author ceiling for text is **~0.60**: weak but real. No single feature
carries it; it's the combination.

## What over-performs (reach-controlled, `overperformance_analysis.md`)

- **Attach media — the most consistent edge.** `has_media`: 72% of over-performers
  vs 65% of normal, leaning positive for ~74% of authors, lift 1.11. The single
  most consistent direction — but small, and not robust at this sample size. A
  chart/screenshot/demo clip is the least-bad move.
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
- **Still modest N** — 51 authors with both classes; the media edge (lift 1.11)
  is directional, not strong. The most robust finding remains the *negative* one:
  wording barely predicts whether a tweet beats its own author's baseline.

## Files

Round 1: `viral_tweets.jsonl` · `analysis.md` · `analyst_review.md` ·
`verifier_validation.md`. Round 2: `overperformance_tweets.jsonl` ·
`author_baselines.json` · `overperformance_analysis.md` ·
`overperformance_qualitative.md` · `overperformance_weights.json` ·
`experiment_cv.md`. Pipeline + reproduce in `README.md`.
