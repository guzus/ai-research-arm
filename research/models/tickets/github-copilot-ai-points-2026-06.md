---
slug: github-copilot-ai-points-2026-06
title: GitHub Copilot transitions to usage-based "AI Points" billing
company: GitHub / Microsoft
model: null
status: released
status_note: |
  GitHub flipped Copilot from a low-cost unlimited monthly subscription
  to a **usage-based billing model on 2026-06-01**, debiting per-model
  and per-token "GitHub AI Points" against three new monthly bundles:
  **Pro $10/mo for 1,500 points**, **Pro+ $39/mo for 7,000 points**,
  and **Copilot Max $100/mo for 20,000 points**. Core code-generation
  is billed per-point. Day-2 enterprise reports (e.g. @dazfl 2026-06-02
  06:11 UTC) describe "burned through 100% of our enterprise AI credits
  ... ran an agent in Visual Studio and burned through an additional
  $5 of credits," surfacing immediate sticker-shock at the new pricing
  envelope. Frames as the dev-tools side of the same Microsoft
  positioning that lands at the Build 2026 keynote
  ([[microsoft-build-2026-models]]) the next day, where Copilot Code
  + Copilot Cowork + Scout 24/7 Agent are expected to launch into a
  pricing model that already moved to usage-based.
expected: "Microsoft Build 2026-06-02 09:30 PT may surface bundle / Visual Studio integration details"
labels:
  - released
  - pricing-change
  - billing-model
  - github-copilot
  - microsoft
  - dev-tools
verification: confirmed
sources:
  - "@Awesome_AI_News"
  - "@dazfl"
created_at: 2026-06-02
updated_at: 2026-06-02
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-02
    change: "Created — GitHub Copilot transitioned 2026-06-01 from unlimited monthly subscription to usage-based 'GitHub AI Points' billing across three tiers (Pro $10/1.5k, Pro+ $39/7k, Max $100/20k), per @Awesome_AI_News 2026-06-02 06:15 UTC bilingual write-up. Day-2 enterprise pain reported by @dazfl 2026-06-02 06:11 UTC: '100% of our enterprise AI credits' burned in ~36h, agent runs in Visual Studio surfacing $5/run effective cost. Status: released (live now); verification: confirmed (specific tier prices + agent-mode cost behaviour described). Frames as the dev-tools/billing side of the Build 2026 unified-Copilot push tracked on [[microsoft-build-2026-models]] — Build keynote 2026-06-02 09:30 PT may surface bundle / Visual Studio Copilot Code integration details"
---

**GitHub Copilot's billing model flipped on 2026-06-01** from a
low-cost unlimited monthly subscription to a **usage-based "GitHub AI
Points" debit system**. The change moves Copilot from flat-rate
predictability to per-model and per-token consumption pricing — the
same direction Anthropic, OpenAI, and Google have been pushing in
their developer surfaces, but Copilot is the first IDE-anchored dev
tool to do this at scale.

**New plan structure (live now):**

- **Copilot Pro** — $10/mo, **1,500 AI Points**.
- **Copilot Pro+** — $39/mo, **7,000 AI Points**.
- **Copilot Max** — $100/mo, **20,000 AI Points**.

Core code-generation is now billed per-point, with point cost varying
by model and token consumption. Agent-mode runs (the Visual Studio
agent surface) burn meaningfully more points than completion-style
usage.

**Why this is a model-timeline ticket** rather than a one-off
business-news item: pricing model changes at this surface
materially affect which underlying frontier models customers can
afford to call for which tasks. Anthropic, OpenAI, DeepSeek, and the
homegrown Microsoft MAI models all sit downstream of Copilot's
billing envelope. Heavy-agent workflows that previously ran free
under unlimited Copilot Pro now hit point ceilings; teams will
optimise for cheaper models, shorter contexts, or different vendors.

**Day-2 enterprise pain signal.** @dazfl (2026-06-02 06:11 UTC,
"Day 2 of the new #github usage model ... already burned through
100% of our enterprise AI credits. Just now ran an agent in Visual
Studio and burned through an additional $5 of credits") gives a
specific cost-shock data point: a single Visual Studio Copilot agent
run costs ~$5 of credits, and an enterprise pool burns out within
~36 hours of the transition. Whether that's the new steady state
or a transition-period artifact of teams not adapting their usage
yet is the open question for week 1.

**Cross-ticket framing:** lands the day before the
[[microsoft-build-2026-models]] keynote (2026-06-02 09:30 PT), where
the unified-Copilot super-app reveal (Copilot Code + Copilot Cowork
+ Scout 24/7 Agent per @testingcatalog leak) ships into a billing
model that already moved to usage-based. The pricing change is
likely the substrate Build will build the agent-mode launches on top
of.

**Transition triggers:**

- Microsoft Build 2026 (2026-06-02) discloses additional Copilot
  bundle / Code / Cowork pricing → UPDATE with the new tiers and any
  enterprise pool changes.
- Microsoft announces a reversal, bundle adjustment, or grace-period
  extension after backlash → UPDATE with history entry; status stays
  `released`.
- Independent third-party cost analysis (Copilot vs Cursor vs Claude
  Code on equivalent workloads) → UPDATE.
- ≥4 weeks past 2026-06-01 transition with the pricing settled into
  normal coverage → `closed: released-and-aged`.

**Dedup note:** further Copilot pricing signal (tier changes, agent-
mode cost adjustments, enterprise-pool sizing, backlash + reversal)
UPDATES this ticket. The broader Microsoft Build 2026 model lineup
(MAI Voice 2, MAI Transcribe 1.5, Copilot Code, Cowork, Scout) is on
[[microsoft-build-2026-models]]. A *successor* billing model (e.g.
"GitHub AI Points 2" or a return to flat-rate) gets its own ticket.
