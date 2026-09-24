---
slug: china-deepseek-moonshot-data-probe-2026-09
title: China's internet regulator probes DeepSeek and Moonshot over user data allegedly routed to Claude
company: PRC (Cyberspace regulator) / DeepSeek / Moonshot AI / Anthropic
status: confirmed
status_note: |
  @theinformation, 2026-09-23 18:00 UTC: "China's internet regulator is
  investigating DeepSeek and Moonshot AI after Anthropic alleged the companies
  routed sensitive user data to Claude without customers' knowledge. The probe
  is examining whether Chinese military, police and state-owned corporate data
  was sent to the U.S."

  The allegation itself, restated by the reporter @jingyanghk (2026-09-24 01:00
  UTC): "Anthropic said that Moonshot and DeepSeek forwarded users' requests,
  including sensitive data such as police security camera footage, without their
  own customers', their own users' knowledge, and passed over the answers to
  their customers as if these were processed by their own models when, in fact,
  they were processed by Claude."

  Note the inversion this creates. Anthropic's prior China complaints were about
  **distillation** — Chinese labs harvesting Claude outputs to train their own
  models ([[anthropic-alibaba-distillation-2026-06]],
  [[moonshot-claude-distillation-us-scrutiny-2026-07]],
  [[xai-claude-training-cutoff-2026-06]]). This allegation is about
  **passthrough**: serving Claude to end users while presenting it as a domestic
  model. Distillation is a theft-of-capability claim; passthrough is a
  data-export and consumer-deception claim, and it is the second one that gives
  Beijing a reason to act against its own national champions.

  No statement from DeepSeek, Moonshot or the regulator in this cycle's signal;
  Anthropic's allegation reaches us through the same reporting. Single outlet,
  but a named reporter with a direct quote of the allegation — status
  `confirmed` on the probe's existence, verification `partial`.
expected: "TBD — no announced timeline. Watch for a regulator finding, a DeepSeek/Moonshot denial, or an Anthropic statement on record."
labels:
  - china
  - deepseek
  - moonshot
  - anthropic
  - regulatory
  - data-security
verification: partial
sources:
  - https://x.com/theinformation/status/2102820348060123302
  - https://x.com/theinformation/status/2102926185533432009
  - https://x.com/theinformation/status/2102792856939245756
created_at: 2026-09-24
updated_at: 2026-09-24
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-24
    change: "Created — CONFIRMED (probe), PARTIAL (allegations). The Information reported 2026-09-23 that China's internet regulator opened an investigation into DeepSeek and Moonshot AI after Anthropic alleged the two routed sensitive user requests to Claude without their customers' or users' knowledge and returned Claude's answers as if produced by their own models; the probe is examining whether Chinese military, police and state-owned corporate data — including police security camera footage — was sent to the United States. Reporter @jingyanghk restated the allegation directly on 2026-09-24. No DeepSeek, Moonshot, regulator or on-record Anthropic statement in this cycle's signal, hence verification partial. Recorded as a distinct claim class from the existing distillation tickets ([[anthropic-alibaba-distillation-2026-06]], [[moonshot-claude-distillation-us-scrutiny-2026-07]]): those allege harvesting Claude outputs to train rival models, this alleges reselling live Claude inference as a domestic model, which is a data-export and misrepresentation claim rather than an IP one."
---

The claim category matters more than the headline. Every previous
Anthropic-versus-China item on this set has been a distillation story: someone
harvesting Claude outputs to train a competing model
([[anthropic-alibaba-distillation-2026-06]],
[[moonshot-claude-distillation-us-scrutiny-2026-07]]). This is the opposite
direction. The allegation is that DeepSeek and Moonshot were *customers* — and
that they passed their own users' requests through to Claude and presented the
results as their own model's output.

If true, three separate harms stack, and only one of them is Anthropic's.
Anthropic's harm is brand and terms-of-service. The Chinese users' harm is that
their data left the country without their knowledge. Beijing's harm is the one
that produces a regulator: police camera footage and state-owned enterprise data
crossing to a US provider is a national-security exposure regardless of what
anyone thinks of Anthropic. That is why this can plausibly be pursued against
two of China's most strategically important labs rather than quietly dropped.

The sourcing asymmetry is worth naming. Everything here — the probe, the
allegation, Anthropic's role — arrives through one outlet. Anthropic has not
said this on the record in this cycle's signal, and neither lab has denied it.
A denial would be informative; so would silence past a couple of cycles, given
how quickly Chinese labs have publicly rebutted US distillation claims before.

Second-order exposure worth tracking: Moonshot's models underpin third-party
products ([[harvey-tenet-legal-model-2026-08]]), and DeepSeek is simultaneously
raising ([[deepseek-second-round-2026-07]]) and building domestic compute
([[deepseek-huawei-ascend-950dt-2026-09]]). A finding that either lab's serving
stack was partly foreign passthrough would land on all three.
