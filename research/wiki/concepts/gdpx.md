---
slug: gdpx
title: GDPx (SemiAnalysis agentic benchmark)
type: concept
aliases: ["GDPx", "SemiAnalysis GDPx", "GDPx benchmark"]
tags: [benchmark, agents, evaluation, semianalysis]
description: SemiAnalysis's 206-task agentic benchmark on which the best model, Claude Opus 5.5, scores only 12.0% at $51 per task.
created_at: 2026-11-03
timestamp: 2026-11-03T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-11-03", path: research/digest/2026-11-03-digest.md}
---

**GDPx** is a 206-task agentic benchmark published by SemiAnalysis
(@SemiAnalysis_, relayed by @notlikeryo_ and @kimmonismus on 2026-11-02/03).

## Results (as relayed; no SemiAnalysis write-up captured)

- [[claude-opus-5-5|Claude Opus 5.5]] leads at **12.0%** at about **$51 per
  task**.
- [[gemini-4-carbon|Gemini 4 Carbon]] is second at **10.9%** for about a third
  of the cost.
- **Ranking flips when cyber, bio and alignment tasks are dropped:** [[astra|GPT-6
  Astra]] then comes first, which suggests Astra's lead on the remaining tasks
  is offset by its performance on the safety-sensitive subset.

## Why it matters

A ceiling of 12% on a cost-reported agentic suite is a counterweight to
vendor-chosen tables, and the cost-per-task column makes the Opus 5.5 versus
Carbon trade-off explicit. Compare [[remote-labor-index]], which also finds
frontier agents failing most real-work tasks.
