---
slug: meta-connect-2026-09
title: Meta Connect 2026 — Muse Charm keychain device, Meta VR Glasses, Muse Realtime Avatar
company: Meta (Meta Superintelligence Labs)
model: Muse (Muse Realtime Avatar / Muse Realtime Voice)
status: confirmed
status_note: |
  Meta Connect ran 2026-09-23 into 2026-09-24. Three artifacts, at different
  confidence levels.

  **Muse Realtime Avatar** — company-primary. @AIatMeta, 2026-09-24 05:43 UTC:
  Zuckerberg "just unveiled Muse Realtime Avatar, our real-time embodiment
  technology that turns Muse Realtime Voice into expressive, interactive
  avatars", starting with real-time conversations in Muse. Builds directly on
  [[meta-muse-voice-transcribe-2026-09]].

  **Muse Charm** — company-primary via Meta's Chief AI Officer. @alexandr_wang,
  2026-09-24 00:56 UTC: "muse charm, the easiest way to use muse that fits on
  your keychain. shipping in dec in time for the holidays." Spec detail via
  @rohanpaul_ai's write-up of the keynote: fingerprint-activated, ~2-inch OLED
  touch screen, a new OS, Muse's realtime voice + avatar stack on-device, 5G,
  front and rear cameras, speakers/mics/USB-C, "holdable" rather than wearable.
  **No pricing, no full spec sheet, and Zuckerberg said only a few units exist
  with hardware still being finalised** against the December target — so the
  device is announced, not shipped.

  **Meta VR Glasses** — third-party only in this cycle's signal
  (@testingcatalog): VR in a glasses form factor rather than a headset, AI-native
  OS, Muse assistant integration with a VR Muse avatar, eye + hand + voice
  control. Recorded at aggregator confidence.

  Also reported at aggregator confidence: FDA-cleared hearing-aid mode on Meta
  Glasses, and on-device private processing Meta says it cannot see.
expected: "Muse Charm targeted at December 2026, hardware not final. Meta VR Glasses and hearing-aid mode have no dated ship commitment in this cycle's signal."
labels:
  - meta
  - muse
  - hardware
  - consumer-agent
  - meta-connect
verification: partial
sources:
  - https://x.com/AIatMeta/status/2102997291732766943
  - https://x.com/alexandr_wang/status/2102925117911388450
  - https://x.com/rohanpaul_ai/status/2102957576686301449
  - https://x.com/testingcatalog/status/2102908929378291780
  - https://x.com/testingcatalog/status/2103015463089238076
  - https://x.com/kimmonismus/status/2102896795051536883
created_at: 2026-09-24
updated_at: 2026-09-24
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-24
    change: "Created — CONFIRMED. Meta Connect 2026 (2026-09-23/24) produced three tracked artifacts. Muse Realtime Avatar, announced by @AIatMeta (company-primary): real-time embodiment turning Muse Realtime Voice into interactive avatars, starting with real-time conversations. Muse Charm, announced by Meta Chief AI Officer @alexandr_wang (company-primary): a fingerprint-activated keychain-sized Muse device shipping December 2026 — ~2-inch OLED touch screen, new OS, on-device realtime voice + avatar stack, 5G, front and rear cameras, speakers/mics/USB-C, described as holdable rather than wearable, with no pricing, no published spec sheet, only a few units built and hardware not finalised. Meta VR Glasses (VR in glasses form, AI-native OS, Muse avatar, eye/hand/voice control) appears only via @testingcatalog with no Meta-primary post captured, as does the FDA-cleared hearing-aid mode. Verification partial: the two Muse items are company-primary, the glasses are aggregator-sourced. Kept as one event ticket per the precedent of [[nvidia-gtc-taipei-2026-06]] rather than split per device; if any single artifact develops its own release arc it gets its own ticket."
---

Meta Connect 2026 was a distribution announcement wearing hardware. The
model-layer news is thin — Muse Realtime Avatar is an embodiment layer on top of
the realtime voice stack Meta already shipped
([[meta-muse-voice-transcribe-2026-09]]) — and the significant move is putting
Muse on endpoints that are not a phone.

Muse Charm is the clearest statement of that thesis: a keychain device whose
entire purpose is to shorten the distance between noticing something and asking
an agent to act on it. It is also the least finished thing announced. Only a few
units exist, hardware is not final, there is no price, and the ship target is
December — roughly ten weeks out. Announcing at that maturity is a competitive
posture, not a product launch, and it should be read next to the fact that Muse
itself is currently the top free app in the US and Canada
([[meta-hatch-muse-spark-2026-06]]) and already straining to serve under a
million users.

The Meta VR Glasses claim is deliberately held at lower confidence. "VR in
glasses rather than a headset" is a large hardware claim to carry on an
aggregator post with no Meta-primary source in this cycle's signal; if it is
real it will be trivially corroborated within days, and this ticket updates
then.

What is not here is a model. Wang teased that Meta is "pretty soon dropping the
most capable model we have ever trained" (@scaling01's relay of the keynote),
and no such model appeared at Connect. Tracked separately when it does;
[[meta-aira-3-2026-09]] and [[meta-hatch-muse-spark-2026-06]] are the current
Meta model-side tickets.
