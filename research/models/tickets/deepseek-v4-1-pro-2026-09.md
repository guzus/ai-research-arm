---
slug: deepseek-v4-1-pro-2026-09
title: DeepSeek V4.1 Pro — reportedly in early gray-scale testing
company: DeepSeek
model: DeepSeek V4.1 Pro
status: in-testing
status_note: |
  **Single Chinese-language source, 2026-09-28 02:56 UTC.** @zane_os: "Deepseek
  V4.1 Pro 正在早期灰度测试" — DeepSeek V4.1 Pro is in early gray-scale (staged
  rollout) testing — with the customary "大的要来了" ("the big one is coming").

  **The most reliable China-desk reader in-window explicitly discounted the
  evidence class.** @teortaxesTex, quoting that post (04:34 UTC): "**ignore
  'gray-scale testing' evidence for your own sanity**", adding "I hope it's not
  Opus 5.5 again (it probably will be, for some queries at least)" — i.e. the
  suspicion that a gray-scale probe is picking up a router serving something
  else. That caveat is recorded here as part of the record, not around it.

  **A related claim was denied in the same window.** @tianyi (03:29 UTC), replying
  to a user: 辟谣，并没有"说过 v4.1 pro 会和 DSH 官方发布一起" — a denial that anyone
  said V4.1 Pro would ship together with the official DSH release. @teortaxesTex's
  reaction: "oh no". So the *bundling* claim is disclaimed; the existence of
  gray-scale testing is not denied, but neither is it corroborated.

  Context for what was being bundled: @teortaxesTex (02:36 UTC) had said "would be
  cool if DeepSeek released DSH 0.2 together with V4.1 Pro that's further trained
  for DSH and agent teams on Monday. I think at least next week until Thursday is
  very likely." That is a wish and a personal probability estimate, not a report.

  **Status `in-testing`, verification `unverified`, and both are deliberate.**
  `in-testing` because a staged rollout is an artifact class this set has
  consistently treated as more than a tease. `unverified` because the entire
  record is one relay account, disputed by a second, with **no DeepSeek post, no
  model card, no API id, no pricing, no benchmark and no firsthand output**.

  **Why a new ticket rather than an update to [[deepseek-v4-1-2026-09]].** That
  ticket tracks V4.1 and V4.1 Flash, which are already released into third-party
  hands. A "Pro" tier is a distinct model id with its own release event and,
  on DeepSeek's history, its own weights-release posture — the V4-Pro line has
  its own precedent at [[deepseek-v4-pro-price-cut-2026-05]].

  **DeepSeek's release shape makes this hard on purpose.** As
  [[deepseek-v4-1-2026-09]] records, V4.1 itself shipped with no announcement,
  no model card and no pricing — the entire record was incidental operator usage.
  Gray-scale chatter preceding a silent launch is this lab's normal pattern, which
  is exactly why it cannot be distinguished from noise in advance.
expected: "TBD — no date. @teortaxesTex put 'at least next week until Thursday' on a DSH-bundled release as his own estimate, and a separate account denied that the bundling was ever claimed. Watch for: an API id, a first third-party hands-on with distinguishing output, or DeepSeek's usual silent availability."
labels:
  - deepseek
  - china
  - frontier-model
  - gray-scale
  - unreleased
verification: unverified
sources:
  - https://x.com/zane_os/status/2104404806848983262
  - https://x.com/teortaxesTex/status/2104429412682985687
  - https://x.com/teortaxesTex/status/2104399733645009217
  - https://x.com/tianyi/status/2104413106990645683
  - https://x.com/teortaxesTex/status/2104419150781165828
created_at: 2026-09-28
updated_at: 2026-09-28
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-28
    change: "Created — @zane_os (2026-09-28 02:56 UTC) reports DeepSeek V4.1 Pro in early gray-scale testing. Status in-testing on the staged-rollout artifact class; verification unverified, with the disconfirming context recorded in full: @teortaxesTex, the strongest China-desk reader in-window, told readers to 'ignore gray-scale testing evidence for your own sanity' and suspects a router may be serving Opus 5.5 for some queries, and @tianyi separately denied that anyone claimed V4.1 Pro would ship alongside the official DSH release. No DeepSeek post, model card, API id, pricing, benchmark or firsthand output. Opened as a new ticket rather than an update to [[deepseek-v4-1-2026-09]] because a Pro tier is a distinct model id with its own release event, on precedent from [[deepseek-v4-pro-price-cut-2026-05]]."
---

One account reports a staged rollout. The most credible reader of Chinese AI
signal in the same window told people to ignore exactly that class of evidence,
and a third account denied a related bundling claim. This ticket exists to hold
the name, not to assert the release.

The reason to open it anyway is DeepSeek's release shape. V4.1 and V4.1 Flash
arrived with no announcement, no model card and no pricing — the entire record on
that ticket is operators discovering the model was already being served. A lab
that ships silently will always have gray-scale chatter ahead of it, and that
chatter will always be indistinguishable from noise until someone posts a
distinguishing output.

The specific failure mode @teortaxesTex names is worth internalising: a
gray-scale probe that reports "something new is being served" may be detecting a
router change, not a new model, and on aggregator surfaces the thing actually
answering has sometimes turned out to be a competitor's model. So "gray-scale
testing observed" is weaker than it sounds even when the observation is honest.

What would move this: an API id, a price, or one reproducible prompt that
separates V4.1 Pro from V4.1.
