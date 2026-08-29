---
slug: xai
title: xAI
type: entity
aliases: [xAI, "x.AI", "@xai", Grok, Colossus, "Colossus 1", "Grok 4.6", "Grok Bot"]
tags: [frontier-lab, grok, compute-landlord, elon-musk, ai-infrastructure]
description: Elon Musk's frontier lab behind Grok; shipped Grok 4.6 into Cursor and Grok Build on 2026-08-13 at $2/$6 per Mtok with a 61 on the Artificial Analysis Intelligence Index, reported top of MedAgentBench (~95.9% pass@1) and now tied #1 with Claude Opus 5 on an agentic index (2026-08-21), while still suing users over Grok-generated CSAM rather than addressing the underlying capability and facing a model-card diff restating four eval results in a flattering direction.
created_at: 2026-06-08
timestamp: 2026-08-22T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-08-22", path: research/digest/2026-08-22-digest.md}
  - {title: "ARA daily digest 2026-08-21", path: research/digest/2026-08-21-digest.md}
  - {title: "ARA daily digest 2026-08-19", path: research/digest/2026-08-19-digest.md}
  - {title: "ARA daily digest 2026-08-13", path: research/digest/2026-08-13-digest.md}
  - {title: "ARA daily digest 2026-08-12", path: research/digest/2026-08-12-digest.md}
  - {title: "ARA daily digest 2026-08-10", path: research/digest/2026-08-10-digest.md}
  - {title: "ARA daily digest 2026-07-30", path: research/digest/2026-07-30-digest.md}
  - {title: "ARA daily digest 2026-07-28", path: research/digest/2026-07-28-digest.md}
  - {title: "ARA daily digest 2026-07-27", path: research/digest/2026-07-27-digest.md}
  - {title: "ARA model ticket — xAI Grok 4.6 (2T) SpaceX data", path: research/models/tickets/xai-grok-2t-spacex-data-2026-07.md}
  - {title: "ARA daily digest 2026-07-19", path: research/digest/2026-07-19-digest.md}
  - {title: "ARA daily digest 2026-07-17", path: research/digest/2026-07-17-digest.md}
  - {title: "ARA daily digest 2026-07-15", path: research/digest/2026-07-15-digest.md}
  - {title: "ARA daily digest 2026-07-14", path: research/digest/2026-07-14-digest.md}
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

- **Grok Build CLI allegedly exfiltrates local repos and secrets; xAI
  responds with a ZDR clarification, not a denial (2026-07-14).** A major
  Hacker News thread alleged **Grok Build CLI uploads entire local
  repositories — including unredacted `.env` secrets — to xAI-controlled
  cloud storage**, a fresh capability-misuse/supply-chain data point on top
  of the earlier Claude-training-data controversy (see
  [[agentic-ai-security]]). xAI responded with a **zero-data-retention
  (ZDR) clarification** rather than a denial of the underlying collection
  behavior — leaving the exfiltration claim itself unaddressed. The same
  day, **Perplexity cited that ZDR guarantee** when announcing a same-day
  **Grok 4.5 integration**, treating the clarification as sufficient
  reassurance for a partner integration even as the community reaction
  produced **Clawk**, a Show HN disposable-Linux-VM sandbox for coding
  agents built directly in response (ARA digest 2026-07-14).

- **Grok Build's codebase-upload behavior confirmed by security press
  (2026-07-15).** The Verge and The Register **confirmed** the 2026-07-14
  allegation: Grok Build was packaging and uploading **entire user code
  repositories — including files it was told not to open — to Google
  Cloud**, per security firm **Cereblab's** findings. xAI turned the
  behavior off only after being caught, and had responded the prior day
  with a zero-data-retention clarification rather than a denial. This
  moves the story from a single Hacker News allegation to press-confirmed
  fact, escalating the privacy dispute [[openai|Sam Altman]] had
  amplified as "concerning" two cycles earlier (ARA digest 2026-07-15).

- **xAI sues users over Grok-generated CSAM instead of fixing the
  underlying issue (2026-07-17).** Following reporting that xAI can no
  longer deny **Grok generates CSAM**, the company is now **suing users
  over the outputs** rather than addressing the underlying generation
  capability — a legal-offense response to a safety failure, in contrast
  to the ZDR-clarification pattern xAI used for the Grok Build data
  exfiltration story two cycles earlier. This is the most severe entry yet
  in xAI's accumulating capability-misuse/safety-response track record (ARA
  digest 2026-07-17).

- **Grok Build 0.2.105 makes Grok 4.5 the default model (2026-07-19).**
  xAI shipped **Grok Build 0.2.105**, making **Grok 4.5** (the 1.5T "V9"
  foundation tracked above) the CLI's **new default model**, adding a
  **selectable reasoning-effort control**, a **`/summarize` command**, and
  **improved long-session compaction** (@mark_k) — an incremental
  developer-tooling update to the agentic-coding surface rather than a new
  foundation model (ARA digest 2026-07-19).

- **Grok 4.6 — the next from-scratch model gets a name and a timeline
  (2026-07-21 → 2026-07-26).** Elon Musk confirmed SpaceX's proprietary
  engineering-data corpus (excluding ITAR-restricted material) will be
  folded into supplemental training for xAI's next ~**2-trillion-parameter**
  model — roughly **2x Grok 4.5's 1.5T** ("V9"). By 2026-07-26 the model had
  a working name, **Grok 4.6**, and a rough timeline — **"already in 2
  weeks"** per Musk, expected to **surpass [[moonshot-kimi-k3|Kimi K3]]** on
  benchmarks (@testingcatalog, corroborated by @kimmonismus). Still a
  training-plan/timeline disclosure with **no artifact** (preview, console
  listing, leak) as of this writing — status stays rumored in the lifecycle
  sense even though the source (the CEO) is primary. See the
  [Grok 4.6 ticket](../../models/tickets/xai-grok-2t-spacex-data-2026-07.md)
  (ARA digest 2026-07-27).
- **Grok 4.7 already projected behind it (2026-07-28).** The Grok 4.6
  timeline held steady — still ~2T parameters targeting a roughly two-week
  ship to surpass [[moonshot-kimi-k3|Kimi K3]] — but Musk is now also
  projecting **Grok 4.7 two weeks after Grok 4.6**, extending xAI's
  from-scratch monthly-cadence claim (tracked since 2026-06-29) one model
  further out. Still no shipped artifact for either (ARA daily digest
  2026-07-28).

- **Grok 4.5 lands in GitHub Copilot and Cursor's India plan; Grok 4.6
  preview date firms up (2026-07-30).** **Grok 4.5** went live in
  **GitHub Copilot's** model picker and **Cursor's** India-only "Start"
  plan — third-party distribution surfaces beyond xAI's own Grok Build
  CLI, extending the model's reach tracked since its 2026-07-12 free
  public release. Musk also previewed a **Grok 4.6** release around
  **~Aug 7** and a further **Grok 4.7** roadmap beyond it, tightening the
  "already in 2 weeks" timeline first floated 2026-07-26. Separately,
  **Grok Voice Think Fast 2.0** reportedly topped the **Artificial
  Analysis Speech-to-Speech Quality Index at 82.9%**, cutting
  time-to-first-audio from 1.25s to 0.70s at 60% fewer reasoning tokens,
  priced **$0.08/minute** (ARA daily digest 2026-07-30).
- **Grok Image 2.0 — xAI's image model takes editing seriously (2026-08-09,
  blog-sourced).** Coverage of a **Grok Image 2.0** release focused on
  substantially improved **image editing** —   positioning it against the
  consumer image-editing front led by Google's [[nano-banana-2-lite|Nano
  Banana]] and [[midjourney]] — a modest capability update to xAI's image
  line rather than a new foundation model. Single-blog coverage in the
  digest; no official xAI announcement or model card was captured (ARA daily
  digest 2026-08-10).
- **Grok Bot enters early beta — persistent cloud agents (2026-08-12).**
  **SpaceXAI** (the xAI/SpaceX pairing) shipped **Grok Bot into early beta**:
  persistent cloud agents that **keep working after the user disconnects**,
  **delegate to one another**, and **sign into sites lacking APIs** —
  distributed through   **[[cursor|Cursor]]'s paid tiers**. It is xAI's
  productized answer to the always-on agent wave and the first consumer-facing
  persistent-agent surface from the Grok line. In the same window, Musk
  pushed **Grok 4.6** to **"later this week"** after it **slipped twice** —
  the model tracked since 2026-07-26 still has no shipped artifact
  (@elonmusk, @AndrewCurran_, @testingcatalog; ARA daily digest 2026-08-12).
- **Grok 4.6 ships — the 2T from-scratch model finally lands (2026-08-13).**
  Live around **15:27 UTC** in **Cursor and Grok Build** same-day, at **$2 per
  million input / $6 per million output** tokens (2× usage included for the
  first week) — repricing the frontier tier against [[claude-fable-5|Claude
  Fable 5 Max]]'s **$10/$50** (roughly 5×/8× cheaper). The vendor table puts it
  at **61 on the Artificial Analysis Intelligence Index** (level with
  [[gpt-5-6|GPT-5.6 Sol]]) and **first on the separate Agentic Index**, ahead
  of Sol on **CursorBench (69.9% vs 67.2%)**, FrontierCode and AA-Briefcase,
  behind on DeepSWE and Terminal-Bench. The "1753" figure Musk amplified at
  launch resolved to a **GDPVal-AA v2 score**. The Decoder reports it
  completes complex agentic workflows in **~53 steps where Opus 5 needs 103,
  at 60%+ lower price**; on Parametric CAD Bench, Grok 4.6 hit **96.9% of
  [[claude-opus-5|Claude Opus 5]]'s top score for 61% of the cost**. Caveats:
  every capability claim at launch traces back to the vendor, and the
  friendliest witness, @scaling01, wrote that on "really long-running and
  autonomous workflows … the best OpenAI and Anthropic models are much better
  in the tails." Musk dated **Grok 4.7 to three or four weeks out** at
  18:34 UTC with initial training already complete (ARA digest 2026-08-13).

- **Grok 4.6 reported top of MedAgentBench; Grok 4.7 "coming soon" (2026-08-19).**
  Grok 4.6 was reported **top of MedAgentBench at ~95.9% pass@1** (three-run
  average, range 95.3–96.3%) against a **prior best of ~94.7% for
  [[gpt-5-6|GPT-5.6 Sol]]**, amplified by Elon Musk — **at least the fourth
  favourable leaderboard placement in six days**, several of them
  **vendor-adjacent**, so treat the superlative with the same skepticism this
  page applies to xAI's bold benchmark claims. Musk separately said **Grok 4.7
  is "a major upgrade" and "coming soon,"** with **no date** — consistent with
  the ~3–4-week cadence dated at the 2026-08-13 Grok 4.6 ship (ARA daily digest
  2026-08-19).

- **Grok 4.6 safety numbers revised downward-by-rewrite; wider rollout
  (2026-08-21).** xAI published a **model-card diff showing four eval results
  restated in the flattering direction and the independent Vals Index deleted
  with no changelog entry** — the same week Ars Technica documented a **Grok
  data-exfiltration technique** (@SafetyChanges, Ars Technica). This is the
  safety-transparency counterweight to the favourable-leaderboard pattern this
  page tracks. Separately, **Grok 4.6 continued rolling out on the X platform**,
  with **Grok Build expanded from a limited cohort to all SuperGrok and X
  Premium users**; a relay putting **Grok 4.6 (High) tied for #1 on Artificial
  Analysis's Agentic Index at 59, level with [[claude-opus-5|Claude Opus 5]]**,
  was retweeted by Elon Musk. TechCrunch separately reported **Grok sending
  gibberish responses to Grok Lite users** (ARA daily digest 2026-08-21).

- **Grok Bot widens, Grok Build 1.0.8, and Grok 4.6 lands on Google Vertex
  (2026-08-22).** Three incremental distribution moves over one day: **Grok Bot**
  (the persistent cloud-agent product) moved to **wider access — later clarified as
  SuperGrok Plus, Cursor Pro+ and Cursor Teams, not general availability**; **Grok
  Build 1.0.8** shipped with **faster non-blocking subagents**; and **Grok 4.6
  landed on Google Vertex AI**, its first hyperscaler-cloud presence since the
  Cursor/Grok Build launch surfaces of 2026-08-13. Vertex availability is the
  distribution-relevant part: it puts the 2T model in front of enterprise/regulated
  buyers without going through Google's own Gemini branding (ARA daily digest
  2026-08-22).

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
