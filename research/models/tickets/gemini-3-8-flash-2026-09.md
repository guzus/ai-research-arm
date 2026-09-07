---
slug: gemini-3-8-flash-2026-09
title: Gemini 3.8 Flash + 3.8 Flash Cyber
company: Google / DeepMind
model: Gemini 3.8 Flash / Gemini 3.8 Flash Cyber
status: released
status_note: |
  Two models, one launch event, 2026-09-02. **Gemini 3.8 Flash** is Google's
  "most intelligent model yet" per @GoogleDeepMind — gains over 3.7 Flash
  across software engineering, agentic tasks and multi-step reasoning — and it
  is generally available: rolling out in Antigravity, via the API in Google AI
  Studio and Android Studio, to Google AI Pro and Ultra subscribers in the
  Gemini app and AI Mode in Search, in Google Sheets, in Stitch, and to Gemini
  Enterprise users from the model dropdown. **Gemini 3.8 Flash Cyber** ships on
  a deliberately narrower channel: the new **Fairwind Program**, trusted access
  for national cyber authorities and essential-service operators
  (telecommunications, energy). Reported results for the Cyber model: leads
  CyberGym on autonomous weakness discovery while staying fast and efficient,
  and produced **2.6x more valid fixes** in real-world testing across Google
  Chrome codebases.

  Cadence is the story as much as capability. @demishassabis framed it as
  "another upgrade in under a month" — 3.7 Flash shipped 2026-08-23
  ([[gemini-3-7-flash-2026-08]]) and 3.8 Flash landed ten days later. It is the
  first of the four frontier releases in the 2026-09-01..09-07 week
  (@testingcatalog: "top models from 4 of the biggest AI labs in a single week:
  Gemini 3.8 Flash, Claude Fable 5.1, Muse Spark 1.3, GPT-6 Astra").

  This ticket supersedes [[gemini-3-5-flash-cyber-2026-07]], which Google itself
  positioned as the prior generation: 3.8 Flash Cyber is "a major improvement
  from our 3.5 generation." That ticket is closed with
  `superseded-by:gemini-3-8-flash-2026-09`.
expected: "RELEASED 2026-09-02. Gemini 3.8 Flash is broadly available; 3.8 Flash Cyber is gated behind Fairwind trusted access (application-based). Open: whether the sub-monthly Flash cadence holds, and where a 3.8 Pro tier lands."
labels:
  - google
  - frontier-model
  - flash-tier
  - cybersecurity
  - released
verification: confirmed
sources:
  - https://x.com/GoogleDeepMind/status/2095175498967949359
  - https://x.com/GoogleDeepMind/status/2095196704769237137
  - https://x.com/demishassabis/status/2095191106665284046
  - "@GoogleAI"
  - "@testingcatalog"
  - "@elliotarledge"
created_at: 2026-09-07
updated_at: 2026-09-07
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-07
    change: "Created — RELEASED. Google launched Gemini 3.8 Flash and Gemini 3.8 Flash Cyber together on 2026-09-02 15:42 UTC (@GoogleDeepMind, @GoogleAI, @demishassabis). 3.8 Flash is Google's 'most intelligent model yet' with significant gains over 3.7 Flash in software engineering, agentic tasks and multi-step reasoning, generally available in Antigravity, the API via Google AI Studio and Android Studio, the Gemini app and AI Mode in Search for AI Pro/Ultra subscribers, Google Sheets, Stitch, and Gemini Enterprise. 3.8 Flash Cyber ships narrower, through the new Fairwind Program for national cyber authorities and essential-service operators, and reportedly leads CyberGym on autonomous weakness discovery and produced 2.6x more valid fixes across Google Chrome codebases in real-world testing. Cadence noted by @demishassabis as 'another upgrade in under a month' — ten days after 3.7 Flash ([[gemini-3-7-flash-2026-08]]). Verification confirmed on Google's own launch posts. Independent third-party measurement in the same week from @elliotarledge's KernelBench runs. This ticket supersedes [[gemini-3-5-flash-cyber-2026-07]], which Google positioned as the prior generation ('a major improvement from our 3.5 generation')."
---

Google's answer to the September frontier week was cadence rather than a
single flagship. Gemini 3.8 Flash arrived ten days after 3.7 Flash, and
@demishassabis's own framing — "another upgrade in under a month" — is the
claim being made: not that Google has the best model, but that it can ship the
workhorse tier faster than anyone else can respond to it. That is a different
competitive bet from OpenAI's ([[openai-gpt-6]]) and Anthropic's
([[anthropic-claude-fable-5-1-2026-08]]) flagship launches the same week.

The Cyber model is the more unusual artifact. Google did not release it; it
distributed it. The Fairwind Program restricts access to national cyber
authorities and essential-service operators, which makes 3.8 Flash Cyber a
gated defensive-capability transfer rather than a product launch, and puts it
in the same category of decision as OpenAI declaring Astra Critical on
cybersecurity under its Preparedness Framework four days earlier. Two labs, the
same week, both concluding that frontier cyber capability needs a distribution
answer separate from the model itself.

Worth watching, and not yet answered: whether the sub-monthly Flash cadence is
sustainable or a one-off pre-empt of Astra, and whether a 3.8 Pro tier follows.
Google's shipping recap for the week bundled 3.8 Flash, 3.8 Flash Cyber and
Lyria 3.5 ([[google-lyria-3-5-2026-07]]) together, which suggests a release
train rather than a single push.
