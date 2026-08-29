---
slug: spacex-cursor-acquisition-2026-06
title: SpaceX acquires Cursor (Anysphere) in ~$60B all-stock deal
company: SpaceX / Anysphere (Cursor)
model: null
status: confirmed
status_note: |
  SpaceX's **own verified account** confirmed (2026-06-16, ~22.4K likes) it has
  **"exercised the option to acquire @cursor_ai in an all-stock transaction"** —
  corroborated by Cursor's account and CEO **Michael Truell** ("joining forces
  with SpaceX"). SpaceX also disclosed that **SpaceXAI has spent months jointly
  training a model with Cursor** (tracked separately on
  [[cursor-spacexai-model-2026-06]]). The **~$60B all-stock figure and Q3-2026
  close** rest on an **SEC-filing reference relayed by aggregators**
  (@testingcatalog, @kimmonismus), not the filing read directly — so the
  acquisition itself is confirmed (principals on-record) but the price/structure
  stay `partial`. At the same Compile event Cursor also announced **Origin**, a
  git-hosting "forge for the agentic era" (waitlist, fall 2026) aimed at GitHub.
expected: "All-stock, ~$60B (per an SEC-filing reference). The Information reported 2026-08-25 that the acquisition has CLOSED and that Musk told Cursor employees 'Grok is falling behind, we need you guys to come in and help us' and that 'Anthropic is leading right now'. Pending: a SpaceX or Cursor post confirming the close, integration detail, and whether the jointly-trained model ([[cursor-spacexai-model-2026-06]]) ships"
labels:
  - acquisition
  - m-and-a
  - coding
  - spacex
verification: partial
sources:
  - "@SpaceX"
  - "@cursor_ai"
  - "@mntruell"
  - "@testingcatalog"
  - "@kimmonismus"
  - "@theinformation"
  - "@graceihle"
created_at: 2026-06-18
updated_at: 2026-08-26
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-18
    change: "Created — SpaceX's own verified account confirmed (2026-06-16) it 'exercised the option to acquire @cursor_ai in an all-stock transaction,' corroborated by Cursor's account and CEO Michael Truell; SpaceX disclosed SpaceXAI has been jointly training a model with Cursor (see [[cursor-spacexai-model-2026-06]]). The ~$60B all-stock figure and Q3-2026 close rest on an SEC-filing reference relayed by aggregators, not read directly → status confirmed (principals on-record), verification partial (price/structure aggregator-relayed). Cursor also unveiled Origin (git hosting, fall-2026 waitlist) at the same Compile event."
  - ts: 2026-08-26
    change: "The deal has closed, and the acquirer's address to the acquired staff reframes the rationale. @theinformation (2026-08-25 21:43 UTC): 'Elon Musk addressed Cursor employees after SpaceX's acquisition of the company closed. He said \"Grok is falling behind, we need you guys to come in and help us.\" \"He outlined the stakes, basically, that Anthropic is leading right now.\"' A second Information post (19:00 UTC) adds that Musk told employees he 'isn't used to losing' and frames the $60 billion acquisition as a bet on closing the gap, reported by @graceihle. Two things change. First, the Q3-2026 close this ticket carried as an expectation is now reported as done - the acquisition is complete, not pending. Second, the stated motive is a competitive deficit rather than the joint-training synergy framing the principals used in June: the acquirer is on record, via reporting, that its own model line is behind, and specifically behind Anthropic. @Jessicalessin puts the deal alongside Stripe's $7B+ OpenRouter purchase ([[stripe-openrouter-acquisition-2026-08]]) as evidence of what big tech now pays for AI growth, and The Information independently carries the ~$60B figure this ticket had only through aggregator relay of an SEC-filing reference. Status stays confirmed; verification stays partial - the close and the quotes are single-outlet, with no SpaceX or Cursor post captured."
---

On **2026-06-16**, **SpaceX's own verified account** posted that it has
**"exercised the option to acquire @cursor_ai in an all-stock transaction
with the goal of building the world's most useful AI models,"** and
disclosed that **"for the past few months, SpaceXAI has been jointly
training a model with Cursor, which will be released… soon."** Cursor's
official account and CEO **Michael Truell** separately confirmed the
tie-up.

**Why its own ticket.** This is a discrete **M&A event** — the class this
timeline tracks alongside releases, funding, and legal actions. The
**jointly-trained frontier-scale model** SpaceX referenced is a distinct
shipping artifact and is tracked on
[[cursor-spacexai-model-2026-06]]; this ticket carries the **acquisition
itself**.

**Confirmed vs. reported.** The acquisition is confirmed by all
principals on-record (SpaceX, Cursor, Truell), which kills the earlier
"this is satire" reading and explains the odd "exercised the option"
phrasing (a pre-existing SpaceXAI/Cursor training partnership). What
stays `partial`: the **~$60B all-stock price and Q3-2026 close** ride on
an **SEC-filing reference relayed by aggregators** (@testingcatalog,
@kimmonismus), not the filing read directly. Various "SpaceX compute
landlord / $2B-a-month" threads circulating are analyst reconstructions,
not disclosed financials.

**Context.** Application-layer consolidation while the model layer is in
upheaval (Anthropic's frontier models sit export-embargoed —
[[anthropic-fable-mythos-export-control-2026-06]]), and a route for
Musk's stack to stop depending on rivals' models. At the same Compile
event Cursor announced **Origin**, a code-storage / git-hosting platform
"for the agentic era," putting it in direct competition with
Microsoft-owned GitHub.

**Transition triggers:**
- The SpaceX/Anysphere SEC merger filing read directly (price, structure,
  close date) → UPDATE, advance `verification` to `confirmed`.
- Deal closes or is blocked/restructured → UPDATE; close once settled and
  rolled into normal coverage.
- ≥4 weeks of settled coverage after close → `closed: released-and-aged`.

**Dedup note:** signal about the *deal* (price, filing, regulatory
review, close) UPDATES this ticket. Signal about the *jointly-trained
model* stays on [[cursor-spacexai-model-2026-06]].
