---
slug: anthropic-claude-oceanus-v1
title: Anthropic "claude-oceanus-v1-p" — red-team model-name leak
company: Anthropic
model: Claude Oceanus
status: rumored
status_note: |
  A new Anthropic model name, **`claude-oceanus-v1-p`**, reportedly
  appeared for **red-team access** (relayed @WesRoth 2026-06-05, citing
  @testingcatalog 2026-06-04 ~846 likes). Read as a possible early sign
  Anthropic is preparing/testing a newer generation of Mythos-related
  models before any broader release. Single-source leak (a name string +
  red-team gating); no Anthropic primary, no benchmarks, pricing, or
  release window. Possibly a successor to / sibling of Claude Mythos
  (see [[mythos-public-release]]).
expected: "Unknown — red-team access only; no release window"
labels:
  - frontier-model
  - rumor
  - red-team
  - anthropic
verification: unverified
sources:
  - "@testingcatalog"
  - "@WesRoth"
created_at: 2026-06-05
updated_at: 2026-06-05
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-05
    change: "Created — a new Anthropic model name `claude-oceanus-v1-p` reportedly surfaced for red-team access (@WesRoth 2026-06-05 relaying @testingcatalog 2026-06-04). Possible Mythos-adjacent next-gen model in pre-release testing ([[mythos-public-release]]). Single-source name-string leak, no Anthropic primary → rumored / unverified"
---

A new Anthropic model identifier — **`claude-oceanus-v1-p`** — was
reported to have appeared for **red-team access**, relayed by @WesRoth on
2026-06-05 citing a 2026-06-04 @testingcatalog post (~846 likes). The
`-p` suffix and red-team gating fit Anthropic's usual pattern of exposing
a frontier candidate to safety/red-team testers well before any public or
even gated-preview surface.

The framing in the signal is that Oceanus may be a **newer generation of
Mythos-related models** — i.e. a possible successor to or sibling of
Claude Mythos ([[mythos-public-release]]), which itself remains a gated,
no-public-release frontier preview. There is nothing here beyond the
name: no benchmarks, no pricing, no architecture, no release window.

**Why `rumored` / `unverified`.** This is a single-source artifact — a
model-name string observed in a red-team context and amplified by AI-news
accounts — with no Anthropic primary (no @AnthropicAI / @claudeai post,
no Anthropic blog). Per the schema that is a textbook `rumored` +
`unverified` entry. It is tracked because a red-team model-name leak is
exactly the kind of early shipping-artifact signal this timeline exists
to catch, and the Mythos dedup note calls for a distinct Anthropic model
variant to get its own ticket.

**Transition triggers:**
- A second corroboration (another tester, an Anthropic system-card /
  policy mention, a console artifact) → UPDATE, raise to partial /
  in-testing.
- An Anthropic primary or public/gated preview → advance to confirmed /
  released and refresh the title if the marketing name differs.
- ≥15 daily cycles with no fresh corroboration → `closed:
  stale-rumor-unverified`.
- If it turns out to be a relabel of an already-tracked model (e.g.
  Mythos) → `closed: superseded-by:<slug>`.

**Dedup note:** further `claude-oceanus` signal UPDATES this ticket.
Mythos-specific signal stays on [[mythos-public-release]].
