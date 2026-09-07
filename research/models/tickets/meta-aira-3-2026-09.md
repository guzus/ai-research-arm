---
slug: meta-aira-3-2026-09
title: AIRA₃ — Meta's autonomous AI research system, Kaggle gold at 8th of ~4,000
company: Meta (Meta Superintelligence Labs)
model: AIRA₃
status: confirmed
status_note: |
  Disclosed 2026-09-05 by @AIatMeta. In June, Meta entered AIRA₃ — the next
  generation of its autonomous AI research system — into a **live Kaggle
  competition run by NVIDIA** to fine-tune a 30B Nemotron model for better
  reasoning, with all competitors on equal information and graded externally on
  a private test set. AIRA₃ placed **8th out of ~4,000 teams**, a gold medal.

  Architecture, per Meta: no central controller. AIRA₃ runs many long-running
  agents — each a model paired with a coding harness, in its own isolated
  environment — coordinating asynchronously through two shared substrates, a
  **forum** for hypotheses and findings and a **shared filesystem** for solution
  artifacts.

  The disclosure is unusually honest about which models did the work: the gold
  entry ensemble was **GPT 5.5 (w/ OpenCode) + Claude 4.8 (w/ ClaudeCode)** —
  competitors' models, not Meta's. Post-hoc, Meta assessed Muse Spark 1.2 (w/
  MuseCode) at gold-medal level, and Muse Spark 1.1 (w/ OpenCode) and GLM 5.2
  (w/ OpenCode) at silver. Generalization claims beyond Kaggle: a **27% latency
  reduction on production GPU kernels** and gold-level performance translating
  4,000-year-old Akkadian clay tablets, changing only the task specification.

  Status `confirmed` (Meta's own disclosure of a completed, externally-graded
  result), not `released` — AIRA₃ is an internal system, not a product anyone
  can use.
expected: "No public availability announced. Watch for whether Meta productizes the multi-agent forum/filesystem substrate, and whether a Muse-only ensemble reaches gold without competitor models."
labels:
  - meta
  - autonomous-research
  - multi-agent
  - benchmark
verification: confirmed
sources:
  - https://x.com/AIatMeta/status/2096271545589190927
  - https://x.com/AIatMeta/status/2096271550517575918
  - https://x.com/AIatMeta/status/2096271547229167748
  - https://x.com/AIatMeta/status/2096271554237936107
created_at: 2026-09-07
updated_at: 2026-09-07
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-07
    change: "Created — CONFIRMED. @AIatMeta disclosed on 2026-09-05 16:17 UTC that AIRA₃, the next generation of its autonomous AI research system, was entered in June into a live NVIDIA-run Kaggle competition to fine-tune a 30B Nemotron model for better reasoning — equal information for all entrants, externally graded on a private test set — and placed 8th of ~4,000 teams for a gold medal. Architecture: no central controller; many long-running agents (model + coding harness) in isolated environments coordinating asynchronously via a shared forum for hypotheses/findings and a shared filesystem for solution artifacts. Notably, the gold entry ensemble ran on competitors' models — GPT 5.5 with OpenCode plus Claude 4.8 with ClaudeCode — with Muse Spark 1.2 (MuseCode) assessed post-hoc at gold level and Muse Spark 1.1 (OpenCode) and GLM 5.2 (OpenCode) at silver. Generalization claims: 27% latency reduction on production GPU kernels and gold-level performance translating Akkadian clay tablets, changing only the task specification. Status confirmed rather than released: AIRA₃ is an internal system with no public availability."
---

The result worth arguing about is not the gold medal, it is which models earned
it. Meta's own writeup says the 8th-place ensemble was GPT 5.5 with OpenCode and
Claude 4.8 with ClaudeCode — OpenAI's and Anthropic's models inside Meta's
research harness. Meta then assessed Muse Spark 1.2 post-hoc at gold level, but
that is a post-hoc assessment, not the live entry. A lab publishing a headline
autonomous-research result achieved on its competitors' models is a claim about
the *harness* being the contribution, and Meta is unusually explicit about it.

That framing also makes AIRA₃ the clearest external data point on the question
OpenAI raised the next day
([[openai-automated-research-intern-2026-09]]): how much research can be
delegated. OpenAI reports a ratio — 3.1 agent-workdays per human workday — from
inside its own organization, which nobody can check. Meta reports a placement in
a live, externally-graded competition against ~4,000 human teams, which is a
weaker claim about autonomy but a much harder number to game.

The no-central-controller design is the part most likely to matter downstream.
Agents coordinating through a shared forum and filesystem rather than an
orchestrator is a bet that research parallelism is bounded by communication
substrate, not by planning. If Meta ships that substrate, it is more
consequential than the medal.
