---
slug: mythos-public-release
title: Claude Mythos — full public release
company: Anthropic
model: Mythos
status: in-testing
status_note: |
  Multi-cloud gated preview (AWS Claude Platform GA 2026-05-11, GCP Vertex AI
  Private Preview 2026-05-16) with no plan for a public release.
expected: TBD — voluntary CAISI partnership; toned-down variant possible "in foreseeable future" (Boris Cherny, 2026-05-05)
labels:
  - frontier-model
  - gated
  - multi-cloud
  - project-glasswing
verification: confirmed
sources:
  - https://red.anthropic.com/2026/mythos-preview/
  - https://cloud.google.com/blog/products/ai-machine-learning/claude-mythos-preview-on-vertex-ai
  - https://www.anthropic.com/glasswing
  - "@AnthropicAI"
  - "@scaling01"
  - "@kimmonismus"
  - "@AndrewCurran_"
  - "@AiBattle_"
  - "@testingcatalog"
  - "@techcrunch"
  - "@alexalbert__"
  - https://the-decoder.com/anthropics-mythos-model-is-reportedly-powering-nsa-offensive-cyber-ops-against-china-and-iran/
created_at: 2026-04-12
updated_at: 2026-06-08
closed_at: null
closed_reason: null
history:
  - ts: 2026-04-12
    change: Created — initial Mythos benchmark traces leaked
  - ts: 2026-05-05
    change: "Pricing reported at $25 / $125 per MTok input/output by Boris Cherny"
  - ts: 2026-05-11
    change: AWS Claude Platform GA — first cloud surface for Mythos (gated)
  - ts: 2026-05-15
    change: "scaling01 viral post (\"It's over. Mythos is insane\") — Mythos at ~69% on the benchmark vs GPT-5.5 baseline"
  - ts: 2026-05-16
    change: GCP Vertex AI Private Preview confirmed via Google Cloud blog — Mythos appears in GCP console without a preview label
  - ts: 2026-05-16
    change: kimmonismus argues a public release is structurally implausible despite GCP artifact
  - ts: 2026-05-20
    change: "Secondary report: Anthropic is reportedly letting Glasswing partners share cybersecurity findings surfaced by Mythos with other organizations — a governance change for the gated preview (not yet confirmed on Anthropic's own channels)"
  - ts: 2026-05-25
    change: "TechCrunch coverage — \"Anthropic debuts preview of Mythos in a new cybersecurity initiative,\" putting the gated cyber angle in primary tech press and corroborating the 2026-05-20 Glasswing cyber-findings-sharing report"
  - ts: 2026-05-28
    change: "Glasswing month-1 update (official @AnthropicAI, 2026-05-22 19:38 UTC): Anthropic + partners have found more than 10,000 high- or critical-severity vulnerabilities in essential software since the April launch, framed by Anthropic as a volume the software industry will need to adapt to. Separately on 2026-05-26 @alexalbert__ RTd @__alpoge__ checking whether Mythos can solve the Erdős unit-distance problem (the same problem OpenAI announced an internal-model breakthrough on May 20) — a third-party capability probe rather than an Anthropic claim, but on the same benchmark surface"
  - ts: 2026-05-29
    change: "Opus 4.8 launch coverage (2026-05-28) references Project Glasswing as continuing to test Claude Mythos Preview for cybersecurity applications, with broader availability hinted 'in the coming weeks' (per IT-Administrator and other launch-day write-ups). No primary @AnthropicAI confirmation of a Mythos public-release schedule — adjacent signal, gated-preview stance unchanged"
  - ts: 2026-06-05
    change: "Glasswing preview expansion (secondary): reports describe Anthropic extending Claude Mythos Preview access from the initial ~50 partners to **150+ organizations across 15 countries (incl. India)**, prioritizing critical sectors (power, water, healthcare, hardware) and partners where one exploit could affect 100M+ people; initial cohort said to have surfaced 10,000+ high/critical flaws (consistent with the 2026-05-22 official month-1 figure). Pricing restated at **$25 / $125 per MTok**. Separately, a new Anthropic model name **`claude-oceanus-v1-p`** reportedly appeared for red-team access — a possible Mythos-adjacent successor, spun out to its own ticket [[anthropic-claude-oceanus-v1]]. Still no public-release schedule; gated stance unchanged, status remains in-testing"
  - ts: 2026-06-07
    change: "New deployment + leak signal, gated stance unchanged. The Decoder (2026-06-05) reports **Mythos is powering NSA offensive cyber ops against China and Iran**, with ~6 Anthropic engineers stationed at the NSA adapting the model — a national-security application angle for the gated preview (secondary, no Anthropic primary). MIT Tech Review's 'the Meta hack shows there's more to AI security than Mythos' (2026-06-05) keeps Mythos as the reference point in the AI-security discourse. This-cycle X leak chatter stayed rumor-grade: a `claude-mythos-5` slug reportedly surfaced in Dev Mode (floated as a fourth class above Opus), plus a 'too dangerous to release' branding-critique thread and unsourced 'Apple + 150+ orgs, public in weeks' hype — no Anthropic primary, held to skeptic-grade. Status remains in-testing / confirmed"
  - ts: 2026-06-08
    change: "Mythos-5 rebrand rumor persists (skeptic-grade, no new corroboration). Low-credibility single source (@ssict / Saudi ICT Shopper News, 2026-06-08 07:33 UTC) claims **'Claude Mythos 5' will be the official new name for Anthropic's next flagship, dropping the Opus brand entirely** — framed against a purported 'June 16 IPO filing.' The IPO-date claim garbles the already-confirmed 2026-06-01 confidential S-1 ([[anthropic-ipo-2026-06]]), undercutting the source's reliability. Restates the 2026-06-07 `claude-mythos-5` Dev-Mode slug chatter without adding a primary source. No @AnthropicAI confirmation; gated-preview stance and status unchanged (in-testing / confirmed)"
---

Mythos is Anthropic's post-Opus-4.7 frontier model, operated as a
multi-cloud gated product rather than a public release. It surfaces only
inside **Project Glasswing** — a ~40-org partnership including AWS, Apple,
Microsoft, Google, CrowdStrike, and Palo Alto — and through the two
cloud surfaces that the partner companies happen to run on (AWS, GCP).

The benchmark dominance is large enough that Alex Heath called Mythos
"despite not being widely available, has reset how every lab talks about
what leading means." `scaling01`'s May 15 viral post puts Mythos at
~69% on the unspecified frontier benchmark vs the GPT-5.5 baseline.

**Why this ticket stays open:** Anthropic has explicitly signaled no
public release ("toned-down version in foreseeable future" — Cherny).
That is itself the news. The ticket tracks the multi-cloud preview's
expansion (AWS → GCP → ?) rather than a release date. If Anthropic
ever flips to public availability, this ticket transitions to
`released`. If a permanently-gated stance is confirmed (e.g. by a
formal Anthropic statement), this ticket closes with reason
`gated-permanent` and the ongoing Glasswing coverage moves to a
dedicated `project-glasswing` ticket.

**Dedup notes for the agent:** new signal about Mythos pricing,
preview expansions, or partner additions UPDATES this ticket. A new
Anthropic model variant (e.g. "Sonnet-Mythos") with a different
release plan is a separate ticket; reference this one from its body.
