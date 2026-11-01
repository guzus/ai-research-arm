---
slug: ai-text-watermarking
title: AI Text Watermarking
type: concept
aliases: ["text watermarking", "Grok watermarking", "invisible text watermark", "SynthID Text", "TextSeal2"]
tags: [watermarking, provenance, transparency, policy]
description: Invisible watermarks embedded in model-generated text so a detector can flag it; xAI announced Grok text watermarking on 2026-10-31, leaving ChatGPT as the last major North American text model without one by one count.
created_at: 2026-11-01
timestamp: 2026-11-01T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-11-01", path: research/digest/2026-11-01-digest.md}
---

**AI text watermarking** hides a statistical signal in generated text so that
the provider (or a detector it controls) can later recognize the output as
machine-made. It is becoming the default posture among large labs.

## State of play (2026-11-01)

- **[[xai]]** announced invisible watermarking for Grok text on Oct 31. It
  appears to roll out globally from **Nov 7**, with an opt-out page. By
  @AndrewCurran_'s count, North American ChatGPT ([[openai]]) is now the only
  major text model without one.
- Anthropic's watermark rollout reportedly **misses two older Claude models**
  (The Decoder); see [[anthropic]].
- The push follows the **EU Code of Practice on Transparency of AI-Generated
  Content**, signed by Anthropic, OpenAI, Google, Meta, Microsoft and Mistral
  but **not xAI** — see [[eu-ai-regulation]].
- Research: Meta's **TextSeal2** watermark is reported to survive speculative
  decoding (arXiv, one-line mention in the digest).

## Caveats

- Critics note **only the lab holds the detector**, so the watermark gives
  users and third parties no independent verification.
- The "ChatGPT is the only one without" claim is a single commentator's count,
  and xAI's rollout date is inferred ("appears to"), not a confirmed schedule.
