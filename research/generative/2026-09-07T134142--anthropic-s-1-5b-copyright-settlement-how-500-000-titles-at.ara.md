---
eyebrow: REPORT · AI & COPYRIGHT
title: "The $3,000 book: what Anthropic's $1.5B settlement actually bought, and who gets to keep it"
domain: policy
deck: America's largest copyright settlement is a price, not a precedent — and the rule that decides who collects turns on a single date in August 2022.
lede: |
  On 20 July 2026, Judge Araceli Martínez-Olguín entered final judgment on a
  $1.5 billion class settlement covering 482,460 books that Anthropic had
  downloaded from two pirate libraries. The headline number — "about $3,000
  per book" — has been repeated so often that it now reads as a fact about
  what authors receive. It is not. It is a gross allocation before a 6.8%
  fee award, before an $18.2 million administration reserve, before a
  default 50/50 split with a publisher, and before a dispute process that
  in September 2026 turned out to be the main event. This is an account of
  where the money actually goes, why the reverted-rights rule is the most
  consequential and least-understood provision in the agreement, and why
  the number almost certainly does not travel.
stats:
  - {label: Settlement fund, value: $1.5B, note: "Four installments, 2025–2027"}
  - {label: Works on the list, value: "482,460", note: "From 7M+ pirated copies"}
  - {label: Gross per work, value: "~$3,000", note: "Before fees and splits"}
  - {label: First distribution, value: "$2,203.56", note: "Target: by 15 Nov 2026"}
  - {label: Claims rate, value: 92.77%, note: "As of 14 May 2026"}
---

:::callout(kind=info, label="The short answer")
- **$1.5 billion buys deletion, not permission.** The release covers only past acquisition and training of listed works through 25 August 2025. It grants no licence, releases no output claim, and reaches no work absent from the Works List.[^27,2]
- **~$3,000 is a gross figure, and no individual receives it.** After a $101,561,111 fee award, ~$2.6M in expenses and an $18.22M administration reserve, roughly $1.377 billion reaches the class — and a trade title's award then splits 50/50 with the publisher by default.[^1,3]
- **The reverted-rights rule is binary and back-dated.** An author who is the sole rightsholder takes 100%. But ownership is assessed at the moment of infringement, and the agreement fixes a single "Download Date" of **10 August 2022**.[^2,11,13]
- **The first cheque is ~$2,203.56 per work, targeted for no later than 15 November 2026** — and only for works where every claimant already agrees.[^22,13]
- **It is not precedent.** A district-court settlement binds two parties and decides nothing. Judge Alsup's fair-use order, the only law the case produced, is now permanently unappealable.[^17,29]
:::

## 01. The number everyone quotes is not the number anyone receives

The settlement's arithmetic is a chain of subtractions, and almost every public account stops at the first link. The final approval order records a definitive count of **482,460 works** and describes an estimated per-work payment of "approximately $3,000," which it calls "four times the minimum statutory damages amount" — the $750 ordinary floor of 17 U.S.C. § 504(c)(1).[^1,29] That is the number that entered the press.

What the order also does is deduct. It awarded class counsel **$101,561,111** — "nearly 6.8% percent of the non-reversionary Settlement Fund" — applying a 3.75 multiplier to a $27,082,963 lodestar, and withheld 10% of even that pending a post-distribution accounting.[^1] It approved roughly $2.64 million in litigation expenses, an **$18,220,000** cost reserve for settlement administration on top of the administrator's own ~$15 million estimated expenses, and cut service awards for Andrea Bartz, Charles Graeber and Kirk Wallace Johnson from the $50,000 each requested to $15,000.[^1,9,15]

:::exhibit(num="Exhibit 1", title="Where the $1.5 billion goes", subtitle="Share of the gross settlement fund, per the final approval order", source="Order Granting Final Approval and Judgment, Dkt. 680 (20 July 2026)", note="Excludes escrow interest, which accrues to the class. The administration figure is a court-approved reserve — a ceiling, not an incurred cost.")
:::stack-bar(legend=true)
- {label: Net fund available to claimants, pct: 91.8}
- {label: Attorneys' fees, pct: 6.8}
- {label: Administration reserve, pct: 1.2}
- {label: Expenses and service awards, pct: 0.2}
:::
:::

A caution the coverage has mostly skipped: **no court document states a current "Net Settlement Fund" figure.** The $1,291,350,049.74 net figure published in April 2026 was computed against the *requested* $187.5 million fee, which the court then cut by roughly $86 million.[^16] The ~$1.377 billion above is a reconstruction from the order's own published inputs; the official language remains "approximately $3,000 per work … plus interest earned on the Settlement fund, less the Court-approved costs and fees."[^10] Judge Alsup's own arithmetic at preliminary approval was blunter: "Because 482,460 works were finally identified, not 500,000, the total per work is about $3,100."[^70]

Then comes the split. Under the court-approved class notice, "the payment, by default, will be split 50-50 between authors and publishers," a rule the notice calls the Default Option.[^3] The operative denominator is not the full list but the **449,731 works finally claimed**, per class counsel's 2 September 2026 status report — which also fixes the immediately distributable amount at **$2,203.56 per work**, because Anthropic has funded only about $1.05 billion of the $1.5 billion so far.[^69,23] So the realistic path for a mid-list trade author with one book on the list runs: ~$3,063 eventual gross → roughly **$1,530** after the publisher's half, and about **$1,100** in the first cheque.

:::compare
- {role: LOWEST, name: "Trade author's half, first tranche", value: "~$1,100"}
- {role: HIGHEST, name: "Headline figure, as reported", value: "~$3,000"}
- {role: SUBJECT, name: "Sole rightsholder, first tranche", value: "$2,203.56"}
:::

**What would weaken this.** The per-work figure is a quotient, not a fixed sum, so it moves upward as claims are rejected and as escrow interest accrues — the escrow held $1,074,903,166.44 plus roughly $25 million of interest at the September status report.[^69,23] And unlike most mega-fund settlements, this one is non-reversionary: every dollar the court denied class counsel stays with the class rather than returning to the defendant.[^1] **Why it matters:** the gap between "$3,000 a book" and "about $1,100 in November" is the difference between a headline that reads as vindication and a payment that reads as a nuisance fee.

## 02. How seven million books became 482,460

The class is 6.9% of the corpus, and the reason is not that the other 93% was lawfully acquired.

The record establishes three acquisition events across nineteen months. Anthropic co-founder Ben Mann downloaded the 196,640-book Books3 dataset in early 2021; in June 2021 he "downloaded in this way at least five million copies of books from Library Genesis, or LibGen, which he knew had been pirated"; and in July 2022 Anthropic took at least two million more from the Pirate Library Mirror.[^5,56] The order's aggregate: Anthropic "thereby pirated over seven million copies of books."[^5]

That figure counts *copies*, not titles — the same book appears across all three libraries — which is the first and largest term in the reconciliation.[^56] The rest is eligibility engineering. Judge Alsup wrote the class definition himself and limited it to works "in the versions of LibGen or PiLiMi downloaded by Anthropic," excluding Books3 entirely on the ground that it carried "fewer fields of metadata, less routinely complete files."[^6] He then required an ISBN or ASIN plus US copyright registration within five years of publication and before Anthropic's download, or within three months of publication.[^6,8]

:::exhibit(num="Exhibit 2", title="The eligibility funnel", subtitle="Pirated copies to settled works", source="Order on Fair Use, Dkt. 231; Class Certification Order (17 July 2025); Authors Guild settlement FAQ [^71]", note="The two intermediate figures are Authors Guild estimates, not court findings. Exclusion from the class is not a finding that a work was lawfully acquired.")
:::bars
- {label: "Pirated copies downloaded (LibGen + PiLiMi + Books3)", value: "7,000,000+", pct: 100}
- {label: "Unique works, estimated", value: "~4,000,000", pct: 57}
- {label: "English-language works, estimated", value: "~1,500,000", pct: 21}
- {label: "Works on the final Works List", value: "482,460", pct: 7}
:::
:::

That last filter is the load-bearing one, and it is not about harm. The Authors Guild's own reconstruction of the funnel runs from roughly four million unique works down through non-English and unregistered exclusions to the final list.[^71] 17 U.S.C. § 412 bars statutory damages where registration came after infringement began, unless registration followed within three months of first publication.[^44] Without statutory damages, a plaintiff must prove actual loss — and the provable actual loss from one ingested copy of one book is close to the cover price. The class was therefore drawn along the line of who could credibly threaten a large number, not along the line of who was copied.

The consequence is uncomfortable and worth stating plainly: **every author whose book Anthropic pirated but who registered late, published abroad, or wrote before ISBNs — is outside the settlement, and was compensated nothing.** The final approval order preserves their claims rather than releasing them, which is legally correct and practically inert.[^15]

**What would weaken this.** The Works List was not arbitrary: it was reconstructed from the seven million files Anthropic produced in discovery, matched on two independent tracks — US Copyright Office records and the Bowker/ISBNdb commercial databases — and notice reached 594,945 potential class members covering 482,374 works, or 99.98% of the list.[^12,9] The filters are defensible as remedial design even if they are indefensible as a map of who was harmed. **Why it matters:** any future AI-training class action will be drawn along the same § 412 line, which means the population of authors who can be made whole is structurally much smaller than the population whose books were taken.

## 03. Alsup's split decision, and the arithmetic that forced a settlement

The settlement exists because of a single distinction drawn on 23 June 2025: Judge Alsup held that the *use* was fair and the *acquisition* was not.

On training, the language was not hedged. The order found "the use of the books at issue to train Claude and its precursors was exceedingly transformative and was a fair use under Section 107," and elsewhere calls it "spectacularly so."[^5,7] On the fourth factor, Alsup assumed a training-licensing market could emerge and still held it non-cognizable: such a market "is not one the Copyright Act entitles Authors to exploit."[^5] He analogised the authors' displacement theory to complaining that "training schoolchildren to write well would result in an explosion of competing works."[^5]

He also blessed the destructive scanning. Anthropic hired Tom Turvey, "the former head of partnerships for Google's book-scanning project," in February 2024; vendors "stripped the books from their bindings, cut their pages to size, and scanned the books into digital form — discarding the paper originals."[^5,42] Alsup held that fair use on a narrow, non-training rationale: "The print original was destroyed. One replaced the other."[^5]

And then the piracy. "Creating a permanent, general-purpose library was not itself a fair use excusing Anthropic's piracy," the order says, adding that "there is no carveout, however, from the Copyright Act for AI companies."[^5] The retention was the liability, not the training — Anthropic became wary of training on pirated books "for legal reasons," in the court's summary, and "kept them anyway."[^5,56]

Class certification on 17 July 2025 converted that holding into an existential number.[^6] Statutory damages under § 504(c) run per work, without proof of harm: $750 to $30,000 ordinarily, up to $150,000 for willful infringement.[^43]

:::exhibit(num="Exhibit 3", title="What a book was worth at trial", subtitle="Per-work statutory damages against the settled price", source="17 U.S.C. § 504(c); Order Granting Final Approval, Dkt. 680", note="Statutory damages are set by a jury within the band. The settled figure is gross, before fees and any author/publisher split.")
:::compare
- {role: LOWEST, name: "§ 504(c)(1) statutory minimum", value: "$750"}
- {role: HIGHEST, name: "§ 504(c)(2) willful maximum", value: "$150,000"}
- {role: SUBJECT, name: "Bartz settlement, gross per work", value: "~$3,000"}
:::
:::

Across 482,460 works the willful ceiling is $72.4 billion; across the seven million pirated copies, over a trillion. Anthropic's amici put it in a form the Ninth Circuit could not miss: statutory damages at $150,000 per work "could exceed the entire gross domestic product of each of 171 countries, including Switzerland," and "even a small risk of incurring such extraordinary damages is coercive enough to force almost any defendant to settle."[^31] Anthropic petitioned the Ninth Circuit for Rule 23(f) review on 31 July 2025, with the 1 December trial date left intact; the settlement was noticed within weeks and the petition was never decided on the merits.[^32]

**What would weaken this.** The ceiling is theoretical. A jury sets the figure within the band, compilations count as one work, and the constitutional limits on aggregated statutory damages were never tested here. The commonly repeated "bet-the-company" framing is commentary, not a judicial finding — the closest thing on the record is Judge Martínez-Olguín's observation that "success at trial was not assured, and a loss would have left the Class with no recourse."[^1,31] **Why it matters:** the price was set by an untested damages ceiling, not by any assessment of what a book is worth as training data. That is the single most important thing to know before treating $3,000 as a market rate.

## 04. The reverted-rights rule and the 10 August 2022 hinge

Here is the provision that decides who actually keeps the money, and the reason it is more brittle than its advocates suggest.

The settlement's ownership taxonomy is three-way. A legal owner holds the exclusive reproduction right; a beneficial owner holds a royalty interest; and a **sole owner** "holds all rights to reproduce the work" — a category whose enumerated examples include "an author whose rights in the work have reverted from the publisher."[^11] For non-Education Works the Default Option splits the award 50/50; for Education Works there is no default at all, and claimants must "make a good-faith representation regarding the percentage of recovery they believe they are entitled to receive."[^3] A sole owner takes the full amount.[^11,17]

:::kv
- {term: "Sole rightsholder", def: "Self-published, rights reverted, grant terminated, or a non-exclusive licence — author takes 100%."}
- {term: "Trade or university-press title, rights in force", def: "Default Option: 50/50 author/publisher, applied without producing the contract if both sides elect it."}
- {term: "Education Work", def: "No default. Each claimant states a good-faith percentage — publishers are reported claiming 75–90%."}
- {term: "Co-authors", def: "The author share divides among them; if any co-owner opts out, the whole work leaves the class."}
- {term: "Burden of production", def: "Sits on whichever party departs from the default. Documentation is elective at filing, decisive once contested."}
:::

Now the hinge. A class claim is an accrued cause of action belonging to whoever owned the right *when the infringement happened* — not to whoever owns it today. The Settlement Agreement fixes one date for the whole class: "'Download Date' means August 10, 2022 for purposes of this Agreement."[^2] The Authors Guild's reading, published to its members on 4 September 2026, is that "an author whose rights reverted before August 10, 2022 … should be entitled to 100 percent of the funds for the title," while "if rights in an author's work reverted after August 10, 2022, the publisher may have a valid claim."[^13]

:::statement(attr="ARA Research")
The entire 2022–2026 wave of backlist reversions — much of it driven by authors reclaiming rights precisely because of AI licensing — is worth nothing under this settlement.
:::

That inverts the intuition every author brings to the claim form. Owning a book in 2026 does not entitle you to the 2022 claim on it. And note the asymmetry: ==the Agreement uses 10 August 2022 explicitly as a registration-eligibility date; the ownership-assessment framing is the Authors Guild's gloss, not language I could verify in the Plan of Allocation, which is not machine-readable on the administrator's document index.==[^2,10,13]

The evidentiary regime compounds it. Reversion is self-asserted at filing — the portal invites a claimant to "upload supporting documentation for this work, if you choose to do so" — and only becomes contested when a publisher files a competing claim.[^10] Then a 30-day co-claimant window opens, after which unresolved splits go to Special Master **Theodore K. Cheng**, appointed 25 November 2025 "at the rate of $500 per hour," whose determinations are final and binding without appeal.[^4]

Cheng's fees come from the common fund, not from the disputants — so escalation is free to the claimant and negative-sum for the class.[^4] Do the arithmetic on a contested trade title: the amount actually in dispute is half of ~$3,127, or roughly $1,564. Three hours of special-master time consumes the entire disputed sum, and the class pays for it. Meanwhile funds for the work are frozen for *both* sides until agreement is reached.[^13] For a lone author with one book, the dominant strategy is to accept 50% of something now rather than prove 100% of something later.

**What would weaken this.** The rule is genuinely more author-favourable than the alternative of routing everything through publishing contracts, the Special Master is free at the point of use, and the Authors Guild offers members legal help before escalation.[^13] **Why it matters:** a rule that is pro-author in form and default-favouring in operation transfers real money — and the transfer is invisible in every summary that reports "authors get 100% if rights have reverted."

## 05. First contact: the September 2026 allocation notices

In early September 2026 the administrator sent claimants a reconciliation notice disclosing co-claimants and their claimed percentages, opening a 30-day window to resolve differences.[^13,23] The rule met its class, and the result was not orderly.

Victoria Strauss's Writer Beware, collecting author reports, catalogued more than twenty publishers filing **100% allocation claims on in-print titles** where the default is 50/50 — "odd how many university presses are in this category" — and a comparable set filing 50% or 100% claims on works whose rights had already reverted, spanning most major trade houses.[^19] Authors reported reversions from 1996 through 2017 being claimed: seven titles reverted between 1996 and 2008 drawing a 50% publisher claim, a 2009-reverted title drawing a 100% third-party claim.[^19] The author April Henry publicly asked what HarperCollins was "playing at" after it claimed a book that had reverted to her at least seventeen years earlier.[^20]

:::exhibit(num="Exhibit 4", title="What non-authors are claiming", subtitle="Share of a work's award, as reported by claimants in September 2026", source="Writer Beware (4 Sept 2026); Authors Guild (4 Sept 2026); court-approved class notice", note="Reported figures are self-reported by authors, not an administrator dataset. The 50% row is the settlement's own default for non-Education Works.")
:::rank-list
- {label: "Publishers filing full claims on in-print titles", value: "100%", pct: 100}
- {label: "Educational publishers on textbook titles (reported)", value: "75–90%", pct: 90}
- {label: "Settlement Default Option, non-Education Works", value: "50%", pct: 50, highlight: true}
- {label: "Literary agencies claiming commission", value: "15–25%", pct: 25}
:::
:::

Three failure modes are tangled together here, and they are not equivalent. The first is **administrative error**: Kensington's chief executive indicated the 100% election was not intended, and at least five publishers said they were correcting filings.[^19] Authors Guild chief executive Mary Rasenberger told the *New York Times* it was not "a grab by the publishers."[^20]

The second is a **records failure**, which is what the reverted-rights claims mostly are. A publisher's backlist database records what it once licensed, not what it later gave back; reversion is documented by a private letter, if at all. This is where the rule's design does its damage: one publisher's batch error mis-allocates thousands of works, while one author's omission costs one work. Penguin Random House's own author FAQ explains the 50/50 default and never mentions reversion, out-of-print status or terminated grants — the single fact that would let an author claim the full amount.[^59]

The third is **strategic and lawful**. Educational works were carved out of the default precisely so contract royalty rates could govern, so a publisher asserting a 10% author royalty and claiming 90% is not making an error; it is asserting a position. There is precedent within this very case: in December 2025 Sage emailed textbook authors directing them to claim their royalty rate and warning a different split "could result in a delay," withdrawing only under a Textbook & Academic Authors Association motion to compel a curative notice.[^55]

Two coda details. Literary agencies — thirteen of them, by author reports — filed for 15–25% commissions, though {accent}agents are not rightsholders in the books they sell{/} and the class is defined as copyright owners.[^19] And a firm soliciting as Phoenix Trade Finance began offering claimants "up to 1500 USD per book" in immediate cash — roughly 32% below the November tranche and around half a sole rightsholder's expected total, but close to par for an author entitled only to half.[^19] The offer is priced off the seller's ignorance of their own rights status.

**What would weaken this.** Every number in this section is self-reported to advocacy blogs; Strauss calls her sample "a peek through a small crack in a massive wall."[^19] **The gap that matters most: no source — administrator, class counsel, court filing or press — has published any count of how many works are subject to competing claims.**[^16] The administrator generated the notices and therefore knows. **Why it matters:** that number determines how much of the $1.5 billion moves in November, and its absence from the record means the settlement's central operational risk is currently unmeasurable from outside.

## 06. What Bartz establishes, and what it only appears to

A settlement is a contract. It binds two parties, decides nothing, and makes no law. That distinction is doing more work here than almost any coverage admits.

:::timeline
- {date: 2021-06, headline: "LibGen download", body: "At least five million pirated copies; PiLiMi follows in July 2022."}
- {date: 2025-06-23, headline: "Alsup: training fair, piracy not", body: "Training 'exceedingly transformative'; the pirated central library is not excused."}
- {date: 2025-07-17, headline: "Class certified", body: "LibGen and PiLiMi works with an ISBN/ASIN and timely US registration."}
- {date: 2025-09-08, headline: "Preliminary approval refused", body: "Alsup demands a Works List, claim form and allocation protocol; grants approval on 25 September."}
- {date: 2025-11-25, headline: "Special Master appointed", body: "Theodore K. Cheng, $500/hour, paid from the fund."}
- {date: 2026-03-30, headline: "Claims deadline", body: "Rate reaches 92.77% of listed works by the 14 May fairness hearing."}
- {date: 2026-07-20, headline: "Final approval and judgment", body: "Fees cut to $101.56M; 54 objections overruled; 350 opt-outs."}
- {date: 2026-09-04, headline: "Allocation notices go out", body: "Publishers, agents and third parties surface as co-claimants."}
:::

Start with the release, because it is narrower than the price implies. Class counsel's own description: the settlement "does not release any claims – past or future – based on the output" of AI models, and "does not give Anthropic a license or permission for future AI training."[^27] The class notice puts it more bluntly still — the deal is not "a license to torrent, scan, or train AI models on any copyrighted works, or to create infringing outputs."[^3] So $1.5 billion bought a release for input-side conduct through 25 August 2025, plus an obligation to destroy the LibGen and PiLiMi files within thirty days of judgment and certify it — with an express carve-out preserving the scanned copies, and **no obligation whatsoever to retrain a model or delete a weight.**[^2] An objector's request for deletion of the models was overruled as beyond the settlement's scope.[^1]

Named commentators converge on the same reading. Fortune reported that the settlement "does not establish a legal precedent," but that experts expected it to act as "an anchor figure."[^26] Luke McDonagh of the LSE: "This kind of sum—$3,000 per work—is manageable for a firm valued as highly as Anthropic and the other large AI firms," adding "It may be less so for smaller firms."[^26] The Authors Alliance is blunter: the deal "does not create any precedent that is binding on future courts, who may one day find that such use is non-infringing."[^17]

Two historical comparisons are routinely mangled, and both cut against the settlement.

**Google Books.** The 2009 Amended Settlement Agreement's Author-Publisher Procedures used the same 100%-on-reversion architecture — but with a vintage tier Bartz dropped. For out-of-print unreverted books first published before 1987, "the Registry will pay 65% to the author and 35% to the publisher"; from 1987, 50/50.[^34,35] The rationale, per the court record, was that "most form book publishing contracts in the late 1980s began to include express electronic rights grants to the publisher."[^34] Given a Works List skewed toward older backlist, dropping that tier is a real transfer to publishers. And the common claim that Judge Chin rejected Google Books over its allocation rule is simply false: he cites the Author-Publisher Procedures exactly once, in a neutral recitation of revenue mechanics, and rejected the deal because it "exceeds what the Court may permit under Rule 23," because orphan works are "more suited for Congress," and because it "would give Google a de facto monopoly over unclaimed works."[^33]

**Tasini.** *In re Literary Works in Electronic Databases* is not an author-versus-publisher precedent at all — its Categories A, B and C tracked copyright registration timing, exactly as § 412 requires.[^36] But its procedural lesson is directly on point: the Second Circuit vacated approval because "the interests of class members who hold only Category C claims fundamentally conflict with those of class members who hold Category A and B claims," and held that "only the creation of subclasses, and the advocacy of an attorney representing each subclass, can ensure that the interests of that particular subgroup are in fact adequately represented."[^36] That reasoning tracks closely to the objection Professor Lea Bishop raised against Bartz — that the distribution plan systematically favours publishers over authors.[^18] Judge Martínez-Olguín overruled it. Unlike Tasini, no one appealed the settlement's merits: the only notices of appeal reported are fee-award challenges from firms excluded from the fee, which the settlement carves out of the effective date.[^60]

**What would weaken this.** The anchoring effect is real even if the precedent is not. Aaron Moss's summary is the sharpest on record: "the largest copyright recovery in history sets no precedent—only a price," and for an AI developer "infringement liability isn't so much an existential threat as a line item."[^67] Anthropic is meanwhile being sued repeatedly on the claims Bartz did *not* release — a January 2026 music-publisher action over 21,231 compositions, a March 2026 BMG suit, an August 2026 Round Hill suit, and an August 2026 Sony Music Publishing action, the last of which names Dario Amodei and Benjamin Mann as individual defendants alongside the company.[^51,74] **Why it matters:** by settling, Anthropic removed the only vehicle that would have taken Alsup's fair-use reasoning to the Ninth Circuit. Two days after that order, Judge Chhabria reached the opposite conclusion on the same factor, holding that a properly developed market-dilution record would ordinarily be decisive for plaintiffs on factor four — the theory Alsup had rejected outright.[^30] That split between two judges of one district is now permanently unresolvable through this case.

## 07. Did $1.5 billion deter anything?

The tempting answer is no, and the tempting evidence is a ratio. It is weaker than it looks, and the honest version is more interesting.

At announcement, $1.5 billion was roughly 30% of Anthropic's then-disclosed run-rate: the Series F post, three days earlier, put the company at "$13 billion" raised on a "$183 billion post-money valuation" with run-rate "over $5 billion."[^37] Eleven months later the reported run-rate was above $65 billion.[^40]

:::exhibit(num="Exhibit 5", title="The denominator ran away from the penalty", subtitle="Anthropic annualised run-rate revenue, $ billion", source="Anthropic Series F/G/H announcements; Bloomberg via TechCrunch (17 Aug 2026)", note="Run-rate is annualised from a recent period, not booked revenue. Anthropic is private and publishes no audited financials, so every ratio below rests on company posts and press reports.")
:::line-chart(title="Annualised run-rate revenue", subtitle="$ billion", y-unit=$)
x: 2025-01,2025-08,2025-12,2026-02,2026-05,2026-07
Run-rate: 1,5,9,14,47,65
:::
:::

:::slope(left-label="Aug 2025", right-label="Jul 2026", unit=%)
| Measure | Aug 2025 | Jul 2026 |
|---|---|---|
| Settlement as share of run-rate revenue | 30.0 | 2.3 |
| Settlement as share of post-money valuation | 0.82 | 0.16 |
:::

Anthropic raised $30 billion at a $380 billion post-money in February 2026 and $65 billion at $965 billion in May.[^38,39] Against the later mark the settlement is 0.16% of the valuation and about **eight days of revenue**.

Now the three strongest objections, because each survives.

**The instrument is indexed to growth, not diluted by it.** The Settlement Agreement accelerates both $450 million installments to thirty days after a qualifying financing above $5 billion or an IPO above $10 billion in gross proceeds.[^2] Series G and Series H both clear that trigger. The "denominator grew, so the penalty shrank" framing inverts what the contract does: growth pulls the cash forward. The agreement also contains a $3,000-per-work escalator above a 500,000-work threshold — which never fired, because the final list came in below it, capping the class's upside rather than raising Anthropic's payment.[^2]

**The ratios rest on unaudited figures.** Anthropic is a private company and publishes no audited revenue, loss, cash-burn or litigation-reserve figure; run-rate is an instantaneous annualisation of a recent month, and it is the most flattering denominator available. Both 30% and 2.3% should be read as orders of magnitude, not measurements.

**The licence comparison fails at the corporate level.** It is true that the HarperCollins AI training licence — reported as Microsoft's, though the contract does not name the licensee — paid "a per-title fee of US$2,500" to the author and "an equal amount of US$2,500" to the publisher, $5,000 gross against ~$3,000 settled, for a three-year non-exclusive term with output capped at 200 consecutive words or 5% of the text.[^41,68] But those buy different things. The licence bought usable training data; the settlement bought a release for past conduct plus an obligation to *destroy* the files, for works Anthropic represents were never in any released model's training corpus.[^2] The comparison does survive at the author level, though, and that is the uncomfortable part: a HarperCollins author received $2,500; a Bartz trade author receives roughly $1,530.

What remains, then, is not "the penalty was too small" but something narrower and sharper. Alsup's order separated acquisition from training and held only acquisition unlawful — so the cheapest compliant path is first-sale purchase and destructive scanning, which he blessed.[^5] Anthropic took exactly that path, buying "millions of print books" for "many millions of dollars."[^5,42] ==Widely circulated per-book scanning costs of $10–30 are not supported by the court record or any source I could verify — the order gives no per-book, throughput or vendor figure.==[^5]

**What would weaken this.** Anthropic's non-released exposure is substantial and growing: the January 2026 music-publisher suit covers 21,231 compositions and names Dario Amodei and Benjamin Mann individually, with BMG, Round Hill and Sony Music Publishing actions following through August 2026.[^51,74] At the willful maximum those 21,231 works imply $3.19 billion — more than twice the book settlement — though no complaint pleads that as a demand, lyrics carry live *de minimis* defences, and Anthropic's motion to strike argues the publishers plead "not even a single example of any allegedly infringing output."[^51] **Why it matters:** the deterrent, if there is one, is the tail of unreleased claims and the personal exposure of two named founders, not the $1.5 billion that has already been priced in.

## 08. Why $3,000 does not travel

The per-work price is denominated in a US statutory unit that most of the world does not have.

$3,000 is approximately four times the § 504(c)(1) floor of $750 — a benchmark the final approval order used explicitly.[^1,29] Statutory damages require no proof of loss, and § 412 gates them on timely registration.[^43,44] Strip that architecture out and the number has nothing to stand on.

It is worth sitting with how ordinary the figure is inside that architecture. Aaron Moss, reviewing the empirical work on real-world copyright awards, notes that the single most common statutory award is the $750 floor, that $3,000 is the *second* most common, that more than half of all awards fall below $6,000, and that for printed materials the median is $1,214 per work.[^67] The settlement did not discover the price of a book as training data. It landed on the most ordinary number in American copyright litigation.

| Jurisdiction | Per-work damages schedule | Aggregation mechanism |
|---|---|---|
| *United States* | *§ 504(c): $750–$30,000; $150,000 willful; no proof of loss required*[^43] | *Rule 23(b)(3) opt-out class*[^6] |
| United Kingdom | None. CDPA s.97(2) gives discretionary "additional damages" keyed to flagrancy[^45] | *Lloyd v Google* bars a uniform per-work damages class |
| European Union | None. Enforcement Directive Art. 13: actual prejudice, or a lump sum of "at least" the royalties that would have been due[^64] | Representative Actions Directive is consumer-only |
| Germany | *Lizenzanalogie* — real, but not a per-work schedule[^66] | Collecting-society actions |
| Canada | CAD 500–20,000 per work — a *higher* ceiling than Bartz[^72] | No opt-out damages class of this scale |

The empirical record bears it out. GEMA beat OpenAI at the Landgericht München I in November 2025 and Suno before the same chamber in July 2026, winning findings of infringement plus disclosure orders — but in the OpenAI judgment the only sum actually ordered was **EUR 4,620.70 in pre-litigation legal fees**, with damages granted declaratorily and quantum deferred.[^66] Getty Images abandoned its primary copyright and database-right claims mid-trial in London on a territoriality concession and lost the surviving secondary-infringement claim, the court holding that "the Model itself does not store any of those Copyright Works; the model weights are not themselves an infringing copy."[^48,49] In India, interim relief against OpenAI was declined on 24 July 2026, the court holding that storage of literary works for LLM training would prima facie "fall under Section 52(1)(a)" fair dealing.[^65] The world's most successful non-US AI-copyright claimants have injunctions and disclosure orders; none of them has a per-work price.

Note also what Canada does to the simple version of this argument. Its statutory band runs to **CAD 20,000 per work** for commercial infringement — nearly seven times the Bartz figure — and a 2024 news-publisher action against OpenAI pleads exactly that.[^72] The binding constraint is therefore not the size of the per-work number; it is the ability to multiply one by 482,460 in a single proceeding, which only Rule 23 supplies.

Nor is the US position stable. On 1 September 2026 the Department of Justice filed a Statement of Interest under 28 U.S.C. § 517 in the OpenAI MDL, arguing "it would be problematic—and legally incorrect—to impose broad copyright liability that would generally render training of AI models impermissible without licensing," and calling the *Kadrey* court's fourth-factor application "deeply flawed."[^46] A footnote tells Judge Stein that the Register of Copyrights' contrary view "does not warrant deference," citing *Loper Bright*.[^46] The Copyright Office's Part 3 report on generative-AI training, meanwhile, has sat as a pre-publication draft since 9 May 2025 with no final version.[^50] Register Shira Perlmutter was removed the day after it appeared, won an injunction pending appeal from the D.C. Circuit, and still holds the office while her removal case is litigated — the Office's own leadership page lists her without an acting designation.[^75,46]

There is a real asymmetry buried in the DOJ filing that almost nobody has flagged: **it defends the training stage and says nothing about acquisition.** Acquisition is precisely what Anthropic paid $1.5 billion for. The most significant federal-executive intervention in AI copyright does not undercut the settlement's price; it undercuts a different stage of the pipeline.

Legislatively, nothing moved. The Hawley–Blumenthal bill (S. 2367, introduced 21 July 2025) and the TRAIN Act (S. 2455, 24 July 2025) both predate the settlement and both have sat at committee referral with no recorded action since.[^61,62] The UK went the other way: on 18 March 2026 the government reported that "a broad copyright exception with opt-out is no longer the government's preferred way forward," after a consultation drawing 11,520 responses, and committed to no legislation "until we are confident that they will meet our objectives."[^47] The EU's Digital Omnibus on AI — Regulation (EU) 2026/1744, in force 27 July 2026 — pushed Annex III high-risk obligations back to December 2027 but left Article 53 untouched: general-purpose-AI providers must still publish "a sufficiently detailed summary about the content used for training," and Commission enforcement powers began on 2 August 2026 as scheduled.[^63,58]

**What would weaken this.** Hypothetical-royalty damages under the Enforcement Directive and German Lizenzanalogie can be non-trivial in aggregate, and $3,000 may function as a negotiating anchor in licensing talks regardless of the legal theory behind it. **Why it matters:** a US class settlement priced off an untested statutory ceiling is being read internationally as a market rate for a book. It is not one, and no court outside the United States has been given a mechanism to reach a comparable number.

## 09. What would break this analysis

Four things, in descending order of how much they would cost.

**The disputed-work count.** Everything in Section 05 is anecdote until someone publishes how many of the 449,731 claimed works drew competing claims. If the answer is 2%, the September notices were a media event and the November distribution proceeds essentially intact. If it is 20%, roughly $275 million is frozen behind a single special master billing at $500 an hour, and the settlement's administration becomes the story. The administrator generated the notices and therefore knows; no filing I could reach discloses it.[^69,16]

**The Plan of Allocation.** I could not extract its text, and neither could three independent research passes — the PDF on the administrator's own document index returns an empty body through every route available here.[^10] The 10 August 2022 Download Date is verified in the Settlement Agreement, but its *use* as the ownership-assessment date is the Authors Guild's construction.[^2,13] If the Plan of Allocation says something different — for instance, that ownership is assessed per-library, with a June or July 2021 date for LibGen-only works — then a band of 2021–2022 reversions changes hands and this article's central mechanism needs correcting.

**The deterrence framing.** The best counter is structural, not empirical: the settlement contract accelerates on financing events, so Anthropic's growth pulls the cash forward rather than diluting the burden.[^2] And the revenue ratios that make the settlement look trivial are built on reported run-rate figures with no audited denominator behind them. A reader who rejects both ratios still has the author-level licence comparison — roughly $1,530 settled against $2,500 licensed — which does not depend on any Anthropic financial at all.[^41,68]

**The precedent claim, in reverse.** I have argued the settlement is a price rather than law. The counter is that prices become law by other means: plaintiffs' co-lead Justin Nelson publicly frames the deal as "a precedent requiring AI companies to pay copyright owners," and the anchor is doing work in every negotiation whether or not it binds a court.[^27,26] Against that, fourteen months on, no announced licensing transaction has been priced at or near $3,000 per book, and the purpose-built per-book AI licensing marketplaces still decline to quote a reference price. The doctrinally correct position and the practically operative one have come apart — but the practically operative one has not yet produced a market.

One last note on the shape of the whole thing. The settlement's most-praised feature — its narrowness — is also what makes it a poor template. It resolved the one question on which Anthropic had already lost, at a price set by a damages ceiling nobody tested, for a class drawn along a registration formality, distributed by a rule that hands half the money to publishers by default and asks authors to prove otherwise. It is a competent liquidation of a specific legal exposure. It is not a settlement of the underlying question, and it was never trying to be.

:::source
Court filings via the settlement administrator's document index, CourtListener/RECAP, and the Caselaw Access Project. Claims and allocation figures as of 7 September 2026; run-rate and valuation figures as dated in the text.
:::

:::references
- {id: 1, title: "Order Granting Final Approval of Class Action Settlement; Granting in Part Motion for Attorney's Fees; Judgment (Dkt. 680)", url: "https://assets-us-01.kc-usercontent.com/1eeb16db-4934-006e-40a6-38fa91285ebb/36cce252-a32c-4cbb-a624-31dd8ac9574c/2026-07-20%20Order%20Granting%20Final%20_dckt%20680_0_.pdf", source: "N.D. Cal.", date: "2026-07-20"}
- {id: 2, title: "Class Action Settlement Agreement, Bartz v. Anthropic PBC", url: "https://assets-us-01.kc-usercontent.com/1eeb16db-4934-006e-40a6-38fa91285ebb/d8578720-9fd0-4c27-9c7f-041bac826869/Class%20Action%20Settlement%20Agreement.pdf", source: "Settlement administrator", date: "2025-09-25"}
- {id: 3, title: "Court-Approved Long-Form Class Notice (deadlines second update)", url: "https://assets-us-01.kc-usercontent.com/1eeb16db-4934-006e-40a6-38fa91285ebb/34a80bf3-70fc-414a-8a4c-daa81b5a0caf/ANT%20-%20Long-Form%20Notice_DeadlinesSecondUpdate%201.27.26.pdf", source: "Settlement administrator", date: "2026-01-27"}
- {id: 4, title: "Order Approving Stipulation Referring Claimant Disputes to Special Master Theodore K. Cheng (Dkt. 501)", url: "https://assets-us-01.kc-usercontent.com/1eeb16db-4934-006e-40a6-38fa91285ebb/255f15f4-cbba-466b-a868-75ba3853db93/2025-11-25%20Order%20Approving%20And%20_dckt%20501_0_.pdf", source: "N.D. Cal.", date: "2025-11-25"}
- {id: 5, title: "Order on Fair Use (Dkt. 231), Bartz v. Anthropic PBC", url: "https://copyrightalliance.org/wp-content/uploads/2025/06/Bartz-v.-Anthropic-Order.pdf", source: "N.D. Cal. (Alsup, J.)", date: "2025-06-23"}
- {id: 6, title: "Order Granting Class Certification on the Pirated-Books Class", url: "https://chatgptiseatingtheworld.com/wp-content/uploads/2025/07/Class-Certification-Order-on-pirated-books-class-Bartz-v.-Anthropic-July-17-20250-.pdf", source: "N.D. Cal.", date: "2025-07-17"}
- {id: 7, title: "Order on Fair Use, RECAP copy (gov.uscourts.cand.434709.231.0)", url: "https://storage.courtlistener.com/recap/gov.uscourts.cand.434709/gov.uscourts.cand.434709.231.0.pdf", source: "CourtListener/RECAP", date: "2025-06-23"}
- {id: 8, title: "Bartz v. Anthropic PBC — order clarifying the class definition", url: "https://case-law.vlex.com/vid/bartz-v-anthropic-pbc-1093500941", source: "vLex", date: "2025-10-17"}
- {id: 9, title: "Order Approving Settlement (mirror)", url: "https://cdn.arstechnica.net/wp-content/uploads/2026/07/Bartz-v-Anthropic-Order-Approving-Settlement-7-20-26.pdf", source: "Ars Technica mirror", date: "2026-07-20"}
- {id: 10, title: "Official settlement website and allocation-portal instructions", url: "https://www.anthropiccopyrightsettlement.com/allocation-portal-instructions", source: "JND Legal Administration", date: "2026-09-07"}
- {id: 11, title: "Claim form — ownership categories (legal, beneficial and sole owners)", url: "https://www.anthropiccopyrightsettlement.com/claim-form", source: "JND Legal Administration", date: "2026-09-07"}
- {id: 12, title: "Search tips — how the Works List was constructed", url: "https://www.anthropiccopyrightsettlement.com/search-tips", source: "JND Legal Administration", date: "2026-09-07"}
- {id: 13, title: "Important information regarding Anthropic copyright settlement claim notices", url: "https://authorsguild.org/news/important-information-regarding-anthropic-copyright-settlement-claim-notices/", source: "Authors Guild", date: "2026-09-04"}
- {id: 14, title: "What authors need to know about the Anthropic settlement", url: "https://authorsguild.org/advocacy/artificial-intelligence/what-authors-need-to-know-about-the-anthropic-settlement/", source: "Authors Guild", date: "2026-09-04"}
- {id: 15, title: "Court grants final approval of Anthropic copyright settlement", url: "https://authorsguild.org/news/court-grants-final-approval-anthropic-copyright-settlement/", source: "Authors Guild", date: "2026-07-21"}
- {id: 16, title: "Anthropic settlement update: 91 percent of books claimed", url: "https://authorsguild.org/news/anthropic-settlement-update-91-percent-of-books-claimed/", source: "Authors Guild", date: "2026-04-17"}
- {id: 17, title: "Bartz v. Anthropic settlement FAQ", url: "https://www.authorsalliance.org/resources/generative-ai/bartz-v-anthropic-settlement-faq/", source: "Authors Alliance", date: "2026-09-07"}
- {id: 18, title: "Settlement update: new fairness-hearing date and unsealed objections", url: "https://www.authorsalliance.org/2026/04/14/bartz-v-anthropic-settlement-update-new-date-and-time-for-the-fairness-hearing-you-can-join-online-and-unsealed-objections/", source: "Authors Alliance", date: "2026-04-14"}
- {id: 19, title: "Anthropic copyright settlement: publishers are making incorrect claims on authors' payouts", url: "https://writerbeware.blog/2026/09/04/anthropic-copyright-settlement-publishers-are-making-incorrect-claims-on-authors-payouts/", source: "Writer Beware (Victoria Strauss)", date: "2026-09-04"}
- {id: 20, title: "Authors push back as publishers and agents seek share of Anthropic settlement", url: "https://techcrunch.com/2026/09/06/authors-push-back-as-publishers-and-agents-seek-share-of-anthropic-settlement/", source: "TechCrunch", date: "2026-09-06"}
- {id: 21, title: "Anthropic settlement FAQ", url: "https://sfwa.org/anthropic-faq/", source: "SFWA", date: "2026-05-20"}
- {id: 22, title: "Anthropic settlement tracker", url: "https://www.taaonline.net/anthropic-settlement", source: "Textbook & Academic Authors Association", date: "2026-09-04"}
- {id: 23, title: "Widespread problems as authors receive Anthropic settlement notices", url: "https://lunch.publishersmarketplace.com/2026/09/widespread-problems-as-authors-receive-anthropic-settlement-notices/", source: "Publishers Lunch", date: "2026-09-04"}
- {id: 24, title: "Anthropic settlement appears to cruise through its final fairness hearing", url: "https://publishingperspectives.com/2026/05/anthropic-settlement-appears-to-cruise-through-its-final-fairness-hearing/", source: "Publishing Perspectives", date: "2026-05-14"}
- {id: 25, title: "Judge delays preliminary approval in Anthropic copyright settlement", url: "https://www.publishersweekly.com/pw/by-topic/digital/copyright/article/98552-judge-delays-preliminary-approval-in-anthropic-copyright-settlement.html", source: "Publishers Weekly", date: "2025-09-09"}
- {id: 26, title: "Anthropic reaches $1.5 billion settlement with authors in landmark copyright case", url: "https://fortune.com/2025/09/05/anthropic-reaches-1-5-billion-settlement-with-authors-in-landmark-copyright-case/", source: "Fortune", date: "2025-09-05"}
- {id: 27, title: "Susman Godfrey secures $1.5 billion settlement in landmark AI piracy case", url: "https://www.susmangodfrey.com/wins/susman-godfrey-secures-1-5-billion-settlement-in-landmark-ai-piracy-case/", source: "Susman Godfrey (class counsel)", date: "2025-09-05"}
- {id: 28, title: "The Bartz v. Anthropic settlement: understanding America's largest copyright settlement", url: "https://legalblogs.wolterskluwer.com/copyright-blog/the-bartz-v-anthropic-settlement-understanding-americas-largest-copyright-settlement/", source: "Kluwer Copyright Blog", date: "2025-11-10"}
- {id: 29, title: "The Bartz/Anthropic settlement is still the only per-work number we have", url: "https://ipkitten.blogspot.com/2026/08/the-bartzanthropic-settlement-is-still.html", source: "The IPKat", date: "2026-08-11"}
- {id: 30, title: "Kadrey v. Meta Platforms, order on fair use", url: "https://caselaw.findlaw.com/court/us-dis-crt-n-d-cal/117422847.html", source: "N.D. Cal. (Chhabria, J.)", date: "2025-06-25"}
- {id: 31, title: "Brief of TechNet, CCIA et al. as amici curiae, Bartz v. Anthropic (9th Cir.)", url: "https://ccianet.org/wp-content/uploads/2025/08/TechNet-CCIA-et-al.-Amicus-Bartz-v.-Anthropic-CA9.pdf", source: "CCIA", date: "2025-08-07"}
- {id: 32, title: "Anthropic files Rule 23(f) petition to appeal class certification", url: "https://chatgptiseatingtheworld.com/2025/08/05/anthropic-filed-rule-23f-petition-to-appeal-judge-alsups-class-certification-in-9th-circuit/", source: "ChatGPT Is Eating the World", date: "2025-08-05"}
- {id: 33, title: "Authors Guild v. Google, Inc., 770 F. Supp. 2d 666 (S.D.N.Y.)", url: "https://www.courtlistener.com/opinion/2476173/authors-guild-v-google-inc/", source: "CourtListener (Chin, J.)", date: "2011-03-22"}
- {id: 34, title: "Court exhibit quoting Author-Publisher Procedures § 6.2(c), Authors Guild v. Google (2d Cir. record 13-4829)", url: "https://cases.justia.com/federal/appellate-courts/ca2/13-4829/45/2.pdf", source: "Justia / 2d Cir. record", date: "2013-08-26"}
- {id: 35, title: "How the Authors Guild v. Google settlement will work", url: "https://authorsguild.org/news/how-the-authors-guild-v-google-settlement-will-work/", source: "Authors Guild", date: "2008-12-04"}
- {id: 36, title: "In re Literary Works in Electronic Databases Copyright Litigation, 654 F.3d 242 (2d Cir.)", url: "https://static.case.law/f3d/654/html/0242-01.html", source: "Caselaw Access Project", date: "2011-08-17"}
- {id: 37, title: "Anthropic raises Series F at $183B post-money valuation", url: "https://www.anthropic.com/news/anthropic-raises-series-f-at-usd183b-post-money-valuation", source: "Anthropic", date: "2025-09-02"}
- {id: 38, title: "Anthropic raises $30 billion Series G at $380 billion post-money valuation", url: "https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation", source: "Anthropic", date: "2026-02-12"}
- {id: 39, title: "Anthropic Series H", url: "https://www.anthropic.com/news/series-h", source: "Anthropic", date: "2026-05-28"}
- {id: 40, title: "Anthropic's annualized revenue surges to $65B", url: "https://techcrunch.com/2026/08/17/anthropics-annualized-revenue-surges-to-65b/", source: "TechCrunch", date: "2026-08-17"}
- {id: 41, title: "Why I took the $2,500 check to license my book for AI", url: "https://bernoff.com/blog/why-i-took-the-2500-check-to-license-my-book-for-ai", source: "Josh Bernoff", date: "2025-04-15"}
- {id: 42, title: "Anthropic 'destructively' scanned millions of books to build Claude", url: "https://www.washingtonpost.com/technology/2026/01/27/anthropic-ai-scan-destroy-books/", source: "Washington Post", date: "2026-01-27"}
- {id: 43, title: "17 U.S.C. § 504 — Remedies for infringement: damages and profits", url: "https://www.law.cornell.edu/uscode/text/17/504", source: "Cornell LII"}
- {id: 44, title: "17 U.S.C. § 412 — Registration as prerequisite to certain remedies", url: "https://www.law.cornell.edu/uscode/text/17/412", source: "Cornell LII"}
- {id: 45, title: "Copyright, Designs and Patents Act 1988, s.97 — provisions as to damages", url: "https://www.legislation.gov.uk/ukpga/1988/48/section/97", source: "legislation.gov.uk"}
- {id: 46, title: "Statement of Interest of the United States on Fair Use, In re OpenAI Copyright Infringement Litigation (MDL 25-md-3143)", url: "https://chatgptiseatingtheworld.com/wp-content/uploads/2026/09/Statement-of-Interest-of-the-United-States-on-Fair-Use-Sept-1-2026-gov.uscourts.nysd_.640396.1682.0.pdf", source: "US Department of Justice", date: "2026-09-01"}
- {id: 47, title: "Report on copyright and artificial intelligence", url: "https://www.gov.uk/government/publications/report-and-impact-assessment-on-copyright-and-artificial-intelligence/report-on-copyright-and-artificial-intelligence", source: "UK Government (DSIT/DCMS/IPO)", date: "2026-03-18"}
- {id: 48, title: "Getty Images (US) Inc v Stability AI Ltd [2025] EWHC 2863 (Ch)", url: "https://www.judiciary.uk/judgments/getty-images-v-stability-ai/", source: "England and Wales High Court", date: "2025-11-04"}
- {id: 49, title: "Getty Images v Stability AI: English High Court rejects secondary copyright claim", url: "https://www.lw.com/en/insights/getty-images-v-stability-ai-english-high-court-rejects-secondary-copyright-claim", source: "Latham & Watkins", date: "2025-11-06"}
- {id: 50, title: "Copyright and artificial intelligence — reports and status", url: "https://www.copyright.gov/ai/", source: "US Copyright Office", date: "2026-09-07"}
- {id: 51, title: "Concord Music Group, Inc. v. Anthropic PBC, No. 5:26-cv-00880 (N.D. Cal.) — docket", url: "https://www.courtlistener.com/docket/72199828/concord-music-group-inc-v-anthropic-pbc/", source: "CourtListener", date: "2026-01-28"}
- {id: 52, title: "Anthropic's landmark $1.5B copyright settlement is approved", url: "https://techcrunch.com/2026/07/20/anthropics-landmark-1-5b-copyright-settlement-is-approved/", source: "TechCrunch", date: "2026-07-20"}
- {id: 53, title: "Statement on proposed settlement of $1.5 billion in Bartz v. Anthropic class action suit", url: "https://publishers.org/news/statement-on-proposed-settlement-of-1-5-billion-in-bartz-v-anthropic-class-action-suit/", source: "Association of American Publishers", date: "2025-09-05"}
- {id: 54, title: "Princeton University Press statement on the Bartz v. Anthropic settlement", url: "https://press.princeton.edu/news/bartz-v-anthropic", source: "Princeton University Press", date: "2025-09-08"}
- {id: 55, title: "Sage textbook authors settle dispute over Anthropic settlement guidance", url: "https://publishingperspectives.com/2026/01/sage-textbook-authors-settle-dispute-over-anthropic-settlement-guidance/", source: "Publishing Perspectives", date: "2026-01-20"}
- {id: 56, title: "Bartz v. Anthropic PBC — Order on Fair Use, full opinion text", url: "https://case-law.vlex.com/vid/bartz-v-anthropic-pbc-1094702944", source: "vLex", date: "2025-06-23"}
- {id: 57, title: "Victory for GEMA in Germany against OpenAI", url: "https://www.technollama.co.uk/victory-for-gema-in-germany-against-openai", source: "TechnoLlama (Andres Guadamuz)", date: "2025-11-22"}
- {id: 58, title: "EU AI Act Article 53 — obligations for providers of general-purpose AI models", url: "https://artificialintelligenceact.eu/article/53/", source: "EU AI Act explorer", date: "2026-08-02"}
- {id: 59, title: "Bartz v. Anthropic copyright settlement — FAQ for authors", url: "https://www.penguinrandomhouse.com/bartz-v-anthropic-copyright-settlement-faq-for-authors/", source: "Penguin Random House", date: "2026-01-12"}
- {id: 60, title: "Publishers' coordination counsel files notice of appeal in Bartz of fee award", url: "https://chatgptiseatingtheworld.com/2026/08/18/update-publishers-coordination-counsel-files-notice-of-appeal-in-bartz-of-fee-award-does-not-affect-payout-schedule/", source: "ChatGPT Is Eating the World", date: "2026-08-18"}
- {id: 61, title: "S. 2367, AI Accountability and Personal Data Protection Act — bill status", url: "https://www.govinfo.gov/bulkdata/BILLSTATUS/119/s/BILLSTATUS-119s2367.xml", source: "GovInfo (119th Congress)", date: "2025-07-21"}
- {id: 62, title: "S. 2455, TRAIN Act — bill status", url: "https://www.govinfo.gov/bulkdata/BILLSTATUS/119/s/BILLSTATUS-119s2455.xml", source: "GovInfo (119th Congress)", date: "2025-07-24"}
- {id: 63, title: "Regulation (EU) 2026/1744 of 8 July 2026 (Digital Omnibus on AI)", url: "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202601744", source: "EUR-Lex, Official Journal", date: "2026-07-24"}
- {id: 64, title: "Directive 2004/48/EC on the enforcement of intellectual property rights, Article 13", url: "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32004L0048R(01)", source: "EUR-Lex", date: "2004-04-29"}
- {id: 65, title: "OpenAI did not violate copyright by using ANI news to train ChatGPT: Delhi High Court declines interim relief", url: "https://www.barandbench.com/news/litigation/openai-did-not-violate-copyright-laws-by-using-ani-news-to-train-chatgpt-delhi-high-court-declines-interim-relief", source: "Bar and Bench", date: "2026-07-24"}
- {id: 66, title: "GEMA v. OpenAI, Endurteil, LG München I, 42 O 14139/24", url: "https://aifray.com/wp-content/uploads/2025/11/42-O-14139-24-Endurteil.pdf", source: "Landgericht München I", date: "2025-11-11"}
- {id: 67, title: "The Anthropic settlement: the largest copyright recovery in history sets no precedent, only a price", url: "https://copyrightlately.com/anthropic-settlement/", source: "Copyright Lately (Aaron Moss)", date: "2025-09-08"}
- {id: 68, title: "Agents, authors question HarperCollins AI deal", url: "https://www.publishersweekly.com/pw/by-topic/industry-news/publisher-news/article/96533-agents-authors-question-harpercollins-ai-deal.html", source: "Publishers Weekly", date: "2024-11-19"}
- {id: 69, title: "Class counsel status report on claims and distribution (Dkt. 688)", url: "https://storage.courtlistener.com/recap/gov.uscourts.cand.434709/gov.uscourts.cand.434709.688.0.pdf", source: "N.D. Cal. via CourtListener/RECAP", date: "2026-09-02"}
- {id: 70, title: "Order Granting Preliminary Approval of Class Action Settlement (Dkt. 437)", url: "https://storage.courtlistener.com/recap/gov.uscourts.cand.434709/gov.uscourts.cand.434709.437.0.pdf", source: "N.D. Cal. (Alsup, J.)", date: "2025-09-25"}
- {id: 71, title: "Bartz v. Anthropic settlement FAQs", url: "https://authorsguild.org/advocacy/artificial-intelligence/anthropic-settlement-faq/", source: "Authors Guild", date: "2026-09-07"}
- {id: 72, title: "Copyright Act (Canada), s. 38.1 — statutory damages", url: "https://laws-lois.justice.gc.ca/eng/acts/C-42/section-38.1.html", source: "Justice Laws Website, Canada"}
- {id: 74, title: "Sony Music Publishing (US) LLC v. Anthropic PBC, No. 5:26-cv-09217 (N.D. Cal.) — docket", url: "https://www.courtlistener.com/docket/74720572/sony-music-publishing-us-llc-v-anthropic-pbc/", source: "CourtListener", date: "2026-08-28"}
- {id: 75, title: "U.S. Copyright Office leadership", url: "https://www.copyright.gov/about/leadership/", source: "US Copyright Office", date: "2026-09-07"}
:::
