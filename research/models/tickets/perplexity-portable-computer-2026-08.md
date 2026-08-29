---
slug: perplexity-portable-computer-2026-08
title: Perplexity Portable Computer — fully local agent runtime on NVIDIA DGX Spark
company: Perplexity / NVIDIA
model: PPLX 27B (post-trained on Qwen)
status: released
status_note: |
  Launched 2026-08-25 (@perplexity_ai 15:10 UTC, ~4.3K engagement): "Today
  we're launching Portable Computer on @NVIDIA DGX Spark. Portable Computer is
  a fully local version of Perplexity Computer, where the entire runtime:
  orchestrator LLM, subagent LLM, agent harness all run on your local hardware.
  **No cloud dependency.**"

  Published numbers (@perplexity_ai research post, 18:43 UTC): with an
  **on-device 27B model**, the harness scores **82.6%** on "real knowledge
  work," which Perplexity says beats the open-source harnesses **Pi and
  Hermes**; its own post-trained **PPLX 27B** reaches **85.4%**. @AravSrinivas
  adds the design constraint: "you need co-design of the model and the harness.
  The first version ships with a post-trained model on top of **Qwen**, but we
  intend to support **Nemotron 3.5 Lightning** and more models in the future.
  Post-training also allows the orchestrator to **escalate to a cloud frontier
  with user permission**."

  NVIDIA's own account promoted the launch the same day, and @AravSrinivas says
  Jensen Huang gifted the team a **DGX Station** after an early demo — which is
  the commercial relationship the separately-reported NVIDIA investment
  ([[nvidia-perplexity-investment-2026-08]]) would formalise.
expected: "Shipped 2026-08-25 for NVIDIA DGX Spark, first version on a Qwen-post-trained PPLX 27B. Pending: the benchmark behind the 82.6%/85.4% 'real knowledge work' figures named and independently run, availability beyond DGX Spark (DGX Station, and the Apple-silicon class of hardware announced the same day), Nemotron 3.5 Lightning support, and whether the cloud-escalation path preserves the no-cloud-dependency claim in practice"
labels:
  - agents
  - local-inference
  - perplexity
  - nvidia
  - released
verification: confirmed
sources:
  - "@perplexity_ai"
  - "@AravSrinivas"
  - "@nvidia"
  - "@NaderLikeLadder"
created_at: 2026-08-26
updated_at: 2026-08-26
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-26
    change: "Created — Perplexity shipped Portable Computer on 2026-08-25 (@perplexity_ai 15:10 UTC, ~4.3K engagement): 'a fully local version of Perplexity Computer, where the entire runtime: orchestrator LLM, subagent LLM, agent harness all run on your local hardware. No cloud dependency.' Launching for NVIDIA DGX Spark. Its research post (18:43 UTC) publishes numbers: with an on-device 27B model the harness scores 82.6% on 'real knowledge work', beating the open-source harnesses Pi and Hermes, and its own post-trained PPLX 27B reaches 85.4%. @AravSrinivas gives the thesis — 'In a compute and power-constrained world, a good chunk of agentic inference needs to move to local hardware. A drastic version of that is a fully local agent runtime' — and the architecture constraint: co-design of model and harness, first version post-trained on top of Qwen, with Nemotron 3.5 Lightning intended next, and an orchestrator that can escalate to a cloud frontier model with user permission. NVIDIA's own account promoted it ('one-click local inference setup and an optimized agentic experience for DGX Spark'), NVIDIARTXSpark congratulated the launch, and @AravSrinivas says Jensen Huang gifted the team a DGX Station after seeing an early demo — the same commercial relationship that the separately-reported NVIDIA investment talks would formalise ([[nvidia-perplexity-investment-2026-08]]). @NaderLikeLadder supplies the honest framing of why now: 'Local AI hit an inflection point with frontier open source models like GLM 5.2, Deepseek v4 flash, and Nemotron + hardware powerful enough to run them ... The current bottleneck is the know-how to set up inference and get meaningful performance out of it' — i.e. the product is packaging, not a capability breakthrough. Status released (available today, named hardware target, first-party launch); verification confirmed on Perplexity's and NVIDIA's own accounts. What is NOT established: the '82.6% on real knowledge work' benchmark is unnamed and vendor-run, the Pi/Hermes comparison is Perplexity scoring its competitors, and the cloud-escalation path is in tension with the headline 'no cloud dependency' claim. Lands the same day Apple announced 512GB/1.2TB/s local-inference hardware ([[apple-m5-ultra-mac-studio-2026-08]]), with practitioners immediately arguing DGX Spark just lost its price/performance case."
---

**Portable Computer** is Perplexity's local-first agent runtime, launched
2026-08-25 for **NVIDIA DGX Spark**. The claim is total locality: orchestrator
LLM, subagent LLM and agent harness all run on the user's hardware, with **no
cloud dependency**.

**The numbers Perplexity published.** With an on-device 27B model, the harness
scores **82.6%** on what it calls "real knowledge work," beating the
open-source harnesses **Pi** and **Hermes**; its own post-trained **PPLX 27B**
reaches **85.4%**.

**The architecture argument.** @AravSrinivas: "In a compute and
power-constrained world, a good chunk of agentic inference needs to move to
local hardware." Getting there requires **co-designing the model and the
harness** — the first release ships a model post-trained on top of **Qwen**,
with **Nemotron 3.5 Lightning** intended next. Post-training also lets the
orchestrator **escalate to a cloud frontier model with user permission**.

**Why now, honestly.** @NaderLikeLadder — who demoed an early version to
Jensen Huang — describes the enabling conditions as frontier open-weight
models (GLM 5.2, DeepSeek V4 Flash, Nemotron) plus hardware capable of running
them, with the remaining bottleneck being *setup know-how*. On that account
the product is **packaging**, not a capability breakthrough, which is a
reasonable thing for it to be.

**What is not established.** The "82.6% on real knowledge work" benchmark is
**unnamed and vendor-run**, and the Pi/Hermes comparison is Perplexity scoring
its own competitors. The user-permissioned cloud-escalation path also sits in
tension with the headline "no cloud dependency" — both can be true, but the
marketing line describes the default rather than the ceiling.

**Adjacent, same day.** Apple announced 512GB/1.2TB/s unified-memory hardware
and a clustered "trillion parameter models locally" claim
([[apple-m5-ultra-mac-studio-2026-08]]), with several practitioners arguing
DGX Spark's price/performance case just got substantially worse. Whether
Portable Computer stays DGX-Spark-only is therefore a live question about the
product's reach, not a detail.

**Transition triggers:**
- Availability beyond DGX Spark (DGX Station, other hardware) → UPDATE.
- The knowledge-work benchmark named, or independently run → UPDATE and firm
  the capability claim.
- Nemotron 3.5 Lightning or additional model support ships → UPDATE.

**Dedup note:** further Portable Computer / PPLX-27B signal UPDATES this
ticket. The reported NVIDIA investment in Perplexity stays on
[[nvidia-perplexity-investment-2026-08]].
