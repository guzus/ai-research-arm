---
slug: anthropic-stream-data-centers-2026-09
title: Anthropic in early talks to lease up to 1GW directly from Apollo-backed Stream Data Centers
company: Anthropic / Stream Data Centers (Apollo)
status: rumored
status_note: |
  @theinformation, 2026-09-23 20:30 UTC (exclusive): "Anthropic is discussing a
  deal for up to 1 gigawatt of data center capacity, an investment that could
  require at least $40 billion. Leasing facilities directly could give it more
  control over chips and lower its reliance on cloud providers."

  Counterparty and chip detail come from @mark_k's read of the same reporting
  (2026-09-23 11:41 UTC): Apollo-backed **Stream Data Centers**, with sites
  potentially filled with **Google and Broadcom TPUs** rather than NVIDIA.

  Explicitly early-stage. The Information's own framing is "discussing" and
  "could require"; there is no signed agreement, no site list, no timeline and
  no Anthropic statement in this cycle's signal. Status `rumored`, verification
  `partial` — a named outlet with a named counterparty and a number, but no
  primary confirmation from either side.

  The structural claim is the one to watch, not the dollar figure: leasing
  facilities *directly* is a different posture from buying capacity through
  AWS/Google/Nscale, and it is what would let Anthropic choose its own silicon.
expected: "TBD — early talks. A signed lease, a named site, or an Anthropic/Stream statement would move this to confirmed."
labels:
  - anthropic
  - compute
  - datacenter
  - tpu
  - rumored
verification: partial
sources:
  - https://x.com/theinformation/status/2102858053053718586
  - https://x.com/mark_k/status/2102725116882780590
created_at: 2026-09-24
updated_at: 2026-09-24
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-24
    change: "Created — RUMORED. The Information reported 2026-09-23 that Anthropic is in early talks for up to 1GW of data center capacity requiring at least $40B, leased directly rather than bought through a cloud provider. @mark_k's read of the same reporting names the counterparty as Apollo-backed Stream Data Centers and says the sites could be filled with Google and Broadcom TPUs rather than NVIDIA. No signed deal, no sites, no timeline, no statement from Anthropic or Stream in this cycle's signal — status rumored, verification partial on a named outlet with a named counterparty. Distinct from the aggregate exposure tracked at [[anthropic-compute-commitments-2026-09]] and from the existing supplier-side deals [[anthropic-nscale-compute-2026-08]], [[anthropic-spacex-colossus-2026-05]] and [[anthropic-google-datacenter-financing-2026-07]]; if this is later reported to be the same transaction as the Google-backed financing ticket, one closes as superseded rather than being renamed."
---

The number is eye-catching and the structure is the actual news. Anthropic's
compute to date has been bought *through* someone — AWS, Google, Nscale, SpaceX
([[anthropic-nscale-compute-2026-08]], [[anthropic-spacex-colossus-2026-05]]).
Leasing a gigawatt directly from a developer inverts that: Anthropic picks the
silicon, controls the buildout schedule, and stops paying a cloud margin on the
largest line item it has.

That the sites could be filled with **Google and Broadcom TPUs** is the detail
that makes it strategically coherent rather than merely large. A direct lease is
only worth the operational burden if you intend to put hardware in it that your
cloud provider would not otherwise sell you at that scale — and it lines up with
Anthropic's other non-NVIDIA moves ([[anthropic-amd-compute-evaluation-2026-07]],
[[anthropic-samsung-chip-talks-2026-06]], [[anthropic-micron-supply-2026-06]]).

Two reasons to keep this at `rumored` despite the sourcing quality. First, "early
talks" reported by an outlet with good access is still a negotiation that can
die — the ticket set already carries
[[anthropic-google-datacenter-financing-2026-07]], an advanced-talks item from
July that has not resolved. Second, ≥$40B against a company whose disclosed
commitments already run to $517B
([[anthropic-compute-commitments-2026-09]]) is the kind of figure that gets
restated once terms firm up.

The editorial observation @mark_k makes is fair and worth keeping in view: a
company publishing an essay on pacing the frontier
([[anthropic-pace-the-frontier-2026-09]]) is simultaneously contracting the
capacity to accelerate. Those are consistent positions — pacing is about release
discipline, not capacity — but the tension is real and will be used against
Anthropic either way.
