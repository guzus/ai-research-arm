---
eyebrow: REPORT · ALPHABET
domain: finance
title: The $43.8 billion everyone calls off-balance-sheet is the one number Alphabet actually put on the balance sheet
deck: Google's TPU lease backstops are marked at $815 million. The genuinely unrecognized layer sits somewhere else, it is roughly twenty times larger, and the capex guide captures none of it.
lede: |
  Between September 2025 and June 2026 Alphabet went from backstopping $6.5 billion
  of other companies' data center payments to backstopping $43.8 billion of them — a
  6.7x increase in three quarters, built to move TPUs against Nvidia. The number is
  real and it comes straight from the 10-Q. But the framing attached to it in most
  coverage is wrong in a specific and instructive way: these backstops are accounted
  for as credit derivatives carried at fair value, which makes them the *least*
  off-balance-sheet obligation in Alphabet's AI stack. The $707 billion of contracted
  supply and the $85.2 billion of leases that have not yet commenced are the ones
  the balance sheet does not see.
stats:
  - {label: Backstop notional, value: $43.8B, note: "at Jun 30, 2026"}
  - {label: Carried liability, value: $815M, note: 1.9% of notional}
  - {label: Uncommenced leases, value: $85.2B, note: commence 2026–2031}
  - {label: Fixed commitments, value: $707.0B, note: contracts over 1 year}
  - {label: 2026 capex guide, value: $195–205B, note: third raise of the year}
---

## 01. The short answer

:::kv
- {term: What the $43.8B is, def: "Gross notional of credit derivatives — Alphabet's backstop of third-party data center payment obligations — as of June 30, 2026, up from $16,940M at December 31, 2025."}
- {term: "Is it off-balance-sheet?", def: "No. Alphabet books these as credit derivatives at fair value. An $815M liability is recorded, versus $69M at year-end 2025."}
- {term: What IS off-balance-sheet, def: "$85.2B of leases not yet commenced, $707.0B of fixed or guaranteed commitments on contracts over one year, $7.6B of energy guarantees, $21.9B of VIE funding commitments."}
- {term: Why Alphabet does it, def: "A guarantee from an AAA-equivalent balance sheet lets a neocloud borrow cheaply; the cheap debt funds a data center that buys Google TPUs and rents them to Anthropic."}
- {term: The real question, def: "Not whether $43.8B is hidden — it is disclosed and partly recognized — but whether $815M is the right mark on a Level 3 exposure concentrated in one customer ecosystem."}
:::

The topic that prompted this piece framed $43.8 billion of TPU lease backstops as
"the off-balance-sheet layer hyperscaler capex guides don't capture."[^1] Half of
that framing survives contact with the filings and half does not. The capex-guide
half is correct and understated. The off-balance-sheet half is, for this particular
number, backwards — and the reason it is backwards turns out to be the most
interesting thing about the disclosure.

## 02. What the filings actually say

Alphabet's Q2 2026 Form 10-Q discloses, inside the derivatives note rather than the
commitments note, a line called *credit derivatives*. The gross notional was
$43,785 million at June 30, 2026, against $16,940 million at December 31, 2025.[^2]
The accompanying language is precise: Alphabet has entered "agreements with certain
third parties to backstop certain payment obligations related to data centers, which
we account for as credit derivatives," and the notional amounts "represent the
maximum potential exposure regarding future payments in the event of specified
default scenarios by underlying parties."[^2] The agreements "carry remaining terms
of up to 15 years and the total potential exposure reduces over time as the
underlying parties fulfill their payment obligations."[^3]

The series is short, because the instrument is new. It did not exist eighteen months
ago.

:::exhibit(num="Exhibit 1", title="Alphabet data center backstops: notional versus carried liability", subtitle="$ billion, quarter-end", source="Alphabet Forms 10-Q, Q3 2025 / Q1 2026 / Q2 2026; Form 10-K FY2025", note="Notional is maximum potential exposure under specified default scenarios, not expected loss.")
:::line-chart(title="Backstop notional vs. recognized liability", subtitle="$ billion", y-unit=$)
x: 2024-12,2025-09,2025-12,2026-03,2026-06
Notional: 0,6.529,16.94,28.436,43.785
Carried liability: 0,0,0.069,0.339,0.815
:::
:::

At December 31, 2024 the notional was zero.[^4] At September 30, 2025 it was
$6,529 million, and the same filing put maximum exposure to loss on the related
unconsolidated VIEs at "$6.5 billion," with the fair value of the credit derivatives
described as "not material."[^4] By March 31, 2026 notional had reached $28,436
million with a carried liability of $339 million, and Alphabet recognized $(148)
million of losses on credit derivatives in other income and expense for the
quarter.[^5] That same Q1 filing disclosed as a subsequent event that in April 2026
the company entered further data center backstops "with notional amounts totaling
approximately $15.3 billion."[^5]

That subsequent-event line does most of the work explaining the headline. $28.4
billion at March plus roughly $15.3 billion signed in April is approximately $43.7
billion — essentially the entire Q2 balance.[^5,6] The "sevenfold increase" that
travelled through the coverage is real measured from September 2025, but it is not
a smooth ramp: it is two discrete quarters of deal signing, most of the second
quarter's growth landing in a single month.

:::note
Figures are as reported at each quarter end. The September 30, 2025 carried liability
is shown as zero because Alphabet described it as not material rather than disclosing
a separate amount.
:::

## 03. Why "off-balance-sheet" is the wrong word here

The phrase "off-balance-sheet" has a specific accounting meaning: an obligation that
exists economically but is not recognized as a liability. Alphabet's backstops fail
that test. They are derivatives, they are marked, and the mark is on the balance
sheet — $815 million of credit derivative liabilities at June 30, 2026, with no
offsetting asset balance.[^2]

This matters because it is a *harder* treatment than the alternative, not an easier
one. A residual value guarantee under ASC 842 need not be recorded at all unless
non-renewal is judged probable.[^7] A credit derivative must be fair-valued every
quarter, and the change runs through earnings — which is exactly why Alphabet booked
a $148 million loss in Q1 2026 on instruments that had not paid out a dollar.[^5]
The company chose, or was required by the structure it wrote, to take the mark.

:::statement(attr="ARA Research")
The scandal-shaped number is the one being marked to market every quarter. The
obligations that genuinely escape recognition are duller, larger, and almost never
make headlines.
:::

Where the criticism does bite is on *how* the mark is set. Alphabet classifies these
credit and equity derivatives within Level 3 of the fair value hierarchy, valued with
probability-weighted expected return models using unobservable inputs including
counterparty credit default rates and the risk-free rate.[^8] Level 3 means the
$815 million rests on management judgment about default probabilities for private,
largely unrated counterparties in a sector fifteen months old. A 1.9%-of-notional
mark is not obviously wrong; it is simply unfalsifiable from outside the company.

The distinction to hold onto: **disclosure is excellent, recognition is partial, and
verification is impossible.** That is a different complaint from "hidden," and a more
durable one. CCIR, which rebuilt the hyperscaler commitment stack from filings,
reaches the same conclusion from the other direction, rejecting the "hidden" framing
in favour of "disclosed but unrecognized."[^9]

## 04. The machine: how a guarantee becomes TPU demand

The economic logic is a distribution subsidy, and it is not subtle. Anthropic wants
compute. Fluidstack leases and develops data centers, fills them with Google TPUs,
and rents the capacity to Anthropic. Google backstops Fluidstack's lease obligations,
which lets the landlord's lenders finance the project at investment-grade-adjacent
rates because an AAA-equivalent balance sheet stands behind the rent.[^10,11] Cheaper
debt makes the project viable; the viable project buys TPUs.

Google is, in other words, running Nvidia's playbook against Nvidia — using balance
sheet to manufacture demand for its own silicon.[^12] The reported economics of the
underlying financing are large: Google's backstops underpin roughly $35 billion of
debt for Anthropic chip capacity, led by Apollo Global Management with Blackstone and
a syndicate of banks.[^13,14]

:::timeline
- {date: 2025-09, headline: "First disclosure", body: "$6,529M of credit derivative notional appears in the Q3 2025 10-Q; fair value described as not material."}
- {date: 2025-10, headline: "TeraWulf Abernathy JV", body: "25-year HPC joint venture covering 168MW in Texas; Google backs roughly $1.3B of lease obligations."}
- {date: 2025-12, headline: "Year-end mark", body: "Notional $16,940M; carried liability $69M. Separate financial guarantees of $5.7B maximum potential payments."}
- {date: 2026-03, headline: "Q1 step-up", body: "Notional $28,436M; carried liability $339M; $(148)M of credit-derivative losses run through OI&E."}
- {date: 2026-04, headline: "The April block", body: "Subsequent-event disclosure of approximately $15.3B of additional backstops — most of the quarter's growth in one month."}
- {date: 2026-06, headline: "River Bend and the $35B financing", body: "Hut 8 signs a 15-year, 245MW triple-net lease with Fluidstack valued near $7B; Bloomberg reports Google backstops underpinning ~$35B of Anthropic chip debt."}
- {date: 2026-06, headline: "Q2 balance", body: "Notional $43,785M against an $815M carried liability; energy guarantees $7.6B; VIE funding commitments $21.9B."}
:::

Site-level reporting lets a portion of the notional be attributed. Hut 8's River Bend
campus in Louisiana carries a 15-year, 245MW triple-net lease with Fluidstack valued
at roughly $7 billion — up to $17.7 billion if all options are exercised — with
Google backstopping about $7 billion of lease payments plus roughly $1 billion of
minimum power bills.[^15,16] TeraWulf's Lake Mariner campus in New York carries
roughly $3.2 billion of Google backstop after an incremental $1.4 billion for the
160MW CB-5 building.[^17] The Abernathy, Texas joint venture adds about $1.3 billion,
a Cipher expansion about $1.73 billion, and a Colorado City, Texas lease about $1.4
billion.[^17,12]

:::exhibit(num="Exhibit 2", title="How much of the $43.8 billion can be publicly attributed", subtitle="$ billion of notional, by named site versus unattributed", source="Alphabet Form 10-Q Q2 2026; site-level figures from Barchart, DatacenterDynamics, TNW", note="Site figures are press-reported and may overlap or use different measurement dates than the 10-Q notional.")
:::donut(center-label="$43.8B")
- {label: "Unattributed in public reporting", value: 29.2}
- {label: "River Bend (Hut 8)", value: 7.0}
- {label: "Lake Mariner (TeraWulf)", value: 3.2}
- {label: "Cipher expansion", value: 1.73}
- {label: "Colorado City, TX", value: 1.4}
- {label: "Abernathy JV (TeraWulf)", value: 1.3}
:::
:::

Roughly two-thirds of the notional cannot be traced to a named project from public
sources, and Alphabet names no counterparty in the filings.[^9] That is the single
most important disclosure gap in this structure — not the size of the number, but the
inability of an outside analyst to test its concentration.

:::callout(kind=warn, label=Concentration)
Every publicly identified backstop traces to the same demand source: Fluidstack-
developed capacity running Google TPUs leased to Anthropic.[^10,13] A credit
derivative book whose reference obligations all depend on one counterparty's ability
to pay rent is not a diversified guarantee portfolio, whatever the number of legal
entities involved.
:::

## 05. The layer the capex guide genuinely does not capture

Alphabet guided 2026 capital expenditure to $195–205 billion on the July 22, 2026
call, its third raise of the year from an opening $175–185 billion, with CFO Anat
Ashkenazi describing a "supply-constrained environment" and warning that 2027 would
increase significantly.[^18,19] Q2 capex was $44.9 billion against $39.1 billion of
operating cash flow, producing free cash flow of negative $5.9 billion — Alphabet's
first negative quarter since 2004.[^20]

That guide is a cash-outflow forecast for property and equipment. It does not include
any of the following, all disclosed at June 30, 2026:

:::rank-list
- {label: "Fixed/guaranteed commitments, contracts >1yr", value: $707.0B, pct: 100}
- {label: "Leases signed, not yet commenced", value: $85.2B, pct: 12}
- {label: "Data center backstops (notional)", value: $43.8B, pct: 6, highlight: true}
- {label: "VIE future funding commitments", value: $21.9B, pct: 3}
- {label: "Energy/power guarantees (max potential)", value: $7.6B, pct: 1}
:::

The $707.0 billion is the number that should have been the headline. Alphabet
discloses that as of June 30, 2026, "expected future fixed or guaranteed commitments"
under contracts with terms greater than one year were $707.0 billion, "the
significant majority of which related to long-term supply agreements," covering
production capacity for technical infrastructure and inventory components, energy
service agreements, and content licensing.[^3] Supply and content obligations run
generally through 2030; energy agreements run two to 26 years, with obligations
through 2054.[^3] One quarter earlier the same line read $232.7 billion.[^5]

:::callout(kind=info, label=Adjudication)
Two different figures circulate for Alphabet's commitments and they are not
interchangeable. The 10-Q's **$707.0 billion** is the fixed-or-guaranteed subset of
contracts with terms over one year.[^3] Bloomberg's widely repeated **$811 billion**
is the broader purchase-commitments-and-other-contractual-obligations total, of which
about $200.7 billion falls due within one year.[^21,22] Both are defensible; quoting
one as if it were the other is not. This article uses $707.0 billion where the
primary filing language applies.
:::

The other components: $85.2 billion of leases primarily related to data centers that
had not yet commenced, scheduled to begin between 2026 and 2031 with non-cancelable
terms of one to 26 years, plus a separate June 2026 short-term lease carrying a
non-cancelable commitment of approximately $5.8 billion.[^2] Financial guarantees
supporting counterparty procurement of long-lead-time power equipment with maximum
potential future payments of $7.6 billion, fair value not material.[^2] And
unconsolidated VIE future funding commitments of $21.9 billion against $1.1 billion
at year-end 2025, including $20.0 billion of future capital funding to a private
company contingent on operational and financial milestones through 2030, structured
as an equity derivative.[^2]

Add the layers and Alphabet's disclosed forward obligations approach $865 billion
against a capex guide of $195–205 billion. The guide is not wrong — it measures a
different thing — but any analysis that treats it as the company's committed AI
spend is understating the commitment by roughly four times.

## 06. Three companies, three accounting treatments

The comparison that actually clarifies Alphabet's position is not against its own
capex guide but against its peers' disclosure. On leases not yet commenced — the
cleanest apples-to-apples measure — Alphabet is small.

:::bars
- {label: "Microsoft (Q ended Jun 30, 2026)", value: $329.1B, pct: 100}
- {label: "Meta (Q2 2026)", value: $279B, pct: 85}
- {label: "Alphabet (Q2 2026)", value: $85.2B, pct: 26}
:::

Microsoft disclosed $329.1 billion of uncommenced leases for the quarter ended June
30, 2026, up from $196.6 billion in the prior period — its largest quarterly jump on
record, with leases scheduled to begin from fiscal 2027 through fiscal 2033.[^23,24]
Meta reported $279 billion, up 53% from $183 billion.[^25] Alphabet's $85.2 billion
is roughly a quarter of Microsoft's.[^2]

The structural point is that economically similar credit support is booked three
different ways across the group.[^9] Alphabet writes credit derivatives and marks
them. Meta writes residual value guarantees: it disclosed data center leases starting
in 2029 with an initial commitment near $12.3 billion alongside a residual value
guarantee with an aggregate threshold near $28 billion, judged not probable and
therefore recorded as no liability at all.[^7] Microsoft took a third route entirely:
rather than guaranteeing anyone's debt it signed more than $33 billion of direct
purchase commitments with neoclouds including Nebius, CoreWeave, Nscale and Lambda —
the Nebius contract alone worth up to $19.4 billion for access to more than 100,000
Nvidia GB300 chips — which are expensed over the contract life rather than carried as
credit exposure.[^26,34]

| Company | Instrument | Recognized liability | Disclosure location |
|---|---|---|---|
| *Alphabet | Credit derivative, fair-valued each quarter | $815M on $43.8B notional | Derivatives note |
| Meta | Residual value guarantee, ~$28B threshold | None — non-renewal not probable | Leases / commitments note |
| Microsoft | Direct purchase commitment, >$33B | None — expensed as incurred | Commitments note |

The three are not the same instrument, and that is precisely the problem. Alphabet
takes counterparty credit risk and marks it. Meta takes residual asset risk and marks
nothing. Microsoft takes no credit risk at all but commits the cash. An investor
screening "off-balance-sheet AI risk" across the group with one metric is comparing
three incompatible accounting policies attached to three genuinely different
economic positions — a comparison that cannot be made from the headline numbers
alone.

:::quote(attr="David Gonzales, Moody's Ratings, to Fortune, February 2026")
They have not received the services to trigger this liability as of this time, but
they will.
:::

Moody's calculated that the five largest US hyperscalers held $969 billion of total
undiscounted future lease commitments at end-2025, of which $662 billion related to
leases not yet commenced — equal to 113% of the group's most recent adjusted
debt.[^7,27] Gonzales's framing is deliberately deflationary: the companies have not
"avoided a liability through structuring," the obligations are simply "yet to be on
the balance sheet."[^7] By July 2026 Moody's put group lease commitments at roughly
$1.2 trillion with more than $820 billion uncommenced, and warned that unprecedented
AI spending threatens credit quality at Amazon, Meta and Alphabet.[^28,29]

## 07. What the exposure is actually worth

The notional is not the loss. This is the point most coverage skips, and the filings
are unusually clear about why.

Upon a default under the backstops, Alphabet "retain[s] the right to assume the
underlying leases for internal use or to sublease to third parties," and may elect to
extinguish the obligation by making a termination payment, in which case obligations
"may be partially offset by equity or cash receipts from counterparties" — inflows
not reflected in the notional amounts.[^3] Alphabet also received equity warrants in
several backstopped counterparties, reportedly a pro forma stake near 14% of TeraWulf
and about 5.4% of Cipher, though the Hut 8 structure came without warrants.[^17]

:::compare
- {role: "MAXIMUM NOTIONAL", name: "Gross exposure, Jun 30 2026", value: $43.8B}
- {role: "CARRIED MARK", name: "Credit derivative liability", value: $815M}
- {role: "RECOVERY ASSET", name: "Assumable TPU-ready capacity", value: "2.4 GW"}
:::

The recovery asset is the crux, and it makes Alphabet structurally different from a
financial guarantor. A bank that writes a credit default swap on a data center
receives, on default, a distressed building it does not want. Alphabet receives
powered, TPU-ready capacity in a market where its own CFO says it is
supply-constrained and where it is simultaneously guiding to $195–205 billion of
capex to build exactly that.[^18,19] Its loss given default is the notional minus the
value of compute capacity it was going to buy anyway.
==press-reported, not in the filings: the backstopped footprint is put at roughly
2.4 GW across about ten projects, none yet complete, so the guarantees are not yet
active== — a figure that traces to The Information via aggregators rather than to any
Alphabet disclosure, and which the filings neither confirm nor contradict.[^10]

That is a genuinely strong argument, and it is the company's own: sources described
Alphabet as having made the commitments on the calculation that TPU revenue would
exceed the obligations incurred.[^1] It is also the argument most exposed to a single
assumption — that a default would be idiosyncratic rather than systemic. If Anthropic
misses milestones because AI compute demand disappoints broadly, Alphabet inherits
2.4 GW of capacity in precisely the state of the world where it no longer wants 2.4
GW of capacity, and where the resale market is bid by nobody. The hedge and the
hazard are perfectly correlated.

:::kv
- {term: Contracted revenue against the risk, def: "Google Cloud backlog rose more than $50B sequentially to about $514B in Q2 2026, with cloud revenue up 82% to $24.8B."}
- {term: Cash capacity, def: "Trailing-twelve-month operating cash flow above $174B; $242.5B of cash and marketable securities at quarter end."}
- {term: Funding shift, def: "Long-term debt rose to $98,165M from $46,547M at year-end 2025 after $20.0B of USD and $31.8B of foreign-currency senior notes."}
- {term: Backstop tail, def: "Remaining terms of up to 15 years, with exposure amortizing as underlying parties make payments."}
:::

Alphabet's capacity to absorb the exposure is not seriously in question. Cloud
backlog reached roughly $514 billion with revenue up 82% to $24.8 billion in Q2
2026,[^19,30] trailing operating cash flow exceeded $174 billion,[^9] and the company
funded the buildout with $51.8 billion of new senior notes plus a June issuance of
Class A stock, Class C stock and mandatory convertible preferred stock raising $49.6
billion of net proceeds.[^2,31] It closed the quarter with $242.5 billion of cash,
cash equivalents and marketable securities.[^2] A maximum exposure amortizing over
fifteen years against that cash generation is a solvency non-event.

## 08. What would break this thesis

Four things would falsify the reading above, and they are worth stating precisely
because two of them are live.

**The mark could be wrong by an order of magnitude and no outsider could tell.** The
$815 million is a Level 3 estimate on unobservable inputs.[^8] If realized default
rates on neocloud lessees run at, say, 10% rather than the low single digits the mark
implies, the liability is understated by billions. Nothing in the disclosure permits
an outside test. Search for published criticism of the specific $815 million mark
returns nothing — which is not evidence the mark is right, only that it has not yet
been contested.

**The "recovery asset" argument fails under correlation.** It holds if a lessee
defaults for company-specific reasons and Alphabet absorbs good capacity cheaply. It
inverts if defaults cluster because AI demand disappoints, which is the same scenario
that destroys the capacity's value. The backstops carry terms up to 15 years against
equipment with a four-to-six-year useful life,[^7] so Alphabet is guaranteeing rent
on buildings for two to three hardware generations beyond the economics that justify
them today.

**The accounting could migrate.** Moody's has said it may make non-standard
adjustments to adjusted debt to capture lease obligations, and its position is
already at odds with S&P — whose October opinion let Meta move Hyperion's cost off
balance sheet via $27.3 billion of debt raised through Beignet Investor, an SPV
jointly owned with Blue Owl Capital.[^28,32] If Moody's capitalizes uncommenced
leases and guarantee exposures, Alphabet's reported leverage changes without any
change in economics.

**The circularity critique may be right.** Critics read the structure as vendor
financing in the late-1990s telecom mould, where equipment makers lent customers the
money to buy the equipment and booked the result as revenue.[^12,33] The pattern is
not confined to Google: Nvidia has reportedly been in talks to backstop as much as
$250 billion for OpenAI compute leases.[^33] The counter is that Google is not
recognizing revenue it financed into existence — TPU deployments generate real cloud
revenue against a $514 billion backlog — but the honest position is that the
telecom analogy cannot be dismissed on structure, only on outcome, and the outcome
is not yet known.

:::callout(kind=danger, label="What to watch")
Three observable triggers, in order of information value: (1) the carried credit
derivative liability as a percentage of notional in the Q3 2026 10-Q — a jump well
above 1.9% is management conceding deterioration; (2) whether Alphabet ever names a
counterparty or discloses concentration; (3) whether Moody's converts its
"non-standard adjustment" warning into an actual adjusted-debt restatement.
:::

:::note
Adversarial check on this article's three load-bearing claims: the $43,785M notional
and the $815M carried liability survived searches for contradicting sources
unbroken. The third — the $707.0 billion commitments figure — did surface a
conflicting number, Bloomberg's $811 billion, which is reconciled in section 05 as a
different and broader line item rather than a discrepancy in either source.[^3,21]
:::

The defensible conclusion is narrower than either the alarmed or the dismissive
version. Alphabet has built a $43.8 billion credit-derivative book to seed TPU
distribution, disclosed it clearly, marked it at $815 million on unverifiable
inputs, and concentrated it in one customer ecosystem. That is a real risk and a
small one relative to Alphabet's cash generation. The larger and less discussed fact
is the $707 billion of fixed contractual commitments and $85.2 billion of uncommenced
leases sitting behind a $195–205 billion capex guide — obligations that are
disclosed, unrecognized, and almost entirely absent from how the market discusses
hyperscaler spending.

:::source
Alphabet Forms 10-Q (Q3 2025, Q1 2026, Q2 2026) and Form 10-K (FY2025); Moody's
Ratings via Fortune, Bisnow and CNBC; CCIR filings reconstruction; Bloomberg;
DatacenterDynamics. ARA analysis. Figures as of June 30, 2026 unless stated.
:::

:::references
- {id: 1, title: "Google Piles On Off-Balance-Sheet Risk to Fuel Its AI Chip Push", url: "https://www.barchart.com/story/news/3595044/google-piles-on-off-balance-sheet-risk-to-fuel-its-ai-chip-push", source: Barchart, date: "2026-08-01"}
- {id: 2, title: "Alphabet Inc. Form 10-Q, quarterly period ended June 30, 2026", url: "https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000071/goog-20260630.htm", source: SEC EDGAR, date: "2026-07-23"}
- {id: 3, title: "Alphabet Inc. Form 10-Q Q2 2026 (investor relations PDF)", url: "https://s206.q4cdn.com/479360582/files/doc_financials/2026/q2/GOOG-10-Q-Q2-2026.pdf", source: Alphabet Investor Relations, date: "2026-07-23"}
- {id: 4, title: "Alphabet Inc. Form 10-Q, period ended September 30, 2025", url: "https://s206.q4cdn.com/479360582/files/doc_financials/2025/q3/GOOG-10-Q-Q3-2025.pdf", source: Alphabet Investor Relations, date: "2025-10-30"}
- {id: 5, title: "Alphabet Inc. Form 10-Q, quarterly period ended March 31, 2026", url: "https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000048/goog-20260331.htm", source: SEC EDGAR, date: "2026-04-23"}
- {id: 6, title: "Breaking Down Big Tech's $1.65 Trillion Hidden Debt", url: "https://ccir.io/research/big-tech-hidden-debt", source: CCIR Research, date: "2026-07-22"}
- {id: 7, title: "Moody's flags $662 billion risk at the heart of the data center build-out by just 5 companies", url: "https://fortune.com/2026/02/25/hyperscaler-risk-off-balance-sheet-662-billion-data-center-commitments-meta-amazon-microsoft-oracle-alphabet/", source: Fortune, date: "2026-02-25"}
- {id: 8, title: "Alphabet Inc. Form 10-K, fiscal year ended December 31, 2025", url: "https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm", source: SEC EDGAR, date: "2026-02-04"}
- {id: 9, title: "CCIR: disclosed but unrecognized — hyperscaler commitments reconstruction", url: "https://ccir.io/research/big-tech-hidden-debt", source: CCIR Research, date: "2026-07-22"}
- {id: 10, title: "Google now guarantees $44bn of other people's rent", url: "https://thenextweb.com/news/google-44-billion-data-centre-lease-guarantees-tpu-anthropic", source: The Next Web, date: "2026-07-31"}
- {id: 11, title: "Investment Grade Credit for NeoCloud Data Center Leases", url: "https://blog.ocolo.io/investment-grade-neocloud-data-center-lease/", source: Ocolo, date: "2026-06-01"}
- {id: 12, title: "Google is using Nvidia's own playbook to break its grip on AI chips", url: "https://thenextweb.com/news/google-nvidia-playbook-tpu-circular-financing-anthropic", source: The Next Web, date: "2026-06-10"}
- {id: 13, title: "Google's Backstops Underpin $35 Billion Chip Deal for Anthropic", url: "https://www.bloomberg.com/news/articles/2026-06-09/google-s-backstops-underpin-35-billion-chip-deal-for-anthropic", source: Bloomberg, date: "2026-06-09"}
- {id: 14, title: "Report: Google is backstopping Anthropic's $35 billion data center deal", url: "https://sherwood.news/tech/report-google-is-backstopping-anthropics-35-billion-data-center-deal/", source: Sherwood News, date: "2026-06-09"}
- {id: 15, title: "Hut 8 signs 245MW capacity deal with Fluidstack as part of multi-gigawatt partnership with Anthropic", url: "https://www.datacenterdynamics.com/en/news/hut-8-signs-245mw-capacity-deal-with-fluidstack-as-part-of-multi-gigawatt-partnership-with-anthropic/", source: DatacenterDynamics, date: "2026-06-17"}
- {id: 16, title: "Hut 8 signs 15-year AI lease backed by Google, stock jumps 25% premarket", url: "https://cryptobriefing.com/bitcoin-mining-partnership-hut8-google-fluidstack/", source: Crypto Briefing, date: "2026-06-17"}
- {id: 17, title: "From neo-cloud to AI utility: FluidStack's category shift", url: "https://electroneconomics.substack.com/p/from-neo-cloud-to-ai-utility-fluidstacks", source: Electron Economics, date: "2026-06-20"}
- {id: 18, title: "Alphabet Raises 2026 Capex Guidance to $195-205B, Cloud Revenue Surges 82%", url: "https://mlq.ai/news/alphabet-raises-2026-capex-guidance-to-195-205b-cloud-revenue-surges-82/", source: MLQ News, date: "2026-07-22"}
- {id: 19, title: "Alphabet earnings takeaways: Q2 revenue beats, GOOGL stock sinks on 2026 capex hike", url: "https://www.cnbc.com/2026/07/22/google-earnings-q2-goog-live-updates.html", source: CNBC, date: "2026-07-22"}
- {id: 20, title: "Google goes cash flow negative for the first time as AI data center buildout increases capex to $44.9 billion in a single quarter", url: "https://www.tomshardware.com/tech-industry/big-tech/alphabet-goes-cash-flow-negative-for-the-first-time-as-ai-capex-doubles-to-44-9-billion-in-a-single-quarter", source: Tom's Hardware, date: "2026-07-23"}
- {id: 21, title: "Alphabet's Future Spending Commitments Soar to $811 Billion", url: "https://www.bloomberg.com/news/articles/2026-07-23/alphabet-s-future-spending-commitments-soar-to-811-billion", source: Bloomberg, date: "2026-07-23"}
- {id: 22, title: "Alphabet's purchase commitments surge past US$800 billion amid AI infrastructure expansion", url: "https://www.digitimes.com/news/a20260724PD232/alphabet-infrastructure-anthropic-inventory-2026.html", source: DIGITIMES, date: "2026-07-24"}
- {id: 23, title: "Microsoft's $329.1bn lease stack is capacity that has not started", url: "https://btw.media/en/microsoft-329-1bn-uncommenced-datacentre-leases", source: BTW Media, date: "2026-07-30"}
- {id: 24, title: "Microsoft Reports Over $130 Billion in New Data Center Leases", url: "https://www.bloomberg.com/news/articles/2026-07-29/microsoft-reports-over-130-billion-in-new-data-center-leases", source: Bloomberg, date: "2026-07-29"}
- {id: 25, title: "Meta reveals $279B in future lease agreements for AI data centers", url: "https://cryptobriefing.com/meta-279b-ai-data-center-leases/", source: Crypto Briefing, date: "2026-07-30"}
- {id: 26, title: "Moody's: Hyperscalers understating risks of short-term AI DC lease agreements", url: "https://www.datacenterdynamics.com/en/news/moodys-hyperscalers-understating-risks-of-short-term-ai-dc-lease-agreements-leaving-investors-in-the-dark/", source: DatacenterDynamics, date: "2026-03-05"}
- {id: 27, title: "Moody's: $662B In Data Center Leases Hidden From Big Tech Balance Sheets Poses Looming Risk", url: "https://www.bisnow.com/national/news/data-center-capital-markets/tech-giants-hiding-662b-data-center-leasing-possibly-far-more-133408", source: Bisnow, date: "2026-02-26"}
- {id: 28, title: "Moody's opinion threatens to derail off-balance-sheet data centre deals", url: "https://www.ifre.com/bonds/2390941/moodys-opinion-threatens-to-derail-off-balance-sheet-data-centre-deals", source: IFR, date: "2026-03-12"}
- {id: 29, title: "Moody's says 'unprecedented' AI spending threatens credit quality of Amazon, Meta, Alphabet and others", url: "https://www.cnbc.com/2026/07/24/moodys-ai-spending-credit-quality-amazon-meta-alphabet.html", source: CNBC, date: "2026-07-24"}
- {id: 30, title: "Alphabet Announces Second Quarter 2026 Results", url: "https://s206.q4cdn.com/479360582/files/doc_financials/2026/q2/2026q2-alphabet-earnings-release.pdf", source: Alphabet Investor Relations, date: "2026-07-22"}
- {id: 31, title: "Alphabet $90 Billion Equity and Equity-Linked Offerings", url: "https://www.davispolk.com/experience/alphabet-90-billion-equity-and-equity-linked-offerings", source: Davis Polk, date: "2026-06-05"}
- {id: 32, title: "Moody's Signals Rethink Of CRE Risk Exposure As Off-Book AI Data Center Leases Top $662B", url: "https://allwork.space/2026/03/moodys-signals-rethink-of-cre-risk-exposure-as-off-book-ai-data-center-leases-top-662b/", source: Allwork.Space, date: "2026-03-10"}
- {id: 33, title: "Nvidia's $750 Billion in Deals Reignite Circular AI Fears", url: "https://www.bloomberg.com/news/articles/2026-07-27/nvidia-s-750-billion-deals-revive-fear-of-ai-circular-financing", source: Bloomberg, date: "2026-07-27"}
- {id: 34, title: "Microsoft inks $33 billion in deals with 'neoclouds' like Nebius, CoreWeave", url: "https://www.tomshardware.com/tech-industry/artificial-intelligence/microsoft-inks-usd33-billion-in-deals-with-neoclouds-like-nebius-coreweave-nebius-deal-alone-secures-100-000-nvidia-gb300-chips-for-internal-use", source: Tom's Hardware, date: "2025-10-03"}
:::
