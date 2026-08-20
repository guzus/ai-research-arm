---
slug: qwen-3-8-max
title: Qwen3.8-Max
type: entity
aliases: ["Qwen3.8-Max", "Qwen3.8", "Qwen 3.8 Max", "Qwen3.8 Max", "Qwen3.8-2.4T-A95B"]
tags: [open-weights, model, moe, chinese-llm, long-context, alibaba]
description: Alibaba's 2.4T-parameter / 95B-active MoE flagship, launched 2026-08-04 at $2/$6 per Mtok and open-weighted as Qwen3.8-2.4T-A95B on 2026-08-13 — the first Max-class Qwen ever released open — alongside the contested 27B sibling (Qwen3.8-27B).
created_at: 2026-08-04
timestamp: 2026-08-20T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-08-20", path: research/digest/2026-08-20-digest.md}
  - {title: "ARA daily digest 2026-08-19", path: research/digest/2026-08-19-digest.md}
  - {title: "ARA daily digest 2026-08-18", path: research/digest/2026-08-18-digest.md}
  - {title: "ARA daily digest 2026-08-13", path: research/digest/2026-08-13-digest.md}
  - {title: "ARA daily digest 2026-08-09", path: research/digest/2026-08-09-digest.md}
  - {title: "AINews: Zawinski's Law of MultiAgents (Latent Space)", url: "https://www.latent.space/p/ainews-zawinskis-law-of-multiagents", date: 2026-08-08}
  - {title: "ARA daily digest 2026-08-04", path: research/digest/2026-08-04-digest.md}
  - {title: "ARA daily digest 2026-07-21", path: research/digest/2026-07-21-digest.md}
  - {title: "ARA daily digest 2026-07-20", path: research/digest/2026-07-20-digest.md}
---

**Qwen3.8-Max** is [[alibaba]]'s flagship text model: a **2.4 trillion-parameter
/ 95 billion-active mixture-of-experts** with a **1M-token context**, launched
2026-08-04 at **$2 per million input / $6 per million output** tokens. The
open-weight release landed on **2026-08-13 as `Qwen3.8-2.4T-A95B`** — the
**first Max-class Qwen ever released open** — with **95B active parameters
across 512 experts** and **4.89TB of weights** (ARA digest 2026-08-13).

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
- **The open-weights release gets a named platform and a date (2026-08-07/08).**
  Alibaba staged a **ModelScope page** for `Qwen3.8-2.4T-A95B`, described as the
  **first open-weight Qwen-Max-class model**, with release indicated for the
  **following Wednesday** and `Qwen3.8-27B` to follow on separate pages. The
  staging confirms the 2.4T-parameter / A95B≈95B-active read and hardens the
  launch-day "open weights next week" commitment into a concrete artifact
  target — though as of this ingest the weights remain unpublished
  (r/LocalLLaMA via Latent.Space AINews; ARA daily digest 2026-08-09).
- **The open weights actually ship — `Qwen3.8-2.4T-A95B` lands (2026-08-13).**
  Alibaba open-weighted the 2.4T/95B-active model: **4.89TB of weights, 512
  experts**, **day-0 vLLM support**, and **pre-quantized 4-bit checkpoints
  sized to a single 8×B300 or 8×MI355X node**. vLLM published
  `Inferact/Qwen3.8-2.4T-A95B-NVFP4` at **1.32 TiB** and an **MXFP4 build at
  1.45 TiB**; Unsloth published a **dynamic 1-bit build at 397GB** that still
  needs 410GB+ of RAM or VRAM. **No quality measurement against the
  quantizations was published.** The model card confirms it is the **base of
  Alibaba's own commercial flagship**, with **vision, the 1M default context
  and built-in tools withheld as the paid layer** — the open release is the
  text-and-1M-context base, not the ranked commercial system. The **27B
  sibling** (`Qwen3.8-27B`), "the size most people can actually run," is due
  **Friday 14 August**. HN threads on the release converged on **MoE
  active-parameter economics** — how ~95B-active models price against frontier
  rivals (ARA digest 2026-08-13).

- **The 27B sibling gets a canonical serving path and a strong open-model
  WeirdML score (2026-08-18).** `Qwen3.8-27B` now has a reproducible serve
  path: llama.cpp's Georgi Gerganov showed `llama serve -hf
  ggml-org/Qwen3.8-27B-GGUF --spec-type draft-mtp`, pairing an official
  ggml-org conversion with **speculative decoding through the model's own
  multi-token-prediction head**, so **no separate draft model is needed** —
  the first shared artifact a week of contradictory hands-on results can be
  pinned to (though it does not pin quantization, reasoning budget, or token
  accounting). On **WeirdML**, the **2.4T A95B scored 75.2% at extra-high
  reasoning — second-best open model behind Kimi-K3** — with the caveat that
  it uses a lot of reasoning tokens and writes very long code. Separately, a
  claim that **Qwen3.8-27B reached DeepSeek V4-Pro level on the Artificial
  Analysis index remains unsettled** (HN discussed a score of 52; the only
  Twitter mention was a bare integer with no screenshot, index version or
  quantization). Read against the 27B open-question below — the size most
  people can actually run now has a single canonical command and a credible
  open-model score, while the "matches V4-Pro" claim stays unverified (ARA
  daily digest 2026-08-18).

- **The 27B sibling is the week's most contested model (2026-08-19).** Simon
  Willison reports **52 on the Artificial Analysis Intelligence Index — level
  with [[gpt-5-6|GPT-5.6 Luna]] (max) and one point behind far larger models** —
  calling it "the most fun he's had with a local model," in the day's
  most-engaged Bluesky post (210 likes). A separate screenshot claim puts it at
  **51 on the Agentic Index, above [[zhipu-glm-5-2|GLM-5.2]] and DeepSeek V4
  Pro**, unconfirmed by the benchmark publisher. Against that, a **reproducible
  hands-on test** had it **think 40,000 tokens for ~an hour on a 2D
  fluid-simulation prompt** and return a **non-working page, where Opus 4.5
  one-shot it in ~a minute** (prompt published). **Unsloth's GGUF passed 2.7M
  downloads and sat #2 trending on Hugging Face** — the raw adoption signal
  behind the contested benchmarks (ARA daily digest 2026-08-19).
- **The 27B consolidates as the cycle's dominant open-weights release
  (2026-08-20).** The digest's model-releases rank names `Qwen3.8-27B` the
  cycle's dominant open-weights story: **#2 trending on Hugging Face (~2.7M
  downloads), ~51 on the AA Agentic Index, running on a single consumer GPU**.
  **Unsloth's Dynamic V3 GGUFs** claim **10% higher accuracy**, including
  **1-bit quants retaining 77% accuracy in 8GB of RAM**; **Ethan Mollick
  publicly disputes benchmark placements that put it alongside frontier
  models** — keeping the index-versus-hands-on split from 2026-08-19 live
  (ARA daily digest 2026-08-20).

## Open questions

- **Do the open weights match the commercial model's behavior?** With vision,
  the 1M default context and built-in tools withheld as the paid layer, the
  ranked system and the downloadable base differ in components — the
  component-withholding pattern this wiki tracks on [[open-weights]].
- **Do the vendor wins replicate against the excluded models?** No independent
  head-to-head against Kimi K3 or Opus 5 exists yet.
- **Is the 27B sibling the artifact most people actually run?** A 2.4T MoE is
  out of reach for local inference; `Qwen3.8-27B` (due 2026-08-14) may carry
  the real adoption, and no quality measurement against the quantizations has
  been published.
