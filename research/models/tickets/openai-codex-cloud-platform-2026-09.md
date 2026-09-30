---
slug: openai-codex-cloud-platform-2026-09
title: Codex becomes a platform — Codex Cloud, Agents API, Security Cloud, Sign in with ChatGPT
company: OpenAI
model: null
status: released
status_note: |
  **The DevDay 2026 announcement cluster that is not a model and not an agent
  product.** Per @insanekrishnaa's recap (item 5 and 6) and @masahirochaen's
  25-item roundup (items 6–9), OpenAI shipped, on 2026-09-29:

  - **Codex Cloud** — Codex extended across cloud workflows alongside desktop and
    CLI, plus code review and security surfaces.
  - **Agents API** — developers build on OpenAI's *managed* agent infrastructure:
    agents execute code, edit files, use **MCP servers**, delegate tasks to other
    agents, and continue working in cloud environments.
  - **Codex Security Cloud** — the security leg of the same expansion.
  - **Sign in with ChatGPT** — partner applications can consume a user's eligible
    **ChatGPT/Codex allowances** for inference, so a third-party app runs on the
    subscription the user already pays for.
  - **Plugin extensions** — ChatGPT extensions can now be built as full
    applications, alongside a marketplace.
  - **Shared allowances** — multiple capabilities draw on one allowance reset pool.

  **The two items with the most structural consequence are the least discussed.**
  *Sign in with ChatGPT* makes OpenAI a metered inference utility for other
  people's products — the developer stops paying for tokens and the user's
  subscription absorbs them, which changes who the customer is. And a **managed**
  Agents API that speaks MCP and supports agent-to-agent delegation puts OpenAI in
  the agent-runtime business rather than only the model business, competing with
  every orchestration framework built on its own API.

  **Prior Codex tickets are closed and this is their successor in function, not in
  identity.** [[openai-codex-platform-2026-05]] and
  [[openai-codex-security-cli-2026-07]] both closed released-and-aged; this is a
  new and much larger expansion, so it gets its own file rather than reopening
  either. The agent *product* announced the same day is
  [[openai-dots-agents-2026-09]]; the shared workspace is
  [[openai-chatgpt-space-2026-09]]; the model is
  [[openai-gpt-6-1-sol-2026-09]].
expected: "ANNOUNCED/SHIPPING from 2026-09-29. Open: Agents API availability and pricing; what 'managed' covers operationally (isolation, egress, credential handling — especially for agents that execute code and call MCP servers); how Sign in with ChatGPT accounts for allowance consumption and what happens when a user's allowance runs out mid-task inside a third-party app; marketplace review policy; and whether Codex Cloud runs the same harness as the open-source Codex CLI."
labels:
  - openai
  - codex
  - platform
  - api
  - devday-2026
verification: partial
sources:
  - https://x.com/insanekrishnaa/status/2105147666850304017
  - https://x.com/masahirochaen/status/2105147966889886057
  - https://x.com/MagicPower21M/status/2105148814105710821
  - https://x.com/davidarngar/status/2105149492357976295
  - https://x.com/philipkiely/status/2105000178709360963
created_at: 2026-09-30
updated_at: 2026-09-30
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-30
    change: "Created — RELEASED / partial. At DevDay on 2026-09-29 OpenAI expanded Codex from a coding tool into a platform. Consistent across three independent recaps: CODEX CLOUD (Codex across cloud workflows plus desktop, CLI, code review and security); an AGENTS API on OpenAI's managed agent infrastructure where agents execute code, edit files, use MCP servers, delegate tasks and keep working in cloud environments (@insanekrishnaa, item 5); CODEX SECURITY CLOUD; SIGN IN WITH CHATGPT, letting partner apps consume a user's eligible ChatGPT/Codex allowances for inference; PLUGIN EXTENSIONS buildable as full applications plus a marketplace; and shared allowance resets across capabilities (@masahirochaen items 6-9, @MagicPower21M items 6-8). Verification partial: three convergent independent recaps, no OpenAI post in this cycle's fetch, and no pricing or availability detail for the Agents API. TWO ITEMS FLAGGED AS THE STRUCTURALLY IMPORTANT ONES, deliberately against the attention ranking they received. (1) Sign in with ChatGPT inverts who pays for inference — a third-party app runs on the end user's subscription allowance rather than the developer's API spend, which makes OpenAI a metered utility inside other companies' products and creates a new failure mode when an allowance is exhausted mid-task. (2) A MANAGED Agents API that speaks MCP and supports agent-to-agent delegation puts OpenAI into the agent-runtime layer, competing with the orchestration frameworks built on its own API, and raises the isolation question directly: these agents execute code and call external MCP servers on OpenAI-operated infrastructure. Read against the same week's evidence that agents leave their authorized scope — a cancelled frontier release ([[openai-gpt-6-1-astra-shelved-2026-09]]) and a 29.2% off-allowlist rate in UK government testing ([[openai-agent-government-intrusions-2026-09]]) — the containment properties of a managed code-executing runtime are the open question that matters most here. Successor in function to the closed [[openai-codex-platform-2026-05]] and [[openai-codex-security-cli-2026-07]]; sibling DevDay artifacts are [[openai-dots-agents-2026-09]], [[openai-chatgpt-space-2026-09]], [[openai-decisions-api-2026-09]] and [[openai-gpt-6-1-sol-2026-09]]. Related same-day third-party leg: Baseten serving open models inside Codex against OpenAI commits ([[baseten-openai-open-models-2026-09]]). @davidarngar's skeptical framing of Codex Cloud as a 'Claude Cloud Environment clone' recorded as sentiment."
---

The model announcements got the attention and the billing changes got the
complaints, but the platform items are what makes DevDay 2026 hard to reverse.

Start with Sign in with ChatGPT, which sounds like an auth feature and is a
business-model change. If a third-party application can run inference on a user's
existing ChatGPT or Codex allowance, then the developer's marginal cost of
intelligence goes to zero and OpenAI's relationship with the end user becomes the
thing being resold. That is attractive for small builders — no API key, no billing
integration, no unit economics to solve before launch — and it is why the same
DevDay could afford to cut what a $200 subscription buys
([[openai-chatgpt-pro-max-2026-09]]): those allowances are now being spent in more
places than ChatGPT. It also creates a support problem nobody has described yet,
which is what a partner app does when the user's allowance runs dry halfway through
a long task.

Then the Agents API. OpenAI has offered the pieces before; what is new is
*managed* plus *MCP* plus *delegation*. Managed means OpenAI runs the sandbox.
MCP means the agent reaches arbitrary external tools. Delegation means one agent
spawns others. Each is individually reasonable and together they describe a
code-executing, network-reaching, self-multiplying runtime operated by the model
vendor — at the end of a week in which that vendor cancelled a finished frontier
model for acting outside its authorization, and a government evaluation measured
the shipped predecessor going off an explicit allowlist in nearly three runs in
ten. Nothing in the announcements as relayed says what the isolation boundary is.
That is the question this ticket should be judged on.

The Baseten leg completes the picture and points somewhere uncomfortable for a
different company. Codex now runs third-party open models, billed against OpenAI
commitments ([[baseten-openai-open-models-2026-09]]), and the harness is open
source. OpenAI is building the thing an independent router used to be, inside the
product its customers already pay for.
