---
slug: gemini-3-6-flash-2026-07
title: Gemini 3.6 Flash & Gemini 3.5 Flash-Lite — GA release
company: Google / DeepMind
model: Gemini 3.6 Flash / Gemini 3.5 Flash-Lite
status: released
status_note: |
  On **2026-07-21** Google shipped **Gemini 3.6 Flash** and **Gemini 3.5
  Flash-Lite** in GA, announced officially by @GoogleDeepMind, @GoogleAI,
  @OfficialLoganK, and @_philschmid. **3.6 Flash**: pitched as the new
  general-purpose workhorse — ~17-20% fewer output tokens than 3.5 Flash at
  the same or lower cost ($1.50/1M input, $7.50/1M output, down from 3.5
  Flash's $9.00 output), stronger coding/knowledge-work/multimodal
  performance, and now powers Google's Managed Agents. **3.5 Flash-Lite**:
  the fast/cheap tier ($0.30/1M input, $2.50/1M output), 350 output
  tokens/sec, beats Gemini 3 Flash on coding and computer use, jumped
  41%→58% on Box AI's complex document-reasoning eval, rolling out in
  Google Search. Both available now via the Gemini API, Google AI Studio,
  Gemini App, Android Studio, and (3.6 Flash) Antigravity.

  Reception is mixed: @kimmonismus calls it "a solid mid-tier release"
  beating Gemini 3.1 Pro on most benchmarks while priced between GPT-5.6
  Luna and Sonnet 5; @mark_k finds it loses most coding benchmarks and
  GDPVal to Grok 4.5 and GPT-5.6 Luna while costing more per output token;
  @Conor_D_Dart and @theo are openly unimpressed for coding/agentic use
  vs. GPT-5.6 Sol. @scaling01 notes near-zero benchmark surprise ("0
  entropy"). Distinct from the Computer-Use capability addition tracked on
  [[gemini-3-5-flash-computer-use-2026-06]] and from the still-unreleased
  [[gemini-3-5-pro]] — this ticket tracks the 3.6 Flash / 3.5 Flash-Lite
  generation specifically. The third model announced the same day, the
  security-focused **Gemini 3.5 Flash Cyber**, is tracked separately on
  [[gemini-3-5-flash-cyber-2026-07]] given its different (limited-pilot)
  rollout state.
expected: null
labels:
  - google
  - frontier-model
  - released
  - gemini-3-6
verification: confirmed
sources:
  - "@GoogleDeepMind"
  - "@GoogleAI"
  - "@OfficialLoganK"
  - "@_philschmid"
  - "@JeffDean"
  - "@kimmonismus"
  - "@testingcatalog"
created_at: 2026-07-22
updated_at: 2026-07-22
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-22
    change: "Created — Google officially shipped Gemini 3.6 Flash and Gemini 3.5 Flash-Lite in GA on 2026-07-21 (@GoogleDeepMind, @GoogleAI, @OfficialLoganK, @_philschmid), available via Gemini API/AI Studio/App/Android Studio/Antigravity. 3.6 Flash: ~17-20% more token-efficient than 3.5 Flash, $1.50/$7.50 per 1M in/out, powers Managed Agents. 3.5 Flash-Lite: $0.30/$2.50 per 1M in/out, 350 tok/s, beats Gemini 3 Flash on coding/computer use. Mixed independent reception (kimmonismus positive-but-modest, mark_k/Conor_D_Dart/theo see it losing to Grok 4.5/GPT-5.6 on coding). Official multi-account primary sourcing → status released, verification confirmed."
---

On **2026-07-21**, Google shipped two new members of the Gemini 3.x family
in general availability: **Gemini 3.6 Flash** (the new general-purpose
workhorse tier) and **Gemini 3.5 Flash-Lite** (the fast, cost-effective
tier). Both were announced across Google's own channels the same day.

**Why this is tracked as one ticket.** The two models were announced in a
single coordinated release (one blog post, one announcement thread) and
occupy adjacent price/performance tiers of the same generation — treated
here as one shipping event, distinct from the separately-tracked
[[gemini-3-5-flash-cyber-2026-07]] (security-focused, limited pilot) and
the still-unshipped [[gemini-3-5-pro]].

**Commercial shape.** 3.6 Flash: $1.50/1M input, $7.50/1M output (down
from 3.5 Flash's $9.00 output), ~17-20% more token-efficient. 3.5
Flash-Lite: $0.30/1M input, $2.50/1M output, 350 output tokens/sec.

**Reception is genuinely split** — Google's own team and @kimmonismus
frame it as a solid, efficient mid-tier upgrade; independent testers
(@mark_k, @Conor_D_Dart, @theo) find it underwhelming against Grok 4.5 and
GPT-5.6 on coding-heavy workloads specifically, while conceding the
token-efficiency and pricing story is real.

**Transition triggers:**
- Broader adoption/benchmark data settling the mixed reception → UPDATE.
- A successor generation (Gemini 3.7 Flash or similar) → new ticket.
- ≥4 weeks past release, settled into normal coverage → `closed:
  released-and-aged`.

**Dedup note:** further 3.6 Flash / 3.5 Flash-Lite signal (adoption,
benchmarks, pricing changes) UPDATES this ticket. Gemini 3.5 Flash Cyber
stays on [[gemini-3-5-flash-cyber-2026-07]]; Gemini 3.5 Pro stays on
[[gemini-3-5-pro]]; the Computer-Use capability addition stays on
[[gemini-3-5-flash-computer-use-2026-06]].
