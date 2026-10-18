---
slug: opencode-distillation-breach-2026-10
title: "OpenCode discloses a security breach tied to a large-scale distillation attack on linked provider keys"
company: OpenCode
model: null
status: confirmed
status_note: |
  **Primary disclosure, 2026-10-17 18:08 UTC (@opencode, ~9.7K likes):** "We had a
  security breach last night related to a large scale distillation attack that impacted
  1.4% of OpenCode Console users." The affected users were a subset with external
  providers linked, and all were emailed. "The incident is ongoing so we cannot share
  more details at this point but we are working with Anthropic, OpenAI, and Google to
  remediate."

  **Interpretation, not fact.** @ItsTonyTalk (2026-10-18 08:43 UTC) reads the
  three-lab response as a sign that the target was model outputs, not user data. On
  this reading, linked bring-your-own-key provider credentials were used to pull
  training data at victims' expense. OpenCode has not confirmed the mechanism.
expected: "Incident ongoing. Open: the attack mechanism, which provider keys and models were abused, any attribution of the distilling party, and statements from Anthropic, OpenAI or Google."
labels:
  - security-incident
  - distillation
  - agent-tooling
verification: confirmed
sources:
  - "https://x.com/opencode/status/2111519637049319818"
  - "https://x.com/ItsTonyTalk/status/2111739912923881848"
created_at: 2026-10-18
updated_at: 2026-10-18
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-18
    change: "Created — CONFIRMED / confirmed. @opencode (2026-10-17 18:08 UTC) disclosed a security breach the previous night linked to a 'large scale distillation attack' affecting 1.4% of OpenCode Console users, specifically users with external providers linked. Users were notified by email. OpenCode says the incident is ongoing and it is working with Anthropic, OpenAI and Google to remediate. Primary source, so verification is confirmed. The BYOK-key-abuse mechanism suggested by @ItsTonyTalk is interpretation and is not adopted. Related lab-side distillation context: [[anthropic-alibaba-distillation-2026-06]] and the closed [[openai-moonshot-distillation-disclosure-2026-10]]."
---

Distillation has mostly been a lab-versus-lab dispute. Anthropic and OpenAI have
publicly accused Chinese labs of harvesting their outputs. This incident puts the
same fight in a different place: a third-party coding tool that holds many users'
provider keys.

OpenCode says three competing labs are helping with remediation. That suggests the
abused resource was model access through linked credentials rather than OpenCode's
own data, but the company has not said how the attack worked. The details that
matter are which keys were used, how much traffic was extracted, and who did it.

**Transition triggers:** a post-mortem or a lab statement naming the distilling
party → UPDATE; no further developments for about four weeks → close.
