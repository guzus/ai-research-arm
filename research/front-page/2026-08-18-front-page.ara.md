---
title: "THE AGI AWARENESS POST"
kicker: "Your Daily Artificial Intelligence Briefing"
date: "August 18, 2026"
edition: "All Sources Edition"
volume: "2026"
number: "230"
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

:::lead(id="lead-top-story", label="Top Story", title="Nvidia guarantees $105B of OpenAI's Ohio lease")
the chipmaker agreed to backstop up to $105 billion of OpenAI's 20-year lease at the PORTS-Pike campus because OpenAI cannot borrow on its own credit. That guarantee, not the separately reported $1.5B equity stake in developer SB Energy, is the real exposure (The Decoder, TechCrunch, The Information via @theinformation/@rohanpaulai).

Anthropic reports $65B annualized run rate, the company told investors over the weekend that annualized revenue hit $65 billion at end-July on preliminary Q2 revenue of $11.5 billion, up 14x year over year, with positive adjusted operating income. All figures are company-supplied and unaudited ahead of a reported September listing window (Bloomberg via @kimmonismus, @AndrewCurran).

Stripe acquires OpenRouter for over $7B, Bloomberg reports the payments company is buying the model-routing gateway at more than 5x its $1.3B May valuation. The mechanism that surfaced this cycle: Stripe already runs OpenRouter's billing and has an LLM-token billing product in beta that needs a router underneath it (TechCrunch, The Decoder, Stratechery).

DeepSeek's V4 Pro repricing goes live, the new card charges $1.32/$3.96 per Mtok at peak and exactly half off-peak, making even the cheapest output rate 2.28x last week's. Independent WeirdML scoring puts Pro at 66.2% against its own cheaper Flash tier at 63.0% (@thisisdimm, @htihle, VentureBeat).
:::

:::briefs(id="briefs-stories", title="Stories", columns=2)
- headline: "Nvidia backstops OpenAI's record Ohio data center lease, the guarantee is capped at $105…"
  tag: "Breaking"
- headline: "Anthropic discloses $11.5B in preliminary Q2 revenue, up from $787 million a year earlier…"
  tag: "Breaking"
- headline: "Groq raises $350M at a $3.5B valuation, roughly half its $6.9 billion September 2025…"
  tag: "Breaking"
- headline: "DeepSeek V4 Pro's price card is live at $1.32/M input and $3.96/M output at…"
  tag: "Models"
- headline: "The premium tier buys about 3.2 points"
  tag: "Models"
- headline: "Qwen3.8-27B has a canonical serving path. llama.cpp's Georgi Gerganov showed llama serve -hf ggml-org/Qwen3.8-27B-GGUF…"
  tag: "Models"
- headline: "Qwen 3.8 2.4T A95B scored 75.2% on WeirdML at extra-high reasoning, second-best open model…"
  tag: "Models"
- headline: "Vice President JD Vance put the doom-marketing charge on the record in a \"Diary…"
  tag: "Policy"
- headline: "Dario Amodei says the AI backlash is \"fundamentally a crisis of trust,\" rejecting glitzy…"
  tag: "Policy"
- headline: "Anthropic's EU watermarking compliance drew a prior-art objection, with critics arguing the SynthID-Text-style technique…"
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
"Independent swarms converging on the same wrong answers and models hallucinating in wild ways when they don't have ways to verify against reality really tempers my expectations." — @davis7, reporting that his DEF CON GoldBug agent swarms solved 3 of 13 puzzles — while his human team took the Black Badge. The convergence detail is the load-bearing one: parallel sampling is the standard remedy for model error and it assumes the errors are independent. On tasks with no verifier, swarm size does not buy correctness. He is reporting against his own interest, which is why it counts.
:::
