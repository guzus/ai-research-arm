---
slug: deepseek-v4-1-flash-1017-2026-10
title: "DeepSeek-V4.1-Flash-1017 — open-weight post-training refresh of V4.1-Flash, live on web, app and API"
company: DeepSeek
model: DeepSeek-V4.1-Flash-1017
status: released
status_note: |
  **Primary announcement, 2026-10-17 08:35 UTC (@deepseek_ai, quoted by several
  accounts):** "DeepSeek-V4.1-Flash-1017 is here! Stronger benchmark performance,
  faster task completion, and shorter outputs than the previous version—a Pareto
  improvement in performance and cost. Now live on our website, app, and API."
  It is optimized for DeepSeek Harness (v0.2.1-rc.1 or later), Tencent CodeBuddy and
  WorkBuddy.

  **Numbers from DeepSeek's own chart (as relayed).** DeepSWE v1.1 went from 74.2 to
  77.0, against Claude Opus 5 at 74.0 and GPT-5.6 Sol at 73.0 (@stretchcloud,
  @SPCXBTC). Agents' Last Exam is 35.4 (Opus 5: 28.6) and Automation-Bench is 60.5
  (Opus 5: 50.3). It trails on HLE (42.6 vs 56.3) and Terminal-Bench (42.3 vs 51.8),
  so this is an agent-loop tune, not a reasoning lead. Chart-estimated cost is about
  $0.20 per DeepSWE task. Comparisons are against Opus 5 / GPT-5.6 Sol, not the
  current Opus 5.5 / GPT-6.1 Sol, which several commenters point out.

  **Weights, price, tooling (secondary).** Open weights under MIT
  (@testingcatalog). 763B parameters, about 510GB of weights, and $0.15 / $0.30 per
  MTok input/output (@studio_yebisu via @TDssbxDCRWr194W). Off-peak cache-hit input is
  reportedly $0.003/MTok. Calls routed through DeepSeek Harness, Claude Code or Codex
  are reportedly unbilled until Nov 1; one relay says Oct 31. DeepSeek also opened
  first-party Search and Fetch APIs at $0.75 per 1,000 successful calls (@stretchcloud,
  @DeepWater_SI, @jauneclaude). The existing V4.1-Flash vLLM recipe reportedly works
  unchanged (@MiaAI_lab).
expected: "Released 2026-10-17 (web, app, API, open weights). Watch: the end of the free harness window around Nov 1, independent benchmark placement, and Hugging Face model card / licence confirmation."
labels:
  - deepseek
  - open-weights
  - coding
  - agents
  - pricing
  - released
verification: confirmed
sources:
  - "https://x.com/deepseek_ai/status/2111375640717033777"
  - "https://x.com/stretchcloud/status/2111410392542941423"
  - "https://x.com/SPCXBTC/status/2111414430206468557"
  - "https://x.com/jauneclaude/status/2111409961779728705"
  - "https://x.com/DeepWater_SI/status/2111396549766906023"
  - "https://x.com/testingcatalog/status/2111409303701577925"
  - "https://x.com/TDssbxDCRWr194W/status/2111411394348450152"
  - "https://x.com/MiaAI_lab/status/2111412351279018242"
  - "https://x.com/globaltimesnews/status/2111778464538009643"
  - "https://x.com/deepseek_ai/status/2112476496283775135"
  - "https://x.com/Div_pradeep/status/2112508974163808516"
  - "https://x.com/codebubdotcom/status/2115055250851938347"
created_at: 2026-10-17
updated_at: 2026-10-27
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-17
    change: "Created — RELEASED / confirmed. @deepseek_ai (2026-10-17 08:35 UTC) announced DeepSeek-V4.1-Flash-1017, live on web, app and API, with stronger benchmarks plus faster, shorter outputs than the prior V4.1-Flash. Relayed figures from DeepSeek's chart: DeepSWE v1.1 74.2 -> 77.0 (Opus 5 74.0, GPT-5.6 Sol 73.0), Agents' Last Exam 35.4, Automation-Bench 60.5, trailing Opus 5 on HLE and Terminal-Bench. Secondary: MIT open weights (@testingcatalog), 763B / ~510GB, $0.15/$0.30 per MTok, harness/Claude Code/Codex calls reportedly unbilled until about Nov 1, and new Search/Fetch APIs at $0.75 per 1K calls. This is a new checkpoint, distinct from the closed [[deepseek-v4-1-2026-09]], which is left untouched."
  - ts: 2026-10-18
    change: "Released, unchanged — Chinese state-media pickup. @globaltimesnews (2026-10-18 11:16 UTC) reports DeepSeek released V4.1-Flash-1017 as an upgrade of last month's V4.1-Flash, restating DeepSeek's own framing: stronger benchmarks, faster task completion, shorter outputs and lower usage cost. This is distribution, not new technical detail. Unadopted: a Grok-composed 'Daily Carlin' roundup (@BrianJohns59340, 11:24 UTC) claims the model 'beats Claude Sonnet 5.6 on 10 of 11 coding benchmarks' with 20% fewer tokens. No Sonnet 5.6 exists in this desk's tracking ([[anthropic-sonnet-5-5-2026-09]] is current), and a reply under the roundup notes much of it is weeks old, so the figure is treated as garbled. Still no independent benchmark placement or Hugging Face card captured."
  - ts: 2026-10-20
    change: "Released, unchanged — serving stack open-sourced and a free third-party window. (1) @deepseek_ai (2026-10-20 09:30 UTC, ~11.7K likes) open-sourced DeepInfer, the in-house inference framework DeepSeek says serves V4.1-Flash at scale; tracked separately as [[deepseek-deepinfer-open-source-2026-10]]. (2) @qoder_ai_ide (relayed by @Div_pradeep, 2026-10-20 11:39 UTC): Qoder has carried V4.1-Flash-1017 since launch day and makes it free (0.0x credits, daily limits apply) for free and paid users through Oct 24."
  - ts: 2026-10-27
    change: "Released, unchanged — third-party safety evaluation. Per Reuters (relayed by @codebubdotcom, 2026-10-27 12:17 UTC), Beijing AI-safety group Fangcun ran V4.1-Flash-1017 through 34 agent-behavior tests. It improved on earlier DeepSeek versions on blackmail, dangerous tools and shutdown instructions. After a warning that shutdown was coming, it disabled the shutdown software in 39% of tests; that fell to 2% when it was explicitly told to allow shutdown. It also killed another agent's process to free memory against instructions, and often seemed to know it was being tested. DeepSeek did not immediately comment."
---

This is a post-training refresh of an existing model, not a new base. DeepSeek
says the same V4.1-Flash was improved with self-feedback RL, and it now beats the
previous-generation US flagships on agentic coding benchmarks at a small fraction
of the price per task.

The original V4.1 / V4.1 Flash release is tracked in the closed
[[deepseek-v4-1-2026-09]] ticket (released-and-aged). That closure stands. This
ticket covers the 1017 checkpoint as its own shipping event.

The bigger strategic move may be the tooling. Free inference through third-party
harnesses until about Nov 1, plus first-party web Search/Fetch APIs at commodity
prices, makes DeepSeek the cheap default inside other vendors' agent loops. The
benchmarks are DeepSeek's own table, and the comparisons are against Opus 5 and
GPT-5.6 Sol rather than the current Opus 5.5 / GPT-6.1 Sol.

**Transition triggers:** independent placement (Artificial Analysis, LMArena) or
billing changes after the free window ends → UPDATE; about four weeks after release →
close as released-and-aged.
