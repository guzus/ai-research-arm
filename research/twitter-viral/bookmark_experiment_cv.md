# Experiment: honest ceiling on predicting over-performance (LOO-CV)

*2026-05-24T14:22:50.456149+00:00 — logistic regression, leave-one-author-out CV, 3644 tweets / 663 over-performers / 53 authors.*

Each tweet is scored by a model trained on **other authors only**, so the score can't memorize "this account pops." LOO AUC is the real out-of-sample ceiling; the in-sample column shows how optimistic the naive fit is.

| feature set | # feats | in-sample AUC | **LOO global AUC** | LOO within-author AUC |
|---|--:|--:|--:|--:|
| form | 26 | 0.666 | **0.589** | 0.616 |
| content | 17 | 0.578 | **0.488** | 0.546 |
| all | 43 | 0.683 | **0.588** | 0.608 |

**Out-of-sample, the `form` set is best within-author (0.616).** Read 0.50 as a coin flip. The in-sample → LOO drop is the optimism the round-2 composites carried.

## Verdict

- The full feature model, scored honestly out-of-sample, reaches **LOO global AUC 0.588**, within-author **0.608** — a real (if modest) signal. (Within-author is the honest number for a writer; global mixes in between-author effects — predicting *which accounts* pop more.)
- **Form carries real within-author signal** (LOO within-author 0.616) — surface features (length / media / numbers / …) predict this metric *within* an author, not just across accounts. This is the actionable part.
- Content within-author out-of-sample: 0.546.
- The in-sample→LOO drop (all: 0.683 → 0.588 global) is how much the naive fit was memorizing *which author* tweeted rather than what makes a tweet pop.
- Out-of-sample ceiling for *text-only* prediction on this corpus: within-author ~0.61. See the companion analysis for which features (if any) survive the within-author check; reach, timing and luck carry the rest.