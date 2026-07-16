---
slug: gpt-5-6
title: OpenAI GPT-5.6
type: entity
aliases: ["GPT-5.6", "GPT 5.6", "GPT-5.6 Pro", "GPT-5.6 Mini", "GPT-5.6 Sol", "GPT-5.6 Terra", "GPT-5.6 Luna", "Sol", "Terra", "Luna"]
tags: [model-release, openai, gpt, frontier-model, government-gated, preview]
description: OpenAI frontier family — Sol (flagship) / Terra (balanced) / Luna (fast/cheap); Sol Ultra went GA 2026-07-10 and now leads the CritPt physics-reasoning benchmark at 32.3%; usage limits reset a reported 5th time by 2026-07-15 (past 8M active users) alongside acknowledged file-deletion incidents.
created_at: 2026-06-20
timestamp: 2026-07-15T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-07-15", path: research/digest/2026-07-15-digest.md}
  - {title: "ARA daily digest 2026-07-14", path: research/digest/2026-07-14-digest.md}
  - {title: "ARA daily digest 2026-07-13", path: research/digest/2026-07-13-digest.md}
  - {title: "ARA daily digest 2026-07-12", path: research/digest/2026-07-12-digest.md}
  - {title: "ARA daily digest 2026-07-05", path: research/digest/2026-07-05-digest.md}
  - {title: "ARA daily digest 2026-07-04", path: research/digest/2026-07-04-digest.md}
  - {title: "ARA daily digest 2026-06-29", path: research/digest/2026-06-29-digest.md}
  - {title: "ARA daily digest 2026-06-23", path: research/digest/2026-06-23-digest.md}
  - {title: "ARA daily digest 2026-06-21", path: research/digest/2026-06-21-digest.md}
  - {title: "ARA daily digest 2026-06-20", path: research/digest/2026-06-20-digest.md}
  - {title: "ARA model ticket — OpenAI GPT-5.6", path: research/models/tickets/openai-gpt-5-6.md}
  - {title: "OpenAI — Previewing GPT-5.6 Sol", url: "https://openai.com/index/previewing-gpt-5-6-sol/", date: 2026-06-26}
---

**GPT-5.6** is [[openai]]'s frontier family, shipped **2026-06-26** as a
**US-government-gated limited preview** after weeks of rumor. It lands as a
three-tier family — **Sol** (flagship), **Terra** (balanced), **Luna**
(fast/cheap) — with new **"max" reasoning effort** and an **"ultra" mode** that
spawns subagents. Per the model ticket `openai-gpt-5-6`, the lifecycle advanced
from `rumored` to `in-testing` on 2026-06-26 (a real admin-panel artifact plus a
gated external preview); GA is "in the coming weeks."

## Why it matters

- **Shipped — but gated at the US government's request (2026-06-26).** OpenAI
  began a **limited preview of the GPT-5.6 family** with access restricted, **at
  the US government's request**, to a small group of trusted partners shared
  with the government before broader release — the same "de facto licensing
  regime" shape as the [[claude-fable-5|Fable 5 / Mythos 5]] export suspension
  (see [[federal-ai-policy]]). OpenAI stated "this kind of government access
  process shouldn't become the long-term default." *The Information*/Axios report
  the request came through the Office of the National Cyber Director and OSTP
  under the voluntary June 2 frontier-model review EO, and that GPT-5.6 has
  **"Mythos-like" capability** — OpenAI had reportedly pushed for release since
  before the Fable ban. **GA "in the coming weeks"; Polymarket prices ~90% chance
  of public release by July 31.**
- **Capability + pricing.** Sol sets a new SOTA on **Terminal-Bench 2.1** and
  improves agentic coding, biology, and cybersecurity. Pricing (per 1M tokens):
  **Sol $5 in / $30 out**; **Terra $2.50 / $15**; **Luna $1 / $6**, with new
  explicit cache breakpoints and a 30-minute minimum cache life.
- **From rumor to artifact — the prelude.** For most of June the signal was
  anticipation, not a shipping artifact: prediction markets priced a
  by-2026-06-30 release ~89%; a `gpt-5.6-preview` route leaked in OpenAI's admin
  panel (2026-06-25, @scaling01/@haider1); chief scientist **Jakub Pachocki**
  reportedly called it internally a "meaningful improvement" over GPT-5.5. The
  viral "stealth GPT-5.6-Pro" demos were debunked as model-tier confusion
  (testers were on GPT-5.5-Pro). The leaked ~1.5M-context / ~3×-cheaper-than-
  Fable-5 specs were rumor until the preview.
- **The competitive backdrop.** GPT-5.6 is the closed-frontier counterweight to a
  field where [[anthropic]]'s [[claude-fable-5|Fable 5 / Mythos 5]] sits embargoed
  and open weights like [[zhipu-glm-5-2|GLM-5.2]] are closing the gap. It shipped
  the same window as OpenAI's **Jalapeño** custom inference ASIC
  ([[broadcom|Broadcom]]-co-designed) — vertical integration on both the model
  and the silicon layer.

- **GA timing narrows to a single-leaker July 7 target (2026-07-04).** Tier
  names **"Sol," "Terra," and "Luna"** were spotted embedded in Codex app
  code (not yet enabled); real-time voice support reportedly remains in
  development. A single leaker (@synthwavedd) now names **July 7** as the
  most likely launch date within a July 7–9 window — explicitly timed to
  catch users leaving [[claude-fable-5|Claude]] after Fable 5's
  subscription-plan cutoff — with plan limits claimed to be "significantly
  more generous" than Fable 5's, though unconfirmed. Prediction-market
  activity (one trader accumulating ~8,000 shares) also clusters on July 7,
  though this reads as pattern-matching rather than inside information.
  *Single-source; no OpenAI confirmation or system card yet* (ARA digest
  2026-07-04).
- **Tier names upgrade from code-spotted to primary-source confirmed
  (2026-07-05).** The **Sol / Terra / Luna** tier names are now confirmed
  via a primary-source commit in OpenAI's Codex GitHub repo (not just
  spotted in shipped app code as reported 2026-07-04), and live Codex-app UI
  sightings reinforce the rumored **July 7 ("Tuesday")** launch date — still
  unconfirmed as an official date; no OpenAI statement or system card has
  landed (ARA digest 2026-07-05).

- **Sol Ultra goes GA; a 50-year-old math proof and CritPt benchmark lead
  (2026-07-12).** OpenAI's own account confirmed **GPT-5.6 Sol Ultra went
  generally available on 2026-07-10**, and Sam Altman said GPT-5.6 is now
  "the preferred model in Microsoft 365 Copilot" — dozens of independent
  users report hitting rate limits, consistent with broad rollout beyond
  the earlier ~20-org gated preview. Sol Ultra reportedly used **64
  subagents** to produce a novel proof for a 50-year-old open math problem
  in under an hour, and now **leads the CritPt physics-reasoning benchmark
  at 32.3%** — ahead of GPT-5.5 Pro (30.6%) and GPT-5.6 Terra (30.0%), with
  Gemini 3 Pro Deep Think at 25.7% and Claude Opus 4.8 at 20.9%, giving
  OpenAI all top-5 spots. Separately, **GPT-5.6 Luna** reportedly hit
  "model at capacity" errors for some users shortly after rollout — early
  capacity-scaling friction, not independently confirmed. *The CritPt
  ranking traces to a single secondary-source tweet, not a verified
  leaderboard* (ARA digest 2026-07-12).

- **Third capacity intervention in 48 hours — the usage-cap backlash escalates
  (2026-07-13).** Codex/ChatGPT Work lead **@thsottiaux** announced [[openai]]
  is **temporarily removing the 5-hour usage cap** and **banking a reset for
  500K users**, the **third capacity move in 48 hours** following two prior
  resets since Friday. At least one close OpenAI-watcher reads the pattern as
  **PR management of a real capacity/cost problem** rather than a genuine fix
  — undercutting OpenAI's own "halved inference cost" claims from the GPT-5.6
  GA window and landing the same cycle [[anthropic]] extended
  [[claude-fable-5|Claude Code's]] own rate-limit boost through July 19 (ARA
  digest 2026-07-13).

- **Rollout continues; "ChatGPT Work" and a 2.2x-latency production case
  study (2026-07-14).** The **Sol / Terra / Luna** family and **"ChatGPT
  Work"** (powered by Codex + GPT-5.6) continued rolling out — official
  OpenAI YouTube uploads this cycle included a 35-minute livestream intro
  plus short product spots. A production case study surfaced on Hacker News
  reporting that migrating an agent workload to GPT-5.6 yielded **2.2x
  faster latency and 27% lower cost** — an independent-ish (practitioner
  self-report) data point on the capacity/cost claims that have driven the
  repeated usage-cap interventions tracked above (ARA digest 2026-07-14).

- **A 5th usage-limit reset; file-deletion reports acknowledged
  (2026-07-15).** [[openai]] reset Codex/ChatGPT Work usage limits for a
  **reported 5th time** since launch, with active users now crossing
  **8M** — continuing the capacity-intervention pattern tracked since
  July 13. Separately, social reports describe the model **deleting
  files/data without warning** in some sessions, a behavior OpenAI has
  **acknowledged as a previously-disclosed issue** rather than denied
  (ARA digest 2026-07-15).

## Open questions

- **Does the government gate become the default?** OpenAI itself said the access
  process "shouldn't become the long-term default" — but with Sol gated and
  [[claude-fable-5|Mythos 5]] export-suspended, the de facto licensing regime now
  covers both US frontier flagships. Watch whether GA actually opens "in the coming
  weeks" or slips (Polymarket ~90% by July 31).
- **Neutral benchmarks.** Sol's Terminal-Bench 2.1 SOTA is OpenAI's own claim;
  no independent eval has landed. Does it hold up against [[claude-fable-5|Fable 5]]
  and [[zhipu-glm-5-2|GLM-5.2]] on contamination-aware harnesses?
- **Family-at-once cadence.** Shipping Sol/Terra/Luna together (plus "ultra"
  subagent-spawning mode) is a break from staggered GPT-5.x rollouts — a signal
  about OpenAI's product discipline ahead of its IPO.
