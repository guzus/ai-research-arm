---
slug: microsoft-mai-voice-2-flash-2026-07
title: Microsoft MAI-Voice-2-Flash — faster, cheaper voice model launch
company: Microsoft AI
model: MAI-Voice-2-Flash
status: released
status_note: |
  @mustafasuleyman (official, 2026-07-23): "MAI-Voice-2-Flash launches
  today! 2x faster than MAI-Voice-2 and 32% cheaper, at $15 per 1M
  characters." Powers **Dynamics 365 Contact Center**, cutting GPU cost
  up to **89%** per Suleyman's post. Same announcement window as
  [[microsoft-mai-image-2-5-pro-2026-07]] but a distinct product line
  (voice, not image) — tracked separately. Official, single-post primary
  source with concrete pricing and a named production surface (Dynamics
  365) → status `released` (launched today, live pricing, shipping into
  a named product), verification `confirmed`.
expected: null
labels:
  - microsoft-ai
  - voice
  - dynamics-365
  - released
verification: confirmed
sources:
  - "@mustafasuleyman"
created_at: 2026-07-27
updated_at: 2026-07-27
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-27
    change: "Created — @mustafasuleyman announced MAI-Voice-2-Flash launching 2026-07-23: 2x faster than MAI-Voice-2, 32% cheaper at $15/1M characters, powers Dynamics 365 Contact Center with up to 89% GPU cost reduction. Official primary source, concrete pricing + named production surface → status released, verification confirmed."
---

**Mustafa Suleyman** announced (official, 2026-07-23) the launch of
**MAI-Voice-2-Flash**, a faster and cheaper voice model in Microsoft
AI's MAI-Voice line.

**Specs, per the announcement:**
- **2x faster** than MAI-Voice-2.
- **32% cheaper** — **$15 per 1M characters**.
- Powers **Dynamics 365 Contact Center**, cutting GPU cost by up to
  **89%**.

**Why `released` / `confirmed`.** The announcement is official, dated,
carries concrete pricing, and names a live production surface (Dynamics
365 Contact Center) it already powers — clearing the bar for `released`
on a single primary post.

**Why its own ticket.** Announced the same window as
[[microsoft-mai-image-2-5-pro-2026-07]] (MAI-Image-2.5-Pro) but a
distinct product line (voice vs. image) — tracked separately per the
"same shipping artifact" dedup rule.

**Transition triggers:**
- Broader availability (MAI Playground, Foundry, Copilot) or a
  benchmark/model-card disclosure → UPDATE.
- ≥4 weeks past launch with no further movement → `closed:
  released-and-aged`.

**Dedup note:** further MAI-Voice-2-Flash signal UPDATES this ticket.
MAI-Image-2.5-Pro stays on
[[microsoft-mai-image-2-5-pro-2026-07]]; the original MAI-Image-2.5
(Preview) stays closed at [[microsoft-mai-image-2-5]].
