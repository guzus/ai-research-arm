# Skeptical review of the viral-tweet feature analysis

*Independent stress-test of `analysis.md` / `feature_weights.json`. All numbers below were
recomputed from `research/twitter-viral/viral_tweets.jsonl` (677 tweets) with stdlib-only
Python, using `scripts/tweet_features.extract_features` unchanged. My recomputed global r
matches the report exactly (has_allcaps +0.2352, char_len +0.1488, word_count +0.1465), so
the original pipeline is faithful — the disagreements below are about interpretation and
robustness, not arithmetic.*

## TL;DR

The three "robust" features are **directionally real but weak, and over-attributed to
"emphasis/length as a writing lever."** What they mostly measure is **topic/account type**
(markets, crypto, geopolitics, whale-watching) leaking through form. The biggest unmentioned
problem is a **dataset construction flaw**: there is not a single author who is "all-low,"
every low tweet is from one source (`user-tweets`), and 108 high tweets have no low
counterpart at all. The honest verifier built from this is a faint conformance nudge
(within-author AUC ≈ 0.61), not a like predictor.

---

## Premise 1 — Is ">=100 likes" mostly *who*, not *how*? **Verdict: YES, identity dominates.**

- A predictor using **only author identity** (each tweet scored by its author's
  leave-one-out base rate of being "high") gets **global AUC 0.815**. Content form, by
  contrast, tops out around 0.65–0.68 globally and ~0.61 within author.
- Structural proof the corpus is identity-stratified: of 98 authors, **79 are "all-high,"
  0 are "all-low,"** 19 are dual. So "what makes a low tweet" is *defined entirely inside the
  19 dual authors* — the other 79 accounts only contribute positives.
- Marginal test (within the 19 dual authors, the only place a fair contest exists): author
  base-rate alone scores AUC 0.776; the 3-feature content score scores 0.674 pooled; content
  adds only a small bump on top of identity (0.776 → 0.808 with a tiny content nudge).

**Conclusion:** who tweeted explains the lion's share. The paired ("follower-controlled")
view is the *right* instinct and is the only part worth trusting — but it rests on 19 authors
and, as Premise 5 shows, is statistically fragile.

## Premise 2 — has_allcaps: emphasis or artifact? **Verdict: mostly artifact (tickers/acronyms/topic), not emphasis.**

Top ALL-CAPS tokens by class are damning. In HIGH tweets, of 1,950 all-caps tokens only
**~3% are emphasis words**; the rest are tickers/acronyms/stopwords-in-shouty-text:

- **HIGH top tokens:** AI (157), THE (51), TO (36), WHALE (36), WATCH (34), DARVAS (30),
  IRAN (24), OF (23), BTC (13), GPT (9), NVDA (8)…
- **LOW top tokens:** VS (28), YOY (24), THE (23), RUPEES (22), AI (16), EBITDA (10),
  PROFIT/REVENUE/MARGIN/NET (~8 each)…

This is not "winners shout BREAKING." It is **whale-watching/crypto/geopolitics accounts
(WHALE, DARVAS, IRAN, BTC) landing in HIGH vs earnings-recap accounts (YOY, EBITDA, RUPEES,
MARGIN) landing in LOW.** has_allcaps is largely a proxy for "is this a markets/news account
posting tickers and country codes."

Robustness checks on the emphasis hypothesis:
- Strip known tickers/units/country-codes/stopwords and keep only plausible *emphasis* caps:
  rate is high 0.52 vs low 0.38 — the gap shrinks and the surviving "emphasis" tokens are
  still mostly **topic** words (WATCH, SAYS, UPDATE, DEAL, ETF, DOJ, HORMUZ, PAKISTAN).
- has_allcaps is **not** just a length proxy (corr with char_len only +0.19), so it is a
  semi-independent feature — but its content is topical, not emphatic.

**Implication for the verifier:** do NOT advise "add an emphatic ALL-CAPS word." That would
be cargo-culting a topic signal. At most: "ALL-CAPS appears more in winners, largely because
winners here are markets/news posts with tickers — treat as weak conformance, not a lever."

## Premise 3 — char_len / word_count: one factor, and partly a structure confound. **Verdict: collapse to ONE length factor; treat as real-but-weak.**

- **corr(char_len, word_count) = 0.994.** They are the same axis. Counting both double-weights
  length. Use one (char_len).
- Length does hold within author (char_len paired agreement 0.63, 12/19) — so it's not purely
  a between-author artifact.
- BUT long tweets are structurally different: long tweets are **90% multiline** vs 23% for
  short, and have *fewer* quotes/URLs. So "long" partly means "multiline thread-style post,"
  not just verbose. The lever is closer to "write a structured, multi-line post" than "type
  more characters." Still one factor.

## Premise 4 — Were the near-misses correctly excluded?

| feature | global r | low rate | paired agree | verdict |
|---|--:|--:|--:|---|
| `has_hashtag` | +0.176 | **0.005** | 0.32 (+6/−0) | **Correctly excluded — and it's a source artifact, not author style.** Low tweets are 100% `user-tweets`; high `user-tweets` hashtag rate is 0.109, low is 0.005. The 21× "lift" is almost entirely *search-sourced* high tweets carrying campaign hashtags. Real but not actionable; do not advise "add a hashtag." |
| `has_numbers` | +0.161 | 0.264 | 0.47 (+8/−9) | **Correctly excluded.** Paired sign is a coin flip; numbers track finance accounts (tickers/earnings), which sit on both sides. Not a lever. |
| `has_question` | +0.146 | 0.041 | 0.58 (+11/−2) | **Borderline — the strongest of the rejects.** Sign is consistent (11 of 13 nonzero authors positive); only "agreement 0.58" because 6 authors had zero questions in either bucket (counted as non-agreement). On nonzero authors it's 11/13 ≈ 0.85. **I'd promote this to a weak, low-confidence positive lever** ("a genuine question can help"), clearly below the top 3. |
| `money_or_pct` | +0.141 | 0.119 | 0.42 (+8/−4) | **Correctly excluded.** Same topic confound as numbers; weak paired sign. |
| `has_media` | +0.132 | 0.311 | 0.32 (+6/−7) | **Correctly excluded as actionable.** Paired sign negative-leaning. Folk wisdom says media helps; this data does not support it within author. |
| `has_emoji` | +0.125 | 0.228 | 0.32 (+6/−5) | **Correctly excluded.** Author-style artifact; near-zero paired diff. |

Net: the author was right to kill hashtag/media/emoji/numbers/money. The one I'd reopen is
**has_question** as a tertiary, low-weight positive.

## Premise 5 — Stability of the 3 robust features. **Verdict: fragile; "robust" is too strong a word.**

With 19 dual authors, all three sit at the **same** paired agreement 0.632 (12/19):

- **Leave-one-author-out:** agreement stays in [0.611, 0.667] for all three — no single author
  flips the headline, which is reassuring.
- **Author bootstrap (2,000 resamples):** 95% CI on agreement is **[0.42, 0.84]** for all
  three, and P(agreement > 0.5) is only **0.87–0.89.** So there is a ~11–13% chance the
  "majority of authors agree" claim is just noise. This is *suggestive*, not *robust*.
- **Same-source stress test (the real killer for has_allcaps):** restrict each dual author to
  `user-tweets` only (removing the search-sourced high tweets), and paired agreement drops to
  **has_allcaps 0.50, char_len 0.56, word_count 0.61.** has_allcaps becomes a coin flip once
  you stop mixing X's "Top" search results with timeline tweets. Its 0.63 was partly inflated
  by the 29 search-sourced high tweets (which shout more).

**Conclusion:** length (char_len/word_count) is the most stable of the three. **has_allcaps is
the least stable**, despite having the largest global r — its global r is inflated by
between-author topic differences and by search-vs-timeline source mixing.

## Premise 6 — Does it actually discriminate? **Verdict: weakly. Better than chance, far from a predictor.**

Simplest scorer = z-scored sum of the 3 robust features (all positive direction):

- **Global AUC: 0.681.** On the cleaner same-source subset (`user-tweets` only): **0.654.**
- **Within-author AUC: 0.606** pair-weighted, **0.614** author-averaged (median author 0.65).
- Single-feature global AUCs: char_len 0.638, has_allcaps 0.628, word_count 0.628.
- **It is not uniform across authors.** Within-author AUC ranges from **0.32 (WhaleFactor,
  anti-predictive) to 0.89 (darvasboxtrader)**; 7 of 19 dual authors are *below 0.5* (the score
  ranks their flops above their hits). It works for finance/news/astrology accounts and
  actively misfires for whale-alert and a couple of builder accounts.

A within-author AUC of ~0.61 means: given one of an author's hits and one of their flops, the
score picks the hit ~61% of the time vs 50% by coin flip. Real, small, unreliable per-account.

---

## Corrected final feature list for the verifier

| feature | direction | rough weight | rationale |
|---|---|--:|---|
| `char_len` **(use as the single LENGTH factor; drop word_count, r=0.994 dup)** | longer / more structured | **0.5** | Most stable of the three; holds within author (0.63) and same-source (0.56). Frame as "write a substantive, multi-line post," not "pad characters." |
| `has_allcaps` | weak positive | **0.3** | Keep because it has the largest signal, but **demote** — it's mostly tickers/topic and collapses to 0.50 same-source. Do not turn into "add an emphatic word." |
| `has_question` | weak positive | **0.2** | Promoted from the rejects: consistent paired sign (11/13 nonzero authors). Lowest confidence; a *genuine* question, not a rhetorical tic. |

(word_count removed as a near-duplicate of char_len. has_hashtag/has_media/has_emoji/
has_numbers/money_or_pct stay out — real globally, artifact within author.)

Suggested behavior: a 0–100 *conformance* score, not a like estimate. Expect it to add maybe
~0.05–0.10 AUC over "post like this account usually posts." It should never claim to predict
like counts.

## HONESTY BOX — what the verifier must NOT over-claim

1. **Do not call it a like predictor.** Within-author AUC ≈ 0.61; global "accuracy" is mostly
   the model relearning *which account* tweeted (author-only AUC 0.815).
2. **Do not advise "ADD AN ALL-CAPS WORD."** The all-caps signal is ~97% tickers/acronyms/
   topic (AI, BTC, NVDA, YOY, EBITDA, IRAN) and evaporates to a coin flip (0.50) once you
   compare same-source tweets. It measures "this looks like a markets/news account," not emphasis.
3. **Do not advise "ADD A HASHTAG."** 0% of low tweets had one only because every low tweet
   came from `user-tweets`; the lift is a source artifact, not a writing tactic.
4. **Length is one factor, not two.** char_len and word_count are r=0.994. Reporting both as
   separate wins is double-counting.
5. **The "robust" bar is soft.** Bootstrap 95% CI on the paired-sign agreement is [0.42, 0.84]
   with only 19 authors; ~12% of the time the majority-agreement claim is noise. Say "suggestive
   within-author," not "robust."
6. **It misfires for whole account types.** 7 of 19 dual authors have within-author AUC < 0.5.
   For whale-alert / some builder accounts the score is actively wrong. Don't present a single
   global number as if it generalizes per author.
7. **Selection bias is baked in.** Positives are partly X "Top" search results; negatives are
   only an author's own recent timeline. The corpus answers "does this resemble tweets that got
   surfaced," not "will this get 100 likes."
