---
slug: mistral-leanstral-1-5
title: Mistral ships Leanstral 1.5 — open-weight formal-verification model for Lean 4
company: Mistral AI
model: Leanstral 1.5
status: released
status_note: |
  Mistral shipped **Leanstral 1.5** ("Proof Abundance for All"), an
  **open-weight (Apache 2.0), 119B-A6B MoE** formal-verification model for
  **Lean 4** — primary announcement on Mistral's own blog
  (mistral.ai/news/leanstral-1-5) plus a dated model card
  (docs.mistral.ai, 2026-06-26/30), with weights live on Hugging Face
  (mistralai/Leanstral-1.5-119B-A6B). It **saturates miniF2F** and sets
  **SOTA on FATE-H/FATE-X**, and in a practical demonstration found **5
  previously-unknown bugs** scanning 57 open-source repos. Independently
  corroborated by two separate Hacker News waves (2026-06-30, 309 pts;
  2026-07-03, 364 pts) and The Decoder. Primary blog + model card + live
  weights + multi-wave third-party corroboration → `released` /
  `confirmed`.
expected: null
labels:
  - open-weights
  - formal-verification
  - lean4
  - coding
  - released
verification: confirmed
sources:
  - https://mistral.ai/news/leanstral-1-5/
  - https://docs.mistral.ai/models/model-cards/leanstral-1-5-26-06
  - https://huggingface.co/mistralai/Leanstral-1.5-119B-A6B
created_at: 2026-07-05
updated_at: 2026-07-05
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-05
    change: "Created — Mistral shipped Leanstral 1.5, an Apache-2.0, 119B-A6B MoE formal-verification model for Lean 4 (primary blog + dated model card + live Hugging Face weights). Saturates miniF2F, SOTA on FATE-H/FATE-X, and found 5 previously-unknown bugs across 57 scanned repos. Two independent Hacker News waves (06-30 309pts, 07-03 364pts) plus The Decoder corroborate. Primary source + live artifact + multi-wave third-party pickup → status released, verification confirmed."
---

Mistral released **Leanstral 1.5** ("Proof Abundance for All"), an
**open-weight formal-verification model** built for **Lean 4** proof
engineering. Reported at **119B-A6B** (Mixture-of-Experts), licensed
**Apache 2.0**.

**What ships.** The model **saturates the miniF2F** benchmark and sets
**SOTA on FATE-H/FATE-X**. Beyond leaderboard placement, Mistral
demonstrated a practical capability: scanning 57 open-source repositories
and surfacing **5 previously-unknown bugs** via machine-checked proofs.

**Why `released` / `confirmed`.** Unlike most single-tweet model leaks
this timeline tracks, Leanstral 1.5 has a **primary Mistral blog post**
(mistral.ai/news/leanstral-1-5) and a **dated model card**
(docs.mistral.ai), with **weights live on Hugging Face**
(mistralai/Leanstral-1.5-119B-A6B). Two separate Hacker News submissions
(2026-06-30 and 2026-07-03) both cleared 300+ points, and The Decoder
covered it independently — a genuine two-source-plus-primary
convergence, not a single-outlet tease.

**Why its own ticket.** Formal verification (machine-checked Lean 4
proofs) is a distinct frontier from the general coding/agentic benchmarks
most 2026 open-weight releases compete on — complementary rather than a
head-to-head rival to models like [[zhipu-glm-5-2]] or
[[meituan-longcat-2-2026-06]]. An earlier "Leanstral" (implicitly v1) shipped
back in March 2026 as part of a bundled Mistral release wave, tracked only
in the pre-ticket legacy timeline tables — this ticket covers the distinct
1.5 release and its own evidence trail.

**Transition triggers:**
- Independent (non-Mistral-benchmark) evaluation of the bug-finding claim,
  or adoption inside formal-methods/safety-critical teams → UPDATE.
- A successor (Leanstral 2.x) → new ticket; do not reopen this one.
- ≥4 weeks settled into normal coverage → `closed: released-and-aged`.

**Dedup note:** further Leanstral 1.5 signal (benchmarks, adoption,
follow-on versions) UPDATES this ticket.
