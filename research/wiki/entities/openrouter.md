---
slug: openrouter
title: OpenRouter
type: entity
aliases: ["OpenRouter", "openrouter.ai", "@OpenRouterAI", "OpenRouter Fusion", "Fusion API"]
tags: [llm-router, inference, infrastructure, capital-markets]
description: LLM-routing API serving 400+ models to 8M+ developers; closed a $113M Series B at $1.3B post-money on 2026-05-30, surfaced Fusion API, and was reportedly acquired by Stripe for over $7B (2026-08-18).
created_at: 2026-06-01
timestamp: 2026-08-18T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-08-18", path: research/digest/2026-08-18-digest.md}
  - {title: "ARA daily digest 2026-08-11", path: research/digest/2026-08-11-digest.md}
  - {title: "ARA daily digest 2026-07-30", path: research/digest/2026-07-30-digest.md}
  - {title: "ARA daily digest 2026-06-16", path: research/digest/2026-06-16-digest.md}
  - {title: "ARA daily digest 2026-06-01", path: research/digest/2026-06-01-digest.md}
  - {title: "OpenRouter Series B announcement", date: 2026-05-30}
---

**OpenRouter** is a unified API surface for **400+ LLMs** routing
developer requests across frontier and open-weights providers. It is
the developer-facing aggregation layer between application code and
the underlying inference market — a counterpart to per-provider SDKs
like the Anthropic SDK or the OpenAI Python client.

## Why it matters

The **2026-05-30 Series B** is the most consequential router-layer
funding signal of the cycle:

- **$113M Series B at $1.3B post-money**, **CapitalG (Alphabet)
  led**, **NVentures (NVIDIA)** participated. Front-paged on Hacker
  News at 395 pts.
- **Weekly token volume jumped 5× to 25T tokens** — on track for **>1
  quadrillion tokens in 2026**.
- **400+ models served to 8M+ developers**.
- **Fusion API surfaced on HN (2026-06-16).** OpenRouter's Fusion API blends
  outputs across multiple LLMs behind one route. It is the router-layer cousin
  of [[sakana-ai]]'s multi-model Marlin bet: instead of picking one winner,
  orchestrate and arbitrate across model diversity. This is also the practical
  product response to [[open-weights]] fragmentation as [[zhipu-glm-5-2]],
  [[moonshot-kimi-k2-7-code]], [[minimax-m3]], and other models compete on
  price, context, and specialty.

- **Stripe reportedly discussed a ~$10B acquisition (2026-07-30).** The
  Information (exclusive) reports **Stripe has discussed paying nearly
  $10B for OpenRouter** — roughly **70x** the routing startup's recent
  annualized revenue, and a massive step up from its **$1.3B** May 2026
  Series B post-money valuation. If it happens, it would be one of the
  largest acquisitions yet in the AI-infrastructure layer and a bet by a
  payments company on owning the developer-facing routing chokepoint
  between applications and the frontier-model market this page tracks.
  Nothing is confirmed by either company (ARA daily digest 2026-07-30).
- **Stripe acquires OpenRouter for over $7B (2026-08-18).** Bloomberg reports
  the payments company is buying the model-routing gateway at **more than 5x**
  its **$1.3B May 2026** valuation — the reported figure **over $7B** (a WSJ
  figure was ~$10B; a ~30% gap between two outlets looks more like a live
  negotiation than a signed deal, with **no Stripe or OpenRouter statement**
  yet). The mechanism that surfaced the deal this cycle: **Stripe already runs
  OpenRouter's billing** and has an **LLM-token billing product in beta** that
  needs a router underneath it. Stratechery framed it as an implicit bet on a
  future market of models and a shot at Aggregation — a payments company
  owning the developer-facing routing chokepoint between applications and the
  frontier-model market this page tracks. It resolves the earlier 2026-07-30
  talks into a concrete print and confirms the routing-layer consolidation
  scramble that began 2026-08-10 (Bloomberg via TechCrunch, The Decoder,
  Stratechery; ARA daily digest 2026-08-18).
- **The Stripe talks trigger a scramble across the routing layer (2026-08-10).**
  The reported ~$10B Stripe talks have set off competition across the routing
  layer: competitor **Requesty says at least 25 companies approached it in
  recent weeks about investment, acquisition or partnership** — an
  industry-wide consolidation signal on the developer-facing routing
  chokepoint, independent of whether the Stripe deal closes. Treat the Requesty
  count as a competitor's self-reported datapoint (ARA daily digest 2026-08-11).

**Why the round matters.** OpenRouter sits between the application
layer and the inference layer, capturing routing economics across
[[anthropic]] / [[openai]] / Google / open-weights providers without
running its own training stack. CapitalG + NVentures as co-investors
align both Google and NVIDIA with a vendor-neutral router — a hedge
against any single frontier lab winning the developer surface.

The round is the developer-tools counterpart to the [[ai-capex]]
supercycle's infrastructure spend: as inference moves to a quadrillion-
token annual scale, the routing layer captures the optionality value
across providers. Inference startups (Fireworks, Baseten, Modal,
Together) face NVIDIA-rental margin pressure on the supply side;
OpenRouter monetizes from the demand side.

## Open questions

- **Routing-margin durability.** Per-call routing fees compress as
  developers route directly to per-provider APIs they understand.
  Does the 25T tokens/week volume hold as the largest customers go
  direct?
- **NVIDIA × CapitalG co-investment.** Two strategic investors who
  *compete on the underlying inference stack* (Google TPU vs NVIDIA
  GPU) is an unusual cap-table shape. What is the actual governance
  cost of that pairing for routing-policy neutrality?
- **Provider mix.** "400+ models" implies long-tail open-weights
  coverage. How much of the >1Q-token run rate is open-weights vs
  closed-frontier — and how does that shift as DeepSeek V4 Pro's
  75% price cut compounds?
- **Fusion quality.** Does blending improve answer quality enough to justify
  latency and attribution complexity, or is it mostly a way to sell model
  optionality when the underlying leaderboard is unstable?
