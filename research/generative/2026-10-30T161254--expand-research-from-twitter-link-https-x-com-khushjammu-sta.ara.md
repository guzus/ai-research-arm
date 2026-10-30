---
eyebrow: ANALYSIS · AGENTIC PAYMENTS · STABLECOIN RAILS
title: "Link balance runs on Tempo, but the chain is the thinnest layer of the purchase. The money-handling terms sit around it."
domain: infra
deck: What Stripe's agent wallet actually puts onchain, what Tempo's own specs promise for that leg, and which questions public documents leave open.
lede: |
  On October 29, 2026 the builder @khushjammu wrote that he had enjoyed Link balance and, because it runs on Tempo, had traced its funds flow onchain; his write-up is titled "Inspecting my Link Balance onchain." [^1] The linked X article was not retrievable from this research environment (HTTP 402), so this piece does not report his findings. It does the complementary job: it reads the first-party documents for Link, Tempo, Issuing and USDC, derives what an onchain trace should and should not be able to show, and marks where the public record is silent or inconsistent.
stats:
  - {label: Link balance launch, value: "Oct 26, 2026", note: "Instinct as launch partner, eligible US users"}
  - {label: Tempo mainnet, value: "Mar 18, 2026", note: "per CoinDesk"}
  - {label: Non-payment gas cap per block, value: "6%", note: "30M of 500M, per Tempo fee spec"}
  - {label: Cost of a ~50k-gas transfer, value: "$0.00003–$0.0006", note: "floor to cap"}
---

:::callout(kind=info, label="Direct answer")
- **What runs where:** Link's FAQ says funds are held in USDC, [^4] Tempo's page says the balance is settled in stablecoins on Tempo, [^2] and a secondary summary puts the two together as USDC on Tempo. [^3] No single first-party page states both. A merchant is paid through a one-time card, not a chain transaction. [^5,6]
- **What the chain buys:** Tempo's stated reasons are 24/7 settlement, sub-cent fees paid in stablecoins and reserved payment blockspace. [^2] Each is specified in Tempo's docs. [^8,9]
- **What public documents do not say:** whether each purchase moves tokens on Tempo, and whether a given user's balance is custodial (Bridge) or self-custodial (Privy). Launch materials do not say which Instinct users receive. [^3]
- **The real risk sits off-chain:** the user is "responsible for all purchases your agent makes." [^5]
- **Scope limit:** the seed author's onchain findings were unreadable here, so every inference below comes from documents, not from transactions.
:::

## 01. What the seed claim is, and what it is not

**Thesis: the tweet is evidence of one builder's tracing exercise, not of any particular finding.** The only content recoverable is the tweet's text and the article preview: Link balance has drawn hype on FinTech Twitter, the author finds the hype deserved because the UX is smooth, and he traced the funds flow because the product runs on Tempo. [^1] No transaction hashes, addresses or conclusions are visible in that preview, and the full article returned HTTP 402 to the fetcher used here.

That limit shapes the method. A first-principles reading asks what an observer could see if they followed a Link balance deposit through a public chain, using only what the operators have documented. Tempo's mainnet is chain ID 4217 with a public explorer, so the leg is in principle inspectable. [^11] What is inspectable is a token ledger. It is not the card authorization, the Lead Bank prepaid account or the Visa clearing that follow. [^3,17]

The prior ARA article on this launch read the contract terms and US payment rules. This one asks the infrastructure question instead. Why would an agent wallet for ordinary consumers sit on a purpose-built chain, and what exactly does the chain do?

:::note
The seed tweet is dated October 29, 2026 (20:23 UTC) and links to the article; the Link launch came on October 26–27. [^1,2] Treat the seed author's comments as claims about what he observed, not as verified facts.
:::

## 02. The product as the operators describe it

**Thesis: Link balance is a prepaid, USDC-denominated float that lets an agent spend under a per-purchase cap without a fresh approval each time.** Tempo's customer story says users deposit funds and choose a cap per purchase; the agent spends within the cap and never sees card details. [^2] Link's launch date is October 26, 2026, and it targets eligible US regions with New York "coming soon." [^2]

The funding path, as summarized by one secondary source, runs: debit-card top-up, conversion by Stripe's onramp into a dollar stablecoin on Tempo, a Privy-powered wallet behind the Link account, an agent-wallet limit, then a Stripe-issued virtual card for the purchase. [^3] That architecture is assembled from several reports and is not published as a single diagram by Stripe in the sources reviewed here, so treat the exact sequencing as plausible, not confirmed. The Link FAQ confirms funds are held in USDC, [^4] and the secondary summary adds that receipts show USDC even for card-funded balances. [^3]

:::kv
- {term: Holding asset, def: "USDC, per Link's balance FAQ"}
- {term: Settlement layer, def: "Tempo, per Tempo's Link customer story"}
- {term: Per-top-up ceiling, def: "US$150 per setup link (secondary summary of Link support)"}
- {term: Spend request ceiling, def: "50,000 cents (US$500)"}
- {term: Eligible users, def: "18+, US SSN verification check"}
- {term: Unsupported cards, def: "Amex, Discover, Capital One (secondary summary)"}
:::

The Instinct integration is the launch consumer. A Brazilian report says Instinct takes requests by text message or call, and that the balance feature began rolling out in the US on Monday, October 26. [^20] Spend through such an agent recurs, which is why a per-purchase cap matters: approval prompts are the main friction. Tempo frames the problem the same way, with concert presale tickets and price-drop shoes as the time-sensitive buys that stall behind a human approval. [^2]

Why it matters: the chain is the settlement and custody layer for the float, not the thing the merchant interacts with, which determines what a trace can show.

## 03. Four layers, and which one is onchain

**Thesis: only one of four layers is a public ledger.** The other three are an identity and approval layer, a card-issuing layer and a card-network layer.

:::stack-rows
categories: [Public chain, Link app and policy, Issuing and bank, Card network]
rows:
  - {label: Funding the float, values: [60, 20, 10, 10]}
  - {label: Agent decides to buy, values: [0, 60, 20, 20]}
  - {label: Merchant gets paid, values: [0, 5, 35, 60]}
:::

:::note
The bars above are ARA's qualitative weighting of where each step is visible, not measured data.
:::

The agent-facing credential is explicit in Link's own tooling. The open-source Link CLI hands agents one of three credential types: a virtual card, a Link Pay Token for supported Stripe surfaces, or a Shared Payment Token for merchants using the Machine Payments Protocol. [^6] Its README sets the security posture: the user approves each request through a push notification with a 30-minute window, and the tool is currently limited to US and Canadian Link accounts. [^6]

On the card layer, a secondary analyst reading described the flow as a card in all but name: Stripe sells the needed USDC, funds a prepaid card account at Lead Bank, and payment runs over Visa to the merchant's processor, so merchants need no wallet or stablecoin support. [^3] Stripe's Issuing documentation confirms the generic capability: virtual cards, spending controls and real-time authorizations delivered by webhook. [^17] The Lead Bank detail is a single-source claim and is not named in Stripe's public Issuing page. [^3,17]

Implication: if the merchant sees a Visa card, the chain's contribution is upstream. A tracer would see tokens arrive and leave, but a "purchase" is a card event that a block explorer cannot show.

## 04. What Tempo specifies for the payment leg

**Thesis: Tempo's fee and blockspace design is engineered for exactly this kind of small, frequent stablecoin transfer.** Four documented mechanics matter.

### Fees in dollars, with no gas token

Tempo has no native gas token. The explorer page notes the currency symbol is USD and that account funds are held as TIP-20 balances. [^11] The fee spec quotes fees in attodollars per gas, caps the base fee at 12 billion attodollars per gas and floors it at 600 million. [^9] On those parameters a roughly 50,000-gas TIP-20 transfer costs about 600 microdollars ($0.0006) at the cap and about 30 microdollars ($0.00003) at the floor. [^9]

:::compare
- {role: LOWEST,  name: "Transfer at fee floor",  value: "$0.00003"}
- {role: HIGHEST, name: "Transfer at fee cap",    value: "$0.0006"}
- {role: SUBJECT, name: "US$16 lunch (Tempo's own example)", value: "$16.00"}
:::

Against a US$16 lunch, the cap-level fee is about 0.004% of the purchase (ARA arithmetic: 0.0006 ÷ 16). The point is not that fees are small in absolute terms; it is that the fee is irrelevant to the unit economics of a consumer purchase, so the chain's cost advantage must come from somewhere else, such as settlement timing and operational simplicity.

### Fee token choice and the Fee AMM

Fee payment follows a precedence: transaction field, account preference, TIP-20 transfer token, DEX swap input token, then a pathUSD fallback. [^9] If the user's token differs from the validator's preferred token, the Fee AMM converts at a fixed 0.9970 rate per hop, a 0.3% spread that stays in the pool. [^9] A user holding only USDC therefore need not hold anything else, which is what Tempo means by sub-cent fees paid in stablecoins. [^2,9]

### Reserved payment blockspace

The fee spec states a 500M total block gas limit with 30M for general use, so non-payment gas is capped at about 6% of a block and the other ~94% is available to payments. [^9] That is a ceiling on general computation, not a guaranteed allotment or fixed fee for payments, and the ~94% figure is ARA arithmetic on the spec's two numbers. [^9] The payment-lane spec explains the mechanism: a transaction qualifies only if every call matches an allow-listed payment call shape and its access list and authorization lists are empty. [^8] The separation is an accounting constraint, not a positional one, and payment transactions can use remaining block capacity. [^8]

:::donut(center-label="Block gas")
- {label: "Not capped by the general limit", value: 94}
- {label: "General (non-payment) gas", value: 6}
:::

### Memos and issuer controls

TIP-20 adds fixed 32-byte memo fields (`transferWithMemo`) and a shared policy layer, so a payment can carry a reference an app can reconcile. [^10] The same spec gives token issuers pause, `burnBlocked` and `burnAt` roles and transfer-policy hooks, with `decimals()` fixed at 6. [^10]

:::callout(kind=warn, label="Caveat")
The payment-lane page states no separate base-fee rule for payment lanes, so the "reserved blockspace" claim rests on the gas-budget accounting, not on a documented price guarantee. [^8] Whether the USDC held in Link balances is a native TIP-20 or a bridged representation was not established from the sources reviewed.
:::

Why it matters: these four mechanics are the chain's real contribution, and each can be checked in documents without trusting marketing copy.

## 05. Tempo's three promises, tested one by one

**Thesis: two of Tempo's three stated reasons survive first-principles scrutiny; the third is weaker than it sounds for a card-settled product.**

Tempo's customer story gives the reasons: near-instant 24/7 settlement, sub-cent fees paid in stablecoins, and blockspace reserved for payments. [^2]

| Claim | What the spec supports | What is unproven for Link |
|---|---|---|
| *24/7 settlement | Consensus is Simplex BFT via Commonware with "deterministic sub-second finality" [^7] | The merchant leg settles over card networks, not the chain [^3] |
| Sub-cent fees | $0.00003–$0.0006 per ~50k-gas transfer [^9] | Whether each purchase triggers a transfer |
| Reserved blockspace | General gas capped at 30M of 500M [^9], allow-list classification [^8] | No separate fee rule documented [^8] |

The first-principles test is simple. A claimed advantage only matters if the product's critical path crosses it. For a purchase, the critical path crosses a Visa authorization, and the card is authorized through Issuing's real-time webhook flow. [^17] The Link FAQ says pending merchant charges can sit up to seven days before an authorization expires. [^5] None of that timing is improved by sub-second finality.

Where finality plausibly helps is funding. A debit-card top-up at midnight can become spendable USDC without a bank cutoff, which matches Tempo's argument that stablecoins move around the clock. [^2,3] That is a real advantage over bank-hours funding, but it concerns the float, and it would be equally served by an internal ledger Stripe controls. The chain's distinct value is that the float is a portable asset: a self-custodial Privy wallet can export its private key, and crypto withdrawals typically land in minutes at no fee. [^3,4]

:::timeline
- {date: 2025-06, headline: "Stripe agrees to buy Privy", body: "Wallet infrastructure; terms undisclosed, per Blockworks."}
- {date: 2025-10, headline: "Tempo raises $500M", body: "Series A at roughly $5B, led by Thrive and Greenoaks."}
- {date: 2026-03, headline: "Tempo mainnet + MPP", body: "Mainnet live March 18 with the Machine Payments Protocol."}
- {date: 2026-04, headline: "Visa, Stripe, Zodia join as validators", body: "Moving past an initial small circle of operators."}
- {date: 2026-10, headline: "Link balance launches", body: "October 26, with Instinct as launch partner."}
:::

Counterpoint: a stablecoin leg may matter more strategically than operationally. If agents later pay merchants directly through MPP, the same wallet becomes a payment credential on a native rail; the Link CLI already lists MPP and Shared Payment Tokens as credential types. [^6,14] The present card-based flow may be a bridge to that world.

## 06. Custody: the question the launch materials leave open

**Thesis: "on-chain" does not settle who holds the keys, and that is the user's biggest practical unknown.** Link's FAQ language and secondary summaries describe two models. In the custodial model, Bridge, a Stripe company, holds the USDC and manages the private keys while assets remain the user's. In the self-custodial model, Link and Privy provide an onchain wallet whose private key can be exported at any time, and losing login and recovery methods may mean permanent loss. [^3] The same summary states that launch materials do not say which version Instinct users receive. [^3]

Stripe's acquisitions explain why both models exist in one stack. Stripe agreed to buy Privy in June 2025, a wallet infrastructure provider, and it already owned the stablecoin company Bridge. [^19,12] Bridge handles money movement; Privy gives users wallets that feel like a normal login. [^19]

:::compare
- {role: LOWEST,  name: "Custodial (Bridge)",       value: "Keys held by Stripe unit"}
- {role: HIGHEST, name: "Self-custodial (Privy)",   value: "Key exportable by user"}
- {role: SUBJECT, name: "Instinct launch",          value: "Not stated"}
:::

The distinction changes the failure modes. A custodial balance leaves the user with a claim on a regulated intermediary. A self-custodial balance leaves the user with a key and a recovery method. Crypto transfers are irreversible by nature, though failed transfers that never reached the chain return to the balance. [^4] Either way, an onchain trace of the wallet address reveals movements, not who legally controls the funds.

Why it matters: a builder tracing the funds flow can show the wallet's transfers, but a reader should not infer custody or legal ownership from the chain alone.

## 07. Who runs the chain

**Thesis: the settlement layer is controlled by a small, institutional validator set, which suits payments and concentrates trust.** Tempo's mainnet went live on March 18, 2026, built by Stripe and Paradigm after roughly three and a half months of testing. [^12,14] On April 14, 2026, The Block reported that Visa, Stripe and Zodia Custody by Standard Chartered signed on as early validators, moving beyond an "initial small circle of operators." [^13] The report does not give the earlier validator count or say whether the network is permissioned. [^13]

Tempo raised $500 million at about a $5 billion valuation in October 2025 in a round led by Thrive Capital and Greenoaks, and neither Stripe nor Paradigm invested in that round. [^18] A chain whose validators include the issuer of the card (Visa) and the company that built the wallet and onramp (Stripe) is coherent for payments: the parties already trust each other commercially. It is a different trust model from a permissionless chain, and the report says Tempo is starting to widen its validator set. [^13]

:::kv
- {term: "Mainnet chain ID", def: "4217"}
- {term: "Testnet (Moderato) chain ID", def: "42431"}
- {term: "TIP-20 decimals", def: "6"}
- {term: "Consensus", def: "Simplex BFT via Commonware"}
:::

The consensus design is public: Simplex BFT via Commonware, advertised as sub-second deterministic finality with Byzantine fault tolerance. [^7] Users inherit those properties only as far as the operators behave; the practical protection is contractual and regulatory, not cryptographic.

Counterpoint: a small institutional validator set also reduces some risks that matter to consumers, such as chain reorganizations around a merchant payout. The tradeoff is censorship resistance and exit options, which the self-custodial key export partly restores. [^3]

## 08. Rules and rights around the float

**Thesis: the USDC itself and the card sitting on top of it are governed by different regimes, and the consumer-facing promises come from Link's terms, not from the chain.** The US GENIUS Act framework is moving: the OCC issued its final implementing rule on October 21, 2026, and both the rule and the Act take effect January 18, 2027. [^16] The release says the rule sets standards for reserve backing, redemption and risk management, and a separate Treasury-coordinated rulemaking will cover Bank Secrecy Act, AML and sanctions requirements. [^16]

Circle, the USDC issuer, shows reserve categories on its transparency page as of October 26, 2026: bank deposits, overnight reverse repo and Treasuries maturing in under three months, with most held in the Circle Reserve Fund managed by BlackRock. [^15] The page names Deloitte & Touche as financial auditor and shows a September 2026 monthly examination report as the latest linked. [^15] Numeric circulation and reserve totals were not retrievable, so no current supply figure is asserted here.

The consumer promises are narrower. Link says withdrawals to a bank take 3–5 business days and crypto withdrawals usually minutes, with no fee for crypto withdrawals. [^4] On the agent side, Link says the user is responsible for all purchases the agent makes even if it buys a different product than the one shown, with disputes routed by cause to Link, the merchant or the agent platform. [^5] Approval for each purchase requires biometric sign-off in the standard flow, though the FAQ gives both a 30-minute and a 10-minute expiry. [^5]

:::bars
- {label: "Per setup link (secondary)", value: "$150", pct: 30}
- {label: "Per spend request (docs)", value: "$500", pct: 100}
- {label: "Developer daily limit (CLI README)", value: "$500", pct: 100}
:::

The balance flow changes the logic: with a per-purchase cap, orders under the cap skip approval, and a $0 limit restores approval on every purchase. [^3] A single spend request cannot exceed 50,000 cents in USD, and the request moves through ten statuses from `created` to `succeeded` or `failed`. [^21] The cap is per purchase, not weekly or monthly, so the funded balance is the only cumulative ceiling. [^3] The Link FAQ also says overall spend "varies by behavior and agent," resets daily and cannot be raised. [^3,5] A user cannot compute their worst-case daily exposure from the documents alone.

Why it matters: the chain provides a clean audit trail for the float, but the consumer's protections against an agent error live in Link's terms.

## 09. What an onchain trace can and cannot prove

**Thesis: a trace can falsify architecture claims but cannot adjudicate liability or fairness.** From the specs above, an observer with a Link balance address could in principle verify:

- that value is held in TIP-20 token balances rather than a native coin, since Tempo has none; [^11]
- the fee token used and the cost of each transaction, bounded by the documented base-fee floor and cap; [^9]
- the presence of 32-byte memo fields on `transferWithMemo` calls, if Link or Bridge uses them; [^10]
- whether top-ups arrive as one deposit per card charge or are batched, which would show how the onramp aggregates;
- whether purchases move tokens individually or in batched treasury sweeps.

A trace cannot show: the card authorization, interchange, the merchant's identity, the dispute outcome, or the legal custody model. Stripe's Issuing docs describe those in a separate system of records. [^17] This is exactly where public analysis tends to overreach. Funds flowing between two addresses is evidence about token movement; it is not evidence about what the user is owed.

A narrower and more interesting forensic question is whether the float is pooled. If many users' balances sit in a commingled omnibus address while the app tracks per-user entitlements, the onchain picture would show few large addresses and the per-user ledger would be offchain. Public documents do not say, and that would be the finding most worth confirming in the seed author's write-up.

## 10. What could break this thesis

**Thesis: the main risk to this reading is that I am reasoning from documents about a system that the documents describe incompletely.** Four specific ways it could be wrong.

1. **Purchases may be fully onchain.** If Link settles each agent purchase by an onchain transfer into an Issuing funding account, the chain would be on the critical path and the fee and finality arguments would carry more weight than assumed above. The reviewed sources only show the funding architecture second-hand. [^3]
2. **The Lead Bank detail is single-sourced.** The prepaid-account description comes from one analyst's reading as summarized by a secondary site; Stripe's own Issuing page does not name a sponsor bank. [^3,17]
3. **Inconsistent limits.** Link's own FAQ gives two approval windows, 30 and 10 minutes, and the developer docs say 30. [^5,3] Limits quoted from the CLI README apply to the standard approval flow and may differ for balance-funded spending. [^6]
4. **The seed author may have seen something different.** His article preview indicates he found enough in the flow to write up, and this piece cannot confirm or contradict it. [^1]

There are also disagreements in the secondary record. A secondary summary reports that Instinct raised US$1 billion at a US$10 billion valuation in September; that was not verified against a primary filing, and it does not affect the technical analysis. [^3] One outlet (The Block) describes the April validator additions as mainnet, while a blog describes them as testnet; the draft follows The Block. [^13]

:::statement(attr="ARA Research")
The chain makes the float portable and always-on; it does not make the purchase safer or the user's recourse stronger.
:::

## 11. What to watch

- Whether Link publishes which custody model Instinct users get, since launch materials do not say. [^3]
- The New York rollout, which Tempo lists as coming soon. [^2]
- The first non-Instinct agent to enable balances through the Link CLI. [^3,6]
- The January 18, 2027 effective date of the GENIUS Act and OCC rule. [^16]
- Tempo's validator expansion beyond Visa, Stripe and Zodia Custody. [^13]
- Whether MPP, co-developed by Stripe and Tempo and currently running only on Tempo, begins to carry agent purchases directly instead of through a card. [^14]

:::references
- {id: 1, title: "khush (@khushjammu) tweet: Inspecting my Link Balance onchain", url: "https://x.com/khushjammu/status/2115902443225813486", source: "X", date: "2026-10-29"}
- {id: 2, title: "Link balance on Tempo (customer story)", url: "https://tempo.xyz/customer-stories/link/", source: "Tempo", date: "2026-10-27"}
- {id: 3, title: "Link Balance: How Stripe Lets AI Agents Spend USDC", url: "https://stablecoininsider.org/link-balance/", source: "Stablecoin Insider", date: "2026-10"}
- {id: 4, title: "Link balance FAQ", url: "https://support.link.com/questions/link-balance-faq", source: "Link Support", date: "2026-10"}
- {id: 5, title: "Link Agent Wallet FAQ", url: "https://support.link.com/questions/link-agent-wallet-faq", source: "Link Support", date: "2026-10"}
- {id: 6, title: "stripe/link-cli README", url: "https://github.com/stripe/link-cli", source: "GitHub", date: "2026-10"}
- {id: 7, title: "Tempo developer documentation index", url: "https://tempo.xyz/developers", source: "Tempo", date: "2026-10"}
- {id: 8, title: "Tempo payment lane specification", url: "https://tempo.xyz/developers/docs/protocol/blockspace/payment-lane-specification.md", source: "Tempo", date: "2026-10"}
- {id: 9, title: "Tempo fee specification", url: "https://tempo.xyz/developers/docs/protocol/fees/spec-fee.md", source: "Tempo", date: "2026-10"}
- {id: 10, title: "TIP-20 specification", url: "https://tempo.xyz/developers/docs/protocol/tip20/spec.md", source: "Tempo", date: "2026-10"}
- {id: 11, title: "Tempo network details", url: "https://tempo.xyz/developers/docs/quickstart/connection-details.md", source: "Tempo", date: "2026-10"}
- {id: 12, title: "Stripe-led payments blockchain Tempo goes live with protocol for AI agents", url: "https://www.coindesk.com/tech/2026/03/18/stripe-led-payments-blockchain-tempo-goes-live-with-protocol-for-ai-agents", source: CoinDesk, date: "2026-03-18"}
- {id: 13, title: "Visa, Stripe and Zodia Custody become validators on Tempo", url: "https://www.theblock.co/news/business/2026-04-14-visa-stripe-zodia-custody-standard-chartered-validators-tempo-397286", source: "The Block", date: "2026-04-14"}
- {id: 14, title: "Stripe, Tempo and Paradigm MPP AI payments protocol", url: "https://fortune.com/2026/03/18/stripe-tempo-paradigm-mpp-ai-payments-protocol/", source: Fortune, date: "2026-03-18"}
- {id: 15, title: "Circle transparency", url: "https://www.circle.com/transparency", source: Circle, date: "2026-10-26"}
- {id: 16, title: "OCC final rule implementing the GENIUS Act (NR 2026-92)", url: "https://occ.gov/news-issuances/news-releases/2026/nr-occ-2026-92.html", source: OCC, date: "2026-10-21"}
- {id: 17, title: "Stripe Issuing documentation", url: "https://docs.stripe.com/issuing", source: Stripe, date: "2026-10"}
- {id: 18, title: "Stripe-backed Tempo raises $500M Series A at $5B valuation", url: "https://www.theblock.co/post/375152/stripe-tempo-500-million-series-a-thrive", source: "The Block", date: "2025-10-17"}
- {id: 19, title: "Stripe acquires crypto wallet provider Privy", url: "https://blockworks.co/news/stripe-acquires-privy-wallet", source: Blockworks, date: "2025-06-11"}
- {id: 20, title: "Instinct lança saldo no Link com teto por compra", url: "https://www.letsmoney.com.br/ia/instinct-link-balance-agente-ia-teto-por-compra/", source: LetsMoney, date: "2026-10-27"}
- {id: 21, title: "Link spend requests (developer docs)", url: "https://docs.link.com/concepts/spend-requests", source: "Link docs", date: "2026-10"}
:::
