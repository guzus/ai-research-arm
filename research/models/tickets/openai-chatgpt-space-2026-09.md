---
slug: openai-chatgpt-space-2026-09
title: ChatGPT Space — shared human/agent workspace announced at DevDay 2026
company: OpenAI
model: null
status: released
status_note: |
  **Announced at DevDay, 2026-09-29.** Space is a collaborative workspace inside
  ChatGPT where people, teams and their Dots work **in the same shared context**.
  The accompanying surfaces, per @AI_Whisper_X: **Pages** (documents humans and
  agents co-edit), collaborative **Slides**, **Teams**, and shared task lists.
  @insanekrishnaa's summary is the compact version: "chat is becoming a
  workspace."

  **Best available quotation is a press line, relayed.** @Zen_with_AI quotes
  coverage directly: "Most notably, OpenAI launched a feature called Space, a
  shared workspace inside ChatGPT where co-workers can collaborate with the
  chatbot and with their own Dots." Four independent recaps carry it
  (@masahirochaen ranked it ~7th of 25, @insanekrishnaa #3, @MagicPower21M,
  @AI_Whisper_X); no verbatim OpenAI post is in this cycle's fetch, hence
  verification `partial`.

  **The argument attached to it is worth recording separately from the product.**
  @Zen_with_AI claims Space productises an internal Anthropic engineering
  practice — engineers sharing all Claude sessions and project context, with
  tasks visible and claimable across the org — and predicts the pattern spreads
  through Silicon Valley within six months and across software within one to
  three years. The Anthropic-internals description is explicitly flagged by its
  relayer as unverified ("先说不保真"), was contested in its own replies as more
  likely a shared idea pool than a task free-for-all, and is recorded here as
  commentary, NOT as a fact about Anthropic.

  **Why its own ticket rather than folded into Dots.** Dots
  ([[openai-dots-agents-2026-09]]) is an agent runtime; Space is a
  multi-participant context and document surface that Dots plug into. They
  shipped together and are separable artifacts — a team could adopt one without
  the other — and Space is the one that changes where work lives rather than who
  does it.
expected: "Announced 2026-09-29 with Pages, Slides, Teams and shared task lists. Open: availability and plan gating (nothing in signal says which tiers get it); whether Pages/Slides are new surfaces or renamed Canvas/Workspace features; how agent edits are attributed and reverted inside a shared document; and what a Dot can see of a Space it is added to, which is the access-control question the shared-context design creates."
labels:
  - openai
  - collaboration
  - devday-2026
  - agents
  - released
verification: partial
sources:
  - https://x.com/insanekrishnaa/status/2105147666850304017
  - https://x.com/AI_Whisper_X/status/2105148071009206761
  - https://x.com/Zen_with_AI/status/2105089984504234283
  - https://x.com/masahirochaen/status/2105147966889886057
  - https://x.com/MagicPower21M/status/2105148814105710821
created_at: 2026-09-30
updated_at: 2026-09-30
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-30
    change: "Created — RELEASED / partial. OpenAI announced ChatGPT Space at DevDay on 2026-09-29: a shared workspace inside ChatGPT where people, teams and their Dots operate in one shared context, with Pages (co-edited documents), collaborative Slides, Teams and shared task lists. Four independent DevDay recaps carry it with consistent detail — @insanekrishnaa ranking it #3 ('chat is becoming a workspace'), @masahirochaen in his 25-item roundup, @MagicPower21M, @AI_Whisper_X listing the companion surfaces — and @Zen_with_AI quotes press coverage verbatim describing Space as 'a shared workspace inside ChatGPT where co-workers can collaborate with the chatbot and with their own Dots'. Verification PARTIAL: convergent independent reporting plus a quoted press line, but no OpenAI post in this cycle's fetch and no availability or plan-gating detail anywhere in signal. Split from [[openai-dots-agents-2026-09]] because they are separable artifacts that happened to ship together — Dots is an agent runtime, Space is the multi-participant context and document layer agents attach to. RECORDED AS COMMENTARY AND EXPLICITLY NOT AS FACT: @Zen_with_AI's argument that Space productises an internal Anthropic practice (engineers sharing all Claude sessions and project context, tasks visible and claimable org-wide) with a prediction that the pattern spreads across Silicon Valley in six months and the software industry in one to three years. The relayer himself disclaims accuracy on the Anthropic-internals claim and his own replies contested it as more plausibly a shared idea pool than task-stealing; no Anthropic source supports it and it should not be repeated as a description of how Anthropic works. Competitive frame: @davidarngar's skeptical recap reads Space as a 'Notion + Claude Tag clone'."
---

The interesting claim in Space is not collaboration. It is shared context.

Every agent product so far has been one-to-one: your conversation, your memory,
your tool permissions. Space inverts that — the context is the team's, and the
agents sitting in it read what the humans put there and each other's output. That
is a genuine architectural choice rather than a UI one, and it resolves a real
problem, because the expensive part of delegating work to an agent is assembling
the context it needs, and doing that once per person does not scale.

It also creates an access-control surface that did not exist before, and nothing
in this cycle's signal describes it. If a Dot is added to a Space, what can it
read? All prior documents? Every participant's messages? The task list including
items it was not assigned? An always-on agent with a browser and 4,000 app
integrations ([[openai-dots-agents-2026-09]]) that inherits a team's full working
context is a different risk object from one scoped to a single user's thread, and
it is the question this ticket should be judged on as detail emerges.

The commentary circulating alongside the launch is worth keeping at arm's length.
A widely-shared thread reads Space as OpenAI productising an internal Anthropic
engineering culture — fully shared sessions, claimable tasks — and forecasts
industry-wide adoption within three years. The Anthropic description is
second-hand and disclaimed by the person relaying it, and the replies it drew made
the obvious objection: if credit went to whoever finished a task first,
engineers would hide work rather than pool it. Treat the forecast as a
practitioner's read on where collaborative tooling goes, not as reporting on any
company's internals.

What is not in dispute is the direction. Between Space, Dots and Codex Cloud,
DevDay 2026 moved OpenAI's product surface from "a place you ask questions" to "a
place work is stored and executed." The revenue model moved with it, in the same
announcement ([[openai-chatgpt-pro-max-2026-09]]).
