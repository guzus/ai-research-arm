---
slug: fireworks-ai
title: Fireworks AI
type: entity
aliases: ["Fireworks", "Fireworks.ai", "Fireworks AI Inc.", "Ember-1", "Fireworks Ember-1"]
tags: [funding, inference-infra, series-d, ai-capex]
description: AI inference-infrastructure company; Ember-1 is a Kimi K3 specialist the lab says keeps K3 quality with about 40% fewer tokens, after a $1.505B Series D at $17.5B.
created_at: 2026-07-18
timestamp: 2026-09-28T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-09-28", path: research/digest/2026-09-28-digest.md}
  - {title: "ARA daily digest 2026-07-18", path: research/digest/2026-07-18-digest.md}
---

**Fireworks AI** is an AI inference-infrastructure company that serves
model inference at scale for third-party developers and enterprises,
rather than building its own frontier models. It raised a **$1.505B
Series D at a $17.5B valuation** on 2026-07-18, led by **Nvidia, Index
Ventures, and TCV**, citing **40T+ tokens/day** served across its
platform — one of the largest inference-infrastructure funding rounds of
the [[ai-capex]] cycle.

## Why it matters

- **Scale of the round.** At $17.5B, the valuation places Fireworks among
  the largest independent inference-serving vendors, distinct from the
  neocloud GPU-rental model ([[coreweave]], [[nebius]]) and from the
  frontier labs themselves ([[openai]], [[anthropic]]) — it monetizes the
  serving layer that sits between GPU capacity and application traffic.
- **Nvidia as lead investor.** [[nvidia]] backing an inference-serving
  platform (rather than only chips) is a vertical-integration signal
  consistent with its broader pattern of investing across the AI stack it
  supplies hardware to.
- **40T+ tokens/day.** The disclosed serving volume is a concrete demand
  data point for the inference side of the [[ai-capex]] buildout, distinct
  from training-side capex figures (TSMC, hyperscaler GPU orders) that
  otherwise dominate the capex narrative.

## Ember-1: a Kimi K3 specialist that spends fewer tokens (2026-09-28)

- **Fireworks shipped Ember-1**, a [[moonshot-kimi-k3|Kimi K3]]
  specialist trained across >50 experiments / >200 evals. The
  post says K3 sometimes spends >90% of generated tokens on
  internal reasoning. Bench vs K3-max: Terminal Bench 2.1
  **82.0% vs 80.9%**; SWE-bench Verified **92.2% vs 93.2%**;
  DeepSWE 1.1 **75.2% vs 66.4%**. Live customer A/B: **0.753 vs
  0.751** quality, **29.9K vs 49.3K** output tokens (−39%
  total, −71.3% reasoning). Research Preview serverless beside
  base K3 at the same **$3 / $0.30 / $15** card; weights are
  not released. Closed Sunday as HN's #2 AI story at 287/159.
  Same-Sunday [[naive-ai|N0.5-Flash]] is the open counterpart
  — MIT weights, continued-pretrain, not a closed specialist
  (Fireworks, HN; ARA daily digest 2026-09-28).
- **A $30B Fireworks valuation remains a single-relay
  Information attribution.** The last confirmed raise on this
  page is still July's **$1.505B at $17.5B** (ARA daily digest
  2026-09-28).

## Open questions

- **Customer concentration.** No breakdown of which labs/enterprises drive
  the 40T+ tokens/day figure has been disclosed.
- **Competitive position.** How the round and valuation compare against
  other inference-serving platforms (e.g. [[openrouter]], which routes
  rather than serves inference directly) as the field consolidates.
