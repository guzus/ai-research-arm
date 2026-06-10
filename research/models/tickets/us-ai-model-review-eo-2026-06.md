---
slug: us-ai-model-review-eo-2026-06
title: Trump signs AI executive order — voluntary 30-day pre-release review of frontier models + Treasury cybersecurity clearinghouse
company: US Government / White House
model: null
status: confirmed
status_note: |
  President Trump signed an executive order on **2026-06-02 (Tuesday)**
  establishing a **voluntary** framework for government review of frontier
  AI models before public release. Under it, AI developers engage the
  government to determine whether a model under development is a "covered
  frontier model," then provide **up to 30 days** of pre-release access
  and collaborate on selecting "trusted partners" for early evaluation.
  Participation is explicitly voluntary — companies can decline without
  penalty. The order also directs creation of an **AI cybersecurity
  clearinghouse within 30 days**, coordinated by the Treasury Secretary,
  the National Cyber Director, the NSA, and CISA, to review
  vulnerabilities discovered by AI models. This is substantially narrower
  than the draft Trump scrapped on **2026-05-21** (which proposed a
  *mandatory* 90-day pre-release window and formal federal evaluation
  authority); David Sacks reportedly blessed the revised version after the
  review window was cut from 90 to 30 days. Matters to this lane because
  it directly touches the release cadence of every US frontier lab — see
  the voluntary-CAISI-partnership condition already noted on
  [[mythos-public-release]].
expected: "AI cybersecurity clearinghouse stand-up within 30 days (~by early July 2026, Treasury-coordinated); 'covered frontier model' criteria + trusted-partner list TBD"
labels:
  - regulation
  - executive-order
  - frontier-model-review
  - us-policy
  - cybersecurity
verification: confirmed
sources:
  - https://www.npr.org/2026/06/02/nx-s1-5844347/ai-safety-trump-executive-order
  - https://www.cnbc.com/2026/06/02/trump-executive-order-ai.html
  - https://www.theregister.com/ai-and-ml/2026/06/02/trump-ai-executive-order-sets-30-day-frontier-model-review/5250322
  - https://thenextweb.com/news/trump-signs-downsized-ai-executive-order-voluntary-review
  - https://federalnewsnetwork.com/cybersecurity/2026/06/ai-executive-order-sets-stage-for-new-cybersecurity-directives/
  - "@shashj"
created_at: 2026-06-03
updated_at: 2026-06-10
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-03
    change: "Created — Trump signed an executive order 2026-06-02 asking AI companies to voluntarily give the government up to 30 days of pre-release access to 'covered frontier models,' plus an AI cybersecurity clearinghouse (Treasury / National Cyber Director / NSA / CISA) to stand up within 30 days. Narrowed from the mandatory-90-day draft scrapped 2026-05-21; David Sacks reportedly assented once the window was cut to 30 days. Corroborated across NPR, CNBC, The Register, TNW, Federal News Network, plus a NYT-sourced summary in the bird signal"
  - ts: 2026-06-10
    change: "First implementation signal (single-source, secondary). @shashj reports that administration officials — including **National Cyber Director Sean Cairncross** — told the **Center for AI Standards and Innovation (CAISI)** to **halt publication of its model assessments** while this executive order is implemented. If accurate, it is the first concrete downstream effect of the EO on the model-evaluation pipeline: a pause on CAISI's public eval releases pending the new framework. Held to secondary/single-source pending corroboration on official channels; scope (all assessments vs. specific findings) and duration unstated. Status stays confirmed (the EO itself is unchanged); logged as an implementation development"
---

On **2026-06-02**, President Trump signed an executive order creating a
**voluntary** framework under which AI developers can give the federal
government early access to their most powerful models before public
release. It is the administration's most concrete step yet toward
regulating frontier AI, and a reversal of the hands-off posture adopted
since the start of the term.

**What the order actually requires (and doesn't).** Developers would
engage the government to determine whether a model under development
qualifies as a **"covered frontier model"**, then offer **up to 30 days**
of pre-release access and help pick **"trusted partners"** for early
evaluation. Crucially, the framework is **voluntary** — a company can
decline to participate with no stated penalty. A separate directive sets
up an **AI cybersecurity clearinghouse within 30 days**, coordinated by
the Treasury Secretary alongside the National Cyber Director, the NSA,
and CISA, to triage security vulnerabilities surfaced by AI models.

**How it got narrowed.** The signed order is materially weaker than the
draft Trump rejected on **2026-05-21**, when he scrapped a planned
signing over concerns it could "dull America's edge on AI technology."
That earlier draft proposed a **mandatory 90-day** pre-release review and
formal federal evaluation authority. Reporting indicates David Sacks
opposed the original and blessed the revised version only after the
review window was cut from 90 to 30 days and made voluntary, following a
White House meeting with Treasury Secretary Bessent and Defense Secretary
Hegseth.

**Why this is in the model-timeline lane.** This is a policy event, not a
model, but it bears directly on the *release cadence* this lane tracks: a
voluntary 30-day pre-release window is exactly the kind of condition that
can sit between "model is ready" and "model ships publicly." The
[[mythos-public-release]] ticket already carries a "voluntary CAISI
partnership" condition; this EO is the broader regulatory backdrop to
that pattern.

**Transition triggers:**
- "Covered frontier model" criteria, the trusted-partner list, or the
  clearinghouse charter get published → UPDATE with a history entry.
- A named lab publicly opts in or out (Anthropic / OpenAI / Google /
  xAI / Microsoft) → UPDATE; if it reshapes a specific model's ship date,
  cross-link that model's ticket.
- The order is rescinded, enjoined, or superseded by legislation → close
  with the appropriate reason and link the successor.
- Routine aging with no fresh developments → keep `confirmed`; this is a
  standing policy fact, not a time-boxed rumor.
