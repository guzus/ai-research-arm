---
slug: microsoft-mai-code-1-flash
title: Microsoft MAI Code 1 Flash — homegrown coding model in GitHub Copilot
company: Microsoft AI
model: MAI Code 1 Flash
status: released
status_note: |
  Reported live 2026-06-05: Microsoft's own coding model inside **GitHub
  Copilot**, available **free across every Copilot tier** (selectable from
  the model dropdown in VS Code Copilot Chat). Claimed specs: **256K
  context**, **~60% fewer tokens** on complex tasks vs comparable models,
  **85.8%** on Microsoft's adversarial coding benchmark, and trained
  *inside* the Copilot production environment rather than externally tested
  and handed over. Positioned as Microsoft's bid to defend Copilot against
  Cursor and Claude Code with a cheap/fast first-party option. This is the
  "coding" model in the pre-leaked Build 2026 MAI lineup (see
  [[microsoft-build-2026-models]]). Verification is unverified: the launch
  claim comes from a single hype account (@cyrilXBT) with no Microsoft
  primary captured in-window, though it is consistent with the confirmed
  Build coding-model narrative.
expected: null
labels:
  - coding-model
  - microsoft-ai
  - mai-models
  - github-copilot
  - released
verification: unverified
sources:
  - "@cyrilXBT"
created_at: 2026-06-05
updated_at: 2026-06-05
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-05
    change: "Created — reported launch of **MAI Code 1 Flash**, Microsoft's first-party coding model inside GitHub Copilot, free across all Copilot tiers from today (@cyrilXBT). Claimed: 256K context, ~60% fewer tokens on complex tasks, 85.8% on Microsoft's adversarial coding benchmark, trained inside the Copilot production environment. Fills the 'coding' slot of the confirmed Build 2026 MAI lineup ([[microsoft-build-2026-models]]). Single hype-account source, no Microsoft primary in-window → status released (availability claim) but verification unverified"
---

**MAI Code 1 Flash** is reported (2026-06-05, @cyrilXBT) as Microsoft's
own coding model shipping inside **GitHub Copilot** — selectable from the
model dropdown in VS Code's Copilot Chat and available **free on every
Copilot tier**, including the no-credit-card free plan. It is pitched as
*not* rented from OpenAI and *not* built on OpenAI data: a Microsoft model
trained inside the Copilot production environment.

Claimed numbers: a **256K context window**, **~60% fewer tokens** on
complex tasks versus comparable models, and **85.8%** on Microsoft's own
adversarial coding benchmark. The strategic read is consistent with the
confirmed Build 2026 narrative — Microsoft wants a cheap, fast first-party
coding model to defend GitHub Copilot's share against Cursor and Claude
Code rather than paying for third-party frontier models on every call.

**Why a separate ticket.** The [[microsoft-build-2026-models]] bundle is
the umbrella for Microsoft's homegrown-AI push and explicitly anticipated
the coding model spinning out once named and shipped. MAI Code 1 Flash is
now that named, load-bearing artifact, so it gets its own ticket; the
bundle stays the umbrella.

**Why `unverified`.** The launch claim rests on a single promotional
account with no Microsoft primary (no @MicrosoftAI / @satyanadella /
@mustafasuleyman post, no Microsoft blog) captured in this cycle. The
specifics (free-for-all-tiers, the benchmark figure, the model name) are
detailed and fit the confirmed Build coding-model slot, but they have not
been independently corroborated yet.

**Transition triggers:**
- Microsoft primary (blog / @MicrosoftAI / @mustafasuleyman) or
  independent press confirming MAI Code 1 Flash → UPDATE, raise
  verification to partial/confirmed.
- A successor/sibling (MAI Code 1 Full, MAI Code 2) → new ticket, link
  back here.
- ≥4 weeks past public availability settled into normal coverage →
  `closed: released-and-aged`.
- If no corroboration appears and the claim is contradicted →
  reassess toward `unverified` closure.

**Dedup note:** further MAI Code 1 Flash signal (Microsoft primary,
pricing, benchmarks, surface changes) UPDATES this ticket.
