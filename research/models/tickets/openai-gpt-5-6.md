---
slug: openai-gpt-5-6
title: OpenAI GPT-5.6 — anticipated frontier release
company: OpenAI
model: GPT-5.6
status: rumored
status_note: |
  GPT-5.6 is the most-watched unreleased OpenAI model, expected **alongside the
  ChatGPT "super app" overhaul** ([[openai-chatgpt-superapp-2026-06]]). Signal is
  anticipation, not artifact: Andrew Curran flagged a "next week" window;
  **prediction markets price a by-2026-06-30 release at ~89%**; and multiple
  developers independently hit **"Model not found: gpt-5.5" 404s inside Codex** —
  a *weak* backend tell equally consistent with a routing hiccup, and about 5.5
  rather than 5.6. **No OpenAI on-record date, no public artifact, no benchmarks.**
expected: "Prediction markets ~89% by 2026-06-30; no OpenAI-confirmed date"
labels:
  - openai
  - frontier-model
  - upcoming
  - rumor
verification: partial
sources:
  - "@AndrewCurran_"
  - "@Polymarket"
created_at: 2026-06-09
updated_at: 2026-06-09
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-09
    change: "Created — GPT-5.6 anticipated alongside OpenAI's ChatGPT 'super app' overhaul ([[openai-chatgpt-superapp-2026-06]]). Andrew Curran flagged a 'next week' window; prediction markets price a by-2026-06-30 release ~89%; multiple devs hit 'gpt-5.5' 404s in Codex (weak tell, and about 5.5 not 5.6). No OpenAI on-record date, no artifact, no benchmarks → status rumored, verification partial (multiple secondary corroborations, no primary)"
---

**GPT-5.6** is OpenAI's most-anticipated unreleased frontier model, widely
expected to land **alongside the "super app" ChatGPT overhaul**
([[openai-chatgpt-superapp-2026-06]]). As of this cycle the signal is
**anticipation rather than a shipping artifact**.

**What there is:** Andrew Curran flagged a **"next week"** window;
**prediction markets price a by-2026-06-30 release at ~89%**; and several
developers independently reported **"Model not found: gpt-5.5" 404s inside
Codex**. The 404s are a *weak* rollout tell — equally consistent with a backend
hiccup, and they reference **gpt-5.5**, not 5.6.

**What there isn't:** no OpenAI on-record date, no public artifact, no
benchmarks, no pricing. That maps cleanly to `rumored`. `verification` is
`partial` (not `unverified`) only because the expectation is corroborated by
**multiple independent secondary signals** (a credible reporter + prediction
markets + multi-dev 404 reports), none of them primary.

**Transition triggers:**
- A console/API artifact, leaked spec, or private preview of GPT-5.6 → `in-testing`.
- An OpenAI on-record announcement → `confirmed`.
- Public rollout (API / ChatGPT) → `released`.
- ≥15 cycles with the window lapsed and no fresh corroboration → `closed: stale-rumor-unverified`.

**Dedup note:** GPT-5.6 model signal (artifacts, benchmarks, launch) UPDATES
this ticket. The ChatGPT product overhaul stays on
[[openai-chatgpt-superapp-2026-06]]; the Codex platform stays on its own ticket.
