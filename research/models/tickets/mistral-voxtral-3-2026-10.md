---
slug: mistral-voxtral-3-2026-10
title: "Mistral releases Voxtral 3 (Transcribe + Speech) and a voice agents API with a LiveKit-based SDK"
company: "Mistral AI"
model: "Voxtral 3"
status: released
status_note: |
  **Primary announcement.** @MistralAI (2026-10-20 16:00 UTC): "Introducing Voxtral 3:
  state-of-the-art Transcribe and Speech models powering Mistral's new voice agents API."
  The thread adds a voice agent SDK built on LiveKit: Transcribe listens, a reasoning
  model thinks and calls tools, and Speech replies, streamed as one pipeline.

  **In use.** By 2026-10-21 @MistralAI was retweeting a user (@noctus91) testing the new
  Voxtral transcription model on a 135-year-old noisy French recording, so the model is
  reachable by outside users, not just announced.

  The "state-of-the-art" claim is Mistral's own. No independent WER or speech-quality
  numbers, pricing or open-weights status were captured in this cycle's signal.
expected: "Released 2026-10-20 (voice agents API + SDK). Open: pricing, whether Voxtral 3 ships open weights like earlier Voxtral releases, and independent transcription/TTS benchmarks."
labels:
  - mistral
  - speech
  - voice-agents
  - transcription
  - tts
verification: confirmed
sources:
  - "https://x.com/MistralAI/status/2112574615318876178"
  - "https://x.com/MistralAI/status/2112574627381936345"
  - "https://x.com/MistralAI/status/2112574629181116644"
  - "https://x.com/MistralAI/status/2112807891094716723"
created_at: 2026-10-21
updated_at: 2026-10-21
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-21
    change: "Created — RELEASED / confirmed. @MistralAI (2026-10-20 16:00 UTC) introduced Voxtral 3, Transcribe and Speech models powering a new Mistral voice agents API, plus a LiveKit-based voice agent SDK that streams transcribe -> reasoning model with tool calls -> speech as one pipeline. Mistral's account retweeted an outside user testing the new transcription model on 2026-10-21, so it is live. Benchmark claims are company-stated; pricing and weights status not captured."
---

Voxtral 3 is Mistral's move from selling speech models to selling a voice-agent
stack. The model pair (Transcribe in, Speech out) wraps a reasoning model that can
call tools, and the SDK runs on LiveKit, the transport many voice-agent teams
already use.

That puts Mistral in the same lane as OpenAI's realtime/voice APIs, ElevenLabs
([[elevenlabs-eleven-v4-2026-09]]), xAI's Grok Voice 3 ([[xai-grok-voice-3-2026-10]])
and Microsoft's MAI voice models ([[microsoft-mai-transcribe-2-streaming-2026-10]]).
The open question is price and whether weights follow, since earlier Voxtral
releases were open and that was their main draw.
