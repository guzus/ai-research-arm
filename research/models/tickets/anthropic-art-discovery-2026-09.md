---
slug: anthropic-art-discovery-2026-09
title: Claude discovers "ART" — a novel phage reverse-transcriptase system, from Anthropic's new wet lab
company: Anthropic
model: Claude
status: confirmed
status_note: |
  Announced 2026-09-23 18:18 UTC by @AnthropicAI: "Claude has discovered a
  previously unknown enzyme system hidden in the DNA of bacteriophages. Beside
  the enzyme's gene sits a long array of repeating DNA — a structure that looks
  somewhat similar to CRISPR." Anthropic is explicit about the limit: "We don't
  yet understand what this system does."

  Two claims, and they should not be merged. (1) The biology: an unusual reverse
  transcriptase sitting next to a partner gene and a repeat array that produces
  distinct short RNAs — named ART. (2) The method: this is the first result from
  Anthropic's **new molecular biology lab**, where a team of Anthropic
  biologists uses Claude to generate hypotheses their scientists then test in a
  BSL1/BSL2 facility. The second claim is the one this ticket is really about;
  the first is an open question by Anthropic's own admission.

  Campaign scale, reported by @AndrewCurran_ quoting the write-up and by
  @rohanpaul_ai: ~950 Claude agent sessions over ~21 hours, 215.6M tokens,
  1.94B protein clusters searched, 198,290 RT clusters recovered, 19 reports
  produced. One agent noticed a repeat array *outside* the features the search
  was set up to examine.

  Contested framing, on the record. @DarioAmodei: "The work was done mostly,
  though not entirely, by Claude." @NaderLikeLadder pushes back directly: "That
  isn't true. It was done by some of the smartest life science researchers in
  the world, using every tool at their disposal." @BoWang87 (Xaira) is the
  substantive scientific caveat: repeat-rich regions in assembled phage genomes
  are error-prone, he wants "raw read support across the arrays and their
  boundaries in independent isolates," and notes a Stanford team independently
  described a similar-but-distinct RT system — which Dario also acknowledges.
expected: "Function of ART is unknown. Watch for a preprint/paper with raw read support, and for whether the system proves programmable."
labels:
  - anthropic
  - ai-for-science
  - biology
  - agentic-research
verification: confirmed
sources:
  - https://x.com/AnthropicAI/status/2102824959827742916
  - https://x.com/AnthropicAI/status/2102824961538920822
  - https://x.com/DarioAmodei/status/2102835095740830082
  - https://x.com/AndrewCurran_/status/2102828524201816228
  - https://x.com/rohanpaul_ai/status/2103031424777658749
  - https://x.com/BoWang87/status/2102903234000191869
  - https://x.com/NaderLikeLadder/status/2102862367407428061
  - https://x.com/WesRoth/status/2102889195329245256
created_at: 2026-09-24
updated_at: 2026-09-24
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-24
    change: "Created — CONFIRMED. On 2026-09-23 18:18 UTC @AnthropicAI announced that Claude discovered a previously unknown enzyme system in bacteriophage DNA — an unusual reverse transcriptase beside a repeat array that produces distinct short RNAs, named ART — and that this is the first result from Anthropic's new molecular biology lab. Anthropic states plainly that the system's function is unknown. @DarioAmodei published a long companion post describing the workflow (life-sciences team picked the area, Claude read literature and genome data and proposed experiments, Anthropic scientists ran them in a BSL1/BSL2 facility) and tied it to a claimed exponential in AI-for-biology. Campaign scale via @AndrewCurran_ and @rohanpaul_ai: ~950 agent sessions, ~21 hours, 215.6M tokens, 1.94B protein clusters searched, 198,290 RT clusters recovered, 19 reports. Verification confirmed on company-primary sources. Recorded as an explicit counter-record rather than smoothed over: @NaderLikeLadder disputes Dario's \"done mostly by Claude\" framing as diminishing the human researchers, and @BoWang87 (Xaira) — a domain practitioner — flags that repeat-rich phage assemblies are error-prone and asks for raw read support across array boundaries in independent isolates, while noting a Stanford group independently described a similar but distinct RT system (also acknowledged by Dario)."
---

The headline is a biology result; the durable claim is a methodology one. What
Anthropic actually shipped on 2026-09-23 is evidence that a large agent swarm
can do the *noticing* step of science at a scale no lab can staff — ~950 Claude
sessions, ~21 hours, 215.6M tokens, ~200,000 reverse transcriptases surveyed.
The find itself came from an agent following something it was not told to look
for: a repeat array next to an odd RT, outside the search's declared feature
set.

That is why @BoWang87's framing is the right one to hold. "Scaling scientific
attention" is a claim that survives even if ART turns out to be mundane; "Claude
discovered CRISPR 2.0" (@WesRoth) is a claim that does not, and Anthropic itself
did not make it. The company's own post says the function is unknown, that only
a handful of known systems share its features, and that much more work is
needed.

Two caveats are load-bearing and both come from people who work in this area.
The assembly caveat: repeat-rich regions in assembled phage genomes are exactly
where spurious structure appears, so raw read support across the arrays and
their boundaries, in independent isolates, is the experiment that would settle
whether ART is real as described. The priority caveat: a Stanford team
independently described a novel RT system with an associated non-coding array
that is similar in some ways — Dario names this in his own post, and calls the
systems distinct and independently evolved.

The attribution fight is worth logging because it will recur. Dario's "the work
was done mostly, though not entirely, by Claude" is the sentence that drew
pushback, and the objection is not anti-AI — it is that the sentence erases the
researchers who chose the domain, designed the validation, and ran the bench
work. Both descriptions of the same event are in the record here.

Related: [[anthropic-protein-binder-design-2026-08]] (Claude de novo protein
binder design), [[anthropic-claude-science-2026-06]] (the Claude Science
workbench, closed), [[anthropic-fermat-lean-proof-2026-09]] (the mathematics
analogue Dario's exponential argument leans on), and
[[anthropic-pace-the-frontier-2026-09]] for the safety framing Anthropic is
simultaneously arguing.
