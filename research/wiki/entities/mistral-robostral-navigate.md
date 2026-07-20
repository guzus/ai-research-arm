---
slug: mistral-robostral-navigate
title: Mistral Robostral Navigate
type: entity
aliases: ["Robostral Navigate", Robostral]
tags: [robotics, mistral, embodied-ai, model-release]
description: Mistral AI's first embodied-navigation model — an 8B-parameter model that guides robots to autonomously perform natural-language-specified tasks, announced 2026-07-08.
created_at: 2026-07-12
timestamp: 2026-07-12T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-07-12", path: research/digest/2026-07-12-digest.md}
  - {title: "ARA model ticket — Mistral Robostral Navigate", path: research/models/tickets/mistral-robostral-navigate-2026-07.md}
---

**Robostral Navigate** is **Mistral AI**'s first model for **embodied
navigation**: an **8-billion-parameter** model that guides robots to
autonomously perform tasks specified in plain natural language. Announced
directly by Mistral's own account via a 3-tweet thread on 2026-07-08.

## Why it matters

It marks Mistral's first entry into embodied-AI/robotics, distinct from
its text and formal-verification model lines (e.g.
[[mistral-leanstral-1-5]]), opening a new competitive axis — robotics
foundation models — alongside [[figure-ai]]'s Helix-02 VLA. It shipped
the same digest cycle as [[tencent-hunyuan-hy3]], another open-weight
release, on a day with two notable open-weight drops.

Official primary source (Mistral's own account), real shipping artifact
— `verification: confirmed`.

## Open questions

- **Access and pricing.** Is Robostral Navigate open-weight, API-only, or
  both? No pricing or SDK access details have surfaced yet.
- **Benchmarks.** No third-party navigation-task benchmarks have been
  reported; how does it compare with Figure's Helix-02 or other embodied
  models?

## Changelog

- [2026-07-12] created | Mistral's first embodied-navigation model), updated 5 (openai — Apple lawsuit + Sol Ultra GA/CritPt benchmark lead
