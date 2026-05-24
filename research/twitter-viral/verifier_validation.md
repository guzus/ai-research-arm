# Independent validation of `tweet_virality_verifier.py` (rewrite)

> **Historical note:** validations below were run against the round-1 (677) and
> the original 562-tweet round-2 cuts. Round 2 later grew to 3924 tweets / 57
> authors (via birdy), which corrected some numbers (form does not
> anti-generalize; no feature is robust — media is only the most consistent, small
> direction; LOO within-author ceiling ~0.60). `SYNTHESIS.md` is the current
> source of truth.

*Fresh-eyes review. Every number below was recomputed from
`research/twitter-viral/viral_tweets.jsonl` by importing the FINAL
`score_tweet` and implementing AUC as the Mann-Whitney rank statistic
(stdlib only, ties = 0.5). Verdict: **SHIP**.*

## 1. Empirical discrimination (the key check)

Scored all 677 tweets (484 high / 193 low), passing `has_media`/`is_quote`
from each record into `score_tweet`.

| Metric | AUC |
|---|--:|
| **Global** (score vs high/low) | **0.6683** |
| Global, brute-force O(n²) cross-check | 0.6683 (identical) |
| **Within-author, pair-weighted** (19 dual authors) | **0.6366** |
| Within-author, author-averaged | 0.6388 |
| Within-author, median author | 0.6691 |

- HIGH ranks **above** LOW everywhere. No anti-correlation. Global > 0.5,
  within-author > 0.5. **No correctness bug.**
- Matches `analyst_review.md` (global ~0.66–0.68, within-author ~0.61).
  Within-author is slightly higher than the review's 0.606 because the
  shipped scorer adds `has_question` (a lever the review promoted from the
  rejects); direction and magnitude are consistent.
- Per-author spread, as the review warned, is wide: 5 of 19 dual authors
  are anti-predictive (`shawtyastrology` 0.351, `sniffalt` 0.393,
  `Kadimu174Ai` 0.394, `REDBOXINDIA` 0.401, `stallseok` 0.450). The
  disclaimer's "misfire for some accounts" claim is therefore honest.
  (The review's "7 of 19 < 0.5" used a caps+length-only score; adding
  `has_question` flips two borderline authors above 0.5. Not a defect.)

## 2. Code review

- **No network, no data dependency.** Verifier imports only
  `argparse`/`json`/`sys`/`typing` + `tweet_features`. No
  `requests`/`urllib`/`socket`/`open()`. The only mentions of
  `viral_tweets.jsonl` / `feature_weights.json` are in docstrings.
- **CI-safe:** ran the test suite with BOTH data files renamed away →
  **17 passed**. No hard dependency on the data.
- **`_length_strength`** guards divide-by-zero (`if high > low`), and the
  constants satisfy `high > low` on both axes. Output clamped to [0,1];
  extreme inputs (−100, 1e9) map to 0.0 / 1.0 correctly.
- **Score clamped to [0,100]:** empty → 0.0; all-levers + huge length →
  100.0 (verdict `strong`).
- **Feature logic fully delegated** to `tweet_features.extract_features`
  — no regex/`isupper`/`findall` re-implemented in the verifier. Cannot
  drift from the analyzer.
- **No dead references** to removed symbols. Dropped features
  (`has_hashtag`/`has_media`/`has_emoji`/`has_numbers`/`money_or_pct`)
  appear only in the WHY-THESE-WEIGHTS comment, not in code.
- **argparse wiring** correct: `text` positional, `--media`/`--quote`/`--json`
  flags map straight into `score_tweet`. CLI JSON + human smoke tests pass.

## 3. Honesty / anti-cargo-cult (verified by running code)

- **(a) Never advises caps/hashtags.** 10 caps-less drafts → 0 suggestions
  containing `caps`/`all-caps`/`capital`/`uppercase`/`hashtag`/`#`. 4
  caps-present drafts → still 0 caps advice. The only suggestions are the
  length lever and an optional genuine question.
- **(b)** `length` (50) is the strict single max weight (> `has_allcaps`
  30 > `has_question` 20; sum = 100).
- **(c)** Disclaimer present, says "NOT a like prediction," frames as a
  "writing nudge, not a forecast," and contains no over-claim
  ("guarantee" / "will go viral" / "predicts likes").
- **Tests enforce these, non-vacuously.** `_mentions_caps_advice`
  genuinely catches "add ALL-CAPS" / "capitalize" / "use caps" and passes
  clean advice. `test_dropped_artifacts_are_not_scored` asserts the factor
  set is *exactly* `{length, has_allcaps, has_question}`.
  `test_allcaps_scored_but_never_suggested` proves caps raises the score
  yet never appears in advice.

## 4. Test runs

```
$ python3 -m pytest scripts/test_tweet_virality_verifier.py -q
17 passed in 0.10s

$ python3 -m pytest scripts/ -q
185 passed, 6 skipped in 10.05s
```

(The 6 skips are `test_research_search.py` live smoke tests gated behind
`RESEARCH_SEARCH_LIVE_TESTS=1` — unrelated to the verifier.)

## Findings

- No blockers.
- Nit (report-only, not fixed): docstring/comment cite within-author
  AUC ~0.61, the shipped scorer measures 0.637 because `has_question`
  was added after the review's 3-feature number. Harmless under-claim.
- Nit: dataset is 484 high / 193 low — the module docstring's "484 high /
  193 low" is correct; just noting it for the record.

**VERDICT: SHIP.**

---

# Round 2 — over-performance validation (independent recompute)

*Fresh-eyes review of the over-performance reframe. All numbers below were
recomputed from `overperformance_tweets.jsonl` by importing ONLY the feature
extractors (`extract_features` / `extract_content_features`) and reimplementing
the loader (file-iteration), AUC (brute pairwise Mann-Whitney, ties = 0.5),
composites, and within-author aggregation from scratch.*
*Verdict: **SHIP with caveats** — the negative headline is solid; two specific
numbers are optimistic/inflated and should be softened.*

## 1. Composite AUCs — match exactly

| group | global AUC (mine / report) | within-author (mine / report / claim) |
|---|---|---|
| form | 0.625 / 0.625 | **0.450** / 0.450 / ~0.45 ✅ |
| content | 0.593 / 0.593 | **0.599** / 0.599 / ~0.60 ✅ |
| combined | 0.662 / 0.662 | **0.556** / 0.556 / ~0.55 ✅ |

Form within-author < 0.5 ✅; content > form within-author ✅. Analyzer is
deterministic and reproduces its committed `overperformance_weights.json`
byte-for-byte. **Claim 1 confirmed.**

## 2. Sensitivity — the headline DIRECTION survives; the MAGNITUDE is cutoff-flattered

Re-derived the over-performer label from `like_count` vs per-author median at
several ratios/floors and recomputed within-author composite AUCs:

| ratio | floor | n_over | dual | form_w | content_w | combined_w | content−form |
|--:|--:|--:|--:|--:|--:|--:|--:|
| 2.0 | 5 | 137 | 20 | 0.546 | 0.592 | 0.621 | +0.046 |
| 3.0 | 5 | 81 | 18 | 0.450 | 0.599 | 0.556 | +0.149 |
| 4.0 | 5 | 57 | 15 | 0.469 | 0.584 | 0.547 | +0.115 |
| 5.0 | 5 | 41 | 11 | 0.456 | 0.558 | 0.547 | +0.102 |

- **"Form ≈ chance within-author" is robust** — form_w ∈ [0.449, 0.546], at or
  below 0.5 at every threshold/floor. ✅
- **"Content beats form within-author" holds in DIRECTION at all 8 settings.** ✅
- **But the gap is widest exactly at the chosen 3× cutoff** (+0.149) and shrinks
  to +0.046 at 2×. The "0.45 vs 0.60" framing is real but flattered by the 3×
  threshold. Globally, form *beats* content at every threshold (0.60–0.69 vs
  0.56–0.65) — "content wins" is a within-author-only statement (report is
  careful about this).

## 3. Out-of-sample sign selection — `content ~0.60` does NOT survive a held-out split

The composites take each feature's direction sign from the **global Pearson r on
the same rows** they're evaluated on (in-sample sign + normalization). Refitting
signs/normalization on a held-out half and scoring within-author on the other
half (20 random 50/50 splits):

| group | in-sample within-AUC | out-of-sample mean | min / max |
|---|--:|--:|--:|
| form | 0.450 | **0.413** | 0.347 / 0.480 |
| content | 0.599 | **0.530** | 0.406 / 0.588 |

- Form stays sub-chance out-of-sample (mean 0.413) → the negative form finding is
  if anything **understated**. ✅
- Content's true out-of-sample within-author AUC is **~0.53, not ~0.60** — the
  headline "0.60" carries ≈0.07 of in-sample optimism. content > form still holds
  in **18/20** splits, so the *direction* is real; the *number* is inflated.

## 4. `is_stance` back-test — best lever claim is partly a regex artifact

| metric | as shipped | after removing bare-"actually" false positives |
|---|--:|--:|
| fires on | 55/562 | 40/562 |
| rate over / normal | 17.3% / 8.5% | 11.1% / 6.4% |
| lift | **2.03×** | 1.72× |
| global r | **+0.104** | +0.064 |
| global AUC | 0.544 | 0.523 |
| within-author AUC | **0.526** | 0.508 (≈ chance) |
| paired sign agreement | 33% (6 pos / 8 neg / 4 zero of 18) | — |

- As shipped, `is_stance` matches the report (r +0.10, lift 2.0×). ✅ But the
  `_STANCE_CORRECTION` regex alternation includes a bare `\bactually\b`, which
  matches "actually" as a mid-sentence intensifier. **15 of 55 firings (27%) are
  this false-positive class** (crypto promos, tarot "actually FEEL your
  emotions", "how LLMs actually work") — not stances or corrections.
- Deglitched, lift falls to 1.72×, r to +0.064 (no longer clearly the top
  content feature — comparable to `has_negation` r +0.074), within-author AUC to
  chance. **`is_stance`'s "single best lever" status is inflated by the regex.**
- Within-author paired agreement is only **33%** (the report's table value), and
  8 of 18 dual authors point *negative* — so even as shipped this is a coin flip
  within author, not a robust lever. The "not topic-confounded" framing is
  charitable: it also fires on crypto/tarot accounts via "actually".

## 5. "Shorter + less ALL-CAPS reverses" (claim 3) — true POOLED, backwards WITHIN-author

| feature | over (pooled) | normal (pooled) | within-author single-feat AUC | paired direction |
|---|--:|--:|--:|---|
| char_len | 178.1 | 206.3 | 0.529 | +20.8 (10 authors over>norm / 8 <) |
| word_count | 27.7 | 31.8 | 0.530 | — |
| has_allcaps | 0.457 | 0.574 | 0.546 | +0.019 (10 over>norm / 7 <) |

- **Pooled:** over-performers are shorter and use less caps. ✅ (matches SYNTHESIS).
- **Within author the sign FLIPS:** paired diffs are *positive* (over-performers
  are slightly *longer* and use slightly *more* caps than the same author's
  normal tweets), and within-author single-feature AUCs are all 0.53–0.55 (same
  side, weakly). The "shorter/less caps" reversal is a **between-author
  confound** (verbose, caps-heavy markets/news accounts have higher medians →
  fewer over-performers), not a within-author writing effect.
- ⚠️ This makes the verifier's `anti_levers_note` ("within author, length and
  ALL-CAPS even point the wrong way") and SYNTHESIS bullet 2 ("Within author,
  length and caps point the *wrong* way") **factually backwards**. The defensible
  statement is "**no within-author signal**" (composite 0.45, char_len AUC
  0.500), not "wrong way."

## 6. Code review / CI-safety

- **CI-safe:** renamed `overperformance_tweets.jsonl`, `author_baselines.json`,
  `viral_tweets.jsonl`, `feature_weights.json` away → `pytest
  test_tweet_virality_verifier.py` = **24 passed**. No network/data dependency.
- `tweet_virality_verifier.py` / `tweet_content.py` / `tweet_features.py` import
  no `socket`/`urllib`/`requests`/`subprocess` (verifier's `subprocess` is only
  in the test file, for CLI smoke). Pure.
- **`assess_overperformance` does NOT reward form:** long shouty draft → 0
  levers; `anti_levers` correctly lists length/ALL-CAPS/media/emoji/$%/hashtags;
  stance present → suggested-out. ✅
- **Divide-by-zero:** `enrich` uses `base = max(median(likes), floor)`, floor
  default 5 → safe even if all likes 0. (Only `--floor 0` + all-zero author
  would divide by zero; not a default path.)
- `extract_content_features(None)` safe (`text = text or ""`; `stripped[:2]` on
  "" is fine). Determinism: `assess_overperformance`/`score_tweet` idempotent.
- **DATA BUG (latent, NIT):** ~10 tarot-account records contain a raw U+2028
  LINE SEPARATOR in `text`. `json.dumps(ensure_ascii=False)` does NOT escape
  U+2028/U+2029, so it sits raw in the JSONL. The analyzer is **unaffected**
  (`for line in fh:` splits only on `\n`), but any consumer using
  `.splitlines()`/`read_text().splitlines()` (e.g. a naive reader or the
  dashboard prebuild) silently splinters those records and drops ~10 tweets.
  Root cause is upstream text capture (round-1 `collect_viral_tweets.flatten`),
  not round-2 code; `enrich._write_jsonl` faithfully round-trips it. Fix when
  touched: `text.replace(" "," ").replace(" "," ")` at capture, or
  `json.dumps(...).encode().decode("unicode_escape")`-style sanitation.

## 7. Test runs

```
$ python3 -m pytest scripts/test_tweet_virality_verifier.py -q   # data files renamed away
24 passed in 0.16s

$ python3 -m pytest scripts/ -q
192 passed, 6 skipped in 10.09s
```
(6 skips = `test_research_search.py` live smoke tests behind `RESEARCH_SEARCH_LIVE_TESTS=1`.)

## Findings (round 2)

- **No blockers.** The load-bearing NEGATIVE conclusion — *surface form has no
  within-author signal; the text explains little; nothing is robust* — is
  confirmed and, for form, understated.
- **Medium 1 (report-only):** `content within-author ~0.60` is an in-sample
  figure; true out-of-sample ≈ **0.53**. Soften the number or add the
  in-sample-optimism caveat. Direction (content > form) is robust.
- **Medium 2 (report-only, design-level → not fixed):** `is_stance` is inflated
  ~27% by a bare-`actually` regex false positive (`_STANCE_CORRECTION` in
  `tweet_content.py`). Deglitched lift 1.72× / r +0.064 / within-AUC ≈ chance —
  no longer clearly the top lever. Tightening the regex would desync the
  committed analysis numbers + verifier notes, so reported rather than fixed.
- **Medium 3 (report-only):** "within author, length/caps point the *wrong* way"
  (verifier `anti_levers_note` + SYNTHESIS bullet 2) is backwards — within author
  they're weakly *neutral-to-positive*. Reword to "no within-author signal."
- **Nit:** `tweet_content.py` docstring claims `is_stance` "AUC 0.57, lift 2.3x,
  50% within-author paired agreement"; the committed report and my recompute say
  **0.544 / 2.03× / 33%**. Stale docstring numbers; align them.
- **Nit (data):** latent U+2028 JSONL landmine (see §6).

**VERDICT: SHIP with caveats.** The verifier ships correctly (does not reward
form, honest disclaimers, CI-safe, 24/24 + 192/6). The analysis's negative
headline holds. Fix the three "medium" wording/number over-claims and the stale
docstring before treating any positive lever (esp. `is_stance`) as established.
