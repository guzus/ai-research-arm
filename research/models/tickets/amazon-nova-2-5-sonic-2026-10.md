---
slug: amazon-nova-2-5-sonic-2026-10
title: Amazon Nova 2.5 Sonic speech-to-speech model reported generally available on Bedrock
company: Amazon / AWS
model: Nova 2.5 Sonic
status: released
status_note: |
  **Single secondary relay of an AWS announcement.** @Cozy2054934 (2026-10-06 12:43
  UTC, posted twice): "AWS made Amazon Nova 2.5 Sonic generally available on Oct 5.
  It's a speech-to-speech model built for real-time voice agents." Quoted from AWS's
  announcement: better reasoning, instruction following and tool-calling accuracy
  with lower latency; asynchronous tool calling; voice and text in the same session;
  controllable turn-taking; 256K context; expressive voices in 7 languages; same
  pricing as Nova 2 Sonic; four Bedrock regions (N. Virginia, Oregon, Stockholm,
  Tokyo).

  **Verification unverified.** No @awscloud or AWS What's New post was captured
  in-window, and an attempt to corroborate against AWS's site was blocked in this
  run. The specificity of the relayed details makes it plausible, but it is one
  account.
expected: "Reported GA 2026-10-05 in four Bedrock regions. Open: AWS first-party confirmation, additional regions, latency figures."
labels:
  - speech
  - voice-agents
  - bedrock
  - amazon-nova
verification: unverified
sources:
  - https://x.com/Cozy2054934/status/2107451789620486420
  - https://x.com/Cozy2054934/status/2107451921871106335
created_at: 2026-10-06
updated_at: 2026-10-06
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-06
    change: "Created — RELEASED (reported) / unverified. @Cozy2054934 (2026-10-06 12:43 UTC) relays an AWS announcement that Amazon Nova 2.5 Sonic, a real-time speech-to-speech model for voice agents, became generally available on 2026-10-05: improved reasoning, instruction following and tool-calling accuracy at lower latency, asynchronous tool calling, mixed voice/text sessions, 256K context, 7 languages, Nova 2 Sonic pricing, four Bedrock regions. Single-source relay; no AWS first-party post captured and direct corroboration was not possible this run, so verification is unverified."
---

Nova 2.5 Sonic is a point release of Amazon's speech-to-speech line, aimed squarely
at the real-time voice-agent market where OpenAI's GPT-Live
([[openai-gpt-live-1-api-2026-09]]), Google's Gemini 3.8 Live
([[google-gemini-3-8-live-2026-09]]) and Microsoft's MAI-Voice line
([[microsoft-mai-transcribe-2-streaming-2026-10]]) all shipped updates in the past
month.

The relayed feature list emphasises asynchronous tool calling and turn-taking
rather than voice quality — consistent with where voice agents actually fail:
dead air while a tool call returns. Holding price flat with Nova 2 Sonic is the
other notable choice.

The broader Nova frontier-model story ([[amazon-nova-frontier-reorg-2026-07]]) was
closed as a stale rumor; this ticket tracks only the Sonic speech model.

Transition triggers: AWS first-party confirmation → verification confirmed; ≥4
weeks after GA → close as released-and-aged.
