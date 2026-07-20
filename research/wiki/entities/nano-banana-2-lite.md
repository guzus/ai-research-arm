---
slug: nano-banana-2-lite
title: Nano Banana 2 Lite
type: entity
aliases: ["Nano Banana 2 Lite", "gemini-3.1-flash-lite-image", "gemini-3-1-flash-lite-image", "Gemini Omni Flash"]
tags: [google, gemini, image-generation, video-generation, multimodal]
description: Google's fastest/cheapest image model (gemini-3.1-flash-lite-image), live 2026-06-30 at ~4s and ~$0.034/image — shipped alongside Gemini Omni Flash, which brings text-prompt video generation/editing to the Gemini API for the first time.
created_at: 2026-07-01
timestamp: 2026-07-01T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-07-01", path: research/digest/2026-07-01-digest.md}
  - {title: "@testingcatalog / Ars Technica / The Decoder", date: 2026-06-30}
---

Nano Banana 2 Lite (`gemini-3.1-flash-lite-image`) is **Google's fastest and
cheapest image model yet**, live **2026-06-30** on Google AI Studio and in the
Gemini app: **~4s image generation at ~$0.034/image** ($0.25 input /
$0.0336 output), trading some quality for speed. It shipped alongside
**Gemini Omni Flash**, which brings **text-prompt video generation/editing to
the Gemini API for the first time** (ARA digest 2026-07-01).

## Why it matters
- **Speed/cost as the axis.** At ~4s and ~$0.034/image it is tuned for
  high-volume, latency-sensitive image workloads rather than maximum fidelity —
  Google pushing the price floor on generation, the same competitive lever the
  [[open-weights]] wave applies to text.
- **Video generation reaches the API.** Gemini Omni Flash exposing text-prompt
  video gen/editing through the API is the more strategically notable half of
  the release — moving Google's video capability from app demo to a programmable
  primitive developers can build on.
- **Part of Google's fast-tier lineup.** It extends the low-cost, agent-oriented
  positioning of [[gemini-3-5-flash]] into image/video, alongside the
  open-weights [[gemma-4]] family — Google spanning hosted-cheap and
  open-weight tiers simultaneously.

## Open questions
- **Quality-vs-speed acceptance.** Whether the deliberate quality trade lands
  with developers or pushes them to the full-fat image tier for anything
  presentation-grade.
- **Omni Flash video maturity.** First-to-API is a milestone; output quality,
  length limits, and pricing under real load are untested in-window.

## Changelog

- [2026-07-01] created | Google's fastest/cheapest image model + Omni Flash API video gen), updated 3 (anthropic — Sonnet 5 + Claude Science launches, Amazon $1B FDE org + repricing tension, Fable re-release absent
