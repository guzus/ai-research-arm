---
slug: anthropic-google-datacenter-financing-2026-07
title: Anthropic-linked datacenter developer reportedly in advanced talks on $15B Google-backed financing
company: Anthropic / Google
model: null
status: rumored
status_note: |
  WSJ scoop (via journalist anissagardizy8, relayed by @AndrewCurran_):
  a datacenter developer (Nexus Data Centers) working with Anthropic is
  reportedly in **advanced talks** to borrow **$15B** to build a
  campus/power plant in Texas (Hubbard, TX), with **Google providing
  financial guarantees and TPUs**, and a **Morgan Stanley-led bank
  consortium** lending to Nexus. Explicitly framed as "in advanced talks"
  — not a signed/closed deal. Single-outlet (WSJ) sourcing relayed
  secondhand in this signal, no primary WSJ article or company statement
  captured directly → verification `partial`, status `rumored` pending
  a signed deal or primary confirmation.
expected: "Deal signing or an official Anthropic/Google/Nexus statement would advance this to confirmed; a completed financing close plus infrastructure buildout would move toward in-testing/confirmed on the compute-capacity side"
labels:
  - anthropic
  - google
  - compute
  - datacenter
  - financing
verification: partial
sources:
  - "@AndrewCurran_"
created_at: 2026-07-31
updated_at: 2026-07-31
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-31
    change: "Created — WSJ scoop (relayed by @AndrewCurran_): a datacenter developer (Nexus Data Centers) working with Anthropic reportedly in advanced talks to borrow $15B to build a campus/power plant in Hubbard, TX, with Google providing financial guarantees and TPUs, and a Morgan Stanley-led bank consortium lending to Nexus. Explicitly 'in advanced talks,' not finalized; single-outlet sourcing relayed secondhand → status rumored, verification partial."
---

A **datacenter developer (Nexus Data Centers)** reportedly working with
**Anthropic** is said to be in **advanced talks** to borrow **$15B** to
build a large campus/power plant in **Hubbard, Texas**, with **Google**
providing financial guarantees and supplying **TPUs**, and a
**Morgan Stanley-led bank consortium** providing the lending. The report
traces to a **WSJ scoop** relayed via journalist anissagardizy8 and
amplified by @AndrewCurran_.

**Why tracked.** This would be a significant compute-infrastructure event
for Anthropic's roadmap — consistent with this ticket set's existing
practice of tracking Anthropic's compute deals
([[anthropic-micron-supply-2026-06]], [[anthropic-spacex-colossus-2026-05]])
and Google's compute partnerships ([[google-spacex-compute-2026-06]]).

**Why `rumored` / `partial`.** The story is specific (named developer,
dollar figure, location, named financing structure) but traces to a
single outlet relayed secondhand in this signal, and is explicitly
described as "advanced talks" rather than a signed deal.

**Transition triggers:**
- A signed/closed financing deal, or a primary Anthropic/Google/Nexus
  statement → UPDATE, advance status toward `confirmed`.
- The talks fall through or are denied → UPDATE, consider closure.
- ≥15 cycles with no fresh corroboration → `closed: stale-rumor-unverified`.

**Dedup note:** further signal on this specific financing deal UPDATES
this ticket. Other Anthropic/Google compute deals stay on their own
tickets.
