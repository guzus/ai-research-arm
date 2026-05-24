# Does content beat form? (over-performance analysis)

*Generated 2026-05-24T14:10:41.620732+00:00 from `bookmark_tweets.jsonl`.*

- **3644** timeline tweets: **663** over-performers (>=3x the author's median) / **2981** normal, across **46** authors with both classes.
- Label is per-author, so the pooled comparison is already largely reach-controlled. AUC = P(rank an over-performer above a normal tweet).

## Headline: form vs content vs combined

| feature group | global AUC | within-author AUC |
|---|--:|--:|
| form | 0.625 | 0.633 |
| content | 0.568 | 0.570 |
| combined | 0.632 | 0.639 |

**Within-author, the form composite separates over-performers at AUC 0.63, with 5 feature(s) surviving the paired check** — a real, if modest, content signal. Confirm out-of-sample with the companion leave-one-author-out experiment.

## Robust features (survived the within-author paired check)

- **`char_len`** (form, more) — over avg 502.3 vs 359.4; r=+0.085, AUC=0.584, paired agree 83%.
- **`allcaps_words`** (form, more) — over avg 3.8 vs 2.4; r=+0.087, AUC=0.576, paired agree 63%.
- **`has_allcaps`** (form, more) — 64% of over-performers vs 50% of normal, 1.28x; r=+0.108, AUC=0.570, paired agree 70%.
- **`has_numbers`** (form, more) — 61% of over-performers vs 47% of normal, 1.29x; r=+0.106, AUC=0.569, paired agree 76%.
- **`has_media`** (form, more) — 71% of over-performers vs 60% of normal, 1.18x; r=+0.085, AUC=0.554, paired agree 76%.

## Full ranking by single-feature AUC

| feature | group | AUC | r | over | normal | lift | paired Δ | agree | robust |
|---|:--|--:|--:|--:|--:|--:|--:|--:|:--:|
| `char_len` | form | 0.584 | +0.085 | 502.3 | 359.4 | — | +143.670 | 83% | ✅ |
| `allcaps_words` | form | 0.576 | +0.087 | 3.8 | 2.4 | — | +1.348 | 63% | ✅ |
| `has_allcaps` | form | 0.570 | +0.108 | 64% | 50% | 1.3x | +0.136 | 70% | ✅ |
| `number_groups` | form | 0.569 | +0.062 | 2.7 | 1.9 | — | +0.950 | 59% |  |
| `has_numbers` | form | 0.569 | +0.106 | 61% | 47% | 1.3x | +0.111 | 76% | ✅ |
| `has_media` | form | 0.554 | +0.085 | 71% | 60% | 1.2x | +0.146 | 76% | ✅ |
| `line_count` | form | 0.545 | +0.070 | 7.2 | 5.2 | — | +2.203 | 61% |  |
| `starts_caps_word` | form | 0.544 | +0.087 | 26% | 17% | 1.5x | +0.028 | 24% |  |
| `avg_word_len` | form | 0.539 | +0.063 | 4.8 | 4.6 | — | +0.215 | 63% |  |
| `is_multiline` | form | 0.532 | +0.051 | 69% | 62% | 1.1x | +0.054 | 67% |  |
| `is_curiosity_gap` | content | 0.525 | +0.119 | 7% | 2% | 3.8x | +0.056 | 28% |  |
| `negation_count` | content | 0.519 | +0.071 | 0.7 | 0.5 | — | +0.245 | 54% |  |
| `is_advice` | content | 0.518 | +0.083 | 6% | 2% | 2.6x | +0.023 | 26% |  |
| `has_negation` | content | 0.515 | +0.026 | 28% | 26% | 1.1x | +0.059 | 59% |  |
| `is_personal` | content | 0.511 | +0.056 | 4% | 2% | 2.1x | +0.016 | 28% |  |
| `is_announcement` | content | 0.510 | +0.037 | 6% | 4% | 1.5x | +0.019 | 41% |  |
| `is_prediction` | content | 0.507 | +0.025 | 6% | 4% | 1.3x | +0.012 | 30% |  |
| `is_list` | content | 0.506 | +0.039 | 2% | 1% | 2.0x | +0.003 | 11% |  |
| `is_question_hook` | content | 0.504 | +0.014 | 6% | 5% | 1.2x | +0.005 | 33% |  |
| `is_news_break` | content | 0.504 | +0.012 | 6% | 6% | 1.1x | +0.014 | 24% |  |
| `money_or_pct` | form | 0.504 | +0.007 | 20% | 20% | 1.0x | +0.037 | 44% |  |
| `is_opinion` | content | 0.503 | +0.013 | 3% | 2% | 1.2x | +0.006 | 22% |  |
| `is_stance` | content | 0.503 | +0.013 | 3% | 2% | 1.2x | +0.003 | 22% |  |
| `is_gratitude` | content | 0.502 | +0.011 | 2% | 2% | 1.2x | -0.003 | 33% |  |
| `superlative_count` | content | 0.500 | +0.017 | 0.1 | 0.1 | — | +0.026 | 41% |  |
| `has_superlative` | content | 0.500 | +0.000 | 11% | 10% | 1.0x | +0.025 | 44% |  |
| `is_thread` | content | 0.498 | -0.006 | 5% | 6% | 0.9x | -0.016 | 26% |  |
| `starts_with_i` | content | 0.497 | -0.015 | 2% | 3% | 0.8x | -0.006 | 50% |  |
| `has_url` | form | 0.496 | -0.005 | 47% | 48% | 1.0x | +0.026 | 56% |  |
| `url_count` | form | 0.495 | +0.009 | 0.6 | 0.6 | — | -0.012 | 41% |  |
| `has_exclaim` | form | 0.495 | -0.014 | 8% | 9% | 0.9x | -0.006 | 52% |  |
| `exclaim_count` | form | 0.494 | -0.014 | 0.1 | 0.2 | — | -0.015 | 54% |  |
| `hashtag_count` | form | 0.493 | -0.018 | 0.1 | 0.2 | — | -0.015 | 39% |  |
| `has_hashtag` | form | 0.493 | -0.024 | 4% | 6% | 0.8x | +0.004 | 9% |  |
| `title_colon` | form | 0.492 | -0.018 | 14% | 16% | 0.9x | -0.019 | 50% |  |
| `first_person` | form | 0.490 | -0.016 | 31% | 33% | 0.9x | -0.034 | 56% |  |
| `question_count` | form | 0.490 | +0.022 | 0.2 | 0.2 | — | +0.042 | 39% |  |
| `has_question` | form | 0.490 | -0.024 | 11% | 13% | 0.8x | +0.003 | 46% |  |
| `is_quote` | form | 0.489 | -0.022 | 17% | 19% | 0.9x | -0.022 | 48% |  |
| `has_emoji` | form | 0.472 | -0.047 | 25% | 30% | 0.8x | +0.004 | 39% |  |
| `mention_count` | form | 0.470 | -0.042 | 0.1 | 0.2 | — | -0.020 | 46% |  |
| `has_mention` | form | 0.469 | -0.068 | 10% | 16% | 0.6x | -0.007 | 39% |  |
| `emoji_count` | form | 0.466 | -0.051 | 0.5 | 0.8 | — | -0.178 | 48% |  |

## Caveats

1. **Small N.** 663 over-performers across 46 authors; rare rhetorical features are noisy. Treat as directional.
2. **Heuristic content detectors.** Keyword/structure based — they under-detect (see `overperformance_qualitative.md` for what they miss).
3. **Population is not pure AI.** Authors span markets/crypto/astrology/news; conclusions are about *this mix*, not AI Twitter specifically.
4. **Over-performance ≠ likes.** A small account's over-performer may have few absolute likes. This measures relative pop, which is the writer-actionable part.
5. **Composite AUCs are in-sample.** Each composite takes its feature signs from the global r on the *same* rows it scores, so they are optimistic. Trust the companion leave-one-author-out experiment for the honest out-of-sample number.
6. **A high single-feature AUC is not a reliable lever** until it also survives the within-author paired check across many authors. Read this for the **negative** result too — whether the text predicts the metric at all.