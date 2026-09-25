---
slug: oracle-project-jupiter-power-2026-09
title: Oracle's Project Jupiter datacenter — force-majeure report, Oracle denies any schedule slip
company: Oracle / STACK Infrastructure
model: null
status: confirmed
status_note: |
  **A disputed event with a primary rebuttal in-window, 2026-09-24.**
  @zerohedge relayed the report: "Oracle's Massive 'Project Jupiter' Data
  Center Declares Force Majeure, Jeopardizing Entire US AI Rollout" (14:54
  UTC). @Oracle's own account answered directly (12:54 UTC): "Project Jupiter
  remains on our planned schedule. We are fully committed to New Mexico and
  confident in our path forward... This includes **reimagining Project
  Jupiter's power plan** as part of our long-term commitment to be a good
  neighbor to the residents of Doña Ana County. STACK Infrastructure has been a
  tremendous partner... More than 3,600 construction workers are helping build
  the campus, including more than 1,000 New Mexico residents."

  **The rebuttal concedes the substance while denying the headline.** Oracle
  denies a schedule slip; it does not deny that the power plan has changed. A
  force-majeure declaration and "reimagining the power plan" are compatible
  descriptions of the same event from opposite ends. That is why this is
  tracked as a power-procurement event, not as a "delay" — the slug says
  `power`, not `delay`, on purpose.

  **A third party says it called this months ago.** @SemiAnalysis_ (16:33 UTC):
  "ORACLE DELAY: We already said it in our energy model on May 29 and on our
  twitter on Jul 17." That is an independent analyst asserting a prior public
  call, which raises the prior that something real happened, and is not itself
  a document.

  **Why this belongs in a model-release timeline.** Grid interconnection and
  generation are now the binding constraint on frontier capacity, which is the
  same thesis Google used to justify flying TPUs into orbit the same day
  ([[google-suncatcher-tpu-satellite-2026-09]]) and the reason nuclear SMR
  procurement is tracked here at all
  ([[ai-hyperscaler-nuclear-smr-deals-2026-07]]). A flagship campus having to
  re-plan its power supply is the constraint showing up in a specific place.
expected: "Contested. Open: the force-majeure filing or notice itself rather than a headline about it; what 'reimagining the power plan' concretely means (generation source, interconnect date, on-site generation); whether Oracle restates a Jupiter energization date; and whether any customer capacity commitment is affected."
labels:
  - oracle
  - datacenter
  - power
  - infrastructure
  - contested
verification: partial
sources:
  - https://x.com/Oracle/status/2103105677874897334
  - https://x.com/zerohedge/status/2103135896702788048
  - https://x.com/SemiAnalysis_/status/2103160990493712496
created_at: 2026-09-25
updated_at: 2026-09-25
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-25
    change: "Created — CONFIRMED / partial. On 2026-09-24 a report circulated that Oracle's Project Jupiter datacenter in Doña Ana County, New Mexico had declared force majeure, framed by @zerohedge as 'jeopardizing entire US AI rollout' (14:54 UTC, ~1,118 likes). @Oracle's own account rebutted the same day (12:54 UTC, ~880 likes): the project 'remains on our planned schedule', Oracle is 'fully committed to New Mexico', and — the concession inside the denial — this 'includes reimagining Project Jupiter's power plan'; it also named STACK Infrastructure as partner and cited 3,600+ construction workers. @SemiAnalysis_ (16:33 UTC) said it had flagged an Oracle delay in its energy model on 2026-05-29 and publicly on 2026-07-17. Status confirmed because a primary Oracle statement establishes that the power plan is being changed and that the project is publicly contested; verification partial because the force-majeure notice itself is not in evidence and the only direct primary source is the party denying the headline. Slug deliberately says 'power' rather than 'delay': what both sides agree on is a power-plan change, and the schedule claim is exactly what is disputed. Tracked here because grid and generation constraints are now the binding limit on frontier capacity — the same thesis behind [[google-suncatcher-tpu-satellite-2026-09]] and [[ai-hyperscaler-nuclear-smr-deals-2026-07]]."
---

Read the denial closely and it is not quite a denial.

Oracle disputes exactly one claim — that Jupiter has slipped. It volunteers,
unprompted, that the power plan is being "reimagined", and it wraps that in
neighbourly language about Doña Ana County. Companies do not reimagine the
power plan of a flagship campus mid-build for reputational reasons; they do it
when the original plan stopped being available, usually because an interconnect
or a generation source did not land.

So the two accounts are less contradictory than they look. A force-majeure
notice against a power supplier and "we are reimagining the power plan" can be
the same fact narrated by the party who filed it and the party who received it.
What genuinely remains open is whether the schedule survives the re-plan, and
Oracle is the only one asserting that it does.

The SemiAnalysis claim is the one to weigh carefully. An analyst saying "we
called this in May" is a reputational assertion, not evidence — but it is
checkable, and if their energy model did flag Jupiter's interconnect months
ago, that materially raises the odds that the headline is directionally right
and the denial is about timing rather than substance.

For this timeline, the durable point is not Oracle. It is that the constraint
has moved. Chips are procurable; megawatts, on a schedule, at a specific
latitude, are not. Every large program in this file is now partly a power
story.
