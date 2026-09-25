---
slug: google-gemini-3-8-live-2026-09
title: Gemini 3.8 Live and 3.8 Live Extended Thinking — Google's live-audio models, shipped
company: Google / DeepMind
model: Gemini 3.8 Live / Gemini 3.8 Live Extended Thinking
status: released
status_note: |
  **2026-09-24 — GA in Gemini Enterprise, with Live Avatar.**
  @GoogleCloudTech (primary, 16:19 UTC), retweeted by @GoogleDeepMind: "Gemini
  3.8 Live with Live Avatar is now generally available in Gemini Enterprise. Key
  capabilities include: video avatars, fluid dialogue, tool calling, and more."
  @testingcatalog's 2026-09-25 brief adds **97 languages and async tool calls
  mid-conversation**.

  This closes the first item this ticket listed as open — "GA out of preview" —
  for the **enterprise** surface specifically. The Gemini API path was in public
  preview via AI Studio at ship; nothing in this window says that changed, so the
  API is still recorded as preview.

  **Live Avatar is a new capability, not just a channel.** Video avatars with
  lip-sync take the model from live audio into live audio-visual output, which is
  a different product than the one this ticket was opened for. Recorded here
  rather than as a separate ticket because Google shipped it as a capability of
  3.8 Live rather than as a named model.

  **Still open:** the independent benchmark. The Quality Index and tau-banking
  placements Google claimed at launch remain lab-side tables; no neutral
  organisation has published them.

  **Shipped 2026-09-15 with four independent Google primaries.** @GoogleAI
  ("Introducing our most advanced Gemini Audio models yet"), @GoogleDeepMind
  ("our best conversational AI"), @OfficialLoganK (Gemini product lead) and
  @_philschmid (Google DeepMind DevRel) all posted the launch within ~15
  minutes of each other.

  **Two models, one family.** *Gemini 3.8 Live* is the scale/speed/cost tier —
  mid-sentence interruption handling, on-the-fly switching across **97
  languages**, visual context understanding. *Gemini 3.8 Live Extended
  Thinking* adds background reasoning and **asynchronous tool calls made while
  the model is still talking**, which is the actually novel bit: it decouples
  multi-step tool use from conversational turn-taking.

  **Distribution is broad on day one.** 3.8 Live: consumers via Search Live,
  developers in public preview in the Gemini API via AI Studio, enterprises in
  private preview via Gemini Enterprise. 3.8 Live Extended Thinking: Gemini
  Live in the Gemini app, Google AI Pro/Ultra subscribers in Workspace (Docs),
  all Google AI subscribers in Gmail and Keep, plus Gemini API public preview.
  Partner plugins named for LiveKit, Pipecat, LangChain and Vercel.

  **Numbers, and who is asserting them.** @_philschmid (Google) claims **82.6,
  #1 on the Artificial Analysis Quality Index** and **35.1, #1 on agentic task
  completion (τ-banking)**, at **$0.005/min input and $0.018/min output**.
  Those are first-party claims relayed by a Google employee, not a neutral
  benchmark org's own publication — recorded as claims. The price point is
  independently echoed by a third-party daily AI digest as **$1.38/API hour
  against $3.00 for OpenAI's GPT-Live-1**
  ([[openai-gpt-live-1-api-2026-09]]), which is the competitive frame this
  release is aimed at.
expected: "RELEASED, and now GENERALLY AVAILABLE in Gemini Enterprise (2026-09-24) with Live Avatar — video avatars, lip-sync, fluid dialogue, tool calling, 97 languages, async mid-conversation tool calls. The Gemini API path via AI Studio is still recorded as public preview. Open: API GA, and an independent benchmark org publishing the Quality Index / tau-banking placements Google is claiming."
labels:
  - google
  - gemini
  - voice
  - audio
  - realtime
  - released
verification: confirmed
sources:
  - https://x.com/GoogleAI/status/2099908000924193124
  - https://x.com/GoogleDeepMind/status/2099907440422830269
  - https://x.com/OfficialLoganK/status/2099909465705447807
  - https://x.com/_philschmid/status/2099908172899357093
  - https://x.com/FadyEid/status/2100184052338667874
  - https://x.com/GoogleCloudTech/status/2103157502988746877
  - https://x.com/testingcatalog/status/2103371709281632423
created_at: 2026-09-16
updated_at: 2026-09-25
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-16
    change: "Created — RELEASED. Google shipped Gemini 3.8 Live and Gemini 3.8 Live Extended Thinking on 2026-09-15 (~17:05-17:23 UTC), announced simultaneously by @GoogleAI, @GoogleDeepMind, Gemini product lead @OfficialLoganK and DeepMind DevRel @_philschmid — four first-party accounts, so verification is confirmed on the release itself. 3.8 Live is the scale/cost tier (mid-sentence interruption handling, 97 languages with on-the-fly switching, visual context); 3.8 Live Extended Thinking adds background thinking and asynchronous tool calls issued while the model keeps talking. Distribution day one: Search Live (consumer), Gemini API public preview via AI Studio (developer), Gemini Enterprise private preview; Extended Thinking additionally in Gemini Live in the Gemini app, Workspace/Docs for AI Pro and Ultra, and Gmail and Keep for all Google AI subscribers, with named partner plugins for LiveKit, Pipecat, LangChain and Vercel. FIRST-PARTY CLAIMS, NOT INDEPENDENT BENCHMARKS: @_philschmid reports 82.6 and #1 on the Artificial Analysis Quality Index, 35.1 and #1 on agentic task completion (tau-banking), at $0.005/min input and $0.018/min output. A third-party daily AI digest (@FadyEid 2026-09-16) independently frames the pricing as $1.38/API hour versus $3.00 for OpenAI's GPT-Live-1, which is the competitive read. Separate artifact from [[gemini-3-8-flash-2026-09]] (text/Flash tier) and from [[gemini-3-5-transcribe-2026-08]] (transcription), and the direct rival of [[openai-gpt-live-1-api-2026-09]]."
  - ts: 2026-09-25
    change: "Released, unchanged; the preview->GA step landed on the enterprise surface. @GoogleCloudTech announced on 2026-09-24 16:19 UTC (~314 likes) that 'Gemini 3.8 Live with Live Avatar is now generally available in Gemini Enterprise', with video avatars, fluid dialogue and tool calling; retweeted by @GoogleDeepMind, making it primary twice over. @testingcatalog's 2026-09-25 daily brief adds 97 languages and async tool calls mid-conversation. This closes the 'GA out of preview' item this ticket opened with — but ONLY for Gemini Enterprise: the Gemini API path via AI Studio was in public preview at ship and nothing in-window says that changed, so the API is still recorded as preview and the expected field now distinguishes the two. Live Avatar is noted as a genuine capability addition rather than a distribution change — lip-synced video output moves 3.8 Live from live audio to live audio-visual — and is kept on this ticket rather than spun out because Google shipped it as a capability of 3.8 Live, not as a named model. The remaining open item is unchanged and unaddressed: no neutral organisation has published the Quality Index or tau-banking placements Google claimed at launch."
  - ts: 2026-09-25
    change: "Bookkeeping — citations added for the 2026-09-25 entry: @GoogleCloudTech (Gemini 3.8 Live with Live Avatar generally available in Gemini Enterprise; retweeted by @GoogleDeepMind) and @testingcatalog's daily brief (97 languages, async mid-conversation tool calls). No status, verification or content change."
---

Google shipped a **live-audio pair** on 2026-09-15, and the interesting half
is the smaller one: *3.8 Live Extended Thinking* runs tool calls
**asynchronously in the background while the conversation continues**. Every
prior voice stack in this repo's coverage — OpenAI's GPT-Live line, Grok
Voice, Muse Voice — treats a tool call as a stall the product then has to
paper over with filler audio. Decoupling the two is an architecture claim, not
a latency tweak, and it is the thing to check first when anyone gets hands-on.

**Why `confirmed` immediately.** Four Google accounts, including two official
org handles, posted the launch inside a 20-minute window with concrete
availability surfaces named per audience. There is nothing to corroborate; the
release is the primary source.

**What is not confirmed.** The leaderboard rows. 82.6 / #1 on the Artificial
Analysis Quality Index and 35.1 / #1 on τ-banking both come from a Google
employee's launch thread. That is a vendor benchmark claim until Artificial
Analysis publishes it themselves — the same standing this repo applied to the
Qwen3.8-27B agentic-index number ([[alibaba-qwen-3-8-27b-2026-08]]) and to
Meta's own Muse Spark evals ([[meta-hatch-muse-spark-2026-06]]).

**The price is the strategy.** At $0.005/min in and $0.018/min out, a
third-party digest computes **$1.38 per API hour against $3.00 for GPT-Live-1**
— roughly half. Google shipped the day after OpenAI's new full-duplex API
model, at half the hourly cost, with a longer language list. Read the two
tickets together; neither release explains itself alone.

**Transition triggers:**
- GA out of public preview, or Gemini Enterprise moving to general
  availability → UPDATE.
- Artificial Analysis or another neutral org publishes the Quality Index /
  τ-banking placements → UPDATE, note whether the first-party numbers held.
- A successor audio tier (3.9 Live, or a Live variant of a later Gemini) →
  new ticket; do not reopen.
- ≥4 weeks past release with no fresh signal → `closed: released-and-aged`.

**Dedup note:** Gemini 3.8 *text/Flash* signal stays on
[[gemini-3-8-flash-2026-09]]; transcription stays on
[[gemini-3-5-transcribe-2026-08]]; OpenAI's competing full-duplex API model is
[[openai-gpt-live-1-api-2026-09]].
