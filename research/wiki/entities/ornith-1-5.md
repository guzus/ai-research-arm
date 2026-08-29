---
slug: ornith-1-5
title: Ornith-1.5
type: entity
aliases: ["Ornith 1.5", "Ornith", "Ornith-1.5 family"]
tags: [open-weights, mit, self-improving, local-inference]
description: Open-weights 9B dense / 35B MoE / 397B MoE model family shipped under MIT on 2026-08-20 by the lab Ornith, claiming Claude Opus 4.8-class scores from a training loop that writes its own RL tasks — every number self-reported with no independent eval landed yet.
created_at: 2026-08-20
timestamp: 2026-08-20T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-08-20", path: research/digest/2026-08-20-digest.md}
---

**Ornith-1.5** is an open-weights model family shipped by the lab **Ornith**
under an **MIT license on 2026-08-20**: three sizes — **9B dense, 35B MoE and
397B MoE** — released same-day with **FP8, GGUF, MLX and NVFP4 quantizations**,
claimed scores of **86.1 Terminal-Bench 2.1, 86 SWE-Bench Verified, 65.1
SWE-Bench Pro, 44.6 HLE, and 71.2 Tool Decathlon**, and a headline thesis: a
**training loop that writes its own RL tasks** (Twitter/@ornith_, HN; ARA daily
digest 2026-08-20).

## Why it matters

- **The claim is frontier-scale and fully self-published.** The scores would put
  Ornith-1.5's top tier in **[[claude-opus-4-8]]-class** agentic/coding
  territory from a team outside the major labs — but **every number is
  self-reported and no independent eval has landed**, and the release drew a
  cluster of near-identical praise posts from low-follower accounts inside
  three minutes. The digest's read is blunt: **amplification rather than
  corroboration**.
- **Read alongside the fragility paper.** It arrives the same cycle as arXiv
  2608.18066, "On the Fragility of Self-Improving Agents," which argues
  memory-based self-improving agents show **high across-run variance,
  task-order dependence, and underspecification** as hidden prerequisites for
  their reported wins — the paper this release's self-improvement claim should
  be weighed against (see the [[open-weights]] theme for both together).
- **MIT plus day-0 quantizations is the open playbook fully executed.** As with
  [[zhipu-glm-5-2|GLM-5.2]] and [[deepseek-v4-flash|V4-Flash]] before it, the
  release posture — permissive license and instant ecosystem builds — is
  designed to make the weights the default choice regardless of how the
  benchmark claims age (ARA daily digest 2026-08-20).

## Open questions

- **Does any independent eval reproduce the four headline numbers?** Until one
  does, the class-level claim stays vendor-supplied.
- **What is Ornith the company?** The lab is new to the board — no prior
  releases, funding, or principal naming was captured in-window.