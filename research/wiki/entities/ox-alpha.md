---
slug: ox-alpha
title: Ox Alpha
type: entity
aliases: ["Ox Alpha", "OxAlpha"]
tags: [stealth-model, mystery-model, hype-cycle, open-weights]
description: An unattributed, free-to-use model whose headline number collapsed from a retracted 80% to ~63% and then a "realistic" 60-61% with the task list and sample size still unpublished (2026-08-24) — attribution reading drifts from a Z.ai GLM Flash variant toward a Zhipu multimodal GLM-5.3 variant, with no lab having claimed it through day four and the free window dated to close near 2026-08-27.
created_at: 2026-08-23
timestamp: 2026-08-25T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-08-25", path: research/digest/2026-08-25-digest.md}
  - {title: "ARA model ticket — Ox Alpha stealth model", path: research/models/tickets/stealth-ox-alpha-model-2026-08.md}
  - {title: "ARA daily digest 2026-08-24", path: research/digest/2026-08-24-digest.md}
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
- **The headline number collapses — again (2026-08-24).** The figure that
   opened the hype arc is now written off by its own source: the headline
   number ran **retracted 80% → ~63% → a "realistic" 60-61%**, and **the task
   list and sample size remain unpublished after eight feed cycles** — a live
   demonstration of the default deflation path for an unrepeatable,
   unattributed claim (see [[verification-bottleneck]]).
- **The attribution drift finds a mechanics argument against the Cursor
   theory (2026-08-24).** The earlier Cursor hypothesis was **argued down on
   capability grounds** — a code-only shop has no commercial reason to
   post-train vision — which pushed the community read further toward a
   **Zhipu multimodal [[zhipu-glm-5-3|GLM-5.3]]-lineage variant**, still
   unacknowledged by Zhipu. The one thing the week's measurements did not
   dislodge was the consensus that it is a ***Flash*-class model** that
   approaches Sol-mid on tasks — the size implication, not the attribution,
   remains the load-bearing claim.

## Open questions

- **Who actually hosts it?** The consensus read points at a Z.ai GLM Flash
  variant, but no lab has claimed the model on the record.
- **Does the deflation feed the attribution-skepticism norm?** The
  unrepeatable-eval + no-attribution pattern is a test of how the community
  prices unreleased-model claims going forward.

## Day four unclaimed — the benchmark footprints keep landing (2026-08-25)

- **Still nobody has claimed it, and the spec table quietly grows.** On day
  four the model still carries **no lab claim, no model card, no pricing and no
  weights**, and both a "mysterious AI model" write-up in trade aggregators and
  the guessing-game-as-parody dynamic (see the ticket's pseudo-architecture
  episode) have become coverage in themselves. Two unsupported hypotheses
  surfaced — an **Anthropic experiment** (on a claimed "telltale marker") and
  **xAI's unreleased [[xai|Grok 4.7]]** in pre-release testing — both
  single-account; the **GLM-family reading from firsthand testers remains
  best-supported** (ARA model ticket, 2026-08-24/25).
- **The agentic-benchmark footprints are the day's real new datapoints
  (2026-08-25).** Agents on Rails added Ox Alpha to its **`lemans` agentic
  benchmark at 52/63 — tied 5th with Grok 4.6**, behind the most-accurate
  [[claude-opus-5|Opus 5]] (58/63) and ahead of OpenAI's Terra (49/63); and the
  model joined **Context Arena's 8-needle long-context board**. It also drew
  **two cybersecurity evaluations with opposite readings**. The picture is now
  the same mid-pack, Flash-class, Sol-adjacent profile the controlled evals on
  this page already established — consistent, but consistent mid, never
  frontier (ARA daily digest 2026-08-25).
- **The free window is the clock to watch.** The free access period is dated to
  close **near 2026-08-27** — the natural forcing function for either a
  [[zhipu-glm-5-3|Zhipu]] claim or a silent de-listing, whichever comes first.