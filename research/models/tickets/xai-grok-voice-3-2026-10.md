---
slug: xai-grok-voice-3-2026-10
title: "Grok Voice 3.0 — speech-to-speech model tops Artificial Analysis, same $0.08/min price"
company: "SpaceX / xAI"
model: "Grok Voice 3.0"
status: released
status_note: |
  **Official.** @SpaceXSI (2026-10-14 17:04 UTC): "Introducing Grok Voice 3.0, the
  world's most intelligent speech-to-speech model. It excels at resolving customer
  calls, responds in under a second, and costs less than other frontier models."

  **Details from relays** (consistent across @DevKazu42, @XFreeze and @Sdyahaya_;
  not read from a primary page in this signal):
  - Artificial Analysis Speech-to-Speech Index 86.9, #1. GPT-Live-1 (Astra) is 83.2
    and Gemini 3.8 Live is 82.6.
  - Mean time to first audio 0.81s, against 1.34s for GPT-Live-1. Grok Voice 2.0 was
    0.70s, so 3.0 is slightly slower than its predecessor.
  - τ-Voice (noisy and accented support calls) 71.6%, #2 behind GPT-Live-1 at 74.5%.
  - Blind-preference Elo #3 on AA. #1 there is Gemini 3.1 Flash Live.
  - Price unchanged from 2.0 at $0.08/min. `grok-voice-latest` aliases moved to 3.0
    automatically, with no API change.
  - Deployed in Tesla vehicles and Grok Bot voice mode. Starlink's call centre is
    cited at ~20K calls/day, ~70% resolved without a human.

  **Status `released`.** The model is live behind the existing API alias and in
  shipping products.
expected: "Released 2026-10-14. Open: an Artificial Analysis primary page for the 86.9 figure, the latency regression versus 2.0, and non-English quality."
labels:
  - xai
  - spacex
  - voice
  - speech-to-speech
  - released
verification: confirmed
sources:
  - "https://x.com/SpaceXSI/status/2110416580899168305"
  - "https://x.com/XFreeze/status/2110422583317524876"
  - "https://x.com/XFreeze/status/2110686405085261896"
  - "https://x.com/DevKazu42/status/2110700656415945143"
  - "https://x.com/Sdyahaya_/status/2110677945819783440"
created_at: 2026-10-15
updated_at: 2026-10-15
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-15
    change: "Created — RELEASED / confirmed. @SpaceXSI announced Grok Voice 3.0 on 2026-10-14 17:04 UTC as 'the world's most intelligent speech-to-speech model', citing customer-call resolution, sub-second response and lower cost than other frontier models. Relays agree on the specifics: AA Speech-to-Speech Index 86.9 (#1, ahead of GPT-Live-1 Astra at 83.2 and Gemini 3.8 Live at 82.6); 0.81s mean time to first audio (GPT-Live-1 1.34s; Grok Voice 2.0 0.70s, so a small latency regression); τ-Voice 71.6% (#2 behind GPT-Live-1 at 74.5%); #3 on AA blind-preference Elo; price unchanged at $0.08/min; the 'grok-voice-latest' alias moved to 3.0 with no API change. It also powers voice in Tesla vehicles and Grok Bot. This is a new artifact, not an update: the predecessor [[xai-grok-voice-2-2026-08]] is closed (released-and-aged) and stays untouched. Its closure note anticipated a Grok Voice 3 successor. Competitor context: [[openai-gpt-live-1-api-2026-09]]."
---
Successor to [[xai-grok-voice-2-2026-08]], which is closed and untouched.

The headline index win holds up less well on the details. Grok Voice 3.0 leads
the composite AA index. It is second on the hardest task-specific benchmark
(τ-Voice, behind GPT-Live-1), third on human preference, and slightly slower to
first audio than its own predecessor. Price is unchanged, so the improvement is
capability per dollar at the same latency budget, not a latency gain.

Distribution is a large advantage. Every agent pinned to `grok-voice-latest`
moved to 3.0 without a code change. Tesla and Starlink give it production call
volume that most voice competitors do not have.
