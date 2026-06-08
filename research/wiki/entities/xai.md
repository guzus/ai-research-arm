---
slug: xai
title: xAI
type: entity
aliases: [xAI, "x.AI", "@xai", Grok, Colossus, "Colossus 1"]
tags: [frontier-lab, grok, compute-landlord, elon-musk, ai-infrastructure]
summary: Elon Musk's frontier lab behind Grok; increasingly defined by its compute-landlord business — renting Colossus capacity to rival labs at $2B+/month (Anthropic ~$1.25B, Google ~$920M).
created_at: 2026-06-08
updated_at: 2026-06-08
sources:
  - {title: "ARA daily digest 2026-06-08", path: research/digest/2026-06-08-digest.md}
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
- **Grok V9-Medium pending.** A **1.5T-parameter** frontier foundation model is
  reportedly training-complete with public release weeks out — the model that
  would put xAI back in the public benchmark race against GPT-5.x and the gated
  [[anthropic|Anthropic Mythos]].
- **Training-data controversy.** Reporting that xAI trained its coding models on
  [[anthropic|Claude]] outputs and continued after Anthropic cut access is an
  open credibility thread on the lab's model-provenance.

## Open questions

- **Does the landlord business cannibalize the lab?** Selling Colossus capacity
  to [[anthropic]] and Google funds the buildout but hands compute to direct
  competitors — a structurally odd posture for a frontier lab.
- **Where does the [[spacex]] IPO leave xAI's balance sheet?** The compute that
  props up SpaceX's pre-IPO revenue line is the same capacity xAI needs for its
  own Grok roadmap — the S-1 language will clarify who has first call on it.
- **Can Grok V9-Medium close the frontier gap?** xAI's public models trail the
  GPT/Claude/Gemini frontier; V9-Medium is the test of whether the compute
  advantage converts into model capability.
