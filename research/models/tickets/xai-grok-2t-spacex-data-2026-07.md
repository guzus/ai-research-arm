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

  **2026-07-27 update:** @testingcatalog also relays (2026-07-25, same
  window as the Grok 4.6 timing) a follow-on claim that a further model,
  **Grok 4.7**, is expected "in 4 weeks" — sourced to the same relayed
  Elon Musk comment rather than a direct Musk tweet captured this cycle.
  Weaker sourcing tier than the Grok 4.6 timing itself (no independent
  corroboration yet, unlike @kimmonismus's independent Grok 4.6 listing).
  Still no artifact for either model. Status stays `rumored`.
expected: "Grok 4.6 is shipping and in general use as of 2026-08-19 (Grok Build harness, third-party subscriptions). Still pending: an xAI confirmation that the shipped checkpoint is the 2T run trained on SpaceX engineering data, and any sign of the single-sourced Grok 4.7 (~2026-08-22)"
labels:
  - frontier-model
  - training-data
verification: confirmed
sources:
  - https://x.com/elonmusk/status/2079446276299465185
  - https://x.com/testingcatalog/status/2081148852695093410
  - "@kimmonismus"
created_at: 2026-07-21
updated_at: 2026-08-19
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-21
    change: Created — Elon Musk confirmed SpaceX engineering data (excluding ITAR-restricted material) will be added to supplemental training for xAI's next 2T-parameter Grok model.
  - ts: 2026-07-26
    change: "The 2T model now has a working name (Grok 4.6) and a rough timeline — '~2 weeks' per Elon Musk via @testingcatalog, corroborated independently by @kimmonismus. 2T vs 1.5T on Grok 4.5, expected to surpass Kimi. No artifact yet → status stays rumored; model field updated to 'Grok 4.6 (2T, next-gen)', expected/status_note updated with the timeline."
  - ts: 2026-07-27
    change: "A further model, Grok 4.7, reported 'in 4 weeks' per the same @testingcatalog relay of an Elon Musk comment. Weaker/single-sourced vs. the independently-corroborated Grok 4.6 timing. No artifact for either model. Status stays rumored."
  - ts: 2026-08-19
    change: "Status → released. Grok 4.6 is in users hands, on roughly the timeline this ticket recorded (~2026-08-08 per Musk via @testingcatalog). Firsthand usage reports in the 2026-08-19 window: @kamellperry_ (relayed by @elonmusk) — I have finally had the chance to play with Grok 4.6 today after exhausting all of my Codex usage. Grok Build + 4.6 has been…; @doodlestein (also relayed by @elonmusk) — Grok 4.6 with the grok build harness is probably the best all-around, value-for-money subscription out there. Grok Build itself shipped 1.0.6 on 2026-08-18 (@mark_k, changelog-level detail). No xAI post captured in-window restates the 2T parameter count or confirms that SpaceX engineering data made it into the shipped checkpoint, so the training-data claim this ticket was opened on stays at Musk original statement — status advances to released on the model shipping, verification stays confirmed for the same reason. The separately-reported Grok 4.7 (~4 weeks out, single-sourced) has not appeared."
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
