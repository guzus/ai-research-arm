---
slug: openai-codex-platform-2026-05
title: OpenAI Codex platform — Mac/iOS/Android/Windows agentic coding cadence
company: OpenAI
model: Codex
status: released
status_note: |
  OpenAI shipped a multi-week "Codex Thursday" cadence in May 2026 that
  built out the Codex agentic-coding surface across operating systems:
  Codex in the ChatGPT mobile app (iOS + Android preview, 2026-05-14),
  Mac Appshots + hooks + programmatic access tokens (2026-05-14 / 2026-05-21),
  Codex can securely use Mac apps from a phone even when the Mac is
  locked (2026-05-22), and **computer use on Windows + Codex in ChatGPT
  mobile for Windows (2026-05-29, primary @OpenAI announcement)**. The
  shipping surface for OpenAI's agentic-coding lane, distinct from the
  underlying GPT-5.x family. Parallel to xAI's Grok Build CLI
  ([[xai-grok-build-2026-05]]), Anthropic Claude Code rate-limit and
  Fast-mode pushes around [[opus-4-8]], and Google Antigravity 3x
  rate-limit resets logged on [[gemini-3-2-flash]]. **2026-05-31
  milestone**: @thsottiaux (Tibo, OpenAI; 05:59 UTC, ~320 RT) — "Five
  million users would agree. Resetting the limits tomorrow morning to
  celebrate. Time to go /fast." RT'd by @sama 14:48 UTC quote-tweeting
  Aaron Levie's "switching back from Claude to Codex xhigh to remind
  you how much better 5.5 is right now." First concrete OpenAI-side
  Codex penetration number, though the denominator (Codex API users vs
  Plus/Pro seats vs ChatGPT-as-whole) is undefined. **2026-05-31 same-
  day fix**: @simonw 18:51 UTC caught a Codex Desktop "Copy as Markdown"
  feature regression; @PhilippSpiess (OpenAI) committed at 21:17 UTC
  to restore — first publicly-acknowledged same-day Codex Desktop fix
  pledge.
expected: null
labels:
  - coding
  - agentic-cli
  - released
  - codex
  - windows
verification: confirmed
sources:
  - "@OpenAI"
  - "@OpenAIDevs"
  - "@sama"
  - "@thsottiaux"
  - "@PhilippSpiess"
  - "@simonw"
created_at: 2026-05-30
updated_at: 2026-06-01
closed_at: null
closed_reason: null
history:
  - ts: 2026-05-30
    change: "Created — multi-week May 2026 Codex platform shipping cadence consolidated: Codex in ChatGPT mobile preview iOS/Android 2026-05-14, hooks + programmatic access tokens 2026-05-14, Mac Appshots 2026-05-21, secure Mac app control from phone with screen off 2026-05-22, and the 2026-05-29 push of computer use on Windows + Codex in ChatGPT mobile for Windows (primary @OpenAI). Distinct from underlying GPT-5.x family; tracks the developer surface OpenAI is using to compete with Claude Code, Grok Build (xai-grok-build-2026-05), and Antigravity"
  - ts: 2026-06-01
    change: "5M Codex users milestone: @thsottiaux (Tibo, OpenAI) 2026-05-31 05:59 UTC ~320 RT — 'Five million users would agree. Resetting the limits tomorrow morning to celebrate. Time to go /fast.' RT'd by @sama 14:48 UTC. First concrete OpenAI-side Codex penetration number (denominator undefined: API users vs Plus/Pro seats vs ChatGPT-as-whole). Codex Desktop 'Copy as Markdown' regression caught by @simonw 2026-05-31 18:51 UTC (~479 likes), committed-to-fix by @PhilippSpiess (OpenAI) 21:17 UTC — first publicly-acknowledged same-day Codex Desktop fix pledge. @reach_vb logs Codex multi-file ops anecdote (verified codec/fps/resolution, stitched MP4s without re-encoding) 2026-05-31 23:09 UTC"
---

This ticket tracks the **OpenAI Codex platform** as a shipping surface —
the agentic-coding CLI + ChatGPT-app integration that OpenAI has been
extending Thursday-by-Thursday across May 2026.

**What shipped in this window (all primary @OpenAI / @OpenAIDevs):**

- **2026-05-14 (Codex Thursday):** Codex in the ChatGPT mobile app
  (preview, iOS + Android), letting users start new work, review
  outputs, steer execution, and approve next steps from the phone while
  Codex keeps running on a laptop, Mac mini, or devbox. Same drop added
  hooks (scripts at key points in the Codex loop) and programmatic
  access tokens for Business/Enterprise teams.
- **2026-05-21 (Codex Thursday):** Appshots — `Command-Command` on Mac
  attaches an app window to a Codex thread, giving Codex both a
  screenshot and text from the window including content beyond what's
  visible onscreen (cross-plan on Mac; enterprise access coming soon).
  Sam Altman: "new codex ships today!"
- **2026-05-22 (Codex Thursday highlights):** Codex can securely use
  apps on a Mac from a phone, even when the Mac is locked and the
  screen is off. Plus advanced annotation mode for collaborating on web
  pages.
- **2026-05-29 (Codex Thursday):** **Computer use now works on
  Windows**, so Codex can take action on a Windows machine; and Windows
  support for **Codex in the ChatGPT mobile app**, with the user
  starting/reviewing/steering tasks on the go while work continues on
  the Windows machine. Framed as "an early experience" but is the
  cross-OS parity move users had been asking for.

**Why this is its own ticket.** Codex runs on the GPT-5.x family — the
shipping artifact here is the *platform surface*, not a model. Within
the model-timeline lane, this parallels
[xai-grok-build-2026-05](./xai-grok-build-2026-05.md) (the Grok Build
CLI + `grok-build-0.1` shipping push) and the Claude Code rate-limit /
Fast-mode bundle around [opus-4-8](./opus-4-8.md). The four labs are
all visibly competing on the developer-tooling surface in May 2026, and
keeping each lab's push in a dedicated ticket lets the lane stay
diffable.

**Transition triggers:**

- A new shipping artifact in the Codex platform (e.g. a dedicated
  Codex-tier OpenAI model with its own name, Linux computer-use, or a
  pricing change) → UPDATE with a history entry; do not split into a
  new ticket unless it represents a genuinely independent surface.
- A successor platform rename → new ticket, link back here.
- ≥4 weeks past the 2026-05-29 Windows shipping with no fresh material
  cadence signal → `closed: released-and-aged`.

**Dedup note:** further OpenAI Codex platform / Codex Thursday signal
UPDATES this ticket. The OpenAI "Guaranteed Capacity" announcement
(2026-05-19), the OpenAI Foundation $250M commitment (2026-05-27), and
the unit-distance / Erdős math-breakthrough announcement (2026-05-20)
are adjacent OpenAI events and would each get their own ticket if they
need active tracking — they are not duplicates of this Codex-platform
ticket.
