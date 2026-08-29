---
slug: openai-codex-security-cli-2026-07
title: OpenAI open-sources the Codex Security CLI
company: OpenAI
model: Codex Security CLI
status: closed
status_note: |
  OpenAI announced (2026-07-29 00:35 UTC, official @OpenAI) that it
  "quietly released the open-source Codex Security CLI, but Hacker News
  found it before we had a chance to share it here" — an early release
  they're iterating on based on feedback. It scans repositories, tracks
  security findings across runs, verifies fixes, and wires security
  checks into CI/CD. Install via `npm install @OpenAI/codex-security`.
  Distinct from the existing Codex-family tickets
  [[openai-codex-platform-2026-05]] (the broader Codex platform launch)
  and [[openai-codex-hardware-2026-06]] (dedicated Codex hardware) — this
  is a standalone open-source security-scanning tool under the Codex
  brand. Primary company account, concrete public artifact (npm package)
  → status `released`, verification `confirmed`.
expected: "Closed 2026-08-26 as released-and-aged: shipped publicly 2026-07-29 as an npm package and settled into normal coverage with no follow-on signal in four weeks"
labels:
  - openai
  - codex
  - security
  - open-source
  - developer-tooling
  - released
verification: confirmed
sources:
  - "@OpenAI"
  - https://x.com/OpenAI/status/2082263717916586117
  - https://x.com/OpenAI/status/2082263719460094127
  - https://x.com/OpenAI/status/2082263720777101505
created_at: 2026-07-29
updated_at: 2026-08-26
closed_at: 2026-08-26
closed_reason: "released-and-aged"
history:
  - ts: 2026-07-29
    change: "Created — OpenAI open-sourced the Codex Security CLI (npm install @OpenAI/codex-security), announced via its official account after Hacker News discovered it first. Scans repos, tracks findings across runs, verifies fixes, adds CI/CD security checks. Framed as an early release still being iterated on. Primary source, concrete public npm package → status released, verification confirmed."
  - ts: 2026-08-26
    change: "Closed - released-and-aged. The Codex Security CLI shipped publicly on 2026-07-29 (official @OpenAI, npm package @OpenAI/codex-security) and has now been out four weeks with no captured follow-on signal in the intervening cycles: no version bump with material new capability, no security-research evaluation of its effectiveness, and no adoption datapoint. That is precisely the transition trigger this ticket set at creation ('>=4 weeks settled into normal coverage with no further developments -> closed: released-and-aged'), and it is the ordinary end state for a shipped tool rather than a judgement about the product. Closing preserves the full record; a future material development - a major release, a vulnerability in the tool itself, or deprecation - would open a successor ticket referencing this slug rather than reopening it. Broader Codex platform news continues on [[openai-codex-platform-2026-05]]."
---

**OpenAI** open-sourced the **Codex Security CLI**, a standalone
security-scanning tool distributed under the Codex brand. The company
disclosed it somewhat sheepishly: "We quietly released the open-source
Codex Security CLI, but Hacker News found it before we had a chance to
share it here."

**What it does.** Per OpenAI's own description, the CLI can scan
repositories, track security findings across multiple runs, verify that
fixes actually resolved flagged issues, and be wired into CI/CD
pipelines as an automated security gate. Installation is via
`npm install @OpenAI/codex-security`, with source and docs published
alongside the npm package.

**Why a separate ticket.** This is a distinct product from
[[openai-codex-platform-2026-05]] (the broader Codex coding-agent
platform launch) and [[openai-codex-hardware-2026-06]] (dedicated Codex
inference hardware) — a standalone, purpose-built security tool rather
than a general coding agent or infrastructure investment.

**Confirmed vs. reported.** This is about as clean a `confirmed` /
`released` case as this lane tracks: OpenAI's own official account
announced it, with a concrete, installable public artifact (an npm
package with source and docs) rather than a claim requiring third-party
corroboration.

**Transition triggers:**
- Notable adoption, a security-research writeup evaluating its
  effectiveness, or a version bump with material new capability →
  UPDATE.
- ≥4 weeks settled into normal coverage with no further developments →
  `closed: released-and-aged`.

**Dedup note:** further Codex Security CLI signal (version updates,
adoption, security community reception) UPDATES this ticket. Broader
Codex platform news stays on [[openai-codex-platform-2026-05]].
