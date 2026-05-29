---
slug: google-nano-banana-2-2026-05
title: Google Nano Banana 2 + Nano Banana Pro — image generation GA
company: Google / DeepMind
model: Nano Banana 2 / Nano Banana Pro
status: released
status_note: |
  Nano Banana 2 and Nano Banana Pro went generally available on
  2026-05-28, surfaced via @GoogleDeepMind retweet of @Google: "Our best
  image generation models are now available to develop[ers]" with
  immediate availability for developer use. Positions Google's image
  stack against MAI-Image-2.5 (see [[microsoft-mai-image-2-5]]) and
  Grok Imagine.
expected: null
labels:
  - released
  - image-generation
  - multimodal
verification: confirmed
sources:
  - "@GoogleDeepMind"
  - "@Google"
created_at: 2026-05-28
updated_at: 2026-05-28
closed_at: null
closed_reason: null
history:
  - ts: 2026-05-28
    change: "Created — Nano Banana 2 and Nano Banana Pro now generally available to developers, announced by @Google and retweeted by @GoogleDeepMind 16:33 UTC. GA on developer platforms"
---

Google's **Nano Banana 2** and **Nano Banana Pro** image generation
models hit general availability on **2026-05-28**, announced by
@Google and amplified by @GoogleDeepMind. The succinct framing — "Our
best image generation models are now available to develop[ers]" —
puts Google's image stack into the same competitive frame as
Microsoft's [MAI-Image-2.5](./microsoft-mai-image-2-5.md) (Text-to-Image
Arena #3) and the xAI Grok Imagine pricing push.

**What this ticket tracks.** The shipping artefacts are two named
models surfaced on the same day:

- **Nano Banana 2** — the broader-tier image model (positioning
  consistent with workhorse/efficient slot).
- **Nano Banana Pro** — the higher-fidelity sibling for production
  creative work.

Distribution is via the existing Google developer surfaces (Google AI
Studio, Gemini API, presumably Vertex AI follow-on); detailed pricing
and rate cards were not in the launch post and will be tracked here as
they surface.

**Why this is its own ticket** (rather than rolling into Gemini Omni or
the Gemini 3.5 family): Nano Banana is Google's named consumer-image
brand and ships on its own cadence. Gemini Omni
([gemini-omni](./gemini-omni.md)) is the multimodal video-first
generation stack; Nano Banana is the image-native sibling. Future
Nano-Banana point releases UPDATE this ticket.

**Transition triggers:**
- ≥4 weeks past 2026-05-28 GA → close with `released-and-aged`.
- Successor (Nano Banana 3, rebrand to Imagen N, etc.) → new ticket.
- Pricing / Arena leaderboard moves get appended as history entries
  here.
