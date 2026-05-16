---
eyebrow: AI INFRASTRUCTURE · GPU CLOUDS · UNIT ECONOMICS
title: 'Renting the AI Stack: CoreWeave''s $99B Backlog, $25B Debt, and the Customer-Concentration Question'
deck: A first-principles audit of CoreWeave's GPU-as-a-service economics — what the contracts actually
  say, what the SPVs actually pledge, and where the model breaks if any of three counterparties blinks.
lede: 'CoreWeave (NASDAQ: CRWV) closed Q1 2026 with **$98.8 billion of contracted backlog**, [^1]**$25.1
  billion of on-balance-sheet debt**,[^1] roughly **$60 billion of off-balance-sheet operating-lease commitments
  not yet commenced**,[^1] and a single "Customer A" — Microsoft — that supplied 67% of FY2025 revenue
  but only 45% of Q1 2026 revenue as OpenAI and Meta took its place.[^1,2] The story underwriting the
  equity is that a 5-year, 98%-take-or-pay contract book has been bootstrapped into the first investment-grade-rated
  GPU-backed loan in history — the $8.5B DDTL 4.0 facility, rated **A3 by Moody''s** at the SPV level
  versus Ba3 at the parent.[^57] The story breaking the equity is that ~22% of the backlog sits with OpenAI
  (private, ~$25B/yr operating burn), the remaining 80% sits with three counterparties total, and a Core
  Scientific acquisition that would have brought 1.3 GW of owned power onto the balance sheet was rejected
  by CORZ shareholders 91.5% to 8.5%.[^11] What follows is the audit.'
---

:::kv
- term: Q1 2026 revenue
  def: $2,078M, +112% YoY[^1]
- term: Contracted backlog (RPO)
  def: $98.8B; +$38B in one quarter[^1]
- term: Top-3 customers
  def: Microsoft + OpenAI + Meta ≈ 80%+ of backlog[^2]
- term: Effective total obligations
  def: $25.1B debt + $10.1B leases (commenced) + ~$60B leases not yet commenced[^1]
- term: DDTL 4.0 ($8.5B)
  def: 'First IG-rated GPU-backed debt: Moody''s A3 / DBRS A-low[^57]'
- term: Nvidia stake
  def: ~13% post-PIPE; $6.3B residual-capacity backstop through 2032[^55,56]
:::

## 1. The $99B Backlog and the Rotating Customer Mix

**Section thesis:** CoreWeave's $98.8B contracted backlog is genuinely real and genuinely growing — but the apparent "diversification" away from Microsoft is a rotation of anchor tenants, not a broadening of the customer base. The Top-3 still consume roughly 80%+ of revenue; the names on the marquee simply changed.

As of March 31, 2026, CoreWeave reported $98.8 billion of unsatisfied remaining performance obligations (RPO), of which 36% is scheduled to convert to revenue in the first 24 months, 39% in months 25–48, and the residual tail across months 49–84.[^1] That backlog has compounded with extraordinary velocity: from $15.1B at year-end 2024 to $50.0B at the end of Q3 2025, $60.7B at year-end 2025, and $98.8B by Q1 2026 close — roughly $38B of net contracted additions in a single quarter.[^1,2] Management characterizes 98% of FY2025 revenue as flowing from take-or-pay committed contracts, the structural feature that allows the company to underwrite multi-billion-dollar debt facilities against the forward book.[^2]

"Customer A" — disclosed in industry reporting and consistent with the partnership architecture as Microsoft — represented 67% of FY2025 revenue, up from 62% in FY2024 and 35% in FY2023.[^2] In Q1 2026 that share collapsed to 45%, down from 72% in the year-ago quarter.[^1,61] A naive read calls that diversification. The actual mechanism is replacement: Microsoft declined to exercise a roughly $12B expansion option in early 2025, and OpenAI stepped directly into the same incremental capacity.[^62] The cumulative OpenAI master services agreement now stands at approximately $22.4B through May 2031 — $11.9B signed in March 2025, an approximately $4B expansion in May, and a further $6.5B announced via 8-K on September 25, 2025.[^3] Five days later, CoreWeave disclosed a Meta order form worth up to $14.2B through December 14, 2031, with optional expansions running into 2032.[^9]

| Customer | FY2023 | FY2024 | FY2025 | Q1 2026 |
|---|---|---|---|---|
| Customer A (Microsoft) | 35% | 62% | 67% | 45% |
| Customer B (likely OpenAI in Q1 2026) | \* | <10% | \* | 20% |
| Customer C / D (Meta, others) | \* | \* | 11% of A/R | combined ~30%+ of A/R |
| **Backlog (RPO, $B)** | n/a | 15.1 | 60.7 | 98.8 |

*Sources: 10-K FY2025* [^2] *, 10-Q Q1 2026* [^1] *. Asterisks denote periods where the customer was either below the 10% disclosure threshold or where the alphabetic mapping in the 10-K reshuffled between years. The 10-Q itself warns that "the customer references of A through D may represent different customers than those reported in a previous period."*

:::callout(kind=info)
**Rotating, not diversifying.** The FY2025 10-K explicitly names only three customers — Microsoft, OpenAI, and Meta — as the expected significant counterparties going forward.[^2] Customer A and Customer D alone represented 68% and 11% of accounts receivable at year-end 2025 — 79% of money owed to CoreWeave was owed by two entities.[^2] A 45% top-customer share looks healthier than 67% only if you ignore that the second and third slots are now occupied by counterparties with their own balance-sheet questions.
:::

The Microsoft step-down is also entangled with structural changes at the anchor. Microsoft's October 28, 2025 restructuring of its OpenAI partnership re-baselined the compute relationship and explicitly removed Microsoft's right of first refusal on OpenAI compute, which is what enabled OpenAI's direct contracting with third-party providers — CoreWeave being the largest beneficiary.[^33] In other words, the shift in CoreWeave's revenue mix is downstream of a single corporate-development event at one of its three customers, not the outcome of a broad commercial campaign.

**What would weaken this thesis:** if CoreWeave converts the Top-3 anchor contracts into a foundation that pulls in sovereign AI buyers, tier-2 model labs (Mistral, Cohere, AI21), and large enterprise inference workloads at meaningful scale over 2026–2027, the concentration ratio could decay organically rather than through musical chairs. The 10-K gestures at pipeline activity in these segments, but none has yet appeared as a named >10% revenue contributor.[^2] Second weakening vector: if RPO continues compounding at Q1 2026's pace, even a constant 80% top-three share leaves an absolute dollar value of "other" revenue that becomes material.

**Why this matters:** every subsequent section of the CoreWeave thesis — unit economics, debt covenants, SPV structures, pricing power, depreciation policy, and the 2029 contract-roll cliff — is conditional on the durability of three counterparties. Backlog growth and customer concentration are not independent variables; they are the same variable observed twice.

## 2. Unit Economics of a Rented GPU

**Section thesis:** A single H100 GPU rented by CoreWeave under a five-year take-or-pay contract throws off roughly **$17,600 of EBITDA on a $40,000 installed capex** — an unlevered IRR near **35%** that is real, attractive, and durable *if and only if* (a) the six-year accounting useful life holds and (b) realized price does not compress by more than ~30% over the asset's life. Both assumptions are contested.[^2,25]

### 2.1 The base-case build

Start with the asset. SemiAnalysis pegs the fully-loaded, ready-to-rent cost of an H100 inside a CoreWeave-style HGX node — silicon plus NVLink, InfiniBand fabric, storage allocation, rack, and integration — at **~$40,000 per GPU**.[^22] An HGX H100 server houses eight GPUs and draws ~10.2 kW under sustained load, or roughly **1.275 kW per GPU** at the rack inlet before PUE.[^22] CoreWeave depreciates "technology equipment" over **six years**, a useful life it extended from five years effective January 1, 2023.[^2]

Now layer realized pricing. CoreWeave's *public* on-demand rate is $6.16/GPU-hr for H100, $6.31 for H200 and $8.60 for B200,[^15] but more than 98% of revenue sits inside multi-year take-or-pay contracts that trade roughly 50–60% off list. A defensible blended realized rate is **~$2.75/GPU-hr**. At 85% effective utilization — the level implied by take-or-pay structures where the counterparty pays whether it runs the silicon or not — annual revenue per GPU is $2.75 × 8,760 × 0.85 ≈ **$20,477**.

### 2.2 The per-GPU P&L

| Line (per H100, annual) | Base case | Derivation |
|---|---|---|
| Revenue | **$20,477** | $2.75 × 8,760 hr × 85% util |
| Power + colocation | ($1,836) | 1.5 kW landed × $100/kW-mo × 12[^12] |
| Ops, networking, S&M allocation | ($1,024) | ~5% of revenue |
| **Cash EBITDA** | **$17,617** | ~86% margin |
| D&A (6-yr life) | ($6,667) | $40,000 / 6[^2,22] |
| **EBIT** | **$10,950** | ~53% margin |
| Unlevered IRR (5-yr contract) | **~35.5%** | $40k outlay, 5×$17.6k inflows, ~$5k residual |
| Cash payback | **~2.3 yr** | $40,000 / $17,617 |

The colocation+power line is anchored to two recent primary disclosures. Core Scientific's April 21, 2026 supplemental disclosed a CoreWeave rack rate of **$100/kW-month** on the legacy footprint,[^12] and Applied Digital's August 29, 2025 8-K describes the Polaris Forge 1 lease as **$11B over 15 years across 400 MW** — implying ~$152/kW-month when CoreWeave is the customer and APLD funds the powered-shell build.[^13] The $100 number is the right input for assets inside CoreWeave's own footprint; the $150+ number is what marginal capacity now costs and is one reason new vintages are slightly less attractive than this base case.

### 2.3 Sensitivity: where the IRR breaks

:::kv
- term: '**Useful life 6 → 4 years (Burry/Chanos scenario)**[^25]'
  def: D&A jumps from $6,667 to $10,000. Cash IRR is mechanically *unchanged* — CoreWeave still collects
    the same dollars under contract — but reported EBIT collapses from $10,950 to ~$7,617, a ~30% haircut.
    Book ROIC falls into the high single digits even though the contract is performing.
- term: '**30% price compression realized over years 3–5**'
  def: Silicon Data's H100 marketplace index fell from $7–10/hr in 2023 to **$1.92–2.36/hr** by late 2025
    — roughly 70% peak-to-trough.[^23] The take-or-pay book is insulated *through expiry*, but renewals
    re-price into the new curve. If realized blended drops to ~$1.93/hr in years 3–5, unlevered IRR falls
    from 35% to **~22%**.
- term: '**Combined stress (4-yr life + 30% price compression)**'
  def: Cash IRR holds around **~22%** because the original contract dollars are locked, but the asset
    finishes its book life under-depreciated relative to fair value and the firm prints reported losses
    through the second half of the GPU's life — exactly the pattern critics expect.
:::

### 2.4 The Nvidia framing, recalibrated

Nvidia management has repeatedly suggested customers earn "**$5 of revenue per $1 of GPU**" over the life of the asset. Plug the numbers in: $5 × $40k = $200k of lifetime revenue, which over six years requires sustained pricing near **$4.50–$5.00/GPU-hr at 85% utilization** — i.e., hyperscaler-tier rates that *only* exist today on short-tenor, retail SKUs.[^15] At the realistic blended $2.75/hr embedded above, lifetime revenue is ~$123k, or a **~3x revenue multiple on cost** — still attractive, but well below the talking point and offering no margin for further compression.

### 2.5 Reconciling to reported financials

The per-unit P&L scales. CoreWeave reported **$2,454M of D&A on $5,131M of revenue in FY2025 — 47.8% of revenue**[^2] — almost exactly what a fleet-average $20k/yr-revenue / $6.7k/yr-D&A unit implies once weighted for mid-life vintages and a growing H200/B200 mix. FY2025 capex of **$10,309M** and Q1 2026 cash capex of **$7,695M** plus another **$4,592M of non-cash P&E additions**[^1] tell you the fleet is still steeply front-loaded: D&A as a percent of revenue will keep rising for at least two more quarters before run-rate revenue catches the depreciation curve.

**Why this matters:** the entire CoreWeave equity thesis reduces to a single bet — that a 35% unlevered IRR per GPU survives the next two Nvidia generations. The contracted backlog protects vintages already deployed; it does *nothing* for the ~$12B per quarter of *new* silicon that has to clear at competitive returns to justify the capital stack examined in Section 5.

## 3. The Take-or-Pay Architecture: Turning Contracts Into Investment-Grade Debt

**Section thesis:** CoreWeave's most underappreciated asset isn't its H100 fleet — it's a repeatable legal structure that converts a single named hyperscaler take-or-pay contract into a bankruptcy-remote SPV whose secured debt now prices six notches inside the parent, a financial-engineering arbitrage that turns customer credit into GPU credit and has compressed the company's marginal cost of capital from 15% to 7% in roughly twenty-four months.

The mechanic is disclosed in plain English. Per the FY2025 10-K, ">98%, 96% and 88% of our revenue, respectively, \[for 2025, 2024, 2023\]" came from "committed contracts… typically structured as take-or-pay agreements, requiring payment regardless of the level of utilization."[^2] CoreWeave then drops the GPUs purchased to serve a specific contract — together with the contract receivables themselves — into a single-purpose LLC (the "Delayed Draw Term Loan" or DDTL borrower). The SPV pledges (i) substantially all of its assets (the GPU servers), (ii) the equity of the SPV itself, and (iii) the contracted customer cash-flow waterfall to the lender syndicate.[^1,2] Debt is non-recourse to the parent; the borrowing base is capped at the depreciable cost of the underlying GPU servers and is governed by project-level DSCR covenants.[^2]

DDTL 3.0, executed July 2025, was the template that proved the structure. The press release explicitly identified the anchor counterparty: "The funding will be used to support the purchase and maintenance of advanced equipment, hardware, and cloud infrastructure systems to deliver services under a long-term agreement with OpenAI," with OpenAI CFO Sarah Friar quoted in the release itself.[^8] DDTL 4.0, signed March 31, 2026, generalized the playbook and was secured by a new SPV — CoreWeave Compute Acquisition Co. VIII, LLC ("CCAC VIII"). The 8-K states the facility "was entered into primarily to finance capital expenditures required to perform a customer contract, including the acquisition of GPU servers and related infrastructure."[^6,7]

**DDTL ladder at March 31, 2026 — the rate compression story**

| Facility | Drawn (Mar-26, $B) | Effective Rate | Maturity | Parent Recourse? |
|---|---|---|---|---|
| DDTL 1.0 (Magnetar/Blackstone) | 1.44 | ~15% | 2028 | No (SPV) |
| DDTL 2.0 | 4.43 | ~11% | 2030 | No (SPV) |
| DDTL 2.1 | 3.00 | ~9% | 2031 | No (SPV) |
| DDTL 3.0 (OpenAI-anchored) | 1.70 | ~9% | 2030 | No (SPV) |
| DDTL 4.0 (CCAC VIII) | 1.26 drawn / $8.5B commitment | ~7% | 2032 | No (SPV) |
| **Aggregate DDTL commitments** | **~24.0** | — | — | — |

The pricing arbitrage culminates in DDTL 4.0's rating action. On March 31, 2026, Moody's assigned CCAC VIII an **A3** rating — the first GPU-collateralized loan ever rated investment grade.[^57] The parent CoreWeave Inc. carries a Moody's corporate family rating of **Ba3**: a *six-notch gap* between the SPV and its sponsor. The gap is not a quirk; it is the entire thesis. The agencies are rating the take-or-pay cash flow of a named hyperscaler counterparty plus the bankruptcy-remote ring-fence, not CoreWeave's standalone credit. DDTL 4.0 also introduced a first-of-its-kind covenant package requiring explicit power-price hedging at the SPV level, plugging the one cash-flow leakage point that prior facilities tolerated.[^6]

**Why this matters — the 300bp math.** Management has publicly cited a "300 bps improvement" in cost of capital from DDTL 1.0 to 4.0. On a $25B drawn debt base, 300bps is roughly $700M of pre-tax cash flow annually — the difference between CoreWeave being a self-funding growth platform and a zombie business compounding interest faster than it depreciates assets. S&P's April 9, 2026 outlook revision to positive made the upgrade path explicit and conditional: material-weakness remediation by YE2026 plus sustained FFO/debt > 12% *and* CFO/debt > 10%.[^58] Hitting those covenants is what unlocks another leg of rate compression.

**Counterpoint — the rating is contract credit, not company credit.** The A3 rating on CCAC VIII rests on the assumption that the named customer pays the take-or-pay coupon for the contract's full term. DDTL 3.0's underlying contract is OpenAI's. If OpenAI restructured, renegotiated, or unilaterally terminated — or if the contract were ever recharacterized in a bankruptcy stay — the "investment grade" rating on the secured loan unravels in the same quarter, and the parent's Ba3 reasserts as the binding credit. The IG label is a derivative of one customer's solvency, not CoreWeave's. That is the structural fragility Section 4 examines next.

## 4. OpenAI as Anchor Counterparty

**Section thesis:** CoreWeave's investment-grade debt narrative is functionally a credit-derivative on a private, cash-flow-negative counterparty: OpenAI represents ~22% of the $99B backlog and the explicit collateral pool for the $11B IG-rated DDTL stack, yet it is also the smallest line item in OpenAI's own $1.4T compute commitment book and therefore the first that would be cut in a liquidity squeeze.

The structural rotation began in early 2025 when Microsoft declined a roughly $12B CoreWeave expansion option, and OpenAI absorbed that capacity through a $11.9B, five-year master services agreement running through October 2030.[^62] A second tranche of approximately $4B followed in May 2025, and an 8-K on September 25, 2025 disclosed an incremental $6.5B extension through May 2031, taking cumulative OpenAI commitments to roughly $22.4B.[^3] That figure equates to ~22% of the $99B contracted backlog reported in the Q1 2026 10-Q,[^1] and the September 2025 DDTL 3.0 facility ($2.6B) was explicitly underwritten against the OpenAI MSA receivables.[^8]

Scaling that commitment against the customer's broader procurement reveals the asymmetry. On November 6, 2025, Sam Altman stated OpenAI has "approximately $1.4 trillion" of compute commitments over the next eight years;[^31] CoreWeave is the smallest named vendor in that stack.

**OpenAI's verbal vendor stack (per Altman, Nov 6, 2025)**

| Counterparty | Committed $ | Share of $1.4T |
|---|---|---|
| Broadcom (custom silicon) | $350B | 25.0% |
| Oracle (Stargate) | $300B | 21.4% |
| Microsoft Azure | $250B | 17.9% |
| Nvidia | $100B | 7.1% |
| AMD | $90B | 6.4% |
| AWS | $38B | 2.7% |
| **CoreWeave** | **$22.4B** | **1.6%** |
| Unallocated / residual | ~$250B | 17.9% |

The counterparty's own solvency profile is the central question. OpenAI generated approximately $13B of revenue in FY2025 and exited Q1 2026 at an annualized run rate near $20B per CFO Sarah Friar; leaked financial reporting summarized by Fortune and The Information indicates operating cash burn of roughly $25B in 2026, rising to $57B in 2027, with cumulative cash consumption through 2029 of approximately $115B. The March 2026 $122B primary round at an $852B post-money valuation — led by Amazon ($50B), Nvidia ($30B), and SoftBank ($30B) — leaves OpenAI with ~$40B of cash on hand, implying an 18-month runway against the 2026 burn rate absent further financing.[^32]

Microsoft, historically the backstop, is no longer that. The October 28, 2025 restructuring crystallized Microsoft's stake at roughly 27% as-converted, eliminated Microsoft's right of first refusal on OpenAI compute, and obligated OpenAI to an incremental $250B Azure commitment.[^33] The ROFR elimination is precisely what enabled the $300B Oracle Stargate arrangement[^64] and the $50B AWS deal that is now in dispute between Microsoft and Amazon over surviving exclusivity terms (April 2026). Microsoft's own 10-Q discloses that its $13B funding commitment to OpenAI is essentially fully drawn ($11.8B funded as of March 31, 2026), so any liquidity bridge would have to come from new external capital, not the legacy partner.

**Counterpoint.** The take-or-pay structure detailed in Section 3 is binding through 2030–2031: if OpenAI internally deprioritizes CoreWeave capacity, it still owes the contracted minimum, and OpenAI has never missed a payment to date. The only contractual off-ramp is the carve-out disclosed in the 10-K risk factors: "in the event of the Company's repeated failure to meet availability of service requirements, OpenAI has the right to terminate all or a portion of the committed amount."[^2] That is termination-for-cause, not termination-for-convenience — the exposure is operational (uptime SLAs on H100/H200/GB200 clusters) rather than financial.

**Why this matters.** The DDTL 3.0 facility and the broader $11B IG-rated debt stack are priced on the implicit assumption that the OpenAI receivable is investment-grade-equivalent for the contracted term. OpenAI carries no external credit rating, is cash-flow-negative at the corporate level, and ranks CoreWeave as its smallest named compute vendor at 1.6% of total commitments. The asymmetry cuts both ways: a small share means CoreWeave is unlikely to be the line OpenAI defends in a crunch, but it also means OpenAI can almost certainly fund the $22.4B contractually owed even in a downside scenario — $22.4B is roughly one quarter of a single primary round at the March 2026 valuation.

## 5. The Capital Stack: $25B Debt, $66B Effective Obligations

CoreWeave's March 31, 2026 balance sheet shows **$25.1B of principal debt and $0.24B of finance-lease liabilities**, but this GAAP figure understates true contractual fixed obligations by roughly **2.6x on a present-value basis and 4.1x undiscounted**. The gap is the $40.7B of executed-but-not-yet-commenced operating leases plus a single 525 MW campus lease carrying $18.7–19.6B of contractual rent — neither on the balance sheet today, both beginning to recognize expense between late 2026 and 2029.[^1]

**Debt tranches at March 31, 2026 ($M principal)**[^1]

| Tranche | Principal | Eff. rate | Maturity |
|---|---|---|---|
| DDTL 1.0 | $1,438 | 15% | Mar 2028 |
| DDTL 2.0 | $4,425 | 11% | Aug 2030 |
| DDTL 2.1 | $3,000 | 9% | Mar 2031 |
| DDTL 3.0 | $1,700 | 9% | Aug 2030 |
| DDTL 4.0 (non-recourse, $8.5B commit.) | $1,260 | 7% | Mar 2032 |
| 2030 Sr Notes (9.25% cpn) | $2,000 | 10% | Jun 2030 |
| 2031 Sr Notes (9.00% cpn) | $1,750 | 10% | Feb 2031 |
| 2031 Convertible Sr Notes (1.75% cpn) | $2,588 | 2% | Dec 2031 |
| Convertible Promissory Notes | $171 | 7% | Apr 2026 |
| Revolver | $1,500 | 6% | Nov 2029 |
| OEM / Software License Financing | $5,036 | 10% | Jul 2026–2030 |
| Magnetar Loan (reclassified deposit) | $281 | 12% | Jan 2029 |
| **Total principal** | **$25,149** | — | — |

Three features warrant emphasis. First, weighted blended cost is high: even excluding the 1.75% converts, the rest of the stack averages roughly **9–10%**, with the original DDTL 1.0 still costing 15%.[^1] Second, growth is fast — debt rose from $8.0B at year-end 2024 to $21.6B at year-end 2025 to $25.1B at quarter-end, a tripling in 15 months.[^1,2] Third, April 2026 issuance of **$2.75B of 9.75% Senior Notes due 2031 and $4.0B of 1.75% Convertible Notes due 2032** — neither in the Q1 balance sheet — pushed pro-forma debt to approximately **$31.9B** before the $171M converts settled.[^60] The 9.75% coupon on the new senior notes is the highest reset yet, signaling that incremental capital is getting more expensive even as the absolute quantum balloons.

**Effective contractual obligations, on- and off-balance-sheet**[^1]

| Bucket | PV ($B) | Undiscounted ($B) | Status |
|---|---|---|---|
| Debt principal | 25.1 | 25.1 | On-balance-sheet |
| Finance-lease liability | 0.2 | 0.3 | On-balance-sheet |
| Commenced operating leases | 10.1 | 17.0 | On-balance-sheet |
| Leases executed, not yet commenced | ~22 | 40.7 | Footnote only |
| 525 MW 16-yr campus lease | ~9–10 | 18.7–19.6 | Footnote only |
| Lessee-owned equipment commitments | ~1 | 0.9–1.6 | Footnote only |
| **Effective total** | **~67–69** | **~103–104** | — |

At a 10% incremental borrowing rate — the IBR CoreWeave itself uses in both its 10-K and 10-Q footnotes for lease discounting[^1,2] — the **effective fixed-obligation PV lands in the $66–69B range, versus a market capitalization of roughly $58.5B** at the ~$107 mid-May 2026 share price on 545.6M shares outstanding.[^38] Effective obligations therefore equal **113–118% of equity value**. Undiscounted, the figure is closer to $103–104B, or *1.77x enterprise value*. On a leverage-multiple basis, debt alone runs **5.5x annualized Q1 2026 Adjusted EBITDA** of $1.157B (56% margin);[^61] including all leases, the multiple climbs to **~14.5x**.

Cash provides a thin cushion. The company ended Q1 with $2.24B unrestricted plus $1.08B restricted, totaling $3.32B — but the unrestricted balance *fell $883M sequentially*.[^1] Q1 interest expense alone was $536M ($427M after capitalization), annualizing to roughly **$2.1B** in cash interest before the April issuance adds another ~$340M of annual coupon at the 9.75% rate.[^1,60]

**Counterpoint.** ASC 842's "leases not yet commenced" disclosure is standard, not buried — sophisticated lenders and credit analysts already capitalize it. And the $8.5B DDTL 4.0 facility is explicitly *non-recourse*: specific GPU + customer-contract pools are siloed in SPVs, so equity holders' downside isn't quite the gross stack. If a single customer cohort impairs, the related SPV — not the parent — bears the loss first. That structural protection meaningfully reduces tail risk versus a naive sum-of-obligations read.

**Why this matters.** The $40.7B not-yet-commenced bucket will start converting to recognized rent expense at roughly ==$4–5B per year between late 2026 and 2029==, on top of the ~$2.1–2.5B of cash interest the existing debt already costs. Combined with depreciation step-ups (Section 7), reported operating margins compress sharply *unless* revenue keeps doubling — which is precisely the bet the take-or-pay backlog (Section 3) is designed to underwrite. Miss the revenue ramp by even one quarter and the off-balance-sheet wedge becomes the dominant variable in the equity story.

## 6. Pricing Position: Discount to Hyperscaler, Premium to Neocloud

CoreWeave's published price card tells the cleanest story about its market repositioning. In 2023 the company was the disruptor, undercutting AWS H100 list prices by 60–70% and helping pull marketplace H100 rentals from $7–10/GPU-hr down toward $2/GPU-hr.[^23] By mid-2026 that posture has inverted: CoreWeave's list pricing now sits roughly 10–15% below AWS on H100, ~50% below Azure, but 50–100% above pure commodity neoclouds like Nebius and Crusoe.[^15,19] CoreWeave is no longer pricing as a neocloud disruptor — it is pricing as a premium specialty cloud, with the Blackwell spread to hyperscalers carrying most of the remaining customer-acquisition story.

| Provider | H100 $/GPU-hr | H200 | B200 | GB200 |
|---|---|---|---|---|
| Nebius | 2.95 | 3.50 | 5.50 | n/a |
| Crusoe | 3.90 | 4.29 | contact | contact |
| Lambda | 3.99 | n/a public | 6.69 | n/a public |
| CoreWeave | 6.16 | 6.31 | 8.60 | 10.50 |
| AWS (p5/p5en/p6, on-demand) | 6.88 | 7.91 | 14.24 | n/a public |
| GCP (A3/A3U/A4) | 11.06 | 12.27 | 4.28\* | reservation-only |
| Azure (NDv5/NDv6) | 12.29 | 13.78 | n/a public | n/a public |

*\*GCP A4 (B200) list of $4.28/GPU-hr is anomalously low and reflects a mandatory capacity-reservation commitment rather than true on-demand availability.* [^18]

Three observations follow directly. First, the Hopper gap has compressed materially: CoreWeave's $6.16/hr H100 list is now only ~$0.72/hr cheaper than AWS p5 on-demand at $6.88/hr.[^15,16] Second, the Blackwell spread is the widest in CoreWeave's favor in years — $8.60/hr for B200 against AWS p6 list at $14.24/hr is a ~40% discount,[^16] exactly the wedge CoreWeave needs to win new Blackwell workloads from enterprises evaluating hyperscalers. Third, against pure neoclouds CoreWeave looks expensive: Nebius lists B200 at $5.50/hr (~36% below CoreWeave)[^19] and Lambda is at $6.69/hr.[^21]

The reserved-pricing dynamic is the most underappreciated risk to the list-price story. AWS's 3-year reserved H100 on p5 instances clears at roughly $2.97/GPU-hr[^16] — undercutting CoreWeave's on-demand H100 by approximately 50%. Any hyperscaler willing to publish similarly aggressive reserved pricing on Blackwell SKUs erodes CoreWeave's structural pricing wedge precisely where the company needs it most.

The market today sorts into three pricing tiers:

:::kv
- term: Hyperscaler tier ($7–14/hr list)
  def: AWS, Azure, GCP. Customers pay for managed services, enterprise compliance, multi-region failover,
    and integration with the rest of the stack (S3, IAM, BigQuery). Reserved tiers can drop to ~$3/hr
    for committed multi-year tenants.[^16]
- term: Premium neocloud / specialty (CoreWeave, $6–9/hr)
  def: Pays for InfiniBand-grade clusters, validated reference architectures, dedicated cluster managers,
    and a software stack (SUNK, Mission Control) that pure capacity vendors do not offer.[^15]
- term: Commodity neocloud ($3–5/hr)
  def: Nebius, Crusoe, Lambda. Pure capacity rental, typically smaller fabric scale, less software, less
    white-glove support.[^19,20,21]
:::

**Counterpoint — list price is misleading.** CoreWeave's realized contracted rate, backed out from the Section 2 revenue/MW math, is closer to $2.50–3.00/GPU-hr blended across its hyperscaler-heavy customer book — well below list and effectively in the same range as Crusoe, Lambda, and Nebius. The "premium" tier described above is structural (cluster scale, managed services, multi-year contracted commits) rather than something each marginal customer is asked to pay every hour. The storefront is premium; the actual P&L is commodity-adjacent with operating leverage.

**Why this matters:** if hyperscalers continue publishing competitive reserved pricing on Blackwell SKUs — as AWS already has on Hopper at ~$2.97/hr[^16] — CoreWeave's customer-acquisition cost rises, contract renewals re-price downward, and the implied ~35% IRR per GPU (Section 2) degrades materially over the asset's useful life.

## 7. Depreciation, Useful Life, and the GPU Half-Life Debate

No accounting line on CoreWeave's income statement is more contested than depreciation. The company depreciates its computing equipment over six years — tied with Google at the top of the hyperscaler range, but a full two years longer than its closest pure-play comparable, Nebius. Because depreciation already consumed 47.8% of FY2025 revenue,[^2] even small adjustments to useful-life assumptions cascade directly into reported losses. CoreWeave is not a numerical outlier versus the diversified hyperscalers, but it is the most exposed to a useful-life reset: it has no advertising, cloud, or device earnings to absorb the hit, and it runs its fleet at sustained training utilization rather than the mixed workloads that justify longer lives at AWS or Azure.

CoreWeave's own disclosure is explicit. "Effective January 1, 2023, the Company changed its estimate of the useful life for its computing equipment utilized in data centers from five to six years, reflecting continuous advancements in hardware performance, software optimization, and data center design improvements."[^2] Software is depreciated over three to six years; data-center equipment and leasehold improvements over the shorter of remaining lease term or up to twelve years; furniture over three to five years.[^2] The tech-equipment line is the one that matters: gross book value grew from $20.9B at December 31, 2025 to $26.6B at March 31, 2026, a 27% sequential increase.[^1]

The peer comparison is where the bear case bites. The industry is bifurcating: diversified hyperscalers with mixed workloads are extending lives, while pure-play AI infrastructure operators are shortening them.

| Company | Asset class | Useful life | Direction of last change |
|---|---|---|---|
| CoreWeave | Technology equipment (GPUs) | 6 years | Extended from 5 to 6 yrs, eff. Jan 1, 2023[^2] |
| Alphabet | Servers and network equipment | 6 years (generally) | Extended from 4 to 6 yrs, eff. FY2023[^27] |
| Microsoft | Computer equipment | 2 to 6 years (range) | Range disclosed; no single weighted-average[^28] |
| Meta | Servers and network equipment | 5.5 years | Extended from 5 to 5.5 yrs, eff. Jan 1, 2025[^29] |
| Amazon | Subset of servers and networking | 5 years | **Shortened** from 6 to 5 yrs, eff. Jan 1, 2025[^30] |
| Nebius | GPU servers | 4 years | Pure-play peer benchmark[^24] |

Amazon's January 2025 reset is the most telling: management explicitly attributed the shortening to "the increased pace of technology development, particularly in the area of artificial intelligence and machine learning," and booked $1.4B of incremental depreciation and a $1.0B net-income hit in a single year.[^30] Meta moved the other direction, extending to 5.5 years and harvesting $2.9B of reduced D&A and $2.6B of net income ($1.00/diluted share).[^29] Neither company is a pure-play; both have inference-heavy and non-AI workloads that can plausibly extend asset lives.

Short sellers have seized on the gap. Kerrisdale Capital's September 2025 report argued that CoreWeave's six-year assumption is "aggressive given the rapid pace of innovation," contrasted it explicitly with Nebius's four years and Amazon's reset, and warned that "a shift to shorter useful lives would eviscerate CoreWeave's unit economics and margins"; the firm set a $10 price target.[^24] Michael Burry escalated the critique in November 2025, estimating that the five largest AI hyperscalers will collectively understate depreciation by roughly $176B over 2026–2028 and arguing that the true useful life of training GPUs is closer to two or three years.[^25] Jim Chanos put it bluntly the following month: "If the chips last for three years, you have to depreciate a third of what you spend."[^26] The empirical evidence cuts both ways — on-demand H100 rental prices have fallen roughly 70% peak-to-trough,[^23] while used A100 80GB units still clear at $12–18k versus $25k+ new.[^23]

Management's counter is credible. CEO Mike Intrator has noted that CoreWeave's A100 fleet remains "all fully booked" years after launch, and that a recent batch of H100s coming off contract was re-leased at 95% of the original contracted price. If the secondary contracted-revenue market continues to clear at near-parity to original pricing, the accusation of aggressive accounting weakens substantially — the six-year life matches Google's disclosed policy[^27] and sits at the top of Microsoft's two-to-six-year range,[^28] both of which auditors have signed off on.

Sensitivity: a forced reset from six to four years on the $26.6B March 31, 2026 technology-equipment base would add approximately $3–4B of annual depreciation. Against an FY2025 net loss of $1.17B,[^2] that is a compounding rather than a marginal hit. **Why this matters:** such a reset would not change cash IRR on contracted GPU fleets, but it would convert reported EBIT into substantial losses — and CoreWeave's equity story, particularly the S&P credit-upgrade path that hinges on FFO-to-debt metrics, is currently underwritten on reported numbers, not just cash.

## 8. Power, Grid, and the Unraveled Core Scientific Deal

**Thesis:** CoreWeave is not GPU-constrained — it is power-constrained. The binding scarcity in the AI infrastructure stack in 2025–2026 is not Hopper or Blackwell silicon; it is energized, interconnected, cooled megawatts. CoreWeave's response is a two-pronged real-estate strategy: (i) attempt to acquire its largest landlord, Core Scientific, to bring 1.3 GW of owned capacity onto its own balance sheet, and (ii) when shareholders rejected that deal, pivot to long-dated colocation licenses that achieve most of the operational result without the equity dilution. The Q3 2025 earnings miss — 590 MW active versus a Street-consensus ~625 MW, with the 2025 capex guide cut from $20–23B to $12–14B on data-center-availability delays[^41] — was the first observable financial leak from this bottleneck.

The numerator side of the growth story is extraordinary: 70 MW active at end-2023, 360 MW end-2024, 850+ MW end-2025 across 43 data centers, with a total contracted pipeline of ~3.1 GW.[^2] Q1 2026 added another 525 MW from a single 16-year lease carrying $18.7–19.6B of contractual rent.[^1] The 2026 capex guide of $30–35B is roughly 3× 2025 and is meant to take active power to 1.7 GW by year-end. None of that demand-side math works unless the underlying powered shells are delivered on schedule.

The Core Scientific transaction announced July 7, 2025 was designed to remove that schedule risk. The all-stock deal — 0.1235 CRWV shares per CORZ share, implied equity value ~$9.0B at announcement — would have folded 1.3 GW of gross CORZ capacity plus an incremental 1 GW+ of expansion potential onto CoreWeave's balance sheet.[^10] CORZ shareholders rejected it on October 30, 2025: 20.75M for, 203.45M against, 21.59M abstain — only 8.5% support, one of the most lopsided merger rejections of the year.[^11] CORZ holders concluded that the bitcoin-mining optionality and the standalone HPC trajectory were worth more than the CRWV stock consideration.

Post-rejection, CoreWeave and Core Scientific restructured the relationship as long-term colocation licenses across six sites, disclosed in CORZ's April 21, 2026 supplemental.[^12] The licenses cover Austin, Denton, Dalton 1, Dalton 4, Marble, and Muskogee — approximately 590 MW net IT load (roughly 900 MW gross grid) at a base rate of $100/kW-month ($115 in Austin) with 3.5% annual escalators and ~15-year initial terms. Aggregate revenue to CORZ is approximately $10B net of rent repayments, with CoreWeave funding construction costs offset by revenue credits capped at $1.5M/MW.

| Site | Lessor | MW (Net IT / Contracted) | Notes |
|---|---|---|---|
| Austin, TX | Core Scientific | in ~590 MW pool | $115/kW-month base rate (premium)[^12] |
| Denton, TX | Core Scientific | in ~590 MW pool | $100/kW-month, 3.5% escalator, ~15-yr[^12] |
| Dalton 1 + 4, GA | Core Scientific | in ~590 MW pool | legacy crypto-mining substation rights[^12] |
| Marble, NC | Core Scientific | in ~590 MW pool | ~$10B aggregate revenue across 6 sites[^12] |
| Muskogee, OK | Core Scientific | in ~590 MW pool | inherited via Polaris-DS acquisition[^12] |
| Polaris Forge 1 (Ellendale, ND) | Applied Digital | 400 MW across 3 leases; B1 100 MW energized Q4 2025 | ~$11B agg revenue, ~15-yr; B2 150 MW mid-2026; B3 150 MW 2027[^13,14] |
| Kenilworth, NJ JV | CoreWeave (own JV) | MW not disclosed | 15% → 20% equity stake by Q1 2026; first vertical-integration move[^1] |
| Q1 2026 new 525 MW lease | undisclosed | 525 MW, 16-yr | $18.7–19.6B contractual rent on a single site[^1] |

The macro context makes clear that CoreWeave's delivery problem is the industry's delivery problem. LBNL's *Queued Up 2025* shows ~1,400 GW of generation plus 890 GW of storage waiting in US interconnection queues at year-end 2024, with a 77% historical withdrawal rate and median interconnection-request-to-commercial-operation now exceeding four years.[^42] In PJM the time from request to commercial operation has grown from under two years in 2008 to more than eight years in 2025.[^43] Dominion has 70 GW of large-load delivery points queued against an all-time system peak of 24.7 GW. ERCOT's large-load queue went from 63 GW at end-2024 to 226 GW in November 2025 to ~410 GW by March 2026 (~87% data centers), against an ERCOT 2026 summer peak forecast of just 90.5–98 GW.[^44] Cleanview counted ~46 US data centers and ~56 GW of behind-the-meter capacity online or under construction by February 2026, and more than one-third of all new US natural-gas plant capacity is now being built for data centers.[^47]

**Counterpoint:** the queue is everyone's problem. Microsoft, Google, Meta, Amazon, and Oracle all face the same PJM, ERCOT, and Dominion arithmetic, and CoreWeave's strategy of leasing already-interconnected sites from CORZ and APLD — substations and grid rights inherited from the prior bitcoin-mining buildout — is plausibly faster than greenfield queue entries hyperscalers must wait years to clear. The Core Scientific deal collapse looks bad strategically, but the licensing structure that replaced it captures most of the operational benefit (~590 MW of dedicated, long-term capacity at fixed escalators) without ~$9B of equity dilution or the integration risk of absorbing a still-operating bitcoin miner.

**Why this matters:** every additional quarter of powered-shell delay pushes contracted revenue right while leaving interest expense on debt already drawn against that capacity unchanged — the compounding cost of unlit megawatts is the single most underappreciated line in the CRWV model.

## 9. Hyperscaler In-Housing and the 2029 Cliff

Every anchor tenant on CoreWeave's customer roster is simultaneously funding a parallel silicon program designed to reduce its dependence on rented Nvidia capacity. Amazon has Trainium, Google has Ironwood, Microsoft has Maia, Meta has MTIA, and OpenAI has Titan in tape-out with Broadcom on TSMC N3. The take-or-pay structure of CoreWeave's $98.8B RPO makes this a non-event for revenue recognition through roughly 2029 — customers must pay whether they consume the GPU-hours or not.[^2] The question is not the back-half of the existing book; it is whether net new signings keep compounding once each anchor has multiple generations of its own accelerator in volume production.

The cumulative scale is no longer theoretical. AWS Project Rainier is operating more than 500,000 Trainium2 chips for Anthropic alone,[^48] and the expanded Anthropic–Amazon arrangement commits roughly 5 GW of Trainium capacity over a $100B, ten-year envelope, with Trainium3 ramping in late 2026 and approximately 1 GW of combined Trainium2+3 live by year-end.[^49] Anthropic separately committed to up to one million TPU v7 Ironwood chips through Google — about 400,000 direct-purchase units (~$10B) plus roughly 600,000 of GCP rental capacity (~$42B in RPO on Google's books), for a combined commitment north of $52B and well above 1 GW.[^50] Ironwood itself reached general availability in late 2025 with 192 GB of HBM3e and 7.4 TB/s of bandwidth per chip, and third-party teardowns peg its total cost of ownership roughly 44% below GB200 for inference-heavy workloads.[^51]

Microsoft's Maia 200 (codename Braga) entered production in Q1 2026 at the Iowa campus and is expanding into Phoenix, rated at 10.15 PFLOPS FP4 at 750W TDP and positioned as inference-first.[^54] Meta's MTIA roadmap is the most aggressive in absolute unit volume: MTIA 300 in production today, with MTIA 400, 450, and 500 cadenced every roughly six months through late 2027, supporting hundreds of thousands of accelerators deployed across ranking and ads inference.[^53] OpenAI's Titan, designed with Broadcom on TSMC N3, is targeted for mass production in H2 2026, with a Titan 2 follow-on on TSMC's A16 1.6nm node in 2027.[^52]

:::kv
- term: Insulated 2026–2028 (~75% of $98.8B RPO recognized)
  def: Contracts are take-or-pay with ~4-year weighted-average life. Microsoft, OpenAI, and Meta together
    account for roughly 80%+ of backlog and are legally obligated to pay regardless of whether Maia, Titan,
    or MTIA absorbs incremental workload. In-house silicon ramps in this window are largely additive to,
    not substitutive for, already-committed CoreWeave capacity.[^2]
- term: Exposed 2029+ (~25% of current RPO + all future signings)
  def: The stated 5–8 GW post-2030 growth target requires net new contracts signed in 2027–2029 — exactly
    when Trainium3, Ironwood successors, Maia 300, MTIA 450/500, and Titan 2 will all be in volume. New
    marginal training capacity will be benchmarked against in-house TCO, not against H100 pricing.
:::

| Vendor | Chip | Anchor Customer | 2026 | 2027 | 2028 |
|---|---|---|---|---|---|
| AWS | Trainium2/3 | Anthropic | ~1 GW live | ~3 GW | ~5 GW (full Rainier) |
| Google | TPU v7 Ironwood | Anthropic / internal | GA, ~400k Anthropic | v7e + v8 tape-out | >1 GW Anthropic alone |
| Microsoft | Maia 200 (Braga) | OpenAI inference | Iowa prod, Phoenix build | Maia 300 sampling | Multi-site, training-capable |
| Meta | MTIA 300/400/450 | Meta (ads/ranking/Llama) | MTIA 300 in prod | MTIA 400 + 450 | MTIA 500, training-class |
| OpenAI/Broadcom | Titan / Titan 2 | OpenAI inference | Titan mass production H2 | Titan 2 (A16 1.6nm) | Multi-GW deployment |

**Counterpoint.** In-house silicon has a long history of underdelivering relative to roadmap. Microsoft's Maia 100 was widely characterized as disappointing on perf-per-watt; Maia 200 still lags Blackwell on raw FP8/FP4 throughput.[^54] Custom accelerators typically need three to five deployment cycles to close the compiler, networking, and collective-comms gap with Nvidia's NVLink + CUDA stack — which is why even Trainium2 and Ironwood are absorbed predominantly by inference and mid-scale training, while the frontier 100,000+ accelerator runs (GPT-6-class, Claude Opus 5-class, Gemini 3 Ultra-class) still default to Blackwell and Rubin clusters. CoreWeave's unique selling proposition — InfiniBand fabrics tuned for the very largest synchronous training jobs — remains structurally protected for the marginal frontier workload through at least 2030, even as commodity inference migrates in-house.

**Why this matters.** The question is not whether the existing take-or-pay book gets paid — it will, contract terms are airtight. The question is whether CoreWeave can keep *compounding* RPO at the current pace once each anchor customer has multi-generation in-house silicon at scale. If 2028 closes with zero net new commitments from Microsoft, OpenAI, or Meta, the equity story breaks regardless of how cleanly the legacy contracts amortize.

## 10. Nvidia, Supplier-Shareholder-Customer-of-Last-Resort

No supplier relationship in modern infrastructure is structured quite like the one between CoreWeave and Nvidia. Nvidia is simultaneously CoreWeave's largest hardware vendor, its second-largest shareholder, and the counterparty on a $6.3B residual-capacity backstop that runs through April 2032. The same entity appears on both sides of CoreWeave's income statement and cash-flow statement — Nvidia sells the GPUs CoreWeave depreciates, owns the equity that absorbs the dilution, and, if demand softens, contractually rents the leftover capacity. This trifecta is the single most important — and most contested — feature of the CoreWeave story.

| Role | Quantum | Mechanism | Disclosed in |
|---|---|---|---|
| Top hardware supplier | One of three vendors at 23% / 20% / 17% of FY2025 purchases | GPU and systems procurement under master supply agreements; Nvidia widely understood by analysts to be one of the named three | CoreWeave 10-K FY2025[^2] |
| Second-largest equity holder | ~13% post-PIPE, ~$4.4B at recent price; doubled from ~7% pre-IPO | $2.0B PIPE Jan 23, 2026: 22.9M Class A shares at $87.20 (discount to $92.98 prior close), tied to commitment to build 5 GW of Rubin/Vera/Bluefield AI factories by 2030 | Nvidia/CoreWeave press release Jan 2026[^56] |
| Customer-of-last-resort | $6.3B residual-capacity backstop through April 13, 2032 | New order form Sep 9, 2025 under MSA dated April 10, 2023; hybrid take-or-pay (Nvidia gets to use what it pays for); either-party 30-day termination | CoreWeave 8-K Sep 9, 2025[^55] |

The PIPE is the cleanest illustration. Nvidia injected $2.0B of cash in exchange for stock that was already, on the day of pricing, six percent below the prior Friday's close, and that has since traded back above $107 — Nvidia's January check is already in the money by roughly 23% on paper, and the position has lifted from ~7% pre-IPO to ~13%.[^56] In return CoreWeave is locked into a 5 GW Rubin/Vera/Bluefield deployment path by 2030, effectively pre-committing the design of its 2027–2030 fleet to Nvidia's roadmap.

Zoom out and CoreWeave is one node in a much larger pattern. Nvidia's customer concentration in its Q3 FY26 10-Q shows four direct customers at 22%, 15%, 13% and 11% — 61% of revenue from four buyers.[^34] Those same buyers are increasingly recipients of Nvidia equity: up to $100B promised to OpenAI as 10 GW deploys on Vera Rubin (with Nvidia's CFO conceding in December that the deal is "still not definitive"),[^35] up to $10B into Anthropic alongside a $30B Anthropic-to-Azure commitment that runs on Nvidia silicon,[^36] $2B into xAI, $5B into Intel, $2B into Nebius, $3.2B into Corning, and $2.1B of warrants in IREN — over $40B of YTD equity bets across 67 AI-linked deals in 2025 by CNBC's count. New Street Research has framed the loop with a 3.5x multiplier: every $10B Nvidia equity check appears to yield ~$35B in GPU revenue back.

The pattern is drawing regulatory attention. The DOJ is reviewing the Nvidia–OpenAI architecture; FTC and DOJ have a joint inquiry open into Microsoft/OpenAI/Nvidia; the FTC HSR-cleared Nvidia–Intel on Dec 19, 2025 but Senators Warren and Blumenthal wrote on March 20, 2026 specifically about the Nvidia–Groq deal; and EU competition staff publicly flagged "circular spending" in March 2026. The comparison being drawn in rating-agency notes is to Lucent's and Nortel's pre-2000 vendor financing.

**Counterpoint.** Unlike Lucent vendor paper, Nvidia is generating real cash, has $50B+ of manufacturing commitments backing real shipments, and is monetizing the equity it receives at materially positive marks (OpenAI's stake, Intel's stake, and now CoreWeave's are all in the money). For CoreWeave specifically, "Exemplar Cloud" status, the Jan-2026 $2B at $87.20, and preferential Rubin allocation are tangible competitive advantages that competitors do not enjoy — Oracle, Microsoft and Google get GPUs, but they don't get equity-backed allocation priority. If you must be inside a circular financing structure, being a top recipient of the dominant supplier's preference is structurally better than being outside it.

**Why this matters:** if regulators force Nvidia to unwind any of its equity positions or restructure the $6.3B backstop, the embedded support for CoreWeave's cost of capital weakens precisely when CoreWeave most needs cheap funding to deliver the 5 GW 2030 buildout it has now contractually promised.

## 11. What Could Break the Thesis

A first-principles audit forces the question: what specific events would convert CoreWeave from a $58B-equity, IG-rated growth platform into a distressed asset? Each of the following is plausible enough to model, sourced to a primary disclosure, and large enough — individually — to move the equity by ≥30%.

1. **OpenAI restructures the MSA.** If the next OpenAI funding round arrives at a flat or down valuation (post the March 2026 $852B mark), OpenAI's bankers will look first at the smallest, least-strategic vendor on the $1.4T compute stack — that is CoreWeave at 1.6%.[^31] The 10-K already discloses a termination-for-cause carve-out tied to availability SLAs.[^2] A partial termination that re-cuts the $22.4B commitment by even 25% would impair the DDTL 3.0 collateral pool and force Moody's to re-examine the A3 rating on DDTL 4.0.[^57]
2. **A useful-life reset.** If CoreWeave's auditors follow Amazon's January 2025 lead and require a shortening from 6 to 5 years on training GPUs, the FY2026 incremental depreciation hit is ~$1.5–2B; a more aggressive 6→4 reset adds $3–4B.[^30] Either scenario converts reported EBIT to a substantial loss and shuts the S&P upgrade path that requires FFO/debt > 12%.[^58]
3. **Powered-shell delays compound.** Q3 2025 already showed a 35 MW slip producing a ~$8B capex guide cut.[^41] If two of the four large 2026 commencements (the 525 MW lease, Polaris Forge 1 buildings 2/3, the not-yet-named 363 MW commitments, or any of the six CORZ sites) slip by even one quarter, contracted revenue moves right while debt service on already-drawn DDTLs continues. Interest expense is now $2.1B annualized and rising.[^1]
4. **The off-balance-sheet wedge hits the income statement.** When the $40.7B of leases-not-yet-commenced begins recognizing rent expense at ~$4–5B per year between late 2026 and 2029,[^1] margins compress unless revenue keeps doubling. The market currently models CoreWeave on Adjusted EBITDA, which excludes most of this drag. A repricing toward GAAP EBIT would cut multiples meaningfully.
5. **A hyperscaler-tier reserved Blackwell list price.** If AWS, Azure, or GCP publishes 3-year reserved B200/B300 at the equivalent of ~$4/GPU-hr — half of CoreWeave's $8.60 on-demand — the customer-acquisition wedge in Section 6 collapses on incremental contracts.[^16] AWS already does this on H100 at $2.97/hr versus CoreWeave $6.16/hr.[^16]
6. **Regulatory unwind of the Nvidia circular structures.** If DOJ/FTC compel Nvidia to divest its CoreWeave equity, restructure the $6.3B capacity backstop, or refrain from preferential GPU allocation in exchange for compute commitments, the cost-of-capital benefit currently embedded in the IG-rated DDTL stack erodes.[^55,56]
7. **A material-weakness re-issuance.** S&P's outlook revision to positive was explicitly conditional on remediating the previously disclosed material weakness by YE2026.[^58] A re-issuance — or an expansion of the existing weakness — would not only block the upgrade path but could trigger covenant resets on the senior unsecured stack.

Several often-cited risks do *not* belong on this list. The frequently repeated worry that "in-house silicon will kill CoreWeave" is technically wrong on the contracted backlog: take-or-pay survives Maia, Trainium, Ironwood, MTIA, and Titan deployment through 2029. The worry that "OpenAI will go bankrupt" is innumerate: $22.4B is one quarter's worth of equity raise at OpenAI's current valuation. The worry that "Microsoft will cancel" is contractually impossible without breach. The real risk surface is narrower and more structural — it lives in seven specific failure modes, six of which are conditional events the company itself has flagged in its own filings.

:::callout(kind=info)
**The unified question.** Every break-the-thesis scenario above ultimately reduces to one variable: does Q1 2026's $38B/quarter RPO growth rate sustain through 2028? If yes, the model self-funds, the IG rating extends to the parent, and even three of the seven risks above are absorbable. If no, the off-balance-sheet leverage detonates ahead of revenue.
:::

## References

:::references
- id: 1
  title: CoreWeave, Inc. Form 10-Q for the quarter ended March 31, 2026 (filed May 2026)
  url: https://www.sec.gov/Archives/edgar/data/1769628/000176962826000222/crwv-20260331.htm
- id: 2
  title: CoreWeave, Inc. Form 10-K for fiscal year ended December 31, 2025 (filed March 2, 2026)
  url: https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm
- id: 3
  title: CoreWeave 8-K, "OpenAI Order Form for up to $6.5B through May 31, 2031," filed September 25,
    2025
  url: https://www.sec.gov/Archives/edgar/data/1769628/000119312525216497/d17274d8k.htm
- id: 6
  title: CoreWeave 8-K, "DDTL 4.0 Facility — $8.5B," filed March 31, 2026
  url: https://www.sec.gov/Archives/edgar/data/1769628/000176962826000129/crwv-20260330.htm
- id: 7
  title: CoreWeave press release, "First Investment-Grade Rated GPU-Backed Financing — $8.5B DDTL 4.0,"
    Exhibit 99.1 to 8-K, March 31, 2026
  url: https://www.sec.gov/Archives/edgar/data/1769628/000176962826000129/ex991.htm
- id: 8
  title: CoreWeave press release, "DDTL 3.0 — $2.6B Facility for OpenAI Services," Exhibit 99.1 to 8-K,
    July 2025
  url: https://www.sec.gov/Archives/edgar/data/1769628/000176962825000033/ddtl30pressrelease-ex991x6.htm
- id: 9
  title: CoreWeave 8-K, "Meta Order Form up to $14.2B through Dec 14, 2031," filed September 30, 2025
  url: https://www.sec.gov/Archives/edgar/data/1769628/000176962825000050/crwv-20250925.htm
- id: 10
  title: CoreWeave–Core Scientific merger announcement, Exhibit 99.1 to CRWV 8-K, July 7, 2025
  url: https://www.sec.gov/Archives/edgar/data/1769628/000095010325008492/dp231291_ex9901.htm
- id: 11
  title: Core Scientific 8-K, Item 5.07, "Special Meeting Vote Rejecting Merger," filed October 31, 2025
  url: https://www.sec.gov/Archives/edgar/data/1839341/000114036125040020/ef20058085_8k.htm
- id: 12
  title: Core Scientific 8-K, Exhibit 99.2 "Supplemental Information," filed April 21, 2026 (per-site
    MW and $100/kW-month CoreWeave colocation rate)
  url: https://www.sec.gov/Archives/edgar/data/1839341/000119312526165121/d149019dex992.htm
- id: 13
  title: Applied Digital 8-K, "Polaris Forge 1 Lease — 400 MW / ~$11B to CoreWeave," August 29, 2025
  url: https://www.sec.gov/Archives/edgar/data/1144879/000149315225012458/ex99-1.htm
- id: 14
  title: Applied Digital Q3 FY2026 earnings release, filed April 8, 2026 (ELN-02 operational; $185M LoC)
  url: https://www.sec.gov/Archives/edgar/data/1144879/000114487926000029/apldq326earningsrelease.htm
- id: 15
  title: CoreWeave pricing page (May 2026 snapshot)
  url: https://www.coreweave.com/pricing
- id: 16
  title: AWS EC2 p5 / p5en / p6 instance pricing (via Vantage). [p5.48xlarge](https://instances.vantage.sh/aws/ec2/p5.48xlarge),
    [p5en.48xlarge](https://instances.vantage.sh/aws/ec2/p5en.48xlarge),
  url: https://instances.vantage.sh/aws/ec2/p6-b200.48xlarge
- id: 18
  title: Google Cloud GPU pricing
  url: https://cloud.google.com/compute/gpus-pricing
- id: 19
  title: Nebius compute pricing
  url: https://nebius.com/prices
- id: 20
  title: Crusoe Cloud pricing
  url: https://crusoe.ai/cloud/pricing
- id: 21
  title: Lambda GPU Cloud pricing
  url: https://lambda.ai/service/gpu-cloud
- id: 22
  title: SemiAnalysis, "AI Neocloud Playbook and Anatomy."
  url: https://newsletter.semianalysis.com/p/ai-neocloud-playbook-and-anatomy
- id: 23
  title: Silicon Data, "H100 Rental Price Over Time."
  url: https://www.silicondata.com/blog/h100-rental-price-over-time
- id: 24
  title: Kerrisdale Capital, "CoreWeave — Artificial Returns" (short report), September 2025
  url: https://www.kerrisdalecap.com/wp-content/uploads/2025/09/Kerrisdale-CoreWeave.pdf
- id: 25
  title: 'CNBC, "The question everyone in AI is asking: How long before a GPU depreciates?" November 14,
    2025'
  url: https://www.cnbc.com/2025/11/14/ai-gpu-depreciation-coreweave-nvidia-michael-burry.html
- id: 26
  title: 'Yahoo Finance, "Nvidia''s Depreciation Time Bomb: Jim Chanos Warns of ''Massive Financial Risk''
    for CoreWeave, Oracle," December 17, 2025'
  url: https://finance.yahoo.com/news/nvidias-depreciation-time-bomb-jim-003106193.html
- id: 27
  title: Alphabet Inc. Form 10-K for FY2025
  url: https://s206.q4cdn.com/479360582/files/doc_financials/2025/q4/GOOG-10-K-2025.pdf
- id: 28
  title: Microsoft Corp. Form 10-K for FY ended June 30, 2025, filed July 30, 2025
  url: https://www.sec.gov/Archives/edgar/data/789019/000095017025100235/msft-20250630.htm
- id: 29
  title: Meta Platforms Form 10-K for FY2025
  url: https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm
- id: 30
  title: Amazon.com Form 10-K for FY2025
  url: https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm
- id: 31
  title: TechCrunch, "Sam Altman says OpenAI has $20B ARR and about $1.4 trillion in data center commitments,"
    November 6, 2025
  url: https://techcrunch.com/2025/11/06/sam-altman-says-openai-has-20b-arr-and-about-1-4-trillion-in-data-center-commitments/
- id: 32
  title: Bloomberg, "OpenAI Valued at $852 Billion After Completing $122 Billion Round," March 31, 2026
  url: https://www.bloomberg.com/news/articles/2026-03-31/openai-valued-at-852-billion-after-completing-122-billion-round
- id: 33
  title: Microsoft Official Blog, "The next chapter of the Microsoft–OpenAI partnership," October 28,
    2025
  url: https://blogs.microsoft.com/blog/2025/10/28/the-next-chapter-of-the-microsoft-openai-partnership/
- id: 34
  title: Nvidia Form 10-Q for quarter ended October 26, 2025
  url: https://www.sec.gov/Archives/edgar/data/1045810/000104581025000230/nvda-20251026.htm
- id: 35
  title: Nvidia / OpenAI, "Strategic Partnership to Deploy 10 GW of NVIDIA Systems," September 22, 2025
  url: https://nvidianews.nvidia.com/news/openai-and-nvidia-announce-strategic-partnership-to-deploy-10gw-of-nvidia-systems
- id: 36
  title: CNBC, "Anthropic to spend $30B with Microsoft Azure on Nvidia chips, gets investment from both,"
    November 18, 2025
  url: https://www.cnbc.com/2025/11/18/anthropic-ai-azure-microsoft-nvidia.html
- id: 38
  title: StockAnalysis.com CRWV quote page (May 2026)
  url: https://stockanalysis.com/stocks/crwv/
- id: 41
  title: CoreWeave Q3 2025 earnings deck (powered-shell delay disclosure)
  url: https://s205.q4cdn.com/133937190/files/doc_financials/2025/q3/Earnings-Deck-2025-Q3.pdf
- id: 42
  title: 'Lawrence Berkeley National Laboratory, "Queued Up: 2025 Edition."'
  url: https://eta-publications.lbl.gov/sites/default/files/2025-12/queued_up_2025_edition_12.15.2025.pdf
- id: 43
  title: Rocky Mountain Institute, "PJM's Speed-to-Power Problem and How to Fix It."
  url: https://rmi.org/pjms-speed-to-power-problem-and-how-to-fix-it/
- id: 44
  title: ERCOT System Planning and Weatherization Update, December 2, 2025
  url: https://www.ercot.com/files/docs/2025/12/02/16.2-System-Planning-and-Weatherization-Update_Revised.pdf
- id: 47
  title: Grist (citing Cleanview), "Behind-the-meter natural gas powering AI data centers," February 2026
  url: https://grist.org/energy/data-centers-natural-gas-methane-behind-the-meter/
- id: 48
  title: Amazon, "AWS activates Project Rainier, its compute cluster powered by AWS Trainium2 chips."
  url: https://www.aboutamazon.com/news/aws/aws-project-rainier-ai-trainium-chips-compute-cluster
- id: 49
  title: Anthropic, "Expanded compute partnership with Amazon."
  url: https://www.anthropic.com/news/anthropic-amazon-compute
- id: 50
  title: Anthropic, "Partnership with Google and Broadcom on TPU compute."
  url: https://www.anthropic.com/news/google-broadcom-partnership-compute
- id: 51
  title: Google Cloud blog, "Ironwood TPUs and new Axion-based VMs for your AI workloads."
  url: https://cloud.google.com/blog/products/compute/ironwood-tpus-and-new-axion-based-vms-for-your-ai-workloads
- id: 52
  title: Tom's Hardware, "OpenAI and Broadcom to finalize custom AI processor in the coming months."
  url: https://www.tomshardware.com/tech-industry/artificial-intelligence/openai-and-broadcom-to-finalize-custom-ai-processor-in-the-coming-months-say-industry-sources
- id: 53
  title: Meta Newsroom, "Expanding Meta's custom silicon to power our AI workloads," March 2026
  url: https://about.fb.com/news/2026/03/expanding-metas-custom-silicon-to-power-our-ai-workloads/
- id: 54
  title: The Next Platform, "Microsoft Takes On Other Clouds With Braga Maia 200 AI Compute Engines,"
    January 28, 2026
  url: https://www.nextplatform.com/ai/2026/01/28/microsoft-takes-on-other-clouds-with-braga-maia-200-ai-compute-engines/4092134
- id: 55
  title: CoreWeave 8-K, Nvidia residual-capacity backstop / Sep 9, 2025 order form (under MSA dated April
    10, 2023)
  url: https://www.sec.gov/Archives/edgar/data/1769628/000176962825000047/crwv-20250909.htm
- id: 56
  title: Nvidia press release, "NVIDIA and CoreWeave Strengthen Collaboration to Accelerate Buildout of
    AI Factories" (announcing $2B PIPE, Jan 2026)
  url: https://nvidianews.nvidia.com/news/nvidia-and-coreweave-strengthen-collaboration-to-accelerate-buildout-of-ai-factories
- id: 57
  title: Moody's Ratings, "Moody's assigns A3 to CoreWeave Compute Acquisition Co. VIII, LLC" (rating
    action), March 2026
  url: https://ratings.moodys.com/ratings-news/462400
- id: 58
  title: S&P Global Ratings, "CoreWeave Outlook Revised To Positive, 'B+' Rating Affirmed," April 9, 2026
  url: https://www.spglobal.com/ratings/en/regulatory/article/-/view/type/HTML/id/3543327
- id: 60
  title: CoreWeave investor relations, "CoreWeave Announces Pricing of $1,000 million of 9.750% Senior
    Notes due 2031," April 2026
  url: https://investors.coreweave.com/news/news-details/2026/CoreWeave-Announces-Pricing-of-1000-million-of-9-750-Senior-Notes-due-2031/default.aspx
- id: 61
  title: CNBC, "CoreWeave (CRWV) Q1 2026 earnings report," May 7, 2026
  url: https://www.cnbc.com/2026/05/07/coreweave-crwv-q1-earnings-report-2026.html
- id: 62
  title: Semafor, "Microsoft chose not to exercise $12 billion CoreWeave option," March 20, 2025
  url: https://www.semafor.com/article/03/20/2025/microsoft-chose-not-to-exercise-12-billion-coreweave-option
- id: 64
  title: OpenAI, "Announcing the Stargate Project."
  url: https://openai.com/index/announcing-the-stargate-project/
:::
