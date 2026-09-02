---
slug: google
title: Google
type: entity
aliases: [Google, Alphabet, "Google DeepMind", NotebookLM, "Gemini Notebook", "Google AI Mode", "Gemini Robotics 2", "Gemini Robotics ER 2", "Google AI Studio", "Google Pics"]
tags: [hyperscaler, frontier-lab, antitrust, consumer-ai, gemini]
description: Hyperscaler behind Gemini; launched Pics, an AI-first Workspace design suite aimed at Canva and Adobe (2026-09-02), after Q2 2026 revenue of $119.8B and a revenue-linked equity claim on Marvell.
created_at: 2026-07-17
timestamp: 2026-09-02T00:00:00Z
market:
  ticker: GOOGL
  exchange: NASDAQ
  symbol: NASDAQ:GOOGL
  provider: yahoo
sources:
  - {title: "ARA daily digest 2026-09-02", path: research/digest/2026-09-02-digest.md}
  - {title: "ARA daily digest 2026-08-20", path: research/digest/2026-08-20-digest.md}
  - {title: "ARA daily digest 2026-08-19", path: research/digest/2026-08-19-digest.md}
  - {title: "ARA daily digest 2026-08-13", path: research/digest/2026-08-13-digest.md}
  - {title: "ARA daily digest 2026-08-12", path: research/digest/2026-08-12-digest.md}
  - {title: "ARA daily digest 2026-08-10", path: research/digest/2026-08-10-digest.md}
  - {title: "ARA daily digest 2026-08-06", path: research/digest/2026-08-06-digest.md}
  - {title: "ARA daily digest 2026-08-01", path: research/digest/2026-08-01-digest.md}
  - {title: "ARA model ticket — Gemini Robotics 2", path: research/models/tickets/google-gemini-robotics-2-2026-07.md}
  - {title: "ARA daily digest 2026-07-25", path: research/digest/2026-07-25-digest.md}
  - {title: "ARA daily digest 2026-07-23", path: research/digest/2026-07-23-digest.md}
  - {title: "ARA daily digest 2026-07-22", path: research/digest/2026-07-22-digest.md}
  - {title: "ARA daily digest 2026-07-20", path: research/digest/2026-07-20-digest.md}
  - {title: "ARA daily digest 2026-07-18", path: research/digest/2026-07-18-digest.md}
  - {title: "ARA daily digest 2026-07-17", path: research/digest/2026-07-17-digest.md}
---

**Google** is the hyperscaler and frontier-model builder behind the
**Gemini** family ([[gemini-3-5-flash]], [[gemini-3-6-flash]],
[[gemini-3-7-flash]], [[gemini-3-5-pro]], [[gemini-spark]],
[[gemma-4]], [[nano-banana-2-lite]]). While its individual model releases
have been tracked on their own pages, this page covers Google as a company:
the regulatory and product-strategy threads that don't attach to a single
model. [[gemini-3-5-pro]]'s reported 2026-07-16 schedule slip wiped out
~$200B of market cap — see [[ai-capex]].

## Why it matters

- **EU forces Android and Search open under the DMA (2026-07-17).** A formal
  Digital Markets Act antitrust ruling requires Google to open **Android**
  and **Search** interoperability to rivals, with an explicit
  **AI-data-access dimension** — the EU targeting Google's AI advantage
  through its existing antitrust toolkit rather than AI-specific
  legislation. Lands the same week Germany separately ruled that Google's
  **AI Overviews** and Perplexity fall under media law — two European
  jurisdictions independently applying non-AI-native legal frameworks to
  Google's AI products.
- **NotebookLM rebrands into the Gemini family (2026-07-17).** Google
  renamed **NotebookLM** to **Gemini Notebook** and opened its search app to
  third-party integration — a large, fast-growing Hacker News thread
  (34→162 points) debated the naming/product-strategy move, read as Google
  consolidating its AI product portfolio under a single Gemini brand rather
  than maintaining standalone product names.
- **Gemini Notebook adds native cloud code execution; scale disclosed
  (2026-07-18).** A day after the rename, Google added **native cloud code
  execution** to **Gemini Notebook** and disclosed the product's reach for
  the first time: **30M+ users** and **600K+ organizations** — the first
  concrete usage numbers attached to the rebrand, and a materially larger
  footprint than NotebookLM's public profile suggested (ARA digest
  2026-07-18).
- **Google AI Mode gains task-completion.** Google AI Mode now lets users
  link and interact with select third-party apps directly, moving the
  product beyond Q&A into task completion — the same distribution-through-
  existing-surfaces strategy [[meta]] is running with AI Mode on Facebook.
- **Three new Flash-tier models ship; Pro stays delayed, Gemini 4 already
  training (2026-07-21).** Google shipped **[[gemini-3-6-flash|Gemini 3.6
  Flash, 3.5 Flash-Lite, and Flash "Cyber"]]** together — a security-focused
  variant pitched as a cheaper alternative to dedicated AI-security tools —
  while [[gemini-3-5-pro|Gemini 3.5 Pro]] remains "in testing" and reporting
  says Google is already training **Gemini 4**. The release was the top
  Hacker News story of the day (524 pts / 420 comments) (ARA digest
  2026-07-22).
- **Q2 2026 earnings beat, Cloud up 82% (2026-07-22).** Alphabet's Q2 2026
  print landed as the hardest [[ai-capex]] data point of the week — the
  earnings report the theme flagged on 2026-07-20 as the thing the market
  was pricing ahead of: **revenue $119.8B (+24% YoY, vs. $116.93B
  consensus)**, **Google Cloud revenue up 82% to $24.77B**, ad revenue
  $81.63B, YouTube ad revenue $11.06B. CEO Sundar Pichai credited
  AI-infrastructure/solutions demand for the cloud acceleration — early
  evidence that Alphabet's **~$175-190B 2026 AI capex guidance** is
  converting into cloud revenue rather than sitting as unmonetized buildout
  (9to5Google, CNBC; ARA digest 2026-07-23).

- **Gemini nears a billion-user milestone (2026-07-23).** TechCrunch reports
  Gemini is closing in on another billion-user product for Google, days
  after the Q2 2026 earnings beat — consumer-scale distribution reinforcing
  the same AI-investment thesis the Cloud-revenue acceleration supports
  (ARA digest 2026-07-25).

- **Google pulls Google Earth's AI image generator one day after launch
  (2026-07-31, digested 2026-08-01).** A [[nano-banana-2-lite|Nano Banana 2]]-powered
  feature let anyone superimpose generated imagery onto **authentic satellite
  data** in Google Earth. Within about 24 hours, OSINT researcher **Henk van
  Ess** had produced **synthetic bomb craters and a fake refugee camp that
  passed Hive's AI detectors**, and Google disabled the feature — with no
  on-record statement inside the window. This is the sharpest product-level
  demonstration yet that **provenance tooling fails where the base layer is
  itself authoritative**: the danger was not the generated pixels but their
  fusion with a trusted geospatial reference. It also marks an unusually fast
  Google retraction, one day from ship to kill (TechCrunch, The Verge, Ars
  Technica; ARA daily digest 2026-08-01).
- **Gemini Robotics 2 and ER 2 — whole-body control, and a new safety
  benchmark (2026-07-31).** Google DeepMind launched **Gemini Robotics 2**,
  pitched as "one brain for any robot" and the **first DeepMind robotics model
  with whole-body rather than upper-body-only control**, spanning tabletop
  arms through humanoids, with advanced dexterity and multi-robot teamwork.
  The companion **Gemini Robotics ER 2** (`gemini-robotics-er-2-preview`,
  built on [[gemini-3-5-flash]]) adds a higher-level embodied-reasoning layer,
  reported at **91.3% moment-finding accuracy at 4x faster execution**. Google
  also introduced **"ASIMOV-Agentic,"** an embodied/agentic safety benchmark.
  It was the morning's biggest Hacker News thread (594 points, 480+ comments).
  The `-preview` model ID points at gated partner access rather than open
  availability. Lands against the Chinese humanoid push ([[agibot]]) and
  [[figure-ai]]'s in-house VLA. See the
  [Gemini Robotics 2 ticket](../../models/tickets/google-gemini-robotics-2-2026-07.md)
  (ARA daily digest 2026-08-01).
- **AI Studio's app-building folds into the Gemini app; Lyria 3.5 ships
  (2026-08-01).** Google said it **dropped plans for a standalone AI Studio
  mobile client** so that apps "emerge naturally, in the course of your
  everyday conversations with Gemini" — three unaffiliated product trackers
  reported it independently, though whether the AI Studio *developer* console
  is affected is not evidenced. Separately **Lyria 3.5** shipped and was
  integrated into Google Flow Music. The consolidation is the same pattern as
  the NotebookLM→Gemini Notebook rename flagged below: surfaces collapsing
  into the Gemini app as the single consumer entry point (ARA daily digest
  2026-08-01).
- **The AI leadership layer is rewired inside one hour, and Jeff Dean leaves
  after 27 years (2026-08-06).** **Demis Hassabis** moved from CEO of Google
  DeepMind to **Chair of GDM and Alphabet Chief Scientist**, with CTO **Koray
  Kavukcuoglu** taking operational control of GDM and reporting to **Sundar
  Pichai**. Minutes later **Jeff Dean** announced his departure — he joined at
  25 employees and left at 190,000+ — taking **Sanjay Ghemawat**, **Oriol
  Vinyals** and **Quoc Le** with him to found [[discovery-loop]], with Google
  itself a founding investor and Cloud partner. Read structurally, the two
  announcements are one event: the research founder-figures step out of the
  operating line while a CTO-turned-operator reports directly to the CEO, and
  the departing researchers stay commercially attached to Google rather than
  to a rival. What is *not* evidenced is any change to Gemini's roadmap or to
  the [[ai-capex]] guidance (The Verge, The Decoder, TechCrunch, @JeffDean,
  ARA daily digest 2026-08-06).
- **Google Assistant is retired starting 2026-09-04 (2026-08-06).** Assistant
  is being withdrawn from phones, tablets and Wear OS as **Gemini** takes over
  across Android. Unlike most consolidation reporting this is a *dated,
  first-party commitment*, which makes it the hardest available evidence for
  the surface-collapse pattern already noted above (AI Studio → Gemini app,
  NotebookLM → Gemini Notebook): the pre-LLM assistant brand is being ended on
  a calendar, not deprecated quietly (The Verge, Ars Technica, The Decoder).
- **Google reported in talks to buy Mechanize for ~$1.5B (2026-08-06).**
  Mechanize hand-builds **reinforcement-learning environments for coding
  agents** at roughly **$8k per task**; the reported price is a **~3× step-up
  in three months**. Treat as weak: the report is **single-sourced**
  (@deedydas), names no outlet, and neither company has confirmed. If it
  holds, the interesting part is not the price but what is being bought —
  hand-authored RL environments as a scarce input, i.e. training data for
  agents priced like consulting rather than like scraped corpus.
- **DeepMind's hurricane model buys forecasters an extra day (2026-08-08).**
  DeepMind's AI hurricane-forecasting model surprised weather scientists by
  **extending useful warning lead time by roughly a day** on 2026-08-08
  (Ars Technica) — a concrete validation of ML weather prediction in an
  operational setting, and the strongest science-side DeepMind datapoint in
  the wiki since the leadership rewire tracked above. Details (model name,
  verification, agency adoption) are thin in the source; the lead-time gain
  itself is the headline (Ars Technica; ARA daily digest 2026-08-10).
- **Gemini app crosses one billion monthly users — nominal ChatGPT parity
  (2026-08-12).** Google's **Gemini app reached one billion monthly users**,
  claiming nominal parity with **[[openai|ChatGPT]]**, which hit the same mark
  in June — and **neither company has disclosed retention, session frequency,
  or paid conversion**, so the parity claim measures monthly reach, not
  engagement or revenue. It is the hard number behind the 2026-07-23 "nears a
  billion-user milestone" entry and a consumer-scale validation of the
  [[ai-capex]] thesis (TechCrunch, Ars Technica, The Verge; ARA daily digest
  2026-08-12).
- **AMIE (Video) reaches clinician-level ratings (2026-08-12).** Google
  Research's **AMIE (Video)** — the medical-AI system extended to real-time
  video consultations — was rated **at clinician level by evaluators in a
  randomized OSCE study**, the video counterpart to the text-based AMIE
  trajectory and a concrete read on where AI-for-medicine stands (Google
  Research; ARA daily digest 2026-08-12).
- **Made by Google '26 — the hardware line ships Gemini throughout
  (2026-08-13).** Google announced the **Pixel 11 series**, **Pixel Watch 5 at
  $399**, a **Pixel Tag** AirTag rival, and a slate of **Gemini features** at
  Made by Google '26. In the same window **DeepMind released SL2T**, an
  **American Sign Language–to-English model** running **body-pose tracking
  on-device** and shipping in **Gboard and Live Transcribe on Pixel 11** —
  accessibility-model progress as a consumer-hardware feature rather than a
  cloud API (TechCrunch, The Verge, @GoogleDeepMind; ARA daily digest
  2026-08-13).
- **DeepMind helps push the [[matrix-multiplication-exponent]] below 2.371177 (2026-08-19).** A DeepMind-and-
  academia team combined a reformulated optimization with AlphaEvolve to
  tighten the matrix multiplication exponent ω below **2.371177**, improving
  the prior 2.371339 record — a genuine ML-assisted result in theoretical CS
  in the AlphaTensor lineage (ARA daily digest 2026-08-19).
- **Google takes a revenue-linked equity claim on Marvell (2026-08-20).** Google
  secured a **warrant for up to 58,970,907 Marvell shares at a $206.58 strike**,
  vesting in 240 tranches against **$500M each of custom-silicon purchases** —
  full vesting requires **$120B of Google revenue through fiscal 2033** — a
  supplier-financing structure that converts Google's custom-silicon spending
  into a potential equity claim on the merchant-chip maker. **MRVL rose over
  13% and Broadcom fell about 2%** on the print, a market read that the
  revenue-rebate structure shifts custom-ASIC economics toward [[broadcom]]'s
  merchant rival (ARA daily digest 2026-08-20).

## Pics, Flash video analysis, and a "below the frontier" admission (2026-09-02)

- **Google launched Pics, an AI-first Workspace design suite (2026-09-02).**
  Pics is aimed at Canva and Adobe: users **prompt instead of laying out a
  canvas**, and The Verge and TechCrunch both frame it as professional-grade
  generation and editing rather than a traditional design surface. This is a
  Workspace distribution play, not a new foundation model — the interesting
  part is Google putting a generative suite into the same productivity
  surface that already defaults to Gemini (TechCrunch, The Verge; ARA daily
  digest 2026-09-02).
- **Gemini Flash models gained agent-based video analysis.**
  [[gemini-3-7-flash|3.7 Flash]], [[gemini-3-6-flash|3.6 Flash]], and
  **3.5 Flash-Lite** now choose what to inspect instead of scanning every
  frame, cutting token use by **up to 88 percent** per The Decoder. That is
  a serving-cost claim on the already-cheap Flash tier, not a new
  capability score (The Decoder; ARA daily digest 2026-09-02).
- **Kavukcuoglu said current Google models are "a little bit below the
  frontier."** Google DeepMind's Koray Kavukcuoglu — operational lead since
  the 2026-08-06 leadership rewire — said he is **"100% certain that we
  will be at the frontier,"** with leadership framed as the only metric
  that matters. Treat as a first-party positioning quote, not a
  benchmark (The Decoder; ARA daily digest 2026-09-02).
- **Reported Hollywood catalog-licensing talks.** Google has reportedly
  approached studios for catalog deals to train models; The Verge's read
  is that **Google needs Hollywood more than the studios need AI**.
  Single-outlet, no studio confirmation in today's files (The Verge; ARA
  daily digest 2026-09-02).
- **AlgorithmWatch used DSA access on 4,480 election-related Google
  queries** and found AI Overviews opaque, thin-sourced, and sometimes
  taking sides — a researcher-side read on the same AI-Overviews surface
  already tracked under [[eu-ai-regulation]] (The Decoder; ARA daily
  digest 2026-09-02).
- **Google dropped AI-search advice** that had told users who said they
  were alone with certain nationalities to get to a safe place or call
  emergency services; The Decoder says other Facebook-derived flags
  remain (The Decoder; ARA daily digest 2026-09-02).

## Open questions

- **Does "generate onto authoritative data" survive as a product category?**
  The Google Earth feature was killed in a day because detectors could not
  distinguish generated edits fused with real satellite imagery. Is there a
  provenance design that makes this shippable, or is the category closed?

- **Does the DMA ruling meaningfully change AI competitive dynamics**, or is
  the AI-data-access dimension symbolic alongside the core Android/Search
  interoperability mandate?
- **Does the NotebookLM→Gemini Notebook rename signal further consolidation**
  of Google's separately-branded AI products under one umbrella?
- **How does Germany's AI-Overviews-as-media-law ruling interact with the
  EU-level DMA action** — two different legal theories converging on the
  same company in the same window.
