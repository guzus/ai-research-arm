---
slug: google-gemini-4-carbon-2026-10
title: "Google announces Gemini 4 Carbon — new frontier model, #1 on Artificial Analysis v5.0, rolling out first to cyber defenders"
company: "Google / DeepMind"
model: "Gemini 4 Carbon"
status: confirmed
status_note: |
  **First-party announcement, 2026-10-28 ~17:02 UTC**, two weeks after Gemini 4 Argon reached general
  availability. @GoogleDeepMind: "Gemini 4 Carbon is our next frontier model. It's state-of-the-art across
  cybersecurity and long-horizon capabilities." @Google: #1 on v5.0 of the Artificial Analysis Intelligence
  Index; "rolling out starting this week to cyber defenders through our Fairwind Program, with expanded access
  coming soon." @OfficialLoganK and @demishassabis posted the same announcement.

  **Reported numbers (Google's own tests, run without guardrails, via secondary recaps):** AA Index v5.0 score 59;
  SEC-bench Pro 88.2% (vulnerability discovery), ExploitGym 54.8% (exploitation), CWE-bench 71.0% (patching).
  A Polymarket commentator cites a preliminary #1 on LMArena Text at 1,528 Elo; that figure has not been checked.

  **Why `confirmed`, not `released`:** only an initial group of cyber defenders has access. There is no date
  for wider access.
expected: "Cyber-defender (Fairwind Program) rollout began week of 2026-10-26; broader availability 'soon', no date."
labels:
  - frontier-model
  - google-deepmind
  - cybersecurity
  - gated
verification: confirmed
sources:
  - "https://x.com/GoogleDeepMind/status/2115489356437651654"
  - "https://x.com/GoogleDeepMind/status/2115489359415890211"
  - "https://x.com/OfficialLoganK/status/2115489284404940898"
  - "https://x.com/OfficialLoganK/status/2115489576622174620"
  - "https://x.com/demishassabis/status/2115489550256746502"
  - "@Google"
  - "@AINativeF"
created_at: 2026-10-29
updated_at: 2026-10-29
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-29
    change: "Created — CONFIRMED / confirmed. Google DeepMind announced Gemini 4 Carbon (2026-10-28 ~17:02 UTC). It is described as state-of-the-art in cybersecurity and long-horizon tasks (able to 'work through complex tasks for days'), and #1 on the Artificial Analysis Intelligence Index v5.0. It is rolling out first to cyber defenders through the Fairwind Program, with expanded access 'soon'. Benchmark figures (AA 59; SEC-bench Pro 88.2%, ExploitGym 54.8%, CWE-bench 71.0%) come from secondary recaps of Google's post. Successor tier to Gemini 4 Argon ([[google-gemini-4-2026-09]]), which stays a separate ticket."
---
Gemini 4 Carbon is Google's second Gemini 4 model in two weeks. Argon reached general availability on
2026-10-13 ([[google-gemini-4-2026-09]]). Google calls Carbon its "next frontier model". It is a separate
tier above Argon, not a point update, so it gets its own ticket.

The launch is gated, like Anthropic's Mythos preview ([[mythos-public-release]]). The first users are cyber
defenders, and Google says their feedback will shape guardrails "before we expand access". This is the second
frontier lab to release its strongest cyber-capable model to defenders first.

Most of the leaderboard claims come from Google or from recaps of Google's post. A secondary digest
(@clarityware) also says Google's report puts Terminal-Bench cheating at 0.0%. That is noted, not adopted.

**Transition triggers:** general availability in the Gemini app, API or AI Studio → `released`.
