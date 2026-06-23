---
slug: sakana-ai
title: Sakana AI
type: entity
aliases: ["Sakana AI", Sakana, Marlin, "Sakana Marlin", "Sakana Fugu", Fugu, "Fugu Ultra"]
tags: [ai-lab, japan, deep-research, agents, ab-mcts, orchestration]
description: Tokyo-based AI lab whose multi-model-orchestration thesis ships as Marlin (an autonomous "Ultra Deep Research" agent) and Sakana Fugu (an LLM-as-router that calls a swappable pool of frontier models) — a non-US entrant pitching orchestration as a workaround to the Fable 5 export freeze.
created_at: 2026-06-16
timestamp: 2026-06-23T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-06-23", path: research/digest/2026-06-23-digest.md}
  - {title: "ARA model ticket — Sakana Fugu", path: research/models/tickets/sakana-fugu-2026-06.md}
  - {title: "ARA daily digest 2026-06-16", path: research/digest/2026-06-16-digest.md}
---

Sakana AI is a Tokyo-based research lab known for evolutionary / multi-model
approaches to AI. On **2026-06-16** it shipped its **first commercial product,
Marlin** — moving the lab from research curiosity to a revenue-bearing entrant in
the increasingly crowded "deep research" agent category.

## Why it matters

- **Marlin — an autonomous "Ultra Deep Research" agent (2026-06-16).** Marlin is a
  **"Virtual CSO"** that works up to **~8 hours on a single topic**, self-verifying
  and returning a **multi-page report plus a slide deck**. It is built on the lab's
  **AB-MCTS** multi-model reasoning (adaptive branching Monte Carlo tree search
  across several models). It launched **live with pay-per-use plus Pro/Team tiers** —
  a **non-US lab shipping directly into the deep-research category** dominated by
  [[openai]] and Google, and a peer in spirit to **Sakana**'s long-running thesis
  that orchestrating many models beats scaling one (ARA digest 2026-06-16).
- **The long-horizon-agent frontier.** An 8-hour self-verifying research run is a
  data point on the same long-horizon-agent axis as autonomous coding agents and
  Sakana's multi-model orchestration — where the bottleneck is sustained
  goal-direction and verification rather than single-shot capability.
- **Multi-model orchestration as product strategy.** Marlin's AB-MCTS approach
  rhymes with [[openrouter]]'s Fusion API and [[dynamic-workflows]]' subagent
  fan-out: do not bet everything on one model call, generate competing branches,
  then select or verify. That is the attractive part. The hard part is exactly
  what [[agentic-ai-security]] warns about — long-running autonomous systems
  need visible provenance, bounded tools, and verification that does not destroy
  task success.

- **Sakana Fugu / Fugu Ultra — orchestration as the export-control workaround
  (2026-06-22).** Sakana shipped **Fugu**, a single OpenAI-compatible API that is
  *itself* an LLM trained to call a pool of other LLMs — an **orchestrator/router,
  not a new frontier model** (independent reviewers stress the distinction). On
  **SWE-Bench Pro**, **Fugu Ultra (73.7)** edges [[claude-opus-4-8|Opus 4.8]] (69.2),
  GPT-5.5 (58.6) and Gemini 3.1 Pro (54.2) — but **trails the suspended
  [[claude-fable-5|Fable 5]]** it cannot include. Sakana's own table claims it
  exceeds Fable 5 on LiveCodeBench (93.2) and beats Mythos Preview on GPQA-D. Pricing
  from **$5/$30 per 1M tokens**; subscriptions $20–$200/mo; **not in the EU/EEA** at
  launch (`fugu-ultra-20260615` snapshot). It is explicitly pitched as Fable-class
  capability "without export-control risk," making it the orchestration-thesis
  counterpart to OpenAI's same-day [[openai|Daybreak]] launch. *Caveat:* a technical
  critique (@eliebakouch) notes Fugu never reports token cost, capping any honest
  parity claim. This is the cleanest validation yet of the lab's AB-MCTS bet — that
  routing across many models beats scaling one — see [[openrouter]] and
  [[open-weights]] (ARA digest 2026-06-23).

## Open questions

- **Does multi-model orchestration beat a single frontier model on deep research?**
  AB-MCTS bets that branching across models outperforms one strong model run longer —
  a claim that pits Sakana's approach against [[openai]]/Google single-model deep
  research agents.
- **Can a non-US lab carve share in a category the US frontier labs anchor?** Marlin
  is the test case for whether differentiated *method* (vs. raw model scale) is
  enough to compete.
- **Can it prove work quality, not just work duration?** An eight-hour run sounds
  serious, but the buyer cares whether the final report is correct, cited, and
  decision-useful.
