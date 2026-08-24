---
slug: nvidia-poolside-license-2026-08
title: NVIDIA pays ~$6B to license Poolside's Model Factory and takes on 100+ of its engineers
company: NVIDIA / Poolside
model: null
status: confirmed
status_note: |
  NVIDIA struck a **~$6B deal with Poolside** that licenses Poolside's
  **"Model Factory" technology** and brings **more than 100 Poolside
  engineers into NVIDIA** (@mark_k, 2026-08-23 19:17 UTC). Two
  independent relays carry the same two numbers: @akshoydasss, in a
  pre-earnings NVIDIA roundup, states NVIDIA "paid **$6 BILLION** to
  license AI models from startup Poolside and extended job offers to
  **over 100** of its employees"; @TechThought_org points at a
  **thenextweb.com** writeup ("nvidia-poolside-6bn-model-factory-licence")
  and frames the structure as "pseudo-licensing… to outmaneuver antitrust
  scrutiny while securing frontier capability."

  **The structure is the story, not the price.** A license-plus-hire is
  the shape used repeatedly in 2026 to acquire a lab's capability without
  acquiring the lab — the same pattern this ticket set already records in
  [[groq-funding-2026-06]] (Nvidia's $20B "not-acqui-hire" of Groq staff)
  and in NVIDIA's SSI position ([[nvidia-ssi-investment-2026-07]]). It
  moves people and weights without triggering merger review, and it
  leaves the licensed startup nominally independent.

  **Why it lands in the model lane.** @mark_k's read is that this feeds
  **Nemotron**: NVIDIA is "reportedly working on **Nemotron 4**, a
  massive **1T+ parameter open model**," and Poolside's model-training
  tooling plus its people are what a frontier-class open release from
  NVIDIA would need. Treat the Nemotron 4 link as **that account's
  inference, not a sourced claim** — no NVIDIA statement connects the two,
  and NVIDIA's prior Nemotron distribution move is on the closed
  [[nvidia-nemotron-openrouter-2026-06]].

  Status `confirmed`: three independent relays with matching figures
  ($6B, 100+ engineers, Model Factory) plus a named trade outlet.
  Verification `partial`: **no NVIDIA or Poolside primary post, no
  filing, no press release was captured**, and the thenextweb URL was not
  reachable from this run, so every figure here is secondhand.
expected: "Reported 2026-08-23/24 as a ~$6B licence for Poolside's Model Factory plus job offers to 100+ Poolside engineers. Pending: an NVIDIA or Poolside on-record statement, the licence terms, whether Poolside continues to operate independently, whether it surfaces in NVIDIA's 2026-08-26 earnings disclosure, and whether it in fact feeds a Nemotron 4 open release"
labels:
  - nvidia
  - poolside
  - licence-and-hire
  - open-weights
  - consolidation
verification: partial
sources:
  - "@mark_k"
  - https://x.com/mark_k/status/2091605721611723115
  - "@akshoydasss"
  - https://x.com/akshoydasss/status/2091782749388779738
  - "@TechThought_org"
created_at: 2026-08-24
updated_at: 2026-08-24
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-24
    change: "Created — NVIDIA reportedly paid ~$6B to license Poolside's Model Factory technology and extended offers to 100+ Poolside engineers (@mark_k 2026-08-23 19:17 UTC; independently repeated by @akshoydasss in a pre-earnings NVIDIA roundup and by @TechThought_org citing a thenextweb writeup). Structure is a licence-and-hire, the same capability-without-merger shape as Nvidia's $20B Groq staff deal ([[groq-funding-2026-06]]). @mark_k infers it feeds a rumored 1T+ parameter Nemotron 4 open model — recorded as his inference, not a sourced claim. Status confirmed on three matching independent relays plus a named outlet; verification partial — no NVIDIA or Poolside primary source, no filing, and the cited article was not reachable from this run."
---

NVIDIA is reported to have paid roughly **$6B** to license **Poolside's
"Model Factory"** and to have extended offers to **more than 100
Poolside engineers**. Three independent accounts carry the same figures
in the same window, one of them pointing at a named trade outlet.

**The interesting variable is the deal shape.** This is not an
acquisition; it is a licence attached to a mass hire. NVIDIA has now run
that play at least twice — the Groq arrangement recorded on
[[groq-funding-2026-06]] moved staff at a reported $20B without a
merger, and the SSI position on [[nvidia-ssi-investment-2026-07]] bought
influence over a frontier lab without control of it. The antitrust
reading @TechThought_org offers is speculation, but the structural
observation under it is not: a licence-and-hire transfers the two things
that actually matter — trained people and training machinery — while
leaving no entity to review.

**Why a chip vendor buying model-training tooling matters to this lane.**
NVIDIA's incentive to ship a strong open model is not to sell the model;
it is to make its own silicon the default substrate for everyone
fine-tuning and serving one. If the rumored **Nemotron 4** at 1T+
parameters is real, Poolside's tooling and staff are a plausible input to
it. That link is currently one account's inference and nothing more — it
belongs on the ticket as a hypothesis to test, and the test is whether
NVIDIA ships a frontier-class open-weight model in the next two quarters.

**What would resolve the sourcing gap.** An NVIDIA or Poolside
statement, or the deal appearing in NVIDIA's **2026-08-26** earnings
disclosure — the same event that will test the pricing claims on
[[nvidia-server-price-increase-2026-08]].

Related: [[nvidia-perplexity-investment-2026-08]],
[[nvidia-openai-ohio-datacenter-financing-2026-07]],
[[industry-open-weights-letter-2026-07]].
