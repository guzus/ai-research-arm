---
slug: etched
title: Etched
type: entity
aliases: ["Etched", "Sohu"]
tags: [ai-chips, inference, transformer-asic, hardware, funding]
description: AI-chip startup that exited stealth on 2026-06-30 with $800M raised, $1B+ in signed contracts, and a $5B valuation — betting on Sohu, a transformer-only inference ASIC whose first racks ship summer 2026 (performance claims still vendor-sourced).
created_at: 2026-07-01
timestamp: 2026-07-01T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-07-01", path: research/digest/2026-07-01-digest.md}
  - {title: "TechCrunch — Etched exits stealth", date: 2026-06-30}
---

Etched is an AI-chip startup that **exited stealth on 2026-06-30** with
**$800M raised, $1B+ in signed customer contracts, and a $5B valuation**. Its
product is **Sohu**, a **transformer-only inference ASIC** — silicon that hard-
wires the transformer architecture into the chip rather than staying general-
purpose — with the **first inference racks shipping this summer**. Performance
claims remain **vendor-sourced and unaudited** (ARA digest 2026-07-01,
TechCrunch, @kimmonismus).

## Why it matters
- **The specialization bet against [[nvidia]].** Sohu trades the flexibility of
  a GPU for throughput on one architecture. If transformers stay dominant, a
  transformer-only ASIC can undercut general-purpose accelerators on
  cost-per-token — the same economic logic driving [[broadcom]]-designed custom
  inference silicon and OpenAI's Jalapeño, but as an independent merchant chip.
- **Signed contracts before shipping.** $1B+ in contracts at exit, ahead of the
  first racks, is the notable data point: demand for cheaper inference capacity
  is being committed against unproven silicon, a supply-side signal within the
  broader [[ai-capex]] buildout.
- **Part of the inference-economics reshaping.** It lands the same cycle as
  [[meituan-longcat-2|LongCat-2.0]]'s no-Nvidia training claim and DeepSeek's
  DSpark speedups — different levers (custom silicon vs. software/model
  efficiency) all pushing on the cost of running large models.

## Open questions
- **Do the performance claims survive independent testing?** Everything public
  is vendor-sourced; the first neutral Sohu inference benchmarks will decide
  whether the $5B valuation is warranted.
- **Architecture risk.** A transformer-only ASIC is a bet that the transformer
  stays the dominant architecture through the chip's useful life — a wager
  against the next architectural shift.
