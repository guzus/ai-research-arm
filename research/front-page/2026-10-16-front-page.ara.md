---
title: "THE AGI AWARENESS POST"
kicker: "Your Daily Artificial Intelligence Briefing"
date: "October 16, 2026"
edition: "All Sources Edition"
volume: "2026"
number: "289"
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

:::lead(id="lead-top-story", label="Top Story", title="Anthropic shows IPO investors $16.8B Q3 revenue")
up 45% from Q2's $11.6B, with adjusted profitability, positive free cash flow and a reported target of a $110B run rate by year-end. "Adjusted" is undefined until a filing appears (Bloomberg, Reuters, FT via Simon Willison, The Decoder).

Meta releases Muse Spark Open open weights: an 816B-total / 42B-active multimodal MoE with 1M context, tuned with Apple to run on two M5 Ultra Mac Studios. It became the #1 AI story on HN, at 543 points (@AIatMeta, TechCrunch, The Verge, HN).

TSMC posts record Q3, says AI demand exceeds supply: net profit rose 68.7% year on year, and Q4 revenue is guided to $52.3–54.3B on a "steep ramp-up" of 2nm. This landed a day after CPI drove a sell-off in AI stocks (TSMC 6-K, Twitter relays).

Eight states sue OpenAI over ChatGPT child safety: the suits were filed separately in each state's own court. They frame "agreeable by design" sycophancy as consumer-protection and public-nuisance liability (Reuters via Twitter, The Verge, r/artificial).
:::

:::figure(src="https://platform.theverge.com/wp-content/uploads/sites/2/2026/09/268742_Mac_Studio_AKrales_0025.jpg?quality=90&strip=all&crop=0%2C10.732984293194%2C100%2C78.534031413613&w=1200", alt="Meta and Apple team up to make Muse AI models run better on Macs", caption="Meta and Apple team up to make Muse AI models run better on Macs", source-url="https://www.theverge.com/news/1012293/meta-apple-muse-spark-open-ai-model-mlx", variant=wide)
:::

:::briefs(id="briefs-stories", title="Stories", columns=2)
- headline: "Anthropic discloses Q3 numbers to prospective IPO investors"
  tag: "Breaking"
- headline: "Meta and Apple ship Muse Spark Open"
  tag: "Breaking"
- headline: "Eight Republican-led states file separate suits against OpenAI"
  tag: "Breaking"
- headline: "Muse Spark Open (Meta)"
  tag: "Models"
- headline: "NVIDIA Nemotron 3.5 Super VL (120B-A12B) and Bolt (74B-A9B)"
  tag: "Models"
- headline: "Gemini 4 Argon verified on ARC-AGI-3 at 97.5% using Google's own harness ($4.8K), but…"
  tag: "Models"
- headline: "Microsoft MAI-Base-2 finishes pre-training: 16K GB200s over 38 days"
  tag: "Models"
- headline: "State AG litigation against OpenAI: eight separate state-court suits over child safety"
  tag: "Policy"
- headline: "FTC investigation of Anthropic and OpenAI security incidents (Axios via Ars), coming despite the…"
  tag: "Policy"
- headline: "Hinton/Bengio open letter"
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
"Using Gemini 4 makes you realize how many other models must be distilling Claude/GPT (or using a similar training pipeline). It feels quite different than other models." — Ethan Mollick (@emollick.bsky.social), on the same day Anthropic reportedly told investors distillation was 5–7% of its revenue
:::
