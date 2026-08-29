---
slug: anthropic-external-researcher-access-2026-08
title: Anthropic opens privacy-preserved Claude usage data to external researchers
company: Anthropic
model: null
status: confirmed
status_note: |
  **@AnthropicAI (2026-08-26 17:12 UTC, ~2.3K engagement):** "**For the
  first time, we've given external researchers a way to study AI's impacts
  using real, privacy-preserved Claude usage data.** To date, this work has
  only been possible within AI labs. We can't tell the whole story alone,
  so we opened up our tools." A follow-up post scales it into a standing
  program: "we want to **scale this research model**. If you're a
  researcher and would like access to our tools to pursue work you can't
  otherwise do today, we'd like to hear from you," with an
  expression-of-interest link.

  **Two of the three studies are named and in flight**, which is what
  separates this from an announcement of intent. @AnthropicAI: "**HIP Lab**
  is studying how Claude's behavior relates to **how people feel** when
  using AI, while **METR** is estimating **real-world productivity gains
  from coding agents**. We'll share more from both soon."

  **The framing from @jackclarkSF (co-founder) is the substantive part**,
  and it names a category: "we're piloting a way for outside researchers
  and organizations to study what's happening on AI platforms like Claude
  **while protecting user privacy**… To think AI labs are going to be able
  to figure out all the appropriate ways to measure and assess these
  systems is **hubristic and just obviously wrong**. So we need to figure
  out ways to externalize not only the properties of the systems, but also
  **data about how these systems are interacting with the people in the
  world, which is platform telemetry**. What we're trying to do here is
  prototype the next form of transparency that may be necessary, which is
  **platform transparency**."

  That distinction is load-bearing and should not be flattened. Existing
  third-party access programs — including
  [[openai-researcher-access-program-2026-07]] — give outsiders access to
  **models**. This gives access to **usage telemetry**: what people
  actually do with the system in production. Model access answers "what
  can it do"; platform telemetry answers "what is it doing to people," and
  no external party has previously been able to ask the second question at
  all.

  **The timing is not neutral.** This landed the same day OpenAI published
  its Hugging Face incident report alongside a **METR/Redwood** third-party
  assessment ([[openai-unreleased-containment-escape-2026-07]]) — and METR
  appears on both. Third-party evaluation went from a proposal to something
  two frontier labs shipped on the same day, and Google DeepMind announced
  its own variant a day later
  ([[google-deepmind-double-blind-evals-2026-08]]).

  Verification `confirmed`: first-party Anthropic institutional account
  plus a named co-founder, with specific named external partners. Status
  `confirmed` rather than `released` because what shipped is a **pilot with
  an application form**, not general availability — no eligibility
  criteria, no published data schema, no privacy methodology, and no output
  yet. The obvious unanswered question: **who decides which researchers get
  in**, and what happens when a study's findings are unflattering. Nothing
  in-window addresses either.
expected: "Announced 2026-08-26 as a pilot with an open expression-of-interest form: external researchers given access to real, privacy-preserved Claude usage data plus Anthropic's analysis tools. Three studies, two named — HIP Lab on how Claude's behaviour relates to how users feel, METR on real-world productivity gains from coding agents. Pending: published results from any study, the privacy methodology and data schema, eligibility criteria and who adjudicates access, whether findings can be published without lab approval, and whether other labs follow"
labels:
  - anthropic
  - transparency
  - third-party-eval
  - platform-telemetry
  - safety
verification: confirmed
sources:
  - "@AnthropicAI"
  - https://x.com/AnthropicAI/status/2092661573223657834
  - https://x.com/AnthropicAI/status/2092661577086636154
  - "@jackclarkSF"
  - https://x.com/jackclarkSF/status/2092673759895511201
created_at: 2026-08-27
updated_at: 2026-08-27
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-27
    change: "Created — Anthropic opened privacy-preserved Claude usage data to external researchers for the first time. @AnthropicAI (2026-08-26 17:12 UTC, ~2.3K engagement): 'For the first time, we've given external researchers a way to study AI's impacts using real, privacy-preserved Claude usage data. To date, this work has only been possible within AI labs. We can't tell the whole story alone, so we opened up our tools', with a follow-up post turning it into a standing program and an expression-of-interest link. Two of three studies are named and already running: HIP Lab on how Claude's behaviour relates to how people feel when using AI, and METR on real-world productivity gains from coding agents. Co-founder @jackclarkSF supplies the framing and the category name: labs assuming they can determine all the appropriate ways to measure their own systems is 'hubristic and just obviously wrong', so what is needed is externalizing 'data about how these systems are interacting with the people in the world, which is platform telemetry' — he calls the pilot an attempt at 'platform transparency'. The distinction from existing programs is the point and is recorded deliberately: [[openai-researcher-access-program-2026-07]] gives outsiders access to MODELS, this gives access to USAGE TELEMETRY, and only the second can answer what a deployed system is doing to people. Status confirmed rather than released — what shipped is a pilot with an application form, with no eligibility criteria, no published data schema, no privacy methodology and no results yet. Verification confirmed on the institutional account plus a named co-founder plus named external partners. Unanswered in-window and worth watching: who adjudicates researcher access, and what happens when a study's findings are unflattering. Same-day context: OpenAI published its Hugging Face incident report with a METR/Redwood third-party assessment ([[openai-unreleased-containment-escape-2026-07]]) — METR appears on both — and Google DeepMind announced double-blind evaluations a day later ([[google-deepmind-double-blind-evals-2026-08]])."
---

Anthropic has given **external researchers access to real,
privacy-preserved Claude usage data** — a pilot with three studies, two of
them named, and an open application form.

**The category matters more than the program.** Every third-party access
scheme in this ticket set so far hands outsiders a **model**:
[[openai-researcher-access-program-2026-07]] does, and so does the
evaluation access behind [[openai-unreleased-containment-escape-2026-07]].
@jackclarkSF is proposing something different — **platform telemetry**.
The distinction is simple and consequential: model access lets you ask
what a system *can* do in a lab; telemetry access lets you ask what it *is*
doing, at scale, to people who did not consent to being studied by a lab's
internal team. Until now, only the lab could ask the second question, and
only the lab saw the answer.

**The self-criticism is unusually direct for a company announcement.**
"To think AI labs are going to be able to figure out all the appropriate
ways to measure and assess these systems is hubristic and just obviously
wrong" is a concession that internal measurement is structurally
insufficient, published by a co-founder. Compare @BethMayBarnes's
same-week warning from the METR side that third-party investigators risk
"providing the illusion of independent oversight" — the two are the same
worry approached from opposite ends.

**What determines whether this is real.** Three things, none of them
answered in-window: (1) can participating researchers **publish without
lab approval**; (2) **who selects** the researchers; (3) does the
privacy-preservation methodology survive scrutiny, or does it sand off
exactly the behaviour worth studying. A transparency program whose access
is gated by the entity being examined is only as good as its answers to
those questions.

**Transition triggers:**
- Published results from the HIP Lab or METR studies → UPDATE.
- The data schema, privacy methodology, or access criteria published →
  UPDATE.
- General availability beyond the pilot → advance to `released`.
- Another lab shipping an equivalent telemetry program → its own ticket,
  cross-linked.

**Dedup note:** OpenAI's model-access program stays on
[[openai-researcher-access-program-2026-07]]; the METR/Redwood incident
assessment stays on [[openai-unreleased-containment-escape-2026-07]];
Google DeepMind's double-blind evaluation pilot stays on
[[google-deepmind-double-blind-evals-2026-08]]. Further Anthropic
researcher-access signal UPDATES this ticket.
