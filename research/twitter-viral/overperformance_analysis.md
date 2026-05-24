# Does content beat form? (over-performance analysis)

*Generated 2026-05-24T12:38:30.538110+00:00 from `overperformance_tweets.jsonl`.*

- **1831** timeline tweets: **332** over-performers (>=3x the author's median) / **1499** normal, across **24** authors with both classes.
- Label is per-author, so the pooled comparison is already largely reach-controlled. AUC = P(rank an over-performer above a normal tweet).

## Headline: form vs content vs combined

| feature group | global AUC | within-author AUC |
|---|--:|--:|
| form | 0.629 | 0.550 |
| content | 0.601 | 0.586 |
| combined | 0.662 | 0.592 |

**Within-author, the content composite separates over-performers better.** Both are weak — over-performance is mostly not explained by these features, consistent with round 1 (engagement is dominated by reach + luck + timing).

## Robust features (survived the within-author paired check)

- **`has_media`** (form, more) — 73% of over-performers vs 60% of normal, 1.21x; r=+0.102, AUC=0.564, paired agree 92%.

## Full ranking by single-feature AUC

| feature | group | AUC | r | over | normal | lift | paired Δ | agree | robust |
|---|:--|--:|--:|--:|--:|--:|--:|--:|:--:|
| `has_media` | form | 0.564 | +0.102 | 73% | 60% | 1.2x | +0.195 | 92% | ✅ |
| `is_advice` | content | 0.538 | +0.134 | 11% | 4% | 3.1x | +0.039 | 33% |  |
| `starts_caps_word` | form | 0.535 | +0.075 | 21% | 14% | 1.5x | +0.020 | 33% |  |
| `is_thread` | content | 0.534 | +0.136 | 10% | 3% | 3.5x | +0.029 | 21% |  |
| `title_colon` | form | 0.533 | +0.065 | 25% | 18% | 1.4x | -0.016 | 42% |  |
| `number_groups` | form | 0.529 | +0.071 | 3.4 | 2.2 | — | +0.492 | 46% |  |
| `has_numbers` | form | 0.528 | +0.044 | 56% | 51% | 1.1x | +0.084 | 58% |  |
| `negation_count` | content | 0.528 | +0.069 | 1.3 | 0.9 | — | +0.215 | 62% |  |
| `has_allcaps` | form | 0.526 | +0.040 | 60% | 55% | 1.1x | +0.042 | 54% |  |
| `url_count` | form | 0.525 | +0.038 | 0.4 | 0.4 | — | +0.103 | 58% |  |
| `has_url` | form | 0.525 | +0.040 | 40% | 35% | 1.1x | +0.102 | 62% |  |
| `allcaps_words` | form | 0.522 | +0.028 | 2.5 | 2.2 | — | -0.039 | 58% |  |
| `is_news_break` | content | 0.519 | +0.059 | 9% | 6% | 1.7x | +0.027 | 38% |  |
| `is_prediction` | content | 0.517 | +0.047 | 12% | 8% | 1.4x | +0.011 | 50% |  |
| `is_list` | content | 0.517 | +0.089 | 5% | 2% | 3.1x | +0.004 | 17% |  |
| `has_negation` | content | 0.516 | +0.025 | 41% | 38% | 1.1x | +0.023 | 62% |  |
| `is_curiosity_gap` | content | 0.514 | +0.067 | 5% | 2% | 2.3x | +0.007 | 17% |  |
| `char_len` | form | 0.514 | +0.000 | 499.5 | 499.1 | — | +36.433 | 54% |  |
| `is_announcement` | content | 0.514 | +0.037 | 11% | 8% | 1.3x | +0.025 | 33% |  |
| `first_person` | form | 0.511 | +0.018 | 40% | 37% | 1.1x | -0.042 | 46% |  |
| `is_opinion` | content | 0.509 | +0.039 | 5% | 3% | 1.6x | +0.014 | 29% |  |
| `has_hashtag` | form | 0.508 | +0.024 | 8% | 6% | 1.2x | +0.004 | 17% |  |
| `is_stance` | content | 0.508 | +0.032 | 5% | 4% | 1.4x | +0.009 | 29% |  |
| `hashtag_count` | form | 0.508 | +0.005 | 0.1 | 0.1 | — | -0.002 | 42% |  |
| `is_quote` | form | 0.500 | +0.000 | 21% | 21% | 1.0x | -0.030 | 46% |  |
| `money_or_pct` | form | 0.499 | -0.002 | 22% | 22% | 1.0x | +0.026 | 33% |  |
| `starts_with_i` | content | 0.497 | -0.017 | 2% | 2% | 0.7x | -0.001 | 29% |  |
| `is_question_hook` | content | 0.497 | -0.013 | 4% | 4% | 0.8x | -0.013 | 54% |  |
| `is_personal` | content | 0.495 | -0.023 | 2% | 3% | 0.7x | -0.017 | 46% |  |
| `is_gratitude` | content | 0.495 | -0.036 | 0% | 1% | 0.2x | -0.018 | 33% |  |
| `has_superlative` | content | 0.490 | -0.021 | 12% | 14% | 0.9x | -0.009 | 46% |  |
| `superlative_count` | content | 0.490 | -0.021 | 0.1 | 0.2 | — | -0.023 | 54% |  |
| `is_multiline` | form | 0.490 | -0.017 | 69% | 71% | 1.0x | +0.042 | 62% |  |
| `line_count` | form | 0.486 | +0.037 | 5.3 | 4.6 | — | +0.279 | 42% |  |
| `avg_word_len` | form | 0.484 | +0.004 | 4.8 | 4.8 | — | +0.136 | 62% |  |
| `emoji_count` | form | 0.483 | -0.004 | 0.6 | 0.6 | — | +0.021 | 33% |  |
| `has_emoji` | form | 0.482 | -0.030 | 25% | 29% | 0.9x | +0.015 | 46% |  |
| `exclaim_count` | form | 0.479 | -0.058 | 0.0 | 0.1 | — | -0.031 | 46% |  |
| `has_exclaim` | form | 0.479 | -0.064 | 4% | 8% | 0.5x | -0.026 | 46% |  |
| `question_count` | form | 0.475 | -0.043 | 0.1 | 0.2 | — | -0.055 | 62% |  |
| `has_question` | form | 0.475 | -0.059 | 8% | 14% | 0.6x | -0.040 | 50% |  |
| `has_mention` | form | 0.407 | -0.185 | 3% | 22% | 0.1x | -0.025 | 46% |  |
| `mention_count` | form | 0.406 | -0.125 | 0.0 | 0.4 | — | -0.004 | 46% |  |

## Caveats

1. **Small N.** 332 over-performers across 24 authors; rare rhetorical features are noisy. Treat as directional.
2. **Heuristic content detectors.** Keyword/structure based — they under-detect (see `overperformance_qualitative.md` for what they miss).
3. **Population is not pure AI.** Authors span markets/crypto/astrology/news; conclusions are about *this mix*, not AI Twitter specifically.
4. **Over-performance ≠ likes.** A small account's over-performer may have few absolute likes. This measures relative pop, which is the writer-actionable part.
5. **Composite AUCs are in-sample.** Each composite takes its feature signs from the global r on the *same* rows it scores, so the content/combined numbers are optimistic. On a held-out 50/50 split the content composite within-author is ~0.53 (not ~0.60); form stays sub-chance (~0.41). The direction (content > form) survives ~18/20 splits, but the *gap* is widest exactly at the 3x cutoff.
6. **No single feature is a reliable lever.** Even `is_stance` (best by pooled lift, ~1.9x) is ~chance within author (AUC ~0.51). Read this analysis for the **negative** result — the text barely predicts over-performance — not for a lever.