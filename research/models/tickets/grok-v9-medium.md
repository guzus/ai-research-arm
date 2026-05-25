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
expected: "~2026-06 (2–3 weeks to public release per @elonmusk, 2026-05-25)"
labels:
  - frontier-model
  - coding
  - upcoming
verification: confirmed
sources:
  - "@elonmusk"
  - "@ai_for_success"
created_at: 2026-05-25
updated_at: 2026-05-25
closed_at: null
closed_reason: null
history:
  - ts: 2026-05-25
    change: "Created — @elonmusk announced Grok V9-Medium (1.5T) finished training, fine-tuning underway, RL in days, 2-3 weeks to public release; major coding upgrade over the 0.5T v8-small, trained with heavy Cursor data"
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
