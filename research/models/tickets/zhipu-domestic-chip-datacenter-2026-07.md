---
slug: zhipu-domestic-chip-datacenter-2026-07
title: Z.ai/Zhipu 1GW data center built entirely on domestic (non-Nvidia) chips
company: Zhipu AI / Z.ai
model: null
status: confirmed
status_note: |
  Bloomberg-sourced report (via secondary amplification) that Z.ai
  completed construction of and began partial operations at a
  1-gigawatt AI data center built entirely with domestic Chinese chips,
  with no Nvidia hardware — enough power for roughly 750,000 homes.

  **2026-09-04 — Zhipu confirmed the domestic-silicon claim in a filing.** Per
  @SemiAnalysis_, Zhipu ($2513.HK) filed its first interim report as a public
  company on 2026-08-31 — 19 of its 60 pages read like a technical blog, plus a
  9-page technical glossary — and **officially disclosed for the first time that
  it runs inference on over 100k Chinese accelerators**. SemiAnalysis flags a
  translation ambiguity worth preserving: the English report said "a cluster
  of...", but the Chinese original says only "100k-level" without claiming a
  single cluster. That distinction matters for exactly the question this ticket
  tracks, so it is recorded rather than smoothed over.

  Also in the filing: a GLM-5.3-powered internal infrastructure agent that Zhipu
  says halved the time needed to optimize its infra, a definition of the SOTA
  pareto frontier as iteration speed x intelligence index x per-task cost, and
  two research directions — **Loop Transformer** (layer recycling for depth,
  "shifting compute from remembering to thinking," which SemiAnalysis notes
  OpenAI's Astra is *rumoured* to already use, see [[openai-gpt-6]]) and the claim
  that "the speed of environment building is becoming the new bottleneck."
  Verification advances partial -> confirmed: a filed interim report is a primary
  source.
expected: null
labels:
  - infrastructure
  - china
verification: confirmed
sources:
  - https://x.com/kimmonismus/status/2079283578735640886
  - "@Polymarket"
  - https://x.com/SemiAnalysis_/status/2095919853471224118
created_at: 2026-07-21
updated_at: 2026-09-07
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-21
    change: Created — Bloomberg-sourced report that Z.ai completed and began partial operations of a 1GW AI data center built entirely on domestic (non-Nvidia) chips.
  - ts: 2026-09-07
    change: "Domestic-accelerator claim confirmed in a filing. Per @SemiAnalysis_ (2026-09-04), Zhipu ($2513.HK) filed its first interim report as a public company on 2026-08-31 and officially disclosed for the first time that it runs inference on over 100k Chinese accelerators. Recorded with SemiAnalysis's caveat intact: the English translation said 'a cluster of...', but the Chinese original says only '100k-level' without asserting a single cluster — a distinction that matters directly to this ticket. The filing also discloses a GLM-5.3-powered internal infra agent that halved infra optimization time, defines the SOTA pareto frontier as iteration speed x intelligence index x per-task cost, and names two research directions: Loop Transformer (layer recycling for depth, which SemiAnalysis notes OpenAI's Astra is rumoured to already use, see [[openai-gpt-6]]) and RL environment-building speed as the new bottleneck. Verification partial -> confirmed on the primary filing; status stays confirmed."
---

A Bloomberg-sourced report, relayed by multiple accounts, says Z.ai
(Zhipu) completed construction of and began partial operations at a
1-gigawatt AI data center built entirely using domestic Chinese chips —
no Nvidia hardware — with enough power capacity for roughly 750,000
homes. This is a compute-infrastructure milestone distinct from the
existing `zhipu-glm-5-2` model ticket. Sourced secondhand from Bloomberg
(not Bloomberg's own account directly), so verification is partial
pending a primary link.
