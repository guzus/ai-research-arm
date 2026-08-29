---
eyebrow: CRYPTO · MARKET STRUCTURE
title: "Whose Blockspace Is It, Anyway?"
deck: A Titan Builder CEO says regulators have Ethereum's MEV fight backwards. The citations he leans on don't say what his article implies, the "neutral infrastructure" he's defending isn't neutral, and the system he's calling institution-ready is still, by his own admission, under construction.
lede: |
  On July 15, 2026, Kubi Mensah — CEO of Gattaca, whose Titan Builder builds roughly half of all Ethereum blocks — published a rebuttal to DRW founder Don Wilson's *Financial Times* op-ed and a chain of regulator commentary (IOSCO, ESMA, the SEC) that Mensah says wrongly equates MEV with market manipulation. His argument: blockspace is a scarce, periodically produced "ordinal commodity," transparent competitive auctions are the correct way to allocate it, and institutions already have the tools to participate safely. Checking each load-bearing claim against primary sources tells a messier story than either side's framing admits.
domain: crypto
stats:
  - {label: Titan Builder share, value: "52%", note: "of ETH blocks, Jul 2026"}
  - {label: Sandwich losses, value: "$40-60M", note: "annual, 2025, declining"}
  - {label: "\"Benign\" MEV cost to LPs", value: "$600M+", note: "standing LVR estimate"}
  - {label: ePBS status, value: Devnet, note: "Glamsterdam fork, mid-2026"}
---

:::callout(kind=info, label="Direct answer")
- Regulators have **not** concluded MEV is market manipulation. IOSCO treats it as a disclosure/control-risk factor [^3] [^4], ESMA's strongest language is a hedged 2024 draft consultation and a 2025 research note calling for "more analysis" [^5] [^6], and the SEC's own staff memo says searchers/builders following protocol rules are not being treated as manipulative [^8].
- The UBS/Nethermind pilot Mensah cites as proof institutions can already comply was two **testnet-only** proofs of concept on Sepolia, with zero live transactions [^11].
- Mensah's own company, Titan Builder, builds **~52% of Ethereum blocks** [^19] [^20] — the "neutral infrastructure" framing elides that he runs the dominant firm in the market he's defending.
- Ethereum's own core developers and Mensah's own separate technical writing both describe today's builder/relay system as having "structural gaps" [^28] [^31] — not the mature, institution-ready architecture the article implies.
- The "benign vs. predatory MEV" split holds for the narrowest reading (sandwich attacks, ~$40-60M/yr [^24]) but not for the broader one: arbitrage extraction from liquidity providers is estimated at $600M+ [^26], an order of magnitude larger.
:::

## 01. The rebuttal, and who's arguing it

Mensah's article is explicitly a response: Don Wilson, founder of DRW and its crypto-market-making arm Cumberland, wrote an FT op-ed in late May 2026 arguing that some blockchains "enable front-running" and that regulators should enforce existing anti-front-running rules against MEV rather than write bespoke crypto rules [^1]. Wilson's piece draws a real distinction — he separates ordinary arbitrage from MEV where "profits depend on controlling transaction order," calling only the latter front-running [^1] — but that nuance gets flattened once the argument becomes "Wilson vs. Mensah," each side speaking as if the other represents an undifferentiated position.

Neither side discloses the obvious commercial stake it's arguing from. DRW is a 1992-founded, 1,200-to-2,000-employee proprietary trading firm; Cumberland is its dedicated crypto liquidity desk [^27]. Institutional-sized orders of exactly the kind Cumberland routes are the orders most exposed to public-mempool front-running — so a rule that pushes crypto market structure toward TradFi-style "lit," non-reorderable execution venues would directly lower Cumberland's own execution costs [^27]. Gattaca is smaller but no less interested: founded in London in 2018, it went through Y Combinator, has roughly 19 employees and one disclosed funding round as of mid-2026 [^30] — and its entire commercial model is selling access to the block-building and relay infrastructure whose legitimacy is exactly what Mensah's article defends.

:::kv
- {term: Gattaca / Titan, def: "Founded 2018, London; YC alum; ~19 employees; one disclosed 2021 seed round"}
- {term: DRW / Cumberland, def: "Founded 1992; ~1,200-2,000+ employees; Cumberland is its crypto trading arm"}
- {term: Titan Builder share, def: "~52% of Ethereum blocks (Jul 2026)"}
- {term: Cumberland's stake, def: "Large institutional orders are exposed to the front-running Wilson describes"}
:::

Neither of these financial interests makes either man's technical claims wrong. But they explain why the debate reads less like disinterested market-design theory and more like two infrastructure operators each arguing for the rules that favor the infrastructure they already own — which is precisely why the underlying claims are worth checking independently rather than accepting either framing at face value.

:::statement(attr="ARA Research")
Both sides of this fight are arguing for the market structure that pays them — which is a reason to check the citations, not a reason either side is wrong.
:::

## 02. What the regulators actually said

Mensah's article treats "IOSCO, ESMA, and SEC" as a chorus concluding that MEV is manipulative. The primary documents don't support that reading.

IOSCO's relevant text is not a manipulation finding at all — it's a December 2023 policy report on DeFi that lists MEV strategies as one factor regulators should weigh when assessing whether someone exercises "control" over a DeFi arrangement, for disclosure purposes [^3]. A later October 2025 IOSCO thematic review goes further only in flagging inconsistent MEV handling across custodians and validators as a *transparency* gap, not a manipulation determination [^4]. ESMA's strongest language sits in a hedged May 2024 draft MiCA technical-standards consultation — "may be indicative of" market abuse — and a July 2025 research article that explicitly calls for "more analysis grounded on robust evidence" before any policy conclusion [^5] [^6]. A named industry lawyer, Jonathan Galea, has separately disputed press characterizations of the 2024 ESMA draft as a "clear example of market abuse," pointing out the actual text only says "may be indicative" [^5].

The SEC citation is doing even less work than either of those. The April 13, 2026 staff statement Mensah cites is titled *Staff Statement Regarding Broker-Dealer Registration of Certain User Interfaces* — it is about whether DeFi front-end and wallet-interface software needs broker-dealer registration, and does not discuss block builders, validators, or Ethereum ordering mechanics anywhere in its text [^7]. It contains one hedged footnote noting that "altered sequencing of transactions may be abused... in certain so-called MEV strategies," which is the closest thing to an MEV reference in the document [^7]. It is also explicitly an interim staff position, not Commission rulemaking, with a built-in five-year sunset [^7]. A separate SEC Crypto Task Force staff memo from May 2025 states plainly that searchers and block builders "operating according to the understood protocol rules" are treated differently from deceptive exploits — the SEC's own staff position is that ordinary MEV activity is *not* being pursued as manipulation [^8].

:::timeline
- {date: "2023-12", headline: "IOSCO DeFi policy report", body: "Lists MEV as a disclosure/control-risk factor for DeFi arrangements — not a manipulation finding."}
- {date: "2024-05", headline: "ESMA draft MiCA consultation", body: "Hedged language: validator reordering 'may be indicative of' market abuse. Open for comment, not final."}
- {date: "2025-05", headline: "SEC Crypto Task Force staff memo", body: "States searchers/builders following protocol rules are distinguished from deceptive exploits."}
- {date: "2025-07", headline: "ESMA MEV research article", body: "Calls explicitly for 'more analysis grounded on robust evidence' before any policy step."}
- {date: "2025-10", headline: "IOSCO thematic review", body: "MEV reframed as a custodian/validator disclosure-consistency issue."}
- {date: "2026-04", headline: "SEC staff statement on user interfaces", body: "About DeFi front-end broker-dealer status; contains one hedged MEV footnote, not an MEV ruling."}
:::

The overstatement isn't really about terminology — regulators' technical use of "MEV" tracks the crypto-native taxonomy reasonably well, consistently separating arbitrage/liquidation from front-running-style reordering. The overstatement is about *status*: hedged consultation drafts and research notes calling for more evidence are being cited as if they were settled findings, which they are not [^5] [^6].

## 03. Is anyone actually being prosecuted?

If MEV really were being treated as manipulation, there would be cases. There are two, and neither supports the "MEV is being enforced against" framing as directly as it might seem.

*United States v. Peraire-Bueno* — the closest thing to an MEV prosecution — charges two MIT-trained brothers with wire fraud and money laundering over an alleged $25 million exploit, not securities or commodities market manipulation [^9]. The government's theory rests on an allegedly forged validator signature and deliberately crafted "lure" transactions — a deception theory, not a "profiting from visible transaction order is illegal" theory. The case ended in a mistrial in November 2025, with a Rule 29 hearing in February 2026 and no verdict as of the most recent reporting [^9]. The nearest comparable conviction — Avraham Eisenberg's Mango Markets case, another on-chain exploit prosecuted as manipulation — was fully vacated in May 2025 on improper-venue and failure-to-prove-misrepresentation grounds, with DOJ's appeal still pending [^10]. Courts have so far been resistant to stretching manipulation/fraud theories onto protocol-permitted conduct, not eager to extend them.

On the regulatory side, MiCA's Title VI market-abuse provisions are the most plausible vehicle for an actual EU enforcement case, and national competent authorities were still completing their compliance rollout for the underlying guidelines through September 2026 [^44] — there is, as of this writing, no active case pipeline. Whether MiCA's operative due-diligence duty (Article 92) even reaches validators, builders, or searchers — as opposed to licensed crypto-asset service providers — is itself contested in the legal literature, with one compliance-consultancy reading it narrowly (validators are carved out by Recital 93) and academic commentary arguing the opposite [^45] [^46].

:::callout(kind=warn, label="What this means")
As of mid-2026, MEV-as-manipulation enforcement is prospective, not live. The one real prosecution targets an alleged deception (forged signatures, bait transactions), and its closest precedent was thrown out on appeal. Regulators warning about MEV and regulators *acting* on MEV are two different things — and today, only the first is happening.
:::

## 04. The "ordinal commodity" argument, tested

The technical core of Mensah's piece is a claim that blockspace is an "ordinal commodity" — value depends not just on whether a transaction is included in a block but on its *position* within it — and that competitive, transparent auctions (Proposer-Builder Separation, or PBS) are the correct market design for allocating that position, citing Budish, Cramton & Shim's 2015 *Quarterly Journal of Economics* paper on frequent batch auctions as theoretical backing [^16].

The "ordinal commodity" phrase itself appears to be Mensah's own coinage — it is the title of his own April 2026 EthCC talk, and a search of the prior transaction-fee-mechanism-design literature (Roughgarden's EIP-1559 papers, which use auction-theory terms like UIC and MMIC rather than "ordinal good") turns up no earlier use [^37]. That doesn't make the framing wrong, but it means it should be read as a fresh argument, not an established term Mensah is merely applying.

The Budish-Cramton-Shim citation is genealogically real but doing more work than it can bear. BCS analyze a continuous-time, cross-venue latency-arbitrage problem among symmetric competitors, cleared by a neutral, unforkable exchange utility — their proposed fix (discrete-time batch auctions) replaces speed competition with price competition *within that trusted-clearing-house setting* [^16]. Ethereum's actual PBS mechanism is a different kind of market: a sealed-bid auction adjudicated, each ~12-second slot, by a single economically interested proposer, mediated by a small oligopoly of relays that most builders and proposers must trust [^17]. That is precisely the kind of privileged intermediary position BCS's design was meant to rule out, not reproduce. The academic bridge between the two settings runs through Daian et al.'s 2019 "Flash Boys 2.0" paper, which imported the HFT-frontrunning analogy into DeFi — but that same paper also identified a risk with no TradFi equivalent: sufficiently large MEV can incentivize validators to reorganize the chain itself ("time-bandit attacks"), turning MEV into a consensus-security problem, not merely a market-microstructure inefficiency [^38]. Even research on batch auctions implemented directly on-chain (not just MEV-Boost) finds that "the block builder's current ability to rearrange the batch content is certainly sufficient to extract value" — the discrete-slot, single-block-producer structure reintroduces an ordering privilege that BCS's continuous, multilateral clearing model never had to contend with [^39].

None of this means competitive auctions are the wrong design — they plausibly beat pure latency races, which is BCS's actual, narrower point. It means the specific claim "this is a Budish-Cramton-Shim batch auction, therefore it has batch-auction guarantees" doesn't survive contact with how MEV-Boost actually works today.

## 05. Who controls the blockspace?

Mensah's article draws a line between "neutral" builder infrastructure (analogous to an exchange) and "predatory" searchers running extractive strategies, arguing regulation should target the latter. That framing is harder to sustain once you look at how concentrated the "neutral infrastructure" layer actually is.

Titan Builder built roughly 52-54% of Ethereum blocks as of mid-July 2026, with the next-largest builder, Quasar, at under 22% [^19]. Independent research from Coin Metrics pegged Titan's share at 47.6% as of March 2026 and explicitly frames block-building concentration as a censorship-resistance risk, not a company-specific concern [^20]. A peer-reviewed 2024 paper found the top three builders built roughly 80% of MEV-Boost blocks, driven substantially by exclusive order-flow deals that reduce genuine competition between builders [^21] — and the field has only consolidated further since: Beaverbuild, previously an independent counterweight to Titan, folded its order flow into the multi-party BuilderNet consortium during 2025 [^22], leaving effectively one dominant single company and one multi-party alternative.

:::rank-list
- {label: Titan Builder, value: "52.6%", pct: 100, highlight: true}
- {label: Quasar, value: "21.7%", pct: 41}
- {label: BuilderNet, value: "10.2%", pct: 19}
- {label: Eureka, value: "8.0%", pct: 15}
:::

Titan's own relay compounds the concern rather than resolving it. Gattaca operates both the leading builder and a major relay — Titan Relay, ranked #2 among relays by share [^23] — and the one independent institutional reviewer to examine that structure, Lido's Relay Maintenance Committee, approved Titan Relay in May 2024 only *conditionally*, explicitly naming the vertical integration of builder and relay in one company as a risk that could let Titan's own builder win bids "that don't seem competitive," and recommending ongoing monitoring rather than a clean bill of health [^18]. Mensah's own April 2024 public statement that "our relay will not be vertically integrated" [^2] is the only public rebuttal on record — it is party testimony, not independent verification, and no subsequent independent audit has closed the question the RMC left open.

On the specific axis of OFAC censorship — a separate but related concentration risk — Titan Relay is currently classified non-censoring, and the network-wide picture has genuinely improved from its post-Merge peak: 94.8% of blocks were OFAC-compliant/censoring at the October 2022 high, against 39.1% as of mid-July 2026 (up from an April 2026 trough of 23.8%) [^23]. That volatility is itself a symptom of the underlying structure critics point to — a handful of dominant builders and relays choosing whether to comply, with the network-wide censorship rate swinging on their individual decisions rather than any systemic guarantee [^23].

None of this proves Titan behaves badly. It does mean "builders are neutral infrastructure, distinct from predatory searchers" is being asserted by the CEO of the single most dominant builder in the market, about a market structure whose most rigorous independent reviewer (Lido's RMC) treats his own company's conflict of interest as an open, monitored risk rather than a settled non-issue [^18].

## 06. Benign vs. predatory MEV, by the numbers

The article's other central claim is that "MEV" wrongly lumps efficient activity (arbitrage, liquidations, oracle updates) together with a smaller, genuinely predatory subset (sandwich attacks) — and that regulation should target only the latter. This is the industry's own long-standing framing, articulated plainly by Paradigm's foundational MEV research: a bot that arbitrages a market back to parity "makes the market more efficient without harming the original trader" [^41]. The claim survives on its narrowest reading and collapses on its broadest one.

Sandwich attacks are real, quantifiable, and shrinking: EigenPhi-sourced data covering November 2024 through October 2025 estimates $40-60 million in annual trader losses, with monthly extraction falling from roughly $10 million to $2.5 million over that window even as attack frequency stayed elevated [^24]. That decline is genuine and worth noting on its own terms.

:::compare
- {role: LOWEST, name: "Oct 2025 (monthly)", value: "$2.5M"}
- {role: HIGHEST, name: "Late 2024 (monthly)", value: "$10M"}
- {role: SUBJECT, name: "Sandwich extraction", value: "$2.5M"}
:::

But sandwich losses are a rounding error next to "benign" arbitrage's actual cost. Loss-versus-rebalancing (LVR) research — the formal model for exactly the value an arbitrage bot captures by trading against a stale AMM price — estimates upwards of $600 million extracted from Ethereum liquidity providers, an order of magnitude larger than all sandwich losses combined [^26] [^25]. That cost doesn't disappear because no single identifiable victim exists per transaction; it gets priced into wider LP fees and spreads that every ordinary swapper eventually pays, just diffusely rather than via one traceable sandwich [^25]. Layer on top a further externality Flashbots' own research documents: on OP-Stack rollups, arbitrage-searcher spam — hundreds of low-margin probing transactions per successful arbitrage — consumes more than half of total gas on some chains while paying under a tenth of total fees, pushing baseline transaction costs up for everyone [^42]. And even where arbitrage generates a clean profit, searchers reportedly pay more than 90% of gross revenue upstream to block proposers and builders — functioning less like a diffuse public good and more like a rent captured by a concentrated supply-chain layer [^32].

:::note
The sandwich-attack figures ($40-60M/yr) and the LVR estimate ($600M+) are measured on different bases — one is a trailing-twelve-month EigenPhi tally, the other a standing academic estimate not re-measured for 2025-2026 — so treat the comparison as an order-of-magnitude contrast, not a like-for-like accounting reconciliation.
:::

The "benign vs. predatory" dichotomy, in other words, isn't wrong so much as it's measuring the wrong thing: sandwich attacks have a legible, transaction-level attacker-victim story that makes them easy to count and easy to condemn; arbitrage's cost is real, larger, and simply laundered through LP economics and network congestion where no single attacker-victim pair is visible in any one transaction.

## 07. Is PBS actually ready for institutions?

Underlying Mensah's whole argument is the premise that today's PBS/MEV-Boost system is a mature enough architecture for institutions to trust. Ethereum's own core developers, and Mensah's own separate technical writing, describe it differently.

Enshrined PBS (ePBS, EIP-7732) — the protocol-level fix designed specifically to remove the relay-trust dependency that today's out-of-protocol MEV-Boost system requires — is the headline feature of the upcoming Glamsterdam hard fork, and remained in devnet testing as of mid-2026 [^28]. The Ethereum Foundation's own Checkpoint blog describes the implementation work as "trickier than anticipated" [^28] — not the language of a team confirming a finished, low-risk change. Independent researchers go further: a December 2025 analysis argues that even once ePBS ships, "side-car" bidding systems will still be necessary, because ePBS's staking requirement excludes smaller builders and doesn't fully resolve today's relay-latency and trust problems [^29] — meaning no version of PBS, current or next-generation, is being presented by the people building it as a finished end state.

:::timeline
- {date: "2024-05", headline: "MEV-Boost dominance", body: "Out-of-protocol PBS via MEV-Boost carries the vast majority of Ethereum blocks; relay trust is a known, accepted dependency."}
- {date: "2026-04", headline: "ePBS 'trickier than anticipated'", body: "EF's Checkpoint #9 blog describes enshrined-PBS implementation work as harder than expected."}
- {date: "2026-05", headline: "Mensah co-authors MPBC proposal", body: "Multi-Party Block Construction post [^31] states plainly: 'today's transaction pipeline has structural gaps.'"}
- {date: "2026-07", headline: "Article published", body: "Mensah's 'What Institutions Should Know About Blockspace' frames the current PBS regime as institution-ready."}
:::

The tension is sharpest in Mensah's own words. His co-authored Multi-Party Block Construction proposal, posted to Ethereum's research forum on May 27, 2026 — roughly seven weeks before his institutional-blockspace article — states plainly that "today's transaction pipeline has structural gaps that multiple teams and the community have worked to address" [^31]. That is Mensah, in a technical venue read by his peers, conceding exactly the immaturity his institutional-facing article is written to talk past.

The supporting "tools already exist" claim (private mempools, encrypted flow, TEEs) is similarly mixed rather than settled. SUAVE, Flashbots' flagship encrypted-mempool project and the most-cited example of "mitigation infrastructure already built," was discontinued and its repository archived in May 2025 without ever reaching mainnet [^12]. Flashbots' BuilderNet, a TEE-based alternative, genuinely is in live production since December 2024 [^13] — but the confidentiality guarantees its TEE model relies on were credibly challenged by an October 2025 "TEE.Fail" disclosure demonstrating a hardware-level break capable of undetectable frontrunning, a threat Flashbots disputes as impractical to exploit remotely but has not made disappear [^14]. Shutter Network's threshold-encrypted mempool is real and running in production — on Gnosis Chain, a separate, lower-value network; Ethereum-mainnet integration remained targeted for the following few months as of December 2025, with the in-protocol standard (EIP-8105) still a first draft [^15].

## 08. The TradFi mirror that doesn't quite reflect

The implicit comparison running through Mensah's piece — that MEV is structurally like payment-for-order-flow or dark-pool trading in traditional markets, and that TradFi "solved" this with disclosure and competition rather than outright bans — doesn't hold up as a description of TradFi in 2026, let alone as a template for crypto.

TradFi hasn't settled on "disclosure, not bans." The two jurisdictions most often cited moved in opposite directions in the same month: the EU's PFOF prohibition under MiFIR Article 39a became absolute on June 30, 2026, when Germany's last transitional exemption expired [^33] — an outright ban — while the US SEC proposed *rescinding* Reg NMS Rules 611 and 610(e), the order-protection framework, on June 11, 2026, moving toward less structural regulation, not more [^34]. The SEC's own 2022 proposed Order Competition Rule, which would have addressed PFOF-style conflicts directly, was never finalized [^34]. "TradFi picked disclosure over bans" isn't a consensus; it's one jurisdiction's current, and possibly temporary, choice, sitting opposite another major jurisdiction's opposite choice.

More importantly, the analogy skips past a structural gap the user of this framing needs to confront directly: TradFi's disclosure regime sits on top of an independently enforceable legal duty that disclosure alone does not satisfy. FINRA Rule 5310 imposes a real, litigable best-execution duty on US broker-dealers — regulators have been explicit that order-routing disclosures do not excuse a firm from that duty [^35]. No comparable duty currently binds an Ethereum block builder, relay operator, or searcher. If anything, the SEC's own April 2026 relief for DeFi interface providers is built to keep it that way: qualifying providers must *not* exercise routing discretion or offer "best price" commentary, which is precisely the kind of discretion that creates fiduciary duty in TradFi [^36] [^7]. The result is that the US is currently constructing a "no fiduciary duty" safe harbor for crypto interfaces by design, not failing to notice the gap the TradFi analogy glosses over.

| Dimension | TradFi (US, mid-2026) | TradFi (EU, mid-2026) | Ethereum PBS |
|---|---|---|---|
| PFOF / order-flow payment | Disclosed, not banned; structural rule being rescinded [^34] | *Banned outright since Jun 30, 2026 [^33]* | No equivalent prohibition or disclosure regime |
| Best-execution duty | FINRA Rule 5310, independently enforceable [^35] | Comparable MiFID II duties | No equivalent legal duty on builders/relays/searchers |
| Regulatory direction, 2026 | Deregulating (Reg NMS rescission) [^34] | Tightening (PFOF ban) [^33] | Prospective only; no live enforcement [^8] [^9] |

Whether the question is even legally live is itself contested: industry submissions to the SEC have argued that MEV searchers, validators, and builders could be "brokers" or "dealers" under existing statutory categories, while a rebuttal from DeFi advocates insists infrastructure isn't intermediation [^7]. The one statutory vehicle that might have reached "de facto market makers" closest to on-chain searchers — the SEC's expanded dealer-definition rule — was vacated by a federal court in late 2024 [^7], leaving no current legal hook in place. Even a policy paper that takes the PFOF-MEV analogy seriously concludes broker-dealer-style licensing shouldn't be extended to block builders or relay operators anyway, for reasons distinct from the enforcement-duty gap [^40]. Net effect: the TradFi comparison is a useful starting frame, not a settled precedent either side can lean on as fully decided.

## 09. What would change this assessment

This isn't a case for treating MEV as manipulation, nor a case that Mensah's framing is worthless — several of his technical points hold up: sandwich-attack losses genuinely are small and shrinking [^24]; competitive ordering plausibly does beat pure latency races, in the spirit (if not the letter) of Budish-Cramton-Shim [^16]; and real MEV-mitigation infrastructure (BuilderNet, Shutter) does exist, just less matured than "already solved" implies [^13] [^15]. The counter-evidence assembled here is strongest on three points, each individually falsifiable by future events:

If an independent audit of Titan Relay's bid-allocation data were to show no preferential treatment of Titan's own builder over the monitoring period Lido's RMC specified, the vertical-integration concern in Section 05 would be substantially weakened [^18]. If ePBS ships on schedule in the Glamsterdam fork and demonstrably removes the relay-trust dependency without requiring the side-car systems independent researchers currently expect, the "PBS isn't finished" argument in Section 07 would need updating [^28] [^29]. And if a regulator anywhere brings an actual enforcement action against ordinary MEV activity — as opposed to the deception-based Peraire-Bueno theory — within the next 12-18 months, the "enforcement risk is purely prospective" conclusion in Section 03 would need to be revisited [^9] [^44].

Conversely, the case against treating current infrastructure as fully institution-ready would strengthen further if Titan's block share keeps climbing past its current ~52% without a credible independent competitor emerging, or if another TEE-based vulnerability class following TEE.Fail surfaces before BuilderNet's confidentiality model is hardened [^14] [^19].

As of this research pass, no independent commentary specifically addressing Mensah's July 15 article had yet surfaced — this is a live, one-day-old debate, not one with settled public consensus in either direction [^2].

:::references
- {id: 1, title: "Bad Behavior Is Moving Markets. Where Are the Regulators?", url: "https://www.drw.com/updates/insights/financial-times-how-some-blockchains-enable-front-running", source: "Financial Times / DRW republication", date: "2026-05-26"}
- {id: 2, title: "What Institutions Should Know About Blockspace", url: "https://x.com/kubimensah/status/2077388130676584829", source: "Kubi Mensah / X", date: "2026-07-15"}
- {id: 3, title: "Final Report with Policy Recommendations for Decentralized Finance", url: "https://www.iosco.org/library/pubdocs/pdf/ioscopd754.pdf", source: "IOSCO", date: "2023-12-19"}
- {id: 4, title: "Thematic Review Assessing the Implementation of IOSCO Recommendations", url: "https://www.iosco.org/library/pubdocs/pdf/IOSCOPD801.pdf", source: "IOSCO", date: "2025-10"}
- {id: 5, title: "ESMA targets MEV as potential market abuse in MiCA proposal", url: "https://crypto.news/esma-targets-mev-as-potential-market-abuse-in-mica-proposal/", source: "crypto.news", date: "2024-05-27"}
- {id: 6, title: "Maximal Extractable Value: Implications for crypto markets", url: "https://www.esma.europa.eu/sites/default/files/2025-07/ESMA50-481369926-29744_Maximal_Extractable_Value_Implications_for_crypto_markets.pdf", source: "ESMA (TRV)", date: "2025-07-01"}
- {id: 7, title: "Staff Statement Regarding Broker-Dealer Registration of Certain User Interfaces", url: "https://www.sec.gov/newsroom/speeches-statements/staff-statement-regarding-broker-dealer-registration-certain-user-interfaces-utilized-prepare-staff-statement-regarding-broker-dealer-registration-certain-user-interfaces-utilized", source: "U.S. SEC", date: "2026-04-13"}
- {id: 8, title: "Crypto Task Force staff memo", url: "https://www.sec.gov/files/ctf-memo-paradigm-cooley-051525.pdf", source: "U.S. SEC Crypto Task Force", date: "2025-05-15"}
- {id: 9, title: "United States v. Peraire-Bueno docket", url: "https://www.courtlistener.com/docket/68532791/united-states-v-peraire-bueno/", source: "CourtListener / federal docket", date: "2026-02-26"}
- {id: 10, title: "Federal judge overturns all criminal convictions in Mango Markets case", url: "https://www.trmlabs.com/resources/blog/breaking-federal-judge-overturns-all-criminal-convictions-in-mango-markets-case-against-avraham-eisenberg", source: "TRM Labs", date: "2025-05"}
- {id: 11, title: "UBS and Nethermind Ethereum compliance pilot", url: "https://www.ubs.com/global/en/media/display-page-ndp/en-20260623-nethermind.html", source: "UBS", date: "2026-06-23"}
- {id: 12, title: "flashbots/suave-geth (archived)", url: "https://github.com/flashbots/suave-geth", source: "GitHub / Flashbots", date: "2025-05-12"}
- {id: 13, title: "Migrating to BuilderNet", url: "https://writings.flashbots.net/migrating-to-buildernet", source: "Flashbots Writings", date: "2024-12-05"}
- {id: 14, title: "TEE.fail attack breaks confidential computing on Intel, AMD, Nvidia CPUs", url: "https://www.bleepingcomputer.com/news/security/teefail-attack-breaks-confidential-computing-on-intel-amd-nvidia-cpus/", source: "BleepingComputer", date: "2025-10"}
- {id: 15, title: "The first encrypted mempool is coming to PBS on Ethereum", url: "https://blog.shutter.network/the-first-encrypted-mempool-is-coming-to-pbs-on-ethereum/", source: "Shutter Network", date: "2025-12"}
- {id: 16, title: "The High-Frequency Trading Arms Race: Frequent Batch Auctions as a Market Design Response", url: "https://academic.oup.com/qje/article/130/4/1547/1916146", source: "Budish, Cramton, Shim — QJE", date: "2015"}
- {id: 17, title: "SoK: MEV countermeasures and PBS trust assumptions", url: "https://arxiv.org/pdf/2412.18074", source: "arXiv", date: "2024-2026"}
- {id: 18, title: "Titan Relay RMC assessment", url: "https://operatorportal.lido.fi/public/relay-maintenance-committee/rmc-relay-assessments/add-titan-relays", source: "Lido Relay Maintenance Committee", date: "2024-05-06"}
- {id: 19, title: "relayscan.io builder dashboard", url: "https://www.relayscan.io/", source: "relayscan.io", date: "2026-07-15"}
- {id: 20, title: "State of the Network, Issue 356", url: "https://coinmetrics.substack.com/p/state-of-the-network-issue-356", source: "Coin Metrics", date: "2026-03-24"}
- {id: 21, title: "Builder dominance and exclusive order flow on Ethereum", url: "https://arxiv.org/abs/2407.13931", source: "arXiv (AFT 2024)", date: "2024-07-18"}
- {id: 22, title: "Beaverbuild joins BuilderNet", url: "https://buildernet.org/blog/beaverbuild", source: "BuilderNet", date: "2025"}
- {id: 23, title: "mevwatch.info censorship dashboard", url: "https://www.mevwatch.info/", source: "mevwatch.info", date: "2026-07-14"}
- {id: 24, title: "Exclusive data from EigenPhi reveals that sandwich attacks on Ethereum have waned", url: "https://cointelegraph.com/research/exclusive-data-from-eigenphi-reveals-that-sandwich-attacks-on-ethereum-have-waned", source: "Cointelegraph Research / EigenPhi", date: "2025-11"}
- {id: 25, title: "Loss-Versus-Rebalancing (LVR)", url: "https://arxiv.org/pdf/2208.06046", source: "Milionis, Park, Robinson, Zhang — arXiv", date: "2022"}
- {id: 26, title: "An AMM minimizing user-level extractable value and loss-versus-rebalancing", url: "https://arxiv.org/pdf/2301.13599", source: "arXiv", date: "2023"}
- {id: 27, title: "DRW Trading Group", url: "https://en.wikipedia.org/wiki/DRW_Trading_Group", source: "Wikipedia", date: "2026"}
- {id: 28, title: "Checkpoint #9", url: "https://blog.ethereum.org/2026/04/10/checkpoint-9", source: "Ethereum Foundation Blog", date: "2026-04-10"}
- {id: 29, title: "Do we still need DPaaS after ePBS?", url: "https://decentralizedthoughts.github.io/2025-12-12-dpaas/", source: "Decentralized Thoughts", date: "2025-12-12"}
- {id: 30, title: "Gattaca — company profile", url: "https://www.crunchbase.com/organization/gattaca", source: "Crunchbase", date: "2026"}
- {id: 31, title: "Building towards Multi-Party Block Construction", url: "https://ethresear.ch/t/building-towards-multi-party-block-construction/24975", source: "ethresear.ch", date: "2026-05-27"}
- {id: 32, title: "MEV cross-chain analysis 2025", url: "https://academy.extropy.io/pages/articles/mev-crosschain-analysis-2025.html", source: "Extropy Academy", date: "2025"}
- {id: 33, title: "EU PFOF ban: MiFIR Article 39a", url: "https://theindustryspread.com/eu-pfof-ban-mifir-article-39a-june-2026-vs-us-uk/", source: "The Industry Spread", date: "2026-06"}
- {id: 34, title: "SEC proposes rescission of Regulation NMS Rules 611 and 610(e)", url: "https://www.sec.gov/newsroom/press-releases/2026-54-sec-proposes-rescission-regulation-nms-rules-611-610e", source: "U.S. SEC", date: "2026-06-11"}
- {id: 35, title: "FINRA Regulatory Notice 21-23", url: "https://www.finra.org/rules-guidance/notices/21-23", source: "FINRA", date: "2021"}
- {id: 36, title: "US SEC clears path for decentralized crypto asset security trading", url: "https://www.sidley.com/en/insights/newsupdates/2026/04/us-sec-clears-path-for-decentralized-crypto-asset-security-trading", source: "Sidley Austin", date: "2026-04"}
- {id: 37, title: "Kubi Mensah — EthCC speaker page", url: "https://ethcc.io/speakers/kubi-mensah", source: "EthCC", date: "2026-04-02"}
- {id: 38, title: "Flash Boys 2.0", url: "https://arxiv.org/abs/1904.05234", source: "Daian et al. — IEEE S&P / arXiv", date: "2019-2020"}
- {id: 39, title: "MEV in batch auctions", url: "http://mengqianzhang.me/papers/batch.pdf", source: "academic working paper", date: "n.d."}
- {id: 40, title: "MEV on Ethereum: A Policy Analysis", url: "https://laweconcenter.org/resources/mev-on-ethereum-a-policy-analysis/", source: "ICLE", date: "2023"}
- {id: 41, title: "MEV and Me", url: "https://research.paradigm.xyz/MEV", source: "Paradigm Research", date: "2021"}
- {id: 42, title: "MEV and the limits of scaling", url: "https://writings.flashbots.net/mev-and-the-limits-of-scaling", source: "Flashbots Writings", date: "2025"}
- {id: 44, title: "Compliance table — Guidelines on market abuse under MiCA", url: "https://www.esma.europa.eu/sites/default/files/2025-10/ESMA75-113276571-1625_Compliance_table_Guidelines_on_market_abuse_MiCA.pdf", source: "ESMA", date: "2025-10"}
- {id: 45, title: "Does MEV fall within scope of MiCA's market abuse provisions?", url: "https://blog.bcas.io/does-mev-fall-within-scope-of-micas-market-abuse-provisions", source: "BCAS", date: "2023-2025"}
- {id: 46, title: "Crypto-asset market abuse under EU MiCA", url: "https://www.cambridge.org/core/journals/european-journal-of-risk-regulation/article/cryptoasset-market-abuse-under-eu-mica/FDC11EC096728B9EF1097A5346F0EF27", source: "European Journal of Risk Regulation", date: "2024-2025"}
:::
