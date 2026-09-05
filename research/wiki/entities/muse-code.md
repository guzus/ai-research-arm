---
slug: muse-code
title: Muse Code (Muse Spark 1.3)
type: entity
aliases: ["Muse Code", "Muse Spark 1.2", "Muse Spark 1.3", "Meta Muse Code", "Muse Spark max", "Muse Spark 1.3 max"]
tags: [coding-agent, meta, terminal-agent, benchmarks, pricing]
description: Meta Superintelligence Labs' coding agent; Muse Spark 1.3 max unlocked 2026-09-05 after extra safety testing, still $1.25/$4.25, with a partner-preview AA card at 62 versus xhigh 61.
created_at: 2026-08-06
timestamp: 2026-09-05T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-09-05", path: research/digest/2026-09-05-digest.md}
  - {title: "ARA daily digest 2026-09-03", path: research/digest/2026-09-03-digest.md}
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

## Muse Spark 1.3 (2026-09-03)

- **[[meta]] shipped Muse Spark 1.3** into Muse Code and the Meta Model
  API at the **same $1.25/$4.25 list as 1.2**. Meta's table has DeepSWE
  v1.1 at **75.4** versus [[gpt-5-6|GPT-5.6 Sol]] **73.0** and
  [[claude-opus-5|Opus 5]] **74.0**. Artificial Analysis has the public
  **xhigh SKU at 61 (+4 from 1.2)** and a **gated max at 62**, still
  behind [[claude-fable-5|Fable 5.1]] (**66**) and Opus 5 max (**63**).
  Max reasoning is still in safety testing. The 1.2 open-weight promise
  from 2026-08-10 has not landed (Meta, Artificial Analysis; ARA daily
  digest 2026-09-03).
- **FrontierSWE v2 still scores Muse Spark 1.2 at 12.0%.** The new
  34-task, 20-hour bench put Fable 5.1 at **56.3% mean@5** versus
  **32.2%** for GPT-5.6; **1.3 is not on the board**, and neither is
  [[gemini-3-8-flash]] (Proximal; ARA daily digest 2026-09-03).
- **Hacker News** treated 1.3 as the day's third AI thread (**285
  points / 181 comments**), behind [[gemini-3-8-flash]] and Mistral's
  default user-input training change (ARA daily digest 2026-09-03).

## Muse Spark max unlocks (2026-09-05)

- **[[meta]] unlocked Muse Spark max**, the reasoning tier held
  for extra safety testing after the September 2 ship. This is a
  **setting unlock, not a new family**. Alexandr Wang recommended
  max over high / xhigh for coding and agentic work on Muse Code
  and the Model API. A partner-preview Artificial Analysis card
  had max at Intelligence Index **62** versus xhigh **61**;
  standard list price is still **$1.25 / $4.25 per million
  tokens**. The public AA board still has
  [[claude-fable-5|Fable 5.1]] first (Meta, Twitter, Artificial
  Analysis; ARA daily digest 2026-09-05).
