---
slug: openai-us-govt-stake-2026-06
title: OpenAI–US government equity-stake talks ("Public Wealth Fund")
company: OpenAI / US Government
model: null
status: confirmed
status_note: |
  Multi-outlet reporting (NOTUS, TechCrunch, The Decoder, 2026-06-06) plus
  Trump's own on-record remarks say the **Trump administration is negotiating a
  direct US-government equity position in OpenAI**, reportedly structured
  through a **"Public Wealth Fund"** that would pay out to American citizens.
  Sam Altman is said to have first pitched the administration on the stake;
  Trump publicly floated structuring deals "where the American people can
  benefit from the success of AI." These are **talks, not a closed deal** — no
  signed term sheet, no disclosed stake size, valuation, or instrument, and no
  on-record OpenAI/White House confirmation of terms. The status tracks the
  *negotiation* (multi-source + Trump on-record → confirmed event); the *deal*
  itself remains unconsummated.
expected: "TBD — talks ongoing; no announced structure, stake size, or close date"
labels:
  - openai
  - us-government
  - equity-stake
  - policy
  - funding
verification: partial
sources:
  - https://techcrunch.com/2026/06/06/the-trump-administration-might-take-an-equity-stake-in-openai/
  - https://the-decoder.com/openai-and-the-trump-administration-are-negotiating-a-government-stake-in-the-ai-startup/
  - "@mswnlz"
  - "@Sharity"
created_at: 2026-06-07
updated_at: 2026-06-09
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-07
    change: "Created — Trump administration reportedly negotiating a direct US-government equity stake in OpenAI via a 'Public Wealth Fund' paying out to citizens; Altman said to have pitched it, Trump publicly floated deals 'where the American people can benefit' (NOTUS/TechCrunch 2026-06-06; The Decoder 2026-06-06). Talks only — no signed terms, stake size, or instrument; no on-record OpenAI/WH confirmation → confirmed (the negotiation is multi-source + Trump on-record) / partial (no closed deal)"
  - ts: 2026-06-09
    change: "Scope + structure detail. Per the curated cycle, **Trump confirmed (2026-06-05) the federal government may take 'pieces' of both OpenAI AND xAI** via the OpenAI-pitched 'Public Wealth Fund', with the equity **donated, not sold**. A competing, far more aggressive line emerged: **Sen. Bernie Sanders is pushing a bill for a 50% government stake plus a 50% tax**. **Anthropic is reportedly excluded** from the equity talks. Status stays confirmed (multi-source + Trump on-record) / partial (still no signed terms, stake size, or instrument; framing remains directional)"
---

Per **NOTUS, TechCrunch, and The Decoder** (2026-06-06), the **Trump
administration is negotiating a direct US-government equity position in
OpenAI**, reportedly structured through a **"Public Wealth Fund"** that would
distribute returns to American citizens. Sam Altman is said to have first
pitched the administration on the stake; President Trump publicly tied it to
structuring deals **"where the American people can benefit from the success of
AI."**

**Why `confirmed` event but `partial` verification.** The *negotiation* is
corroborated across multiple independent outlets and anchored to Trump's own
on-record comment, which clears the multi-source bar for a confirmed event.
But it remains **reporting on talks**: every account hedges with
"discussing / considering / might," no **stake percentage, valuation, or
instrument** has been disclosed, and **neither OpenAI nor the White House has
confirmed terms on record**. Treat the framing as directional, not final.

**Why this matters now.** It lands alongside two related threads this cycle:
the **[whitehouse-krishnan-exit-2026-06](./whitehouse-krishnan-exit-2026-06.md)**
departure (a policy-leadership gap opening as an unprecedented government
position in a frontier lab is negotiated) and the
**[openai-chatgpt-superapp-2026-06](./openai-chatgpt-superapp-2026-06.md)** FT
report on OpenAI recasting ChatGPT for an IPO — both point to OpenAI
positioning for a public listing.

**Transition triggers:**
- On-record OpenAI or White House confirmation of a stake size / mechanism →
  UPDATE, advance verification.
- A signed agreement or formal announcement → UPDATE (status stays confirmed;
  note the closed terms).
- Talks collapse or are denied on record → `closed` with the appropriate
  reason.

**Dedup note:** further US-government-stake / Public Wealth Fund signal UPDATES
this ticket. OpenAI's IPO/super-app product roadmap stays on
[[openai-chatgpt-superapp-2026-06]].
