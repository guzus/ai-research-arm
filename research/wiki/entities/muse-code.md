---
slug: muse-code
title: Muse Code (Muse Spark 1.2)
type: entity
aliases: ["Muse Code", "Muse Spark 1.2", "Meta Muse Code"]
tags: [coding-agent, meta, terminal-agent, benchmarks, pricing]
description: Meta Superintelligence Labs' first coding agent (beta, 2026-08-06), a terminal agent with persistent sub-agents running on the new Muse Spark 1.2 at $1.25/$4.25 per Mtok, with a cheaper tier for developers who let Meta train on their code; a Muse Spark 1.2 open-weight version was promised for "the coming weeks" (2026-08-10).
created_at: 2026-08-06
timestamp: 2026-08-11T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-08-11", path: research/digest/2026-08-11-digest.md}
  - {title: "ARA daily digest 2026-08-06", path: research/digest/2026-08-06-digest.md}
  - {title: "ARA model ticket — Meta Hatch / Muse Spark", path: research/models/tickets/meta-hatch-muse-spark-2026-06.md}
---

**Muse Code** is [[meta]]'s first coding agent, launched in beta on
2026-08-06 by Meta Superintelligence Labs and running on a new model,
**Muse Spark 1.2**. It is a **terminal agent with persistent sub-agents**
that plan, implement and validate multi-file changes across large code
bases, demoed turning an mp4 house fly-through into a working booking site.
This page covers the agent and the 1.2 model together, because they shipped
as one product; the maker is tracked on [[meta]] and the earlier
**Muse Spark 1.1** benchmark claims are recorded there.

## Why it matters

- **Meta's third model release in under a month (2026-08-06).** Cadence, not
  capability, is the news: Meta has moved from occasional Llama drops to a
  shipping rhythm, and has now entered the agentic-coding market that
  [[cognition-ai]], [[cursor]] and the frontier labs' own CLIs occupy
  (TechCrunch, @AIatMeta, ARA daily digest 2026-08-06).
- **Priced with a data-for-discount tier.** List price is **$1.25 / $4.25 per
  million tokens**, with a **cheaper tier for developers who let Meta train
  on their code**. That second tier is the load-bearing part: it makes
  proprietary code an explicit unit of payment, which is a different
  commercial posture from the "we do not train on your code" default the
  incumbent coding agents advertise.
- **Independent readings landed within three hours and went the other way.**
  Vendor figures put Muse Spark 1.2 at **59% on DeepSWE 1.1**, ahead of Grok
  Build 4.5 and [[gemini-3-6-flash|Gemini 3.6 Flash]]. Independent readings
  put Muse Code at **82.9% on Terminal-Bench 2.1** versus **86.7%** for Claude
  Code on [[claude-opus-5|Opus 5]], and **59.3% on DeepSWE 1.1** versus
  **65.0%** for Opus 5 and **64.8%** for [[gpt-5-6|GPT-5.6 Terra]]. Behind on
  both benchmarks it launched against.
- **The "#2 terminal coding agent on earth" line is a comparison-set
  artifact.** That claim came from a relay, which appended its own correction
  45 minutes later: the ranking holds **per Meta's published charts** — and
  **Claude Opus 5 does not appear in Meta's comparison set at all**. The
  general lesson for reading launch tables is on
  [[verification-bottleneck]]: an omitted competitor is a stronger signal
  than a reported margin.

## Open questions

- **What does the training-data tier actually cover** — repository contents,
  agent traces, or both — and can it be revoked after the fact?
- **Do the independent Terminal-Bench and DeepSWE numbers hold** once the
  beta widens and harness configuration is matched? Both readings arrived
  within three hours of launch.
- **Is Muse Spark 1.2 open-weight?** Meta committed on 2026-08-10 to
  open-weighting a version of Muse Spark 1.2 ("in the coming weeks") — still a
  promise, not a release, and read as a reversal of the closed posture this
  question was tracking. The commitment landed with the [[muse-glimmer]]
  Apache-2.0 release, Meta's return to [[open-weights]].
- **Where does Hatch fit now?** The earlier Meta Hatch / Muse Spark ticket
  and this release have not been reconciled in one place.
