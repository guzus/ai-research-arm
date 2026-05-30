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
  date now primary-confirmed: 2026-06-02 09:30 PT, kicked off by
  @satyanadella** (per @Microsoft, RT'd by @satyanadella and
  @mustafasuleyman 2026-05-29 19:50 UTC). Model lineup itself still
  partial-verification; awaiting the keynote.
expected: "Microsoft Build 2026 keynote 2026-06-02 09:30 PT (primary @Microsoft confirmation 2026-05-29)"
labels:
  - rumored
  - coding-model
  - microsoft-build
verification: partial
sources:
  - "@the_hindu"
  - "@IndiaTodayTech"
  - "@Awesome_AI_News"
  - "@mustafasuleyman"
  - "@satyanadella"
  - "@Microsoft"
created_at: 2026-05-29
updated_at: 2026-05-30
closed_at: null
closed_reason: null
history:
  - ts: 2026-05-29
    change: "Created — The Information-sourced reports (via The Hindu, India Today Tech, et al.) describe Microsoft planning multiple homegrown AI models for Build 2026, including a cost-efficient code-specific model to compete with Cursor and Claude Code on GitHub Copilot pricing, plus multiple parameter sizes. Foreshadowed by @mustafasuleyman on 2026-05-26 ('with Build just a week away, there's much more to come')"
  - ts: 2026-05-30
    change: "Build keynote date primary-confirmed: 2026-06-02 09:30 PT, kicked off by @satyanadella (per @Microsoft, RT'd by @satyanadella 19:50 UTC and @mustafasuleyman 21:55 UTC on 2026-05-29). The keynote date moves to confirmed; the model lineup itself stays at partial verification pending the keynote announcement"
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
