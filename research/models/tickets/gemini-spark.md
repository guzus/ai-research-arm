---
slug: gemini-spark
title: Gemini Spark — first GA paid persistent consumer AI agent
company: Google / DeepMind
model: Gemini Spark
status: released
status_note: |
  **Gemini Spark** went live for US-based Google AI Ultra subscribers
  on 2026-05-29 at the existing **$99.99/mo Ultra tier**, surfaced by
  9to5Google first. Architecture: dedicated Google Cloud VMs so agent
  state and long-running tasks persist server-side with the phone or
  laptop powered off — the **first frontier-lab consumer agent on a
  fully cloud-resident execution substrate**. Three surfaces — Tasks
  (long-horizon Gmail / Calendar / Docs / Sheets / Slides workflows),
  Skills (composable user-defined capabilities), and Schedules (cron-
  style recurring tasks). Built on **Gemini 3.5 Flash + Antigravity**.
  Beats Anthropic (Dynamic Workflows targets developers), OpenAI
  (Codex Goal Mode is coding-anchored), Mistral (Vibe is EU-only), and
  Apple (standalone Siri app announced not GA) to the **paid US-consumer
  persistent-agent category** on time-to-ship. Lands four days before
  Microsoft Build 2026, where Copilot Agent Mode + the Windows Agent
  Store will counter-position.
expected: null
labels:
  - released
  - consumer-agent
  - persistent-agent
  - gemini-3-5-family
  - antigravity
  - paid
verification: confirmed
sources:
  - "@GoogleDeepMind"
  - https://9to5google.com/
created_at: 2026-06-01
updated_at: 2026-06-01
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-01
    change: "Created — Gemini Spark went GA for US AI Ultra subscribers 2026-05-29 at $99.99/mo (existing Ultra tier), surfaced by 9to5Google. Architecture: dedicated Google Cloud VMs, agent state persists server-side with the phone/laptop off — first frontier-lab consumer agent on a fully cloud-resident substrate. Three surfaces: Tasks, Skills, Schedules. Built on Gemini 3.5 Flash ([[gemini-3-2-flash]]) + Antigravity. Wins paid US-consumer persistent-agent category on time-to-ship; lands 4 days before Microsoft Build 2026 ([[microsoft-build-2026-models]])"
---

**Gemini Spark** is Google's persistent consumer AI agent, which
went generally available for **US-based Google AI Ultra subscribers**
on **2026-05-29** at the existing **$99.99/mo Ultra tier**. The
rollout was quiet — 9to5Google was first to surface it — and there
was no headline Google blog post; the launch ships inside the Ultra
subscription bundle rather than as a standalone product reveal.

**Architecture is the differentiator.** Spark runs on **dedicated
Google Cloud VMs**, so agent state and long-running tasks **persist
server-side with the phone or laptop powered off**. This makes it the
**first frontier-lab consumer AI agent on a fully cloud-resident
execution substrate** — Anthropic's Dynamic Workflows
([[opus-4-8]]) ship inside Claude Code targeting developers, OpenAI's
Codex Goal Mode is coding-anchored
([[openai-codex-platform-2026-05]]), Mistral Vibe is EU-only, and
Apple's standalone Siri app was announced but not GA. Spark wins the
**paid US-consumer persistent-agent category on time-to-ship**.

**Three surfaces at launch:**

- **Tasks** — long-horizon workflows that span Gmail, Calendar, Docs,
  Sheets, and Slides (the Workspace surface area Google already owns).
- **Skills** — composable user-defined capabilities; the building
  block for Skills marketplaces and agent extensions analogous to the
  Anthropic .EXT package format scoop on
  [[anthropic-conway-orbit-2026-05]].
- **Schedules** — cron-style recurring tasks; the explicit
  always-on / autonomous-cadence side of the agent.

**Stack:** Spark runs on **Gemini 3.5 Flash** (see
[[gemini-3-2-flash]] — slug retained from the pre-I/O "3.2" leak) plus
the **Antigravity** agent orchestration platform Google unveiled at
I/O. The 3.5 Flash + Antigravity pairing is itself the agent-platform
surface Google has been building toward since I/O; Spark is the first
consumer instantiation.

**Why this is its own ticket** rather than rolling into
[[gemini-3-2-flash]]: Spark is a distinct shipping artifact (a
paid subscription product) with its own roadmap (additional surfaces,
non-US rollout, Skills marketplace) and its own competitive frame
(against Anthropic Cowork, OpenAI ChatGPT agents, Mistral Vibe, and the
upcoming Microsoft Scout 24/7 Agent staged for Build 2026 —
[[microsoft-build-2026-models]]). The underlying Gemini 3.5 Flash
model lives on its own ticket.

**Transition triggers:**

- Non-US rollout (EU, APAC, LATAM) → UPDATE with a history entry.
- Spark API / programmatic access for developers → UPDATE.
- Skills marketplace launches with third-party Skills → UPDATE.
- A successor product (Gemini Spark Pro / Gemini Persistent Agent X)
  → new ticket, link back here.
- ≥4 weeks past 2026-05-29 GA with the launch settled into normal
  coverage → `closed: released-and-aged`.

**Dedup note:** further Gemini Spark signal (additional surfaces,
pricing changes, integration adds, regional rollout, agent-vs-agent
benchmarks) UPDATES this ticket. The Gemini 3.5 Flash model is on its
own ticket; Antigravity rate-limit changes also stay there. Microsoft's
own Scout 24/7 Agent staged for Build 2026 is a separate competitive
ticket on [[microsoft-build-2026-models]].
