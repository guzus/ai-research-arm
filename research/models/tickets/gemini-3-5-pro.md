---
slug: gemini-3-5-pro
title: Gemini 3.5 Pro — Google I/O 2026 follow-on
company: Google / DeepMind
model: Gemini 3.5 Pro
status: confirmed
status_note: |
  Officially confirmed at Google I/O 2026 (2026-05-19) as "coming next
  month," announced alongside the Gemini 3.5 Flash GA as the Pro tier of
  the new 3.5 family. Reported to already be in internal use at Google.
  No public artifact or API yet. **2026-06-16:** a **"Coming Soon" tag
  reportedly surfaced on the Gemini Pro model card** within the promised
  June window — a weak placeholder/launch tell, not a usable artifact —
  with commentary noting the upcoming model has seen *surprisingly zero
  leaks* (a contrast to 3.5 Flash / 3.1 Pro's active pre-launch rumor
  cycles). Single low-credibility social source; the June commitment is now
  mid-to-late month with still no 3.5 Pro GA/API/pricing.

  **2026-07-04:** A single AI-leak account (@synthwavedd, near-verbatim
  relayed by @whoisanku) claims Google DeepMind **scrapped reusing the old
  2.5 Pro base and reset Gemini 3.5 Pro to a full pretrain**, pushing the
  target to a new, previously-unreported **July 17** date, with a follow-on
  Nano Banana Pro model said to be in progress on the new base. Single-source
  (the @whoisanku relay is not an independent second source); a Polymarket
  market cited by a third account gives ~48% odds on the July 17 date — a
  pricing signal, not corroboration. No Google/DeepMind on-record statement.
  Status stays confirmed (the model's existence was confirmed at I/O);
  verification stays confirmed; the full-retrain/July 17 claim itself is
  flagged unverified pending independent corroboration.
labels:
  - google-io
  - pro-tier
  - frontier-model
  - upcoming
verification: confirmed
sources:
  - "@GoogleDeepMind"
  - "@demishassabis"
created_at: 2026-05-20
updated_at: 2026-07-04
closed_at: null
closed_reason: null
history:
  - ts: 2026-05-20
    change: "Created — Google confirmed at I/O 2026 (official @GoogleDeepMind) that Gemini 3.5 Pro ships next month, the Pro tier of the 3.5 family unveiled with 3.5 Flash; reported in internal use already"
  - ts: 2026-06-08
    change: "Launch-imminence chatter inside the promised June window (the 'next month' commitment is now in-month). Gemini API lead @OfficialLoganK posted a 'bullish on Gemini' teaser (2026-06-08 03:06 UTC, ~1,069 likes / 219 replies), widely read as a pre-launch tell; @haider1 follows (2026-06-08 07:25 UTC, ~30 likes) with 'Gemini 3.5 Pro is probably close to launch,' wishing for better planning/orchestration and codebase tool-use. Semi-primary teaser + community read — still **no public artifact, API, or pricing**, so status stays confirmed (not yet in-testing); verification confirmed"
  - ts: 2026-06-09
    change: "Ecosystem signal inside the promised June window, but still no standalone 3.5 Pro GA. (1) At **WWDC 2026 (2026-06-08)** Apple confirmed **Siri AI's Tier-3 heavy-reasoning runs on a custom ~1.2T-parameter Google Gemini on Nvidia B200s via Google Cloud** ([[apple-wwdc-2026-siri]]) — the highest-profile production Gemini deployment yet, though Apple did not name '3.5 Pro' specifically. (2) Google upgraded **NotebookLM to Gemini 3.5** (with a cloud computer + Antigravity integration). The 'next month' (June) commitment is now mid-month with **3.5 Flash still the only public 3.5 model** and no 3.5 Pro artifact/API/pricing — status stays confirmed, verification confirmed"
  - ts: 2026-06-16
    change: "Launch-imminence tell inside the June window: a 'Coming Soon' tag reportedly appeared on the Gemini Pro model card (single low-credibility social source, @just_v3ra), with commentary noting the upcoming model has seen surprisingly zero leaks — a contrast to the active pre-launch rumor cycles 3.5 Flash and 3.1 Pro had. A placeholder tag is not a usable console/API artifact, so status stays confirmed (not in-testing); the June commitment is now mid-to-late month with 3.5 Flash still the only public 3.5 model. Verification stays confirmed (the I/O commitment is primary; today's tag is secondary)."
  - ts: 2026-07-04
    change: "Single-leaker claim: Google DeepMind scrapped reusing the 2.5 Pro base and reset Gemini 3.5 Pro to a full pretrain, pushing the target to a new July 17 date (previously unreported); a follow-on Nano Banana Pro said to be in progress on the new base. Single-source (@synthwavedd, near-verbatim @whoisanku relay is not independent); a cited Polymarket market gives ~48% odds on July 17 — a pricing signal, not corroboration. No Google/DeepMind on-record statement. Status stays confirmed; verification stays confirmed; the retrain/July 17 claim itself flagged unverified."
---

At Google I/O 2026, Google revealed the **Gemini 3.5** family. The first
release was [Gemini 3.5 Flash](./gemini-3-2-flash.md) (GA the same day);
the Pro tier was confirmed in the same announcement thread:
"This is just the start — Gemini 3.5 Pro is coming next month"
(official @GoogleDeepMind).

This ticket tracks the Pro tier specifically. As of the I/O reveal there
is no public artifact, pricing, or API for 3.5 Pro — only Google's
on-record commitment to a next-month (≈June 2026) release, plus
secondary reports that it is already in internal use.

**Transition triggers:**
- A console/API artifact, private preview, or leaked spec appears →
  `status: in-testing`.
- Public rollout (Gemini app / AI Studio / Vertex AI / Gemini API) →
  `status: released`.

**Dedup note:** signal about 3.5 Pro pricing, benchmarks, or its launch
UPDATES this ticket. The 3.5 Flash GA lives on the
[gemini-3-2-flash](./gemini-3-2-flash.md) ticket (slug retained from the
pre-I/O "3.2" leak).
