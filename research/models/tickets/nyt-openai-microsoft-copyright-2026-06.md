---
slug: nyt-openai-microsoft-copyright-2026-06
title: NYT amends copyright complaint vs OpenAI/Microsoft — bespoke-supercomputer allegation
company: New York Times / OpenAI / Microsoft
model: null
status: confirmed
status_note: |
  Per the 2026-06-29 digest (Policy & Regulation), **The New York Times amended
  its copyright complaint** against OpenAI and Microsoft, newly alleging that
  **Microsoft built a bespoke supercomputer to help OpenAI infringe copyrights**
  — escalating the landmark NYT v. OpenAI/Microsoft case by directly implicating
  Microsoft's infrastructure role in the alleged training-data infringement. A
  discrete **legal action** (an amended complaint is an on-record court filing)
  → status `confirmed`; but in-window sourcing is a **single secondary digest
  line** with no captured primary docket / filing text → verification
  `partial`. The underlying allegations are the NYT's and unproven.
expected: "Pending: the amended complaint's docket/text, OpenAI/Microsoft response or motion to dismiss, and whether the bespoke-supercomputer allegation survives to discovery"
labels:
  - legal-action
  - copyright
  - openai
  - microsoft
  - nyt
verification: partial
sources:
  - "@nytimes"
created_at: 2026-06-29
updated_at: 2026-06-29
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-29
    change: "Created — The New York Times amended its copyright complaint against OpenAI and Microsoft, newly alleging Microsoft built a bespoke supercomputer to help OpenAI infringe copyrights (2026-06-29 digest, Policy & Regulation). Escalates the landmark NYT v. OpenAI/Microsoft case by implicating Microsoft's infrastructure role. A discrete legal-action event (amended complaint = on-record filing) → status confirmed; single secondary digest line without a captured primary docket/filing text → verification partial. Allegations are the NYT's and unproven."
---

The **New York Times amended its copyright complaint** against **OpenAI** and
**Microsoft**, newly alleging that **Microsoft built a bespoke supercomputer
specifically to help OpenAI infringe copyrights** — surfaced via the
2026-06-29 digest's Policy & Regulation section.

**Why its own ticket.** This is a discrete **legal action** — the event
class this timeline tracks alongside releases, funding, and acquisitions.
It is the latest escalation in the landmark **NYT v. OpenAI/Microsoft**
copyright suit, and the bespoke-supercomputer theory pulls Microsoft's
**infrastructure role** directly into the alleged training-data
infringement rather than leaving it a downstream model provider.

**Confirmed vs. unproven.** An amended complaint is an on-record court
filing, so the *event* is `confirmed`. The *allegations* are the NYT's and
**unproven**; OpenAI and Microsoft have not responded in-window. In-window
sourcing is a single secondary digest line with **no captured primary
docket or filing text**, so `verification: partial`.

**Why it matters.** AI training-data copyright is the central unsettled
legal question for the whole frontier-model industry; a theory that a
hyperscaler purpose-built compute to enable infringement, if it survives,
would broaden liability exposure beyond the model lab to its compute
partner.

**Transition triggers:**
- The amended complaint's docket/text, or an OpenAI/Microsoft response or
  motion to dismiss → UPDATE, advance `verification`.
- A ruling, settlement, or dismissal → UPDATE.
- Settles into normal coverage ≥4 weeks after resolution →
  `closed: released-and-aged`.

**Dedup note:** further signal about *this filing / the NYT case* UPDATES
this ticket. Other OpenAI legal matters stay on their own tickets
([[openai-florida-lawsuit-2026-06]], [[openai-state-ag-subpoena-2026-06]]).
