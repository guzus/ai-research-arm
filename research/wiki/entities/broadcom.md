---
slug: broadcom
title: Broadcom
type: entity
aliases: [Broadcom, "Broadcom Inc.", AVGO, "Broadcom custom ASICs"]
tags: [ai-infrastructure, semiconductors, custom-asic, private-credit, ai-capex]
description: Custom AI ASIC vendor and capex sentiment lever; central to Google/Anthropic TPU financing, OpenAI's first custom inference chip (Jalapeño, co-designed with Broadcom), and the June 2026 Broadcom guidance gut-check that erased roughly $320B of market value.
created_at: 2026-06-17
timestamp: 2026-06-29T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-06-29", path: research/digest/2026-06-29-digest.md}
  - {title: "ARA model ticket — OpenAI Jalapeño chip", path: research/models/tickets/openai-jalapeno-chip-2026-06.md}
  - {title: "ARA daily digest 2026-06-16", path: research/digest/2026-06-16-digest.md}
  - {title: "ARA daily digest 2026-06-10", path: research/digest/2026-06-10-digest.md}
  - {title: "ARA daily digest 2026-06-05", path: research/digest/2026-06-05-digest.md}
  - {title: "ARA daily digest 2026-05-09", path: research/digest/2026-05-09-digest.md}
---

Broadcom is the custom AI-silicon vendor sitting behind several of the
cycle's most important non-NVIDIA compute stacks. In ARA's 2026 wiki it matters
less as a generic semiconductor company and more as the ASIC / financing hinge
between frontier labs, hyperscalers, and private-credit capital. It is one of
the clearest named entities inside the [[ai-capex]] supercycle's move from
"buy GPUs" to bespoke, debt-financed compute supply chains.

## Why it matters

- **Anthropic's compute-financing stack.** On 2026-06-10, the money behind
  [[anthropic]]'s compute surge came into view: Google reportedly guaranteed
  lease payments backing high-performance compute across five US data centers,
  enabling roughly **$35B of financing**. In that stack, Broadcom designs the
  custom-chip / TPU silicon layer, Google is the hyperscaler backstop, and
  Apollo / Blackstone provide financing. On 2026-06-16, a related
  Anthropic-adjacent report described Broadcom backing a **~$35B custom-chip
  order** for Anthropic, with Apollo / Blackstone financing and a reported
  **20 GW+** targeted compute footprint. Treat the two $35B figures as
  potentially overlapping descriptions of the same financing architecture, not
  additive commitments, until primary terms distinguish them. The exact
  mechanics remain lighter-sourced, but the direction is clear: Anthropic's
  owned-infrastructure pivot runs through Broadcom-class custom silicon, not
  only rented [[nvidia]] GPUs (ARA digests 2026-06-10, 2026-06-16).
- **OpenAI custom-chip financing snag.** A May 2026 Information scoop said the
  [[openai]]-Broadcom Phase-1 custom-chip program, roughly **1.3 GW** of
  data-center capacity, needed Microsoft to commit to buying about **40%** of
  the chips and renting them back to OpenAI. Microsoft had not signed, exposing
  a structural split between OpenAI's specialized-data-center preference and
  Microsoft's architecture-neutral Fairwater strategy. The read-through:
  OpenAI's non-NVIDIA custom rack likely slips toward 2027 unless a replacement
  financing/offtake party appears (ARA digest 2026-05-09).
- **Market gut-check for the AI trade.** On 2026-06-05, Broadcom printed a
  record Q2 (**$22.19B revenue, +48% YoY; AI semis +143% to $10.8B**) but gave
  an in-line, un-raised **~$16B Q3 AI-chip guide**. AVGO fell about **12.6%**
  at the close, erasing roughly **$320B** of market value. That made Broadcom
  the sharpest expression of the "beats but closes lower" pattern that also
  hangs over [[nvidia]]: the market is no longer paying for AI poetry; it wants
  raised guidance.
- **OpenAI's Jalapeño — Broadcom brings OpenAI's first custom chip to production
  (2026-06-24).** [[openai]] unveiled **Jalapeño**, its **first custom AI chip**
  — **inference-only**, "designed from the ground up by OpenAI and brought to
  production with Broadcom" — with **3nm TSMC engineering samples** already
  hand-delivered to Altman/Brockman. Broadcom CEO **Hock Tan** told Bloomberg
  early testing shows **~50% cost savings per inference token vs standard GPUs**
  and told Reuters performance is "on par with NVIDIA Blackwell and Google TPUs"
  (the 50% is Tan's claim, not OpenAI's — OpenAI hedges to "substantially better
  than state-of-the-art"). A reported **9-month AI-assisted design-to-tape-out**,
  Microsoft reportedly guaranteeing **~40% of initial output** (unconfirmed), and
  prototype deployment **late 2026** ramping **2027–2028**. The honest framing is
  **pricing-power erosion for [[nvidia]], not displacement** — inference-only and
  far from scale — but it lands the same week as NVIDIA's open-sourced DFlash
  speculative decoding, two competing answers to dropping inference cost. It also
  resolves the May OpenAI-Broadcom off-take question partially: Microsoft's
  reported 40% guarantee is the offtake party the May scoop said was missing (ARA
  digest 2026-06-29).

## Open questions

- **Who owns the off-take risk?** Custom ASIC projects only finance cleanly when
  a creditworthy party commits to take capacity. In OpenAI's case Microsoft had
  not signed; in Anthropic's case Google and private-credit lenders appear to
  carry more of the stack. The risk owner determines whether the project is
  infrastructure or leverage.
- **ASIC diversification vs NVIDIA lock-in.** Broadcom is the most visible
  merchant-silicon path around NVIDIA scarcity. Does custom silicon materially
  loosen the accelerator bottleneck, or does it merely move the bottleneck to
  power, networking, packaging, and financing?
- **Sentiment transmission.** Broadcom's June 5 reaction showed that custom
  AI-chip guidance can move the whole AI trade. Does AVGO become the capex
  cycle's second sentiment pin after NVDA?

## Changelog

- [2026-06-17] created | custom ASIC and private-credit hinge for Anthropic/OpenAI compute financing
- [2026-06-29] updated | OpenAI Jalapeño first custom inference ASIC co-designed w/ Broadcom, 50% cost saving claim, 9-mo design, MS ~40% output
