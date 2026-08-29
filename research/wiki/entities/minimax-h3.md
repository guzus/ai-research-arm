---
slug: minimax-h3
title: MiniMax H3
type: entity
aliases: ["MiniMax H3", "MiniMax-H3", "H3"]
tags: [open-weights, model, video-generation, multimodal, chinese-llm, local-inference]
description: MiniMax's 33B unified text/image/video/audio model, released 2026-08-04 — the first open model reported to top a video-generation ranking, and runnable end-to-end on a single consumer GPU.
created_at: 2026-08-04
timestamp: 2026-08-04T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-08-04", path: research/digest/2026-08-04-digest.md}
---

**MiniMax H3** is a **33B unified text/image/video/audio model** from the
Chinese lab MiniMax (see [[minimax-m3]] for its earlier open agentic-coding
release), generating up to **15-second clips with native synchronized stereo
audio**. It is reported as the **first open model to top a video-generation
ranking**, and it shipped with day-zero distribution across **ComfyUI,
Diffusers, SGLang and Hugging Face** (ARA digest 2026-08-04).

## Why it matters

- **It runs on one consumer GPU — verified by two independent testers.**
  End-to-end generation on an **RTX 5090** through a ~40GB ComfyUI stack, and
  in **170 seconds on a 5070Ti** under INT8 quantization. Video generation
  moving onto hardware people already own is a larger shift than the ranking
  position; it is the [[open-weights]] "run it yourself" thesis applied to a
  modality that had stayed server-side.
- **The open artifact is not the model behind the launch demos.** Three
  components stayed on MiniMax's servers: **2K regeneration, context
  orchestration and sparse attention**. Resolution from the weights is
  **768p-class against the 2K advertised**. This is a partial open release
  presented in the frame of a full one — the pattern to watch as labs
  discover which components are cheap to withhold and load-bearing to keep.
- **The license is unconfirmed and possibly territorially restricted.**
  First testers report an **"Excluded Territories"** clause naming the EU, UK,
  South Korea and the United States — **unconfirmed against a published
  license**. If real, it is a geofenced open release, which sits awkwardly
  against the [[eu-ai-regulation|EU AI Act]] transparency duties that went
  live 2026-08-02 and against any claim of open distribution.
- **It lands in a crowded week for video.** [[seedance-2-5|ByteDance Seedance
  2.5]] shipped everywhere except the United States in the same cycle, at
  $0.097/second with 30-second single-pass generation — the closed, hosted
  answer to H3's downloadable one.
- **HN treated it as a local-inference story.** *MiniMax H3 Day-0 Support in
  ComfyUI* (224 pts) sat inside the day's most persistent Hacker News cluster —
  three "run it yourself" stories deep in every window.

## Open questions

- **Does a published license confirm the Excluded Territories clause?** As of
  this ingest the claim rests on first testers reading terms, not on a license
  file.
- **How much of the ranking result survives without the withheld components?**
  The ranked system and the downloadable one are not obviously the same system.
- **Is 768p-from-weights the ceiling, or does the community close the 2K gap?**
