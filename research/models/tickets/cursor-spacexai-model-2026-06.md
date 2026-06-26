---
slug: cursor-spacexai-model-2026-06
title: Cursor × SpaceXAI jointly-trained frontier coding model — now named Composer 3
company: SpaceX / Anysphere (Cursor)
model: Composer 3
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

  **2026-06-26:** The model acquired a name and firmed specs. Cursor is shipping
  **Composer 3** — a **1.5T-parameter model trained from scratch on xAI's
  Colossus** (100K+ NVIDIA GPUs in Memphis), described as **Cursor's first fully
  self-built model with no third-party base**, to ship **"within weeks"**
  (@mycomradio relay). The 1.5T / 100k+-GPU / Colossus / ships-in-Cursor shape
  matches the Compile unveil, so Composer 3 is the apparent name of the
  jointly-trained model — and "Cursor's first fully self-built model" helps
  **disambiguate it from xAI's Grok 4.3** (the prior conflation risk). Still no
  official Cursor model card (name, size, evals) or firm ship date, and the
  "within weeks" timing + specs are a single relay → status stays `in-testing`,
  verification stays `partial`.
expected: "Now named Composer 3: 1.5T params trained from scratch on xAI's Colossus (100K+ NVIDIA GPUs, Memphis), Cursor's first fully self-built model (no third-party base), ships 'within weeks' in Cursor + Grok Build. Still no official model card (evals) or firm ship date; specs single-relayed → verification partial"
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
  - "@mycomradio"
created_at: 2026-06-18
updated_at: 2026-06-26
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-18
    change: "Created — at Compile (2026-06-16) Cursor CEO Michael Truell unveiled the SpaceXAI×Cursor jointly-trained model on stage, described as 'as big as Opus and GPT,' to ship in Cursor and Grok Build; SpaceX's own account named the same release path. @scaling01 pegs it at 1.5T+ params / 100k+ GPUs (community reading, not a model card). No name, benchmarks, or ship date; conflation risk with xAI Grok 4.3 → status in-testing (real on-stage artifact, not yet shipped), verification partial (specs community-relayed). Acquisition context on [[spacex-cursor-acquisition-2026-06]]."
  - ts: 2026-06-26
    change: "Named + specs firmed: Cursor is shipping Composer 3 — a 1.5T-param model trained from scratch on xAI's Colossus (100K+ NVIDIA GPUs, Memphis), Cursor's first fully self-built model (no third-party base), ships 'within weeks' (@mycomradio relay). The 1.5T/100k+-GPU/Colossus/ships-in-Cursor shape matches the Compile unveil, so Composer 3 is the apparent name of the jointly-trained model; 'Cursor's first fully self-built model' disambiguates it from xAI Grok 4.3 (resolving the prior conflation risk toward Composer 3 = the Cursor-branded jointly-trained model). Title/model field updated to Composer 3 (slug unchanged). Still no official model card (evals) or firm ship date; specs single-relayed → status stays in-testing, verification stays partial."
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
