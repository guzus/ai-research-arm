---
slug: nvidia-nemotron-openrouter-2026-06
title: NVIDIA puts two Nemotron models free on OpenRouter
company: NVIDIA
model: Nemotron 3
status: released
status_note: |
  **2026-06-21:** NVIDIA made **two Nemotron models available for free on
  OpenRouter** — a **Nemotron 3.5 Content Safety** classifier and a
  **Nemotron 3 Ultra** frontier-tier model. The economic tell is the point:
  **NVIDIA monetizes GPU demand, not API calls**, so shipping capable models at
  zero marginal price pulls inference workloads onto NVIDIA silicon rather than
  competing for token revenue — a distribution play that pressures paid
  closed-API economics from a direction the labs can't easily answer. Surfaced
  via the 2026-06-21 daily digest's Model Releases section; the models are
  usable now (status `released`), but in-window sourcing is a single secondary
  mention without a captured primary NVIDIA/OpenRouter post or model card, so
  verification stays `partial`.

  **2026-06-29:** Spec firm-up — the digest (Interconnects #22 roundup) gives
  **Nemotron 3 Ultra** concrete specs: a **550B LatentMoE** model under the
  **OpenMDW license**, part of a broader open-weight wave (Cohere Command A+ 218B
  MoE now Apache 2.0, Zyphra ZAYA1-74B, Poolside Laguna-M.1, Kimi-K2.7-Code).
  Still a secondary roundup mention without a captured primary NVIDIA model card
  → status stays `released`, verification stays `partial`.
expected: "Live free on OpenRouter (Nemotron 3.5 Content Safety + Nemotron 3 Ultra, the latter a 550B LatentMoE / OpenMDW-licensed model per Interconnects #22); primary NVIDIA/OpenRouter announcement or model card + neutral benchmark placement pending"
labels:
  - nvidia
  - open-weights
  - released
  - inference-economics
verification: partial
sources:
  - "@OpenRouterAI"
  - "@nvidia"
  - https://openrouter.ai/nvidia
created_at: 2026-06-21
updated_at: 2026-06-29
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-21
    change: "Created — NVIDIA put two Nemotron models free on OpenRouter: a Nemotron 3.5 Content Safety classifier and a Nemotron 3 Ultra frontier-tier model. Read as a GPU-demand distribution play (NVIDIA monetizes silicon, not API calls), pressuring paid closed-API economics. Usable now → status released; single secondary in-window mention (2026-06-21 digest) without a captured primary NVIDIA/OpenRouter post or model card → verification partial."
  - ts: 2026-06-29
    change: "Spec firm-up — the 2026-06-29 digest (Interconnects #22 roundup) gives Nemotron 3 Ultra concrete specs: a 550B LatentMoE model under the OpenMDW license, alongside a broader open-weight wave (Cohere Command A+ 218B MoE now Apache 2.0, Zyphra ZAYA1-74B, Poolside Laguna-M.1, Kimi-K2.7-Code). Also relayed: OpenRouter's top-4 broker models are now all Chinese (GLM-5.2 joining DeepSeek models), reflecting the broker market not direct API usage. Fills part of the model-card gap flagged at creation, but still a secondary roundup mention without a captured primary NVIDIA model card → status stays released, verification stays partial."
---

On **2026-06-21**, **NVIDIA** made **two Nemotron models available for free on
OpenRouter** — a **Nemotron 3.5 Content Safety** classifier and a **Nemotron 3
Ultra** frontier-tier model.

**Why its own ticket.** This is a model-release / availability event of the
kind this timeline tracks. It is distinct from NVIDIA's other in-flight items
— the GTC Taipei keynote ([[nvidia-gtc-taipei-2026-06]]) and the Korea
AI-factories buildout ([[nvidia-korea-ai-factories-2026-06]]) — which are
event/infrastructure tickets, not a shipping model surface.

**Why it matters.** NVIDIA's incentive structure is the story: it **earns on
GPU demand, not on API tokens**, so releasing capable models at zero marginal
price is a way to pull inference workloads onto NVIDIA hardware. That pressures
the paid closed-API economics of the labs from an angle they can't easily
match, and it adds to the open-weights momentum the same cycle's
[[zhipu-glm-5-2]] is driving.

**Why `released` / `partial`.** The models are usable now on OpenRouter →
`released`. In-window sourcing is a single secondary mention (the 2026-06-21
daily digest) with no captured primary NVIDIA or OpenRouter post / model card →
`verification: partial`. A primary announcement or neutral benchmark placement
would advance it to `confirmed`.

**Transition triggers:**
- Primary NVIDIA/OpenRouter announcement or model card → UPDATE, advance
  `verification` to `confirmed`.
- A successor Nemotron generation → new ticket; do not reopen this one.
- ≥4 weeks past release, settled into normal coverage → `closed: released-and-aged`.

**Dedup note:** further Nemotron-on-OpenRouter release/benchmark signal UPDATES
this ticket. NVIDIA's GTC keynote and Korea AI-factory infrastructure stay on
their own tickets.
