---
slug: perplexity
title: Perplexity
type: entity
aliases: ["Perplexity AI", "Perplexity Computer"]
tags: [search, agents, ai-application, funding]
description: AI search-and-agent company behind the Perplexity Computer workflow agent, which drove annualized revenue from under $250M at the start of 2026 past $750M; NVIDIA is reported in talks to invest at a $30B+ valuation (2026-08-25).
created_at: 2026-08-25
timestamp: 2026-08-26T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-08-26", path: research/digest/2026-08-26-digest.md}
  - {title: "ARA daily digest 2026-08-25", path: research/digest/2026-08-25-digest.md}
  - {title: "ARA model ticket — NVIDIA/Perplexity investment talks", path: research/models/tickets/nvidia-perplexity-investment-2026-08.md}
  - {title: "ARA daily digest 2026-08-13", path: research/digest/2026-08-13-digest.md}
---

**Perplexity** is the AI search-and-agent company whose **Perplexity Computer**
workflow-automation agent has become its revenue engine — and whose growth
trajectory just landed it in [[nvidia|NVIDIA]]'s crosshairs as an equity
investment target.

## Why it matters

- **NVIDIA opens equity talks above $30B (2026-08-25).** Per The Information,
  NVIDIA is in **talks to invest in Perplexity at a valuation above $30B** — a
  **>50% step-up from the last round** — in a deal that "may even include a new
  technology licensing agreement." The reported business justification is
  revenue: **annualized revenue up from under $250M at the start of 2026 to
  over $750M**, attributed largely to adoption of **Perplexity Computer**. Two
  caveats govern the sourcing: circulating revenue figures differ by roughly
  4×, so **the valuation is the only sourced number**; and the deal is **talks,
  not a signed round**, with no term sheet or company statement (The
  Information via Twitter/X; ARA daily digest 2026-08-25).
- **The position it would complete.** Inside a single week NVIDIA is reported
  to have licensed [[poolside|Poolside]]'s training stack, raised AI-server
  prices ~17%, and now to be buying equity in an application-layer company
  that rents its compute — the "owning both sides of the invoice" structure
  this wiki trades as the [[ai-capex]] financing pattern. If the revenue
  figure holds, it is also the sharpest datapoint yet on **agent products
  converting to revenue**, not just model capability.
- **The Nemotron precedent (2026-08-13).** NVIDIA already distributes through
  Perplexity: **Nemotron 3.5 Lightning went live on the Perplexity Agent API**
  at $0.0115/$0.17 per million tokens — the cheapest widely-distributed
  agent-model rate card of the cycle — making Perplexity the routing-layer
  outlet for NVIDIA's open-weights play (ARA daily digest 2026-08-13). See
  [[open-weights]] and the analogous routing-layer repricing tracked on
  [[openrouter]].

## Open questions

- **The revenue gap.** $250M → $750M annualized in ~7 months is the entire
  justification for a 50–60% valuation step-up, and it is as yet unsourced —
  the valuation is the only firm number on the table.
- **A technology license over a check?** The Information's framing has the
  conversation "moved off a license-and-hire and onto a check" — whether the
  equity stake carries a licensing component (as in the Poolside structure)
  is unresolved.

## NVIDIA co-launches the local agent runtime — and gifts a DGX Station (2026-08-26)

- **"Portable Computer" ships: orchestrator, subagents and harness all local on
  DGX Spark (2026-08-26).** Perplexity and [[nvidia|NVIDIA]] shipped
  **Portable Computer**, an agent stack running **entirely locally on DGX
  Spark** — orchestrator, subagents and harness — with the shipping model list
  in the **27B-class tier (PPLX 27B, Qwen 3.8 27B, Nemotron 3.5 Lightning
  "coming soon")**. The commercial read is explicit: this is **"the good-enough
  local tier as a supported product, not frontier capability leaving the
  cloud"** — the local-inference answer to the data-residency demand side of
  [[ai-capex]], and the same distribution logic as the Nemotron-on-Agent-API
  precedent on this page (ARA daily digest 2026-08-26).
- **NVIDIA gifted Perplexity a DGX Station (2026-08-26).** Per Perplexity's
  CEO, **NVIDIA gifted the company a DGX Station** the same day — a gesture
  datapoint on the equity-talk relationship (see the 2026-08-25 >$30B entry
  above), consistent with NVIDIA deepening the customer relationship beyond a
  check (ARA daily digest 2026-08-26).