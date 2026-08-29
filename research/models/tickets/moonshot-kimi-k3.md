---
slug: moonshot-kimi-k3
title: Moonshot AI's Kimi K3 spotted live-testing under codename "Kivine," not yet publicly shipped
company: Moonshot AI
model: Kimi K3
status: closed
status_note: |
  Testingcatalog reported Kimi K3 "teased officially" as of **2026-07-15
  22:38 UTC**; separately, **@AndrewCurran_** reports it live-testing in
  a model arena under the stealth codename **"Kivine,"** with early
  tester reports putting it close to parity with **Fable 5**. Distinct
  artifact from the older **Kimi K2.7 Code** model tracked at
  [[moonshot-kimi-k2-7-code]] — do not conflate.

  **2026-07-21:** Now clearly public and live — Moonshot's own
  @Kimi_Moonshot account announced pausing *new* subscriptions (existing
  members unaffected) because demand pushed close to capacity limits over
  the prior 48h, and said membership will split into separate "Kimi
  Membership" and "Kimi Code Membership" plans. A subscription product
  that has to pause new signups due to demand is by definition released
  and in the hands of the public → advancing status to `released`.

  **2026-07-22:** Further corroboration and spec detail, no status change.
  @ryqwzrbuilds relays Moonshot's own framing: Kimi K3 is a **2.8T-parameter**
  open model, available through Moonshot's apps/API now, with **full weights
  due 2026-07-27** — i.e. today's app/API availability is not yet the full
  open-weights release. Epoch AI (via @rohanpaul_ai, @scaling01/@EpochAIResearch
  RT) reports K3 scored **156 on the Epoch Capabilities Index (ECI)**, a new
  open-weights record, placing it between **Claude Opus 4.6 and GPT-5.4** on
  that index — @rohanpaul_ai separately notes it ranks 2nd in agentic
  knowledge work on the AA-Briefcase benchmark, very near Fable 5, though at
  ~$10.57/task (roughly 10x K2.6's cost, above Opus). @theinformation reports
  **Microsoft is evaluating whether K3 could power Copilot features**
  previously handled by OpenAI/Anthropic models — internal testing only, no
  release date, region, or pricing announced (also relayed by
  @Awesome_AI_News). A JPMorgan research note (via @AlphaWireNewsAi) frames
  K3's launch as re-rating Zhipu AI's competitive narrative. Status stays
  `released`; verification stays `confirmed` (Moonshot's own weights-date
  framing + multiple independent benchmark/press relays).

  **2026-07-27 — full open-weights drop, as scheduled.** The full weights
  release Moonshot flagged for today materialized: a **2.8T-parameter MoE**
  model (16 of 896 experts active per token), **1M-token context**, native
  vision, released under a **Modified MIT license**, ~594GB of native
  weights, with vLLM day-0 support in prep (@johnseach, detailed technical
  post). Light independent corroboration: @_A_Radwan_ ("1300+ camped on the
  countdown") and a Chinese-platform weekly roundup already listing K3 live
  on its Web Chat. No official @Kimi_Moonshot capture of the weights drop
  itself in this window — entirely third-party, though detailed and
  internally consistent. Status stays `released` (already released via
  app/API since 07-21); verification stays `confirmed`.

  **2026-07-28 — license terms, pricing, and third-party benchmark rank.**
  The 07-27 weights drop is now more precisely documented: licensing is a
  bespoke **"Kimi K3 License"** (not plain Modified MIT as first relayed) —
  MaaS providers with >$20M trailing-12mo revenue need a separate Moonshot
  agreement, and large products must display the "Kimi K3" name. API
  pricing published at **$0.30 / $3 / $15 per Mtok** (cache-hit / input /
  output). Artificial Analysis' Intelligence Index scores it **57**,
  #1 among open-weight models — ahead of GLM-5.2 (51) and DeepSeek V4 Pro
  (44). Day-0 third-party hosting confirmed from Baseten, Nebius, Vercel AI
  Gateway, and Dell (on-prem). Status stays `released`; verification stays
  `confirmed` (Moonshot's own HF/GitHub release plus ~15 independent
  corroborating accounts).
expected: null
labels:
  - china
  - coding
verification: confirmed
sources:
  - "@testingcatalog"
  - https://x.com/testingcatalog/status/2077523332883231016
  - "@AndrewCurran_"
  - https://x.com/AndrewCurran_/status/2077433196556554306
  - https://x.com/Kimi_Moonshot/status/2078855608565207130
  - "@ryqwzrbuilds"
  - "@rohanpaul_ai"
  - "@EpochAIResearch"
  - "@theinformation"
created_at: 2026-07-16
updated_at: 2026-08-23
closed_at: 2026-08-23
closed_reason: released-and-aged
history:
  - ts: 2026-07-16
    change: "Created — Testingcatalog reported Kimi K3 'teased officially' (2026-07-15 22:38 UTC); @AndrewCurran_ separately reports it live-testing in a model arena under stealth codename 'Kivine,' with early tester reports near-parity with Fable 5. Not yet publicly shipped as of the 2026-07-16 08:00 UTC cycle, continuing a multi-day rumor thread → status in-testing, verification partial (arena sighting + tease, no primary Moonshot statement)."
  - ts: 2026-07-21
    change: "Official @Kimi_Moonshot account announced pausing new subscriptions (existing members unaffected) after demand pushed close to capacity limits over the prior 48h, and announced membership will split into separate 'Kimi Membership' and 'Kimi Code Membership' plans. Widely re-shared (@deedydas, @GavinSBaker, @quxiaoyin, @testingcatalog). A capacity-constrained, oversubscribed paid product is definitionally public and shipped → status advanced from in-testing to released; verification advanced to confirmed (official company account, primary source)."
  - ts: 2026-07-22
    change: "Corroboration + specs, no status change. Moonshot's own framing (relayed by @ryqwzrbuilds): 2.8T-parameter open model, apps/API live now, full weights due 2026-07-27. Epoch AI: 156 on the Epoch Capabilities Index, a new open-weights record, between Claude Opus 4.6 and GPT-5.4 (via @rohanpaul_ai/@EpochAIResearch RT); separately 2nd on the AA-Briefcase agentic benchmark, near Fable 5, at ~$10.57/task (~10x K2.6's cost, above Opus). @theinformation: Microsoft is evaluating K3 for Copilot features previously handled by OpenAI/Anthropic models (internal testing only, no release date/pricing). A JPMorgan note frames K3 as re-rating Zhipu AI's competitive narrative (@AlphaWireNewsAi). Status stays released; verification stays confirmed."
  - ts: 2026-07-27
    change: "Full open-weights drop, as scheduled. 2.8T-param MoE (16/896 experts active), 1M context, native vision, Modified MIT license, ~594GB native weights, vLLM day-0 support in prep (@johnseach). Light independent corroboration (@_A_Radwan_, a CN-platform weekly roundup listing K3 live). No official @Kimi_Moonshot capture of the weights drop itself in this window — entirely third-party, though detailed and internally consistent. Status stays released; verification stays confirmed."
  - ts: 2026-07-28
    change: "License, pricing, and rank detail. Licensing clarified as a bespoke 'Kimi K3 License' (>$20M/12mo-revenue MaaS providers need a separate Moonshot agreement; must display the 'Kimi K3' name) rather than plain Modified MIT. API pricing published: $0.30/$3/$15 per Mtok. Artificial Analysis Intelligence Index: 57, #1 open-weight (ahead of GLM-5.2 at 51, DeepSeek V4 Pro at 44). Day-0 hosting confirmed: Baseten, Nebius, Vercel AI Gateway, Dell on-prem. Status stays released; verification stays confirmed."
  - ts: 2026-08-23
    change: "Closed — released-and-aged. Kimi K3 shipped in mid-July and had licensing, pricing ($0.30/$3/$15 per Mtok), Artificial Analysis Intelligence Index 57 (#1 open-weight at the time) and day-0 hosting all resolved by the 2026-07-28 update; @teortaxesTex (2026-08-23) refers to it as having been 'released 5 weeks ago,' putting it past the >=4-week trigger. It remains an active reference point rather than a forgotten model — @emollick benchmarks the unattributed [[stealth-ox-alpha-model-2026-08]] against it and rates K3 higher on his shader test — but that is normal coverage. The successor signal is a separate artifact: @kimmonismus (2026-08-21) relays that 'Kimi k3.1 also incoming,' which is a zero-artifact single-relay claim and will get its own ticket when an artifact appears. Moonshot's other open tickets ([[moonshot-funding-2026-06]], [[moonshot-claude-distillation-us-scrutiny-2026-07]]) are unaffected. History preserved."
---

**Moonshot AI's** next flagship coding/reasoning model, **Kimi K3**, is
being live-tested in a model arena under the stealth codename
**"Kivine"** — reported by **@AndrewCurran_**, with early tester reports
placing it close to parity with **Fable 5**. Separately, **Testingcatalog**
reported the model "teased officially" as of 2026-07-15 22:38 UTC.

**Why tracked.** An arena sighting under a stealth codename plus an
official tease is a concrete artifact (real inference traffic in a
public arena), clearing the bar for `in-testing` even though Moonshot
has not shipped or announced K3 through its own primary channels yet.

**Corroboration read.** Two independent accounts (Testingcatalog,
AndrewCurran_) report converging but not identical signal — a tease and
an arena sighting — within the same news cycle. No Moonshot AI primary
statement, model card, or API listing yet, so `verification: partial`
rather than `confirmed`.

**Not yet shipped.** As of the 2026-07-16 08:00 UTC cycle, K3 remains
unreleased — this continues a multi-day rumor thread; earlier
expectations (kimmonismus, dejavucoder) pointed to a 2026-07-15/16
release window that has not materialized.

**Dedup note:** this ticket tracks the **Kimi K3** artifact
specifically. It is a distinct model from the older **Kimi K2.7 Code**
release tracked at [[moonshot-kimi-k2-7-code]] — do not conflate the
two; further K2.7 Code signal stays on that ticket.

**Transition triggers:**
- Moonshot AI's own account or blog confirms "Kivine" = Kimi K3, or
  publishes a model card → UPDATE, advance `status` to `confirmed`.
- Public API/weights release → UPDATE, advance `status` to `released`.
- If the rumor goes 15+ daily cycles with no further corroboration →
  close with `closed_reason: stale-rumor-unverified`.
