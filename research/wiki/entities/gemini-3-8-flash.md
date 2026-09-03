---
slug: gemini-3-8-flash
title: Gemini 3.8 Flash
type: entity
aliases: ["Gemini 3.8 Flash", "Gemini 3.8 Flash Cyber", "3.8 Flash Cyber"]
tags: [model-release, google-deepmind, flash-tier, ai-security]
description: Google's third Flash SKU in six weeks, shipped 2026-09-03 at the same $0.75/$3.75 intro price as 3.7 through year-end, plus a gated 3.8 Flash Cyber defender model via Fairwind.
created_at: 2026-09-03
timestamp: 2026-09-03T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-09-03", path: research/digest/2026-09-03-digest.md}
---

**Gemini 3.8 Flash** is [[google]]'s third Flash-tier SKU in six weeks,
following [[gemini-3-7-flash]] (2026-08-13) and [[gemini-3-6-flash]]
(2026-07-21). It is live in the Gemini API, AI Studio, Antigravity, the
Pro/Ultra app, Search AI Mode, and Sheets. A separate **3.8 Flash Cyber**
SKU is gated behind Google's Fairwind defender program and is **not** on
the public Gemini API — a new Daybreak-shaped specialist, not an upgrade
of the July [[gemini-3-6-flash|3.5 Flash Cyber]].

## Why it matters

- **Same intro price as 3.7, then a 2× step-up.** List is **$0.75 / $3.75
  per million tokens through 2026-12-31**, matching 3.7's intro card; after
  that date it becomes **$1.50 / $7.50**. The cadence is the story: Google
  is iterating the cheap workhorse every two weeks while
  [[gemini-3-5-pro]] stays delayed (Google, The Verge, Ars Technica; ARA
  daily digest 2026-09-03).
- **Vendor coding scores sit next to [[claude-opus-5|Opus 5]]; the
  terminal gap does not.** Google's table puts DeepSWE 1.1 at **73.7%**,
  near Opus 5's **74.0%**, and reports HLE-Verified **54.9%**,
  Terminal-Bench 2.1 **89.4%**, and Vals Finance Agent v2 **61.4%**.
  Terminal-Bench 4.0 stays at **19.1% versus 51.8%** for Opus 5. Treat the
  first set as first-party until independently reproduced (Google; ARA
  daily digest 2026-09-03).
- **Artificial Analysis scores Intelligence Index 59 at about $0.58/task.**
  That is cheaper in-band than peers, but **~40% more expensive per task
  than 3.7** because 3.8 burns **~30% more output tokens**. The cheap
  sticker price is not the cheap task price (Artificial Analysis, The
  Decoder; ARA daily digest 2026-09-03).
- **3.8 Flash Cyber is a gated defender model.** Fairwind has **~650
  members**, including CrowdStrike and the Center for Internet Security
  in the local AI-news report. The blog cites CyberGym "frontier-level"
  scores, Chrome Security **2.6× more correct patches**, and Wiz recall
  gains at **2.3–5.2× lower cost**. It is Google's answer the day after
  [[openai]] marked [[astra]] Critical-cyber; it is not a public Flash
  upgrade. See [[agentic-ai-security]] and the earlier
  [[gemini-3-6-flash|Flash Cyber]] SKU (Google DeepMind; ARA daily digest
  2026-09-03).
- **FrontierSWE v2 does not include it.** Proximal's 34-task, 20-hour
  coding bench put [[claude-fable-5|Claude Fable 5.1]] at **56.3% mean@5**
  versus **32.2%** for [[gpt-5-6|GPT-5.6]]; Gemini 3.8 Flash and
  [[muse-code|Muse Spark 1.3]] are not on the board (Proximal; ARA daily
  digest 2026-09-03).
- **Hacker News' runaway thread** on 3.8 Flash and 3.8 Flash Cyber held
  **748 points / 449 comments** by 22:40 UTC (ARA daily digest
  2026-09-03).

## Open questions

- **Does the DeepSWE 73.7% / Terminal-Bench 2.1 89.4% card hold** once
  harness configuration is matched to Opus 5? The Terminal-Bench 4.0 gap
  already argues the vendor table is not a general coding lead.
- **Is Fairwind a durable access model** for a more-permissive cyber SKU,
  or a temporary holding pen until a public Daybreak equivalent ships?
- **Does the ~30% extra output-token burn persist**, or is it a launch
  serving artifact that a later 3.8 cut walks back?
