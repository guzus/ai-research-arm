---
slug: meta-muse-spark-1-4-2026-09
title: Muse Spark 1.4 — next Meta model appears as a registry entry on OpenCode
company: Meta (Meta Superintelligence Labs)
model: Muse Spark 1.4
status: in-testing
status_note: |
  **Registry artifact, 2026-09-24 21:00 UTC, single source.** @kimmonismus:
  "Meta teased its next major model as coming soon during the keynote. Now
  'muse-spark-1.4-contributor' has appeared on OpenCode's data page. Muse Spark
  1.4 seems very close!" with a screenshot.

  **Two facts, one strong and one weak.** STRONG: the exact model id
  `muse-spark-1.4-contributor` appearing on a provider's data page is a
  concrete, checkable artifact, and the `-contributor` suffix matches Meta's
  existing naming — the 1.3 Contributor variant is already a registered
  OpenCode profile in this repo's own backend routing, with its
  model-improvement data-collection consent requirement. WEAK: the inference
  that Connect's "coming soon" tease refers to this specific model. Meta teased
  a major model; nothing links the tease to the 1.4 string except adjacency.

  **Distinct artifact from [[meta-hatch-muse-spark-2026-06]].** That ticket
  tracks the Hatch consumer agent and the Muse Spark 1.3 line, which is
  released and still shipping — 1.3 reached Oracle and Google Cloud private
  preview the same day. A new version number with its own provider registry
  entry is a separate shipping artifact, which is why this is its own ticket
  rather than another history line there.

  **What "contributor" implies and does not.** In the 1.3 generation, the
  Contributor variant was region-limited, used OpenAI Responses transport, and
  required workspace consent to model-improvement data collection. If 1.4
  follows the same shape, a Contributor-tier appearance is an early-access
  channel, not general availability — so a registry entry is closer to a
  staged preview than a launch.
expected: "TBD — no Meta announcement, date, model card, pricing or benchmark. Watch for: the id becoming callable, a non-Contributor variant appearing, a Meta Superintelligence Labs post, and whether this is the model teased at Connect 2026."
labels:
  - meta
  - muse-spark
  - leak
  - registry-artifact
  - unreleased
verification: unverified
sources:
  - https://x.com/kimmonismus/status/2103228052344021308
created_at: 2026-09-25
updated_at: 2026-09-25
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-25
    change: "Created — IN-TESTING / unverified. @kimmonismus reported on 2026-09-24 21:00 UTC (~571 likes) that the model id 'muse-spark-1.4-contributor' has appeared on OpenCode's data page, days after Meta teased its next major model at Connect 2026 ([[meta-connect-2026-09]]). Status in-testing because an exact model id on a provider registry is a concrete artifact of the same class as a console listing; verification unverified because it is one screenshot from one account with no Meta statement, and the link between Connect's tease and this specific string is inference, not evidence. The '-contributor' suffix is given weight: it matches the existing Muse Spark 1.3 Contributor profile shape (region-limited, OpenAI Responses transport, workspace consent to model-improvement data collection), which means a Contributor-tier id is an early-access channel rather than GA — so this is a staged-preview signal, not an imminent-launch signal. Created as a separate ticket from [[meta-hatch-muse-spark-2026-06]] because that ticket tracks the released 1.3 line and the Hatch consumer agent, and a new version number with its own registry entry is a distinct shipping artifact."
---

A model id on a provider's data page is one of the higher-quality leaks
available, because it is not a rumour about a model — it is the serving
infrastructure being configured for one.

The qualifier that matters is `-contributor`. In the 1.3 generation that
variant came with region limits, a different transport, and a requirement that
the workspace consent to having its data used for model improvement. That is
the profile of a model being fed by its early users, not one being sold to
them. So the right reading of this string is "Meta is staging 1.4 for a
data-collecting preview cohort", which is a real step and a smaller one than
"Muse Spark 1.4 is about to launch".

The Connect link is the part to resist. Meta teased a major model at the
keynote; a 1.4 point-release id appearing days later is chronologically
convenient, but point releases and "next major model" are usually different
objects. If Connect's tease was for something bigger — the Watermelon
foundation model that [[meta-hatch-muse-spark-2026-06]] has been tracking as
pending — then 1.4 is an interim ship and the tease is still outstanding.

Cheap to resolve: the id either becomes callable or it does not.
