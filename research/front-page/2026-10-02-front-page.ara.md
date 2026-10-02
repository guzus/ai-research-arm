---
title: "THE AGI AWARENESS POST"
kicker: "Your Daily Artificial Intelligence Briefing"
date: "October 2, 2026"
edition: "All Sources Edition"
volume: "2026"
number: "275"
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

:::lead(id="lead-top-story", label="Top Story", title="Perplexity open-sourced a decision model and cut prices")
pplx-decider-27b ships alongside a Decisions API at $0.04 per million input tokens with free output. It was the third open decision-model release in a day, after Cloudflare's Apache-2.0 Clef/Clef-flash and AutoTrust's JEV-27B-VL, and AWS also released Strands Decider 2B. All quality claims so far are self-reported (Twitter, TechCrunch, HN 334 pts).

OpenAI fired three safety researchers over leaks: OpenAI confirmed the departures, saying those involved "mishandled sensitive information outside established company procedures" (WSJ). Separately, California AG Rob Bonta served OpenAI an investigative subpoena over cybersecurity incidents involving its models. The subpoena is single-source so far (WSJ via Twitter, TechCrunch).

Anthropic opened Claude Code to mods: TypeScript hooks shipped inside plugins can now change Claude Code's behaviour, draw custom UI and replace built-in features. Anthropic says it built /diff and AGENTS.md support this way (@ClaudeDevs, @trq212, @testingcatalog).

Trump floated Intel-style stakes in OpenAI and Anthropic: in a TIME interview he ruled out nationalizing frontier labs but said the government "might" take equity stakes. There is no mechanism or term sheet yet (TIME via Twitter).
:::

:::briefs(id="briefs-stories", title="Stories", columns=2)
- headline: "SoftBank and Nvidia paid their final $10B each into OpenAI"
  tag: "Breaking"
- headline: "DeepMind launched SynthID Bio for AI-designed proteins"
  tag: "Breaking"
- headline: "FT says OpenAI agents reached data on 55 sites"
  tag: "Breaking"
- headline: "Grok 4.7 is rolling out as the base model for every mode (Fast, Expert…"
  tag: "Models"
- headline: "Gemini 4 Argon took #1 on the Vals Index at 68.9%"
  tag: "Models"
- headline: "Cloudflare Clef / Clef-flash are built on Qwen3.8-27B and Qwen3.5-9B with rank-256 LoRA and…"
  tag: "Models"
- headline: "Black Forest Labs FLUX 3 Image is an editing-focused model with 4K output"
  tag: "Models"
- headline: "California signed new workplace-AI bills"
  tag: "Policy"
- headline: "California's AG subpoenaed OpenAI as part of a broader inquiry into cybersecurity incidents and…"
  tag: "Policy"
- headline: "Trump told TIME that companies \"seeking regulation risk being put out of business\""
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
"Put these pieces together and you have the two halves of a worm: a payload that hijacks the agent, and an agent that will carry the payload to the next agent." — Matthew Green, "Is sandboxing sufficient to contain rogue agents?", quoted by Simon Willison
:::
