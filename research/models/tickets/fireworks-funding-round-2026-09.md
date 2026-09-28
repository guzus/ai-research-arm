---
slug: fireworks-funding-round-2026-09
title: Fireworks AI weighing a round at a ~$30B valuation, ten weeks after $17.5B
company: Fireworks AI
model: null
status: rumored
status_note: |
  **The Information, relayed 2026-09-27 10:39 UTC by @mark_k:** Fireworks AI "is
  considering a round that could value it at **$30 billion**." Anchors in the same
  report: it **raised $1.5B at a $17.5B valuation in July** and **says it now
  serves more than 40 trillion tokens a day**.

  **The delta is the whole story.** $17.5B → $30B is **+$12.5B in just over two
  months**, on a business whose scale claim is a self-reported token volume rather
  than revenue. @mark_k states the obvious constraint himself: "Neither new round
  has closed."

  **Status `rumored`, and the hedge language is load-bearing.**
  "Considering… could value" — no lead, no terms, no close date, no Fireworks
  statement. Verification `partial`: one outlet, one relay of that outlet.

  **What makes the multiple arguable rather than absurd.** Fireworks shipped its
  own model in the same window — Ember-1, a Kimi K3 post-train claiming ~40%
  cheaper reasoning ([[fireworks-ember-1-2026-09]]). @quxiaoyin described the
  pattern in-window without naming the company: host the strong Chinese open
  weights, sell the inference, ship a model of your own, and raise on the blended
  story. A provider that is also a lab prices differently from a provider.

  **What cuts against it.** The 40-trillion-tokens-a-day figure is Fireworks'
  own; no revenue number for Fireworks appears in-window (its comparable, fal, is
  reported at ~$800M annualized). The account is also **suspended for non-payment
  on this repo's own billing** as recorded on the Fireworks credential note — an
  unrelated incident, but a reminder that token volume and collected revenue are
  different quantities.

  **Sibling ticket from the same report:** [[fal-funding-round-2026-09]].
expected: "TBD — reported consideration only. Watch for a named lead, confirmed terms, a close, or a Fireworks statement. A revenue figure would be the single most useful missing datapoint."
labels:
  - funding
  - inference-provider
  - megaround
  - rumor
verification: partial
sources:
  - https://x.com/mark_k/status/2104159069531467928
created_at: 2026-09-28
updated_at: 2026-09-28
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-28
    change: "Created — The Information (relayed by @mark_k, 2026-09-27) reports Fireworks AI is considering a round valuing it at ~$30B, against $1.5B raised at $17.5B in July and a self-reported >40 trillion tokens/day. Status rumored on the report's own hedges ('considering… could value'), verification partial — one outlet, one relay, no lead, terms, close date or company statement. Recorded alongside [[fireworks-ember-1-2026-09]], shipped the same week, because a provider that also ships a model is being priced as a lab rather than as infrastructure. No Fireworks revenue figure in-window, which is the gap that matters for a +$12.5B step in ten weeks."
---

Two months after closing at $17.5B, Fireworks is reportedly testing $30B. The
supporting number in the report is a token count, not a revenue line.

That distinction matters more here than in most funding tickets. Fireworks'
comparable in the same report, fal, comes with an annualized revenue figure
(~$800M). Fireworks comes with 40 trillion tokens a day, which it states about
itself, and which converts to revenue only at a price and a margin neither
disclosed.

What plausibly justifies re-rating is the week's other Fireworks event: it
shipped Ember-1, its own post-trained model on a disclosed Kimi K3 base. An
inference provider earns an infrastructure multiple. A provider with a model
earns something closer to a lab multiple. Shipping one ten weeks into a
fundraising window is either good sequencing or the point.

Nothing has closed, and the report says so. Treat the $30B as the ask.
