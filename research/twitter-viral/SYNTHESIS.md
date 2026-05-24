# What actually makes a tweet pop — two rounds, one honest answer

This is the capstone for the `twitter-viral` study. Read this first.

## TL;DR

We asked "what's the secret ingredient of a >100-like tweet?" twice, and the
second, more rigorous pass **overturned the first**.

1. **Raw likes are mostly reach.** Who tweets predicts high/low at **AUC ~0.82**;
   the entire text (form *and* content) tops out around **0.67**. The biggest
   "secret ingredient" is having followers.
2. **Form is a mirage.** Round 1 said "longer tweets with an ALL-CAPS word."
   Controlling for the author kills it: form has **no within-author signal**
   (composite AUC ~0.45 — its global correlation is a between-author artifact).
   Pooled, over-performers are even *shorter* (178 vs 206 chars) and use *less*
   ALL-CAPS (46% vs 57%); within author it's just noise. ALL-CAPS was ~97%
   tickers/acronyms (AI, BTC, NVDA), not emphasis.
3. **Content beats form, but only as a weak composite.** Within an author's own
   feed, content separates hits from normal tweets at **~0.53 held-out** (0.60
   in-sample) vs **~0.45 for form**. But **no single feature is a reliable
   lever**: even taking a first-person stance — the best by pooled lift (~1.9×)
   and the recurring move in the qualitative read — is ~chance *within* author.
4. **Mostly it isn't the text.** Reach, timing, and luck dominate. The single
   biggest over-performer in the data was a news headline that popped for two
   unrelated accounts at once — the news cycle, not the phrasing.

So the honest "secret ingredient" is: **say something only you would say, take a
side, and have an audience.** Everything else is rounding error.

## How we got here

| Round | Question | Method | Result |
|---|---|---|---|
| **1** | What separates a >=100-**raw-like** tweet from a flop? | 677 tweets (search + author timelines); global correlation + within-author paired check | Length looked like the one semi-stable lever; ALL-CAPS topped raw correlation but was a topic artifact. Verifier AUC ~0.67 — but raw likes ≈ reach. |
| **2** | What makes a tweet beat its **own author's median** (reach removed)? | 562 timeline tweets (uniform source), 18 authors with both classes; form **+ content/rhetorical** features; AUC + paired check + a qualitative read of the actual texts | Form within-author AUC **0.45** (no signal); content **~0.53 held-out**; **no single feature beats chance within author**. It's mostly not the text. |

The key methodological move in round 2: **reframe "viral" as over-performance vs
the author's own baseline.** That removes the follower confound *by construction*
(every comparison is within one person) and, by using only timeline tweets, also
kills the "Top"-search selection bias that inflated round 1.

## What over-performs (reach-controlled, all weak — see `overperformance_analysis.md`)

Directional levers (none robust; treat as faint nudges):

1. **First-person stance / correcting a take** — `is_stance`, the best content
   tendency by pooled lift (~1.9×) and the recurring qualitative move, but
   **~chance within author** (AUC ~0.51 after removing a regex artifact). *"I
   think the AI-detection panic is wrong — the real reason students get flagged
   is broken tools"* beat its author's diary tweets by 269×.
2. Question hook, news-break framing, curiosity gap, self-contained list/data —
   weaker and **topic-shaped** (markets / news / astrology), unlikely to transfer.

Anti-levers (do **not** help you beat your own baseline; they mark big or topical
accounts): **length, ALL-CAPS, media, emoji, $/%, hashtags.** These have no
within-author signal — their global correlation is a between-author artifact.

The qualitative read (`overperformance_qualitative.md`) adds color: the moves that
pop are *stake-planting opinion in your own voice*, *flattering identity call-outs*
(astrology-only), and *underdog-beats-the-giant* framing — but it stresses the
corpus is **not** AI Twitter (only ~15-20% of over-performers are AI-native) and
that one viral thread inflates a cluster of replies.

## The verifier (`scripts/tweet_virality_verifier.py`)

Two functions for the two questions, both honest about being faint:

- `score_tweet(text, ...)` — **raw-likes conformance** (round 1), validated
  AUC ~0.67. A high score mostly means "you write like a high-follower account."
- `assess_overperformance(text, ...)` — **round-2 guidance**: surfaces the stance
  lever, refuses to reward length/caps, and states plainly that the text explains
  little.

```bash
python3 scripts/tweet_virality_verifier.py "draft" --overperformance   # round-2 guidance
python3 scripts/tweet_virality_verifier.py "draft"                      # raw-likes score
```

## What this is NOT

- **Not an AI-virality study.** The corpus drifted into astrology, crypto/markets,
  politics, and news-wires; conclusions describe opinion/commentary Twitter, not
  AI content specifically.
- **Not causal, and not reach-aware.** Only `like_count` is used (no impressions,
  bookmarks, reposts). Timing and news cycles are uncontrolled.
- **Small N / nothing robust.** 18 dual authors, 81 over-performers; every lever
  is a hypothesis, not a law. The most defensible finding is the *negative* one:
  surface form does not make your tweet beat your baseline.

## Files

`viral_tweets.jsonl` · `analysis.md` · `analyst_review.md` · `verifier_validation.md`
(round 1) — `overperformance_tweets.jsonl` · `author_baselines.json` ·
`overperformance_analysis.md` · `overperformance_qualitative.md` ·
`overperformance_weights.json` (round 2). Pipeline + reproduce steps in `README.md`.
