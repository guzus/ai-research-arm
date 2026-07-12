---
slug: openai-gpt-live-2026-07
title: OpenAI GPT-Live — full-duplex voice, general rollout
company: OpenAI
model: GPT-Live
status: released
status_note: |
  OpenAI's full-duplex voice architecture, **GPT-Live**, is now **fully
  rolled out to all ChatGPT users globally**. OpenAI's own account
  retweeted the announcement (@athyuttamre, official OpenAI staff):
  "GPT-Live is now fully rolled out to all ChatGPT users globally. We're
  also doubling everyone's voice usage limit..." Distinct shipping
  artifact from the GPT-5.6 text-model family
  ([[openai-gpt-5-6]]) — this is the voice/full-duplex product surface,
  not a text-model release.
expected: null
labels:
  - voice
  - openai
  - released
verification: confirmed
sources:
  - "@OpenAI"
  - "@athyuttamre"
created_at: 2026-07-12
updated_at: 2026-07-12
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-12
    change: "Created — OpenAI's own account RT'd its full-duplex voice architecture GPT-Live as fully rolled out to all ChatGPT users globally, doubling everyone's voice usage limit (@athyuttamre, official OpenAI staff, RT'd by @OpenAI 2026-07-11). Real, general-availability rollout with an official primary → status released, verification confirmed. Distinct from the GPT-5.6 text-model family ([[openai-gpt-5-6]])."
---

**GPT-Live** is OpenAI's full-duplex voice architecture — real-time,
interruptible, low-latency voice conversation distinct from the
turn-based voice mode it replaces. It shipped to **all ChatGPT users
globally** as of 2026-07-11, with OpenAI simultaneously **doubling
everyone's voice usage limit** to absorb the wider rollout.

**Why its own ticket.** GPT-Live is a distinct product surface from the
GPT-5.6 text-model family ([[openai-gpt-5-6]]) — same company, different
shipping artifact, different release cadence.

**Transition triggers:**
- Pricing, API access, or a named successor voice architecture → UPDATE.
- ≥4 weeks past 2026-07-11 with no fresh signal → `closed:
  released-and-aged`.

**Dedup note:** further GPT-Live signal (API, pricing, capability
changes) UPDATES this ticket. GPT-5.6 text-model signal stays on
[[openai-gpt-5-6]].
