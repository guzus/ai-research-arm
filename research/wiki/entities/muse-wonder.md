---
slug: muse-wonder
title: Muse Wonder
type: entity
aliases: ["Muse Wonder", "Muse Wonder Full", "Wonder Full", "Meta Muse Wonder"]
tags: [model-release, meta, frontier-model, pricing, coding-agent]
description: Meta's first independently scored frontier pair; Artificial Analysis puts Wonder at 52 and subscriber-only Full at 56 on its Intelligence Index, up from Muse Spark 1.3's 48.
created_at: 2026-10-13
timestamp: 2026-10-16T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-10-16", path: research/digest/2026-10-16-digest.md}
  - {title: "ARA daily digest 2026-10-13", path: research/digest/2026-10-13-digest.md}
---

**Muse Wonder** and **Muse Wonder Full** are [[meta]]'s first models to land
an independent Artificial Analysis Intelligence Index score above the
[[muse-code|Muse Spark]] line. Wonder is live on the Meta Model API and in
[[muse-code|Muse Code]] with **1M context** plus Active Memory / Active
Focus. Full is limited to Muse Code subscribers on the **$50 and $200**
tiers and has no public per-token price yet.

This page tracks the Wonder pair. The earlier Spark SKUs and the consumer
agent stay on [[muse-code]]; the 30B Apache-2.0 distill is
[[muse-glimmer]]; the 2026-10-16 open-weight Spark cut is
[[muse-spark-open]]. A separate "Watermelon" codename is still an unreleased
next-foundation tease and is **not** this ship.

## Why it matters

- **Independent scores, not only Meta's table.** Artificial Analysis
  scores Wonder **52** and Full **56** on the Intelligence Index, up
  from **48** for Muse Spark 1.3. Opus 5.5 still leads AA's overall
  index. Full beat Spark 1.3 on all ten of AA's evals, with
  Terminal-Bench 4.0 rising from **33% to 57%** and GDPval-AA v2.1
  gaining **176 Elo**. Full scores **68** on AA's Coding Agents Index,
  tied with Claude Code on [[claude-sonnet-5-5|Sonnet 5.5]] and ahead
  of [[claude-opus-5-5|Opus 5.5]] (**66**) (@AIatMeta, Artificial
  Analysis, TechCrunch, The Verge, The Decoder; ARA daily digest
  2026-10-13).
- **Per-token cheap is not per-task cheap.** Wonder lists at
  **$4/$20 per million tokens** — Meta's "60% cheaper than Fable" line
  — but AA prices it at **$4.52 per task** because it reads ~**7.7M**
  input tokens per task. That is cheaper than [[claude-fable-5|Fable
  5.1]] (**$7.63**) and Opus 5.5 (**$5.98**) and well above
  [[gpt-6|GPT-6.1 Sol]] (**$0.72**). See
  [[verification-bottleneck]] (Artificial Analysis; ARA daily digest
  2026-10-13).
- **Distribution, not only the card.** HN's lead AI thread (527 / 299)
  asked whether Facebook, Instagram, and WhatsApp matter more than the
  benches. Nathan Lambert said Meta "is back at the frontier" pending
  independent evals. The skeptic flag is the inverse: "Meta officially
  overtakes OpenAI" rests on Meta-picked benches, and HN commenters
  noted the marketing page's scores are for Full, not Wonder.

## Caveats on this cycle

- Relays of Meta's own benchmark table disagree on specific figures.
  Dan Shipper withdrew a result after finding a problem in the run.
  Alexandr Wang confirmed a Muse Code usage-limit bug, with resets
  promised (ARA daily digest 2026-10-13).

## Open questions

- **Does Full get a public per-token card**, or does Meta keep the
  stronger SKU inside the $50/$200 Muse Code subscription?
- **Do third-party evals besides AA hold** once harnesses match, given
  the withdrawn Shipper run and the Full-vs-Wonder marketing mix-up?
- **Is Watermelon a later foundation model**, or a discarded
  Spark-era codename? Leadership teases on 2026-10-12 were emoji-only.
