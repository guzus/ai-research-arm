---
slug: deepseek-second-round-2026-07
title: DeepSeek targets a $71-74B valuation in a second funding round, weeks after its $7.4B raise
company: DeepSeek
model: null
status: confirmed
status_note: |
  Per **Bloomberg** (via **@haricinews**, 2026-07-15 14:00 UTC): DeepSeek
  is preparing to raise up to another **$7.4B**, structuring a **second,
  distinct funding round** targeting overseas (particularly Middle East)
  dollar-denominated capital, aiming to file **IPO paperwork this year or
  early next year** for a mainland China **STAR Market** listing by
  **2027**. **@AShmueil** independently put the fresh-round target at
  **~$74B**, up from the ~$66.6B post-money valuation of the first $7.4B
  round that closed in June (see [[deepseek-funding-round-2026-05]]) —
  that ticket's own dedup note anticipates exactly this: "A follow-on
  round (Series-X / pre-IPO) gets a new ticket and links here."
  **@guo_lin99725** independently cited "50B yuan at a 500B yuan
  valuation," consistent in magnitude.

  **Unreconciled conflict to flag:** The Information's own account
  separately claimed DeepSeek is "seeking a tenfold valuation increase"
  — this desk could not reconcile that figure with Bloomberg's 10-15%
  figure; treat "tenfold" as unverified rather than additive.

  **2026-07-26 update:** Per **@rohanpaul_ai**, the round has reportedly
  been **paused before investors signed new agreements**, still
  targeting the ~$74B figure. Single-relay coverage; treated as an
  update to the round's status, not a contradiction of its existence.
expected: "Round reportedly paused before investor agreements signed; IPO paperwork timeline and STAR Market listing target unchanged pending resumption"
labels:
  - funding
  - china
  - ipo-track
verification: partial
sources:
  - "@haricinews"
  - https://x.com/haricinews/status/2077392750387892382
  - "@AShmueil"
  - https://x.com/AShmueil/status/2077392771615187099
  - "@guo_lin99725"
  - https://x.com/rohanpaul_ai/status/2081212716224778680
  - https://x.com/jukan05/status/2103010622019699076
  - https://x.com/rohanpaul_ai/status/2103056580128497793
  - https://x.com/jukan05/status/2103009658839638487
created_at: 2026-07-16
updated_at: 2026-09-24
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-16
    change: "Created — Bloomberg (via @haricinews, 2026-07-15 14:00 UTC) reports DeepSeek preparing a second, distinct funding round of up to $7.4B targeting overseas (Middle East) dollar capital, aiming to file IPO paperwork this year or early next year for a mainland China STAR Market listing by 2027. @AShmueil independently put the target valuation at ~$74B (up from ~$66.6B post-money in the first round, [[deepseek-funding-round-2026-05]]); @guo_lin99725 independently cited '50B yuan at 500B yuan valuation,' consistent in magnitude → status confirmed (multi-source convergence), verification partial (no DeepSeek primary). The Information's separate 'tenfold valuation increase' claim could not be reconciled with Bloomberg's ~10-15% figure — flagged as unreconciled, not added to the headline figure."
  - ts: 2026-07-26
    change: "@rohanpaul_ai reports the second round has been paused before investors signed new agreements, still targeting the ~$74B valuation reported 2026-07-16. Single-relay coverage in this window; status stays confirmed (underlying round is real, per the 2026-07-16 multi-source convergence) but status_note/expected updated to reflect the pause."
  - ts: 2026-09-24
    change: "FIRST REVENUE FIGURE, and a compute disclosure that bears on the raise. @jukan05, 2026-09-24, citing The Information: DeepSeek's ARR has reached $1 billion; the company allocates 70% of compute to training and 30% to inference; and it is running inference for its smaller models on NVIDIA gaming GPUs to free training capacity amid the shortage. @rohanpaul_ai quotes the same reporting more cautiously — '[Liang] told investors that DeepSeek's internal tests show its smaller models can run well on graphics chips designed for gaming' — i.e. a pitch to investors about test results, not a confirmed production deployment, and that weaker reading is the one adopted here. Recorded on this ticket rather than a new one because both items are material to the round it tracks: $1B ARR is the first public revenue anchor for a ~$71-74B ask, and the 70/30 split plus gaming-GPU substitution is a direct answer to the compute-constraint objection an investor would raise. Status stays confirmed, verification stays partial — single outlet via two relays, no DeepSeek statement, and no update on whether the paused round has resumed. Unverified adjacent claim, not adopted: @jukan05's suggestion that this explains RTX 5090 retail scarcity. Compare [[deepseek-huawei-ascend-950dt-2026-09]] for the domestic-silicon leg of the same compute problem, and note the concurrent regulatory exposure at [[china-deepseek-moonshot-data-probe-2026-09]]."
---

**DeepSeek** is preparing a **second, distinct funding round** — up to
another **$7.4B** — weeks after closing its first external round
(tracked at [[deepseek-funding-round-2026-05]]). Per **Bloomberg** (via
@haricinews), the round targets overseas capital, particularly from the
**Middle East**, denominated in dollars, and is part of a broader push
toward an **IPO**: DeepSeek aims to file paperwork this year or early
next year for a mainland China **STAR Market** listing by 2027.

**Why a separate ticket.** The first round's own dedup note explicitly
anticipated this: "A follow-on round (Series-X / pre-IPO) gets a new
ticket and links here." This is that follow-on — a structurally distinct
raise (different investor base, IPO-track purpose) from the June round,
not an update to the same instrument.

**Corroboration read.** Three independent accounts converge on the same
underlying event within the same cycle: @haricinews relays Bloomberg's
reporting on the round mechanics and IPO timeline; @AShmueil
independently reports a ~$74B target valuation, up from the ~$66.6B
post-money valuation of the first round; @guo_lin99725 independently
cites "50B yuan at a 500B yuan valuation" — consistent in order of
magnitude with the dollar figures. Three independent sources converging
clears the bar for `status: confirmed`, but there is still no DeepSeek
primary statement or filing, so `verification` stays `partial`.

**Unreconciled conflict.** The Information's own account separately
claimed DeepSeek is "seeking a tenfold valuation increase." This desk
could not reconcile that figure with Bloomberg's implied ~10-15% step-up
(~$66.6B → ~$71-74B) reported elsewhere in the same cycle. Treating
"tenfold" as an unverified outlier rather than folding it into the
headline valuation figure until it's independently corroborated or
explained.

**Transition triggers:**
- Round closes at a disclosed size/valuation → UPDATE with the number;
  ≥4 weeks of normal coverage → `closed: released-and-aged`.
- IPO paperwork actually filed → UPDATE, likely warrants advancing
  `verification` toward `confirmed` if via a named regulator/filing.
- The Information's "tenfold" figure gets independently corroborated or
  debunked → UPDATE `status_note` to reconcile.
- Round withdrawn or contradicted → close per `closed_reason`.

**Dedup note:** further signal on this second/pre-IPO round UPDATES
this ticket. The first, already-closed external round stays on
[[deepseek-funding-round-2026-05]]; do not conflate the two.
