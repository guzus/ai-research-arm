---
eyebrow: Capital · AI Infrastructure
title: 'Situational Awareness LP: when the AGI manifesto came with a brokerage account'
deck: Leopold Aschenbrenner turned a 165-page essay into a $5.5B hedge fund. The book is one big bet that
  the bottleneck to superintelligence is electrons and copper, not weights.
lede: 'In June 2024 a 22-year-old ex-OpenAI researcher published a manifesto arguing that the world was
  sleepwalking into artificial general intelligence by 2027. Within months he had launched a hedge fund
  built around exactly that thesis. By the March 2026 13F filing, Situational Awareness LP reported **$5.52
  billion** in U.S. equity exposure across just **24 positions** — a concentration that is unusual even
  by activist standards, and that translates the abstract essay into a very specific wager: that the binding
  constraint on AGI is not algorithms, but power plants, fiber, and racks.'
stats:
- label: '13F AUM'
  value: $5.52B
  note: Q1 2026 filing[^1]
- label: Positions
  value: '24'
  note: Long-only U.S. equities + options
- label: Top 5 weight
  value: '60%'
  note: Power, AI compute, optics
- label: Founded
  value: '2024'
  note: San Francisco · co-managed with Carl Shulman[^6]
---

## 01. The manifesto becomes a mandate

Aschenbrenner — Columbia valedictorian at 19, FTX Future Fund alum, OpenAI Superalignment researcher until his April 2024 dismissal — published ["Situational Awareness: The Decade Ahead"](https://situational-awareness.ai/) two months after leaving the lab.[^2] The essay's central argument is brutally compressed: extrapolate the GPT-2 to GPT-4 jump forward another four years, fold in roughly half an order of magnitude per year of compute scaling plus a similar contribution from algorithmic gains, and AGI is the modal outcome by 2027. Beyond that, hundreds of millions of automated researchers could "compress a decade of algorithmic progress into ≤1 year" — the recursive-self-improvement story dressed in tidy economist's notation.[^3]

The actionable corollary, and the one underwriting the fund, is industrial: "trillions of dollars will go into GPU, datacenter, and power buildout before the end of the decade."[^3] The bet is not that this is a contrarian claim — by 2026 it is consensus — but that public markets are still under-pricing how lopsided the value capture will be. If you believe the essay, marginal model quality is a commodity; megawatts on a contract starting before 2028 are not.

> The most valuable assets in the AI era may not be algorithms, but electricity and computing power.
> — Aschenbrenner, paraphrased by Fortune (March 2026)

## 02. Picks and shovels, not models

The fund deliberately avoids the names a retail "AI portfolio" would default to. There is no direct exposure to the frontier labs (most are private), light positioning in Nvidia, and the megacap hyperscalers are conspicuously underweight. Instead the book concentrates on three layers of the buildout: behind-the-meter and grid-scale **power**, neocloud and former-crypto **compute**, and the **optical / memory** plumbing that connects them.

- **Power generation.** Bloom Energy (solid-oxide fuel cells deployable next to data centers), with prior 13Ds and disclosures pointing at independent power producers like Vistra and Constellation.[^4]
- **AI cloud and reconverted miners.** CoreWeave (common and calls), Core Scientific, IREN, Applied Digital — companies whose land, substations, and ASIC-cooled shells are being rezoned for GPUs.[^5]
- **Physical connectivity.** Lumentum (optical transceivers for AI fabrics) and Sandisk (NAND for inference caches and checkpoint storage).[^5]

The framing is closer to a 19th-century railroad fund than to a tech hedge fund — what matters is right-of-way and interconnect queue position, not who runs the trains.

## 03. Inside the book

The March 31, 2026 13F shows a top-heavy long book with two derivatives sleeves — CoreWeave and Intel — used to express conviction at higher delta than cash equity would allow on a fund this concentrated.[^1]

| Rank | Position | Weight | Reported value | Role in thesis |
|---|---|---|---|---|
| 1 | Bloom Energy (BE) | 15.9% | $875.5M | Off-grid fuel cells for data centers |
| 2 | CoreWeave calls (CRWV) | 14.0% | $774.4M | Levered exposure to neocloud growth |
| 3 | Intel calls (INTC) | 13.5% | $746.8M | Foundry / domestic fab option value |
| 4 | Lumentum (LITE) | 8.7% | $478.6M | Optical transceivers for AI fabrics |
| 5 | CoreWeave common (CRWV) | 7.9% | $436.7M | Core compute infrastructure |
| 6 | Core Scientific (CORZ) | 7.4% | — | Reconverted miner → AI hosting |
| 7 | IREN | 6.0% | — | Power-connected greenfield sites |
| 8 | Applied Digital (APLD) | 5.0% | — | Custom data centers, CoreWeave partner |
| 9 | Sandisk (SNDK) | 4.5% | — | NAND for inference / checkpoint storage |

:::bars
- label: Bloom Energy
  value: '15.9%'
  pct: 16
- label: CoreWeave (calls)
  value: '14.0%'
  pct: 14
- label: Intel (calls)
  value: '13.5%'
  pct: 14
- label: Lumentum
  value: '8.7%'
  pct: 9
- label: CoreWeave (common)
  value: '7.9%'
  pct: 8
- label: Core Scientific
  value: '7.4%'
  pct: 7
- label: IREN
  value: '6.0%'
  pct: 6
- label: Applied Digital
  value: '5.0%'
  pct: 5
- label: Sandisk
  value: '4.5%'
  pct: 5
:::

Two structural notes deserve attention. First, the *quarterly change* in CoreWeave call notional was +368% — a clean tell that the fund is pyramiding into its highest-conviction name, not trimming after a run.[^1] Second, the 13F understates the real book. It does not include short positions, foreign listings, private placements, or the strike-and-expiry of those CRWV and INTC calls, so what looks like a 14% weight is almost certainly running at a much higher delta-adjusted economic exposure.

## 04. Performance: bright days, black quarters

Public performance numbers are partial and need a haircut for survivorship- and proxy-error. Latticework, working off a value-overlay framework, reports the fund posting "more than 96 percentage points of alpha over the S&P 500" with returns exceeding 100% by early 2026.[^7] Third-party 13F-proxy trackers tell a noisier story: a brutal **−21.3%** drawdown in Q4 2025 followed by a recovery month that proxy services scored at **+60% in April 2026**.[^8]

:::callout(kind=warn, label=Caveat)
All third-party performance figures are reconstructed from quarterly 13Fs, which exclude shorts, options strikes, and foreign positions. Reported quarterly returns are best read as a *direction*, not a number — and a fund this concentrated will mark to market with the kind of vol a 60/40 buyer should not casually annualize.
:::

:::kv
- term: Style
  def: Concentrated long with selective calls; thematic, not market-neutral
- term: Top-heavy
  def: Top 5 ≈ 60% of disclosed book; top 9 ≈ 83%
- term: Best month (proxy)
  def: +60.2% — Apr 2026
- term: Worst month (proxy)
  def: −9.7% — Nov 2025
- term: Beta to S&P 500 (proxy)
  def: ≈ 3.2 — high single-stock risk
:::

## 05. Backers, lockups, and the copycat trade

The cap table is a Who's Who of the AI-adjacent founder class: Patrick and John Collison (Stripe), Daniel Gross (now co-leading Meta Compute), and Nat Friedman (now Meta's AI product lead) are all seed LPs.[^9] Aschenbrenner has reportedly put "almost all of his own net worth" into the fund — skin in the game that is rhetorically powerful but also a portfolio-construction red flag if the thesis blows up.[^4]

Terms are friendly to the manager. Independent notes peg the structure at a **$25M minimum**, a **two-year lockup** with quarterly redemptions over two further years, Qualified Purchaser requirements, and a classical **"2 and 20"** fee load.[^6] That schedule is what you sign when you believe the manager genuinely needs the dry powder; it is also what you sign when liquidity in some of the underliers — small-cap miners, sub-billion utilities — is too thin to support open-ended redemptions.

:::callout(kind=info, label=Note)
A whole micro-ecosystem of "copycat" 13F replicators has sprung up around the fund — open-source notebooks that rebalance into the disclosed long book each quarter. They miss shorts, foreign names, and the actual delta of the option positions, so even a faithful copycat is a watered-down version of the strategy and will diverge from the LP class.[^6]
:::

## 06. Three ways this could be wrong

The fund's pitch has internal coherence — but coherence is not correctness. The hard parts of the thesis are the same hard parts as the underlying essay.

### A. The bottleneck migrates back to software

Picks-and-shovels works as long as compute is the binding constraint. Two plausible futures break that: (i) algorithmic efficiency gains compress how much compute frontier training actually needs (the DeepSeek-style argument); (ii) inference moves on-device or to dramatically cheaper accelerators, gutting hyperscale demand growth. In either case Bloom Energy and Core Scientific are still cyclical energy and real-estate names — they just stop being a derivative on AGI.

### B. The 2027 timeline is wrong, or the buildout is

If AGI slips to 2030+, the buildout doesn't stop, but the multiple does. A 24-stock book levered with calls is exquisitely sensitive to *narrative* velocity, not just earnings. The Q4 2025 drawdown is a worked example: the underlying companies didn't lose 21% of their fundamentals in three months.

### C. Reflexivity in the seed LP base

Several of the fund's largest backers now hold operating roles at the very hyperscaler — Meta — whose AI capex decisions drive demand for half the book. That is not a scandal, but it does mean the fund is a leveraged read on a buildout that its biggest investors directly influence. When that loop tightens, it works; when it loosens, the same loop unwinds the trade.

:::callout(kind=danger, label=Risk)
The fund's largest disclosed sleeves are options on two single names (CRWV, INTC) totalling roughly 27% of the 13F. That is a structural commitment to gamma. It pays linearly into a melt-up and decays painfully through a chop — which is exactly what proxy services seem to have captured between November 2025 and April 2026.
:::

## 07. What to watch next

- **Q2 2026 13F (August filing).** The signal is whether the CoreWeave call sleeve is rolled, taken to delta-one, or trimmed. Each implies a different read on the AI capex cycle.
- **Bloom Energy contract disclosures.** Behind-the-meter fuel-cell deals with named hyperscalers would convert a thesis into a multi-year revenue ramp; their absence would be a tell.
- **Interconnect queue news from PJM and ERCOT.** If grid timelines compress, the fund's power names re-rate; if they extend further into the 2030s, the picks-and-shovels narrative gets a discount-rate problem.
- **Frontier-lab efficiency announcements.** A credible 10x training-efficiency claim from a frontier lab would test the thesis more directly than any macro datapoint.
- **Any return data Aschenbrenner himself confirms.** All quoted performance to date is reconstructed or sourced to media accounts. An audited number will move the conversation either way.

---

## Sources

:::references
- id: 1
  title: Insider Monkey — Situational Awareness LP 13F portfolio, filing dated March 31, 2026
  url: https://www.insidermonkey.com/hedge-fund/situational+awareness+lp/1581/
- id: 2
  title: Wikipedia — Leopold Aschenbrenner (biography, OpenAI tenure, dismissal)
  url: https://en.wikipedia.org/wiki/Leopold_Aschenbrenner
- id: 3
  title: 'Aschenbrenner, "Situational Awareness: The Decade Ahead" (June 2024)'
  url: https://situational-awareness.ai/
- id: 4
  title: Fortune — "Why Leopold Aschenbrenner's AI hedge fund is betting big on power companies and Bitcoin
    miners" (March 5, 2026)
  url: https://fortune.com/2026/03/05/leopold-aschenbrenner-ai-hedge-fund-superintelligence-agi-power-companies-crypto-miners/
- id: 5
  title: Motley Fool — Top 7 holdings of Situational Awareness fund (April 25, 2026)
  url: https://www.fool.com/investing/2026/04/25/artificial-intelligence-ai-prodigy-leopold-aschenb/
- id: 6
  title: Pablo Stafforini — Notes on Situational Awareness LP (structure, lockups, copycat methodology)
  url: https://stafforini.com/notes/situational-awareness-lp/
- id: 7
  title: Latticework — "Situational Awareness Meets Value Investing"
  url: https://www.latticework.com/p/situational-awareness-meets-value
- id: 8
  title: HedgeFollow — Situational Awareness performance history (13F-proxy basis)
  url: https://hedgefollow.com/funds/Situational+Awareness/Performance-History
- id: 9
  title: Situational Awareness LP — About page
  url: https://situationalawarenesslp.com/about
:::
