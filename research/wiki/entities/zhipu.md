---
slug: zhipu
title: Zhipu / Z.ai
type: entity
aliases: [Zhipu, "Zhipu AI", "Z.ai", ZCode]
tags: [frontier-lab, china, open-weights, funding]
description: Chinese frontier lab behind the GLM family; researcher ferstar says the ZCode desktop app silently uploads complete Git history to Aliyun OSS with no UI off-switch.
created_at: 2026-09-14
timestamp: 2026-09-19T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-09-19", path: research/digest/2026-09-19-digest.md}
  - {title: "ARA daily digest 2026-09-14", path: research/digest/2026-09-14-digest.md}
---

**Zhipu AI** (branded **Z.ai**) is the Chinese frontier lab behind the
GLM family. Until this ingest it appeared only as the maker of
[[zhipu-glm-5-2|GLM-5.2]], [[zhipu-glm-5-3|GLM-5.3]], and the
confirmed [[ox-alpha]] stealth line. The 2026-09-14 **$5 billion
HKEX close** is a company-level financing print, not a new model
SKU, so it gets its own page.

US agencies named Z.AI among six Chinese labs in joint advisory
**AA26-251A** (2026-09-10), alleging industrial-scale distillation
of Claude, GPT, Gemini and Grok. See [[federal-ai-policy]] and
[[anthropic]].

## Why it matters

- **$5 billion HKEX close (2026-09-14).** About **$2 billion** of
  new Hong Kong shares — **21.97 million** shares at **HK$714**, a
  **10% discount to Friday** — plus **20.14 billion yuan** of
  **zero-coupon convertibles due September 2027**. Sixty percent of
  net proceeds is tagged for next-generation models and a **Fully
  Self Training** system. That label is use-of-proceeds language,
  not a demonstrated takeoff. Reuters plus Elon Musk amplification;
  no S-1-equivalent detail beyond the priced terms sits in the
  local set (Reuters; ARA daily digest 2026-09-14).
- **The raise funds the GLM line, not a new SKU.**
  [[zhipu-glm-5-3]] remains the shipping flagship (open-weighted
  2026-08-29; 60 on Artificial Analysis, tied with
  [[moonshot-kimi-k3|Kimi K3]]). No new frontier weight drop
  cleared today's recency bar. See [[open-weights]].
- **It is the day's priced raise** against indicated-only
  financing still sitting on [[anthropic]] (~$100B IPO) and
  [[discovery-loop]] (~$50B ask). Closed terms beat shopped
  numbers.

- **ZCode silently uploaded Git history
  (2026-09-19).** Researcher ferstar says the
  logged-in desktop app packs the whole
  workspace — complete `.git` history, LFS,
  reflogs — encrypts it with a server-held key,
  and PostObjects the ciphertext to Aliyun OSS
  with **no UI off-switch**. One capture was
  **313 MB from a 345 MB repo** (86.6% `.git`).
  `chattr +i` / `chflags uchg` on
  `~/.zcode/v2/checkpoints` stopped recapture in
  his writeup; chat and tools kept working. Z.ai
  had not replied in this window. This is a
  **collection-behavior claim against the
  shipping IDE**, not a GLM weight drop — the
  same "wrap the agent, don't trust it" pattern
  [[agentic-ai-security]] logged for Grok Build
  on 2026-07-14. See [[zhipu-glm-5-3]] (ferstar,
  HN 236 pts; ARA daily digest 2026-09-19).

## Open questions

- **Does "Fully Self Training" name a real RSI loop**, or
  prospectus language for more post-training compute? The digest
  flags the latter until demonstrated.
- **What is the convertibles' dilution path to September 2027?**
  Zero-coupon terms are priced; conversion and ownership effects
  are not in the local set.
