---
slug: zhipu-glm-5-2
title: Zhipu GLM-5.2
type: entity
aliases: ["Zhipu GLM 5.2", "Zhipu GLM-5.2", "GLM 5.2", "GLM-5.2", "Z.ai GLM-5.2"]
tags: [open-weights, china, coding, long-context, frontier-model]
description: Zhipu AI / Z.ai flagship model shipped under an MIT license with 1M context and two reasoning-effort levels; the marquee long-context Chinese open-weight release in the Fable 5 shutdown window — and, late June, the subject of a debunked "matches Mythos" cybersecurity headline.
created_at: 2026-06-17
timestamp: 2026-07-05T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-07-05", path: research/digest/2026-07-05-digest.md}
  - {title: "ARA daily digest 2026-07-02", path: research/digest/2026-07-02-digest.md}
  - {title: "ARA daily digest 2026-06-29", path: research/digest/2026-06-29-digest.md}
  - {title: "ARA daily digest 2026-06-23", path: research/digest/2026-06-23-digest.md}
  - {title: "ARA daily digest 2026-06-21", path: research/digest/2026-06-21-digest.md}
  - {title: "ARA daily digest 2026-06-20", path: research/digest/2026-06-20-digest.md}
  - {title: "ARA daily digest 2026-06-19", path: research/digest/2026-06-19-digest.md}
  - {title: "ARA daily digest 2026-06-18", path: research/digest/2026-06-18-digest.md}
  - {title: "ARA daily digest 2026-06-17", path: research/digest/2026-06-17-digest.md}
  - {title: "ARA model ticket — Zhipu GLM-5.2", path: research/models/tickets/zhipu-glm-5-2.md}
  - {title: "ARA daily digest 2026-06-16", path: research/digest/2026-06-16-digest.md}
  - {title: "ARA daily digest 2026-06-15", path: research/digest/2026-06-15-digest.md}
  - {title: "ARA daily digest 2026-06-14", path: research/digest/2026-06-14-digest.md}
---

Zhipu GLM-5.2 is the cycle's marquee Chinese open-weight flagship. Per the
ARA model ticket, it is already deployed in the GLM Coding Plan, with API access
and **MIT-licensed open weights** promised within about a week of the
2026-06-15 launch announcement. Reported specs include **1M-token context** and
max/high "thinking" modes.

## Why it matters

- **Long-context flagship for the open-weights wave.** GLM-5.2 gives the
  [[open-weights]] page a concrete long-context anchor: usable now in a coding
  plan, MIT weights promised, 1M context, and reported early community coding
  tests ranking it above Qwen 3.6 27B. It belongs beside [[minimax-m3]],
  [[moonshot-kimi-k2-7-code]], [[gemma-4]], and [[deepseek]] in the open-model
  pressure stack.
- **It filled the Fable 5 vacuum.** As [[claude-fable-5|Fable 5 / Mythos 5]]
  stayed dark under the US export-control order, GLM-5.2 became one of the
  examples used to argue that closed-frontier shutdowns accelerate the very
  open-weight commoditization they are supposed to slow.
- **The verification status is intentionally conservative.** The ticket is
  `released` because the model is usable in the GLM Coding Plan, but
  `verification: partial` because ARA had not captured a primary Zhipu model
  card and the MIT weights were still described as forthcoming.

- **Shipped under MIT (2026-06-17).** GLM-5.2 went out **under an MIT
  license** — **1M context**, **two reasoning-effort levels (max/high)**,
  **priced the same as GLM-5.1**, framed as "frontier intelligence" — with
  **day-0 vLLM v0.23.0 support** plus live **Notion** and **Baseten**
  availability within hours. Z.ai claims it "leads GLM-5.1 by a wide margin"
  and **46.2% on DeepSWE**; a community "62 vs [[claude-opus-4-8|Opus 4.8]]'s
  69 on SWE-Bench Pro" comparison is circulating but unverified, and neutral
  third-party SWE-bench/LiveCodeBench placement has not yet landed. The MIT
  ship converts the earlier "weights promised" status into a concrete
  open-weights anchor in the [[claude-fable-5|Fable 5]] shutdown window — see
  [[open-weights]] (ARA digest 2026-06-17).

- **Tops the Artificial Analysis Intelligence Index; ~1pt off Opus 4.8 on
  FrontierSWE (2026-06-18).** GLM-5.2 climbed to **#1 on the Artificial Analysis
  Intelligence Index** — the first time an MIT-licensed open weight has led that
  composite — under a "Built for Long-Horizon Tasks" framing, and The Decoder
  reported it **trails [[claude-opus-4-8|Claude Opus 4.8]] by just ~1 point on
  FrontierSWE**, the tightest neutral-eval gap an open model has posted against
  the frontier this cycle. It was the **#1 story on Hacker News (689 pts, 354
  comments)** — a referendum on Chinese open models catching the closed labs.
  Z.ai also shipped a **"ZCode" desktop coding agent** built around the model.
  Practical caveat (@antirez): GLM-5.2 is **~2× the raw weight size of
  [[deepseek|DeepSeek V4 PRO]]**, so local inference likely needs **~512GB RAM** —
  the efficiency frontier [[xiaomi-mimo-v2-5-pro|MiMo]] is chasing matters here.
  See [[open-weights]] (ARA digest 2026-06-18).

- **Tops Artificial Analysis' open-weights board; Willison's endorsement
  (2026-06-19).** Reported at **753B params, 1M-token context, MIT-licensed**,
  GLM-5.2 **topped Artificial Analysis' open-weights leaderboard**, with **Simon
  Willison** calling it "**probably the most powerful text-only open-weights
  LLM**" — a credentialed third-party read that hardens the day-prior
  intelligence-index milestone. It is the anchor of the day's "China is closing
  the gap" discourse while [[claude-fable-5|Fable 5 / Mythos 5]] stays embargoed;
  **Elon Musk pegs Chinese "Fable-class" models at ~Q1 2027**. See
  [[open-weights]] (ARA digest 2026-06-19).

- **The migration focal point as Anthropic's models stay gated (2026-06-20).** With
  [[claude-fable-5|Fable 5 / Mythos 5]] still embargoed, developers are visibly
  migrating and **GLM-5.2 is the focal point** — praised as the best open model
  "**aside from Fable 5**" and rated "**[[claude-opus-4-8|Opus 4.6]] / GPT-5.4 tier**."
  Benchmarks still show closed frontier ahead (Fable 5 #1 on DeepSWE ~70%), so this
  reads as a **real-but-soft substitution trend**, not a confirmed share shift — see
  [[open-weights]] (ARA digest 2026-06-20).

- **The moat thesis gets its first leaderboard teeth (2026-06-21).** GLM-5.2 drew
  multi-practitioner raves (**Jeremy Howard**, ~7K likes) and took **#1 on Design
  Arena's single-turn HTML web-design board, beating a frozen [[claude-fable-5|Fable
  5]]** — the first neutral-ish scoreboard backing the practitioner praise. It also
  anchored the day's loudest open-vs-closed debate: an independent benchmark claim
  that **GPT-5.5 hallucinates ~3× more than MIT-licensed GLM-5.2** topped Hacker News
  (467 pts / 232 comments). Reported model details firmed: a **Terminal-Bench 2.1
  jump 63.5 → 81.0**, 1M-token context, and an **anti-reward-hacking RL module**.
  The day's defection — developer **@burkov** "already cancelled my Anthropic
  subscription… No moat isn't hypothetical anymore" after three days on GLM-5.2 with
  OpenCode — crystallized public subscription-cancellation churn (caveat: he keeps
  Codex because GLM "cannot see"). **Caveats hold:** design-only board, no vision,
  and senior devs note self-hosting still doesn't pencil out vs. a $200 Codex plan —
  see [[open-weights]] (ARA digest 2026-06-21).

- **Hardened from thinkpiece into multi-board data (2026-06-23).** GLM-5.2's
  agentic credentials firmed across several neutral boards in one cycle: a **#3
  overall / #1 open-weights placement on GDPval-AA** (**1524 Elo**, level with
  GPT-5.5 xhigh and the top open-weights model by a wide margin), a **2nd-place Game
  Dev Arena** ranking (Elo 1368, inside [[claude-fable-5|Fable 5]]'s band), a **#1
  open-weights score on Artificial Analysis's Intelligence Index (51)**, and it
  became the **first open-weights model to run alphaXiv's autoresearch pipeline
  end-to-end**. A widely-shared independent benchmark claim that GLM-5.2 beats
  GPT-5.5 on multiple long-horizon coding tasks "for 1/6th the cost" anchored the
  day's open-vs-closed discourse (@AndrewCurran_ Quote of the Day). It is now the
  leading **"DeepSeek moment for agents"** candidate. **Caveat:** it still lacks
  image understanding — see [[open-weights]] (ARA digest 2026-06-23).

- **The "matches Mythos" cybersecurity headline is debunked (2026-06-29).** A viral
  weekend claim that GLM-5.2 "matches [[claude-fable-5|Claude Mythos]]" on security
  bug detection was **corrected as a category error**. The real result (Semgrep's
  own blog): **~39% F1 on the narrow Semgrep IDOR benchmark at $0.17/task, beating
  Claude Code's ~32%** — prompt-only vulnerability detection, **not** Mythos-class
  autonomous exploit-chain capability. @janekm: "not vs Mythos but vs Opus, not in
  the same harness, and only for IDOR. Terrible methodology." A separate Chinese
  effort — **360 Security's "Tulongfeng"** (3,432 vulnerabilities flagged, per
  founder Zhou Hongyi) — is the more direct Mythos analog, and remains unverified.
  Zhipu's stock nonetheless **jumped ~30% on the Hong Kong exchange** on the
  headline — a market move decoupled from what the benchmark actually showed, and a
  reminder that the model's narrative momentum now outruns its verified capability
  (ARA digest 2026-06-29).

- **ZCode 3.0 ships as a GLM-5.2 agentic harness; #1 open-source on LMArena Code
  (2026-07-02).** Z.ai shipped **ZCode 3.0** — an **agentic coding harness/IDE
  optimized for GLM-5.2** — extending the earlier "ZCode" desktop agent into a full
  plan→code→review→deploy loop with a **`/goal` long-horizon feature**, **SSH remote
  dev**, and mobile control via WeChat/Feishu/Telegram. It lands the "harness, not just
  the model" thesis directly on top of GLM-5.2, and reignited a **200+ comment HN
  debate** on Chinese labs chasing the coding-agent workflow. On the leaderboard,
  GLM-5.2 now sits **#1 open-source / #2 global on LMArena Code**, behind only
  [[claude-fable-5|Fable 5]] (freshly back from its export ban) — the tightest the
  open-weights gap has been on a neutral coding board this cycle. See [[open-weights]]
  (ARA digest 2026-07-02).

- **A wafer.ai cost-per-token benchmark, and another unverified "matches
  Mythos" claim (2026-07-05).** An HN-featured wafer.ai benchmark on AMD
  hardware shows GLM-5.2 improving cost-per-token performance, feeding the
  ongoing local-inference-economics debate. Separately on Twitter, a
  single-source claim says GLM-5.2 matches [[claude-fable-5|Claude Mythos]]
  on vulnerability-hunting benchmarks — notable given Mythos's US-government
  export restriction was justified by that exact capability, but unverified
  by any independent benchmark. This is the same "matches Mythos" pattern
  debunked on 2026-06-29 above; treat with the same skepticism until a
  neutral third party replicates it (ARA digest 2026-07-05).

## Open questions

- **Weights actually landing.** The decisive transition is public MIT weights
  plus a primary model card. Until then, the open-weight claim is directionally
  important but not complete.
- **Neutral evals.** Does GLM-5.2 hold up on contamination-aware coding,
  long-context, and agentic tasks, or is the current signal mostly community
  excitement and vendor-adjacent benchmarking?
- **Router adoption.** If GLM-5.2 becomes a default open coding backend, does it
  show up in [[openrouter]] traffic mix and price discovery, or stay inside
  Z.ai's own product surface?
