---
slug: etched
title: Etched
type: entity
aliases: ["Etched", "Sohu"]
tags: [ai-chips, inference, transformer-asic, hardware, funding]
description: AI-chip startup that exited stealth on 2026-06-30 with $800M raised and a $5B valuation, then raised $700M at a $21B valuation (2026-08-19) and shipped its first Sohu rack to lead investor Jane Street — betting on a transformer-only inference ASIC (performance claims still vendor-sourced).
created_at: 2026-07-01
timestamp: 2026-08-19T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-08-19", path: research/digest/2026-08-19-digest.md}
  - {title: "ARA daily digest 2026-08-07", path: research/digest/2026-08-07-digest.md}
  - {title: "ARA daily digest 2026-07-01", path: research/digest/2026-07-01-digest.md}
  - {title: "ARA daily digest 2026-07-25", path: research/digest/2026-07-25-digest.md}
  - {title: "TechCrunch — Etched exits stealth", date: 2026-06-30}
  - {title: "TechCrunch — AI chip startup Etched defies skeptics, hits $10.3B valuation from big-name investors", date: 2026-07-23}
---

Etched is an AI-chip startup that **exited stealth on 2026-06-30** with
**$800M raised, $1B+ in signed customer contracts, and a $5B valuation**. Its
product is **Sohu**, a **transformer-only inference ASIC** — silicon that hard-
wires the transformer architecture into the chip rather than staying general-
purpose — with the **first inference racks shipping this summer**. Performance
claims remain **vendor-sourced and unaudited** (ARA digest 2026-07-01,
TechCrunch, @kimmonismus).

## Why it matters
- **Valuation more than doubled within a month (2026-07-23).** TechCrunch
  reports Etched "defies skeptics" and hit a **$10.3B valuation** from
  big-name investors — up from the **$5B** stealth-exit mark just three
  weeks earlier — a sharp re-rating before the first Sohu racks have
  shipped or been independently benchmarked (ARA digest 2026-07-25).
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

- **Repriced at $10B by SK Hynix and TSMC — the same day AMD bought a rival
  (2026-08-07).** The digest records Etched **repriced at $10B by SK Hynix and
  TSMC**, which adds named strategic investors to the $10.3B mark already
  recorded above rather than a new number. What makes it worth noting is the
  timing: **the market marked [[model-specific-silicon]] up at the exact moment
  [[amd]] acquired [[taalas]]**, the second such acquisition after Nvidia–Groq.
  Etched sits one notch less specialized than Taalas — Sohu freezes the
  *transformer architecture*, Taalas freezes *one model's weights* — so an
  incumbent GPU vendor validating the far end of that spectrum is a read-through
  to Etched's own bet (ARA daily digest 2026-08-07). Note the investor identity:
  a memory maker and a foundry, i.e. suppliers, not customers.

- **$700M at a $21B valuation; first rack ships to its own lead investor
  (2026-08-19).** TechCrunch reports Etched raised **$700M at a $21B
  valuation** — **doubling in roughly a month** off the $10.3B mark — in a
  round **led by Jane Street**, with **Kleiner Perkins, Sequoia, a16z, Peter
  Thiel, BCV and Blackstone**. Crucially, **Jane Street tested the chip, led
  the round, and took delivery of the first Sohu system** — a **closed loop**
  that is a **weaker signal than an arm's-length customer deployment**. The
  named risk is **architecture lock-in**: hardcoding transformers into silicon
  (TechCrunch, @Etched via @jukan05; ARA daily digest 2026-08-19).

## Open questions
- **Do the performance claims survive independent testing?** Everything public
  is vendor-sourced; the first neutral Sohu inference benchmarks will decide
  whether the $5B valuation is warranted.
- **Architecture risk.** A transformer-only ASIC is a bet that the transformer
  stays the dominant architecture through the chip's useful life — a wager
  against the next architectural shift.
