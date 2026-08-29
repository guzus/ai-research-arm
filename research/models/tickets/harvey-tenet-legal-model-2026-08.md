---
slug: harvey-tenet-legal-model-2026-08
title: Harvey unveils "Tenet", a legal foundation model post-trained on Moonshot's Kimi K3
company: Harvey / Moonshot AI
model: Harvey Tenet
status: in-testing
status_note: |
  **Harvey** — the legal-AI company valued at **~$11B**, backed by
  OpenAI, Sequoia and a16z — is reported to have unveiled **Harvey
  Tenet**, its first in-house foundation model, built by post-training
  **Moonshot AI's open-weight Kimi K3** on specialized legal data
  (@Chlowcr9, 2026-08-24 07:09 UTC).

  Reported specifics: trained in **~2 months on ~150 B300 GPUs**;
  claimed to **outperform GPT-5.6 on complex legal tasks**; sharply
  lower inference cost. The same relay says **AT&T is evaluating Kimi K3
  and DeepSeek** for internal use and that **DoorDash and Airbnb** made
  similar choices.

  Status `in-testing`, not `rumored`: the claim is not a tease about a
  future model but a description of a **trained, benchmarked artifact**
  with a named base model, a training budget and a compute figure. It is
  also not `confirmed` — verification is **`unverified` and that is the
  honest call**: this is a **single French-language secondary relay**,
  with no Harvey post, no model card, no benchmark table, and no
  Moonshot acknowledgement captured. Every number here (the $11B
  valuation, the 2 months, the 150 B300s, the GPT-5.6 comparison) rests
  on that one account.

  **If it holds, the significance is the direction of the dependency,
  not the model.** An OpenAI-funded American vertical unicorn choosing a
  **Chinese open-weight base** over its own investor's closed API is the
  sharpest instance yet of the substitution pattern already visible
  across this ticket set — open-weight token share on Vercel's gateway
  going 28% → 62% in two months, and Microsoft separately evaluating K3
  for Copilot features (recorded on [[moonshot-kimi-k3]] before it
  closed).
expected: "Reported 2026-08-24 as an unveiled model: Harvey Tenet, post-trained from Kimi K3 on legal data, ~2 months on ~150 B300 GPUs, claimed to beat GPT-5.6 on complex legal work. Pending: ANY primary evidence — a Harvey announcement, model card, benchmark methodology, or availability date — plus independent confirmation of the AT&T / DoorDash / Airbnb evaluations. Close as stale-rumor-unverified if no corroboration appears within ~15 cycles"
labels:
  - harvey
  - legal-ai
  - kimi-k3
  - open-weights
  - vertical-model
verification: unverified
sources:
  - "@Chlowcr9"
  - https://x.com/Chlowcr9/status/2091784824411598893
created_at: 2026-08-24
updated_at: 2026-08-24
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-24
    change: "Created — Harvey (legal AI, ~$11B, backed by OpenAI/Sequoia/a16z) reportedly unveiled Harvey Tenet, its first in-house foundation model, post-trained from Moonshot's open-weight Kimi K3 on specialized legal data: ~2 months, ~150 B300 GPUs, claimed to beat GPT-5.6 on complex legal tasks at sharply lower inference cost; same relay says AT&T is evaluating Kimi K3 and DeepSeek internally, with DoorDash and Airbnb making similar choices (@Chlowcr9 2026-08-24 07:09 UTC). Status in-testing — a described trained-and-benchmarked artifact, not a tease. Verification unverified — a single secondary relay, no Harvey post, no model card, no benchmark table, no Moonshot acknowledgement; every figure rests on that one account. Significance if true is the dependency direction: an OpenAI-funded US vertical building on a Chinese open-weight base rather than its investor's closed API."
---

**Harvey**, the legal-AI company most closely identified with building on
OpenAI's models, is reported to have shipped its own foundation model —
**Tenet** — by post-training **Moonshot AI's Kimi K3** open weights on
legal data.

**Read the sourcing before the story.** This ticket exists on one
account's post. There is no Harvey announcement, no model card, no
published benchmark, and no acknowledgement from Moonshot. The
`unverified` flag is not a formality here: if this turns out to be a
garbled retelling of a partnership or a pilot, nothing in the numbers
above survives. It is filed because the specificity is checkable — a
named base model, a named GPU (**B300**), a count (**~150**), and a
duration (**~2 months**) are the kind of claims that get corrected fast
if wrong.

**Why the claim is structurally plausible.** Vertical AI companies have
the one thing frontier labs do not: proprietary domain data and a
narrow, well-defined task distribution. Post-training a strong open base
on that data is cheap relative to renting frontier inference at scale
forever — ~150 B300s for two months is a rounding error next to an
enterprise API bill. The economics point this way regardless of whether
this particular instance is real.

**The uncomfortable part, if it is real, is whose weights.** Harvey's
investors include OpenAI. Choosing Kimi K3 — a 2.8T-parameter Chinese
open-weight model released under a Modified MIT licence
([[moonshot-kimi-k3]]) — over a closed American API is a procurement
decision with a policy shadow: the same K3 line is the subject of US
scrutiny over alleged Claude distillation
([[moonshot-claude-distillation-us-scrutiny-2026-07]]), and open-weight
policy is actively contested
([[industry-open-weights-letter-2026-07]]).

**Close trigger to honour:** if nothing corroborates this within ~15
cycles, close it `stale-rumor-unverified` rather than letting an
unsourced $11B-company claim sit open indefinitely.

Related: [[stealth-ox-alpha-model-2026-08]],
[[deepseek-v4-flash-vision-exp-2026-08]], [[openai-gpt-5-6]].
