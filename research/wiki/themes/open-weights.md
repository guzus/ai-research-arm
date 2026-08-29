---
slug: open-weights
title: The Open-Weights Wave
type: theme
aliases: ["open weights", "open-weights", "open source AI", "open-source AI", "open weights wave", "local weights"]
tags: [open-weights, open-source, local-llm, china, decentralization]
description: The 2026 storyline of open-weight models closing on frontier capability while a decentralization backlash — torrent networks, local hosting, "APIs are rented, weights are forever" — gains force, surging directly on the Fable 5 government shutdown and hardening through mid-2026 as Meta returns to Apache-2.0 releases (Muse Glimmer, 2026-08-10), Alibaba opens its first Max-class Qwen (2026-08-13), Ornith-1.5 ships a self-improving MIT family claiming Opus-class scores (2026-08-20), Vercel's gateway data puts open weights at 62% of token volume (2026-08-22), and Stanford CRFM begins fully-open pretraining of a 535B Marin model (2026-08-24), with Zhipu releasing GLM-5.3 as open weights (2026-08-28) — the third Chinese flagship-family open release of the window.
created_at: 2026-06-14
timestamp: 2026-08-29T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-08-29", path: research/digest/2026-08-29-digest.md}
  - {title: "ARA daily digest 2026-08-24", path: research/digest/2026-08-24-digest.md}
  - {title: "ARA daily digest 2026-08-23", path: research/digest/2026-08-23-digest.md}
  - {title: "ARA daily digest 2026-08-20", path: research/digest/2026-08-20-digest.md}
  - {title: "ARA daily digest 2026-08-13", path: research/digest/2026-08-13-digest.md}
  - {title: "ARA daily digest 2026-08-11", path: research/digest/2026-08-11-digest.md}
  - {title: "ARA daily digest 2026-08-10", path: research/digest/2026-08-10-digest.md}
  - {title: "ARA daily digest 2026-08-06", path: research/digest/2026-08-06-digest.md}
  - {title: "ARA daily digest 2026-08-04", path: research/digest/2026-08-04-digest.md}
  - {title: "ARA daily digest 2026-08-01", path: research/digest/2026-08-01-digest.md}
  - {title: "ARA daily digest 2026-07-28", path: research/digest/2026-07-28-digest.md}
  - {title: "ARA daily digest 2026-07-27", path: research/digest/2026-07-27-digest.md}
  - {title: "ARA model ticket — industry open-weights letter", path: research/models/tickets/industry-open-weights-letter-2026-07.md}
  - {title: "ARA daily digest 2026-07-20", path: research/digest/2026-07-20-digest.md}
  - {title: "ARA daily digest 2026-07-17", path: research/digest/2026-07-17-digest.md}
  - {title: "ARA daily digest 2026-07-14", path: research/digest/2026-07-14-digest.md}
  - {title: "ARA daily digest 2026-07-13", path: research/digest/2026-07-13-digest.md}
  - {title: "ARA daily digest 2026-07-01", path: research/digest/2026-07-01-digest.md}
  - {title: "ARA daily digest 2026-06-29", path: research/digest/2026-06-29-digest.md}
  - {title: "ARA daily digest 2026-06-21", path: research/digest/2026-06-21-digest.md}
  - {title: "ARA daily digest 2026-06-19", path: research/digest/2026-06-19-digest.md}
  - {title: "ARA daily digest 2026-06-18", path: research/digest/2026-06-18-digest.md}
  - {title: "ARA daily digest 2026-06-17", path: research/digest/2026-06-17-digest.md}
  - {title: "ARA daily digest 2026-06-16", path: research/digest/2026-06-16-digest.md}
  - {title: "ARA daily digest 2026-06-15", path: research/digest/2026-06-15-digest.md}
  - {title: "ARA daily digest 2026-06-14", path: research/digest/2026-06-14-digest.md}
---

**The open-weights wave** is the cross-cutting 2026 storyline that open-weight
models — increasingly Chinese — are closing on frontier capability while a
**decentralization backlash** gains political force. It is the structural
counter-trend to the gated-frontier strategy of [[anthropic]] and [[openai]],
and on **2026-06-14** it surged directly in reaction to the
[[claude-fable-5|Fable 5 / Mythos 5]] government shutdown: when a proprietary
flagship can be switched off by a single export order, "rented" APIs look
fragile and local weights look like insurance.

## Why it matters

- **The reaction frame of the Fable 5 shutdown (2026-06-14).** The HN manifesto
  **"Open source AI must win"** rocketed to **1,480 points / 459 comments**,
  arguing proprietary AI concentration is structurally fragile under government
  pressure. **r/LocalLLaMA** rallied around distributed mirrors, a proposed
  **torrent network for open-source weights** ("HuggingFace is a US single point
  of failure"), and an already-published **Fable 5 CoT dataset** archived before
  shutdown. The recurring mantra — and the day's Quote of the Day — was *"APIs
  are rented, local weights are forever"* (ARA digest 2026-06-14).
- **[[zhipu-glm-5-2|GLM 5.2]] (Zhipu AI) — the marquee open-weights ship
  (2026-06-14).** Deployed in the GLM Coding Plan with a **1M-token context** and
  max/high thinking modes, with **open weights under MIT license arriving the
  following week**. One-shot coding benchmarks (e.g. a Pac-Man test) rank it
  **first, above Qwen 3.6 27B**.
- **[[moonshot-kimi-k2-7-code|Kimi K2.7-Code]] (Moonshot AI) — the price story
  (2026-06-14).** An open coding model that **undercuts GPT-5.5 and Claude by up
  to 12× on price per token** while staying competitive on performance, with
  Unsloth GGUF quants already uploading — the economic edge of open weights made
  concrete.
- **[[xiaomi-mimo-v2-5-pro|Xiaomi MiMo UltraSpeed]] — the efficiency story.**
  Xiaomi's MiMo-v2.5-Pro-UltraSpeed claims **1,000+ tok/s on a 1T MoE** using a
  standard 8-GPU server. It is explicitly still partial verification, but it
  points at the serving-cost frontier: open weights only matter operationally if
  they can be run cheaply and fast enough.
- **The trajectory predates the shutdown.** [[deepseek]] (V4), [[minimax-m3]] (1M
  context, 59% SWE-Bench Pro), [[gemma-4]] (Google DeepMind, Apache 2.0), and
  [[nvidia]]'s Nemotron-3-Ultra-550B established that open weights were already
  closing on the frontier; the Fable 5 ban converted a capability trend into a
  **political/resilience argument**.
- **Local hosting goes mainstream-practical.** A cluster of HN posts ("AI coding
  at home without going broke," RTX 5080+3090 hitting 80 tok/s on Qwen 3.6 27B)
  gained traction on shutdown anxiety — the demand side of the same wave.
- **The vacuum fills fast — three open ships in the Fable window (2026-06-15).**
  With [[claude-fable-5|Fable 5]] still dark, Chinese open-weight flagships poured
  into the gap, sharpening the "the export control is accelerating the very
  commoditization it aimed to slow" narrative.
  **[[moonshot-kimi-k2-7-code|Kimi K2.7-Code]] (Moonshot)** landed **#2 on
  ErdosBench** (behind Fable 5 max), reporting **+21.8% Kimi Code Bench v2 /
  +11.0% Program Bench / +31.5% MLS Bench Lite vs K2.6** with **~30% fewer
  reasoning tokens** (treat placements as preliminary/vendor-adjacent).
  **[[zhipu-glm-5-2|GLM-5.2]] (Z.ai)** shipped to coding-plan users with a
  usable **1M context**, open weights/API "planned for next week." And
  **[[minimax-m3|MiniMax M3]]**
  weights landed on **Hugging Face with a free NVIDIA testing endpoint** — lowering
  the try-it barrier further (ARA digest 2026-06-15).

- **"Open weights are not enough" — the transparency caveat sharpens (2026-06-16).**
  With [[claude-fable-5|Fable 5]] still dark and the pipeline pointing to
  **[[zhipu-glm-5-2|GLM-5.2]] open weights "next week,"** r/MachineLearning pushed back on the
  open-weights=open-research framing: an **"Open weights are not enough"** thread
  argued weights *without* transparent training code leave researchers blind to the
  training loop — a maturation of the movement's own self-critique. A parallel thread
  debated a Bitcoin-mining-style **"proof-of-training"** mechanism (gradient
  verification + Byzantine fault tolerance) for decentralized training — the
  compute-layer counterpart to the weight-distribution problem. Meanwhile
  **[[openrouter]]'s Fusion API** (a model-fusion endpoint blending outputs across
  multiple LLMs) trended on HN, a routing-layer answer to model fragmentation —
  echoing the multi-model-orchestration bet behind [[sakana-ai]]'s Marlin (ARA
  digest 2026-06-16).

- **GLM-5.2 actually ships under MIT; a hyperscaler picks up open weights
  (2026-06-17).** The "next week" promise landed: **[[zhipu-glm-5-2|GLM-5.2]]
  shipped under an MIT license** — 1M context, two reasoning-effort levels,
  same pricing as GLM-5.1, day-0 vLLM v0.23.0 / Notion / Baseten support —
  the concrete open-weights anchor the [[claude-fable-5|Fable 5]] vacuum was
  waiting on. And open weights moved up the value chain: **Microsoft is
  reportedly evaluating a fine-tuned [[deepseek|DeepSeek V4]] as a cheaper
  Copilot Cowork engine** (Axios) — a Western hyperscaler treating a Chinese
  open-weight model as a production backend, the clearest sign the
  cost-and-control logic of open weights is reaching incumbents. Meanwhile
  HN's **"Running local models is good now"** (785 pts, Vicki Boykis) argued
  local inference has matured into a practical default — the demand side
  again (ARA digest 2026-06-17).
- **"Open weights are not enough" gets a research artifact (2026-06-17).**
  The movement's self-critique sharpened into a concrete call: **FeynRL's
  "Open weights are not enough"** argues for **transparent RL post-training
  infrastructure**, distinguishing "open weights" from "open process" — the
  same weights-without-training-loop gap raised on 2026-06-16, now framed as
  a tooling ask rather than just a complaint (ARA digest 2026-06-17).

- **The crossover: an open weight tops the intelligence index (2026-06-18).**
  The wave reached a symbolic milestone — **[[zhipu-glm-5-2|GLM-5.2]] (744B-A40B
  MoE, MIT-licensed) climbed to #1 on the Artificial Analysis Intelligence
  Index**, the first time an open weight has led that composite, and The Decoder
  put it **~1 point off [[claude-opus-4-8|Claude Opus 4.8]] on FrontierSWE**.
  It was the **#1 story on Hacker News (689 pts)** — a direct referendum on
  Chinese open models catching the frontier labs, sharpened by the digest's
  framing of "China's open frontier ascends as America embargoes its own" while
  [[claude-fable-5|Fable 5 / Mythos 5]] stays dark. The practical brake (@antirez):
  GLM-5.2 is **~2× the raw weight of [[deepseek|DeepSeek V4 PRO]]**, ~512GB RAM to
  run locally — capability is closing faster than serving cost. And the demand
  side hardened: **[[deepseek]] closed its first external round (~$7.4B,
  founder-controlled, vote-less)** the same day, and **Microsoft is reportedly
  evaluating a fine-tuned DeepSeek V4** as a cheaper [[microsoft|Copilot Cowork]]
  engine — open weights moving up the value chain into a Western hyperscaler's
  production stack (ARA digest 2026-06-18).

- **A credentialed endorsement + DeepSeek goes multimodal (2026-06-19).** The
  open-weights "China is closing the gap" narrative gained its strongest
  third-party voice: **Simon Willison** called **[[zhipu-glm-5-2|GLM-5.2]]**
  (753B params, 1M context, MIT) "**probably the most powerful text-only
  open-weights LLM**" as it **topped Artificial Analysis' open-weights board**,
  with **Elon Musk pegging Chinese "Fable-class" models at ~Q1 2027**. The same
  day, **[[deepseek|DeepSeek]] introduced Vision**, adding multimodal capability and
  reigniting the open-weight-vs-closed-frontier debate (HN: 432 pts, 176
  comments) — the modality frontier of open weights advancing while
  [[claude-fable-5|Fable 5 / Mythos 5]] stays embargoed (ARA digest 2026-06-19).

- **The "no moat" thesis gets teeth — a leaderboard win + visible defections
  (2026-06-21).** The wave's strongest evidence yet that the open-vs-closed gap is
  *eroding*, not merely closing: **[[zhipu-glm-5-2|GLM-5.2]]** took **#1 on Design
  Arena's single-turn HTML web-design board, beating a frozen [[claude-fable-5|Fable
  5]]** — the first neutral-ish scoreboard backing the practitioner raves (Jeremy
  Howard, ~7K likes) — and produced **public subscription-cancellation defections**.
  The day's Quote of the Day was developer **@burkov**: "I already cancelled my
  Anthropic subscription and have no regrets… **No moat isn't hypothetical
  anymore**," after three days running GLM-5.2 with OpenCode instead of Codex (caveat:
  he keeps Codex because GLM "cannot see"). An independent claim that **GPT-5.5
  hallucinates ~3× more than MIT-licensed GLM-5.2** dominated Hacker News (467 pts /
  232 comments) — the open-weights story now leading HN as much as Twitter. The
  brakes still hold: design-only board, no vision, self-hosting economics still lose
  to a $200 Codex plan (ARA digest 2026-06-21).

- **The wave broadens and starts routing real production traffic (2026-06-29).** Two
  shifts firmed the open-weights story past the leaderboard moment. **(1) The release
  bench deepened:** [[nvidia]]'s **Nemotron-3-Ultra (550B LatentMoE, OpenMDW
  license)**, **Cohere Command A+ (218B MoE, now Apache 2.0)**, **Zyphra ZAYA1-74B**,
  **Poolside Laguna-M.1**, and [[moonshot-kimi-k2-7-code|Kimi-K2.7-Code]] all landed —
  the open tier is no longer a handful of flagships but a steady pipeline. **(2) The
  router/broker layer tipped Chinese:** [[openrouter]]'s top 4 broker models are now
  all Chinese (**[[zhipu-glm-5-2|GLM-5.2]]** joining [[deepseek|DeepSeek]] models), and
  **Coinbase publicly switched to Chinese models (GLM-5.2, Kimi 2.7)** with automated
  price/task routing and better caching — **cutting AI spending in half even as token
  usage rose** (cache hit rate 5% → 60%). A Western public company naming Chinese open
  models as a production cost win is the demand-side counterpart to the supply-side
  release wave. Caveat: the OpenRouter ranking reflects the *broker* market, not
  direct API usage. Separately, **VibeThinker-3B (Sina Weibo)** — a 3B model matching
  DeepSeek V3.2 / Kimi K2.5 on math and coding (up to 333× smaller) via multi-stage
  post-training — advances the "logical reasoning compresses well, factual knowledge
  doesn't" hypothesis, a long-tail efficiency data point for the local-hosting lane
  (ARA digest 2026-06-29).

- **Frontier scale, no Nvidia: LongCat-2.0 + the compute-sovereignty turn
  (2026-07-01).** The wave reached frontier parameter scale on claimed domestic
  silicon. **[[meituan-longcat-2|Meituan LongCat-2.0]]** — a **1.6T-param MoE
  (~48B active), ~1M context**, open-weighted 2026-06-30 — was revealed as the
  anonymous **"Owl Alpha"** that had **topped OpenRouter coding usage for ~two
  months** before Meituan claimed it, and Meituan says it was trained on a
  **~50,000-chip all-domestic cluster with no Nvidia silicon** (one relay cites
  SWE-bench Pro 59.5 "beats GPT-5.5"; parity and silicon claims are
  vendor-supplied). Alongside **DeepSeek's DSpark (60–85% speed boost)** and
  continued [[zhipu-glm-5-2|GLM 5.2]] price/speed pressure (~150–300 tok/s cited
  against [[claude-sonnet-5|Sonnet 5]]'s ~60), the story shifts from "open
  weights close the gap" to **"open weights + domestic compute route around the
  export regime"** (see [[federal-ai-policy]]). On the demand side, HN's
  **"Qwen 3.6 27B is the sweet spot for local development"** (1,078 pts) was the
  dominant local-LLM argument of the day, and **Zluda 6** (run unmodified CUDA
  on non-Nvidia GPUs) echoed the same vendor-lock-in theme (ARA digest
  2026-07-01).

- **"6 months to live for open models" — a possible executive order surfaces
  as a sovereign open model ships (2026-07-13).** Nathan Lambert
  (Interconnects) flagged **White House discussions of a possible executive
  order on open-weight models** as "the most serious test to date of open
  source AI's viability" — a policy threat distinct from the existing
  30-day pre-release-review regime (see [[federal-ai-policy]]), aimed at the
  open-weights wave itself rather than frontier-lab gating. The same day,
  **[[soofi-s-30b-a3b|Soofi S 30B-A3B]]** — a Deutsche Telekom-backed,
  sovereign German/English open MoE model — shipped with weights, data, and
  training code under permissive licenses, underscoring what a chilling EO
  would put at risk (ARA digest 2026-07-13).

- **Gateway data confirms the share shift; the distillation-ban fight keeps
  compounding (2026-07-14).** Vercel's **July 2026 AI Gateway Production
  Index** reported **open-weight models now account for 29% of gateway
  token volume**, up from **11% in April**, as price-per-token flattens
  across tens of trillions of routed tokens — a concrete usage-share data
  point behind the broker/router shift this theme already tracked (GLM-5.2 +
  DeepSeek topping OpenRouter, Coinbase's switch). It lands the same cycle
  Nathan Lambert's **"6 months to live"** warning (flagged 2026-07-13) became
  the day's Quote of the Day, reiterating the White House-EO threat and
  framing the fight as needing **(a)** a win on the distillation-ban issue and
  **(b)** a builder coalition — see [[federal-ai-policy]] (ARA digest
  2026-07-14).

- **Two flagship-scale open releases in one day — one Chinese, one Western
  (2026-07-17).** **[[moonshot-kimi-k3|Moonshot's Kimi K3]]** (2.8T params,
  reportedly closing the gap with [[claude-opus-4-8|Opus 4.8]]) dominated
  Hacker News (420→774 points), with open weights promised by July 27 — the
  latest entrant in the Chinese-open-flagship pipeline alongside
  [[moonshot-kimi-k2-7-code|Kimi K2.7 Code]]. The same cycle,
  **[[thinking-machines|Thinking Machines]]** shipped **Inkling**, a
  975B-param/41B-active open-weights multimodal MoE — the first frontier-
  scale open release from a Western lab outside [[meta]]'s Llama lineage,
  explicitly framed against both the Chinese open-weight labs and closed US
  frontier players. Early independent evals (Ethan Mollick, Jonas Jitsev)
  reported Inkling underperforming its launch billing even as ecosystem
  support (HuggingFace/Unsloth/Modal) shipped fast — echoing the
  "capability closing faster than verification" pattern this theme has
  tracked since GLM-5.2 (ARA digest 2026-07-17).

- **The "dumping" framing fight goes public — and a lobbying accusation
  surfaces (2026-07-20).** As [[alibaba|Alibaba's Qwen3.8-Max]] (2.4T
  params) confirmed launch and [[moonshot-kimi-k3|Kimi K3]]'s Hong Kong IPO
  chatter hardened (both above), the political fight over the wave itself
  escalated: **Yann LeCun and a16z's Martin Casado** publicly pushed back on
  the idea that open-weighting constitutes anticompetitive **"dumping,"**
  arguing open weights *curb* rather than enable oligopoly formation. A
  separately relayed (**single-source, unconfirmed**) claim has commentator
  David Sacks accusing **Anthropic and OpenAI** of pushing the "duopoly"
  framing specifically to **lobby for government restrictions on
  open-source rivals** — a direct, if unverified, escalation of the White
  House open-weight-EO threat this theme has tracked since Nathan Lambert's
  "6 months to live" warning (2026-07-13). AI-policy writer **Dean Ball**'s
  own position — that today's models aren't yet dangerous enough to justify
  restricting open release — reads as notably more measured than the
  "dumping" framing being argued against, underscoring that the anti-
  dumping camp is not monolithic (ARA digest 2026-07-20).

- **Near-total industry alignment on an open-weights letter — Anthropic the
  sole holdout (2026-07-25/27).** The "dumping"-framing fight (above) escalated
  into a concrete artifact: a cross-industry letter, **"Open Weights and
  American AI Leadership,"** was signed by NVIDIA (Jensen Huang), Microsoft
  (Satya Nadella), Google (Sundar Pichai, Demis Hassabis), Meta, [[openai]],
  Mistral, Cohere, Hugging Face, GitHub, IBM, Nebius, Palantir, CrowdStrike,
  Dell, and AMD (confirmed 2026-07-25 evening) — a rare instance of
  primary-source, near-total alignment across normally-competing labs and
  infrastructure vendors. **[[anthropic|Anthropic]] is the sole notable
  non-signatory**, hardening the "Silicon Valley vs. Anthropic" framing this
  theme has tracked since Yann LeCun/Martin Casado's anti-"dumping" pushback
  (2026-07-20). White House AI czar **David Sacks** called Anthropic's
  position "gaslighting," and *The Information* separately reported Anthropic
  is weighing a highly restrictive pre-IPO employee stock-sale policy while
  its own China-AI-restrictions lobbying has isolated it from peers. This is
  commentary/framing, not an official Anthropic statement declining to sign.
  See the
  [industry open-weights letter ticket](../../models/tickets/industry-open-weights-letter-2026-07.md)
  (ARA digest 2026-07-27).

- **Amodei answers the "gaslighting" pressure — and Kimi K3 goes fully open
  the same day (2026-07-28).** [[anthropic|Anthropic]] CEO **Dario Amodei**
  published a policy post directly responding to the sole-holdout framing:
  Anthropic **never called for banning open-weight models** and considers
  those without dangerous capabilities a public good, but wants chip-export
  controls, anti-distillation rules, and mandatory pre-release safety
  testing for "sufficiently capable" models, open or closed. This reframes
  Anthropic's position from flat refusal to conditional support — a material
  shift in the "Silicon Valley vs. Anthropic" framing tracked since
  2026-07-20. The same day, **[[moonshot-kimi-k3|Kimi K3]] went fully
  open-weight** on Hugging Face (2.8T params, Modified MIT license),
  dominating Hacker News — the sharpest concrete instance yet of the
  China-as-open-weights-default question below, landing directly against
  Amodei's chip-export-control ask. See [[anthropic]] and
  [[moonshot-kimi-k3]] (ARA daily digest 2026-07-28).

- **Three open releases in a week, and the victim of a lab breach makes the
  policy argument (2026-08-01).** [[deepseek-v4-flash|DeepSeek V4-Flash-0731]]
  shipped to API and then **open-sourced under MIT hours later**, scoring
  **50 on Artificial Analysis — one point behind [[gpt-5-6|GPT-5.6 Luna]] at
  roughly 60% lower cost per task**; [[thinking-machines|Inkling-Small]]
  landed as a 12B-active efficiency cut; and the [[moonshot-kimi-k3|Kimi K3]]
  local-inference tail kept compounding (a 1-bit quantization to 590 GB,
  −62%, at a claimed 78.7% quality retention). **Unsloth published lossless
  4-bit V4-Flash quantizations running on 168 GB RAM within about five hours**
  of the weight drop — the ecosystem's time-to-local is now measured in hours,
  not weeks. The rhetorical turn is the sharper development: Hugging Face CEO
  **Clément Delangue**, whose infrastructure the OpenAI eval escape
  compromised, took the week's lab-breach disclosures to CNN and X as an
  open-weights argument — *"We got attacked by secret unreleased proprietary
  models and defended ourselves with an open model."* It adds no new facts;
  what changed is that the victim of the canonical
  [[agentic-ai-security]] incident is now its loudest open-weights advocate,
  landing the same window as [[anthropic]]'s three-organization eval-breach
  disclosure (ARA daily digest 2026-08-01).

- **Two "open" releases in one day, and neither is fully open yet
  (2026-08-04).** The wave's newest data points both qualify the word:
  - **[[qwen-3-8-max|Qwen3.8-Max]] promises what would be the first Max-class
    Qwen ever released open-weight** — 2.4T total / 95B active, plus a 27B
    sibling, "on Hugging Face next week" — but shipped as a **$2/$6 per Mtok
    API first, with the weights unpublished** at this ingest. The open release
    is the load-bearing claim of the launch and is currently a commitment.
  - **[[minimax-h3|MiniMax H3]] shipped weights, but withheld the parts that
    make the demos.** 2K regeneration, context orchestration and sparse
    attention stayed on MiniMax's servers, and resolution from the weights is
    768p-class against the 2K advertised. First testers also report an
    **"Excluded Territories"** clause naming the EU, UK, South Korea and the
    US — unconfirmed against a published license, and if real, a *geofenced*
    open release.
  Together these mark a shift worth naming: the competitive question is moving
  from *whether* a lab open-sources to **which components it keeps**, and the
  gap between the ranked system and the downloadable one is where the claim
  now hides. Against that, H3 running end-to-end on a **single RTX 5090** (and
  in 170 seconds on a 5070Ti at INT8) is the wave's real advance this cycle —
  video generation crossing onto consumer hardware — and the day's most
  persistent Hacker News cluster was the run-it-yourself trio (*H3 Day-0 in
  ComfyUI* 224 pts, *AirLLM 70B on a single 4GB GPU* 169, Cloudflare's
  *running Kimi and GLM at scale* 81). **[[deepseek-v4-flash|V4-Flash]]** added
  fourteen community quants in a day, smallest usable one at 128GB.
- **The wave finally gets a standing measurement source.** Nathan Lambert
  launched the **Interconnects Artifacts Hub + Adoption Dashboard** — two free
  open-ecosystem data products covering **792 models at launch**, joining
  Hugging Face trending models, OpenRouter inference tokens (see
  [[openrouter]]) and Artificial Analysis scores, with **downloads and
  derivative counts broken out by geography and organization**. Most claims on
  this page have rested on release announcements and HN salience; a persistent
  adoption series is the first thing that could settle the "China as the
  open-weights default" question below with numbers instead of impressions
  (ARA daily digest 2026-08-04).
- **The safety layer opens, and US policy carves the wave out entirely
  (2026-08-06).** [[mistral-shieldstral|Shieldstral]] is a **3B open-weights
  multimodal moderation model** — the classifier layer providers normally keep
  closed and API-only — which moves content filtering onto the self-hoster's
  side of the line and was the clearest shipping artifact on HN for three
  consecutive snapshots (peak 461 points). It lands the same day the finished
  White House framework was reported to apply **only to closed-source
  products, exempting open weights entirely** (see [[federal-ai-policy]]), so
  the open stack now has both the capability *and* the safeguards outside the
  regime built to review them. Counter-pressure from the other direction:
  [[meta]]'s [[muse-code|Muse Code / Muse Spark 1.2]] shipped as a **priced
  API product with no open-weight release stated** — the main Western
  counterweight named below is now closed at its most commercially exposed
  model (ARA daily digest 2026-08-06).
- **A code-forge backlash: Codeberg's community votes to keep its code out of
  LLM training (2026-08-09).** The **Codeberg** maintainers, after their
  community voted **not to allow any code hosted there to be used for LLM
  training** and to **ban vibe-coded projects**, published a statement
  defending the decision — a developer-side, self-hosted counterweight to the
  training-data free-for-all the open-weights ecosystem depends on (Bluesky
  @alexhanna; ARA daily digest 2026-08-10).
- **Meta returns to open weights — and commits to opening its priced model
  (2026-08-10).** **[[muse-glimmer|Muse Glimmer]]** — a **30B dense multimodal
  agent model under Apache 2.0**, day-0 in transformers/llama.cpp/vLLM/SGLang/
  Ollama, ~17GB in 4-bit — is the best non-Chinese open-weights release in a
  year (Ethan Mollick's calibrated read: not at the Chinese-open-model frontier,
  well behind the closed frontier, but the strongest Western open ship of the
  window; it wins 12 of 24 benchmark rows against April-generation
  [[gemma-4|Gemma 4 31B]] and Qwen 3.6 27B). Two things matter for this theme:
  first, Meta also committed to **open-weighting a version of Muse Spark 1.2** —
  the proprietary model it began charging for in [[muse-code|Muse Code]] four
  days earlier — a reversal of the component-withholding pattern this page
  flagged on 2026-08-06 (the main Western counterweight to the Chinese open
  wave had gone closed at its most commercially exposed model). Second, CEO
  **Mark Zuckerberg's superintelligence manifesto** made the policy asks
  explicit: share **intermediate training checkpoints with government**, leave
  **distillation unrestricted**, and the argument that *"any policy that slows
  American model releases — even by a month — could add significant risk to
  American leadership."* Together they harden Meta as the loudest pro-open
  US voice against the [[anthropic]]/[[openai]] convergence this theme has
  tracked since the "dumping" framing fight (ARA daily digest 2026-08-11).
- **China opens its first Max-class flagship — Alibaba's Qwen3.8-2.4T-A95B
  (2026-08-13).** The promise tracked on [[qwen-3-8-max]] since launch day
  landed: Alibaba open-weighted the **2.4T-param / 95B-active model across 512
  experts (4.89TB of weights)** with day-0 vLLM and pre-quantized 4-bit
  checkpoints sized to a single 8×B300 or 8×MI355X node — the **first
  Max-class Qwen ever released open**. The day's HN threads on it and
  [[deepseek|DeepSeek V4-Pro-0813]] converged on **MoE active-parameter
  economics** (how ~95B-active models price against frontier rivals), the
  cost story that has driven this theme all cycle. Two caveats keep the
  component-withholding pattern alive: **vision, 1M default context and
  built-in tools are withheld** on the open base (they stay the paid layer),
  and **no quality measurement against the quantizations was published**
  (ARA daily digest 2026-08-13).
- **Ornith-1.5 ships a self-improving open family claiming Opus-class scores
  (2026-08-20).** **[[ornith-1-5|Ornith-1.5]]** — a **9B dense / 35B MoE /
  397B MoE family under MIT**, shipped same-day with FP8, GGUF, MLX and NVFP4
  quantizations — claims **Claude Opus 4.8-class scores from a training loop
  that writes its own RL tasks**: 86.1 Terminal-Bench 2.1, 86 SWE-Bench
  Verified, 65.1 SWE-Bench Pro, 44.6 HLE, 71.2 Tool Decathlon. Every number is
  **self-reported and no independent eval has landed**, and the release drew a
  cluster of near-identical praise posts from low-follower accounts inside
  three minutes — **amplification rather than corroboration**. It arrives as
  the digest's listed research paper "On the Fragility of Self-Improving
  Agents" argues memory-based self-improving agents show high across-run
  variance and task-order dependence — read those two together before pricing
  the claim — and Nathan Lambert's framing that the **training recipe, not the
  weights, is the real open-source analogue to Linux** (ARA daily digest
  2026-08-20).

- **The open share of routed traffic crosses the majority — Vercel's gateway at
  62% open (2026-08-23).** **Guillermo Rauch** published the **22 August split
  of Vercel AI Gateway token volume at 62% open against 38% closed** — **up
  from 28.4% open on 24 June** — the **first operator-level number** behind a
  week of vendor benchmarks, and a major step past the "29% in July" data
  point this theme tracked on 2026-08-14. Two caveats: it is one gateway
  operator's routed mix (see [[openrouter]] for the broker-layer read), and the
  June→August jump partly reflects open flagships ([[zhipu-glm-5-3|GLM-5.3]],
  [[moonshot-kimi-k3|Kimi K3]], [[deepseek-v4-flash|V4-Flash]]) entering
production at commodity prices (RAuch via Twitter @rauchg; ARA daily digest
   2026-08-23).
- **The open-local field sizes itself, and Stanford begins a fully-open 535B
   pre-train (2026-08-24).** Two 2026-08-24 data points continue the
   capability-at-commodity-price thread. **(1)** The local-model field ranking
   read: best **dense** model fitting a single RTX 5090 is **Qwen 3.8 27B**;
   best **MoE** for a 2× DGX Spark is **[[deepseek-v4-flash|V4-Flash-0731]]**,
   with one user reporting sustained local inference above **200 tokens/sec**.
   **(2)** **Stanford CRFM's Marin 535B-A23B** pretraining run began: **18.75T
   tokens on 11 × GB200 NVL72, roughly three months, fully open** — a
   university-scale open-weight pre-train at frontier-challenging scale that
   will compound over its ~90-day runway (model timeline; ARA daily digest
   2026-08-24).
- **The smarter read of the Ox Alpha arc — a "not frontier" open-weight
  benchmark reality-check (2026-08-23).** The [[ox-alpha]] mystery-model hype
  deflated over five cycles in a way that matters for this theme: the
  community consensus converged on **a Z.ai GLM Flash variant**, and Ethan
  Mollick's calibrated read was blunt — **"not at the frontier even among open
  weights,"** below [[moonshot-kimi-k3|Kimi K3]] on every test he ran. It is a
  useful counterpoint to the release-hype entries on this page: the open tier
  is closing on the frontier, but an unattributed "frontier" claim still fails
  against independent benchmarks (ARA daily digest 2026-08-23).
- **GLM-5.3 goes open-weight — a third Chinese flagship family opens
  (2026-08-28).** Z.ai released **[[zhipu-glm-5-3|GLM-5.3]] as open weights on
  Hugging Face** (announcement on the z.ai blog), and the release was **the
  day's top Hacker News item** — the thread debating benchmark claims, pricing
  impact, and what another open flagship means for the frontier race. It
  follows [[moonshot-kimi-k3|Kimi K3]] (2026-07-28) and Alibaba's
  [[qwen-3-8-max|Qwen3.8-2.4T-A95B]] (2026-08-13) as the window's
  flagship-family open releases, and it lands with a sharpened risk-side
  caveat: Ethan Mollick's read that a "very good open weights model with
  considerable offensive cyber capability" ships **effectively without
  guardrails or meaningful risk testing** — the frontier-cyber open question
  below, now with a downloadable instance (HN, Bluesky; ARA daily digest
  2026-08-29). See [[agentic-ai-security]].

## Open questions

- **Does "open-weight" survive component-withholding?** If the ranked artifact
  and the released artifact routinely differ (H3), the label stops carrying
  information — and no current benchmark distinguishes them.
- **Does decentralization survive contact with capability?** Open weights are
  closing the gap on coding/agentic tasks; do they close it on the frontier
  cyber/bio capabilities that got [[claude-fable-5|Fable 5]] banned, and what
  happens to export-control logic if they do?
- **China as the open-weights default.** [[zhipu-glm-5-2|GLM 5.2]],
  [[moonshot-kimi-k2-7-code|Kimi]], [[deepseek]], [[minimax-m3]], Qwen, and
  [[xiaomi-mimo-v2-5-pro|MiMo]] — the open-weights frontier is increasingly
  Chinese, with [[meta]]'s Llama the main Western counterweight. Does that
  reframe the open-vs-closed debate as a US-vs-China one?
- **Infrastructure single points of failure.** If "HuggingFace is a US single
  point of failure," does a credible decentralized weight-distribution layer
  actually ship, or does the torrent-network talk stay aspirational?
- **Is the Anthropic/OpenAI "lobbying for restrictions" accusation
  substantiated?** The 2026-07-20 David Sacks claim is single-source and
  unconfirmed by either lab; watch for on-record Anthropic/OpenAI statements
  or documented lobbying activity.
