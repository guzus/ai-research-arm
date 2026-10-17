---
slug: bfl-flux-3-klein-2026-10
title: "Black Forest Labs releases FLUX 3 Image Klein — 5.6B open-weight image model with native 4K"
company: Black Forest Labs
model: FLUX 3 Image Klein
status: released
status_note: |
  **Two independent secondary sources.** @testingcatalog's 2026-10-16 brief (quoted in
  its 2026-10-17 brief): "Black Forest Labs released FLUX 3 Image Klein, a 5.6B
  open-weight image model with native 4K that runs on a single consumer GPU."
  @DogukanUrker's 2026-10-17 roundup of this week's open-weight releases lists "FLUX 3
  Klein".

  `partial`: no @bfl_ml post or model card/licence was captured.
expected: "Released ~2026-10-16 (open weights). Open: BFL announcement, licence (FLUX open-weight releases have historically used non-commercial terms), larger FLUX 3 tiers."
labels:
  - black-forest-labs
  - image-generation
  - open-weights
  - released
verification: partial
sources:
  - "https://x.com/testingcatalog/status/2111409303701577925"
  - "https://x.com/DogukanUrker/status/2111337663286706405"
created_at: 2026-10-17
updated_at: 2026-10-17
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-17
    change: "Created — RELEASED / partial. Black Forest Labs released FLUX 3 Image Klein, a 5.6B open-weight image model with native 4K output that runs on a single consumer GPU (@testingcatalog 2026-10-16 brief, quoted 2026-10-17; listed in @DogukanUrker's 2026-10-17 open-weights roundup). No BFL primary or licence captured."
---

"Klein" is BFL's small tier. A 5.6B model generating natively at 4K on one
consumer GPU puts high-resolution open image generation within reach of local
users. Whether larger FLUX 3 tiers exist, and under what licence, is still open.

**Transition triggers:** BFL post/model card → verification `confirmed`; about four
weeks after release → close as released-and-aged.
