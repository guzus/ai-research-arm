---
slug: moonshot-kimi-k3
title: Moonshot AI's Kimi K3 spotted live-testing under codename "Kivine," not yet publicly shipped
company: Moonshot AI
model: Kimi K3
status: in-testing
status_note: |
  Testingcatalog reported Kimi K3 "teased officially" as of **2026-07-15
  22:38 UTC**; separately, **@AndrewCurran_** reports it live-testing in
  a model arena under the stealth codename **"Kivine,"** with early
  tester reports putting it close to parity with **Fable 5**. As of the
  2026-07-16 08:00 UTC cycle, still **not publicly shipped** — continuing
  a multi-day rumor thread. Distinct artifact from the older **Kimi K2.7
  Code** model tracked at [[moonshot-kimi-k2-7-code]] — do not conflate.
expected: "Ship date unknown; kimmonismus and dejavucoder both expected a release around 2026-07-15/16 but it had not shipped as of the 08:00 UTC 2026-07-16 cycle"
labels:
  - rumored-release
  - china
  - coding
verification: partial
sources:
  - "@testingcatalog"
  - https://x.com/testingcatalog/status/2077523332883231016
  - "@AndrewCurran_"
  - https://x.com/AndrewCurran_/status/2077433196556554306
created_at: 2026-07-16
updated_at: 2026-07-16
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-16
    change: "Created — Testingcatalog reported Kimi K3 'teased officially' (2026-07-15 22:38 UTC); @AndrewCurran_ separately reports it live-testing in a model arena under stealth codename 'Kivine,' with early tester reports near-parity with Fable 5. Not yet publicly shipped as of the 2026-07-16 08:00 UTC cycle, continuing a multi-day rumor thread → status in-testing, verification partial (arena sighting + tease, no primary Moonshot statement)."
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
