---
slug: moonshot-kimi-k2-7-code
title: Moonshot Kimi K2.7 Code — open coding model
company: Moonshot AI
model: Kimi K2.7 Code
status: released
status_note: |
  **Moonshot AI** launched **Kimi K2.7 Code**, an **open** coding model that,
  per The Decoder (2026-06-13), **undercuts GPT-5.5 and Claude by up to ~12× on
  price per token** while staying competitive on performance. Open weights are
  shipping — an **Unsloth Kimi-K2.7-Code-GGUF** quantization was being uploaded
  to Hugging Face this cycle. The model lane is distinct from Moonshot's funding
  story ([[moonshot-funding-2026-06]]). Part of the Chinese open-weights surge
  alongside [[zhipu-glm-5-2]], [[minimax-m3]], [[alibaba-qwen-3-7-plus]].
expected: "Open weights / GGUF quantizations rolling out on Hugging Face"
labels:
  - open-weights
  - china
  - coding
  - moonshot
  - released
verification: partial
sources:
  - https://the-decoder.com/moonshots-open-model-kimi-k2-7-code-undercuts-gpt-5-5-and-claude-by-up-to-12x-on-price-per-token/
  - https://www.reddit.com/r/LocalLLaMA/comments/1u4m7i6/unsloth_kimik27codegguf/
created_at: 2026-06-14
updated_at: 2026-06-14
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-14
    change: "Created — Moonshot AI launched Kimi K2.7 Code, an open coding model that undercuts GPT-5.5 and Claude by up to ~12x on price per token while staying competitive (The Decoder, 2026-06-13); open weights shipping (Unsloth K2.7-Code-GGUF uploading to Hugging Face). Real, available artifact → status released; corroborated by The Decoder + community GGUF uploads but no captured primary Moonshot URL/model card → verification partial. Distinct artifact from Moonshot's funding round ([[moonshot-funding-2026-06]]); sits in the Chinese open-weights surge with [[zhipu-glm-5-2]], [[minimax-m3]], [[alibaba-qwen-3-7-plus]]"
---

**Kimi K2.7 Code**, from **Moonshot AI**, is an **open coding model** that
— per The Decoder (2026-06-13) — **undercuts GPT-5.5 and Claude by up to
~12× on price per token** while remaining competitive on performance. Open
weights are shipping: an **Unsloth Kimi-K2.7-Code-GGUF** quantization was
uploading to Hugging Face this cycle, putting the model in reach of local
runners.

**Why it's its own ticket.** This is a **model release** — distinct from
Moonshot's separate **funding** storyline ([[moonshot-funding-2026-06]]),
which tracks the lab's ~$30B valuation target. The funding ticket's own
dedup note calls out that Kimi model releases get their own ticket; this is
that ticket.

**Why `released` / `partial`.** The model is a real, available artifact
(open weights + community quantizations), so the lifecycle is `released`.
`verification` stays `partial`: it is corroborated by The Decoder and the
community GGUF uploads, but no **primary Moonshot announcement or model
card** was captured in-window — that would advance it to `confirmed`.

**Context.** It lands in the **Chinese open-weights surge** alongside
[[zhipu-glm-5-2]], [[minimax-m3]], and [[alibaba-qwen-3-7-plus]], and the
price-per-token undercut sharpens the cost pressure on frontier US labs —
a theme amplified this week by the open-weights/sovereignty discourse
around the Anthropic export-control shutdown
([[anthropic-fable-mythos-export-control-2026-06]]).

**Transition triggers:**
- A primary Moonshot model card / benchmark page → UPDATE, advance
  `verification` to `confirmed`.
- A successor (K2.x Code) → new ticket; do not reopen this one.
- ≥4 weeks past release, settled into normal coverage → `closed: released-and-aged`.

**Dedup note:** further Kimi K2.7 Code release/benchmark/weights signal
UPDATES this ticket. Moonshot funding/valuation signal stays on
[[moonshot-funding-2026-06]].
