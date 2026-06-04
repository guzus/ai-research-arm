---
slug: minimax-m3
title: MiniMax M3
type: entity
aliases: ["MiniMax M3", "M3", "MiniMax-M3", MiniMax]
tags: [open-weights, model, agentic-coding, chinese-llm, long-context]
summary: MiniMax's open-weights model with 1M context and 59% SWE-Bench Pro — the strongest open-weights agentic-coding model of the cycle.
created_at: 2026-06-03
updated_at: 2026-06-04
sources:
  - {title: "ARA daily digest 2026-06-03", path: research/digest/2026-06-03-digest.md}
  - {title: "ARA daily digest 2026-06-04", path: research/digest/2026-06-04-digest.md}
---

**MiniMax M3** is an open-weights model from the Chinese lab MiniMax, shipping
with a **1M-token context window** and **59% SWE-Bench Pro** — the **strongest
open-weights agentic-coding model of the cycle** (ARA digest 2026-06-03). It
lands the same week as Microsoft's [[microsoft|MAI-Code-1-Flash]] (51%) and
ahead of it on the agentic-coding benchmark despite being fully open.

## Why it matters

- **Open-weights agentic frontier.** At 59% SWE-Bench Pro, M3 closes much of the
  gap to closed agentic-coding leaders (OpenAI's GPT-5.2-Codex and Claude Code
  from [[anthropic]]) while remaining downloadable — the clearest 2026 data
  point for Nathan Lambert's framing that "closed models will stay slightly
  smarter, open models will be cheaper."
- **No political censorship.** The community notes M3 appears to **lack the
  political censorship typical of Chinese LLMs** — a differentiator versus prior
  Chinese open-weights releases and a factor in Western adoption.
- **Long context.** The 1M-token window puts it in the same long-context tier as
  the frontier closed models, relevant for repo-scale agentic refactors.
- **MiniMax Sparse Attention (MSA) — the engine under the 1M window
  (2026-06-04).** MiniMax detailed a new attention architecture, **MSA**, that
  scales natively to 1M tokens: claimed **4× faster than Flash-Sparse-Attention**,
  with a **9× prefill / 15× decode speedup** and **~1/20th the compute at full
  1M context**. MSA is the mechanism that makes M3's long-context tier
  economically viable rather than just nominally supported — the architectural
  story behind the headline window (ARA digest 2026-06-04).

This release sits inside the broader open-weights wave — alongside Google's
[[gemma-4]] and [[deepseek]]'s family — that pressures the
frontier labs' pricing, and feeds the [[ai-capex]] inference-demand story:
cheaper capable open models expand the addressable inference base routed through
layers like [[openrouter]].

## Open questions

- **Does the SWE-Bench Pro number replicate?** As with [[microsoft|MAI-Thinking-1]],
  the headline benchmark needs independent confirmation.
- **Deployment economics.** Open weights at this capability shift the
  build-vs-buy line for enterprises; how much agentic-coding volume migrates off
  closed APIs to self-hosted M3?
