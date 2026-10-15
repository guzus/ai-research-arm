---
slug: typesafe-jev-1-14-2026-10
title: "TypeSafe AI ships Jev 1.14.0 with opt-in 'danger zone' features (images, box type, longer context)"
company: "TypeSafe AI"
model: "Jev 1.14.0"
status: released
status_note: |
  **Single secondary source.** @bykimdohoon (2026-10-15): TypeSafe AI shipped Jev
  1.14.0 on 2026-10-14. Experimental features sit behind opt-in API headers called
  "danger zone": image input, a new `box` type returning one bounding box, and longer
  context. `jev-latest` moves to 1.14.0 in a week, and 1.13.0 deprecation comes with
  60 days' notice.

  **New ticket, not a reopen.** The original Jev ticket
  ([[typesafe-jev-2026-09]]) is closed and stays untouched. This is a new versioned
  artifact.
expected: "Released 2026-10-14; jev-latest alias moves to 1.14.0 ~2026-10-21; 1.13.0 deprecation after 60 days' notice. Open: a TypeSafe primary changelog."
labels:
  - typesafe
  - versioned-release
  - multimodal
  - unverified
verification: unverified
sources:
  - "https://x.com/bykimdohoon/status/2110696542541861273"
created_at: 2026-10-15
updated_at: 2026-10-15
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-15
    change: "Created — RELEASED / unverified. @bykimdohoon (2026-10-15 11:37 UTC) reports TypeSafe AI shipped Jev 1.14.0 on 2026-10-14. It adds opt-in 'danger zone' API headers gating image input, a new single-bounding-box 'box' type and longer context. The jev-latest alias moves to 1.14.0 in one week, and 1.13.0 will get 60 days' deprecation notice. Single secondary source with no TypeSafe changelog captured, hence unverified. The predecessor [[typesafe-jev-2026-09]] is closed and untouched. Company context: [[typesafe-funding-round-2026-09]]."
---
This is a point release, tracked because it adds a modality (images) and a
structured-output type to a model line already in the set
([[typesafe-jev-2026-09]], closed).

The useful operational detail is the alias policy. `jev-latest` moves in a week,
so anyone pinned to the alias gets new behaviour without deploying anything.
