---
slug: anthropic-cloud-sessions-ga-2026-09
title: Claude Code cloud sessions leave research preview, with one-time Pro/Max credits
company: Anthropic
model: Claude Code (cloud sessions)
status: released
status_note: |
  @ClaudeDevs, 2026-09-23 21:23 UTC: "Cloud sessions are officially available
  and out of research preview! They let you keep Claude Code working, even when
  your laptop is closed. Existing subscribers get a one-time credit to try them:
  $100 on Pro, $250 on Max."

  Terms, from the same thread and a follow-up: claim via the link or
  `/claim-credit` in the CLI, GitHub must be connected to start a session,
  claim deadline **2026-10-07**, one credit per account, cloud sessions only.
  The credit is separate from usage limits and is spent *first*, after which
  cloud sessions fall back onto normal Pro/Max plan usage — Anthropic posted a
  correction (2026-09-24 01:57 UTC) because the original wording read to some
  users as cloud sessions being credit-metered rather than plan-metered.

  Shipped in the same window and tracked here as adjacent context rather than
  as their own tickets: Projects in Claude Code can now run threads locally
  (@ClaudeDevs, 2026-09-23 22:49 UTC), with Projects access still rolling out
  from a waitlist to more Pro and Max users; and a Claude Marketplace with Slack
  and Notion connectors and third-party agents, which in this cycle's signal
  appears only in a third-party aggregator brief (@testingcatalog) with no
  Anthropic-primary post captured — so it is noted, not asserted.
expected: "GA. Watch whether the Oct 7 credit expiry is extended and whether cloud sessions get their own pricing separate from Pro/Max plan usage."
labels:
  - anthropic
  - claude-code
  - agent-product
  - released
verification: confirmed
sources:
  - https://x.com/ClaudeDevs/status/2102871550974427462
  - https://x.com/ClaudeDevs/status/2102871555244257518
  - https://x.com/ClaudeDevs/status/2102871554069774451
  - https://x.com/ClaudeDevs/status/2102940480736821610
  - https://x.com/ClaudeDevs/status/2102893178273874102
  - https://x.com/ClaudeDevs/status/2102893179662106684
  - https://x.com/testingcatalog/status/2103015463089238076
created_at: 2026-09-24
updated_at: 2026-09-24
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-24
    change: "Created — RELEASED. @ClaudeDevs announced on 2026-09-23 21:23 UTC that Claude Code cloud sessions are out of research preview and generally available, letting sessions keep running with the laptop closed. Launch promo: a one-time credit of $100 (Pro) / $250 (Max) for existing subscribers, claimed via link or `/claim-credit`, GitHub connection required, claim by 2026-10-07, one per account, cloud sessions only. Anthropic clarified 2026-09-24 01:57 UTC that cloud sessions run on the normal Pro/Max plan and the credit is merely spent first — issued as a correction after the original announcement was widely read as cloud sessions being separately metered. Verification confirmed on company-primary posts. Adjacent, same window, deliberately not given separate tickets: local thread execution for Projects in Claude Code (@ClaudeDevs, company-primary) and a Claude Marketplace with Slack/Notion connectors and Cursor/CrowdStrike agents, which appears only in @testingcatalog's third-party daily brief with no Anthropic post in this cycle's signal."
---

The product change is small; the billing question it opened is the interesting
part. Cloud sessions decouple a Claude Code run from the developer's machine —
close the laptop, the agent keeps going — which is the precondition for
long-horizon agent work being a normal thing rather than a babysitting exercise.
Anthropic shipped the same capability shape as the always-on agents its
competitors have been marketing ([[anthropic-claude-conway-2026-07]] is the
internal remote-agent line this descends from).

What made it noisy was the credit. Announcing "$100 on Pro, $250 on Max" next to
a GA notice reads as a price, and enough users read it that way that Anthropic
posted a clarification within five hours: cloud sessions bill against the
existing plan, and the credit is an optional pot spent before plan usage. The
correction is the durable fact here — cloud execution is a plan feature, not a
metered add-on, at least for now.

The claim deadline (2026-10-07) is the thing to watch. A two-week window on a
one-time credit is a usage-shaping instrument, not a giveaway: it front-loads
demand for a newly-GA compute surface at exactly the moment Anthropic is also
absorbing Opus 5.5 traffic ([[anthropic-opus-5-5-2026-09]]) and raised Claude
Code 5-hour limits 20%. If the deadline slips, that is evidence the capacity
held; if cloud sessions get separate pricing before then, that is evidence it
did not.

Marketplace is recorded in `status_note` at aggregator-only confidence on
purpose. If an Anthropic-primary announcement surfaces, it is a distinct
shipping artifact and earns its own ticket rather than being folded in here.
