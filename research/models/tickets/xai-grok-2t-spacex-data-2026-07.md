---
slug: xai-grok-2t-spacex-data-2026-07
title: xAI's next 2T-parameter Grok run to train on SpaceX engineering data
company: xAI / SpaceX
model: Grok 4.6 (2T, next-gen)
status: rumored
status_note: |
  Elon Musk (primary/company source) says SpaceX's engineering-data
  corpus — excluding ITAR-restricted material — will be added during
  supplemental training of xAI's next ~2-trillion-parameter model. No
  ship date given at filing; this is a training-plan disclosure, not a
  release.

  **2026-07-26 update:** The next model now has a working name — **Grok
  4.6** — and a rough timeline. Per **@testingcatalog** (citing Elon
  Musk): Grok 4.6 is expected to land "already in 2 weeks," built on
  ~2T parameters (vs 1.5T for Grok 4.5 / V9-Medium, [[grok-v9-medium]]),
  and is expected to surpass Kimi (presumably Kimi K3,
  [[moonshot-kimi-k3]]) on benchmarks. @kimmonismus independently lists
  "Grok 4.6 in 2 weeks" alongside other near-term model expectations.
  Still no artifact (preview, console listing, leak) — this remains a
  primary-source timeline disclosure, not evidence of an existing build,
  so status stays `rumored` pending a real artifact.
expected: "Grok 4.6 (2T) expected ~2 weeks from 2026-07-25 per Elon Musk, via @testingcatalog"
labels:
  - frontier-model
  - training-data
verification: confirmed
sources:
  - https://x.com/elonmusk/status/2079446276299465185
  - https://x.com/testingcatalog/status/2081148852695093410
  - "@kimmonismus"
created_at: 2026-07-21
updated_at: 2026-07-26
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-21
    change: Created — Elon Musk confirmed SpaceX engineering data (excluding ITAR-restricted material) will be added to supplemental training for xAI's next 2T-parameter Grok model.
  - ts: 2026-07-26
    change: "The 2T model now has a working name (Grok 4.6) and a rough timeline — '~2 weeks' per Elon Musk via @testingcatalog, corroborated independently by @kimmonismus. 2T vs 1.5T on Grok 4.5, expected to surpass Kimi. No artifact yet → status stays rumored; model field updated to 'Grok 4.6 (2T, next-gen)', expected/status_note updated with the timeline."
---

Elon Musk announced directly that SpaceX's proprietary engineering-data
corpus will be folded into supplemental training for xAI's next
generation flagship model, described only as "the 2T run" (~2 trillion
parameters). ITAR-restricted material is explicitly excluded. This is a
company-source (CEO) disclosure of a training plan, not a product
release — filed as `rumored` in the lifecycle sense (no artifact exists
yet) even though the source itself is as primary as it gets.

Distinct from the existing `xai-grok-build-2026-05` ticket, which tracks
a released coding-agent artifact (`grok-build-0.1`), not this future
flagship base model.
