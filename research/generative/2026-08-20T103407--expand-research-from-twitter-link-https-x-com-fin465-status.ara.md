---
eyebrow: GROWTH TACTICS · SALES TECH
title: The "Secret" LinkedIn Buying-Intent Hack Isn't Secret, and Its Legal Ground Isn't Stable
deck: A viral tweet frames scraping LinkedIn posts for buying-intent language as an underused growth trick. The company behind it, the market it sits in, and LinkedIn's escalating enforcement record tell a more complicated story.
lede: |
  On 2026-08-20, Origami AI co-founder Finn Mallery told his followers about a "secret" tactic: scrape LinkedIn for posts and likes signaling buying intent, then cold-email the poster within hours. The playbook is real, but every part of the pitch — the novelty, the anecdote, and the legal footing — holds up worse than the tweet suggests.
stats:
  - {label: LinkedIn scraper suits since 2022, value: 3, note: "hiQ, Proxycurl, ProAPIs"}
  - {label: Real reply rate (disclosed studies), value: "0.45%", note: "vs. 3.4%+ marketed"}
  - {label: Closest EU fine, value: "€200K", note: "CNIL vs. Kaspr, Dec 2024"}
---

:::callout(kind=info, label="In short")
- The tactic — scraping LinkedIn posts for buying-intent language, then fast cold-emailing the poster — is not novel; it's a named "signal-based selling" sub-category with funded competitors that predate the viral tweet by years, and the identical mechanic is officially sold by G2 on its own review platform.
- LinkedIn has sued or delisted every scraping-dependent vendor that grew large enough to notice — hiQ Labs (2017-2022, $500K judgment despite winning the CFAA question), Proxycurl (shut down mid-2025 at $10M ARR), ProAPIs (sued Oct. 2025), plus a March-2025 search-visibility purge of Apollo, Seamless.ai, and Evaboot.
- The viral anecdote itself — a $25k/month founder, a signed deal 7 hours after a LinkedIn post — has no independent corroboration anywhere online, and its author has a documented pattern of posting precise, unaudited growth figures.
- Outside the US, the risk gets sharper: France's CNIL fined a directly comparable LinkedIn-enrichment tool, Kaspr, €200,000 in December 2024 for GDPR violations.
- None of this means the underlying category is worthless — it's a real, if modest and commoditized, corner of a multi-billion-dollar market. It means the specific pitch — that this is a secret, low-risk, repeatable trick — doesn't survive scrutiny.
:::

## 01. The pitch, the pitcher, and the company

A viral cold-outreach tactic traces to a real, YC-backed company whose own legal and marketing language quietly declines to make the LinkedIn claim its founder makes on X.

On 2026-08-20, Finn Mallery (@fin465) posted a tweet — 682 likes, 1,630 bookmarks, 58,900+ views — describing a pipeline: scrape LinkedIn posts containing phrases like "anyone got recommendations for [tool]," pull the people who *liked* similar posts, enrich the results with verified emails, and cold-email within hours of the post going up [^1]. The thread closes on a plug for his own product, Origami AI, which he says "searches linkedin by keyword in real time... with verified contact info attached" [^1].

Origami AI (origami.chat) is not a fabricated shell — it's a Y Combinator F24 company co-founded by Mallery and Kenson Chung, based in San Francisco [^2].

:::stats
- {label: YC batch, value: F24}
- {label: Seed round, value: $2M, note: "Jan 2025, VentureBeat"}
- {label: Beta MRR, value: $50K, note: "8-week beta, founder-reported"}
:::

VentureBeat reported the company raised a $2M seed and reached $50K in monthly recurring revenue during an eight-week beta, with the founders quoted calling it the fastest-growing startup in their YC batch [^3]. Those are founder-supplied numbers relayed by press, not figures an outside party has audited — a distinction that matters once the growth-hacking anecdote in the tweet is weighed on its own.

:::timeline
- {date: 2024, headline: "Origami AI founded", body: "Y Combinator F24 batch; co-founders Finn Mallery and Kenson Chung, San Francisco."}
- {date: 2025-01, headline: "$2M seed round", body: "VentureBeat reports the raise alongside an $50K-MRR, 8-week-beta claim attributed to the founders."}
- {date: 2026-02, headline: "#1 Product of the Day, 1,000+ signups", body: "Product Hunt launch reported as organic growth with no paid marketing — again a company-sourced claim, not externally verified."}
:::

The Product Hunt milestone repeats the pattern: #1 Product of the Day and over 1,000 signups in February 2026, described as "organic growth" achieved with "no paid marketing" [^4]. That characterization originates inside the company and was carried by coverage without independent confirmation.

Here is the tension the tweet obscures. Origami's own homepage describes searching "50+ sources in real time — Google Maps, social profiles, job boards, company sites" — and does not name LinkedIn anywhere in the visible product copy, even though LinkedIn is the explicit mechanism Mallery describes publicly [^5]. The company's Terms of Service go further: they require the *customer*, not Origami, to represent that "your use of LinkedIn and any other connected platform complies with that platform's terms of service," and warn that platforms may restrict or terminate accounts running automated outreach [^6] — language that contractually routes LinkedIn-ToS exposure onto the end user. Origami's Privacy Policy, meanwhile, names LinkedIn only as an ad/subprocessor vendor and an optional user-connected account, describing enrichment sourcing in the generic terms of "third-party data providers and publicly available sources" rather than naming LinkedIn scraping directly [^7]. A founder can say "LinkedIn" on X; the documents his own company is bound by are notably less specific.

Mallery's background adds a second layer of caution. An independent org-chart aggregator lists his prior role as "Director of Stanford Operations" at Fizz, a campus social app that raised over $40M — an operations title, not a founder or CEO role, and no earlier company he founded or led was found [^8]. His "studied AI at Stanford" framing is self-reported across bio and aggregator profiles with no institutional confirmation, and sits awkwardly next to his own April 2025 tweet stating he "left stanford after the first day of class to build an ai startup" [^9] — a claim hard to square with language describing a completed course of study.

That matters directly for the viral anecdote itself: exhaustive search turned up no independent corroboration anywhere online of the specific story in the tweet — a YC founder reaching $25k/month via this technique, closing a deal seven hours after a public LinkedIn post. It traces to a single tweet, with no named company, no third-party witness, and no earlier mention [^1]. And it is not an isolated case: Mallery has a multi-year, cross-tweet history of posting precise, high-specificity, self-reported growth figures — "3,119 emails, 5.3% response rate... ~$22k new MRR" in 40 days, "0-to-$10k MRR in 30 days" — none independently audited [^10], a pattern consistent with the broader "growth-hacking influencer" genre rather than a one-off case study.

To be fair, founder-reported MRR and growth figures without third-party audit are standard practice at the seed stage across the startup world — Mallery's numbers are not unusually unverifiable for a company this size, just unverified. What is unusual is the gap between what he claims the product does on X and what the product's own binding documents say it does — a gap the rest of this piece uses as the seam to pull on when testing whether the tactic, and the legal cover it implies, actually holds up.

## 02. Not a secret: the category already exists

Scraping public posts for buying-intent language and racing to the poster's inbox is not an underused hack; it is a named, funded, populated corner of a market already worth billions. The category holding that tactic — commonly called "signal-based selling," sometimes "social listening for sales" — sits inside the broader sales-intelligence software market, which independent analysts size at roughly $4.99B globally in 2026, growing from an estimated $4.42B in 2025 toward $9.15B by 2031 at a 12.89% compound annual growth rate [^11]. Other research firms' estimates for the same category range from under $0.5B to more than $12B depending on how broadly "sales intelligence" is scoped, so the dollar figure below should be read as directional, not precise.

:::compare
- {role: LOWEST, name: "2025", value: $4.42B}
- {role: HIGHEST, name: "2031 (forecast)", value: $9.15B}
- {role: SUBJECT, name: "2026", value: $4.99B}
:::

The specific mechanic — monitor public LinkedIn (and X) posts for hiring signals, funding news, complaint language, or competitor mentions, then trigger outreach — predates the viral pitch by close to a decade. LeadSift has run this play since roughly 2016 as part of the Terminus account-based-marketing stack, scraping public posts, forums and job boards for buying-signal language at scale, and is licensed as one of Apollo's own intent-data sources today. A newer wave of venture-backed tools — Buska, OutX, Cleed, Trigify, Gojiberry AI, Teamfluence, and Mentionkit — pitch essentially the same "LinkedIn post monitoring, fast contact" workflow as a standalone product [^12]. None of these is a household name, which is itself informative: the tactic has had years to compound into a dominant platform and has instead stayed a fragmented tier of small tools competing on the same idea.

Database-scale claims across the vendors that sit above this layer are inconsistent even within a single company's own site — Apollo.io's own pages cite 210 million contacts in its API documentation, 240M+ on its flagship product page, and 275M+ contacts across 73 million accounts in its support knowledge base [^13] — and the spread only widens across competitors:

:::rank-list
- {label: "Seamless.ai", value: "1.3-1.7B contacts", pct: 100}
- {label: "Cognism", value: "400-440M contacts", pct: 28}
- {label: "ZoomInfo", value: "~500M (self) / 265-321M (3rd-party)", pct: 27}
- {label: "Lusha", value: "280M contacts", pct: 19}
- {label: "Apollo.io", value: "210-275M contacts (inconsistent, self-reported)", pct: 16, highlight: true}
:::

The same "scrape public text for intent signal, then contact" mechanic exists well outside LinkedIn, too. On Reddit, F5Bot has offered free keyword alerting across Reddit, Hacker News, and Lobsters since 2017, and a newer commercial layer — Linkeddit, Octolens, Syften, Awario — adds lead-scoring and drafted replies on top of the same raw signal [^14]. That layer is noisier than it looks: one vendor's self-reported data put the false-positive rate on Reddit keyword matches at roughly 92%, meaning the "find the exact prospect" framing understates how much of this is manual triage after the scrape, not before it.

On review platforms, the identical signal type isn't merely tolerated — it's sold as an official first-party product, the inverse of LinkedIn's posture (Section 03). G2 runs "Buyer Intent Data" directly through sell.g2.com, built from its own 100M+ annual review-marketplace visitor traffic, and third-party tools such as Amplemarket build reviewer-identification features on top of G2 and Capterra review activity with the platforms' blessing [^15].

There is a real edge here, though the sourcing deserves a caveat: vendor material reports proactive, signal-driven sales motions closing at 33-41% win rates versus 18-25% for reactive outreach, and signal-driven outbound getting replied to 73% more often than generic cold sends [^16] — figures that trace back through vendor blogs citing other vendor or research sources, not an independently audited study. Even taken at face value, "signal-based selling" remains a smaller, less-capitalized corner of the market than the co-op and first-party intent-data leaders — Bombora, 6sense, and ZoomInfo's own intent products — which aggregate demand signal across thousands of B2B sites rather than one scraped feed. That matters for how the viral pitch should be read: what's being sold as a discovered trick is, at best, a competent implementation of a well-known, moderately effective, and already commoditized category — not a secret that gives its user an edge the rest of the market lacks.

## 03. The legal ground is not stable

Every company that has built a product on top of LinkedIn scraping has eventually been sued, forced to settle, or shut down entirely — and the pattern has only hardened as LinkedIn's parent Microsoft has scaled up enforcement each year since 2017.

LinkedIn's User Agreement is unambiguous on paper: Section 8.2 bars using "any automated software, devices, scripts, robots or other means or processes" to access, scrape, or copy data from the platform, prohibits redistributing anything obtained from LinkedIn without consent, and separately bans using bots or automation to send connection requests or messages [^17]. A signal-based selling tool that watches profile activity and drafts outreach off it sits close to the center of that clause, not at its edge.

The case that gets cited as the industry's legal safe harbor, *hiQ Labs v. LinkedIn*, is more equivocal than the headline suggests. The Ninth Circuit held in 2019 — and reaffirmed on remand in 2022 after the Supreme Court's *Van Buren* decision narrowed "unauthorized access" — that scraping data LinkedIn had made publicly visible does not violate the federal Computer Fraud and Abuse Act [^18]. That is a narrow ruling about one criminal-liability statute, not a green light for building a business on LinkedIn's data. hiQ won that single question and still lost the war: the parties settled in December 2022 for a **$500,000** judgment against hiQ plus a permanent injunction ordering it to destroy every piece of LinkedIn-derived data, source code, and algorithm it had built [^19]. hiQ had already bled funding, clients, and staff across six years of litigation uncertainty; the CFAA win came too late to save a company that was, by the time of settlement, effectively dead. The lesson buried in that outcome is the section's thesis in miniature: technical legality and commercial survival are separate axes, and LinkedIn has repeatedly used breach-of-contract theory — not the CFAA — to win the axis that actually kills a company.

:::timeline
- {date: 2017, headline: "hiQ v. LinkedIn litigation begins", body: "hiQ sues LinkedIn after a cease-and-desist over profile scraping, opening six years of CFAA litigation."}
- {date: 2019, headline: "Ninth Circuit hands hiQ a narrow CFAA win", body: "Scraping public profile data does not violate the CFAA's unauthorized-access clause — a criminal-liability holding, not a business green light."}
- {date: "Dec 2022", headline: "Kennected cease-and-desist and hiQ contract settlement", body: "LinkedIn sends Kennected a cease-and-desist over scraping and fake engagement; the same month hiQ settles LinkedIn's contract claims for $500K plus a data-destruction injunction, despite its CFAA win."}
- {date: "Jan-Jul 2025", headline: "Proxycurl sued, then shut down at $10M ARR", body: "LinkedIn sues the scraping-API vendor over hundreds of thousands of fake accounts; Proxycurl settles and shutters a product generating roughly $10M annually."}
- {date: "Mar-May 2025", headline: "Apollo, Seamless.ai, Evaboot purged from LinkedIn search", body: "LinkedIn removes lead-gen vendors' company pages and search visibility; smaller vendors vanish from LinkedIn entirely while Apollo absorbs the hit via diversified sourcing."}
- {date: "Oct 2025", headline: "ProAPIs (iScraper) sued", body: "LinkedIn alleges over 1M fake accounts scraping data sold at up to $15,000/month; its VP of Legal cites the Proxycurl settlement as precedent."}
:::

:::stats
- {label: hiQ settlement, value: $500K}
- {label: Proxycurl ARR at shutdown, value: $10M}
- {label: ProAPIs alleged fake accounts, value: "1M+"}
- {label: ProAPIs price point, value: $15K, unit: "/mo"}
:::

The most recent cases show the pattern compounding rather than plateauing. LinkedIn sued Proxycurl (Nubela Pte Ltd) in January 2025 over an alleged industrial-scale fake-account scraping operation; Proxycurl settled and permanently shut down its product that July, walking away from roughly **$10 million** in annual revenue [^20]. Its founder was explicit that the shutdown wasn't a concession that scraping was illegal — it was the American Rule on legal fees colliding with a Microsoft-backed litigation budget: "there is no winning in fighting this" [^20]. Nine months later, LinkedIn sued ProAPIs Inc. over its "iScraper API," alleging over a million fake accounts scraping data at 150 requests per second and reselling access for up to $15,000 a month; LinkedIn's own VP of Legal invoked Proxycurl directly as precedent: "Every one of our previous lawsuits against scrapers has resulted in a judgment prohibiting scraping" [^21]. Enforcement isn't limited to courtrooms, either — starting around March 2025 LinkedIn simply de-listed the company pages and search visibility of Apollo.io, Seamless.ai, Evaboot, and LGM, a platform-level lever that needs no lawsuit at all; Apollo's diversified data sourcing let it shrug the removal off, but vendors more dependent on LinkedIn-native scraping reportedly disappeared from LinkedIn search results outright [^22]. Automation vendor Kennected shows the timescale of the slower version of this: a December 2022 cease-and-desist ("services like Kennected... will not be tolerated") didn't kill it instantly, but it forced a 2024 sale and rebrand, with the LinkedIn-automation product line fully discontinued only in 2025 — a multi-year decay rather than an on/off switch [^23]. None of this is opportunistic, either: LinkedIn's own engineering blog documents a deep-learning anti-abuse system whose first production use case, described in a 2021 post, was specifically detecting logged-in accounts scraping profile data [^24]. Enforcement is not a legal afterthought bolted onto the platform — it is instrumented infrastructure that predates most of these lawsuits.

The open counterpoint is scale. Every enforcement action above targeted an operation with fake-account fleets, six- or seven-figure ARR, or industrial request volumes — Proxycurl, ProAPIs, and the delisted lead-gen vendors were all running at a scale that shows up on LinkedIn's abuse-detection dashboards. Whether a single-founder tool making a few dozen API calls a day against real, cookie-authenticated accounts draws the same response is genuinely untested; LinkedIn has not, to date, sued a tool at that volume, and it's plausible the platform's enforcement math only pencils out above some threshold. That gap is exactly the space Origami AI is operating in, and it's explored further in later sections.

Why it matters here: Origami AI is not choosing whether to build on contested legal ground — that choice was already made, repeatedly, by every predecessor category member, and every one of them eventually paid for it in cash, injunctions, or a forced pivot regardless of how the CFAA question was resolved.

## 04. What LinkedIn actually sanctions

LinkedIn does not treat "signal-based selling" as a monolith to be permitted or banned wholesale — it draws a precise, product-shaped line, and the tactic under review sits on the wrong side of it. Sales Navigator's official Buyer Intent feature aggregates 180+ distinct engagement signals, but the object being measured is a saved, tracked target account — not an open-ended keyword search that surfaces strangers across arbitrary third-party posts platform-wide [^25]. That distinction matters: Buyer Intent tells a rep when a company they already track shows interest in *them*; it does not let a rep discover strangers who typed "looking for a vendor" anywhere on LinkedIn.

Sales Navigator does natively cover part of the adjacent ground. Its "Search for member posts" feature lets a user run keyword search across posts, filterable by content type, author, and date — a legitimately sanctioned analog to hunting for buying-intent phrases in public content [^26]. Third-party guides note the match quality is fuzzy rather than semantic, but the capability itself is first-party and documented.

What is conspicuously absent from that same documentation is any feature to view who liked or reacted to a given post. LinkedIn ships no "post likers" export anywhere in Sales Navigator's sanctioned toolset [^26] — and that gap is exactly the capability third-party scraping tools exist to fill. This is not an oversight; it is the boundary the rest of LinkedIn's platform architecture is built to enforce.

:::kv
- {term: "API reaction/comment scope", def: "own org page admins only"}
- {term: "Mass messaging via API content", def: "explicitly prohibited"}
- {term: "Cross-attribution aggregation", def: "explicitly prohibited"}
:::

LinkedIn's official Community Management API confirms this by construction, not just by omission: `r_organization_social`/`w_organization_social` scopes grant reaction and comment read access only to organizations where the authenticated member holds an admin-tier role on their *own* company page — there is no first-party, credentialed path to reading who liked a stranger's post [^27]. A scrape-then-contact workflow has to go around the API entirely to get that data, and LinkedIn's API Terms of Use directly prohibit the resulting composite: aggregating LinkedIn content with third-party data in ways that break user attributability, and separately, using API-sourced content to power mass or automated messaging (Section 3.1, item 10) [^28]. The Help Center backs this with its own enforcement categories — "inauthentic engagement" (automated liking/commenting) and messaging bots — both grounded in the same User Agreement Section 8.2 clauses [^29].

| Capability | Status |
|---|---|
| Buyer Intent (own page) — 180+ signals | Sanctioned |
| Post keyword search | Sanctioned (native) |
| *Who-liked-this + contact export | Not sanctioned (third-party only) |

The compliance calculus is not purely theoretical, either. In litigation against scraper Proxycurl, LinkedIn told a court its technical defenses detect and restrict scraping accounts "within about a day" [^30]. Treat that figure with the skepticism it deserves: it is LinkedIn's own characterization, offered as litigation testimony rather than an independently audited SLA, and it describes an arms race — new scraping accounts are created faster than restrictions land — not a guarantee that any given account survives a day or a month. What the number does establish, credibly, is that detection is active and non-hypothetical, not merely a clause sitting unused in a terms-of-service document.

That specificity is the point of this section: the "see who liked this post" plus contact-export pattern is not a gray area LinkedIn simply hasn't gotten around to addressing — it targets precisely the capability gap between the *sanctioned* Buyer Intent/post-search tools and the *unsanctioned* reactor-identity data that the Community Management API, the API Terms, and the anti-scraping detection stack were each independently built to keep out of third-party hands.

## 05. Beyond the US: what the law says elsewhere

US law is largely permissive on the cold-email mechanics themselves, but the underlying act of scraping public LinkedIn posts to build a contact database runs into far harder constraints once EU/UK privacy law and state-level computer-crime statutes enter the picture — and a French regulator has already fined a directly comparable tool.

Start with the part most founders get wrong. CAN-SPAM does **not** require prior consent to send commercial email, including B2B email — this is the single most commonly misstated fact about the statute [^31]. What it requires is narrower: accurate headers and subject lines, a clear advertisement disclosure, a valid physical postal address, and a working opt-out mechanism honored within 10 business days [^31]. Origami AI's "signal-based" cold email, mechanically, is not a US legal problem in the way it might feel to a recipient — it's an opt-out regime, not an opt-in one. The exposure that does exist is real: the FTC's 2025 inflation adjustment set the maximum civil penalty at $53,088 per violating email, effective January 17, 2025 [^32].

:::stats
- {label: Kaspr fine, value: "€200K"}
- {label: Kaspr database size, value: "160M", unit: "contacts"}
- {label: CAN-SPAM max penalty, value: "$53,088", unit: "/email"}
:::

Europe inverts the framework. GDPR Article 6(1)(f) does allow "legitimate interest" as a lawful basis for processing personal data without consent, and Recital 47 explicitly names direct marketing as a candidate legitimate interest [^33] — so a scraping-for-outreach tool is not automatically unlawful in the EU either. But it is not a self-certifying exemption: UK ICO guidance, drawing on the CJEU's Rigas balancing test, requires a documented three-part test that weighs whether the data subject would "reasonably expect" their data to be used this way [^34]. A person publicly posting "we're hiring" or "closing our Series A" arguably has a weaker reasonable-expectation claim against enrichment than a target of random scraping — but that's an argument to be documented case-by-case, not a categorical pass. And once a data subject invokes their Article 21 right to object to direct marketing, the balancing test stops mattering entirely: the objection is absolute, no counter-weighing applies, and the tool needs a working, honored opt-out that is separate from and in addition to the upfront legitimate-interest justification [^35].

| Requirement | US CAN-SPAM | EU GDPR |
|---|---|---|
| Consent needed to send | No — opt-out regime | No — legitimate interest permitted |
| Post-send opt-out required | Yes, honored within 10 business days | Yes — Art. 21 right to object, absolute once invoked |
| *Upfront balancing test required | No | Yes — documented 3-part legitimate-interest test |
| Max penalty observed | $53,088 per email | Case-specific; Kaspr precedent: €200,000 |

This isn't hypothetical. On December 5, 2024, the French data protection authority (CNIL) fined Kaspr — a LinkedIn-scraping, contact-enrichment, sales-prospecting tool structurally very close to what Origami AI is described as doing — €200,000 over a database of roughly 160 million contacts, citing Article 6 (lawfulness of processing), Article 5(1)(e) (retention limits), and Articles 12/14 (transparency) [^36]. It is the closest direct enforcement precedent found for this category of tool. The counterpoint matters, though: Kaspr's core violation centered on scraping profiles where the LinkedIn user had restricted visibility to 1st/2nd-degree connections, plus separate retention and transparency failures — not a blanket EU finding that all enrichment from public posts is unlawful. A tool that scraped only fully-public content, retained it for a defined window, and gave clear notice would face a materially different — though still non-trivial — risk profile under the same framework.

The US side isn't purely a federal opt-out story either. Independent of CFAA (Section 03), state computer-crime statutes add exposure LinkedIn has already tested: California Penal Code Section 502(c)(2) criminalizes knowingly accessing a computer or network without permission to take, copy, or use data, and LinkedIn asserted it against hiQ Labs, though courts never definitively resolved whether it reaches purely public-post scraping the way it reaches private systems [^37]. Georgia goes further: its Computer Systems Protection Act creates a standalone "Computer Invasion of Privacy" felony for examining another person's data with knowledge the access is unauthorized, carrying penalties up to $50,000 and **15 years imprisonment** — a criminal exposure layer that exists entirely apart from any federal CFAA analysis [^38].

None of this is academic for a tool sold globally: a US-only compliance read that stops at CAN-SPAM's opt-out floor will misjudge the actual exposure the moment a customer runs the same "signal-based selling" playbook against EU or UK prospects — or triggers a state prosecutor rather than a federal regulator.

## 06. Does the anecdote add up?

Measured against real industry base rates for reply rates, B2B sales-cycle length, and email deliverability physics, the tweet's "7 hours from public LinkedIn post to signed deal" anecdote sits so far outside the normal distribution that it reads as a curated best case rather than a repeatable process — and the tactic's implicit need to scale collides directly with the deliverability constraints that gate cold email at volume.

Start with the reply rate the anecdote implicitly promises. A rigorous, disclosed-sample study — Belkins, 7,530,489 emails sent across 2025 campaigns — found an average reply rate of 0.45% [^39]. A separate 2M+-email dataset (via Apollo/Sales.co) found a 2.09% overall reply rate, of which only 14.1% were genuinely positive — roughly a 0.64% "interested reply" rate, or about one reply worth following up on per 156 emails sent [^39]. Set those against vendor-marketing figures: Instantly's own self-reported platform data, sample size undisclosed, claims a 3.43% average reply rate and 10.7%+ for "elite" senders — roughly 7-8x higher than the disclosed-sample studies [^40]. That gap is not noise; it is what happens when a headline number comes from whoever is selling the tool.

:::bars
- {label: "Belkins (7.5M emails, disclosed)", value: "0.45%", pct: 4}
- {label: "Sales.co interested-only (2M+ emails)", value: "0.64%", pct: 6}
- {label: "Instantly (vendor-reported, undisclosed N)", value: "3.43%", pct: 32}
- {label: "Instantly elite tier (vendor-reported)", value: "10.7%", pct: 100}
:::

Even taking the generous, vendor-reported end of that range, a single reply is not a signed deal. It is the start of a sales cycle — and that cycle has its own well-documented floor. A disclosed-panel study of 939 companies puts the median B2B SaaS sales cycle at roughly 84 days; even the fastest quartile of SMB deals (under $15K ACV, "often single decision-maker, credit-card checkout possible") runs 14-30 days from first contact to close [^41]. That 14-30 day band is itself a percentile, not an observed floor: stage-level minimums for the same fastest-SMB cohort — discovery-to-demo 3-5 days, demo-to-proposal 1-3 days, proposal-to-negotiation 3-7 days, negotiation-to-close 2-5 days — still sum to roughly 9-20 days even when every stage moves at its fastest recorded pace [^41].

:::compare
- {role: CLAIMED, name: "Tweet's anecdote", value: "7 hours", subject: true}
- {role: "FASTEST OBSERVED", name: "SMB 25th percentile", value: "14 days"}
- {role: TYPICAL, name: "B2B SaaS median", value: "84 days"}
:::

For a 7-hour close to be genuine and repeatable rather than a curated outlier, the deal would have had to skip nearly every one of those normal stages — no demo, no negotiation, no procurement — which is consistent with a trivially small, self-serve-priced purchase or a pre-existing warm relationship, not a generalizable cold-outreach tactic. To be fair to the anecdote, a single fast close is not itself statistically impossible: sales-cycle-length distributions are heavily right-skewed by a small number of long enterprise deals, and outliers from either tail — the freak 7-hour close or the freak 400-day slog — are expected to turn up by chance alone in a large enough pool of attempts, no special explanation required. The failure mode is not that the anecdote happened; it's treating a tail event as the operating model.

The tactic's other structural problem shows up only once it is pushed to the volume a repeatable playbook requires: deliverability. Google requires SPF/DKIM/DMARC authentication for any domain sending over 5,000 messages a day to Gmail and caps the tolerated spam-complaint rate at roughly 0.3% (0.1% recommended) [^42]. Practitioner guidance reports that a fresh, unwarmed sending domain can get flagged within about 48 hours once pushed to scaled volume, and the most commonly cited trigger is a sudden day-over-day volume spike — not message content or personalization quality. That distinction matters because deliverability practitioners explicitly rank personalization *last* in their recommended order of operations, behind infrastructure, list quality, relevance, and offer, because inbox placement is governed by sender-behavior signals — volume, velocity, complaint rate, authentication — that are indifferent to how well an email references a scraped LinkedIn post. Personalization can lift the reply rate once a message is already sitting in the inbox; it does nothing to get it past a spam classifier in the first place. These are two separable problems, and the tweet's framing conflates them into one.

Even the tweet's framing of scarcity deserves scrutiny. The claim that "everyone is fighting over the same 210M contacts" implies a single, agreed-upon pool, but Apollo's own site cites larger, inconsistent figures elsewhere — 240M+ on its main product page, 275M+ in its support knowledge base — and competitor databases range from 280M (Lusha) to 1.3-1.7B (Seamless.ai) by vendor self-report [^13]. "Everyone shares the same 210M pool" is a rhetorical simplification, not a documented fact, even though there is a real, separately-documented industry problem with data staleness and duplication across large B2B contact databases generally.

This matters because the tactic is being marketed as a repeatable playbook, and repeatability at volume is exactly where both constraints bite: the sales-cycle base rate says a 7-hour close is a tail event, not a template, and deliverability physics says the moment "signal-based selling" is scaled to the send volume a real pipeline needs, the same authentication, complaint-rate, and warm-up limits that gate any cold-email program take over — regardless of how precisely the message was personalized.

## 07. The bigger wave: AI SDRs, funding, and backlash

Origami AI's signal-based pitch sits inside a much larger, unevenly funded "AI SDR" category that in the past year alone has minted a multi-billion-dollar leader, weathered a viral backlash campaign, and been rocked by a marketing-fabrication scandal at a well-capitalized peer — even as the executives who buy these tools say, in survey after survey, that they still can't prove the software pays for itself.

Capital has concentrated hard at the top. Clay, the category's clear leader, closed a $100M Series C led by CapitalG in August 2025 at a $3.1B valuation [^43]. Below it, funding drops off steeply and unevenly: 11x.ai raised a $50M Series B led by a16z at roughly a $350M valuation in November 2024 [^44], Regie.ai raised a $30M Series B co-led by Scale Venture Partners and Foundation Capital in February 2025, bringing its total to $50.8M [^45], and Artisan AI raised a $25M Series A led by Glade Brook Capital in April 2025 [^46] — its only large disclosed round to date. Lavender, by contrast, hasn't closed a round since an $11M Series A in February 2023, with nothing newer reported through 2026 [^47] — a reminder that "AI SDR" funding momentum describes a handful of breakout winners, not a rising tide lifting the whole category.

:::rank-list
- {label: Clay, value: "$100M Series C / $3.1B val.", pct: 100, rank: 1}
- {label: "11x.ai", value: "$50M Series B / $350M val.", pct: 50, rank: 2}
- {label: Regie.ai, value: "$30M Series B", pct: 30, rank: 3}
- {label: Artisan AI, value: "$25M Series A", pct: 25, rank: 4}
- {label: Lavender, value: "$11M Series A (2023, stale)", pct: 11, rank: 5, highlight: true}
:::

Money hasn't been the only thing separating winners from also-rans; so has how each company markets itself. Artisan ran a "Stop Hiring Humans" billboard campaign across San Francisco that first went viral in November-December 2024 — months before its Series A closed, not concurrent with it — and kept generating backlash into 2025 [^48]. Its CEO has since said on record that the campaign was deliberately designed to provoke outrage and described receiving death threats over it, while named critics called the framing dehumanizing and tone-deaf during a stretch of local tech layoffs [^48]. Regie.ai has staked out the opposite positioning, explicitly branding itself around "keeping humans in the loop" [^45] — a direct rebuttal, intentional or not, to the full-automation framing that made Artisan's billboards so combustible.

A separate and more serious credibility problem hit 11x.ai — a distinct company and a distinct scandal from Artisan's, and the two should not be conflated. A March 2025 TechCrunch investigation found that after its $50M raise, 11x had displayed customer logos — including ZoomInfo and Airtable — from companies that said they were not customers, alongside allegations of inflated ARR and 70-80% ex-employee-estimated churn; its CEO stepped down about six weeks after the story ran [^44].

Set against that backdrop, the buyer-side survey data is unflattering for the category as a whole, not just its most controversial entrants.

:::stats
- {label: "CSOs citing AI-ROI difficulty", value: "31%", note: "Gartner, n=227"}
- {label: "Human-vs-AI deal-credit gap", value: "28pp", note: "Gartner, n=645 buyers"}
:::

Gartner's survey of 227 Chief Sales Officers, fielded August-September 2025, found 31% named difficulty proving the ROI of AI-driven sales tools a top challenge for 2026 [^49] — real skepticism from the executives writing the checks, not merely from critics outside the industry. A separate Gartner survey of 645 B2B buyers found human sales reps were 28 percentage points more likely than generative-AI tools to be credited with advancing a deal toward close [^50] — evidence that the buyer side of the transaction still associates trust and progress with a human rep, even as vendors race to automate that role away.

None of this means the category is collapsing, and the counterpoint matters: Clay's $3.1B round landed after both 11x's scandal and Artisan's backlash had already run their course, so serious capital keeps flowing to the entrant that has, so far, avoided a public credibility hit — a pattern that reads less like a bubble bursting than a sorting process, separating durable products from marketing-driven pretenders. LinkedIn's enforcement wave, discussed in Section 03, hasn't been the extinction event that framing might suggest either: of the well-known LinkedIn automation vendors checked — PhantomBuster, Dux-Soup, Waalaxy, Expandi, Dripify, MeetAlfred, HeyReach — the large majority remain actively operating with live 2026 pricing pages, and LinkedIn's March 2026 action against HeyReach removed its company page and founders' personal profiles without disabling the product for paying customers [^51] — enforcement in practice looks selective by scale and visibility, not comprehensive.

Origami AI is not an outlier in any of this. It is a small, early-stage entrant navigating the same funding scarcity, the same reputational tripwires, and the same buyer skepticism as everyone else racing to automate the sales-development function — without, yet, the capital, the customer base, or the public scandal that would make it a category bellwether in either direction.

## 08. What could break this thesis

Everything above argues the tactic is unoriginal and its legal footing shaky. Three things would weaken that case, and one open question determines how much they matter.

First, LinkedIn's enforcement is demonstrably selective by scale, not comprehensive. The lawsuits and delistings in Section 03 all targeted operations with fake-account fleets, six- to seven-figure revenue, or industrial request volumes. The much larger population of individual-account, rate-limited automation tools — PhantomBuster, Dux-Soup, Waalaxy, and peers — has operated for years despite a written policy with no stated scale exception, and LinkedIn's one 2026 action against a mid-sized player (HeyReach) removed a company page rather than killing the product [^51]. If enforcement genuinely tracks scale rather than the bright-line rule, a small tool making modest daily calls against real, logged-in sessions may simply never cross the threshold that triggers a suit.

Second, the tactic's platform-dependence is empirically demonstrated, not merely argued: the identical "scrape public buying-intent signal, contact fast" mechanic is officially sanctioned and monetized by G2 through its own first-party Buyer Intent Data product [^15]. That shows the underlying idea is not inherently illegitimate — it is LinkedIn's specific contractual posture, not some universal legal principle, that makes this version of it risky.

Third, building on unauthorized platform access has a long history of working out for well-known companies despite the legal gray zone, at least commercially: Airbnb's Craigslist cross-posting bot [^52], Instacart's early unauthorized Trader Joe's cataloging [^54] (a December 2025 Consumer Reports investigation separately found Instacart still uses Target's product data despite Target denying any formal partnership [^55]), and DoorDash's original unauthorized-menu MVP [^56] all sit in the same shape as Origami's LinkedIn tactic — and all three companies went on to IPO. Y Combinator's own canonical growth-hacking doctrine, "Do Things That Don't Scale," never actually endorses legal risk-taking in its text [^53]; the connection to tactics like these was constructed by outside commentators, not YC itself. But the retrospective pattern in its portfolio is real, and it argues against treating gray-zone growth tactics as automatically fatal.

What ties these together, and what remains genuinely unresolved, is Origami's specific technical posture. Unlike Proxycurl and ProAPIs, which built businesses on mass fake-account fleets and data resale, Origami's founder has described a live-fetch, no-storage architecture — querying rather than warehousing [^4]. Whether that distinction matters to LinkedIn's enforcement calculus, which has so far only ever been tested against industrial-scale operations against the much larger population of individual-account tools that keep operating undisturbed [^51], is an open empirical question, not a settled one.

:::position(confidence=medium, horizon="12-18 months")
stance: "Origami AI's live-fetch, no-storage architecture probably reduces its LinkedIn legal exposure relative to Proxycurl's mass-fake-account resale model, but this is untested, not proven safe."
consensus: "Coverage of LinkedIn's 2025 lawsuits treats any LinkedIn-derived sales tool as equally exposed to the Proxycurl/ProAPIs enforcement pattern."
resolves: "Whether LinkedIn brings an enforcement action against a low-volume, single-session scraping tool, rather than an industrial fake-account operation, within the next 12-18 months."
:::

None of this rehabilitates the viral tweet's specific claims — the anecdote is still uncorroborated, the tactic is still not a secret, and the reply-rate and sales-cycle math still don't support "repeatable playbook." But it does mean the honest conclusion isn't "this will get sued into oblivion." It's narrower and less satisfying: a real, modestly effective, already-commoditized tactic, built by a small company whose technical architecture may or may not sit below LinkedIn's enforcement threshold — a bet nobody involved, including Origami AI itself, has actually tested yet.

:::references
- {id: 1, title: "Tweet describing the LinkedIn buying-intent scraping tactic", url: "https://x.com/fin465/status/2090272639839576492", source: "Finn Mallery (@fin465) on X", date: "2026-08-20"}
- {id: 2, title: "Origami — Company profile", url: "https://www.ycombinator.com/companies/origami-2", source: "Y Combinator"}
- {id: 3, title: "Y Combinator's hottest startup Origami Agents secures $2M seed round", url: "https://venturebeat.com/ai/y-combinators-hottest-startup-origami-agents-secures-2m-seed-round-to-supercharge-sales-teams-with-ai", source: "VentureBeat"}
- {id: 4, title: "Origami — Product Hunt launch page", url: "https://www.producthunt.com/products/origami-chat", source: "Product Hunt"}
- {id: 5, title: "Origami AI — homepage", url: "https://origami.chat", source: "Origami AI"}
- {id: 6, title: "Origami AI — Terms of Service", url: "https://origami.chat/terms", source: "Origami AI"}
- {id: 7, title: "Origami AI — Privacy Policy", url: "https://origami.chat/privacy", source: "Origami AI"}
- {id: 8, title: "Finn Mallery — org chart profile", url: "https://theorg.com/org/fizzsocial/org-chart/finn-mallery", source: "TheOrg"}
- {id: 9, title: "Tweet on leaving Stanford after the first day of class", url: "https://x.com/fin465/status/1911516207322439730", source: "Finn Mallery (@fin465) on X", date: "2025-04-13"}
- {id: 10, title: "Tweet with prior growth-figure claims (email/response-rate/MRR)", url: "https://x.com/fin465/status/2039021693050691596", source: "Finn Mallery (@fin465) on X"}
- {id: 11, title: "Sales Intelligence Market — Size, Share & Growth Analysis", url: "https://www.mordorintelligence.com/industry-reports/sales-intelligence-market", source: "Mordor Intelligence", date: "2026-01-22"}
- {id: 12, title: "Top 15 Intent Data Providers Compared 2026", url: "https://www.autobound.ai/blog/top-15-intent-data-providers-compared-2026", source: "Autobound"}
- {id: 13, title: "Apollo — Prospect database product page", url: "https://www.apollo.io/product/prospect", source: "Apollo.io"}
- {id: 14, title: "F5Bot — Reddit/HN/Lobsters keyword alerts", url: "https://f5bot.com", source: "F5Bot"}
- {id: 15, title: "G2 Buyer Intent Data", url: "https://sell.g2.com/buyer-intent-data-g2", source: "G2"}
- {id: 16, title: "Signal-Based Selling — guide", url: "https://www.unifygtm.com/explore/signal-based-selling", source: "Unify GTM"}
- {id: 17, title: "LinkedIn User Agreement", url: "https://www.linkedin.com/legal/user-agreement", source: "LinkedIn"}
- {id: 18, title: "hiQ Labs, Inc. v. LinkedIn Corp. — Ninth Circuit opinion", url: "https://cdn.ca9.uscourts.gov/datastore/opinions/2022/04/18/17-16783.pdf", source: "U.S. Court of Appeals for the Ninth Circuit", date: "2022-04-18"}
- {id: 19, title: "LinkedIn's Data Scraping Battle with hiQ Labs Ends with Proposed Judgment", url: "https://www.privacyworld.blog/2022/12/linkedins-data-scraping-battle-with-hiq-labs-ends-with-proposed-judgment/", source: "Privacy World", date: "2022-12-07"}
- {id: 20, title: "Goodbye Proxycurl", url: "https://nubela.co/blog/goodbye-proxycurl/", source: "Nubela", date: "2025-07-04"}
- {id: 21, title: "LinkedIn sues ProAPIs for using 1M fake accounts to scrape user data", url: "https://www.bleepingcomputer.com/news/legal/linkedin-sues-proapis-for-using-1m-fake-accounts-to-scrape-user-data/", source: "BleepingComputer", date: "2025-10-02"}
- {id: 22, title: "A pair of lead-gen providers have disappeared from LinkedIn", url: "https://martech.org/a-pair-of-lead-gen-providers-have-disappeared-from-linkedin/", source: "MarTech", date: "2025-05-06"}
- {id: 23, title: "Indianapolis-based Kennected hit with cease-and-desist letter from LinkedIn", url: "https://www.ibj.com/articles/indianapolis-based-kennected-hit-with-cease-and-desist-letter-from-linkedin", source: "Indianapolis Business Journal"}
- {id: 24, title: "Using Deep Learning to Detect Abusive Sequences of Member Activity", url: "https://www.linkedin.com/blog/engineering/trust-and-safety/using-deep-learning-to-detect-abusive-sequences-of-member-activi", source: "LinkedIn Engineering Blog"}
- {id: 25, title: "Sales Navigator — Buyer Intent", url: "https://www.linkedin.com/help/sales-navigator/answer/a507435", source: "LinkedIn Help"}
- {id: 26, title: "Sales Navigator — Search for member posts", url: "https://www.linkedin.com/help/sales-navigator/answer/a526104", source: "LinkedIn Help"}
- {id: 27, title: "Community Management API overview", url: "https://learn.microsoft.com/en-us/linkedin/marketing/community-management/community-management-overview", source: "Microsoft / LinkedIn"}
- {id: 28, title: "LinkedIn API Terms of Use", url: "https://www.linkedin.com/legal/l/api-terms-of-use", source: "LinkedIn"}
- {id: 29, title: "Prohibited software and extensions", url: "https://www.linkedin.com/help/linkedin/answer/a1341387", source: "LinkedIn Help"}
- {id: 30, title: "LinkedIn's war against bot scrapers ramps up as AI gets smarter", url: "https://news.bloomberglaw.com/artificial-intelligence/linkedins-war-against-bot-scrapers-ramps-up-as-ai-gets-smarter", source: "Bloomberg Law"}
- {id: 31, title: "CAN-SPAM Act: A Compliance Guide for Business", url: "https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business", source: "Federal Trade Commission"}
- {id: 32, title: "FTC Publishes Inflation-Adjusted Civil Penalty Amounts for 2025", url: "https://www.ftc.gov/news-events/news/press-releases/2025/02/ftc-publishes-inflation-adjusted-civil-penalty-amounts-2025", source: "Federal Trade Commission", date: "2025-02-01"}
- {id: 33, title: "Art. 6 GDPR — Lawfulness of processing", url: "https://gdpr-info.eu/art-6-gdpr/", source: "GDPR.eu"}
- {id: 34, title: "What is the 'legitimate interests' basis?", url: "https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/legitimate-interests/what-is-the-legitimate-interests-basis/", source: "UK Information Commissioner's Office"}
- {id: 35, title: "Art. 21 GDPR — Right to object", url: "https://gdpr-info.eu/art-21-gdpr/", source: "GDPR.eu"}
- {id: 36, title: "Data scraping: French SA fines Kaspr €200,000", url: "https://www.edpb.europa.eu/news/news/2025/data-scraping-french-sa-fined-kaspr-eu200-000_en", source: "European Data Protection Board", date: "2024-12-05"}
- {id: 37, title: "California Penal Code Section 502", url: "https://codes.findlaw.com/ca/penal-code/pen-sect-502/", source: "FindLaw"}
- {id: 38, title: "O.C.G.A. Section 16-9-93 — Computer invasion of privacy", url: "https://law.justia.com/codes/georgia/2021/title-16/chapter-9/article-6/part-1/section-16-9-93/", source: "Justia"}
- {id: 39, title: "B2B Cold Email Response Rates Study", url: "https://belkins.io/blog/cold-email-response-rates", source: "Belkins", date: "2026-06-26"}
- {id: 40, title: "Cold Email Benchmark Report 2026", url: "https://instantly.ai/cold-email-benchmark-report-2026", source: "Instantly.ai", date: "2026-01-12"}
- {id: 41, title: "B2B Sales Cycle Length Benchmarks", url: "https://optif.ai/learn/questions/sales-cycle-length-benchmark/", source: "Optifai"}
- {id: 42, title: "Email sender guidelines", url: "https://support.google.com/a/answer/81126?hl=en", source: "Google Workspace Admin Help", date: "2024-02-01"}
- {id: 43, title: "Clay confirms it closed $100M round at $3.1B valuation", url: "https://techcrunch.com/2025/08/05/clay-confirms-it-closed-100m-round-at-3-1b-valuation", source: "TechCrunch", date: "2025-08-05"}
- {id: 44, title: "a16z- and Benchmark-backed 11x has been claiming customers it doesn't have", url: "https://techcrunch.com/2025/03/24/a16z-and-benchmark-backed-11x-has-been-claiming-customers-it-doesnt-have", source: "TechCrunch", date: "2025-03-24"}
- {id: 45, title: "Regie.ai injects sales enablement with AI, but keeps humans in the loop", url: "https://techcrunch.com/2025/02/26/regie-ai-injects-sales-enablement-with-ai-but-keeps-humans-in-the-loop/", source: "TechCrunch", date: "2025-02-26"}
- {id: 46, title: "Artisan raises $25M to replace repetitive work with AI employees", url: "https://www.forbes.com/sites/dariashunina/2025/04/09/artisan-raises-25m-to-replace-repetitive-work-with-ai-employees/", source: "Forbes", date: "2025-04-09"}
- {id: 47, title: "Lavender lands $13.2M for its AI-powered email marketing engine", url: "https://techcrunch.com/2023/02/02/lavender-lands-13-2m-for-its-ai-powered-email-marketing-engine/", source: "TechCrunch", date: "2023-02-02"}
- {id: 48, title: "The real person behind San Francisco's hated anti-human ad campaign", url: "https://sfstandard.com/2025/04/07/the-real-person-behind-san-franciscos-hated-anti-human-ad-campaign/", source: "The San Francisco Standard", date: "2025-04-07"}
- {id: 49, title: "Gartner Survey Shows 31% of Chief Sales Officers Cited Difficulty Proving ROI of AI-Driven Tools", url: "https://www.gartner.com/en/newsroom/press-releases/2026-05-19-gartner-survey-shows-thirty-one-percent-of-chief-sales-officers-cited-difficulty-proving-roi-of-ai-driven-tools-as-a-top-challenge-for-sales-objectives-in-two-thousand-twenty-si", source: "Gartner", date: "2026-05-19"}
- {id: 50, title: "Gartner Survey Finds Sales Organizations That Provide AI-Enabled Next-Best Actions Are 2.6x More Likely to Achieve Commercial Growth", url: "https://www.gartner.com/en/newsroom/press-releases/2026-05-20-gartner-survey-finds-sales-organizations-that-provide-ai-enabled-next-best-actions-are-two-point-six-times-more-likely-to-achieve-commercial-growth", source: "Gartner", date: "2026-05-20"}
- {id: 51, title: "25 Best LinkedIn Automation Tools 2026", url: "https://lagrowthmachine.com/best-linkedin-automation-tools/", source: "La Growth Machine"}
- {id: 52, title: "Growth Hacker is the New VP Marketing — the Airbnb/Craigslist case study", url: "https://andrewchen.com/how-to-be-a-growth-hacker-an-airbnbcraigslist-case-study/", source: "Andrew Chen"}
- {id: 53, title: "Do Things That Don't Scale", url: "http://paulgraham.com/ds.html", source: "Paul Graham", date: "2013-07-01"}
- {id: 54, title: "Instacart — founding story", url: "https://research.contrary.com/company/instacart1", source: "Contrary Research"}
- {id: 55, title: "Instacart's AI pricing experiment is inflating grocery bills", url: "https://www.consumerreports.org/money/questionable-business-practices/instacart-ai-pricing-experiment-inflating-grocery-bills-a1142182490/", source: "Consumer Reports", date: "2025-12-01"}
- {id: 56, title: "DoorDash trio built company from 'super simple, ugly' web page", url: "https://www.seattletimes.com/business/doordash-trio-built-company-from-super-simple-ugly-web-page/", source: "Seattle Times"}
:::
