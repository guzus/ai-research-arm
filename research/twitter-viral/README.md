# twitter-viral — what makes a tweet clear 100 likes

A one-off study (not part of the auto-pipeline) of what drives tweet engagement,
plus a verifier that scores a draft. **Start with [`SYNTHESIS.md`](SYNTHESIS.md)** —
it ties the two research rounds together and states the honest conclusion (round 2
overturned round 1: raw likes are mostly reach; surface form does *not* help a
tweet beat its own author's baseline).

> **Not deployed to the dashboard.** `dashboard/scripts/prebuild.mjs` only
> copies `twitter/`, `models/`, `front-page/`, `digest/`, `audio/`,
> `generative/`. This directory is intentionally not in that list, so the raw
> tweet dump never ships to ara.guzus.xyz.

## Files

| File | Round | What it is |
|---|:--:|---|
| `SYNTHESIS.md` | both | **Entry point.** The whole story + honest conclusion. |
| `viral_tweets.jsonl` | 1 | 677 tweets. `label` = `high` (>=100 likes) / `low`. `source` = `search` (viral hits) / `user-tweets` (baseline). |
| `meta.json` | 1 | Collection params + counts. |
| `analysis.md` / `feature_weights.json` | 1 | High-vs-low form-feature comparison (global r + within-author paired Δ). |
| `analyst_review.md` | 1 | Independent stress-test — overturns the naive "ALL-CAPS" conclusion. |
| `verifier_validation.md` | 1 | Independent AUC check of the verifier. |
| `overperformance_tweets.jsonl` | 2 | 562 timeline tweets labeled by `overperformance_ratio` (likes ÷ author median) + `overperformer`. |
| `author_baselines.json` | 2 | Per-author median likes + counts (the reach control). |
| `overperformance_analysis.md` / `overperformance_weights.json` | 2 | Form-vs-content comparison vs over-performance (the reach-controlled question). |
| `overperformance_qualitative.md` | 2 | Qualitative read of the actual top/bottom over-performer texts + codeable detectors. |
| `experiment_cv.md` | 2 | Leave-one-author-out CV — the honest out-of-sample ceiling (form *anti*-generalizes; text barely predicts). |

## The headline result

Short version (full story in `SYNTHESIS.md`):

- **Raw likes are mostly reach.** Author identity alone predicts high/low at
  AUC ~0.82; the whole text tops out ~0.67.
- **Round 1 (raw likes)** said "longer + an ALL-CAPS word." **Round 2
  (over-performance vs the author's own median) overturned it:** over-performers
  are *shorter* and use *less* ALL-CAPS. Form has ~no within-author signal
  (AUC 0.45). ALL-CAPS was ~97% tickers/acronyms, not emphasis.
- **Content beats form, weakly** (within-author ~0.53 held-out vs ~0.45 for
  form). **No single feature is a reliable lever** — even a first-person stance
  is ~chance within author. Reach, timing and luck dominate.

## Reproduce / refresh

```bash
# Round 1 — raw-likes study (networked: needs bird CLI + valid X cookies)
python3 scripts/collect_viral_tweets.py        # -> viral_tweets.jsonl
python3 scripts/analyze_viral_tweets.py        # -> analysis.md + feature_weights.json (offline)

# Round 2 — reach-controlled over-performance study
python3 scripts/enrich_overperformance.py      # -> overperformance_tweets.jsonl (reuses round-1 timelines; --refresh to re-pull)
python3 scripts/analyze_overperformance.py     # -> overperformance_analysis.md (offline; form vs content)
python3 scripts/experiment_overperf_cv.py      # -> experiment_cv.md (leave-one-author-out CV; honest ceiling)

# Score / assess a draft (pure, offline)
python3 scripts/tweet_virality_verifier.py "your draft" [--media] [--quote]   # raw-likes conformance
python3 scripts/tweet_virality_verifier.py "your draft" --overperformance     # round-2 guidance
```

Feature extraction is shared (`scripts/tweet_features.py` for form,
`scripts/tweet_content.py` for rhetorical) so analyzers and verifier can't drift.
Tests: `python3 -m pytest scripts/test_tweet_virality_verifier.py -q`.
