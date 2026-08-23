---
slug: anthropic-claude-code-effort-mapping-2026-08
title: Claude Code "high" reasoning effort mapped to 10/100 — Anthropic calls it a numerical bug, not a downgrade
company: Anthropic
model: Claude (Claude Code effort scale)
status: confirmed
status_note: |
  On **2026-08-22** the community established that **Claude Code's
  "high" reasoning-effort setting was resolving to a value of 10 on a
  0–100 scale** — the same number that had previously meant "low."
  @kimmonismus surfaced it at 14:58 UTC (~2,100 likes): "If Fable has
  felt noticeably dumber this week, it's because Claude Code has
  apparently been running 'high' reasoning effort at just 10/100, the
  same level that was 'low' before. They dumbed down fable without
  telling it seems."

  **Anthropic answered the same day.** Engineer **Thariq (@trq212)**
  said the 10 was a **numerical mapping issue, not a stealth downgrade**
  — "high" is still high, and internal evals show **no performance
  regression**. He also conceded the underlying complaint on the record:
  "Yeah I agree that Opus 5 is a really spiky model and we want our
  models to be consistent." X's own trending surface carried it as
  "Anthropic Engineer Explains Claude Code Effort Scale Change"
  (~1,800 posts).

  **The explanation did not settle the perception.** @kimmonismus, after
  accepting the clarification, still reports that "most models currently
  feel significantly dumber to use. Especially Opus," and separately that
  Claude "speaks in such convoluted, overly long, and unnecessarily wordy
  terms that it's simply no fun." @TheAhmadOsman: "Friends don't let
  friends use Claude Code in August 2026." @kimmonismus reads the
  engagement as Anthropic taking the criticism seriously and expects a
  **Opus 5.1** — that expectation is his, not Anthropic's, and there is
  no Anthropic statement about any 5.1.

  Status `confirmed` and verification `confirmed`: the effect was
  reproduced by many users and the vendor engineer responded on the
  record. What is **not** established is whether an observable quality
  regression occurred — Anthropic says no, evals say no, users say yes,
  and no one has published a measurement either way.
expected: "Explained by Anthropic as a display/mapping issue on 2026-08-22 with no eval regression. Pending: a fix landing in the CLI, a written changelog entry rather than a reply, and whether the separate consistency complaint about Opus 5 produces a model update"
labels:
  - anthropic
  - claude-code
  - reasoning-effort
  - developer-tooling
  - confirmed
verification: confirmed
sources:
  - "@kimmonismus"
  - "@trq212"
  - "@TheAhmadOsman"
  - "@mark_k"
  - "@theo"
created_at: 2026-08-23
updated_at: 2026-08-23
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-23
    change: "Created — Claude Code's 'high' reasoning-effort setting was found resolving to 10 on a 0-100 scale, the value that previously meant 'low' (@kimmonismus 2026-08-22 14:58 UTC, ~2,100 likes), fuelling a week of 'Fable/Opus feels dumber' reports. Anthropic engineer Thariq (@trq212) responded the same day: a numerical mapping issue, not a stealth downgrade, with internal evals showing no performance regression; he separately conceded on the record that 'Opus 5 is a really spiky model and we want our models to be consistent.' Carried on X trending as 'Anthropic Engineer Explains Claude Code Effort Scale Change' (~1,800 posts). Status confirmed / verification confirmed on the vendor-engineer response plus wide reproduction; the underlying question of whether output quality actually regressed remains unmeasured on both sides. Community expectation of an 'Opus 5.1' is @kimmonismus's inference, not an Anthropic statement."
---

This ticket exists because a **configuration mapping** produced, for one
week, the same user-visible outcome as a silent model downgrade — and
because the vendor's correction and the users' experience still do not
agree.

**What is settled.** Claude Code's `high` effort setting was emitting 10
on a 0–100 scale. Anthropic's own engineer confirmed the number and
called it a mapping bug rather than a policy change, and said internal
evaluations show no regression in performance. That is a primary-source
response from the vendor, which is why verification is `confirmed`.

**What is not settled is the thing users actually care about.** Anthropic
asserts no regression; a large number of heavy users assert the models
have felt materially worse for a week. Neither side has published a
measurement. Note the asymmetry in what each claim can prove: internal
evals can show a *scored* metric held steady while the property being
complained about — verbosity, consistency, "spikiness" — is not on the
eval. Thariq's own concession that Opus 5 is "really spiky" and that
Anthropic wants consistency is the strongest evidence that the
complaints are tracking something real, whether or not the effort
mapping caused it.

**Why it matters beyond one CLI flag.** Reasoning-effort settings are
now a priced product surface across the industry — OpenAI adjusted
GPT-5.6's effort budget post-GA and compensated with banked resets
([[openai-gpt-5-6]]); @LottoLabs reports Qwen 3.8 27B scoring *better* at
medium than at xhigh on Terminal-Bench 2.1. Effort is not monotonic, it
is not always visible, and when a vendor changes it, users experience it
as the model getting worse. That is a recurring failure mode, not a
one-off.

The timing compounded it: the reports landed the same week
[[stealth-ox-alpha-model-2026-08]] had developers comparing a free
stealth model favourably against Fable and Sol, and the day before
OpenAI cut GPT-5.6 Sol API pricing by 20%.

Related: [[anthropic-opus-5-leak-2026-07]], [[claude-fable-5]],
[[anthropic-claude-code-design-2026-08]].
