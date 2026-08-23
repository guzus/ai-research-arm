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
expected: "Generally available and free to try as of 2026-08-21/22, after expanding to SuperGrok Plus, Cursor Pro+ and Cursor Teams and then to everyone; official @bot / @grok posts now exist. Pending: docs and a spec, plan-level pricing detail after the free-try period, Grok mobile-app availability, and the promised sharing feature and iPad app"
labels:
  - xai
  - spacex
  - agentic
  - developer-tooling
  - released
verification: confirmed
sources:
  - "@GavinSBaker"
  - "@elonmusk"
  - "@mark_k"
  - "@iruletheworldmo"
  - "@doodlestein"
  - "@bot"
  - "@grok"
  - "@testingcatalog"
  - "@ns123abc"
  - "@AndrewCurran_"
created_at: 2026-08-19
updated_at: 2026-08-23
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-19
    change: "Created — Grok Bot (@bot), the SpaceXAI/xAI multi-agent product, is shipped and in wide use. Firsthand third-party assessment from @GavinSBaker (2026-08-17): another Claude Code moment, personal AI usage up ~100x, built a podcast summarizer in ~15 seconds. Shipped-changelog corroboration via @mark_k (2026-08-18): per-Bot grouped mobile notifications, easier phone access to the remote computer, multi-account plugins, improved plugin marketplace, Command-D dictation; plus Grok Build 1.0.6 with breaking subagent-spawning changes. @elonmusk promoted it continuously across the window. Status released; verification partial — no official @SpaceXAI launch post, docs or pricing captured, and Musk's posts are promotion rather than a launch announcement. Known gaps: no sharing feature, no iPad app."
  - ts: 2026-08-23
    change: "Access widens twice in two days, and the official account finally speaks. @bot (relayed by @AndrewCurran_, 2026-08-21 17:34 UTC, ~1,000 RT): 'We're making Grok Bot more widely available. All SuperGrok Plus, Cursor Pro+, and Cursor Teams subscribers now have access.' Roughly seven hours later @grok posted that Grok Bot 'has expanded to more plans and is now free to try' (relayed @ns123abc 2026-08-22 00:04 UTC), with @mark_k confirming 'it's now available for EVERYONE' and a 24-hour free Pro+ month promotion circulating. @elonmusk amplified continuously across the window ('Try Grok @Bot', 'It's that easy to use Grok @Bot', ~7,300 and ~4,800 likes). Product iteration continued: channels inside bot conversations, Discord/Slack style (@mark_k 2026-08-21 17:06 UTC), and @testingcatalog spotting Grok Bot coming to the Grok mobile apps with a hidden nav item for custom agents plus a SuperGrok-to-Heavy upgrade promotion. This closes part of the gap this ticket flagged: an official @bot/@grok post now exists, so verification advances partial -> confirmed. Still missing: docs, a spec, plan-level pricing detail, and the promised sharing feature and iPad app. Status stays released."
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
