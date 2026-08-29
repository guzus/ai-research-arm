---
title: "THE AGI AWARENESS POST"
kicker: "Your Daily Artificial Intelligence Briefing"
date: "July 16, 2026"
edition: "All Sources Edition"
volume: "2026"
number: "197"
deck: "An interactive newspaper edition generated from the daily AI digest."
---

:::paper-index
- label: "Lead"
  target: "#lead-top-story"
- label: "Breaking"
  target: "#briefs-breaking-policy"
- label: "Signals"
  target: "#meter-signal-mix"
- label: "Departments"
  target: "#deck-departments"
:::

:::lead(id="lead-top-story", label="Top Story", title="Pentagon confirms Grok directed 2,000+ munitions in Iran strikes — the first official U.S. government acknowledgment that a commercial AI chatbot was used in live combat operations, surfaced via sworn testimony in a Mississippi data-center lawsuit.")
Thinking Machines ships Inkling, a 975B-total/41B-active MoE open-weights multimodal model (text, image, audio; up to 1M context) — Mira Murati's lab's first public model, read as a rare non-Chinese entrant near the open-weight frontier; picked up Day-0 FP4 inference support hours later.

xAI open-sources Grok Build's CLI and harness and resets usage limits for all users, in the middle of a multi-day dispute over whether the tool exfiltrates unredacted .env secrets.

Legal exposure widens for two frontier labs: 26 Meta employees sue alleging AI tools targeted disabled/on-leave staff for layoffs, and xAI sues a Grok user over alleged CSAM deepfakes — an early instance of an AI company suing its own user.
:::

:::figure(src="https://techcrunch.com/wp-content/uploads/2026/07/Supply-Co-Page_Brand.png?resize=1200,623", alt="Amid hardware legal battle, OpenAI releases a $230 keyboard for Codex", caption="Amid hardware legal battle, OpenAI releases a $230 keyboard for Codex", source-url="https://techcrunch.com/2026/07/15/amid-hardware-legal-battle-openai-releases-a-230-keyboard-for-codex/", variant=wide)
:::

:::briefs(id="briefs-breaking-policy", title="Breaking & Policy", columns=2)
- headline: "Pentagon Official Confirms Grok Used to Direct 2,000+ Munitions in Iran Strikes. Cameron Stanley, the DoD's chief digital and AI officer, disclosed in sworn court testimony that Grok \"enabled U.S. forces to deploy over 2,000 munitions to 2,000 distinct targets within 96 hours\" during \"Operation Epic Fury.\" The disclosure surfaced in a Mississippi lawsuit over pollution from gas turbines at xAI's Colossus 2 data center, with the DOJ calling the facility \"vital\" to national security missions. It's the most concrete public confirmation yet of a frontier consumer chatbot embedded in live combat operations, intensifying the congressional fight over Sen. Kirsten Gillibrand's bill to ban unsupervised LLM use in force decisions."
  tag: "Breaking"
- headline: "Apple Intelligence Cleared for China via Alibaba Partnership (contested sourcing). TechCrunch reported Apple Intelligence was approved for launch in China through a partnership bringing Alibaba's Qwen models to Apple's OS. Separately, Caixin Global — the first named, credible outlet to weigh in — reported Chinese regulators approved the first batch of mobile-based generative AI models, resolving a claim this desk's Twitter monitor had flagged as unconfirmed rumor across three prior cycles. Still awaiting a second named-outlet or Apple/Alibaba on-the-record confirmation as of this writing."
  tag: "Breaking"
- headline: "xAI Open-Sources Grok Build. Elon Musk announced Grok Build's CLI, harness, and code are now open source on GitHub (Apache 2.0, per one account), with usage limits reset for all users. The move lands squarely inside an unresolved dispute dating to July 12 over whether the tool uploads unredacted repository secrets to xAI — the open client code doesn't resolve what xAI's servers do with data already collected, a distinct question covered by xAI's July 13 zero-retention statement."
  tag: "Breaking"
- headline: "New York signed the first statewide moratorium on hyperscale data centers, pausing environmental review for facilities over 50MW and proposing to end related tax incentives."
  tag: "Policy"
- headline: "26 Meta employees sued in federal court (Oakland, CA) alleging AI tools — including the \"Metamate\" assistant and employee-tracking/productivity-score systems — were used to select workers on medical, parental, or family leave for mass layoffs, alleging ADA/FMLA/Pregnancy Discrimination Act violations; Meta disputes that AI made the decisions."
  tag: "Policy"
- headline: "xAI sued a Grok user (already facing criminal charges) over alleged CSAM deepfakes generated via the platform, seeking damages and a permanent injunction — one of the first cases of an AI company suing its own user over generated content."
  tag: "Policy"
:::

:::news-meter(id="meter-signal-mix", title="Signal Mix")
- label: "Breaking news"
  value: 75
  display: "3 items"
  tone: hot
- label: "Model releases"
  value: 100
  display: "4 items"
  tone: watch
- label: "Research highlights"
  value: 20
  display: "1 items"
  tone: research
- label: "Funding and compute"
  value: 100
  display: "4 items"
  tone: market
:::

:::story-deck(id="deck-departments", title="Departments")
- headline: "Models & Systems"
  summary: "Thinking Machines — Inkling: First public foundation model from Mira Murati's lab. 975B total / 41B active parameter MoE, natively multimodal (text, image, audio), up to 1M token context, controllable reasoning effort, trained from scratch on GB300s (reportedly 45T tokens). Available on Tinker and Hugging Face. Company framing claims it beats Nemotron 3 Ultra and lands between Kimi 2.5 and 2.6 on benchmarks — not yet corroborated by independent leaderboards (LMArena, Artificial Analysis) as of this snapshot. Picked up Day-0 FP4 inference support on NVIDIA and AMD via PyTorch/TokenSpeed kernels hours after release. OpenAI — GPT-5.6 / GPT-Red / Codex Micro / ChatGPT Work: GPT-5.6 (including a \"Sol\" variant) is now generally available; OpenAI also shipped GPT-Red, an automated self-play red-teaming system OpenAI says finds successful attacks in 84% of test scenarios versus 13% for human red-teamers, feeding directly into hardening GPT-5.6. Separately, OpenAI launched its first branded hardware — \"Codex Micro,\" a $230 desktop controller for triggering Codex PR review/debug/refactor workflows — and introduced \"ChatGPT Work,\" a workplace product powered by Codex and GPT-5.6. xAI — Grok Build open source (see Breaking News)."
  meta: "4 digest items"
  tone: hot
- headline: "Research Ledger"
  summary: "No new arXiv batch posted in this window — arXiv's daily listing was still serving the 2026-07-15 04:00 UTC batch as of the last RSS check (08:27 UTC), over 4 hours later than its usual 04:00 UTC posting time. r/MachineLearning's hot list carried mostly ongoing discussion threads rather than new dated papers, notably a debate on whether chain-of-thought is a \"scaling trap\" pointing toward latent-reasoning approaches (Coconut/HRM/RecursiveMAS), a JEPA-critique request thread, and continued interest in mechanistic interpretability of individual convolutional neurons."
  meta: "1 digest items"
  tone: research
- headline: "Capital & Compute"
  summary: "Neko Health (Daniel Ek's AI/sensor-driven body-scanning startup) raised a $700M Series C at a ~$7B valuation (up from $1.7B in early 2025), co-led by Lightspeed and O.G. Venture Partners, funding a US launch starting in New York. Monumental, an Amsterdam bricklaying-robotics startup founded by ex-Palantir alumni, raised a $32M Series B led by Khosla Ventures to expand its 150+ autonomous robot fleet into the US (Texas, Florida, Virginia, Arizona). DeepSeek: Conflicting valuation reporting today — Bloomberg-sourced figures put a fresh raise at $71–74B (10–15% above its $66.6B post-money June mark), while a relayed claim from The Information described a \"tenfold\" valuation jump this desk could not reconcile with the Bloomberg number. DeepSeek is separately reported to be nearing $500M ARR and prepping a Shanghai STAR Market IPO as early as Q2 2027 (unverified, per The Information/WSJ)."
  meta: "4 digest items"
  tone: market
:::

:::quote(label="Quote of the Day")
"Vera Rubin is already in production. Giant amounts of production incoming." — Nvidia CEO Jensen Huang, at a Tokyo developer event, rebutting a SemiAnalysis report of manufacturing delays while acknowledging "we haven't really started much shipment yet."
:::
