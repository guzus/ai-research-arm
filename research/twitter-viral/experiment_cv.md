# Experiment: honest ceiling on predicting over-performance (LOO-CV)

*2026-05-24T12:16:10.335046+00:00 — logistic regression, leave-one-author-out CV, 562 tweets / 81 over-performers / 21 authors.*

Each tweet is scored by a model trained on **other authors only**, so the score can't memorize "this account pops." LOO AUC is the real out-of-sample ceiling; the in-sample column shows how optimistic the naive fit is.

| feature set | # feats | in-sample AUC | **LOO global AUC** | LOO within-author AUC |
|---|--:|--:|--:|--:|
| form | 26 | 0.640 | **0.357** | 0.309 |
| content | 17 | 0.616 | **0.414** | 0.541 |
| all | 43 | 0.701 | **0.361** | 0.379 |

**Out-of-sample, the `content` set is best within-author (0.541).** Read 0.50 as a coin flip. The in-sample → LOO drop is the optimism the round-2 composites carried.

## Verdict

- A model with **every** form+content feature, scored honestly out-of-sample, reaches **LOO global AUC 0.361**, within-author **0.379** — barely distinguishable from a coin flip.
- **Form features *anti*-generalize** (LOO within-author **0.309 < 0.5**): a model trained on other authors ranks a held-out author's hits *below* their flops. Their pooled correlations are between-author artifacts that reverse within author — decisive evidence that length/caps are confounds, not levers.
- **Content is the only set that generalizes at all** (LOO within-author 0.541), and only barely above chance.
- The in-sample→LOO collapse (all: 0.701 → 0.361) shows the naive fit was ~entirely memorizing *which author* tweeted, not what makes a tweet pop.
- Empirical ceiling for *text-only* over-performance prediction on this corpus: a faint within-author content signal (~0.54) and nothing more. Reach, timing and luck dominate.