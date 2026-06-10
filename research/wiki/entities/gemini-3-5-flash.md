---
slug: gemini-3-5-flash
title: Gemini 3.5 Flash
type: entity
aliases: ["Gemini 3.5 Flash", "Gemini 3.2 Flash", "Gemini 3.5 Live Translate"]
tags: [model-release, google-deepmind, flash-tier, agentic]
summary: Google's fast, low-cost frontier model shipped GA at Google I/O 2026, positioned for agents rather than chatbots; gained a real-time speech-to-speech Live Translate variant (70+ languages) on 2026-06-09.
created_at: 2026-05-24
updated_at: 2026-06-10
sources:
  - {title: "ARA daily digest 2026-06-10", path: research/digest/2026-06-10-digest.md}
  - {title: "ARA daily digest 2026-05-20", path: research/digest/2026-05-20-digest.md}
  - {title: "ARA daily digest 2026-05-21", path: research/digest/2026-05-21-digest.md}
---

Gemini 3.5 Flash is the fast, low-cost member of Google DeepMind's Gemini 3.5
family, revealed and shipped generally available at **Google I/O 2026
(2026-05-19)**. It launched the same day across the Gemini app, AI Mode in Google
Search (the new global default), the Antigravity coding agent, the Gemini API,
and AI Studio. Google positions it explicitly for **agents, not chatbots** (ARA
digest 2026-05-20). It competes directly with the fast tiers from frontier labs
like [[anthropic]] (Claude Haiku) and OpenAI.

> Note on naming: pre-launch leaks (GCP console, iOS app) labeled this model
> "Gemini 3.2 Flash"; Google branded the public release **3.5**. The ARA model
> ticket keeps its original immutable slug `gemini-3-2-flash` even though the
> product is 3.5 — this wiki page uses the shipped branding.

## Why it matters
- **Speed and economics.** Demis Hassabis claimed it is ~4x faster than
  comparable frontier models (12x and ~800 tok/s inside Antigravity) and "often
  at less than half the cost," beating Gemini 3.1 Pro on coding and agentic tasks
  (ARA digest 2026-05-20). Reported pricing **$1.50 / $9.00 per MTok** (secondary)
  — notably *higher* than the $0.25 / $2.00 the earlier "3.2 Flash" leak quoted,
  so the "cheap Flash" framing weakened on launch.
- **Agentic positioning.** It ranked #1 on Zapier's Automation Bench shortly
  after launch, and Antigravity tripled Gemini rate limits across paid tiers
  after users hit limits fast (ARA digest 2026-05-21) — demand signals that feed
  the broader [[ai-capex]] story.
- **Frontier framing.** Analysts placed the 3.5 family "in the class of GPT-5.5,
  well short of Mythos," using [[anthropic]]'s gated frontier model as the
  high-water mark — a model that has since shipped publicly as
  [[claude-fable-5|Fable 5 / Mythos 5]].
- **Live Translate — same-day counter-programming (2026-06-09).** Google shipped
  **Gemini 3.5 Live Translate**, a real-time **speech-to-speech** translation
  model spanning **70+ languages** (in and out) that begins translating as you
  speak while preserving **tone, pace, and pitch**. Announced by DeepMind product
  lead Logan Kilpatrick / GoogleDeepMind / GoogleAI; live now in the Gemini API,
  AI Studio, and Google Translate, with Google Meet "coming soon." The obvious read
  is timing: it landed the **same day as [[anthropic]]'s
  [[claude-fable-5|Fable 5 / Mythos 5]] launch** — a release engineered to share
  the news cycle (ARA digest 2026-06-10).

## Open questions
- **Pro tier.** Gemini 3.5 Pro was confirmed for "next month" — does it close the
  gap to the gated frontier, or stay a tier below?
- **Cost trajectory.** Does Flash-tier pricing keep drifting up as inference
  demand strains [[neocloud]] and hyperscaler capacity?
- **Default-model leverage.** As the new default for AI Mode in Search, how much
  does forced distribution inflate "adoption" versus genuine preference?
