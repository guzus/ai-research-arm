# Does content beat form? (over-performance analysis)

*Generated 2026-05-24T09:37:14.194493+00:00 from `overperformance_tweets.jsonl`.*

- **562** timeline tweets: **81** over-performers (>=3x the author's median) / **481** normal, across **18** authors with both classes.
- Label is per-author, so the pooled comparison is already largely reach-controlled. AUC = P(rank an over-performer above a normal tweet).

## Headline: form vs content vs combined

| feature group | global AUC | within-author AUC |
|---|--:|--:|
| form | 0.626 | 0.454 |
| content | 0.582 | 0.591 |
| combined | 0.658 | 0.550 |

**Within-author, the content composite separates over-performers better.** Both are weak — over-performance is mostly not explained by these features, consistent with round 1 (engagement is dominated by reach + luck + timing).

## Robust features (survived the within-author paired check)

*None cleared the bar — no feature reliably predicts over-performance within author. The honest answer: it's mostly not in the text.*

## Full ranking by single-feature AUC

| feature | group | AUC | r | over | normal | lift | paired Δ | agree | robust |
|---|:--|--:|--:|--:|--:|--:|--:|--:|:--:|
| `is_quote` | form | 0.552 | +0.084 | 35% | 24% | 1.4x | +0.041 | 33% |  |
| `has_negation` | content | 0.543 | +0.074 | 28% | 20% | 1.4x | -0.017 | 56% |  |
| `negation_count` | content | 0.542 | +0.028 | 0.4 | 0.3 | — | -0.104 | 56% |  |
| `is_question_hook` | content | 0.523 | +0.091 | 7% | 3% | 2.7x | +0.028 | 28% |  |
| `first_person` | form | 0.523 | +0.036 | 32% | 27% | 1.2x | -0.012 | 61% |  |
| `is_news_break` | content | 0.518 | +0.075 | 6% | 2% | 2.5x | +0.053 | 17% |  |
| `is_stance` | content | 0.514 | +0.053 | 6% | 3% | 1.9x | -0.008 | 39% |  |
| `is_curiosity_gap` | content | 0.512 | +0.069 | 4% | 1% | 3.0x | +0.013 | 17% |  |
| `is_announcement` | content | 0.510 | +0.034 | 6% | 4% | 1.5x | +0.032 | 22% |  |
| `is_advice` | content | 0.508 | +0.038 | 4% | 2% | 1.8x | +0.068 | 17% |  |
| `mention_count` | form | 0.504 | +0.092 | 0.2 | 0.0 | — | +0.808 | 11% |  |
| `has_mention` | form | 0.504 | +0.016 | 4% | 3% | 1.3x | +0.041 | 11% |  |
| `is_opinion` | content | 0.504 | +0.021 | 2% | 2% | 1.5x | +0.006 | 6% |  |
| `is_gratitude` | content | 0.502 | +0.015 | 1% | 1% | 1.5x | -0.004 | 22% |  |
| `char_len` | form | 0.500 | -0.036 | 178.1 | 206.3 | — | +20.769 | 56% |  |
| `is_thread` | content | 0.500 | -0.000 | 1% | 1% | 1.0x | -0.011 | 22% |  |
| `is_prediction` | content | 0.498 | -0.009 | 2% | 3% | 0.8x | -0.016 | 39% |  |
| `exclaim_count` | form | 0.498 | +0.004 | 0.1 | 0.1 | — | +0.029 | 17% |  |
| `starts_with_i` | content | 0.498 | -0.007 | 5% | 5% | 0.9x | +0.018 | 11% |  |
| `has_exclaim` | form | 0.497 | -0.006 | 9% | 9% | 0.9x | -0.031 | 44% |  |
| `is_list` | content | 0.497 | -0.030 | 0% | 1% | 0.0x | -0.006 | 11% |  |
| `is_personal` | content | 0.496 | -0.035 | 0% | 1% | 0.0x | -0.007 | 11% |  |
| `has_superlative` | content | 0.496 | -0.013 | 5% | 6% | 0.8x | +0.053 | 22% |  |
| `superlative_count` | content | 0.495 | -0.034 | 0.0 | 0.1 | — | +0.042 | 17% |  |
| `hashtag_count` | form | 0.490 | -0.006 | 0.1 | 0.1 | — | +0.107 | 17% |  |
| `has_hashtag` | form | 0.489 | -0.030 | 5% | 7% | 0.7x | +0.007 | 17% |  |
| `starts_caps_word` | form | 0.477 | -0.040 | 16% | 21% | 0.8x | +0.061 | 33% |  |
| `question_count` | form | 0.473 | -0.051 | 0.1 | 0.1 | — | +0.014 | 22% |  |
| `has_question` | form | 0.473 | -0.062 | 6% | 12% | 0.5x | +0.008 | 22% |  |
| `url_count` | form | 0.468 | -0.045 | 0.3 | 0.4 | — | -0.133 | 50% |  |
| `has_url` | form | 0.467 | -0.048 | 31% | 37% | 0.8x | -0.115 | 44% |  |
| `line_count` | form | 0.467 | +0.044 | 3.0 | 2.5 | — | +4.691 | 33% |  |
| `is_multiline` | form | 0.466 | -0.048 | 43% | 50% | 0.9x | +0.023 | 39% |  |
| `emoji_count` | form | 0.458 | -0.023 | 0.9 | 1.2 | — | -0.441 | 39% |  |
| `avg_word_len` | form | 0.456 | +0.008 | 4.6 | 4.6 | — | +0.051 | 44% |  |
| `has_numbers` | form | 0.455 | -0.066 | 28% | 37% | 0.8x | +0.045 | 44% |  |
| `number_groups` | form | 0.455 | -0.009 | 1.1 | 1.2 | — | +2.416 | 39% |  |
| `has_emoji` | form | 0.447 | -0.081 | 22% | 33% | 0.7x | -0.018 | 33% |  |
| `has_media` | form | 0.442 | -0.083 | 28% | 40% | 0.7x | -0.067 | 50% |  |
| `title_colon` | form | 0.442 | -0.098 | 12% | 24% | 0.5x | -0.007 | 28% |  |
| `has_allcaps` | form | 0.442 | -0.083 | 46% | 57% | 0.8x | +0.019 | 56% |  |
| `money_or_pct` | form | 0.431 | -0.120 | 9% | 22% | 0.4x | -0.020 | 33% |  |
| `allcaps_words` | form | 0.423 | -0.025 | 3.7 | 4.2 | — | +3.876 | 39% |  |

## Caveats

1. **Small N.** 81 over-performers across 18 authors; rare rhetorical features are noisy. Treat as directional.
2. **Heuristic content detectors.** Keyword/structure based — they under-detect (see `overperformance_qualitative.md` for what they miss).
3. **Population is not pure AI.** Authors span markets/crypto/astrology/news; conclusions are about *this mix*, not AI Twitter specifically.
4. **Over-performance ≠ likes.** A small account's over-performer may have few absolute likes. This measures relative pop, which is the writer-actionable part.
5. **Composite AUCs are in-sample.** Each composite takes its feature signs from the global r on the *same* rows it scores, so the content/combined numbers are optimistic. On a held-out 50/50 split the content composite within-author is ~0.53 (not ~0.60); form stays sub-chance (~0.41). The direction (content > form) survives ~18/20 splits, but the *gap* is widest exactly at the 3x cutoff.
6. **No single feature is a reliable lever.** Even `is_stance` (best by pooled lift, ~1.9x) is ~chance within author (AUC ~0.51). Read this analysis for the **negative** result — the text barely predicts over-performance — not for a lever.