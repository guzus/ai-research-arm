---
slug: xiaomi-mimo-code-2026-06
title: Xiaomi open-sources MiMo Code — coding-focused open-weight LLM
company: Xiaomi
model: MiMo Code
status: released
status_note: |
  **Xiaomi open-sourced MiMo Code** (surfaced 2026-06-11/12), a **coding-focused
  open-weight LLM**, drawing community debate versus **Qwen** and **DeepSeek**
  coding alternatives (357 pts on Hacker News). Distinct from the
  general-purpose **MiMo v2.5 Pro** line ([[xiaomi-mimo-v2-5-pro]]): this is a
  separate, code-specialized open release. Adds to the open-weight coding race
  alongside MiniMax M3 ([[minimax-m3]]) and Cohere's BLS Mini Code
  ([[cohere-bls-mini-code-1]]).
expected: "Open weights available now"
labels:
  - open-weight
  - coding
  - xiaomi
  - released
verification: partial
sources:
  - "@HackerNews"
created_at: 2026-06-12
updated_at: 2026-06-12
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-12
    change: "Created — Xiaomi open-sourced MiMo Code, a coding-focused open-weight LLM (surfaced 2026-06-11/12, 357 pts on HN), with community debate vs Qwen/DeepSeek coding models. Separate code-specialized line from the general-purpose MiMo v2.5 Pro ([[xiaomi-mimo-v2-5-pro]]). Status released (open weights out); no captured repo/model-card URL in-window → verification partial"
---

**Xiaomi open-sourced MiMo Code**, a **coding-focused open-weight LLM**, which
surfaced in the 2026-06-11→12 window and drew an active Hacker News thread
(357 pts) debating it against **Qwen** and **DeepSeek** coding alternatives.

**Why it's its own ticket.** MiMo Code is a **code-specialized** release,
distinct from Xiaomi's general-purpose **MiMo v2.5 Pro** line
([[xiaomi-mimo-v2-5-pro]]). Per the dedup convention, a separately-named model
with its own release gets its own ticket rather than folding into the existing
MiMo line.

**Where it fits.** It joins a busy open-weight coding race: **MiniMax M3**
leads open SWE-Bench Pro ([[minimax-m3]]) and **Cohere BLS Mini Code**
([[cohere-bls-mini-code-1]]) targets the small-code niche. Open-source coding
models are increasingly where Chinese labs apply pressure on the closed
agentic-coding incumbents.

**Why `released` / `partial`.** Open weights being downloadable makes the
release `released`. No primary repository or model-card URL was captured
in-window, so `verification` stays `partial`.

**Transition triggers:**
- Primary repo / model card / benchmark suite → UPDATE, advance
  `verification` to `confirmed`.
- A successor MiMo Code version → new ticket; do not reopen this one.
- ≥4 weeks past release, settled into normal coverage → `closed: released-and-aged`.

**Dedup note:** further MiMo Code (code-specialized) signal UPDATES this
ticket. General MiMo v2.5 Pro signal stays on [[xiaomi-mimo-v2-5-pro]].
