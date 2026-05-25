---
slug: mythos-public-release
title: Claude Mythos — full public release
company: Anthropic
model: Mythos
status: in-testing
status_note: |
  Multi-cloud gated preview (AWS Claude Platform GA 2026-05-11, GCP Vertex AI
  Private Preview 2026-05-16) with no plan for a public release.
expected: TBD — voluntary CAISI partnership; toned-down variant possible "in foreseeable future" (Boris Cherny, 2026-05-05)
labels:
  - frontier-model
  - gated
  - multi-cloud
  - project-glasswing
verification: confirmed
sources:
  - https://red.anthropic.com/2026/mythos-preview/
  - https://cloud.google.com/blog/products/ai-machine-learning/claude-mythos-preview-on-vertex-ai
  - https://www.anthropic.com/glasswing
  - "@scaling01"
  - "@kimmonismus"
  - "@AndrewCurran_"
  - "@AiBattle_"
  - "@testingcatalog"
  - "@techcrunch"
created_at: 2026-04-12
updated_at: 2026-05-25
closed_at: null
closed_reason: null
history:
  - ts: 2026-04-12
    change: Created — initial Mythos benchmark traces leaked
  - ts: 2026-05-05
    change: "Pricing reported at $25 / $125 per MTok input/output by Boris Cherny"
  - ts: 2026-05-11
    change: AWS Claude Platform GA — first cloud surface for Mythos (gated)
  - ts: 2026-05-15
    change: "scaling01 viral post (\"It's over. Mythos is insane\") — Mythos at ~69% on the benchmark vs GPT-5.5 baseline"
  - ts: 2026-05-16
    change: GCP Vertex AI Private Preview confirmed via Google Cloud blog — Mythos appears in GCP console without a preview label
  - ts: 2026-05-16
    change: kimmonismus argues a public release is structurally implausible despite GCP artifact
  - ts: 2026-05-20
    change: "Secondary report: Anthropic is reportedly letting Glasswing partners share cybersecurity findings surfaced by Mythos with other organizations — a governance change for the gated preview (not yet confirmed on Anthropic's own channels)"
  - ts: 2026-05-25
    change: "TechCrunch coverage — \"Anthropic debuts preview of Mythos in a new cybersecurity initiative,\" putting the gated cyber angle in primary tech press and corroborating the 2026-05-20 Glasswing cyber-findings-sharing report"
---

Mythos is Anthropic's post-Opus-4.7 frontier model, operated as a
multi-cloud gated product rather than a public release. It surfaces only
inside **Project Glasswing** — a ~40-org partnership including AWS, Apple,
Microsoft, Google, CrowdStrike, and Palo Alto — and through the two
cloud surfaces that the partner companies happen to run on (AWS, GCP).

The benchmark dominance is large enough that Alex Heath called Mythos
"despite not being widely available, has reset how every lab talks about
what leading means." `scaling01`'s May 15 viral post puts Mythos at
~69% on the unspecified frontier benchmark vs the GPT-5.5 baseline.

**Why this ticket stays open:** Anthropic has explicitly signaled no
public release ("toned-down version in foreseeable future" — Cherny).
That is itself the news. The ticket tracks the multi-cloud preview's
expansion (AWS → GCP → ?) rather than a release date. If Anthropic
ever flips to public availability, this ticket transitions to
`released`. If a permanently-gated stance is confirmed (e.g. by a
formal Anthropic statement), this ticket closes with reason
`gated-permanent` and the ongoing Glasswing coverage moves to a
dedicated `project-glasswing` ticket.

**Dedup notes for the agent:** new signal about Mythos pricing,
preview expansions, or partner additions UPDATES this ticket. A new
Anthropic model variant (e.g. "Sonnet-Mythos") with a different
release plan is a separate ticket; reference this one from its body.
