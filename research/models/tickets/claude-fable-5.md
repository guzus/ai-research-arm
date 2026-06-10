---
slug: claude-fable-5
title: Claude Fable 5 — public release of the Mythos-class model
company: Anthropic
model: Claude Fable 5
status: released
status_note: |
  **Publicly released 2026-06-09** (@claudeai 17:08 UTC: "Introducing Claude
  Fable 5: a Mythos-class model that we've made safe for general use. Its
  capabilities exceed those of any model we've ever made generally available.").
  Fable 5 is the **public-safe derivative of the Mythos class** ([[mythos-public-release]]):
  same frontier intelligence, wrapped in safety classifiers that **block or
  downgrade high-risk prompts** (cybersecurity, biology, chemistry, model
  distillation) and silently fall back to **Opus 4.8** ([[opus-4-8]]) — reported
  to trigger in **<5% of sessions**. The unrestricted twin, **Mythos 5**, ships
  only to vetted defenders / governments and stays tracked on
  [[mythos-public-release]]. Pricing **$10 / $50 per MTok** in/out (less than half
  the prior Mythos Preview's $25/$125). **Free for Pro / Max / Team until
  2026-06-22**, then usage credits required. Anthropic also introduced a new
  **30-day data-retention** policy across Fable/Mythos traffic. Available via
  the Claude apps, Claude API, Claude Code, and major cloud platforms.
expected: "Free access for Pro/Max/Team through 2026-06-22; credit-metered thereafter"
labels:
  - frontier-model
  - released
  - mythos-class
  - safety-gated
  - coding
  - vision
verification: confirmed
sources:
  - "@claudeai"
  - "@AnthropicAI"
  - "@venturetwins"
  - "@chimpansky"
  - "@scaling01"
created_at: 2026-06-10
updated_at: 2026-06-10
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-10
    change: "Created — Anthropic publicly released **Claude Fable 5** on 2026-06-09 (@claudeai 17:08 UTC, ~90K likes / 12.8K RT): a Mythos-class model 'made safe for general use,' Anthropic's strongest generally-available model. Two-tier launch alongside the restricted **Mythos 5** (vetted defenders/govts, tracked on [[mythos-public-release]]). Fable 5 falls back to **Opus 4.8** on high-risk prompts (cyber/bio/chem/distillation), reportedly <5% of sessions. Pricing $10/$50 per MTok (≈½ the Mythos Preview's $25/$125); free for Pro/Max/Team until 2026-06-22, then credit-metered; new 30-day retention policy. Benchmarks: SOTA on Artificial Analysis (~65), SWE-bench Pro 80.3, Hex first-ever 90% on its analytics benchmark; Stripe used it to migrate a 50M-line Ruby codebase in ~a day. Spun out from [[mythos-public-release]] per that ticket's dedup note (a toned-down public variant with its own release plan = separate ticket). Status released, verification confirmed (official @claudeai/@AnthropicAI primary)"
---

**Claude Fable 5** is the public-facing resolution of the long-running
question tracked on [[mythos-public-release]]: whether Anthropic would
ever bring its post-Opus, Mythos-class frontier intelligence out of the
gated Project Glasswing preview and into general availability. On
**2026-06-09** it did — but as a **two-tier launch**, not a single
public release.

**The two products, one set of weights.**
- **Fable 5 (public):** Mythos-class capability with hard safety
  classifiers. When a prompt touches cybersecurity, biology, chemistry,
  or model distillation, the classifier blocks or downgrades the request
  and hands it to **Opus 4.8** ([[opus-4-8]]) — no refusal banner, just a
  quieter answer. Anthropic reports the fallback triggers in **fewer than
  5% of sessions**.
- **Mythos 5 (restricted):** the unrestricted twin, available only to
  approved organizations (critical-infrastructure defenders, select
  life-sciences partners, government) via Project Glasswing and an
  upcoming trusted-access program. It is **not** publicly available and
  continues to be tracked on [[mythos-public-release]].

**Why this is its own ticket.** Per the dedup note on
[[mythos-public-release]], a toned-down Anthropic variant with a
*different release plan* gets its own ticket. Fable 5 is exactly that:
the Cherny-floated "toned-down version in the foreseeable future" became
a real, publicly-shipping product, while Mythos proper stays gated. This
ticket carries the public-release lifecycle; the Mythos ticket carries
the gated line.

**Commercial shape.** Pricing is **$10 per MTok input / $50 per MTok
output** — less than half the $25/$125 reported for the earlier Mythos
Preview. It is **free for Pro, Max, and Team subscribers until
2026-06-22**, after which continued use requires purchased credits.
Early users widely flag it as **token-hungry and expensive** ("burst
compute" — best reserved for hard planning, refactors, and final review,
then routing down to cheaper models). Anthropic also shipped a new
**30-day data-retention** policy across Fable/Mythos traffic concurrent
with launch.

**Capability signal.** Independent and Anthropic-cited benchmarks put
Fable 5 at the frontier: ~65 on Artificial Analysis (chart-topping),
**80.3 on SWE-bench Pro**, Hex's first-ever 90% on its long-running
analytics benchmark, and strong vision results (rebuilding web apps from
screenshots; beating Pokémon FireRed from raw frames). The marquee
real-world demo: **Stripe migrated a ~50-million-line Ruby codebase in
about a day**, work normally measured in months.

**Transition triggers:**
- Successor public model (e.g. a Fable 5.x or next-class public release)
  → create a new ticket; do not reopen this one.
- ≥4 weeks past 2026-06-09 release with no successor → close with
  `released-and-aged`.
- Anthropic pulls or pauses general availability, or materially changes
  the safety-fallback behaviour → keep `released`, document via history.
- Mythos 5 itself flips to public availability → that is a state change on
  [[mythos-public-release]], not here.

**Dedup note:** Fable 5 pricing, availability, benchmark, and safety-
classifier signal UPDATES this ticket. Mythos 5 (restricted) /
Glasswing / gated-preview signal stays on [[mythos-public-release]].
