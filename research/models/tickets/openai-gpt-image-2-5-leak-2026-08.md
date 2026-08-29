---
slug: openai-gpt-image-2-5-leak-2026-08
title: OpenAI's next image models leak as "mona-lisa-1" and "luna-lisa-alpha"
company: OpenAI
model: GPT-Image-2.5 / GPT-Image-2.5 Mini (codenames mona-lisa-1 / luna-lisa-alpha)
status: in-testing
status_note: |
  **@mark_k** (2026-08-22 17:13 UTC): "Just to clear this up: @OpenAI has
  **two new image models in the pipeline**: **`mona-lisa-1`** —
  GPT-Image-2.5 (presumably); **`luna-lisa-alpha`** — GPT-Image 2.5 Mini
  (based on GPT Luna). The big model provides a noticeable (but not
  spectacular) improvement over the current GPT-Image-2. The smaller
  model is faster, and about on the same level as the current one.
  Unfortunately **both models still suffer from the noise artifact
  problem**."

  Status `in-testing` rather than `rumored`: the post reads as **hands-on
  output comparison** — the leaker reports relative quality, speed, and a
  persisting specific defect (noise artifacts) across two distinct
  codenames. That is testing an artifact, not relaying a tease. The
  codename naming also follows a consistent internal scheme
  (`*-lisa-*` for image, with the Mini explicitly tied to the existing
  **GPT Luna** tier), and the `-alpha` suffix on one of them is itself a
  stage marker.

  Verification `unverified`: **single account, no screenshots, no API
  string, no OpenAI acknowledgement** captured. The `GPT-Image-2.5`
  product names are the leaker's inference ("presumably"), not disclosed
  labels.

  Adjacent, and separately sourced: OpenAI shipped **transparent
  backgrounds for GPT-Image-2 on the API** (@testingcatalog, 2026-08-21)
  — the current generation still receiving feature work.
expected: "Two unreleased image models under test as of 2026-08-22 per a single leaker, with product names inferred rather than disclosed. Pending: an API string or console route, screenshots or samples, whether the noise-artifact defect blocks launch, and an OpenAI announcement"
labels:
  - openai
  - image-generation
  - leak
  - in-testing
  - unverified
verification: unverified
sources:
  - "@mark_k"
  - "@testingcatalog"
created_at: 2026-08-23
updated_at: 2026-08-23
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-23
    change: "Created — @mark_k reports two unreleased OpenAI image models in the pipeline under the codenames mona-lisa-1 (inferred GPT-Image-2.5) and luna-lisa-alpha (inferred GPT-Image-2.5 Mini, built on the GPT Luna tier), 2026-08-22 17:13 UTC. He characterises the large model as a noticeable but not spectacular improvement over GPT-Image-2, the small one as faster and roughly at parity with the current model, and says both still exhibit the existing noise-artifact defect. Status in-testing — the report is hands-on relative-quality comparison across two named codenames with a persisting specific defect, which is artifact-grade rather than tease-grade. Verification unverified — single account, no screenshots, no API string, no OpenAI acknowledgement, and the GPT-Image-2.5 product names are the leaker's inference. Separately, OpenAI shipped transparent backgrounds for GPT-Image-2 on the API (@testingcatalog, 2026-08-21)."
---

Two things make this more than a codename drop.

**First, the report is comparative and it is unflattering.** The leaker
says the big model is a "noticeable (but not spectacular)" improvement,
the Mini is at parity with what already ships, and — the detail that
carries the most weight — **both still have the noise-artifact problem**
that afflicts GPT-Image-2. Leaks that flatter their subject are cheap;
a leak that reports an unfixed defect across a generation boundary is
describing something the leaker actually looked at. That is why this
ticket sits at `in-testing` rather than `rumored`, even at
`verification: unverified`.

**Second, the naming is internally consistent.** `mona-lisa-1` and
`luna-lisa-alpha` share a scheme, and the Mini is tied to the existing
**Luna** tier — the cheap/fast member of the GPT-5.6 family already
tracked on [[openai-gpt-5-6]]. OpenAI has reused tier names across
modalities before; a Luna-derived image Mini is the shape you would
predict, which cuts both ways as evidence (consistent, but also
guessable).

**The gap to watch is the defect.** If noise artifacts persist into a
2.5 generation, either they are an accepted characteristic of the
architecture or they are a launch blocker — and which one it is
determines whether these ship soon or sit. Nothing captured here
resolves it, and no artifact (API string, console route, sample images)
exists yet.

Related: [[google-nano-banana-2-2026-05]],
[[google-nano-banana-2-lite-2026-06]],
[[microsoft-mai-image-2-6-2026-08]],
[[alibaba-qwen-image-3-2026-07]] — the competing image lines this would
launch against.
