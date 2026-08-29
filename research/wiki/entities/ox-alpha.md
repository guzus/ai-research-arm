---
slug: ox-alpha
title: Ox Alpha
type: entity
aliases: ["Ox Alpha", "OxAlpha"]
tags: [stealth-model, mystery-model, hype-cycle, open-weights]
description: Z.ai confirmed on 2026-08-27 that it is the lab behind the formerly unattributed, free-to-use stealth model Ox Alpha — with weights said to be released soon — resolving weeks of speculation that had drifted among GLM-flash, DeepSeek and Google metrics after the model's headline number collapsed.
created_at: 2026-08-23
timestamp: 2026-08-27T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-08-27", path: research/digest/2026-08-27-digest.md}
  - {title: "ARA daily digest 2026-08-26", path: research/digest/2026-08-26-digest.md}
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

## Day six unclaimed — consumption numbers that can't be reconciled, and a first per-kernel read (2026-08-26)

- **Six days cloaked, with mutually inconsistent consumption figures
  (2026-08-26).** The model **still carries no lab claim**, and the running
  token-consumption estimates now contradict each other outright —
  **11.6T/3 days, 26T/4 days, 16.6T/5 days** — so none of them separates
  organic demand from a **zero-price promo** (the model has been **free
  throughout**). The free-window deadline (~2026-08-27) remains the forcing
  function (ARA daily digest 2026-08-26).
- **The first per-kernel KernelBench read lands it mid-pack on kernels —
  behind Opus 5, ahead of the pack on none of the headline rows
  (2026-08-26).** An independent **KernelBench** run gave Ox Alpha its
  **first per-kernel read: 7.17% of roofline on a top-k bitonic kernel, just
  behind Opus 5**, but **last place on sparse attention because it never
  emitted tensor-core tiling**. That profile is consistent with the existing
  mid-pack, Flash-class consensus — competent on familiar shapes, poor on
  specialized kernels (ARA daily digest 2026-08-26).
- **Attribution arguments now point at Zhipu/Z.ai on capacity-contention
   grounds (2026-08-26).** The day's attribution case is **capacity, not
   artifact**: a Zhipu/**Z.ai** run is argued on **capacity-contention grounds**
   — explicitly an **inference, not a disclosure** (ARA daily digest
   2026-08-26). The claim remains uncorroborated by any lab.

## Z.ai confirms it is the lab behind Ox Alpha (2026-08-27)

- **The mystery resolves: Z.ai owns it, weights soon (2026-08-27).** Z.ai
  **confirmed it is the lab behind Ox Alpha**, the model that had topped
  leaderboards while unattributed, with **weights said to be released soon** —
  ending weeks of speculation about the stealth entrant that this page's "open
  questions" had been tracking since day one. The confirmation lands the same
  window as the day's **top Hacker News item, [[zhipu-glm-5-3|GLM-5.3-Flash]]**
  (824 points / 414 comments), and effectively makes the Ox Alpha arc a
  **family launch** rather than a single flagship: the unattributed flash-class
  model resolves to a Z.ai GLM variant (TechCrunch; ARA daily digest
  2026-08-27). See [[open-weights]] and [[zhipu-glm-5-3]].
- **The deflation story now reads as a launch mechanic, not a riddle.** The
  hype-then-deflation arc this page documented in detail — the retracted 80% → a
  "realistic" 60-61%, the mid-pack benchmark footprints, the free window dating
  to ~2026-08-27 — closes with an attribution that was always at the top of the
  candidate list. The load-bearing remainder is the open-weights transition: the
  prompt says weights release soon, which the wiki will track on
  [[zhipu-glm-5-3]].