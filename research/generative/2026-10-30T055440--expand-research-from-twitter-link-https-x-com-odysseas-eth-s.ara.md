---
eyebrow: INCIDENT ANALYSIS · EXCHANGE SECURITY · ETHEREUM
title: "The Binance sweep was not an EIP-7702 bug. It was a signing-path failure that 7702 made cheap to cash out."
deck: What the on-chain record, Binance's own statement and the analytics firms establish about the 29 October 2026 hot-wallet drain, and what they do not.
domain: crypto
lede: |
  On 29 October 2026 a signed EIP-7702 delegation turned a Binance-labelled Ethereum wallet into a sweeper, and 3 minutes 24 seconds later it was emptied of 167,464 ETH and 63 tokens including 1.615 billion USDT.[^1,2,5,6] The viral framing says the protocol feature "turned the wallet into the sweeper." The chain says something narrower and more worrying: every authorization was signed by the victim's own key or by a system able to sign for it, so the real question is who controlled that signing path.[^6,9,10] Figures for the total range from $2.8 billion to $6.36 billion depending on chain scope and valuation time, all as of 2026-10-30.[^8,10,28]
stats:
  - {label: First Ethereum sweep, value: "167,464 ETH", note: "+ 63 tokens, 20:24:23 UTC"}
  - {label: USDT in that tx, value: "1.615B", note: "Etherscan, block 26300770"}
  - {label: Delegation to sweep, value: "3m 24s", note: "20:20:59 to 20:24:23 UTC"}
  - {label: TRM gross theft, value: "$6.36B", note: "10 chains, as of 2026-10-30"}
  - {label: Frozen (Binance), value: "~$3B", note: "announcement, 2026-10-30"}
---

:::callout(kind=info, label="Direct answer")
The seed claim is accurate on its numbers and incomplete on its mechanism. The sweep transaction was sent by the attacker, not by the wallet; the wallet only ran the attacker's code because it had been delegated to it.[^5,6] Fifty authorizations recovered to the Binance 14 address, so the signing path was already compromised before EIP-7702 entered the story.[^6,13] Binance says it found no leaked private key and points to a compromised DevOps laptop, which is consistent with a signing-oracle compromise but is unverified until its post-mortem.[^8] Net of freezes the loss is probably in the low billions, which a roughly $129B customer base can absorb on paper.[^8,10,18]
:::

## 01. What the tweet says, and what the chain lets us check

The seed is the first post of a four-part thread by Odysseus (@odysseas_eth), founder of Phylax Systems, posted 2026-10-29 at 20:54 UTC.[^1] It says EIP-7702 "can turn the wallet itself into the sweeper" and that a Binance-labelled wallet moved 167,464 ETH plus 63 tokens, including about 1.615 billion USDT, roughly 3 minutes 24 seconds after a signed delegation was installed.[^1] The thread was drawn to 235,011 views within hours.[^1]

Every number in that opener is checkable, and the numbers hold. The sweep transaction, `0x53bd38b8…e2f3`, is in block 26300770 with timestamp 2026-10-29 20:24:23 UTC and shows an internal transfer of 167,464.2478 ETH plus 63 ERC-20 transfers from Binance 14 to an address Etherscan labels "Binance Hot Wallet Exploiter 2".[^5] The largest legs were roughly 1.615 billion USDT, 62.6 million RLUSD, 29,934 wBETH, 11,372 XAUt, 6.19 million UNI and 198 million ENA.[^5] The delegation transaction, `0xad99264d…`, sits in block 26300753 at 20:20:59 UTC and is a type-4 (EIP-7702) transaction carrying 50 authorizations.[^6] 20:24:23 minus 20:20:59 is exactly 3 minutes 24 seconds.[^2,6]

:::stats
- {label: Sweep block, value: "26300770"}
- {label: Delegation block, value: "26300753"}
- {label: Authorizations in one tx, value: "50"}
- {label: Authorizations that took effect, value: "1"}
- {label: Sweep gas fee, value: "0.00041 ETH", note: "about $0.93"}
:::

The first correction is about who acted. In the tweet's wording "the wallet itself" is the sweeper. On-chain, the sweep was a plain type-2 transaction sent by the attacker's externally owned account, `0x7C86…5CA0`, at sender nonce 11, calling `sweep()` on Binance 14; it carried no authorization list.[^5] The delegation transaction was sent by that same account at nonce 10.[^6] The attacker paid the gas for both, about 0.0065 ETH for the delegation and under a thousandth of an ETH for the sweep, so the victim wallet needed no ETH to be emptied.[^5,6,11]

The second correction is that the tweet's "50 authorizations" figure does not come from the thread; it comes from Blockaid, relayed by an aggregator account.[^37,9] The thread itself is more careful than its headline. Its third post says the delegate hard-coded a Tornado-funded operator and that "how these signatures were obtained remains unknown," allowing either a stolen key or a malicious owner-signed authorization.[^3] Its fourth says the delegated wallet used its owner role on a separate smart wallet to move another 780 million USDC at 20:41:23.[^4]

:::note
The thread author runs a security-tooling company, which gives him an interest in stories about delegated code acting on its own. The thread pitches nothing, and its quantitative claims match the chain, so the interest is noted rather than held against it.[^1,3]
:::

## 02. The mechanics: why 50 signatures and why it worked

EIP-7702, introduced with the Pectra upgrade, lets an externally owned account set its code to a delegation indicator, `0xef0100` followed by an address, by signing an authorization tuple of chain id, address and nonce.[^13] The spec requires the nonce in the tuple to equal the authority's current nonce, otherwise the tuple is skipped silently, and anyone may submit the carrying transaction because the signature, not the sender, carries authority.[^13] Delegating to the zero address resets the account to empty code.[^13]

That design explains the attacker's most distinctive move. Binance 14 was busy, sending 33 transactions in the three minutes before the attack, about one every six seconds.[^11] An attacker who cannot predict the nonce at inclusion time has to cover a range. The carrying transaction held 50 authorizations for nonces 18,914,775 through 18,914,824; the wallet's nonce reached 18,914,808 by inclusion, and only the authorization for 18,914,809 was valid.[^6,11] Forty-nine were dead on arrival, which cost the attacker nothing because signatures are free once a signer will produce them.[^6,11]

:::timeline
- {date: "2026-10-28", headline: "Operator funded", body: "Three small Tornado Cash withdrawals fund the operator address, at least 36 hours before the theft per TRM."}
- {date: "2026-10-29 02:28", headline: "Rehearsals begin", body: "Nine transactions deploy a sweeper and delegate throwaway accounts using 2- and 3-nonce windows."}
- {date: "2026-10-29 15:59", headline: "Final sweeper deployed", body: "The contract hard-codes the operator as its only caller."}
- {date: "2026-10-29 20:20:59", headline: "50 authorizations land", body: "One type-4 transaction; nonce 18,914,809 takes effect."}
- {date: "2026-10-29 20:24:23", headline: "Binance 14 swept", body: "167,464 ETH and 63 tokens in one transaction, 3m 24s later."}
- {date: "2026-10-29 21:01", headline: "First Tether freeze", body: "971.1M USDT frozen at the main receiving wallet."}
- {date: "2026-10-30 00:10:35", headline: "Delegation cleared", body: "An authorization to the zero address removes the code."}
:::

The delegate contract is simple. Etherscan shows verified source, a contract named "Target" compiled with Solidity 0.8.28, exposing `sweep(to, tokens[])`, `callExecute(target, to, value, data)`, `withdrawETH` and `withdrawToken`, and the bytecode hard-codes the attacker's operator address as the only authorized caller.[^7] The `callExecute` function matters: it lets the operator make arbitrary calls as the wallet, which is how the delegated wallet could exercise ownership of a separate smart wallet and move 780 million USDC.[^4,7] Early press and Blockaid called the contract unverified; the Etherscan page now shows it verified, a discrepancy best explained by verification after the fact, though that is inference.[^7,9]

The delegation also outlived the first sweep. Blockaid found it still active at 22:00 UTC, 808bits at 23:50, and a later sweep of Binance 14 at 21:44 took about 200 million USDT.[^9,11,30] Binance cleared it at 00:10:35 UTC on 30 October with an authorization to the zero address, and Blockaid notes that rotating keys alone does not clear a delegation.[^9,11]

:::callout(kind=warn, label="Source caveat")
Our own RPC checks were blocked in this run, so the code-state and nonce facts above rest on Etherscan and Blockscout pages and on 808bits' signer-recovery work rather than a fresh `eth_getCode` call.[^6,11]
:::

## 03. Who signed? The collision between two accounts of the same event

Fifty signatures recovered to the Binance 14 address as authority.[^6] ECDSA recovery cannot be satisfied for a chosen address without the matching key, so someone or something held signing capacity over that key.[^6,13] That is the fact that matters, and it is independent of the delegation feature.

Binance's account, published 2026-10-30 at 02:23, is that its initial probe "may involve a compromised DevOps engineer's laptop," giving access to a service container used to submit unauthorized withdrawals, and that it has "found no evidence of any wallet private key leak."[^8] Blockaid's wording is stronger: a copy of the Binance 14 key signed the authorizations.[^9] Its chief executive later said the pattern looked like a compromise of signing infrastructure rather than a leaked key.[^34]

These are reconcilable. A service container with a cloud-signing role, an HSM or KMS "sign" permission, or a multi-party-computation node that can both initiate and co-sign would let an attacker obtain valid signatures without ever extracting key material. The chain cannot tell the cases apart, because the signature bytes are identical.[^6,13] What the chain does show is breadth: ten more hot wallets across four chains sent funds to the same collection address within 12 minutes using ordinary transactions signed by their own keys, per Blockaid, and TRM's wider tally spans ten chains.[^9,10] TRM reads that as signing infrastructure compromise, because wallets on different chains, with different key types and signature schemes, all produced valid signatures within about half an hour.[^10]

The inference worth stating is that a transaction-only signing policy would normally refuse a 7702 authorization, which is a signed digest of the form `keccak(0x05 ‖ rlp([chain_id, address, nonce]))` and not a transaction.[^13] That the signer produced fifty of them suggests a signer willing to sign raw digests. This is inference from the spec and the evidence, not a statement Binance has made.[^13]

:::rank-list
- {label: "Stolen-key framing (Blockaid, early posts)", value: "key copy signed", pct: 100}
- {label: "Signing-infrastructure compromise (TRM, Blockaid CEO)", value: "no key extracted", pct: 85, highlight: true}
- {label: "Binance preliminary statement", value: "DevOps laptop → container, no key leak", pct: 70}
- {label: "Malicious owner-signed authorization (thread, tweet 3)", value: "not ruled out", pct: 30}
:::

:::note
The bars above order hypotheses by how many named parties assert them as of 2026-10-30; they are not probabilities. Only Binance's post-mortem can settle which holds.[^3,8,9,10,34]
:::

## 04. Reconciling $2.8B, $5.5B, $6.3B and $6.36B

Five headline numbers circulate, and they measure different things. The $2.8 billion figure, reported as moved from the Binance 14 Ethereum hot wallet, covers Ethereum alone.[^28,16] Blockaid's "at least $5.5 billion" rests on public tallies across Ethereum, Arbitrum, Avalanche, Optimism, Bitcoin and Tron.[^9] Binance's own estimate of "around $6.3B" is described as total impact, not a confirmed theft figure.[^8] Arkham's tally, relayed by ChainCatcher, is $6.01 billion across nine chains.[^17] TRM puts gross theft at about $6.36 billion across ten chains at theft-time prices, or $6.23 billion at later prices.[^10]

:::donut(center-label="$6.36B")
- {label: Ethereum, value: 3.79}
- {label: Bitcoin, value: 1.47}
- {label: Tron, value: 0.628}
- {label: XRP Ledger, value: 0.296}
- {label: Solana, value: 0.096}
- {label: "L2s, Avalanche, Polygon", value: 0.077}
:::

:::source
TRM Labs, per-chain gross theft at theft-time prices, USD billions, as of 2026-10-30; the L2 bucket combines Arbitrum, Optimism and Base ($39M), Avalanche ($28M) and Polygon ($10M).[^10]
:::

The per-chain split sums: 3.79 + 1.47 + 0.628 + 0.296 + 0.096 + 0.039 + 0.028 + 0.010 is about $6.36 billion.[^10] On Ethereum, TRM counts 200,630 ETH plus 185 tokens including 1.875 billion USDT, 823 million USDC and 88.5 million RLUSD, a larger set than the single sweep because it adds the second sweep, the 780 million USDC leg and Binance 16.[^5,9,10] The first sweep alone was about $2.5 billion, matching Blockaid and the Etherscan-derived ranges.[^5,9]

Two cautions follow. These are gross outflows, not net losses; the net loss is gross minus assets frozen or recovered, which was still moving as of 2026-10-30.[^8,10] And the largest single input, Bitcoin, is not an EIP-7702 matter at all. 18,270 BTC left on the Bitcoin chain in eleven transactions in one block around 20:20 UTC, which means the EIP-7702 delegation explains only the Binance 14 leg, about $2.5 billion or roughly 40% of the gross total.[^9,10,17]

## 05. Freezes, and what escaped them

Stablecoin issuers did what no one can do for ETH or BTC: they froze. Tether froze about 1.77 billion USDT, Circle about 825 million USDC, Ripple 40.5 million RLUSD, and World Liberty Financial 27.8 million USD1, while the Arbitrum Security Council moved 8,426 ETH and 74.6 million ARB (about $30 million) to a restricted wallet.[^10] TRM totals this at about $2.7 billion as of 00:30 UTC on 30 October.[^10] Tether's first freeze, 971.1 million USDT at the main receiving wallet, came at 21:01 UTC, 37 minutes after the sweep, and Circle's followed at 21:04.[^10] Executives' own numbers were lower early: Tether's chief executive said more than $1.567 billion and Circle's said more than $800 million.[^12]

:::bars
- {label: "Tether (USDT)", value: "$1.77B", pct: 100}
- {label: "Circle (USDC)", value: "$825M", pct: 47}
- {label: "Ripple (RLUSD)", value: "$40.5M", pct: 2}
- {label: "World Liberty (USD1)", value: "$27.8M", pct: 2}
- {label: "Arbitrum Security Council", value: "~$30M", pct: 2}
:::

:::note
Frozen amounts per TRM at 00:30 UTC 2026-10-30; a freeze blocks transfer and is not a recovery, because funds only return if the issuer reissues them.[^10,15]
:::

The "$2.54 billion verified" number that headlines carried is a Binance report at 23:35 UTC, per TRM's timeline, and Binance's own later announcement says about $3 billion.[^8,10] These are snapshots of a growing total, not rival estimates. Independent on-chain work by CryptoTicker found 1.1755 billion USDT and 823 million USDC sitting frozen at the main receiving address, and about 700 million USDT that moved before the freeze.[^15]

What escaped is the larger strategic fact. TRM says the attacker sold about 325 million USDT to market makers at a discount of more than 10%, and deposited 60 million USDT in Aave to borrow about 19,760 ETH.[^10] It reports the attacker holds more than 420,000 ETH and 18,270 BTC, about $2.4 billion, "beyond any issuer's reach," with the BTC moving through a peel chain.[^10] Native assets such as ETH, AVAX, OP and ARB cannot be frozen by an issuer.[^9]

:::compare
- {role: LOWEST, name: "Frozen share of gross theft (issuers, TRM)", value: "~42%"}
- {role: HIGHEST, name: "Frozen share on Binance's own numbers ($3B of $6.3B)", value: "~48%"}
- {role: SUBJECT, name: "Attacker-held, beyond issuer reach (TRM)", value: "~$2.4B"}
:::

The percentage cards are our arithmetic: $2.7B over $6.36B is 42%, and $3B over $6.3B is 48%.[^8,10] The comparison to the February 2025 Bybit theft is instructive but unfetched in detail here: that loss was about $1.5 billion according to the FBI, mostly in ETH, so there was little for an issuer to freeze.[^22] Part of why this incident has a recovery layer at all is that the haul was stablecoin-heavy.[^5,10]

## 06. Attribution and the Bybit template

TRM attributes the theft to North Korea's TraderTraitor group "with high confidence," citing on- and off-chain intelligence it does not publish.[^10] Chainalysis's chief executive called it "likely" the same group in CoinDesk, and ZachXBT said likely Lazarus.[^20] An anonymous source in the same CoinDesk piece cautioned there was no definitive attribution and that DPRK groups usually move funds faster.[^20] Neither Binance nor any government had confirmed attribution as of 2026-10-30.[^8,20]

The structural overlaps TRM cites are small Tornado Cash withdrawals funding the operator, early staging, and signatures obtained beforehand and executed in one burst, the same traits as Bybit and the April 2026 KelpDAO theft.[^10] The FBI attributed the roughly $1.5 billion Bybit theft to North Korea within five days.[^22] Sygnia's forensic report traced Bybit to a compromised Safe developer workstation on 4 February 2025, access inside Safe's AWS between 5 and 17 February, a modified S3 script on 19 February and the theft on 21 February: about 17 days from foothold to theft.[^21] The Binance record shows a different shape. Visible preparation lasted about 36 hours from operator funding to theft, and Binance's own pre-compromise dwell time is unknown.[^10]

Chainalysis counted $2.02 billion stolen by DPRK-linked actors in 2025, about 59% of more than $3.4 billion stolen that year.[^23] If TRM's attribution holds, this single incident would be about three times that annual figure.[^10,23] That sentence is conditional on an attribution that only private-sector firms have made.[^20]

## 07. Solvency and the market reaction

The solvency question is arithmetic. Binance's SAFU fund was converted to 15,000 BTC in February 2026, worth about $1.0 billion then, with a pledge to top up if it fell below $800 million.[^19] At a Bitcoin price near $79,400 on 29 October the fund was worth about $1.19 billion by our arithmetic, against $1.157 billion in another analyst's estimate.[^19,28,18] One analyst estimate sets customer assets near $129.4 billion and reserves near $166 billion, and a net gap after freezes and SAFU of about $2.14 billion, which the same piece calls fillable but uneven across assets.[^18] The $6.3 billion headline is about 4.9% of that customer base, and the net gap after Binance's $3 billion frozen and SAFU is about $2.1 billion by our arithmetic.[^8,18,19]

:::kv
- {term: "Binance statement", def: "Will cover all losses from SAFU and company funds; user funds are safe"}
- {term: "SAFU fund", def: "15,000 BTC, about $1.0B (Feb 2026), about $1.19B at $79.4k BTC"}
- {term: "Customer assets (analyst est.)", def: "About $129.4B"}
- {term: "Withdrawals", def: "Suspended; Binance's Yi He said resumption was expected within 48 hours (per crypto.news, ref 12)"}
- {term: "Next steps promised", def: "Technical post-mortem and an updated proof of reserves"}
:::

"User funds are safe" is a statement about coverage and solvency, not about whether funds left the wallets, and the claim is unaudited until the promised proof of reserves.[^8,12,18] The better health signal is that withdrawals were suspended without a firm date at the time of the announcement.[^8,12]

Market effects are confounded. BNB fell 8.6% to about $694 and Korea's KOSPI closed down 4.9%, but a same-day tech and AI-capex selloff led by weak Amazon and Intel results overlapped.[^26] Contemporaneous reporting shows ETH slipping from $2,335 to $2,255 and BTC from $80.8k to $78.8k by 20:51 UTC, and at 20:55 a separate commentator blamed technology stocks, not the incident.[^27] Liquidations reached $627.7 million within an hour, $606.6 million of them longs and $344.8 million on Binance, the most hack-specific signal.[^28]

:::rank-list
- {label: "Binance, Oct 2026 (gross, TRM)", value: "$6.36B", pct: 100, highlight: true}
- {label: "Bybit, Feb 2025", value: "~$1.5B", pct: 24}
- {label: "Poly Network, 2021", value: "~$610M", pct: 10}
- {label: "Ronin, 2022", value: "~$540M", pct: 8}
- {label: "Coincheck, 2018", value: "~$530M", pct: 8}
- {label: "Mt. Gox", value: "~$500M", pct: 8}
- {label: "Wormhole, 2022", value: "$320M", pct: 5}
:::

:::source
Factbox ranking at nominal values at the time of loss; Binance bar uses TRM's $6.36B and the rest use a published factbox, with Ronin and Mt. Gox figures that vary within that page.[^10,29]
:::

## 08. What EIP-7702 changes, and what defenses follow

The premise that EIP-7702 "caused" this does not survive first principles. A tuple only takes effect if the authority's key signed it, so the key or the signing path was compromised first.[^13,6] Experts made the same point about earlier sweeper waves: Taylor Monahan said "It's not actually a 7702 issue," and a Base engineer said the wallets were not hacked using 7702 but already had leaked keys.[^24,25] SlowMist's Yu Xian said the attacker chose 7702 solely for the convenience of cleanup.[^35]

What 7702 does add is operational. One type-4 transaction with no calldata installed attacker code and the victim paid no gas.[^5,6] The 63-token sweep went out in a single atomic call, and the delegation kept new deposits reachable until it was cleared.[^5,9] Delegations are not rare in the wild: Wintermute reported in June 2025 that more than 90% of delegations it saw were going to malicious sweeper code, a figure The Block reported as more than 80%, so the tooling for abusing the feature was mature well before this incident.[^24,25]

The defenses cluster on the signer, not the protocol. Blockaid and TRM recommend treating authorizations as privileged operations, monitoring hot wallets for code appearing at addresses that should have none, keeping a pre-approved revocation signing method, and treating a request for many authorizations across a nonce range as a compromise indicator.[^9,10] Blockaid's detector fired 1 minute 55 seconds after the sweep, while the delegation sat on-chain for 3 minutes 24 seconds before it, so a detector wired to an automatic freeze could in principle have fired inside that window.[^9] Both vendors sell the products they recommend, which is why the list is best read as a set of testable controls and not as proof of efficacy.[^9,10]

:::callout(kind=warn, label="Inference, not finding")
A signer that refuses type-4 authorizations and raw 0x05-prefixed digests, or that applies per-wallet value caps and destination allowlists, would have bounded this theft. That is our reading of the mechanics and of the Bybit lesson; no source confirms which controls Binance had.[^13,21]
:::

## 09. What could break this thesis

**Counter-argument one: the signing path was not the point.** If Binance's post-mortem shows an ordinary key exfiltration, then the "signing-infrastructure" reading is wrong, though the mechanism conclusion stays: 7702 would still be the cash-out convenience rather than the cause.[^8,10,35]

**Counter-argument two: the numbers may be revised.** Every loss figure here is preliminary. TRM's own freezes and attacker holdings do not sum to its gross theft, since sold or borrowed assets sit in neither bucket, and Arkham's holdings snapshot lists about $5.875 billion across 65 tokens at a point when the ETH figures conflict across sources (195,460; 420,000; 460,568 ETH).[^10,31] The gross-versus-net distinction means "largest hack ever" is true on gross nominal value and unproven on net loss.[^10,29]

**Counter-argument three: attribution is private-sector only.** TRM, Chainalysis and ZachXBT lean toward DPRK, while an anonymous source in CoinDesk noted the laundering tempo was unusual for DPRK groups; TRM itself says this laundering relied on market makers and lending protocols rather than bridges.[^10,20]

**Counter-argument four: the aggregator problem.** Much of the secondary coverage repeats three origins: Binance's announcement, Blockaid's report and TRM's on-chain analysis.[^8,9,10] CryptoTicker, drk.vc and ChainCatcher add independent on-chain checking in places, but several articles carry the same text, so apparent corroboration overstates independence.[^14,17,30]

**Red-team result.** An adversarial pass on the three load-bearing claims found no contradiction to the timing and amount of the first sweep. It found only low-severity pushback on the totals: Binance has not published an independently verified loss figure, some analysts warn the larger estimates may include unrelated transfers, and freeze figures of $2 billion to $3 billion "have not been independently reconciled."

:::statement(attr="ARA Research")
The protocol did not break. A signer produced fifty signatures it should not have, and a feature designed for convenience made the last mile free.
:::

:::references
- {id: 1, title: "Odysseus (@odysseas_eth), thread post 1/4 via fxtwitter", url: "https://api.fxtwitter.com/odysseas_eth/status/2115910280140276155", source: "X / fxtwitter", date: "2026-10-29"}
- {id: 2, title: "Odysseus, thread post 2/4 (timestamps)", url: "https://api.fxtwitter.com/odysseas_eth/status/2115910292886692314", source: "X / fxtwitter", date: "2026-10-29"}
- {id: 3, title: "Odysseus, thread post 3/4 (hard-coded operator, unknown signatures)", url: "https://api.fxtwitter.com/odysseas_eth/status/2115910304697819279", source: "X / fxtwitter", date: "2026-10-29"}
- {id: 4, title: "Odysseus, thread post 4/4 (780M USDC via owner role)", url: "https://api.fxtwitter.com/odysseas_eth/status/2115910316592857593", source: "X / fxtwitter", date: "2026-10-29"}
- {id: 5, title: "Etherscan: sweep transaction 0x53bd38b8…e2f3", url: "https://etherscan.io/tx/0x53bd38b816c23e74134786c29a8c18d792777998a3b9326047b583100e88e2f3", source: Etherscan, date: "2026-10-29"}
- {id: 6, title: "Etherscan: delegation transaction 0xad99264d…", url: "https://etherscan.io/tx/0xad99264d5532ae0dd04b2004eebda05f25657e70dacb764f7ac8d4ccd051298b", source: Etherscan, date: "2026-10-29"}
- {id: 7, title: "Etherscan: delegate contract 0x63e842B0…6fAe", url: "https://etherscan.io/address/0x63e842B054Bd624a465454D533C33F573e9c6fAe", source: Etherscan, date: "2026-10-30"}
- {id: 8, title: "Binance: Security Incident Update", url: "https://www.binance.com/en/support/announcement/detail/c5a8729a97ac486d963784d96c5642d7", source: Binance, date: "2026-10-30"}
- {id: 9, title: "Blockaid: Binance $5.5B hack report", url: "https://blockaid.io/blog/binance-55b-hack-using-advanced-ai-models-blockaid-detects-the-biggest-theft-in-crypto-history", source: Blockaid, date: "2026-10-29"}
- {id: 10, title: "TRM Labs: North Korea steals $6.36 billion from Binance", url: "https://www.trmlabs.com/resources/blog/north-korea-steals-usd-6-36-billion-from-binance-in-the-largest-hack-in-history", source: "TRM Labs", date: "2026-10-30"}
- {id: 11, title: "808bits: Binance hot wallet signed 50 EIP-7702 delegations 3 minutes before the drain", url: "https://808bits.com/articles/binance-hot-wallet-eip-7702-delegations/", source: 808bits, date: "2026-10-30"}
- {id: 12, title: "crypto.news: How one wallet trick led to a $6.3 billion breach", url: "https://crypto.news/binance-hack-eip-7702-wallet-attack", source: "crypto.news", date: "2026-10-30"}
- {id: 13, title: "EIP-7702: Set Code for EOAs", url: "https://eips.ethereum.org/EIPS/eip-7702", source: "Ethereum EIPs", date: "2025-05-07"}
- {id: 14, title: "CryptoTicker: Binance hack on-chain analysis", url: "https://cryptoticker.io/en/binance-hack-on-chain-analysis/", source: CryptoTicker, date: "2026-10-30"}
- {id: 15, title: "CryptoTicker: How much of the Tether freeze is real", url: "https://cryptoticker.io/en/tether-freeze-usdt-binance-hack-how-much-frozen/", source: CryptoTicker, date: "2026-10-29"}
- {id: 16, title: "Finance Magnates: Binance hacked, estimated $6.3 billion drained", url: "https://www.financemagnates.com/cryptocurrency/binance-hacked-estimated-63-billion-in-crypto-drained/", source: "Finance Magnates", date: "2026-10-30"}
- {id: 17, title: "ChainCatcher: Arkham per-chain tally of the Binance drain", url: "https://www.chaincatcher.com/en/article/2300305", source: ChainCatcher, date: "2026-10-30"}
- {id: 18, title: "ChainCatcher: Binance solvency estimate after the drain", url: "https://www.chaincatcher.com/en/article/2300297", source: ChainCatcher, date: "2026-10-30"}
- {id: 19, title: "CoinDesk: Binance converts its $1 billion SAFU fund into 15,000 BTC", url: "https://www.coindesk.com/business/2026/02/12/binance-converts-its-usd1-billion-safu-fund-into-15-000-btc", source: CoinDesk, date: "2026-02-12"}
- {id: 20, title: "CoinDesk: North Korea's Lazarus Group likely behind Binance hack, sleuths say", url: "https://www.coindesk.com/policy/2026/10/29/crypto-s-longtime-foe-north-korea-s-lazarus-group-likely-behind-binance-hack-blockchain-sleuths", source: CoinDesk, date: "2026-10-29"}
- {id: 21, title: "Sygnia: Investigation of the Bybit hack", url: "https://www.sygnia.co/blog/sygnia-investigation-bybit-hack/", source: Sygnia, date: "2025-02-26"}
- {id: 22, title: "FBI IC3 PSA 250226: North Korea responsible for Bybit theft", url: "https://www.ic3.gov/psa/2025/psa250226", source: "FBI IC3", date: "2025-02-26"}
- {id: 23, title: "Fortune: North Korea stole a record amount of crypto in 2025", url: "https://fortune.com/2025/12/18/north-korea-stole-a-record-amount-of-crypto/", source: Fortune, date: "2025-12-18"}
- {id: 24, title: "Unchained: Ethereum EIP-7702 brings new risks, Wintermute says", url: "https://unchainedcrypto.com/ethereum-eip-7702-brings-new-risks-wintermute-says/", source: Unchained, date: "2025-06-02"}
- {id: 25, title: "The Block: Wintermute warns Pectra upgrade leaves Ethereum users at risk", url: "https://www.theblock.co/post/356481/wintermute-warns-pectra-upgrade-leaves-ethereum-users-at-risk-of-automated-attacks", source: "The Block", date: "2025-06-01"}
- {id: 26, title: "investingLive: Binance hack shakes crypto", url: "https://investinglive.com/news/investinglive-asia-pacific-market-news-binance-hack-shakes-crypto/", source: investingLive, date: "2026-10-30"}
- {id: 27, title: "FinanceFeeds: Ethereum price after the Binance hack", url: "https://financefeeds.com/ethereum-price-after-binance-hack/", source: FinanceFeeds, date: "2026-10-29"}
- {id: 28, title: "BigGo Finance: liquidations after the Binance incident", url: "https://finance.biggo.com/news/4040e4bf-0936-4930-8231-7617ba9b7e90", source: BigGo, date: "2026-10-29"}
- {id: 29, title: "Factbox: where Binance's $6.3 billion breach ranks among crypto hacks", url: "https://www.globalbankingandfinance.com/factbox-where-binances-6-3-billion-breach-ranks-cryptos/", source: "Global Banking & Finance", date: "2026-10-30"}
- {id: 30, title: "drk.vc: Binance 14 EIP-7702 drain", url: "https://drk.vc/news/binance-14-eip-7702-drain", source: drk.vc, date: "2026-10-30"}
- {id: 31, title: "KuCoin News (Arkham via BlockBeats): hacker cluster holds $5.875B", url: "https://www.kucoin.com/news/flash/binance-hacker-cluster-holds-5-875b-across-65-tokens-2-54b-in-related-funds-frozen", source: "KuCoin News", date: "2026-10-29"}
- {id: 34, title: "Coin-Turk: Blockaid CEO suggests signing infrastructure flaw", url: "https://en.coin-turk.com/blockaid-ceo-suggests-signing-infrastructure-flaw-in-binance-2-5-billion-hack/", source: "Coin-Turk", date: "2026-10-29"}
- {id: 35, title: "ChainCatcher: SlowMist's Yu Xian on the Binance attacker's use of 7702", url: "https://www.chaincatcher.com/en/article/2300182", source: ChainCatcher, date: "2026-10-30"}
- {id: 37, title: "International Cyber Digest (@IntCyberDigest) on the 50 authorizations", url: "https://api.fxtwitter.com/IntCyberDigest/status/2115947714353480160", source: "X / fxtwitter", date: "2026-10-29"}
:::
