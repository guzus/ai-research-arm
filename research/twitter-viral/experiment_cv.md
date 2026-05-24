# Experiment: honest ceiling on predicting over-performance (LOO-CV)

*2026-05-24T12:51:27.766277+00:00 — logistic regression, leave-one-author-out CV, 1831 tweets / 332 over-performers / 28 authors.*

Each tweet is scored by a model trained on **other authors only**, so the score can't memorize "this account pops." LOO AUC is the real out-of-sample ceiling; the in-sample column shows how optimistic the naive fit is.

| feature set | # feats | in-sample AUC | **LOO global AUC** | LOO within-author AUC |
|---|--:|--:|--:|--:|
| form | 26 | 0.708 | **0.583** | 0.508 |
| content | 17 | 0.619 | **0.519** | 0.547 |
| all | 43 | 0.750 | **0.634** | 0.544 |

**Out-of-sample, the `content` set is best within-author (0.547).** Read 0.50 as a coin flip. The in-sample → LOO drop is the optimism the round-2 composites carried.

## Verdict

- The full feature model, scored honestly out-of-sample, reaches **LOO global AUC 0.634**, within-author **0.544** — weak, but above chance. (Within-author is the honest number for a writer; the higher global AUC is partly between-author — predicting *which accounts* pop more.)
- **Form has ~no within-author signal** out-of-sample (LOO within-author 0.508 ≈ chance); its higher global AUC (0.583) is between-author — it tracks which account tweeted, not which tweet pops.
- Content within-author out-of-sample: 0.547 (weak).
- The in-sample→LOO drop (all: 0.750 → 0.634 global) is how much the naive fit was memorizing *which author* tweeted rather than what makes a tweet pop.
- Empirical ceiling for *text-only* over-performance prediction on this corpus: a weak but real out-of-sample signal (within-author ~0.54); reach, timing and luck still dominate. The one within-author-robust feature in the companion analysis is attaching **media**.