---
slug: weight-space-programming
title: Weight-space programming
type: concept
aliases: ["weight-space programming", "weight editing by LLM", "Astra weight editing", "self-rewriting"]
tags: [interpretability, model-editing, mit-csail, astra]
description: MIT CSAIL claim that GPT-6 Astra edited 0.016% of a small Qwen's weights (MATH-500 7.9%→48.1%); a later multi-lab paper reports gradient-free self-rewriting on Qwen3.5, with only the 27B improving.
created_at: 2026-11-03
timestamp: 2026-11-21T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-11-21", path: research/digest/2026-11-21-digest.md}
  - {title: "ARA daily digest 2026-11-04", path: research/digest/2026-11-04-digest.md}
  - {title: "ARA daily digest 2026-11-03", path: research/digest/2026-11-03-digest.md}
---

**Weight-space programming** is the framing of an MIT CSAIL paper (relayed by
@rohanpaul_ai; HN's top story on 2026-11-02/03 at 1,980 points and 630
comments, "Astra can read and write weights to improve Qwen").

## Claims

- [[astra|GPT-6 Astra]] located and removed the internal signal behind a small
  Qwen model's repetition loops, raising **MATH-500 from 7.9% to 48.1%** while
  touching **0.016% of weights**.
- The paper also claims LLMs can infer a network's training purpose from raw
  weights.

## Public checkpoint and a log rebuild (2026-11-04)

- **The edited Qwen checkpoint is on [[hugging-face|Hugging Face]].** A
  rebuild from the published logs scored **51.0% on MATH-500** versus the
  paper's **48.1%**. That is a public artifact, not an independent eval on
  other benches (ARA daily digest 2026-11-04; @rikiyatakehi, @_akhaliq).
- **Simon Willison found [[qwen-3-8-max|Qwen 3.8 27B]] can interpret model
  weights on a laptop.** The follow-up says the trick is not Astra-only
  (simonwillison.net; ARA daily digest 2026-11-04).
- The HN thread climbed to **2,744 points / 831 comments**, up from 1,980 /
  630 the day this page was created, and remained the top r/MachineLearning
  post (ARA daily digest 2026-11-04).

## Caveats

- **No independent evals yet beyond MATH-500.** The 51.0% rebuild is a
  reproduction of the paper's own task, not a third-party suite.
- Critics note looping ablation is "basic surgery humans can do too"
  (@teortaxesTex, r/MachineLearning); the novelty is who did the work, not the
  edit itself.
- Related checking problem: [[verification-bottleneck]]. A separate claim on
  2026-11-03 that Astra is a major Chinese distillation target (The Information,
  headline only) concerns [[openai]]'s defenses, not this result.

## Gradient-free self-rewriting on Qwen3.5 (2026-11-21)

- **UIUC / CMU / Rutgers / Princeton / Stanford / Yale report
  gradient-free “self-rewriting” on Qwen3.5.** Only the **27B** improves
  or repairs; **2B makes no edit** and **4B / 9B break themselves**.
  Repair of eight rows of layer-30 MLP noise lifts a held-out copy from
  **0.0% to 33.0%**. This is a different mechanism from the Astra-edits-Qwen
  MIT CSAIL claim: the model rewrites *its own* weights, not a smaller
  student's, and the effect is size-gated. Link the 27B sibling via
  [[qwen-3-8-max|Qwen3.8-27B]] only as the nearby Qwen 27B card already on
  this wiki — the paper names Qwen3.5, not Qwen3.8 (arXiv 2611.21885, HN;
  ARA daily digest 2026-11-21).
