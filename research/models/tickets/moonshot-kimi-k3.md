---
slug: moonshot-kimi-k3
title: Moonshot AI's Kimi K3 spotted live-testing under codename "Kivine," not yet publicly shipped
company: Moonshot AI
model: Kimi K3
status: released
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
expected: "Shipped; membership plans splitting into 'Kimi Membership' and 'Kimi Code Membership'; new subscriptions temporarily paused for capacity; full open weights due 2026-07-27"
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
polymarket:
  - event_slug: moonshot-publishes-kimi-k3-weights-by-july-27-20260717164254847
    market_id: "2962189"
    token_id: "75115059341633093064218172577665054472726102773501095008666040339558881159279"
    question: "Moonshot publishes Kimi K3 weights by July 27?"
    outcome: "Jul 27 2026"
created_at: 2026-07-16
updated_at: 2026-07-23
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-16
    change: "Created — Testingcatalog reported Kimi K3 'teased officially' (2026-07-15 22:38 UTC); @AndrewCurran_ separately reports it live-testing in a model arena under stealth codename 'Kivine,' with early tester reports near-parity with Fable 5. Not yet publicly shipped as of the 2026-07-16 08:00 UTC cycle, continuing a multi-day rumor thread → status in-testing, verification partial (arena sighting + tease, no primary Moonshot statement)."
  - ts: 2026-07-21
    change: "Official @Kimi_Moonshot account announced pausing new subscriptions (existing members unaffected) after demand pushed close to capacity limits over the prior 48h, and announced membership will split into separate 'Kimi Membership' and 'Kimi Code Membership' plans. Widely re-shared (@deedydas, @GavinSBaker, @quxiaoyin, @testingcatalog). A capacity-constrained, oversubscribed paid product is definitionally public and shipped → status advanced from in-testing to released; verification advanced to confirmed (official company account, primary source)."
  - ts: 2026-07-22
    change: "Corroboration + specs, no status change. Moonshot's own framing (relayed by @ryqwzrbuilds): 2.8T-parameter open model, apps/API live now, full weights due 2026-07-27. Epoch AI: 156 on the Epoch Capabilities Index, a new open-weights record, between Claude Opus 4.6 and GPT-5.4 (via @rohanpaul_ai/@EpochAIResearch RT); separately 2nd on the AA-Briefcase agentic benchmark, near Fable 5, at ~$10.57/task (~10x K2.6's cost, above Opus). @theinformation: Microsoft is evaluating K3 for Copilot features previously handled by OpenAI/Anthropic models (internal testing only, no release date/pricing). A JPMorgan note frames K3 as re-rating Zhipu AI's competitive narrative (@AlphaWireNewsAi). Status stays released; verification stays confirmed."
  - ts: 2026-07-23
    change: "Linked Polymarket odds (metadata-only, no status change): 'Moonshot publishes Kimi K3 weights by July 27?' (event moonshot-publishes-kimi-k3-weights-by-july-27-20260717164254847, market 2962189, Gamma snapshot ~92% Yes). Resolution requires complete official K3 weights to be publicly downloadable—API-only, partial, converted, or third-party weights do not count—exactly matching this ticket's remaining open-weights milestone; IDs read from the Gamma API."
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
