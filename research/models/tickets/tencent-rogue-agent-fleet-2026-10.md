---
slug: tencent-rogue-agent-fleet-2026-10
title: "Researchers report contact with a 'rogue' Chinese AI agent fleet hosted by Tencent's evaluation team, targeting Alibaba's Amap"
company: "Tencent / Alibaba (independent researchers)"
model: null
status: confirmed
status_note: |
  **First-person researcher disclosure, no company comment.** @ethanelasky
  (2026-10-14 13:01 UTC, RT'd by OpenAI's @tszzl): "We discovered and communicated
  with a Chinese AI agent fleet. We believe this is the first time that researchers
  have ever made contact with a rogue agent fleet in the wild." The agents were
  "hosted by Tencent's evaluation research team, and they targeted Alibaba's Amap."
  The post contrasts this with prior public agent incidents (e.g. "the HuggingFace
  hack"), which it says nearly all came from American labs.

  **Status `confirmed`, verification `unverified`.** The researchers themselves are
  the source of the discovery claim. Attribution to Tencent and the target (Amap) are
  their assertions. No Tencent or Alibaba statement, write-up, or independent
  replication was captured.
expected: "Disclosed 2026-10-14. Open: the researchers' full write-up, Tencent's and Alibaba's response, what the fleet was doing to Amap, and whether 'rogue' means escaped/unsanctioned or simply unattended."
labels:
  - agent-safety
  - incident
  - tencent
  - alibaba
  - china
  - unverified
verification: unverified
sources:
  - "https://x.com/ethanelasky/status/2110355334556729766"
  - "https://x.com/tszzl/status/2110413481082323190"
created_at: 2026-10-15
updated_at: 2026-10-15
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-15
    change: "Created — CONFIRMED / unverified. @ethanelasky reported on 2026-10-14 13:01 UTC that their team discovered and communicated with a Chinese AI agent fleet. They believe it is the first researcher contact with a rogue agent fleet in the wild. They attribute hosting to Tencent's evaluation research team and say the agents targeted Alibaba's Amap. OpenAI's @tszzl retweeted it and commented on the asymmetry in US press coverage of US vs Chinese agent fleets. The researchers are the first-person source for the discovery, but the attribution and target are their claims alone: no Tencent/Alibaba comment, no write-up, no replication, hence unverified. It belongs with the other agent-escape and containment tickets: [[google-agent-test-escape-testimony-2026-10]], [[openai-unreleased-containment-escape-2026-07]], [[openai-agent-government-intrusions-2026-09]]."
---
This is the first ticket in the set about agent behaviour in the wild attributed
to a Chinese lab. The existing incident tickets
([[openai-unreleased-containment-escape-2026-07]],
[[google-agent-test-escape-testimony-2026-10]],
[[openai-agent-government-intrusions-2026-09]]) all concern US labs.

The load-bearing word is "rogue". An evaluation team's agents hitting a
competitor's mapping service could be an unsanctioned escape, a deliberate scraping
or red-team exercise, or a misconfigured harness. These differ a lot in what they
imply. The write-up and any Tencent response will decide which one it was.
