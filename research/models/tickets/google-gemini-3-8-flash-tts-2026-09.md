---
slug: google-gemini-3-8-flash-tts-2026-09
title: Gemini 3.8 Flash TTS and Flash-Lite TTS — Google's voice-design text-to-speech models, shipped
company: Google / DeepMind
model: Gemini 3.8 Flash TTS / Gemini 3.8 Flash-Lite TTS
status: released
status_note: |
  Shipped 2026-09-23 ~15:25 UTC across @GoogleAI, @GoogleDeepMind and
  @OfficialLoganK. Two models, split by job: **Flash TTS** for bespoke vocal
  personas with line-by-line control (gaming, audiobooks, podcasts); **Flash-Lite
  TTS** for cost-efficient scale with automatic tone/pacing adjustment (real-time
  voice agents, bulk dubbing).

  Capabilities as stated by Google: 2,000+ production-ready voices, custom voice
  design from a prompt, voice replication from ~30s of audio behind a consent
  check, 100+ languages, line-by-line delivery direction with inline cues
  (`<laughs>`, `<sigh>`, backchannels like `|mhm|`), two-speaker scenes, and
  hours of consistent glitch-free audio. Every clip carries SynthID.

  Availability: both models in the Gemini API and Google AI Studio from launch
  day; consumers get Flash TTS in Gemini Notebook and Flash-Lite TTS in Google
  Vids; Gemini Enterprise "coming soon." @OfficialLoganK adds a new AI Studio
  experience and a **lower cost than the previous 3.1 Flash TTS model**.

  Benchmark claims are Google's own and should be read as such: #1 on Hume AI's
  Voice Design benchmark, #1 and #2 on Hume Quality, top of Voice Arena in six
  languages. Independent hands-on within hours from @simonw, who called them
  "super-cheap" and built multi-voice conversations with them — corroborating
  availability and price, not the leaderboard positions.
expected: "Released. Gemini Enterprise availability still 'coming soon'; no date given."
labels:
  - google
  - deepmind
  - tts
  - audio
  - released
verification: confirmed
sources:
  - https://x.com/GoogleAI/status/2102781694730285427
  - https://x.com/GoogleAI/status/2102781697372934481
  - https://x.com/GoogleDeepMind/status/2102781530867126505
  - https://x.com/GoogleDeepMind/status/2102781533274734801
  - https://x.com/OfficialLoganK/status/2102785495726219305
  - https://x.com/OfficialLoganK/status/2102786116453880283
  - https://x.com/_philschmid/status/2102781788531667322
  - https://x.com/simonw/status/2102861892549279922
created_at: 2026-09-24
updated_at: 2026-09-24
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-24
    change: "Created — RELEASED. Google shipped Gemini 3.8 Flash TTS and Gemini 3.8 Flash-Lite TTS on 2026-09-23, announced by @GoogleAI, @GoogleDeepMind and @OfficialLoganK. Flash TTS targets bespoke voice design with line-by-line delivery control; Flash-Lite TTS targets cost-efficient real-time and bulk use. Stated capabilities: 2,000+ ready voices, prompt-designed custom voices, ~30s voice replication behind a consent check, 100+ languages, inline delivery cues and two-speaker scenes, SynthID watermarking on every clip. Live day one in the Gemini API and AI Studio, plus Gemini Notebook (Flash) and Google Vids (Flash-Lite); Gemini Enterprise coming soon. Priced below the prior 3.1 Flash TTS model per @OfficialLoganK. Verification confirmed on company-primary posts. Google's own leaderboard claims (#1 Hume Voice Design, #1/#2 Hume Quality, top of Voice Arena in 6 languages) are recorded as vendor claims; independent same-day hands-on from @simonw corroborates availability and low cost only. Distinct from [[google-gemini-3-8-live-2026-09]] (live-audio conversational models) and [[gemini-3-5-transcribe-2026-08]] (speech-to-text); this is the synthesis side of the same audio push."
---

Google now has the full audio stack shipped under one version number. Transcribe
handles speech-in ([[gemini-3-5-transcribe-2026-08]]), Live handles full-duplex
conversation ([[google-gemini-3-8-live-2026-09]]), Lyria handles music
([[google-lyria-3-5-2026-07]]), and 3.8 Flash TTS/Flash-Lite TTS now handle
speech-out. Logan Kilpatrick made the point explicitly — "from TTS, to Live, to
Lyria, to Translate, to Transcribe" — and the strategic content of this release
is the completeness, not any single capability.

The split between the two models is the interesting design choice. Flash TTS
gives the caller line-by-line authority: style directives, `<laughs>`, `|mhm|`
backchannels, two-speaker scenes. Flash-Lite TTS deliberately takes that
authority away and adjusts tone and pacing automatically, which is what a
real-time voice agent actually needs — an agent cannot stop to direct its own
delivery. Pricing follows the same logic, with Flash-Lite aimed at bulk dubbing
and high-volume agents and the whole line priced under the previous 3.1 Flash
TTS.

Voice replication is the part with policy surface. Cloning from ~30 seconds of
audio is cheap enough to be abused; Google's answer is a consent check on
replication plus SynthID on every generated clip. Whether the consent check is
an attestation or a verification is not stated in this cycle's signal, and that
distinction is the whole safeguard.

The leaderboard claims are Google's. Hume runs the Voice Design benchmark Google
says it tops, and a vendor reporting its own #1 on a third-party board is a
claim to verify rather than a fact to record. What is independently established
within hours is narrower and still meaningful: @simonw had multi-voice
conversations working the same evening and called the models super-cheap.
