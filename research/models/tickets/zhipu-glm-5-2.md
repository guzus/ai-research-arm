---
slug: zhipu-glm-5-2
title: Zhipu GLM 5.2 — open-weight frontier model
company: Zhipu AI
model: GLM 5.2
status: released
status_note: |
  **GLM 5.2** (Zhipu AI / Z.ai) is **out** — deployed in the **GLM Coding
  Plan** now, with **API access and MIT-licensed open weights "in a week."**
  Reported specs: **1M-token context**, **max/high "thinking" modes**. Early
  community benchmarks place it strongly among open models — a one-shot Pac-Man
  coding test ranked it **first above Qwen 3.6 27B**. Dominant open-weights
  story this cycle (HN front page ~468 pts; top of r/LocalLLaMA). Tracked
  alongside other open-weight contenders [[minimax-m3]], [[alibaba-qwen-3-7-plus]],
  [[gemma-4]]. **2026-06-16:** corroborated by a dated **2026-06-15 launch
  announcement** (Zhipu/"Huazhang Technology") billing GLM-5.2 as its newest
  flagship — **1M long context**, "leading on long-range tasks," **to be
  open-sourced under MIT** — restated across China-tech aggregators. Still no
  captured primary Zhipu blog/model card and the MIT weights are described as
  forthcoming, so verification stays `partial`.

  **2026-06-18:** MIT weights are now **live** and the release is fully
  corroborated. Z.ai's **official announcement thread** (@Zai_org, 2026-06-16
  17:40 UTC) bills GLM-5.2 as "Frontier Intelligence, Open Weights" — a
  **744B-A40B MoE**, **1M context**, two reasoning-effort levels (max/high),
  priced the same as GLM-5.1, **46.2% DeepSWE**. Same-day **ecosystem uptake**:
  **vLLM day-0 support in v0.23.0**, plus Notion and Baseten live, and MIT
  weights on HuggingFace. Community placement is strong — @kimmonismus calls it
  "the third best model available across open and proprietary," it reportedly
  took the top of the design arena after Fable 5 was pulled, and @ns123abc rates
  it "Opus 4.6 / GPT-5.4 tier." Z.ai also shipped a **ZCode** desktop coding
  agent built around the model. With an official thread + live MIT weights +
  independent ecosystem adoption, verification advances to `confirmed`; neutral
  SWE-bench/LiveCodeBench placement beyond the lab's own DeepSWE number is the
  remaining gap.

  **2026-06-20:** Surface + benchmark expansion. GLM-5.2 is now **live on Z.ai
  Web Chat** (following the API launch), putting the 1M-context model in the
  browser. Neutral-leaderboard placement — the gap flagged on 06-18 — has begun
  to fill: community recaps put it **#1 on Design Arena**, **#1 open-weights on
  the Artificial Analysis Intelligence Index**, the **first open model >80% on
  Terminal-Bench**, and ~**74.4 on FrontierSWE vs Opus 4.8's 75.1** (i.e.
  near-frontier on a third-party coding eval), at ~**$1.4/$4.4 per MTok**. Still
  routed largely through secondary/community accounts rather than a neutral
  benchmark org's primary post, so it sharpens — but does not replace — the
  neutral-placement caveat. Status stays `released`, verification stays
  `confirmed`.

  **2026-06-21:** The open-weights "no moat" thesis got its sharpest day yet.
  GLM-5.2 took **#1 on Design Arena's single-turn web-design board** — beating a
  frozen Fable 5 — and drew multi-practitioner raves (**Jeremy Howard**, ~7K
  likes). An independent benchmark claiming **GPT-5.5 hallucinates ~3× more than
  MIT-licensed GLM-5.2** hit the HN front page (467 pts / 232 comments), and
  public **subscription-cancellation defections** surfaced (developer @burkov:
  "I already cancelled my Anthropic subscription… No moat isn't hypothetical
  anymore," keeping Codex only because GLM "cannot see"). Restated specs include
  a **Terminal-Bench 2.1 jump 63.5→81.0**, 1M context, and an
  **anti-reward-hacking RL module**. Caveats persist: design-only board, no
  vision, and senior devs note self-hosting still doesn't pencil out vs. a $200
  Codex plan. Status stays `released`, verification stays `confirmed`.

  **2026-06-22:** The model story became a **market event**. The raves crossed
  into mainstream dev-tooling leadership — **Vercel CEO Guillermo Rauch**
  ("almost shocked… this changes things," ~5.4K likes) joined Jeremy Howard
  on-record — and **Elon Musk's** "GLM could reach Fable-class by Q1" line
  circulated as a catalyst. Maker **Zhipu/Z.ai (HK:02513)** is reported **up
  ~15× since its ~6-month-old IPO**, with JPMorgan said to have lifted its target
  to **HK$1,800**, and its market cap **broke 1 trillion HKD intraday** (~HK$2,980
  high) on June 22 — five sessions of GLM-5.2-driven gains. China also reportedly
  **opened its 5th STAR Market listing standard to pre-revenue AI labs**, with
  Zhipu's **A-share IPO (~$15B raise) "accepted"** — a domestic capital pipeline
  insulating it from US financial pressure. Caveats: the precise figures
  (+1,700% YTD, +48% single-day, the exact HK$1,800 / trillion-HKD print) come
  from **retail/CT accounts** (some marketing onchain HK-equity perps), the float
  is thin (~4%), and a ~July 8 share unlock looms — directional re-rating is real
  and multi-sourced, the decimals are not. Status stays `released`, verification
  stays `confirmed`.

  **2026-06-23:** Neutral-leaderboard placement keeps filling in. Fresh
  third-party numbers put GLM-5.2 at **#3 overall / #1 open-weights on
  GDPval-AA** (1524 Elo, level with GPT-5.5 xhigh), **2nd on Game Dev Arena**
  (Elo 1368, inside Fable 5's band), and **#1 open-weights on Artificial
  Analysis's Intelligence Index** (score 51); it is also reported as the first
  open-weights model to run alphaXiv's autoresearch pipeline end-to-end. The
  open-weights tier now clearing GPT-5.5-class agentic work while the
  US-controlled frontier sits partly frozen. Caveat: still **no image
  understanding**. Status stays `released`, verification stays `confirmed`.

  **2026-06-26:** GLM-5.2 (Max) jumped from 1408 to **1595 on the Code Arena
  Frontend** benchmark overnight, **surpassing Opus 4.8** ([[opus-4-8]]) and
  narrowing the gap to **Claude Fable 5 (1665)** — with **OpenRouter's new
  Benchmarks API** simultaneously ranking GLM-5.2 the **best available model for
  both coding and design**. Multi-source: @arena published the trajectory
  directly (~27 likes), @jp54362 relayed the 1595 score with a screenshot, and
  @OpenRouter independently ranked it #1 for coding & design (a +187-point
  single-leap gain). It also returned to the top of the **Design Arena** per
  artificial-analysis data. Two caveats: Code Arena Frontend is one agentic
  benchmark (a frontend-coding slot where GLM-5.2's vision-language training
  gives it an edge, not general frontier supremacy), and Fable 5's 1665 score
  is **frozen** (Fable 5 removed mid-June, [[claude-fable-5]]) — GLM-5.2 is
  "closing" on a stationary target, so the real test is the next Zai_org model
  vs whatever replaces Fable 5 on the leaderboard. Separately, Cursor published
  research that Opus 4.8 and Composer 2.5 retrieve benchmark solutions from the
  internet/git history during eval (scores drop under a stricter harness) — but
  that work did not test GLM-5.2, so GLM-5.2's 1595 stands until someone applies
  Cursor's methodology to it specifically. Status stays `released`, verification
  stays `confirmed`.
expected: "Shipped — MIT weights live (HuggingFace), API + GLM Coding Plan + Web Chat, day-0 vLLM/Notion/Baseten support; leaderboards strong (Design Arena #1, AA Index #1 open-weights, Terminal-Bench 2.1 ~81, Code Arena Frontend 1595 past Opus 4.8 / closing on frozen Fable 5 1665; OpenRouter ranks it best available for coding & design). Now a market event: Vercel CEO/Jeremy Howard on-record raves, maker Zhipu (HK:02513) up ~15× since IPO / >1T HKD intraday, reported STAR A-share IPO (~$15B) accepted; exact figures retail-sourced, neutral-org primary benchmark placement still settling. Caveat: still no image understanding"
labels:
  - frontier-model
  - open-weights
  - china
  - coding
  - released
verification: confirmed
sources:
  - "@Zai_org"
  - https://news.ycombinator.com/item?id=48518684
  - "@testingcatalog"
  - "@kimmonismus"
  - "@ns123abc"
  - "@jeremyphoward"
  - "@burkov"
  - https://news.ycombinator.com/item?id=48600167
  - "@rauchg"
  - "@guohao_li"
  - "@AndrewCurran_"
  - https://venturebeat.com/technology/z-ais-open-weights-glm-5-2-beats-gpt-5-5-on-multiple-long-horizon-coding-benchmarks-for-1-6th-the-cost
  - "@arena"
  - "@jp54362"
  - "@OpenRouter"
created_at: 2026-06-14
updated_at: 2026-06-26
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-14
    change: "Created — Zhipu AI shipped GLM 5.2: deployed in the GLM Coding Plan now, with API + MIT open weights promised within a week. Reported 1M context, max/high thinking modes; early one-shot coding benchmarks rank it above Qwen 3.6 27B. Dominant open-weights story this cycle (HN ~468 pts, top of r/LocalLLaMA). Usable in the coding plan now → status released; widely corroborated across HN/r/LocalLLaMA but no captured primary Zhipu blog/model card and weights not yet public → verification partial. Sits with open-weight peers [[minimax-m3]], [[alibaba-qwen-3-7-plus]], [[gemma-4]]"
  - ts: 2026-06-16
    change: "Corroboration — a dated 2026-06-15 launch announcement (attributed to Zhipu / 'Huazhang Technology') restates GLM-5.2 as the newest flagship with 1M long context, a claimed lead on long-range tasks, and MIT open-sourcing, echoed across China-tech aggregators. Strengthens the release record but still no captured primary Zhipu blog/model card and the MIT weights are described as forthcoming → status stays released, verification stays partial."
  - ts: 2026-06-18
    change: "MIT weights live + verification → confirmed. Z.ai's official thread (@Zai_org 2026-06-16) bills GLM-5.2 as 744B-A40B MoE, 1M context, max/high reasoning, 46.2% DeepSWE, same price as GLM-5.1. Day-0 ecosystem uptake (vLLM v0.23.0, Notion, Baseten) plus HuggingFace MIT weights. Strong community placement — @kimmonismus 'third best model across open + proprietary,' top of design arena after Fable 5's pull, @ns123abc 'Opus 4.6 / GPT-5.4 tier'; Z.ai also shipped a ZCode desktop agent. Official thread + live weights + independent adoption → verification confirmed; neutral SWE-bench/LiveCodeBench placement still the open gap."
  - ts: 2026-06-20
    change: "Surface + benchmark expansion. GLM-5.2 now live on Z.ai Web Chat (after the API launch), putting the 1M-context model in the browser. Neutral-leaderboard placement (the 06-18 gap) starts filling: community recaps put it #1 on Design Arena, #1 open-weights on the Artificial Analysis Intelligence Index, first open model >80% on Terminal-Bench, and ~74.4 FrontierSWE vs Opus 4.8's 75.1, at ~$1.4/$4.4 per MTok. Still mostly secondary/community routing rather than a neutral benchmark org's primary post → status stays released, verification stays confirmed. Sources: @aimeowyak 2068237497562517938, @johnseach 2068237957669228677."
  - ts: 2026-06-21
    change: "Open-weights 'no moat' thesis got teeth. GLM-5.2 took #1 on Design Arena's single-turn web-design board (beating a frozen Fable 5) and drew multi-practitioner raves (Jeremy Howard ~7K likes). An independent benchmark claiming GPT-5.5 hallucinates ~3× more than MIT-licensed GLM-5.2 hit the HN front page (467 pts / 232 comments); public subscription-cancellation defections surfaced (@burkov: 'I already cancelled my Anthropic subscription… No moat isn't hypothetical anymore,' keeps Codex only because GLM 'cannot see'). Restated specs: Terminal-Bench 2.1 63.5→81.0, 1M context, anti-reward-hacking RL module. Caveats persist (design-only board, no vision, self-hosting still doesn't pencil out vs a $200 Codex plan). First leaderboard-backed erosion of the open-vs-closed gap. Status stays released, verification stays confirmed."
  - ts: 2026-06-22
    change: "Model story became a market event. Raves crossed into mainstream dev-tooling leadership — Vercel CEO Guillermo Rauch ('almost shocked… this changes things,' ~5.4K likes) alongside Jeremy Howard; Musk's 'GLM could reach Fable-class by Q1' line cited as a catalyst. Maker Zhipu/Z.ai (HK:02513) reported up ~15× since its ~6-month IPO, JPMorgan said to lift PT to HK$1,800, market cap broke 1 trillion HKD intraday (~HK$2,980 high) on June 22; China reportedly opened a 5th STAR Market listing standard to pre-revenue AI labs with Zhipu's A-share IPO (~$15B) 'accepted.' Directional re-rating multi-sourced; exact figures (+1,700% YTD, +48%/day, HK$1,800, trillion-HKD print) are retail/CT-sourced (thin ~4% float, ~July 8 unlock). Status stays released, verification stays confirmed. Sources: @rauchg, @guohao_li, @au_xbt, @ns123abc."
  - ts: 2026-06-23
    change: "Neutral-leaderboard placement keeps filling in. Fresh third-party numbers (VentureBeat + community recaps) put GLM-5.2 at #3 overall / #1 open-weights on GDPval-AA (1524 Elo, level with GPT-5.5 xhigh), 2nd on Game Dev Arena (Elo 1368, inside Fable 5's band), and #1 open-weights on Artificial Analysis's Intelligence Index (51); also reported as the first open-weights model to run alphaXiv's autoresearch pipeline end-to-end. @AndrewCurran_ (quote of the day) frames the open-weights tier as now clearing GPT-5.5-class agentic work while the US-controlled frontier sits partly frozen. Caveat: still no image understanding. Status stays released, verification stays confirmed."
  - ts: 2026-06-26
    change: "GLM-5.2 (Max) jumped 1408→1595 on Code Arena Frontend overnight, surpassing Opus 4.8 ([[opus-4-8]]) and closing on Fable 5's 1665; OpenRouter's new Benchmarks API simultaneously ranked GLM-5.2 best available for coding & design. Multi-source: @arena published the trajectory, @jp54362 relayed the 1595 score with a screenshot, @OpenRouter ranked it #1 (+187-point single-leap); also returned to the top of Design Arena. Caveats logged: Code Arena Frontend is one agentic benchmark (frontend-coding slot favoring GLM-5.2's vision-language training, not general frontier supremacy); Fable 5's 1665 is frozen (model removed mid-June, [[claude-fable-5]]) so GLM-5.2 is 'closing' on a stationary target. Cursor's benchmark-contamination research named Opus 4.8 and Composer 2.5 — not GLM-5.2 — so the 1595 stands until Cursor's methodology is applied to it specifically. Status stays released, verification stays confirmed. Sources: @arena, @jp54362, @OpenRouter."
---

**GLM 5.2**, from **Zhipu AI (Z.ai)**, is the cycle's dominant open-weights
release. It is **already deployed in the GLM Coding Plan**, with **API
access and MIT-licensed open weights** promised **within a week**. Reported
specs include a **1M-token context window** and **max/high "thinking"
modes**.

**Capability signal.** Early community benchmarks are strong rather than
authoritative: a widely-shared one-shot Pac-Man coding test ranked GLM 5.2
**first, above Qwen 3.6 27B**. The release topped r/LocalLLaMA and reached
the Hacker News front page (~468 points), with the open-weights / local-
hosting community treating it as a timely counterpoint to the same week's
Anthropic export-control shutdown
([[anthropic-fable-mythos-export-control-2026-06]]).

**Why `released` / `partial`.** Because GLM 5.2 is usable now inside the
GLM Coding Plan, the lifecycle is `released`. `verification` stays
`partial`: the release is corroborated across HN and r/LocalLLaMA, but no
**primary Zhipu blog post or model card** was captured in-window, and the
MIT open weights are not yet public — both would advance it to `confirmed`.

**Transition triggers:**
- MIT weights + API go live, or a primary Zhipu model card → UPDATE,
  advance `verification` to `confirmed`.
- A successor (GLM 5.x) → new ticket; do not reopen this one.
- ≥4 weeks past release, settled into normal coverage → `closed: released-and-aged`.

**Dedup note:** further GLM 5.2 release/benchmark/weights signal UPDATES
this ticket. Other open-weight models stay on their own tickets
([[minimax-m3]], [[alibaba-qwen-3-7-plus]], [[gemma-4]]).
