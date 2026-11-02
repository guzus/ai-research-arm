---
slug: openai-chatgpt-codex-token-allowance-2026-11
title: "ChatGPT and Codex move to a shared token-based allowance on Plus, Pro and Business from December (reported)"
company: OpenAI
model: null
status: confirmed
status_note: |
  **Single secondary source describing an OpenAI announcement.** @FeildenStuart (2026-11-02 15:39 UTC): "From
  December, ChatGPT and Codex will share a token-based allowance on Plus, Pro and Business. Instant chat won't
  count. The announcement gives no allowance sizes or model rates."

  Context: @eth_ansh (15:57 UTC) refers to "six rule changes in one week" and Codex limits on the $200 plan
  "flipping twice". That suggests recent churn in Codex plan limits but does not confirm the December change.

  `confirmed` because the post describes a dated company announcement. `unverified` because no OpenAI post
  or help-center page was captured.
expected: "December 2026 (reported). Allowance sizes and per-model token rates not yet published."
labels:
  - openai
  - chatgpt
  - codex
  - pricing
  - plan-limits
  - unverified
verification: unverified
sources:
  - "https://x.com/FeildenStuart/status/2117280400389099638"
  - "https://x.com/eth_ansh/status/2117285033795010896"
created_at: 2026-11-02
updated_at: 2026-11-02
closed_at: null
closed_reason: null
history:
  - ts: 2026-11-02
    change: "Created — CONFIRMED / unverified. @FeildenStuart (2026-11-02 15:39 UTC) reports an announcement that from December ChatGPT and Codex will share one token-based allowance on Plus, Pro and Business, with Instant chat excluded; no allowance sizes or model rates given. @eth_ansh separately describes repeated Codex limit changes on the $200 plan this week. No OpenAI primary captured."
---

OpenAI currently meters ChatGPT messages and Codex usage separately. A shared token allowance would make
the two products draw on one budget, priced by tokens rather than by messages or tasks. Whether it is a
cut depends on the allowance sizes and per-model rates, which the reported announcement does not give.

This matters for Codex-heavy users. A frontier model such as GPT-6 Astra or the reported GPT-6.2 Astra
([[openai-gpt-6-2-astra-2026-11]]) would presumably burn the shared budget faster than Instant chat.

**Transition triggers:** OpenAI post or help-center page → verification `confirmed`; allowance numbers
published → history update; December rollout → `released`.
