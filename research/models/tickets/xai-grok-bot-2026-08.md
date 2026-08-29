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

  **2026-08-26/27 — the free-try period converts into subscription
  entitlement, and the usage clock resets.** **@bot**, first-party: "**All
  SuperGrok and Cursor Pro subscribers now have access to Grok Bot. We're
  also resetting weekly usage limits for all users.**" @elonmusk amplified
  it as "Free usage limit reset for Grok @Bot users" (~29K engagement, the
  largest single item in this run's window). @testingcatalog and @mark_k
  both relayed the expansion independently. Note the tier change: the
  2026-08-21 step was **SuperGrok *Plus*, Cursor *Pro+* and Cursor Teams**;
  this one drops to **SuperGrok and Cursor Pro** — a strictly wider,
  cheaper entitlement, which is what makes it a distribution event rather
  than a repeat.

  **Growth claim, from the distribution partner rather than xAI.**
  @mntruell (Cursor): "Grok Bot is now available to everyone with a
  standard Grok or Cursor subscription. **It's grown faster than any
  product we've seen.** It's been particularly exciting to see the range of
  jobs people delegate to Grok Bot, from running small e-commerce
  businesses (including support, advertising, inventory…)." @GavinSBaker,
  who called it a "Claude Code moment" a week earlier: "Cursor has had some
  high growth products before this. **Grok Bot has been transformational
  for me.**"

  **The honest friction, on the record.** @mark_k: "Hearing from lots of
  people that they have **trouble using Grok @Bot with a SuperGrok
  subscription, due to the complex login situation.** I hope @SpaceXAI will
  fix this soon and **unify all of the different X / Grok / Cursor
  accounts**. Would be a shame to lose customers because of it." A fix
  followed the same day for one segment — @romanugarte_: "We've fixed this
  for **X Premium+** subscribers" — leaving the general account-unification
  problem open. So the entitlement widened faster than the identity system
  behind it.

  **Adjacent, still unshipped:** @testingcatalog reports **voice call
  support** for Grok Bot spotted in development ("Soon? 👀") — recorded as
  a UI find, not a release. @mark_k separately logs **Grok Build 1.0.11**
  (configurable default permission mode, auto-approved subagent messages in
  Auto mode, headless sessions in the resume picker, background monitors
  losing their 10-hour timeout), and Cursor **permanently raising included
  usage** for first-party SpaceXAI Grok models again after doubling limits
  last month, attributed to demand following Grok 4.6.

  Verification advances `partial` → `confirmed` is **not** taken: the
  access change is first-party from @bot, but there is still **no docs, no
  spec and no plan-level pricing** after the free-try period, which is what
  the previous cycle said `confirmed` required. It stays `confirmed` where
  it already was for the product's existence.
expected: "Generally available; as of 2026-08-26 access extends to ALL SuperGrok and Cursor Pro subscribers (down from the 2026-08-21 SuperGrok Plus / Cursor Pro+ / Cursor Teams tier) with weekly usage limits reset for everyone, per first-party @bot. Cursor's @mntruell says it has grown faster than any product they have seen. Pending: docs and a spec, plan-level pricing after the free-try period, unification of the X / Grok / Cursor login mess (fixed for X Premium+ only), the promised sharing feature and iPad app, and the voice-call support spotted in development"
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
  - "@mntruell"
  - "@romanugarte_"
  - https://x.com/elonmusk/status/2092691713399931124
created_at: 2026-08-19
updated_at: 2026-08-27
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-19
    change: "Created — Grok Bot (@bot), the SpaceXAI/xAI multi-agent product, is shipped and in wide use. Firsthand third-party assessment from @GavinSBaker (2026-08-17): another Claude Code moment, personal AI usage up ~100x, built a podcast summarizer in ~15 seconds. Shipped-changelog corroboration via @mark_k (2026-08-18): per-Bot grouped mobile notifications, easier phone access to the remote computer, multi-account plugins, improved plugin marketplace, Command-D dictation; plus Grok Build 1.0.6 with breaking subagent-spawning changes. @elonmusk promoted it continuously across the window. Status released; verification partial — no official @SpaceXAI launch post, docs or pricing captured, and Musk's posts are promotion rather than a launch announcement. Known gaps: no sharing feature, no iPad app."
  - ts: 2026-08-23
    change: "Access widens twice in two days, and the official account finally speaks. @bot (relayed by @AndrewCurran_, 2026-08-21 17:34 UTC, ~1,000 RT): 'We're making Grok Bot more widely available. All SuperGrok Plus, Cursor Pro+, and Cursor Teams subscribers now have access.' Roughly seven hours later @grok posted that Grok Bot 'has expanded to more plans and is now free to try' (relayed @ns123abc 2026-08-22 00:04 UTC), with @mark_k confirming 'it's now available for EVERYONE' and a 24-hour free Pro+ month promotion circulating. @elonmusk amplified continuously across the window ('Try Grok @Bot', 'It's that easy to use Grok @Bot', ~7,300 and ~4,800 likes). Product iteration continued: channels inside bot conversations, Discord/Slack style (@mark_k 2026-08-21 17:06 UTC), and @testingcatalog spotting Grok Bot coming to the Grok mobile apps with a hidden nav item for custom agents plus a SuperGrok-to-Heavy upgrade promotion. This closes part of the gap this ticket flagged: an official @bot/@grok post now exists, so verification advances partial -> confirmed. Still missing: docs, a spec, plan-level pricing detail, and the promised sharing feature and iPad app. Status stays released."
  - ts: 2026-08-27
    change: "Access widens again, to a strictly cheaper tier, and the usage clock resets. First-party @bot: 'All SuperGrok and Cursor Pro subscribers now have access to Grok Bot. We're also resetting weekly usage limits for all users.' @elonmusk amplified it as 'Free usage limit reset for Grok @Bot users' at ~29K engagement — the largest single item in this run's window — with @testingcatalog and @mark_k relaying independently. The tier movement is the substance: the 2026-08-21 step was SuperGrok Plus / Cursor Pro+ / Cursor Teams, this one is SuperGrok and Cursor Pro, so it is a genuine widening rather than a restatement. Growth claim comes from the distribution partner rather than xAI — @mntruell (Cursor): 'Grok Bot is now available to everyone with a standard Grok or Cursor subscription. It's grown faster than any product we've seen,' citing delegated jobs including running small e-commerce businesses end to end; @GavinSBaker, who called it a Claude Code moment a week ago, now calls it 'transformational for me'. Friction recorded rather than smoothed: @mark_k reports many SuperGrok subscribers cannot actually use it 'due to the complex login situation' and asks @SpaceXAI to unify the X / Grok / Cursor accounts before it costs customers; @romanugarte_ says the fix landed for X Premium+ subscribers only, so entitlement widened faster than the identity system behind it. Adjacent and NOT shipped: @testingcatalog reports voice-call support spotted in development, recorded as a UI find; @mark_k logs Grok Build 1.0.11 quality-of-life changes (configurable default permission mode, auto-approved subagent messages in Auto mode, headless sessions in the resume picker, background monitors losing the 10-hour timeout), and Cursor permanently raising included usage for first-party SpaceXAI Grok models again after doubling limits last month, attributed to post-Grok-4.6 demand. Status stays released; verification stays confirmed. Docs, spec and plan-level pricing after the free-try period are still missing."
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
