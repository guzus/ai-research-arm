---
slug: openai-aeon-agent-2026-09
title: OpenAI "Aeon" — rumored persistent always-on agent
company: OpenAI
model: Aeon (project name)
status: closed
status_note: |
  **Single-source tease, 2026-09-24 11:09 UTC.** @mark_k: "He's referring to
  project 'Aeon': Aeon is rumored to be @OpenAI's answer to Grok Bot: a
  persistent, always-on AI agent that can remember ongoing work, operate across
  apps and websites, and continue completing tasks in the background over days
  or weeks. Release may be today!"

  **It did not release that day.** The post is ~25 hours old at this ticket's
  creation and nothing named Aeon has appeared. The "release may be today"
  prediction is recorded precisely because it failed — an unmet same-day
  release call is the cheapest available evidence about a source's confidence
  level, and it lowers the prior here.

  **Status `rumored`, verification `unverified`, and both are honest.** There
  is no artifact: no registry entry, no app string, no console listing, no
  OpenAI statement. This is one account relaying a project codename and a
  capability description. It is exactly the class of claim the lifecycle puts
  at the bottom.

  **The shape is plausible, which is not evidence.** A persistent background
  agent is the obvious competitive answer to [[xai-grok-bot-2026-08]], it fits
  the "super app" overhaul already tracked at
  [[openai-chatgpt-superapp-2026-06]], and OpenAI acquired Ona for exactly this
  primitive — persistent cloud environments for Codex agents
  ([[openai-ona-acquisition-2026-06]]). A rumour that fits a company's
  announced strategy is more likely true and no better corroborated.

  **Near-term resolution.** OpenAI DevDay is 2026-09-29. If Aeon is real and
  close, that is the venue; if DevDay passes with nothing, this should close as
  a stale unverified rumour rather than sit open on a codename.
expected: "OpenAI DevDay, 2026-09-29 (@OpenAIDevs posted a 72-hour countdown on 2026-09-26). The naming question is largely answered: the consumer product appears to be 'o', and 'Aeon' is reported to be the internal name for the EXISTING ChatGPT Workspace custom-Agents feature it would be built on. Open: an actual announcement, capability scope, which plans get it, pricing, and whether 'o' is an agent, a model, or both."
labels:
  - openai
  - agents
  - rumor
  - unreleased
verification: partial
sources:
  - https://x.com/mark_k/status/2103079300689691086
  - https://x.com/testingcatalog/status/2103787365986623925
  - https://x.com/OpenAIDevs/status/2103929727761137940
  - https://x.com/testingcatalog/status/2103931271374307508
  - https://x.com/testingcatalog/status/2104493424472674634
  - https://x.com/mark_k/status/2104462157689602072
  - https://x.com/insanekrishnaa/status/2105147666850304017
created_at: 2026-09-25
updated_at: 2026-09-30
closed_at: 2026-09-30
closed_reason: superseded-by:openai-dots-agents-2026-09
history:
  - ts: 2026-09-25
    change: "Created — RUMORED / unverified. @mark_k (2026-09-24 11:09 UTC, ~844 likes) described project 'Aeon' as OpenAI's rumored answer to Grok Bot — a persistent, always-on agent that remembers ongoing work, operates across apps and websites, and continues tasks in the background over days or weeks — and predicted 'Release may be today!'. It did not release that day, and that failed same-day call is recorded deliberately as a downward adjustment on the source's confidence. Status rumored and verification unverified because there is NO artifact of any kind: no registry entry, app string, console listing or OpenAI statement, only one account relaying a codename. The capability shape is consistent with OpenAI's stated direction — a competitive answer to [[xai-grok-bot-2026-08]], fitting the super-app overhaul at [[openai-chatgpt-superapp-2026-06]], and built on the persistent-cloud-environment primitive acquired via [[openai-ona-acquisition-2026-06]] — but coherence with strategy is not corroboration and is recorded as context only. DevDay on 2026-09-29 is the natural resolution point; if it passes silently this should close under stale-rumor-unverified rather than persist on a codename alone."
  - ts: 2026-09-28
    change: "The ticket's central question — 'is Aeon a real thing' — got a partial answer that PARTLY FALSIFIES its own title, and an artifact appeared. @testingcatalog (2026-09-26 10:02 UTC): the upcoming always-on assistant will be named 'o'; its reference 'appeared briefly on the ChatGPT upgrade screen for some users'; internal config carries 'o' as a display name and '-o' as an email suffix, implying email handling. Critically, the same post reframes this ticket's subject: 'A rumored Aeon reference is an internal name for the existing custom Agents implementation for ChatGPT Workspace accounts. Yet OpenAI will likely build a consumer-facing o assistant on top of this feature.' So 'Aeon' is reported to be an existing internal feature name, not an unreleased product — the codename this ticket was opened on was pointed at the wrong object. Status rumored -> in-testing on the app-string artifact (config entries and an upgrade-screen reference are the same evidence class as a console listing), verification unverified -> partial (an artifact plus a first-party teaser, still no OpenAI statement naming the product). First-party timing anchor: @OpenAIDevs (2026-09-26 19:28 UTC) '72 hours to OpenAI DevDay. We've been building. Time to show our work.', which @testingcatalog read as OpenAI teasing 'o' for the event. Rollout detail, chatter-grade: all Pro plans rather than Pro Max only, Codex Plus excluded, Fast Mode referenced (2026-09-28 brief). @mark_k predicts DevDay ships 'o', Astra 6.1, and the ChatGPT/Work unification ([[openai-chatgpt-superapp-2026-06]]) — a prediction, logged as such. TITLE KEPT per the no-rename rule; if 'o' ships as a named product it gets its own ticket and this one closes as superseded."
  - ts: 2026-09-30
    change: "CLOSED — superseded-by:openai-dots-agents-2026-09, on the transition this ticket declared for itself. The product shipped at DevDay on 2026-09-29 and it is called DOTS: always-on agents running on GPT-6 Astra, each with its own cloud computer and browser, working across 4,000+ apps and inside ChatGPT, Slack and Teams. The successor is [[openai-dots-agents-2026-09]]. Scoring this ticket honestly, because that was its stated purpose: the SHAPE was right and arrived early — @mark_k's 2026-09-24 description of a persistent always-on agent that remembers ongoing work, operates across apps and websites and continues tasks in the background over days or weeks is very close to what shipped, and the DevDay venue this ticket named on 2026-09-25 was correct. The NAMES were both wrong. 'Aeon' was reported on 2026-09-26 to be an internal label for an existing ChatGPT Workspace Agents feature, and 'o' — the name this ticket switched to on 2026-09-28 on the strength of an upgrade-screen string and internal config entries — is not what the product is called either. That is the durable lesson and the reason this ticket existed: app-surface artifacts reliably tell you a product is coming and reliably do not tell you what it will be named. The failed same-day release call of 2026-09-24 stands as recorded. History preserved and not rewritten; the successor carries the shipped artifact."
---

This ticket exists to make a weak claim decay honestly rather than get
retold until it sounds established.

The substance is one post, one codename, and a same-day release prediction that
did not happen. Everything else about it — that a persistent background agent
is where the product category is heading, that OpenAI bought the exact
infrastructure primitive for it, that xAI already shipped something similar —
is context that makes the rumour feel right without making it any better
sourced.

That combination is precisely the failure mode worth guarding against. A rumour
that coheres with a company's public strategy gets repeated more, not verified
more, and after a few cycles the repetition becomes the evidence.

DevDay on September 29 resolves it cheaply in either direction. Until then the
only defensible statement is that one account has described an unannounced
OpenAI project by name, and nothing has appeared.
