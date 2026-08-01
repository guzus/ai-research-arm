---
slug: deepseek-v4-flash
title: DeepSeek V4-Flash-0731
type: entity
aliases: ["V4-Flash", "V4-Flash-0731", "DeepSeek-V4-Flash", "DeepSeek V4-Flash-0731"]
tags: [frontier-model, open-weights, chinese-llm, moe, agentic-coding, mit-license]
description: DeepSeek's 284B-total / 13B-active MoE model with 1M context — API public beta at $0.28/$0.87 per Mtok on 2026-07-31, MIT-licensed weights hours later, scoring 50 on Artificial Analysis at ~60% lower cost per task than GPT-5.6 Luna.
created_at: 2026-08-01
timestamp: 2026-08-01T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-08-01", path: research/digest/2026-08-01-digest.md}
  - {title: "ARA model ticket — DeepSeek V4 GA + surge pricing", path: research/models/tickets/deepseek-v4-ga-surge-pricing-2026-06.md}
---

**DeepSeek V4-Flash-0731** is [[deepseek|DeepSeek's]] fast-tier flagship: a
**284B-total / 13B-active-parameter MoE** (6-of-256 experts) with **1M
context**, shipped to public-beta API on **2026-07-31** at **$0.28 input /
$0.87 output per million tokens** and open-sourced under the **MIT license**
on Hugging Face hours later, with a technical report.

## Why it matters

- **Near-frontier capability at a discount-tier price.** Artificial Analysis
  scored it **50 on its intelligence index — one point behind
  [[gpt-5-6|GPT-5.6 Luna]] — at roughly 60% lower cost per task**. That
  price/intelligence breakdown was the counterweight readers paired with the
  vendor changelog on Hacker News (493 points, 271 comments), while the
  release itself held the **#1 AI slot across three consecutive front-page
  snapshots (453 → 562 → 652 points)**.
- **Post-training, not scale, did the work.** Same architecture and same
  active-parameter count as the preview, with a **~10-point index gain
  attributed to post-training alone** — a direct data point on how much
  headroom remains after pre-training in the current open-weights cycle.
- **Vendor benchmarks vs. independent reads.** DeepSeek cites **Terminal-Bench
  2.1 82.7, DeepSWE 54.4, Cybergym 76.7**. Outside evidence is genuinely
  mixed: one external security harness put it level with Grok 4.5 at ~10x
  lower cost, while skeptical testers flag weakness on CritPt and
  hallucination-heavy evals. The model **still has no vision** — that is
  slated for 4.1.
- **The open-weights flywheel closes fast.** Unsloth published **lossless
  4-bit quantizations running on 168 GB RAM (3-bit on 110 GB) within about
  five hours** of the weight drop — the local-inference ecosystem now
  productionises a frontier-adjacent open release the same day. See
  [[open-weights]].
- **Rate card resolved, surge pricing not evidenced.** The June GA
  announcement paired the release with the first major LLM **time-of-day
  surge pricing** (peak ~2× off-peak). The launch as digested carries the flat
  $0.28/$0.87 pair and no evidence the peak/off-peak scheme went live; treat
  surge pricing as announced-but-unconfirmed for this model.

## Context

The release lands days after [[moonshot-kimi-k3|Kimi K3]] open-sourced 2.8T
parameters and alongside [[thinking-machines|Thinking Machines']]
Inkling-Small — three open-weight drops inside one week, against Western
frontier weights that remain closed or export-gated
([[claude-fable-5]], [[federal-ai-policy]]). It is also the cheap-inference
demand-side mirror of the [[ai-capex]] buildout: capability is arriving at
prices that assume enormous served volume.

## Open questions

- **Does the MIT license hold for successors?** V4-Flash is DeepSeek's first
  post-commercialization open release ([[deepseek]] took outside capital in
  June); whether the next tier stays MIT is the test of that posture.
- **Do the vendor benchmarks reproduce?** Terminal-Bench 2.1 82.7 and Cybergym
  76.7 are vendor-cited; independent reproduction has not landed.
- **When does vision ship?** Deferred to 4.1, leaving V4-Flash text-only while
  competing open models are multimodal.
