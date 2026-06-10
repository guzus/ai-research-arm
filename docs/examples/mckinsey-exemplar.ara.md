---
eyebrow: PERSPECTIVE · AI INFRASTRUCTURE
title: The economics of an AI factory, 2026
deck: The cost of frontier compute is collapsing per token and exploding per cluster at the same time. The two curves are not in tension — they are the whole investment thesis. A McKinsey-style read of where the money actually clears.
domain: finance
lede: |
  In 2026 the AI buildout crossed a threshold that reframes every
  capital-allocation question around it: a single gigawatt-class training
  campus now costs on the order of forty billion dollars to stand up, while
  the price of serving a million tokens from a frontier model has fallen by
  roughly an order of magnitude in two years. Both facts are true, and the
  gap between them is where operators win or lose. This is the long version —
  the unit economics, the depreciation fight that nobody agrees on, and the
  one assumption every model in the market is quietly resting on.
stats:
  - {label: 1 GW campus capex, value: $40, unit: "B"}
  - {label: Annual TCO (5-yr life), value: $8.5, unit: "B"}
  - {label: Frontier $/M tokens, value: -90, unit: "% / 2yr"}
  - {label: Pilots with zero ROI, value: 95, unit: "%"}
---

## 01. The two curves

The thesis sentence: the cost of intelligence is falling fast on a
per-token basis and rising fast on a per-cluster basis, and an AI factory
is a bet that the first curve pulls enough demand to fill the second.

Per token, the deflation is real and steep. Independent trackers put the
fall in the price of frontier-quality inference at roughly an order of
magnitude over two years, driven by better accelerators, higher
utilization, and aggressive competition among inference vendors.[^1] Per
cluster, the inflation is just as real: a gigawatt-scale GB-class training
campus now carries an up-front cost near forty billion dollars, with total
cost of ownership around eight and a half billion dollars a year under a
five-year hardware life.[^2] The same technology that makes a token cheap
makes a cluster expensive, because the way you make tokens cheap is to buy
more silicon and run it hotter.

:::statement(attr="The 2026 compute thesis, in one line")
Cheap tokens and expensive clusters are the same fact seen from two ends.
The question is never which curve is real — it is whether demand arrives
fast enough to sit between them.
:::

The market has already split into two ways of expressing this. One owns
the *token* — model labs and inference platforms betting that volume
compounds faster than price erodes. The other owns the *megawatt* — the
operators, utilities, and memory makers who get paid whether or not any
single model wins. The rest of this article is about which side has the
legible unit economics.

## 02. Anatomy of the cost

Thesis: the cost of an AI factory is not dominated by the chips you read
about in headlines — it is dominated by the things around them, which is
why power and memory, not GPU logic, are the binding constraints.

Decompose a frontier accelerator and the intuition inverts. For a
Blackwell-class B200, high-bandwidth memory plus advanced packaging account
for roughly two-thirds of unit cost; the GPU logic die itself is the
minority of the bill of materials.[^3] Scale that to a campus and the same
pattern holds at the facility level: power delivery, cooling, and the
memory subsystem dominate, while the marginal logic transistor is
comparatively cheap. When the vendor's own marketing optimizes for "token
throughput per megawatt," megawatts — not GPU counts — are the scarce
input.[^4]

:::exhibit(num="Exhibit 1", title="Where the money goes in a frontier accelerator", subtitle="Share of B200-class unit cost, %", source="Epoch AI, B200 cost breakdown (2026)", note="Packaging includes CoWoS-class advanced packaging; shares are approximate and move with HBM spot pricing.")
:::donut(center-label="B200")
- {label: "HBM memory + packaging", value: 66}
- {label: "GPU logic die + other", value: 34}
:::
:::

That cost structure is why the cleanest way to own the buildout has been
the memory chokepoint. Every incremental accelerator shipped — into a
sovereign cloud, a hyperscaler, or a neocloud — mechanically pulls
high-bandwidth memory, and a single supplier is expected to provide about
two-thirds of next-generation HBM.[^3] The value capture there is direct
and quantified in a way a services bet rarely is.

:::exhibit(num="Exhibit 2", title="Annual total cost of ownership is a depreciation story", subtitle="$ billion per year for a 1 GW campus, by assumed hardware life", source="Epoch AI, AI data-center cost breakdown (2026)", note="TCO includes power, staff, and amortized capex. Shorter assumed life front-loads cost; the spread is the contested variable in §03.")
:::bar-chart(orientation=horizontal, value-unit=$, value-suffix=B)
categories: 3-year life, 5-year life, 7-year life
Annual TCO: 12.0, 8.5, 7.0
:::
:::

## 03. The depreciation fight

Thesis: the single most important number in AI-factory economics is one
nobody can agree on — how long a GPU stays economically useful — and the
honest answer in 2026 is still "it depends who is selling."

The sensitivity is not academic. Shorten the assumed hardware life from
five years to three and the annual cost of a gigawatt campus jumps from
about eight and a half billion to roughly twelve billion dollars — a
{bubble:+41%} move from one accounting assumption.[^2] Stretch it to seven
years and the same campus costs about seven billion a year. Nothing about
the physical machine changed; only the schedule did.

:::cols
The market cannot even agree with itself. Public neoclouds depreciate
near-identical accelerators over horizons that differ by years — one over
six, another over four — which mechanically changes reported margins for
the same hardware doing the same work.[^5] Prominent skeptics argue the
true economic life is closer to two or three years, given the annual
cadence of new accelerator generations that strand the old ones at the
frontier.[^5]

The bull rejoinder is equally coherent: a vendor's newest interconnect can
push appreciably more usable GPUs into the same power envelope, which
improves the tokens-per-dollar math and lets a landlord with a multi-year
demand backlog underwrite a long life honestly.[^4] But that argument
*requires* the backlog to exist — which is precisely the assumption §05
puts on trial. Until the life question settles, every discounted-cash-flow
model of an AI factory is really a bet on a number in a footnote.
:::

The practical consequence is a fork. Read GPU life as three years and the
merchant-cloud model is a value-destructive capex sink that needs near-
perfect utilization to clear. Read it as six or seven and the same asset is
a durable infrastructure annuity. Both readings are defensible from public
data today; the operators have disclosed neither their assumed life nor
their contracted utilization.[^6]

> A bare-metal GPU cloud has almost no margin of safety: returns flatline
> if utilization slips below the low-eighties or if rental prices dip.
> — SemiAnalysis, AI neocloud anatomy

## 04. Where the trade clears

Thesis: if you want the AI buildout with real unit economics rather than
narrative, you want the inputs that are sold out regardless of which model
wins — and the market has already figured this out.

The contrast is the article's core finding. A model-services bet is an
option on monetization: real, but unproven, and exposed to the same token
deflation that is the bull case. A memory-and-power bet is an oligopoly
input sold years forward at peak-of-industry margins. One is a story about
what *might* be monetized; the other is a price you can already read in the
income statement.

:::exhibit(num="Exhibit 3", title="Two ways to own the same macro view", subtitle="Qualitative profile of each expression of the AI-compute trade", source="ARA analysis", note="Stylized; not investment advice. 'Legibility' refers to how directly unit economics are observable from public disclosure.")
| Expression | Pays when | Margin visibility | Key risk |
|---|---|---|---|
| Own the token (labs / inference) | Volume outpaces price erosion | Low — bundled, pre-revenue | Token deflation, model churn |
| Own the megawatt (operators) | Capacity is contracted | Medium — utilization-driven | GPU depreciation, power cost |
| *Own the memory (HBM duopoly) | Any accelerator ships | High — sold forward | Cycle peak, share shift |
:::

The numbers behind the third row are the proof. The leading memory supplier
posted record results in early 2026 — a quarterly operating margin above
seventy percent, higher than the marquee accelerator and foundry names —
and told the market that customer demand for the next three years already
exceeds its capacity to supply.[^7] That is what a legible AI-compute
business looks like: a sold-out input, not a promised platform.

:::stats
- {label: HBM supplier op margin, value: 72, unit: "%"}
- {label: Demand visibility, value: 3, unit: "yr+"}
- {label: HBM share of B200 cost, value: 66, unit: "%"}
- {label: Frontier inference deflation, value: -90, unit: "% / 2yr"}
:::

Ranked by reported operating margin, the input layer of the stack sits
above the platforms it supplies — the inverse of where most attention, and
most equity-story premium, is directed.

:::exhibit(num="Exhibit 4", title="The input layer earns the fattest margin", subtitle="Most recent reported operating margin, %, selected AI-stack names", source="Company filings via CNBC (2026)", note="Margins are point-in-time and cyclical; the memory figure is a cycle-peak reading, not steady-state.")
:::rank-list
- {label: "HBM memory (duopoly)", value: "~72%", pct: 100, highlight: true}
- {label: "Lead accelerator vendor", value: "~62%", pct: 86}
- {label: "Leading foundry", value: "~59%", pct: 82}
- {label: "Merchant GPU cloud", value: "~25%", pct: 35}
:::
:::

## 05. The assumption under everything

Thesis: every AI-factory model rests on one demand assumption that is, so
far, more asserted than demonstrated — and the independent evidence on
whether compute converts to return is mixed at best.

The demand case is most loudly made by the company that sells the
accelerators, which has framed roughly a trillion dollars of cumulative
demand for its next two generations.[^8] A genuine secular argument can
coincide with self-interest — but a total addressable market sized by the
chip vendor is one to interrogate, not to underwrite.

The independent read is sobering. A widely cited study found that the large
majority of enterprise generative-AI pilots produced no measurable return,
and top-down analysis suggests the global buildout needs on the order of
two trillion dollars of annual revenue by 2030 to pencil — a bar it is
currently projected to miss by a wide margin.[^9] None of this proves the
clusters will sit idle. It sets a high hurdle the AI-factory story has not
yet cleared.

---

The honest verdict is narrow, not nihilistic. The bear case is not "AI
compute is worthless." It is that the 2026 buildout is top-of-cycle,
priced on a vendor-sized TAM, and exposed to a hardware-life assumption no
one will commit to in writing. Underwrite the megawatt and the memory,
where the unit economics are legible; treat the token-monetization story as
the option it is, and pay an option price for it — not an infrastructure
multiple.

:::references
- {id: 1, title: "LLM inference price trends", url: "https://epoch.ai/data-insights/llm-inference-price-trends", source: Epoch AI, date: "2026-05-01"}
- {id: 2, title: "AI data center cost breakdown (1 GW TCO; depreciation sensitivity)", url: "https://epoch.ai/data-insights/ai-datacenter-cost-breakdown", source: Epoch AI, date: "2026-05-14"}
- {id: 3, title: "Blackwell B200 cost breakdown", url: "https://epoch.ai/data-insights/b200-cost-breakdown", source: Epoch AI, date: "2026-04-01"}
- {id: 4, title: "NVIDIA unveils DSX AI-factory infrastructure", url: "https://nvidianews.nvidia.com/news/dsx-infrastructure-ai-factory", source: NVIDIA Newsroom, date: "2026-05-31"}
- {id: 5, title: "AI GPU depreciation: CoreWeave, Nebius, and the bear case", url: "https://www.cnbc.com/2025/11/14/ai-gpu-depreciation-coreweave-nvidia-michael-burry.html", source: CNBC, date: "2025-11-14"}
- {id: 6, title: "AI Neocloud Playbook and Anatomy", url: "https://newsletter.semianalysis.com/p/ai-neocloud-playbook-and-anatomy", source: SemiAnalysis, date: "2026-01-20"}
- {id: 7, title: "SK Hynix Q1 2026: AI memory shortage, 72% operating margin", url: "https://www.cnbc.com/2026/04/23/sk-hynix-earnings-ai-memory-shortage-hbm-demand.html", source: CNBC, date: "2026-04-23"}
- {id: 8, title: "Jensen Huang sees ~$1 trillion in cumulative demand", url: "https://www.fool.com/investing/2026/03/24/jensen-huang-sees-1-trillion-in-demand-3-ai-stocks/", source: The Motley Fool, date: "2026-03-24"}
- {id: 9, title: "MIT report: 95% of enterprise generative-AI pilots failing", url: "https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo/", source: Fortune, date: "2025-08-18"}
:::
