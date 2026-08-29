---
slug: microsoft-copilot-cowork-2026-06
title: Microsoft Copilot Cowork GA (multi-model, usage-based) — reportedly evaluating DeepSeek V4
company: Microsoft
model: null
status: closed
status_note: |
  **Satya Nadella** announced (2026-06-16, own account) that **Copilot Cowork is
  generally available worldwide with multi-model support and usage-based
  pricing** (~**$0.01/task**, per relays) — every org can "put long-running
  agents to work." Separately, **Axios** reports Microsoft is **evaluating a
  Microsoft-hosted, fine-tuned DeepSeek V4** as a cheaper alternative to OpenAI
  and Anthropic for high-volume agentic tasks (Charles Lamanna: "costs can go
  very high") — a hedge away from its own marquee suppliers. The **Cowork GA is
  confirmed** (Satya's own account); the **DeepSeek-V4 angle is "evaluating," not
  deployed**, sourced to Axios via multiple relays → verification `partial`.
expected: "Cowork GA worldwide now (multi-model, usage-based ~$0.01/task); Microsoft-hosted fine-tuned DeepSeek V4 reportedly under evaluation for Cowork 'in coming weeks' (Axios) — not yet shipped"
labels:
  - product
  - agents
  - microsoft
  - deepseek
verification: partial
sources:
  - "@satyanadella"
  - "@ns123abc"
  - "@kimmonismus"
  - "@AndrewCurran_"
created_at: 2026-06-18
updated_at: 2026-07-16
closed_at: 2026-07-16
closed_reason: released-and-aged
history:
  - ts: 2026-06-18
    change: "Created — Satya Nadella announced (2026-06-16) Copilot Cowork GA worldwide with multi-model support and usage-based pricing (~$0.01/task); Axios reports Microsoft is evaluating a Microsoft-hosted fine-tuned DeepSeek V4 as a cheaper Cowork engine vs. OpenAI/Anthropic. Cowork GA confirmed (Satya's own account) → status released; the DeepSeek-V4 evaluation is reported (Axios via relays), not deployed → verification partial. 'Microsoft body blow to OpenAI' framings overstate Axios — it is evaluation, not a switch."
  - ts: 2026-07-16
    change: "Closed — ≥4 weeks past release with no unresolved transition triggers; settled into normal coverage. closed_reason: released-and-aged."
---

On **2026-06-16**, **Satya Nadella** posted that **Copilot Cowork is now
generally available worldwide, with multi-model support** and a move to
**usage-based pricing** (~**$0.01 per task**, per relays): "Every
organization can put long-running agents to work." Multi-model Cowork is
the structural enabler for the second half of this story.

**The DeepSeek angle.** **Axios** reports Microsoft is **evaluating a
Microsoft-hosted, fine-tuned DeepSeek V4** as a **cheaper alternative to
OpenAI and Anthropic** for high-volume agentic Cowork tasks (Charles
Lamanna told Axios "costs can go very high"). If it ships it would be an
optional, safeguarded, Azure-hosted tier — a notable supplier hedge by
OpenAI's largest backer.

**Confirmed vs. reported.** The **Cowork GA + multi-model + usage-based
pricing** is confirmed from **Satya's own verified account**, so the
shipping artifact is `released`. The **DeepSeek-V4 evaluation** is
**"considering/testing," not a committed deployment**, sourced to Axios
and relayed by multiple accounts → `verification: partial`. The viral
"Microsoft body blow to OpenAI" framing overstates the reporting.

**Context.** Pairs with the week's open-weight-substitution theme — GLM-5.2
([[zhipu-glm-5-2]]), DeepSeek's ~$7.4B raise
([[deepseek-funding-round-2026-05]]) — at the exact moment US policy is
restricting its own frontier ([[anthropic-fable-mythos-export-control-2026-06]]).
A Chinese open model named as the cheap tier inside a US enterprise
product is the structural shift to watch.

**Transition triggers:**
- Microsoft confirms DeepSeek V4 is actually selectable in Cowork → UPDATE,
  advance `verification`.
- Any policy/security pushback against a Chinese model in a US enterprise
  product → UPDATE.
- ≥4 weeks of settled coverage → `closed: released-and-aged`.

**Dedup note:** signal about *Cowork's availability/pricing/models*
UPDATES this ticket; a separate Microsoft model release gets its own
ticket (e.g. [[microsoft-mai-code-1-flash]]).
