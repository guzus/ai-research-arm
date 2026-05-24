# Does content beat form? (over-performance analysis)

*Generated 2026-05-24T14:10:40.675972+00:00 from `overperformance_tweets.jsonl`.*

- **3924** timeline tweets: **571** over-performers (>=3x the author's median) / **3353** normal, across **51** authors with both classes.
- Label is per-author, so the pooled comparison is already largely reach-controlled. AUC = P(rank an over-performer above a normal tweet).

## Headline: form vs content vs combined

| feature group | global AUC | within-author AUC |
|---|--:|--:|
| form | 0.623 | 0.582 |
| content | 0.589 | 0.584 |
| combined | 0.651 | 0.624 |

**Within-author, the content composite separates over-performers better (0.58), but both are weak** — mostly not explained by these features; reach, timing and luck dominate.

## Robust features (survived the within-author paired check)

*None cleared the bar — no feature reliably predicts over-performance within author. The honest answer: it's mostly not in the text.*

## Full ranking by single-feature AUC

| feature | group | AUC | r | over | normal | lift | paired Δ | agree | robust |
|---|:--|--:|--:|--:|--:|--:|--:|--:|:--:|
| `starts_caps_word` | form | 0.538 | +0.070 | 24% | 17% | 1.4x | +0.047 | 39% |  |
| `has_media` | form | 0.536 | +0.054 | 72% | 65% | 1.1x | +0.122 | 74% |  |
| `number_groups` | form | 0.534 | +0.053 | 3.0 | 2.2 | — | +0.668 | 43% |  |
| `is_advice` | content | 0.530 | +0.113 | 9% | 3% | 3.2x | +0.033 | 24% |  |
| `has_numbers` | form | 0.528 | +0.039 | 57% | 51% | 1.1x | +0.103 | 59% |  |
| `is_thread` | content | 0.525 | +0.075 | 10% | 5% | 2.0x | +0.021 | 16% |  |
| `allcaps_words` | form | 0.524 | +0.027 | 3.1 | 2.7 | — | +0.942 | 49% |  |
| `is_curiosity_gap` | content | 0.523 | +0.099 | 7% | 2% | 3.1x | +0.028 | 20% |  |
| `is_list` | content | 0.523 | +0.105 | 6% | 2% | 3.6x | +0.024 | 16% |  |
| `has_allcaps` | form | 0.521 | +0.031 | 62% | 58% | 1.1x | +0.112 | 63% |  |
| `negation_count` | content | 0.518 | +0.068 | 1.0 | 0.7 | — | +0.087 | 49% |  |
| `is_news_break` | content | 0.517 | +0.055 | 8% | 5% | 1.7x | +0.018 | 24% |  |
| `is_announcement` | content | 0.517 | +0.051 | 9% | 6% | 1.6x | +0.021 | 33% |  |
| `has_url` | form | 0.517 | +0.024 | 46% | 43% | 1.1x | +0.056 | 55% |  |
| `url_count` | form | 0.515 | -0.008 | 0.5 | 0.6 | — | -0.054 | 43% |  |
| `is_prediction` | content | 0.512 | +0.037 | 8% | 5% | 1.5x | -0.000 | 49% |  |
| `has_hashtag` | form | 0.511 | +0.033 | 8% | 6% | 1.4x | +0.026 | 20% |  |
| `hashtag_count` | form | 0.511 | +0.008 | 0.2 | 0.2 | — | +0.079 | 18% |  |
| `has_negation` | content | 0.510 | +0.015 | 33% | 31% | 1.1x | +0.011 | 51% |  |
| `superlative_count` | content | 0.508 | +0.011 | 0.2 | 0.1 | — | +0.015 | 33% |  |
| `has_superlative` | content | 0.508 | +0.018 | 13% | 11% | 1.1x | +0.020 | 35% |  |
| `is_stance` | content | 0.502 | +0.009 | 3% | 3% | 1.1x | -0.004 | 35% |  |
| `title_colon` | form | 0.502 | +0.004 | 16% | 16% | 1.0x | -0.033 | 57% |  |
| `is_opinion` | content | 0.502 | +0.007 | 4% | 3% | 1.1x | +0.024 | 22% |  |
| `is_personal` | content | 0.502 | +0.007 | 3% | 3% | 1.1x | -0.013 | 47% |  |
| `starts_with_i` | content | 0.501 | +0.003 | 2% | 2% | 1.1x | -0.005 | 37% |  |
| `is_question_hook` | content | 0.498 | -0.008 | 4% | 4% | 0.9x | -0.018 | 49% |  |
| `has_exclaim` | form | 0.497 | -0.009 | 5% | 6% | 0.9x | -0.010 | 47% |  |
| `exclaim_count` | form | 0.497 | -0.022 | 0.1 | 0.1 | — | -0.021 | 45% |  |
| `is_gratitude` | content | 0.494 | -0.037 | 0% | 1% | 0.1x | -0.010 | 41% |  |
| `has_emoji` | form | 0.491 | -0.013 | 28% | 30% | 0.9x | +0.029 | 33% |  |
| `first_person` | form | 0.490 | -0.015 | 31% | 33% | 0.9x | -0.025 | 61% |  |
| `emoji_count` | form | 0.489 | +0.007 | 0.8 | 0.8 | — | +0.897 | 31% |  |
| `is_quote` | form | 0.480 | -0.035 | 17% | 21% | 0.8x | -0.035 | 65% |  |
| `avg_word_len` | form | 0.479 | -0.026 | 4.7 | 4.8 | — | +0.009 | 53% |  |
| `char_len` | form | 0.479 | +0.001 | 438.0 | 436.2 | — | +6.827 | 43% |  |
| `question_count` | form | 0.473 | -0.042 | 0.1 | 0.1 | — | -0.056 | 59% |  |
| `has_question` | form | 0.473 | -0.061 | 6% | 12% | 0.5x | -0.046 | 61% |  |
| `line_count` | form | 0.468 | +0.001 | 5.4 | 5.4 | — | +1.734 | 37% |  |
| `money_or_pct` | form | 0.464 | -0.057 | 20% | 27% | 0.7x | +0.019 | 31% |  |
| `is_multiline` | form | 0.460 | -0.060 | 61% | 69% | 0.9x | -0.042 | 47% |  |
| `has_mention` | form | 0.446 | -0.110 | 4% | 15% | 0.3x | -0.012 | 39% |  |
| `mention_count` | form | 0.446 | -0.062 | 0.1 | 0.2 | — | +0.056 | 10% |  |

## Caveats

1. **Small N.** 571 over-performers across 51 authors; rare rhetorical features are noisy. Treat as directional.
2. **Heuristic content detectors.** Keyword/structure based — they under-detect (see `overperformance_qualitative.md` for what they miss).
3. **Population is not pure AI.** Authors span markets/crypto/astrology/news; conclusions are about *this mix*, not AI Twitter specifically.
4. **Over-performance ≠ likes.** A small account's over-performer may have few absolute likes. This measures relative pop, which is the writer-actionable part.
5. **Composite AUCs are in-sample.** Each composite takes its feature signs from the global r on the *same* rows it scores, so they are optimistic. Trust the companion leave-one-author-out experiment for the honest out-of-sample number.
6. **A high single-feature AUC is not a reliable lever** until it also survives the within-author paired check across many authors. Read this for the **negative** result too — whether the text predicts the metric at all.