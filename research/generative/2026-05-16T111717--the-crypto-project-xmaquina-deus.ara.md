---
eyebrow: Project profile · Crypto × Physical AI · 2026-05-16
title: 'XMAQUINA: tokenized exposure to humanoid robotics, 11 days before TGE'
deck: A Base-deployed DAO selling fractionalized stakes in private robotics companies, governed by veToken
  holders, with the launch price still ahead of it.
lede: XMAQUINA is a DAO that buys equity in humanoid-robotics startups and routes governance over those
  positions through **$DEUS**, an ERC-20 deployed on Base. The token went live on chain May 12, 2026;
  its Token Generation Event is scheduled for **May 27, 2026** — eleven days from today. Pre-TGE, the
  contract has 1,044 holders, ~$110 of DEX liquidity, and one disclosed portfolio position (Apptronik).
  The pitch is real, the legal architecture is a question mark, and most of what gets sold on May 27 is
  still aspirational — the only deployed equity allocation today is a single stake voted in via Snapshot.
stats:
- label: Max supply
  value: '1'
  unit: B
  note: '874.1M minted on Base today'
- label: Capital raised
  value: $10
  unit: M+
  note: ~2,000 contributors across waves
- label: On-chain holders
  value: '1,044'
  note: Base mainnet · 2026-05-16
- label: TGE
  value: May 27
  note: '110M DEUS pre-sale unlocks'
---

## 01. What you're actually buying

The official framing on [xmaquina.io](https://www.xmaquina.io/) is that DEUS holders gain exposure to a "treasury of the world's leading robotics companies, governed by DEUS holders." Concretely, the DAO uses contributor capital to take pre-IPO equity positions in private robotics companies, then routes governance over those positions through a vote-escrow token (xDEUS) minted by staking DEUS. The intent is that exits and revenue eventually flow back to the DAO, where votes decide between equity acquisitions, DEUS buybacks, and staking rewards.

The DAO publicly groups its target market into four verticals:

| Vertical | What gets bought | Named prospects |
|---|---|---|
| Humanoid companies | Pre-IPO equity in robot makers | Apptronik, 1X, Agility, Figure AI |
| Physical AI stack | Actuators, sensors, chips, infra | Not disclosed |
| Robotics protocols | Early Web3 robotics projects | Not disclosed |
| Humanoid AI | Intelligence layers / VLA models | Neura Robotics |

Of those names, only **Apptronik** has actually been approved by a DAO vote — "BOT-1," passed with **98.05%** support on `snapshot.xmaquina.io`. Every other company on the homepage is currently a target, not a holding. The project claims its Apptronik position has appreciated over 100% since acquisition; this number is not independently verifiable from primary sources and should be treated as a project claim, not a market-marked figure.

:::callout(kind=warn, label="What \"exposure\" legally means")
Tokenizing exposure to private US equity is a regulated activity in most jurisdictions XMAQUINA's holders sit in. The site is careful to call DEUS a governance token, not a claim on the underlying equity — there is no white paper language promising pro-rata distribution of exit proceeds, only that governance can direct inflows toward "DEUS buybacks and staking rewards." Whether US holders can legally buy a token whose value tracks a portfolio of private securities is the open question this product depends on.
:::

## 02. The token

DEUS is an ERC-20 deployed on Base at `0x940A319B75861014A220D9c6c144d108552B089B`, Solidity 0.8.28, MIT-licensed, source-verified on Basescan. The contract bundles three non-default behaviors worth naming:

- **LayerZero OFT** — omnichain transfer surface, so the same token can move between Base, Solana, and peaq (the three chains CoinGecko lists).
- **ERC-5805 voting / delegation** — on-chain vote balance with delegation, the standard veToken substrate.
- **Owner-gated transfer flag plus a child-token guard** — transfers can be paused at the contract level; the contract can be locked out of further minting via a one-way "mark as child" call.

Allocation is laid out in [docs.xmaquina.io](https://docs.xmaquina.io/dao/tokenomics):

:::bars
- label: DAO Treasury
  value: '30.00%'
  pct: 30
- label: Genesis Auctions
  value: '23.24%'
  pct: 23
- label: Core Contributors
  value: '12.50%'
  pct: 13
- label: Liquidity & Ecosystem
  value: '8.26%'
  pct: 8
- label: Strategic Contributors
  value: '8.00%'
  pct: 8
- label: DEUS Dev Lab
  value: '7.50%'
  pct: 8
- label: Foundation
  value: '7.50%'
  pct: 8
- label: RCM Protocol
  value: '2.00%'
  pct: 2
- label: Advisors
  value: '1.00%'
  pct: 1
:::

Two cross-source notes. First, Impossible Finance's research report cites a slightly different split (Genesis 30%, Liquidity 3.5%) that does not match the current docs page; the docs are presumably the more recent authoritative version. Second, the contract's on-chain "max total supply" reads **874,148,340** today against a stated cap of **1,000,000,000** — the ~125.8M delta is consistent with allocations that haven't yet been minted (the 110M pre-sale block and ecosystem reserves due at TGE).

The May 27 TGE governance proposal allocated **128,067,280 DEUS** (12.8% of supply) and **$150,000 USDC** for the event: 110M for the final community pre-sale, ~18M plus the stablecoins for liquidity bootstrapping. The vote passed with 96% approval on roughly 19M votes cast.

## 03. Governance, on paper and on chain

The xDEUS veToken model follows the now-standard Curve / Aerodrome playbook: stake DEUS, mint a non-transferable vote-escrow position, get voting power that scales with lock duration. Operationally, proposals are aggregated from Snapshot (off-chain signaling) and Aragon OSx (on-chain execution), with a "governance-authorized multisig" handling operational settlement.

The docs page on governance does not publish a quorum threshold, proposal-submission threshold, or voting period — those mechanics live in the Aragon OSx config rather than in human-readable form. A spot-check of one execution path is possible today via the DAO Portal, but external observers can't replicate the parameters without reading the on-chain contract. Worth requesting publicly before staking.

:::callout(kind=danger, label="Centralization surfaces to verify")
Three contract behaviors deserve attention before the token is freely transferable: the owner-gated transfer flag (currently off, but owner-mutable), the absence of any security audit attached to the verified source on Basescan, and the multisig signer set governing operational settlement. None of these are necessarily disqualifying — most veToken systems carry similar surfaces during launch — but each is a single point of failure until either renounced or formally audited.
:::

## 04. Who's behind it, who's funding it

:::kv
- term: CEO / Co-founder
  def: Mauricio Zolliker — previously Head of Growth and Business Development at peaq
- term: CMO
  def: Jessica Alvarez — 10+ years marketing and communications
- term: Team size
  def: '7 full-time, 2 part-time (per Impossible Finance research, mid-2025)'
- term: Notable advisors
  def: Michael Ganser (ex-Cisco SVP), Simon Dedic (Moonrock Capital co-founder), Anil Lulla (Delphi Digital
    co-founder)
- term: Institutional backers (named)
  def: Borderless Capital, Moonrock, MH Ventures, Generative Ventures, Fundamental Labs, Waterdrip, vVv,
    Clairvoyant Labs, Signal Ventures, Wise3 Ventures, Mulana, EoT Ventures, CoinIX, Advanced Blockchain
- term: Total raised across waves
  def: $10M+ from ~2,000 contributors
- term: Headquarters
  def: Spain (per The AI Insider's January 2026 coverage of the $10M raise)
:::

Two takeaways from the cap table. Backers cluster in the Asia-and-EU crypto-native fund universe (Moonrock, MH, Waterdrip, KuCoin Ventures partners) rather than Silicon Valley deep-tech VCs — which makes sense for a token launch but is worth noting if the eventual exit path runs through US robotics M&A. The angel set, by contrast, is heavyweight: an ex-Cisco SVP, a Delphi co-founder, and the founder of Moonrock all sitting in the advisor tier with a combined ~1% of supply suggests genuine conviction rather than vanity placements.

## 05. Timeline

:::timeline
- date: '2024 Q4'
  headline: Pre-seed closed.
  body: Estimated $20–25M FDV per Impossible Finance; Advanced Blockchain AG named as a strategic investor.
- date: '2025-08'
  headline: Platform live.
  body: XMAQUINA.io launches; Genesis Auctions begin (Wave 1 at ~$37M FDV per Impossible Finance, with
    subsequent waves stepping up to $40M and $45M).
- date: '2025-Q4'
  headline: BOT-1 passes.
  body: 'First on-chain governance vote: strategic allocation to Apptronik, 98.05% approval via Snapshot.'
- date: '2026-01'
  headline: $10M raise milestone.
  body: Cumulative auction proceeds cross ten million; DAO declares itself "fully capitalized to continue
    securing stakes."
- date: '2026-05-12'
  headline: DEUS contract live on Base.
  body: Claims open for Genesis Auction participants (33% immediately, 67% over 12-month linear vest).
- date: '2026-05-27'
  headline: TGE scheduled.
  body: '110M DEUS final community pre-sale; ~18M + $150K USDC for liquidity bootstrap. Transfers expected
    to enable.'
:::

## 06. Risks worth pricing

This category of product — a DAO holding tokenized exposure to private US equity — sits in the most legally fraught corner of crypto. The risks to underwrite, in roughly descending order of how badly they'd damage holders:

1. **Securities classification.** If the SEC or an equivalent EU regulator classifies DEUS as a security claim on the underlying portfolio, secondary trading and exchange listings collapse. The project's defense is that DEUS is a governance token, not a profit-share — defensible but untested.
2. **Single-asset concentration today.** The treasury is currently one disclosed equity position (Apptronik) plus stablecoins and unspecified crypto. "Diversified humanoid robotics exposure" is the pitch; "one private stake plus optimism" is the current reality.
3. **Smart-contract risk without audit cover.** Basescan does not show a submitted audit report against the verified source. The contract is short and follows OpenZeppelin patterns, but for a token that will hold $10M+ in DAO-routed capital, this gap is unusual.
4. **Owner-mutable transfer flag.** Until owner privileges are renounced or moved to the DAO's own multisig, the deployer can in principle re-pause transfers. Worth tracking who currently holds owner.
5. **Apptronik mark-to-market is a project claim.** The "+100% in a few months" number on Apptronik exposure has no independent source; private-equity valuations are by definition illiquid marks. Treat as a marketing figure, not a P&L.
6. **Pre-TGE liquidity is thin.** ~$110 in DEX pools today; expect price discovery to be violent in the first week of free transferability.

## 07. What to verify before pulling the trigger

If you're considering participating in the May 27 pre-sale or post-TGE secondary, the things worth checking yourself rather than taking on faith:

- The pre-sale price and per-wallet cap — not yet published in the sources we could fetch; expect them in a final blog post in the week before TGE.
- The multisig signer set and whether contract ownership has been transferred from the deployer EOA. Read directly from the contract on Basescan.
- The Apptronik allocation size in dollars and the DAO's actual reported share. The DAO Portal at [dao.xmaquina.io](https://dao.xmaquina.io/) should now display this.
- The xDEUS lock terms — minimum lock duration, slope of voting power vs. lock length — before staking. These mechanics live in the Aragon OSx configuration rather than the docs page.
- Any audit posted between now and TGE. A token with this much treasury depth shipping unaudited would be a meaningful negative signal.

The thesis is coherent: humanoid-robotics private equity is hard to access, robotic capability is compounding rapidly, and a tokenized DAO structure is the kind of product that can plausibly underwrite the access gap. Whether DEUS specifically clears the legal, governance, and liquidity bars is what gets answered in the next sixty days.

---

## 08. Sources

1. [xmaquina.io](https://www.xmaquina.io/) — official homepage, verticals, named prospects.
2. [DEUS token page](https://www.xmaquina.io/deus-token) and [robotics token page](https://www.xmaquina.io/robotics-token) — token utility framing.
3. [docs.xmaquina.io/dao/tokenomics](https://docs.xmaquina.io/dao/tokenomics) — canonical allocation table.
4. [docs.xmaquina.io/dao/governance](https://docs.xmaquina.io/dao/governance) — xDEUS / Aragon OSx model.
5. [Basescan contract](https://basescan.org/token/0x940A319B75861014A220D9c6c144d108552B089B) — supply, holders, verified source, audit absence.
6. [XMAQUINA claim guide](https://www.xmaquina.io/blog/how-to-claim-your-deus-tokens) — 33% immediate / 12-month vest.
7. [XMAQUINA blog: Next steps for the DAO](https://www.xmaquina.io/blog/the-next-steps-for-the-dao) — Wave 1.5 figures, governance readiness.
8. [XMAQUINA blog: $10M raised](https://www.xmaquina.io/blog/10m-raised-to-reclaim-the-robotics-capital-markets) — named institutional backers and angels.
9. [XMAQUINA blog: DAO Portal](https://www.xmaquina.io/blog/introducing-the-xmaquina-dao-portal) — Apptronik passed BOT-1 at 98.05%.
10. [Impossible Finance research report](https://blog.impossible.finance/xmaquina-research-report/) — team backgrounds, pre-seed FDV, alternative allocation table.
11. [Phemex: TGE approval](https://phemex.com/news/article/xmaquina-approves-deus-token-generation-event-with-110-million-deus-for-presale-42899) — vote totals, 128M DEUS + $150K USDC allocations.
12. [TradingView / CoinMarketCal](https://www.tradingview.com/news/coinmarketcal:c0cabbee9094b:0-xmaquina-deus-tge-27-may-2026/) — TGE date 2026-05-27.
13. [BlockchainReporter](https://blockchainreporter.net/xmaquina-launches-deus-token-on-base-blockchain-expanding-web3-robot-investment-opportunities-on-chain/) — Base launch 2026-05-12.
14. [The AI Insider](https://theaiinsider.tech/2026/01/15/spain-based-dao-xmaquina-raises-10m-for-early-stage-robotics-investments/) — Spain HQ; $10M raise coverage.
15. [CoinGecko](https://www.coingecko.com/en/coins/xmaquina) — current liquidity (~$110), chains listed (Base, Solana, peaq).
