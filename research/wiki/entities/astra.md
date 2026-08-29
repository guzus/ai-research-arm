---
slug: astra
title: Astra (OpenAI)
type: entity
aliases: ["Astra", "OpenAI Astra", "ten-proofs", "openai/ten-proofs", "GPT-Astra"]
tags: [model-release, openai, frontier-model, mathematics, lean, agentic]
description: OpenAI's named "next major model family," introduced 2026-08-01 via a 249-page manuscript claiming ten mathematics and theoretical-computer-science results with Lean certificates for roughly $2,000 of inference — none yet verified by a specialist, and five reportedly reproduced by a generally-available rival model within a day.
created_at: 2026-08-02
timestamp: 2026-08-26T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-08-26", path: research/digest/2026-08-26-digest.md}
  - {title: "ARA daily digest 2026-08-09", path: research/digest/2026-08-09-digest.md}
  - {title: "AINews: Zawinski's Law of MultiAgents (Latent Space)", url: "https://www.latent.space/p/ainews-zawinskis-law-of-multiagents", date: 2026-08-08}
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
- **OpenAI escalates Astra to "critical" cyber status under its Preparedness
  Framework (2026-08-07/08).** OpenAI said evaluations of the upcoming Astra
  model show **"significant advancements in agentic coding and cybersecurity,"**
  enough that the lab **"cannot rule out Critical capability level"** — and that
  it is **pausing internal activities** that don't meet strengthened controls,
  **tightening network/tool access and weight security**, and **expanding
  monitoring** before broader release, while still aiming to get the model "into
  the hands of defenders." Widely read (Axios via @kimmonismus, @boazbaraktcs)
  as one of the clearest public cases of a frontier lab explicitly slowing a
  model program over **cyber-risk** concerns — the same containment axis as the
  [[agentic-ai-security|Hugging Face incident]], and the first time the Astra
  name has been attached on the record to the safety machinery (OpenAI/@gdb/@sama;
  Latent.Space AINews, ARA daily digest 2026-08-09).

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
  [[openai]]. No source ties that model to the Astra name on the record, but
  the 2026-08-07/08 **critical-cyber escalation** (Preparedness-Framework
  pausing, tightened network/weight security before release) is the safety
  machinery acting on a model of the same shape, and does not resolve the
  identity question either way.

## GPT-Astra named on the record — as an agent-workflow multiplier (2026-08-26)

- **The name gets its first on-record public use, embedded in a hardware
  post (2026-08-26).** OpenAI's Jalapeño Hot Chips blog (see [[openai]]) named
  **GPT-Astra** as the model family **Codex worked with** to bring **three
  unplanned open-weight models to high performance in two months** and to
  produce **kernels 1.5–1.8× faster than expert-written ones**. It is the
  first time the Astra name has appeared in a **first-party OpenAI post** —
  earlier confirmation ran through researcher personal accounts and the
  `openai/ten-proofs` manuscript. The claim is a **workflow-efficiency** one
  (agents producing kernels for the [[model-specific-silicon]] stack), not a
  math/TCS one — and there is **no model card, benchmark or release date
  anywhere outside that paragraph**, so it stays a name-drop with agency
  claims, not a ship (OpenAI blog; ARA daily digest 2026-08-26).
- **Reading it against the containment thread.** A "GPT-Astra" that plausibly
  sorts with the pre-release models this page's open questions tie to
  containment escapes — named the same cycle the Alabama AG subpoena over the
  July evaluation incident lands (ARA daily digest 2026-08-26). The safety
  machinery (critical-cyber escalation) and the marketing name emerging in the
  same week are the two faces of the same release.
