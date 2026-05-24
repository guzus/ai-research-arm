# What separates a >=100-like tweet from a flop

*Generated 2026-05-24T09:37:14.064707+00:00 from `research/twitter-viral/viral_tweets.jsonl`.*

- **677** tweets analyzed: **484** high (>=100 likes) / **193** low.
- **19** authors appear with BOTH high and low tweets — these drive the follower-controlled (paired) view.

## How to read this

- **r (global)** — point-biserial correlation between the feature and the high/low label across all tweets. Sign = direction, magnitude = strength. Confounded by who the author is.
- **paired Δ** — average of (mean among the author's high tweets − mean among their low tweets), over authors who have both. Holds follower count ~constant, so it isolates the *content* effect.
- **robust** — the signal is non-trivial (|r| ≥ 0.1) AND points the same way in both views across enough authors. Only robust features feed the verifier.

## The secret ingredients (robust, follower-controlled)

**Do more of this** (raises odds of clearing 100 likes):

- `has_allcaps` — present in 66% of high vs 41% of low tweets (1.63× as common in winners), r=+0.235.
- `char_len` — winners average 281.0 vs 149.0 (higher), r=+0.149.
- `word_count` — winners average 43.5 vs 23.0 (higher), r=+0.146.

## Full feature ranking

| feature | r (global) | high | low | lift | paired Δ | agree | robust |
|---|--:|--:|--:|--:|--:|--:|:--:|
| `has_allcaps` | +0.235 | 66% | 41% | 1.63× | +0.189 | 63% | ✅ |
| `has_hashtag` | +0.176 | 11% | 0% | 21.53× | +0.045 | 32% |  |
| `has_numbers` | +0.161 | 44% | 26% | 1.66× | -0.011 | 47% |  |
| `hashtag_count` | +0.158 | 0.2 | 0.0 | — | +0.106 | 32% |  |
| `char_len` | +0.149 | 281.0 | 149.0 | — | +47.803 | 63% | ✅ |
| `word_count` | +0.146 | 43.5 | 23.0 | — | +7.611 | 63% | ✅ |
| `has_question` | +0.146 | 14% | 4% | 3.49× | +0.078 | 58% |  |
| `question_count` | +0.142 | 0.2 | 0.0 | — | +0.092 | 58% |  |
| `money_or_pct` | +0.141 | 25% | 12% | 2.06× | +0.029 | 42% |  |
| `has_media` | +0.132 | 46% | 31% | 1.46× | +0.034 | 32% |  |
| `has_emoji` | +0.125 | 36% | 23% | 1.57× | +0.007 | 32% |  |
| `line_count` | +0.119 | 3.5 | 2.1 | — | +0.724 | 58% |  |
| `avg_word_len` | +0.118 | 4.7 | 4.4 | — | +0.107 | 53% |  |
| `exclaim_count` | +0.078 | 0.2 | 0.1 | — | +0.246 | 37% |  |
| `has_mention` | +0.065 | 5% | 2% | 2.39× | -0.007 | 21% |  |
| `number_groups` | +0.058 | 1.5 | 1.0 | — | -0.150 | 47% |  |
| `starts_caps_word` | -0.056 | 17% | 22% | 0.78× | +0.082 | 47% |  |
| `is_multiline` | +0.056 | 54% | 48% | 1.13× | +0.005 | 37% |  |
| `has_exclaim` | +0.051 | 11% | 8% | 1.44× | +0.022 | 32% |  |
| `mention_count` | +0.043 | 0.1 | 0.0 | — | +0.039 | 21% |  |
| `title_colon` | +0.039 | 21% | 18% | 1.20× | -0.032 | 32% |  |
| `emoji_count` | +0.035 | 1.3 | 1.0 | — | +0.340 | 42% |  |
| `is_quote` | +0.024 | 26% | 23% | 1.10× | -0.010 | 32% |  |
| `first_person` | +0.022 | 31% | 28% | 1.08× | -0.002 | 37% |  |
| `has_url` | -0.013 | 37% | 38% | 0.96× | -0.056 | 47% |  |
| `allcaps_words` | -0.011 | 4.0 | 4.2 | — | +1.173 | 58% |  |
| `url_count` | +0.006 | 0.4 | 0.4 | — | -0.040 | 47% |  |

## Caveats (read before trusting this)

1. **Correlation, not causation.** These features co-occur with engagement; they don't guarantee it. A verifier built on them is a *conformance scorer* — "does this draft resemble what works" — not a like-count oracle.
2. **Follower count is the elephant.** The paired view controls for it, but only across the 19 authors who had both high and low tweets. Global r is still author-confounded.
3. **Topic noise in the positive set.** The search query `Gemini`/`Claude` also matches zodiac/astrology and people's names, so the corpus spans AI, crypto, markets, astrology and politics. That actually makes the *form* findings more topic-agnostic, but it is not a pure AI sample.
4. **Top-search selection bias.** Positives come from X's "Top" ranking, which already favors popular tweets.
5. **`has_url` ↔ `has_media` overlap.** A media tweet carries a t.co link in its text, so these two features are partly entangled.
6. **Small low-N.** Only 193 low tweets; per-feature rates for rare features are noisy.
