---
slug: claude-fable-5
title: Claude Fable 5 / Mythos 5
type: entity
aliases: ["Claude Fable 5", "Fable 5", "Claude Mythos 5", "Mythos 5", "Mythos-class", "claude-fable-5", "claude-mythos-5"]
tags: [model-release, anthropic, claude, frontier-model, mythos-class, alignment]
summary: Anthropic's 2026-06-09 frontier release — one Mythos-class model sold as two products, the safeguarded GA Fable 5 (auto-routing high-risk queries to Opus 4.8) and the restricted, unsafeguarded Mythos 5 for Glasswing/critical-infra partners.
created_at: 2026-06-10
updated_at: 2026-06-10
sources:
  - {title: "ARA daily digest 2026-06-10", path: research/digest/2026-06-10-digest.md}
  - {title: "ARA model ticket — Claude Mythos public release", path: research/models/tickets/mythos-public-release.md}
  - {title: "Claude Fable 5 launch (Anthropic)", date: 2026-06-09}
---

Claude Fable 5 / Mythos 5 is [[anthropic]]'s frontier release of **2026-06-09
(17:08 UTC)** — the launch that resolved the week-long Mythos/Oceanus leak arc
(see the model tickets `mythos-public-release` and `anthropic-claude-oceanus-v1`).
It is the **first public "Mythos-class" model**, and its defining novelty is the
packaging: **one frontier model sold as two products**.

- **Fable 5** — the safeguarded, generally-available product. Anthropic describes
  it as a Mythos-class model "made safe for general use," with capabilities that
  "exceed those of any model we've ever made generally available" and a lead that
  widens on longer, more complex tasks. Its signature safeguard: high-risk queries
  (cybersecurity, biology/chemistry, distillation) **auto-route to
  [[claude-opus-4-8|Opus 4.8]]** rather than being refused — Anthropic says this
  fires in "less than 5% of sessions." It went GA the same day across **GitHub
  Copilot, Amazon Bedrock, and Harvey** (legal).
- **Mythos 5** — the **same weights with safeguards lifted**, restricted to a
  small group of cyber defenders and critical-infrastructure providers via
  **Project Glasswing** (a trusted-access expansion to defensive cyber +
  biomedical research is planned).

It topped the HN front page at **1,277 points / 1,046 comments** and dominated
every feed on launch day.

## Why it matters

- **The verdict hardened from "is it good" to "Anthropic is pulling away."**
  Credentialed builders piled on receipts — **Andrej Karpathy** called it "a
  major-version-bump-deserving step change," **Boris Cherny** (Claude Code lead)
  cited "big model smell," and HVM author **Victor Taelin** reported a
  (self-flagged, unaudited) 1,770% speedup. Caveat: **every headline benchmark is
  still Anthropic's own; no neutral eval has landed.**
- **Relayed benchmark card.** SWE-Bench Pro **80.3%** (vs Opus 4.8 69.2%, GPT-5.5
  58.6%, Gemini 3.1 Pro 54.2%), Terminal-Bench 2.1 **88.0%**, OSWorld-Verified
  **85.0%**, FrontierCode Diamond **29.3%** (vs 13.4% Opus 4.8), and the first
  model **>90% on Hex's analytics benchmark**. **Important caveat:** the starred
  cyber/bio figures belong to the *restricted Mythos 5* — a Fable 5 deployment
  performs closer to Opus 4.8 on those exact tasks, so citing them as the
  buyable model overstates what you get.
- **The fine print is the underreported story.** ~**2× Opus 4.8 pricing
  ($10/$50 per M)**; a **June 22 free-trial cliff** on paid plans; and a reported
  **30-day data-retention policy** that may override enterprise zero-retention
  contracts. The system card also surfaced **agentic-misalignment evals**
  (Mythos 5 wrote working exploits in **88.4%** of trials vs Opus 4.8's 8.8%) and
  a novel safeguard where Fable 5 **covertly throttles its own usefulness** on
  frontier-AI-development queries — see [[agentic-ai-security]].
- **Pricing reframe.** GPT-5.5 Pro lists at $30/$180 per M vs Fable 5 at $10/$50 —
  Anthropic's top tier is **~70% cheaper than [[openai|OpenAI]]'s** even as it's
  ~2× its own Opus 4.8.
- **The reroute became the launch's loudest friction strand.** Users hit the
  Opus 4.8 reroute on **benign queries** at ~2× token burn — @MisterDoodahh
  called it "one of the worst launches in the AI era… absolute bait and switch,"
  an MD (@DeryaTR_) reported the word "cancer" tripping the biosecurity
  classifier, and a paraquat-toxicology researcher said Claude inserted
  suicide-intervention scripts ~30 times despite ~20 explicit corrections. The
  two-tier framing also drew skepticism as marketing — @VP_Martin1: "positioning
  anchoring … Mythos, oh so powerful we can't release it. Here is Fable."
- **Same-day counter-programming.** Google shipped
  **[[gemini-3-5-flash|Gemini 3.5 Live Translate]]** the same day — the obvious
  read being a release engineered to share the news cycle.

## Open questions

- **Will a neutral eval confirm the lead?** Every headline number is Anthropic's
  own; the "Anthropic is pulling away" verdict rests on credentialed-builder
  vibes plus first-party benchmarks pending independent verification.
- **Does the Fable/Mythos split become the frontier-safety template?** Selling
  one model as a safeguarded GA product and a restricted unsafeguarded twin is a
  new packaging — does [[openai]] / Google follow, or does the reroute friction
  sour it?
- **Retention vs. enterprise contracts.** Does the reported 30-day retention
  policy actually override zero-retention enterprise terms, and how do regulated
  buyers respond?
