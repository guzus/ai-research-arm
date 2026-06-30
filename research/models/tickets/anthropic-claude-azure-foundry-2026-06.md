---
slug: anthropic-claude-azure-foundry-2026-06
title: Claude GA in Microsoft Foundry on Azure — Anthropic's first NVIDIA-GPU deployment
company: Anthropic / Microsoft
model: Claude Opus 4.8 / Haiku 4.5
status: released
status_note: |
  Announced **2026-06-29** by the official **@claudeai**, **@nvidia**, and
  **@Azure** accounts within the same hour: **Claude Opus 4.8** ([[opus-4-8]])
  and **Claude Haiku 4.5** are now **generally available in Microsoft Foundry**,
  hosted natively on **Azure** with Azure authentication, billing, and
  commitment retirement (prompt caching + extended thinking supported). The
  models run on **NVIDIA GB300 NVL72 (Blackwell Ultra)** systems with
  Quantum-X800 InfiniBand — reported (via @firstadopter, "I am told") to be the
  **first time Anthropic models run on NVIDIA GPUs**, whose stack historically
  leaned on AWS Trainium and Google TPUs. This completes a native Claude
  presence across **all three hyperscaler clouds** (AWS Bedrock, Google Vertex,
  Azure Foundry), and makes Microsoft the only cloud offering both OpenAI and
  Anthropic frontier models on one platform.

  "GA in Foundry" is largely a **procurement/billing integration** — Claude was
  already reachable on Azure indirectly. The genuinely new facts are (a) native
  Azure auth/billing/commitment retirement and (b) the NVIDIA-GPU lane. The GA
  and three official announcements are on-record → status `released`,
  verification `confirmed`; the "first-ever on NVIDIA" superlative is
  single-sourced (@firstadopter) and flagged `partial` in spirit until a
  spec sheet states it directly.
expected: "Live now in Microsoft Foundry. Watch: Foundry pricing/commitment-retirement vs. AWS Bedrock; whether the GB300 deployment is a one-off or a standing Anthropic→NVIDIA compute lane distinct from its Trainium/TPU mix"
labels:
  - distribution
  - anthropic
  - microsoft-azure
  - nvidia
  - released
verification: confirmed
sources:
  - "@claudeai"
  - "@nvidia"
  - "@Azure"
  - "@firstadopter"
  - https://x.com/claudeai/status/2071653958905467027
  - https://x.com/nvidia/status/2071654937335926864
  - https://x.com/Azure/status/2071651695323492418
created_at: 2026-06-30
updated_at: 2026-06-30
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-30
    change: "Created — Claude Opus 4.8 + Haiku 4.5 went GA in Microsoft Foundry on Azure (announced 2026-06-29 by official @claudeai, @nvidia, @Azure within the same hour), hosted natively with Azure auth/billing/commitment retirement, prompt caching + extended thinking. Runs on NVIDIA GB300 NVL72 (Blackwell Ultra) with Quantum-X800 InfiniBand — reported (@firstadopter, 'I am told') as Anthropic's first deployment on NVIDIA GPUs, completing a native Claude presence across AWS Bedrock + Google Vertex + Azure Foundry. Status released (live GA, three official accounts); verification confirmed for the GA, the 'first-ever NVIDIA' superlative single-sourced. Distribution play paired with the California state deal ([[anthropic-california-state-deal-2026-06]]) and the Amazon repricing ([[anthropic-amazon-repricing-2026-06]])."
---

On **2026-06-29**, Anthropic and Microsoft announced that **Claude Opus
4.8** ([[opus-4-8]]) and **Claude Haiku 4.5** are **generally available in
Microsoft Foundry**, hosted natively on **Azure** — with Azure
authentication, billing, and commitment retirement, and support for prompt
caching and extended thinking. The announcement came from the official
**@claudeai**, **@nvidia**, and **@Azure** accounts within the same hour.

The notable infrastructure detail: the models run on **NVIDIA GB300 NVL72
(Blackwell Ultra)** systems with Quantum-X800 InfiniBand networking —
reported by @firstadopter ("I am told") to be the **first time Anthropic
models have run on NVIDIA GPUs**, a stack historically built on AWS
Trainium and Google TPUs.

**Why a separate ticket.** This is a discrete **distribution / partnership
event**, distinct from the Opus 4.8 model lifecycle ([[opus-4-8]]). With
Foundry GA, Claude is now native across **all three hyperscaler clouds**
(AWS Bedrock, Google Vertex, Azure Foundry), and Microsoft becomes the only
cloud offering both OpenAI and Anthropic frontier models on one platform.

**Confirmed vs. reported.** The GA and the three official announcements are
on-record → `released` / `verification: confirmed`. "GA in Foundry" is
mostly a procurement/billing integration; the genuinely new facts are the
native Azure auth/billing/commitment-retirement and the NVIDIA-GPU lane. The
"first-ever Anthropic-on-NVIDIA" superlative rests on one well-placed
commentator until a spec sheet states it.

**Context.** This is the second distribution pillar in 48h after the
California state-government deal ([[anthropic-california-state-deal-2026-06]])
and the Amazon repricing ([[anthropic-amazon-repricing-2026-06]]) — Anthropic
converting model scarcity into omni-cloud reach rather than a single cloud
patron, even as the frontier-export gate
([[anthropic-fable-mythos-export-control-2026-06]]) constrains who can use
its strongest weights.

**Transition triggers:**
- Foundry pricing / commitment-retirement terms vs. AWS Bedrock → UPDATE.
- Confirmation the GB300 deployment is a standing Anthropic→NVIDIA lane (or a
  one-off) → UPDATE.
- ≥4 weeks settled into normal coverage → `closed: released-and-aged`.

**Dedup note:** further Claude-on-Azure-Foundry distribution signal UPDATES
this ticket. Opus 4.8 / Haiku model-capability signal stays on [[opus-4-8]].
