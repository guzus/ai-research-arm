---
slug: cursor-claude-code-extension-tamper-2026-10
title: "Tampered Claude Code extension published on Cursor's marketplace; Anthropic says its own systems were not compromised"
company: "Cursor / Anthropic"
model: "Claude Code (extension)"
status: confirmed
status_note: |
  **Anthropic statement, 2026-10-30 14:08 UTC.** @felixrieseberg (Anthropic; retweeted by
  @alexalbert__): "We're working with Cursor on this incident, but it wasn't a compromise of Anthropic's
  systems or employee laptops. A malicious actor used access to Cursor's marketplace to publish a
  tampered copy of the Claude Code extension, which we didn't build or publish. The versions on our
  official channels are not affected and this only impacts Cursor users."

  **Payload details are relay-strength.** @ishkme (2026-10-31) says the fake builds were versions
  2.1.312 / 2.1.313, that they planted an attacker SSH key and a startup job, and that uninstalling
  may not remove them. No Cursor advisory was captured in this signal.
expected: "Open: a Cursor post-mortem or advisory (how marketplace publish access was obtained, affected install count, cleanup steps), and confirmation of the reported payload."
labels:
  - security
  - supply-chain
  - claude-code
  - cursor
verification: confirmed
sources:
  - https://x.com/felixrieseberg/status/2116170451466543578
  - https://x.com/alexalbert__/status/2116185216146620606
  - https://x.com/ishkme/status/2116513901525217673
created_at: 2026-10-31
updated_at: 2026-10-31
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-31
    change: "Created — CONFIRMED / confirmed. Anthropic's @felixrieseberg (2026-10-30 14:08 UTC, retweeted by @alexalbert__) says a malicious actor used access to Cursor's extension marketplace to publish a tampered copy of the Claude Code extension that Anthropic did not build or publish. He says Anthropic's systems and employee laptops were not compromised, that Anthropic's official channels are unaffected, and that only Cursor users are affected; Anthropic is working with Cursor. Relay @ishkme (2026-10-31) gives the fake versions as 2.1.312/2.1.313 and says they planted an attacker SSH key and a startup job that uninstalling may not remove; those details are relay-strength. No Cursor statement captured."
---
This is a marketplace-integrity incident, not an Anthropic breach. The attacker did not need
Anthropic's signing or publishing keys. Access to a third-party editor's extension marketplace
was enough to ship a lookalike Claude Code to that editor's users.

It is the second agent-tooling supply-chain story this month, after the LiteLLM PyPI/Docker
compromise relayed in the same signal. Developer agents run with shell and repository access, so
a poisoned extension is effectively a remote shell.

If the reported SSH-key and startup-job persistence is accurate, affected users need to audit their
machines as well as uninstall the extension. That is why a Cursor advisory is the next thing to watch.
