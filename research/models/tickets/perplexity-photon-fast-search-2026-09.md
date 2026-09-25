---
slug: perplexity-photon-fast-search-2026-09
title: Perplexity Fast Search — Photon, a Rust retrieval/ranking engine built by agent loops
company: Perplexity
model: Photon (retrieval + ranking engine)
status: released
status_note: |
  **Shipped, 2026-09-24 18:07 UTC, primary.** @perplexity_ai: "Introducing Fast
  Search in the Perplexity Search API. Fast Search runs on Photon, our new
  Rust-based retrieval and ranking service that we built with a small team of
  engineers and hundreds of agents. It returns 95% of search results in 230 ms
  or less." @AravSrinivas (CEO, 18:50 UTC) adds the competitive claim:
  "Perplexity has the fastest and most capable Search API... achieving
  sub-250ms p95 latency while still ranking highly on relevance and accuracy
  benchmarks."

  **The claim worth separating from the product.** Both posts say Photon was
  built by a small team plus "hundreds of agents" / "hundreds of auto-research
  loops powered by a more capable internal version of Perplexity Computer".
  That is a first-party assertion about AI-authored production infrastructure,
  made by the party that benefits from it, with no artifact — no commit
  history, no team size, no ablation. The latency number is checkable by any
  API customer; the authorship claim is not checkable at all. They should not
  be believed at the same strength.

  **What `released` covers.** Fast Search is live in the Perplexity Search API
  now, which clears the bar. `Photon` is infrastructure, not a model, and is
  named here because it is what the ticket's claims attach to.

  **Benchmark context, one day later.** @kimmonismus (2026-09-25) reports
  Artificial Analysis data putting a competitor, Octen, at 0.21s per query and
  "the only Search API in the top 3 for quality, speed and search cost", on
  Sept 8 data. That is a pre-Photon snapshot and therefore not a rebuttal — but
  it establishes that an independent arbiter for this exact claim exists, which
  is where "fastest and most capable" should be settled.

  **Relationship to other Perplexity tickets.** Distinct from
  [[perplexity-portable-computer-2026-08]] (local agent runtime) and
  [[perplexity-wilson-hire-2026-08]]; the internal "more capable Perplexity
  Computer" referenced as the build tool is the same product line, used here as
  an engineering input rather than shipped.
expected: "Fast Search live in the Perplexity Search API. Open: an independent latency and relevance measurement — Artificial Analysis already runs this category — against the sub-250ms p95 and 'fastest and most capable' claims; pricing; and any substantiation at all for the 'built by hundreds of agents' authorship claim."
labels:
  - perplexity
  - search-api
  - infrastructure
  - agentic-engineering
  - released
verification: confirmed
sources:
  - https://x.com/perplexity_ai/status/2103184653373014509
  - https://x.com/AravSrinivas/status/2103195385804238972
  - https://x.com/kimmonismus/status/2103322857082408967
created_at: 2026-09-25
updated_at: 2026-09-25
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-25
    change: "Created — RELEASED. @perplexity_ai announced Fast Search in the Perplexity Search API on 2026-09-24 18:07 UTC (~413 likes), running on Photon, a new Rust-based retrieval and ranking service returning 95% of results in 230ms or less; @AravSrinivas (CEO, 18:50 UTC, ~155 likes) claimed 'the fastest and most capable Search API' at sub-250ms p95 while 'ranking highly on relevance and accuracy benchmarks'. Status released and verification confirmed — vendor primary, product live. The ticket deliberately splits two claims that arrived together: the LATENCY figure, which any API customer can measure, and the AUTHORSHIP claim that Photon was built by 'a small team of engineers and hundreds of agents' / 'hundreds of auto-research loops powered by a more capable internal version of Perplexity Computer', which is first-party, self-serving, and backed by no commit history, team size or ablation. Only the first is treated as established. Context recorded but explicitly not as rebuttal: @kimmonismus (2026-09-25) relays Artificial Analysis Sept-8 data placing competitor Octen at 0.21s/query and the only Search API top-3 on quality, speed and cost — a pre-Photon snapshot, but proof that an independent arbiter for the 'fastest and most capable' claim exists. Distinct artifact from [[perplexity-portable-computer-2026-08]]."
---

The product claim here is ordinary and verifiable. The claim underneath it is
neither, and it is the one that will get repeated.

"We built a production retrieval engine with a small team and hundreds of
agents" is, if true, one of the more concrete data points anyone has offered on
AI-authored infrastructure at scale. It is also exactly the kind of statement
that cannot be checked from outside, made by a company whose product is the
agent doing the building. There is no repository, no measure of what fraction
of Photon the agents wrote, and no counterfactual. Treat it as a marketing
assertion until Perplexity publishes something with a denominator in it.

The latency number, by contrast, is a good claim precisely because it is
falsifiable. Sub-250ms p95 on a live API is something any customer can
instrument, and Artificial Analysis already benchmarks this category — their
early-September data had a different vendor leading on the same axes. A
head-to-head after Photon is the thing to wait for, and it will arrive on its
own.

The strategic read is that search infrastructure is becoming a latency market.
Agent loops make many more queries than humans do and block on each one, so
p95 latency compounds into agent wall-clock in a way it never did for a human
typing into a box. Shipping a Rust rewrite whose headline feature is speed
rather than relevance is Perplexity pricing for that customer.
