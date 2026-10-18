---
eyebrow: "Finance · Corporate Governance · Anthropic"
title: "Anthropic's Public Benefit Fund: what the 5%, the 2% tranches and the '20%' actually commit"
deck: "The 5% is real but needs a stockholder vote, the 2% tranches are optional, and three-quarters of the '20%' are personal pledges with no enforcement mechanism attached."
domain: finance
lede: |
  On Sunday 18 October 2026, about a month before its expected IPO, Anthropic said it would commit 5% of its shares to a new Anthropic Public Benefit Fund. The board could add a further 2% for every 50% rise in the company's value above a set baseline. Counting earlier founder and employee pledges, Anthropic said roughly 20% of its shares would be "dedicated to the public good". Each of those three numbers commits something different. This piece separates them: what is legally committed today, what depends on a future vote or on board discretion, and what rests only on the word of the people who made the pledge.
stats:
  - {label: "Initial stake", value: "5%", note: "subject to stockholder approval"}
  - {label: "Escalator", value: "+2%", note: "per +50% value, board discretion"}
  - {label: "Headline total", value: "~20%", note: "incl. founder & employee pledges"}
  - {label: "5% at Series H mark", value: "$48B", note: "5% × $965B post-money, May 2026"}
---

:::kv
- {term: "What is committed today?", def: "A promise to place 5% of Anthropic's shares in a wholly-owned LLC, conditional on a stockholder vote that has not happened. While the LLC holds them, the shares cannot vote under Delaware law, and in Anthropic's consolidated accounts they are treated like treasury stock."}
- {term: "What do the 2% tranches commit?", def: "Very little. Each tranche is at the board's discretion and the baseline is undisclosed. Depending on whether the +50% steps compound or add, a 10× rise in value implies a fund of 15% or 41% of the company. That is a ceiling the board may choose to reach, not a floor it owes."}
- {term: "What is the 20%?", def: "About 5 points are the fund. Roughly 9–10 points are the co-founders' 80% pledge, using Forbes' stake estimates, and the rest are employee pledges and Anthropic's matching shares. Only the employee shares already in donor-advised funds are plausibly irrevocable."}
- {term: "How big is it in dollars?", def: "About $48B at the $965B Series H preferred price, about $75B at the ~$1.5T IPO valuation investors reportedly discussed, and $0 of mandated annual payout, because an LLC has no distribution rule."}
- {term: "Who decides?", def: "Anthropic's seven-member board, where directors appointed by the Long-Term Benefit Trust have held a majority since April 2026. Governance rules for the fund itself are promised only 'in the coming months'."}
:::

## 01. The text, not the headline

Every downstream argument depends on what the announcement says, and it says less than the headlines suggest. The operative sentence is: "Subject to stockholder approval, 5% of Anthropic's shares will be committed today, with an additional 2% added at the board's discretion for every 50% increase in the company's value above a set baseline."[^1] The same post says the fund will be "a wholly-owned LLC—rather than a 501(c)(3) or other format", chosen for "adjustability between different forms of giving".[^1] It also promises that "none of the Anthropic equity held by the LLC will be used for lobbying or political giving, in the US or abroad."[^1]

The post leaves out several things a buyer of the IPO would want to know. It gives no baseline valuation, no share denominator (basic or fully diluted), no date for the stockholder vote, no named managers for the LLC, and no payout policy. Anthropic says only that "in the coming months, we will share more about the Anthropic Public Benefit Fund's structure and governance."[^1] Reuters' wire story, the most first-hand independent account, adds no executive quotes and no figures, and confirms that the trigger sits "above a baseline that has yet to be disclosed".[^2] Business Insider supplied the widely repeated "$48 billion", explicitly as arithmetic on "the company's most recent valuation in May".[^3] So the $48B is a reporter's multiplication, not an Anthropic disclosure.

The timing tells you how to read the post. It came four days after New York City's pension funds asked Anthropic to pause its IPO over governance,[^34] and in the same week Reuters reported that investors at Anthropic's investor day had discussed a valuation of about $1.5 trillion, against the roughly $2 trillion previously expected.[^9]

:::timeline
- {date: "2025-03-03", headline: "Series E at $61.5B post-money", body: "Lightspeed-led $3.5B round."}
- {date: "2025-09-02", headline: "Series F at $183B post-money", body: "ICONIQ-led $13B round; run-rate revenue 'over $5 billion'."}
- {date: "2026-02-12", headline: "Series G at $380B post-money", body: "$30B led by GIC and Coatue."}
- {date: "2026-04-14", headline: "Trust-appointed directors become a board majority", body: "Vas Narasimhan joins the seven-member board."}
- {date: "2026-05-28", headline: "Series H at $965B post-money", body: "$65B led by Altimeter, Dragoneer, Greenoaks, Sequoia; run-rate revenue over $47B."}
- {date: "2026-06-01", headline: "Confidential draft S-1 submitted", body: "Share count and price 'not yet set'."}
- {date: "2026-09-28", headline: "Reuters: Founder LLC to hold 50.1% of votes", body: "Draft S-1 gives co-founders a single Class F share with majority voting power on key matters."}
- {date: "2026-10-14", headline: "NYC Comptroller letter; investor day", body: "Pension funds ask Anthropic to pause the IPO; attendees reportedly discuss ~$1.5T."}
- {date: "2026-10-18", headline: "Public Benefit Fund announced", body: "5% now, +2% per +50% value step, '~20%' total public-good equity."}
:::

:::source
Anthropic newsroom (Series F, G, H, board, S-1 notice); Reuters via Investing.com and MarketScreener; NYC Comptroller.[^7,6,5,32,4,8,10,9,34]
:::

The pattern is a pre-IPO company facing a live governance critique and announcing a large, mostly conditional pledge. That does not prove the pledge is cosmetic, but it means the burden of proof falls on the governance documents Anthropic has not yet published. **Why it matters:** an IPO prospectus has to describe the fund's terms under securities-law liability. A blog post does not, so the S-1 is where the commitment will either harden or soften.

## 02. The 5%: committed to whom?

The first 5% is the only part of the package with a defined size, and even it is a promise to move shares into a box Anthropic itself owns. Three bodies of rules settle what that means while the shares sit in the LLC.

**Governance: the shares cannot vote.** Delaware's §160(c) says a corporation's own shares held by an entity it controls "shall neither be entitled to vote nor be counted for quorum purposes", and it applies expressly to any entity "if a majority of the voting power of such other entity is held, directly or indirectly, by the corporation".[^13] A wholly-owned LLC fits that definition exactly, so the fund's 5% is inert in every stockholder vote until it leaves Anthropic's control. (The statute preserves voting of stock held "in a fiduciary capacity", and the unpublished operating agreement could try to rely on that carve-out.)[^13]

**Accounting: the shares are not outstanding.** Under US GAAP, "shares of the parent held by a subsidiary shall not be treated as outstanding shares… [they] shall be eliminated in the consolidated financial statements and reflected as treasury shares."[^14] On Anthropic's consolidated statements, the fund's stake should therefore look like treasury stock: no dilution to earnings per share and no expense until shares or proceeds are actually granted to an outside recipient. (That is our reading of ASC 810; Anthropic has not disclosed how it will account for the fund.)

**Tax: the LLC is Anthropic.** A single-member LLC owned by a corporation is, by default, "reflected on its owner's federal tax return as a division of the corporation".[^15] So the LLC files no separate return and carries no exempt status. Crucially, nothing comparable to the private-foundation payout rule applies: a private foundation must distribute roughly 5% of its non-charitable assets each year or pay a 30% excise tax on the shortfall.[^16] Choosing the LLC buys flexibility and gives up any mandated spending clock.

:::callout(kind=warn, label="What 'committed' means here")
While the shares sit in the LLC, they cannot vote, they are not outstanding for accounting purposes, they are not separately taxed, and no rule forces them to be spent. Economically, they become someone else's only when a grant leaves the LLC. Until then, "committed" is a statement of intent backed by a stockholder resolution, not a transfer of ownership.[^13,14,15,16]
:::

There are real reasons not to use a 501(c)(3). A private foundation's holdings of a business are capped at "20 percent of the voting stock, reduced by" what disqualified persons own,[^17] and the founders' own stakes would count against that cap. The corporate charitable deduction is limited to 10% of taxable income (above a 1% floor) with a five-year carryforward,[^18] which is worth little to a company that only recently turned adjusted-profitable.[^61] Zuckerberg made the same trade in 2015: "By using an LLC instead of a traditional foundation, we receive no tax benefit… but we gain flexibility."[^21] His 8-K also disclosed that he "will control the voting and disposition of any shares held by such entity."[^22] Here the control sits with Anthropic's board rather than with an individual. Either way, the vehicle's owner keeps control until the money goes out.

Why is a stockholder vote needed at all? Under Delaware law a board can issue shares within the authorized count on its own, but raising the authorized count requires a charter amendment approved by "a majority of the outstanding stock" plus separate class votes where a class's authorized shares change.[^20] Pre-IPO preferred stock may also carry protective provisions that require separate class consent. Anthropic's charter is not public, so it is unclear which of these triggers the vote. The vote itself is the gating event.

### What 5% is worth depends on which price you use

:::bars
- {label: "Series G post-money ($380B, Feb 2026)", value: "$19.0B", pct: 25}
- {label: "Series H post-money ($965B, May 2026)", value: "$48.25B", pct: 64}
- {label: "Secondary blocks (~$1.4T, Sept 2026)", value: "$70B", pct: 93}
- {label: "Investor-day IPO talk (~$1.5T, Oct 2026)", value: "$75B", pct: 100}
:::

:::note
5% × each valuation mark. As of 2026-10-19. Series H is a preferred-stock price; the secondary figure is Caplight's estimate from thin block trading, share class unspecified; the $1.5T is anonymous-source investor talk, not a price range.[^5,4,12,9]
:::

None of these is a clean price for a block of common stock. The $965B is the post-money price of Series H preferred,[^4] which normally carries a liquidation preference that common lacks. The ~$1.4T secondary figure reflects scarce blocks, often sold piecemeal by fund GPs, with demand running 3–5× supply,[^12] up from about $1.2T in July.[^58] The $1.5T is what three anonymous attendees said investors discussed.[^9] **What would weaken this section:** if the S-1 shows the fund's shares going to an LLC with independent managers and an irrevocable transfer clause, §160(c) and treasury treatment would still apply, but control would move outside the board and "committed" would mean more. **Why it matters:** the dollar figure in every headline uses the most generous price available, for a stake that cannot yet vote, spend or be sold.

## 03. The 2% tranches: an option the board holds, not one it owes

The escalator looks like a formula, but it is a menu, and its size depends on two terms Anthropic has not defined. The text says 2% is added "at the board's discretion for every 50% increase in the company's value above a set baseline".[^1] Read strictly, that obliges nothing. A board can already issue shares within the authorized count,[^20] so the clause states a policy the board may follow, not a contingent right the fund can enforce.

The two undefined terms matter. First, are the +50% steps **arithmetic** (1.5×, 2.0×, 2.5× the baseline…) or **compounding** (1.5×, 2.25×, 3.375×…)? Second, is "2%" two percentage points of a fixed share count, or new issuance of 2% of then-outstanding shares? We modelled the percentage-point reading:

:::bar-chart(title="Maximum fund stake if every tranche is granted", subtitle="% of company, by value multiple of the undisclosed baseline", orientation=vertical, mode=grouped, value-suffix=%)
categories: 1.5×, 2×, 3×, 5×, 10×
Arithmetic +50% steps: 7, 9, 13, 21, 41
Compounding +50% steps: 7, 7, 9, 11, 15
:::

:::note
ARA calculation. Fund % = 5% + 2% × n. Arithmetic n = floor((M−1)/0.5); compounding n = largest k with 1.5^k ≤ M. Under a new-issuance reading each tranche also dilutes the fund's earlier shares, so 10× gives about 33.5% (arithmetic) or 14.0% (compounding).
:::

The gap is the most consequential undisclosed term in the announcement. At 10× the baseline, arithmetic steps imply 18 tranches and a fund owning 41% of the company. Compounding steps imply five tranches and 15%. Measured by what the fund receives relative to the value each step creates, compounding is self-consistent: every tranche costs existing holders about 6% of the increment it rewards. Arithmetic steps get steadily more expensive, rising to 40% of the increment by the 18th tranche. (These are ARA derivations; Anthropic has published no schedule.)

The baseline is the second trap. If it were the $380B Series G price,[^5] today's $965B Series H mark[^4] would already be 2.54× the baseline, triggering two or three tranches before the fund opens. The more plausible baselines are the Series H price or the IPO price, and the board decides which. A baseline set at an IPO price near $1.5T[^9] would mean the first tranche arrives only at roughly $2.25T.

### Compared with the obvious precedent

Anthropic presents the fund as an alternative to a common practice: "It is common practice for tech companies to offer escalating compensation awards to their executives… We are instead directing that equity to the public benefit."[^1] The comparison it invites is Tesla's 2025 CEO award: "12 tranches of 35,311,992 shares per tranche", 12% of the adjusted share count in total, "requiring $8.5 trillion market capitalization for the last tranche", with a preliminary fair value of $87.75B.[^23] The structures differ in ways that matter:

| Term | Tesla 2025 CEO award | Anthropic Public Benefit Fund |
|---|---|---|
| Size cap | 12 tranches, 12% of a fixed share count[^23] | None stated[^1] |
| Trigger | Market-cap milestones $2T→$8.5T, plus an operational milestone for each tranche[^23] | "Every 50% increase in the company's value" above an undisclosed baseline[^1] |
| Value test | Trailing-average market cap[^23] | Undefined ("company's value")[^1] |
| Earned how | Automatically, once disinterested directors certify the milestones[^23] | "At the board's discretion"[^1] |
| Beneficiary | One executive | A company-owned LLC |

There is a further tension. Reuters' account of the draft S-1 says the board has *also* promised Dario and Daniela Amodei more RSUs, some tied to retention and some to the IPO.[^11] The fund replaces a Musk-style mega-grant; it does not replace executive equity awards altogether. **What would weaken this critique:** a published schedule with a fixed baseline, per-share (not post-money) measurement, and automatic vesting would turn the menu into a contract. **Why it matters:** a raise of new primary capital lifts post-money "value" without any per-share gain, so an undefined "value" test could be met by fundraising alone. That is why Tesla tests trailing market cap and OpenAI's warrant tests share price.[^23,47]

## 04. Taking apart the "20%"

The 20% figure combines three different kinds of claim, and Anthropic gives no breakdown. The post says: "When Anthropic was founded, our co-founders pledged to donate 80% of their equity holdings"; Anthropic runs "an equity donation match program that allows employees to pledge equity which Anthropic matches"; "approximately half of our employees participate"; and "when combined with today's announcement, roughly 20% of Anthropic shares will be dedicated to the public good."[^1] Reuters notes the 20% excludes any future milestone shares.[^2]

**Founders.** The seven co-founders' stakes have not been disclosed; Reuters says the draft S-1 "does not describe the founders' share of ownership in the company."[^11] Forbes estimates each holds "just over 1.7%",[^24] which puts the seven at about 11.9% and their 80% pledge at about 9.5% of Anthropic. Bloomberg's wealth index says each owns "less than 1%",[^25] which caps the pledge at under 5.6%. The two estimates differ by roughly a factor of two, and that gap is the largest uncertainty in the arithmetic.

**Employees.** Anthropic's careers page today offers "optional equity donation matching at a 1:1 ratio, up to 25% of your equity grant."[^27] Earlier hires reportedly received a 3:1 match on pledges of up to 50% of their grants,[^28,30] so a full early pledge plus match equals twice the original grant in donated shares. The match is large. The Information reported, per secondary summaries, more than $660M of non-cash expense for matching stock between October 2025 and March 2026, excluded from adjusted operating profit.[^29,30]

:::donut(center-label="~20%")
- {label: "New Public Benefit Fund", value: 5}
- {label: "Co-founders' 80% pledge (Forbes basis)", value: 9.5}
- {label: "Employee pledges + Anthropic match (residual)", value: 5.5}
:::

:::note
ARA reconstruction, % of Anthropic shares. Anthropic discloses only the ~20% total. Founder slice = 7 × ~1.7% (Forbes) × 80%; employee slice is the residual. On Bloomberg's stake estimates the founder slice falls below 5.6% and the employee residual would have to exceed 9%, which requires near-universal maximum pledging by early staff.[^1,24,25]
:::

Bindingness splits the 20% even more sharply than the source of the shares does. Ranked by how hard each slice is to reverse:

:::stack-rows
categories: [Irrevocably transferred, Conditional on vote/board, Personal pledge only]
rows:
  - {label: "New fund (5 pts)", values: [0, 100, 0]}
  - {label: "Founder pledge (~9.5 pts)", values: [0, 0, 100]}
  - {label: "Employee pledges in DAFs + match (~5.5 pts)", values: [70, 0, 30]}
:::

:::note
ARA judgement on the evidence cited; the 70/30 split for employee shares is illustrative, since Anthropic has not disclosed how many pledged shares have actually moved to donor-advised funds.[^28,26,1]
:::

The founder pledge is the weakest link. A widely cited LessWrong post says "apparently this pledge is not legally binding",[^28] and Forbes notes "it's not yet clear how, when or to where they will transfer any funds."[^24] The wording has also narrowed over time. In January 2026 Fortune reported the pledge as 80% of the founders' "wealth",[^26] while the S-1 language reported by Reuters is 80% of "personal Anthropic equity".[^11] Employee pledges are firmer: an Anthropic employee wrote that their pledge is "legally binding, because of the equity already having been transferred to a DAF".[^28] But a donor-advised fund has no payout deadline, and the donor recommends the recipients. **What would weaken this section:** an S-1 beneficial-ownership table showing founder stakes and pledged shares already transferred to charitable vehicles. **Why it matters:** on our reconstruction, perhaps a quarter of the "20%" is irrevocable today. The rest rests on a stockholder vote, board discretion, or personal honour.

## 05. Who actually holds the pen

Every discretionary lever in the fund — whether to add tranches, how to spend, when to sell — runs through Anthropic's board, so the fund is only as independent as that board. Anthropic's Long-Term Benefit Trust holds Class T stock and elects a growing share of directors. Its design includes failsafes that let the arrangement change "without the consent of the Trustees if sufficiently large supermajorities of the stockholders agree".[^31] With Vas Narasimhan's appointment on 14 April 2026, "Trust-appointed directors now make up a majority of the Board", a board of seven that includes Dario and Daniela Amodei.[^32]

Two facts complicate the picture of a Trust-majority board guarding the fund:

- **The Trust is thin.** In August 2026 trustee Tino Cuéllar "stepped down from the Trust to join the company" as Chief Global Affairs Officer, running policy and government relations.[^33] That is a direct move from overseer to the executive team that handles policy. It matters because the fund's lobbying ban covers only "equity held by the LLC",[^1] while Anthropic itself has given $40M to the AI-policy group Public First Action.[^38]
- **The post-IPO structure concentrates founder votes.** According to Reuters' reading of the draft S-1, "a majority vote of the seven co-founders will direct a single share of Class F stock" amounting to "50.1% of the total voting power over key corporate matters", while the Trust elects the other four directors.[^10]

:::quote(attr="Mark Levine, New York City Comptroller, letter to Anthropic, 14 Oct 2026")
A gap between control and accountability is especially concerning for investors.
:::

Early public reaction made the same point in rougher terms. On Hacker News one commenter wrote that the money goes "to an LLC that is owned and controlled by anthropic", and another called "a 2% for every 50% increase… just insulting."[^57] The critics' common point is enforcement. Columbia's CLS Blue Sky blog published Marco Mari's framing: "For Anthropic, the question is who can check those entrusted with its mission."[^35] Zach Stein-Perlman argued in 2024 that "it may be easy for profit-motivated investors to reach a supermajority" that overrides the Trust.[^36] Delaware's PBC statute supplies one accountability tool, a stockholder benefit statement "no less than biennially", and limits suits to enforce the balancing duty to holders of 2% of shares (or $2M of listed shares).[^19] The public cannot sue, and neither can the fund: its own shares cannot vote,[^13] and as treasury-like shares they arguably do not count toward that 2%.

The economic owners may have little say either. Court filings in the Google search case showed Google owned 14% of Anthropic "but holds no voting rights, board seats, or board observer rights."[^37] Google then committed $10B in cash at a $350B valuation in April 2026, with $30B more if performance targets are met.[^59] So the stockholder vote that gates the 5% may be decided largely by voting common and preferred holders whose identities and protective provisions are not public. **Counterpoint:** a Trust-majority board is a real constraint by Silicon Valley standards, and the board, not the founders, holds the discretion. **Why it matters:** the fund has no independent governance of its own yet. Until its operating agreement names managers who are not Anthropic directors, "the public benefit" is whatever Anthropic's board decides it is.

## 06. Big philanthropy, small labour policy

At the Series H mark the fund would rank among the world's largest charitable pools. Measured against the labour-market disruption it gestures at, it is a pilot programme. Anthropic names one example use: "Anthropic has already committed $200 million to studying and addressing this issue", and the fund might pursue "large donations to traditional nonprofits or direct distributions to specific populations."[^1] That $200M is a research fund that "primarily fund[s] projects in the $5-30 million range", with "longer-duration unconditional income pilots at livable levels" on its agenda.[^39]

The CEO's own framing of the problem is far larger. Dario Amodei reiterated in January 2026 his warning that "AI could displace half of all entry-level white collar jobs in the next 1–5 years."[^40] In June 2026 he suggested long-term income support "could be financed through taxes on relevant companies or raising the capital gains tax."[^41] In other words, his own view is that the remedy at scale is fiscal, not philanthropic.

Annualised, the comparison is stark. No payout rule applies, but suppose the fund spent at the private-foundation rate of 5% a year[^16] on a $48.25B corpus. That is about $2.4B a year:

:::rank-list
- {label: "US unemployment insurance, 2025 (BEA)", value: "$36.9B/yr", pct: 100}
- {label: "Gates Foundation planned spend (from 2026)", value: "~$9B/yr", pct: 24}
- {label: "Fund at a 5% payout on $48.25B (hypothetical)", value: "$2.4B/yr", pct: 7, highlight: true}
- {label: "GiveDirectly, last 12 months", value: "$229M", pct: 1}
- {label: "Anthropic Economic Futures Research Fund (total)", value: "$200M", pct: 1}
:::

:::note
As of 2026-10-19. UI: FRED series A1589C1A027NBEA. Gates: Chronicle of Philanthropy. GiveDirectly: its own about page. The fund line is an ARA illustration, since the LLC has no payout rule.[^42,44,43,39]
:::

On those numbers, a 5% payout would equal about 6.5% of one ordinary year of US unemployment insurance, which was $36.9B in 2025 and $314.2B at the 2021 pandemic peak.[^42] Against private philanthropy it is large: about 27% of the Gates Foundation's planned annual spend under its plan to give away $200B by 2045,[^44] about ten times GiveDirectly's annual transfers (over $1 billion delivered since 2009),[^43] and about 2% of the $109.81B US foundations gave in 2024 out of $592.50B total giving.[^45] For scale on cash pilots: OpenResearch's study paid $1,000 a month to 1,000 people for three years and found recipients "worked 1.3 fewer hours per week".[^60] A $2.4B annual budget could fund pilots of that design for roughly 200,000 people.

**Counterpoint:** the fund is uncapped, and if the arithmetic escalator ran to 10× it could hold 41% of a far larger company, which would change the comparison by orders of magnitude. **Why it matters:** the fund can test income-support designs at a scale no NGO can, but it cannot be the income support. Anyone pricing it as an answer to AI-driven unemployment is overestimating it by about an order of magnitude.

## 07. Measured against precedents: control and payout, not headline percentage

Equity-for-public-good structures differ less in their headline percentages than in two quieter variables: who controls the shares, and how much has actually been paid out. On both, Anthropic's fund currently sits with the founder-controlled LLCs, not with the foundation-controlled companies.

| Vehicle | Headline stake | Who controls the shares | Paid out vs pledged |
|---|---|---|---|
| *Anthropic Public Benefit Fund (2026) | 5% + discretionary tranches[^1] | Anthropic's board, via a wholly-owned LLC[^1] | Nothing yet; no payout rule |
| OpenAI Foundation (2025) | 26%, ~$130B, plus a warrant if share price rises >10× after 15 years[^47,48] | Foundation appoints and removes the OpenAI Group board, under AG conditions[^50] | ~$40.5M announced Dec 2025 against a $25B pledge with no time frame[^49] |
| Novo Nordisk Foundation | >25% of capital, >70% of votes[^51] | Foundation, obliged to keep controlling ownership[^51] | DKK 11.8B (€1.6B) awarded in 2025[^52] |
| Hershey (Milton Hershey School Trust) | ~79% of votes[^53] | Trust | Ongoing school funding |
| Patagonia (2022) | 98% non-voting to Holdfast; 2% voting to a Purpose Trust[^54] | Family-steered Purpose Trust[^54] | ~$100M/yr expected dividends[^54] |
| Chan Zuckerberg Initiative (2015) | 99% of Facebook shares, ~$45B[^21] | Zuckerberg, via LLC[^22] | ~$4B to science since 2016[^56] |
| Salesforce 1-1-1 | 1% equity, product, time[^55] | Company | "Just shy of $900 million" in grants[^55] |

The closest structural analogue is OpenAI. Its foundation holds a 26% stake "valued at approximately $130 billion",[^48] plus a warrant for "an undisclosed amount of additional shares" if OpenAI Group's share price "grows more than tenfold after 15 years".[^47] Microsoft separately disclosed holding "roughly 27 percent on an as-converted diluted basis".[^46] The differences are telling. OpenAI's escalator is a contract tested on *share price* at a fixed date, and the nonprofit that holds the shares controls the company under state attorney-general conditions.[^50] Anthropic's escalator is discretionary, tested on undefined "value", and held by an entity the company controls. Payout is a weak point for both: the OpenAI Foundation pledged $25B "without providing a time frame", had announced $40.5M of grants by December 2025, and in March 2026 pledged $1 billion over the following year.[^49]

:::compare
- {role: "LOWEST", name: "OpenAI Foundation — granted vs. $25B pledge", value: "0.2%"}
- {role: "HIGHEST", name: "CZI — paid vs. ~$45B pledge", value: "~9%"}
- {role: "SUBJECT", name: "Anthropic fund — paid vs. ~$48B mark", value: "0%"}
:::

:::note
Ratios are ARA arithmetic on cited figures: $40.5M/$25B; ~$4B/~$45B. Different time horizons, so treat these as illustrations, not a league table.[^49,56,21]
:::

**Counterpoint:** an LLC is not automatically worse. CZI's flexibility let it fund for-profit science tools, and a 501(c)(3)'s 20% holdings cap[^17] would have forced Anthropic into a different design. **Why it matters:** the precedents that produced sustained payouts, Novo and Hershey, bound the shares to an independent holder. The ones that relied on the owner's discretion have paid out a single-digit share of their headline values.

## 08. Who pays: the dilution lands on outside holders

Charity funded with equity is not free. Somebody's ownership shrinks, and in this design it is outside stockholders, not the founders. If the 5% is newly issued, a holder of 10% before the fund holds 9.5% after. If every arithmetic tranche were granted up to 10× the baseline, that holder would fall to 5.9%. Under compounding the same holder ends at about 8.5% (ARA calculation; see §03). The founders' pledge, by contrast, comes out of the founders' own shares and dilutes no one.

The existing match programme previews the accounting. Per secondary summaries of The Information, the stock Anthropic issues to match employee pledges generated more than $660M of non-cash expense in six months, roughly $125M in Q1 2026 alone, and is "projected to climb into the billions after the IPO".[^29,30] Anthropic reportedly excludes it from adjusted operating profit, a treatment Calcbench's chief executive described to The Information as "not common at all".[^29] Reuters reported Q3 revenue of $16.8B and adjusted profitability.[^9] Investors should check whether future fund grants, which would be non-cash contribution expense at fair value when they leave the LLC, are excluded the same way.

:::callout(kind=info, label="For IPO buyers")
Read three things in the public S-1: (1) whether fund shares are counted in the fully diluted share count, (2) whether fund grants and match expense are excluded from adjusted metrics, and (3) the exact baseline and step definition. A sentence such as "issuable in Anthropic's discretion" means the escalator is an option the company holds, not an obligation it owes.[^1,29]
:::

**Counterpoint:** a 5% charitable carve-out may cost holders less than the alternative Anthropic names, a Musk-scale executive grant worth $87.75B at grant,[^23] and a credible public-benefit posture may lower political and regulatory risk enough to pay for itself. **Why it matters:** the fund's economic cost is real but deferred. It hits reported earnings only as grants go out, so the company's own disclosure choices will decide how visible it is.

## 09. What could break this analysis

This piece argues that the fund commits less than its headlines, chiefly because control stays inside Anthropic and the escalator is discretionary. Here is what would falsify or weaken that.

- **The governance documents could be strong.** Anthropic has promised details "in the coming months".[^1] An operating agreement with independent managers, an irrevocable-transfer clause, a published payout floor and Form 990-style reporting would make the 5% more binding than CZI's LLC and closer to the Novo model. The critique here is of what is known as of 2026-10-19, not of what may be published.
- **The escalator could be defined tightly.** A fixed baseline, per-share measurement and automatic grants would turn the menu into a warrant comparable to OpenAI's. Our 15%-vs-41% range is driven entirely by ambiguity that one sentence in the S-1 could resolve.
- **The founder stakes could be larger and the pledges firmer.** If the S-1 shows founder stakes at Forbes' 1.7% each[^24] and pledged shares already transferred to charitable vehicles, the "20%" becomes arithmetically honest and more binding than we credit.
- **Reputation can bind.** A PBC that publicly reneges on a dated, IPO-disclosed pledge risks its benefit report,[^19] its employees (about half of whom have pledged equity),[^1] and its regulatory standing. Commitments that are not legally enforceable are not therefore worthless.
- **The valuation premise could fail.** All dollar values here assume marks of $965B–$1.5T.[^4,9] Secondary-market participants have themselves said Anthropic "feels overpriced",[^12] so a lower IPO price would shrink every dollar figure while leaving the percentages unchanged.

Red-team pass: 3/3 top claims unbroken. An adversarial search found no source contradicting the conditional, LLC-held 5%, the undisclosed baseline and board discretion over tranches, or the $965B Series H mark. The only caveat it raised was the §160(c) fiduciary carve-out noted in §02.

:::references
- {id: 1, title: "Investing in the public benefit", url: "https://www.anthropic.com/news/public-benefit-fund", source: "Anthropic", date: "2026-10-18"}
- {id: 2, title: "Anthropic to commit 5% stake to new public benefit fund", url: "https://www.ksl.com/article/51637860/anthropic-to-commit-5-stake-to-new-public-benefit-fund", source: "Reuters via KSL", date: "2026-10-18"}
- {id: 3, title: "Anthropic commits billions to public benefit fund", url: "https://uk.finance.yahoo.com/news/anthropic-commits-billions-public-benefit-184601337.html", source: "Business Insider via Yahoo Finance", date: "2026-10-18"}
- {id: 4, title: "Anthropic raises $65B Series H at $965B post-money", url: "https://www.anthropic.com/news/series-h", source: "Anthropic", date: "2026-05-28"}
- {id: 5, title: "Anthropic raises $30 billion Series G at $380 billion post-money", url: "https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation", source: "Anthropic", date: "2026-02-12"}
- {id: 6, title: "Anthropic raises Series F at $183B post-money valuation", url: "https://www.anthropic.com/news/anthropic-raises-series-f-at-usd183b-post-money-valuation", source: "Anthropic", date: "2025-09-02"}
- {id: 7, title: "Anthropic raises Series E at $61.5B post-money valuation", url: "https://www.anthropic.com/news/anthropic-raises-series-e-at-usd61-5b-post-money-valuation", source: "Anthropic", date: "2025-03-03"}
- {id: 8, title: "Anthropic confidentially submits draft S-1", url: "https://www.anthropic.com/news/confidential-draft-s1-sec", source: "Anthropic", date: "2026-06-01"}
- {id: 9, title: "Investors temper Anthropic IPO valuation expectations over revenue growth slowdown, sources say", url: "https://www.marketscreener.com/news/investors-temper-anthropic-ipo-valuation-expectations-over-revenue-growth-slowdown-sources-say-ce785dd3d18ef225", source: "Reuters via MarketScreener", date: "2026-10-15"}
- {id: 10, title: "Exclusive: Anthropic leaders to control AI lab via founder LLC", url: "https://www.investing.com/news/stock-market-news/exclusiveanthropic-leaders-to-control-ai-lab-via-founder-llc-to-promote-public-good-over-market-forces-4921448", source: "Reuters via Investing.com", date: "2026-09-28"}
- {id: 11, title: "Exclusive: Anthropic's Amodei made $18 million last year", url: "https://www.investing.com/news/stock-market-news/exclusiveanthropics-amodei-made-18-million-last-year-middle-of-the-tech-ceo-pack-4933813", source: "Reuters via Investing.com", date: "2026-10-06"}
- {id: 12, title: "To buy Anthropic you need at least $25 million", url: "https://fortune.com/2026/09/03/anthropic-need-at-least-25-million-openai-closer-to-1-million/", source: "Fortune", date: "2026-09-03"}
- {id: 13, title: "Delaware Code Title 8, Ch. 1, Subchapter V (§160)", url: "https://delcode.delaware.gov/title8/c001/sc05/index.html", source: "State of Delaware"}
- {id: 14, title: "Roadmap: Noncontrolling interests, 6.6 (ASC 810-10-45-5)", url: "https://dart.deloitte.com/USDART/home/codification/broad-transactions/asc810-10/roadmap-noncontrolling-interests/chapter-6-attribution-income-other-comprehensive/6-6-attribution-in-income-in", source: "Deloitte DART"}
- {id: 15, title: "Single member limited liability companies", url: "https://www.irs.gov/businesses/small-businesses-self-employed/single-member-limited-liability-companies", source: "IRS"}
- {id: 16, title: "26 U.S. Code §4942 — Taxes on failure to distribute income", url: "https://www.law.cornell.edu/uscode/text/26/4942", source: "Cornell LII"}
- {id: 17, title: "26 U.S. Code §4943 — Taxes on excess business holdings", url: "https://www.law.cornell.edu/uscode/text/26/4943", source: "Cornell LII"}
- {id: 18, title: "26 U.S. Code §170 — Charitable contributions", url: "https://www.law.cornell.edu/uscode/text/26/170", source: "Cornell LII"}
- {id: 19, title: "Delaware Code Title 8, Ch. 1, Subchapter XV — Public Benefit Corporations", url: "https://delcode.delaware.gov/title8/c001/sc15/index.html", source: "State of Delaware"}
- {id: 20, title: "Delaware Code Title 8, Ch. 1, Subchapter VIII (§242)", url: "https://delcode.delaware.gov/title8/c001/sc08/index.html", source: "State of Delaware"}
- {id: 21, title: "Mark Zuckerberg defends giving money to an LLC", url: "https://www.nbcnews.com/tech/social-media/facebooks-mark-zuckerberg-defends-giving-money-llc-n474206", source: "NBC News", date: "2015-12-04"}
- {id: 22, title: "Facebook Form 8-K, December 2015", url: "https://www.sec.gov/Archives/edgar/data/0001326801/000132680115000035/form8kdec2015.htm", source: "SEC EDGAR", date: "2015-12-01"}
- {id: 23, title: "Tesla 2025 CEO Performance Award, Exhibit 99.2", url: "https://www.sec.gov/Archives/edgar/data/1318605/000110465925108507/tm2530590d1_ex99-2.htm", source: "SEC EDGAR", date: "2025-09"}
- {id: 24, title: "Anthropic cofounders become billionaires many times over (Forbes)", url: "https://www.forbes.com.au/?p=191366", source: "Forbes Australia", date: "2026-05-29"}
- {id: 25, title: "Anthropic co-founders worth $8 billion each after funding round", url: "https://news.bloomberglaw.com/private-equity/anthropic-co-founders-worth-8-billion-each-after-funding-round", source: "Bloomberg", date: "2026-05-29"}
- {id: 26, title: "Anthropic's billionaire cofounders are giving away 80% of their wealth", url: "https://fortune.com/2026/01/27/anthropic-billionaire-cofounders-ceo-dario-amodei-giving-away-80-percent-of-wealth-fighting-inequality-ai-revolution/", source: "Fortune", date: "2026-01-27"}
- {id: 27, title: "Careers at Anthropic", url: "https://www.anthropic.com/careers", source: "Anthropic", date: "2026-10-19"}
- {id: 28, title: "Front-load giving because of Anthropic donors?", url: "https://www.lesswrong.com/posts/oJM6TmFLwsHrBfRpk/front-load-giving-because-of-anthropic-donors", source: "LessWrong", date: "2025-12-04"}
- {id: 29, title: "Anthropic's charity-match charge hit $660M in six months to March", url: "https://aiweekly.co/alerts/anthropics-charity-match-charge-hit-660m-in-six-months-to-march", source: "AI Weekly (summarising The Information)", date: "2026-10-04"}
- {id: 30, title: "Anthropic charitable stock matching tops $660 million", url: "https://cryptobriefing.com/anthropic-charitable-stock-matching-660-million/", source: "Crypto Briefing (summarising The Information)", date: "2026-10-05"}
- {id: 31, title: "The Long-Term Benefit Trust", url: "https://www.anthropic.com/news/the-long-term-benefit-trust", source: "Anthropic"}
- {id: 32, title: "Vas Narasimhan joins Anthropic's board", url: "https://www.anthropic.com/news/narasimhan-board", source: "Anthropic", date: "2026-04-14"}
- {id: 33, title: "Tino Cuéllar joins Anthropic as Chief Global Affairs Officer", url: "https://anthropic.com/news/tino-cuellar", source: "Anthropic", date: "2026-08-04"}
- {id: 34, title: "Letter to Anthropic re: planned initial public offering", url: "https://comptroller.nyc.gov/reports/letter-to-anthropic-re-planned-initial-public-offering/", source: "NYC Comptroller", date: "2026-10-14"}
- {id: 35, title: "Marco Mari on founder control and Anthropic", url: "https://clsbluesky.law.columbia.edu/?p=72289", source: "Columbia CLS Blue Sky Blog", date: "2026-10-02"}
- {id: 36, title: "Maybe Anthropic's Long-Term Benefit Trust is powerless", url: "https://www.lesswrong.com/posts/sdCcsTt9hRpbX6obP/maybe-anthropic-s-long-term-benefit-trust-is-powerless", source: "LessWrong (Zach Stein-Perlman)", date: "2024-05-27"}
- {id: 37, title: "Google owns 14% stake in Anthropic, holds no voting rights", url: "https://www.tipranks.com/news/the-fly/google-owns-14-stake-in-anthropic-holds-no-voting-rights-ny-times-reports", source: "The Fly / TipRanks (NYT reporting)", date: "2025-03-12"}
- {id: 38, title: "Anthropic donates additional $20 million to Public First Action", url: "https://pulse2.com/anthropic-donates-additional-20-million-to-public-first-action-for-ai-policy-education/", source: "Pulse 2.0", date: "2026-07-22"}
- {id: 39, title: "Economic Futures Research Fund: research agenda", url: "https://anthropic.com/news/economic-futures-research-fund-agenda", source: "Anthropic", date: "2026-07-22"}
- {id: 40, title: "The Adolescence of Technology", url: "https://www.darioamodei.com/essay/the-adolescence-of-technology", source: "Dario Amodei", date: "2026-01"}
- {id: 41, title: "Policy on the AI exponential", url: "https://darioamodei.com/post/policy-on-the-ai-exponential", source: "Dario Amodei", date: "2026-06"}
- {id: 42, title: "Government social benefits: unemployment insurance (A1589C1A027NBEA)", url: "https://fred.stlouisfed.org/series/A1589C1A027NBEA", source: "BEA via FRED", date: "2026-09-30"}
- {id: 43, title: "About GiveDirectly", url: "https://www.givedirectly.org/about/", source: "GiveDirectly", date: "2026-10"}
- {id: 44, title: "The Gates Foundation announces plans to shutter in 2045", url: "https://www.philanthropy.com/news/the-gates-foundation-the-worlds-biggest-philanthropy-announces-plans-to-shutter-in-2045/", source: "Chronicle of Philanthropy", date: "2025-05-08"}
- {id: 45, title: "Giving USA 2025: U.S. charitable giving grew to $592.50 billion in 2024", url: "https://givingusa.org/giving-usa-2025-u-s-charitable-giving-grew-to-592-50-billion-in-2024-lifted-by-stock-market-gains/", source: "Giving USA", date: "2025-06"}
- {id: 46, title: "The next chapter of the Microsoft–OpenAI partnership", url: "https://blogs.microsoft.com/blog/2025/10/28/the-next-chapter-of-the-microsoft-openai-partnership/", source: "Microsoft", date: "2025-10-28"}
- {id: 47, title: "Microsoft gets 27% of OpenAI, access to AI until 2032", url: "https://sg.finance.yahoo.com/news/microsoft-27-openai-access-ai-053722572.html", source: "Bloomberg via Yahoo Finance", date: "2025-10-28"}
- {id: 48, title: "OpenAI completes restructuring into for-profit company", url: "https://finance.yahoo.com/news/openai-completes-restructuring-profit-company-151841977.html", source: "Quartz via Yahoo Finance", date: "2025-10-29"}
- {id: 49, title: "OpenAI Foundation pledges $1B in grants", url: "https://finance.yahoo.com/sectors/technology/articles/openai-foundation-pledges-1b-grants-160543442.html", source: "AP via Yahoo Finance", date: "2026-03-25"}
- {id: 50, title: "AG Jennings completes review of OpenAI recapitalization", url: "https://news.delaware.gov/2025/10/28/ag-jennings-completes-review-of-openai-recapitalization/", source: "Delaware Department of Justice", date: "2025-10-28"}
- {id: 51, title: "The Novo Group", url: "https://novoholdings.com/novo-group/", source: "Novo Holdings"}
- {id: 52, title: "DKK 11.8 billion awarded to benefit people and the planet in 2025", url: "https://novonordiskfonden.dk/en/news/dkk-11-8-billion-e1-6-billion-awarded-to-benefit-people-and-the-planet-in-2025/", source: "Novo Nordisk Foundation", date: "2026-02-25"}
- {id: 53, title: "The Hershey Company 10-K, stockholders' equity note", url: "https://www.sec.gov/Archives/edgar/data/47111/000162828026008586/R23.htm", source: "SEC EDGAR", date: "2026-02"}
- {id: 54, title: "Patagonia founder transfers ownership to fight climate change", url: "https://www.retaildive.com/news/patagonia-founder-transfers-ownership-earth-shareholder/631893/", source: "Retail Dive", date: "2022-09-14"}
- {id: 55, title: "Salesforce philanthropy: 1-1-1 model", url: "https://www.salesforce.com/news/?p=93389", source: "Salesforce", date: "2026-05-01"}
- {id: 56, title: "Zuckerberg, Chan shift bulk of philanthropy to science", url: "https://www.clickondetroit.com/business/2025/11/06/zuckerberg-chan-shift-bulk-of-philanthropy-to-science-focusing-on-ai-and-biology-to-curb-disease/", source: "AP via ClickOnDetroit", date: "2025-11-06"}
- {id: 57, title: "Investing in the public benefit (discussion)", url: "https://news.ycombinator.com/item?id=50143755", source: "Hacker News", date: "2026-10-18"}
- {id: 58, title: "Anthropic reportedly reaches $1.2 trillion valuation on secondary markets", url: "https://pulse2.com/anthropic-reportedly-reaches-1-2-trillion-valuation-on-secondary-markets/", source: "Pulse 2.0", date: "2026-07-12"}
- {id: 59, title: "Google to invest up to US$40B in AI rival Anthropic", url: "https://www.bnnbloomberg.ca/business/company-news/2026/04/24/google-to-invest-up-to-us40b-in-ai-rival-anthropic/", source: "Reuters via BNN Bloomberg", date: "2026-04-24"}
- {id: 60, title: "Unconditional cash study", url: "https://www.openresearchlab.org/studies/unconditional-cash-study/study", source: "OpenResearch", date: "2024-07"}
- {id: 61, title: "Anthropic's Q3 revenue hits $16.8B but growth slows ahead of planned November IPO", url: "https://the-decoder.com/anthropics-q3-revenue-hits-16-8b-but-growth-slows-ahead-of-planned-november-ipo/", source: "The Decoder", date: "2026-10-15"}
:::
