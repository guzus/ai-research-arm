---
title: "THE AGI AWARENESS POST"
kicker: "Your Daily Artificial Intelligence Briefing"
date: "November 21, 2026"
edition: "All Sources Edition"
volume: "2026"
number: "325"
deck: "An interactive newspaper edition generated from the daily AI digest."
---

:::paper-index
- label: "Lead"
  target: "#lead-top-story"
- label: "Stories"
  target: "#briefs-stories"
- label: "Signals"
  target: "#meter-signal-mix"
:::

:::lead(id="lead-top-story", label="Top Story", title="Alpöge claims Claude proved Riemann Hypothesis")
Anthropic mathematician Levent Alpöge posted a four-page note plus a 14-part Lean archive arguing a Claude-assisted proof of RH that “easily extends” to GRH. Terence Tao ranks that Lean-only artifact the least digested of three AI-assisted claims; Scott Aaronson stamps 17.4 million Lean lines and bets the proof will stand, while Clay’s $1M Millennium Prize still requires publication, two years, and general acceptance (HN, The Verge, TechCrunch, Simon Willison).

Masullo posts competing human GRH proof, Stanford’s Ravi Vakil hurried out Alessandro Masullo’s 940-page draft after Brian Conrad’s months of review, stressing it is “all human, with no AI.” Conrad says the paper is undergoing major revision; an in-progress Lean autoformalization notes Chapter 13 does not yet state its main theorem (HN, Simon Willison, Latent Space).

Thinking Machines shipped Inkling 2 Mini, an open-weights looped transformer aimed at laptops: 26.4B total, 3.4B active, about 20GB of memory, and a 1M-token window. Vendor benches put it at 79.2% SWE-bench Verified and tied with Qwen3.8-27B on AA Index; Stanford Hazy’s “intelligence per joule” on DGX Spark is 0.703 versus 0.430 for a Qwen 3.6 MoE (HN, Thinking Machines).

Signal blocks on-screen mobile AI agents, screenshot blocking on iOS 27 and Android Screen security so Gemini Intelligence and Siri AI cannot read chats. Meredith Whittaker calls agentic on-screen analysis an existential privacy threat; users can disable the protection in-app, and macOS still has no reliable screenshot block (The Verge, The Decoder, HN).
:::

:::figure(src="https://platform.theverge.com/wp-content/uploads/sites/2/2026/11/gettyimages-2305894185.jpg?quality=90&strip=all&crop=0%2C10.732984293194%2C100%2C78.534031413613&w=1200", alt="Anthropic mathematician claims to have solved prestigious Millennium Prize problem with Claude", caption="Anthropic mathematician claims to have solved prestigious Millennium Prize problem with Claude", source-url="https://www.theverge.com/ai-artificial-intelligence/1010051/anthropic-riemann-hypothesis-millennium-prize-problem", variant=wide)
:::

:::briefs(id="briefs-stories", title="Stories", columns=2)
- headline: "Google Search dropped the search button, the desktop homepage now opens with an AI…"
  tag: "Breaking"
- headline: "Google Gemini now calls businesses, Google Research traces Duplex from the 2018 demo to…"
  tag: "Breaking"
- headline: "Gemini for Mac runs desktop apps, Computer Use can operate desktop apps, local files…"
  tag: "Breaking"
- headline: "Thinking Machines shipped Inkling 2 Mini, 24 stored layers in four blocks of six…"
  tag: "Models"
- headline: "NVIDIA released Nemotron-Labs-Sigma, 14 open 3B/8B continuous diffusion LM checkpoints"
  tag: "Models"
- headline: "RadixArk shipped DaisyRose-27B, an Apache 2.0 agentic coder post-trained from Qwen3.8-27B with RL only"
  tag: "Models"
- headline: "Reflection published the Beam report, a 501.3B-parameter sparse MoE (23.4B active) pretrained on 23.8T…"
  tag: "Models"
- headline: "Trump threatened a tremendous overseas-AI tax, aimed at companies that build data centers outside…"
  tag: "Policy"
- headline: "Signal asked Apple, Google, and Microsoft for an app-level opt-out, covering screen, filesystem, notifications…"
  tag: "Policy"
- headline: "SEC staff are looking at Nvidia accounting, a confidential inquiry described by two anonymous…"
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

:::quote(label="Quote of the Day")
"So far, not one of the AI results with Lean certificates has needed to be retracted (while several without Lean certificates have needed to be). So I'm not 100% sure, but my bet is that the proof will stand." — Scott Aaronson, on Alpöge’s 17.4 million-line Lean GRH artifact (HN / scottaaronson.blog)
:::
