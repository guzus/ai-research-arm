---
slug: cursor-spacexai-model-2026-06
title: Cursor × SpaceXAI jointly-trained frontier coding model — now named Composer 3
company: SpaceX / Anysphere (Cursor)
model: Composer 3
status: in-testing
status_note: |
  **2026-09-24 — Musk puts a window on it, and it is a capability claim
  rather than a ship date.** Relayed by @mark_k (17:38 UTC): Elon Musk says
  **SpaceXAI could have a model at Fable or GPT-6 level within 2 to 3 months**,
  and that he is "cautiously optimistic" — which puts the target around end of
  2026. Separately (relayed @StragglerLiu, 2026-09-25) Musk argued xAI's effort
  is only three years old against Anthropic's six and OpenAI's ten, and that if
  the second derivative holds, SpaceX reaches "pole position in about six
  months".

  **Note what moved and what did not.** The previous entry had Composer 3 named,
  specced at 1.5T parameters, and shipping "within weeks" in Cursor and Grok
  Build. Today's claim is a *capability parity* target 2-3 months out. Those are
  not the same statement, and the gap between "ships within weeks" and "reaches
  frontier parity in 2-3 months" is either a scope split between shipping and
  matching, or slippage. Nothing in-window resolves which.

  **Still absent, for the fourth consecutive update:** a model card, any
  benchmark, any pricing, and a firm ship date. Status holds at `in-testing`.

  **Source-quality note.** These are principal statements from the funder, which
  is a strong source class for intent and a weak one for delivery. Musk's
  published timelines are the relevant prior, and this ticket already carries one
  "within weeks" that has not landed.

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
expected: "Named Composer 3: 1.5T params trained from scratch on xAI's Colossus, Cursor's first fully self-built model, previously said to ship 'within weeks' in Cursor + Grok Build. Musk now (2026-09-24) targets Fable/GPT-6-level capability within 2-3 months, i.e. around end of 2026, and claims pole position in ~6 months. Still no model card, benchmark, pricing or firm ship date; specs remain single-relayed."
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
  - https://x.com/troyluhman/status/2102839041737867638
  - https://x.com/eric_luhman1/status/2102838938016862448
  - https://x.com/mark_k/status/2103082138417700890
  - https://x.com/elonmusk/status/2102839221593710678
  - https://x.com/mark_k/status/2103177237835268482
  - https://x.com/StragglerLiu/status/2103422985180946706
created_at: 2026-06-18
updated_at: 2026-09-25
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-18
    change: "Created — at Compile (2026-06-16) Cursor CEO Michael Truell unveiled the SpaceXAI×Cursor jointly-trained model on stage, described as 'as big as Opus and GPT,' to ship in Cursor and Grok Build; SpaceX's own account named the same release path. @scaling01 pegs it at 1.5T+ params / 100k+ GPUs (community reading, not a model card). No name, benchmarks, or ship date; conflation risk with xAI Grok 4.3 → status in-testing (real on-stage artifact, not yet shipped), verification partial (specs community-relayed). Acquisition context on [[spacex-cursor-acquisition-2026-06]]."
  - ts: 2026-06-26
    change: "Named + specs firmed: Cursor is shipping Composer 3 — a 1.5T-param model trained from scratch on xAI's Colossus (100K+ NVIDIA GPUs, Memphis), Cursor's first fully self-built model (no third-party base), ships 'within weeks' (@mycomradio relay). The 1.5T/100k+-GPU/Colossus/ships-in-Cursor shape matches the Compile unveil, so Composer 3 is the apparent name of the jointly-trained model; 'Cursor's first fully self-built model' disambiguates it from xAI Grok 4.3 (resolving the prior conflation risk toward Composer 3 = the Cursor-branded jointly-trained model). Title/model field updated to Composer 3 (slug unchanged). Still no official model card (evals) or firm ship date; specs single-relayed → status stays in-testing, verification stays partial."
  - ts: 2026-07-21
    change: "Leak (@mark_k, quoting @LuminaXspace): a leaked Cursor checkpoint shows Composer 3 being tested under the internal codename 'Vega,' with fast/medium/high/xhigh reasoning tiers and six internal variants — suggesting public release may be imminent. Single-source leak, no official Cursor confirmation or ship date yet → status stays in-testing, verification stays partial."
  - ts: 2026-09-24
    change: "TALENT SIGNAL, no change to the model's status. Two senior ex-OpenAI researchers announced on 2026-09-23 that they have joined the Cursor/SpaceXAI effort, self-reported and therefore primary: @troyluhman ('excited to be starting a new role at Cursor/SpaceXAI! I will be working on long term research with @ellev3n11 and the amazing team here') and @eric_luhman1 ('excited to join the amazing team at @SpaceXAI'). @mark_k identifies them as the Luhman brothers, two former OpenAI engineers who worked on Sora — that attribution is a relay read, not self-stated, and is recorded as such. @elonmusk posted 'SpaceXAI' the same hour. Status stays IN-TESTING and verification stays partial: hiring is not shipping, and this ticket's open item is unchanged — Composer 3 still has no official Cursor model card, no evals, and no firm ship date, roughly two months after being described as shipping 'within weeks'. Logged because the hires are on LONG-TERM RESEARCH rather than the Composer 3 launch, which is weak evidence that the joint effort is being staffed as a durable lab rather than a one-model collaboration. Video-generation provenance is worth noting against [[katzenberg-ai-video-startup-2026-09]], which tracks a different ex-Sora departure."
  - ts: 2026-09-25
    change: "In-testing, unchanged, for the fourth consecutive update with no artifact. Elon Musk said SpaceXAI could have a model at Fable or GPT-6 level within 2 to 3 months and that he is 'cautiously optimistic' (relayed @mark_k, 2026-09-24 17:38 UTC, ~183 likes), putting the target around end of 2026; separately he argued xAI's effort is three years old against Anthropic's six and OpenAI's ten and that SpaceX reaches 'pole position in about six months' (relayed @StragglerLiu, 2026-09-25). The important observation is that this is a DIFFERENT claim from the one on file, not a refinement of it: the previous entry had Composer 3 named, specced at 1.5T parameters, and shipping 'within weeks' in Cursor and Grok Build, whereas today's is a capability-parity target 2-3 months out. 'Ships within weeks' and 'reaches frontier parity in 2-3 months' are either a deliberate split between shipping and matching, or slippage, and nothing in-window resolves which — recorded as unresolved rather than narrated as progress. Still absent: a model card, any benchmark, any pricing, any firm ship date. Source-quality note recorded explicitly: these are principal statements from the funder, strong evidence of intent and weak evidence of delivery, and this ticket already carries one unlanded 'within weeks'."
  - ts: 2026-09-25
    change: "Bookkeeping — citations added for the 2026-09-25 entry: @mark_k (Musk: SpaceXAI could have a Fable/GPT-6-level model within 2-3 months, 'cautiously optimistic') and @StragglerLiu (Musk's three-vs-six-vs-ten-years framing and the 'pole position in about six months' claim). No status, verification or content change."
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
