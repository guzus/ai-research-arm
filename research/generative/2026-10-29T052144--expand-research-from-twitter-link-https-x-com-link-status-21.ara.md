---
eyebrow: REPORT · AGENTIC PAYMENTS · STRIPE LINK
title: "Link balance hands an AI agent a funded wallet. The contract keeps every mistake on the user."
deck: Stripe's October 2026 launch moves consent from "approve each purchase" to "set a cap and walk away." The cap bounds the dollar loss per event. Neither the rules nor the evidence yet bound how often events happen.
lede: |
  On October 26, 2026 the Stripe-built Link account announced "Link balance," a way to fund an agent and let it buy while the owner is away.[^1] The first partner is Instinct, a text-message assistant.[^2] This article reads the product from its own contracts, the US payment rules, agent-security research and the traffic and volume data, and asks one question: what exactly is the user agreeing to, and does anyone have evidence that the bet pays off?
domain: finance
stats:
  - {label: Announced, value: "2026-10-26", note: "US, New York later"}
  - {label: Link users (Stripe, via Payments Dive), value: "300M", note: "registered wallets, not agent users"}
  - {label: Stripe 2025 volume, value: "$1.9T", note: "+34% YoY"}
  - {label: Disclosed agent volume, value: "no totals", note: "Visa cited only 'hundreds' of transactions"}
---

## 01. The direct answer

:::kv
- {term: "What it is", def: "A USDC balance inside Link, spent through a Lead Bank prepaid debit card or a Shared Payment Token, so an agent can buy under a per-purchase threshold without asking."}
- {term: "What the tweet calls a budget", def: "Two separate dials: a funded balance (cumulative ceiling) and a per-purchase threshold. The threshold is not a running budget."}
- {term: "Who bears an agent's mistake", def: "The user. The terms treat agent-initiated transactions as the user's own, including those caused by bugs, hallucinations or misinterpretations."}
- {term: "Is the balance insured", def: "No. The terms say it is not FDIC-insured and not a bank or deposit account."}
- {term: "Is there proof of demand", def: "Not yet. No agent-completed purchase volume has been disclosed, and the one native-checkout trial was scaled back."}
:::

The seed post is short. It says users can fund an agent to buy concert tickets overnight, get shoes when the price falls, or order a shopping list from one prompt, and that users choose how much to load and set spending limits.[^1] Everything else in this article comes from documents the post does not quote. *As of 2026-10-29.*

## 02. Two dials, not one budget

**Thesis: the consent model changed from per-purchase approval to a standing mandate, and the "budget" in the marketing is two different controls.**

In April 2026 Stripe launched the Link agent wallet. An agent signs in through OAuth, files a spend request with context, and the consumer approves it in the Link app before a one-time card or Shared Payment Token (SPT) is released. Stripe's own post says every request then required the person's review.[^3] Link balance removes that step below a threshold. The user chooses how much money to add and a limit for each purchase, and purchases above the limit still need approval.[^4] The limit applies to each purchase separately and does not accumulate. Setting it to $0 prevents the agent from skipping approval.[^4]

That means the cumulative ceiling is the funded balance, nothing else. The setup page says a funding link is invalid above $150 or outside USD, but the same coverage notes this is not a lifetime cap, so a user can top up again.[^4][^5] The older CLI documents harder limits: $500 per request, $500 per day, $20,000 per 30 days, a 30-minute approval window and 48-hour credential validity.[^6] Those are the original agent-wallet defaults, and no fetched page confirms they govern unattended balance spending. ==unverified: the daily and 30-day caps apply to Link balance==.

:::timeline
- {date: "2025-09-29", headline: "ACP and Instant Checkout", body: "Stripe and OpenAI launch the Agentic Commerce Protocol with merchants of record unchanged."}
- {date: "2026-03-06", headline: "OpenAI moves checkout to Apps", body: "OpenAI says Instant Checkout is moving to Apps."}
- {date: "2026-04-29", headline: "Link agent wallet", body: "Spend requests with human approval for every credential."}
- {date: "2026-08-24", headline: "Leak of unattended controls", body: "A Link setup screen shows budgets, recurring purchases and pre-approved future purchases."}
- {date: "2026-10-26", headline: "Link balance with Instinct", body: "Funded balance and per-purchase threshold go live in the US."}
:::

The sequence is consistent with the roadmap Stripe stated in April, which promised spending limits and a path to actions without extra approval.[^3][^7]

**Counterpoint.** A per-purchase cap with no cumulative cap per day would be weaker than a card with a monthly limit. The balance supplies that ceiling only if the user keeps it small. **Why it matters:** the safety of the product is a user-chosen number, not a protocol property.

## 03. The plumbing: USDC in, card out

**Thesis: the money is stablecoin behind a card, which changes who holds it and what protections attach.**

Link balance holds USDC, which the support page describes as designed to be worth $1 and backed by cash and short-dated Treasuries.[^10] The terms name Bridge, a Stripe company, as custodian of the digital assets in the custodial option, say Bridge does not take title, and say the user bears all risk of loss. A non-custodial option runs on Privy wallet infrastructure.[^11] Both are described as not FDIC-insured and not a bank or deposit account.[^11]

At checkout the card layer converts. The prepaid debit card is issued by Lead Bank, a federally chartered bank, with Stripe, LLC as program manager. At each purchase the system checks the stablecoin balance, sells enough stablecoin to fund the dollars, and declines the transaction if the balance is short.[^12] Authorizing a purchase is treated as express and irrevocable consent to the sale, and refunds return to the balance as stablecoin.[^12] The agreement states that funds on the card are not FDIC insured and that the card has no overdraft or credit feature.[^12] The fees listed in the agreement are $0, including foreign-currency transactions, though Visa may add its own charges abroad.[^12]

For an agent, there are two credential routes. A one-time virtual card works at any card-accepting web checkout, while an SPT works with merchants that accept it. The README says the virtual card is not restricted to Link-enabled sellers.[^6] An SPT is issued per transaction, bound to the seller's profile, carries a currency, a maximum amount and an expiry, and can be revoked.[^13] Stripe's Issuing for agents adds single-task cards that are invalidated after use and a real-time authorization webhook with a two-second default timeout.[^14]

**Counterpoint.** Those limits are enforced on Stripe's servers, as policy. The documentation describes a refusal rule, not a cryptographic proof held by the user.[^13] **Why it matters:** the guarantee is trust in Stripe's authorization logic, which is reasonable but is not the "protocol-level" safety the vocabulary suggests.

## 04. The contract: who eats the agent's mistake

**Thesis: Link's terms are explicit that an agent's error is the user's transaction.**

The terms state that the user is responsible for all agent-initiated transactions as if they had taken the action themselves, and that a connection authorizes transactions whether or not they were intended. They name transactions caused by bugs, hallucinations or misinterpretations, and those that differ from the user's instructions. The exception is a Stripe technical failure.[^11] The same document says such transactions are not treated as unauthorized transactions, and says US consumers who report unauthorized activity within 60 days may be eligible for a refund.[^11] The prepaid card agreement is consistent: the loss tiers are $50 if reported within two business days and up to $500 later, but anyone the user lets use the card, including software agents, is treated as authorized.[^12] Coverage of the launch repeats the point: users remain responsible if the agent buys a different item than the one shown.[^5]

The regulatory background explains why this is a design choice and not a quirk. Regulation E defines an unauthorized transfer as one initiated by a person without actual authority and from which the consumer receives no benefit.[^15] Its official comment keeps a consumer liable for transfers by someone they authorized until they notify the institution that the authority has ended.[^16] The liability tiers themselves are $50 within two business days, $500 afterward, and unlimited for later transfers if the institution proves timely notice would have prevented them.[^17] Delegating to an agent resembles the comment's case of a person given a card, though the comment was written about people, not software.

Whether the balance is even a Regulation E account is open. The prepaid-account rule applies full Regulation E treatment to accounts that meet its definition, and the fetched text was truncated before the error-resolution subsection.[^18] No regulator or court ruling that applies these provisions to AI agents turned up in our search. Stripe's money-transmitter arm, Stripe Payments Company, is licensed state by state, and its licence page says nothing about deposit insurance.[^19]

:::callout(kind=warn, label="Reading the terms")
The agreement and the regulation agree on the structure: a user who authorizes a software agent has authorized what it does within its permissions. The product's protection against a hijacker is the user's $50/$500-style tier, and its protection against a mistaken agent is the size of the balance.
:::

| Scenario | What the fetched documents say | Who bears the loss |
|---|---|---|
| Third party steals card details | Unauthorized-transaction coverage if reported in time[^11][^12] | Link, up to the tier caps |
| Agent buys the wrong item, hallucinated or misread | Not treated as unauthorized[^11] | User |
| Agent is steered by injected text to a bad merchant | Not addressed in fetched text; likely read as agent-initiated[^11] | Probably user |
| Stripe technical fault | Explicit exception[^11] | Link |

**Counterpoint.** The terms are a contract and can be softened by dispute handling, network rules and goodwill, none of which is visible in documents. **Why it matters:** a product aimed at consumers who do not read terms places the entire downside of model error in a clause.

## 05. Security: a cap bounds the loss, not the rate

**Thesis: pre-funded balances limit the damage from one manipulated session, and the research shows manipulation is common enough that the rate matters more.**

The arithmetic is simple. The loss from one compromised session cannot exceed the lesser of the balance and the number of transactions times the per-purchase threshold. We found no study that measured loss bounding through spending caps; that statement is our reasoning, not a finding. What the literature does measure is how often agents are redirected.

Anthropic reported that its browser agent's prompt-injection attack success rate fell from 23.6% to 11.2% on 123 test cases after mitigations, and that purchasing was gated behind an ask-the-user step in that product.[^20] A later Anthropic evaluation of Opus 4.5 under an adaptive attacker with 100 attempts per environment reported 7.6% with older safeguards and 1.4% with improved ones, and described even 1% as meaningful risk.[^21]

:::slope(left-label="Earlier safeguards", right-label="Later safeguards", unit=%)
| Item | Earlier safeguards | Later safeguards |
|---|---|---|
| Claude for Chrome, 123 test cases (Aug 2025) | 23.6 | 11.2 |
| Opus 4.5 adaptive attacker, 100 attempts (Nov 2025) | 7.6 | 1.4 |
:::

Independent academic work is less reassuring. Microsoft Research's Magentic Marketplace found that agents accept the first proposal they receive, giving speed a 10 to 30 times advantage over quality.[^22] StakeBench, a 2026 benchmark on shopping agents, reported indirect injection success of 41.67% to 68.59% and direct injection success of 76.85% to 92.28% across four configurations, with GPT-5 and Gemini-2.5-Flash backbones.[^23] A persuasion-based study found agents diverted in 25% of tasks on average across cloned shopping and service sites, ranging from 13% to 43% by model.[^24] A red-team of Google's payments protocol AP2 reported that merchant-controlled text could subvert agent behavior despite the protocol's authorization layer.[^25] OpenAI has said prompt injection is unlikely to ever be fully solved, and OWASP's first mitigation is to restrict the model's privileges to the minimum.[^26][^27]

Even absent an adversary, performance is not settled. ShoppingBench reported absolute success under 50% for GPT-4.1 on grounded shopping tasks.[^28] Those models are older than the ones now in service.

**Counterpoint.** Several of these are sandbox or clone environments, and the strongest Claude result is far lower than the headline rates. A defender can also run more than one control: merchant allowlists, category limits and the real-time authorization hook are available in Issuing for agents.[^14] **Why it matters:** a cap turns a catastrophic failure into a small one, and small ones repeated daily are still a cost the user pays under Section 04.

## 06. Is the Stripe stack differentiated?

**Thesis: the differentiation is cross-rail settlement and distribution, not a new trust primitive.**

Stripe co-developed the Agentic Commerce Protocol with OpenAI. The repository describes an Apache 2.0 open protocol jointly governed by OpenAI and Stripe as founding maintainers.[^29] Stripe's docs also list it as a member of the Tech Council of a second protocol, the Universal Commerce Protocol, which reads as hedging across standards.[^30] On the machine side, Stripe accepts agent payments through MPP and x402 in stablecoin, settled into a merchant's Stripe balance in fiat, with a stablecoin minimum of 0.01 USDC against a 50-cent SPT card minimum.[^31] That floor is where cards are weakest.

Competitors are mostly at the announcement stage. Visa's Trusted Agent Protocol was released with Cloudflare in October 2025 and rests on signing agent traffic.[^32] Visa's July 2026 call framed a $3 to $5 trillion addressable opportunity but gave no agentic transaction count,[^33] and its only count in our search was a December 2025 statement that hundreds of agent-initiated transactions had completed with partners.[^50] Mastercard's CEO said cards will prevail in an agentic world, and its machine-payments product has more than 30 launch users, with no counted volume.[^34] PayPal's second-quarter release reports $486.4B of payment volume and no agentic metric.[^35] Amazon reported that 350 million customers tried its shopping assistant over twelve months, which counts trying, not buying.[^36] Adyen launched an agentic product and joined the x402 Foundation, and its half-year release discloses no agentic volume.[^37] Only x402 has counted transactions: Chainalysis reported more than 100 million cumulative transactions on Base through the first quarter of 2026 while stating that mass adoption remains distant.[^38] Other counts reported by trade press differ and do not reconcile.[^39]

**Counterpoint.** Standards fragmenting favours the party that sits above them. ==unverified: a wallet with 200 million registered users, which Stripe's letter reports, is a distribution asset.== Payments Dive relays a Stripe figure of 300 million Link users globally, counting registered wallets and not agent users.[^9] **Why it matters:** Stripe's position is a bet that identity, risk and settlement outrank the protocol. The first partner, Instinct, is a single early-stage startup, so launch distribution is not evidence of scale.[^9]

## 07. Demand: forecasts versus what is observed

**Thesis: the forecasts differ by an order of magnitude because they define the thing differently, and the observed series measure something else again.**

McKinsey's scenario is up to $1 trillion of US B2C retail revenue orchestrated by agents by 2030, and $3 to $5 trillion globally.[^42] Bain's range is $300 to $500 billion, or 15% to 25% of US e-commerce, counting purchases agents initiate, influence or complete.[^43] The Census Bureau puts Q2 2026 US retail e-commerce at $340.2 billion, 17.1% of retail sales, up 12.2% from a year earlier.[^44] By our arithmetic that annualizes to about $1.36 trillion, so McKinsey's US figure is roughly three-quarters of today's entire US e-commerce, and Bain's upper end about 37%.

:::rank-list
- {label: "US e-commerce, Q2 2026 annualized (Census x4)", value: "$1,361B", pct: 100}
- {label: "McKinsey: agent-orchestrated US revenue, 2030 scenario", value: "up to $1,000B", pct: 73, highlight: true}
- {label: "Bain: US agentic, 2030, upper end", value: "$500B", pct: 37}
- {label: "Bain: US agentic, 2030, lower end", value: "$300B", pct: 22}
:::

The observed data are about AI-assisted discovery, not agent checkout. Adobe reported AI-referred US retail traffic up 693% in the 2025 holiday season, converting 31% better than other traffic.[^45] A human still checks out in that flow. Salesforce attributes $262 billion, about 20% of holiday sales, to AI and agents, and the page does not define how influence is measured.[^46] The one large native-checkout trial reversed: OpenAI said Instant Checkout is moving to Apps after launching in September 2025.[^47]

Economics cut both ways. Merchants paid $198.25 billion in swipe fees in 2025, with Visa and Mastercard credit at about 2.36% of volume, so an agent that routes to cheaper rails earns a reward for merchants and a threat for card revenue.[^48] The consumer side is unproven: an agent that waits for a price drop or an in-stock size is a good fit for a balance, though no source we fetched shows how many consumers want to delegate that decision.

**Counterpoint.** Conversion gains in AI-referred traffic are real, and growth from a small base is steep, so the funnel could convert quickly once an agent holds a credential. **Why it matters:** until one party publishes agent-completed volume, forecast ranges are definitions and not data.

## 08. What could break the thesis

**Thesis: the strongest objections are about evidence and incentives, not technology.**

- **The tail bound works.** If users keep balances small, losses stay bounded and the contract's harshness is irrelevant in practice. The source says the funding link is capped at $150 per link.[^4]
- **Agents get safer faster than attackers adapt.** The Anthropic results show a falling trend from 23.6% to 11.2% and from 7.6% to 1.4%.[^20][^21] The attacker still gets repeated attempts.
- **Regulators may reach agents.** We found no ruling on agent-initiated transfers, so the first dispute is a precedent in waiting.[^15][^16]
- **Disclosure arrives and is large.** Visa, Mastercard or Stripe could publish agent volume, which would replace the definitional spread in Section 07 with a measurement.[^33][^34]
- **The product is the contract.** A critic would add that a product whose terms assign all model error to the user is optimized for Stripe's risk, not the user's.[^11]

:::note
Two items could not be verified from primary text: how Link's terms interact with the prepaid-account rule in Regulation E, and whether the original wallet's daily and 30-day caps apply to Link balance. Treat both as open.
:::

:::references
- {id: 1, title: "Link (@link) - Introducing Link balance, 2026-10-26 (mirror)", url: "https://api.fxtwitter.com/i/status/2114799287645393098", source: "X via fxtwitter", date: "2026-10-26"}
- {id: 2, title: "Noah Shinn (@noahrshinn) - Give your Instinct a budget (mirror)", url: "https://api.fxtwitter.com/noahrshinn/status/2114796685251826016", source: "X via fxtwitter", date: "2026-10-26"}
- {id: 3, title: "Giving agents the ability to pay", url: "https://stripe.com/blog/giving-agents-the-ability-to-pay", source: "Stripe", date: "2026-04-29"}
- {id: 4, title: "Link balance brings USDC-funded agent spending to Instinct", url: "https://defiprime.com/link-balance-instinct-usdc-agent-spending", source: "DeFi Prime", date: "2026-10-27"}
- {id: 5, title: "Set up a balance for agent wallet purchases", url: "https://support.link.com/questions/set-up-a-balance-for-agent-wallet-purchases", source: "Link support", date: "2026-10-29"}
- {id: 6, title: "stripe/link-cli README", url: "https://github.com/stripe/link-cli/blob/main/README.md", source: "GitHub", date: "2026-10-29"}
- {id: 7, title: "Stripe is building unattended AI-agent spending into Link balance", url: "https://runtimewire.com/article/stripe-link-balance-ai-agents-unattended-spending", source: "RuntimeWire", date: "2026-08-24"}
- {id: 8, title: "Everything we announced at Sessions 2026", url: "https://stripe.com/blog/everything-we-announced-at-sessions-2026", source: "Stripe", date: "2026-04-29"}
- {id: 9, title: "Stripe's digital wallet and PayPal embrace AI bots", url: "https://www.paymentsdive.com/news/stripes-digital-wallet-paypal-embraces-ai-bots-agentic-commerce/830753/", source: "Payments Dive", date: "2026-09-18"}
- {id: 10, title: "Link balance FAQ", url: "https://support.link.com/questions/link-balance-faq", source: "Link support", date: "2026-10-29"}
- {id: 11, title: "Link terms (Agentic, Account, Link Balance terms)", url: "https://link.com/terms", source: "Link", date: "2026-10-29"}
- {id: 12, title: "Link Prepaid Debit Cardholder Agreement", url: "https://link.com/terms/prepaid-debit-cardholder-agreement", source: "Link / Lead Bank", date: "2026-10-29"}
- {id: 13, title: "Shared Payment Tokens", url: "https://docs.stripe.com/agentic-commerce/concepts/shared-payment-tokens.md?agent-seller=agent", source: "Stripe docs", date: "2026-10-29"}
- {id: 14, title: "Issuing for agents", url: "https://docs.stripe.com/issuing/agents", source: "Stripe docs", date: "2026-10-29"}
- {id: 15, title: "12 CFR 1005.2 Definitions (unauthorized EFT)", url: "https://www.consumerfinance.gov/rules-policy/regulations/1005/2/", source: "CFPB", date: "2026-10-29"}
- {id: 16, title: "Regulation E official interpretation, Section 1005.2", url: "https://www.consumerfinance.gov/rules-policy/regulations/1005/interp-2/", source: "CFPB", date: "2026-10-29"}
- {id: 17, title: "12 CFR 1005.6 Liability of consumer", url: "https://www.consumerfinance.gov/rules-policy/regulations/1005/6/", source: "CFPB", date: "2026-10-29"}
- {id: 18, title: "12 CFR 1005.18 Requirements for financial institutions offering prepaid accounts", url: "https://www.consumerfinance.gov/rules-policy/regulations/1005/18/", source: "CFPB", date: "2026-10-29"}
- {id: 19, title: "Stripe Payments Company licenses", url: "https://stripe.com/spc/licenses", source: "Stripe", date: "2026-10-29"}
- {id: 20, title: "Piloting Claude for Chrome", url: "https://claude.com/blog/claude-for-chrome", source: "Anthropic", date: "2025-08-25"}
- {id: 21, title: "Mitigating the risk of prompt injections in browser use", url: "https://www.anthropic.com/research/prompt-injection-defenses", source: "Anthropic", date: "2025-11-24"}
- {id: 22, title: "Magentic Marketplace", url: "https://arxiv.org/abs/2510.25779", source: "arXiv", date: "2025-10-27"}
- {id: 23, title: "StakeBench: shopping-agent attack benchmark", url: "https://arxiv.org/html/2606.13385", source: "arXiv", date: "2026-06-11"}
- {id: 24, title: "TRAP: persuasion injection on web agents", url: "https://arxiv.org/abs/2512.23128", source: "arXiv", date: "2025-12-29"}
- {id: 25, title: "Whispers of Wealth: red-teaming Google's Agent Payments Protocol", url: "https://arxiv.org/abs/2601.22569", source: "arXiv", date: "2026-01-30"}
- {id: 26, title: "OpenAI says AI browsers may always be vulnerable to prompt injection", url: "https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/", source: "TechCrunch", date: "2025-12-22"}
- {id: 27, title: "LLM01: Prompt Injection", url: "https://genai.owasp.org/llmrisk/llm01-prompt-injection/", source: "OWASP"}
- {id: 28, title: "ShoppingBench", url: "https://arxiv.org/abs/2508.04266", source: "arXiv", date: "2025-08-06"}
- {id: 29, title: "Agentic Commerce Protocol repository", url: "https://github.com/agentic-commerce-protocol/agentic-commerce-protocol", source: "GitHub", date: "2026-10-29"}
- {id: 30, title: "Agentic commerce protocols (UCP)", url: "https://docs.stripe.com/agentic-commerce/protocol", source: "Stripe docs", date: "2026-10-29"}
- {id: 31, title: "Machine payments", url: "https://docs.stripe.com/payments/machine", source: "Stripe docs", date: "2026-10-29"}
- {id: 32, title: "Cloudflare collaborates with leading payments companies to secure agentic commerce", url: "https://www.cloudflare.com/press/press-releases/2025/cloudflare-collaborates-with-leading-payments-companies-to-secure-and-enable-agentic-commerce/", source: "Cloudflare", date: "2025-10-14"}
- {id: 33, title: "Visa's $4T bet: agentic commerce as a growth driver", url: "https://forkast.news/visas-4t-bet-the-largest-payment-network-declares-agentic-commerce-a-growth-driver/", source: "Forkast", date: "2026-07-28"}
- {id: 34, title: "Mastercard touts agentic AI tools during earnings call", url: "https://www.americanbanker.com/payments/news/mastercard-touts-agentic-ai-tools-during-earnings-call", source: "American Banker", date: "2026-07-30"}
- {id: 35, title: "PayPal Q2 2026 earnings release (8-K)", url: "https://www.sec.gov/Archives/edgar/data/0001633917/000163391726000080/pypl2q-26earningsrelease.htm", source: "SEC EDGAR", date: "2026-07-28"}
- {id: 36, title: "Jassy on stores growth and AI shopping, Q2 2026", url: "https://www.aboutamazon.com/md/news/company-news/amazon-ceo-andy-jassy-stores-growth-ai-shopping-q2-2026-earnings", source: "Amazon", date: "2026-07-30"}
- {id: 37, title: "Adyen H1 2026 financial results", url: "https://www.adyen.com/press-and-media/adyen-publishes-h1-2026-financial-results-3wjne", source: "Adyen", date: "2026-08-13"}
- {id: 38, title: "x402 and agentic payments adoption", url: "https://chainalysis.com/blog/x402-agentic-payments-adoption", source: "Chainalysis", date: "2026-06-03"}
- {id: 39, title: "Coinbase's x402 has processed over 100 million transactions on Base", url: "https://crypto.news/coinbases-x402-has-processed-over-100-million-transactions-on-base/", source: "crypto.news", date: "2026-06-04"}
- {id: 40, title: "Stripe publishes 2025 annual letter and announces tender offer", url: "https://stripe.com/newsroom/news/stripe-2025-update", source: "Stripe", date: "2026-02-24"}
- {id: 42, title: "McKinsey forecast: $5 trillion agentic commerce sales by 2030", url: "https://www.digitalcommerce360.com/2025/10/20/mckinsey-forecast-5-trillion-agentic-commerce-sales-2030/", source: "Digital Commerce 360", date: "2025-10-20"}
- {id: 43, title: "2030 forecast: how agentic AI will reshape US retail", url: "https://www.bain.com/insights/2030-forecast-how-agentic-ai-will-reshape-us-retail-snap-chart/", source: "Bain", date: "2025-12-17"}
- {id: 44, title: "Quarterly retail e-commerce sales", url: "https://www.census.gov/retail/eCommerce.html", source: "US Census Bureau", date: "2026-08-18"}
- {id: 45, title: "AI has changed holiday shopping: here's what the numbers say", url: "https://www.marketingdive.com/news/ai-has-changed-holiday-shopping-heres-what-the-numbers-say/810265/", source: "Marketing Dive", date: "2026-01-23"}
- {id: 46, title: "2025 holiday shopping data", url: "https://www.salesforce.com/news/stories/2025-holiday-shopping-data/", source: "Salesforce", date: "2026-01-08"}
- {id: 47, title: "OpenAI shifts checkout plans, agentic commerce strategy", url: "https://digitalcommerce360.com/2026/03/06/openai-shifts-checkout-plans-agentic-commerce-strategy/", source: "Digital Commerce 360", date: "2026-03-06"}
- {id: 48, title: "Swipe fees totaled $198.25 billion in 2025", url: "https://insideoutdoor.com/?p=79926", source: "Nilson Report via trade press", date: "2026-03-18"}
- {id: 50, title: "Visa press release on agent-initiated transactions", url: "https://usa.visa.com/about-visa/newsroom/press-releases.releaseId.21961.html", source: "Visa", date: "2025-12-01"}
:::
