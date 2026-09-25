---
slug: anthropic-billable-safeguard-blocks-2026-09
title: Anthropic resumes charging for safeguard-blocked requests in three abuse categories
company: Anthropic
model: null
status: released
status_note: |
  **In effect from 2026-09-24, announced primary.** @ClaudeDevs: "Today, we'll
  resume charging for requests our safeguards block before Claude responds.
  This only applies in categories with low false positive rates: **biology,
  distillation attacks, and frontier LLM development**. We've seen some
  coordinated attacks on our systems in recent weeks, and this is one layer of
  defense. In recent testing, 99.7% of accounts using Claude Code, Claude.ai,
  or Cowork did not hit any of these newly 'billable blocks.' The classifiers
  behind the blocks we're resuming charging for today are tuned to have a
  <0.1% false positive rate."

  **Why this is a shipping artifact and not just a policy note.** It changes
  what a customer is billed for: a request that never reaches the model now
  costs money. "Resume" also means this was previously charged, then stopped,
  and is now restarted — a reversal, which makes it a discrete, dated event.

  **The economic logic is explicit and worth stating plainly.** Free refusals
  make probing free. An attacker mapping a classifier's boundary needs many
  rejected requests, and if rejections cost nothing the attacker's search is
  unpriced while Anthropic pays the inference and serving cost of every probe.
  Charging for blocks puts a price on boundary-mapping. That is a defensive
  measure whose entire effect is on the cost curve, not on capability.

  **The category list is the tell about which attacks are live.**
  "Distillation attacks" is named second, and Anthropic has already publicly
  accused Alibaba-linked operators of the largest documented distillation
  attack on Claude ([[anthropic-alibaba-distillation-2026-06]]); China's
  regulator is separately probing whether DeepSeek and Moonshot routed data
  through Claude ([[china-deepseek-moonshot-data-probe-2026-09]]), and US
  officials have alleged Moonshot used fraudulent accounts to distill Claude
  into Kimi K3 ([[moonshot-claude-distillation-us-scrutiny-2026-07]]).
  "Frontier LLM development" as a billable-block category is the same concern
  stated generically.

  **The number that deserves scrutiny.** A <0.1% false-positive target and
  "99.7% of accounts hit none of these" are different statistics answering
  different questions, and neither bounds the harm to the 0.3% who did. A
  legitimate biosecurity or safety researcher is, by construction, the user
  most likely to be billed for refusals — and Anthropic runs an external
  researcher access program ([[anthropic-external-researcher-access-2026-08]])
  whose participants sit squarely in these categories.
expected: "In effect now. Open: whether the false-positive rate holds outside internal testing, whether any refund or appeal path exists for wrongly-billed blocks, whether the category list expands, and whether legitimate biosecurity/safety researchers report being charged."
labels:
  - anthropic
  - pricing
  - safety
  - abuse-prevention
  - distillation
  - released
verification: confirmed
sources:
  - https://x.com/ClaudeDevs/status/2103170368794185758
  - https://x.com/testingcatalog/status/2103371709281632423
created_at: 2026-09-25
updated_at: 2026-09-25
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-25
    change: "Created — RELEASED. @ClaudeDevs announced on 2026-09-24 17:11 UTC (~2,554 likes) that Anthropic is resuming charging for requests its safeguards block BEFORE Claude responds, limited to three low-false-positive categories: biology, distillation attacks, and frontier LLM development. Stated rationale: 'coordinated attacks on our systems in recent weeks'; stated impact: 99.7% of accounts on Claude Code, Claude.ai or Cowork hit none of these 'billable blocks' in recent testing, with the underlying classifiers tuned to a <0.1% false positive rate. Independently relayed in @testingcatalog's 2026-09-25 daily brief. Status released and verification confirmed — primary announcement, in effect the day of. Tracked as a shipping artifact rather than a policy note because it changes what customers are billed for and is explicitly a RESUMPTION, i.e. a dated reversal. The mechanism is recorded as an economic one: free refusals make classifier-boundary probing free to the attacker and costly to Anthropic, so charging for blocks prices the attacker's search. The category list is read as evidence of which attack classes are currently live, cross-linked to [[anthropic-alibaba-distillation-2026-06]], [[china-deepseek-moonshot-data-probe-2026-09]] and [[moonshot-claude-distillation-us-scrutiny-2026-07]]. Flagged for scrutiny: '<0.1% false positive rate' and '99.7% of accounts unaffected' are different statistics answering different questions, neither bounds harm to the affected minority, and the users most exposed are exactly the legitimate biosecurity and safety researchers Anthropic separately recruits via [[anthropic-external-researcher-access-2026-08]]."
---

This is a small billing change that encodes a real piece of adversarial
economics.

A safety classifier is a boundary, and boundaries get mapped by probing them.
The attacker's cost of probing is the number of requests they have to send; the
defender's cost is serving every one of those requests and running the
classifier on it. When refusals are free, that asymmetry runs entirely against
the defender — the attacker gets an unmetered oracle. Charging for blocked
requests flips it: each probe now costs the attacker something, and the cost
scales with how thoroughly they want to map the boundary.

The category selection follows from that. Anthropic is only charging where it
believes the classifier is precise, because in a low-precision category the
same mechanism would bill legitimate users for the model's own mistakes. That
is the right constraint to impose on yourself, and it is also the thing to
audit rather than accept: the false-positive rate quoted is from internal
testing, and the population that trips a biology classifier in the wild is not
the population that trips it in an eval set.

Note what this is not. It is not a price rise and not a capability change —
it changes the cost of being refused, which for 99.7% of accounts is zero. The
interesting number is never the 99.7%; it is who is in the 0.3%, and whether
any of them are the biosecurity researchers Anthropic has been actively
courting.
