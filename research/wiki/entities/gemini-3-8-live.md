---
slug: gemini-3-8-live
title: Gemini 3.8 Live
type: entity
aliases: ["Gemini 3.8 Live", "Gemini 3.8 Live Extended Thinking", "3.8 Live Extended Thinking"]
tags: [model-release, google-deepmind, speech-to-speech, live-dialogue]
description: Google's live-dialogue pair in public preview; 3.8 Live takes the Artificial Analysis speech-to-speech lead at 82.6 and about $0.84/hour, roughly 80% cheaper than OpenAI's GPT-Live 1.
created_at: 2026-09-16
timestamp: 2026-09-16T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-09-16", path: research/digest/2026-09-16-digest.md}
---

**Gemini 3.8 Live** is [[google]]'s live-dialogue pair, now in public
preview in the Gemini API and AI Studio. It is a speech-to-speech SKU,
not an upgrade of [[gemini-3-8-flash|3.8 Flash]]. The pair is **3.8 Live**
(scale, cost, visual grounding) and **3.8 Live Extended Thinking**
(multi-step work with early verbal cues and live progress narration while
tool calls run async). Audio is SynthID-watermarked. Live goes to Search;
Extended Thinking goes to the Gemini app plus Docs, Gmail and Keep for
subscribers.

## Why it matters

- **Price, not the narrow quality lead, is the durable fact.** Google
  claims **#1 on the Artificial Analysis speech-to-speech index at 82.6**
  and **35.1 on τ-Voice banking**, at **$0.005/min input and $0.018/min
  output** — about **$0.84 per hour**, taking the slot from [[openai]]'s
  GPT-Live 1 at roughly **80% lower measured cost**. 3.8 Live is also
  reported **#2 on Speech Agent Arena**. Extended Thinking posts **68.6%
  τ-Voice** and **97.7% Big Bench Audio**. Treat the vendor benches as
  first-party until independently reproduced; the cost gap is the
  harder number (Google blog, The Decoder, Hacker News 230 pts; ARA
  daily digest 2026-09-16).
- **The product surface is mid-conversation, not chat.** Google cites
  **97-language mid-sentence switching**, background thinking, async
  tool calls, and visual grounding. Simon Willison published an
  interruptible WebSocket browser UI built from the docs with no
  libraries — a same-day developer receipt that the API is usable
  without a SDK (Google, Simon Willison; ARA daily digest 2026-09-16).
- **It is a sibling of 3.8 Flash, not a rename.** [[gemini-3-8-flash]]
  shipped 2026-09-03 as the cheap text/agent workhorse. Live is the
  speech stack. Do not fold the two SKUs.

## Open questions

- **Does the 80% cost gap survive once GPT-Live 1 is measured on the
  same hour-long workload**, or is it a list-price comparison?
- **How much of the AA 82.6 lead is Extended Thinking versus the
  cheaper Live SKU?** Google's table mixes the pair.
