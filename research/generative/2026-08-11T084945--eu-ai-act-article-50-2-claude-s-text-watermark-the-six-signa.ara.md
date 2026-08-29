---
eyebrow: POLICY · EU AI ACT
title: "Article 50(2): what Claude's watermark actually is, and three numbers that are wrong"
deck: Anthropic shipped a text watermark for a European transparency law. The framing that travelled with it — six signatories, xAI's refusal, a 400-token detectability floor — survives contact with the primary sources in none of its three particulars.
domain: policy
lede: |
  On 10 August 2026 Anthropic published a help-centre page saying it had signed the EU's Article 50(2) Code of Practice and that Claude now weaves an imperceptible watermark into generated text. The page is real, short, and unusually candid about its own limits. Almost everything attached to it since is not. The Commission counts about 190 signatories, not six. xAI is absent from the list, which is not the same thing as refusing. And no source anywhere — not Anthropic, not the Code, not the Guidelines — states a 400-token detectability floor; the Code's only text threshold is 200 tokens, and it is a scoping rule, not a detection bar. Underneath the corrections sits the fact nobody reported: Anthropic's newest model shipped nine days before the cutoff its own policy keys to.
stats:
  - {label: Code signatories, value: "~190", note: "82 providers / 152 deployers"}
  - {label: Text threshold in the Code, value: 200, unit: "tokens"}
  - {label: Claude models marked at launch, value: 0, note: "as of 2026-08-11"}
  - {label: Art. 99(4) exposure, value: "3%", note: "of worldwide turnover, or €15M"}
---

:::callout(kind=info, label="Direct answer")
- **The watermark is real.** Anthropic signed the Article 50(2) Code of Practice as a provider of both models and systems, and says generated text carries an imperceptible model-level watermark applied worldwide, with C2PA-signed metadata on `.svg`, `.png` and `.jpg` files.[^1]
- **"Six signatories" is wrong by a factor of about thirty.** The Commission records roughly 190 organisations — 82 under Section 1 (providers) and 152 under Section 2 (deployers).[^2]
- **"xAI's refusal" is unsupported.** xAI is absent from the list, and no public statement of refusal exists. It *did* sign only one of three chapters of the separate 2025 GPAI Code — a different instrument governing a different article.[^31]
- **"A 400-token detectability floor" has no source.** Anthropic states no token count at all.[^1] The Code's only free-form-text number is 200 tokens.[^6] 400 tokens is a benchmark *generation length* in Google's SynthID-Text paper.[^16]
- **The unreported fact:** Anthropic's marking promise applies to "models launched on or after August 2, 2026".[^1] Claude Opus 5 launched 24 July 2026.[^11] No shipping Claude model qualifies.
:::

## 01. What Anthropic actually shipped, and the date that undoes the headline

Anthropic's disclosure arrived not as a newsroom post but as a help-centre article. It says the company "has signed the EU AI Act's Article 50(2) Code of Practice on Transparency of AI-Generated Content, as a provider" of both generative AI models and generative AI systems.[^1] Two techniques are described. For text, Claude "weaves an imperceptible watermark directly into the text itself" — a model-level mark that "will travel with the text when it's copied and pasted elsewhere, and may persist through some editing."[^1] For files, Anthropic applies signed provenance metadata following the C2PA standard to supported types.[^1] Coverage is asserted across five surfaces — Claude Platform, Claude, Claude Code, Claude Cowork, Claude Tag — plus AWS, Google Cloud and Microsoft Foundry, and applies "wherever Claude is offered, worldwide."[^1,13] The page hedges once, on the metadata layer only: "Signed provenance metadata may not be supported on every platform."[^1]

That worldwide framing is the most consequential voluntary choice in the announcement. Nothing in Article 50(2) requires marking outputs served to users in Ohio. Anthropic, whose EU entity is Anthropic Ireland and whose EMEA region it has called its "fastest-growing,"[^52] chose the single global standard — the classic Brussels-effect move. It is worth noting that the theory's originator now thinks that reflex is weakening: Anu Bradford's view is that "the high-water mark of Europe's regulatory leadership is behind us," precisely because complying globally with the strictest standard "might earn them punishment elsewhere."[^51] Anthropic's choice cuts against that, and is evidence of the effect rather than of its decline.

The sentence that governs everything else is narrower than the coverage claim: "Claude models launched on or after August 2, 2026 support marking at launch."[^1] Everything older sits in a transition period, with retrofit described only as "in progress" and no completion date.[^1] A second fetch of the same page returned the sentence with an "in the EU" qualifier attached, which sits awkwardly beside the worldwide claim; the cutoff date is identical in both renderings.[^1]

Anthropic's newest model, Claude Opus 5, launched on 24 July 2026 — nine days before that cutoff — and its announcement mentions watermarking, provenance and the AI Act not once.[^11] Anthropic's own Transparency Hub, last updated 23 July 2026, dates the Claude 5 family to June 2026 and does not list Opus 5 at all.[^12] On the public record, ==no shipping Claude model was launched on or after 2 August 2026==, which means the "at launch" guarantee currently binds nothing, and every marked output must come from the undated retrofit path.

:::timeline
- {date: 2026-06-10, headline: "Code of Practice published", body: "The AI Office releases the Transparency Code, drafted by independent experts."}
- {date: 2026-07-08, headline: "Commission adequacy opinion", body: "The AI Board adopts its assessment the following day; adherence is expressly not conclusive evidence of compliance.[^39]"}
- {date: 2026-07-20, headline: "Article 50 Guidelines adopted", body: "The Commission publishes its interpretive guidance alongside the Code.[^46]"}
- {date: 2026-07-24, headline: "Claude Opus 5 launches", body: "Nine days before the marking cutoff Anthropic's policy keys to.[^11]"}
- {date: 2026-07-27, headline: "Digital Omnibus enters into force", body: "Annex III high-risk duties slip to 2 December 2027; Article 50 keeps its application date.[^30]"}
- {date: 2026-07-31, headline: "Initial signatory list published", body: "About 190 organisations; 82 Section 1, 152 Section 2."}
- {date: 2026-08-02, headline: "Article 50 applies", body: "Enforcement powers of the AI Office and national authorities commence."}
- {date: 2026-08-10, headline: "Anthropic publishes its marking page", body: "No detector, no technical documentation, no numbers."}
- {date: 2026-12-02, headline: "Grace period ends", body: "Article 50(2) marking bites on systems placed on the market before 2 August 2026."}
- {date: 2027-02-02, headline: "Interoperability deadline", body: "Code signatories must implement a watermark-detection interoperability solution."}
:::

The counterpoint worth stating plainly: a model launch is not the only way to place a system on the market, and Anthropic serves Claude as a *system*, continuously updated, not as a boxed product. A regulator could reasonably read a retrofitted serving stack as in scope. But that reading is the regulator's to make, and Anthropic has not published which models are marked today. This matters because it is the difference between a shipped compliance measure and a shipped compliance *intention*.

## 02. Auditing the framing: three claims, three corrections

Each of the three circulating claims is wrong in an instructive way. None is a random error; each is a real fact detached from its instrument.

| Claim as circulated | Status | What the primary sources say |
|---|---|---|
| *"The six signatories"* | **False** | ~190 organisations: 82 Section 1, 152 Section 2.[^2] The Code was drafted by independent experts; there is no official grouping of six.[^54] |
| *"xAI's refusal"* | **Unsupported** | xAI is absent from the list. Absence is not refusal, and the Commission names no refusers.[^2] xAI *did* decline two of three chapters of the 2025 **GPAI** Code.[^31] |
| *"The 400-token detectability floor"* | **False as stated** | Anthropic states no token count.[^1] The Code's threshold is **200** tokens.[^6] 400 is SynthID-Text's benchmark text length.[^16] |
| *"Claude output is watermarked today"* | **Unverified** | Only models launched on or after 2 Aug 2026 are marked at launch; none exists.[^1,11] |

The pattern is that a real number gets lifted out of the instrument that gives it meaning. 200 tokens is real, but it scopes *when to watermark*, not *when detection works*. 400 tokens is real, but it is Google's test-corpus length, not Anthropic's floor. xAI's refusal is real, but it belongs to Article 53 model documentation, not Article 50 output marking. A reader who accepted all three would have a confident and entirely false picture of a regime whose actual weaknesses lie elsewhere.

:::statement(attr="ARA Research")
Every one of the three errors makes the regime sound more precise and more contested than it is. The real problem is the opposite: the obligation is vaguer than reported, and almost nobody is refusing it.
:::

## 03. Article 50(2): the obligation, and the three qualifiers that hollow it out

The operative duty is short. Providers of AI systems generating synthetic audio, image, video or text must ensure "the outputs of the AI system are marked in a machine-readable format and detectable as artificially generated or manipulated."[^7] Then comes the standard: solutions must be "effective, interoperable, robust and reliable as far as this is technically feasible," accounting for "the specificities and limitations of various types of content, the costs of implementation and the generally acknowledged state of the art."[^7]

Three qualifiers do enormous work. *Technical feasibility* is a standing defence, and the academic literature on watermark removal is precisely the evidence a provider would cite for it. *Costs of implementation* invites a proportionality argument. *Generally acknowledged state of the art* is a floating benchmark that today is set by the very firms subject to it. Recital 133 names the contemplated techniques — watermarks, metadata identifications, cryptographic provenance methods, logging, fingerprints — and repeats the feasibility qualifier rather than resolving it.[^10] A further carve-out disapplies the duty where the system "perform[s] an assistive function for standard editing or do[es] not substantially alter the input data."[^7]

Article 50(2) binds providers. Article 50(4) is a separate deployer duty covering deepfakes and public-interest text, with exemptions for evidently artistic or satirical work and for text under human editorial control.[^7] The Commission is explicit that the two do not substitute: deployers "cannot simply rely on the machine-readable marking embedded in the content by the provider," because their disclosure must be perceivable without specialist tools.[^3]

Dates matter more than usual here. Article 50 applies from 2 August 2026.[^3,9] The Digital Omnibus, in force from 27 July 2026, deferred Annex III high-risk obligations to 2 December 2027 and Annex I to 2 August 2028, and left Article 50's *application date* untouched — though not its text: the Commission's own Article 50 page carries a notice that the article has been amended by the omnibus.[^30,7] What it did add is a limited grace period: for AI systems placed on the market before 2 August 2026, the Article 50(2) marking duty bites "only as from 2 December 2026."[^3] Content generated before 2 August 2026 needs no retroactive labelling.[^3]

Penalties sit in Article 99(4), which captures Article 50 transparency breaches and sets fines of up to €15,000,000 or 3% of total worldwide annual turnover, whichever is higher.[^8] The Commission's own FAQ restates the figure.[^3] Article 99(6) inverts the test to whichever is *lower* for SMEs and start-ups.[^8]

:::compare
- {role: "SMALLER FIRM", name: "3% of €200M turnover", value: "€6M → €15M floor binds"}
- {role: "LARGER FIRM", name: "3% of €40B turnover", value: "€1.2B"}
- {role: "CROSSOVER", name: "3% × €500M", value: "= €15M exactly"}
:::

The €500M crossover is the point at which the percentage term overtakes the flat floor. Anthropic stated run-rate revenue above $47 billion in May 2026;[^35] whatever its audited turnover proves to be, it is far above the crossover, so its exposure is governed by the percentage, not the cap. Two caveats before anyone does the multiplication: run-rate is not "total worldwide annual turnover for the preceding financial year," and Anthropic publishes no audited revenue figure at all.

## 04. The Code of Practice: two layers of marking, and a 200 that is not a floor

The Code, published 10 June 2026, is where the abstraction becomes operational. Its central design choice is that no single technique satisfies Article 50(2)'s four adjectives, so it "generally requir[es] at least two layers of machine-readable marking" — digitally signed, time-stamped, tamper-proof metadata plus an imperceptible watermark, with fingerprinting and logging optional.[^5,6]

Free-form text is the exception, and for a structural reason. A `.png` has a container into which a signed manifest can be written; raw words in a chat window or pasted into a form have no container at all. So for free-form text "the watermark alone is sufficient to meet the marking requirement since such text cannot transport metadata."[^6] The rule tracks the presence of a container, not the fact of being text: a `.docx` or `.pdf` still needs both layers.[^37]

Notably, the Code names technique *categories* rather than standards. It does not name C2PA — though the IPTC, itself a C2PA stakeholder, argues that "while it is not named specifically, the only technology that meets these criteria is C2PA."[^49] That reticence is defensible in a technology-neutral instrument and awkward in practice, because the metadata layer has a measured survival problem. A survey of 50 generative AI image systems found only 19 embedded any machine-readable marking at all, and only five used C2PA.[^41] The standards community's answer is Durable Content Credentials — pairing the manifest with an invisible watermark and a content fingerprint so a stripped manifest can be looked up again.[^40] Its published implementations are image watermarking, and fingerprinting presupposes perceptual redundancy that a paragraph of text does not have. For text, the second layer is not merely waived; it has nowhere to live.

This is where 200 tokens enters. The Code provides that "the reliability requirements for watermarking are less strict for very short texts (fewer than 200 tokens)."[^6] Practitioner readings differ on how hard that line is — one reads it as a relaxed-reliability tier above which watermarking is still expected, another as a scoping rule under which text below 200 tokens need not be watermarked at all.[^6,38] ==The Code's own PDF is not machine-readable, so the precise operative wording could not be verified at source for this article.== What both readings agree on is the number, and on what it is *not*: a statement about the length at which any particular detector works. It is a rule about when the duty applies, written by lawyers, not a measured property of any watermark.

:::kv
- {term: "Default marking layers", def: "At least two — signed metadata plus imperceptible watermark"}
- {term: "Free-form text", def: "One layer; watermark only, because text carries no metadata container"}
- {term: "Text threshold", def: "200 tokens — reliability expectations relaxed below it"}
- {term: "Quantitative performance bar", def: "None. No accuracy, false-positive or survival rate is specified"}
- {term: "Detection access", def: "Free to authorities, researchers, media and fact-checkers; fee exception below 1M monthly users"}
- {term: "Interoperability deadline", def: "2 February 2027"}
- {term: "Legal effect of signing", def: "No presumption of conformity"}
:::

The absence in that table is the important entry. The Code enumerates the attacks a solution should withstand — recompression, screenshotting, cropping, paraphrasing, translation cycles, print-and-scan — but requires only that solutions "maintain intended performance levels," with "intended" undefined and the threat model self-scoped.[^5] One measure states outright that "there is no quantitative evaluation metric linked to this Measure."[^5] Until the AI Office endorses external benchmarks, signatories may test against internal ones.[^5]

Nor does signing buy legal cover. The Commission's position is that "any enforcement consequences would relate to non-compliance with obligations in Article 50 of the AI Act, not the absence of adherence to the code."[^4] Practitioners put it more bluntly: adherence "does not give rise to a genuine presumption of conformity, however, let alone an irrefutable one."[^6] What signatories get is procedural — non-signatories "may be subject to a larger number of requests for information."[^4] That is a triage differential, not a safe harbour, and conflating the two is the single most common error in commentary on the Code.

## 05. Detection versus length: what the numbers actually are

The reason a length threshold exists at all is statistical, not regulatory. Green-list watermark detectors run a one-proportion hypothesis test on how many generated tokens fall in a pseudo-randomly chosen "green" set. The test statistic in the canonical scheme is `z = (|s|_G − γT) / √(Tγ(1−γ))`, so evidence accumulates with the square root of the token count `T`.[^14] Short text simply does not contain enough trials to reject the null at a demanding false-positive rate.

That structure means the "floor" is not a property of a watermark but of a watermark *plus* a chosen error rate. The follow-up paper gives the relationship explicitly: required tokens scale with the square of the z-threshold.[^15] Tightening from a 1-in-100 false-positive rate to 1-in-a-million therefore costs roughly four times more text, not four times more confidence — an arithmetic consequence of the formula rather than a measured result.

The published anchors bracket 400 tokens on both sides, and none of them is Anthropic's:

:::rank-list
- {label: "16 tokens — idealised hard watermark, every token green", value: "z = 4", pct: 8}
- {label: "35 tokens — average z > 5 under beam search", value: "z > 5", pct: 12}
- {label: "50 tokens — SynthID-Text, TPR ≈ 0.30 at 1% FPR", value: "0.30 TPR", pct: 18}
- {label: "200 tokens — EU Code of Practice reliability pivot", value: "regulatory", pct: 45, highlight: true}
- {label: "400 tokens — SynthID-Text benchmark generation length", value: "benchmark", pct: 70}
- {label: "800 tokens — detectable at 1e-5 FPR after strong human paraphrase", value: "1e-5 FPR", pct: 100}
:::

The 16- and 35-token figures come from the original watermarking paper under favourable assumptions.[^14] The 50-token and 400-token SynthID figures come from a 2026 re-analysis reporting a maximum true-positive rate around 0.30 at 1% false-positive rate for 50-token text, rising to roughly 85% at 400 tokens — the latter under a Bayesian score function with 30 tournament layers, so the two anchors are not two points on one curve.[^17] The 800-token figure is Kirchenbauer et al.'s headline robustness claim: after strong human paraphrasing, the watermark is "detectable after observing 800 tokens on average, when setting a 1e-5 false positive rate."[^15]

In the Nature SynthID-Text paper, 400 tokens is a caption: "Texts are length 400 tokens, generated from Gemma 7B-IT at three different model temperatures."[^16] The same paper elsewhere uses 200-token texts, so 400 is not even SynthID's canonical length.[^16] It is a test condition that migrated into a claim about a different company's undisclosed scheme.

:::note
The figures above come from different papers, models, watermark families and error rates, and are not directly comparable. They are assembled to show the range in which published thresholds fall — roughly 16 to 800 tokens depending entirely on the assumptions — not to describe a single curve.
:::

The counterpoint: none of this establishes that Claude's floor *isn't* around 400 tokens. Anthropic has published no algorithm, no key scheme and no performance figures, so the number is unfalsifiable rather than false. That is itself the finding. A regime whose central technical claim cannot be checked by anyone outside the provider has a verification problem that no token count fixes.

## 06. Robustness: the attack literature the feasibility defence rests on

Article 50(2) asks for solutions that are "robust." The academic record on text watermarks is the most important context for judging whether that word is being met or merely invoked.

Paraphrasing is devastating and cheap. DIPPER paraphrasing drops DetectGPT's accuracy from 70.3% to 4.6% at a constant 1% false-positive rate.[^18] Watermarks fare better but not well: the same study degrades the Kirchenbauer detector from 100.0% to 57.2% in its strongest paraphrase setting, while concluding watermarking is nonetheless "the most resilient detector to paraphrasing."[^18] Recursive paraphrasing pushes soft watermarking from 99% to 15% true-positive rate at 1% FPR.[^19] Commercial humanizer tooling reproduces the effect against a SynthID reimplementation, taking detection from 87.6% to 5.4% at 5% FPR and from 66.5% to 1.5% at 1%.[^23]

:::slope(left-label="Clean text", right-label="After paraphrase", unit=%)
| Detector | Clean | Paraphrased |
|---|---|---|
| DetectGPT (zero-shot) | 70.3 | 4.6 |
| Soft watermark, recursive | 99.0 | 15.0 |
| SynthID reimpl. (humanizer) | 66.5 | 1.5 |
| KGW watermark (strongest DIPPER) | 100.0 | 57.2 |
:::

:::source
Detection accuracy or true-positive rate, all at a 1% false-positive rate; different models, corpora and watermark implementations per row. DetectGPT and KGW from Krishna et al. (2023); soft watermark from Sadasivan et al. (2023); SynthID reimplementation from Kumarage et al. (2025). Not a controlled comparison.
:::

Translation works too: routing watermarked text through a pivot language drops area-under-curve from 0.95 to 0.67 "without performance loss."[^22] And removal is not the worst case. Jovanović et al. showed a watermark can be approximately reverse-engineered from API queries alone, so that "for under $50 an attacker can both spoof and scrub state-of-the-art schemes previously considered safe," at an average success rate over 80%.[^21] Spoofing is the more corrosive attack, because it lets an adversary attach a provider's mark to content that provider never generated. Zhang et al. go further, proving strong watermarking impossible against an attacker with a quality oracle and a perturbation oracle, and empirically removing marks from three published schemes "with only minor quality degradation."[^20]

There is a genuine expert disagreement here, and it should not be flattened. Kirchenbauer et al.'s counter-position is that paraphrases leak n-grams of the original, so watermarks survive if enough text is observed — the 800-token result above.[^15] That is a real defence, and it is also a concession: 800 tokens is roughly 600 words, and most of the artefacts anyone wants to adjudicate (a social post, an exam answer, a product review, a comment) are far shorter. Google DeepMind, whose scheme is the most deployed, says so itself: SynthID "isn't built to directly stop motivated adversaries" and "isn't a silver bullet."[^32]

## 07. Roughly 190 signatories, and why the count means less than it looks

The Commission's own page is unambiguous: "About 190 organisations signed the Code of Practice on Transparency of AI-generated Content," recorded as 82 Section 1 signatories and 152 Section 2 signatories.[^2] The two numbers sum to 234 because organisations may sign both sections, which is why the Commission hedges with "about." Section 1 examples named by the Commission are Aleph Alpha, Anthropic, Black Forest Labs, Cohere, Google, Meta, Microsoft, Mistral, OpenAI and Synthesia — ten, not six.[^2]

:::compare
- {role: "AS CIRCULATED", name: "\"the six signatories\"", value: "6"}
- {role: "COMMISSION FIGURE", name: "Organisations signed", value: "~190"}
- {role: "LIST ENTRIES", name: "Section 1 + Section 2", value: "234"}
:::

The headline count nonetheless overstates the industry consensus in one direction and understates the story in another. About half the signatories are "small and recent companies," on the Commission's own characterisation, and the roster includes public bodies with no generative output to mark.[^2] Signature is an intent instrument, not evidence of shipped technology: of the named Section 1 frontier providers, only Google and Anthropic have publicly documented a shipped *text* watermark, and for systems already on the market that is lawful until 2 December 2026 anyway.[^2,3]

The genuinely interesting name is Meta. Meta publicly refused the 2025 GPAI Code, with Joel Kaplan writing that "Europe is heading down the wrong path on AI."[^53] Twelve months later Meta signed Section 1 of the transparency Code.[^2] That single fact does more analytical work than the signatory count: it shows refusal is instrument-specific rather than a blanket rejection of EU AI regulation, and it isolates xAI rather than placing it in a bloc.

What would weaken this reading: the Commission publishes no country or size breakdown, no machine-readable export of the list, and updates it on a rolling basis, so any composition claim beyond the ten named examples is reconstructed rather than sourced.[^2] It is also worth keeping the denominator in view. Eurostat records that 20% of EU businesses used AI at all in 2025 — 55% of large firms against 19% of SMEs, and 42% in Denmark against 5% in Romania.[^50] A voluntary code signed by roughly 190 organisations is not a proxy for a market that is itself unevenly exposed to the technology being regulated.

## 08. xAI: absence is not refusal, and refusal would barely matter

xAI does not appear on the Commission's transparency-Code signatory list.[^2] That is the whole of the verified record. No xAI statement about the 2026 Code, Article 50, watermarking or provenance could be located, and the Commission names no refusers.[^2]

The factual substrate for the "refusal" framing is real but belongs elsewhere. On the 2025 General-Purpose AI Code of Practice, the Commission's own page records that "xAI signed up to the Safety and Security Chapter" and must therefore "demonstrate compliance with the AI Act's obligations concerning transparency and copyright via alternative adequate means."[^31] That is a genuine partial refusal — the only one the Commission discloses — but the GPAI Code implements Article 53 model documentation, not Article 50 output marking. The two are different instruments, different articles, different duties.

Three consequences follow, and they cut against the drama.

First, non-signature is not a breach. The Commission states flatly that "signing the code of practice is voluntary. Not signing it does not constitute non-compliance with the AI Act."[^4] Second, the Code confers no presumption of conformity on those who do sign, so the gap between signing and not signing is narrower than the coverage implies — it is a difference in evidentiary posture and expected volume of information requests.[^4,6] Third, Article 50(2) binds xAI regardless. The obligation attaches to output placed on the Union market, not to whether a company joined a voluntary code, and Article 99(4) exposure follows the same logic.[^7,8]

The one place absence does bite is supervision. The Commission says Article 50 "will mainly be enforced by national competent market surveillance authorities," with the AI Office holding a limited role confined to systems where the same provider supplies both the general-purpose model and the system, or where the system sits inside a DSA-designated very large online platform.[^3] Grok in the X app satisfies both conditions at once. So the provider least visible in the voluntary regime is among the most exposed in the mandatory one — the opposite of the story the "refusal" framing tells.

:::callout(kind=warn, label="Evidential care")
Absence from a rolling list published on 31 July 2026, capturing signatures received by the end of that month, is weak evidence of intent. The Code remains open for signature, and a signature filed after the cut-off for that initial list would look identical to a decision not to sign.[^2,4] Reporting absence as refusal converts a null result into a claim.
:::

## 09. Who enforces this, with what

An obligation is only as real as the capacity behind it, and the capacity is thin. The Commission's own list of national single points of contact under the AI Act names authorities for just 8 of 27 member states, three of those still pending final designation — and the page carries a last-update stamp of 26 September 2025, nearly eleven months stale.[^27]

:::iso
- {label: "Member states with a listed single point of contact", glyph: "■", count: 8}
- {label: "Member states in the EU", glyph: "■", count: 27}
:::

The AI Office, which holds the narrow but pointed competence over first-party GPAI systems, "employs more than 125 staff" and was recruiting a further 40 contractual agents with an application deadline of 8 September 2026 — more than a month after its enforcement powers commenced.[^28] Those powers, for both the AI Office and national authorities, only became exercisable on 2 August 2026.[^29] No AI Act enforcement action, published investigation or penalty against any provider has been recorded as of 11 August 2026.[^29] Germany's implementing law took effect four days before Article 50 applied, and its regulator's announcement framed the role as "Enabler und Ansprechpartner" — enabler and point of contact — without mentioning sanctions at all.[^47]

The natural base rate is GDPR. It became applicable on 25 May 2018; the CNIL's deliberation SAN-2019-001, imposing a €50 million fine, is dated 21 January 2019 — roughly eight months later.[^36] Two caveats on that comparison: the published Légifrance text anonymises the respondent, and ==the reasons CNIL was able to act that quickly, rather than through the one-stop-shop, are not established by the cited decision text.== On a realistic reading, the first meaningful Article 50 action is a 2027 event, and the 2 December 2026 grace-period expiry is the earliest date on which most providers are even formally in scope.

Why this matters: the compliance question for the next eighteen months is not whether a watermark survives paraphrasing. It is whether anyone with authority will ask to see one — and today, no authority has published a detector, a benchmark, or an enforcement priority for Article 50.

## 10. The asymmetric signal: what happens when this reaches schools and employers

The most likely harm from Article 50(2) is not that the watermark fails. It is that it works well enough to be believed.

Anthropic's own framing is careful in both directions. "A detected mark provides a signal that content was processed by Claude, but is not fully conclusive," because "Claude may not be the original author" — a person may have written the text and used Claude to proofread, translate or summarise it.[^1] And the negative carries no information either: "Lack of a detected mark doesn't mean the content wasn't AI-generated or processed," for five listed reasons including a pre-marking model, heavy editing, a short passage, stripped metadata, or an unsupported surface.[^1] A signal that is weakly positive and meaningless when negative is exactly the shape most likely to be misread as proof.

The empirical record on what happens next is unambiguous. Seven GPT detectors misclassified human-written TOEFL essays by non-native English speakers as AI-generated at an average false-positive rate of 61.3%, against a near-zero rate for US eighth-grade essays; all seven unanimously misflagged 19.8% of them.[^24] The authors "strongly caution against the use of GPT detectors in evaluative or educational settings."[^24] Turnitin, whose detector is the most widely deployed, disclosed a sentence-level false-positive rate of around 4% against the sub-1% document-level figure it marketed.[^26] Vanderbilt disabled the detector after computing that a 1% rate applied to the 75,000 papers it submitted in 2022 would have wrongly flagged around 750 students.[^25]

Watermarking does not solve this; it may sharpen it. A 2025 simulation found that a threshold falsely flagging 4% of fully human essays flagged 25.5% of essays where the student used only *permitted* AI grammar editing — precisely the proofreading case Anthropic names as non-authorship.[^45]

:::bars
- {label: "Human-written essays flagged at α = 0.05", value: "4%", pct: 4}
- {label: "Essays with permitted AI grammar editing flagged", value: "25.5%", pct: 26}
- {label: "TOEFL essays flagged by ≥1 of 7 detectors", value: "97.8%", pct: 98}
- {label: "TOEFL essays flagged by all 7 detectors", value: "19.8%", pct: 20}
:::

The legal gap is that Article 50 regulates the *making* of the signal and says nothing about its *use*. No paragraph constrains a university or employer acting on a detection.[^7] The obvious backstop — the AI Act's own high-risk regime for education and employment under Annex III — was deferred by the Digital Omnibus to 2 December 2027.[^30] So there is a window of roughly sixteen months in which marking is mandatory, detection is unstandardised, and the downstream high-risk regime has not yet arrived.

Two structural facts make the window worse. Detection is key-bound: current schemes "tightly couple detection with injection, requiring access to keys or provider-side scheme-specific detectors for verification," which forecloses independent verification.[^44] And the Code's answer — an interoperability solution by 2 February 2027 — offers routing options such as an "industry-standard access method (API)" or a "signpost" in the content rather than a universal detector, with a "shared, provider-agnostic detection solution operated by a consortium" merely one option among four.[^38] Interoperability here means finding the right vendor's detector, not having one anybody can run.

## 11. What would falsify this analysis

The honest summary is that this article's strongest claims are negative ones, and negative claims about a rolling list and an undisclosed algorithm are the most fragile kind.

**The signatory correction is time-stamped, not permanent.** The ~190 figure is the Commission's own count of signatures received by the end of July 2026, published on 31 July, on a list it updates continuously.[^2] If xAI signs next month, the "absence" finding expires — though "absence is not refusal" would then be *more* true, not less.

**"No Claude model is marked at launch" could be technically true and practically wrong.** Anthropic says retrofit of older models is in progress.[^1] If Opus 5 or Sonnet 5 output already carries a mark, the substance of the announcement holds and only its formal framing was misleading. Anthropic could settle this in one sentence and has not.

**The 400-token finding rests on absence of evidence.** Our own review of eleven outlets covering the announcement — including The Register and explainx.ai, the two most technically careful — found none attaching a token count to Claude; the coverage mirrors Anthropic's qualitative wording instead.[^13,48] That is a clean negative, but web coverage is not exhaustively searchable, and Anthropic's promised technical documentation could yet publish a number near 400 — which would make the figure premature rather than invented.

**The robustness critique may prove the wrong thing.** The steelman deserves stating. Watermarking is not designed to defeat motivated adversaries; it targets the non-adversarial majority.[^32] Its clearest payoff may be training-data hygiene: Shumailov et al. show recursive training on generated data degrades models and note it is "unclear how content generated by LLMs can be tracked at scale."[^34] Even Zhang et al., authors of the impossibility proof, carve out that "weak watermarks can still be useful for applications like preventing AI-generated content from being used for training."[^20] With detector-based estimates putting primarily AI-generated articles at roughly half of new web articles,[^42] a bulk-scale signal has value that per-document adjudication does not. Scott Aaronson's original argument still bites: most misuse requires concealing AI authorship, so watermarking "would simultaneously attack most misuses."[^33]

**Red-team result: 3/3 top claims unbroken.** An adversarial pass tasked with falsifying this article's three load-bearing claims — that roughly 190 organisations signed rather than six, that Anthropic states no token threshold while the Code's number is 200 and SynthID's 400 is a benchmark length, and that Claude Opus 5 launched 24 July 2026 before the marking cutoff — found no contradicting source for any of them across four independent Anthropic release channels and repeated adversarial searches. The nearest miss was an Anthropic post dated 7 August 2026 about Claude Fable 5, which turned out to concern a model generally available from 9 June 2026 — before the cutoff, not after.

**The counter-argument I find most serious** is that judging a first-generation transparency rule by its adversarial robustness is a category error. Standards enable audits, audits inform enforcement, enforcement creates incentives — and researchers who call the current state governance theatre still "argue for enforceable watermarking as a critical step toward meaningful AI governance."[^43] On that view the 200-token rule, the missing benchmarks and the absent detector are what a regime looks like in month one, not evidence it will stay that way. The 2 February 2027 interoperability deadline and the two task forces the Commission says signatories will be invited into from September 2026 are the ratchet's next teeth.[^38,2]

Against that: ratchets need someone pulling them. Eight of twenty-seven authorities, no published benchmark, no detector, and zero enforcement actions is not month one of a tightening regime — it is month one of an untested one.[^27,29] The measurable difference between those two futures will be visible by 2 December 2026, when the grace period ends and every provider serving the EU either has a mark on its output or does not.

:::references
- {id: 1, title: "How Claude marks AI-generated content", url: "https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content", source: "Anthropic Help Center", date: "2026-08-10"}
- {id: 2, title: "Strong backing for the Code of Practice on Transparency of AI-generated Content", url: "https://digital-strategy.ec.europa.eu/en/news/strong-backing-code-practice-transparency-ai-generated-content", source: "European Commission", date: "2026-07-31"}
- {id: 3, title: "Transparency obligations under Article 50 of the AI Act (FAQ)", url: "https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act", source: "European Commission", date: "2026-07-24"}
- {id: 4, title: "Signing the Code of Practice on Transparency of AI-generated Content (FAQ)", url: "https://digital-strategy.ec.europa.eu/en/faqs/signing-code-practice-transparency-ai-generated-content", source: "European Commission", date: "2026-07-29"}
- {id: 5, title: "Code of Practice on Transparency of AI-Generated Content (full text)", url: "https://alia.public.lu/wp-content/uploads/2026/06/European-Commission_Code-of-Practice-on-Transparency-of-AI-Generated-Content.pdf", source: "European Commission / ALIA mirror", date: "2026-06-10"}
- {id: 6, title: "New EU Code of Practice on Transparency of AI-generated Content: impact and options", url: "https://www.gleisslutz.com/en/know-how/new-eu-code-practice-transparency-ai-generated-content-impact-and-options", source: "Gleiss Lutz", date: "2026-07-21"}
- {id: 7, title: "AI Act Article 50 — Transparency obligations", url: "https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50", source: "EU AI Act Service Desk", date: "2024-06-13"}
- {id: 8, title: "AI Act Article 99 — Penalties", url: "https://artificialintelligenceact.eu/article/99/", source: "EU Artificial Intelligence Act", date: "2024-07-12"}
- {id: 9, title: "AI Act Article 113 — Entry into force and application", url: "https://artificialintelligenceact.eu/article/113/", source: "EU Artificial Intelligence Act", date: "2024-06-13"}
- {id: 10, title: "AI Act Recital 133", url: "https://artificialintelligenceact.eu/recital/133/", source: "EU Artificial Intelligence Act", date: "2024-06-13"}
- {id: 11, title: "Claude Opus 5", url: "https://www.anthropic.com/news/claude-opus-5", source: "Anthropic", date: "2026-07-24"}
- {id: 12, title: "Transparency Hub", url: "https://www.anthropic.com/transparency", source: "Anthropic", date: "2026-07-23"}
- {id: 13, title: "Anthropic pledges to embed watermarks to help discern AI slop", url: "https://www.theregister.com/ai-and-ml/2026/08/11/anthropic-pledges-to-embed-watermarks-to-help-discern-ai-slop-in-sop-to-eu/5285792", source: "The Register", date: "2026-08-11"}
- {id: 14, title: "A Watermark for Large Language Models", url: "https://arxiv.org/abs/2301.10226", source: "Kirchenbauer et al., arXiv", date: "2023-01-24"}
- {id: 15, title: "On the Reliability of Watermarks for Large Language Models", url: "https://arxiv.org/abs/2306.04634", source: "Kirchenbauer et al., arXiv", date: "2023-06-07"}
- {id: 16, title: "Scalable watermarking for identifying large language model outputs", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC11499265/", source: "Dathathri et al., Nature", date: "2024-10-23"}
- {id: 17, title: "Re-analysis of tournament-sampling text watermark detectability", url: "https://arxiv.org/html/2603.03410v2", source: "arXiv", date: "2026-03-01"}
- {id: 18, title: "Paraphrasing evades detectors of AI-generated text (DIPPER)", url: "https://arxiv.org/abs/2303.13408", source: "Krishna et al., arXiv", date: "2023-03-23"}
- {id: 19, title: "Can AI-Generated Text be Reliably Detected?", url: "https://arxiv.org/abs/2303.11156", source: "Sadasivan et al., arXiv", date: "2023-03-17"}
- {id: 20, title: "Watermarks in the Sand: Impossibility of Strong Watermarking", url: "https://arxiv.org/abs/2311.04378", source: "Zhang et al., arXiv", date: "2023-11-07"}
- {id: 21, title: "Watermark Stealing in Large Language Models", url: "https://proceedings.mlr.press/v235/jovanovic24a.html", source: "Jovanović et al., PMLR (ICML)", date: "2024-02-29"}
- {id: 22, title: "Can Watermarks Survive Translation? Cross-lingual watermark removal", url: "https://arxiv.org/abs/2402.14007", source: "He et al., arXiv", date: "2024-02-21"}
- {id: 23, title: "Evaluating humanizer tooling against AI-text detectors and watermarks", url: "https://arxiv.org/abs/2501.03437", source: "arXiv", date: "2025-01-06"}
- {id: 24, title: "GPT detectors are biased against non-native English writers", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC10382961/", source: "Liang et al., Patterns", date: "2023-07-10"}
- {id: 25, title: "Guidance on AI detection and why we're disabling Turnitin's AI detector", url: "https://www.vanderbilt.edu/brightspace/2023/08/16/guidance-on-ai-detection-and-why-were-disabling-turnitins-ai-detector/", source: "Vanderbilt University", date: "2023-08-16"}
- {id: 26, title: "Understanding the false positive rate for sentences of our AI writing detection capability", url: "https://www.turnitin.co.uk/blog/understanding-the-false-positive-rate-for-sentences-of-our-ai-writing-detection-capability", source: "Turnitin", date: "2023-06-14"}
- {id: 27, title: "Market surveillance authorities under the AI Act", url: "https://digital-strategy.ec.europa.eu/en/policies/market-surveillance-authorities-under-ai-act", source: "European Commission", date: "2025-09-26"}
- {id: 28, title: "European AI Office", url: "https://digital-strategy.ec.europa.eu/en/policies/ai-office", source: "European Commission", date: "2026-08-10"}
- {id: 29, title: "Enforcement of the AI Act", url: "https://digital-strategy.ec.europa.eu/en/policies/enforcement-ai-act", source: "European Commission", date: "2026-08-07"}
- {id: 30, title: "AI Omnibus enters into force", url: "https://digital-strategy.ec.europa.eu/en/news/ai-omnibus-enters-force", source: "European Commission", date: "2026-07-27"}
- {id: 31, title: "The General-Purpose AI Code of Practice — contents and signatories", url: "https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai", source: "European Commission", date: "2026-07-31"}
- {id: 32, title: "Watermarking AI-generated text and video with SynthID", url: "https://deepmind.google/blog/watermarking-ai-generated-text-and-video-with-synthid/", source: "Google DeepMind", date: "2024-05-14"}
- {id: 33, title: "My AI Safety Lecture for UT Effective Altruism", url: "https://scottaaronson.blog/?p=6823", source: "Scott Aaronson", date: "2022-11-28"}
- {id: 34, title: "AI models collapse when trained on recursively generated data", url: "https://www.nature.com/articles/s41586-024-07566-y", source: "Shumailov et al., Nature", date: "2024-07-24"}
- {id: 35, title: "Anthropic Series H", url: "https://www.anthropic.com/news/series-h", source: "Anthropic", date: "2026-05-28"}
- {id: 36, title: "Délibération SAN-2019-001 — sanction of EUR 50 million against Google LLC", url: "https://www.legifrance.gouv.fr/cnil/id/CNILTEXT000038032552/", source: "CNIL / Légifrance", date: "2019-01-21"}
- {id: 37, title: "What the EU's new Code of Practice means for AI-generated content transparency", url: "https://www.dlapiper.com/en-us/insights/publications/2026/07/what-the-eus-new-code-of-practice-means", source: "DLA Piper", date: "2026-07-16"}
- {id: 38, title: "EU AI Act unpacked: the final Code of Practice on Transparency of AI-generated content", url: "https://www.freshfields.com/en/our-thinking/blogs/technology-quotient/eu-ai-act-unpacked-33-the-final-code-of-practice-on-transparency-of-ai-generate-102n4yx", source: "Freshfields", date: "2026-06-25"}
- {id: 39, title: "Transparency obligations for AI-generated content: the Code of Practice adequacy decision", url: "https://www.reedsmith.com/our-insights/blogs/viewpoints/102nbz0/transparency-obligations-for-ai-generated-content-the-code-of-practice-adequacy/", source: "Reed Smith", date: "2026-07-20"}
- {id: 40, title: "Durable Content Credentials", url: "https://opensource.contentauthenticity.org/docs/durable-cr/", source: "Content Authenticity Initiative", date: "2026-08-11"}
- {id: 41, title: "Missing the Mark: adoption of watermarking for generative AI systems", url: "https://arxiv.org/html/2503.18156v3", source: "Rijsbosch et al., arXiv", date: "2025-10-08"}
- {id: 42, title: "AI now writes as many online articles as humans do", url: "https://graphite.io/five-percent/research/ai-now-writes-as-many-online-articles-as-humans-do", source: "Graphite", date: "2026-05-01"}
- {id: 43, title: "Position: enforceable watermarking as a step toward meaningful AI governance", url: "https://arxiv.org/html/2505.23814v2", source: "Nemecek et al., arXiv", date: "2026-03-02"}
- {id: 44, title: "TTP-Detect: key-agnostic detection of watermarked text", url: "https://arxiv.org/abs/2603.14968", source: "arXiv (ACL Findings)", date: "2026-03-16"}
- {id: 45, title: "Watermark in the Classroom: A Conformal Framework for Adaptive AI Usage Detection", url: "https://arxiv.org/html/2507.23113v1", source: "Xie, Chen, Ren & Su, arXiv", date: "2025-07-30"}
- {id: 46, title: "Guidelines on transparency obligations for providers and deployers of AI systems", url: "https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems", source: "European Commission", date: "2026-07-20"}
- {id: 47, title: "Bundesnetzagentur wird Marktüberwachungsbehörde für KI", url: "https://www.bundesnetzagentur.de/1112336", source: "Bundesnetzagentur", date: "2026-07-29"}
- {id: 48, title: "Claude invisible watermarks — what they detect (and miss)", url: "https://explainx.ai/blog/anthropic-claude-invisible-watermarks-c2pa-august-2026", source: "explainx.ai", date: "2026-08-11"}
- {id: 49, title: "European AI Office releases Code of Practice on Transparency of AI-Generated Content", url: "https://iptc.org/news/eu-ai-transparency-code-of-practice-june-2026/", source: "IPTC", date: "2026-06-10"}
- {id: 50, title: "Digitalisation in Europe — 2026 edition", url: "https://ec.europa.eu/eurostat/web/interactive-publications/digitalisation-2026", source: "Eurostat", date: "2026-01-01"}
- {id: 51, title: "A conversation with Anu Bradford", url: "https://www.capgemini.com/ch-en/insights/research-library/a-conversation-with-anu-bradford/", source: "Capgemini Research Institute", date: "2026-03-04"}
- {id: 52, title: "New offices in Paris and Munich expand European presence", url: "https://www.anthropic.com/news/new-offices-in-paris-and-munich-expand-european-presence", source: "Anthropic", date: "2025-11-07"}
- {id: 53, title: "Meta refuses to sign EU's AI code of practice", url: "https://techcrunch.com/2025/07/18/meta-refuses-to-sign-eus-ai-code-of-practice/", source: "TechCrunch", date: "2025-07-18"}
- {id: 54, title: "Code of Practice on Transparency of AI-generated Content", url: "https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content", source: "European Commission", date: "2026-07-31"}
:::
