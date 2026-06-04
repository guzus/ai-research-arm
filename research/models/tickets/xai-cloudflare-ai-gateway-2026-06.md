---
slug: xai-cloudflare-ai-gateway-2026-06
title: Cloudflare × xAI — Grok (LLM + image / audio / video) live on Cloudflare AI Gateway
company: xAI / Cloudflare
model: Grok
status: confirmed
status_note: |
  Multiple independent relays (2026-06-03 → 06-04) describe an @xai /
  @Cloudflare partnership putting Grok models — text, image, audio and
  video generation, including a Grok Imagine Video 1.5 Preview demo — on
  Cloudflare's AI Gateway, so developers can call and pay for Grok through
  Cloudflare without provisioning a separate xAI API key. A distribution /
  reach play, not a new model capability. No first-party @Cloudflare or
  @xai post was captured in-snapshot (a `from:Cloudflare` lookup returned
  nothing in-window), so specifics — model list, pricing pass-through,
  GA vs. preview — are report-grade pending the official blog/handle.
expected: null
labels:
  - partnership
  - distribution
  - grok
  - inference-gateway
verification: partial
sources:
  - https://x.com/AiToolsRecap/status/2062392993164972480
  - https://x.com/mmalss2525/status/2062374199348613292
created_at: 2026-06-04
updated_at: 2026-06-04
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-04
    change: "Created — relays (2026-06-03 → 06-04) report an xAI × Cloudflare partnership making Grok's LLM, image, audio and video models callable and billable through Cloudflare AI Gateway (no separate xAI key), with a Grok Imagine Video 1.5 Preview demo. Multi-relay but no captured first-party Cloudflare/xAI primary → status confirmed-report, verification partial"
---

Independent relays on 2026-06-03 → 06-04 describe a **partnership between
xAI and Cloudflare** that makes **Grok models — text, image, audio and
video generation — available directly through Cloudflare's AI Gateway**.
The pitch is friction reduction: developers can call and pay for Grok via
Cloudflare without provisioning a separate xAI API key, and a demo clip
showcased **Grok Imagine Video 1.5 Preview**.

This is a **distribution event, not a capability release** — it puts Grok
in front of Cloudflare's developer base with lower integration friction
and routes billing through Cloudflare. It continues the "model layer
racing to distribution + price" thread: after DeepSeek's price cuts (see
[deepseek-v4-pro-price-cut-2026-05](./deepseek-v4-pro-price-cut-2026-05.md))
and Grok Composer's cheap input pricing, getting Grok onto a major
edge/gateway is about reach.

**Why verification is `partial`:** the substance is consistent across
multiple independent relays and is mundane/plausible (Cloudflare already
runs an AI Gateway product), but no first-party @Cloudflare or @xai post
was captured in-snapshot — a `from:Cloudflare` search returned nothing
in-window. Treat the model list, pricing pass-through and GA-vs-preview
status as report-grade.

**Transition triggers:**
- Official @Cloudflare / @xai blog or docs confirming the integration →
  UPDATE, advance verification to `confirmed`, refine the model/pricing
  detail.
- Other gateways or labs respond, or Grok gateway pricing undercuts
  incumbents → UPDATE.
- ≥4 weeks once GA and settled into normal coverage → `closed:
  released-and-aged`.

**Dedup note:** new signal about Grok-on-Cloudflare-AI-Gateway (model
list, pricing, GA) UPDATES this ticket. A separate xAI Grok model release
gets its own ticket.
