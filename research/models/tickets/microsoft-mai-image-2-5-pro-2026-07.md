---
slug: microsoft-mai-image-2-5-pro-2026-07
title: Microsoft MAI-Image-2.5-Pro launches in Foundry (preview)
company: Microsoft AI
model: MAI-Image-2.5-Pro
status: in-testing
status_note: |
  @mustafasuleyman (official, 2026-07-23): "MAI-Image-2.5-Pro launches
  today in Foundry for preview." This is a distinct rollout event from
  the original **MAI-Image-2.5 (Preview)** launch tracked (and closed,
  released-and-aged) at [[microsoft-mai-image-2-5]] — that ticket's own
  transition triggers flagged a Foundry GA as the expected next step, and
  a "-Pro" tier landing specifically in Microsoft Foundry (the
  enterprise-facing surface) is a materially different artifact/surface
  from the original Copilot.com consumer preview. Official, single-post
  primary source, no further specs (pricing, benchmarks, Arena
  placement) captured yet → status `in-testing` (Foundry preview, gated
  rather than broad GA), verification `confirmed` (official Suleyman
  account).
expected: "TBD — broader Foundry GA, pricing, and benchmark placement for MAI-Image-2.5-Pro"
labels:
  - microsoft-ai
  - text-to-image
  - foundry
  - preview
verification: confirmed
sources:
  - "@mustafasuleyman"
created_at: 2026-07-27
updated_at: 2026-07-27
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-27
    change: "Created — @mustafasuleyman announced MAI-Image-2.5-Pro launching in Microsoft Foundry for preview (2026-07-23). Distinct artifact/surface from the closed [[microsoft-mai-image-2-5]] ticket (that was the Copilot.com consumer preview); this is the enterprise Foundry Pro tier. Official primary source, gated preview → status in-testing, verification confirmed."
---

**Mustafa Suleyman** announced (official, 2026-07-23) that
**MAI-Image-2.5-Pro** launched that day in **Microsoft Foundry** for
preview.

**Why its own ticket, not an update to [[microsoft-mai-image-2-5]].**
The original MAI-Image-2.5 (Preview) ticket tracked the May 26
Copilot.com consumer launch and was already closed
(`released-and-aged`) on 2026-07-01. That ticket's own transition
triggers anticipated exactly this: "Foundry / MAI Playground GA →
UPDATE with the surface details + API availability," but per the CRUD
dedup protocol, a closed ticket stays closed and new signal that
extends/contradicts it gets a new ticket referencing the old one. The
"-Pro" naming and the enterprise-facing Foundry surface (vs. the
original's consumer Copilot.com preview) also plausibly mark this as a
distinct commercial artifact, not simply the same preview continuing.

**What's confirmed vs. missing.** Official, primary-source
confirmation of the launch and surface (Foundry, preview). No pricing,
benchmark/Arena placement, or broader GA timeline captured yet.

**Transition triggers:**
- Broader Foundry GA, pricing, or Arena benchmark placement → UPDATE,
  consider advancing `status` to `released`.
- A successor or the "-Pro" tier reaching MAI Playground / Copilot → UPDATE.
- ≥4 weeks past a broad GA with no further movement → `closed:
  released-and-aged`.

**Dedup note:** further MAI-Image-2.5-Pro / Foundry signal UPDATES this
ticket. The original consumer MAI-Image-2.5 (Preview) stays closed at
[[microsoft-mai-image-2-5]]. MAI-Voice-2-Flash (announced the same
window) is tracked separately at
[[microsoft-mai-voice-2-flash-2026-07]].
