---
slug: mistral-leanstral-1-5
title: Mistral Leanstral 1.5
type: entity
aliases: ["Leanstral 1.5", "Leanstral"]
tags: [mistral, open-weights, formal-verification, lean4, coding]
description: Mistral's open-source (Apache 2.0) formal-verification model for Lean 4 — saturates miniF2F, sets SOTA on FATE-H/FATE-X, and found 5 previously-unknown bugs across 57 scanned open-source repos; the day's top Hacker News AI story.
created_at: 2026-07-05
timestamp: 2026-07-05T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-07-05", path: research/digest/2026-07-05-digest.md}
---

Leanstral 1.5 is Mistral's open-source formal-verification model for **Lean 4** — reported at **119B-A6B** (Mixture-of-
Experts) per Reddit/LocalLLaMA — released under **Apache 2.0**. It
**saturates the miniF2F** benchmark and sets **SOTA on FATE-H/FATE-X**, and
in a practical demonstration of its verification capability it **found 5
previously-unknown bugs** while scanning 57 open-source repositories.

## Why it matters

- **Formal verification as a distinct open-weights front.** Most of the
  2026 [[open-weights]] wave has competed on general coding/agentic
  benchmarks; Leanstral 1.5 stakes out formal verification (machine-checked
  proofs via Lean 4) as its own frontier, complementary to rather than
  competing directly with general-purpose coding models.
- **Independently corroborated top story.** Covered independently by both
  The Decoder and Hacker News, where it was the **top AI story of the day**
  (320 → 346 points across two fetch passes) — a two-source convergence
  rather than a single-outlet tease.
- **Real bug-finding, not just benchmark saturation.** The 5 previously-
  unknown bugs found across 57 scanned repos is a concrete practical
  capability demonstration beyond miniF2F/FATE-H/FATE-X leaderboard
  placement, which strengthens the release's credibility.

## Open questions

- **Does formal-verification capability generalize?** miniF2F and
  FATE-H/FATE-X are Lean-specific benchmarks; whether the underlying
  capability transfers to other proof assistants (Coq, Isabelle) or to
  general software-verification tasks is untested in-window.
- **Adoption.** Does Leanstral 1.5 see uptake inside formal-methods research
  groups or safety-critical software teams, or does it stay a benchmark
  curiosity?
