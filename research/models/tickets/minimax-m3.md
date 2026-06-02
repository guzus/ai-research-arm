---
slug: minimax-m3
title: MiniMax M3 — open-weights frontier coding + agentic + 1M-context launch
company: MiniMax
model: MiniMax M3
status: released
status_note: |
  MiniMax officially launched M3 at 2026-06-01 01:59 UTC (primary
  @MiniMax_AI, ~2,965 likes / 430 RT on the announcement tweet) as
  "the first open-weights model to combine three frontier capabilities":
  coding + agentic, 1M-token context via the new MiniMax Sparse Attention
  mechanism, and natively multimodal "from step zero". Self-reported
  headline benchmarks: 59.0% SWE-Bench Pro, 66.0% Terminal Bench 2.1,
  34.8% SWE-fficiency, 28.8% KernelBench Hard, 74.2% MCP Atlas. The API
  is live now with 50% off ≤512K context for the first 7 days; weights
  + tech report promised in ~10 days (~mid-June 2026). Same-cycle day-zero
  integrations: @ollama Cloud (US-based hosting), @OpenRouter (50% off
  first week), @AskVenice (anonymous), @opencode (free trial), and
  Hermes Agent (Nous Research, auto-populated in model picker). Trending
  #2 on X with ~3,400 posts. Third-party live test @jiayuan_jy: "subjective
  feel approaching Opus 4.7"; @MikaStars39 reports M3 independently
  reproducing an ICLR 2025 Outstanding Paper Award winner ("Learning
  Dynamics..."). Open critique from @buildwithhassan: the small delta
  vs MiniMax's own M2.7 on multiple tasks implies M2.x numbers may have
  been inflated.
expected: "Weights + tech report drop ~2026-06-10/11"
labels:
  - released
  - open-weights
  - frontier-model
  - china
  - long-context
  - sparse-attention
  - coding
  - agentic
  - multimodal
verification: confirmed
sources:
  - "@MiniMax_AI"
  - "@ollama"
  - "@OpenRouter"
  - "@AskVenice"
  - "@opencode"
  - "@buildwithhassan"
  - "@jiayuan_jy"
  - "@MikaStars39"
created_at: 2026-05-28
updated_at: 2026-06-02
closed_at: null
closed_reason: null
history:
  - ts: 2026-05-28
    change: "Created — MiniMax M3 teased with a new sparse-attention mechanism and 15.6× long-context response speed boost over M2, per secondary roundup coverage 2026-05-27/28. No MiniMax-primary source in the visible signal; status set to `rumored` with `verification: unverified` accordingly"
  - ts: 2026-06-01
    change: "Released — primary @MiniMax_AI launch tweet 2026-06-01 01:59 UTC (~2,965 likes / 430 RT). Open-weights, MiniMax Sparse Attention scaling context to 1M, natively multimodal from step zero. Self-reported benchmarks: 59.0% SWE-Bench Pro, 66.0% Terminal Bench 2.1, 34.8% SWE-fficiency, 28.8% KernelBench Hard, 74.2% MCP Atlas. API live now (50% off ≤512K context first 7 days); weights + tech report in ~10 days. Day-zero integrations: Ollama Cloud, OpenRouter (50% off first week), AskVenice (anonymous), OpenCode (free trial), Hermes Agent. status: rumored → released; verification: unverified → confirmed. Trending #2 on X (~3,400 posts). Third-party live test @jiayuan_jy: subjective feel approaching Opus 4.7. @buildwithhassan skeptic note: small delta vs M2.7 implies M2.x scores may have been inflated"
  - ts: 2026-06-02
    change: "Adoption / sibling-product clarifications surfaced in-cycle: (1) **MiniMax Code** was launched same-tweet as M3 ('🚀New! MiniMax Code') — a coding-agent product surface bundled with the API release, separate from the model itself; reframes the launch as an M3 + Code-agent dual-ship rather than a pure model drop. (2) Pricing comparison framing emerging in third-party coverage (@_Venturini 2026-06-02 08:00 UTC): 'M3 supera GPT 5.5 e Gemini 3.1 Pro... custa 5-10% dos rivais, open source' — claim that M3 runs at ~5–10% of frontier closed-model API cost (directional, not yet third-party verified). (3) Multimodal upload of long-research-project framing from secondary aggregators: 12-hour autonomous research run with 18 code commits cited as MiniMax-supplied internal example. Status unchanged (released); waiting for weight drop (~2026-06-10/11) before independent benchmark reproductions"
---

**MiniMax M3** launched on **2026-06-01 at 01:59 UTC** via the primary
@MiniMax_AI account, resolving the May 27–28 secondary-source rumor
that originally seeded this ticket. The launch tweet (~2,965 likes /
430 RT) pitched M3 as "the first open-weights model to combine three
frontier capabilities" — coding + agentic, 1M-token context, and
native multimodal architecture from step zero.

**What shipped (per primary @MiniMax_AI):**

- **Coding + agentic frontier**, with self-reported benchmark numbers:
  59.0% SWE-Bench Pro, 66.0% Terminal Bench 2.1, 34.8% SWE-fficiency,
  28.8% KernelBench Hard, 74.2% MCP Atlas.
- **MiniMax Sparse Attention**, the new architectural mechanism, scaling
  context to **1M tokens**. A Together.ai live session with
  @zpysky1125 is announced for the day after launch to detail the
  mechanism; the full **tech report + open weights** are promised in
  ~10 days (~2026-06-10/11).
- **Native multimodal "from step zero"** — image, audio, text bundled
  into the same training stack rather than bolted on.

**Distribution on day zero:**

- **API live now** at `api@minimax.io` with self-serve access "in the
  next few days"; **50% off standard usage (≤512K context) for the
  first 7 days**.
- **Ollama Cloud** — US-based hosting, official partnership.
- **OpenRouter** — same-day listing with 50% off the first week.
- **AskVenice** — anonymous access at launch.
- **OpenCode** — free trial day-one.
- **Hermes Agent (Nous Research)** — auto-populated in the model
  picker at day-zero.

**Third-party signal in the launch cycle:**

- @jiayuan_jy: testing M3 all morning; subjective feel **approaching
  Opus 4.7**; using M3 to code with Opus 4.8 + GPT-5.5 as adversarial
  code reviewers, completed 1 PR.
- @MikaStars39 (RT'd by @MiniMax_AI): M3 independently reproduced an
  **ICLR 2025 Outstanding Paper Award winner** ("Learning Dynamics
  ..."), an unusually strong technical-validation signal in a launch
  blog.
- @buildwithhassan skeptic note: M3's reported delta over MiniMax's
  own M2.7 is small enough on multiple tasks to imply M2.x's
  published scores were inflated. Treat absolute benchmark numbers as
  provisional until weights drop and external eval shops re-run.

**Why the status moves to `released`:** the API is live, day-zero
integration partners are live, and the launch is primary @MiniMax_AI.
The weights + tech report drop in ~10 days; per the schema, the API
being live to anyone with credentials is sufficient for `released` —
the weight drop will be a history-level UPDATE, not a status change.

**Transition triggers:**
- Weights + tech report drop (~2026-06-10/11) → UPDATE with a history
  entry; weight-release slippage or partial release materially affects
  the "open-weights" framing.
- Independent reproduction of the SWE-Bench Pro 59.0% / Terminal Bench
  2.1 66.0% scores (Artificial Analysis, METR, Princeton SWE-Bench
  team) → UPDATE with the comparator.
- M3 variant (M3-mini, M3-Pro, M3-Heavy) ships → new ticket and link
  back here.
- ≥4 weeks past 2026-06-01 GA with the launch settled into normal
  coverage → `closed: released-and-aged`.

**Dedup note:** further M3 / MiniMax Sparse Attention / 1M-context /
benchmark-reproduction signal UPDATES this ticket. A distinct
M3-variant tier or successor model family gets its own ticket and
links back here. The PRC outbound-investment rules
([[china-outbound-deal-rules-2026-06]]) land the same cycle and could
affect a future MiniMax cap-table or compute-routing event; that's
tracked separately.
