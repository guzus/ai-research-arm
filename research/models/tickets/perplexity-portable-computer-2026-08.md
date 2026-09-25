---
slug: perplexity-portable-computer-2026-08
title: Perplexity Portable Computer — fully local agent runtime on NVIDIA DGX Spark
company: Perplexity / NVIDIA
model: PPLX 27B (post-trained on Qwen)
status: released
status_note: |
  **2026-09-24 — second hardware platform, and an AMD partnership.**
  @perplexity_ai (primary): "Portable Computer for Windows is now available on
  @AMD Ryzen AI Max Series processors. It makes it easy to run local AI agents
  that work with your connected apps and local files. Kick off tasks or schedule
  recurring work that runs entirely on your device." AMD's @jackhuynh announced
  the partnership from the other side the same morning, framing it as bringing
  Portable Computer to **AMD Ryzen AI Halo** and "creating a new kind of agentic
  PC". @AravSrinivas relayed.

  This answers the largest open item on this ticket — "LOCAL-runtime availability
  beyond DGX Spark" — with an **x86 Windows** platform rather than the DGX
  Station or Apple-silicon paths that were anticipated. Two vendors announcing
  from both ends makes this the best-sourced update the ticket has had.

  **Note the naming inconsistency, unresolved.** Perplexity says "Ryzen AI Max
  Series"; AMD says "Ryzen AI Halo". These are plausibly the same silicon under
  product-marketing and codename, but nothing in-window states that, and it is
  recorded rather than smoothed over.

  **Aged-close trigger deliberately deferred.** Portable Computer shipped
  2026-08-25, which is past the four-week `released-and-aged` threshold. It is
  NOT closed this cycle because a new hardware platform and a named OEM
  partnership landed today — the trigger is meant to retire artifacts that have
  rolled into normal coverage, and this one is still actively shipping surface.
  Revisit next cycle.

  **Separate Perplexity artifact shipped the same day:** Fast Search on the
  Photon engine — [[perplexity-photon-fast-search-2026-09]].

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
  **2026-09-16 — first OEM pre-install, and it is NOT the local runtime.**
  @perplexity_ai (2026-09-15 15:02 UTC): "Perplexity **Computer** will now come
  pre-installed on **HP ZBook Ultra G3a**. Use Computer to run complex
  multi-step work from a simple interface. Computer agents are grounded in
  accurate deep research and connected to hundreds of tools, now including
  **Autodesk**." Read the product name carefully: this is *Perplexity
  Computer*, the cloud product, shipping on an OEM workstation — **not**
  *Portable Computer*, the fully-local DGX Spark runtime this ticket tracks.
  It is logged here because this ticket's own `expected` names "availability
  beyond DGX Spark" as the open question, and an OEM pre-install is the
  commercial answer to it arriving on the cloud side first. Do not read it as
  local-runtime distribution.

  **Second-order signal on the same axis:** @AravSrinivas disclosed
  (2026-09-15 20:16 UTC) that Perplexity built **CobbleDB**, an in-house
  DynamoDB replacement, with "two engineers and hundreds of persistent
  Computer agents over two months", claiming up to **$100M/year** in savings.
  First-party, unaudited, and a claim about the agent harness rather than
  about the local runtime — recorded as the strongest in-house usage datapoint
  for Computer to date, not as a benchmark.
expected: "Shipped 2026-08-25 for NVIDIA DGX Spark; expanded 2026-09-24 to Windows on AMD Ryzen AI Max Series / Ryzen AI Halo via an AMD partnership. Pending: the benchmark behind the 82.6%/85.4% 'real knowledge work' figures named and independently run; whether 'Ryzen AI Max Series' (Perplexity) and 'Ryzen AI Halo' (AMD) denote the same silicon; DGX Station and Apple-silicon support; Nemotron 3.5 Lightning support; and whether the cloud-escalation path preserves the no-cloud-dependency claim in practice. Note the first OEM pre-install (HP ZBook Ultra G3a, 2026-09-15) is the CLOUD Computer product, not this one."
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
  - https://x.com/perplexity_ai/status/2099876468872638717
  - https://x.com/AravSrinivas/status/2099957318935028173
  - https://x.com/perplexity_ai/status/2103161414919872628
  - https://x.com/jackhuynh/status/2103157519719842037
created_at: 2026-08-26
updated_at: 2026-09-25
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-26
    change: "Created — Perplexity shipped Portable Computer on 2026-08-25 (@perplexity_ai 15:10 UTC, ~4.3K engagement): 'a fully local version of Perplexity Computer, where the entire runtime: orchestrator LLM, subagent LLM, agent harness all run on your local hardware. No cloud dependency.' Launching for NVIDIA DGX Spark. Its research post (18:43 UTC) publishes numbers: with an on-device 27B model the harness scores 82.6% on 'real knowledge work', beating the open-source harnesses Pi and Hermes, and its own post-trained PPLX 27B reaches 85.4%. @AravSrinivas gives the thesis — 'In a compute and power-constrained world, a good chunk of agentic inference needs to move to local hardware. A drastic version of that is a fully local agent runtime' — and the architecture constraint: co-design of model and harness, first version post-trained on top of Qwen, with Nemotron 3.5 Lightning intended next, and an orchestrator that can escalate to a cloud frontier model with user permission. NVIDIA's own account promoted it ('one-click local inference setup and an optimized agentic experience for DGX Spark'), NVIDIARTXSpark congratulated the launch, and @AravSrinivas says Jensen Huang gifted the team a DGX Station after seeing an early demo — the same commercial relationship that the separately-reported NVIDIA investment talks would formalise ([[nvidia-perplexity-investment-2026-08]]). @NaderLikeLadder supplies the honest framing of why now: 'Local AI hit an inflection point with frontier open source models like GLM 5.2, Deepseek v4 flash, and Nemotron + hardware powerful enough to run them ... The current bottleneck is the know-how to set up inference and get meaningful performance out of it' — i.e. the product is packaging, not a capability breakthrough. Status released (available today, named hardware target, first-party launch); verification confirmed on Perplexity's and NVIDIA's own accounts. What is NOT established: the '82.6% on real knowledge work' benchmark is unnamed and vendor-run, the Pi/Hermes comparison is Perplexity scoring its competitors, and the cloud-escalation path is in tension with the headline 'no cloud dependency' claim. Lands the same day Apple announced 512GB/1.2TB/s local-inference hardware ([[apple-m5-ultra-mac-studio-2026-08]]), with practitioners immediately arguing DGX Spark just lost its price/performance case."
  - ts: 2026-09-16
    change: "First OEM pre-install lands — on the CLOUD product, not this one. @perplexity_ai (2026-09-15 15:02 UTC): 'Perplexity Computer will now come pre-installed on HP ZBook Ultra G3a. Use Computer to run complex multi-step work from a simple interface. Computer agents are grounded in accurate deep research and connected to hundreds of tools, now including Autodesk.' Logged here because this ticket's expected: field names 'availability beyond DGX Spark' as the open question and an OEM workstation pre-install is the first commercial answer on that axis — but the product named is Perplexity COMPUTER, the cloud product, NOT Portable Computer, the fully-local DGX Spark runtime this ticket tracks. Deliberately not read as local-runtime distribution, and the local-availability question stays open. Autodesk tool integration is new and is a vertical-workstation signal consistent with the HP ZBook target. SECOND-ORDER, same window: @AravSrinivas (2026-09-15 20:16 UTC) disclosed that Perplexity built CobbleDB, an in-house DynamoDB replacement serving web content for search, with 'two engineers and hundreds of persistent Computer agents over two months', claiming savings of 'up to a hundred million dollars yearly'; @perplexity_ai published the research. First-party and unaudited, and a claim about the agent harness rather than the local runtime — recorded as the strongest in-house usage datapoint for Computer to date, not as a benchmark and not as evidence for the 82.6%/85.4% figures, which remain vendor-run and unnamed. Status stays released; verification stays confirmed."
  - ts: 2026-09-25
    change: "Released, unchanged. Platform expansion with two-sided primary sourcing: @perplexity_ai announced on 2026-09-24 16:35 UTC (~317 likes) that Portable Computer for Windows is now available on AMD Ryzen AI Max Series processors, running local agents against connected apps and local files with scheduled recurring on-device work; AMD's @jackhuynh announced the same partnership from AMD's side that morning (~456 likes plus an @AravSrinivas RT), framing it as bringing Portable Computer to AMD Ryzen AI Halo and 'creating a new kind of agentic PC'. This resolves the ticket's largest open item — local-runtime availability beyond DGX Spark — via an x86 Windows path rather than the DGX Station or Apple-silicon routes previously anticipated. Recorded unsmoothed: Perplexity says 'Ryzen AI Max Series' and AMD says 'Ryzen AI Halo', plausibly the same silicon under two names, but nothing in-window states that. CLOSURE NOTE, stated explicitly: this ticket shipped 2026-08-25 and is 31 days old, past the four-week released-and-aged threshold, and is deliberately NOT closed this cycle because a new hardware platform and a named OEM partnership landed today — the trigger exists to retire artifacts that have rolled into routine coverage, which this has not. Re-evaluate for closure next cycle. Separately, Perplexity shipped an unrelated artifact the same day, tracked at [[perplexity-photon-fast-search-2026-09]]."
  - ts: 2026-09-25
    change: "Bookkeeping — citations added for the 2026-09-25 entry: @perplexity_ai (Portable Computer for Windows now available on AMD Ryzen AI Max Series) and AMD's @jackhuynh (the partnership announced from AMD's side, framed as Ryzen AI Halo and 'a new kind of agentic PC'). No status, verification or content change."
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
