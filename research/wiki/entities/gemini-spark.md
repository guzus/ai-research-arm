---
slug: gemini-spark
title: Gemini Spark
type: entity
aliases: ["Gemini Spark", "Google Gemini Spark", "Spark agent"]
tags: [agents, google, gemini, consumer-agent, product]
summary: Google's persistent consumer agent for Gemini, hit GA on 2026-05-29 for US AI Ultra subscribers at $99.99/mo — the first GA paid frontier-lab persistent consumer agent, running on dedicated Google Cloud VMs so state persists with the phone off.
created_at: 2026-06-01
updated_at: 2026-06-01
sources:
  - {title: "ARA daily digest 2026-06-01", path: research/digest/2026-06-01-digest.md}
  - {title: "9to5Google — Gemini Spark GA", date: 2026-05-29}
---

**Gemini Spark** is Google's persistent consumer agent layered on top
of the **Gemini** assistant. It went GA for US-based **Google AI Ultra**
subscribers on **2026-05-29** at the existing **$99.99/mo** Ultra tier
(no separate SKU). The rollout was quiet — 9to5Google was first to
surface it.

## Why it matters

- **First paid persistent consumer agent shipped by a frontier lab.**
  [[anthropic]] [[dynamic-workflows]] targets developers; OpenAI Codex
  Goal Mode is coding-anchored; Mistral Vibe is EU-only; Apple's
  standalone Siri app was announced not GA. Spark wins the **paid
  US-consumer persistent-agent** category on time-to-ship.
- **Cloud-resident execution substrate.** Spark runs on **dedicated
  Google Cloud VMs**, so agent state and long-running tasks **persist
  server-side with the phone or laptop powered off**. First frontier-lab
  consumer agent to ship on a fully cloud-resident execution model
  rather than an on-device runtime.
- **Three surfaces.** **Tasks** (long-horizon Gmail / Calendar / Docs /
  Sheets / Slides workflows), **Skills** (composable user-defined
  capabilities), **Schedules** (cron-style recurring tasks).
- **Built on Gemini 3.5 Flash + Antigravity.** Spark runs on
  [[gemini-3-5-flash]] with the **Antigravity agent orchestration
  platform** Google introduced at I/O 2026 — not a new base model.
- **Counter-positioning window.** Spark lands four days before
  Microsoft Build (June 2), where Copilot Agent Mode + the Windows
  Agent Store are staged as the counter-position — and a week before
  WWDC's Siri reboot. Google ships before the headline event, claiming
  the "first paid frontier-lab consumer agent" frame.

## Open questions

- **Cloud-VM economics.** Persistent agent state on dedicated Google
  Cloud VMs per Ultra subscriber is structurally expensive. Does the
  $99.99 Ultra tier subsidize this from the rest of the Gemini bundle,
  or is Spark a loss-leader for the bundle?
- **EU/UK availability.** US-only at GA — Spark's persistence on Google
  Cloud VMs creates a clear data-residency surface for EU AI Act and
  UK regulators. International rollout cadence will be the test of
  whether the cloud-resident model is portable.
- **Counter-position fit.** Microsoft Copilot's unified super-app (Code
  + Cowork + Scout 24/7 Agent) is the explicit consumer-agent rival
  staged for June 2. Does the agent-store / extension model out-compete
  Spark's Skills surface on developer mindshare?
