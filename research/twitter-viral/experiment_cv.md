# Experiment: honest ceiling on predicting over-performance (LOO-CV)

*2026-05-24T13:34:53.656624+00:00 — logistic regression, leave-one-author-out CV, 3924 tweets / 571 over-performers / 57 authors.*

Each tweet is scored by a model trained on **other authors only**, so the score can't memorize "this account pops." LOO AUC is the real out-of-sample ceiling; the in-sample column shows how optimistic the naive fit is.

| feature set | # feats | in-sample AUC | **LOO global AUC** | LOO within-author AUC |
|---|--:|--:|--:|--:|
| form | 26 | 0.672 | **0.581** | 0.553 |
| content | 17 | 0.607 | **0.494** | 0.534 |
| all | 43 | 0.724 | **0.648** | 0.595 |

**Out-of-sample, the `all` set is best within-author (0.595).** Read 0.50 as a coin flip. The in-sample → LOO drop is the optimism the round-2 composites carried.

## Verdict

- The full feature model, scored honestly out-of-sample, reaches **LOO global AUC 0.648**, within-author **0.595** — weak, but above chance. (Within-author is the honest number for a writer; the higher global AUC is partly between-author — predicting *which accounts* pop more.)
- **Form has ~no within-author signal** out-of-sample (LOO within-author 0.553 ≈ chance); its higher global AUC (0.581) is between-author — it tracks which account tweeted, not which tweet pops.
- Content within-author out-of-sample: 0.534 (weak).
- The in-sample→LOO drop (all: 0.724 → 0.648 global) is how much the naive fit was memorizing *which author* tweeted rather than what makes a tweet pop.
- Empirical ceiling for *text-only* over-performance prediction on this corpus: a weak but real out-of-sample signal (within-author ~0.60); reach, timing and luck still dominate. No single feature clears the robustness bar; the most consistent (but small) tendency in the companion analysis is attaching **media**.