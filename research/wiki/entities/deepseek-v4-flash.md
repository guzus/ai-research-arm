---
slug: deepseek-v4-flash
title: DeepSeek V4-Flash-0731
type: entity
aliases: ["V4-Flash", "V4-Flash-0731", "DeepSeek-V4-Flash", "DeepSeek V4-Flash-0731"]
tags: [frontier-model, open-weights, chinese-llm, moe, agentic-coding, mit-license]
description: DeepSeek's 284B-total / 13B-active MoE model with 1M context — API public beta at $0.28/$0.87 per Mtok on 2026-07-31, MIT-licensed weights hours later, scoring 50 on Artificial Analysis and relayed as undercutting Claude Fable 5 by 105× on cost per task.
created_at: 2026-08-01
timestamp: 2026-08-22T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-08-22", path: research/digest/2026-08-22-digest.md}
  - {title: "ARA daily digest 2026-08-13", path: research/digest/2026-08-13-digest.md}
  - {title: "ARA daily digest 2026-08-09", path: research/digest/2026-08-09-digest.md}
  - {title: "AINews: Zawinski's Law of MultiAgents (Latent Space)", url: "https://www.latent.space/p/ainews-zawinskis-law-of-multiagents", date: 2026-08-08}
  - {title: "ARA daily digest 2026-08-04", path: research/digest/2026-08-04-digest.md}
  - {title: "ARA daily digest 2026-08-03", path: research/digest/2026-08-03-digest.md}
  - {title: "ARA daily digest 2026-08-02", path: research/digest/2026-08-02-digest.md}
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

## Day-two outside evidence (2026-08-02)

- **The 105× cost-per-task claim.** Cline relayed an **Artificial Analysis
  cost-per-task comparison putting V4-Flash 105× cheaper than
  [[claude-fable-5|Anthropic's Fable 5]]** on the same workload — a far larger
  spread than the ~60% figure from launch day, because it measures **cost per
  completed task**, not per token. Relayed via @cline / @AravSrinivas, not
  published by Anthropic or DeepSeek.
- **It kept clearing independent tests.** **50 on the Artificial Analysis
  Intelligence Index at $0.14/$0.27 per Mtok**; **LMArena Pareto-frontier
  placement** in the Frontend Code Arena; **first place on Lech Mazur's
  940-puzzle Extended NYT Connections benchmark (89.6 vs
  [[gemini-3-6-flash|Gemini 3.6 Flash]] 89.0)**; and **parity with
  [[gpt-5-6|GPT-5.6 Sol]] and [[moonshot-kimi-k3|Kimi K3]]** in Aikido
  Security's pentest evaluation.
- **The caveat that travelled with every result: reasoning effort.** The strong
  numbers depend on running at **high** effort. Simon Willison got *"a
  disappointing pelican"* at default mode — meaning the headline
  price/performance and the default-mode experience are **not the same
  product**, and cost comparisons that assume high effort understate real spend.
- **A published quirk in its own inference path.** *Numerical State in Sparse
  MoE Inference* ([arXiv:2607.28097](https://arxiv.org/abs/2607.28097)) shows
  **mathematically equivalent expert aggregations produce divergent
  continuations in DeepSeek-V4-Flash** — a reproducibility hazard for anyone
  benchmarking it across serving stacks, and an instance of the
  [[verification-bottleneck]].
- **Open discrepancy to resolve.** Launch-day sourcing described the model as
  **284B total / 13B active**; the 2026-08-02 digest describes the open-weights
  release as **304B (MIT, 167GB)**. Both figures are carried here as digested;
  neither has been reconciled against the technical report in-window.

## Day-three: the 304B figure firms, and the reception splits (2026-08-03)

- **The open-source release is described as 304B with GGUF quantization for
  local deployment**, restating the higher of the two parameter counts this page
  carries. The **284B-vs-304B discrepancy is still unreconciled** against the
  technical report; both remain digested-as-relayed.
- **The same tracker praised and panned it in one cycle.** A skeptical tester
  called V4-Flash *"14 times cheaper, 50% faster and vastly better than
  V4-Pro"* while also finding it *"mostly burns tokens on nonsense"* and losing
  to Luna on **time-to-completion**. That is not incoherence — it is what a
  cheap-but-verbose model looks like when you price by token versus by finished
  task, and it sits directly on top of the high-reasoning-effort caveat above.
- **Correction: there was no "preview subsidy."** A same-day correction
  establishes that **SiliconFlow's prices are distinct from DeepSeek's own** and
  are **worse on cached input** — so the earlier read that launch pricing was a
  temporary promotional rate does not hold. Third-party host pricing must not be
  attributed to [[deepseek]].
- **Serving economics move off NVIDIA on the neighbouring model.** A wafer.ai
  writeup claims **AMD MI355X beats [[nvidia|NVIDIA]] B300 on
  performance-per-dollar** for [[moonshot-kimi-k3|Kimi K3]] inference — an
  open-weight *serving-cost* argument rather than a capability one, which is the
  axis V4-Flash competes on. It drew 92 HN comments and aged off unresolved,
  with the one venue that actually benchmarks open-weight inference on owned
  hardware (r/LocalLLaMA) offline for the entire argument. See [[ai-capex]].

## Day-four: the parameter question resolves, agentic gains isolate (2026-08-04)

- **No parameter change — it is a re-post-train.** The 2026-08-04 digest states
  the model is **284B/13B, re-post-trained**, with the gains coming from
  post-training rather than a new base. That is the first statement that
  reconciles the 284B-vs-304B split above in favour of 284B, and it reframes
  the whole release: what shipped is a training-recipe result, not a scale one.
- **Independent scoring firmed up, and it is higher than day one.** Artificial
  Analysis now puts it at **50 on the intelligence index — up 10 points, and
  six above DeepSeek's own larger V4 Pro**. WeirdML scored it **57.1% / 63.0%
  at high / max effort** — again the high-reasoning-effort caveat is doing
  work. A cheap fast-tier model beating the lab's own larger flagship is the
  uncomfortable result for tiered pricing generally.
- **The gains concentrate in agentic work.** **GDPval-AA v2 moved 1189 → 1559
  Elo** and **Terminal-Bench 2.1 rose 17 points to 79%**. Note 79% is *below*
  the vendor-cited 82.7 this page already flags as unreproduced — the
  independent number landing under the vendor number is the ordinary outcome,
  and worth recording as such.
- **API-beta surface is broader than a chat endpoint.** The beta opened with
  1M context, **tool calling, built-in web search and OpenAI Responses API
  support** — packaged for agent frameworks, not for chat.
- **A second price pair is now in circulation: $0.14/$0.28 per Mtok**, against
  the $0.28/$0.87 recorded at launch on this page. Both are digested-as-relayed
  and **unreconciled**; given the same-day SiliconFlow correction above, do not
  assume either figure is DeepSeek's own list price without a primary source.
- **Fourteen community quants shipped by end of day**, the smallest usable one
  aimed at **128GB machines** — the practical local-inference ceiling for this
  model. See [[open-weights]].
- **Adoption momentum (2026-08-07/08).** **Cline** reported V4-Flash became its
  **#1 most-used model**, with **+40% usage and 3× token growth** after the
  0731 update, while **Ollama** rolled out deployment support — the
  cost-per-task adoption story this page has tracked since day two showing up
  as served-volume share in agent tooling (Latent.Space AINews; ARA daily
  digest 2026-08-09).
- **The Pro sibling prices itself 4.5× higher — and Flash wins a friendly
  head-to-head (2026-08-13).** [[deepseek]] listed **`DeepSeek-V4-Pro-0813`**
  at **$0.435/$0.87 per Mtok** at 1M context — roughly **4.5× V4-Flash's
  $0.28/$0.87 input price**. Within two hours, pro-DeepSeek analyst
  @teortaxesTex reported the **cheaper V4-Flash 0731 outperforming the new
  Pro on his own tasks**, calling the release evidence that "they need more
  than scale" — the strongest public instance yet of this model beating its
  lab's own larger flagship, the "cheap fast-tier model beating the flagship"
  pattern flagged on day four (ARA digest 2026-08-13).

## V4-Flash-Vision-Exp — DeepSeek's first image-capable model (2026-08-22)

[[deepseek|DeepSeek]] shipped **`V4-Flash-Vision-Exp`**, its **first image-capable
model**, live on its API with **mixed text-plus-image input** across Chat
Completions, Messages and Responses — at **V4-Flash token prices** (reported **CNY
3/9 per million input/output at peak, halved off-peak**), with **images billed at
117–384 tokens each**, an **unchanged 2,500 request concurrency**, and a **free
Files API for image reuse**. Three qualifications matter for how this reads. First,
**the vendor's own wording is performance "close to Opus 4.8"** — amplifiers
escalated that to "outperforms" within the hour, and **no independent benchmark run
exists**. Second, **nothing has been said about open weights** — the load-bearing
omission for this lab, whose MIT release of the base V4-Flash was what made it a
frontier event. Third, the **"exp" suffix historically marks a pipeline validation
rather than a flagship** on DeepSeek's release ladder. It was the day's top Hacker
News AI thread (414 points, 136 comments), weighing pricing and capability against
the family's cost-performance reputation (The Decoder, DeepSeek API announcement,
@teortaxesTex hands-on; ARA daily digest 2026-08-22).

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
  competing open models are multimodal — **partially answered on 2026-08-22 by
  V4-Flash-Vision-Exp**, DeepSeek's first image-capable model, but the "exp"
  experimental suffix and its silent open-weights posture keep the question open
  for the GA line.
