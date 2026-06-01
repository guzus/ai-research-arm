---
slug: openrouter
title: OpenRouter
type: entity
aliases: ["OpenRouter", "openrouter.ai", "@OpenRouterAI"]
tags: [llm-router, inference, infrastructure, capital-markets]
summary: LLM-routing API serving 400+ models to 8M+ developers; closed a $113M Series B at $1.3B post-money on 2026-05-30 (CapitalG led, NVentures participated); weekly volume jumped 5× to 25T tokens, on track for >1 quadrillion tokens in 2026.
created_at: 2026-06-01
updated_at: 2026-06-01
sources:
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
