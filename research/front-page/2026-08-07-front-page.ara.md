---
title: "THE AGI AWARENESS POST"
kicker: "Your Daily Artificial Intelligence Briefing"
date: "August 7, 2026"
edition: "All Sources Edition"
volume: "2026"
number: "219"
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

:::lead(id="lead-top-story", label="Top Story", title="OpenAI gives free ChatGPT users unlimited text chats")
collapsing the Instant/Thinking split so GPT-5.6 Sol powers every paid chat while Free and Go tiers get unlimited GPT-5.6 Luna plus a "Think" button. The one quantified claim — 68% fewer factually wrong responses — is measured against GPT-5.5 Instant, the non-reasoning tier, so it reads more as a routing change than a capability jump (OpenAI, The Verge, TechCrunch, The Decoder).

AI models designed 16 working viruses, as Arc Institute and Stanford researchers led by Brian Hie published in Science the first complete bacteriophage genomes written from scratch by the Evo 1 and Evo 2 genome language models. Viruses capable of infecting complex organisms were excluded from training data and the work ran in a secure lab (Science via NYT/BBC, Ars Technica, Twitter).

AMD acquires inference-chip startup Taalas, buying a company that hardwires a single model directly into silicon — the second model-specific-silicon acquisition of the cycle after Nvidia–Groq. No deal terms and no first-party statement from either company have surfaced (The Register, HN, Twitter).

Anthropic will design its own AI chips, confirming an in-house silicon team in a move framed alongside OpenAI's as both labs scaling capacity while reducing Nvidia dependence. It landed the same day AMD bought Taalas, making custom inference silicon the day's dominant infrastructure theme (Ars Technica).
:::

:::figure(src="https://cdn.arstechnica.net/wp-content/uploads/2025/01/amodei_header_1-1152x648.jpg", alt="Anthropic will design its own hardware to power Claude", caption="Anthropic will design its own hardware to power Claude", source-url="https://arstechnica.com/ai/2026/08/anthropic-confirms-plans-to-build-an-in-house-silicon-team/", variant=wide)
:::

:::briefs(id="briefs-stories", title="Stories", columns=2)
- headline: "OpenAI ends the Instant-versus-Thinking split in ChatGPT, making GPT-5.6 Sol the single model behind…"
  tag: "Breaking"
- headline: "Arc Institute publishes AI-written viral genomes in Science, with Evo 1 trained on 2.7…"
  tag: "Breaking"
- headline: "Anthropic confirms an in-house silicon team, saying it will design its own hardware to…"
  tag: "Breaking"
- headline: "GPT-5.6 Sol / Luna (OpenAI). Sol becomes the default across all paid ChatGPT surfaces…"
  tag: "Models"
- headline: "Qwen3.8 Max was ranked best overall model on Artificial Analysis's agentic index"
  tag: "Models"
- headline: "No model launch cleared the independent-verification bar in the news-research sweep for the 2026-08-06/07…"
  tag: "Models"
- headline: "Reported but unconfirmed"
  tag: "Models"
- headline: "OpenAI × American Psychological Association partnership on evidence-based guidance, resources and safeguards for youth…"
  tag: "Policy"
- headline: "OpenAI v. Apple trade secrets"
  tag: "Policy"
- headline: "Meta's Alexandr Wang publicly named Mercor and Surge, arguing data companies serving the US…"
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
"A million-line codebase (also known as a 'harness'), running at inference time, orchestrating thousands of calls to a neural network for any given task, is the exact definition of a 'neurosymbolic architecture'." — François Chollet (@fchollet, 2.6K likes), closing the ARC-AGI-3 harness dispute by conceding the definition rather than the result. It lands on the same day the top agent paper credits its SWE-Bench Pro number to the harness rather than the model.
:::
