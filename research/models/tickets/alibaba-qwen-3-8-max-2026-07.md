---
slug: alibaba-qwen-3-8-max-2026-07
title: Qwen3.8-Max Preview
company: Alibaba
model: Qwen3.8-Max
status: in-testing
status_note: |
  Alibaba released a preview of Qwen3.8-Max — 2.4T parameters, MoE,
  1M-token context, coding/agent focus — with open weights promised but
  not yet shipped. Multiple independent accounts corroborated the same
  specifics the same morning.
expected: "Open weights promised, no date given"
labels:
  - frontier-model
  - moe
  - preview
verification: confirmed
sources:
  - https://x.com/Leoskie_L/status/2079484883382993389
  - "@jarvana_sv"
  - "@aiseomastery"
created_at: 2026-07-21
updated_at: 2026-07-21
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-21
    change: Created — Alibaba released Qwen3.8-Max Preview (2.4T params, MoE, 1M context), with open weights promised but not yet released.
---

Alibaba released a preview of Qwen3.8-Max, described consistently across
several independent accounts as a 2.4-trillion-parameter MoE model with a
1M-token context window and a coding/agent focus. Open weights were
promised but have not shipped yet, so this is filed `in-testing` rather
than `released`.

This is a distinct, larger/newer artifact from the existing
`alibaba-qwen-3-7-plus` ticket (Qwen3.7-Plus) — different model name and
generation, not merely a version-number correction, so it gets its own
ticket per the dedup contract rather than an update to the 3.7-Plus
entry. A separate, weaker single-source claim that "two ex-Qwen
researchers" are about to open-weight their own "Qwen 3.8" surfaced the
same day (via @NielsRogge); given it's unconfirmed and plausibly a
garbled description of this same Alibaba release, it's noted here rather
than filed as its own ticket.
