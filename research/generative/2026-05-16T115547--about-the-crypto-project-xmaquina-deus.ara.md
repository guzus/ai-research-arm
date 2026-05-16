---
eyebrow: Project profile · Crypto × Humanoid Robotics · 2026-05-16
title: 'Inside the DEUS basket: what XMAQUINA holders actually own, 11 days before TGE'
deck: A first-principles audit of the underlying robotics companies, the regulated alternatives DEUS competes
  with, the legal wrapper that just got smaller, and the comp data that decides whether $0.06 at TGE is
  cheap or structurally indefensible.
lede: XMAQUINA's **$DEUS** token launches on Base in eleven days into a humanoid-robotics narrative whose
  underlying companies — Apptronik, Figure, 1X, Sanctuary, Agility, Neura, Unitree — have well-documented
  primary-source profiles, but whose accessibility to a $10M DAO treasury is mathematically narrow. This
  piece deliberately departs from prior coverage of the wrapper to audit what is actually inside the basket,
  what the regulated alternatives offer non-accredited retail today (KOID, HUMN, BOTZ, Forge), what shrank
  in the legal stack between October 2025 and January 2026, and what the Virtuals Titan launchpad comp
  set (ROBO -68%, AIXBT -97%, GAME -98%) implies for blended expected value. The thesis is real; the price
  has to clear a high comp-data hurdle.
stats:
- label: TGE
  value: May 27
  note: T-11 days · Base
- label: Voted-in holdings
  value: '1'
  note: Apptronik (BOT-1)
- label: $10M = % of one Figure round
  value: '0.026'
  unit: '%'
  note: of the $39B Series C
- label: Titan comp drawdowns
  value: '-68 to -97'
  unit: '%'
  note: ROBO · AIXBT · GAME
---

## 01. The basket today: one voted-in, six aspirational

Eleven days before the May 27, 2026 DEUS token generation event, the practical question for a buyer is narrow: what is actually inside the treasury that DEUS is supposed to represent? On the evidence trail a third party can independently walk today, the answer is **one** verifiably executed humanoid-OEM equity position (Apptronik, via BOT-1), **one** on-chain governance-approved allocation that has not been independently confirmed on the cap table (Sanctuary, via BOT-11), **one** additional governance-approved USDC transfer for 1X common shares (BOT-07), plus a marketing roadmap that names a further set of targets the DAO's roughly $10M raise cannot meaningfully buy into.[^3,1,7]

Start with what is unambiguous. The XMAQUINA DAO raised roughly $10 million from "nearly two thousand contributors" to fund what it calls the Robotics Capital Markets Protocol.[^3] The first acquisition proposal, BOT-1, passed Snapshot with 98.05% in favor and was framed by the project itself as the DAO's foundational position in Apptronik.[^1,2] A second proposal, BOT-07, was approved to deploy 800,000 USDC into common shares of 1X Technologies; this is on-chain governance evidence of intent, not yet confirmation that the shares appear on 1X's cap table.[^7] A third proposal, BOT-09, generated a thesis blog around Neura Robotics but is positioned as forward-looking research, not a closed transaction.[^8]

Then there is BOT-11, the proposal to acquire 13,000 shares of Sanctuary AI dated May 4, 2026. This is where the basket's most important disclosure asymmetry sits. The DAO Portal describes a generic mechanism of a "licensed intermediary and secured through escrow," but in primary sources reachable today there is no Sanctuary-side cap-table disclosure, no broker name, no escrow agent, and no settlement transaction hash that a third party can verify.[^10] A Snapshot vote is a signal of *authorization*; it is not, on its own, evidence of *settlement*. Until that gap closes, prudent underwriting treats BOT-11 as an intent-to-purchase, not as a confirmed holding.

The DEUS contract itself sharpens the picture. BaseScan shows 874,148,340.165 DEUS minted across 1,044 holders with `transferEnabled=false` as of today.[^4] CoinGecko reports a price of $0, on-chain liquidity of $110, and an FDV of $0, consistent with a pre-TGE token that has not been released for trading.[^5] The XMQ-02 vote allocates 110 million DEUS to a community pre-sale and earmarks 128 million DEUS plus 150,000 USDC for related TGE mechanics.[^9] In other words, the entire pricing question for May 27 is whether the market will value those tokens against the *actually-closed* assets in the treasury or against the *marketed* ones.

| Name | Status in treasury | Primary-source evidence today | Verifiability |
|---|---|---|---|
| Apptronik (BOT-1) | Voted in, project-confirmed as foundational holding | Snapshot 98.05% pass; DAO Portal blog[^1,2] | Strongest of the basket; size and price not publicly disclosed |
| 1X Technologies (BOT-07) | Governance-approved, 800,000 USDC for common shares | Third-party news summary of approved proposal[^7] | Authorization confirmed; settlement on 1X cap table not independently visible |
| Sanctuary AI (BOT-11) | Governance-approved, 13,000 shares dated May 4, 2026 | DAO Portal describes generic "licensed intermediary / escrow" — no Sanctuary, broker, or tx hash named[^10] | Not independently verifiable in primary sources |
| Neura Robotics (BOT-09 context) | Thesis blog, not a closed deal | "Is Neura the next big player?" DAO post[^8] | Aspirational |
| Figure AI | Named target on homepage | Homepage target list; Figure's own Series C closed at $39B post-money[^6,14] | Aspirational; size mismatch (see below) |
| Agility, AgiBot, Unitree, Sunday Robotics, Physical Intelligence | Named in homepage verticals / Northstar Council | Homepage[^6] | Aspirational |
| Munich robo-cafe + Robotico (DEUS Labs) | Disclosed operating asset ($1.285M physical) and 20% DAO equity in a spinout | DAO blog disclosures[^13,15] | Real but small relative to humanoid-OEM thesis |

The size mismatch is the single most important quantitative datapoint. Figure AI's most recent disclosed primary round was its Series C at a $39 billion post-money valuation.[^14] The entire $10 million XMAQUINA raise, even if deployed in one shot into a single Figure round, would equal roughly **0.026%** of that round's post-money — and that is before netting out the USDC already committed to BOT-07 and the operating expenses absorbed by Robotico and the Munich robo-cafe.[^3,7,13] The DAO can credibly become an anchor on a smaller, earlier name like Apptronik; it cannot credibly become a meaningful holder of the entire homepage list.

:::callout(kind=warn)
**What would weaken this read.** If Sanctuary AI, its transfer agent, or the named escrow intermediary publishes a cap-table or settlement confirmation for the 13,000 BOT-11 shares before TGE, the "one voted-in" framing tightens to "two voted-in, settled." Equally, if 1X confirms the BOT-07 800,000 USDC tranche on its cap table, that materially upgrades the verifiable basket. Both are easy disclosures to make and have not, as of 2026-05-16, been made.[^10,7]
:::

Why this matters: every later section of this article — the Apptronik deep-dive, the aspirational-basket reality check, the macro pressure-test, the regulated alternatives, the legal-stack review, the RCM Protocol delivery audit, and the exit math — is downstream of one question a buyer should answer before May 27. Is the price you are about to pay for DEUS anchored to the *verifiable* column of the table above, or to the *aspirational* column? The rest of this piece argues that the gap between those two columns is the entire investment debate.

## 02. Apptronik (BOT-1): the only voted-in position, by the numbers

Of the seven humanoid names XMAQUINA names on its homepage, exactly one — Apptronik — has actually been ratified through a Snapshot vote and funded from the DAO treasury, and on the underlying company Apptronik is the strongest single asset the basket could plausibly hold; the problem is not the company, it is the chain of inference between the company's last primary at a $5.3B post-money mark and the "+100% in a few months" headline XMAQUINA is using to sell DEUS into the May 27 TGE.

The objective Apptronik facts, in order of how much weight they should carry:

- Apptronik closed an oversubscribed Series A-X extension in February 2026, bringing total Series A capital to **over $935M** across the original $350M tranche and a $520M extension, with the extension "opened at a 3x multiple of the initial Series A valuation"[^17]. TechCrunch pegs the resulting post-money at **$5.3B**[^18].
- The original $350M Series A in February 2025 was co-led by B Capital and Capital Factory, with Google participating, and was earmarked for scaling Apollo manufacturing against "growing orders across priority verticals"[^16].
- Apptronik is one of only nine humanoid OEMs NVIDIA named as foundation partners for the GR00T / Isaac robotics platform — a non-trivial signal because it bundles model access, simulation tooling, and implicit GPU allocation[^20].
- The platform's R&D pedigree is real: Apollo is a direct commercial descendant of NASA's Valkyrie humanoid program, with the founding team having worked on Valkyrie at UT Austin's Human Centered Robotics Lab[^21].
- Apptronik signed a manufacturing partnership with Jabil in February 2025 to industrialize Apollo production and deploy units inside Jabil's own facilities — this is the single most credible "we can actually build these at scale" signal in the file[^23].
- Mercedes-Benz signed a commercial pilot agreement in March 2024 to test Apollo in manufacturing facilities[^19]. Mercedes is *both* an equity participant in the Series A and a customer, which means any "marquee customer list" reading must avoid double-counting the same relationship as independent validation.

That set of facts justifies treating Apptronik as a top-three Western humanoid platform alongside Figure and 1X. It does **not**, by itself, justify the headline number XMAQUINA is putting in front of retail.

:::callout(kind=warn)
**The "+100% in a few months" claim is structurally unverifiable.** XMAQUINA's blog and Snapshot record disclose that BOT-1 passed with 98.05% approval, but they do *not* publish the dollar size of the allocation, the share count acquired, the SAFE/equity instrument used, the price per share, or any preferred-stack terms[^27]. The "+100%" mark is therefore *internally consistent* with Apptronik's own disclosed 3x markup[^17] — and conservative relative to it — but it cannot be independently audited from primary sources. DEUS holders are being asked to underwrite a P&L claim whose denominator has not been published.
:::

A second qualification: the customer roster, as it actually exists in primary disclosures, is meaningfully thinner than the implication. The most-cited "GXO is using Apollo" line traces back to a June 2024 GXO press release that explicitly frames the relationship as a *multi-phase R&D initiative*, with GXO saying Apollo "has great potential to add value" — future-tense language, not a deployment[^24]. Compare this to GXO's *other* humanoid announcement from the same month: a multi-year commercial agreement with Agility Robotics' Digit, which GXO itself labeled as an "industry-first" Robotics-as-a-Service deal[^25]. The same logistics buyer, in the same month, distinguished between a commercial RaaS contract (Agility) and an R&D collaboration (Apptronik). Conflating those is the single most common error in humanoid investor decks, and XMAQUINA's homepage framing does not correct it[^26].

A third qualification, smaller but worth flagging: Apptronik has at points been mentioned in coverage of an Apple humanoid program, but the primary TechCrunch reporting on Apple's exploration of humanoids does *not* name Apptronik as the partner[^22]. Any "Apple is a customer" inference should be treated as rumor-driven until a primary disclosure exists.

For valuation context, Apptronik's $5.3B post-money[^18] sits at roughly one-seventh of Figure's $39B Series C mark from September 2025[^28]. A bull would call that a discount to the category leader; a bear would note that Figure has demonstrated commercial throughput with BMW that Apptronik has not yet matched, and that the gap is therefore at least partly earned. Either way, the read-through for DEUS holders is the same: BOT-1 is the basket's *real* position — the only one funded, the only one marked up, the only one with a defensible "+100%" floor — and almost the entire rest of the deck is aspiration. If the Apptronik thesis breaks, the entire DEUS humanoid narrative breaks with it, because there is no second leg yet. That concentration risk, more than any single Apptronik-specific concern, is what should govern position sizing into the 11-day TGE window.

## 03. The aspirational basket: what the six other names actually offer

Of the six other humanoid names XMAQUINA dangles in front of prospective DEUS holders, only **Agility** currently has a paying enterprise customer in production[^44,45], only **Sanctuary** appears in any treasury narrative the DAO has gestured at on-chain, and the strongest brand names — Figure at a ==$39B== post-money[^31] and 1X reportedly targeting ==$10B==[^37] — are mathematically out of reach for a treasury of roughly $10M.

The right way to read the "basket" pitch is as a valuation-weighted reality check. A DAO with ~$10M of deployable capital is not buying meaningful primary exposure to any frontier US humanoid program; it is buying, at best, a secondary scrap, an SPV slot, or a token-wrapped IOU. The table below tracks each name against current valuation, commercial status, and what $10M would actually represent at the most recent primary round.

| Name | Latest valuation / round | Commercial status (May 2026) | $10M as % of last round |
|---|---|---|---|
| **Figure** | $39B post-money, Series C, $1B+ raised, Sep 2025[^31] | Figure 03 unveiled Oct 2025 at $20K target list[^35]; BMW Spartanburg pilot disclosed but not a revenue contract[^34] | **0.026%** of one round |
| **1X** | $820M post-Series B (Jan 2024)[^36]; reported (unverified) SoftBank-led $10B talks late 2025[^37] | NEO consumer pre-order at $20K / $499 mo. (Oct 2025)[^38]; VP of AI Eric Jang departed Apr 2026[^39] | **0.10%** at the $10B target |
| **Sanctuary** | ~$140M cumulative (C$75.5M Series A 2022[^40], BDC/InBC strategic Jul 2024[^41]) | CEO Geordie Rose forced out + ~30 layoffs Nov 2024[^42]; CTO Suzanne Gildert departed Apr 2024[^43]; no paying enterprise contract disclosed | ~**7%** of cumulative raised — only practical primary entry, but distressed |
| **Agility** | $2.12B pre-money on $400M Series C-3 (2025)[^46] | Multi-year GXO RaaS contract since Jun 2024[^44]; **100,000+ totes moved by Digit** at GXO by Nov 2025[^45] | **0.47%** of pre-money |
| **Neura** | €120M Series B, Jan 2025[^47] | 3rd-gen 4NE-1 humanoid: ships **late 2026** per Automatica 2025 unveil[^48] — no commercial deployments | ~**7.7%** of last round (if EUR/USD parity-ish), but EU-domiciled |
| **Unitree** | ~$1.7B Series C+ (Jun 2025)[^49]; Shanghai IPO approval at $7B target (Mar 2026)[^50] | Quadrupeds in volume; humanoid (H1, G1) is research/demo SKU, not enterprise contract | **0.14%** of IPO target — but cap table closed to non-strategic foreign LPs at primary |

### Figure: a brand, not a buyable slot

Figure closed a Series C at **$39B post-money** in September 2025 on $1B+ raised, led by Parkway Venture Capital with participation from NVIDIA, Microsoft and Salesforce-adjacent funds[^31]. The company shipped its own Helix VLA stack (35 DoF, 200 Hz control, 500 hours of training data) in February 2025[^33], terminated its OpenAI partnership the same week[^32], and unveiled Figure 03 in October 2025 at a $20K target list price[^35]. The BMW Spartanburg pilot — Figure 02 supporting ~30,000 X3 vehicles over 1,250 hours / 11 months[^34] — is a pilot, not a paying contract of record. For XMAQUINA, $10M is **0.026%** of just the September 2025 round; secondary at $39B implies the DAO would own roughly 26 millionths of one of the most defensively-syndicated cap tables in the sector. There is no realistic path to a meaningful Figure position from this treasury size.

### 1X: NEO ships, but the AI org is bleeding

1X sat at ~$820M post-Series B as of January 2024 (Sacra reconstruction of the $100M round)[^36], and ==unverified: reported but not primary-source-confirmed== SoftBank-led talks at a $10B valuation in late 2025[^37]. NEO opened consumer pre-orders October 28, 2025 at $20,000 outright or $499/month with a $200 deposit[^38] — the first humanoid SKU with a real consumer price card. But VP of AI Eric Jang stepped down in April 2026[^39], removing the most public face of 1X's learning stack a month before DEUS's TGE. At the $10B target, $10M is **0.10%**; even if XMAQUINA could buy in, it cannot move the needle.

### Sanctuary: the only on-chain claim, and it is the weakest underlying

Sanctuary is the one name where XMAQUINA has gestured at an actual treasury holding, and the underlying has had a brutal seven months. After raising C$75.5M (US$58.5M) Series A in March 2022[^40] and topping up via BDC Capital / InBC in July 2024[^41] to roughly $140M cumulative, the company lost CTO and co-founder Suzanne Gildert in April 2024[^43], then forced out CEO and co-founder Geordie Rose with ~30 layoffs in November 2024[^42].

:::callout(kind=warn)
**Counterpoint — bear on DEUS's only verified humanoid name:** Sanctuary's leadership exodus plus the absence of a public BOT-11 verification of the on-chain position means the one humanoid exposure DEUS holders can plausibly point to is both operationally distressed and unverifiable from outside the foundation.
:::

### Agility: the only one with revenue, and the only realistic primary entry

Agility Robotics is the lone humanoid with a disclosed, paying enterprise customer in the US through November 2025: GXO Logistics signed a multi-year RaaS agreement in June 2024[^44], and Digit crossed **100,000+ totes moved** at the Spanx Flowery Branch facility by November 20, 2025[^45]. The $400M Series C-3 at $2.12B pre-money[^46] means $10M would be ~**0.47%** — the only line item in the basket where DEUS's treasury could plausibly clear a $5–10M SPV allocation and end up with a non-trivial cap-table position. If the basket has one real entry beyond Apptronik, it should be this one.

### Neura and Unitree: timing and access gaps

Neura Robotics' €120M Series B closed in January 2025 (not January 2024 as some XMAQUINA materials imply)[^47], and the third-generation 4NE-1 unveiled at Automatica 2025 is slated to ship in **late 2026**[^48] — meaning no enterprise deployments will exist at TGE. Unitree raised Series C+ at ~$1.7B in June 2025[^49] and received Shanghai IPO approval at a $7B target in March 2026[^50].

:::callout(kind=danger)
**Counterpoint:** the Unitree IPO is not investable for a Western DAO — A-share access for foreign offshore vehicles requires Stock Connect or QFII rails neither XMAQUINA nor its (currently-struck-off) foundation has disclosed, and Unitree's primary rounds have closed to non-strategic foreign LPs. $10M = **0.14%** of the IPO valuation in theory; in practice it is zero.
:::

**Why this matters for DEUS holders eleven days before TGE:** the basket pitch implies diversified exposure to seven humanoid names. The data says the DAO can credibly target *one* — Agility — through a secondary or SPV, holds an unverifiable position in *one* distressed name — Sanctuary — and is mathematically locked out of the four largest underlyings (Figure, 1X, Neura at the program stage, Unitree at the access stage). Pricing DEUS as if it tracks a basket of six investable humanoid winners is not supported by the cap-table math.

## 04. The macro pitch: how grounded is the trillion-dollar humanoid thesis?

The headline "trillion-dollar humanoid" forecasts that DEUS marketing leans on are 25-to-35-year terminal-value thought experiments stacked on residential adoption assumptions that none of the near-term shipment data supports; the only forecast grounded in observable supply-side capacity is Goldman's $38B by 2035, and even that pace assumes Tesla Optimus stops missing its own guidance by roughly 100% per year.

The first thing to do with a trillion-dollar TAM number is to ask what year it terminates in and what adoption curve it requires. When that arithmetic is unpacked, the four major sell-side forecasts split cleanly into two camps: one near-term and industrial, three long-dated and consumer-dependent.

:::callout(kind=info, label="Forecast map")
Major sell-side humanoid forecasts sort by terminal year: the only one inside a normal corporate-planning horizon is Goldman's.
:::

### The grounded number is smaller than people think

Goldman revised its humanoid TAM up six-fold to $38B by 2035[^51], which sounds large until it is contextualised: $38B is roughly three months of NVIDIA's current data-center revenue run-rate. The supporting unit forecast is 250,000 humanoids per year by 2030, "almost all of which would be for industrial use"[^52]. That single phrase quietly contradicts the Morgan Stanley and Citi terminal values, which only reach $5–7T if humanoids cross into homes, eldercare, and consumer services at scale. If Goldman is right that the 2030 mix is overwhelmingly factory floors, then the 2050 trillions are a second S-curve that has to start, not an extension of the first.

### The most-resourced program is missing its own guidance

The cleanest stress test for any humanoid forecast is Tesla Optimus, because it is the best-funded, most-vertically-integrated humanoid program in the West and has explicit annual production targets. On the Q4 2025 earnings call Elon Musk conceded that Optimus is "still R&D" and is "not in usage in factories in a material way"[^59] — after a year of public claims that thousands of units would be doing useful internal work by year-end. A roughly 100% miss against a one-year target from the program with the most capital and the most vertical integration is the single most important datapoint when evaluating Citi's 8.9-week-payback model[^56], which assumes a $35k bill of materials and reliable 24/7 labor substitution that no fielded unit can currently sustain.

### Where the units actually ship today

Bank of America projects 18,000 humanoid shipments in 2025 scaling to 10 million by 2035[^54] — an 88% CAGR that depends on whoever is shipping the 18,000. According to TrendForce / Omdia channel data, two Chinese vendors — AgiBot and Unitree — are on track to account for roughly 80% of 2026 humanoid shipments[^57]. A DAO domiciled in the Marshall Islands, marketing to Western retail, and depending on Apptronik (a US program with no consumer footprint) has no clean exposure to the supply that the unit-count forecasts are actually being filled by. The "basket exposure" thesis effectively asks holders to bet on the smaller, slower, more expensive half of the global market.

### Public markets are not pricing the terminal narrative

If institutional capital genuinely believed Morgan Stanley's $5T-by-2050 number, the publicly traded humanoid-adjacent vehicle would reflect it. The Global X Robotics & AI ETF (BOTZ) holds $3.82B in AUM and has compounded at 11.39% annually since 2016 inception — trailing the S&P 500 over the same window[^62]. Nine years of underperformance from a regulated, liquid product is a strong revealed preference: large pools of capital are not yet willing to pay an option premium for the trillion-dollar story, even with full access to the supply chain that a Marshall-Islands DAO cannot reach. Set against that, 2025 robotics venture funding hit a record $14B versus $8.2B in 2024[^58] — but VC pricing the option and public markets pricing the cashflows are very different signals, and only the latter is liquid.

:::callout(kind=warn)
**The bull case isn't dead — it's just on a longer clock.** Figure's 02 unit is doing real work assembling BMW X3s at the Spartanburg plant, with 1,250 documented production hours across 30,000 vehicles[^61], and NVIDIA's Physical AI framing at GTC 2025 has pulled real enterprise capex toward the category[^60]. The point is not that humanoids fail; it is that the grounded trajectory is Goldman's industrial $38B-by-2035, not Citi's residential $7T-by-2050. Those are different investments with different timelines and different winners.
:::

**Why this matters for DEUS holders:** the token's pitch leans on the 2050 trillion-dollar narratives, but the only forecast with observable shipment data behind it is a $38B industrial market 9 years out — and the basket's marquee holding (Apptronik) has to take share inside that smaller, slower, China-dominated reality before the terminal-value math ever comes into play.

## 05. The regulated alternatives DEUS must beat

XMAQUINA markets DEUS as the singular retail on-ramp to humanoid robotics, but as of May 2026 there are at least two US-listed ETFs purpose-built for the humanoid thesis, a Hong Kong-listed active fund, a $3.7B incumbent robotics ETF, and accredited-only secondary venues quoting actual Figure AI shares — meaning the "only way" claim collapses for public-equity exposure and survives only in the narrow, accreditation-gated pre-IPO lane.

The most direct contradiction is **KraneShares KOID**, launched 4 June 2025, which now holds $191.5M in AUM at a 0.69% net expense ratio and whose top weights — STMicroelectronics (2.89%), Harmonic Drive (2.88%), Hiwin (2.61%) — are precisely the actuator and silicon supply-chain names XMAQUINA's "Physical AI stack" vertical claims to deliver.[^66] Three weeks later, **Roundhill HUMN** launched (26 June 2025) at 0.75% expense, holding 43 names with Tesla (8.68%), UBTech (7.10%), and NVIDIA (4.15%) as anchors — including the pure-play Chinese humanoid maker UBTech that DEUS investors cannot reach directly.[^67] For investors content with a broader robotics aperture, Global X BOTZ has carried this exposure since 2016 at roughly $3.7–3.8B AUM and a 0.68% expense ratio.[^68] ARK's ARKQ adds another vector — Tesla at ~10%, plus Teradyne, AMD, Alphabet, and Palantir as adjacent AI-robotics plays.[^69] Asia-Pacific retail has its own ticker: **Global X 3139.HK**, an active EV & humanoid robot ETF listed in Hong Kong, currently $1.30M USD AUM at 0.75% OCF — small but live and HKEX-regulated.[^70]

| Vehicle | Launch | AUM | Fee | Min | Retail access | What you actually own |
|---|---|---|---|---|---|---|
| KraneShares KOID | Jun 2025 | $191.5M | 0.69% net | ~1 share | Open, US brokerage | Listed humanoid supply chain (STM, Harmonic, Hiwin) |
| Roundhill HUMN | Jun 2025 | n/d | 0.75% | ~1 share | Open, US brokerage | 43 names incl. Tesla, UBTech, NVIDIA |
| Global X BOTZ | 2016 | ~$3.7–3.8B | 0.68% | ~1 share | Open, US brokerage | Broad robotics & automation |
| Global X 3139.HK | 2024 | $1.30M | 0.75% | 1 board lot | Open, HKEX | Active EV + humanoid basket |
| Forge Global (Figure) | Live | n/a | ~5% spread | Accredited | Accredited only | Actual Figure AI common, 45-60d settle |
| EquityZen (Figure) | Live | n/a | Fund fees | Accredited | Accredited only | Fund-of-one wrapper on Figure shares |
| Republic Mirror Notes | 2025 | n/a | Per-deal | $50 | Accredited US | Debt note mirroring SPV economics |
| XMAQUINA DEUS | TGE May 27 2026 | $10M raised | Implicit | ~Gas fee | Open, on-chain | Governance token over DAO treasury |

On the pre-IPO side — where XMAQUINA's "only way" framing has more force — the gate is real but not absolute. **Forge Global**'s Figure AI page currently quotes a Forge Price of $174.00/share, implying a $34.22B post-money mark, with settlement in 45–60 days for accredited investors only. [^71]**EquityZen** runs a parallel fund-of-one product on the same name, also accredited-gated. [^72]**Republic**'s Mirror Token program (rSPAX, and most recently a Databricks note) extends the accredited tent down to a $50 minimum via debt instruments referencing SPV economics — but no Figure AI Mirror Note has been issued, and the structure remains a debt claim against RepublicX LLC, not equity in the underlying.[^73,77] The SEC's accredited-investor definition still demands $1M net worth (excluding primary residence) or $200K/$300K income, so a non-accredited US retail user is genuinely locked out of all three Figure-specific paths.[^74] Backed Finance's tokenized equities (bTSLA, bGOOGL, etc.) operate under the Swiss DLT Act and are 1:1 with listed shares — useful for Tesla exposure on-chain, but Backed explicitly only tracks listed names, so Figure is unreachable there too.[^75]

The quantitative comparison is brutal at the retail unit-of-account level. With $10M cumulatively raised, XMAQUINA's entire treasury is roughly 1% of Figure's last primary round.[^76] Its disclosed humanoid exposure is dominated by a single $800K 1X SAFE cited via the BOT-07 reference.[^78] A retail buyer deploying $1,000 into DEUS at TGE captures a fractional governance claim on a treasury whose Figure-equivalent exposure is approximately zero; the same $1,000 buys roughly 5–6 KOID shares delivering immediate, daily-marked, prospectus-disclosed exposure to the listed humanoid supply chain at a 0.69% drag.[^66]

:::callout(kind=warn)
**Fair counterpoint:** ETFs do not give pre-IPO equity exposure to Apptronik, Figure, or 1X — they own listed suppliers, which is a different cash flow profile. The Forge/EquityZen/Republic pre-IPO stack requires accreditation. If — and only if — XMAQUINA ships a working SubDAO/RCM Protocol structure that lets non-accredited retail share economically in a private-company SPV without violating securities law, it is a genuinely novel product. As of 11 days before TGE, that mechanism is unaudited, unlaunched, and legally untested.
:::

**Why this matters:** the "only way" pitch is the load-bearing element of DEUS's premium-to-NAV story. The moment a non-accredited retail buyer accepts that KOID and HUMN already capture the listed humanoid supply chain at 0.7% all-in — and that the accredited pre-IPO routes already reach actual Figure AI at a daily-quoted $34B mark — the question stops being "is DEUS the only way?" and becomes "what does DEUS deliver that KOID, HUMN, Forge, and Republic don't, net of token volatility, governance friction, and the absence of a working SubDAO?" Eleven days before TGE, that answer is still a roadmap.

## 06. The legal stack just got smaller

The legal wrapper XMAQUINA points to in marketing — a Singapore Foundation parent, a Marshall Islands DAO LLC, and per-asset SPVs — got materially smaller between October 2025 and January 2026: the Singapore vehicle that gives the project its public name was struck off the ACRA register on 9 October 2025[^81], a ==unverified: secondary reference to a Cayman foundation alternative in the project's broader GitBook materials==[^93] has surfaced but is not corroborated in the canonical docs.xmaquina.io legal-structure page[^94], and the remaining offshore stack now has to defend itself against a United States enforcement posture that, in the same window, expanded rather than contracted with respect to tokenized equity references[^86].

Start with the entity that marketing actually names. "XMAQUINA Foundation Ltd." appears on the ACRA mirror as UEN `202422336Z`, incorporated 4 June 2024 as a Public Company Limited by Guarantee, and recorded as struck off on 9 October 2025[^81]. ==unverified: the struck-off date is sourced from a secondary ACRA mirror (recordowl.com), not a direct ACRA Bizfile pull — readers should re-query ACRA before relying on the exact date.== The entity form matters independently of liveness: a Singapore Company Limited by Guarantee has no share capital and is structurally prohibited from distributing surplus to its members[^82]. Even in the world where the Foundation is restored, the wrapper marketing is pointing at cannot, by statute, route economic value back to DEUS holders — which is consistent with the project's own "governance only, no profit rights" framing[^94] but inconsistent with the basket-exposure pitch.

Underneath the (struck-off) Foundation sits the Marshall Islands DAO LLC layer. MIDAO's own framework documents two paths: a Non-Profit DAO LLC that, like the Singapore CLG, cannot distribute to members; and a For-Profit DAO LLC that is subject to a 3% Marshall Islands Gross Revenue Tax and to Beneficial Ownership Information Report (BOIR) disclosure for any party holding 25% or more of governance rights[^83]. Both branches collide with crypto marketing language: the non-profit branch cannot pay holders, and the for-profit branch is taxable and pseudonymity-incompatible above the 25% threshold. There is no third door labeled "decentralized and distributing and anonymous."

The enforcement backdrop hardened in two steps. In *CFTC v. Ooki DAO*, the Northern District of California entered a default judgment of **USD 643,542** against an unincorporated DAO, holding that a DAO is a "person" under the Commodity Exchange Act and that controlling token-holders can be reached directly[^84]. An RMI DAO LLC is meaningfully better positioned than Ooki's unincorporated association — it has legal personality and a registered agent — but the doctrinal point (that offshore form does not block US jurisdiction over US-touching conduct) bleeds across. In parallel, Judge Failla's March 2024 ruling in *SEC v. Coinbase* let the SEC proceed on the theory that thirteen named tokens remained securities in secondary-market trading, not only at issuance[^85].

:::callout(kind=danger)
**The single most important new legal fact for DEUS holders.** On 28 January 2026, the SEC's Divisions of Corporation Finance, Trading and Markets, and Investment Management issued a joint staff statement on tokenized securities. The core line is that a token issued by a third party that *references* an underlying security may itself be a separate security — and may not inherit any exemption the underlying enjoyed[^86]. A "basket token" whose value tracks SPV-held equity in private robotics issuers is exactly the structure the statement is describing.
:::

The defenses XMAQUINA-style structures usually invoke are weaker than they read. Regulation S permits offshore offerings to non-US persons but imposes a one-year distribution compliance period and prohibits "directed selling efforts" into the United States — a standard that English-language Twitter/X marketing and US-facing Discord onboarding strain against[^92]. The "sufficiently decentralized therefore not a security" idea traces to William Hinman's 2018 speech, which was explicitly his personal view and was never codified[^89]. The cleanest US safe harbor proposal — Commissioner Hester Peirce's 2020 Token Safe Harbor — is a speech, not a rule; it was never adopted by the Commission[^88]. The one path that has actually worked end-to-end in the United States is INX Limited's 2020 F-1 registration as a security token, which required full registered-offering compliance rather than an exemption[^91].

There is a real counterpoint and DEUS holders should hold it in mind. SEC leadership rotated in 2025; Commissioner Peirce now chairs the Crypto Task Force, and the January 2026 statement is staff-level guidance, not a Commission rule or an enforcement action — staff statements can be withdrawn faster than rules can be repealed[^86]. The Token Safe Harbor concept could plausibly be revived in some form under a friendlier Commission[^88]. The Singapore Foundation can be re-incorporated, or replaced by any alternative offshore wrapper the project may already be quietly maintaining; a struck-off CLG is a paperwork problem, not necessarily a project-ending one. And the European MiCA regime, fully in force across all titles since 30 December 2024, gives non-US issuers a coherent jurisdiction to operate from even if US distribution is foreclosed[^87]. Finally, an attestation (not an audit) of off-chain SPV holdings under AICPA standards is a real, available control if the project chooses to commission one[^90].

For DEUS holders eleven days from TGE, the practical translation is narrow and concrete. The named legal parent is currently struck off in the registry that names it; the surviving DAO-LLC layer is either non-distributing or taxable-and-disclosed; the standard offshore defenses (Reg S, Hinman, Peirce safe harbor) are weaker than their reputation; and the most relevant new SEC statement, issued less than four months ago, directly targets third-party tokens that reference underlying equity. None of that makes DEUS uninvestable, but it does mean the legal-wrapper diagram on the marketing site is doing meaningfully less work than it was when the round was first pitched, and any size taken before TGE should be sized to the wrapper that actually exists on 16 May 2026 rather than the one in the deck.

## 07. RCM Protocol: governance-approved, on schedule, no code

The Robotic Capital Markets (RCM) Protocol is the load-bearing pillar of XMAQUINA's entire investment thesis — it is the mechanism by which illiquid SPV-held claims on private robotics companies are supposed to become tradeable on-chain — yet four months before its stated Q3 2026 launch, there is no public code, no audited contract, no disclosed broker-dealer or ATS partner, and no technical specification beyond a marketing overview.[^96]

The Q3 2026 timeline is from XMAQUINA's own roadmap, where RCM Protocol is the only major item marked *Pending* against roughly twelve completed predecessors (Genesis Auctions, DEUS token, xDEUS staking, OFT cross-chain, DAO Portal).[^97] Funding for RCM development was approved via the XMR-03 governance vote with ~9M votes behind Option 2 (~61% of participating voting power), so the project is both scheduled and bankrolled by the DAO it is meant to serve.[^101] Phemex's January 29, 2026 launch coverage explicitly characterized RCM as architecturally aligned with Pump.fun and Virtuals — permissionless launchpad mechanics applied to robotics SubDAOs — which is the analytic comp that should be doing the work in any honest assessment.[^102]

### What public artifacts actually exist

The XMAQUINA-DAO GitHub organization has exactly three public repositories: a docs site in MDX, `deus-solana-oft` (Rust, three commits, last touched March 7, 2026), and a fork of `assets-info`. None contains the strings *rcm*, *subdao*, *auction*, *spv*, or *orderbook* in its name or description.[^98] The one non-trivial repo, the Solana OFT, is a *reproducibility* artifact for an already-deployed token — "the minimal source code required to reproduce a deterministic build of the DEUS OFT program deployed on Solana"[^99] — not in-flight protocol engineering. The audits page tells the same story from the other direction: only two contracts have been audited (Genesis Auction Swap and DEUS Token), both by Hashlock, with the most recent engagement dated October 2024.[^100] Eighteen months of audit silence for a protocol pitched to launch in four.

### The legal architecture problem

The most consequential single sentence in the RCM documentation is the design choice that "all robotics SubDAO markets are paired against DEUS within DEX pools"[^96] — meaning that claims ultimately backed by SPV-held private equity (e.g., the Apptronik exposure) would trade against a governance token inside an AMM. Architecturally that is Pump.fun applied to securities,[^102] and the comp is honest only if you accept that Pump.fun and Virtuals have *zero* regulated-security nexus while RCM, by its own marketing copy, explicitly does. Comparable regulated venues for tokenized private equity — tZERO, Securitize, INX, Tokeny — all required some combination of FINRA-registered broker-dealer, ATS, or MiFID II venue licensing. None of those credentials, or the names of any U.S. or EU partner that holds them, appear anywhere in XMAQUINA's published materials. The RCM docs concede the design is "under active legal structuring."[^96]

:::callout(kind=warn)
**SubDAO-on-DEX, designed-in:** DEUS Labs is described as "an independent SubDAO under its own mandate, with oversight from the XMAQUINA DAO."[^103] If the first live SubDAO market pairs a claim on Apptronik economics against DEUS in a permissionless pool, the design question is not *whether* this is an unregistered offering of a security in the United States — it is *which* jurisdiction's enforcement arrives first. The Aspecta pre-market IOU venue[^104] is the closest live comp and notably does not custody equity claims; it trades vesting-rights IOUs. RCM, as written, custodies the equity.
:::

### Delivery scorecard, honestly

| Roadmap item | Status | Engineering complexity |
|---|---|---|
| Genesis Auction | Shipped, audited | Low (fixed-price swap) |
| DEUS token + xDEUS staking | Shipped, audited | Low (ERC-20 + staking) |
| LayerZero OFT to Solana | Shipped, reproducible build | Medium (integration) |
| DAO Portal | Shipped | Low (frontend) |
| RCM Protocol (SubDAO launch + AMM + SPV nexus + legal wrapper) | Pending, no code, no audit, no named regulated partner[^98,100] | High (novel securities + smart-contract + cross-border) |

XMAQUINA *has* shipped on schedule before — roughly twelve of thirteen prior roadmap items are marked complete[^97] — and a team that ships earns the benefit of some doubt on the next item. It is entirely plausible that RCM engineering lives in private repositories (most regulated-securities work does), that an ATS or broker-dealer partner is under NDA until announcement, and that the "marketing overview only" public posture[^105] is a deliberate legal-comms choice rather than evidence of vapor. The Hashlock relationship is established and could be re-engaged on weeks of notice. But the previously shipped items are governance and treasury primitives — categorically lower-complexity than the legal-plus-smart-contract-plus-AMM stack RCM requires, and the slope from "we deployed an OFT" to "we operate a tokenized-PE secondary market" is not linear.

**Why this matters for the trade:** the entire upside case for buying DEUS pre-TGE is that *illiquid SPV claims become liquid* via RCM. If RCM slips two quarters, or launches without U.S. participation, or launches in a form that regulators promptly enjoin, the basket reverts to what it materially is today — a closed-end fund of pre-IPO robotics names with no exit ramp before the underlying companies themselves go public. The four-months-no-code datapoint is not dispositive, but in a market that has been trained by Worldcoin, Friend.tech, and a dozen launchpad protocols to discount roadmap promises, it is the single most underweighted risk in the current DEUS narrative.

## 08. Exit math: the Virtuals base rate vs. the IPO bull case

At $0.06 per token, $60M FDV, and roughly $12M circulating market cap against ~$1M of paired DEX liquidity, DEUS launches into a comp set whose realized 12-month drawdown distribution is brutally one-sided — and the only scenarios that recover a positive expected value require both a public-market catalyst (Figure or Apptronik IPO) inside 18–24 months *and* RCM's "liquid claims" mechanism shipping and surviving securities review, which on probability-weighted basis still leaves blended EV materially negative over the 6–12 month horizon that matters to TGE participants.

Start with the base rate, because it is the part of the problem that is not subjective. The Virtuals Titan launchpad has now produced a multi-token sample: VIRTUAL itself is down ~85% from its January 2025 ATH[^106], AIXBT is down 96.7% from ATH[^107], GAME by Virtuals is down ~97.9%[^108], and Fabric Protocol's ROBO — the most direct comp because it is the first Titan launch and shares the robotics narrative — is down 68.1% in roughly ten weeks since its own launch[^109]. That is four for four with drawdowns greater than 68%, and three of four greater than 85%. Titan-tier launches are designed around a $50M minimum valuation with only $500K USDC of paired liquidity required[^110]; DEUS launches with a $1M+ TVL pool[^111], which is better than the floor but still thin against a $12M circulating cap and the 67% supply that linearly vests over 12 months[^111]. Token unlock cliffs historically apply downward price pressure roughly 90% of the time[^112], and DEUS will be unlocking continuously for a full year before any consensus IPO catalyst even arrives.

Now the catalyst side. The bull case is not fantasy — it is timing-constrained. Apptronik raised $403M in February 2026 at a $5.3B post-money valuation[^114], roughly tripling its valuation in twelve months, and Figure AI's IPO consensus across pre-IPO trackers is 2027–2028[^113]. The mechanism that would translate either event into DEUS price action is the RCM "liquid claims" structure, which mirrors the pre-IPO token model where holders only receive payout 6 months after the IPO settles[^117]. Even in the optimistic scenario — Figure files Q4 2027, prices Q1 2028, payout Q3 2028 — that is 28 months from TGE during which DEUS holders absorb continuous vesting dilution against a $1M LP, with no guarantee the SEC blesses tokenized claims on a U.S.-domiciled private company. For context on what DEUS is competing for attention against: the entire CoinGecko Robotics category sits at $773M total market cap, dominated by VIRTUAL itself at $472M[^116] — meaning even a 10x from $60M FDV would put DEUS at #2 in the category, behind only the launchpad token itself.

:::callout(kind=warn)
**Three-scenario probability-weighted return, 6–12 month horizon from TGE (May 27, 2026):**

| Scenario | Probability | Comp anchor | 180-day FDV | Return vs. $60M TGE | Contribution to EV |
|---|---|---|---|---|---|
| **Bear** — DEUS tracks Titan median | 60% | ROBO -68%, AIXBT -97%, GAME -98%[^107,108,109] | $10–20M | -70% to -85% | -45.0% |
| **Base** — narrative holds, treasury delivers, no IPO | 30% | VIRTUAL itself -85% but still $472M cap[^106,116] | $30–50M | -15% to -50% | -9.0% |
| **Bull** — Figure/Apptronik IPO catalyst priced in early | 10% | Apptronik 3x in 12mo[^114]; pre-IPO mirror tokens[^117] | $200–500M | +230% to +730% | +40.0% |
| **Blended expected value, 6–12 months** | **-14%** |  |  |  |  |
:::

The arithmetic is the point. Even granting a generous 10% probability that the bull case lands inside the relevant window — which itself requires the IPO timing to compress from 2027–2028 consensus[^113] down into something the market can price in within 6–12 months of TGE — the bear case is so heavily anchored by the four-comp Titan distribution that EV stays negative. To flip EV positive at these probabilities, the bull-case FDV would need to clear roughly $700M, which would make DEUS larger than every robotics token on CoinGecko except VIRTUAL itself[^116]. To flip EV positive at $400M bull FDV, the bull probability needs to roughly double to ~20% — a defensible view only if you assume RCM ships, survives review, and one of the two IPOs prices earlier than consensus, all conditional on each other.

**Counterpoint worth taking seriously:** the IPO catalyst is genuinely real, not hypothetical. Apptronik's valuation tripled in twelve months on private-market evidence alone[^114], and the XMAQUINA team did raise $10M from credible robotics-adjacent backers to build exactly this infrastructure[^118] — meaning the bull-case capital and intent are present in a way that pure-meme Titan launches like AIXBT never had. Small-cap mispricings *do* resolve when narrative aligns with primary-market catalysts, and if RCM mirror tokens become the standard mechanism for retail exposure to humanoid IPOs, the optionality is convex. The honest pushback to the table above is that 10% may understate the bull probability if you weight team quality and primary-market signal more than launchpad comps.

**Why this matters:** the 11 days before TGE are the only window in which DEUS exposure can be sized against the comp data rather than against post-launch narrative momentum — and the comp data says the marginal Titan participant has been wrong, badly, four times out of four.

## 09. What could falsify this bear take

Almost every section above is built around a primary-source-anchored bear or skeptical reading. That bias is deliberate — analyst-grade research should lead with the falsification risk, not the marketing — but it carries a corresponding obligation: spell out what would invalidate the bear case, specifically and in advance. Five things would.

**One — Apptronik alone is enough.** The treasury's single funded position is in a company that just tripled its private mark to $5.3B in twelve months[^18], has a Jabil manufacturing relationship designed for volume[^23], and is a foundation partner on NVIDIA's GR00T stack[^20]. If Apptronik IPOs by 2027 at a $20–30B mark — entirely plausible given the trajectory — and XMAQUINA's BOT-1 stake turns out to be ~$2–5M of cost basis (the unverifiable number), that single position could mark at $10–25M against a $60M FDV. The basket framing is shaky; the concentration on one excellent company is not.

**Two — RCM ships on or near schedule.** The team has cleared roughly twelve of thirteen prior roadmap items[^97], and the no-public-code finding[^98] may simply reflect that securities-adjacent work lives in private repositories under NDA — most regulated-tokenization work does. If RCM lands in Q3 or Q4 2026 with a registered ATS or non-US regulated-venue partner, the legal-architecture critique in §07 inverts and DEUS gets a re-rating event the comp set never had. The four-month window is the test.

**Three — the Singapore Foundation re-incorporates or the Cayman replacement formalizes.** A struck-off CLG is a paperwork problem, not a fatal one. There are ==unverified secondary references==[^93] to an alternative offshore wrapper in the project's broader materials, suggesting a replacement entity may already be operational. If the project publishes a clean updated legal-structure document before TGE — naming the live foundation, the SPV custodians, and the audit/attestation partner — the §06 critique collapses to a narrow "verify, then trust" framing.

**Four — the SEC posture rotates further than the January 2026 staff statement suggests.** The Peirce-chaired Crypto Task Force could, in 2026, propose rules that explicitly carve out governance tokens over RWA baskets from securities classification. Staff statements are not rules[^86]; a Commission-level shift would re-open distribution channels and exchange listings that the current posture closes. The risk is asymmetric the other way too — the same staff could escalate to enforcement — but the political read of the current Commission is friendlier than 2023's.

**Five — a humanoid IPO catalyst arrives faster than the 2027–2028 consensus.** Figure has the capital and the product line; Apptronik has the manufacturing relationship; either could file in 2026 if the bank window opens. The 28-month catalyst horizon in §08 collapses to ~12 months if Brett Adcock or Jeff Cardenas decides to test public markets early. The IPO does not need to actually price for DEUS to re-rate — a confidential S-1 filing and analyst day in Q4 2026 would do most of the work.

:::callout(kind=info)
**The honest probabilistic update.** The bear case in §08 assigns ~10% to the bull scenario. If you weight team-and-primary-market signal heavily — Apptronik's 3x markup, the $10M raised from real names, twelve of thirteen prior roadmap items shipped — a defensible bull probability is closer to 15–20%, which is enough to flip blended expected value back to roughly flat at a $400M bull FDV. The bear case is not a guarantee. It is the default outcome conditional on the Titan launchpad base rate, the four-months-no-RCM-code datapoint, and the absence of a verified BOT-11 settlement. Each of those can change before May 27 or within the year that follows, and a buyer should track them in that order.
:::

The reason the article does not write itself as a bull case is that, today, the bear case is the one anchored in primary-source data and the bull case is the one anchored in trajectories and intent. Those are not the same epistemic objects. Eleven days before TGE, the appropriate posture is sized to the data that exists, not the one that hasn't been published yet — and with one of the five inversions above, the calculus changes.

---

## 10. References

:::references
- id: 1
  title: snapshot.box · XMAQUINA-DAO Snapshot space
  url: https://snapshot.box/#/s:xmaquina-dao.eth
  source: BOT-1 Apptronik proposal passed with 98.05% approval
- id: 2
  title: XMAQUINA blog · Introducing the DAO Portal
  url: https://www.xmaquina.io/blog/introducing-the-xmaquina-dao-portal
  source: BOT-1 framed as foundational; generic "licensed intermediary and escrow" mechanism described
- id: 3
  title: XMAQUINA blog · $10M raised
  url: https://www.xmaquina.io/blog/10m-raised-to-reclaim-the-robotics-capital-markets
  source: $10M cumulative, ~2,000 contributors (Jan 12, 2026)
- id: 4
  title: BaseScan · DEUS contract
  url: https://basescan.org/token/0x940A319B75861014A220D9c6c144d108552B089B
  source: '874,148,340 DEUS minted, 1,044 holders, transfers disabled (snapshot 2026-05-16)'
- id: 5
  title: CoinGecko · XMAQUINA
  url: https://www.coingecko.com/en/coins/xmaquina
  source: price $0, liquidity $110, FDV $0 pre-TGE
- id: 6
  title: xmaquina.io · homepage
  url: https://www.xmaquina.io/
  source: target verticals and Northstar Council named list
- id: 7
  title: Bitget News · BOT-07 (1X $800K USDC)
  url: https://www.bitget.com/news/detail/12560605058339
  source: approved allocation summary
- id: 8
  title: XMAQUINA blog · Is Neura the next big player?
  url: https://www.xmaquina.io/blog/is-neura-robotics-the-next-big-player-in-humanoids
  source: BOT-09 Neura thesis post
- id: 9
  title: Phemex · XMAQUINA TGE approval
  url: https://phemex.com/news/article/xmaquina-approves-deus-token-generation-event-with-110-million-deus-for-presale-42899
  source: '128M DEUS + $150K USDC allocations, 110M pre-sale tranche'
- id: 10
  title: XMAQUINA blog · DAO Portal (BOT-11 verification gap)
  url: https://www.xmaquina.io/blog/introducing-the-xmaquina-dao-portal
  source: generic escrow mechanism described, no Sanctuary-side cap-table confirmation or tx hash
- id: 13
  title: XMAQUINA blog · Munich robo-cafe and Robotico disclosures
  url: https://www.xmaquina.io/blog/10m-raised-to-reclaim-the-robotics-capital-markets
- id: 14
  title: Figure AI · Series C announcement
  url: https://www.figure.ai/news/series-c
  source: $39B post-money, $1B+ raised (Sep 16, 2025)
- id: 15
  title: XMAQUINA · DEUS Labs SubDAO page
  url: https://www.xmaquina.io/deus-labs
- id: 16
  title: GlobeNewswire · Apptronik $350M Series A. (Feb 13, 2025)
  url: https://www.globenewswire.com/news-release/2025/02/13/3025687/0/en/Apptronik-Raises-350-Million-to-Scale-Production-of-AI-Powered-Humanoid-Robots-and-Meet-Significant-Customer-Demand.html
- id: 17
  title: GlobeNewswire · Apptronik $935M Series A close
  url: https://www.globenewswire.com/news-release/2026/02/11/3236352/0/en/apptronik-closes-over-935-million-series-a-with-new-520-million-extension-round.html
  source: '"3x multiple of the initial Series A valuation" (Feb 11, 2026)'
- id: 18
  title: TechCrunch · Apptronik $5.3B post-money
  url: https://techcrunch.com/2026/02/11/humanoid-robot-startup-apptronik-has-now-raised-935m-at-a-5b-valuation/
- id: 19
  title: PR Newswire · Apptronik–Mercedes-Benz pilot. (Mar 15, 2024)
  url: https://www.prnewswire.com/news-releases/apptronik-and-mercedes-benz-enter-commercial-agreement-that-will-pilot-apptroniks-apollo-humanoid-robot-in-mercedes-benz-manufacturing-facilities-302089972.html
- id: 20
  title: NVIDIA Newsroom · GR00T / Isaac launch
  url: https://nvidianews.nvidia.com/news/foundation-model-isaac-robotics-platform
  source: '9 humanoid OEM foundation partners'
- id: 21
  title: NASA Spinoff · Apollo / Valkyrie heritage
  url: https://spinoff.nasa.gov/Humanoid_Robots_Assist_Assembly_Lines
- id: 22
  title: TechCrunch · Apple humanoid rumor
  url: https://techcrunch.com/2025/02/12/apple-is-reportedly-exploring-humanoid-robots/
  source: Apptronik not named as partner
- id: 23
  title: Jabil IR · Apptronik manufacturing partnership. (Feb 25, 2025)
  url: https://investors.jabil.com/news/news-details/2025/Apptronik-and-Jabil-Collaborate-to-Scale-Production-of-Apollo-Humanoid-Robots-and-Deploy-in-Manufacturing-Operations/default.aspx
- id: 24
  title: GXO · Apptronik R&D initiative. (Jun 2024) — explicitly R&D, not commercial
  url: https://gxo.com/news_article/gxo-announces-multi-phase-r-and-d-initiative-with-apptronik/
- id: 25
  title: GXO · Agility commercial RaaS
  url: https://gxo.com/news_article/gxo-signs-industry-first-multi-year-agreement-with-agility-robotics/
  source: industry-first humanoid RaaS (Jun 27, 2024)
- id: 26
  title: xmaquina.io · homepage humanoid framing
  url: https://www.xmaquina.io/
- id: 27
  title: Snapshot · XMAQUINA BOT-1 vote disclosure
  url: https://snapshot.box/#/s:xmaquina-dao.eth
  source: does not include dollar size, share count, or instrument terms
- id: 28
  title: Figure AI · Series C comp ($39B)
  url: https://www.figure.ai/news/series-c
- id: 31
  title: Figure AI · Series C ($39B)
  url: https://www.figure.ai/news/series-c
- id: 32
  title: Brett Adcock · X post terminating OpenAI partnership. (Feb 4, 2025)
  url: https://x.com/adcock_brett/status/1886860098980733197
- id: 33
  title: Figure AI · Helix VLA announcement. (Feb 20, 2025)
  url: https://www.figure.ai/news/helix
- id: 34
  title: Figure AI · BMW Spartanburg pilot
  url: https://www.figure.ai/news/production-at-bmw
  source: '30k vehicles, 1,250 hours'
- id: 35
  title: TIME · Figure 03 reveal
  url: https://time.com/7324233/figure-03-robot-humanoid-reveal/
  source: $20K target list (Oct 9, 2025)
- id: 36
  title: '1X · Series B announcement'
  url: https://www.1x.tech/discover/1x-secures-100m-in-series-b-funding
  source: $100M (Jan 11, 2024)
- id: 37
  title: Crunchbase News · 1X SoftBank investment context
  url: https://news.crunchbase.com/ai/softbank-humanoid-robotics-investment-1x-tech/
  source: original linked article documents earlier 1X funding; the $10B SoftBank-led talks figure circulated
    in late-2025 secondary press but is not confirmed at this URL — treat as unverified
- id: 38
  title: '1X · NEO consumer launch'
  url: https://www.1x.tech/discover/neo-home-robot
  source: $20K / $499/mo, $200 deposit (Oct 28, 2025)
- id: 39
  title: Humanoids Daily · Eric Jang departs 1X. (Apr 15, 2026)
  url: https://www.humanoidsdaily.com/news/eric-jang-steps-down-as-vp-of-ai-at-1x-technologies
- id: 40
  title: Sanctuary AI · Series A
  url: https://www.sanctuary.ai/blog/sanctuary-ai-closes-75-million-series-a-funding
  source: C$75.5M (US$58.5M), Mar 2, 2022
- id: 41
  title: PR Newswire · Sanctuary AI BDC/InBC strategic financing. (Jul 3, 2024)
  url: https://www.prnewswire.com/news-releases/sanctuary-ai-announces-strategic-financing-from-bdc-capital-and-inbc-302188928.html
- id: 42
  title: BCTechnology · Sanctuary CEO Geordie Rose departure + layoffs. (Nov 12, 2024)
  url: https://www.bctechnology.com/news/2024/11/12/Sanctuary-AI-Announces-Leadership-Update-Company-Co-Founder-Geordie-Rose-Leaving-CEO-Position.cfm
- id: 43
  title: BCTechnology · Sanctuary CTO Suzanne Gildert departure. (Apr 10, 2024)
  url: https://www.bctechnology.com/news/2024/4/10/Sanctuary-AI-CEO-Geordie-Rose-Releases-Company-and-Team-Update-Announces-Departure-of-Company-Co-Founder-and-CTO-Suzanne-Gildert.cfm
- id: 44
  title: GXO · Agility industry-first commercial RaaS
  url: https://gxo.com/news_article/gxo-signs-industry-first-multi-year-agreement-with-agility-robotics/
- id: 45
  title: Agility Robotics · Digit moves 100K+ totes at GXO. (Nov 20, 2025)
  url: https://www.agilityrobotics.com/content/digit-moves-over-100k-totes
- id: 46
  title: SiliconANGLE · Agility $400M Series C-3 at $2.12B pre-money
  url: https://siliconangle.com/2025/04/01/humanoid-robot-creator-agility-robotics-targets-400m-funding-round/
- id: 47
  title: Neura Robotics · €120M Series B. (Jan 2025)
  url: https://neura-robotics.com/neura-robotics-secures-euro-120-million-series-b/
- id: 48
  title: Robotics 24/7 · Neura 4NE-1 third gen, ships late 2026
  url: https://www.robotics247.com/article/automatica-2025-neura-robotics-unveils-3rd-generation-4ne1-humanoid
- id: 49
  title: '36Kr · Unitree Series C/C+ at ~$1.7B. (Jun 19, 2025)'
  url: https://eu.36kr.com/en/p/3344368397190018
- id: 50
  title: Caproasia · Unitree Shanghai IPO approval at $7B target. (Mar 23, 2026)
  url: https://www.caproasia.com/2026/03/23/china-robotics-startup-unitree-robotics-receives-approval-for-shanghai-ipo-to-raise-610-million-previous-reported-7-billion-valuation-for-ipo-raised-series-c-funding-at-1-7-billion-valuation-in-2/
- id: 51
  title: Goldman Sachs · Humanoid robot TAM $38B by 2035. (revised up 6x)
  url: https://www.goldmansachs.com/insights/articles/the-global-market-for-robots-could-reach-38-billion-by-2035
- id: 52
  title: Goldman Sachs · 250k units/yr by 2030, "almost all industrial"
  url: https://www.goldmansachs.com/insights/articles/the-global-market-for-robots-could-reach-38-billion-by-2035
- id: 53
  title: Morgan Stanley · $5T humanoid market by 2050. (Apr 29, 2025)
  url: https://www.morganstanley.com/insights/articles/humanoid-robot-market-5-trillion-by-2050
- id: 54
  title: Bank of America · Humanoid Robots
  url: https://institute.bankofamerica.com/content/dam/transformation/humanoid-robots.pdf
  source: '18k 2025 to 10M 2035 (Apr 29, 2025) [PDF]'
- id: 55
  title: Bank of America · Physical AI Part 2
  url: https://institute.bankofamerica.com/content/dam/transformation/physical-ai-part-2.pdf
  source: '3B units by 2060 (Mar 12, 2026) [PDF]'
- id: 56
  title: Citi · The Rise of AI Robots
  url: https://www.citigroup.com/global/insights/the-rise-of-ai-robots-humanoids-are-coming-for-you
  source: $7T by 2050, 8.9-week payback (Nov 4, 2024)
- id: 57
  title: TrendForce · AgiBot + Unitree to ~80% of 2026 shipments
  url: https://www.trendforce.com/presscenter/news/20260409-13007.html
- id: 58
  title: Crunchbase News · 2025 robotics VC $14B vs $8.2B 2024
  url: https://news.crunchbase.com/robotics/ai-funding-high-figure-raise-data/
- id: 59
  title: Electrek · Musk Q4 2025 — Optimus "still R&D, not in factories materially"
  url: https://electrek.co/2026/01/28/musk-admits-no-optimus-robots-are-doing-useful-work-at-tesla-after-claiming-otherwise/
- id: 60
  title: NVIDIA Blog · Jensen Huang Physical AI framing (CES 2025)
  url: https://blogs.nvidia.com/blog/ces-2025-jensen-huang/
- id: 61
  title: Figure AI · BMW Spartanburg production
  url: https://www.figure.ai/news/production-at-bmw
- id: 62
  title: StockAnalysis · BOTZ ETF
  url: https://stockanalysis.com/etf/botz/
  source: $3.82B AUM, 11.39% CAGR since 2016, trailing SPY
- id: 66
  title: KraneShares · KOID Humanoid Robot ETF
  url: https://kraneshares.com/etf/koid/
  source: $191.5M AUM, 0.69% net
- id: 67
  title: Roundhill · HUMN Humanoid Robotics ETF
  url: https://www.roundhillinvestments.com/etf/humn/
  source: '0.75% expense'
- id: 68
  title: Global X · BOTZ Robotics & AI ETF
  url: https://www.globalxetfs.com/funds/botz
- id: 69
  title: ARK · ARKQ Autonomous Tech & Robotics ETF
  url: https://www.ark-funds.com/funds/arkq
- id: 70
  title: Global X HK · 3139.HK EV & Humanoid Robot Active ETF
  url: https://www.globalxetfs.com.hk/funds/ev-and-humanoid-robot-active-etf/
- id: 71
  title: Forge Global · Figure AI secondary quote
  url: https://forgeglobal.com/figure-ai_stock/
  source: $174.00/share, ~$34.22B implied
- id: 72
  title: EquityZen · Figure AI fund-of-one
  url: https://equityzen.com/company/figureb5dc/
- id: 73
  title: Crowdfund Insider · Republic Mirror Token program
  url: https://www.crowdfundinsider.com/2025/10/254835-ai-firm-databricks-is-the-next-mirror-note-listed-on-republic/
- id: 74
  title: SEC · Accredited Investor definition
  url: https://www.sec.gov/resources-small-businesses/capital-raising-building-blocks/accredited-investors
- id: 75
  title: Backed Finance · Tokenized equities launch
  url: https://backed.fi/news-updates/backed-launches-five-new-tokenized-equities-including-bgoogl-btsla-and-bgme
- id: 76
  title: XMAQUINA · $10M cumulative raise
  url: https://www.xmaquina.io/blog/10m-raised-to-reclaim-the-robotics-capital-markets
- id: 77
  title: Republic · rSPAX Mirror Token
  url: https://republic.com/rspax
- id: 78
  title: Bitget · BOT-07 (1X $800K USDC) approved
  url: https://www.bitget.com/news/detail/12560605058339
- id: 81
  title: Recordowl (ACRA mirror) · XMAQUINA Foundation Ltd, UEN 202422336Z, struck off 09 Oct 2025
  url: https://recordowl.com/company/xmaquina-foundation-ltd
- id: 82
  title: Singapore Legal Advice · CLG cannot distribute surplus to members
  url: https://singaporelegaladvice.com/law-articles/set-up-company-limited-by-guarantee-singapore/
- id: 83
  title: MIDAO · RMI DAO LLC framework
  url: https://docs.midao.org/llms-full.txt
  source: '3% GRT, BOIR for 25%+ governance holders'
- id: 84
  title: CFTC · CFTC v. Ooki DAO default judgment
  url: https://www.cftc.gov/PressRoom/PressReleases/8715-23
  source: $643,542 penalty
- id: 85
  title: Fintech & Digital Assets · SEC v. Coinbase ruling summary. (Mar 27, 2024)
  url: https://www.fintechanddigitalassets.com/2024/04/ruling-for-sec-clears-path-for-continued-litigation-in-sec-v-coinbase/
- id: 86
  title: SEC · Joint staff statement on tokenized securities. (Jan 28, 2026)
  url: https://www.sec.gov/newsroom/speeches-statements/corp-fin-statement-tokenized-securities-012826
- id: 87
  title: EUR-Lex · MiCA Reg (EU) 2023/1114
  url: https://eur-lex.europa.eu/eli/reg/2023/1114/oj/eng
- id: 88
  title: SEC · Peirce Token Safe Harbor speech. (Feb 6, 2020) — proposal, not rule
  url: https://www.sec.gov/news/speech/peirce-remarks-blockress-2020-02-06
- id: 89
  title: American Bar Association · Hinman 2018 sufficient-decentralization speech
  url: https://www.americanbar.org/groups/business_law/resources/business-law-today/2018-august/senior-sec-official-provides-regulatory-clarity/
- id: 90
  title: The Network Firm · AICPA attestation vs audit distinction
  url: https://www.thenetworkfirm.com/blog/proof-of-reserves-vs-financial-statement-audits-what-crypto-companies-need-to-know
- id: 91
  title: Baker McKenzie · INX Limited F-1 as first SEC-effective security token
  url: https://blockchain.bakermckenzie.com/2020/08/31/u-s-sec-approves-the-first-full-securities-registration-for-a-company-issuing-crypto-tokens/
- id: 92
  title: K&L Gates · Reg S 1-year compliance period
  url: https://www.klgates.com/Navigating-US-Regulatory-and-Tax-Issues-A-Primer-for-Singapore-Managers-Marketing-Private-Funds-in-the-United-States-11-5-2024
- id: 93
  title: XMAQUINA GitBook · Cayman foundation reference
  url: https://xmaquina.gitbook.io/xmaquina/
- id: 94
  title: docs.xmaquina.io · Legal structure ("governance only, no profit rights")
  url: https://docs.xmaquina.io/dao/legal-structure.md
- id: 96
  title: docs.xmaquina.io · RCM Protocol
  url: https://docs.xmaquina.io/rcm-protocol
  source: '"under active legal structuring and technical development."'
- id: 97
  title: xmaquina.io · Roadmap
  url: https://www.xmaquina.io/road-map
  source: RCM Q3 2026 marked Pending
- id: 98
  title: GitHub · XMAQUINA-DAO org
  url: https://github.com/XMAQUINA-DAO
  source: '3 public repos, none labeled RCM/SubDAO/auction'
- id: 99
  title: GitHub · DEUS Solana OFT
  url: https://github.com/XMAQUINA-DAO/deus-solana-oft
  source: reproducibility build only
- id: 100
  title: docs.xmaquina.io · Smart Contract Audits
  url: https://docs.xmaquina.io/smart-contract-audits
  source: Hashlock only, last Oct 2024
- id: 101
  title: Bitget News · XMR-03 RCM funding governance vote
  url: https://www.bitget.com/news/detail/12560605180545
- id: 102
  title: Phemex · RCM launch coverage. (Pump.fun/Virtuals comp)
  url: https://phemex.com/news/article/xmaquina-launches-rcm-protocol-to-democratize-robot-capital-markets-56730
- id: 103
  title: xmaquina.io · DEUS Labs as independent SubDAO
  url: https://www.xmaquina.io/deus-labs
- id: 104
  title: trade.aspecta.ai · Aspecta pre-market IOU venue
  url: https://trade.aspecta.ai/
- id: 105
  title: XMAQUINA blog · Introducing the RCM Protocol
  url: https://www.xmaquina.io/blog/introducing-the-rcm-protocol
- id: 106
  title: CoinGecko · Virtuals Protocol
  url: https://www.coingecko.com/en/coins/virtual-protocol
  source: VIRTUAL -85% from ATH
- id: 107
  title: CoinGecko · AIXBT
  url: https://www.coingecko.com/en/coins/aixbt-by-virtuals
  source: '-96.7% from ATH'
- id: 108
  title: CoinGecko · Virtuals ecosystem category
  url: https://www.coingecko.com/en/categories/virtuals-protocol-ecosystem
  source: GAME ~-97.9% from ATH
- id: 109
  title: CoinGecko · Fabric Protocol (ROBO)
  url: https://www.coingecko.com/en/coins/fabric-protocol
  source: '-68.1% in ~10 weeks'
- id: 110
  title: KuCoin News · Virtuals Titan launch mechanics
  url: https://www.kucoin.com/news/flash/virtuals-launches-pegasus-unicorn-and-titan-token-launch-mechanisms
  source: $50M minimum, $500K paired LP
- id: 111
  title: xmaquina.io · Community Genesis Auction
  url: https://www.xmaquina.io/community-genesis-auction
  source: $1M+ TVL, $0.06 price, 33% liquid at TGE
- id: 112
  title: Yellow · Token unlocks ~90% negative impact
  url: https://yellow.com/learn/token-unlocks-explained-how-vesting-schedules-impact-crypto-prices-and-market-liquidity
- id: 113
  title: TechMarketBriefs · Figure AI IPO consensus 2027–2028
  url: https://techmarketbriefs.com/pre-ipo/figure-ai/
- id: 114
  title: TechCrunch · Apptronik $5.3B post-money
  url: https://techcrunch.com/2026/02/11/humanoid-robot-startup-apptronik-has-now-raised-935m-at-a-5b-valuation/
- id: 116
  title: CoinGecko · Robotics category
  url: https://www.coingecko.com/en/categories/robotics
  source: $773M total market cap, VIRTUAL leads at $472M
- id: 117
  title: Bitget Academy · Republic IPO-Prime / pre-IPO mirror tokens
  url: https://www.bitget.com/amp/academy/what-is-republic-ipo-prime-and-openai-pre-ipo-token
  source: '6-month post-IPO lockup payout'
- id: 118
  title: XMAQUINA · $10M cumulative raise
  url: https://www.xmaquina.io/blog/10m-raised-to-reclaim-the-robotics-capital-markets
:::
