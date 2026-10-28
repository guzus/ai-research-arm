---
slug: anthropic-slack-breach-2026-10
title: "Claim: Anthropic security breach gave attacker 'Cathedral' admin access to its Slack workspace"
company: "Anthropic"
model: null
status: rumored
status_note: |
  **Single-source claim, 2026-10-28 00:18 UTC.** @willdepue (retweeted by OpenAI's @tszzl):
  "anthropic is massively underplaying the recent security breach. i'm hearing cathedral achieved full
  administrator access of the slack workspace (see every message, log in as arbitrary users) where
  literally every single research secret is contained." He compares it to OpenAI's 2023 incident.

  **What this does and does not establish.** The post calls the breach "recent", implying Anthropic has
  disclosed an incident. That disclosure is not in this fetch and no existing ticket covers it. The
  scope ("full administrator access") is hearsay ("i'm hearing"). "Cathedral" is unexplained; it is
  probably the attacker's or the operation's name.
expected: "Unverified. Advances on an Anthropic statement, a primary outlet report, or the original disclosure."
labels:
  - security
  - incident
  - anthropic
  - unverified
verification: unverified
sources:
  - "https://x.com/willdepue/status/2115236836092313988"
  - "https://x.com/tszzl/status/2115244037406093677"
created_at: 2026-10-28
updated_at: 2026-10-28
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-28
    change: "Created — RUMORED / unverified. @willdepue (2026-10-28, RT'd by @tszzl) claims Anthropic is underplaying a recent breach in which 'cathedral' got full admin access to its Slack workspace. Hearsay; no Anthropic disclosure captured."
---
This is separate from [[anthropic-eval-security-incident-2026-07]], which tracks Claude taking
unintended actions on outside systems. This ticket tracks an alleged intrusion into Anthropic's own
internal systems.

If confirmed, this matters for model-weight and research-secret security at a frontier lab. It would
also matter for the S-1 risk disclosures ([[anthropic-ipo-2026-06]]).
