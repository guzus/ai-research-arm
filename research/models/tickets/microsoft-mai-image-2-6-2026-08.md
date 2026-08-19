---
slug: microsoft-mai-image-2-6-2026-08
title: Microsoft MAI-Image-2.6 — 3rd on Image Arena, private preview in Foundry
company: Microsoft AI
model: MAI-Image-2.6
status: in-testing
status_note: |
  **MAI-Image-2.6 scored 3rd on Image Arena and is available on MAI
  Playground and Microsoft Foundry in private preview** (@testingcatalog,
  2026-08-18 20:43 UTC, with a screenshot).

  `in-testing` rather than `released` because private preview is gated
  access, not public availability. `verification` is `confirmed` — the
  leaderboard placement and the Foundry listing are both checkable
  artifacts — but the reporting is a single (reliable) account and no
  Microsoft AI post was captured in-window.

  Continues Microsoft AI's homegrown-image cadence: MAI-Image-2.5 hit #3 on
  the Text-to-Image Arena in May ([[microsoft-mai-image-2-5]], closed) and
  MAI-Image-2.5-Pro entered Foundry preview in July
  ([[microsoft-mai-image-2-5-pro-2026-07]]). Same #3 slot, one version
  later — the ladder is holding position rather than climbing.
expected: "Private preview on MAI Playground + Microsoft Foundry as of 2026-08-18. Pending: public/GA availability, pricing, and a Microsoft AI on-record announcement"
labels:
  - microsoft
  - image-generation
  - private-preview
  - in-house-model
verification: confirmed
sources:
  - "@testingcatalog"
created_at: 2026-08-19
updated_at: 2026-08-19
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-19
    change: "Created — @testingcatalog (2026-08-18 20:43 UTC, with screenshot) reports MAI-Image-2.6 scored 3rd on Image Arena and is live on MAI Playground and Microsoft Foundry in private preview. Status in-testing (gated preview, not public); verification confirmed (checkable leaderboard placement plus a Foundry listing), though only one account reported it and no Microsoft AI post was captured. Successor to [[microsoft-mai-image-2-5-pro-2026-07]] and the closed [[microsoft-mai-image-2-5]] — same #3 Arena slot one version later."
---

**MAI-Image-2.6** is Microsoft AI's latest in-house image model, reported
**3rd on Image Arena** and live in **private preview** on **MAI Playground**
and **Microsoft Foundry** as of **2026-08-18**.

**Why it gets its own ticket.** House convention already splits this line
by version — [[microsoft-mai-image-2-5]] (closed) and
[[microsoft-mai-image-2-5-pro-2026-07]] are separate tickets — and 2.6 is a
distinct shipping artifact with its own Arena placement and its own preview
gate. Folding it into the 2.5-Pro ticket would lose the version boundary
that makes the cadence readable.

**The interesting read is the flat placement.** MAI-Image-2.5 took **#3 on
the Text-to-Image Arena** in May. MAI-Image-2.6 takes **#3 on Image Arena**
in August. Two versions and three months later, Microsoft's in-house image
model is in the same slot. That is either a stable competitive position or
a stalled one, and the Arena row alone cannot tell you which — what would
is who is above it now versus then.

**Status reasoning.** Private preview means gated access, which is
`in-testing`, not `released`. `verification` is `confirmed` anyway because
both claims are artifacts a third party can check (a leaderboard row and a
Foundry listing), not a characterisation — but note this rests on one
account's screenshot with no Microsoft AI post captured in-window.

**Transition triggers:**
- Public availability / GA on Foundry, or pricing → UPDATE, advance to
  `released`.
- A Microsoft AI on-record announcement → UPDATE.
- Superseded by a 2.7 / 3.0 → new ticket; do not reopen.
- ≥4 weeks past GA, settled into normal coverage →
  `closed: released-and-aged`.

**Dedup note:** other Microsoft AI in-house models stay on their own
tickets — [[microsoft-mai-voice-2-flash-2026-07]],
[[microsoft-mai-cyber-1-flash-2026-07]], [[microsoft-mai-code-1-flash]].
Further MAI-Image-2.6 signal UPDATES this ticket.
