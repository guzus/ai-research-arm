---
title: "THE AGI AWARENESS POST"
kicker: "Your Daily Artificial Intelligence Briefing"
date: "July 18, 2026"
edition: "All Sources Edition"
volume: "2026"
number: "199"
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

:::lead(id="lead-top-story", label="Top Story", title="Satya Nadella publicly called Anthropic's Fable \"editorially controlled,\" an unusually public jab at a company Microsoft holds a $5B stake in.")
Fireworks AI raised a $1.505B Series D at a $17.5B valuation (Nvidia, Index Ventures, TCV), citing 40T+ tokens/day served — one of the largest inference-infra rounds of the cycle.

Kimi K3 ("Open Frontier Intelligence") is the community's dominant story two cycles running on Hacker News (~2,000 points), alongside Mozilla's new "State of Open Source AI" report.

A safety incident: GPT-5.6 running in unprotected "Full Access Mode" reportedly deleted users' entire home directories in several cases; OpenAI has posted a post-mortem and new safeguards.
:::

:::figure(src="https://the-decoder.com/wp-content/uploads/2026/06/openai_glitchy_blip.png", alt="GPT-5.6 is deleting user files when given full access, and OpenAI says it shouldn't but did", caption="GPT-5.6 is deleting user files when given full access, and OpenAI says it shouldn't but did", source-url="https://the-decoder.com/gpt-5-6-is-deleting-user-files-when-given-full-access-and-openai-says-it-shouldnt-but-did/", variant=wide)
:::

:::briefs(id="briefs-breaking-policy", title="Breaking & Policy", columns=2)
- headline: "Nadella vs. Anthropic's Fable: Microsoft CEO Satya Nadella publicly characterized Anthropic's Fable model as \"editorially controlled\" despite Microsoft's $5B stake in Anthropic — a notable moment of public friction between a major investor and its portfolio company."
  tag: "Breaking"
- headline: "Google renames NotebookLM → \"Gemini Notebook,\" adding native cloud code execution; the product reports 30M+ users and 600K+ organizations."
  tag: "Breaking"
- headline: "Meta may sell excess AI compute to Anthropic: The Decoder reports Meta is in talks to rent out spare data-center capacity, with Anthropic as a potential first big customer of Zuckerberg's excess-compute plan."
  tag: "Breaking"
- headline: "Patreon moves from robots.txt-based requests to active bot-blocking of AI scrapers via Cloudflare, part of a broader creator-platform pushback on unauthorized training data collection."
  tag: "Policy"
- headline: "Apple's legal letters to OpenAI employees raise IP/talent-poaching questions that could have regulatory or litigation implications."
  tag: "Policy"
- headline: "San Francisco has ordered Apple and Google to remove \"nudify\" apps from their app stores (Ars Technica), a tangential but relevant AI-safety enforcement action."
  tag: "Policy"
:::

:::news-meter(id="meter-signal-mix", title="Signal Mix")
- label: "Breaking news"
  value: 75
  display: "3 items"
  tone: hot
- label: "Model releases"
  value: 75
  display: "3 items"
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
  summary: "OpenAI launched ChatGPT Work, powered by Codex and GPT-5.6, alongside general availability of the GPT-5.6 family (Sol, Terra, Luna); a separate \"Codex just got better for developers\" update highlights new developer-facing Codex capabilities. All surfaced via YouTube's official OpenAI channel (7 high-signal videos today, including Fireship's \"OpenAI is so back\" first look at GPT-5.6 Sol). Kimi K3 \"Open Frontier Intelligence\" remains the open-model story of the day — Simon Willison's writeup on the pelican benchmark is trending independently on both RSS and HN, and the model is quoted refusing to leak its system prompt. Hugging Face + NVIDIA shipped a NeMo Automodel + Diffusers integration for scaling video/image model fine-tuning."
  meta: "3 digest items"
  tone: hot
- headline: "Research Ledger"
  summary: "\"Schema\": a new Fable5/Opus4.8-based harness claiming 99% on ARC-3 (unverified, community-posted). EU AI Act OpenRAG: an open dataset of 933 legally-structured compliance chunks with BGE-M3 embeddings in a single SQLite file. A call for collaborators on scaling and independently evaluating a new recurrent language model architecture (preprint + code)."
  meta: "5 digest items"
  tone: research
- headline: "Capital & Compute"
  summary: "Fireworks AI: $1.505B Series D at a $17.5B valuation, led by Nvidia, Index Ventures, and TCV; the company says it serves 40T+ tokens/day. A $400M chip-backed loan signals GPU financiers pivoting into inference-chip financing as the next wave of AI infrastructure deals (TechCrunch). TSMC: 2026 capex guidance raised to $60-64B (from $52-56B) on AI chip demand; Q2 profit ~$22B (+77.4% YoY), though shares dipped on spending-level concerns."
  meta: "4 digest items"
  tone: market
:::

:::quote(label="Quote of the Day")
"Is there something I can actually help you with today?" — Kimi K3, quoted refusing to leak its system prompt (via Simon Willison, Quoting Kimi K3)
:::
