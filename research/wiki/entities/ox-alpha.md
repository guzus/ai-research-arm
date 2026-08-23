---
slug: ox-alpha
title: Ox Alpha
type: entity
aliases: ["Ox Alpha", "OxAlpha"]
tags: [stealth-model, mystery-model, hype-cycle, open-weights]
description: An unattributed, free-to-use model whose hype arc closed downward over five Twitter cycles (2026-08-22/23) — debunk-consensus reads it as a Z.ai GLM Flash variant, and no lab has claimed it, with the free window dated to close near 2026-08-27.
created_at: 2026-08-23
timestamp: 2026-08-23T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-08-23", path: research/digest/2026-08-23-digest.md}
---

**Ox Alpha** was an unattributed, free-to-use model whose short hype arc
closed **downward** over five straight Twitter feed cycles on 2026-08-22/23 —
a live case study in how a stealth-model rumor cycle forms without any
attribution and then deflates on the first controlled measurements.

## Why it matters

- **The first controlled eval placed it mid-pack.** A controlled run by
  Serafim Batzoglou on an **ICML 2026 induction benchmark** placed the model
  **below [[gpt-5-6|GPT-5.6 Luna]] and [[deepseek-v4-flash|DeepSeek V4 Pro]]
  and just above [[gemini-3-7-flash|Gemini 3.7 Flash]]**, and required **551
  API calls to collect 87 scoreable answers (~16% yield)** — an expensive,
  low-yield evaluation profile.
- **Independent testers deflated the frontier claim (2026-08-22/23).** Ethan
  Mollick reported it **below [[moonshot-kimi-k3|Kimi K3]]** and "not at the
  frontier even among open weights"; @teortaxesTex logged **58.4 on DeepSWE**;
  the community read converged on **a Z.ai GLM Flash variant**
  ([[zhipu-glm-5-3]]-lineage) rather than a new frontier-lab flagship.
- **At least eight incompatible attributions in ~12 hours.** Attributions
  published included a widely-shared **"it's a Gemini model by GoogleDeepMind"**
  claim with no evidence attached. **Z.ai has not claimed it**, and the free
  window is dated to close around **2026-08-27**. For the theme-level read —
  an unattributed "frontier" claim failing against independent benchmarks —
  see [[open-weights]].

## Open questions

- **Who actually hosts it?** The consensus read points at a Z.ai GLM Flash
  variant, but no lab has claimed the model on the record.
- **Does the deflation feed the attribution-skepticism norm?** The
  unrepeatable-eval + no-attribution pattern is a test of how the community
  prices unreleased-model claims going forward.