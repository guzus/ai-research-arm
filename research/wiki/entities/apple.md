---
slug: apple
title: Apple
type: entity
aliases: [Apple, "Apple Inc.", Siri, "Apple Intelligence", "Private Cloud Compute", PCC]
tags: [consumer-tech, on-device-ai, apple-intelligence, siri, wwdc]
summary: Consumer-hardware giant whose long-delayed Siri rebuild — reportedly powered by a custom Google Gemini model with a user-selectable "Extensions" layer — is the marquee AI item at WWDC 2026 (keynote 2026-06-08).
created_at: 2026-06-08
updated_at: 2026-06-10
sources:
  - {title: "ARA daily digest 2026-06-10", path: research/digest/2026-06-10-digest.md}
  - {title: "ARA daily digest 2026-06-08", path: research/digest/2026-06-08-digest.md}
  - {title: "ARA model ticket — Apple WWDC 2026 Siri", path: research/models/tickets/apple-wwdc-2026-siri.md}
  - {title: "The Verge — Apple WWDC 2026 AI Siri / Gemini", url: "https://www.theverge.com/tech/944245/apple-wwdc-2026-ai-siri-gemini", date: 2026-06-06}
  - {title: "TechCrunch — What to expect from WWDC 2026", url: "https://techcrunch.com/2026/06/06/what-to-expect-from-wwdc-2026-siris-highly-anticipated-revamp-and-apple-intelligence-updates/", date: 2026-06-06}
---

**Apple** is tracked in the LLM wiki as the largest consumer-AI distributor —
its install base makes any model it adopts an instant frontier-scale
deployment surface. Unlike [[openai]] or [[anthropic]], Apple builds little
frontier capability in-house; its 2026 AI story is a **partner-and-distill**
strategy, putting it on the consuming side of the [[ai-capex]] economy rather
than the building side.

## Why it matters

- **WWDC 2026 — the Siri rebuild (keynote 2026-06-08, 17:00 UTC).** The week's
  marquee AI catalyst. Per multi-path reporting (The Information's paywalled
  preview, The Verge, TechCrunch), Apple is set to reintroduce a rebuilt Siri
  — recast as a **standalone, chatbot-style app** — reportedly powered by a
  **custom ~1.2T-parameter Google Gemini model** under a **~$1B/yr licensing**
  arrangement. **On-device Siri runs a distilled Gemini** on iPhone silicon;
  heavier queries reportedly route to **Google Cloud** rather than Apple's own
  **Private Cloud Compute**, processed via **NVIDIA's confidential-compute
  stack** ([[nvidia]]) — a material retreat from the 2024 promise that nothing
  would leave Apple silicon, even as the PCC brand is reportedly retained. See
  the model ticket for the full rumor-state detail (ARA digest 2026-06-08).
- **An "Extensions" layer.** Apple is reportedly adding a system letting users
  pick **ChatGPT ([[openai]]), Gemini ([[gemini-3-5-flash|Gemini]]), or Claude
  ([[anthropic]])** to power Apple Intelligence — turning Apple into a neutral
  distribution rail across the three frontier labs rather than a captive of any
  one, and a high-value funnel each lab will compete to occupy.
- **Distillation hunt.** Apple is reportedly scouting on-device-AI shops —
  **[[liquid-ai]]** named — to accelerate the model-shrinking work the distilled
  Gemini stack needs. This puts Apple directly in the small-efficient-model
  competitive frame alongside Gemma and the LFM family.
- **Talent vector.** Mark Gurman scooped that **Kelsey Peterson** — the Apple AI
  engineer who introduced the never-launched 2024 Siri revamp on stage at WWDC —
  started at [[openai]] eight days before WWDC 2026: a defection to the lab whose
  model is *not* the reported Siri partner.

- **AFM 3 + CoreAI ship — the on-device stack (2026-06-10).** Apple announced
  **AFM 3 Core Advanced**, a **20B on-device foundation model** for iPhone 17 Pro
  that **keeps the full model in flash and streams only the active slice into
  memory** — its concrete answer to the on-device-frontier squeeze. It also
  announced **CoreAI**, a new on-device inference framework (**replacing CoreML**)
  supporting up to **20B-param MoE** models. This is the productized core of the
  partner-and-distill strategy: a custom-Gemini-backed Siri "designed for privacy"
  riding on Apple's own on-device runtime (ARA digest 2026-06-10).
- **Apple pulls Siri AI from the EU (2026-06-10).** After EU regulators **denied an
  exemption request to the DMA**, Apple **withheld its new AI Siri features from
  the EU** (and reportedly China at launch) — a flashpoint in the AI-governance
  debate (**282 pts / 480 HN comments**). It puts Apple's distribution leverage
  directly against EU digital-markets rules and echoes the broader
  [[federal-ai-policy]] / regional-fragmentation tension over where frontier
  features may ship (ARA digest 2026-06-10).

**Status update (2026-06-10).** The 2026-06-08 keynote has now landed; the
distilled-Gemini + on-device (AFM 3 / CoreAI) architecture above is **confirmed in
broad strokes**, and the EU/China launch carve-out is now a concrete policy event
rather than a rumor. Earlier rumor-state caveats remain only on the finer cloud-routing
mechanics.

**Status caveat (pre-keynote, retained for history).** As of the 2026-06-08 ingest Apple had **confirmed nothing**; the
architecture is single-/multi-source reporting and the 2026-06-08 keynote (which
lands after the digest's generation time) will confirm or contradict the
distilled-Gemini + cloud-routing detail. Treat every figure above as reported,
not announced.

## Open questions

- **Does the keynote confirm the Gemini-powered architecture?** If Apple ships a
  materially different stack (Apple-silicon-only, or a different cloud partner),
  the whole partner-and-distill read changes.
- **What does outsourcing the frontier model do to Apple's privacy brand?**
  Routing queries off Apple silicon to Google Cloud while keeping the "Private
  Cloud Compute" name is the core tension privacy researchers will probe.
- **Who wins the "Extensions" default?** Being the user-selectable backend for
  Apple Intelligence is a distribution prize [[openai]], Google, and
  [[anthropic]] will all fight over.
