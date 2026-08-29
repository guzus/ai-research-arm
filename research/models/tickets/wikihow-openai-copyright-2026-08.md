---
slug: wikihow-openai-copyright-2026-08
title: wikiHow sues OpenAI over scraping 11,000+ articles to train GPT models
company: wikiHow / OpenAI
model: null
status: confirmed
status_note: |
  **Reuters, relayed by @rohanpaul_ai (2026-08-25 00:07 UTC):** wikiHow
  has sued OpenAI, alleging it **scraped more than 11,000 articles** to
  train GPT models without permission. The complaint says that copying
  **infringed at least 1,200 registered copyrights** and fed models that
  can reproduce wikiHow text. **Filed 2026-08-21 in the Southern District
  of New York**; at the complaint stage, with no ruling on the
  allegations. OpenAI's position, per the same relay, is that its models
  use publicly available data under fair use.

  Status `confirmed` — a docketed filing with a named court, a named
  filing date, a named plaintiff and quantified claims, attributed to
  Reuters. Verification `partial`: **the Reuters article itself and the
  docket entry were not captured in-window**, so the specific counts
  (11,000 articles / 1,200 registrations) rest on one relay of one outlet.
  Registration counts are the checkable part and should be confirmed
  against the complaint before being reused as facts.

  **The legally interesting move is the second allegation, not the
  first.** Training-set scraping claims are now routine
  ([[nyt-openai-microsoft-copyright-2026-06]],
  [[anthropic-copyright-settlement-approved-2026-07]]). wikiHow additionally
  alleges **market substitution** — that ChatGPT answers displace the
  how-to pages that supplied the training text — which targets the fourth
  fair-use factor directly rather than arguing transformativeness. That
  connects training provenance to market effect in one pleading.

  **The counterweight is in the same relay and belongs on the record:**
  U.S. copyright protects expression, not the underlying procedure,
  process, method or fact. A model can explain how to perform a task
  without infringing the article describing it — which is a materially
  stronger defence against how-to content than against reported journalism.
expected: "Filed 2026-08-21 in SDNY; complaint stage, no ruling. Pending: capture of the complaint and docket number, OpenAI's answer or motion to dismiss, whether the market-substitution theory survives that motion, and any consolidation with the other pending OpenAI copyright matters"
labels:
  - openai
  - wikihow
  - copyright
  - litigation
  - fair-use
verification: partial
sources:
  - "@rohanpaul_ai"
created_at: 2026-08-25
updated_at: 2026-08-25
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-25
    change: "Created — Reuters (via @rohanpaul_ai, 2026-08-25 00:07 UTC) reports wikiHow sued OpenAI on 2026-08-21 in the Southern District of New York, alleging OpenAI scraped 11,000+ articles to train GPT models without permission and infringed at least 1,200 registered copyrights, and further alleging market substitution because ChatGPT answers can displace the how-to pages that supplied the text. OpenAI's stated position is fair use over publicly available data. Status confirmed — a docketed filing with named court, date, plaintiff and quantified claims. Verification partial — neither the Reuters article nor the docket entry was captured, so the counts rest on a single relay. Noted on the ticket that the idea/expression divide is an unusually strong defence against how-to content, and that the substitution theory is the novel half. Sits with [[nyt-openai-microsoft-copyright-2026-06]] and [[anthropic-copyright-settlement-approved-2026-07]]."
---

**wikiHow has sued OpenAI** in the Southern District of New York, filed
**2026-08-21**, over the alleged scraping of **11,000+ articles** and
infringement of **at least 1,200 registered copyrights**.

**Why this one is not just another scraping suit.** The complaint pairs
the usual ingestion claim with a **market-substitution** claim: that
ChatGPT answering "how do I…" displaces the pages that supplied the
training data. That is an argument aimed squarely at the fourth fair-use
factor — effect on the market for the original — rather than at whether
training is transformative. Most training suits fight on factor one;
wikiHow is fighting on factor four, where a plaintiff with a
high-traffic, ad-funded corpus has the cleanest damages story.

**And why it may still fail.** Copyright protects expression, not the
procedure, process, method or fact described. How-to content is the genre
where that line is least favourable to the plaintiff: a model that
explains how to unclog a drain has not necessarily copied the article
explaining how to unclog a drain. The substitution harm may be real and
economically severe while the copyright hook stays weak — those are
different questions, and this ticket does not merge them.

**Registration count is the number to verify.** 1,200 registered
copyrights is what sets the statutory-damages ceiling and is the single
most checkable claim in the filing; it is also the one carried here on a
single relay. It should be confirmed against the complaint before it is
repeated as fact.

**Where it sits.** OpenAI's live copyright exposure now spans
[[nyt-openai-microsoft-copyright-2026-06]] and this matter, against the
backdrop of Anthropic's approved class settlement
([[anthropic-copyright-settlement-approved-2026-07]]) — the closest thing
to a price signal for what this class of claim settles at. Separately,
OpenAI is fielding state consumer-protection process over the Hugging Face
incident ([[openai-unreleased-containment-escape-2026-07]]), which is a
different theory against the same defendant in the same season.
