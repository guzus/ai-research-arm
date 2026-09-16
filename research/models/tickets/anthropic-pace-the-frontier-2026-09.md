---
slug: anthropic-pace-the-frontier-2026-09
title: "Amodei's \"We Must Pace the Frontier\" essay and the industry/government response"
company: Anthropic / OpenAI / Microsoft / Google / Cohere / US Government / PRC
model: null
status: confirmed
status_note: |
  Dario Amodei published an essay, **"We Must Pace the Frontier"**, arguing that
  frontier development should be deliberately slowed to let alignment and
  monitoring keep up. Over 2026-09-13..09-14 it became the dominant story in the
  cycle, and — unusually for a position piece — it produced on-record responses
  from most of the people who would have to act on it.

  **Amodei's own bounding of the claim (primary, broadcast).** On CBS Sunday
  Morning, asked "Does that then mean that Anthropic is going to stop releasing
  more advanced models?", he answered: "It doesn't mean that. What it means is
  that we need to make sure that every generation of models that we release is
  properly tested." On governance he went further than the essay: "I am
  concerned that one single government could abuse this technology just as
  easily as a single company could. But I think a combination of democratically
  elected governments — I don't know about handing over, but some kind of
  oversight, some kind of joint governance. Again, that would be the work of
  years."

  **OpenAI agreed, and disclosed a process change doing it (primary,
  @sama 2026-09-14 04:05 UTC).** Altman: "We welcome a federal framework that
  sets consistent safety requirements for frontier AI. But we do not believe we
  need to wait for an anti-trust exemption or legislation to begin the work."
  The roadmap-relevant disclosure is concrete: Responsible Scaling Policies and
  Preparedness Frameworks "focused primarily on the deployment of completed
  models, not what happens during their development process", and "at OpenAI we
  now formulate explicit safety cases in advance of frontier reinforcement
  learning runs we expect to significantly increase capability." He defines the
  term the same way Amodei does — "When we talk about 'pacing', we do not mean
  'stopping' … But it should be slower than it otherwise could be" — and names
  the two failure modes as loss of control and concentration of power, including
  "one lab ending up with too much power."

  **Microsoft and Google DeepMind aligned.** Satya Nadella: "Superintelligence
  that doesn't benefit humanity and is not under human control doesn't worth
  pursuing" and "We welcome the research, focus, and deliberate pacing needed to
  get alignment right as the design goal"; separately, "I think of this like
  testing. We all do deliberate pacing when it comes to pre-release R&D and
  testing." @demishassabis said he is aligned with Amodei's direction
  (both relayed by @testingcatalog).

  **The dissents are the load-bearing part.** President Trump, asked whether the
  industry should slow down: "I think you have a lot of negative forces that are
  bringing it up that shouldn't be bringing it up, and they're bringing up
  things that won't happen. But whoever wins with AI wins." White House AI czar
  David Sacks replied to Amodei directly ("go ahead…" — only truncated retweet
  text was captured, so his full position is NOT recorded here). **Cohere**
  published the industry counter-position: "Artificial intelligence needs
  evidenced standards, not a cartel" (@aidangomez). **China rejected it
  outright** — Global Times (via Reuters) accused the US of trying "to curb
  China's AI development through technological barriers and regulatory
  monopolies", calling the proposal a "silent AI Cold War" that is "hypocritical
  and short-sighted"; the Foreign Ministry (via AP) said "Fearmongering,
  confrontation and vicious competition will only disrupt the process of global
  AI governance which serves no one's interest."

  **It moved markets.** Asian AI-linked equities sold off on 2026-09-14:
  SoftBank down as much as 13.2%, Kioxia 9.8%, SK Hynix 5.3%, Samsung
  Electronics 3.7%, TSMC 1.2%; European semis followed with ASML -6.2% and ASM
  International -10%+. Recorded as market reaction, not as evidence about the
  policy.

  **Unresolved and deliberately not asserted here:** whether any of this changes
  a shipping schedule. No lab announced a delayed model. The one concrete
  mechanism disclosed is OpenAI's pre-RL safety cases. Two adjacent artifacts
  are tracked separately: the industry standards body reportedly under
  construction ([[industry-frontier-safety-standards-body-2026-09]]) and the
  conflict-of-interest question raised by Amodei making this argument mid-IPO
  ([[anthropic-ipo-2026-06]]).

  **2026-09-16 — Meta answers, and it answers "each lab, alone."** The two
  holdouts responded, both first-party. **Mark Zuckerberg** (@finkd, RT'd by
  @AIatMeta): "Every lab has the responsibility and incentive to move at the
  pace required to train its models safely, **and the ability to take its own
  actions to ensure that happens**… trust and alignment are quickly becoming
  the most important capabilities that will differentiate agents and models."
  **Alexandr Wang** (Meta Superintelligence Labs) set out a three-point
  position: businesses will only use aligned agents so labs face market
  discipline; every lab should have a governance framework including
  **external evaluators and independent oversight of launch safety criteria**;
  and labs operate inside democratic institutions that impose liability. That
  is agreement on *outcome* with rejection of *coordination* — the unilateral
  answer to the coordinated one.

  **The first cited instance of an actually-held release, and it is
  retrospective.** Wang, in-window: "Meta delayed shipping Muse for several
  months to focus on safety and security. **We didn't call for everyone else
  to do this before we would.**" This ticket's stated falsifier is "some lab
  announces a model it held back, and says why." Meta claims one — months, for
  safety — and it corroborates from the company side The Information's earlier
  reporting of Hatch's unauthorized-action problems
  ([[meta-hatch-muse-spark-2026-06]]). It is a claim about the past made in a
  debate about the future, so it is logged, not treated as proof the norm
  works.

  **Nadella took it to a non-industry venue**, appearing on the All-In Summit
  under the framing "The AI Doomer Slowdown / Common Sense AI Guardrails /
  What 'Slowdown' Means for New AI Products."

  **Political capture, in both directions, inside 48 hours.** **Barack Obama**
  endorsed it: "I was encouraged this week to see the leaders of the frontier
  labs agree on the need for them to slow down the pace of AI development…
  a good and necessary first step," while explicitly refusing both the
  accelerationist and doomer labels. Against that, @rynorhn named the failure
  mode precisely: "the second AI safety becomes attached to politicians and
  political tribes, half the country is going to oppose it simply because the
  other half supports it." With Trump already on the opposite side, this is
  the partisan split forming in real time.

  **China escalated from rejection to attribution of motive.** A China Daily
  editorial named **Altman, Musk and Amodei** and argued the sudden alignment
  "looks less like a new concern for humanity and more like a bid to protect
  profits and slow Chinese competitors." Separately, People's Daily pushed
  back on the NSA/CISA/FBI advisory accusing Chinese firms of
  "industrial-scale" distillation — and, as @kyleichan (a credible China
  analyst) observes, **Beijing never denies the distillation; it argues it is
  standard industry practice**. That is a substantive concession worth more
  than the editorial.

  **A commercial cost is now being attributed to pacing.** Ramp card data
  relayed in-window puts **OpenAI at ~13% of enterprise AI spend against
  Anthropic's ~8%**, with the relays explicitly attributing part of the gap to
  "Anthropic's decision to slow its frontier development." Recorded as
  a third-party attribution, not as a measured causal effect — enterprise
  share moved for at least one other obvious reason in this window, the GPT-6
  Astra launch ([[openai-gpt-6]]).

  **Backlash intensified and turned financial.** @kevinnbass published an
  "audit of Anthropic's finances" calling for a **Congressional
  investigation**, arguing METR is financially dependent on Anthropic equity
  and therefore compromised as the "third-party evaluator" Amodei proposes.
  Unverified single-source advocacy, logged because the conflict-of-interest
  attack has now moved from timing (the IPO) to the evaluation
  infrastructure itself — which is the same institution Wang's point 2 relies
  on.

  **Still unchanged: no lab has announced a forward-looking delayed release.**
  Meta's is retrospective. The falsifier stands.
expected: "Open-ended. Watch for: an actual paced/delayed release at any lab; the industry standards body formalizing; whether Senate negotiators act on the reported duty-of-care and block-unsafe-release authority; and whether OpenAI's pre-RL safety cases get published in any form."
labels:
  - policy
  - safety
  - governance
  - frontier-model
  - regulation
verification: confirmed
sources:
  - https://x.com/sama/status/2099348812305473766
  - https://x.com/sama/status/2099352016988614852
  - https://x.com/AndrewCurran_/status/2099211348865658940
  - https://x.com/AndrewCurran_/status/2099173166828720526
  - https://x.com/cohere/status/2099284354731999680
  - "@rohanpaul_ai"
  - "@testingcatalog"
  - "@kimmonismus"
  - "@mark_k"
  - https://x.com/finkd/status/2099997096896274533
  - https://x.com/alexandr_wang/status/2100011173278290347
  - https://x.com/BarackObama/status/2099642023922036982
  - "@theallinpod"
  - "@kyleichan"
  - "@v_shakthi"
  - "@rynorhn"
  - "@kevinnbass"
created_at: 2026-09-14
updated_at: 2026-09-16
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-14
    change: "Created — CONFIRMED. Dario Amodei published 'We Must Pace the Frontier', arguing frontier development should be deliberately slowed so alignment and monitoring can keep up, and over 2026-09-13..09-14 it drew on-record responses from most parties who would have to act on it. Amodei bounded the claim himself on CBS Sunday Morning: asked whether Anthropic would stop releasing more advanced models, 'It doesn't mean that. What it means is that we need to make sure that every generation of models that we release is properly tested'; on governance he floated 'some kind of oversight, some kind of joint governance' by 'a combination of democratically elected governments'. @sama (2026-09-14 04:05 UTC, ~11K likes) agreed and disclosed a process change: prior Responsible Scaling Policies and Preparedness Frameworks 'focused primarily on the deployment of completed models, not what happens during their development process', and 'at OpenAI we now formulate explicit safety cases in advance of frontier reinforcement learning runs we expect to significantly increase capability'; he also welcomed 'a federal framework that sets consistent safety requirements for frontier AI' and defined pacing as 'not stopping'. Satya Nadella and @demishassabis both aligned with pacing (via @testingcatalog). Dissent: President Trump rejected a slowdown ('whoever wins with AI wins'); White House AI czar David Sacks replied to Amodei directly, but only truncated RT text was captured so his position is NOT recorded; Cohere published 'AI needs evidenced standards, not a cartel' (@aidangomez); China rejected it via Global Times/Reuters ('silent AI Cold War', 'hypocritical and short-sighted') and the Foreign Ministry via AP ('Fearmongering, confrontation and vicious competition will only disrupt the process of global AI governance'). Market reaction recorded but not treated as evidence: SoftBank -13.2%, Kioxia -9.8%, SK Hynix -5.3%, Samsung -3.7%, TSMC -1.2%, ASML -6.2%, ASMI -10%+. Status confirmed / verification confirmed on multiple first-party accounts and verbatim broadcast quotes. Distinct from the July employee petition [[industry-pace-ai-development-petition-2026-07]], which this escalates from staff-signature to CEO-and-government level. No lab announced an actually delayed model — that is the falsifier this ticket exists to hold."
  - ts: 2026-09-16
    change: "META ANSWERS UNILATERALLY; the debate acquires a political axis, a commercial cost, and its first cited held release. Status stays confirmed. (1) META, both first-party. @finkd (RT'd by @AIatMeta 2026-09-15 23:01 UTC): 'Every lab has the responsibility and incentive to move at the pace required to train its models safely, and the ability to take its own actions to ensure that happens', adding that 'trust and alignment are quickly becoming the most important capabilities that will differentiate agents and models' — agreement on the outcome, rejection of coordination. @alexandr_wang (2026-09-15 23:57 UTC) set out three points: aligned agents win on the market so labs are already incentivized; every lab should have a governance framework across training and deployment including external evaluators and independent oversight of launch safety criteria; and labs operate inside democratic institutions that impose liability. (2) FIRST CITED HELD RELEASE, and it is retrospective: Wang, in-window — 'Meta delayed shipping Muse for several months to focus on safety and security. We didn't call for everyone else to do this before we would.' This ticket's falsifier is a lab announcing a model it held back and saying why; Meta claims one, months long, and it corroborates from the company side The Information's earlier reporting of Hatch's unauthorized-action problems ([[meta-hatch-muse-spark-2026-06]]). Logged as a past-tense claim inside a forward-looking debate, NOT as proof the norm works — no lab has announced a FORWARD-looking delay and the falsifier stands. (3) POLITICAL CAPTURE, both directions, inside 48h. @BarackObama (2026-09-14 23:30 UTC) endorsed it — 'I was encouraged this week to see the leaders of the frontier labs agree on the need for them to slow down the pace of AI development… a good and necessary first step' — while refusing both the accelerationist and doomer labels. @rynorhn named the resulting failure mode: 'the second AI safety becomes attached to politicians and political tribes, half the country is going to oppose it simply because the other half supports it.' With Trump already opposed (2026-09-14 entry), the partisan split is forming. Satya Nadella took the argument to a non-industry venue, appearing on the All-In Summit under the framing 'The AI Doomer Slowdown / Common Sense AI Guardrails' (@theallinpod 2026-09-15). (4) CHINA ESCALATED FROM REJECTION TO MOTIVE. A China Daily editorial named Altman, Musk and Amodei and argued the sudden alignment 'looks less like a new concern for humanity and more like a bid to protect profits and slow Chinese competitors' (@v_shakthi relay, 2026-09-16). Separately People's Daily rebutted the NSA/CISA/FBI advisory on 'industrial-scale' distillation as 'politicizing technology issues, an old tactic of US hegemony'; @kyleichan's observation is the substantive part — 'Beijing never denies doing distillation and instead argues it's a common industry practice.' (5) COMMERCIAL COST NOW ATTRIBUTED. Ramp data relayed in-window puts OpenAI at ~13% of enterprise AI spend versus Anthropic's ~8%, with relays attributing part of the gap to Anthropic slowing frontier development. Recorded as third-party attribution, NOT a measured causal effect — the GPT-6 Astra launch ([[openai-gpt-6]]) is an obvious confound in the same window. (6) BACKLASH MOVED TO THE EVALUATION INFRASTRUCTURE. @kevinnbass published an 'audit of Anthropic's finances' calling for a Congressional investigation and arguing METR is financially dependent on Anthropic equity and therefore compromised as the third-party evaluator Amodei proposes. Unverified single-source advocacy; logged because the conflict-of-interest attack has moved from timing (the IPO, [[anthropic-ipo-2026-06]]) to the institution Wang's own point 2 depends on. The coordination itself was separately confirmed on the record this cycle — see [[industry-frontier-safety-standards-body-2026-09]]."
---

The useful question is not whether the essay is right. It is whether anything
shipped differently because of it, and so far the honest answer is: one thing.
Altman disclosed that OpenAI now writes explicit safety cases *before* frontier
reinforcement-learning runs it expects to raise capability significantly. That
is a gate on training, not on deployment, and it is the first concrete
relocation of a safety checkpoint from the end of the pipeline to the middle.
Everything else in this window — agreements, op-eds, rejections — is position,
not process.

The second thing worth separating is the difference between the arguments. Both
Amodei and Altman name concentration of power as a risk, and Altman explicitly
includes "one lab ending up with too much power" as an example. Cohere's
response is that this is exactly what a standards regime run by the largest
labs would produce: "evidenced standards, not a cartel." Those are not two
different opinions on pacing; they are two different accounts of who is made
safer by it. The reported industry-led standards body
([[industry-frontier-safety-standards-body-2026-09]]) is where that argument
becomes a structure or fails to.

Third, the timing has an obvious conflict and it was noticed in-window: Amodei
is making a slow-down-the-industry argument while Anthropic meets prospective
investors ahead of a potential $2T market debut ([[anthropic-ipo-2026-06]]).
Trade press framed it as a balancing act; the sharper version, circulating from
open-weights advocates, is that a safety regime raises fixed compliance costs
and therefore barriers to entry. Neither reading is established here. What is
established is that both things are true at once, which is why the market
reaction and the IPO storyline are logged on this ticket rather than dismissed
as noise.

The falsifier is simple and worth stating in advance. If pacing is real, some
lab eventually announces a model it held back, or a release date it moved, and
says why. Until then this ticket tracks a debate, and the entries above should
be read as positions taken, not as capability schedules changed.
