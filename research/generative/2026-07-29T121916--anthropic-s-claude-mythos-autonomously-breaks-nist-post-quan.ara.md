---
eyebrow: RESEARCH · AI & CRYPTOGRAPHY
title: Claude Mythos vs. HAWK — What Actually Broke, and What "Autonomous" Really Means
deck: Anthropic says its unreleased model cut a NIST post-quantum candidate's security in half and sped up an AES attack 800x. Its own fine print, and a contested trail of $100K, 60 hours, and a month of human verification, describes something narrower.
lede: |
  On July 28, 2026, Anthropic announced that Claude Mythos Preview had found a lattice flaw in HAWK — a NIST post-quantum signature candidate — and a technique that speeds up an attack on reduced-round AES-128 by up to 800 times. Both claims check out against Anthropic's own technical writeup. Both are also narrower, on every axis that matters for security practice, than the "AI breaks encryption" framing that spread on social media within a day.
stats:
  - {label: "HAWK-256 attack cost", value: "2^38 ops", note: "down from thought-2^64"}
  - {label: "AES speedup claimed", value: "200-800x", note: "on 7-of-10 rounds only"}
  - {label: "Cost per result", value: "~$100K", note: "API spend, excludes labor"}
  - {label: "AES verification time", value: "~1 month", note: "2 researchers, by hand"}
  - {label: "HAWK's NIST status", value: "Round 3", note: "candidate, not selected"}
---

## 01. The direct answer

Claude Mythos Preview — an unreleased, gated Anthropic model — did produce two real cryptanalytic results, published with technical detail Anthropic itself calls narrow in scope [^1]. Read past the headline and five things matter more than the number that trends on social media:

:::kv
- {term: "Did it \"break\" HAWK?", def: "No. It cut the cost of attacking a deliberately weak *challenge* parameter (HAWK-256, ~64-bit security, never submitted to NIST) from 2^64 to 2^38 operations — a real, practical key recovery on that toy target. The NIST-submitted parameters (HAWK-512, HAWK-1024) remain exponential and unbroken."}
- {term: "Is HAWK a \"finalist\"?", def: "No. NIST's own vocabulary has no \"finalist\" stage. HAWK is one of 9 Round 3 candidates in a still-open on-ramp expected to run roughly two more years before any standardization decision."}
- {term: "Did AES get sped up 800x?", def: "Yes, on 7-of-10 rounds, against a chosen-plaintext model needing 2^105 plaintexts — an attack Anthropic itself calls \"completely impractical\" and would cost \"hundreds of millions of dollars\" to run. Full, deployed AES-128 is untouched."}
- {term: "Was it \"autonomous\"?", def: "Contested. The model needed explicit human encouragement after refusing the AES problem as too hard, and two researchers spent \"several hundred hours\" over nearly a month verifying the result was even correct — dwarfing the model's own working time."}
- {term: "Has anyone independently checked it?", def: "Not yet, publicly, by a named disinterested cryptographer. The strongest outside reaction found is a process objection asking for machine-checkable proofs, not a confirmation or refutation of the math."}
:::

The rest of this piece works through each of those five answers with the primary sourcing behind it, then asks what would have to be true for the more dramatic framing to hold up.

## 02. The HAWK attack: a real number, a deliberately weak target

Anthropic's technical writeup states plainly what the model found: a "nontrivial automorphism" in HAWK's lattice structure, enabling a faster — though still exponential — enumeration attack against HAWK's private key [^1]. The headline figure is precise: HAWK-256's expected full key-recovery cost, previously estimated at 2^64 operations, was demonstrated at 2^38 [^1]. Independent technical commentary reports Mythos's team then recovered an actual signing-equivalent key end-to-end in a few hours on a single multi-core server [^9].

What that figure does *not* mean is that HAWK, the algorithm NIST is evaluating for real-world use, is broken. HAWK-256 is a "challenge" parameter set the HAWK team itself published specifically to invite cryptanalysis, with claimed security around 64 bits — explicitly "too low for submission to NIST" [^25]. The parameters HAWK's designers actually submitted for standardization are HAWK-512 (NIST security level I) and HAWK-1024 (level V) [^25]. Independent commentary reports the same automorphism technique cuts HAWK-512's estimated gate-count security from roughly 2^150 to at most 2^108, and HAWK-1024's from roughly 2^288 to at most 2^182 [^9] — both still astronomically infeasible, and neither figure independently confirmed against Anthropic's own technical paper as of this writing [^9]. ==The HAWK-512/1024 numbers should be read as provisional secondary reporting, not settled primary figures, until an independent source reproduces them.==

Two facts sharpen how surprised anyone should be. First, this was not cryptanalysis from a standing start: a 2025 paper by van Gent and Pulles analyzed exactly this style of automorphism attack against HAWK's *already-once-amended* hardness definition and concluded that no further exploitable automorphism was known at the time, i.e. "this work does not affect the security of HAWK" under the assumptions it examined [^4]. ==The precise scope of what the 2025 paper ruled in versus out is a technical nuance this piece has not independently resolved beyond what Anthropic and secondary commentary state; treat the "closed a known gap" framing below as directionally right, not word-for-word certain.== That paper's starting point was itself shaped by an earlier finding (Luo et al., ASIACRYPT 2024) that had broken part of HAWK's *original* hardness assumption, forcing the design team to amend its security definition before this cycle even began [^4]. Mythos's contribution, on the evidence available, was finding a specific automorphism instance within a family of attacks the 2025 theory paper had already mapped — not inventing the attack template from nothing [^4].

Second, Anthropic's own framing is unusually blunt about scope: "It is specific to HAWK and does not impact other NIST post-quantum signature candidates or lattice-based cryptography in general" [^1]. Independent commentary similarly concludes the finding does not make the deployment-target HAWK-512 parameter set attackable today [^9]. Whether that self-assessment is complete is exactly the open question — HAWK's Lattice Isomorphism Problem is mathematically distinct from ML-DSA (Dilithium)'s Module-LWE/Module-SIS foundation, which is the more consequential reason the two shouldn't be conflated (see Section 08), not merely Anthropic's say-so.

:::slope(left-label="Prior estimate", right-label="Mythos-demonstrated", unit=" bits")
| Item | Prior estimate | Mythos-demonstrated |
|------|------|------|
| HAWK-256 (challenge, ~64-bit) | 64 | 38 |
| *HAWK-512 (NIST Level I) | 150 | 108 |
| HAWK-1024 (NIST Level V) | 288 | 182 |
:::
:::note
HAWK-512/1024 rows are independent secondary reporting, not yet confirmed against Anthropic's primary technical paper [^9]. Values shown as log2(operations), i.e., effective security bits.
:::

**Why this matters:** a halved security margin against a *candidate* still years from standardization is a genuinely useful data point for NIST's evaluation — and a poor basis for the "post-quantum encryption is broken" reading that circulated within hours of the announcement.

## 03. The Möbius bridge: sizing an 800x speedup

The second result targets AES-128, not a post-quantum scheme — a "sanity check" cipher, in Anthropic's framing, chosen because its security is extremely well-studied [^1]. Mythos's "Möbius bridge" is a fingerprinting method that eliminates a guess step in an existing meet-in-the-middle attack, cutting the work involved by a factor of 256, partly offset by additional computational cost that further optimization then absorbed [^1]. The net effect, per Anthropic's own writeup: an existing attack on 7-of-10-round AES-128 — which already required 2^105 chosen plaintexts before this work — runs 200 to 800 times faster depending on how the runtime is measured [^1]. ==Some secondary aggregation of this result cites more precise before/after operation counts (roughly 2^99 down to a 2^89-2^91 range); this piece could not confirm those exact exponents directly against Anthropic's primary technical paper, so they are omitted here rather than restated as settled.==

Every number in that paragraph describes an attack on a *reduced-round variant* of a cipher already well outside real-world use in that form. Full AES-128, as deployed in TLS, disk encryption, and everything else, uses all 10 rounds; its best known attack remains the 2011 biclique attack at 2^126.1 operations against a 2^128 brute-force baseline — barely better than brute force, and explicitly not considered a practical threat [^8]. Anthropic states its own result plainly: it "does not break the full cipher," would need "hundreds of millions of dollars" to actually run given the 2^105 chosen-plaintext requirement, and has no bearing on deployed systems [^1].

Reduced-round AES cryptanalysis is also not a new research frontier Mythos opened. Academic meet-in-the-middle cryptanalysis of reduced-round AES is an established lineage running back to 2008, and had already pushed 7-round AES-128 attacks below 2^100 combined data/time/memory complexity more than a decade before this result [^2]. One Hacker News commenter, citing established block-cipher cryptanalyst Orr Dunkelman, put the lineage point sharply: improving an already-thin sliver of a well-trodden attack is "like saying you knocked out Mike Tyson's brother's cousin's uncle's sister's nephew" [^7].

:::compare
- {role: "PRIOR BEST (7-round, combined complexity)", name: "Pre-2026 academic lineage", value: "below 2^100"}
- {role: "MYTHOS RESULT (7-round)", name: "Möbius bridge speedup", value: "200-800x faster"}
- {role: "FULL CIPHER (10-round)", name: "Best known attack, deployed AES-128", value: "2^126.1"}
:::

**Counterpoint:** an 800x constant-factor improvement on a mature attack lineage is a legitimate, citable cryptanalytic contribution in its own right — academic cryptography regularly publishes and rewards exactly this kind of incremental gain. The complaint is not that the result is fake; it's that "sped up an AES attack 800x" reads, to a lay audience, as a claim about deployed AES security that the underlying math doesn't support.

## 04. How autonomous was "autonomous"?

Anthropic's public framing leans on autonomy: the model worked "mostly autonomously and mostly without human intervention," with human input "limited to project management" [^1]. The disclosed numbers tell a more mixed story. The HAWK result took about 60 human-researcher hours total — finding, developing, and verifying the attack — performed by one researcher with a theoretical-computer-science background who was, by Anthropic's own account, not a lattice-cryptography expert [^1]. The AES result was developed over roughly a week of concentrated model working time, producing on the order of a billion output tokens across the project [^1] — but validating that the result was even correct took two researchers "several hundred hours" and very nearly a month [^1].

The most-quoted detail from Anthropic's own transcripts captures the tension directly: Claude initially expressed reluctance about the AES task, stating "AES-128 r5/r6 is just genuinely hard" — a position Anthropic itself calls "well-founded" — and proceeded only after a researcher's explicit prompt not to abandon the problem [^1]. Simon Willison's independent commentary on the release focused specifically on these shared prompts, calling them "the best part" of the disclosure precisely because they show how much steering was required to keep the model persistent [^10].

None of this makes the underlying cryptanalysis illegitimate — human-in-the-loop AI research is still AI-assisted research, and $100,000 of compute plus 60 hours of expert time to find a real, previously-unknown lattice weakness is a meaningfully different cost structure than a team of specialist cryptographers spending months on the same problem unaided. But "autonomous," read literally, overstates the case: roughly 5-15x more human-hours went into *verifying* the AES result than the model is credited with spending *finding* it.

:::compare
- {role: "MODEL WORKING TIME", name: "AES attack development", value: "~1 week"}
- {role: "HUMAN VERIFICATION", name: "AES correctness check (2 researchers)", value: "~1 month"}
- {role: "SUBJECT", name: "HAWK: model + human time combined", value: "~60 hrs"}
:::

**Why this matters:** how a capability claim gets labeled shapes how much scrutiny it receives. "AI autonomously broke encryption" invites less scrutiny than "AI found a real lattice weakness after 60 expert-hours, and a real speedup after a month of human verification" — even though the second description is the one Anthropic's own numbers support.

## 05. Standing on giants: the lineage nobody's headline mentioned

Both results sit on top of published, citable, years-old academic work — a pattern worth stating plainly because none of the viral coverage of this story led with it. HAWK's automorphism story runs at least three steps deep: the original Lattice Isomorphism Problem construction (Ducas, Postlethwaite, Pulles, and van Woerden, 2022) [^3]; an ASIACRYPT 2024 finding that broke part of HAWK's original hardness assumption and forced a design amendment [^4]; and the May 2025 van Gent-Pulles paper that mapped out this style of automorphism attack in detail [^4]. The AES lineage is older still: academic meet-in-the-middle cryptanalysis of reduced-round AES had already reached sub-2^100 complexity on 7 rounds through more than a decade of published refinement before this result extended it further [^2].

:::timeline
- {date: "2008", headline: "Demirci-Selçuk meet-in-the-middle attack", body: "The foundational technique for reduced-round AES cryptanalysis, introduced at FSE 2008."}
- {date: "2010", headline: "Dunkelman-Keller-Shamir refinement", body: "ASIACRYPT 2010 substantially improves the meet-in-the-middle approach on reduced-round AES."}
- {date: "2013", headline: "Derbez-Fouque-Jean", body: "EUROCRYPT 2013 pushes 7-round AES-128 attacks below 2^100 complexity — the direct baseline Mythos improved on."}
- {date: "2024", headline: "Luo et al. break HAWK's original assumption", body: "ASIACRYPT 2024 forces the HAWK team to amend its omSVP hardness definition."}
- {date: "2025-05", headline: "van Gent-Pulles theory paper", body: "Proves an automorphism would enable an attack, but finds none exists in the amended scheme -- \"does not affect the security of HAWK.\""}
- {date: "2026-07-28", headline: "Anthropic publishes the Mythos results", body: "Claude Mythos Preview finds the specific automorphism, and a Möbius-bridge speedup on the AES lineage."}
:::

This is not a criticism unique to Anthropic — crediting the full citation trail behind a "novel" result is a chronic problem in how AI capability claims get reported generally, not something specific to this lab. But it does mean the correct frame is "a well-resourced AI system closed a gap that specialists had already mapped," rather than "an AI discovered new mathematics unaided," and the distinction matters for calibrating how much of a capability jump this really represents.

**Counterpoint:** closing a gap specialists have mapped but not yet closed is still a nontrivial result — plenty of respected cryptography papers do exactly that, and "found the specific automorphism the theory said would matter" is a real, falsifiable, checkable technical contribution rather than an empty one.

## 06. The verification gap

As of this writing, no named, professionally disinterested cryptographer has published an independent reproduction or confirmation of Anthropic's specific HAWK or AES figures [^9] [^11] [^12] [^13]. Press coverage — the-decoder, CyberScoop, TheHackerNews, Simon Willison's blog — relays Anthropic's own numbers with light editorial framing rather than independent technical verification; CyberScoop's one outside quote, from a cryptography-vendor executive, is affirming rather than critical, and comes from a company that sells crypto-inventory tooling with a commercial interest in PQC anxiety [^12]. Anthropic states it "consulted with academics to confirm the validity of our findings" and coordinated disclosure with HAWK's own design team before publication [^1] — but no individual outside reviewer is named, and the university partners on the companion CryptanalysisBench benchmark (ETH Zurich, Tel Aviv University, University of Haifa) are credited with building a shared evaluation tool, not with validating these two specific results [^15].

The clearest piece of genuine outside scrutiny found is procedural rather than mathematical: cryptographer Markku-Juhani Saarinen reportedly argued on NIST's public pqc-forum that AI-assisted cryptanalysis claims of this kind should ship machine-checkable proofs or working demonstrations, not prose write-ups alone [^9] — an implicit statement that the current disclosure format doesn't yet meet that bar. Separately, two outlets give conflicting accounts of whether cryptographer Daniel Apon replied on the same forum confirming the HAWK result: one reports finding no replies on the thread, the other reports a confirming response [^11] [^9]. ==Whether Apon in fact confirmed the result is contested between sources and unresolved as of this writing.== HAWK's own design team is confirmed to have reviewed the finding privately before the coordinated disclosure [^1], but has issued no independent public statement characterizing its severity.

The Hacker News discussion of the release — which grew from 17 points to over 200 within a day, making it the platform's fastest-rising story that week [^14] — leaned skeptical rather than impressed on balance, with commenters citing cryptographic backgrounds converging on the same two points made in Sections 02-05: the practical impact is narrow, and "autonomous" oversells the process [^7] [^14].

**Why this matters:** a company's own technical writeup, however detailed and however hedged in its own caveats, is not the same evidentiary category as independent reproduction. Both things can be true at once: the numbers may well hold up, and it is still accurate to say they have not yet been checked by anyone without a stake in the result.

## 07. CyberGym and the benchmark arms race

The same week, a different, unrelated comparison circulated: Microsoft's new MAI-Cyber-1-Flash model, paired with its MDASH multi-agent harness (per Microsoft's own account, MAI-Cyber-1-Flash working alongside GPT-5.4), reportedly scored about 96% on the "CyberGym" benchmark — cited elsewhere as roughly 12 percentage points above an Anthropic Mythos figure on the same test [^16]. ==Some outlets attribute that comparison figure to "Mythos Preview" and others to a later "Mythos 5" checkpoint; this piece could not fully resolve which specific model version the ~84% comparison point refers to.== Some commentary conflated this benchmark story with the HAWK/AES cryptanalysis story, as though the two events measured the same thing. They don't. CyberGym is an independent UC Berkeley benchmark built around proof-of-concept reproduction for 1,507 real, previously disclosed vulnerabilities across 188 open-source projects [^17] — a closed, scored, repeatable task set, mechanically distinct from the open-ended structural cryptanalysis behind HAWK and AES, which produced one unscored result apiece after a month of human verification [^1] [^17].

Every CyberGym figure now circulating — Microsoft's 96% [^16], Sakana's Fugu-Cyber at 86.9% [^18], OpenAI's GPT-5.5-Cyber near 85.6% [^26], Google's Gemini 3.5 Flash Cyber at 83.2% [^27], and the Anthropic Mythos figure near 83-84% cited by Microsoft [^16] — is self-reported by the vendor that produced it, on that vendor's own chosen configuration. CyberGym's own creators reported top model combinations clearing only around 20% at the benchmark's ICLR 2026 baseline [^17]; the jump to 83-96% within roughly a year, with no published methodology change explaining it, is worth treating as marketing until an independent party re-runs the comparison under one fixed harness.

:::rank-list
- {label: "Microsoft MAI-Cyber-1-Flash + MDASH", value: "96%", pct: 100}
- {label: "Sakana Fugu-Cyber", value: "86.9%", pct: 90}
- {label: "OpenAI GPT-5.5-Cyber", value: "85.6%", pct: 89}
- {label: "Anthropic Mythos", value: "83.8%", pct: 87, highlight: true}
- {label: "Google Gemini 3.5 Flash Cyber", value: "83.2%", pct: 87}
:::
:::source
Self-reported vendor figures on the CyberGym benchmark, July 2026; not independently re-verified under a common harness [^16] [^17] [^18] [^26] [^27].
:::

Cybench, the CTF-style predecessor benchmark, illustrates the underlying dynamic: frontier models have driven its baseline from 17.5% at launch to roughly 93%, with Anthropic's own Mythos Preview topping its leaderboard at a maxed 1.000 score [^18] — a pattern that reads at least as much like benchmark saturation as like unbounded growing capability, since a fully-saturated test stops differentiating models by ability and starts differentiating them by who ran it last.

**Counterpoint:** the strongest non-vendor evidence in this space — the UK AI Security Institute's own evaluation of GPT-5.5, which found autonomous end-to-end success on a 32-step attack range in one or two attempts out of ten against a weakly defended target [^19] — does support a real, if narrow, capability trend independent of any single vendor's benchmark number. That finding, notably, required its own public correction after AISI found a scoring-pipeline error in the figure OpenAI had originally cited [^19] — a small case study in how even "independent verification" of these claims is itself contested terrain.

## 08. HAWK's actual place in the queue

NIST's post-quantum program has two, easily conflated, tracks. The first — Kyber (now ML-KEM, FIPS 203), Dilithium (now ML-DSA, FIPS 204), and SLH-DSA (FIPS 205) — was finalized in August 2024 [^20] and is the target of the US federal government's actual migration mandate: Executive Order 14412 and subsequent OMB guidance, issued in the second half of June 2026, set 2030 and 2031 deadlines for high-value and high-impact federal systems, with 2035 as a backstop [^20]. HAWK belongs to the second, separate track — the "Additional Digital Signatures" on-ramp, created specifically because NIST wanted a backup signature scheme built on different mathematical foundations than ML-DSA's, in case lattice problems generally turn out weaker than assumed [^5]. HAWK advanced to Round 3 of that on-ramp — as the sole lattice-based candidate among nine, alongside FAEST, MAYO, MQOM, QR-UOV, SDitH, SNOVA, SQIsign, and UOV — on May 14, 2026, with the round expected to run roughly two more years before any standardization decision [^5].

That timeline gap matters more than the cryptanalysis itself for near-term policy: a finding against a candidate still years from selection cannot, by construction, change a federal migration mandate that was targeting a different, already-finalized set of algorithms regardless of what happens to HAWK. The one substantive industry reaction found treats the news as validation of NIST's evaluation process working as intended, and as a reminder to maintain visibility into cryptographic inventory — not as a trigger to alter any deployed system [^12] [^20].

Whether the underlying mathematics generalizes is the more consequential open question, and here the record is more honest than the tweet-length version suggests. HAWK's security rests on the Lattice Isomorphism Problem; ML-DSA's rests on Module-LWE and Module-SIS — different problems, not different parameter choices of the same one [^3] [^20]. Both Anthropic and independent commentary state the automorphism technique is specific to HAWK's particular lattice structure and does not extend to ML-DSA or to lattice-based cryptography generally [^1] [^20]. That is a real, checkable mathematical distinction rather than a rhetorical dodge — but it is also, again, an assertion resting on the same not-yet-independently-verified foundation discussed in Section 06.

**Why this matters:** the policy-relevant question is not "did an AI weaken a cryptographic algorithm" but "did an AI weaken *an algorithm anyone has to rely on*" — and on the evidence available, the honest answer is no, not yet, and not on the current standardization timeline even if the parameter-level numbers eventually firm up.

## 09. Pattern-matching against AlphaTensor and AlphaEvolve

This is not the first time a frontier lab has announced an AI system making a "novel" mathematical or algorithmic discovery, and the prior cases are informative about how much initial framing tends to survive scrutiny. DeepMind's 2022 AlphaTensor, which found new matrix-multiplication algorithms, proved difficult for independent researchers to reproduce: a 2024 reproduction paper reported it was "really hard to reproduce due to the massive tricks and lack of source code," though the results were eventually confirmed rather than overturned [^21]. AlphaEvolve, DeepMind's more recent discovery system, received a partial walk-back from a DeepMind-affiliated November 2025 follow-up paper, which conceded the system "was not able to match or exceed previous results in all cases" and that traditional computational or theoretical methods could likely have matched some of its individual improvements [^22] — a case where the initially reported scope of novelty proved narrower on closer, later inspection.

Independent capability-tracking work offers a partial counterweight to pure skepticism. METR's cross-lab "time horizon" metric — the length of tasks frontier models can complete autonomously with 50% reliability — has roughly doubled every seven months over six years, a trend independent of any single lab's self-reporting [^23]. But even METR's own framing carries a caveat directly relevant here: comparisons between minimally-scaffolded older models and heavily-engineered newer agent harnesses can inflate the apparent capability gain, since some of the improvement reflects better tooling around the model rather than a smarter model underneath it [^23] — precisely the ambiguity Section 04 raised about how much of the HAWK/AES result reflects Mythos's own reasoning versus the surrounding human-plus-scaffolding process.

Anthropic's own recent track record on capability-related transparency adds a further, if indirect, data point: in June 2026, the company reversed an undisclosed policy that had quietly limited a prior model's capabilities, after public researcher backlash accused it of undisclosed "sabotage" [^24]. That episode concerns model-behavior disclosure rather than a scientific-discovery claim, but it is a recent, concrete instance of an Anthropic public representation proving less complete on first telling than a fuller account later required — relevant context, not a direct precedent, for how much any single Anthropic capability announcement should be taken at face value before independent scrutiny catches up.

**Counterpoint:** none of AlphaTensor's, AlphaEvolve's, or (on current evidence) Mythos's core results were shown to be fabricated — the pattern across all three is "real but initially overstated in scope or autonomy," not "false." That distinction matters: the right skeptical prior here is calibration, not dismissal.

## 10. What would change this picture

Every argument in this piece for a narrower reading of the Mythos/HAWK story rests on evidence available within roughly 48 hours of Anthropic's announcement — the honest caveat for a story this fresh. Several concrete developments would meaningfully shift the assessment:

- **A named, independent cryptographer publicly reproducing or directly disputing the specific 2^38 (HAWK-256) or 200-800x (AES) figures**, rather than the current mix of Anthropic's own paper and unsigned or contested secondary commentary [^9] [^11].
- **NIST's pqc-forum or an official NIST statement** addressing HAWK's status ahead of the Round 3 parameter-tweak deadline (August 14, 2026) — silence so far is not evidence either way, but a substantive response would be [^5].
- **Confirmation or correction of the disputed HAWK-512/1024 figures** (2^108 and 2^182) against Anthropic's primary technical paper, which independent commentary has flagged as not verified line-for-line [^9].
- **A second, unrelated frontier lab publishing a comparably rigorous cryptanalytic result** using a similar AI-assisted process, which would move the "is this a genuine capability trend or a one-off" question (Section 09) from speculative to empirical.
- **Any evidence the automorphism technique generalizes beyond HAWK's specific Lattice Isomorphism Problem construction** to Module-LWE/Module-SIS schemes like the already-standardized ML-DSA — which, on all evidence gathered here, has not been claimed or shown by anyone, including Anthropic itself [^1] [^20].

Until one or more of those happens, the calibrated summary is the one this piece opened with: real results, honestly hedged by their own author, overstated by everyone who repeated only the headline.

:::references
- {id: 1, title: "Discovering Cryptographic Weaknesses with Claude", url: "https://www.anthropic.com/research/discovering-cryptographic-weaknesses", source: "Anthropic", date: "2026-07-28"}
- {id: 2, title: "Improved Meet-in-the-Middle Attacks on Reduced-Round AES", url: "https://eprint.iacr.org/2012/477", source: "IACR ePrint", date: "2012-08-27"}
- {id: 3, title: "HAWK: Module LIP Makes Lattice Signatures Fast", url: "https://eprint.iacr.org/2022/1155", source: "IACR ePrint", date: "2022-09-01"}
- {id: 4, title: "On the Automorphisms of HAWK's Lattice", url: "https://eprint.iacr.org/2025/928", source: "IACR ePrint", date: "2025-05-23"}
- {id: 5, title: "Nine Candidates Advance to the Third Round of Additional Digital Signatures", url: "https://www.nist.gov/news-events/news/2026/05/nine-candidates-advance-third-round-additional-digital-signatures-pqc", source: "NIST", date: "2026-05-14"}
- {id: 6, title: "Improved Key Recovery Attacks on Reduced-Round AES", url: "https://eprint.iacr.org/2013/573", source: "IACR ePrint / EUROCRYPT 2013", date: "2013-01-01"}
- {id: 7, title: "Discovering Cryptographic Weaknesses with Claude (comments)", url: "https://news.ycombinator.com/item?id=49087091", source: "Hacker News", date: "2026-07-28"}
- {id: 8, title: "Biclique Cryptanalysis of the Full AES", url: "https://eprint.iacr.org/2011/449", source: "IACR ePrint / ASIACRYPT 2011", date: "2011-01-01"}
- {id: 9, title: "AI Cryptanalysis: HAWK and AES", url: "https://postquantum.com/security-pqc/ai-cryptanalysis-hawk-aes/", source: "postquantum.com", date: "2026-07-29"}
- {id: 10, title: "Discovering cryptographic weaknesses with Claude", url: "https://simonwillison.net/2026/Jul/28/discovering-cryptographic-weaknesses-with-claude/", source: "Simon Willison", date: "2026-07-28"}
- {id: 11, title: "Claude AI Just Cracked a Post-Quantum Cipher", url: "https://thehackernews.com/2026/07/claude-ai-just-cracked-post-quantum.html", source: "The Hacker News", date: "2026-07-28"}
- {id: 12, title: "Anthropic says Claude Mythos found flaws in cryptographic algorithms", url: "https://cyberscoop.com/anthropic-claude-mythos-encryption-flaws-hawk-aes-pqc/", source: "CyberScoop", date: "2026-07-28"}
- {id: 13, title: "Anthropic says its Mythos model found vulnerabilities in cryptographic algorithms that secure the internet", url: "https://the-decoder.com/anthropic-says-its-mythos-model-found-vulnerabilities-in-cryptographic-algorithms-that-secure-the-internet/", source: "The Decoder", date: "2026-07-28"}
- {id: 14, title: "Discovering Cryptographic Weaknesses with Claude — HN front page tracking", url: "https://news.ycombinator.com/item?id=49087091", source: "Hacker News", date: "2026-07-29"}
- {id: 15, title: "CryptanalysisBench: Can LLMs Do Cryptanalysis?", url: "https://arxiv.org/html/2607.18538v1", source: "arXiv", date: "2026-07-28"}
- {id: 16, title: "Introducing MAI-Cyber-1-Flash Inside MDASH", url: "https://microsoft.ai/news/introducing-mai-cyber-1-flash-inside-mdash/", source: "Microsoft AI", date: "2026-07-27"}
- {id: 17, title: "CyberGym: Evaluating AI Agents' Real-World Cybersecurity Capabilities at Scale", url: "https://arxiv.org/abs/2506.02548", source: "arXiv", date: "2026-03-01"}
- {id: 18, title: "Fugu-Cyber Release", url: "https://sakana.ai/fugu-cyber-release/", source: "Sakana AI", date: "2026-07-25"}
- {id: 19, title: "Our evaluation of OpenAI's GPT-5.5 cyber capabilities", url: "https://www.aisi.gov.uk/blog/our-evaluation-of-openais-gpt-5-5-cyber-capabilities", source: "UK AI Security Institute", date: "2026-04-30"}
- {id: 20, title: "US Post-Quantum Cryptography Regulatory Framework 2026", url: "https://postquantum.com/security-pqc/us-pqc-regulatory-framework-2026/", source: "postquantum.com", date: "2026-06-24"}
- {id: 21, title: "Reproducing AlphaTensor's Discovered Matrix Multiplication Algorithms", url: "https://arxiv.org/abs/2405.20748", source: "arXiv", date: "2024-05-31"}
- {id: 22, title: "A Closer Look at AlphaEvolve's Discovered Improvements", url: "https://arxiv.org/pdf/2511.02864", source: "arXiv", date: "2025-11-01"}
- {id: 23, title: "Measuring AI Ability to Complete Long Tasks", url: "https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/", source: "METR", date: "2025-03-19"}
- {id: 24, title: "Anthropic accused of quietly limiting Claude capabilities for researchers", url: "https://fortune.com/2026/06/10/anthropic-accu-claude-fable-5-limits-capabilities-ai-researchers-developers/", source: "Fortune", date: "2026-06-10"}
- {id: 25, title: "HAWK Signature Scheme Specification", url: "https://hawk-sign.info/hawk-spec.pdf", source: "HAWK design team", date: "2025-02-05"}
- {id: 26, title: "GPT-5.5 with trusted access for cyber", url: "https://openai.com/index/gpt-5-5-with-trusted-access-for-cyber/", source: "OpenAI", date: "2026-05-07"}
- {id: 27, title: "Introducing Gemini 3.5 Flash Cyber", url: "https://deepmind.google/blog/introducing-gemini-3-5-flash-cyber/", source: "Google DeepMind", date: "2026-07-21"}
:::
