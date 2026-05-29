---
slug: xai-grok-build-2026-05
title: xAI Grok Build — agentic coding CLI + grok-build-0.1 model
company: xAI
model: grok-build-0.1
status: released
status_note: |
  xAI's agentic coding push shipped in two stages: an early beta on
  2026-05-14 limited to SuperGrok Heavy subscribers, then general beta
  on 2026-05-25 for all SuperGrok and X Premium+ users. The product is
  the **Grok Build** CLI (agentic coding + apps + automation, with Plan
  Mode and Imagine for images/video). The underlying coding model is
  branded `grok-build-0.1` and is also exposed via third-party harnesses
  — @opencode (2026-05-21), @openclaw (2026-05-19), and @kilocode
  (2026-05-27). After fast rate-limit consumption, xAI reset Grok Build
  usage limits on 2026-05-26. This is the developer-tooling surface for
  xAI's coding push and is distinct from the still-pending 1.5T Grok
  V9-Medium release (see [[grok-v9-medium]]).
expected: null
labels:
  - coding
  - agentic-cli
  - released
  - developer-tooling
verification: confirmed
sources:
  - "@xai"
  - "@grok"
created_at: 2026-05-28
updated_at: 2026-05-29
closed_at: null
closed_reason: null
history:
  - ts: 2026-05-28
    change: "Created — xAI Grok Build agentic coding CLI shipped in stages: early beta 2026-05-14 (SuperGrok Heavy), general beta 2026-05-25 (all SuperGrok / X Premium+), with backing model `grok-build-0.1` exposed across @opencode (May 21), @openclaw (May 19), @kilocode (May 27). xAI reset Grok Build usage limits on 2026-05-26 after early users hit rate caps fast. Distinct from the pending 1.5T Grok V9-Medium release (grok-v9-medium)"
  - ts: 2026-05-29
    change: "Grok Build 0.2.7 point release (@xai, 2026-05-28 20:55 UTC): adds /usage and /login slash commands, shared terminals across subagents, and improved image understanding. First post-launch capability bump — incremental, not a model swap"
---

**Grok Build** is xAI's agentic coding CLI + developer-platform surface,
launched in two stages:

- **2026-05-14**: early beta, SuperGrok Heavy subscribers only — "agentic
  CLI for coding, building apps, and automating workflows."
- **2026-05-25**: general beta — extended to all SuperGrok and X Premium+
  users, with Plan Mode, Imagine (image/video generation), and an
  automation/orchestrator CLI.

The model branded `grok-build-0.1` is the engine under the CLI and the
same model that xAI now exposes through third-party agentic harnesses:

- **2026-05-19**: @openclaw subscription compatibility (chat, image/video
  generation, X-post search inside the openclaw agent surface).
- **2026-05-21**: @opencode integration ("Use the model powering Grok
  Build for high speed and codebase intelligence").
- **2026-05-27**: @kilocode integration via SuperGrok / X Premium+
  subscription.

**Post-launch rate-limit response.** Users hit Grok Build usage limits
quickly after the general beta opened; xAI's team posted (2026-05-26
20:45 UTC) that caching improvements were identified and Grok Build
usage limits were reset across all accounts.

**Why a separate ticket from [grok-v9-medium](./grok-v9-medium.md):**
Grok V9-Medium is the 1.5T-parameter frontier foundation model (training
complete, fine-tuning in progress, public release "2-3 weeks out" per
Musk on 2026-05-25). `grok-build-0.1` is a distinct coding-focused model
shipping today behind the Grok Build CLI; the two surfaces will
converge if/when V9-Medium ships, but until then they have separate
release cadences, subscription gating, and user-visible names.

**Transition triggers:**
- A successor `grok-build-1.0` (or rename) tied to V9-Medium GA →
  UPDATE here, cross-reference the V9-Medium ticket.
- Public pricing for Grok Build subscriptions or API access changes →
  UPDATE.
- ≥4 weeks past general-beta availability settled into normal coverage
  → `closed: released-and-aged`.

**Dedup note:** further `grok-build-0.x` signal (subsequent point
releases, capability expansion, more third-party integrations, rate
limit changes) UPDATES this ticket. Grok V9-Medium public release goes
to its own ticket; the V9-Medium ticket back-links here for context.
