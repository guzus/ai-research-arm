---
slug: agent-lifespan-engineering
title: Agent Lifespan Engineering
type: concept
aliases: ["Agent Lifespan Engineering", "agent half-life", "AgingBench", "Your Agents Are Aging Too"]
tags: [agents, evaluation, benchmarks, memory, deployment]
summary: Treating deployed agentic systems as objects whose effectiveness degrades over a deployment horizon, with memory policy — not model strength — as the dominant variable; the underlying frame of the 2026-05-29 AgingBench paper.
created_at: 2026-05-29
updated_at: 2026-05-29
sources:
  - {title: "ARA daily digest 2026-05-29", path: research/digest/2026-05-29-digest.md}
  - {title: "Your Agents Are Aging Too — r/MachineLearning", url: "https://www.reddit.com/r/MachineLearning/", date: 2026-05-29}
---

**Agent Lifespan Engineering** is the framing — coined in the **AgingBench /
"Your Agents Are Aging Too: Agent Lifespan Engineering for Deployed Systems"**
paper on r/MachineLearning, 2026-05-29 — that an agentic system's
effectiveness should be measured as a **lifespan curve over a deployment
horizon**, not as a single-shot score, and that **memory policy is the
dominant variable** in that curve.

## Why it matters
- **The "just upgrade the model" instinct is empirically wrong.** AgingBench
  reports that swapping **Sonnet 4.6 → Opus 4.7** in Claude Code CLI *dropped*
  PyTest pass rate by **~15%** over the deployment horizon. The frontier-er
  model was worse in the deployed-agent setting (ARA digest 2026-05-29).
- **Memory policy ≫ model choice.** **Memory policy alone produced a 4.5×
  spread in agent "half-life."** The dominant lever for production-agent
  longevity is how the agent curates and forgets, not which Claude/GPT model
  sits underneath.
- **Direct relevance to fan-out agents.** [[dynamic-workflows]] makes
  hundreds of subagent lifespans run in parallel from a single parent
  session. Agent Lifespan Engineering predicts that the relevant question is
  not "which model do the subagents use" but "what is the parent's memory
  policy for them."
- **Pairs with the disagreement counter-signal.** The same digest carried
  the Lenz Research finding that **five frontier LLMs disagree on 67% of
  1,000 real-world fact-check claims** (164 pts on HN). Together, the two
  results define the day's "reliability + cost" reliability narrative
  against the "just ship a bigger model" frame (ARA digest 2026-05-29).

## Open questions
- **Generalization.** Does the Sonnet → Opus regression generalize beyond
  Claude Code CLI / PyTest, or is it a benchmark-specific artifact?
- **What constitutes a "memory policy"?** AgingBench's 4.5× spread is the
  punchline; the underlying design space (rolling-window vs. summarized
  vs. retrieval-backed memory, eviction priority, etc.) needs taxonomic
  work to be actionable.
- **Counter-signal to Mythos GA?** If frontier model strength has rapidly
  diminishing returns on deployed-agent half-life, what does that imply for
  Anthropic's Mythos-class GA rollout (see [[anthropic]])?
