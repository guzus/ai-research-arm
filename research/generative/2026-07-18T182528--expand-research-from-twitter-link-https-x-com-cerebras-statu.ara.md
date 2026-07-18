---
eyebrow: ENGINEERING · ENTERPRISE AI
title: Cerebras opens its company brain — and reveals the build-vs-buy war eating enterprise AI search
deck: A freshly public, margin-strained chip company just published a rigorously-cited blueprint for the internal knowledge base its 15,000-questions-a-day engineering culture runs on. The architecture mostly holds up to scrutiny. The more interesting story is what building it in-house, rather than buying it, says about a market where the leading vendor just marked a $7.2B valuation on tripling revenue.
lede: |
  On July 16, 2026, Cerebras Systems — ten weeks removed from a $5.55B Nasdaq debut and three weeks removed from a margin-guidance stock selloff — published a long, technically dense engineering post titled "How We Built Our Knowledge Base." [^1] It describes a single Postgres table, a hybrid retrieval stack citing five external research papers, an agentic planner-executor-synthesis query pipeline exposed to Claude Code over the Model Context Protocol, and one blunt number: employees, automations, and agents ask it more than 15,000 questions a day. [^1] The post is a genuinely good piece of engineering writing. It is also, on close inspection, a case study in almost every live tension in enterprise AI infrastructure right now — RAG versus agentic search, Postgres versus dedicated vector databases, and build versus buy in a market where the category leader, Glean, just told investors its revenue tripled to roughly $300M. [^28]
stats:
  - {label: Daily KB queries, value: "15,000+", note: "3 months post-launch"}
  - {label: CocoIndex age at adoption, value: "~15 mo.", note: "single-founder OSS project"}
  - {label: Glean valuation, value: "$7.2B", note: "Jun 2025, unpriced since"}
  - {label: Cerebras market cap, value: "$47.9B", note: "Jul 17, 2026, -50% from IPO peak"}
---

:::kv
- {term: What it is, def: "An internal, agentic RAG system — Slack, code, and custom-DB search unified in one Postgres table, queried 15,000+ times a day"}
- {term: The claim, def: "Hybrid retrieval (full-text + embeddings + IDF + age decay), RRF fusion, MCP-exposed tools for Claude Code"}
- {term: What checks out, def: "Every cited paper is real; RRF, HNSW, and Contextual Retrieval are correctly represented"}
- {term: What's thinner than it looks, def: "The chunking engine is Cerebras's own code, not CocoIndex's advertised feature; the 'top 10' cutoff isn't empirically derived from the cited paper"}
- {term: The bigger story, def: "Cerebras built rather than bought — while Glean, the obvious buy, just tripled ARR to ~$300M on a $7.2B mark"}
:::

## 01. What Cerebras actually built

Strip away the storytelling and the architecture is legible: one Postgres table holds embeddings, LLM-generated summaries, and metadata from every source — Slack threads, code repositories, and team-contributed custom databases — with a Postgres GIN index handling full-text search alongside a vector index for semantic matching. [^1] Slack ingestion runs on Socket Mode (a persistent WebSocket connection that sidesteps the Web API's rate limits), and on any new message the system re-fetches the entire thread and re-embeds it as one unit rather than indexing isolated messages. [^1]

:::stats
- {label: Embedding dimensions, value: "3,072"}
- {label: RRF constant, value: "k=60", note: "Cormack et al., 2009"}
- {label: Reranked results kept, value: "10", note: "of many candidates, scored 0–10"}
- {label: Named query tools, value: "6", note: "search, search_slack, search_code, recent_prs, who_knows, subsystem_index"}
:::

Two design choices carry the most engineering weight. First, "distillation": before anything is embedded, an LLM converts raw Slack threads into structured JSON with explicit fields — question, summary, resolution, systems, code references — because, in the company's words, "accuracy increased significantly when the thread was normalized into a consistent format." [^1] Second, "bursting": consecutive messages from one author get grouped, prepended with the thread topic, and embedded as a separate unit if they clear a bar of at least 200 combined characters, a rare token with inverse-document-frequency ≥4.0, and social-signal reactions — a heuristic aimed at surfacing buried high-signal replies that a naive one-message-per-embedding scheme would miss. [^1]

Retrieval itself runs a planner-executor-synthesis loop: an LLM planning pass picks tools and sources from a compact index description, an executor fans those out in parallel, and a synthesis pass writes a cited, caveat-aware answer from the normalized results. [^1] The fusion step uses Reciprocal Rank Fusion — SCORE(D) = Σ 1/(60 + rank) — to merge ranked lists from different retrieval methods before a small reranker model scores survivors 0–10 and keeps the top ten, which then get re-expanded with neighboring context (adjacent wiki sections, sibling code chunks) to restore continuity that chunking severed. [^1] The retrieval primitives — `search`, `search_slack`, `search_code`, `recent_prs`, `who_knows` — are exposed as narrow, LLM-free Model Context Protocol tools, with Claude Code (or any MCP-compatible agent) serving as the orchestration layer on top. [^1]

:::callout(kind=info, label="Scope note")
Cerebras's own post carries no visible byline date; the publish window is reconstructed from the tweet timestamp (July 16, 18:27 UTC) and subsequent social promotion, and the "3 months since launch" figure is the company's own framing, not independently timestamped. [^1][^2]
:::

## 02. The citations mostly check out — with two honest asterisks

A post this citation-heavy invites a citation audit, and it survives one better than most vendor engineering blogs. Both Reciprocal Rank Fusion and HNSW are correctly and precisely attributed: the RRF formula traces to Cormack, Clarke, and Büttcher's 2009 SIGIR paper (DOI 10.1145/1571941.1572114), and k=60 is genuinely that paper's own recommended constant — though the original data shows mean average precision barely moving across k∈[10,100], meaning 60 is a robust default sitting in a flat plateau, not a razor-tuned optimum. [^3][^4] Both Elasticsearch and OpenSearch ship RRF with k=60 as their own default, which is real corroboration that this is now standard production practice rather than an academic curiosity. [^5] It is not, however, uncontested: a peer-reviewed 2022 critique in ACM TOIS shows a tuned convex combination of normalized scores can beat RRF within a single domain, with RRF's actual edge being zero-shot robustness across mismatched retrievers — not a proven accuracy ceiling. [^6] The HNSW citation (arXiv:1603.09320, Malkov and Yashunin) checks out exactly, and the algorithm is indeed the one underlying pgvector's HNSW index and most other production vector search — Milvus, Qdrant, Chroma, ClickHouse, Redis, and Lucene all implement it too. [^7][^8]

Anthropic's "Introducing Contextual Retrieval" is also faithfully represented: contextual embeddings alone cut top-20-chunk retrieval failures 35% (5.7%→3.7%), stacking contextual BM25 gets to 49%, and adding a final reranking pass — the step Cerebras's own pipeline includes — gets to 67%. [^9] Cerebras's LLM-distillation-before-embedding step is a direct, credited descendant of that technique.

The two research-paper citations attached to the retrieval pipeline's shape hold up less precisely. Li et al.'s "Search-o1" (arXiv:2501.05366) genuinely proposes an agentic RAG loop plus a document-distillation module for reasoning models, and Cerebras's planner-emits-tools/executor-fans-out-in-parallel pattern is a legitimate, if loosely-named, descendant of that idea. [^10] Liu et al.'s "Lost in the Middle" (arXiv:2307.03172) is real and its core finding is stark — accuracy on 20-document multi-document QA falls from roughly 75% when the answer sits first, to around 55% when it's buried in the middle, before recovering to about 72% when it's last. [^11][^12]

:::bar-chart(title="Answer-position accuracy, multi-document QA", subtitle="Liu et al. 2023, approximate figures reported in follow-on analysis", orientation=horizontal, value-unit="", value-suffix="%")
categories: Answer first, Answer middle, Answer last
Accuracy: 75, 55, 72
:::

That U-shaped curve is real, and it is a legitimate reason to prefer fewer, better-ranked documents over dumping everything into context. But the paper never derives an optimal cutoff — nothing in Liu et al.'s experiments tests or recommends "keep the top 10." [^11] Cerebras's specific number is a defensible internal choice consistent with the paper's spirit, dressed with more citation authority than the underlying data actually provides — a small but real gap between "directionally grounded" and "empirically derived."

## 03. CocoIndex: fifteen months old, one founder, forty gigabytes of proprietary code

The post credits CocoIndex, described as "an open-source document embedding framework," for the incremental, per-commit re-embedding that keeps code search fresh across repositories the company says exceed 40GB. [^1] CocoIndex is real — an Apache-2.0, Rust-core project with 10.9k GitHub stars, 833 forks, and 211 releases — and its central claim (re-embed only the chunks a commit actually changed, tracked via Postgres-stored sync metadata) is independently documented, not a Cerebras invention. [^13] That specific capability is architecturally distinct from the naive full-recompute pipelines most teams start with, and it is a legitimate reason to choose the tool.

:::timeline
- {date: 2024, headline: "CocoIndex founded", body: "By Linghua Jin, an ex-Google engineer, per third-party company-tracker data; reportedly unfunded."}
- {date: 2025-04, headline: "First public Show HN launch", body: "Positioned as an incremental data-freshness engine for AI agents."}
- {date: 2025-05, headline: "Early PyPI releases, including a yanked build", body: "Rapid iteration; API still settling."}
- {date: 2026-07, headline: "Cerebras discloses production use", body: "~15 months after public launch, on repositories exceeding 40GB."}
:::

What the post elides is scale of adoption elsewhere: CocoIndex's own enterprise marketing page lists no named customers or case studies, so the "credible enough for 40GB+ production code" claim currently rests on Cerebras's word alone, with no corroborating deployment from the vendor's side. [^14][^15] And the flashiest specific claim — "language-aware chunking" that tries class boundaries first, then methods, then smaller blocks — turns out, on a close read of Cerebras's own text, to be a custom regex-boundary splitter the company built itself, not the Tree-sitter/AST-based chunker CocoIndex advertises as a first-class feature. [^1][^13] CocoIndex supplies the incremental sync engine; Cerebras supplies the chunking logic riding on top of it. That's a reasonable architectural division of labor, but it's a narrower claim than "we adopted an open-source framework that does language-aware chunking" implies.

None of this means the choice is wrong — plenty of durable infrastructure started this young, and delta-only re-embedding is a real, valuable property regardless of the vendor's age. It does mean a frontier AI hardware company is trusting a sub-two-year-old, apparently single-founder project with the freshness pipeline over its proprietary source code, a dependency-risk fact the post itself never surfaces.

## 04. One Postgres table: the QPS math that defangs most of the skepticism

"A single Postgres table for embeddings, summaries, and metadata from everything" is the kind of line that reads as either admirably simple or dangerously naive, depending on how skeptical the reader already is of relational databases doing vector search. The math resolves it faster than the architecture debate does: 15,000 queries a day averages to roughly 0.17 queries per second, and even a generous 50x peak-hour concentration factor lands under 9 QPS. [^1] Independent pgvector-versus-dedicated-vector-database benchmarks report meaningful divergence in the hundreds-to-tens-of-thousands-of-QPS range — Cerebras's actual load, as disclosed, isn't close to that regime. The genuinely open variable is corpus size (total embedded rows), which the post never states — "some repositories larger than 40GB" describes a subset, not the aggregate table size.

Where hard numbers exist, they favor pgvector more than the "Postgres can't really do this" narrative suggests. A vendor benchmark from Tiger Data (maker of the pgvectorscale extension) reported 471.57 QPS at 99% recall on 50 million 768-dimension vectors, versus 41.47 QPS for Qdrant on the same hardware class — an 11.4x throughput edge, though Qdrant held a 39–48% latency advantage at that same recall target. [^17] Supabase's earlier benchmark of pgvector's HNSW index (added in v0.5.0, released August 2023) found more than 6x the throughput of the prior IVFFlat index at 0.99 accuracy@10, closing most of the historical gap with dedicated vector stores at moderate scale. [^18][^21] Real production migrations run in the direction the skeptics wouldn't expect: both Confident AI and Firecrawl reportedly moved workloads from Pinecone to Postgres/pgvector, citing roughly $250/month versus $675/month at 10 million vectors. [^20]

The honest counter-evidence is a named practitioner critique arguing HNSW in Postgres carries real operational costs at scale that vendor benchmarks tend to understate — elevated memory (10+ GB for a few-million-vector index), slow index builds, and write-lock contention under heavy ingestion — while noting that most public pgvector benchmarks, including the vendor-published ones above, lean on toy-scale demonstrations rather than rigorous production data. [^19] Every benchmark cited here that shows pgvector winning was published by a company selling Postgres infrastructure (Tiger Data, Supabase); the skeptical counterpoint has no comparable commercial backer and, tellingly, cites no hard numbers of its own. [^17][^18][^19] Given Cerebras's actual disclosed query volume, the single-table design reads less like a bold simplification and more like a correctly-scoped decision for a workload that was never going to stress the architecture in the first place — the caveat is that nobody outside Cerebras can verify that from the numbers published.

## 05. MCP, agentic search, and whether classic RAG is already the wrong model

Exposing retrieval tools over the Model Context Protocol places Cerebras inside a genuinely fast-moving standardization story, not a proprietary integration choice. MCP shipped from Anthropic in November 2024; by March 2026 its SDK was reportedly seeing roughly 97 million monthly downloads, up from about 100,000 in its first month, and in December 2025 Anthropic donated protocol governance to a new Agentic AI Foundation under the Linux Foundation, with AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, and OpenAI all seated as Platinum members. [^22][^23][^24] A Stacklok 2026 survey — cited specifically because it corrects an earlier, unsourced 78% figure that had circulated — puts real production MCP adoption at 41% among surveyed software organizations, a meaningfully lower but still substantial number. [^24] MCP-exposed tools for Claude Code, as Cerebras describes, is now a documented industry pattern rather than a novelty.

:::stats
- {label: MCP SDK downloads, value: "~97M/mo", note: "Mar 2026, from ~100K in Nov 2024"}
- {label: Production adoption, value: "41%", note: "Stacklok 2026 survey, software orgs"}
- {label: AAIF Platinum members, value: "8", note: "incl. AWS, Google, Microsoft, OpenAI"}
:::

Where the story gets genuinely contested is whether the retrieval pattern underneath those MCP tools — hybrid search, RRF, reranking, the whole classic-RAG apparatus — is even the right long-term architecture. Anthropic's own Claude Code team ran the experiment and abandoned it: "Early versions of Claude Code used RAG + a local vector db, but we found pretty quickly that agentic search generally works better," Claude Code's lead Boris Cherny wrote, describing a move toward grep-and-glob-style agentic file search over a persistent vector index. [^25] That's a direct, primary-source data point for the "RAG is dying" camp, from the team building one of the most widely deployed coding agents. The counter-argument is economic and empirical rather than rhetorical: retrieval remains roughly three orders of magnitude cheaper per query than long-context brute force at production volume, and "Lost in the Middle"-style degradation doesn't disappear just because the context window got bigger. [^11][^26] A VentureBeat enterprise-buyer tracker found intent to adopt hybrid retrieval architectures — not pure vector RAG, not pure agentic search — roughly tripled from 10.3% to 33.3% between January and March 2026, alongside a similar rise in custom in-house retrieval stacks. [^27]

Cerebras's own architecture is, read carefully, evidence for that synthesis rather than a clean win for either extreme: the post states plainly that after testing pure vector search, the team "quickly realized that vector search alone was insufficient for matching all relevant data" — which is precisely why the final system fuses full-text search, embeddings, IDF filtering, and age decay rather than picking one retrieval mode. [^1] Cerebras built a hybrid system in mid-2026, at the exact moment enterprise buying intent was swinging toward hybrid systems — less a contrarian architecture and more a company arriving at the same conclusion the broader market was converging on simultaneously.

## 06. The Glean-shaped hole in the build decision

Nowhere does Cerebras's post mention whether buying was ever seriously considered, but the comparison is unavoidable: Glean, the category-defining enterprise AI-search vendor, priced a $150M Series F at a $7.2B valuation in June 2025 — up from $4.6B nine months earlier — and has since reported ARR crossing $200M by December 2025 and roughly $300M by May 2026, tripling in fifteen months. [^28][^29][^30][^31]

:::line-chart(title="Glean annualized revenue, trailing 18 months", subtitle="Company-disclosed figures", y-unit=$)
x: ~2025-02,2025-12,2026-05
Glean ARR ($M): 100,200,300
:::

That growth curve makes "why not just buy Glean" a fair question, and the honest answer is that the comparison is weaker than the valuation numbers suggest. Glean's own technical disclosure is thin relative to what Cerebras just published: the most detailed public description of Glean's retrieval stack — a BM25-and-dense-vector hybrid fused with RRF under a knowledge graph — traces back through several layers of secondary blog synthesis to a single April 2023 podcast conversation with a former Glean engineer, not a company engineering blog or technical whitepaper. [^32][^33] Glean has never published anything resembling the level of architectural detail Cerebras just did. And Glean's go-to-market is built for a different scale problem: reported initial contract values run $100K–$500K annually for organizations above roughly 500 employees, with Fortune 500 deals clearing $5M, and named customers like Databricks, Reddit, Pinterest, and Samsung skew toward broad knowledge-worker search rather than the engineering-team-scale, code-heavy internal tool Cerebras describes. [^34] Buying Glean would have solved a workplace-search problem Cerebras may not have primarily had.

The build-versus-buy literature that exists is thin and not neutral: the most-cited statistic — that vendor-partner enterprise AI deployments succeed roughly twice as often as in-house builds (67% versus 33%), drawn from an MIT "GenAI Divide" study reporting 95% of enterprise GenAI pilots fail to show P&L impact — is relayed to the public specifically through Glean's own marketing, a vendor with an obvious stake in the "buy" conclusion. [^35] A credible open-source middle path exists and is already in real production: Onyx (formerly Danswer), MIT-licensed and self-hosted, reports usage at Ramp (115,000 queries/month), Thales (1,400 monthly active users across 82,000 employees), and an air-gapped deployment at UC San Diego (37,000+ users), with a managed cloud tier priced at $20 per user per month — a fraction of Glean's reported per-seat economics. [^36]

:::compare
- {role: LOWEST, name: "Onyx (self-hosted OSS)", value: "$20/user/mo"}
- {role: HIGHEST, name: "Glean (enterprise ACV)", value: "$100K–$500K/yr"}
- {role: SUBJECT, name: "Cerebras (in-house build)", value: "engineering time, no license fee"}
:::

Set against that spectrum, Cerebras's choice reads less like a snub of Glean specifically and more like a rational bet that a narrower, code-and-Slack-centric internal tool for an engineering-heavy company was cheaper to build than to buy at Glean's pricing tier — a decision every well-resourced engineering organization now faces as this market matures around it.

## 07. Why now: a hiring pitch timed to a rough quarter

The post closes with a hiring line for Cerebras's "AI/growth team," and the timing context makes that read as more than incidental. Cerebras priced its IPO at $185 a share on May 14, 2026, opened at $385, and closed its debut day at $311 — a peak that gave way to a post-IPO low of $160.81 on June 26, after CEO Andrew Feldman said the company's margin forecast had been "misunderstood" following its first earnings report as a public company. [^37][^38][^39] That report showed GAAP revenue of $193.4 million, up 94% year over year, against a GAAP operating loss of $15.0 million and gross margin near 45% — strong top-line growth paired with a margin story investors didn't like. [^39] By July 17, 2026 — the day before the knowledge-base post's social promotion peaked — the stock traded around $170.65, a roughly 50% market-cap decline from its debut-day peak. [^38]

:::compare
- {role: LOWEST, name: "Post-selloff low (Jun 26)", value: "$160.81"}
- {role: HIGHEST, name: "IPO-day peak (May 14)", value: "$386.34"}
- {role: SUBJECT, name: "As of Jul 17, 2026", value: "$170.65"}
:::

Two more pieces of context sharpen the timing. Cerebras's revenue remains heavily concentrated: 86% of 2025 revenue came from two UAE-linked entities, G42 (24%) and Mohamed bin Zayed University of AI (62%) — a structural risk the company itself discloses in filings, and one a credibility-signaling engineering post can help offset with a broader, technically sophisticated audience. [^40] And the competitive-inference-chip conversation moved fast around the same week: Nvidia announced a non-exclusive technology-licensing agreement absorbing Groq's inference IP on December 24, 2025, and rival SambaNova landed a $1B Series F at an $11B valuation on July 8, 2026 — eight days before this post — alongside a marquee win naming SambaNova as JPMorgan Chase's on-prem inference provider. [^41][^42]

Cerebras headcount data is directionally consistent with a genuine hiring push, not a freeze — third-party workforce tracking shows growth from roughly 358 employees in January 2024 to about 1,016 by December 2025 (+24% year over year), with active job postings up 38.4% over the same period. [^43] More specifically, Cerebras has an open "Developer Experience Engineer" role explicitly described in its own listing as the company's "engine for visibility and growth" — a near-exact match for the kind of hiring pitch a detailed engineering blog post is built to support. [^44] None of this proves the post was written primarily as a recruiting-and-IR instrument rather than a genuine act of engineering-culture transparency; Cerebras never states its motive. But the surrounding facts — a margin-driven stock decline, a live competitive threat, a persistent customer-concentration risk, and a named growth-recruiting function — all point the same direction, and none of them appear anywhere in the post itself.

## 08. What would break this thesis

The skeptical reading above rests on inference from timing, not a stated motive, and it could be wrong in a specific way: plenty of companies publish detailed engineering posts purely because a team is proud of the work, independent of stock price or hiring needs — Anthropic's own engineering blog and its 22-page internal-AI-usage document follow the same "here's what we actually built" genre with no IPO or margin story attached. [^45] If Cerebras publishes a second, third, and fourth post in this series over the next year regardless of its stock price, the opportunistic-timing read weakens considerably.

The architecture critique has a similar ceiling. Everything in Section 4's skepticism about "one Postgres table" is scoped to Cerebras's disclosed 15,000-queries-a-day load; if that number grows an order of magnitude as the tool becomes more embedded in daily workflows, the QPS math that currently defangs the concern stops applying, and the untested variable — total corpus size — becomes the binding constraint nobody can verify from outside. Similarly, CocoIndex's youth is a real dependency risk today, not a proof of eventual failure — plenty of foundational infrastructure (including Postgres itself, once) started as a small team's side project, and CocoIndex's 10.9k stars and near-daily release cadence show it maturing quickly, not stagnating. [^13]

Finally, this post's independent scrutiny is still thin by the nature of its youth: as of this research, no dedicated Hacker News discussion thread for "How We Built Our Knowledge Base" could be found, and reaction so far is limited to X/Twitter engagement — thousands of likes and bookmarks, praise from at least one named engineer at another AI infrastructure company, but no substantive independent technical critique yet surfaced in public. [^46] A post this citation-dense, from a company this newly public, will likely draw sharper scrutiny once practitioners have had more than 72 hours to read it closely — and that scrutiny, not this article, will be the real test of whether the architecture holds up at whatever scale comes next.

:::references
- {id: 1, title: "How We Built Our Knowledge Base", url: "https://www.cerebras.ai/blog/how-we-built-our-knowledge-base", source: "Cerebras Systems", date: "2026-07-16"}
- {id: 2, title: "Cerebras announcement tweet", url: "https://x.com/cerebras/status/2077822555159945507", source: "X / Cerebras", date: "2026-07-16"}
- {id: 3, title: "Reciprocal rank fusion outperforms Condorcet and individual rank learning methods", url: "https://dblp.org/rec/conf/sigir/CormackCB09.html", source: "SIGIR 2009 / DOI 10.1145/1571941.1572114", date: "2009"}
- {id: 4, title: "Reciprocal Rank Fusion", url: "https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion", source: "Elastic docs", date: "2026"}
- {id: 5, title: "Introducing Reciprocal Rank Fusion for hybrid search", url: "https://opensearch.org/blog/introducing-reciprocal-rank-fusion-hybrid-search/", source: "OpenSearch blog", date: "2026"}
- {id: 6, title: "A critical analysis of offline evaluation for rank fusion methods (RRF critique)", url: "https://dl.acm.org/doi/full/10.1145/3596512", source: "ACM TOIS", date: "2022"}
- {id: 7, title: "Efficient and robust approximate nearest neighbor search using HNSW graphs", url: "https://arxiv.org/abs/1603.09320", source: "arXiv:1603.09320 (Malkov & Yashunin)", date: "2016"}
- {id: 8, title: "pgvector", url: "https://github.com/pgvector/pgvector", source: "GitHub", date: "2026"}
- {id: 9, title: "Introducing Contextual Retrieval", url: "https://www.anthropic.com/news/contextual-retrieval", source: "Anthropic", date: "2024-09-19"}
- {id: 10, title: "Search-o1: Agentic Search-Enhanced Large Reasoning Models", url: "https://arxiv.org/abs/2501.05366", source: "arXiv:2501.05366 (Li et al.)", date: "2025-01-09"}
- {id: 11, title: "Lost in the Middle: How Language Models Use Long Contexts", url: "https://arxiv.org/abs/2307.03172", source: "arXiv:2307.03172 (Liu et al.)", date: "2023-07-06"}
- {id: 12, title: "Lost in the Middle (PDF, with position-accuracy figures)", url: "https://cs.stanford.edu/~nfliu/papers/lost-in-the-middle.arxiv2023.pdf", source: "Stanford NLP", date: "2023-11-20"}
- {id: 13, title: "cocoindex-io/cocoindex", url: "https://github.com/cocoindex-io/cocoindex", source: "GitHub", date: "2026-07-19"}
- {id: 14, title: "Show HN: CocoIndex – Open-Source Data framework for AI", url: "https://news.ycombinator.com/item?id=43772582", source: "Hacker News", date: "2025-04-24"}
- {id: 15, title: "CocoIndex Enterprise", url: "https://cocoindex.io/enterprise/", source: "CocoIndex", date: "2026-07-19"}
- {id: 16, title: "CocoIndex company profile", url: "https://tracxn.com/d/companies/cocoindex/__3uzEhPrOAu9NdwACSSElc-Mw0dsZE4HPDnvFE0co8kg", source: "Tracxn", date: "2026-07-19"}
- {id: 17, title: "pgvector vs. Qdrant benchmark", url: "https://www.tigerdata.com/blog/pgvector-vs-qdrant", source: "Tiger Data (Timescale)", date: "2025-04-29"}
- {id: 18, title: "Increase performance of pgvector's HNSW index", url: "https://supabase.com/blog/increase-performance-pgvector-hnsw", source: "Supabase", date: "2023-08"}
- {id: 19, title: "The case against pgvector", url: "https://alex-jacobs.com/posts/the-case-against-pgvector/", source: "Independent practitioner blog", date: "2025-10-29"}
- {id: 20, title: "Vector databases are dying: the production evidence", url: "https://medium.com/data-science-collective/vector-databases-are-dying-heres-the-production-evidence-8c17b54687e2", source: "Medium / Data Science Collective", date: "2026"}
- {id: 21, title: "pgvector 0.5.0 released", url: "https://www.postgresql.org/about/news/pgvector-050-released-2700/", source: "PostgreSQL News", date: "2023-08-28"}
- {id: 22, title: "Code execution with MCP: building more efficient AI agents", url: "https://www.anthropic.com/engineering/code-execution-with-mcp", source: "Anthropic Engineering", date: "2025-11-04"}
- {id: 23, title: "Donating the Model Context Protocol and establishing the Agentic AI Foundation", url: "https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation", source: "Anthropic", date: "2025-12-09"}
- {id: 24, title: "MCP Enterprise Adoption: The July 2026 State of Play", url: "https://andrew.ooo/answers/mcp-model-context-protocol-enterprise-adoption-july-2026/", source: "andrew.ooo", date: "2026-07"}
- {id: 25, title: "Claude Code moved from RAG + vector DB to agentic search", url: "https://x.com/bcherny/status/2017824286489383315", source: "X / Boris Cherny", date: "2026"}
- {id: 26, title: "RAG is dead. Long live RAG.", url: "https://lighton.ai/lighton-blogs/rag-is-dead-long-live-rag-retrieval-in-the-age-of-agents", source: "LightOn", date: "2025-11-12"}
- {id: 27, title: "Context architecture is replacing RAG as agentic AI pushes enterprise retrieval to its limits", url: "https://venturebeat.com/data/context-architecture-is-replacing-rag-as-agentic-ai-pushes-enterprise-retrieval-to-its-limits", source: "VentureBeat", date: "2026-05-18"}
- {id: 28, title: "Glean Raises $150M Series F at $7.2B Valuation", url: "https://www.glean.com/press/glean-raises-150m-series-f-at-7-2b-valuation-to-accelerate-enterprise-ai-agent-innovation-globally", source: "Glean", date: "2025-06-10"}
- {id: 29, title: "Enterprise AI startup Glean lands a $7.2B valuation", url: "https://techcrunch.com/2025/06/10/enterprise-ai-startup-glean-lands-a-7-2b-valuation/", source: "TechCrunch", date: "2025-06-10"}
- {id: 30, title: "Glean's top line crosses $300M as AI budget-cutting becomes its major selling point", url: "https://techcrunch.com/2026/05/28/gleans-top-line-crosses-300m-as-ai-budget-cutting-becomes-its-major-selling-point/", source: "TechCrunch", date: "2026-05-28"}
- {id: 31, title: "Glean Surpasses $200M in ARR for Enterprise AI", url: "https://www.businesswire.com/news/home/20251208127913/en/Glean-Surpasses-$200M-in-ARR-for-Enterprise-AI-Doubling-Revenue-in-Nine-Months", source: "Business Wire", date: "2025-12-08"}
- {id: 32, title: "Deedy Das on enterprise search architecture", url: "https://www.latent.space/p/deedy-das", source: "Latent Space podcast", date: "2023-04"}
- {id: 33, title: "Glean revenue, funding & news", url: "https://sacra.com/c/glean/", source: "Sacra", date: "2026-05-29"}
- {id: 34, title: "Should I build or buy an enterprise AI assistant for my business?", url: "https://www.glean.com/perspectives/should-i-build-or-buy-an-enterprise-ai-assistant-for-my-business", source: "Glean", date: "2026"}
- {id: 35, title: "Enterprise RAG platforms 2026", url: "https://onyx.app/insights/enterprise-rag-platforms-2026", source: "Onyx", date: "2026"}
- {id: 36, title: "onyx-dot-app/onyx", url: "https://github.com/onyx-dot-app/onyx", source: "GitHub", date: "2026-07-19"}
- {id: 37, title: "Cerebras raises $5.5B, kicking off 2026's IPO season with a bang", url: "https://techcrunch.com/2026/05/14/cerebras-raises-5-5b-kicking-off-2026s-ipo-season-with-a-bang/", source: "TechCrunch", date: "2026-05-14"}
- {id: 38, title: "Cerebras Systems shares climb after key trading signal", url: "https://www.benzinga.com/Opinion/26/07/60510850/cerebras-systems-shares-climb-5-percent-after-key-trading-signal", source: "Benzinga", date: "2026-07-17"}
- {id: 39, title: "Cerebras Systems Announces Strong First Quarter 2026 Results", url: "https://investors.cerebras.ai/news-releases/news-release-details/cerebras-systems-announces-strong-first-quarter-2026-results", source: "Cerebras Investor Relations", date: "2026-06-23"}
- {id: 40, title: "Cerebras refiles for IPO but UAE ties remain", url: "https://www.agbi.com/tech/2026/04/cerebras-refiles-for-ipo-but-uae-ties-remain/", source: "AGBI", date: "2026-04"}
- {id: 41, title: "Groq and Nvidia enter non-exclusive inference technology licensing agreement", url: "https://groq.com/newsroom/groq-and-nvidia-enter-non-exclusive-inference-technology-licensing-agreement-to-accelerate-ai-inference-at-global-scale", source: "Groq", date: "2025-12-24"}
- {id: 42, title: "SambaNova AI chip funding valuation", url: "https://www.cnbc.com/2026/07/08/sambanova-ai-chip-funding-valuation.html", source: "CNBC", date: "2026-07-08"}
- {id: 43, title: "Cerebras Systems employee data", url: "https://www.reveliolabs.com/companies/cerebras-systems/employees/", source: "Revelio Labs", date: "2025-12"}
- {id: 44, title: "Developer Experience Engineer, Cerebras", url: "https://jobs.eclipse.capital/companies/cerebras-2/jobs/62003195-developer-experience-engineer", source: "Cerebras careers (mirrored)", date: "2026-07"}
- {id: 45, title: "How AI Is Transforming Work at Anthropic", url: "https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic", source: "Anthropic", date: "2026"}
- {id: 46, title: "Reaction to Cerebras knowledge-base post", url: "https://x.com/DBredvick/status/2078150905078206789", source: "X / Drew Bredvick", date: "2026-07-17"}
:::
