---
slug: google-gemini-spark-computer-use-2026-08
title: Gemini Spark gains Computer Use on the Gemini Desktop app
company: Google / DeepMind
model: Gemini Spark
status: in-testing
status_note: |
  **2026-09-24 — still in closed testing, now with permission controls
  and a voice path.** @testingcatalog (12:07 UTC): "It seems like the upcoming
  Gemini Task mode on Gemini desktop will support Gemini Live as well. Users will
  likely be able to control Gemini Tasks by voice. The **Computer Use feature also
  got more granular settings, letting users configure whitelisted and blocked
  apps**. These features already undergo closed testing, and we may see them
  announced soon."

  **The permission model is the substantive change.** Per-app allow/deny lists
  are what a computer-use agent needs before it can be given to consumers at all
  — it is the difference between a demo and a product with a blast radius you can
  bound. Its appearance is a better leading indicator of an imminent launch than
  any capability demo would be.

  **The Gemini Live tie-in is a second, weaker claim.** Voice-driving Tasks would
  connect this to the now-GA 3.8 Live stack
  ([[google-gemini-3-8-live-2026-09]]); @testingcatalog hedges it with "seems
  like" and "likely", and it is recorded at that strength.

  **Status holds at `in-testing`, 37 days after the first sighting**, with still
  no Google announcement, rollout date, plan gating or documentation. Same single
  outlet as the original entry — this refreshes the ticket, it does not add an
  independent source.

  **Computer Use has been spotted in testing on the Gemini Desktop app**
  (@testingcatalog, 2026-08-18 15:39 UTC): **Gemini Spark will be able to
  control other apps and access selected folders**, arriving alongside an
  **Advanced Backup** option that lets Gemini back up files to Google Drive
  **before modifying them**.

  Status is `in-testing` because the claim is a build artifact observed in
  a shipping desktop app, not a prediction. Verification is `partial`: one
  reliable leaker, no Google post, no availability date, no docs.

  The Advanced Backup detail is the substantive part. Every agent vendor
  shipping filesystem write access this year has had to answer "what
  happens when it is wrong"; pre-modification snapshotting to Drive is a
  concrete answer and a differentiator Google is uniquely placed to ship.
expected: "TBD — still no Google announcement, rollout date, plan gating or documentation, 37 days after the first sighting. As of 2026-09-24 the feature remains in closed testing and has gained per-app whitelist/blocklist settings; a Gemini Task mode on desktop is reported as likely to support voice control via Gemini Live. Watch for a DeepMind/Google post or a staged consumer rollout."
labels:
  - google
  - gemini
  - computer-use
  - agentic
  - leak
verification: partial
sources:
  - "@testingcatalog"
  - https://x.com/testingcatalog/status/2103094052409250062
created_at: 2026-08-19
updated_at: 2026-09-25
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-19
    change: "Created — @testingcatalog (2026-08-18 15:39 UTC) reports Computer Use spotted in testing on the Gemini Desktop app: Gemini Spark will be able to control other apps and access selected folders, alongside an Advanced Backup option that backs files up to Google Drive before Gemini modifies them. Status in-testing (an artifact observed in a shipping app, not a prediction); verification partial (single reliable leaker, no Google statement, date or docs). Extends the closed [[gemini-spark]] and [[gemini-3-5-flash-computer-use-2026-06]] threads from the desktop side rather than reopening either."
  - ts: 2026-09-25
    change: "In-testing, unchanged, refreshed after 37 days. @testingcatalog (2026-09-24 12:07 UTC, ~445 likes) reports that Computer Use 'got more granular settings, letting users configure whitelisted and blocked apps', that an upcoming Gemini Task mode on Gemini desktop will likely support Gemini Live so Tasks can be voice-controlled, and that both features 'already undergo closed testing'. The per-app allow/deny permission model is treated as the substantive development: bounded blast radius is the precondition for shipping a computer-use agent to consumers at all, so its appearance is a stronger leading indicator of launch than any capability demo. The Gemini Live tie-in is recorded at the weaker strength its source gives it ('seems like', 'likely') and would connect this to the now-GA 3.8 Live stack ([[google-gemini-3-8-live-2026-09]]) if it holds. Explicitly noted: this is the SAME single outlet as the original 2026-08-19 sighting, so it refreshes recency without adding an independent source, and verification stays partial. Still no Google announcement, rollout date, plan gating or documentation."
  - ts: 2026-09-25
    change: "Bookkeeping — citation added for the 2026-09-25 entry: @testingcatalog (Computer Use gains per-app whitelist/blocklist settings; Gemini Task mode on desktop likely to support Gemini Live voice control; both still in closed testing). Same outlet as the original sighting, so recency refreshes but the source count does not. No status, verification or content change."
---

Google is wiring **Computer Use** into **Gemini Spark on the desktop**.
Per @testingcatalog, a build of the Gemini Desktop app shows Spark able to
**control other applications** and **access selected folders**, shipping
alongside an **Advanced Backup** option that snapshots files to Google
Drive **before** Gemini modifies them.

**Why this is not a duplicate of the existing Gemini computer-use work.**
[[gemini-3-5-flash-computer-use-2026-06]] (closed) covered Computer Use as
a **native built-in tool in the model/API**. [[gemini-spark]] (closed)
covered Spark shipping as the first GA paid persistent consumer agent. This
is the third thing: the **consumer agent getting local machine control on
the desktop**, with local filesystem access. Different surface, different
risk profile, and it is the surface where computer-use capability actually
reaches non-developers.

**The backup detail is the design decision worth logging.** Filesystem
write access is where consumer agents break things irreversibly, and every
vendor has had to answer for it this year. Snapshotting to Drive before
modification is a real mitigation, and it is one Google can ship cheaply
because it already owns the storage — a structural advantage over agent
vendors who would have to build or rent it.

**Evidence is thin and honestly labelled.** One leaker, no Google post, no
date, no plan gating, no documentation. `in-testing` reflects that a build
artifact exists; `partial` reflects that only one source has seen it.

**Transition triggers:**
- Google/DeepMind announcement, docs, or a staged rollout → UPDATE,
  advance to `confirmed`/`released` and `verification: confirmed`.
- A second independent sighting → UPDATE `verification`.
- ≥15 cycles with no corroboration → `closed: stale-rumor-unverified`.

**Dedup note:** model/API-level computer use stays on
[[gemini-3-5-flash-computer-use-2026-06]] (closed); the Spark product
launch stays on [[gemini-spark]] (closed). Further desktop computer-use
signal UPDATES this ticket.
