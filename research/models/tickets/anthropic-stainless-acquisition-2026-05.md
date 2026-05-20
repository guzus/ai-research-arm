---
slug: anthropic-stainless-acquisition-2026-05
title: Anthropic acquires Stainless (SDK / MCP platform)
company: Anthropic
model: null
status: confirmed
status_note: |
  Official Anthropic announcement (2026-05-18): Anthropic is acquiring
  Stainless (@stainlessapi), the SDK and MCP-server platform that has
  powered every Anthropic SDK since the earliest days of the API. Deal
  terms not disclosed in the announcement.
expected: null
labels:
  - acquisition
  - sdk
  - mcp
  - tooling
verification: confirmed
sources:
  - "@AnthropicAI"
  - "@stainlessapi"
created_at: 2026-05-20
updated_at: 2026-05-20
closed_at: null
closed_reason: null
history:
  - ts: 2026-05-20
    change: "Created — Anthropic announced (2026-05-18, official @AnthropicAI) the acquisition of @stainlessapi, the SDK + MCP-server platform behind Anthropic's SDKs since the earliest API days"
---

Anthropic announced on 2026-05-18 that it is acquiring **Stainless**
(@stainlessapi), the SDK and MCP-server platform that has generated and
maintained Anthropic's client SDKs since the earliest days of the API.

This is a tooling/developer-platform acquisition rather than a model
release, but it sits squarely on the roadmap: bringing SDK + MCP-server
generation in-house tightens Anthropic's control over the developer
surface (and MCP, the protocol Anthropic stewards) at a moment when the
agent ecosystem is consolidating around it.

Deal terms were not disclosed in the announcement. No regulatory or
close-date signal yet.

**Transition triggers:**
- Deal close, integration milestones, or terms disclosure → UPDATE with a
  history entry.
- ≥4 weeks with the acquisition settled into normal coverage →
  `status: closed` with `closed_reason: released-and-aged`.

**Dedup note:** further Stainless / SDK / MCP-platform signal from
Anthropic UPDATES this ticket. Other Anthropic acquisitions get their own
`anthropic-<target>-acquisition-<yyyy-mm>` ticket.
