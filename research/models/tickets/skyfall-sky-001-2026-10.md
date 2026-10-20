---
slug: skyfall-sky-001-2026-10
title: "Skyfall SKY-001 — compositional visual world model for part-by-part CAD planning"
company: Skyfall
model: SKY-001
status: confirmed
status_note: |
  Announced in a thread by @spisallyouneed (post 6/n, 2026-10-19 18:11 UTC, ~262 likes),
  written in the first person ("our vision"). SKY-001 is described as a "Compositional
  Visual World Model" that produces a visual, component-by-component plan of an
  engineered object. The next step is to pair it with a VLA agent that executes each
  step, inspects the result and revises failures. Company attribution ("Skyfall's new
  SKY-001") comes from @thesignal24 (2026-10-20 11:00 UTC). The poster's role at
  Skyfall is not established. Access, pricing and benchmarks are not in signal.
expected: "Announced; executable CAD operations and editable feature history are the stated next step. Availability unknown."
labels:
  - world-model
  - cad
  - engineering
verification: partial
sources:
  - "https://x.com/spisallyouneed/status/2112245274261557330"
  - "https://x.com/thesignal24/status/2112499068325015655"
created_at: 2026-10-20
updated_at: 2026-10-20
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-20
    change: "Created — CONFIRMED / partial. A first-person launch thread by @spisallyouneed (2026-10-19 18:11 UTC) presents SKY-001 as a Compositional Visual World Model that plans engineered objects part by part, with a VLA executor and editable CAD history as next steps; @thesignal24 (2026-10-20) attributes it to Skyfall. No official company handle in signal; access and benchmarks unknown."
---

SKY-001 plans an object as a sequence of components instead of generating one
finished mesh. The pitch is that a separate agent can then carry the plan out
step by step in CAD. The team argues that even smaller open models could then
build complex CAD, because the planning work is already done.

@thesignal24 points out the gap: a convincing 3D render is not an editable
engineering file. That only closes with executable CAD operations and feature
history, which the roadmap lists as the next step, not something shipped today.

**Transition triggers:** an official Skyfall post or product page → verification
confirmed; public access → released; executable-CAD release → UPDATE.
