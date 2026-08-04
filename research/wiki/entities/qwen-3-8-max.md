---
slug: qwen-3-8-max
title: Qwen3.8-Max
type: entity
aliases: ["Qwen3.8-Max", "Qwen3.8", "Qwen 3.8 Max", "Qwen3.8 Max"]
tags: [open-weights, model, moe, chinese-llm, long-context, alibaba]
description: Alibaba's 2.4T-parameter / 95B-active MoE flagship, launched 2026-08-04 at $2/$6 per Mtok with open weights promised the following week — which would be the first Max-class Qwen ever released open.
created_at: 2026-08-04
timestamp: 2026-08-04T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-08-04", path: research/digest/2026-08-04-digest.md}
  - {title: "ARA daily digest 2026-07-21", path: research/digest/2026-07-21-digest.md}
  - {title: "ARA daily digest 2026-07-20", path: research/digest/2026-07-20-digest.md}
---

**Qwen3.8-Max** is [[alibaba]]'s flagship text model: a **2.4 trillion-parameter
/ 95 billion-active mixture-of-experts** with a **1M-token context**, launched
2026-08-04 at **$2 per million input / $6 per million output** tokens. Alibaba
says Max plus a **27B sibling** reach Hugging Face **next week** — which would
make it the **first Max-class Qwen ever released open-weight**. As of this
ingest the weights are still unpublished, so the load-bearing claim of the
launch is a promise, not an artifact (ARA digest 2026-08-04).

It is the shipped form of the model tracked since 2026-07-20 on the
[[alibaba]] page as "going open-weight soon," and previewed 2026-07-21 with a
self-reported #2 overall rank behind [[claude-fable-5|Claude Fable 5]].

## Why it matters

- **Price is the sharp end of the claim.** $2/$6 per Mtok against Fable 5's
  $10/$50 is roughly a **5×/8× discount** at the input/output ends. If the
  capability claim survives contact with independent evals, the pricing — not
  the benchmark table — is what moves inference volume. See [[open-weights]].
- **The benchmark table is Alibaba's own, and its exclusions are the tell.**
  Vendor numbers claim wins on **51 of 54** comparable tests against
  [[claude-opus-4-8|Opus 4.8]] and **46/54** against [[gpt-5-6|GPT-5.6-Sol]],
  but fall to **37/49** against [[claude-fable-5|Fable 5]] and **omit
  [[moonshot-kimi-k3|Kimi K3]] and [[claude-opus-5|Opus 5]] entirely** — the
  two models a "beats the frontier" framing would most need to include.
- **First independent touches were more muted than the launch pitch.**
  @emollick's shader test landed on "solid, but not Kimi K3 level," and
  @teortaxesTex found agentic benchmarks (NL2Repo, DeepSWE, Agent's Last Exam)
  landing close to the far smaller [[deepseek-v4-flash|DeepSeek V4-Flash]] —
  a much cheaper model, which is the comparison that matters commercially.
- **The 16-day autonomous-coding figure is unaudited and already drifting.**
  The pitch shifted to a claimed **16-day unattended run producing 265 commits,
  127 PRs and 151 issues**, a figure that appeared as **"10+ days"** in a second
  retelling of the same material. No log or harness has been released, and
  commit/PR counts are output volume, not accepted work.
- **It owned Hacker News, then saturated.** It led the AI slice in **five
  consecutive windows**, climbing 115 → 464 → 653 → 861 → 960 points, with
  per-cycle gains decaying monotonically before it aged off the front page.

## Open questions

- **Do the weights actually ship, and under what license?** "Next week" (from
  2026-08-04) is the commitment. A Max-class open release would be a genuine
  first; a slip or a restrictive license would make this a normal API launch.
- **Do the vendor wins replicate against the excluded models?** No independent
  head-to-head against Kimi K3 or Opus 5 exists yet.
- **Is the 27B sibling the artifact most people actually run?** A 2.4T MoE is
  out of reach for local inference; the small model may carry the real adoption.
