---
slug: anthropic-claude-code-design-2026-08
title: Claude Code /design — artboard design workflow ships as a research preview
company: Anthropic
model: null
status: released
status_note: |
  Anthropic shipped a **`/design` skill in Claude Code (research preview)**
  on **2026-08-17**, announced by **@ClaudeDevs** (21:57 UTC): "Claude Code
  can design now. The new /design skill (research preview) brings Claude
  Design's artboard workflow into the CLI and Desktop, built on artifacts.
  Run /design to get editable artboards for your UI — pick one, tweak it,
  then have Claude implement it." **Available on Pro, Max, Team and
  Enterprise**; requires a Claude Code update.

  Part of a dense week of Claude surface expansion, all from primary
  accounts: **Claude Cowork on mobile** for all paid plans, **Gmail send +
  Google Drive file management** via updated connectors with new in-chat UI
  components, and performance work (Claude Code CLI **2x less CPU at p99**
  after fixing Bun GC timer behaviour; Claude Desktop **~2x faster
  startup**). @testingcatalog additionally spotted an unshipped **"Hub
  Mode"** and a Claude-managed **task board for sub-agents** under a
  `/hub` path — those are unshipped and are *not* covered by this ticket's
  `released` state.
expected: "Shipped as a research preview 2026-08-17 on Pro/Max/Team/Enterprise. Pending: exit from research preview, and whether the spotted /hub task-board and Hub Mode surfaces ship as part of the same design/orchestration push"
labels:
  - anthropic
  - claude-code
  - developer-tooling
  - research-preview
  - released
verification: confirmed
sources:
  - "@ClaudeDevs"
  - "@testingcatalog"
  - "@kimmonismus"
created_at: 2026-08-19
updated_at: 2026-08-19
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-19
    change: "Created — Anthropic shipped a /design skill in Claude Code as a research preview on 2026-08-17 (@ClaudeDevs 21:57 UTC), bringing Claude Design's artboard workflow into the CLI and Desktop on top of artifacts; available on Pro, Max, Team and Enterprise. Corroborated by @testingcatalog the same evening. Logged alongside the same week's Claude surface expansion (Cowork on mobile for all paid plans, Gmail send + Drive management via updated Google connectors, Claude Code CLI 2x less CPU at p99, Claude Desktop ~2x faster startup) and the separately-spotted, unshipped Hub Mode / /hub sub-agent task board. Status released; verification confirmed (Anthropic's own developer account)."
---

Anthropic put **design generation inside Claude Code**. The `/design`
skill, shipped **2026-08-17** as a **research preview**, brings the
artboard workflow from Claude Design into the CLI and Desktop on top of
artifacts: run `/design`, get editable artboards for a UI, pick one, tweak
it, then have Claude implement it. It is live on **Pro, Max, Team and
Enterprise**.

**Why it is a ticket.** It closes the loop that coding agents have been
missing. The recurring complaint this cycle — @nutlope's "stop letting your
agents ship ugly UIs," @kimmonismus's "software is about to have a taste
problem… generating a working app is close to free now, and from here what
separates products is judgment" — is about the gap between *code that runs*
and *a product worth shipping*. Putting a design step in front of the
implementation step is Anthropic's answer, and it arrives the same week
that competing design-agent products (OJO) launched into the same gap.

**It is one of several surfaces shipped in the same week**, all from
primary accounts: **Claude Cowork on mobile** for every paid plan, **Gmail
sending and Google Drive file management** through updated connectors with
new in-chat UI components, and two performance wins worth noting because
they are unusually specific — Claude Code CLI now uses **2x less CPU at
p99** (Bun's GC was running on a fixed timer and stealing CPU mid-turn; it
now waits for idle), and Claude Desktop starts **~2x faster** than a month
ago.

**What is explicitly not shipped.** @testingcatalog spotted a **"Hub
Mode"** and a Claude-managed **task board for sub-agents** under a `/hub`
path — an orchestration surface for visualising multiple agents' progress.
Both are unshipped leaks and are logged here as context only; this ticket's
`released` state covers `/design`, not them. If `/hub` ships it likely
warrants its own ticket.

**Transition triggers:**
- `/design` exits research preview, or lands on additional plans/surfaces →
  UPDATE.
- Hub Mode or the `/hub` sub-agent board ships → new ticket for the
  orchestration surface; do not fold it in here.
- ≥4 weeks past GA, settled into normal coverage →
  `closed: released-and-aged`.

**Dedup note:** Claude Team plan pricing stays on
[[anthropic-claude-team-plan-2026-07]]; the always-on Conway agent stays on
[[anthropic-claude-conway-2026-07]]. Further `/design` signal UPDATES this
ticket.
