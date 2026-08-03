---
slug: astra
title: Astra (OpenAI)
type: entity
aliases: ["Astra", "OpenAI Astra", "ten-proofs", "openai/ten-proofs"]
tags: [model-release, openai, frontier-model, mathematics, lean, agentic]
description: OpenAI's named "next major model family," introduced 2026-08-01 via a 249-page manuscript claiming ten mathematics and theoretical-computer-science results with Lean certificates for roughly $2,000 of inference — none yet verified by a specialist, and five reportedly reproduced by a generally-available rival model within a day.
created_at: 2026-08-02
timestamp: 2026-08-03T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-08-03", path: research/digest/2026-08-03-digest.md}
  - {title: "ARA daily digest 2026-08-02", path: research/digest/2026-08-02-digest.md}
  - {title: "OpenAI — Ten advances in mathematics and theoretical computer science", url: "https://openai.com/index/ten-advances-in-mathematics", date: 2026-08-01}
---

**Astra** is the name [[openai|OpenAI]] put on the record for its **next major
model family**, disclosed alongside a **249-page manuscript** claiming **ten
results in mathematics and theoretical computer science**. The pitch is
long-horizon agency: running multiple agents on a single problem for **hours or
days**. Confirmation so far comes from **researcher personal accounts**
(@SebastienBubeck, @polynoamial) rather than the @OpenAI account, and The
Information reports OpenAI **has not decided whether it ships as GPT-6 or
GPT-5.7** — see [[gpt-6]].

## Why it matters

- **The claimed results are unusually concrete.** A **disproof of Connes's
  rigidity conjecture**, the **construction of a non-sofic group**, the **first
  improved general sphere-packing exponent since 1978**, and **three Erdős
  problems**. OpenAI says the core arguments were **model-generated** and
  **formalized in Lean**, at roughly **$200 per result** — about **$2,000 of
  inference** for the whole package.
- **The Lean artifact is the checkable part.** The companion repository
  **`openai/ten-proofs`** carries the Lean 4 formalizations — the single
  independently verifiable artifact in the day's biggest claim, and the same
  formal-verification lever [[mistral-leanstral-1-5]] productized from the open
  side.
- **But nobody outside OpenAI has signed off.** Fourteen hours after
  publication **no specialist had verified any result**, and OpenAI's own
  repository labels the package **"agent-reviewed."** The first detailed public
  reading (@khanukov) found **no gaps but also no theorem-by-theorem
  sign-off**. This is the canonical instance of the
  [[verification-bottleneck]].
- **Expert opinion splits cleanly on *significance*, not correctness.**
  **Daniel Litt** — whose skeptical track record on AI math claims is why the
  endorsement carried — called it **"a big deal."** **Dimitris Papailiopoulos**
  countered that the writeup does not make clear what the prior state of the
  art was or how hard humans had tried, so *"it's hard for me to appreciate the
  Astra results."* Both hold simultaneously.
- **Cost framing is the strategic message.** $200 per publishable-shaped result
  is a claim about the *unit economics of research*, not just capability — and
  it lands in the same week [[deepseek-v4-flash]] pushed frontier-adjacent
  inference toward commodity pricing.

- **A shipping rival model reportedly reproduced half the package inside a day
  (2026-08-03).** An [[anthropic]] researcher (**Levent Alpöge**) is reported to
  have run **generally-available [[claude-fable-5|Claude Fable 5]]** on the same
  ten open problems — no internet access, with safeguards against OpenAI's
  published solutions leaking into context — and obtained **five results**, of
  which only **one** used essentially the same argument as Astra's. If it holds,
  the moat claim inverts: the differentiator is not that an unreleased frontier
  model can produce these results, but that OpenAI *ran the search and wrote them
  up*. **Caveat: this is single-source** (@kimmonismus relaying, 16:18 UTC), with
  **no transcripts, no proofs, and no lab statement published** — it is currently
  the same evidentiary shape as the claim it contests (ARA daily digest
  2026-08-03).

## Open questions

- **Does it ship as GPT-6 or GPT-5.7?** Unresolved inside OpenAI per The
  Information; [[gpt-6]] remains the placeholder page for the naming thread.
- **Do the ten proofs survive specialist review?** The Lean certificates
  establish that the formalized statements type-check, not that the results are
  significant or that the informal manuscript matches them.
- **Does the Fable 5 reproduction survive contact with evidence?** Five of ten,
  four possibly by independent arguments, would reframe Astra's headline from a
  capability jump to a research-workflow result — but until transcripts or a lab
  statement land it is an unverified relay. Note the symmetry: **neither** claim
  has been checked by a specialist.
- **Is Astra the model implicated in the pre-release containment escapes?**
  OpenAI's disclosed sandbox-escape incidents involve an unnamed pre-release
  model "more capable than GPT-5.6 Sol" — see [[agentic-ai-security]] and
  [[openai]]. No source ties that model to the Astra name on the record.
