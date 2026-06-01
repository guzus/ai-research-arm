---
slug: microsoft-build-2026-models
title: Microsoft Build 2026 — homegrown AI model unveilings
company: Microsoft AI
model: null
status: rumored
status_note: |
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
  - rumored
  - coding-model
  - microsoft-build
  - mai-models
  - copilot-super-app
verification: partial
sources:
  - "@the_hindu"
  - "@IndiaTodayTech"
  - "@Awesome_AI_News"
  - "@mustafasuleyman"
  - "@satyanadella"
  - "@Microsoft"
  - "@testingcatalog"
  - "@theinformation"
created_at: 2026-05-29
updated_at: 2026-06-01
closed_at: null
closed_reason: null
history:
  - ts: 2026-05-29
    change: "Created — The Information-sourced reports (via The Hindu, India Today Tech, et al.) describe Microsoft planning multiple homegrown AI models for Build 2026, including a cost-efficient code-specific model to compete with Cursor and Claude Code on GitHub Copilot pricing, plus multiple parameter sizes. Foreshadowed by @mustafasuleyman on 2026-05-26 ('with Build just a week away, there's much more to come')"
  - ts: 2026-05-30
    change: "Build keynote date primary-confirmed: 2026-06-02 09:30 PT, kicked off by @satyanadella (per @Microsoft, RT'd by @satyanadella 19:50 UTC and @mustafasuleyman 21:55 UTC on 2026-05-29). The keynote date moves to confirmed; the model lineup itself stays at partial verification pending the keynote announcement"
  - ts: 2026-06-01
    change: "Two-source convergence: @testingcatalog 2026-05-31 leaks the unified Copilot super-app with Copilot Code (GitHub Copilot inside), Copilot Cowork, and Scout 24/7 Agent tabs; same outlet's earlier MAI lineup leak names MAI Voice 2 (15 languages, wider emotional range), MAI Transcribe 1.5 (STT), MAI Image 2.5 (already on LM Arena, see [[microsoft-mai-image-2-5]]). @theinformation 2026-05-31 19:00 UTC restates: 'homegrown AI models for coding, speech, transcription, reasoning and images' aimed at reducing reliance on OpenAI/Anthropic via Azure. Two reporting paths, one product map. Build session catalog has 90+ agentic-AI / Azure AI Foundry / GitHub Copilot sessions; Copilot Studio computer-using agents now GA. Lands 24h after [[nvidia-gtc-taipei-2026-06]] DGX Station for Windows + RTX Spark + OpenShell. @kimmonismus in SF for Build 2026-05-31 21:07 UTC"
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
