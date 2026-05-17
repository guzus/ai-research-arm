---
eyebrow: REPORT · MARKETS · ROBOTICS
title: $BOT by Andrew Kang
deck: RoboStrategy listed on Nasdaq on May 11 2026 at a 434% premium to NAV. The same setup crushed DXYZ in 2024.
lede: |
  Andrew Kang spent five years as one of crypto's most-watched leveraged traders before writing a $19M personal check into Figure AI in February 2024 and pivoting to humanoid robotics. RoboStrategy, Inc. (Nasdaq: BOT) is the public-market expression of that pivot — a 1940-Act-registered closed-end fund holding ~$147M of private positions in Figure, Apptronik, Dyna Robotics, Standard Bots, and Dexmate. On its first session it closed 434% above NAV. Four days later it signed a $2B committed equity facility with Roth Principal. This is a structural reading of the wrapper, the holdings, the math of the premium, and the conflicts the prospectus is admirably blunt about.
stats:
  - {label: Listing date, value: "2026-05-11"}
  - {label: Day-1 close, value: $39.00, note: "5x NAV"}
  - {label: NAV/share (3/31/26), value: $7.31}
  - {label: Premium at IPO close, value: "434%"}
  - {label: Equity facility, value: $2.0B, note: "Roth Principal"}
  - {label: Top holding, value: "Figure AI", note: "$39B post-money"}
---

## 01. The Ticker

RoboStrategy, Inc. ({accent}Nasdaq: BOT{/}) is a Maryland-incorporated, registered closed-end management investment company that began trading on the Nasdaq Global Market on May 11, 2026,[^2] holding minority equity stakes in five private humanoid- and industrial-robotics companies against roughly $146.2M of net assets as of February 28, 2026.[^1] On its debut session the fund closed at $39.00 — a 434% premium to its 3/31/2026 NAV of $7.31[^7] — then whipsawed −46% / +71% over the next four sessions as Nasdaq tripped multiple LULD circuit-breaker halts.[^4,6] In SEC filings BOT is registered under the Investment Company Act of 1940 (file 811-24118), which is what makes the day-one mispricing legible: unlike a SPAC or a crypto-treasury vehicle, BOT must publish NAV monthly, so the premium math is on the tape rather than in the imagination.[^3]

:::stats
- {label: Listing date, value: "2026-05-11"}
- {label: Day-1 close, value: $39.00, note: "+5x NAV"}
- {label: NAV/share (3/31/26), value: $7.31}
- {label: Premium to NAV, value: "434%", note: "at IPO close"}
:::

The first five sessions of price discovery were, by any sober reading, disordered. After opening on May 11 at $39, BOT printed $25.40 the next day, $21.01 on the 13th (a single-session decline of −15.35% punctuated by repeated volatility halts and characterized in trade-press coverage as driven by "heavy retail investor interest"),[^6] then ripped back to $27.10 on the 14th and $36.01 on the 15th.[^4] Initial market capitalization on debut was reported near $730M against ~19.9M shares outstanding[^5,1] — i.e., the market was capitalizing the fund's ~$147M of underlying private positions at roughly 5x cost, before any liquidity event at the portfolio level.

:::line-chart(title="$BOT, daily close, debut week", subtitle="Yahoo Finance via yfinance", y-unit=$)
x: 2026-05-11,2026-05-12,2026-05-13,2026-05-14,2026-05-15
BOT: 39.0,25.4,21.01,27.1,36.01
:::

The 434% premium is large in absolute terms but not unprecedented. US closed-end funds have historically traded at a {accent}~10% average discount{/} to NAV across the long run, which makes BOT's debut a roughly 4.4-sigma deviation from the base case. The standing record is Destiny Tech100 (DXYZ), which printed a 2,070% premium at its April 8, 2024 peak of $105 — the highest premium in US CEF history, eclipsing a 1929 record of 1,235%.[^8] BOT today sits comfortably below DXYZ's peak but well above the prior modern range for venture-style CEFs.

:::compare
- {role: LOWEST, name: "Long-run CEF average", value: "-10%"}
- {role: HIGHEST, name: "DXYZ peak, Apr 2024", value: "+2,070%"}
- {role: SUBJECT, name: "$BOT day-1 close", value: "+434%"}
:::

The portfolio inside the wrapper is concentrated and named: five disclosed positions — {accent}Figure AI, Apptronik, Dyna Robotics, Standard Bots, and Dexmate{/} — covering humanoid and industrial-robotics platforms, with the per-name breakdown deferred to §03.[^9] Capital structure is the other half of the story: on May 15, four trading days into listing, BOT and Roth Capital Partners announced a $2B at-the-market equity facility against the same ~$147M base of net assets, a structure deconstructed in §06.[^10] That filing is what converts the premium from a curiosity into a {accent}mechanism{/}: a registered investment company can, in principle, harvest its own premium by issuing new shares above NAV — but BOT is a registered investment company, not a SPAC, so it must publish NAV monthly and disclose every issuance, which exposes the premium math in a way that crypto-treasury wrappers don't.

Why this matters: BOT is the live test case for whether a 1940-Act-registered closed-end fund can be re-engineered into a retail venture wrapper at scale — a structure that, if it holds its premium long enough to issue into it, would let public-market demand fund private humanoid-robotics positions on terms unavailable to those same companies in a primary round.

## 02. The Pivot

Andrew Kang's path from {accent}leveraged crypto trader to humanoid-fund CEO{/} is the single biographical line that explains every clause of $BOT's prospectus — and every reason a sober investor should read it twice.

:::timeline
- {date: 2020-09, headline: "Mechanism Capital founded", body: "Kang co-founds the crypto-native VC with Daryl Lau and Benjamin Simon, anchoring his reputation as a full-time on-chain principal."}
- {date: 2023-02, headline: "Mid-eight-figure BTC/ETH shorts", body: "Arkham flags 4 personal wallets and 10 Mechanism wallets running mid-eight-figure short books with $10M+ in unrealized profit before the trade reverses."}
- {date: 2023-08-18, headline: "100x longs, fourteen liquidations", body: "After an overnight crash, Kang publicly tries to catch the bounce with 100x leverage and is liquidated 14 times in a single session, for a disclosed loss of roughly $432K."}
- {date: 2024-02, headline: "$19M personal check into Figure", body: "Kang writes the largest venture check of his career into Figure AI, disclosed publicly two months later as the 'most excited since Bitcoin' moment."}
- {date: 2025, headline: "Leads $120M Apptronik consortium (per Kang)", body: "Kang claims (Sep 2025) that 'earlier this year' Mechanism led a $120M consortium into Apptronik — the company's own Series A extension closed in Feb 2026 at $520M."}
- {date: 2025-09-15, headline: "Co-leads $68M Dyna Robotics Series A", body: "A second humanoid lead in the same quarter; the thesis is now a strategy, not a single check."}
- {date: 2025-09-17, headline: "The Humanoid Thesis essay", body: "Kang publishes the $5T–$50T-at-$50K-per-unit framing that becomes $BOT's de facto marketing deck."}
- {date: 2026-05-11, headline: "RoboStrategy lists on Nasdaq as $BOT", body: "The on-chain trader becomes a Nasdaq-listed closed-end fund CEO, with the same private positions now wrapped for a public bid."}
:::

Kang co-founded Mechanism Capital in September 2020 with Daryl Lau and Benjamin Simon, and the firm spent its first three years as a recognizably crypto-native shop: token investments, market making, and a principal book that Kang ran in public.[^11] That public-ness matters. By early 2023, on-chain analytics firm Arkham had attributed four personal wallets and ten Mechanism-linked wallets to him, and was livestreaming the P&L of his mid-eight-figure BTC and ETH shorts — at peak more than $10M in unrealized gains before the position bled out as the market rallied through Q2.[^15] Six months later, on August 18 2023, the *other* side of the leverage tape played out: Kang tried to fade a post-crash bounce with 100x perpetual longs, took fourteen liquidations across the session, and acknowledged roughly $432K of realized losses by morning.[^19] The 40x $100M BTC long opened from a wallet that analytics services labeled "funded by Rewkang" on April 9 2025 — minutes after a market-moving Trump tariff post — sits in the same lineage. Kang disclaimed the wallet, but it priced into the tape regardless,[^16] a reminder that his on-chain shadow trades whether or not he wants it to.

The pivot started underneath that noise. In February 2024, Kang wrote a $19M personal check into Figure AI — disclosed in an April 4 2024 X post that has since become the founding document of his second act:[^12]

:::quote(attr="Andrew Kang, @Rewkang, Apr 4 2024")
In February, I made a $19M investment in @Figure_robot. It's the largest venture check I've written and it's also the most excited I've been about a world changing technological revolution since diving into Bitcoin/crypto.
:::

That single sentence is the genome of $BOT. The Figure check was followed by Kang's claim, made publicly in September 2025, that "earlier this year, we led an investment consortium that invested $120M into @Apptronik," and on September 15 2025 by co-leading Dyna Robotics' $68M Series A.[^14] Two days after the Dyna close he published "The Humanoid Thesis," a long-form essay arguing that a $50K humanoid unit price implies a $5T–$50T addressable market — the framing that now appears, almost verbatim, in $BOT marketing.[^13] Industry observers in February 2025 had already started calling the arc "crypto to deep tech … a legendary parlay,"[^17] and the May 2025 Mechanism rebrand made it official: the firm restyled itself as a frontier-tech investor while keeping the same balance sheet.[^21] Even Kang's October 17 2025 trading update — closing ETH shorts for profit and flipping to a 7,637 ETH long at $3,783 — read less like a hedge-fund trade than a CEO clearing the deck before listing.[^20]

The counterpoint is in Kang's own positioning. The same Kang who in May 2025 floated a "$1 quadrillion at 20 billion robots" framing[^55] is asking the public to capitalize a NAV against humanoid platforms whose own benchmark-robustness gaps are documented in §07. Stack that against the Aug 2023 liquidations and the Apr 2025 wallet-attribution episode and you get a CEO who has been publicly, expensively wrong about timing leverage — now asking the public market to hand him a permanent-capital vehicle to be early again.[^15,19,16]

Why this matters: every public-vehicle CEO is also a brand, but Kang's brand is {accent}doxxed onchain and historically wrong about leverage{/}. The same Arkham feed that priced his 2023 shorts will price BOT's NAV-vs.-price spread tick by tick — and the same audience that watched the 100x liquidations is now being asked to pay a premium for his curated humanoid book.

## 03. What BOT Owns

RoboStrategy's prospectus names five core private holdings — Figure AI, Apptronik, Dyna Robotics, Standard Bots, and Dexmate — but the fund {accent}does not disclose per-position weights{/}, leaving retail buyers to triangulate concentration from a single SEC-filed $74.5M in-kind contribution figure (which covers only Figure and Apptronik) against the fund's $146M Feb-28 net assets.[^9,31]

The five holdings span an enormous valuation gradient. Ranked by latest disclosed post-money mark, Figure AI alone is roughly 8x the size of the next-largest position and ~950x the size of the smallest:

:::rank-list
- {label: Figure AI, value: "$39B post-money", pct: 100, highlight: true}
- {label: Apptronik, value: "~$5B post-money", pct: 13}
- {label: Dyna Robotics, value: "undisclosed (Series A $120M)", pct: 5}
- {label: Standard Bots, value: "undisclosed (Series B $63M)", pct: 3}
- {label: Dexmate, value: "~$41M total raised", pct: 1}
:::

Figure AI is the anchor — and the reason BOT exists in its current shape. The company closed a $1B+ Series C on Sep 16 2025 at a $39B post-money valuation, a ~15x markup in 18 months that re-rated every secondary share BOT now claims to hold.[^22] The headline operating proof point is the BMW Spartanburg pilot, where Figure 02 robots logged 1,250+ runtime hours, handled 90K+ parts, and touched ~30K X3 vehicles over a 10-month deployment.[^30] Figure 03 was unveiled in Oct 2025 as the production-intent successor, slotted into the BotQ Gen-1 manufacturing line and ramping toward ~240 units/month by Apr 2026 against a stated 12,000 units/year nameplate capacity.[^30]

:::kv
- {term: "Latest round", def: "Series C, $1B+, Sep 16 2025"}
- {term: "Post-money valuation", def: "$39B"}
- {term: "Customer pilot", def: "BMW Spartanburg (Figure 02)"}
- {term: "Production line", def: "BotQ Gen-1, 12,000 units/yr capacity"}
- {term: "Latest model", def: "Figure 03 (Oct 2025)"}
:::

Apptronik is the only other holding with a recently-marked institutional round and a named customer roster. Its $520M Series A extension closed Feb 11 2026 at roughly $5B post-money, taking total Series A funding past $935M.[^25] Crucially for the thesis, Apollo — Apptronik's humanoid — has disclosed pilot or supply relationships with Mercedes-Benz, GXO, Jabil, and John Deere, the kind of multi-vertical customer set that distinguishes a real OEM-track program from a demo-reel company.[^26]

Stacking the named commercial exposure of the top two robots side by side makes the concentration risk visible: every disclosed customer for both Figure and Apollo sits in either automotive or logistics/manufacturing. Consumer is a future story, not a current revenue line.

:::stack-rows
categories: [Auto, Logistics, Manufacturing, Consumer]
rows:
  - {label: "Figure 02/03", values: [100, 0, 0, 0]}
  - {label: "Apptronik Apollo", values: [25, 25, 50, 0]}
:::

The remaining three holdings are smaller, earlier, and — in one case — entangled with BOT itself. {accent}Dyna Robotics{/} closed a $120M Series A on Sep 15 2025 co-led by CRV, First Round, and {accent}RoboStrategy{/}, meaning the manager is marking its own co-lead position; the prospectus does not disclose the post-money valuation, only the round size.[^27] {accent}Standard Bots{/}' last priced round was a $63M Series B led by General Catalyst in July 2024, with its RO1 robotic arm carrying a $37K list price — no Series C has been disclosed in the 22 months since.[^28] {accent}Dexmate{/} is the earliest-stage of the five: a Bay Area startup with MIT/UCSD/CMU founders, roughly $41M raised in total, and a Vega humanoid priced at $89,999 for the developer market.[^29]

:::callout(kind=warn, label="Concentration unknown")
The only weighting disclosure on record is the in-kind contribution that seeded the fund: Kang and Weinstein entities contributed Figure and Apptronik SPV interests valued at $37.25M each — $74.5M combined — in exchange for 7.45M shares at $10.[^31] On a $146M Feb-28 NAV that single transaction accounts for roughly half the fund's assets in just two names. The rank-list above sorts by valuation of the underlying companies, not by BOT's exposure to them. A small ticket in Figure could swamp a large ticket in Dexmate.
:::

**Why this matters.** The underlying holdings are not particularly liquid. Figure was last priced eight months ago. Standard Bots was last priced 22 months ago. Dyna and Dexmate have no public secondary market at all. That makes NAV a slow-moving anchor: even if the secondary market re-rates humanoid robotics tomorrow morning, BOT's stated net asset value won't reflect it until the next funding round prints — and there is no contractual obligation for any of these private companies to raise on a schedule that suits a public closed-end fund's marking calendar.

## 04. The Wrapper

RoboStrategy is a 1940-Act-registered closed-end fund — not a SPAC, not a BDC, not an interval fund[^35] — and that legal form chooses a specific set of trade-offs: {accent}no 15% illiquid cap, monthly NAV publication, C-corp taxation in year one, and a 3.22% expense ratio on top of SPV-level fees{/}.

:::kv
- {term: "Legal form", def: "Maryland corporation, organized May 23, 2025"}
- {term: "Registration", def: "Registered closed-end fund, 1940 Act file 811-24118"}
- {term: "Adviser", def: "FP Strategies LLC (Puerto Rico), controlled by Kang + Weinstein"}
- {term: "Auditor", def: "Grant Thornton LLP"}
- {term: "Administrator", def: "U.S. Bancorp Global Fund Services"}
- {term: "Custodian", def: "U.S. Bank N.A."}
- {term: "Transfer Agent", def: "Computershare Trust Company"}
:::

The structural facts are unglamorous and exactly the point. BOT is a Maryland corporation organized on May 23, 2025, registered with the SEC under the Investment Company Act of 1940 (file 811-24118).[^3] The adviser is FP Strategies LLC, a Puerto Rico entity controlled by Andrew Kang and Marc Weinstein under a two-year initial advisory contract.[^32] The plumbing — Grant Thornton as auditor, U.S. Bancorp Global Fund Services as administrator, U.S. Bank N.A. as custodian, Computershare as transfer agent[^33] — is the standard registered-fund stack. There is nothing exotic about the operating apparatus. The exotic part is what the apparatus is wrapped around.

:::stats
- {label: "Management fee", value: "2.50%", note: "on GROSS assets"}
- {label: "Total expense ratio", value: "3.22%"}
- {label: "Year-1 corporate tax", value: "21%", note: "not RIC for FY 8/31/26"}
- {label: "Illiquid cap", value: "None", note: "22e-4 binds open-end only"}
:::

:::callout(kind=warn, label="Structural quirk")
Most retail buyers will assume a closed-end fund inherits the mutual-fund-style 15% illiquid-securities limit. It does not. Rule 22e-4's liquidity-risk-management regime binds {accent}open-end funds only{/} — registered CEFs can hold 100% illiquid private positions, and BOT's prospectus says so explicitly: "no limitation on the portion of the Fund's portfolio that may be invested in illiquid securities."[^36,39] That is the entire reason the wrapper exists. Without that carve-out, a public vehicle holding Figure, Apptronik, and Dyna stakes is structurally infeasible; with it, you get BOT.
:::

That illiquidity-cap exemption is the load-bearing piece of the whole pivot. A BDC would force RoboStrategy to count toward the 70%-qualifying-asset test and would limit private-company concentration; an interval fund would still face Rule 22e-4 in practice. The registered-CEF wrapper sidesteps both, which is why the N-2 explicitly checks "Registered Closed-End Fund" and nothing else.[^35] The cost of that flexibility is that closed-end funds are also the wrapper most prone to trading at persistent discounts — see Section 05.

The tax stack is the second consequence the prospectus is admirably blunt about. For the fiscal year ending August 31, 2026, the Fund {accent}does not expect to qualify as a regulated investment company (RIC) under Subchapter M{/}, which means it will pay corporate tax at the 21% federal rate on net taxable income before any distribution to shareholders.[^34,37] The prospectus itself uses the phrase "double taxation" — the same income gets taxed once at the fund level and again at the holder level when distributed. Management has stated it intends to elect RIC treatment from FY 2027 onward, which would restore pass-through treatment, but year one is a C-corp drag baked into the structure.

The closest listed analog is Pershing Square Holdings (PSH), Bill Ackman's permanent-capital vehicle in Amsterdam. PSH is structured as a Guernsey company and is {accent}permanently subject to entity-level tax frictions{/} — there is no RIC equivalent it can elect into, and the discount has reflected that: PSH went from a ~9% discount at the end of its first year to a 37% discount by September 2023, and has spent the intervening decade trading at a persistent double-digit gap to NAV.[^40] BOT's C-corp problem, by contrast, is a one-year window with a clear exit ramp into Subchapter M. That is meaningfully better, though "better than the worst closed-end discount in the developed world" sets a low bar.

The fee stack deserves its own paragraph because the headline 2.50% management fee is calculated on *gross* assets — meaning if the Fund employs leverage (which the prospectus permits), the fee scales with borrowed dollars, not just equity. Layered on top: other expenses and acquired-fund / interest expense lines that push the total expense ratio to {accent}3.22%{/}.[^38] And that 3.22% sits *above* a second layer of fees most readers will miss: the underlying SPVs that hold Figure, Apptronik, and Dyna positions typically charge their own management fee plus carry to the SPV sponsor. {accent}Investors are paying twice{/} — once at the BOT level and once inside each SPV — before a single dollar of NAV growth reaches the shareholder.

The honest counterpoint: the registered-CEF wrapper is also a feature. Unlike an unregistered private fund or a Cayman-domiciled permanent-capital vehicle, BOT is required to publish NAV monthly, file an annual N-CSR, and submit to PCAOB-audited financials from Grant Thornton.[^33] That creates a clear, third-party-blessed denominator against which the premium or discount can be measured in real time — exactly the transparency PSH spent a decade trying to manufacture and never quite achieved.

Why this matters: BOT is the {accent}first registered-CEF wrapper for a private VC-style book to list on Nasdaq{/}. If the structure holds — if monthly NAV publication, the year-one tax hit, and the no-illiquid-cap exemption all survive contact with the market — expect copycats.

## 05. The 434% Premium

BOT's day-one 434% premium to NAV is not unprecedented — DXYZ printed 2,070% in 2024 — but every recorded large closed-end fund premium has collapsed within months, and the academic literature documents persistent mean reversion with half-lives measured in quarters, not years.

The {accent}base rate for extreme CEF premiums is brutal{/}. Destiny Tech100 (DXYZ), the closest comparable to BOT — a listed CEF holding late-stage private tech — peaked at $105 on April 8 2024, a 2,070% premium to its underlying NAV.[^8] Acadian/Lamont called it "the highest premium ever observed in U.S. CEF history," eclipsing the 1,235% record DeLong and Shleifer documented from the 1929 mania.[^45] BOT's day-one close of $39 against a 3/31/2026 NAV of $7.31 — a 434% premium[^7] — slots into the top tier of that distribution but is roughly one-fifth of the DXYZ peak.

:::rank-list
- {label: "DXYZ peak (Apr 8 2024)", value: "2,070%", pct: 100}
- {label: "DeLong-Shleifer 1929 record", value: "1,235%", pct: 60}
- {label: "$BOT day-1 close (May 11 2026)", value: "434%", pct: 21, highlight: true}
- {label: "Taiwan Fund (1987)", value: "205%", pct: 10}
- {label: "CUBA Fund (Dec 2014)", value: "70%", pct: 3}
:::

The DXYZ tape is the cleanest base-rate example because the structure (NYSE-listed CEF, illiquid private-tech holdings, retail demand for otherwise-inaccessible names) is the same playbook BOT is running. DXYZ listed on NYSE on March 26 2024 at a $9 close against a $4.84 reference NAV — already an 86% premium on day one.[^41] Thirteen sessions later it printed $105.[^8] By year-end 2024 the NAV had been written down to $6.44; one year later the fund's auditors marked NAV up to $19.97, a 209.59% YoY swing driven almost entirely by Level-3 fair-value remarks of OpenAI and SpaceX positions.[^42] Even with that NAV catch-up, the trailing-twelve-month price return is -27.6% and the 52-week range is $19.71-$50.50.[^44] The premium compressed because supply expanded into demand, not because the underlying businesses failed.

:::timeline
- {date: "2024-03-26", headline: "DXYZ lists on NYSE", body: "Day-one $9 close against $4.84 NAV — ~86% premium right out of the gate."}
- {date: "2024-04-08", headline: "Peak: $105", body: "~2,070% premium to NAV — highest ever recorded for a U.S. CEF."}
- {date: "2024-12-31", headline: "NAV marked at $6.44", body: "Price still elevated; premium remains triple-digit on year-end mark."}
- {date: "2025-12-31", headline: "NAV revised to $19.93", body: "+209.59% YoY on Level-3 OpenAI/SpaceX mark-ups — the underlying caught up to the price, not the other way around."}
- {date: "2026-05", headline: "TTM return: -27.6%", body: "52-week range $19.71-$50.50; premium has compressed toward the long-run CEF baseline."}
:::

The academic literature on CEFs explains the gravity. An Auburn 2023 study of 31 equity CEFs found average discounts ranging from -17.23% to +14.99%, with a median mean-reversion half-life of 8.10 months[^43] — meaning that whatever the discount or premium today, half of it is mechanically gone within roughly two-thirds of a year. Pershing Square Holdings (PSH), the benchmark for "high-quality manager, listed wrapper," widened from ~9% at the end of its first year to a 37% discount by September 2023.[^40] That is the equilibrium pull: persistent discounts, not premiums.

:::stats
- {label: "Long-run CEF discount (Auburn)", value: "8-15%"}
- {label: "Median half-life of mean reversion", value: "8.1", unit: "mo"}
- {label: "PSH discount end of yr 1", value: "9%"}
- {label: "PSH discount (Sept 2023)", value: "37%"}
:::

The mechanics matter because BOT's holdings make conventional arbitrage impossible. Arbitrageurs usually compress CEF premiums by going long the underlying and short the wrapper — but you cannot short Dyna or Dexmate the way you can short OpenAI exposure through secondary markets. What reliably erodes premiums is *supply expansion*: the fund itself, or an affiliated facility, issuing new shares into the demand and pocketing the premium. The Roth $2B equity facility detailed in §06 is precisely that mechanism. Combine fresh issuance with a stale NAV (BOT marks monthly, not daily like DXYZ,[^41] and BOT's holdings have *no* secondary market for price discovery, unlike DXYZ's OpenAI/SpaceX positions, which at least clear in tender offers) and the historical pattern says compression follows on a months-not-years timetable. The first five trading days are already noisy in this direction: BOT closed at $39.00, $25.40, $21.01, $27.10, $36.01 between May 11 and May 15[^4] — a 35% intraday-week drawdown and partial recovery that looks far more like DXYZ's 2024 chart than like the steady-compounder narrative the bulls are selling.

:::callout(kind=warn, label="Counterpoint")
The bull rebuttal: BOT's holdings are arguably *underpriced* if the humanoid TAM is real, and a sustained premium is "rational" because retail cannot otherwise access Dyna, Dexmate, or 1X at any price. The interval-fund alternative — ARK Venture Fund (ARKVX) — has no premium/discount but locks investor liquidity, so listed CEFs trade at a premium for genuine reasons.[^46] The problem: this same "rational premium" argument has been made for every triple-digit CEF premium in recorded history, and not one has survived the next 12 months intact.
:::

{accent}Why this matters.{/} The premium *is* the bull thesis. BOT's ability to monetize it — by issuing new shares into the spread via the Roth facility (§06) and converting paper premium into permanent capital — is the only way the structure compounds for existing holders. The bear case is the mirror image: the very issuance that monetizes the premium is the supply expansion the CEF literature identifies as the mean-reversion engine. The harder management presses the Roth facility, the faster the 434% spread collapses toward the 8-15% long-run discount baseline.

## 06. The $2B Equity Facility

Four trading days after listing, RoboStrategy signed a $2.0B committed equity facility with Roth Principal Investments — a structure that, in principle, lets a closed-end fund monetize its own premium by issuing fresh shares above NAV and recycling the proceeds into more of the same illiquid private positions that produced the premium.[^10,47]

:::kv
- {term: "Facility size", def: "Up to $2.0B aggregate gross proceeds"}
- {term: "Term", def: "36-month draw window from effectiveness"}
- {term: "Pricing", def: "VWAP minus 2.0% discount per Market Open Purchase"}
- {term: "Floor price", def: "Greater of $13.45 base price or NAV/share at issuance"}
- {term: "Per-draw cap", def: "2,000,000 shares or a % of Nasdaq session volume"}
- {term: "Nasdaq 19.99% exchange cap", def: "4,052,806 shares (no shareholder vote)"}
- {term: "Resale shares registered", def: "14,100,000"}
:::

The headline terms come straight from the N-2 and the related resale registration: VWAP minus 2.0% per Market Open Purchase, a $13.45 base price floor (or NAV/share, whichever is higher), a per-draw cap of 2,000,000 shares, and 14,100,000 shares registered for resale by Roth as principal.[^47,48,50,54] These are tighter than Roth's standard committed equity terms, which typically run VWAP minus 3% intraday or minus 5% off-hours plus a ~1.5% commitment fee.[^51] Use of proceeds language is exactly what an investor would expect from an MSTR analogue: up to $2B gross to fund {accent}additional investments{/} consistent with BOT's robotics-and-AI mandate.[^49]

:::callout(kind=warn, label="Dilution math")
With 19,908,968 shares outstanding pre-deal[^1] and a Nasdaq 19.99% exchange cap of 4,052,806 shares before a shareholder vote,[^50] the first slug of issuance is mathematically capped. At a $30 average issuance price — already optimistic versus the $13.45 floor — that ceiling translates to roughly **$122M** of the $2B headline, or about **6%** of the facility. To draw the full $2B, BOT needs three things to align simultaneously: (a) shareholder approval to lift the 19.99% cap, (b) a durable premium-to-NAV that keeps the stock well above the $13.45 floor across the entire 36-month draw window, and (c) ~$2B of actual lit-book trading volume to absorb the issuance without collapsing the very premium being monetized. Miss any one and the facility becomes a marketing document.
:::

The X-side bull case is explicit: "MicroStrategy for robotics," an equity-issuance wrapper that converts premium into NAV-multiple capital.[^52,53] The structural comparison is fair on paper — both issuers print stock above the value of their underlying assets and use the proceeds to buy more of the same asset — but the operational comparisons are where the analogy starts to crack.

:::compare
- {role: "LOWEST", name: "MSTR premium-to-NAV (illustrative)", value: "1.7x"}
- {role: "HIGHEST", name: "BOT $2B facility ÷ NAV", value: "13.7x"}
- {role: "SUBJECT", name: "BOT first-tranche cap", value: "$122M"}
:::

| Dimension | BOT (RoboStrategy) | MSTR / treasury wrapper |
|---|---|---|
| Issuer structure | Closed-end fund (40 Act), Level-3 marks | Operating company / treasury vehicle |
| Underlying asset liquidity | Private robotics equities, monthly NAV | BTC, 24/7 continuous price discovery |
| Premium-monetization mechanism | VWAP -2%, $13.45 / NAV floor | ATM equity, convertibles, preferreds |
| Settlement / NAV cadence | Monthly Level-3 marks | Daily mark-to-market on the underlying |

The MSTR comparison is structurally sound but operationally fragile for two reasons. First, MSTR's underlying BTC trades 24/7 with continuous, observable price discovery, so its premium is anchored to a number anyone can verify in real time; BOT's NAV reprices monthly off Level-3 marks on private positions,[^1] which means the "premium" being monetized is itself a function of when management chooses to remark the book. Second, MSTR's premium has been sustained over multiple years of repeated buy-and-issue cycles that conditioned the market to the flywheel; BOT has {accent}five trading days of price history{/} and a single retail-driven spike to roughly 5x NAV ($37.92 against a $7.50 NAV reference) as its only data point.[^52]

The counterpoint to the bull case is built into the document itself. The 19.99% Nasdaq exchange cap limits unilateral issuance to ~$122M absent a shareholder vote, and the $13.45 base price floor means BOT *cannot* issue at all if the premium fully compresses to NAV — the facility goes idle exactly when management would most want the cash to defend the book or fund opportunistic buys. The 36-month window helps, but it is a window, not a guarantee.

Why this matters: the equity facility is best read as a {accent}put on the premium{/}, not a $2B war chest. If BOT can sustain the premium long enough to clear a shareholder vote on the exchange cap and accumulate the lit-book volume to absorb 14.1M resale shares,[^47] it gets NAV-multiple economics on real capital and the MSTR comparison earns its keep. If the premium compresses before the vote — and Section 05's DXYZ precedent suggests that is the base case — the facility was a marketing event timed to peak retail attention, and the headline "$2.0B" never materializes as cash on the balance sheet.

## 07. The Humanoid Thesis, Stress-Tested

Andrew Kang's "BTC-in-2013" framing for humanoid robotics rests on three falsifiable claims — a trillions-of-dollars TAM, sub-human cost-per-hour "in most parts of the world," and fast-converging visuo-motor capability[^13] — and on the evidence available in mid-2026, each one is either contested by a ~180x spread in bank forecasts, contradicted by the wage math in the regions actually building these robots, or directly refuted by the benchmark literature.

Start with the TAM. The "$5T to $50T" range Kang cited[^13] — and the more cartoonish "$1 quadrillion at 20 billion robots" version that circulates on X[^55] — sits inside a real, published spread that is itself absurd. Citi's 2050 number is roughly 180x Goldman's 2035 base case, and even Goldman's bull case is less than a thirtieth of Morgan Stanley's.[^56,57,58] A spread that wide is not a forecast; it is an admission that nobody knows.

:::rank-list
- {label: "Citi (2050): $7T / ~650M units", value: "$7T", pct: 100, highlight: true}
- {label: "Morgan Stanley (2050): $5T / ~1B units", value: "$5T", pct: 71}
- {label: "Goldman bull case (2035): $154B", value: "$154B", pct: 2}
- {label: "Goldman base case (2035): $38B", value: "$38B", pct: 1}
:::

The second claim — that humanoids will be cheaper per hour than humans "in most parts of the world" — survives only in the high-wage half of the planet. The capital-amortization framework published in 2025 — comparing a per-unit capital cost of fractions of a dollar against per-unit labor of ~$0.125 in a US warehouse — already shows the math only works in high-wage Western markets with structured tasks.[^62] ==unverified: At Chinese manufacturing wages of $3-6/hr, the same machine does not beat a human on cost.== That matters because China is where the units are actually being built. ==unverified: Roughly 90% of the 13,000-18,000 humanoid units shipped globally in 2025 came from Chinese factories, backed by a $1.4B Beijing municipal fund and 30% R&D subsidies.==[^61] The country that dominates production is also the country where the unit economics of deployment are weakest — a structural tension Kang's framing skips over.

:::donut(center-label="2025 global units")
- {label: China, value: 90}
- {label: Rest of World, value: 10}
:::

The supply side adds a reality check of its own. Tesla's Optimus program is the most-cited bull data point and the most easily falsified one: the 2025 stated target was "roughly 10,000" units, and by January 2026 Musk himself acknowledged that ==unverified: essentially zero Optimus robots were doing "useful work."== Gen-4 production at Giga Texas is now scheduled for summer 2027.[^59] Figure's BotQ Gen-1 line — the credible Western counterpoint — is rated at 12,000 units/yr of capacity and is currently ramping from about 60 to 240 units per month, which is real but two orders of magnitude short of the Morgan Stanley path.[^30]

:::compare
- {role: LOWEST, name: "Jan 2026 useful-work claim", value: "~0 units"}
- {role: HIGHEST, name: "2027 Giga Texas Gen-4 start", value: "summer 2027"}
- {role: SUBJECT, name: "2025 stated target", value: "~10,000 units"}
:::

The third claim — fast technical convergence — is where the Bitcoin analogy actually breaks. Bitcoin in 2013 worked: the network processed transactions, the cryptography held, the failure modes were economic, not technical. Humanoid VLAs in 2026 do not work robustly outside the lab, and the benchmark literature now says so quantitatively. The LIBERO-PRO study perturbs standard LIBERO tasks with modest, realistic distribution shifts — different lighting, object pose, background — and watches state-of-the-art visuo-motor policies collapse from 90%+ success to effectively 0%.[^63] NVIDIA's GR00T N1 on the Fourier GR-1, the public reference platform, reports 82% on lab pick-and-place and 70.9% on articulated manipulation[^64] — strong inside the eval harness, but a long distance from a robot you would put in a warehouse without a human nearby.

:::bars
- {label: "LIBERO standard", value: "90%", pct: 90}
- {label: "LIBERO-PRO (perturbed)", value: "0%", pct: 1}
- {label: "GR00T N1 pick-and-place (lab)", value: "82%", pct: 82}
- {label: "GR00T N1 articulated manipulation (lab)", value: "70.9%", pct: 71}
:::

That gap — 90% to 0% under modest perturbation — is the strongest single fact in the bear case, and it is not a quibble about edge cases. It is the same gap that separates a demo from a product, and it is exactly the gap a buyer of a $50K-$150K humanoid[^56] cannot tolerate at scale.

The bull case is not empty, however. VC funding into humanoids tripled year-over-year, from $1.5B across 65 deals in 2024 to $6.1B across 139 deals in 2025 {sparkline:1.5,6.1} — a 300% jump that signals real capital conviction, not a fading hype cycle.[^60] Figure's deployment of humanoids on a BMW X3 production line is operationally proven for a narrow, instrumented task.[^23] And the bear case carries its own strong claim: it requires the technical readiness gap to never converge, which on a 5-10 year horizon is itself a bold bet against a field that has compounded at the pace VLA research has since 2023.

**Why this matters for BOT.** $BOT's premium-to-NAV is implicitly pricing the Morgan Stanley/Citi end of the TAM range — the $5T-to-$7T, hundreds-of-millions-of-units world.[^57,58] If the truth is the Goldman base case at $38B by 2035,[^56] the underlying economics of the holdings (Figure, Apptronik, Dyna stakes) do not need to *fail* for the structure to break; they just need to compound at the slower path. The discount-to-NAV compression in section 06 is the second-order risk. The first-order risk is that the NAV itself is calibrated to the wrong bank.

## 08. The Conflicts File and What Could Break the Thesis

$BOT compresses three sets of conflicts into one ticker — adviser-marks-its-own-book, related-party SPVs contributed at sponsor-set prices, and a fund manager who is also one of the loudest public advocates for the asset class. Each is disclosed in the prospectus, each is legal, and each compounds the case for skepticism rather than against it.

The cleanest related-party flag is the in-kind contribution that seeded the fund. Per the N-2, Kang and Weinstein entities contributed Figure AI and Apptronik SPV interests {accent}each preliminarily valued at $37,250,000{/} — $74.5M combined — in exchange for 7,449,998 Fund shares at an effective $10/share basis, executed *before* the Fund was registered under the 1940 Act and therefore *before* Section 17's affiliate-transaction prohibitions attached.[^31] The prospectus notes the value was "based on valuation determined by an independent third-party valuation firm" but does not name that firm. The marks are functionally self-set: the same principals who controlled the SPVs set the price at which they swapped them for what would become public-fund stock.

That problem compounds at the marking layer. The Board has designated the Adviser itself as the official valuation agent under Rule 2a-5, with discretionary use of an unnamed third-party firm — meaning the people whose carry economics depend on NAV growth are also the people who determine when, and at what mark, NAV grows.[^65] In a fund whose holdings are nearly all Level-3 private positions and whose monthly NAV publication is the only thing keeping the premium math honest (§04), the absence of a named independent valuator is a structural gap.

The third conflict sits in the SAI's Conflicts of Interest section, where the Adviser explicitly retains the right to run parallel "Other Accounts" that may "commit a larger percentage of [their] assets to an investment opportunity than" the Fund itself.[^66] In plain English: Mechanism Capital — also controlled by Kang and Weinstein — was the earlier investor in Figure, Apptronik, and Dyna,[^67] and there is no contractual prohibition against Mechanism taking the better tranches of the next round while BOT takes the leftovers. Mechanism's official X account amplifying RoboStrategy's $2B Roth announcement four days after listing is the alignment signal in public;[^68] the lack of a Co-Investment Order under Section 17(d) (or other exemptive relief) is the gap in disclosure.

:::callout(kind=danger, label="Conflicts stack")
1. **Marks.** Sponsor-set in-kind valuation at $10/share, pre-1940-Act registration, for ~half of fund net assets.[^31]
2. **Valuation governance.** Adviser is its own valuation agent under Rule 2a-5; "independent third-party valuation firm" referenced but not named in the prospectus body.[^65]
3. **Parallel books.** SAI explicitly permits Other Accounts at Mechanism Capital to take larger positions than the Fund in the same opportunities.[^66]
4. **Public-vehicle CEO is also the sector's most public advocate.** Every Kang humanoid post — including "The Humanoid Thesis" essay[^13] — is now talking the book of a listed CEF.
:::

The skeptic file extends past the prospectus. A Solana pump.fun token referencing $BOT appeared within hours of the Roth announcement (contract `FVo5hJRs97EwPzDnAPkVPfHTvv5AqdmZtmuZKZDjpump`), unaffiliated with the company but attached to the ticker for retail flow.[^70] On X, observers flagged the day-one trading pattern as "narrative > fundamentals" influencer-driven price action against a low float, with no sell-side initiations yet on record.[^69]

**What could break the thesis.** Five mechanisms, ranked by base-rate likelihood:

1. **Premium compression via the Roth facility itself.** The same issuance that monetizes the premium is the supply expansion the CEF literature identifies as the mean-reversion engine (§05). Auburn's 8.1-month half-life is the prior.[^43]
2. **A bad NAV mark.** One weak Figure tender, one Apptronik down-round, one Dyna funding gap — any of these forces a write-down that exposes the marketing math behind the 434% premium.[^7]
3. **SEC scrutiny of the related-party in-kind valuation and the unnamed third-party valuator.** The pre-registration timing of the SPV contributions was clean under Section 17, but Rule 2a-5 governance is the new enforcement frontier.[^31,65]
4. **The 1940-Act exception getting tightened.** If the SEC moves to apply interval-fund-style liquidity discipline to registered CEFs holding ~100% illiquid books — which has been proposed in the past — the structural advantage that justifies BOT's existence narrows.[^36,39]
5. **The benchmark gap doesn't close fast enough.** LIBERO-PRO's 90%→0% collapse[^63] is a 2025 result; if 2026-2027 humanoid VLA research papers extend rather than close the perturbation gap, the Morgan Stanley/Citi TAMs[^57,58] never crystallize into Figure/Apptronik unit volume, and BOT's NAV growth stalls.

**What could vindicate it.** Two paths. First, a Figure or Apptronik IPO at or above the current mark — Figure's $39B post-money[^22] becomes the floor instead of the ceiling, and BOT's premium re-anchors against an exchange-traded comparable. Second, the Roth facility actually closes meaningfully — say, $500M-$1B drawn at average prices well above NAV inside 18 months — at which point BOT has converted retail enthusiasm into permanent capital and the MSTR analogy earns its keep.

The honest summary: BOT is the first registered-CEF wrapper for a private VC book to list on Nasdaq at this premium magnitude. The structural innovation — using the 1940-Act registered-CEF carve-out from Rule 22e-4 to hold ~100% illiquid private positions, with monthly NAV publication as the only governor — is genuinely novel and could plausibly become a category if it works. The base rates against it (DXYZ peak-to-compression, PSH discount persistence, Auburn half-lives) are equally genuine. The next 12 months will tell us which one is right. The CEF literature's prior says 8.1 months.[^43]

:::references
- {id: 1, title: "RoboStrategy Form N-2 Pre-Effective Amendment No. 7 (share count, NAV $7.34, Feb-28 net assets)", url: "https://www.sec.gov/Archives/edgar/data/2081119/000121390026055474/ea0290107-01_n2.htm", source: "SEC EDGAR", date: "2026-05-13"}
- {id: 2, title: "RoboStrategy lists on Nasdaq under ticker BOT", url: "https://www.globenewswire.com/news-release/2026/05/11/3291751/0/en/RoboStrategy-Inc-Lists-on-NASDAQ-Under-Ticker-BOT-Enabling-Investors-to-Access-a-Portfolio-of-Robotics-and-Physical-AI-Companies-in-a-Single-Stock.html", source: "GlobeNewswire", date: "2026-05-11"}
- {id: 3, title: "RoboStrategy Form 424B3 prospectus — Maryland corp, 1940 Act file 811-24118", url: "https://www.sec.gov/Archives/edgar/data/2081119/000121390026052329/ea0287946-02_424b3.htm", source: "SEC EDGAR", date: "2026-05-05"}
- {id: 4, title: "BOT close-price series 2026-05-11 to 2026-05-15", url: "https://finance.yahoo.com/quote/BOT/history", source: "Yahoo Finance (yfinance)", date: "2026-05-15"}
- {id: 5, title: "RoboStrategy Inc (BOT) launches on Nasdaq — ~$730M initial market cap", url: "https://www.gurufocus.com/news/8848601/robostrategy-inc-bot-launches-on-nasdaq-opening-investment-in-robotics", source: "GuruFocus", date: "2026-05-11"}
- {id: 6, title: "What's Going On With RoboStrategy Stock Wednesday? (-15.35% day-3, LULD halts)", url: "https://finance.yahoo.com/news/whats-going-robostrategy-stock-wednesday-141912403.html", source: "Benzinga via Yahoo Finance", date: "2026-05-13"}
- {id: 7, title: "Form N-2 — Day-1 close $39 = 434% premium over $7.31 NAV (3/31/2026)", url: "https://www.sec.gov/Archives/edgar/data/2081119/000121390026055474/ea0290107-01_n2.htm", source: "SEC EDGAR", date: "2026-05-13"}
- {id: 8, title: "Stupidity Is Our Destiny: Historic Closed-End Fund Overpricing (DXYZ 2,070% peak)", url: "https://www.acadian-asset.com/investment-insights/owenomics/stupidity-is-our-destiny-historic-closed-end-fund-overpricing", source: "Acadian Asset Management (Owen Lamont)", date: "2024-05"}
- {id: 9, title: "Yahoo Finance — RoboStrategy lists on Nasdaq under BOT; portfolio includes Figure, Apptronik, Dyna, Standard Bots, Dexmate", url: "https://finance.yahoo.com/markets/stocks/articles/robostrategy-inc-lists-nasdaq-under-110000888.html", source: "Yahoo Finance", date: "2026-05-11"}
- {id: 10, title: "RoboStrategy Enters Into Committed Equity Facility of up to $2B from Roth Principal Investments", url: "https://www.globenewswire.com/news-release/2026/05/15/3295825/0/en/RoboStrategy-Inc-Enters-Into-Committed-Equity-Facility-of-up-to-2-Billion-from-Roth-Principal-Investments-LLC-to-Support-Strategic-Growth-Initiatives.html", source: "GlobeNewswire", date: "2026-05-15"}
- {id: 11, title: "Andrew Kang investor profile — Mechanism Capital co-founder", url: "https://signal.nfx.com/investors/andrew-kang", source: "NFX Signal", date: "2026-05-17"}
- {id: 12, title: "Andrew Kang on X — $19M investment in @Figure_robot disclosed", url: "https://x.com/Rewkang/status/1775751669008974246", source: "Andrew Kang (@Rewkang)", date: "2024-04-04"}
- {id: 13, title: "The Humanoid Thesis (long-form X post)", url: "https://x.com/Rewkang/status/1968392366987121081", source: "Andrew Kang (@Rewkang)", date: "2025-09-17"}
- {id: 14, title: "Andrew Kang on X — co-led Dyna Series A $68M with $120M Apptronik consortium earlier in year", url: "https://x.com/Rewkang/status/1967752568882266485", source: "Andrew Kang (@Rewkang)", date: "2025-09-16"}
- {id: 15, title: "Andrew Kang: Top Crypto Traders — Arkham wallet attribution, mid-8-fig BTC/ETH shorts", url: "https://info.arkm.com/research/andrew-kang-top-crypto-traders", source: "Arkham Intelligence", date: "2026-03-13"}
- {id: 16, title: "Wallet funded by Rewkang opened 40x $100M BTC long after Trump tariff post", url: "https://x.com/lookonchain/status/1909995598340370666", source: "Lookonchain", date: "2025-04-09"}
- {id: 17, title: "Andrew Kang on X — 'Crypto to Deep Tech … a legendary parlay'", url: "https://x.com/Rewkang/status/1888495144296686075", source: "Andrew Kang (@Rewkang)", date: "2025-02-09"}
- {id: 18, title: "Andrew Kang on X — 'no point ramping factory if AI isn't ready yet'", url: "https://x.com/Rewkang/status/1989925174859501894", source: "Andrew Kang (@Rewkang)", date: "2025-11-16"}
- {id: 19, title: "Andrew Kang 100x long liquidations Aug 18 2023", url: "https://www.chaincatcher.com/en/article/2099718", source: "Chain Catcher", date: "2023-08-18"}
- {id: 20, title: "Address associated with Andrew Kang flipped 7,637 ETH long at $3,783", url: "https://chainthink.cn/en/news/57971130633408517", source: "Chainthink", date: "2025-10-17"}
- {id: 21, title: "Mechanism Capital rebrand — 'Still investing on the frontier'", url: "https://x.com/MechanismCap/status/1922278511902872040", source: "Mechanism Capital (@MechanismCap)", date: "2025-05-13"}
- {id: 22, title: "Figure exceeds $1B in Series C funding at $39B post-money valuation", url: "https://www.prnewswire.com/news-releases/figure-exceeds-1b-in-series-c-funding-at-39b-post-money-valuation-302556936.html", source: "PR Newswire (Figure AI)", date: "2025-09-16"}
- {id: 23, title: "Figure reaches $39B valuation — BMW Spartanburg deployment metrics", url: "https://techcrunch.com/2025/09/16/figure-reaches-39b-valuation-in-latest-funding-round/", source: "TechCrunch", date: "2025-09-16"}
- {id: 24, title: "Figure 03 unveiled (production-intent humanoid for BotQ Gen-1 line)", url: "https://www.figure.ai/news/figure-03", source: "Figure AI", date: "2025-10"}
- {id: 25, title: "Apptronik raises $520M at $5B valuation for Apollo robot", url: "https://www.cnbc.com/2026/02/11/apptronik-raises-520-million-at-5-billion-valuation-for-apollo-robot.html", source: "CNBC", date: "2026-02-11"}
- {id: 26, title: "Apptronik press release — Series A extension; Mercedes-Benz, GXO, Jabil, John Deere customers/investors", url: "https://apptronik.com/press-release", source: "Apptronik", date: "2026-02-11"}
- {id: 27, title: "Dyna Robotics raises $120M Series A co-led by RoboStrategy, CRV, First Round", url: "https://www.prnewswire.com/news-releases/dyna-robotics-raises-120-million-to-advance-robotic-foundation-models-on-the-path-to-physical-artificial-general-intelligence-302556817.html", source: "PR Newswire (Dyna Robotics)", date: "2025-09-15"}
- {id: 28, title: "Standard Bots raises $63M Series B led by General Catalyst", url: "https://www.therobotreport.com/standard-bots-raises-63m-to-bring-cobot-arms-to-market/", source: "The Robot Report", date: "2024-07"}
- {id: 29, title: "Dexmate — Vega humanoid $89,999, MIT/UCSD/CMU founders, ~$41M raised", url: "https://tracxn.com/d/companies/dexmate/__rRs0sXlx4Mtmhljwfho_ZZS5AEpDMSYWo3EDCGxHMQE", source: "Tracxn", date: "2026-02-20"}
- {id: 30, title: "Figure BotQ Gen-1 line capacity + monthly ramp", url: "https://www.figure.ai/news/production-at-bmw", source: "Figure AI", date: "2026-04"}
- {id: 31, title: "Form N-2 — in-kind contribution by Kang/Weinstein entities of $74.5M Figure + Apptronik SPV interests at $10/share", url: "https://www.sec.gov/Archives/edgar/data/2081119/000121390026055474/ea0290107-01_n2.htm", source: "SEC EDGAR", date: "2026-05-13"}
- {id: 32, title: "Form 424B3 — Adviser FP Strategies LLC (Puerto Rico), controlled by Kang + Weinstein", url: "https://www.sec.gov/Archives/edgar/data/2081119/000121390026052329/ea0287946-02_424b3.htm", source: "SEC EDGAR", date: "2026-05-05"}
- {id: 33, title: "Form 424B3 — service providers: Grant Thornton (auditor), US Bancorp, US Bank, Computershare", url: "https://www.sec.gov/Archives/edgar/data/2081119/000121390026052329/ea0287946-02_424b3.htm", source: "SEC EDGAR", date: "2026-05-05"}
- {id: 34, title: "Form 424B3 — not RIC for initial fiscal year ending 8/31/2026 (C-corp treatment)", url: "https://www.sec.gov/Archives/edgar/data/2081119/000121390026052329/ea0287946-02_424b3.htm", source: "SEC EDGAR", date: "2026-05-05"}
- {id: 35, title: "Form N-2 — registration form explicitly checks 'Registered Closed-End Fund' (not BDC, not interval)", url: "https://www.sec.gov/Archives/edgar/data/2081119/000121390026055474/ea0290107-01_n2.htm", source: "SEC EDGAR", date: "2026-05-13"}
- {id: 36, title: "Form N-2 — 'no limitation on the portion of the Fund's portfolio that may be invested in illiquid securities'", url: "https://www.sec.gov/Archives/edgar/data/2081119/000121390026055474/ea0290107-01_n2.htm", source: "SEC EDGAR", date: "2026-05-13"}
- {id: 37, title: "Form N-2 — 'double taxation' language; 21% C-corp federal rate", url: "https://www.sec.gov/Archives/edgar/data/2081119/000121390026055474/ea0290107-01_n2.htm", source: "SEC EDGAR", date: "2026-05-13"}
- {id: 38, title: "Form N-2 — Management fee 2.50% of gross assets; Total Annual Expenses 3.22%", url: "https://www.sec.gov/Archives/edgar/data/2081119/000121390026055474/ea0290107-01_n2.htm", source: "SEC EDGAR", date: "2026-05-13"}
- {id: 39, title: "SEC Liquidity Rule (Rule 22e-4) enforcement action vs Pinnacle Advisors — 15% illiquid binds open-end funds only", url: "https://www.proskauer.com/alert/sec-brings-first-liquidity-rule-enforcement-action-against-investment-adviser-and-fund-board", source: "Proskauer Rose LLP", date: "2023"}
- {id: 40, title: "The Ackman Discount — PSH 9% → 40% → 32% widening", url: "https://www.netinterest.co/p/the-ackman-discount", source: "Net Interest (Marc Rubinstein)", date: "2024"}
- {id: 41, title: "Destiny Tech100 (DXYZ) lists on NYSE March 26 2024", url: "https://www.businesswire.com/news/home/20240321816812/en/Destiny-Tech100-DXYZ-to-List-on-New-York-Stock-Exchange-On-March-26-2024", source: "BusinessWire", date: "2024-03-21"}
- {id: 42, title: "DXYZ Form N-CSR — NAV $6.44 (YE2024) → $19.97 (YE2025), +209.59%", url: "https://www.stocktitan.net/sec-filings/DXYZ/n-csr-destiny-tech100-inc-sec-filing-de885898ba06.html", source: "SEC EDGAR / StockTitan", date: "2026-03-09"}
- {id: 43, title: "Mean Reversion in Closed-End Fund Premiums and Discounts — 8.10-month half-life", url: "https://cla.auburn.edu/econwp/Archives/2023/2023-03.pdf", source: "Auburn University Economics Working Paper", date: "2023-03"}
- {id: 44, title: "DXYZ premium/discount and price history", url: "https://ycharts.com/companies/DXYZ/discount_or_premium_to_nav", source: "YCharts", date: "2025-2026"}
- {id: 45, title: "Acadian/Lamont — DXYZ April 8 2024 peak was 'highest premium ever observed in U.S. CEF history'", url: "https://www.acadian-asset.com/investment-insights/owenomics/stupidity-is-our-destiny-historic-closed-end-fund-overpricing", source: "Acadian Asset Management", date: "2024"}
- {id: 46, title: "ARK Venture Fund (ARKVX) — interval-fund alternative; up to 3.49% expense ratio, 5% quarterly tender", url: "https://www.ark-funds.com/articles/venture-commentary/why-we-believe-ark-venture-fund-arkvx-provides-better-access-to-private-companies-than-an-exchange-traded-closed-end-fund-like-dxyz", source: "ARK Invest", date: "2024"}
- {id: 47, title: "Form N-2 — Roth $2B committed equity facility, 36-month draw, 14.1M resale shares", url: "https://www.sec.gov/Archives/edgar/data/2081119/000121390026055474/ea0290107-01_n2.htm", source: "SEC EDGAR", date: "2026-05-13"}
- {id: 48, title: "Form N-2 — Drawdown mechanism: VWAP minus 2.0%, per-draw cap 2M shares", url: "https://www.sec.gov/Archives/edgar/data/2081119/000121390026055474/ea0290107-01_n2.htm", source: "SEC EDGAR", date: "2026-05-13"}
- {id: 49, title: "Form N-2 — Use of proceeds: up to $2B gross to fund investments", url: "https://www.sec.gov/Archives/edgar/data/2081119/000121390026055474/ea0290107-01_n2.htm", source: "SEC EDGAR", date: "2026-05-13"}
- {id: 50, title: "Press release — $13.45 base price floor, 19.99% Nasdaq exchange cap of 4,052,806 shares", url: "https://www.globenewswire.com/news-release/2026/05/15/3295825/0/en/RoboStrategy-Inc-Enters-Into-Committed-Equity-Facility-of-up-to-2-Billion-from-Roth-Principal-Investments-LLC-to-Support-Strategic-Growth-Initiatives.html", source: "GlobeNewswire", date: "2026-05-15"}
- {id: 51, title: "Roth Principal Investments precedent — Fusemachines $20M CEPA terms (VWAP -3% intraday / -5% off-hours, 1.5% commitment fee)", url: "https://www.stocktitan.net/sec-filings/FUSE/8-k-fusemachines-inc-reports-material-event-423637bb0b02.html", source: "SEC EDGAR / StockTitan", date: "2025-10"}
- {id: 52, title: "X commentary — BOT 5x premium to NAV, MicroStrategy comparison framing", url: "https://x.com/search?q=%24BOT+NAV+premium", source: "X / Twitter", date: "2026-05-15"}
- {id: 53, title: "X commentary — '$BOT is a levered robotics play ... like $MSTR before the market understood their wrapper'", url: "https://x.com/search?q=%24BOT+MicroStrategy+robotics", source: "X / Twitter", date: "2026-05-15"}
- {id: 54, title: "Form N-2 resale prospectus — VWAP -2%, $13.45 floor, 14.1M shares registered", url: "https://www.sec.gov/Archives/edgar/data/2081119/000121390026055474/ea0290107-01_n2.htm", source: "SEC EDGAR", date: "2026-05-13"}
- {id: 55, title: "Andrew Kang on X — '$1 quadrillion at 20B robots' framing", url: "https://x.com/Rewkang/status/1923372713042673823", source: "Andrew Kang (@Rewkang)", date: "2025-05-16"}
- {id: 56, title: "Goldman Sachs — humanoid robot market could reach $38B by 2035", url: "https://www.goldmansachs.com/insights/articles/the-global-market-for-robots-could-reach-38-billion-by-2035", source: "Goldman Sachs Research", date: "2024-01"}
- {id: 57, title: "Morgan Stanley / Adam Jonas — humanoid TAM $5T by 2050", url: "https://www.cnbc.com/2025/04/29/how-to-play-a-5-trillion-market-for-humanoid-robots-by-2050.html", source: "CNBC (summarizing Morgan Stanley 'Humanoid 100')", date: "2025-04-29"}
- {id: 58, title: "Citi — The Rise of AI Robots: ~650M humanoids generating $7T by 2050", url: "https://www.citigroup.com/global/insights/the-rise-of-ai-robots-humanoids-are-coming-for-you", source: "Citi Research", date: "2024-11-04"}
- {id: 59, title: "Tesla Optimus production update — 2025 target missed; 10M/yr Texas goal 2027", url: "https://electrek.co/2026/04/22/tesla-optimus-production-fremont-model-sx-line/", source: "Electrek", date: "2026-04-22"}
- {id: 60, title: "PitchBook — humanoid VC funding $6.1B/139 deals (2025) vs $1.5B/65 deals (2024)", url: "https://pitchbook.com/news/articles/apptronik-raises-520m-as-vc-funding-for-humanoid-robotics-explodes-300", source: "PitchBook", date: "2026"}
- {id: 61, title: "China dominates 90% of 2025 humanoid shipments — Omdia data, USCC report", url: "https://www.uscc.gov/sites/default/files/2024-10/Humanoid_Robots.pdf", source: "US-China Economic and Security Review Commission", date: "2024-10"}
- {id: 62, title: "Humanoid robot cost-per-hour analysis — $50K humanoid breakeven at ~$20/hr US labor", url: "https://www.cleantechnica.com/2026/05/03/the-humanoid-robot-market-is-smaller-than-it-looks/", source: "CleanTechnica", date: "2026-05-03"}
- {id: 63, title: "LIBERO-PRO — VLA models collapse 90%+ to 0% under perturbations", url: "https://arxiv.org/abs/2510.03827", source: "arXiv preprint", date: "2025-10"}
- {id: 64, title: "NVIDIA GR00T N1 on Fourier GR-1 — 82% pick-place, 70.9% articulated manipulation", url: "https://arxiv.org/pdf/2503.14734", source: "arXiv (NVIDIA)", date: "2025-03"}
- {id: 65, title: "Form N-2 — Adviser designated as valuation agent under Rule 2a-5; third-party valuation firm referenced but not named", url: "https://www.sec.gov/Archives/edgar/data/2081119/000121390026055474/ea0290107-01_n2.htm", source: "SEC EDGAR", date: "2026-05-13"}
- {id: 66, title: "Form N-2 SAI Conflicts — Other Accounts may commit larger percentage than the Fund", url: "https://www.sec.gov/Archives/edgar/data/2081119/000121390026055474/ea0290107-01_n2.htm", source: "SEC EDGAR", date: "2026-05-13"}
- {id: 67, title: "Mechanism Capital portfolio — pre-RoboStrategy positions in Figure (2024), Apptronik (2025), Dyna (2025)", url: "https://mechanism.capital", source: "Mechanism Capital", date: "2026-05-17"}
- {id: 68, title: "Mechanism Capital retweets RoboStrategy $2B Roth facility announcement", url: "https://x.com/MechanismCap/status/2055270502344646869", source: "Mechanism Capital (@MechanismCap)", date: "2026-05-15"}
- {id: 69, title: "X commentary — '$BOT it's all about the narrative'; influencer-driven low-float price action", url: "https://x.com/search?q=%24BOT+narrative+influencer", source: "X / Twitter", date: "2026-05-12"}
- {id: 70, title: "Pump.fun Solana meme token FVo5hJRs97EwPzDnAPkVPfHTvv5AqdmZtmuZKZDjpump attached to BOT ticker", url: "https://pump.fun/coin/FVo5hJRs97EwPzDnAPkVPfHTvv5AqdmZtmuZKZDjpump", source: "Pump.fun", date: "2026-05-15"}
:::
