---
slug: opus-4-7
title: Claude Opus 4.7 — public release
company: Anthropic
model: Claude Opus 4.7
status: closed
status_note: |
  Released 2026-04-16. Now the standard Opus offering, including the [1m]
  context tier (model ID claude-opus-4-7[1m]). Closing per "released-and-aged"
  rule (≥4 weeks past public release).
expected: null
labels:
  - released
  - frontier-model
  - context-1m
verification: confirmed
sources:
  - https://www.anthropic.com/news/claude-opus-4-7
  - "@AnthropicAI"
  - "@testingcatalog"
  - "@kimmonismus"
created_at: 2026-03-20
updated_at: 2026-05-19
closed_at: 2026-05-19
closed_reason: released-and-aged
history:
  - ts: 2026-03-20
    change: Created — first leak traces of "Opus 4.7" appearing in GCP console (same pattern Mythos would later follow)
  - ts: 2026-04-10
    change: "Pricing trajectory clarified ($15 / $75 per MTok, in line with 4.6); release window narrowing"
  - ts: 2026-04-16
    change: "Public release — Anthropic announcement, available on api.anthropic.com, AWS Bedrock, and GCP Vertex AI"
  - ts: 2026-04-24
    change: "Opus 4.7 [1m] context tier rolled out — model ID claude-opus-4-7[1m], usable in Claude Code"
  - ts: 2026-05-19
    change: "Closed — released-and-aged (≥4 weeks past public release, now standard coverage)"
---

Claude Opus 4.7 was Anthropic's spring-2026 frontier release: the
direct successor to Opus 4.6, shipped publicly on **2026-04-16** and
followed eight days later by the **[1m] context tier** that became the
default for long-context work in Claude Code.

The release pattern set the template that Mythos is now following: GCP
Cloud Console artifacts appeared ~3-4 weeks before public availability,
and the tiered context release (base tier → [1m] tier) gave Anthropic a
post-launch lever to revisit pricing and rate limits without re-launching
the model.

**Why this ticket is closed:** Opus 4.7 is the current standard Opus
offering. Day-to-day coverage of Opus 4.7 features, pricing tweaks, or
post-train refreshes does not need its own active ticket — those land
under whichever feature ticket they belong to (e.g. a new "Opus 4.7
priority tier" feature would get its own ticket and reference this one).

**If a successor (Opus 4.8) emerges:** create `opus-4-8` as a new
ticket. Do not re-open this one. The Opus 4.7 → Opus 4.8 transition
shows up in the successor's `history`, not here.

**Historical link:** this ticket is the reference point for the
"GCP-console-before-release" detection pattern that surfaces frequently
in [Mythos](./mythos-public-release.md) and
[Gemini 3.2 Flash](./gemini-3-2-flash.md).
