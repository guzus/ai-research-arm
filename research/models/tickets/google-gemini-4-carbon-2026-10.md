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

  **2026-10-30/31 — first third-party agentic leaderboard.** @mercor (RT'd by @demishassabis): Carbon debuts
  #1 on APEX-Agents at 84.2% Pass@1 / 90.4% mean, ahead of Gemini 4 Argon (82.4% / 87.4%) and Claude Sonnet 5.5
  (75.5% / 83.7%); #1 in consulting and banking, #2 in corporate law, where Argon leads.
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
  - https://x.com/DailyAiDriver/status/2116155432494571739
  - https://x.com/AlyBlak3/status/2116156713137287406
  - https://x.com/mercor/status/2116226723968872959
  - https://x.com/demishassabis/status/2116452833167814692
  - https://x.com/linktulu/status/2116885735684944155
created_at: 2026-10-29
updated_at: 2026-11-01
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-29
    change: "Created — CONFIRMED / confirmed. Google DeepMind announced Gemini 4 Carbon (2026-10-28 ~17:02 UTC). It is described as state-of-the-art in cybersecurity and long-horizon tasks (able to 'work through complex tasks for days'), and #1 on the Artificial Analysis Intelligence Index v5.0. It is rolling out first to cyber defenders through the Fairwind Program, with expanded access 'soon'. Benchmark figures (AA 59; SEC-bench Pro 88.2%, ExploitGym 54.8%, CWE-bench 71.0%) come from secondary recaps of Google's post. Successor tier to Gemini 4 Argon ([[google-gemini-4-2026-09]]), which stays a separate ticket."
  - ts: 2026-10-30
    change: "Confirmed, unchanged — access still gated. Secondary relays on 2026-10-30 frame Carbon against Anthropic: @DailyAiDriver puts it at 59 vs Claude Opus 5.5's 58 on the Artificial Analysis overall index, with Claude still leading some individual tests. The 59 matches the figure already recorded. @buildjayy restates the defenders-first rollout, and @AlyBlak3 says a broader release is promised but undated. @RyanYanBuilds' evidence review agrees that Carbon is officially announced with limited initial access. No general availability, pricing or API listing captured. Rumours of models beyond Carbon (Xenon, Hydrogen / Gemini 4 Flash) are tracked separately at [[google-gemini-4-xenon-2026-10]] and [[google-gemini-4-flash-hydrogen-2026-10]]."
  - ts: 2026-10-31
    change: "Confirmed, unchanged — first third-party agentic leaderboard, access still gated. @mercor (2026-10-30 17:52 UTC, retweeted by @demishassabis 2026-10-31 08:50 UTC) puts Carbon #1 on APEX-Agents (multi-step investment-banking, consulting and corporate-law tasks) at 84.2% Pass@1 and 90.4% mean, the only model above a 90% mean, ahead of Gemini 4 Argon (82.4% / 87.4%) and Claude Sonnet 5.5 (75.5% / 83.7%). By domain: consulting 91.9% (#1), banking 86.9% (#1), corporate law 73.8% (#2, behind Argon at 76.7%). Relays also report Elon Musk replying 'Impressive' to Pichai's announcement (@binujayaraj; not checked). No general availability, pricing or API listing yet; secondary recaps (@techtrends_zm, @AIDiscoveryDesk) still describe a defenders-first rollout."
  - ts: 2026-11-01
    change: "Confirmed, unchanged — first pricing captured, access still gated. @linktulu (2026-11-01 13:31 UTC, citing Google's 2026-10-28 Carbon post) reports intro API pricing equal to Argon's, $2 / $10 per 1M input/output tokens with cached input 95% off, rising to $4 / $20 after the intro period (no end date given). The same post repeats the AA v5.0 score of 59 and the cyber benchmarks already recorded, and says broader developer, business and consumer access is 'as soon as possible', not open today. Secondary relay; the price has not been checked against a Google pricing page. @ricklamers (2026-11-01) complains publicly about Google announcing SOTA models that outsiders cannot use, which matches the gated rollout."
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
