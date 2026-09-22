---
slug: xiaomi-mimo-v2-6
title: Xiaomi MiMo-V2.6
type: entity
aliases: ["MiMo-V2.6", "MiMo-V2.6-Pro", "MiMo-V2.6-Flash", "Xiaomi MiMo-V2.6", "Xiaomi MiMo V2.6", "MiMo V2.6"]
tags: [open-weights, china, moe, xiaomi, intelligence-index]
description: Xiaomi's open-weight 1.02T/42B-active MoE; MiMo-V2.6-Pro scored 46 on Artificial Analysis' Intelligence Index at $0.13 per index task, matching Grok 4.7.
created_at: 2026-09-22
timestamp: 2026-09-22T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-09-22", path: research/digest/2026-09-22-digest.md}
---

**Xiaomi MiMo-V2.6** is the open-weight successor to
[[xiaomi-mimo-v2-5-pro|MiMo-v2.5-Pro]]. **Pro** is a
**1.02T-total / 42B-active MoE** scored at **46** on
Artificial Analysis' Intelligence Index — the same
composite [[xai|Grok 4.7]] posted hours earlier, at
**$0.13 per index task** against Grok's **$2/$6 per
Mtok**. **Flash** is **310B total / 15B active** with a
**1M context** window and an MTP drafter. Xiaomi
released RL environments with the weights. See
[[open-weights]].

## Why it matters

- **A 20-point generational jump on a public
  composite (2026-09-21).** Pro's **46** is up from
  [[xiaomi-mimo-v2-5-pro|MiMo-V2.5-Pro]]'s **26**.
  Artificial Analysis placed it on the
  intelligence-vs-cost Pareto frontier. That is
  index-level parity with a closed US flagship, not
  a task-level bake-off (Artificial Analysis via
  @mervenoyann, @testingcatalog, The Decoder; ARA
  daily digest 2026-09-22).
- **Cheap is the comparison.** Grok 4.7 kept the
  **$2/$6** list of Grok 4.6; MiMo-V2.6-Pro's
  **$0.13/task** is the open-weight cost argument
  against that card. The Decoder's read of Grok
  itself is less flattering than xAI's: **46**
  against **53** for [[claude-fable-5|Claude Fable
  5.1]] and [[gpt-6|GPT-6]], with a wider gap on
  agentic coding. See [[xai]].
- **The distillation caveat is unresolved.**
  @teortaxesTex, who reviewed the training details,
  called it "hard to dismiss as distillation. Not
  impossible, but it loses the bite," while
  reporting the model fails his out-of-distribution
  humor probe. Treat the Grok-parity claim as
  **index-level, not task-level**.

## Open questions

- **Does an independent task suite hold the 46?**
  The Intelligence Index match is one composite;
  Grok 4.7's vendor table (CursorBench 4.0 46.3%,
  DeepSWE v1.1 71.0% high-effort, Terminal-Bench
  4.0 38.0%) has no public MiMo counterpart yet.
- **Is Flash the serving SKU?** 15B-active / 1M
  context plus an MTP drafter is the throughput
  story; Pro is the scoreboard story. Which one
  people actually run is still open.
- **Does Xiaomi stay in the open lane?** The
  predecessor page asked this after the UltraSpeed
  claim. V2.6 answers with weights and RL
  environments; it does not settle license or
  cadence.
