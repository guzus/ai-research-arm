---
slug: openai-text-watermarking-2026-10
title: OpenAI launches text watermarking — opt-in on the API worldwide, default for EU ChatGPT/Codex under the AI Act
company: OpenAI
model: null
status: released
status_note: |
  **First-party, @OpenAI thread, 2026-10-05 17:42 UTC:** "In the EU, we'll start
  watermarking eligible text from ChatGPT and Codex over the coming weeks to comply
  with the EU AI Act. Customers using our API can turn on text watermarking for
  select models worldwide today." The watermark is an invisible statistical signal
  embedded at generation time; it does not identify a person, account, conversation
  or prompt, and OpenAI says it has not affected capability, speed or style in
  testing.

  **Limits stated by OpenAI itself:** often undetectable in short passages, removable
  by rewriting or translation; the detector is restricted to approved researchers
  for now.

  **Secondary detail:** AI-news digest @TheInfoMachine names it "textGrain" and
  reports the detector catches roughly 80% of 200-token passages at a 1% false-
  positive rate. Name and figures not captured first-party in-window.
expected: "API opt-in live 2026-10-05; EU ChatGPT/Codex watermarking rolling out 'over the coming weeks'. Open: which models are eligible, detector access beyond approved researchers, and whether other labs follow for EU AI Act compliance."
labels:
  - provenance
  - watermarking
  - eu-ai-act
  - policy
verification: confirmed
sources:
  - https://x.com/OpenAI/status/2107164650249101695
  - https://x.com/OpenAI/status/2107164651478012412
  - https://x.com/OpenAI/status/2107164653147340988
  - https://x.com/TheInfoMachine/status/2107449727696433179
  - "@OpenAI"
created_at: 2026-10-06
updated_at: 2026-10-06
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-06
    change: "Created — RELEASED / confirmed. @OpenAI (2026-10-05 17:42 UTC) expanded content provenance to text: API customers can enable text watermarking for select models worldwide today, and eligible ChatGPT and Codex text in the EU will be watermarked over the coming weeks to comply with the EU AI Act. The signal is an invisible statistical pattern that does not identify users or prompts; OpenAI concedes it is often undetectable in short passages and removable by rewriting or translation, and limits the detector to approved researchers. Secondary (@TheInfoMachine): product name 'textGrain', detector ~80% recall on 200-token passages at 1% FPR."
---

The first major lab to ship text watermarking in production, and it is doing so
because a regulator required it rather than because the technique matured — OpenAI's
own thread is unusually blunt that watermarks are fragile against paraphrase and
translation and weak on short text.

The design choices are the story: default-on only where the EU AI Act compels it,
opt-in elsewhere, and a detector held back from the public. That keeps the
watermark from becoming a consumer "AI detector" with the false-positive problems
those tools have had, while giving OpenAI a compliance artifact for the EU.

Anthropic had a reported but unconfirmed watermarking effort
([[anthropic-claude-watermarking-2026-08]], closed as a stale rumor); Google's
SynthID line covers images, audio and now biology ([[google-synthid-bio-2026-09]]).
Whether Anthropic and Google ship EU text watermarking on the same timetable is the
follow-on question.

Transition triggers: EU ChatGPT/Codex rollout completes → UPDATE; detector opened
more widely → UPDATE; ≥4 weeks after full rollout → close as released-and-aged.
