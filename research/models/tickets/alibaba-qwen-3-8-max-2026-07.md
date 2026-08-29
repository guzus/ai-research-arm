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

  **2026-07-22:** @TimesOfAI_ reports the full open-weight release
  (including model weights and benchmark results) is "expected soon,"
  consistent with the preview-then-weights pattern already noted here — no
  new date given. A skeptical take (@Kozh_Crypto) flags that as of this
  cycle there is still no benchmark table, model card, or license attached
  to the preview, just a tweet and a preview endpoint, and notes the timing
  (2 days after Moonshot's Kimi K3 open-weight ship) as competitive
  positioning rather than a finished release. Status stays `in-testing`;
  verification stays `confirmed` (the preview's existence isn't in
  question; the skepticism is about the *strength* of the claims, which
  the ticket already treats as preview-not-release).
expected: "Open weights promised, expected 'soon' per 2026-07-22 signal, no firm date given"
labels:
  - frontier-model
  - moe
  - preview
verification: confirmed
sources:
  - https://x.com/Leoskie_L/status/2079484883382993389
  - "@jarvana_sv"
  - "@aiseomastery"
  - "@TimesOfAI_"
  - "@Kozh_Crypto"
created_at: 2026-07-21
updated_at: 2026-07-22
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-21
    change: Created — Alibaba released Qwen3.8-Max Preview (2.4T params, MoE, 1M context), with open weights promised but not yet released.
  - ts: 2026-07-22
    change: "Full open-weight release reported 'expected soon' (@TimesOfAI_), no firm date; skeptical read (@Kozh_Crypto) notes no benchmark table/model card/license yet, just a preview endpoint, 2 days after Kimi K3's open-weight ship. Status stays in-testing; verification stays confirmed."
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
