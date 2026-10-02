---
slug: microsoft-mai-transcribe-2-streaming-2026-10
title: Microsoft AI releases MAI-Transcribe-2-Streaming, MAI-Voice-2.1 and MAI-Voice-2.1-Flash
company: Microsoft AI
model: MAI-Transcribe-2-Streaming / MAI-Voice-2.1 / MAI-Voice-2.1-Flash
status: released
status_note: |
  **Announced and shipped 2026-10-01 by primary accounts.** @MicrosoftAI
  "Introducing 3 new models: MAI-Transcribe-2-Streaming, MAI-Voice-2.1 and
  MAI-Voice-2.1-Flash" (relayed by @Azure and @satyanadella). @mustafasuleyman:
  "All models are available today in Microsoft Foundry", with Vercel and
  OpenRouter integrations promised.

  **Independent placement.** @ArtificialAnlys: MAI-Transcribe-2-Streaming is #1
  of 38 on AA-WER Streaming at 2.5% final-transcript WER, 0.13s after end of
  speech, ahead of Grok Voice Transcribe 2.0 (2.7%, 0.49s), Muse Voice Transcribe
  (3.1%) and ElevenLabs Scribe v2 Realtime (3.6%). Price $0.54/hour streaming
  ($9 per 1,000 min) — at the higher end of the streaming field; non-streaming
  $0.10/hour.

  **Claim to discount.** Suleyman's "55% faster and 60% cheaper than ElevenLabs"
  does not match AA's own price table, which puts ElevenLabs Scribe v2 Realtime
  at $6.50 per 1,000 min against Microsoft's $9. The comparison may be to a
  different ElevenLabs tier; it is not adopted.
expected: "Released 2026-10-01 in Microsoft Foundry. Open: Vercel/OpenRouter availability, independent evals of MAI-Voice-2.1 / 2.1-Flash (no third-party numbers captured yet), and the basis of the 'cheaper than ElevenLabs' claim."
labels:
  - microsoft
  - speech
  - transcription
  - tts
  - released
verification: confirmed
sources:
  - https://x.com/Azure/status/2105700825020719573
  - https://x.com/mustafasuleyman/status/2105699115602677984
  - https://x.com/mustafasuleyman/status/2105701549527953839
  - https://x.com/ArtificialAnlys/status/2105694108736188894
  - https://x.com/satyanadella/status/2105791561216958853
created_at: 2026-10-02
updated_at: 2026-10-02
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-02
    change: "Created — RELEASED / confirmed. @MicrosoftAI introduced MAI-Transcribe-2-Streaming, MAI-Voice-2.1 and MAI-Voice-2.1-Flash on 2026-10-01 (relayed by @Azure 16:46 UTC and @satyanadella); @mustafasuleyman says all three are available today in Microsoft Foundry. @ArtificialAnlys ranks MAI-Transcribe-2-Streaming #1 of 38 on AA-WER Streaming (2.5% WER at 0.13s) at $0.54/hour. Suleyman's '60% cheaper than ElevenLabs' conflicts with AA's price table and is not adopted. Successor in the MAI speech line to closed [[microsoft-mai-voice-2-flash-2026-07]]."
---

Microsoft's speech stack now has a streaming transcriber at the top of the one
independent leaderboard that measures both accuracy and latency. That is the
substance. The 2.5% vs 2.7% gap over Grok Voice Transcribe 2.0 is small; the
latency gap (0.13s vs 0.49s) is the part that matters for live voice agents.

The price is where the launch framing and the third-party data split. AA calls
it "the higher end of pricing among the leading streaming models", three times
Muse Voice Transcribe. Suleyman's "60% cheaper than ElevenLabs" is not
reconcilable with AA's table as captured, so this ticket records the price, not
the comparison.

The two voice models (MAI-Voice-2.1, 2.1-Flash) shipped with no independent
numbers in this cycle's signal. Predecessor line: [[microsoft-mai-voice-2-flash-2026-07]] (closed).
