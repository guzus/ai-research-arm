---
slug: moonshot-kimi-k2-7-code
title: Moonshot Kimi K2.7 Code
type: entity
aliases: ["Kimi K2.7 Code", "Kimi K2.7-Code", "Moonshot Kimi K2.7 Code", "Moonshot AI Kimi K2.7 Code"]
tags: [open-weights, china, coding, inference-pricing, local-llm]
description: Moonshot AI's open coding model that undercuts GPT-5.5 and Claude by up to roughly 12x on price per token while staying competitive; one of the Chinese open-weight releases filling the Fable 5 vacuum.
created_at: 2026-06-17
timestamp: 2026-07-03T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-07-03", path: research/digest/2026-07-03-digest.md}
  - {title: "ARA model ticket — Moonshot Kimi K2.7 Code", path: research/models/tickets/moonshot-kimi-k2-7-code.md}
  - {title: "ARA daily digest 2026-06-15", path: research/digest/2026-06-15-digest.md}
  - {title: "ARA daily digest 2026-06-14", path: research/digest/2026-06-14-digest.md}
---

Moonshot Kimi K2.7 Code is a Chinese open coding model that became one of the
week's main examples of open weights turning capability pressure into price
pressure. Per the ARA model ticket, The Decoder reported the model undercuts
GPT-5.5 and Claude by up to roughly **12x on price per token** while staying
competitive on performance, and community GGUF quantizations were already
rolling onto Hugging Face in-window.

## Why it matters

- **The price story in the open-weights wave.** [[zhipu-glm-5-2]] is the
  long-context flagship story; Kimi K2.7 Code is the price story. Together
  with [[minimax-m3]] and [[deepseek]], it makes the [[open-weights]] thesis
  concrete: local or self-hosted models are no longer just sovereignty
  insurance, they can also be much cheaper per useful coding token than the
  closed frontier APIs.
- **It landed into the Fable 5 vacuum.** On 2026-06-15, with
  [[claude-fable-5|Fable 5 / Mythos 5]] still dark, Chinese open-weight
  flagships filled the discourse. Kimi K2.7-Code reportedly landed **#2 on
  ErdosBench** behind Fable 5 max, with higher Kimi Code Bench / Program Bench /
  MLS Bench Lite scores than K2.6 and about **30% fewer reasoning tokens**
  (treat the placements as preliminary/vendor-adjacent).
- **It pressures router and frontier economics.** Models like Kimi are exactly
  the long-tail supply that makes [[openrouter]] useful: if price/performance
  keeps moving, application developers need a routing layer or benchmark habit
  rather than a single-vendor default. It also pushes [[openai]] and
  [[anthropic]] toward price cuts or specialist packaging.

- **GA inside GitHub Copilot — mainstream IDE distribution (2026-07-03).** Kimi
  K2.7 Code is now **generally available inside GitHub Copilot** — the top
  Hacker News story of the day (342 points) — read as a signal that non-US open
  models are winning **first-class mainstream IDE distribution**, not just
  self-hosted/OpenRouter usage. It landed alongside heavy HN discussion of new
  agent-evaluation benchmarks (**Senior SWE-Bench**, **CursorBench 3.1**)
  questioning what current coding-agent benchmarks miss — sharpening the
  question of whether Kimi's price/performance edge (see "Why it matters"
  above) holds up under the same neutral-eval scrutiny (ARA digest 2026-07-03).

## Open questions

- **Primary-source gap.** The ticket remains `verification: partial` because no
  primary Moonshot model card was captured in-window. A primary repo, model
  card, or benchmark suite would harden the release record.
- **Benchmark durability.** Does Kimi's coding performance survive neutral,
  contamination-aware evaluation, or is the main durable advantage the price
  curve?
- **Local-run practicality.** GGUF quantizations make the model accessible, but
  useful local coding depends on latency, context length, tool calling, and
  editor integration, not just weights being public.

## Changelog

- [2026-06-17] created | low-price open coding model filling the Fable 5 vacuum
- [2026-07-03] updated | GitHub Copilot GA, top HN story of the day
