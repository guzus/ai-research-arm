---
slug: anthropic-cowork-browser-2026-08
title: Claude Cowork gets a built-in browser in the desktop app
company: Anthropic
model: null
status: released
status_note: |
  **@claudeai, first-party:** "**Claude now has its own built-in browser in
  Cowork.** When your task involves a website, **a browser opens in
  Cowork's side panel**, and Claude **navigates, fills forms, and finishes
  the job**."

  **Rollout terms**, per @testingcatalog (2026-08-27 06:52 UTC): "The
  built-in browser is **rolling out over the coming week** to **Pro, Max,
  and Team plans** in the **Claude desktop app on macOS, Windows, and
  Linux (in beta)**." Same account had reported the feature as a
  pre-release find days earlier — "Claude desktop will get a dedicated
  Browser inside that app that will always be accessible in Cowork
  sessions" — and now confirms it: "**Now it's official.**" @danshipper:
  "THEY DID IT FOLKS."

  **Why this is a model-lane ticket.** Computer-use is one of the axes the
  frontier labs are actively competing on, and this ticket set already
  tracks the model side of it —
  [[gemini-3-5-flash-computer-use-2026-06]] and
  [[google-gemini-spark-computer-use-2026-08]] for Google,
  [[openai-chatgpt-superapp-2026-06]] for OpenAI. What ships here is the
  **surface**: an in-app browser the agent drives directly, rather than a
  remote VM or a screenshot loop. The distinction matters because the
  side-panel design makes the agent's browsing **visible to the user in
  the same window**, which is a supervision property, not a convenience
  one — @ikm_san's read is exactly that: you can watch what the AI is
  doing and see how far you have delegated.

  **The strategic reading offered in-window**, @testingcatalog: "**A new
  Super App is rising. This looks familiar** 👀" — i.e. the same
  consolidation OpenAI is pursuing at
  [[openai-chatgpt-superapp-2026-06]], and adjacent to Perplexity's
  Comet/Computer line ([[perplexity-portable-computer-2026-08]]). Browsers
  are becoming a component of assistant products rather than a category.

  Verification `confirmed`: first-party @claudeai announcement, plus an
  independent tracker confirming the rollout terms and its own earlier
  pre-release find. Status `released` because it is actively rolling out
  to named paid tiers on named platforms, with the caveat that it is
  **beta on Linux** and staged "over the coming week," so not every
  eligible user has it yet. **Not** established: what browser engine it
  uses, whether it shares session state or credentials with the user's
  real browser, what the sandboxing model is, or how it handles
  prompt-injection from page content — none of which anyone asked in
  public in-window, and all of which matter for an agent that "fills
  forms."
expected: "Rolling out from 2026-08-26/27 over the following week to Pro, Max and Team plans in the Claude desktop app on macOS, Windows and Linux (beta): a browser that opens in Cowork's side panel and that Claude drives directly to navigate and fill forms. Pending: the browser engine, the sandboxing and credential model, whether it shares session state with the user's own browser, prompt-injection handling for agent-read page content, and availability beyond desktop"
labels:
  - anthropic
  - claude-cowork
  - computer-use
  - agents
  - released
verification: confirmed
sources:
  - "@claudeai"
  - "@testingcatalog"
  - https://x.com/testingcatalog/status/2092867859034640790
  - "@danshipper"
created_at: 2026-08-27
updated_at: 2026-08-27
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-27
    change: "Created — Anthropic shipped a built-in browser inside Claude Cowork. First-party @claudeai: 'Claude now has its own built-in browser in Cowork. When your task involves a website, a browser opens in Cowork's side panel, and Claude navigates, fills forms, and finishes the job.' Rollout terms per @testingcatalog (2026-08-27 06:52 UTC): rolling out over the coming week to Pro, Max and Team plans in the Claude desktop app on macOS, Windows and Linux (in beta); the same account had reported it as a pre-release find days earlier and now confirms 'Now it's official.' Status released rather than confirmed because it is actively shipping to named paid tiers on named platforms, with the caveat that Linux is beta and the rollout is staged. Verification confirmed on the first-party account plus an independent tracker that had also caught the pre-release artifact. Earns a model-lane ticket because computer-use is a live competitive axis already tracked on the model side at [[gemini-3-5-flash-computer-use-2026-06]], [[google-gemini-spark-computer-use-2026-08]] and [[openai-chatgpt-superapp-2026-06]]; what ships here is the surface, and the side-panel design is a supervision property rather than a convenience — the user watches the agent browse in the same window. @testingcatalog reads it as super-app consolidation ('A new Super App is rising'), adjacent to [[perplexity-portable-computer-2026-08]]. NOT established and notably unasked in public in-window: the browser engine, the sandboxing and credential model, whether it shares session state with the user's real browser, and how prompt injection from page content is handled — all material for an agent that fills forms."
---

**Claude Cowork now has a browser inside it.** When a task needs the web,
a browser opens in Cowork's side panel and Claude drives it — navigating,
filling forms, finishing the job — rolling out over a week to Pro, Max and
Team on macOS, Windows and Linux (beta).

**The side panel is the design decision worth noticing.** The alternative
implementations of agentic browsing hide the work: a remote VM, a headless
session, a screenshot loop the user sees only in summary. Putting the
browser in the same window as the conversation means the delegation is
**legible while it happens**. That is a supervision affordance, and it is
the cheap version of the problem
[[openai-unreleased-containment-escape-2026-07]] made expensive — agents
doing things nobody watched.

**It is also a super-app move, and everyone is making it.** OpenAI is
consolidating around ChatGPT ([[openai-chatgpt-superapp-2026-06]]),
Perplexity around Computer ([[perplexity-portable-computer-2026-08]]),
Google around Gemini's computer-use surfaces
([[google-gemini-spark-computer-use-2026-08]]). The browser is being
absorbed into the assistant rather than sitting beside it.

**The unasked questions are the interesting ones.** An agent that "fills
forms" is an agent that touches credentials, and a browser that renders
attacker-controlled page text into an agent's context is a
prompt-injection surface by construction. Nothing in-window states the
engine, the sandbox model, whether session state is shared with the user's
real browser, or how page content is isolated from instructions. Those
answers determine whether this is a convenience feature or a new attack
surface on a paid tier.

**Transition triggers:**
- Documentation of the sandboxing, credential or injection-handling model
  → UPDATE.
- General availability beyond the staged rollout, or expansion past
  desktop → UPDATE.
- A demonstrated prompt-injection or credential incident → UPDATE, and
  consider a separate security ticket.
- ≥4 weeks past release, settled into normal coverage →
  `closed: released-and-aged`.

**Dedup note:** Microsoft's unrelated Copilot Cowork product stays on the
closed [[microsoft-copilot-cowork-2026-06]] — same word, different
company. Claude Code surface changes stay on
[[anthropic-claude-code-design-2026-08]]. Further Claude Cowork browser
signal UPDATES this ticket.
