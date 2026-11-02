---
slug: ai-text-watermarking
title: AI Text Watermarking
type: concept
aliases: ["text watermarking", "Grok watermarking", "invisible text watermark", "SynthID Text", "TextSeal2"]
tags: [watermarking, provenance, transparency, policy]
description: Invisible watermarks embedded in model-generated text so a detector can flag it; xAI confirmed global Grok watermarking and Anthropic reportedly extends it to older Claude models from Nov 3, leaving North American ChatGPT the lone holdout by one count.
created_at: 2026-11-01
timestamp: 2026-11-02T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-11-02", path: research/digest/2026-11-02-digest.md}
  - {title: "ARA daily digest 2026-11-01", path: research/digest/2026-11-01-digest.md}
  - {title: "ARA model ticket — Claude text watermarking (older models, Nov 3)", path: research/models/tickets/anthropic-claude-text-watermarking-2026-11.md}
---

**AI text watermarking** hides a statistical signal in generated text so that
the provider (or a detector it controls) can later recognize the output as
machine-made. It is becoming the default posture among large labs.

## State of play (2026-11-02)

- **[[xai]]** announced invisible watermarking for Grok text on Oct 31, and the
  2026-11-02 digest says it now appears to be rolling out globally, with an
  opt-out page. xAI did **not** sign the EU transparency Code of Practice that
  six other labs did. By @AndrewCurran_'s count, North American ChatGPT
  ([[openai]]) is now the only major unwatermarked text model.
- **[[anthropic]]** reportedly extends watermarking from **Nov 3** to Mythos 5,
  Opus 4.7, Opus 4.6 and Sonnet 4.6 across web, Claude Code and API, worldwide;
  newer models such as Opus 5.5 reportedly already carry it. Detection is said
  to be limited to vetted institutions (regulators, law enforcement, media,
  schools, researchers) and shows only that Claude was involved. This rests on a
  **single secondhand post** (@DDJCXX); the cited original was not captured and
  Anthropic has not confirmed. The Decoder separately reported a loophole on two
  older models. It succeeds a closed August rumor
  (`anthropic-claude-watermarking-2026-08`, closed as unverified).
- The push follows the **EU Code of Practice on Transparency of AI-Generated
  Content**, signed by Anthropic, OpenAI, Google, Meta, Microsoft and Mistral
  but **not xAI** — see [[eu-ai-regulation]]. OpenAI's own scheme (early October)
  is opt-in on the API and on by default in the EU.
- Research: Meta's **TextSeal2** distortion-free watermark is reported to survive
  speculative decoding (arXiv 2610.40613).

## Caveats

- Critics note **only the lab holds the detector**, so the watermark gives
  users and third parties no independent verification.
- The "ChatGPT is the only one without" claim is a single commentator's count,
  and the Anthropic Nov 3 date is unconfirmed.
