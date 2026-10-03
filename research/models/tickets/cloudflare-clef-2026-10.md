---
slug: cloudflare-clef-2026-10
title: Cloudflare Clef and Clef-Flash — open decision models positioned against TypeSafe's Jev
company: Cloudflare
model: Clef / Clef-Flash
status: confirmed
status_note: |
  **Single relay of a primary blog post.** @KeisukeIshikawa (2026-10-03 11:38
  UTC) summarises a Cloudflare Blog post and Hugging Face release: Clef and
  Clef-Flash take a state plus a predefined set of decisions and return a
  probability for every option in one non-autoregressive pass — the same
  "decision model" category TypeSafe opened with Jev ([[typesafe-jev-2026-09]]).

  **Claims as relayed (not yet checked against the primary):**
  - Clef is built on Qwen3.8-27B, Clef-Flash on Qwen3.5-9B; most base weights
    frozen, with adapters plus a decision head scoring choices from internal
    representations.
  - Multimodal inputs (text, JSON, images, video).
  - On TypeSafe's own workflow evals, Clef beat Jev in 3 of 4 areas (invoice
    processing, customer service, security incidents); Jev led on agent-trace
    observability.
  - Median latency over a 43-eval run: Jev 524 ms, Clef 209 ms, Clef-Flash
    38.8 ms (~13x faster than Jev).
  - API-compatible with Jev/SystemOne; weights open under Apache 2.0.
expected: "Reported released 2026-10-03 (Cloudflare blog + Hugging Face weights, per relay). Moves to released with verification upgraded once the Cloudflare post or the Hugging Face model pages are captured directly. Open: independent latency/accuracy reproduction, and any TypeSafe response to being benchmarked on its own evals."
labels:
  - decision-model
  - open-weights
  - agent-infrastructure
  - qwen-derived
verification: unverified
sources:
  - https://x.com/KeisukeIshikawa/status/2106348138516676752
created_at: 2026-10-03
updated_at: 2026-10-03
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-03
    change: "Created — CONFIRMED / unverified. @KeisukeIshikawa (2026-10-03 11:38 UTC) reports that Cloudflare released Clef and Clef-Flash, single-pass decision models (state + option set -> probability per option) explicitly benchmarked against TypeSafe's Jev ([[typesafe-jev-2026-09]]): Clef on Qwen3.8-27B, Clef-Flash on Qwen3.5-9B; Clef ahead of Jev in 3 of 4 TypeSafe workflow areas; median latency 524 ms (Jev) vs 209 ms (Clef) vs 38.8 ms (Clef-Flash); Jev/SystemOne-compatible API; Apache 2.0 weights. Status confirmed rather than rumored because the relay cites a specific Cloudflare Blog post and Hugging Face release with concrete numbers; verification unverified because it is one secondary account and neither primary page was captured in this cycle. Not set to released until the weights are seen directly."
---

TypeSafe's argument with Jev was that most agent steps are decisions, not
essays, and that paying an autoregressive LLM to write a paragraph before it
picks an option is waste. Three weeks later, a hyperscale edge provider has
apparently shipped its own take, benchmarked it on TypeSafe's own evals, made
the API drop-in compatible, and open-sourced the weights. That is about the
fastest validation-by-imitation a new category can get.

The architecture claim is the part worth checking: freeze a strong open base
(Qwen3.8-27B, the same checkpoint already turning up across fine-tuning
projects), train adapters and a scoring head, and decide in one forward pass.
If the 38.8 ms median for Clef-Flash holds, the decision layer stops being a
latency budget item at all for agents running on Cloudflare's edge.

Everything above currently rests on one relay. The ticket is opened because
the claim is specific and falsifiable — named bases, named evals, named
latencies — and the primary sources it cites are easy to check.
