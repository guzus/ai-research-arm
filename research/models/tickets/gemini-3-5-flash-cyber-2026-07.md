---
slug: gemini-3-5-flash-cyber-2026-07
title: Gemini 3.5 Flash Cyber — CodeMender security model (limited pilot)
company: Google / DeepMind
model: Gemini 3.5 Flash Cyber
status: closed
status_note: |
  Announced 2026-07-21 alongside [[gemini-3-6-flash-2026-07]] as the third
  model of the day — @GoogleAI and @GoogleDeepMind describe it as built on
  top of Gemini 3.5 Flash and purpose-tuned for **finding software
  vulnerabilities**. Deployed inside **CodeMender**, Google's AI agent for
  code security, where multiple 3.5 Flash Cyber agents work together to
  produce a combined vulnerability report; Google claims competitive
  frontier performance on the **CyberGym** benchmark. Unlike 3.6 Flash /
  3.5 Flash-Lite (both broadly GA the same day), Google's own
  announcement frames Flash Cyber as **"exclusively available via
  CodeMender soon as part of a limited-access pilot program"** — not a
  broad public release yet, hence `in-testing` rather than `released`.
  @testingcatalog corroborates the CyberGym framing.

  **2026-09-07 — CLOSED, superseded.** Google shipped **Gemini 3.8 Flash Cyber**
  on 2026-09-02 and described it as "our most capable cybersecurity model" and
  "a major improvement from our **3.5 generation**" — Google's own words placing
  the new model as this one's direct successor, on the same Fairwind trusted-access
  distribution this ticket tracked. The 3.5 Flash Cyber artifact was never
  generally released and now will not be; the line continues at 3.8. Closed with
  `superseded-by:gemini-3-8-flash-2026-09`. History preserved, nothing rewritten.
expected: "Limited-access CodeMender pilot program 'soon'; no broader API/product availability announced yet"
labels:
  - google
  - cybersecurity
  - codemender
  - limited-pilot
verification: confirmed
sources:
  - "@GoogleAI"
  - "@GoogleDeepMind"
  - "@testingcatalog"
  - https://x.com/GoogleDeepMind/status/2095196704769237137
created_at: 2026-07-22
updated_at: 2026-09-07
closed_at: 2026-09-07
closed_reason: "superseded-by:gemini-3-8-flash-2026-09"
history:
  - ts: 2026-07-22
    change: "Created — Google announced Gemini 3.5 Flash Cyber on 2026-07-21 (@GoogleAI, @GoogleDeepMind), a CodeMender-embedded, CyberGym-competitive vulnerability-finding model built on 3.5 Flash. Google's own announcement frames it as a limited-access CodeMender pilot program 'soon,' not a broad release → status in-testing; official primary sourcing → verification confirmed."
  - ts: 2026-09-07
    change: "CLOSED — superseded-by:gemini-3-8-flash-2026-09. Google launched Gemini 3.8 Flash Cyber on 2026-09-02 alongside Gemini 3.8 Flash, calling it 'our most capable cybersecurity model' with 'frontier-level vulnerability detection and automated patching', and explicitly describing it as 'a major improvement from our 3.5 generation' — Google's own framing of the new model as this ticket's direct successor, shipping on the same Fairwind trusted-access channel (national cyber authorities, telecoms, energy) that this ticket tracked. Reported results for the successor: leads CyberGym on autonomous weakness discovery, and 2.6x more valid fixes in real-world testing across Google Chrome codebases. The 3.5 Flash Cyber artifact never reached general release and the line now continues at 3.8, so this ticket closes rather than advancing."
---

Google's third model announcement of 2026-07-21 (alongside
[[gemini-3-6-flash-2026-07]]) was **Gemini 3.5 Flash Cyber**, a
security-focused model built on top of Gemini 3.5 Flash and purpose-tuned
for finding software vulnerabilities.

**Why its own ticket.** Flash Cyber has a materially different rollout
shape from its siblings: 3.6 Flash and 3.5 Flash-Lite shipped in broad GA
the same day, while Google's own announcement describes Flash Cyber as
"exclusively available via CodeMender soon as part of a limited-access
pilot program" — a narrower, gated rollout that warrants tracking
separately from the GA release.

**What it does.** Deployed inside **CodeMender**, Google's AI agent for
code security, where multiple Flash Cyber agents collaborate to produce a
single combined vulnerability report. Google claims competitive
frontier-level performance on the **CyberGym** benchmark.

**Transition triggers:**
- The pilot opens to a broader audience or ships a standalone API/product
  surface → UPDATE, advance `status` to `released`.
- Independent CyberGym or real-world vulnerability-discovery results →
  UPDATE.
- ≥15 cycles with no further movement on the pilot → consider closure per
  the standard stale-rumor path (though this is a confirmed product, not
  a rumor, so closure would more likely be `released-and-aged` once it
  ships broadly).

**Dedup note:** further Flash Cyber / CodeMender signal UPDATES this
ticket. The GA 3.6 Flash / 3.5 Flash-Lite release stays on
[[gemini-3-6-flash-2026-07]].
