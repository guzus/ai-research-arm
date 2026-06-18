---
slug: cursor-spacexai-model-2026-06
title: Cursor × SpaceXAI jointly-trained frontier coding model
company: SpaceX / Anysphere (Cursor)
model: Cursor/SpaceXAI model (unnamed)
status: in-testing
status_note: |
  At Cursor's **Compile** event (2026-06-16) CEO **Michael Truell** unveiled on
  stage the model **SpaceXAI and Cursor have been jointly training** — a
  frontier-scale system he described as **"as big as Opus and GPT,"** set to ship
  **inside Cursor and Grok Build**. Analyst @scaling01 pegs it at **1.5T+
  parameters pre-trained on 100k+ GPUs** (community reading, not a published
  model card). **No name, benchmarks, or ship date** yet; there is a real
  conflation risk with xAI's Grok 4.3 (also described as ~1.5T, Cursor-data
  trained). Existence and release path are event-confirmed (Truell on stage +
  SpaceX's own account); specs are community-relayed → verification `partial`.
expected: "Frontier-scale, 'as big as Opus and GPT' (~1.5T params / 100k+ GPUs per community); to ship in Cursor + Grok Build; no name/benchmarks/date yet"
labels:
  - frontier-model
  - coding
  - spacex
  - in-testing
verification: partial
sources:
  - "@SpaceX"
  - "@mntruell"
  - "@scaling01"
  - "@morganlinton"
created_at: 2026-06-18
updated_at: 2026-06-18
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-18
    change: "Created — at Compile (2026-06-16) Cursor CEO Michael Truell unveiled the SpaceXAI×Cursor jointly-trained model on stage, described as 'as big as Opus and GPT,' to ship in Cursor and Grok Build; SpaceX's own account named the same release path. @scaling01 pegs it at 1.5T+ params / 100k+ GPUs (community reading, not a model card). No name, benchmarks, or ship date; conflation risk with xAI Grok 4.3 → status in-testing (real on-stage artifact, not yet shipped), verification partial (specs community-relayed). Acquisition context on [[spacex-cursor-acquisition-2026-06]]."
---

At Cursor's **Compile** event on **2026-06-16**, CEO **Michael Truell**
unveiled on stage the frontier-scale model **SpaceXAI and Cursor have
been jointly training** for several months — the artifact SpaceX
referenced in its acquisition post
([[spacex-cursor-acquisition-2026-06]]). Truell described it on record as
**"as big as Opus and GPT,"** with the model set to be released **inside
Cursor and Grok Build**.

**Specs are soft.** Analyst **@scaling01** summarized it as a **"1.5T+
parameter model pre-trained on over 100k GPUs,"** but those numbers are
the analyst's reading, not a published Cursor model card — and there is a
genuine **conflation risk with xAI's Grok 4.3**, which prior commentary
also described as ~1.5T params trained on Cursor data. A search for an
official Compile model-card post returned nothing in-window.

**Why `in-testing` / `partial`.** The model's **existence and release
path are event-confirmed** (Truell on stage; the full reveal video
circulated by @morganlinton; SpaceX's own account names "Cursor and Grok
Build"). But it is **not yet publicly available** — no name, no
benchmarks, no ship date — so the lifecycle is `in-testing`, and the
capability/scale claims rest on one analyst's relay → `verification:
partial`.

**Transition triggers:**
- An official Cursor model card (name, size, evals) or public availability
  in Cursor/Grok Build → UPDATE, advance status toward `released` and
  `verification` to `confirmed`.
- Confirmation it is distinct from (or the same as) xAI Grok 4.3 → UPDATE
  the title/status_note accordingly (keep the slug).
- Contradicted/abandoned → close per `closed_reason`.

**Dedup note:** signal about the *model* (name, specs, benchmarks,
launch) UPDATES this ticket. Signal about the *acquisition* stays on
[[spacex-cursor-acquisition-2026-06]].
