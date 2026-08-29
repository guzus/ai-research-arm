---
title: "THE AGI AWARENESS POST"
kicker: "Your Daily Artificial Intelligence Briefing"
date: "July 12, 2026"
edition: "All Sources Edition"
volume: "2026"
number: "193"
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

:::lead(id="lead-top-story", label="Top Story", title="Apple sues OpenAI over alleged trade-secret theft tied to OpenAI's rumored hardware device, which itself may now slip to no earlier than February 2027 pending the dispute.")
GPT-5.6 Sol Ultra reportedly used 64 subagents to solve a 50-year-old open math problem in under an hour, and now leads the CritPt physics-reasoning benchmark (32.3%) with all top-5 spots held by OpenAI models.

Ben Bernanke joins Anthropic's Long-Term Benefit Trust, and secondary-market chatter puts Anthropic's implied valuation at ~$1.2T — above OpenAI's reported ~$908B.

SK Hynix raises $26.5B via a Nasdaq listing, the largest US share sale ever by a foreign company, underscoring the memory/HBM supply crunch feeding AI datacenters.
:::

:::figure(src="https://the-decoder.com/wp-content/uploads/2026/07/a_math_universe.png", alt="OpenAI's GPT-5.6 Sol Ultra reportedly solves a 50-year-old math problem in under an hour", caption="OpenAI's GPT-5.6 Sol Ultra reportedly solves a 50-year-old math problem in under an hour", source-url="https://the-decoder.com/openais-gpt-5-6-sol-ultra-reportedly-solves-a-50-year-old-math-problem-in-under-an-hour/", variant=wide)
:::

:::briefs(id="briefs-breaking-policy", title="Breaking & Policy", columns=2)
- headline: "Apple v. OpenAI: Apple filed suit alleging trade-secret theft connected to OpenAI's rumored camera-equipped smart-speaker hardware device; per secondhand reporting (The Information, via @rohanpaulai), Apple may seek restrictions on disputed designs, manufacturing, and suppliers but still needs evidence tying specific secrets to OpenAI's product. The device's launch could now slip to no earlier than February 2027."
  tag: "Breaking"
- headline: "Ben Bernanke appointed to Anthropic's Long-Term Benefit Trust — a governance-level addition to the body that oversees Anthropic's mission-alignment structure."
  tag: "Breaking"
- headline: "Anthropic valuation chatter: secondary-market pricing reportedly implies a ~$1.2T valuation for Anthropic, above OpenAI's reported ~$908B — treat as market chatter, not a confirmed round."
  tag: "Breaking"
- headline: "Apple v. OpenAI trade-secret lawsuit (see Breaking News) — the day's most significant legal development, tied directly to OpenAI's hardware ambitions."
  tag: "Policy"
- headline: "The Decoder: reporting that terrorist groups are using every major AI chatbot for attack-planning and weapons-development research — a fresh data point in the ongoing AI-misuse/safety-policy conversation, sourced from a single outlet in this snapshot."
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
  value: 100
  display: "5 items"
  tone: research
- label: "Funding and compute"
  value: 100
  display: "4 items"
  tone: market
:::

:::story-deck(id="deck-departments", title="Departments")
- headline: "Models & Systems"
  summary: "GPT-5.6 Sol Ultra (OpenAI): reportedly produced a novel proof for a 50-year-old math problem using 64 subagents in under an hour (per @emollick.bsky.social and The Decoder); now GA, with Sam Altman noting it's preferred in Microsoft 365 Copilot. Leads CritPt physics-reasoning benchmark at 32.3%, ahead of GPT-5.5 Pro (30.6%) and GPT-5.6 Terra (30.0%); Gemini 3 Pro Deep Think trails at 25.7%, Claude Opus 4.8 at 20.9% — all reported via a single secondary-source tweet, unverified against a primary leaderboard. GPT-5.6 Luna reportedly hitting \"model at capacity\" errors for some users shortly after rollout (per @minimaxir.bsky.social) — early capacity-scaling friction, not independently confirmed. Grok 4.5 / Grok v9-medium: shipped free to all X accounts via Grok Build, ending its private-beta gate (same 1.5T \"V9\" foundation model)."
  meta: "4 digest items"
  tone: hot
- headline: "Research Ledger"
  summary: "OpenCoF: Learning to Reason Through Video Generation — introduces \"Chain-of-Frame\" reasoning, where a video model reasons by generating temporally connected frames instead of text tokens; a genuinely new reasoning modality beyond text/image chain-of-thought. A First-Principles Theory of Slow Thinking and Active Perception — derives \"slow thinking\" from an active-lifting theory of latent sequence sampling and uncertainty reduction, offering theoretical grounding for why test-time reasoning works. When the Judge Changes, So Does the Measurement — shows upgrading the judge model in LLM-as-judge pipelines produces inconsistent results across datasets, with position/verbosity biases persisting even in stronger judges — a direct challenge to a technique this very pipeline leans on."
  meta: "5 digest items"
  tone: research
- headline: "Capital & Compute"
  summary: "SK Hynix: $26.5B Nasdaq listing, largest-ever US share sale by a foreign company. Gradium (Paris voice-AI infra startup): extended its seed round to $100M, with NVIDIA joining the cap table alongside FirstMark, Eurazeo, DST Global, and Eric Schmidt. Training-data/RL-environments market map (via @deedydas, self-compiled estimate, author-flagged as partially \"underreported\"/corrected): ~50+ startups selling training data/RL environments to frontier labs represent ~$8.5B combined revenue and ~$100B combined valuation, with Scale AI, Surge AI, Mercor, and Handshake accounting for >75% of the total."
  meta: "4 digest items"
  tone: market
:::

:::quote(label="Quote of the Day")
"I really want to get artisanal with my model selection: Luna xHigh for recipes, Sol Medium for sonnets, Terra High for bad puns, Luna xLow for limericks, Sol Ultra for true prophecies…" — @emollick.bsky.social
:::
