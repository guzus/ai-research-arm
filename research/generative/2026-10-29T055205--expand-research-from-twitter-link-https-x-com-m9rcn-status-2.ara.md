---
eyebrow: REPORT · PEOPLE DATA · AI AGENTS
title: "Ploid's two-billion-person index: what an agent-readable map of the human economy really has to survive"
deck: A founder tweet says every person and company on earth is now one API call away for "a few cents." The claim is easy to make and expensive to defend, in law, in data quality and in unit economics.
domain: policy
lede: |
  On 28 October 2026 Manny Hernandez, cofounder of Ploid, announced that his company had indexed more than two billion people and was selling access, to humans and AI agents alike, for a few cents. The post showed about 441,000 views when fetched.[^1] Strip away the launch energy and the interesting question is not whether such an index can be built. Aggregators have done it for a decade. It is whether a two-person startup can sell it to autonomous agents in 2026, when California has just switched on mass deletion, LinkedIn has sued data suppliers into shutting down, and the one federal rule that would have forced data brokers to accept FCRA obligations was withdrawn.
stats:
  - {label: Profiles claimed, value: ">2B", note: "self-reported, no methodology published"}
  - {label: Price per credit, value: "$0.15-0.20", note: "Scale / Growth plans"}
  - {label: Published plans, value: "3", note: "Growth, Scale, Custom"}
  - {label: Tweet views at fetch, value: "441,633"}
---

:::callout(kind=info, label="Direct answer")
**What was announced:** a people-and-company search index with web app, REST API, CLI and MCP server, claimed at more than two billion people.[^1,2]

**What is verified:** the product and its pricing page exist; the profile count, source mix and accuracy are not independently verifiable from anything Ploid publishes.[^2,3,4]

**Biggest risk:** not technology but the legal stack around contact data: platform contract law, state data-broker registration and deletion mandates, and GDPR transparency duties.[^8,12,14]

**Biggest opportunity:** the agent channel. Search for people is a tool call now, and the vendors that expose clean, evidence-tagged APIs will be called by agents the way search engines were called by browsers.[^2,28]
:::

## 01. What was actually announced, and what we can check

Section thesis: the launch is a real product with a published price list, wrapped in headline numbers that nobody outside the company can currently audit.

The seed tweet, posted 28 October 2026 by @m9rcn, says the team believes the world's data should be shared, that it has indexed over two billion people, that it merges public web information into one profile per person and company worldwide, and that humans and AI agents can get access for a few cents.[^1] The post is not a reply or quote, and showed 691 likes, 82 reposts and 978 bookmarks when fetched on 29 October 2026.[^1] Bookmarks well above likes suggest a tool people intend to try, but engagement says nothing about data quality.

Ploid's own site describes "a people search and intelligence platform: a living index of more than two billion people", reachable by web app, REST API, CLI and an OAuth 2.1 MCP server.[^2] Its listed endpoints include search, resolve, person, enrich, social and LinkedIn profiles, technographics and monitors, plus a "fill columns" feature that returns public evidence with a 0 to 1 confidence score per cell.[^2] The documentation tells developers to cite sources and separate evidence from inference, which is a sound instruction for a system whose profiles are partly machine-assembled.[^2]

Three details do not line up cleanly. First, the tweet's bio ties the founder to "YC F26", while a third-party directory lists Ploid in Y Combinator's S26 batch.[^1,6] Second, search-engine summaries of third-party directory pages quote a corpus of 1.4 billion rather than 2 billion; those pages warn they may be inaccurate, so treat the gap as noise rather than a contradiction. Third, the tweet says "a few cents", while the published price per credit is 15 to 20 cents, and the page does not state how many credits a person lookup consumes.[^1,3]

:::kv
- {term: "Claimed index size", def: ">2 billion people (company site, 2026-10-29)"}
- {term: "Surfaces", def: "Web app, REST API, CLI, MCP server (OAuth 2.1)"}
- {term: "Data sources named", def: "public web and professional-network signals, licensed or partner feeds, enrichment vendors"}
- {term: "Contact data vendor named", def: "FullEnrich (emails and phones)"}
- {term: "Accuracy disclosure", def: "Contact fields 'not guaranteed complete or current'"}
- {term: "Methodology for the 2B figure", def: "None published"}
:::

The privacy policy is more candid than the tweet. It lists source categories of "public web and professional-network signals, licensed or partner feeds, enrichment vendors," names FullEnrich as one email and phone supplier, and states that contact fields are not guaranteed complete or current.[^4] That admission matters: the product's value to an agent is precisely the contact field, and the vendor disclaims its freshness.

Why this matters: every downstream question, from legal exposure to unit economics, depends on what the two billion actually are. A count of records is not a count of distinct, correct, currently reachable humans, and the 2019 People Data Labs-linked exposure shows how far raw records can diverge from unique people: nearly 3 billion records de-duplicated to roughly 1.2 billion.[^20]

## 02. The money: where a new entrant sits in a commodity-plus-workflow market

Section thesis: raw person data is a crowded, thin-margin commodity, and the value is migrating to orchestration, which is where Ploid's agent-first interface is aimed.

The incumbent anchor is ZoomInfo. For fiscal 2025 it reported revenue of $1,249.5 million versus $1,214.3 million in 2024, roughly 3% growth, with net revenue retention of 90%, according to the company's results release.[^18] Sub-100% retention at the category leader is the first sign that selling more records is not a growth strategy by itself.

:::bar-chart(title="ZoomInfo annual revenue", subtitle="USD millions, fiscal years", orientation=vertical, value-unit=$, value-suffix=M)
categories: FY 2024, FY 2025
Revenue: 1214.3, 1249.5
:::

The growth is in workflow layers on top of data. Clay, which chains many data vendors behind a single enrichment step, restructured its pricing in March 2026 to meter workflow actions separately from data credits, which Sacra reads as monetization moving from enrichment to orchestration.[^19] Secondary coverage reports a September 2026 Series D at a multi-billion-dollar valuation, but I could not corroborate the round or ARR figures against a primary source, so I do not rely on them.

Ploid's price card sits inside this frame. Growth costs $200 per workspace per month for 1,000 credits ($0.20 each); Scale costs $600 for 4,000 credits ($0.15 each); credits pool across app, API, MCP and CLI and do not roll over.[^3] Resolve is free when nothing is found, and Fill-columns bills only found cells, a pay-for-hits model that aligns cost with success.[^2] The price list states no per-lookup credit cost, so the tweet's "few cents" cannot be tested.[^3]

:::bar-chart(title="Ploid published price per credit", subtitle="USD, as of 2026-10-29", orientation=horizontal, value-unit=$)
categories: Growth ($200/mo), Scale ($600/mo)
Price per credit: 0.20, 0.15
:::

Counterpoint: a few cents per profile is plausible if a lookup consumes a fraction of a credit, or if the tweet describes per-record cost at enterprise volume. Neither is documented. The bigger commercial risk is supplier leverage: a startup that resells vendors such as FullEnrich has little power over their prices or their data freshness.[^4]

Why this matters: the plausible winning move for a new entrant is not owning more records but being the cheapest and most legible endpoint for agents, which makes compliance posture a product feature rather than a footnote.

## 03. Layer one of the legal stack: access and contract law

Section thesis: the Ninth Circuit settled that scraping public pages is not a federal crime, but platforms have found that contract and fake-account claims work just as well, and they are using them.

The doctrinal anchor is hiQ v. LinkedIn. The Ninth Circuit, as summarised by counsel, declined to apply the CFAA's "without authorization" language to sites that generally allow public access and have not marked data as private.[^11] That is the part startups quote. The rest of the case is the part that ended the company: in a mixed November 2022 ruling the court found hiQ had breached the user agreement, and in December 2022 the parties stipulated to a $500,000 judgment plus a permanent injunction requiring hiQ to stop scraping and destroy the source code, data and algorithms derived from scraped profiles.[^11] hiQ is now defunct.[^11]

Meta v. Bright Data points the other way, narrowly. In January 2024 Judge Chen granted Bright Data summary judgment because Meta's terms govern a person's "use" of its products, and logged-off scraping of public data was not "use".[^12] The summary judgment concerned the contract claim and analyzes only Meta's terms, does not address scraping behind a login, and lets Meta rewrite its terms.[^12]

LinkedIn's enforcement since has shifted from the public-page argument to the fake-account argument. It sued Proxycurl's parent in January 2025 alleging mass fake-account creation; the product was reported shut down on 4 July 2025, and the founder is quoted saying that fighting a Microsoft-backed plaintiff was unwinnable regardless of the merits.[^15] In October 2025 LinkedIn sued ProAPIs, alleging an "industrial-scale" scheme of fake accounts that scraped data visible only to logged-in members and sold access for up to $15,000 a month; I did not confirm how that case ended.[^16] LinkedIn's user agreement bans scraping tools and bypassing access controls, and its help centre warns members that such tools can get accounts restricted.[^25]

:::timeline
- {date: 2022-12, headline: "hiQ consent judgment", body: "$500,000 and a permanent injunction after a CFAA win on public pages and a contract loss."}
- {date: 2024-01, headline: "Meta v. Bright Data", body: "Logged-off scraping of public data held outside Meta's terms; narrow reading."}
- {date: 2025-01, headline: "LinkedIn sues Proxycurl's parent", body: "Fake-account and mass-scraping claims in N.D. Cal."}
- {date: 2025-07, headline: "Proxycurl shuts down", body: "Founder cites an unwinnable cost asymmetry."}
- {date: 2025-10, headline: "LinkedIn sues ProAPIs", body: "Alleged fake-account mill selling logged-in data."}
:::

Ploid's own documentation says its profiles endpoint pulls full public profiles from social sites including LinkedIn.[^2] Whether Ploid scrapes directly, buys through intermediaries, or relies on licensed feeds is not disclosed, and the privacy policy lists all three source types.[^4] That ambiguity is the single most important unknown in this article. In my assessment, a startup relying on the Bright Data reading is on firmer ground than one relying on logged-in access, though that is one non-binding district-court ruling, and in either case it is exposed to a supplier being sued the way Proxycurl and ProAPIs were.[^15,16]

Counterpoint: contract claims need a counterparty bound by the terms. A vendor that collects only logged-off pages from sites whose terms bind only users has a plausible defence under the Bright Data reasoning.[^12] Press accounts of the Proxycurl endgame vary between settlement and injunction, and I did not locate the primary court order, so the exact terms should be treated as unverified.[^15]

Why this matters: for a data vendor the dominant legal risk is not prosecution but the loss of a supplier, which turns an apparently solid index into a depreciating asset.

## 04. Layer two: privacy law that treats "public" as a starting point

Section thesis: in the jurisdictions that regulate people data, "it was public" is a defence to some claims and no defence to others, and the enforcement calendar for 2026 is the heaviest yet.

**California.** The CCPA excludes "publicly available" information from personal information, and the CPRA widened that from government records to information a business reasonably believes was lawfully made available by the consumer or by widely distributed media.[^26] That helps a vendor, but it does not exempt the vendor from California's separate Delete Act. Data brokers must register annually, and the state's deletion platform DROP went live in January 2026, letting residents file one deletion request that is passed to registered brokers, which the agency's DROP page puts at over 600.[^8] Brokers had to start processing requests in August 2026, and a secondary summary reports they must pull requests at least every 45 days and face $200 per deletion request per day for non-compliance.[^10] Treat those last two figures as secondary until checked against the statute.

Enforcement is real and specifically hits the B2B contact-data niche Ploid occupies. In November 2024 the agency settled with Growbots, an outbound sales platform, for $35,400 and UpLead, a B2B lead generator, for $34,400, both for failing to register as data brokers.[^23] In August 2026 CalPrivacy fined Cybba $52,400 for failing to register before the 2025 deadline, its second broker action in under a week after LocateSmarter, and cited more than a dozen further actions against unregistered brokers.[^7] Because the registration penalty accrues at $200 per day, I read these fines as small mainly because the lapses were caught within months.[^23]

Ploid's privacy policy says it does not "sell your personal information for monetary consideration," says nothing about data-broker registration, takes deletion requests by email to a founder's address, and gives no response deadline beyond "applicable law".[^4,5] Whether Ploid is registered in California, Texas, Oregon or Vermont, all of which run broker registries, I could not determine, and a reader with registry access should check it.[^27] A business selling API access to person records for subscription fees will find the "no monetary sale" language hard to rely on under the statutory definitions, but that is a legal question I flag rather than resolve.

**Europe.** GDPR does not care that data is public. GDPR Article 14 requires telling people when their data is obtained from a third party. The Dutch authority fined Clearview €30.5 million in 2024, citing transparency failures and the lack of a legal basis for its scraped biometric image database, a weaker analogue for contact data.[^13] The closer analogue is France's CNIL fine against KASPR, a LinkedIn contact-extraction tool with about 160 million contacts. On 5 December 2024 CNIL fined it €240,000, finding it collected contact details even from users who had restricted who could see them, kept data for five years after each update, and only began notifying people four years after launch.[^14] The CNIL also held that telling data subjects the data came from "publicly accessible sources" did not satisfy the right of access.[^14] Ploid's policy cites GDPR rights and Article 77 complaint routes, but a founder-email process with no stated deadline is thin relative to what CNIL demanded of KASPR.[^5,14]

Counterpoint: the individual penalties against B2B contact vendors are small relative to venture funding. The deterrent effect lies elsewhere: injunctions to delete data, mandatory deletion pipelines, and the compliance overhead of answering every request properly.[^7,14]

Why this matters: a product built on an unaudited bulk corpus will meet its first regulator through a complaint, not a sweep, and the response process Ploid currently documents is the thing that will be examined.

## 05. Layer three: the federal gap and the state patchwork

Section thesis: the United States has no federal data-broker regime, the attempt to create one was withdrawn, and liability instead arrives through state statutes and private class actions.

On 15 May 2025 the CFPB withdrew its December 2024 proposal that would have treated sales of certain personal and financial data as consumer-reporting activity under the FCRA, saying a rule was not necessary at this time.[^17] State registration regimes such as California's remain in force, as the CalPrivacy actions above show.[^7] The practical consequence is that Ploid's policy language, which tells customers to comply with employment, credit and background-screening laws without naming the FCRA, puts compliance on users.[^4] If a customer uses the output for hiring or tenant decisions, the FCRA risk sits with them, and with the vendor if the product is ever found to be a consumer reporting agency in practice.[^4,17]

New Jersey shows how state law can bite. Daniel's Law lets covered public servants demand removal of home addresses and phone numbers, and assignee Atlas Data has sued data brokers under it. On 12 August 2026 the New Jersey Supreme Court addressed the statute's mental-state question in Atlas Data Privacy v. We Inform, in a ruling a law-firm summary frames as limited to certain actual-damages claims, while the Third Circuit's constitutional review was pending.[^21] I found no confirmed Third Circuit ruling. Whichever way it goes, it demonstrates that a bulk dataset containing home contact details creates plaintiff-friendly, statutory-damages exposure.

Private right-of-publicity suits are the other channel. In Kellman v. Spokeo, which concerned "teaser" profiles that used real names to sell subscriptions, the court denied dismissal in 2022, and a $10 million multi-state settlement was proposed in 2026, pending court approval.[^22,29] A people-search product that surfaces names and photos as marketing is exposed to this theory; an API that returns structured JSON to a logged-in customer is a different fact pattern, which is the best argument for Ploid's design.

:::callout(kind=warn, label="What this does not prove")
None of these cases is about Ploid. They are the nearest published precedents for businesses with its profile, and each turned on specific facts (teaser ads, fake accounts, unregistered status) that may not apply. Treat them as a risk map, not as predictions of liability.
:::

Why this matters: absent a federal rule, the expensive part of compliance is tracking a moving list of state obligations, which is a fixed cost that favours incumbents with legal teams over two-person teams.

## 06. The agent channel changes the threat model, and the accuracy question

Section thesis: selling to agents multiplies query volume and removes the human who might have noticed a bad record, so accuracy and provenance become safety features.

Ploid's API instructs clients to honour retry headers, use idempotency keys and set per-key usage budgets, and offers a free thirty-day trial through a first MCP connection with no card, though the site says workspace scopes still need browser approval by a human.[^2] That is the product's differentiator. It is also where privacy concerns concentrate: an agent can run thousands of lookups on named individuals as a side effect of a vague instruction. Ploid's terms prohibit stalking, doxxing and unlawful discrimination, but a terms-of-use prohibition is a policy, not a technical control.[^4]

On accuracy, the best public evidence is thin and conflicted. PeopleSearchBench, posted on arXiv in March 2026, evaluated four platforms on 119 queries across recruiting, B2B prospecting, expert search and influencer discovery. Lessie scored 65.2, Exa 55.0, Claude Code with Sonnet 4.6 46.0 and Juicebox 45.8.[^28] Two cautions apply. The authors work for LessieAI, which built the top-scoring platform. And Ploid was not among the systems tested, so the paper says nothing about it.[^28] What it does show is that general-purpose agents with web search already come within about 20 points of specialized platforms, which is the competitive baseline Ploid's two billion records must beat.

:::rank-list
- {label: "Lessie (authors' own platform)", value: "65.2", pct: 100, highlight: true}
- {label: "Exa", value: "55.0", pct: 84}
- {label: "Claude Code (Sonnet 4.6)", value: "46.0", pct: 71}
- {label: "Juicebox", value: "45.8", pct: 70}
:::

Counterpoint: a benchmark of four systems with a single LLM judge and an interested author is weak evidence of anything. The fair inference is only that independent evaluation of people-search accuracy is immature, and a vendor that publishes error rates would stand out.[^28]

Why this matters: the 2019 exposure of roughly 1.2 billion unique people from an open Elasticsearch server, which PDL denied owning but which held PDL-sourced indexes, shows what the failure mode of a mass people index looks like when it leaks, and an agent-accessible index adds a new exfiltration path.[^20]

## 07. What could break the thesis

Section thesis: three things would make the sceptical reading wrong, and three would make the bullish reading wrong.

**Against the sceptic.** First, Ploid may hold clean licences and registrations that its public pages simply do not mention; absence of evidence on a privacy page is not proof of non-compliance.[^4,5] Second, the agent-first design may genuinely reduce exposure compared with consumer people-search: no teaser ads, no public pages indexed by search engines, and authenticated, logged access that supports abuse investigations.[^2,22] Third, enforcement against B2B vendors so far has produced five-figure fines, not shutdowns, so the pace of regulatory consequence may be slower than the headline calendar implies.[^7,23]

**Against the enthusiast.** First, supplier risk: Proxycurl, described as a roughly $10 million ARR business, shut down within months of a lawsuit, and nothing in Ploid's disclosure rules out a similar dependency.[^15] Second, commoditisation: if general agents with web search reach comparable accuracy, the index is worth less than its record count.[^28] Third, the deletion pipeline: once DROP requests and GDPR access requests arrive at volume, a founder-email process is not a scalable operating model.[^5,8]

Red-team pass: two of the three strongest claims, the DROP timeline and the gap between Ploid's tweet and its price card, survived adversarial search unbroken. The third, the account of LinkedIn's ProAPIs suit, may be out of date, which is why its outcome is stated above as unconfirmed.

**What to watch.** The Third Circuit's Daniel's Law ruling; whether Ploid appears in the California registry before its next annual cycle; whether Ploid publishes a methodology for its profile count and per-lookup credit cost; and the final disposition of LinkedIn v. ProAPIs.[^16,21]

Bottom line: Ploid's idea, a people-and-company index designed for agents to call, is plausible and commercially timely. Its tweet is a marketing claim, and the infrastructure that would make it a durable business is mostly outside what is publicly visible: provenance of the two billion, registry status, deletion service levels and supplier contracts. Until those are published, the sensible stance for a buyer is to treat the index as an unverified lead generator, require evidence links on every field, and keep high-stakes decisions about named individuals out of agent loops.

:::references
- {id: 1, title: "Manny Hernandez (@m9rcn): Ploid launch post", url: "https://x.com/m9rcn/status/2115499043514445974", source: "X / Twitter", date: "2026-10-28"}
- {id: 2, title: "Ploid: people search and intelligence platform", url: "https://ploid.com", source: "Ploid", date: "2026-10-29"}
- {id: 3, title: "Ploid pricing", url: "https://ploid.com/pricing", source: "Ploid", date: "2026-10-29"}
- {id: 4, title: "Ploid privacy policy", url: "https://ploid.com/privacy", source: "Ploid", date: "2026-10-29"}
- {id: 5, title: "Ploid data rights and requests", url: "https://ploid.com/data-rights", source: "Ploid", date: "2026-10-29"}
- {id: 6, title: "Ploid on the JSV Launchpad directory", url: "https://www.jsv.com/launchpad/companies/ploid", source: "JSV", date: "2026"}
- {id: 7, title: "CalPrivacy announces second data broker enforcement action in less than a week (Cybba)", url: "https://privacy.ca.gov/2026/08/calprivacy-announces-second-data-broker-enforcement-action-in-less-than-a-week/", source: "California Privacy Protection Agency", date: "2026-08-13"}
- {id: 8, title: "About DROP and the Delete Act", url: "https://privacy.ca.gov/drop/about-drop-and-the-delete-act/", source: "California Privacy Protection Agency", date: "2026"}
- {id: 9, title: "ICYMI: California takes historic action against data brokers", url: "https://www.gov.ca.gov/2026/08/13/icymi-california-takes-historic-action-against-data-brokers/", source: "Office of the Governor of California", date: "2026-08-13"}
- {id: 10, title: "DROP is now live: what you need to know", url: "https://www.mondaq.com/drop-is-now-live-what-you-need-to-know/1828226", source: "Mondaq", date: "2026"}
- {id: 11, title: "hiQ and LinkedIn reach proposed settlement in landmark scraping case", url: "https://newmedialaw.proskauer.com/2022/12/08/hiq-and-linkedin-reach-proposed-settlement-in-landmark-scraping-case/", source: "Proskauer", date: "2022-12-08"}
- {id: 12, title: "Major decision affects law of scraping: Meta Platforms v. Bright Data", url: "https://www.fbm.com/post/102kqw7/", source: "Farella Braun + Martel", date: "2024-01-23"}
- {id: 13, title: "Netherlands: Clearview AI fined for violating the GDPR", url: "https://www.loc.gov/item/global-legal-monitor/2024-10-16/netherlands-face-recognition-company-clearview-ai-fined-for-violating-eus-general-data-protection-regulation/", source: "Library of Congress", date: "2024-10-16"}
- {id: 14, title: "Data scraping: KASPR fined €240,000", url: "https://www.cnil.fr/en/data-scraping-kaspr-fined-eu240000", source: "CNIL", date: "2024-12-05"}
- {id: 15, title: "The #1 LinkedIn scraping startup Proxycurl shuts down", url: "https://www.startuphub.ai/ai-news/startup-news/2025/the-1-linkedin-scraping-startup-proxycurl-shuts-down", source: "StartupHub.ai", date: "2025-07"}
- {id: 16, title: "LinkedIn sues ProAPIs for $15K/month scraping scheme", url: "https://securityaffairs.com/183001/security/linkedin-sues-proapis-for-15k-month-linkedin-data-scraping-scheme.html", source: "Security Affairs", date: "2025-10"}
- {id: 17, title: "CFPB withdraws its proposed rule on data brokers", url: "https://infobytes.orrick.com/2025-05-16/cfpb-withdraws-its-proposed-rule-on-data-brokers/", source: "Orrick", date: "2025-05-16"}
- {id: 18, title: "ZoomInfo announces fourth quarter and full year 2025 financial results", url: "https://www.businesswire.com/news/home/20260209677262/en", source: "Business Wire", date: "2026-02-09"}
- {id: 19, title: "Clay: revenue, valuation and funding", url: "https://sacra.com/c/clay/", source: "Sacra", date: "2026"}
- {id: 20, title: "PDL data exposure: a billion people", url: "https://nightlion.com/blog/2019/pdl-data-exposure-billion-people/", source: "Nightlion Security", date: "2019-10"}
- {id: 21, title: "NJ Supreme Court Daniel's Law Atlas Data Privacy decision", url: "https://www.clarkhill.com/news-events/news/nj-supreme-court-daniels-law-atlas-data-privacy-decision/", source: "Clark Hill", date: "2026-08"}
- {id: 22, title: "Class Action Weekly Wire 157: $10M settlement to resolve right-of-publicity class action (Spokeo)", url: "https://blogs.duanemorris.com/classactiondefense/2026/07/23/the-class-action-weekly-wire-episode-157-10-million-settlement-proposed-to-resolve-right-of-publicity-class-action/", source: "Duane Morris", date: "2026-07-23"}
- {id: 23, title: "CPPA settles with first set of data brokers (Growbots, UpLead)", url: "https://cppa.ca.gov/announcements/2024/20241114.html", source: "California Privacy Protection Agency", date: "2024-11-14"}
- {id: 25, title: "Prohibited software and extensions", url: "https://www.linkedin.com/help/linkedin/answer/a1341387", source: "LinkedIn Help", date: "2026"}
- {id: 26, title: "How do the CPRA, CPA and VCDPA treat publicly available information", url: "https://www.bytebacklaw.com/2022/01/how-do-the-cpra-cpa-vcdpa-treat-publicly-available-information/", source: "Byte Back Law", date: "2022-01"}
- {id: 27, title: "State data broker registry laws, fines and warnings", url: "https://therecord.media/state-data-broker-registry-laws-fines-warnings", source: "The Record", date: "2025"}
- {id: 28, title: "PeopleSearchBench: a multi-dimensional benchmark for evaluating AI-powered people search platforms", url: "https://huggingface.co/papers/2603.27476", source: "arXiv / Hugging Face", date: "2026-03-31"}
- {id: 29, title: "Three more yearbook/people database cases signal trouble for defendants", url: "https://blog.ericgoldman.org/?p=23960", source: "Technology & Marketing Law Blog", date: "2022"}
:::
