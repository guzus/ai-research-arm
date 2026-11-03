---
slug: weight-space-programming
title: Weight-space programming
type: concept
aliases: ["weight-space programming", "weight editing by LLM", "Astra weight editing"]
tags: [interpretability, model-editing, mit-csail, astra]
description: MIT CSAIL claim that GPT-6 Astra found and removed the internal signal behind a small Qwen model's repetition loops by editing 0.016% of weights, lifting MATH-500 from 7.9% to 48.1%; unreplicated.
created_at: 2026-11-03
timestamp: 2026-11-03T00:00:00Z
sources:
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

## Caveats

- **No replication yet.**
- Critics note looping ablation is "basic surgery humans can do too"
  (@teortaxesTex, r/MachineLearning); the novelty is who did the work, not the
  edit itself.
- Related checking problem: [[verification-bottleneck]]. A separate claim the
  same day that Astra is a major Chinese distillation target (The Information,
  headline only) concerns [[openai]]'s defenses, not this result.
