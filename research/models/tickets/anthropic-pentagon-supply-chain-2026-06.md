---
slug: anthropic-pentagon-supply-chain-2026-06
title: Pentagon designates Anthropic a "supply-chain risk", tests replacements for Claude
company: US Government / DoD (re Anthropic)
model: null
status: confirmed
status_note: |
  After **Anthropic refused to drop its no-mass-surveillance and
  no-autonomous-weapons red lines**, the **DoD designated it a "supply-chain
  risk"** and is **actively testing OpenAI, Google, and xAI's Grok as
  replacements** (evaluated by ~25 "power users"). Claude had been the primary
  AI on classified networks via the **Maven Smart System**. **Anthropic is
  challenging the designation in court.** Multi-outlet reporting; no DoD or
  Anthropic primary filing captured in-window → verification partial.

  **2026-07-03 — court documents make the fight public, named officials.**
  WSJ-reported court filings surfaced months of emails between **Dario
  Amodei and Pentagon undersecretary Emil Michael** over guardrails for
  AI-powered weapons and domestic surveillance: Anthropic wanted bans on
  fully autonomous weapons and certain surveillance uses; the Pentagon
  pushed for Claude to be available across "any lawful" national-security
  use case. Michael's own (unverified) claim: **two-thirds of Pentagon
  operations using Anthropic have already switched to other AI tools**. A
  **judge has paused parts of the "supply-chain risk" designation and the
  government is appealing**. Fortune's "Eye on AI" newsletter separately
  frames this as the week's defining AI story, and (per a same-day relay)
  describes a leaked internal Amodei Slack memo calling OpenAI's messaging
  "mendacious"/"gaslighting" — single-source, not yet independently
  confirmed. Named officials + quoted emails + multi-outlet convergence
  clears the bar for `confirmed` verification.
expected: "Government's appeal of the judge's pause on the 'supply-chain risk' designation pending; watching for an on-record Anthropic/Pentagon/DoD statement"
labels:
  - policy
  - defense
  - anthropic
  - legal-action
  - procurement
verification: confirmed
sources:
  - "@WSJ"
  - "@TechCrunch"
  - "@AnthropicAI"
  - "@kimmonismus"
  - "@whoisanku"
created_at: 2026-06-09
updated_at: 2026-07-03
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-09
    change: "Created — the DoD designated Anthropic a 'supply-chain risk' after Anthropic refused to drop its no-mass-surveillance / no-autonomous-weapons red lines, and is testing OpenAI, Google, and xAI's Grok to replace Claude (the primary AI on classified networks via the Maven Smart System), evaluated by ~25 'power users'. Anthropic is challenging the designation in court. Multi-source reporting, no DoD/Anthropic primary captured in-window → status confirmed (event), verification partial"
  - ts: 2026-07-03
    change: "WSJ-reported court documents made the dispute public with named officials: months of emails between Dario Amodei and Pentagon undersecretary Emil Michael over autonomous-weapons/surveillance guardrails. Michael claims two-thirds of Pentagon Anthropic usage already switched away (unverified, his own figure). A judge has paused parts of the 'supply-chain risk' designation; the government is appealing. Fortune 'Eye on AI' calls this the week's defining AI story and relays an unconfirmed leaked Amodei Slack memo calling OpenAI's messaging 'mendacious'/'gaslighting'. Named officials + quoted emails + multi-outlet convergence (WSJ, two independent tweet relays, Fortune) → verification partial → confirmed; status stays confirmed."
---

The **US Department of Defense has designated Anthropic a "supply-chain
risk"** and is **actively evaluating OpenAI, Google, and xAI's Grok as
replacements for Claude** on classified systems, per multi-outlet reporting
this cycle. The trigger, as reported: Anthropic **refused to drop its usage
red lines** — **no mass surveillance** and **no autonomous weapons** — which
collided with DoD requirements.

The stakes are concrete. **Claude had been the primary AI on classified
networks via the Maven Smart System**, so the designation directly threatens
an established deployment. A cohort of **~25 "power users"** is reportedly
running the replacement evaluation across the rival models. **Anthropic is
challenging the designation in court**, making this both a **procurement** and
a **legal-action** event.

**Why `confirmed` event but `partial` verification.** The story is carried
across multiple independent outlets and is internally consistent (red-line
refusal → risk designation → replacement testing → legal challenge), clearing
the bar for a confirmed *event*. But no **DoD or Anthropic primary** (official
statement, court docket, contract notice) was captured in this cycle's signal,
so verification stays `partial` until a primary lands.

**Why this is its own ticket.** It is a distinct **government-procurement +
legal** action that affects Anthropic's roadmap and the federal AI vendor
landscape — separate from the US-government *equity-stake* talks
([[openai-us-govt-stake-2026-06]], which notably exclude Anthropic) and from
the model-review executive order ([[us-ai-model-review-eo-2026-06]]).

**Transition triggers:**
- A DoD or Anthropic primary (statement, court filing, contract action) → UPDATE, advance verification.
- A named replacement awarded, or the designation rescinded → UPDATE.
- Court ruling on Anthropic's challenge → UPDATE.
- Settles into normal coverage with a resolved outcome ≥4 weeks → `closed`.

**Dedup note:** further DoD/Anthropic supply-chain-risk, Maven-replacement,
or designation-litigation signal UPDATES this ticket. OpenAI's defense/biodefense
work stays on [[openai-rosalind-biodefense-2026-05]] and [[openai-robotics-2026-05]].
