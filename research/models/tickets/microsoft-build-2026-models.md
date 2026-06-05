---
slug: microsoft-build-2026-models
title: Microsoft Build 2026 — homegrown AI model unveilings
company: Microsoft AI
model: null
status: confirmed
status_note: |
  **KEYNOTE DELIVERED 2026-06-02.** Microsoft used Build to unveil a
  sweeping slate of in-house AI: a new from-scratch reasoning model
  **MAI-Thinking-1** (trained without distillation, reported near-SOTA /
  top marks on math + coding benchmarks), **Project Solara**, autonomous
  workplace assistants, and NVIDIA-powered PCs (RTX Spark, see
  [[nvidia-gtc-taipei-2026-06]]). The unified **Copilot super-app shipped
  a model picker** — notably exposing **Anthropic Claude Opus 4.8** inside
  a Microsoft product ([[opus-4-8]]) — and **MAI-Thinking-1 is available
  now via the Microsoft Frontier program** (requires a GitHub Copilot
  subscription). Status advances rumored → confirmed: the keynote happened
  and the models were announced on Microsoft's own surfaces, with
  MAI-Thinking-1 in limited Frontier availability rather than broad GA.
  Pre-keynote reporting below remains for the audit trail.

  The Information (via The Hindu / India Today Tech / aggregator
  syndication, 2026-05-29 ~07:30 UTC) reports Microsoft will unveil a
  suite of self-developed AI models at next week's Build conference in
  San Francisco, including a coding model intended to boost GitHub
  Copilot in the face of Cursor/Claude Code competition, plus models
  at multiple parameter sizes. Also flagged in @mustafasuleyman's
  2026-05-26 MAI-Image-2.5 tweet ("with Build just a week away, there's
  much more to come from the @MicrosoftAI team"). **Build keynote
  date primary-confirmed: 2026-06-02 09:30 PT, kicked off by
  @satyanadella** (per @Microsoft, RT'd by @satyanadella and
  @mustafasuleyman 2026-05-29 19:50 UTC). **Two-source convergence as
  of 2026-05-31**: @testingcatalog (15:33 UTC, climbed to ~365 likes /
  33 RT by 21:30 UTC) leaked the unified Copilot super app with
  **Copilot Code (GitHub Copilot inside)**, **Copilot Cowork**, and
  **Scout 24/7 Agent** tabs for 2026-06-02 unveil — and named the
  specific model lineup: **MAI Voice 2** (15 languages, broader
  emotional range), **MAI Transcribe 1.5** (STT), **MAI Image 2.5**
  (already on LM Arena preview, see [[microsoft-mai-image-2-5]]).
  @theinformation reposted its enterprise scoop 2026-05-31 19:00 UTC:
  "Microsoft is preparing new homegrown AI models for **coding, speech,
  transcription, reasoning and images**. The push is aimed at reducing
  its reliance on OpenAI and Anthropic while giving developers cheaper
  options through Azure." Two reporting paths, one product map.
  Microsoft Build session catalog already has 90+ agentic-AI / Azure
  AI Foundry / GitHub Copilot / on-device-Windows sessions; Copilot
  Studio's "computer-using agents" are now GA per a late-May
  announcement. Lands 24h after [[nvidia-gtc-taipei-2026-06]] (NVIDIA's
  DGX Station for Windows + RTX Spark + OpenShell trio is a deliberate
  Windows-on-NVIDIA counter-position).
expected: "Microsoft Build 2026 keynote 2026-06-02 09:30 PT (primary @Microsoft confirmation 2026-05-29)"
labels:
  - coding-model
  - microsoft-build
  - mai-models
  - mai-thinking-1
  - copilot-super-app
  - reasoning-model
verification: confirmed
sources:
  - "@the_hindu"
  - "@IndiaTodayTech"
  - "@Awesome_AI_News"
  - "@mustafasuleyman"
  - "@satyanadella"
  - "@Microsoft"
  - "@testingcatalog"
  - "@theinformation"
  - "@gmanews"
  - "@AI_News_Digest"
created_at: 2026-05-29
updated_at: 2026-06-05
closed_at: null
closed_reason: null
history:
  - ts: 2026-05-29
    change: "Created — The Information-sourced reports (via The Hindu, India Today Tech, et al.) describe Microsoft planning multiple homegrown AI models for Build 2026, including a cost-efficient code-specific model to compete with Cursor and Claude Code on GitHub Copilot pricing, plus multiple parameter sizes. Foreshadowed by @mustafasuleyman on 2026-05-26 ('with Build just a week away, there's much more to come')"
  - ts: 2026-05-30
    change: "Build keynote date primary-confirmed: 2026-06-02 09:30 PT, kicked off by @satyanadella (per @Microsoft, RT'd by @satyanadella 19:50 UTC and @mustafasuleyman 21:55 UTC on 2026-05-29). The keynote date moves to confirmed; the model lineup itself stays at partial verification pending the keynote announcement"
  - ts: 2026-06-01
    change: "Two-source convergence: @testingcatalog 2026-05-31 leaks the unified Copilot super-app with Copilot Code (GitHub Copilot inside), Copilot Cowork, and Scout 24/7 Agent tabs; same outlet's earlier MAI lineup leak names MAI Voice 2 (15 languages, wider emotional range), MAI Transcribe 1.5 (STT), MAI Image 2.5 (already on LM Arena, see [[microsoft-mai-image-2-5]]). @theinformation 2026-05-31 19:00 UTC restates: 'homegrown AI models for coding, speech, transcription, reasoning and images' aimed at reducing reliance on OpenAI/Anthropic via Azure. Two reporting paths, one product map. Build session catalog has 90+ agentic-AI / Azure AI Foundry / GitHub Copilot sessions; Copilot Studio computer-using agents now GA. Lands 24h after [[nvidia-gtc-taipei-2026-06]] DGX Station for Windows + RTX Spark + OpenShell. @kimmonismus in SF for Build 2026-05-31 21:07 UTC"
  - ts: 2026-06-03
    change: "Keynote delivered 2026-06-02 — status rumored → confirmed, verification partial → confirmed. Microsoft unveiled the homegrown reasoning model **MAI-Thinking-1** (trained from scratch without distillation, reported near-SOTA / top math + coding benchmark marks), **Project Solara**, autonomous workplace assistants, and NVIDIA-powered PCs. The unified Copilot super-app shipped a **model picker** exposing Anthropic **Claude Opus 4.8** ([[opus-4-8]]) inside a Microsoft product — same week Microsoft reportedly cut internal Claude Code licenses. **MAI-Thinking-1 is available now via the Microsoft Frontier program** (GitHub Copilot subscription required) — limited availability, not broad GA. Sources: GMA News (Microsoft 'announced a sweeping slate of AI initiatives… a new in-house reasoning model'), AI_News_Digest / Marktechpost (MAI-Thinking-1 trained from scratch, top math/coding marks), plus pre-keynote @theinformation / @testingcatalog map confirmed. The reasoning model fulfils 'reasoning' in the pre-leaked coding/speech/transcription/reasoning/images lineup"
  - ts: 2026-06-05
    change: "The pre-leaked **coding** model in the lineup ships as **MAI Code 1 Flash** — Microsoft's own coding model inside GitHub Copilot, reported free across all Copilot tiers from 2026-06-05, with 256K context, ~60% fewer tokens on complex tasks, and 85.8% on Microsoft's adversarial coding benchmark; pitched as trained inside the Copilot production environment to defend Copilot vs Cursor/Claude Code. Spun out to its own per-model ticket [[microsoft-mai-code-1-flash]] (single hype-account source @cyrilXBT, no Microsoft primary in-window). This bundle stays the umbrella; the coding slot in the coding/speech/transcription/reasoning/images map is now filled. Status unchanged (confirmed)"
---

A 2026-05-29 cluster of reports — The Information via several mainstream
aggregators (The Hindu, India Today Tech) and Chinese-language AI news
accounts — describes Microsoft preparing to unveil a **suite of
self-developed AI models** at the upcoming Build conference in San
Francisco. The headline item is a **cost-efficient code-specific
model** positioned to defend GitHub Copilot's share against Cursor and
Claude Code, with additional models at varying parameter sizes
rounding out the announcement.

@mustafasuleyman (MAI lead) foreshadowed this on **2026-05-26**, in
the same thread that introduced MAI-Image-2.5: "with Build just a week
away, there's much more to come from the @MicrosoftAI team."

**Why this ticket and why `rumored`.** The narrative is consistent
across multiple aggregators citing The Information, plus the in-house
signal from @mustafasuleyman, but Microsoft has not yet published a
primary announcement on @MicrosoftAI / Microsoft blog. Per the schema,
that pattern maps to `rumored` + `verification: partial`. Once Build
opens and the models are announced on Microsoft's own surfaces, this
ticket transitions to `confirmed` and then `released` per launch
timing.

**Scope.** This is a *bundle* ticket. Individual models that get named
on stage (e.g. "MAI-Code-1", or whatever the coding model is branded)
may spawn their own per-model tickets after launch if they look
load-bearing on their own — at which point this ticket either closes
with `superseded-by:<slug>` or stays as the bundle-level umbrella.

**Transition triggers:**
- Build keynote announces the models → advance to `confirmed` (or
  `released` if access ships day-of), append a history entry per
  model named.
- Build passes without the unveiling → close with `disproved` and
  link to whatever Microsoft *did* announce.
- ≥15 daily cycles at `rumored` / `partial` with no fresh
  corroboration → close with `stale-rumor-unverified`.
