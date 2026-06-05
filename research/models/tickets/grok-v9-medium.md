---
slug: grok-v9-medium
title: Grok V9-Medium (1.5T) — public release
company: xAI
model: Grok V9-Medium
status: confirmed
status_note: |
  Officially announced by Elon Musk (2026-05-25): the 1.5T-parameter Grok
  V9-Medium foundation model has finished training (evals "look good"),
  fine-tuning is underway, and reinforcement learning starts in days.
  Public release stated at 2-3 weeks out. 3x the 0.5T v8-small that
  currently serves all Grok production traffic; heavy Cursor coding data
  added in supplementary training, positioned as a major upgrade for
  difficult coding tasks. Not yet publicly available.
expected: "~mid-June 2026 (re-reported 'public release days away' / 'this month' as of 2026-06-05; originally 2–3 weeks per @elonmusk 2026-05-25)"
labels:
  - frontier-model
  - coding
  - upcoming
verification: confirmed
sources:
  - "@elonmusk"
  - "@ai_for_success"
created_at: 2026-05-25
updated_at: 2026-06-05
closed_at: null
closed_reason: null
history:
  - ts: 2026-05-25
    change: "Created — @elonmusk announced Grok V9-Medium (1.5T) finished training, fine-tuning underway, RL in days, 2-3 weeks to public release; major coding upgrade over the 0.5T v8-small, trained with heavy Cursor data"
  - ts: 2026-05-28
    change: "Context: xAI shipped the Grok Build agentic coding CLI in general beta on 2026-05-25 (the same day as the V9-Medium training announcement), with the backing model branded `grok-build-0.1` — distinct from V9-Medium. Spun out as its own ticket: see [[xai-grok-build-2026-05]]. The V9-Medium 2-3 week window from 2026-05-25 still points to ~mid-June 2026 for public release; no new signal on benchmarks, pricing, or surface this cycle"
  - ts: 2026-06-05
    change: "Timing tightened (secondary): aggregator restatements (e.g. @GlobalWireLive) frame V9-Medium — 1.5T params, training complete, fine-tuning underway — as 'launching this month' / 'public release days away', consistent with the original ~mid-June window now that we're inside it. Attributed to Musk's prior announcement, no fresh xAI primary this cycle. Added context (single low-cred source, not separately tracked): Grok 4.3 cited at ~75% SWE-bench Verified (current production), and a larger **Grok 5** (~6T-param MoE) said to be 'actively training' on the Colossus 2 supercluster. Status stays confirmed; expected refreshed"
---

xAI's next foundation model, **Grok V9-Medium**, was announced by Elon
Musk on 2026-05-25: training is complete with strong internal evals,
fine-tuning is underway, reinforcement learning begins within days, and
public release is stated as 2-3 weeks out (≈June 2026).

At **1.5 trillion parameters** it is triple the size of the **0.5T
v8-small** that currently serves all Grok production traffic. The
headline differentiator is data, not just scale: xAI added a large
volume of **Cursor** coding interaction data in supplementary training,
explicitly targeting "difficult coding tasks" — multi-file reasoning,
refactors, and agentic workflows — where prior Grok versions lagged
Claude and GPT-class models.

This ticket sits at **confirmed** rather than **released**: the founder's
announcement is a primary source, but the model is not yet publicly
available. Transition to `released` when it ships to users (Grok app /
API / Grok Build). The frequently-repeated "renamed to SpaceXAI" claim
circulating alongside the announcement is single-source and unverified;
it is not tracked here unless corroborated.

**Transition triggers:**
- A public preview, API listing, or rollout → `status: released`.
- If the 2-3 week window passes with no release and no fresh signal →
  refresh `status_note`/`expected`; consider `unverified` drift only if
  the original primary source is retracted.

**Dedup note:** further Grok V9 signal (benchmarks, pricing, release
date, the RL phase, a V9-Large/Heavy variant tier) UPDATES this ticket.
A distinct successor family gets its own ticket and links back here.
