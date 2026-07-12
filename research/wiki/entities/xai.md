---
slug: xai
title: xAI
type: entity
aliases: [xAI, "x.AI", "@xai", Grok, Colossus, "Colossus 1"]
tags: [frontier-lab, grok, compute-landlord, elon-musk, ai-infrastructure]
description: Elon Musk's frontier lab behind Grok; increasingly defined by its compute-landlord business — renting Colossus capacity to rival labs at $2B+/month — and by Grok 4.5, the from-scratch 1.5T "V9" model that ended its private beta and shipped free to all X accounts on 2026-07-10.
created_at: 2026-06-08
timestamp: 2026-07-12T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-07-12", path: research/digest/2026-07-12-digest.md}
  - {title: "ARA model ticket — Grok V9-Medium / Grok 4.5", path: research/models/tickets/grok-v9-medium.md}
  - {title: "ARA daily digest 2026-06-29", path: research/digest/2026-06-29-digest.md}
  - {title: "ARA daily digest 2026-06-08", path: research/digest/2026-06-08-digest.md}
  - {title: "ARA model ticket — Grok V9-Medium", path: research/models/tickets/grok-v9-medium.md}
  - {title: "ARA model ticket — xAI Grok Build", path: research/models/tickets/xai-grok-build-2026-05.md}
  - {title: "ARA model ticket — Anthropic–SpaceX Colossus lease", path: research/models/tickets/anthropic-spacex-colossus-2026-05.md}
  - {title: "ARA model ticket — Google–SpaceX compute pact", path: research/models/tickets/google-spacex-compute-2026-06.md}
---

**xAI** is Elon Musk's frontier AI lab, maker of the **Grok** model family. In
the LLM wiki it matters on two axes: as a frontier-model builder competing with
[[openai]] and [[anthropic]], and — increasingly the bigger story — as the
**compute landlord** of the 2026 cycle, renting its Colossus data-center
capacity (co-located with [[spacex]]) to the very labs it competes with.

## Why it matters

- **The compute-landlord business comes into focus (2026-06-08).** The
  Information confirmed **[[anthropic]] rents xAI/SpaceX capacity at ~$1.25B/month**
  (the Colossus 1 lease through May 2029, ~$15B/yr / ~$40B run-rate), *on top of*
  **Google's reported ~$920M/month** (~$30B through June 2029 for ~110K NVIDIA
  GPUs). Combined, **Elon is taking in $2B+/month selling compute to rival labs**
  — notably **not** [[openai]]. This reframes the contested Google–SpaceX deal:
  on the SpaceX side the capacity sits at **xAI's Colossus-class data centers**,
  making SpaceX/xAI the *seller*, not the buyer. The arrangement is the
  application-layer engine under the [[spacex]] record IPO and a major thread in
  the [[ai-capex]] supercycle (ARA digest 2026-06-08).
- **Grok Build — the agentic-coding surface.** xAI shipped **Grok Build**, an
  agentic coding CLI (Plan Mode, Imagine image/video) backed by the
  `grok-build-0.1` model, in general beta to SuperGrok / X Premium+ users and on
  the xAI API at **$1/m input + $2/m output**, distributed through OpenRouter,
  Vercel AI Gateway, Cursor, and other third-party harnesses — xAI's developer
  answer to [[openai|OpenAI Codex]] and Claude Code ([[dynamic-workflows]]).
- **Grok V9-Medium → Grok 4.5 ships to private beta.** The **1.5T-parameter
  "V9" foundation model** (3× the 0.5T v8 that served Grok 4.3 production, trained
  with heavy [[cursor|Cursor]] data) moved from "training complete" into a **private
  beta at SpaceX and Tesla** as **Grok 4.5** (2026-06-28). Musk claimed early
  internal evals show performance "close to, perhaps exceeding Opus" and committed
  to **from-scratch new models every month** for the rest of 2026 via SpaceX. A
  public **Grok 4.4 (~1T)** may ship within days while 4.5 stays in beta. This is
  xAI's first from-scratch model since Grok 3.
- **Training-data controversy.** Reporting that xAI trained its coding models on
  [[anthropic|Claude]] outputs and continued after Anthropic cut access is an
  open credibility thread on the lab's model-provenance.
- **Grok 4.5: audited by nobody, but the asymmetry is real (2026-06-29).** "Opus"
  is version-ambiguous (4.6/4.7/4.8?), the evals are **internal and unaudited**,
  and xAI has a track record of bold benchmark claims that don't replicate; a
  monthly from-scratch pretraining cadence is extraordinarily aggressive and may
  describe fine-tuned variants. The xAI safety-engineer lawsuit (Devin Kim, filed
  2026-06-10) alleging firing for raising Grok safety concerns days before the
  [[spacex|SpaceX]] IPO adds context to the pace. But the structural point holds:
  a genuinely Opus-competitive Grok shipping **unrestricted** — while
  [[gpt-5-6|GPT-5.6 Sol]] and [[claude-fable-5|Claude Mythos 5]] are
  government-gated — would expose an asymmetry in the de facto US frontier-model
  licensing regime (ARA digest 2026-06-29).

- **Grok 4.5 ends its private beta, ships free to all X accounts
  (2026-07-12).** xAI shipped **Grok 4.5** (the same 1.5T "V9" foundation
  tracked above) free to all X accounts via the Grok Build surface,
  ending the private-beta gate at SpaceX/Tesla. Elon Musk posted a
  "Grok 4.5 Review" (2026-07-11); testingcatalog independently confirmed
  availability to free X accounts (2026-07-10), corroborated by WesRoth
  and a ~44K-post trending topic. This is the first public availability
  for the V9 foundation — clearing the bar this ticket had been tracking
  as `confirmed` (private beta only) since 2026-06-28 (ARA digest
  2026-07-12).

## Open questions

- **Does the landlord business cannibalize the lab?** Selling Colossus capacity
  to [[anthropic]] and Google funds the buildout but hands compute to direct
  competitors — a structurally odd posture for a frontier lab.
- **Where does the [[spacex]] IPO leave xAI's balance sheet?** The compute that
  props up SpaceX's pre-IPO revenue line is the same capacity xAI needs for its
  own Grok roadmap — the S-1 language will clarify who has first call on it.
- **Can Grok V9-Medium close the frontier gap?** xAI's public models trail the
  GPT/Claude/Gemini frontier; Grok 4.5 (the 1.5T V9 in private beta) is the test
  of whether the compute advantage converts into model capability — but with
  no independent benchmarks yet, the Opus-level claim is unaudited.
