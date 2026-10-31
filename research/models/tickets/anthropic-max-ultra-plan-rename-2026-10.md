---
slug: anthropic-max-ultra-plan-rename-2026-10
title: "Anthropic renames Claude Max plans (Max 5x → Max, Max 20x → Ultra) and removes the 5-hour limit for verified Ultra accounts"
company: Anthropic
model: "Claude (Max / Ultra subscriptions)"
status: released
status_note: |
  **First-party, 2026-10-30 17:29 UTC.** @claudeai: "We're renaming our Max plans: Max 5x → Max,
  Max 20x → Ultra. Max is still $100/month, and Ultra is still $200." The 5-hour limit is removed for
  verified Ultra accounts, "starting today with most existing subscribers". Newer accounts keep a
  temporary limit until they are verified, as a fraud and abuse control. Weekly limits are unchanged.

  **Why the rename.** @mboverell (leads product for Claude subscriptions): "Max 20x" described the
  5-hour limit (20x Pro), but the weekly limit was set at 10x Pro, and "some new users assumed 20x
  applied to both limits... I'm sorry." Ultra keeps the 10x-Pro weekly limit and drops the 5-hour one.
  @alexalbert__ (Anthropic): "no more 5 hour rate limits for Ultra subs."

  **Why `released`:** the change is live for most existing subscribers as of 2026-10-30, with a staged
  rollout for the rest.
expected: "Live 2026-10-30 for most existing Ultra subscribers; staged removal of the 5-hour limit for newer accounts after verification. @mboverell: 'We've got more cooking.'"
labels:
  - pricing
  - subscriptions
  - rate-limits
  - claude
verification: confirmed
sources:
  - https://x.com/claudeai/status/2116220869479428500
  - https://x.com/mboverell/status/2116221457252659275
  - https://x.com/alexalbert__/status/2116227345501880781
  - https://x.com/alexalbert__/status/2116227346869194935
created_at: 2026-10-31
updated_at: 2026-10-31
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-31
    change: "Created — RELEASED / confirmed. @claudeai (2026-10-30 17:29 UTC) renamed Max 5x to Max ($100/month) and Max 20x to Ultra ($200/month), and began removing the 5-hour limit for verified Ultra accounts, starting with most existing subscribers. Newer accounts keep a temporary limit until verified, and weekly limits are unchanged. Subscriptions product lead @mboverell says the old name was misleading, because the weekly limit was 10x Pro while only the 5-hour limit was 20x, and apologises. @alexalbert__ relays both posts."
---
This is a packaging change, not a new model, but it changes how much Claude a top-tier subscriber can
use in practice. Removing the 5-hour window means the weekly limit is the only constraint for Ultra.
That is what heavy Claude Code users kept running into mid-session.

The apology matters as much as the policy. Anthropic is admitting that "20x" was read as a promise
for both limits when it applied to only one. Renaming the plan rather than raising the weekly limit
fixes the label, not the allowance: Ultra's weekly limit is still 10x Pro.

The verification gate for newer accounts points to abuse of the top plan, such as account resale or
farming, as the cost Anthropic is guarding against.

**Watch:** whether "more cooking" means a higher tier or weekly-limit changes, and whether the staged
rollout reaches newer accounts as described.
