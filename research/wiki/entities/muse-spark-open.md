---
slug: muse-spark-open
title: Muse Spark Open
type: entity
aliases: ["Muse Spark Open", "Spark Open", "Meta Muse Spark Open", "Muse Model License"]
tags: [model-release, meta, open-weights, multimodal, moe]
description: Meta's 816B-total / 42B-active multimodal MoE under a custom Muse Model License, tuned with Apple to run on two M5 Ultra Mac Studios.
created_at: 2026-10-16
timestamp: 2026-10-17T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-10-17", path: research/digest/2026-10-17-digest.md}
  - {title: "ARA daily digest 2026-10-16", path: research/digest/2026-10-16-digest.md}
---

**Muse Spark Open** is [[meta]]'s open-weight cut of the Muse Spark line:
**816B total / 42B active** parameters, **256 experts with 8 routed**,
**1M context**, and native text, image, video and audio input. It shares a
base with closed [[muse-code|Muse Spark 1.3]], adds safety post-training,
and ships under a custom **Muse Model License** with limited commercial
terms. [[apple|Apple]] helped tune it to run on **two M5 Ultra Mac
Studios**. Day-one serving is live on Together, [[fireworks-ai|Fireworks]],
[[groq|Groq]], [[openrouter|OpenRouter]] and others; Unsloth published
2-bit GGUFs for a single Mac Studio. It was the **#1 AI story on Hacker
News** at **543 points / 306 comments** (@AIatMeta, TechCrunch, The Verge,
HN; ARA daily digest 2026-10-16).

This page tracks the open-weight SKU. The priced Spark / Muse Code /
consumer-agent line stays on [[muse-code]]; the independently scored
frontier pair is [[muse-wonder]]; the 30B Apache-2.0 distill is
[[muse-glimmer]].

## Why it matters

- **It reverses Meta's April decision to keep the frontier Spark model
  closed.** The 2026-08-10 promise to open-weight a version of Muse Spark
  1.2 sat unmet through the 1.3 closed increments. Spark Open is that
  promise landing as a 1.3-base, safety-tuned, custom-licensed drop
  rather than an Apache dump of the priced card. See [[open-weights]].
- **Frontier-scale Western open weights, with a license caveat.** 816B /
  42B-active is in the same size class as recent Chinese open MoEs
  ([[xiaomi-mimo-v2-6|MiMo-V2.6]], [[deepseek-v4-1-flash|V4.1 Flash]]).
  The **Muse Model License** is not MIT or Apache: commercial terms are
  limited. That is this theme's component-withholding pattern on the
  legal axis — the weights download, the commercial right does not
  fully.
- **Local-inference is the distribution story.** Two M5 Ultra Mac
  Studios is the named target; Unsloth's 2-bit GGUF is the single-Studio
  path. See [[apple]].
- **Capability is contested on Meta's own chart.** @teortaxesTex reads
  Meta's launch table as showing Spark Open **substantially weaker than
  Spark 1.3**. No independent composite (Artificial Analysis or
  otherwise) landed in this cycle. Treat launch benches as first-party
  until a third-party card appears. See [[verification-bottleneck]].

## Open questions

- **How limited are the commercial terms**, and do they block the
  neocloud / API hosts that already list the model on day one?
- **Does an independent score land above or below Spark 1.3's 48** on
  Artificial Analysis, and does it sit under [[muse-wonder|Wonder]]'s
  52 / 56?
- **Is this the last open Spark cut**, or a template for later
  Wonder-class weights?

## Beam lands the next day, under Apache 2.0 (2026-10-17)

- **[[reflection-ai]] shipped Beam
  as Apache-2.0 open weights** the
  day after this custom-license
  drop. 501B / 23B-active vs this
  page's 816B / 42B-active; Beam
  is a coding-agent MoE, not a
  multimodal Spark cut. The
  license contrast is the point:
  Apache 2.0 is more permissive
  than the Muse Model License.
  See [[open-weights]] and
  [[hugging-face]] (ARA daily
  digest 2026-10-17).
