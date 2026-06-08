---
eyebrow: MARKET ANALYSIS · KOREA AI
title: Sovereign by the megawatt
deck: NVIDIA promoted NAVER from GPU buyer to AI-factory landlord. The market paid up 14% on a day the KOSPI fell 9%. Here is what the press release left out — and where the Korean AI trade actually clears.
domain: finance
lede: |
  On June 7, 2026, NVIDIA and NAVER announced that Korea's largest internet
  company would build "gigawatt-scale AI factories" on the new NVIDIA DSX
  platform, starting with 55 megawatts at its GAK Sejong data center. The next
  trading session NAVER jumped roughly 14% — even as the KOSPI fell nearly 9%
  and the KOSDAQ tripped a circuit breaker. The narrative is clean: NAVER is
  Korea's sovereign-AI champion, and sovereign AI is the trade of the decade.
  The narrative is also incomplete. The release named no GPU count, no chip,
  and no dollar figure; five months earlier NAVER had been thrown out of
  Korea's flagship sovereign-AI program for using a Chinese model's weights;
  and the cleanest way to own the Korean AI buildout has never been NAVER at
  all. This is the long version.
stats:
  - {label: Start capacity, value: 55, unit: "MW"}
  - {label: APEC GPU pact, value: $9.8B, note: 260k GPUs by 2030}
  - {label: NAVER 1-day move, value: +14%, note: "Jun 8 2026, KOSPI −9%"}
  - {label: SK Hynix Q1 op margin, value: 72%, note: above NVIDIA & TSMC}
---

## 01. The deal, decoded

The thesis sentence: NVIDIA's June 2026 announcement is a *platform and
positioning* commitment, not a procurement disclosure — and the difference is
the whole story.

NVIDIA's own release says NAVER "will expand sovereign AI infrastructure,
starting at 55 megawatts with plans to move to gigawatt scale using the NVIDIA
DSX platform," anchored at the GAK Sejong data center.[^1] That is the entire
hard commitment. The release names {accent}no GPU count, no specific chip SKU,
no dollar capex, and no completion date{/} for the gigawatt stage — the only
other dated item is an "AI Agent Platform" launch in the second half of
2026.[^1] Korean-language coverage adds nuance the English PR omits: the 100MW
(later-2027) and 200MW (2028) steps are framed as {accent}overseas{/}
infrastructure, with the gigawatt endpoint a global ambition rather than a
single Korean campus.[^38]

:::callout(kind=info, label="The short answer")
- **What was actually announced:** a 55MW first phase on NVIDIA DSX at GAK Sejong, scaling "to gigawatt" with no number, no SKU, and no price attached.[^1]
- **Why the stock ran 14%:** the market re-rated NAVER from a GPU *buyer* to an AI-factory *operator/landlord* selling sovereign capacity to government and enterprise.[^25]
- **The hole in the story:** NAVER was cut from Korea's own Sovereign AI Foundation Model program in Jan 2026 for fine-tuning a Chinese model — and said it won't re-enter.[^5]
- **Where the Korean AI trade actually pays:** the HBM memory duopoly. SK Hynix earned a 72% operating margin and ~7x'd in a year; NAVER's AI segment is still ~1-5% of revenue.[^20][^27][^17]
- **The honest verdict:** real optionality, mistimed and over-narrated. Own the megawatt and the memory, not the press release.
:::

The numbers everyone is quoting — "60,000 Blackwell GPUs," "$9.8 billion" —
belong to a *different, earlier* deal. At the APEC CEO Summit in Gyeongju on
October 30-31, 2025, NVIDIA, the Korean government and four conglomerates
committed to deploy {accent}over 260,000 NVIDIA GPUs{/}, a package valued at
up to 14 trillion won (about $9.8 billion) by 2030.[^2][^3] NAVER Cloud's slice
of that — "over 60,000 GPUs" — was the largest single corporate allocation.[^2]
Conflating the October procurement with the June platform deal double-counts
the commitment. Anyone quoting a Rubin/GB300 count or a dollar figure for the
*June* announcement is extrapolating past what NVIDIA actually said.[^1]

:::kv
- {term: Announced, def: "June 7, 2026 (NVIDIA Newsroom)"}
- {term: Platform, def: "NVIDIA DSX (MaxLPS + DSX OS)"}
- {term: First phase, def: "55 MW at GAK Sejong, Korea"}
- {term: Stated endpoint, def: "gigawatt scale — no date, no GPU count"}
- {term: Disclosed capex, def: "none"}
- {term: Nested in, def: "Oct 2025 APEC 260k-GPU national pact"}
:::

Why it matters: a platform commitment is cheap to announce and easy to walk
back; a 260,000-GPU purchase order is neither. The market priced the June
headline as if it were the October purchase order. The rest of this article is
about that gap.

## 02. From buyer to landlord

Thesis: the genuine strategic shift in June 2026 is that NVIDIA elevated NAVER
from a customer that *buys* GPUs to an operator that *sells* AI capacity — a
move up the value chain that is real, but whose economics are unproven.

In October 2025 NAVER was one of five recipients in a national GPU buy.[^2] By
June 2026 it was building "full-stack, end-to-end AI platforms that can serve
enterprises, industries and government" on DSX, fine-tuning NVIDIA's Nemotron 3
Ultra model into the next HyperCLOVA X, and developing a "Seoul World Model" on
NVIDIA Cosmos from its proprietary street-view data.[^1] The pitch to
customers is data sovereignty: a "trusted alternative for secure,
high-performance digital services compliant with local regulatory and
data-sovereignty requirements."[^1] In plain terms, NAVER wants to be the
Korean AWS for anyone who legally cannot — or politically will not — put
sensitive workloads on a US hyperscaler.

:::timeline
- {date: 2026-01-22, headline: "AI Basic Act takes effect", body: "Korea becomes the second jurisdiction after the EU with a comprehensive AI law, framing the sovereign-AI push."}
- {date: 2025-10-31, headline: "APEC Gyeongju: 260k-GPU pact", body: "NVIDIA + govt + Samsung/SK/Hyundai/NAVER commit to >260,000 GPUs, ~$9.8B by 2030. NAVER gets the largest corporate slice (60k+)."}
- {date: 2026-01-15, headline: "NAVER cut from sovereign-AI program", body: "MSIT eliminates NAVER Cloud from the Sovereign AI Foundation Model project; LG AI Research ranks first."}
- {date: 2026-06-07, headline: "NVIDIA DSX / gigawatt AI factories", body: "NAVER to build AI factories on DSX, 55MW → gigawatt. Stock +14% next session."}
:::

The CFO has put money behind the rhetoric. On the Q1 2026 call, NAVER said
infrastructure expenses rose 32.5% year-on-year "mainly due to the acquisition
of new computing assets, including GPUs," and full-year 2025 capex more than
doubled to roughly 1.3 trillion won.[^22] Management guided to over 1 trillion
won of GPU spend in 2026 alone.[^39] This is not a press-release flirtation;
it is a balance-sheet commitment.

The counterpoint is candor from NAVER's own CEO. Asked about HyperCLOVA X, Choi
Soo-yeon described "an overall broad orchestration strategy" that layers
"other open source models" on top of the in-house model.[^22] A sovereign
champion that leans on open-source weights for the hard parts is a weaker moat
than the marketing implies — a tension that becomes a liability in the next
section. Why it matters: the buyer-to-landlord story is the bull case in one
line, and it is plausible. But "plausible platform" and "earned cost of
capital" are very different claims.

## 03. The sovereignty hole

Thesis: the single most important fact about NAVER's sovereign-AI story is
under-reported in the West — its own government threw it out of the flagship
sovereign-AI program, on sovereignty grounds.

In August 2025, Korea's Ministry of Science and ICT (MSIT) selected five
consortia for its Sovereign AI Foundation Model project — NAVER Cloud, LG AI
Research, SK Telecom, Upstage and NC AI — backed by roughly 200 billion won of
support and a brutal cull mechanism: the field narrows every six months, from
five to four to an eventual two by 2027, and each model must reach at least 95%
of frontier performance.[^6] In the first evaluation round, announced January
15, 2026, {accent}NAVER Cloud was eliminated{/}.[^5] LG AI Research ranked
first; SK Telecom and Upstage advanced.[^5]

The stated reason is the part that should give NAVER bulls pause. MSIT found
NAVER's entry "relied on fine-tuning existing overseas models — a practice that
runs counter to the project's core requirement to train models
independently."[^5] Specifically, NAVER's vision encoder reused pretrained
parameters from {accent}Alibaba's Qwen 2.5-VL 32B{/} without allowing weight
updates.[^5] A company selling "sovereign" infrastructure was cut from the
sovereign program for building on Chinese model weights — and then said it
{accent}would not participate in the next round{/}.[^5]

> NAVER Cloud, previously viewed as a front-runner, was eliminated over
> concerns of model originality and technical independence.
> — The Korea Herald, January 15, 2026

The capability gap shows up on benchmarks too. LG's EXAONE 4.0 (32B) ranked
11th globally on the Artificial Analysis Intelligence Index (MMLU-Pro 81.8%,
AIME 2025 85.3%), standing alongside Gemini and GPT-class systems; HyperCLOVA X
leads on *Korean-language* suites like KoBALT-700 but not on global
reasoning.[^7] NAVER's differentiation is narrowing to a Korean-language niche.

And the regulatory moat the whole thesis rests on is eroding. By Korea's Fair
Trade Commission data, AWS holds roughly 60-70% of the Korean cloud market,
Microsoft 10-12%, and the domestic players trailing in third — NAVER on the
order of 7%.[^8][^9] Their real advantage was exclusive access to the public
sector, and in April 2025 AWS received CSAP "Low" certification, breaching
exactly that tier.[^9]

:::rank-list
- {label: AWS, value: "~70%", pct: 100}
- {label: Microsoft Azure, value: "~11%", pct: 16}
- {label: NAVER Cloud, value: "~7%", pct: 10, highlight: true}
- {label: Others (NHN/KT/Kakao/SDS), value: "~12%", pct: 17}
:::

Counterpoint, honestly stated: being cut from a *subsidy program* is not the
same as losing the *commercial* business. NAVER retains its HyperCLOVA X
commercial deployments, public-sector cloud contracts and its NVIDIA GPU
allocation.[^5] But the episode punctures the cleanest version
of the bull case — "government-anointed national champion" — at the source.
Why it matters: a sovereignty premium you cannot defend in your home
sovereign's own tender is a premium the market should discount, not pay up for.

## 04. Follow the megawatt

Thesis: the binding constraint on NAVER's gigawatt ambition is not capital or
chips — it is Korean electrons, and the Korean grid is a geographic-mismatch
machine where cheap power is a myth.

NVIDIA's own DSX marketing concedes the point: DSX MaxLPS exists to maximize
"token throughput per megawatt," letting operators "deploy up to 40% more GPUs
within the same power envelope."[^17][^18] When the vendor optimizes for
tokens-per-MW, megawatts — not GPU counts — are the scarce input. A GB200
NVL72 rack draws ~120kW; a data center fits only 6-8 such racks per
megawatt.[^18] At gigawatt scale, the question is not "can NAVER buy the GPUs"
but "can KEPCO deliver the power."

The Korean grid answer is uncomfortable. First, deliverability: KEPCO's
grid-supply confirmation has reportedly stretched toward roughly a year, up
from a few months, and a large share of its transmission and substation
projects are running late as of late 2025.[^14] Second, cost: after an October 2024 hike,
Korea's industrial electricity runs about 182.7 won/kWh (~$0.13) — roughly
{accent}65% above the US industrial rate{/} of ~$0.08/kWh.[^12][^13] The "cheap
Korean power" tailwind does not exist; if anything policy is *raising* metro
power costs by design to disperse load.

:::compare
- {role: KOREA, name: "Industrial power", value: "$0.13"}
- {role: USA, name: "Industrial power", value: "$0.08"}
- {role: SUBJECT, name: "Korea premium", value: "+65%"}
:::

Third, geography. KEPCO carried about 203 trillion won (~$151B) of debt after
near-bankruptcy in 2023, then swung to roughly 8.9 trillion won of operating
profit in 2024 on tariff hikes and cheaper fuel — a recovery, but one that
constrains the very grid capex AI data centers need.[^10][^11] Generation sits
on the south and east coasts (nuclear, LNG); demand concentrates in the Seoul
metro. That is why GAK Sejong, in the Chungcheong corridor, is on the *right*
side of Korea's data-center dispersal policy.[^15]

But there is a hard physical ceiling on the "gigawatt at GAK Sejong" reading.
GAK Sejong opened in November 2023 with a *planned* 270MW capacity fed from a
{accent}154kV{/} substation.[^15] One gigawatt is nearly four times that. A
true GW campus would require a higher-voltage 345kV-class interconnection — a
multi-year KEPCO transmission dependency against a balance sheet still ~200
trillion won levered.[^10][^15] This is the strongest reason to read "100MW and
200MW overseas" in the Korean coverage literally: the domestic site may
top out well below a gigawatt.[^38]

:::stats
- {label: GAK Sejong (planned), value: 270, unit: "MW"}
- {label: Substation, value: 154, unit: "kV"}
- {label: 1 GW needs, value: 345, unit: "kV+"}
- {label: Grid confirm time, value: "~12", unit: "mo."}
:::

Why it matters: "gigawatt scale" is a power-procurement promise dressed as a
chip announcement. The megawatt, not the GPU, is the thing to underwrite — and
in Korea the megawatt is expensive, slow, and constrained by a recovering but
still-fragile monopoly utility.

## 05. The unit economics of an AI factory

Thesis: even granting NAVER the power, the returns on a gigawatt AI factory
hinge on one contested assumption — how fast a GPU depreciates — and the
honest answer is "nobody knows."

Start with the sticker. A 1GW GB200-class AI data center costs roughly $38
billion up-front, with about $8.5 billion per year of total cost of ownership
under a five-year IT life.[^16] Scale that to NAVER's disclosed steps: 55MW
implies on the order of $2-3 billion of first-phase capex, and a literal
gigawatt would be a $38-50 billion undertaking — against NAVER's entire ~30
trillion won (~$22B) market cap. The numbers only work as a multi-year,
demand-pulled build, not a single check.

The hinge is depreciation. Epoch's own sensitivity is stark: shorten the IT
life from five years to three and annual cost jumps from $8.5B to
{accent}$12B — a 41% increase{/}; stretch it to seven and it falls to
$7B.[^16] This is not academic. Hyperscalers assume 5-6 year lives; critics
including Michael Burry argue the real economic life is 2-3 years given
NVIDIA's annual cadence.[^24] The market cannot even agree with itself:
CoreWeave depreciates GPUs over six years while Nebius uses four for identical
chips.[^24]

:::compare
- {role: BEAR, name: "3-yr GPU life", value: "$12B/yr"}
- {role: BULL, name: "7-yr GPU life", value: "$7B/yr"}
- {role: SUBJECT, name: "Base (5-yr)", value: "$8.5B/yr"}
:::

Then add utilization. SemiAnalysis is blunt that bare-metal GPU clouds run
55-65% gross margins before depreciation but have "almost no margin of safety":
returns "flatline" if utilization slips below 80% or rental prices dip.[^19] A
sovereign cloud with captive government demand can clear that bar; a merchant
arm exposed to spot-rental erosion is far more fragile. NAVER is betting it is
the former.

The bull rejoinder is real: DSX MaxLPS's claimed +40% GPUs-per-megawatt
directly improves the tokens-per-dollar math, and a landlord with a 2-3 year
demand backlog can underwrite long depreciation honestly.[^17][^18] But that
rejoinder *requires* the demand to be there — which is precisely what Section
08 puts on trial. Why it matters: the difference between a 3-year and a 7-year
GPU life is the difference between a value-destructive capex sink and a durable
infrastructure annuity. NAVER has disclosed neither its assumed life nor its
contracted utilization. Underwrite accordingly.

## 06. NAVER, the stock

Thesis: NAVER is genuinely cheap versus global peers, but the cheapness is
doing work the AI story gets credit for — and the AI segment is too small to
move earnings while it is busy compressing margins.

The franchise is profitable and growing. FY2025 revenue was 12.04 trillion won
(+12.1%) with operating profit of 2,208 billion won (+11.6%).[^21] But
{accent}net income fell 5.8%{/} to 1,820 billion won, and Q1 2026 operating
margin compressed to 16.7% (from ~18%) as GPU and media-rights spend
landed.[^20][^21] The market is capitalizing an AI buildout whose costs are
already in the P&L and whose revenues are not.

Here is the scale problem, stated plainly: NAVER's cloud/enterprise segment —
where the entire AI data-center business lives — is only a low-single-digit
share of group revenue, on the order of {accent}1-5%{/}.[^21] A gigawatt of AI factories is a
rounding error against search and commerce today; it is an option on the
future, priced in the present.

:::line-chart(title="NAVER (035420.KS) close, trailing 12 months", subtitle="Yahoo Finance, monthly — KRW", y-unit=₩)
x: 2025-07,2025-08,2025-09,2025-10,2025-11,2025-12,2026-01,2026-02,2026-03,2026-04,2026-05,2026-06
NAVER: 235000,214500,268500,267500,244000,242500,275000,254500,201500,211000,234000,279000
:::

On valuation, NAVER trades around 16x forward earnings versus roughly 22x for
Alphabet and 25x for Meta — a real discount, even after adjusting for the
chronic "Korea discount."[^37] The catch: the 27-analyst
consensus target sits near 292,500 won against a spot near 279,000, implying
only ~5% upside, and recent broker targets have been *cut* (e.g. 340,000 →
300,000 won) as margin compression bites.[^23] The easy re-rating already ran
in the October-2025-to-June-2026 rally.

:::stats
- {label: FY2025 revenue, value: "₩12.0T", note: "+12.1% YoY"}
- {label: FY2025 net income, value: "₩1.82T", note: "−5.8% YoY"}
- {label: Q1'26 op margin, value: "16.7%", note: "from ~18%"}
- {label: Fwd P/E, value: "~16x", note: "vs Alphabet ~22x"}
- {label: Consensus upside, value: "~5%", note: "as of 2026-06-08"}
:::

The tape tells the cleanest story. On June 8, 2026 NAVER rose ~14% to 290,500
won even as the KOSPI fell nearly 9% and the KOSDAQ tripped a circuit breaker
in a memory-led selloff — an idiosyncratic AI bid decoupling NAVER from the
index.[^25][^26] That is the bull case in one candle: when the AI trade is on,
NAVER is now a way to express it. The bear case is the same candle, inverted:
a 14% pop on a no-numbers press release is sentiment, not cash flow.

Counterpoint worth respecting: a profitable platform at 16x with a 5.7% free
cash-flow yield and embedded Webtoon/commerce optionality does not *need* the
AI story to be fairly valued — the AI factory is a free-ish call option.[^37]
Why it matters: buy NAVER for the cheap, cash-generative core and treat the
gigawatt as upside; do not pay an AI multiple for a segment that is 1-5% of
revenue and currently dilutive to margins.

## 07. Where the trade actually clears

Thesis: if you want to own the Korea-NVIDIA buildout with real unit economics
instead of narrative, you want the memory duopoly — and the market already
figured that out.

Every incremental NVIDIA GPU shipped into any AI factory, sovereign or not,
mechanically pulls high-bandwidth memory, and Korea owns that chokepoint. SK
Hynix is expected to supply roughly {accent}two-thirds of NVIDIA's HBM4{/}, and
HBM plus advanced packaging account for about two-thirds of a Blackwell B200's
unit cost.[^29][^30] The value capture is direct and quantified in a way
NAVER's services bet simply is not.

:::donut(center-label="B200 cost")
- {label: "HBM memory + packaging", value: 66}
- {label: "GPU logic die + other", value: 34}
:::

The results are the proof. SK Hynix posted a record Q1 2026 — 52.6 trillion
won revenue, 37.6 trillion won operating profit, a {accent}72% operating
margin{/} higher than NVIDIA's or TSMC's most recent — and management said
customer HBM demand for the next three years already exceeds its supply
capacity.[^27][^28] The stock did the rest: SK Hynix shares rose roughly
seven-fold over the trailing twelve months, and by late May 2026 its market cap
had closed to within 6.8% of Samsung's.[^31]

:::line-chart(title="SK Hynix (000660.KS) close, trailing 12 months", subtitle="Yahoo Finance, monthly — KRW", y-unit=₩)
x: 2025-07,2025-08,2025-09,2025-10,2025-11,2025-12,2026-01,2026-02,2026-03,2026-04,2026-05,2026-06
SK Hynix: 273500,269000,347500,559000,530000,651000,909000,1061000,807000,1286000,2333000,1911000
:::

Set the two trades side by side and the contrast is the article's core
finding. NAVER is a services/optionality bet on a segment that is ~1-5% of
revenue and compressing margins.[^17] SK Hynix is an oligopoly input that is
sold out three years forward at peak-of-industry margins.[^27] One is a story
about what might be monetized; the other is a price you can already see in the
P&L.

:::callout(kind=warn, label=Caveat)
Memory is cyclical. The 72% margin and the ~7x move are cycle-peak readings, not steady-state.[^27] Samsung's HBM4 qualification for NVIDIA is the share-shift risk to SK Hynix's near-monopoly economics, and the analyst "high" targets (e.g. ~4,000,000 won for SK Hynix) are outliers, not consensus.[^29] The point is not "SK Hynix only goes up." It is that the *unit economics* of the memory trade are legible in a way the sovereign-cloud trade's are not.
:::

Why it matters: the Naver-premium pitch that seeded this research is an
equity-story bet on the most narratively appealing name. The disciplined
expression of the same macro view — Korea is structurally central to AI — has
been the boring memory duopoly all along.

## 08. Is "sovereign AI" even sound?

Thesis: the demand assumption under every Korean AI factory is a vendor-promoted
narrative, and the independent evidence on whether AI compute converts to
return is, so far, discouraging.

Sovereign AI's chief evangelist is the company that sells the GPUs. NVIDIA CEO
Jensen Huang has argued that "every country needs to own the production of
their own intelligence," and has framed roughly $1 trillion of cumulative
Blackwell and Rubin demand through 2027.[^34][^35] A genuine policy argument
can coincide with self-interest — but a $1 trillion total addressable market
sized by the chip vendor is a TAM to interrogate, not to underwrite.

The independent ROI evidence is unkind. An MIT study found
{accent}95% of enterprise generative-AI pilots produced zero measurable
return{/}.[^32] Top-down, Bain estimates the global AI buildout needs $2
trillion of annual revenue by 2030 and is on track to fall about $800 billion
short.[^33] Sequoia's "$600B question" makes the same point from the supply
side: at ≤50% utilization a 1GW facility wastes ~$5B/year.[^19] None of this
proves Korea's clusters will sit idle — but it sets a high bar the sovereign
story has not yet cleared.

:::stats
- {label: Enterprise GenAI pilots w/ zero ROI, value: "95%", note: "MIT, 2025"}
- {label: Revenue needed by 2030, value: "$2T", note: "Bain"}
- {label: Projected shortfall, value: "$800B", note: "Bain"}
- {label: Korea domestic market, value: "~52M", note: "people"}
:::

Korea-specific skepticism sharpens it. A US-Korea think-tank notes that a
~52-million-person domestic market "may not be sustainable" for sovereign AI
services long-term, and that HyperCLOVA X promotion leans on nationalistic
sentiment "rather than by an objective evaluation of its performance."[^36]
When a Korean enterprise can call GPT, Claude or Gemini at frontier quality,
the sovereign premium has to be paid for by regulation and patriotism, not
performance — and Section 03 showed even the regulator was unimpressed.[^5]

The steelman, stated fairly: sovereign AI is partly a *non-commercial*
security and cultural good, so a pure-ROI test measures the wrong thing for a
government buyer; and Korea is not choosing AI compute *instead* of its
strength — its HBM fabs *are* the NVIDIA supply chain, so the country is
funding both ends of the trade.[^29] Why it matters: the bear case is not
"sovereign AI is worthless." It is narrower and more dangerous to the NAVER
multiple — the buildout is top-of-cycle, oversized for a 52M market, exposed to
fast GPU depreciation, and resting on a vendor-sized TAM.

## 09. What would break this thesis

Thesis: an honest analyst names the conditions under which they are wrong.
Here are the load-bearing claims and what would falsify them.

**If NAVER discloses a real GPU order and capex for the June deal**, the
"platform, not procurement" read in Section 01 weakens — the buyer-to-landlord
transition would be further along than the press release implies. As of the
June 7 release, no such number exists.[^1]

**If NAVER re-enters and wins a later sovereign-AI round**, the Section 03 hole
partially closes. Against it: NAVER explicitly said it would not
participate again, and the capability gap to EXAONE is real.[^5][^7]

**If KEPCO compresses interconnection timelines and a 345kV tie-in to GAK
Sejong is approved**, the Section 04 power ceiling lifts. Against it: a
12-month confirmation queue, 55% project-delay rate, and a still-levered
utility.[^14][^10]

**If GPU useful life proves to be 6-7 years in practice**, the Section 05
economics turn benign and the merchant-cloud return is real. The contested
3-vs-6-year split (Burry vs. CoreWeave vs. Nebius) is the single most important
unknown in the entire thesis.[^24][^16]

**If the memory cycle rolls over**, the Section 07 "own SK Hynix instead"
conclusion inverts — 72% margins are a peak, not a plateau, and Samsung's HBM4
qualification is the share-shift risk.[^27][^29]

A red-team pass against the article's three load-bearing claims — the 55MW
DSX commitment, the January 2026 sovereign-program cull, and SK Hynix's 72%
margin — found no contradicting primary evidence; all three survived adversarial
search. The conclusion is therefore stated with appropriate confidence, not
certainty: NAVER's gigawatt bet is a genuine option with a real power
constraint, an unproven return, and a sovereignty story its own government
declined to endorse. Own the megawatt and the memory. Treat the press release
as the marketing it is.

:::references
- {id: 1, title: "NAVER Expands AI Infrastructure With NVIDIA", url: "https://nvidianews.nvidia.com/news/naver-ai-infrastructure", source: NVIDIA Newsroom, date: "2026-06-07"}
- {id: 2, title: "NVIDIA, South Korea Government and Industrial Giants Build AI Infrastructure", url: "https://nvidianews.nvidia.com/news/south-korea-ai-infrastructure", source: NVIDIA Newsroom, date: "2025-10-30"}
- {id: 3, title: "Nvidia strikes AI alliance with S.Korea, pledges 260,000 GPUs worth $9.8 billion by 2030", url: "https://www.kedglobal.com/tech,-media-telecom/newsView/ked202510310020", source: KED Global, date: "2025-10-31"}
- {id: 5, title: "Korea's sovereign AI project first-round results: NAVER Cloud eliminated", url: "https://www.koreaherald.com/article/10656367", source: The Korea Herald, date: "2026-01-15"}
- {id: 6, title: "Korea selects five consortia for sovereign AI foundation models", url: "https://www.koreaherald.com/article/10546363", source: The Korea Herald, date: "2025-08-04"}
- {id: 7, title: "LG EXAONE 4.0 ranks among global frontier models", url: "https://www.theinvestor.co.kr/article/10554458", source: The Investor, date: "2025-07-15"}
- {id: 8, title: "AWS dominates Korea cloud market (FTC data)", url: "https://www.koreatimes.co.kr/www/tech/2024/09/129_342689.html", source: The Korea Times, date: "2024-09-20"}
- {id: 9, title: "South Korea cloud computing market — AWS CSAP entry", url: "https://www.marketreportanalytics.com/reports/south-korea-cloud-computing-market-87712", source: Market Report Analytics, date: "2025-05-01"}
- {id: 10, title: "KEPCO debt reaches 203 trillion won after near-bankruptcy", url: "https://www.koreaherald.com/article/3395050", source: The Korea Herald, date: "2024-06-10"}
- {id: 11, title: "KEPCO returns to operating profit in 2024", url: "https://www.koreaherald.com/article/10409931", source: The Korea Herald, date: "2025-02-24"}
- {id: 12, title: "South Korea 9.7% industrial electricity rate hike", url: "https://energynews.pro/en/south-korea-9-7-industrial-electricity-rate-hike-to-reduce-kepcos-losses/", source: EnergyNews.pro, date: "2024-10-24"}
- {id: 13, title: "Electric Power Monthly, Table 5.3 (US industrial price)", url: "https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=table_5_03", source: US EIA, date: "2025-03-01"}
- {id: 14, title: "Over half of KEPCO grid projects delayed", url: "https://www.msn.com/en-xl/news/other/over-half-of-kepco-grid-projects-delayed-risking-renewable-expansion/ar-AA1ORvxw", source: Yonhap via MSN, date: "2025-10-15"}
- {id: 15, title: "NAVER GAK Sejong data center (270MW, 154kV)", url: "https://www.datacentermap.com/south-korea/sejong/naver-gak-sejong/", source: DataCenterMap, date: "2023-11-01"}
- {id: 16, title: "AI data center cost breakdown (1GW TCO, depreciation sensitivity)", url: "https://epoch.ai/data-insights/ai-datacenter-cost-breakdown", source: Epoch AI, date: "2026-05-14"}
- {id: 17, title: "NVIDIA unveils DSX AI-factory infrastructure", url: "https://nvidianews.nvidia.com/news/dsx-infrastructure-ai-factory", source: NVIDIA Newsroom, date: "2026-05-31"}
- {id: 18, title: "NVIDIA extends its grip on the AI datacenter (DSX MaxLPS +40%)", url: "https://www.nextplatform.com/ai/2026/06/02/nvidia-extends-its-grip-on-the-ai-datacenter-outwards/5250344", source: The Next Platform, date: "2026-06-02"}
- {id: 19, title: "AI Neocloud Playbook and Anatomy", url: "https://newsletter.semianalysis.com/p/ai-neocloud-playbook-and-anatomy", source: SemiAnalysis, date: "2026-01-20"}
- {id: 20, title: "NAVER Q1 2026 earnings release", url: "https://www.navercorp.com/en/media/pressReleasesDetail?seq=10034270", source: NAVER IR, date: "2026-04-30"}
- {id: 21, title: "NAVER FY2025 revenue tops 12.04 trillion won", url: "https://www.thepickool.com/naver-fy2025-revenue-hits-krw-12-04-trillion-on-ad-growth/", source: The Pickool, date: "2026-02-06"}
- {id: 22, title: "NAVER Q1 2026 earnings call transcript (CFO/CEO quotes)", url: "https://www.alphaspread.com/security/krx/035420/investor-relations/earnings-call/q1-2026", source: AlphaSpread, date: "2026-04-30"}
- {id: 23, title: "NAVER consensus estimates and price targets", url: "https://www.investing.com/equities/nhn-corp-consensus-estimates", source: Investing.com, date: "2026-06-08"}
- {id: 37, title: "NAVER valuation vs peers (forward P/E, FCF yield)", url: "https://simplywall.st/stocks/kr/media/kose-a035420/naver-shares/future", source: Simply Wall St, date: "2026-06-01"}
- {id: 25, title: "South Korea's NAVER rallies on NVIDIA AI partnership", url: "https://www.investing.com/news/stock-market-news/south-koreas-naver-rallies-on-nvidia-ai-partnership-4729773", source: Investing.com, date: "2026-06-08"}
- {id: 26, title: "KOSDAQ triggers circuit breaker after 8% plunge", url: "https://www.digitaltoday.co.kr/en/view/61433/kosdaq-triggers-circuit-breaker-after-8-percent-plunge-following-kospi-drop", source: Digital Today, date: "2026-06-08"}
- {id: 27, title: "SK Hynix Q1 2026: AI memory shortage, 72% margin", url: "https://www.cnbc.com/2026/04/23/sk-hynix-earnings-ai-memory-shortage-hbm-demand.html", source: CNBC, date: "2026-04-23"}
- {id: 28, title: "SK Hynix announces FY2025 financial results", url: "https://news.skhynix.com/sk-hynix-announces-fy25-financial-results/", source: SK Hynix Newsroom, date: "2026-01-28"}
- {id: 29, title: "SK Hynix to supply about two-thirds of NVIDIA HBM4", url: "https://www.trendforce.com/news/2026/01/28/news-sk-hynix-reportedly-to-supply-about-two-thirds-of-nvidia-hbm4-samsung-targets-early-delivery/", source: TrendForce, date: "2026-01-28"}
- {id: 30, title: "Blackwell B200 cost breakdown", url: "https://epoch.ai/data-insights/b200-cost-breakdown", source: Epoch AI, date: "2026-04-01"}
- {id: 31, title: "SK Hynix closes in on Samsung's market cap (6.8% gap)", url: "https://en.sedaily.com/markets/2026/05/29/sk-hynix-closes-in-on-samsungs-market-cap-68-percent-gap", source: Seoul Economic Daily, date: "2026-05-29"}
- {id: 32, title: "MIT report: 95% of generative AI pilots failing", url: "https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo/", source: Fortune, date: "2025-08-18"}
- {id: 33, title: "$2 trillion in new revenue needed to fund AI scaling", url: "https://www.bain.com/about/media-center/press-releases/20252/", source: Bain & Company, date: "2025-09-23"}
- {id: 34, title: "Huang at World Governments Summit: sovereign AI", url: "https://blogs.nvidia.com/blog/world-governments-summit/", source: NVIDIA Blog, date: "2024-02-12"}
- {id: 35, title: "Jensen Huang sees $1 trillion in demand", url: "https://www.fool.com/investing/2026/03/24/jensen-huang-sees-1-trillion-in-demand-3-ai-stocks/", source: The Motley Fool, date: "2026-03-24"}
- {id: 36, title: "The sovereign AI debate and prospects of Korean AI", url: "https://keia.org/the-peninsula/the-sovereign-ai-debate-and-prospects-of-korean-ai/", source: Korea Economic Institute, date: "2025-01-08"}
- {id: 24, title: "AI GPU depreciation: CoreWeave, Nebius, Burry", url: "https://www.cnbc.com/2025/11/14/ai-gpu-depreciation-coreweave-nvidia-michael-burry.html", source: CNBC, date: "2025-11-14"}
- {id: 39, title: "NAVER to invest over $690 million in GPUs from next year", url: "https://www.koreatimes.co.kr/business/tech-science/20251105/naver-to-invest-over-690-mil-in-gpu-from-next-year", source: The Korea Times, date: "2025-11-05"}
- {id: 38, title: "Nvidia taps Naver for gigawatt-scale AI cloud push in Korea", url: "https://www.koreaherald.com/article/10765602", source: The Korea Herald, date: "2026-06-08"}
:::
