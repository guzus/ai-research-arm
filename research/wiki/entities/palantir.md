---
slug: palantir
title: Palantir Technologies
type: entity
aliases: ["Palantir", "PLTR", "Palantir Technologies Inc.", "Alex Karp", "Maven Smart System"]
tags: [enterprise-ai, government, earnings, public-company, ai-sovereignty]
description: US enterprise/government data-analytics company; a Bloomberg investigation said CENTCOM users of Palantir's Maven Smart System recommended a stale IRGC catalog entry, contributing to a strike on a Minab elementary school.
created_at: 2026-08-04
timestamp: 2026-09-23T00:00:00Z
market:
  ticker: PLTR
  exchange: NASDAQ
  symbol: NASDAQ:PLTR
  provider: yahoo
sources:
  - {title: "ARA daily digest 2026-09-23", path: research/digest/2026-09-23-digest.md}
  - {title: "ARA daily digest 2026-09-15", path: research/digest/2026-09-15-digest.md}
  - {title: "ARA daily digest 2026-08-04", path: research/digest/2026-08-04-digest.md}
  - {title: "Palantir FY26Q2 8-K (accession 0001321655-26-000039), EX-99.1 press release", url: "https://www.sec.gov/Archives/edgar/data/1321655/000132165526000039/a2026q2ex991pressrelease.htm", date: 2026-08-03}
---

**Palantir Technologies** is the US enterprise and government data-analytics
company that has become the loudest vendor case for *not* deploying frontier
models directly. Its **FY26Q2** results (8-K filed 2026-08-03) are the first
Palantir quarter tracked in this wiki and the single issuer earnings report in
the 2026-08-04 digest cycle.

## FY26Q2 (reported 2026-08-03)

| Metric | Value |
|---|---|
| Revenue | **$1.935B**, +93% YoY, +19% QoQ |
| GAAP net income | **$1.062B** (55% margin) |
| GAAP / adjusted EPS | $0.41 / $0.41 |
| Adjusted free cash flow | $1.220B |
| Rule of 40 | 155% |
| Next-quarter revenue guide | $2.160–$2.164B |

## Why it matters

- **93% growth is the clearest public read on AI budget conversion.** Most of
  the [[ai-capex]] story is spend by hyperscalers on their own capacity;
  Palantir's line is revenue booked from enterprises and governments buying
  deployed AI. A 55% GAAP net margin at that growth rate is unusual enough
  that the quarter functions as a demand data point rather than a company one.
- **The "don't trust the labs" thesis is the tracking-worthy part.** CEO Alex
  Karp used the results to argue frontier labs are too untrustworthy for
  enterprise deployment, then called the AI industry **"Marxist"** to
  TechCrunch in the same news cycle. This is competitive positioning from the
  vendor selling the alternative — but "enterprises won't hand their data to
  [[openai]] or [[anthropic]] directly" is a falsifiable claim about market
  structure, not just rhetoric.
- **The sovereignty framing lands on a policy date.** Karp's quoted line —
  *"Their competitive advantage should never become the training data for
  future models"* — was filed the same day the White House prepared to show
  frontier labs a voluntary pre-release model submission framework (see
  [[federal-ai-policy]]). Data control as a product and data control as a
  regulatory question surfaced in the same 24 hours.

## Fable restricted over 30-day safety logging (2026-09-15)

Palantir, [[nvidia]] and Booz Allen
**restricted [[anthropic]]'s [[claude-fable-5|Fable]]**
for sensitive work over **data-retention terms**,
not model quality. The mechanism is the rolling
**30-day safety logging** Anthropic introduced in
June; the customer-managed-logs option can still
be revoked, which is why Palantir's stated bar is
the word **"irrevocable."** This is the first
named-customer enforcement of the "don't trust the
labs" thesis this page opened on — a procurement
bar, not a benchmark result (The Information via
@kimmonismus, @rohanpaul_ai; ARA daily digest
2026-09-15).

## Pentagon cites AI overreliance in the Minab school strike (2026-09-23)

- **A Bloomberg investigation reported that
  CENTCOM users leaned on Palantir's Maven
  Smart System**, which recommended a site
  still cataloged as an IRGC facility from
  outdated targeting data. Two Tomahawks
  hit Shajarah Tayyebeh Elementary School
  in Minab on the opening day of the Iran
  war, killing more than **150 people**
  including at least **123 children**.
  Bloomberg's sources stack three failures
  — overreliance, bad intelligence, and
  stale satellite imagery — and report
  civilian-harm-mitigation staffing down
  **~90%** across DoD, with CENTCOM's team
  cut from **10 people to 1**. Palantir
  said it "is not responsible for the
  underlying data nor identifying
  intelligence deficiencies." Hacker News
  carried the item at **314 points**. This
  is the first named combat use of a
  Palantir targeting stack in this wiki;
  hold at investigation strength. See
  [[federal-ai-policy]] and
  [[agentic-ai-security]] (Bloomberg via
  HN; ARA daily digest 2026-09-23).

## Open questions

- **Is the growth AI-attributable or bookings-cycle-attributable?** The
  company frames it as AI demand; the filing reports revenue, not attribution.
- **Does the anti-lab thesis hold as labs ship enterprise deployment
  themselves?** Both [[openai]] and [[anthropic]] are selling into the same
  accounts.
- **Does the "Marxist" framing cost anything commercially?** Palantir's buyer
  set is unusually tolerant of its CEO's public positioning; that is itself
  the thing to watch if it changes.
