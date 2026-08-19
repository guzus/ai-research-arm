---
slug: xai-grok-bot-2026-08
title: Grok Bot — xAI/SpaceXAI multi-agent product in wide use
company: SpaceX / xAI
model: Grok (Grok Bot harness)
status: released
status_note: |
  **Grok Bot** (@bot) is shipping and in heavy use. The clearest
  third-party read in-window is @GavinSBaker (2026-08-17, ~6,800
  engagement): "I think @bot is another 'Claude Code' moment for AI. I
  would estimate my personal AI usage is up something like 100x… it took me
  about 15 seconds in Grok Bot and is better than what I had before."

  **Shipped-changelog evidence**, not just enthusiasm: @mark_k lists
  quality-of-life improvements shipped by **@SpaceXAI** on 2026-08-18 —
  mobile notifications grouped by Bot with per-Bot icons, easier direct use
  of the remote computer from a phone, multiple accounts on the same
  plugin, an improved plugins marketplace, and Command-D voice dictation.
  Separately **Grok Build 1.0.6** shipped with breaking changes (subagent
  spawning no longer accepts `capability_mode`; tool access is now
  controlled only by agent type).

  **Elon Musk is promoting it directly and continuously** across the window
  ("Clear your email with @Grok @Bot", "What's ur @Bots?", plus repeated
  amplification of user testimonials). As xAI/SpaceX's principal, that is
  primary-adjacent — but it is promotion, not a launch post or
  documentation, and no official @SpaceXAI launch announcement or spec was
  captured. Hence `verification: partial`.

  Known gaps, from users: **no sharing feature and no iPad app** (both said
  to be coming), per @GavinSBaker.
expected: "Shipping and in general use as of 2026-08-19, with active weekly iteration (Grok Build 1.0.6, plugin marketplace, mobile). Pending: a captured official xAI/SpaceXAI launch post or docs, pricing/plan detail, and the promised sharing feature and iPad app"
labels:
  - xai
  - spacex
  - agentic
  - developer-tooling
  - released
verification: partial
sources:
  - "@GavinSBaker"
  - "@elonmusk"
  - "@mark_k"
  - "@iruletheworldmo"
  - "@doodlestein"
created_at: 2026-08-19
updated_at: 2026-08-19
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-19
    change: "Created — Grok Bot (@bot), the SpaceXAI/xAI multi-agent product, is shipped and in wide use. Firsthand third-party assessment from @GavinSBaker (2026-08-17): another Claude Code moment, personal AI usage up ~100x, built a podcast summarizer in ~15 seconds. Shipped-changelog corroboration via @mark_k (2026-08-18): per-Bot grouped mobile notifications, easier phone access to the remote computer, multi-account plugins, improved plugin marketplace, Command-D dictation; plus Grok Build 1.0.6 with breaking subagent-spawning changes. @elonmusk promoted it continuously across the window. Status released; verification partial — no official @SpaceXAI launch post, docs or pricing captured, and Musk's posts are promotion rather than a launch announcement. Known gaps: no sharing feature, no iPad app."
---

**Grok Bot** is xAI/SpaceXAI's multi-agent product — you run a main agent,
it spawns more agents, and they operate a remote computer and plugins on
your behalf. In the 2026-08-17→19 window it was one of the most-discussed
products on the platform.

**The assessment worth taking seriously** comes from @GavinSBaker, who has
no obvious reason to shill xAI and who anchored it against a known
reference point: "another 'Claude Code' moment for AI," with personal AI
usage up "something like 100x," and a concrete task (a podcast summarizer)
done in ~15 seconds and better than what he had. @iruletheworldmo's
description gets at the same thing from the UX side: "you start your main
agent, the agent spins up more agents, and they proactively start to unlock
digital tasks you may never have thought of before."

**Why `released` and not `rumored`.** There is a shipped changelog. @mark_k
enumerated concrete QoL changes SpaceXAI shipped on 2026-08-18 — grouped
per-Bot mobile notifications, phone access to the remote computer,
multi-account plugin connections, a better plugin marketplace, Command-D
dictation — and **Grok Build 1.0.6** shipped with a *breaking* API change
(subagent spawning dropped `capability_mode`; tool access is now governed
by agent type). Weekly breaking changes to a spawning API are the signature
of a live product with real users, not a demo.

**Why `verification: partial`.** Elon Musk promoted it relentlessly in the
window, and as xAI/SpaceX's principal his posts are primary-adjacent — but
"Clear your email with @Grok @Bot" is marketing, not a launch announcement.
No official @SpaceXAI launch post, documentation, spec or pricing was
captured, and the usage claims are anecdotes rather than measurements.

**Bear case, on the record.** @farzyness predicts Grok Bot will generate
"massive revenue for SpaceX" quickly; nothing supports that yet beyond
sentiment. Users report the product still lacks a **sharing feature** and
an **iPad app**. And Grok Bot's tailwind is partly other vendors' capacity
squeeze — several in-window testimonials are from people who exhausted
Codex or Claude limits first, which is switching driven by rationing rather
than by preference.

**Transition triggers:**
- Official xAI/SpaceXAI launch post, docs or pricing → UPDATE, advance
  `verification` to `confirmed`.
- Sharing feature or iPad app ships → UPDATE.
- Usage or revenue disclosed → UPDATE.
- ≥4 weeks with the product settled into normal coverage →
  `closed: released-and-aged`.

**Dedup note:** the underlying next-gen model stays on
[[xai-grok-2t-spacex-data-2026-07]]; the earlier Grok Build CLI launch is
closed at [[xai-grok-build-2026-05]]. Further Grok Bot product signal
UPDATES this ticket.
