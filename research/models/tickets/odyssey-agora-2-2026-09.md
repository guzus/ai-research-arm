---
slug: odyssey-agora-2-2026-09
title: Agora-2 — Odyssey's multi-agent world model, playable multiplayer research preview
company: Odyssey ML
model: Agora-2
status: released
status_note: |
  **Shipped as a playable preview, 2026-09-24 15:37 UTC.** @odysseyml
  (primary): "Introducing Agora-2, our next-generation multi-agent world model.
  Agora-2 supports up to 20 humans and agents interacting inside a shared
  environment, all simulated in real time. Our multiplayer research preview is
  available to try right now!" Corroborated by @testingcatalog with additional
  specifics: "Every frame comes from the model, and each participant's actions
  change what everyone else sees", up to 5× more participants than Agora-1, and
  coverage of multiple environments at once.

  **Status is `released`, and the distinction from
  [[odyssey-3-world-model-2026-09]] is deliberate.** Odyssey-3 was *unveiled*
  nine days earlier with a demo reel and no access path, which is why that
  ticket sits at `confirmed`. Agora-2 is playable by the public right now, so
  it clears the `released` bar — "publicly available, anyone can use it" —
  even though "research preview" is doing real work in that sentence.

  **These are two different artifacts from one company, tracked separately.**
  Odyssey-3 is pitched as a foundation world model for robots, humanoids, cars
  and drones. Agora-2 is a real-time multiplayer simulation with a named
  predecessor (Agora-1). Same lab, different product lines, different
  lifecycles; merging them would lose the fact that one is claimed and one is
  runnable.

  **What is unverified.** Every quantitative claim — 20 concurrent
  participants, "every frame comes from the model", real-time, 5× Agora-1 —
  is first-party or a relay of first-party. No latency figure, resolution,
  session-length limit, model size, or third-party benchmark exists. The
  "every frame comes from the model" claim is the one most worth testing,
  because a hybrid of generated frames over a conventional engine would look
  similar in a clip and be a fundamentally different system.
expected: "Public research preview live now. Open: independent hands-on reports at the claimed 20-participant concurrency, any published latency/resolution/session-length figures, whether frames are fully generated or engine-composited, pricing or API access beyond the preview, and any relationship to Odyssey-3's foundation-model claims."
labels:
  - world-model
  - multi-agent
  - real-time
  - research-preview
  - released
verification: confirmed
sources:
  - https://x.com/odysseyml/status/2103146841378586820
  - https://x.com/testingcatalog/status/2103164517433606640
created_at: 2026-09-25
updated_at: 2026-09-25
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-25
    change: "Created — RELEASED. @odysseyml announced Agora-2 on 2026-09-24 15:37 UTC (~2,564 likes) as a 'next-generation multi-agent world model' supporting up to 20 humans and agents in one shared, real-time-simulated environment, with a multiplayer research preview 'available to try right now'. @testingcatalog corroborated the same day and added detail: every frame comes from the model, each participant's actions change what everyone else sees, up to 5x more participants than Agora-1, multiple environments at once. Status released rather than confirmed because a public access path exists today, which is the bar the lifecycle sets; verification confirmed because the announcing account is the vendor itself. Created as a SEPARATE ticket from [[odyssey-3-world-model-2026-09]] on purpose: Odyssey-3 was unveiled 2026-09-15 with a demo reel and no access path and remains at 'confirmed', while Agora-2 is a distinct product line with its own named predecessor (Agora-1) and is runnable — same company, different shipping artifacts. All quantitative claims (20 participants, fully generated frames, real-time, 5x Agora-1) are first-party and currently unreproduced; the 'every frame comes from the model' claim is flagged as the one to test, since generated frames composited over a conventional engine would present identically in a clip."
---

Odyssey has now put two world models into the record in ten days, and only one
of them can be run.

That contrast is the useful thing here. [[odyssey-3-world-model-2026-09]] makes
the larger claim — one model controlling robots, humanoids, cars on Indian
roads, drones, and games — with nothing but a reel behind it. Agora-2 makes a
narrower claim and hands you a link. A lab that ships the narrow one while the
broad one stays a video is telling you where its actual capability is.

The concurrency number is the technically interesting part. Single-player world
models only have to stay coherent with one action stream. Twenty simultaneous
participants means the model has to keep a shared state consistent across
conflicting inputs in real time, which is a different and harder problem than
frame quality. If that holds up under independent testing at full occupancy, it
is a more meaningful result than any of Odyssey-3's breadth claims.

"Research preview" is the hedge to watch. It usually means session caps, queue
gating, and a small fixed set of environments — none of which are disclosed
here. The first credible third-party report running twenty real participants
will settle more than another announcement would.
