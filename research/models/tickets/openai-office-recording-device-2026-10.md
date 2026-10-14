---
slug: openai-office-recording-device-2026-10
title: OpenAI finds a hidden recording device planted by an employee; FBI makes an arrest
company: OpenAI / FBI
model: null
status: confirmed
status_note: |
  @OpenAINewsroom (2026-10-13 19:48 UTC; captured through an RT by @tszzl, an
  OpenAI staffer): OpenAI found a "sophisticated recording device" hidden in one
  of its offices. It used its own models to analyse the device and trace it to a
  specific employee, who had planted it a few days earlier. OpenAI referred the
  matter to the FBI, which made an arrest, and the investigation is ongoing.
  OpenAI says it has "no indications" that the individual accessed or
  exfiltrated model weights, source code or customer data. The employee was
  terminated. The statement does not name the person, the office or any
  suspected sponsor.
expected: "FBI investigation ongoing. Watch for charging documents (which would name the person, the charge and any foreign nexus) and for any revision of the 'no exfiltration' statement."
labels:
  - openai
  - security
  - insider-threat
  - legal
verification: confirmed
sources:
  - "https://x.com/OpenAINewsroom/status/2110095403198849132"
  - "https://x.com/tszzl/status/2110099445157355535"
created_at: 2026-10-14
updated_at: 2026-10-14
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-14
    change: "Created — CONFIRMED / confirmed. @OpenAINewsroom (2026-10-13 19:48 UTC, ~71K likes; captured via an RT by @tszzl) disclosed that a recording device was hidden in an OpenAI office. Its models identified the employee who planted it a few days earlier, and the FBI made an arrest. OpenAI says it has no indication that model weights, source code or customer data were accessed or exfiltrated, and the employee was terminated. No name, charge or sponsor has been disclosed."
---

The lab's own newsroom disclosed this, so it is a primary source. It is tracked
because a criminal case touching frontier-lab security can affect government
security requirements on labs, and OpenAI ties it to "national importance". It
sits alongside the security-incident tickets [[anthropic-eval-security-incident-2026-07]]
and [[openai-unreleased-containment-escape-2026-07]].

Two claims need to be held to account later. One is "no indications" of
exfiltration, which is a present-tense statement from an investigation still in
progress. The other is the framing that OpenAI's models solved the case. The
charging documents are the next primary artifact.
