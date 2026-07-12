---
slug: tencent-hunyuan-hy3
title: Tencent Hunyuan Hy3
type: entity
aliases: ["Hunyuan Hy3", "Hy3", "Tencent Hy3"]
tags: [open-weight, china, tencent, model-release]
description: Tencent Hunyuan's 295B-parameter open-weight MoE model under Apache 2.0, reported new open SOTA on the MCP-Atlas benchmark, released 2026-07-06.
created_at: 2026-07-12
timestamp: 2026-07-12T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-07-12", path: research/digest/2026-07-12-digest.md}
  - {title: "ARA model ticket — Tencent Hunyuan Hy3", path: research/models/tickets/tencent-hunyuan-hy3-2026-07.md}
---

**Hy3** is Tencent Hunyuan's **295-billion-parameter Mixture-of-Experts**
open-weight model, licensed under **Apache 2.0** with a commercially-usable
API, released 2026-07-06. Independent reporting places it as the new
open-weights SOTA on the **MCP-Atlas** benchmark — surpassing
[[zhipu-glm-5-2]] — and separately claims it beats GPT-5.5 on a science
benchmark using a much smaller compute setup.

## Why it matters

Hy3 is the latest entrant in the accelerating **China open-weight**
release cadence alongside [[zhipu-glm-5-2]], [[minimax-m3]], and
[[deepseek]]'s frontier ambitions — part of the broader [[open-weights]]
theme of open models closing on the frontier. It shipped the same digest
cycle as [[mistral-robostral-navigate]], another open-weight release,
underscoring how competitive open releases now land on the same day
across multiple labs.

Three independent secondary accounts (an ML researcher, a news aggregator,
and a Japanese-language outlet) agree on the specific parameter count,
license, and benchmark claims, but no official Tencent Hunyuan primary
source was captured — `verification: partial`.

## Open questions

- **Official confirmation.** Does a Tencent Hunyuan primary source (blog,
  model card, or official account) corroborate the specifics?
- **Benchmark durability.** Does the MCP-Atlas SOTA and the reported
  GPT-5.5-beating science result hold up under independent, contamination-
  aware evaluation?
