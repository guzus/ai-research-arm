---
slug: elevenlabs-eleven-v4-2026-09
title: Eleven v4 and v4 Turbo — ElevenLabs' new flagship TTS, #1 on Artificial Analysis Provider Voice
company: ElevenLabs
model: Eleven v4 / Eleven v4 Turbo
status: released
status_note: |
  **Shipped 2026-09-28.** @tadaspetra, posting in ElevenLabs' voice (14:51 UTC):
  "Today we release two new models: **Eleven V4** and **Eleven V4 Turbo**. Eleven
  V4 is the flagship model giving the highest quality voices… Eleven V4 Turbo is
  the faster model, which trades a little bit in performance for speed. Great for
  realtime use cases."

  **Independent measurement landed the same hour, which is unusual and is the
  reason verification is `confirmed` rather than `partial`.** @ArtificialAnlys
  (14:27 UTC) published numbers:

  - **Provider Voice TTS Arena: #1**, Elo **1,319** (±19) over 1,674 appearances,
    ahead of Cartesia Sonic 3.6 (1,276) and Google Gemini 3.8 Flash TTS (1,267);
    #1 in all four sub-categories.
  - **Controlled Voice: #2**, Elo **1,157** (±16), behind **Alibaba
    Qwen-Audio-3.1-TTS-Plus (1,178)** and well ahead of Eleven v3 (1,073).
  - **Pronunciation Robustness: 91.7%** — the highest Artificial Analysis has
    measured — vs Gemini 3.8 Flash TTS 89.5% and Eleven v3 85.6%.
  - **Cost: $80 per 1M characters**, vs Sonic 3.6 at $49 and **Gemini 3.8 Flash
    TTS at $16.49**.
  - **Speed: 73.4 characters/sec** of generation, up from 42.5 for v3.
  - Language coverage **90+**, up from 70+ in v3.

  **The price line is the honest read, not the leaderboard line.** Eleven v4 wins
  Provider Voice while costing **~4.9x** Google's Gemini 3.8 Flash TTS
  ([[google-gemini-3-8-flash-tts-2026-09]]), which itself sits 52 Elo behind.
  ElevenLabs is defending a quality premium against a hyperscaler pricing the
  same modality as a commodity, and it loses Controlled Voice to Alibaba
  outright. Whether the premium holds is the substantive question.

  **What is NOT established in-window:** no model card, parameter count,
  architecture, latency figures for v4 Turbo specifically, availability tiers, or
  any first-party post from @elevenlabsio captured this cycle. The release
  statement is from an ElevenLabs staff account, not the corporate handle.

  **Adjacent ticket.** [[elevenlabs-secondary-sale-2026-07]] tracks the $22B
  employee-share-sale valuation; this is the product artifact under it.
expected: "Both models released today. Open: a first-party corporate announcement and model card, v4 Turbo's own benchmark placement and latency numbers (Artificial Analysis measured v4, not Turbo), pricing for Turbo, and whether the $80/1M-character premium survives Gemini 3.8 Flash TTS at $16.49."
labels:
  - elevenlabs
  - tts
  - voice
  - released
  - benchmark
verification: confirmed
sources:
  - https://x.com/tadaspetra/status/2104584846005637348
  - https://x.com/ArtificialAnlys/status/2104578736687653293
created_at: 2026-09-28
updated_at: 2026-09-28
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-28
    change: "Created — RELEASED. ElevenLabs shipped Eleven v4 (flagship) and Eleven v4 Turbo (speed-optimised) on 2026-09-28, announced first-person by ElevenLabs' @tadaspetra. Artificial Analysis published independent measurements the same hour: #1 on Provider Voice TTS Arena at 1,319 Elo, #1 on Pronunciation Robustness at 91.7% (their highest measured), #2 on Controlled Voice behind Alibaba's Qwen-Audio-3.1-TTS-Plus, 90+ languages, 73.4 chars/sec, $80 per 1M characters. Status released, verification confirmed — a vendor release plus a same-day third-party leaderboard placement clears the bar even though the corporate handle was not captured. The load-bearing caveat is priced, not quality: v4 wins Provider Voice at ~4.9x the cost of Google's Gemini 3.8 Flash TTS ([[google-gemini-3-8-flash-tts-2026-09]]), which trails by 52 Elo, and loses Controlled Voice to Alibaba. No model card, parameter count, architecture or Turbo-specific numbers in-window."
---

Eleven v4 takes the top of Artificial Analysis' Provider Voice arena on the day
it ships, with the highest pronunciation-robustness score that leaderboard has
recorded. On quality alone this is a clean generational step over v3: +246 Elo
on Provider Voice, +6.1 points on pronunciation, 1.7x the generation speed, and
twenty more languages.

The pricing table is where the story gets interesting. At $80 per million
characters, v4 costs roughly five times Google's Gemini 3.8 Flash TTS, which
sits 52 Elo behind it and 2.2 points behind on pronunciation. Cartesia's Sonic
3.6 splits the difference at $49. For the assistant and customer-service
workloads that dominate TTS volume, a 4% Elo edge at 5x the price is a hard sell
— which is precisely why ElevenLabs shipped a Turbo variant alongside the
flagship and led its own announcement with realtime use cases.

The Controlled Voice result is the one ElevenLabs did not win, and it is worth
noting who took it: Alibaba's Qwen-Audio-3.1-TTS-Plus. When every model must use
the same custom voice, the specialist's advantage narrows and a Chinese
open-weight-adjacent line comes out ahead.

Nothing here is a capability claim from ElevenLabs that this desk had to take on
faith — the numbers are a third party's. What is missing is everything a model
card would carry, plus any measurement of v4 Turbo at all.
