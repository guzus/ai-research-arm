---
slug: openai-gpt-live-1-api-2026-09
title: OpenAI GPT-Live-1 — full-duplex voice model for the API
company: OpenAI
model: GPT-Live-1
status: confirmed
status_note: |
  **2026-10-16 — OpenAI primary: GPT-Live-1.1.** @OpenAI (2026-10-15 18:19 UTC)
  announced GPT-Live-1.1 with new voices, better accents and less "checking...". It is
  rolling out to all users of Voice in ChatGPT, Codex and dots, and is "coming soon to
  the API". This is OpenAI's own handle naming the versioned line, so verification moves
  to `confirmed`. The API price below still comes from secondary relays only.

  **A named API model, not the consumer rollout.** Two independent
  non-English/third-party relays in this window report OpenAI announcing
  **GPT-Live-1** as a new **API** model: full-duplex, robust to background
  noise and interruption, with the front-end model priced at **$0.05 per
  minute** (@ai_wave03, 2026-09-16). A separate daily AI digest independently
  prices it at **$3.00 per API hour** — the same $0.05/min — while comparing it
  to Google's Gemini 3.8 Live at $1.38/hour (@FadyEid, 2026-09-16).

  **Successor to a closed ticket.** [[openai-gpt-live-2026-07]] tracked the
  *consumer* GPT-Live rollout to all ChatGPT users and was closed
  `released-and-aged` on 2026-08-19. A versioned, separately-priced API model
  is a distinct shipping artifact, so it opens here rather than reopening that
  ticket, per the CRUD dedup protocol.

  **Why `confirmed` but `verification: partial`.** Two independent relays agree
  on the name, the full-duplex capability and the exact price, and the price
  arrives through a competitive comparison rather than a press release — the
  shape you get from real published pricing. But no OpenAI post, model card or
  docs page was captured in-window, so the primary is missing.
expected: "GPT-Live-1.1 rolled out to ChatGPT/Codex/dots voice on 2026-10-15; API availability 'coming soon'. API price ($0.05/min front-end, $3.00/API-hour) still rests on secondary relays. Open: an OpenAI pricing page or API docs entry for GPT-Live-1.1."
labels:
  - openai
  - voice
  - realtime
  - api
  - pricing
verification: confirmed
sources:
  - https://x.com/ai_wave03/status/2100190209514123581
  - https://x.com/FadyEid/status/2100184052338667874
  - "https://x.com/OpenAI/status/2110797830361436604"
created_at: 2026-09-16
updated_at: 2026-10-16
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-16
    change: "Created — CONFIRMED / partial. OpenAI announced GPT-Live-1, a full-duplex voice model for the API, described as resistant to background noise and interruption with natural conversation, front-end model priced at 5 cents per minute (@ai_wave03 2026-09-16 11:49 UTC). Independently corroborated by a daily AI news digest the same morning, which prices it at $3.00 per API hour — arithmetically the same $0.05/min — in a direct comparison against Google's Gemini 3.8 Live at $1.38/hour (@FadyEid 2026-09-16 11:24 UTC). Two independent relays agreeing on name, capability and exact price, with the price surfacing through competitive comparison rather than promotion, so status is confirmed; no OpenAI primary post, model card or pricing page was captured in-window, so verification stays partial. Opened as a SUCCESSOR to the closed [[openai-gpt-live-2026-07]] (the consumer full-duplex rollout, closed released-and-aged 2026-08-19) rather than reopening it: a versioned, separately-priced API model is a distinct shipping artifact. Direct competitive counterpart is [[google-gemini-3-8-live-2026-09]], which shipped the previous day at roughly half the hourly cost."
  - ts: 2026-10-16
    change: "Confirmed, unchanged; verification partial -> confirmed. The model line now has an OpenAI primary. @OpenAI (2026-10-15 18:19 UTC) announced GPT-Live-1.1: new voices, better accents and less 'checking...' latency, with new voices in French, German, Hindi, Mexican Spanish, Korean and Japanese. It is rolling out that day to all users of Voice in ChatGPT, Codex and dots, and is 'coming soon to the API'. OpenAI naming a .1 point release confirms the GPT-Live-1 versioned line this ticket opened on. The 2026-09-16 API price ($0.05/min front-end, $3.00/API-hour) still rests on the two secondary relays only; OpenAI's post gives no price. Status stays confirmed: the ticket tracks the API model, and the 1.1 API is announced as 'coming soon', not shipped. The consumer rollout of 1.1 is logged here rather than on the closed [[openai-gpt-live-2026-07]], which stays untouched."
---

**GPT-Live-1** is the API-productized form of the full-duplex voice
architecture OpenAI rolled out to consumers in July
([[openai-gpt-live-2026-07]], closed). The rollout gave everyone the
capability; this gives developers a version number and a price.

**The price is the whole story.** $0.05/min for the front-end model works out
to $3.00 per API hour. Google announced Gemini 3.8 Live the day before at
$1.38 per API hour ([[google-gemini-3-8-live-2026-09]]) and a third party did
the comparison arithmetic publicly within hours. Whatever else these two
launches are, they are a voice-API price fight opening at roughly 2:1.

**Read "front-end model" carefully.** The phrase implies a tiering — a
cheap front-end handling the duplex audio loop with something larger behind
it — which would mean $3.00/hour is a floor, not the cost of a working voice
agent. Nothing captured in-window specifies what sits behind it. Do not quote
$3.00/hour as the price of the product.

**Why this is not a rumor.** Two accounts with no relationship to each other
— a Japanese AI-news account and an English daily digest — independently
reported the same name, the same capability description and the same number,
and one of them used it inside a comparison table that also contained
correctly-stated Google pricing. That is consistent with published pricing,
not with a leak. It is still not an OpenAI source, which is why
`verification` is `partial` and stays there until a model card or docs page
is captured.

**Transition triggers:**
- An OpenAI primary (post, model card, pricing page, or API docs entry) →
  UPDATE, advance `verification` to `confirmed`.
- General availability, or the full tier structure behind "front-end model" →
  UPDATE, advance `status` to `released`.
- A price change on either side of the Google comparison → UPDATE.
- ≥15 cycles with no corroboration and no primary → reconsider.

**Dedup note:** the 2026-07 consumer rollout stays on the closed
[[openai-gpt-live-2026-07]] — do not modify it. ChatGPT voice *pricing and
limit* changes in the desktop app (the ~60% voice price cut in Codex and Work
announced 2026-09-14) belong to the ChatGPT product surface, not to this
model. Google's competing model is [[google-gemini-3-8-live-2026-09]].

**2026-10-16 — the line gets a primary.** OpenAI's own post names GPT-Live-1.1
and ships it to every ChatGPT voice user. That settles that GPT-Live-1 is a
versioned OpenAI model line, which is what this ticket was waiting for. The API leg
is still "coming soon". When the 1.1 API appears with a price, this ticket moves
to `released`.
