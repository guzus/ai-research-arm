---
slug: odyssey-3-world-model-2026-09
title: Odyssey-3 — foundation world model unveiled
company: Odyssey ML
model: Odyssey-3
status: confirmed
status_note: |
  **Unveiled by the company, 2026-09-15 16:36 UTC.** @odysseyml: "Today we're
  unveiling Odyssey-3, a big step forward for foundation world models. It can
  control robots, power humanoids, drive cars (on the roads of India!), train
  AIs, pilot drones, and even play video games." Relayed by @_akhaliq.

  **Status is `confirmed`, not `released`,** and the distinction matters here:
  "unveiling" with a demo video is an announcement. Nothing in-window
  establishes weights, an API, pricing, access tiers, or a single third-party
  running it. The claimed capability list is entirely first-party.

  **The claim to be skeptical of is the breadth.** One model asserted to
  control robots, power humanoids, drive cars on Indian roads, train other
  AIs, pilot drones and play games is either a genuinely general world model or
  a reel of separately-tuned demos under one name. The India driving clip is
  the strongest single item — unstructured traffic is the hardest published
  driving environment — and it is also the one most in need of independent
  reproduction rather than a highlight video.
expected: "Announced/unveiled. Open: weights or API access, any quantitative eval, and any third-party reproduction — particularly of the India on-road driving claim."
labels:
  - world-model
  - robotics
  - autonomous-driving
  - foundation-model
verification: partial
sources:
  - https://x.com/odysseyml/status/2099900067356586276
  - "@_akhaliq"
created_at: 2026-09-16
updated_at: 2026-09-16
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-16
    change: "Created — CONFIRMED (announcement), verification partial. @odysseyml unveiled Odyssey-3 on 2026-09-15 16:36 UTC as 'a big step forward for foundation world models', claiming a single model that controls robots, powers humanoids, drives cars on the roads of India, trains AIs, pilots drones and plays video games; relayed by @_akhaliq. The company's own post is a primary source for the ANNOUNCEMENT, which is why status is confirmed — but every capability claim is first-party with no captured eval, no weights, no API, no pricing and no third-party hands-on, so verification is partial rather than confirmed and status is NOT released. The breadth claim is the thing to check: one world model spanning robots, humanoids, road driving, drones and games is either genuinely general or a set of separately-tuned demos presented together. The India on-road driving clip is the highest-value and least-reproduced item. Sits alongside the other robot/world-foundation-model tickets ([[google-gemini-robotics-2-2026-07]], [[nvidia-sonic-humanoid-model-2026-09]], [[skild-s1-2026-08]], [[figure-helix-02-2026-05]])."
---

**Odyssey-3** was unveiled as a foundation *world* model — a single model
asserted to act across robots, humanoids, road driving, drones and games.

**Why world models get their own line in this repo.** The robotics tickets
here ([[google-gemini-robotics-2-2026-07]],
[[nvidia-sonic-humanoid-model-2026-09]], [[skild-s1-2026-08]]) track
*policies* — models that output actions for a body. A world model tracks
*dynamics* — it predicts what happens next, and control falls out of that.
If the claim holds, the same artifact serves every embodiment in the list,
which is why the breadth is both the headline and the reason for doubt.

**What is actually established.** That Odyssey announced it, and showed video.
That is it. No weights, no API, no numbers, nobody outside the company has
run it.

**The one claim worth chasing.** Driving on Indian roads. Unstructured,
negotiation-heavy traffic is the environment autonomous-driving programs
avoid publishing on, and a world model handling it end-to-end would be a
substantive result. A highlight clip is not that result. Independent
reproduction, or a route/intervention rate, is.

**Transition triggers:**
- Weights, an API, or any access tier → advance to `released`, UPDATE.
- A quantitative eval or third-party hands-on → UPDATE, advance
  `verification`.
- A deployment partner or customer → UPDATE.
- ≥15 cycles with no access and no reproduction → reconsider.

**Dedup note:** action-policy robot models stay on their own tickets; this is
the world-model line.
