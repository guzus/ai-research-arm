---
eyebrow: LITIGATION ANALYSIS · APPLE v. LIU
title: "Apple's Own Front Door: what OpenAI's post-departure receipts actually prove — and why the offboarding defence is the weakest one it has"
deck: OpenAI did not file the messages. It published them. And the element they attack is the one element a defendant almost never wins.
domain: policy
lede: |
  On 3 August 2026, hours after Apple moved for a preliminary injunction, OpenAI
  published a page titled "Apple is getting this wrong" containing screenshots of
  private messages and lawyer emails. The headline read as a bombshell: Apple's own
  offboarding was so lax that a departed engineer kept reaching its files for months,
  and a still-employed colleague kept asking him for help. If Apple could not keep its
  own secrets, how can it sue anyone for taking them? The instinct is sound and the
  law is against it. Three things are true at once: the material was published, not
  filed; the element it attacks is the one element defendants almost never win as a
  matter of law; and the genuinely dangerous facts for Apple are sitting in Apple's
  own declarations, not OpenAI's blog.
stats:
  - {label: Case, value: "5:26-cv-07078", note: "N.D. Cal., Judge Davila"}
  - {label: Cloud access after exit, value: 95, unit: "days"}
  - {label: Browser sign-in blocked, value: 2, unit: "days"}
  - {label: Files downloaded, value: 37, note: "across 5 sessions"}
  - {label: Apple contested wins, value: 0, note: "4 prior departure suits"}
---

:::callout(kind=info, label="The short answer")
- **OpenAI did not "file" anything.** The post-departure messages appeared on a corporate blog on 3 August 2026.[^1] As of the public docket on 4 August, no defendant had filed an answer, a motion to dismiss, or an opposition; oppositions are due 17 August.[^2]
- **They are iMessages, not Apple offboarding emails.** The exhibits are texts between Chang Liu and Apple colleagues dated 22 January to 14 February 2026, plus a February chain between outside counsel and OpenAI's General Counsel. Nothing from Apple IT, HR or corporate security appears.[^1,3]
- **Apple's own filings are worse for Apple than OpenAI's blog is.** Apple's complaint alleges it "disables and prohibits access to its network storage upon an employee's departure";[^12] its own forensic declaration concedes "the deprovisioning scripts that ran in January 2026 did not properly deprovision (revoke) Mr. Liu's access."[^5]
- **Even so, the offboarding defence is the weakest one OpenAI has.** "Reasonable measures" does not mean perfect measures,[^6,7] the Ninth Circuit holds confidentiality provisions alone are enough to preclude judgment as a matter of law,[^8] and the closest reported case on this exact fact pattern — credentials left live for about four months after departure — denied the defendant summary judgment.[^51]
- **The real leverage is elsewhere:** proving *use* rather than possession, the statutory bar on employment-restraining injunctions,[^9] and Apple's own record of four departure suits with zero contested wins.[^10,11]
:::

## 01. The premise, corrected: published, not filed

The framing that has travelled fastest — that OpenAI "filed" post-departure emails exposing Apple's offboarding — is wrong in two load-bearing ways, and the corrections change what the documents are worth.

First, the venue. OpenAI published a page on its own domain, unsigned and carrying no publication date on its face.[^1] Press coverage dates it to the night of 3 August 2026 — the same day Apple filed its preliminary-injunction motion.[^2,3] The docket in *Apple Inc. v. Liu*, No. 5:26-cv-07078 (N.D. Cal.), tells the rest: through 4 August, every substantive filing is Apple's — defence activity is limited to appearances and two administrative statements.[^2] Oppositions to the injunction are due 17 August, replies 24 August, hearing 1 October before Judge Edward J. Davila.[^2] Nothing OpenAI has said about the merits is yet before the court.

That distinction is not pedantry. A blog exhibit is unsworn, party-selected and party-redacted — OpenAI's own page carries bracketed markers reading "[Redacted — Apple Information]" and one "[Redacted — Apple schematic]," and the images are clipboard-pasted PNGs on a content-delivery network rather than native exports with metadata.[^1] Court filings carry Rule 11 exposure, declarations under penalty of perjury, and an adversary's right to the unredacted original. None of that attaches here.

Second, the documents. They are not correspondence between Apple's institutions and a departing employee. Exhibit one is 57 timestamped iMessages between Chang Liu and Apple colleagues running 22 January to 14 February 2026.[^1] Exhibit two is a February email chain among Apple's outside counsel Gabriel Gross, OpenAI General Counsel Che Chang, and Apple in-house lawyers — the exchange in which, OpenAI says, Apple "now admit[s] that their outside lawyers emailed the wrong person after confusing two Asian last names."[^1] Notably, Tang Tan — OpenAI's Chief Hardware Officer and the highest-profile defendant — is defended in two sentences of prose with no documentary exhibit at all.[^1,3]

:::kv
- {term: Case, def: "Apple Inc. v. Liu, No. 5:26-cv-07078 (N.D. Cal., San Jose)"}
- {term: Filed, def: "10 July 2026"}
- {term: Judge, def: "Edward J. Davila; discovery to Mag. J. Cousins"}
- {term: Defendants, def: "Chang Liu; Tang Yew Tan; OpenAI Foundation; OpenAI Group PBC; io Products LLC"}
- {term: Counts, def: "4 × DTSA misappropriation + 2 × breach of Intellectual Property Agreement"}
- {term: Not pleaded, def: "CUTSA; § 17200 unfair competition; CFAA"}
- {term: PI hearing, def: "1 October 2026"}
:::

What the messages *do* show is real and it is the substantive core of the defence: an Apple employee kept a machine signed into Liu's iCloud session for days past his 22 January last day, and colleagues solicited his help locating files afterwards.[^1] OpenAI's framing is that this is "a common issue with Apple which is caused by them failing to properly manage system access when people leave."[^1] The counterpoint, developed below, is that this is an argument about an element on which plaintiffs almost never lose. What weakens it further is that OpenAI has not yet had to say any of it under oath — and its own redaction of "Apple Information" from messages in its custody sits awkwardly beside its assertion that it does not have Apple's trade secrets.[^1] Why it matters: the entire public conversation is running on evidence that has not been tested, filed, or authenticated.

## 02. Apple's complaint argues with itself

The most damaging document about Apple's offboarding is Apple's complaint. Filed 10 July 2026, it pleads six counts — four Defend Trade Secrets Act misappropriation claims, one each against Liu, Tan, the OpenAI entities and io Products, plus two breach-of-Intellectual-Property-Agreement counts against the individuals.[^12] Conspicuously absent: any California Uniform Trade Secrets Act count, any § 17200 unfair-competition count, and any Computer Fraud and Abuse Act count.[^12] That pleading architecture is deliberate and it is discussed in section 07.

Apple's secrecy-measures allegations run through paragraphs 42 to 52: contractual, physical and digital controls, an annual "Business Conduct" course, locked buildings, cameras and guards, supplier confidentiality and chain-of-custody protocols.[^12] Then comes paragraph 47, which is the sentence that will be read back to Apple at every stage of this case:

:::quote(attr="Apple Inc. v. Liu, complaint ¶ 47")
Apple disables and prohibits access to its network storage upon an employee's departure.
:::

Ten paragraphs later, the complaint concedes that Liu "still could access the Apple's network repository after leaving Apple, the result of a then-unknown authentication vulnerability," and footnote 1 adds: "Upon discovery, Apple quickly fixed this bug."[^12] Paragraph 5 concedes that Liu "failed to return an Apple-issued work laptop that he had previously authenticated to Apple's network."[^12] Paragraph 56 concedes that a non-employee used a current employee's Apple-issued, network-authenticated computer.[^12] And paragraphs 11 and 73 allege that the artefact Tan circulated was Apple's own internal offboarding procedure document, marked "Need to Know" — meaning the policy Apple cites as a protective measure is itself among the things that walked out.[^12]

Apple pre-built its answers. Paragraph 46 pleads that a return obligation existed and that Liu "was unresponsive to Apple's outreach."[^12] Paragraph 52 pleads that when Apple "learns of a bug or vulnerability in its security measures, it investigates and takes steps to fix the issue" — a prophylactic that reads as though it were drafted with paragraph 57 in view.[^12] And Apple's theory is that non-response was coached evasion, not Apple's omission: the complaint alleges an OpenAI recruiter told a hire he "won't sign anything at the exit interview," and that Tan warned recruits "Apple will probably walk you out."[^13]

The counterpoint a defence expert will press is narrower and harder to answer. Reasonableness is judged at the time of the alleged taking, not at the time of the patch. Footnote 1 concedes the measure was defective while the files were moving. And paragraph 145 — pleading breach by "failing to return an Apple-issued work device" — concedes that the offboarding process did not verify return.[^12] Why this matters: Apple has voluntarily put the adequacy of its own access controls into the pleading, which is why the fight over them is now unavoidable.

## 03. Two days, ninety-five days

The complaint left out every timestamp that would prove diligence. It pleads no date for the return demand, no date for credential disablement, no date of discovery and no patch date. Apple's preliminary-injunction package, filed 3 August, finally supplied some of them — and the picture is more specific and more awkward than "a bug."

Roffman's forensic declaration states that "the deprovisioning scripts that ran in January 2026 did not properly deprovision (revoke) Mr. Liu's access," attributing the finding to a 16 July 2026 interview with an Apple IS&T manager.[^5] It states that browser sign-ins by Liu to Apple repositories "would have been blocked as of January 24, 2026" — two days after his last day.[^5] The general credential kill worked. The third-party cloud repository was a separate, silent failure.

:::compare
- {role: "SSO / BROWSER", name: "AppleConnect sign-in blocked", value: "2 days"}
- {role: "CLOUD REPOSITORY", name: "Access still live to last download", value: "95 days"}
- {role: SUBJECT, name: "Unique files downloaded", value: "37"}
:::

The download record is precise. Apple alleges Liu "performed over 240 downloads from this third-party cloud storage, including downloads of at least thirty-seven unique Apple files," with over 470 "Content Access" events, across five sessions on 8 and 10 February, 7 and 11 March, and 27 April 2026 — almost all late at night Pacific time.[^5] From Liu's 22 January departure to that final 27 April session is 95 days. The first download came 17 days after he left.

:::timeline
- {date: 2026-01-22, headline: "Liu's last day at Apple", body: "Confirmed by both Apple's complaint and OpenAI's published response."}
- {date: 2026-01-24, headline: "Browser sign-in blocked", body: "AppleConnect would have blocked repository logins — two days after exit."}
- {date: 2026-02-08, headline: "First download session", body: "Third-party cloud repository access still live; 17 days post-departure."}
- {date: 2026-02-14, headline: "Last published iMessage", body: "End of the date range in OpenAI's exhibit."}
- {date: 2026-04-27, headline: "Final download session", body: "Files 13–37 in a single hour; 95 days post-departure."}
- {date: 2026-07-10, headline: "Apple files suit", body: "Six counts in N.D. Cal.; no CUTSA, no CFAA."}
- {date: 2026-07-17, headline: "Preservation letters", body: "Reported to roughly 40 non-defendant ex-employees at OpenAI."}
- {date: 2026-08-03, headline: "PI motion, then rebuttal", body: "Apple moves on day 24; OpenAI publishes the same night."}
- {date: 2026-10-01, headline: "Preliminary-injunction hearing", body: "Before Judge Davila, San Jose."}
:::

Three timestamps are still missing from the entire injunction record: the date Apple discovered the access, the date it patched, and any date on which Apple demanded the laptop back.[^5,13] Those are the facts that convert "we act promptly" from assertion into evidence, and Apple has now had two opportunities to supply them.

There is a structural gap worth naming. Across nine supporting declarations, no Apple information-security witness declares. The deprovisioning failure rests entirely on attorney-arranged interviews of an unnamed IS&T manager, cited as 16 July by the forensic declarant and 23 July by Apple's expert.[^5,14] Apple's hardware-engineering declarant covers digital measures without mentioning the bug; its human-resources declarant covers offboarding without mentioning deprovisioning.[^14] The counterpoint: on a preliminary-injunction motion the evidentiary bar is lower than at trial, and hearsay is routinely tolerated. Still, on the one element Apple has visibly fortified, the percipient witness is absent. Why it matters: whichever way the injunction goes, the deprovisioning failure is now a documented, dated fact in Apple's own record — not an allegation OpenAI made.

## 04. "Reasonable" is not "perfect" — what the element actually asks

Here is where the popular argument runs into the statute. The Defend Trade Secrets Act defines a trade secret to require that "the owner thereof has taken reasonable measures to keep such information secret."[^15] California's equivalent asks whether the information "[i]s the subject of efforts that are reasonable under the circumstances to maintain its secrecy."[^16] Neither says "effective." Neither says "complete."

The canonical statement is Judge Posner's in *Rockwell Graphic Systems v. DEV Industries*, reversing summary judgment against a trade-secret owner: "perfect security is not optimum security," because precautions cost money and "[i]f trade secrets are protected only if their owners take extravagant, productivity-impairing measures to maintain their secrecy," the incentive to invent falls.[^6] He added the procedural rule that governs everything downstream: "only in an extreme case can what is a 'reasonable' precaution be determined on a motion for summary judgment."[^6] The Seventh Circuit reaffirmed it in *Learning Curve Toys v. PlayWood Toys*, reinstating a jury verdict after the district court took the element away: the standard "does not require perfection," and sufficiency of measures "ordinarily is a question of fact for the jury."[^7] The court acknowledged that "PlayWood might have done more to protect its secret" — and reinstated the verdict anyway.[^7]

The Fifth Circuit put the principle in its sharpest form more than fifty years ago: "Reasonable precautions against predatory eyes we may require, but an impenetrable fortress is an unreasonable requirement."[^17]

Two doctrinal points matter more than the slogans.

First, the Ninth Circuit — the circuit that governs this case — has stated the rule as something close to a floor, not a balance. In *InteliClear v. ETC Global Holdings* it held that "Confidentiality provisions constitute reasonable steps to maintain secrecy," and that the plaintiff's efforts to protect its secrets through licensing agreements "constitute reasonable measures that are adequate to preclude judgment as a matter of law."[^8] The Fourth Circuit followed in November 2025, reversing judgment on the pleadings: it was "sufficient that Appellants allege they protected the Proprietary Software by requiring employees to sign the confidentiality agreement and Invention Provision," and "[b]ut that does not mean they are required to allege more, and we see no reason to create such a requirement."[^18] That is a pleading-stage holding, and the same court cautioned that "what may constitute 'reasonable measures' must be considered in light of the nature of the trade secret."[^18] If Apple has signed Intellectual Property Agreements — and it pleads that it conditions hiring on them[^12] — that line is a short answer to the entire offboarding argument at the dispositive-motion stage.

Second, and more interesting from first principles: reasonableness is *relational to the defendant's method*. Restatement (Third) of Unfair Competition § 43 comment c weighs "the foreseeability of the conduct through which the secret was acquired" and "the availability and cost of effective precautions against such an acquisition, evaluated in light of the economic value of the trade secret."[^19] *duPont* held that "we need not require the discoverer of a trade secret to guard against the unanticipated, the undetectable, or the unpreventable methods of espionage now available."[^17] A defendant arguing that Apple should have foreseen and closed an unknown authentication flaw is, by construction, arguing that the owner should have anticipated an unforeseeable failure — which is the precise argument this line of authority rejects.

The honest counterweight: courts do sometimes end cases here. The Eleventh Circuit affirmed summary judgment in *Yellowfin Yachts*, holding the owner "effectively abandoned all oversight in the security of the Customer Information" because it "encourag[ed] Barker to keep the Customer Information on his cellphone and personal laptop," and "when Barker left Yellowfin, the company did not request that Barker return or delete any of the information."[^20] The Tenth Circuit affirmed in *Snyder v. Beam* in August 2025 that "no reasonable jury could conclude that Snyder's actions meet the minimum definition of reasonable measures or efforts to maintain secrecy" — though there the plaintiff was the departed employee, and the failures were his own.[^21] The Second Circuit affirmed a Rule 12 dismissal in *Turret Labs*, holding that where a claimed secret consists "primarily, if not entirely," of software functionality, "the reasonableness analysis will often focus on who is given access, and on the importance of confidentiality and nondisclosure agreements to maintaining secrecy" — a non-precedential summary order, expressly conditioned on that software predicate.[^22] Why this matters: those cases exist — but read closely, each involves the owner *affirmatively handing information to someone under no confidentiality obligation*, which is a different failure from imperfect revocation.

## 05. The base rate that sinks the offboarding defence

If "reasonable" is measured against what a competent enterprise actually does, the empirical question decides the argument. And the data — with real caveats — says residual post-departure access is ordinary, not aberrant.

A YouGov-fielded survey of 213 senior IT professionals found 49% of enterprises lost at least 5% of technology assets to departures, 27% lost more than 10%, and 42% saw unauthorised post-departure access to software-as-a-service or cloud systems in at least 5% of instances.[^23] Among organisations above 10,000 employees, roughly a quarter reported losing at least 10% of endpoint devices at departure.[^24] A separate survey of 500 US IT decision-makers found 25% take more than a week to deprovision a departing employee and 48% were aware of former employees with live corporate access.[^25] A 2023 survey of 375 US IT professionals found 70% had experienced the impacts of ineffective offboarding — while 79% remained confident in their process, which is the most telling pairing in the set.[^26]

:::rank-list
- {label: "Experienced impacts of ineffective offboarding (n=375 IT pros)", value: "70%", pct: 100}
- {label: "Lost ≥5% of technology assets to departures (n=213)", value: "49%", pct: 70}
- {label: "Unauthorised post-departure cloud access in ≥5% of instances (n=213)", value: "42%", pct: 60}
- {label: "Lost >10% of technology assets (n=213)", value: "27%", pct: 39}
- {label: "Take >1 week to fully deprovision (n=500)", value: "25%", pct: 36}
:::

:::note
These bars come from THREE surveys, not five data points from one: OneLogin (2017, n=500), Oomnitza/YouGov (2022, n=213 — the source of three of the five bars) and Nudge Security (2023, n=375). Different populations, different questions, different years; they are not a single distribution and should not be read as one. All three are vendor-sponsored, though the 213-respondent study was independently fielded by YouGov.
:::

Two honesty checks. Every high figure in this literature comes from a vendor selling the remedy, and the highest numbers — surveys reporting that the great majority of workers retained access to a former employer's systems — are employee self-reports that never verified the access worked, with denominators padded by consumer applications.[^25] Those should not be used. The one independent, peer-reviewed source is qualitative: fifteen practitioner interviews presented at USENIX SOUPS in August 2025, which found offboarding pegged to an "often artificial last day" that "often does not align with the employee's termination date," with email accounts remaining live afterwards.[^27] It establishes mechanism and normality; it establishes no base rate, and thirteen of its fifteen participants are European, which weakens it as a proxy for US practice.[^27]

So the defensible claim is narrower than "near-universal," and it is still sufficient. Residual access and non-returned devices are routine, recognised, non-anomalous outcomes at large enterprises. Even the containment benchmark supports it: insider incidents take an average of 67 days to contain, down from 86 in 2023, at an average annual cost of $19.5 million per affected organisation.[^29] Against that backdrop, a two-day sign-in block plus a 95-day orphaned share on a third-party repository sits inside — not outside — the observed distribution of competent practice. Why this matters: to win on this element, OpenAI must persuade a court that Apple fell below a standard that the available evidence suggests most large enterprises also fall below.

## 06. What Apple thinks its weak spot is: the Pooley tell

Litigants tell you what frightens them by what they spend money on. Apple's preliminary-injunction motion is supported by nine declarations. One of them is from James Pooley — author of the leading trade-secrets treatise, former Deputy Director General of the World Intellectual Property Organization, and the expert whose testimony informed the DTSA itself.[^14]

Pooley was asked one question and gives one operative opinion, confined entirely to reasonable measures: "it is my opinion that Apple has taken reasonable measures to protect the secrecy of the information it has claimed as trade secrets in this action."[^14] He offers nothing on misappropriation, use, damages or the defendants' conduct. Retaining the single most authoritative name in the field to address one element, and only that element, is a direct signal that Apple regards § 1839(3)(A) as the place it can be hurt.

His declaration's actual function is not praise. It is to install the legal scaffolding that makes one failure non-dispositive: a three-factor balancing test — "the value of the information; the risk of loss or contamination; and the cost of various measures that could reduce or eliminate the risk" — and the disclaimer that "Reasonableness does not demand perfection and depends on circumstances."[^14] He cites Restatement § 43 comment c.[^14,19] He touches the vulnerability once, at paragraph 39, purely as remediation: "If issues arise with security for file-sharing platforms, Apple takes action to resolve those issues and ensure they do not repeat."[^14]

The motion itself makes the same move rhetorically. It never uses the word "deprovisioning." It recasts a failure of Apple's revocation pipeline as an affirmative act by Liu — "a previously unknown authentication bug" that he "exploited" — and answers the reasonableness attack with speed rather than explanation: "Apple acted immediately and reasonably, investigating the issue and correcting it."[^13] "Immediately" is undated. And the framing is contestable on Apple's own evidence: Roffman describes not an exotic vulnerability Liu discovered but Apple's own deprovisioning script failing to take.[^5]

Two exposures follow. Pooley never benchmarks Apple against hardware- or semiconductor-industry custom, stating instead that his framework "applies across all industries" — which invites a challenge to the fit of the opinion.[^14] And an expert opinion on the ultimate reasonableness question edges toward the province of the jury in a circuit where that question is conventionally the jury's. The counterpoint: on a preliminary injunction decided by a judge on a paper record, both objections carry far less weight than they would at trial. Why it matters: Apple has told the court, through its own choice of expert, exactly which element it expects to litigate.

## 07. The defences that actually kill these cases

Reason from the mechanics rather than from the headline, and the offboarding theory ranks last among the defences available.

Start with element structure. Section 1839(3) is a *definition*, and it is conjunctive: information is a trade secret only if the owner took reasonable measures **and** it derives independent economic value from secrecy.[^15] Misappropriation, and the "improper means" that qualify it, are defined separately and only operate on something that is already a trade secret.[^15] Two consequences follow, and they cut in opposite directions. If measures fail, no quantity of bad defendant conduct creates a trade secret. But equally, no amount of sloppy offboarding is a *contributory-negligence defence* — reasonable measures is a status element, not a fault allocation.

Now count what is actually available:

| Defence | Mechanism | Realistic force |
|---|---|---|
| *No use, only possession* | DTSA requires misappropriation, not proximity | **Strongest.** This is what killed xAI's suit against OpenAI at the pleadings |
| *§ 1836(b)(3)(A)(i) injunction cap* | Federal limit on employment-restraining relief | **Strong** — limits remedy, not liability |
| *Whyte* / *Hooked Media* | California rejects inevitable disclosure; poaching is lawful | **Strong** against any head-knowledge theory |
| Particularity of identification | Rule 12 and PI-stage identification | **Moderate**, and relocated by *Quintara* |
| § 2019.210 pre-discovery disclosure | California trade-secret identification statute | **Inoperative as pleaded** |
| CUTSA supersession | Displaces common-law claims | **Inoperative as pleaded** |
| *Lax offboarding* | § 1839(3)(A) reasonable measures | **Weakest** — cannot end the case at any stage |

The two "inoperative" rows are the most interesting, because they are the product of deliberate drafting. Section 2019.210 applies by its terms only to an action alleging misappropriation "under the Uniform Trade Secrets Act."[^31] CUTSA supersession operates only on state-law remedies, and § 3426.7(b)(1) expressly provides that the title "does not affect (1) contractual remedies, whether or not based upon misappropriation of a trade secret."[^16] Apple pleaded four federal DTSA counts and two contract counts and nothing else.[^12] In one move, Weil, Gotshal & Manges mooted both. And in August 2025 the Ninth Circuit held in *Quintara Biosciences* that § 2019.210's rule "does not control a federal trade-secret claim," expressly reserving whether it binds federal courts on CUTSA claims — so a DTSA-only complaint sits inside the settled half of that question.[^32]

What remains is where the case will actually be decided. On *use*: Apple must show OpenAI used something, not that former Apple people possess knowledge — the identical vulnerability that ended *X.AI Corp. v. OpenAI* at the pleadings stage on 15 June 2026, dismissed without leave to amend after an earlier dismissal with leave, and that led Judge Alsup in *Waymo* to refuse to halt Uber's programme.[^33,43] On *remedy*: § 1836(b)(3)(A)(i) conditions any injunction on the order not operating to "prevent a person from entering into an employment relationship," and requires that conditions placed on such employment rest on evidence of threatened misappropriation "and not merely on the information the person knows."[^9] Apple's brief steers around it explicitly — "Apple does not seek to restrain employee mobility or prevent Defendants from competing"[^13] — but its first requested order, barring "accessing, acquiring, using, or disclosing" Apple information "in any manner including commercial activities," is the seam a defence brief will call a de facto restraint on two men whose current jobs are hardware.[^13]

And on the mobility theory generally, Apple faces its own precedent. In *Hooked Media Group v. Apple*, the California Court of Appeal affirmed summary judgment **for Apple** as defendant, quoting *Reeves v. Hanlon* for the proposition that "no legal wrong is committed when a company solicits and hires away its competitor's employees; absent some independent illegal act."[^34] That trailing clause is load-bearing in both directions — it is the doorway Apple must now walk through. Why this matters: the 400-plus former Apple employees now at OpenAI[^35] make a vivid narrative and, standing alone, no cause of action.

## 08. What the receipts really damage: the equities, not the element

If the iMessages do not defeat the trade-secret element, what are they for? Three things, and they are not nothing.

**Irreparable harm.** A preliminary injunction is equitable, and equity notices who left the door open. Apple must show urgency in October about files that moved between February and April, on a repository its own script failed to close, discovered through its own audit at an undisclosed date.[^5] Nothing in the injunction record dates the discovery or the patch.[^5,13] An owner that waited five months between its February pre-suit letter and its July complaint,[^1] then another 24 days to move for relief,[^2] has a harder time arguing that the next 60 days are intolerable.

**Consent and improper means.** Apple's theory requires acquisition by improper means — enumerated in the statute as "theft, bribery, misrepresentation, breach or inducement of a breach of a duty to maintain secrecy, or espionage through electronic or other means."[^15] Messages showing Apple employees affirmatively asking a departed colleague to help locate files complicate the "rogue actor against a clean system" narrative on which that framing rests.[^1] But the closest reported analogue cuts against OpenAI. A North Carolina business court faced a departed employee whose cloud credentials "remained active until January 2019, approximately four months following [his] departure," and **denied** summary judgment — reasoning that the employer had timely asked its IT vendor to revoke the access, and that it was entitled "to ask the jury to undertake an analysis of the reasonableness" of its efforts.[^51] A vendor's or a script's failure to execute a timely revocation instruction is not the same as never giving one.

**Credibility.** OpenAI's sharpest published claims are not about security at all. They are that Apple "claimed they had a discussion with our General Counsel, which they now concede never happened," and that Apple's outside counsel misdirected a notice after "confusing two Asian last names."[^1] If those concessions are real, they attack the notice-and-bad-faith predicate Apple built its complaint on. They are also not privileged, not sanctionable, and not a discovery incident — Gross remained counsel of record filing on 4 August.[^2] They are a credibility problem, which at a bench hearing is a real but bounded currency.

**Escalation, meanwhile, runs the other way.** Apple sent litigation-preservation letters to roughly 40 former employees now at OpenAI who are not named defendants, reported on 17 July 2026, telling them to preserve potentially relevant documents and communications.[^50] Read alongside the complaint's own "tip of the iceberg" language and its allegation that defendants may already have deleted data,[^12] that is a spoliation-record-building play and a pipeline for adding defendants. It also imposes real personal legal cost on OpenAI's hardware bench, which is leverage independent of the merits — and precisely the sort of pressure that the reported "wildest allegations" coverage amplifies without testing.[^30]

What the messages emphatically do not reach is the recruiting case against Tan. Apple's allegations there — that he used internal Apple codenames to probe candidates still employed at Apple, that he told them "bring some parts you worked on... mlb, battery, shields type of stuff is interesting," and that one interviewee said he "didn't even know we could take those from the office" — concern people who owed live duties of secrecy on the day they were asked.[^13] Whether Apple's revocation scripts worked has no logical bearing on that. The counterpoint worth stating: because reasonable measures attaches to *each* asserted trade secret, if the lapse were severe enough to defeat a particular secret's protected status, every theory resting on that secret fails together — not because the recruiting theory depends on offboarding, but because both depend on the same secret. Why it matters: OpenAI's structural defence is aimed at Liu and does not travel to Tan.

## 09. The record: four suits, zero contested wins

Base rates outrank narratives, and the base rates here are unkind to the idea that this case ends in a courtroom verdict.

Across 2023–2025 pooled, 65% of federal trade-secret cases ended in likely settlement, 15% in a claimant win, 4% in a defendant win and 15% procedurally — the shares round to 99% in the source.[^36] Median time to trial across that pooled window is about 1,124 days.[^36] Narrowing to 2025 alone, and to a different dataset, just 36 of 1,323 terminations — 2.7% — reached trial.[^37]

:::donut(center-label="2023–25")
- {label: "Likely settlement", value: 65}
- {label: "Claimant win", value: 15}
- {label: "Procedural", value: 15}
- {label: "Defendant win", value: 4}
:::

Filing volume is rising sharply, and the AI share is rising faster. Federal trade-secret filings hit an all-time high of 1,552 in 2025 — a roughly 20% jump over 2024 and the highest total since the DTSA was enacted.[^37,38] Complaints referencing artificial intelligence more than doubled over the same period, from 42 to 105, with the half-year series showing where the inflection sits.[^37]

:::bars
- {label: "AI-referencing complaints, H2 2025", value: "69", pct: 100}
- {label: "H1 2025", value: "36", pct: 52}
- {label: "H2 2024", value: "22", pct: 32}
- {label: "H1 2024", value: "20", pct: 29}
:::

:::note
Only the 2025 total (1,552) and the four half-year AI counts are stated directly in the source; the 2024 annual total is recoverable only by back-computing the reported 20% growth, so no multi-year filings series is charted here. As of the February 2026 report.
:::

Apple's own record is the sharper signal. It has litigated four civil employee-departure matters and obtained **zero contested injunctions and zero litigated damages**. *Apple v. Rivos* — the structurally identical case, mass engineer departure to a startup, N.D. Cal., DTSA plus contract — ran 22.7 months, 690 days, from its 29 April 2022 filing to a stipulated dismissal on 19 March 2024, with no damages and no adjudicated injunction; a joint filing weeks earlier recorded only that "the parties signed an agreement that potentially settles the case."[^10,11] The temporary-restraining-order component of Apple's motion was never adjudicated; only the expedited-discovery half was decided.[^11] *Apple v. Gerard Williams III* was voluntarily dismissed by Apple after 44.6 months and never pleaded a trade-secret count at all.[^39] *Apple v. Lancaster* ended at 19.7 months in an order "granting dismissal and stipulated injunction" — the one matter where Apple obtained injunctive relief, and it came by consent, without any injunction motion ever being filed.[^40] And in *Masimo v. Apple*, on the receiving end, a jury split 6–1 in Apple's favour before a mistrial, and after more than six years of litigation the trade-secret recovery was $0.[^41]

The sector comparators point the same way. OpenAI has now defeated two consecutive suits without a merits adjudication: *X.AI Corp. v. OpenAI*, dismissed at the pleadings, and *Musk v. Altman*, which produced a defence verdict on 18 May 2026 after an advisory jury found every claim time-barred — the merits were never reached.[^33,42] Even the canonical maximum — *Waymo v. Uber*, 14,000 files, a partial injunction and a criminal referral — settled after four days of testimony, on what would have been the fifth trial day, for 0.34% of Uber equity, roughly $245 million in stock, with no admission of misappropriation. Uber's chief executive stopped short of a flat denial, saying only "we do not believe that any trade secrets made their way from Waymo to Uber," while conceding that the circumstances of the departures "in retrospect, raised some hard questions."[^43]

What is genuinely different here is tempo and forum, not stakes. Apple moved for an injunction on day 24 and for expedited discovery on day 25,[^2] and it drew Judge Davila, who wrote the August 2023 *Rivos* order holding Apple had identified its secrets with "sufficient particularity" and who presided over both prosecuted Project Titan criminal cases.[^11] The counterpoint: tempo is not outcome, and *Rivos* also began with a fast motion that was never decided.[^11] Why it matters: the modal outcome is expedited discovery granted in part, an injunction denied or narrowed to the two individuals, and quiet resolution inside 18–30 months.

## 10. What would break this thesis

Four things would, and they deserve to be stated plainly.

**If Apple amends to add a CUTSA count, two dead defences revive at once.** Section 2019.210's pre-discovery identification duty and CUTSA supersession both attach to a Uniform Trade Secrets Act action.[^31,16] They are inoperative today because Apple pleaded around them.[^12] An amendment reopens both, and *Quintara*'s footnote expressly reserved whether § 2019.210 binds federal courts on CUTSA claims.[^32] This is the single contingency most worth watching on the docket.

**If Apple cannot identify a specific secret with particularity, the case narrows drastically regardless of offboarding.** Apple identifies its secrets in five lettered categories at paragraph 40 — hardware engineering and product design, manufacturing and metal-finishing, component technologies, testing methodologies including "negative know-how," and supply chain — with only the metal-finishing process and one manufacturing presentation approaching specificity.[^12] Judge Davila rejected a particularity attack in *Rivos*,[^11] and *Quintara* did not abolish the fight so much as relocate it — the Ninth Circuit preserved district courts' discretion under Rule 26 to "tailor discovery narrowly and to dictate the sequence of discovery," while holding particularity is ordinarily resolved at summary judgment or trial.[^32] Identification is the ground *Quintara* itself was fought on, and paragraph 40's five categories make it live here.[^12,32]

**If OpenAI's exhibits survive contact with the rules of evidence, they become Apple's.** By publishing curated excerpts and telling readers "you can just read the emails for yourself," OpenAI arguably adopted their contents — the Ninth Circuit held in *Sea-Land Service v. Lozen* that a party reproducing another's message with approving framing "incorporated and adopted the contents of Jacques' original message."[^44] It also concedes relevance, which guts a proportionality objection to producing the full unredacted set.[^45] The waiver theory that has circulated is wrong: Rule 502(a) is triggered only by disclosure "made in a federal proceeding or to a federal office or agency," and a blog is neither;[^46] and the iMessages were never privileged, only confidential. But note that Rule 106 runs *against* whoever introduces the statement, and since December 2023 the adverse party "may do so over a hearsay objection" — so if Apple offers the blog content, OpenAI gets to complete it, hearsay-free.[^47] Apple's cleaner play is to introduce the fact and timing of publication, not the content.

**And the publish-instead-of-file gamble may simply keep working.** OpenAI ran this playbook twice against Elon Musk during live litigation, drew zero sanctions, defeated the preliminary injunction outright in March 2025, and won at trial in May 2026.[^42] The one verified case where a public campaign changed an outcome is *Epic v. Apple*, where Judge Gonzalez Rogers wrote that Epic "began a pre-planned, and blistering, marketing campaign against Apple" — and used it to reject the **movant's** reputational-harm theory, which here would cut against Apple.[^48] Markets, for what little the signal is worth, have not moved on the rebuttal at all: Polymarket's implied odds of an OpenAI initial public offering by 31 December 2026 sat at exactly 17.5% on each of 2, 3 and 4 August, spanning the publication.[^52] The complaint itself did move the price — the series ran from about 23.5% down to roughly 18.5% across 10 July — though that day also carried unrelated news, and this is a thinly traded market where illiquidity can explain flatness as easily as considered indifference.[^49,52]

:::statement(attr="ARA Research")
The offboarding argument is the most satisfying thing OpenAI can say and the least useful thing it can prove.
:::

**A methodological disclosure, not a finding:** this article's three load-bearing claims — that OpenAI published rather than filed, that Apple's own declaration concedes the deprovisioning failure, and that the Ninth Circuit treats confidentiality provisions as sufficient measures — were each subjected to a deliberate attempt to falsify them against independent sources, and no contradicting source was located. What did not survive that process was the framing this article started from. OpenAI published rather than filed; the exhibits are iMessages rather than institutional correspondence; and the element they attack is one the Ninth Circuit has said confidentiality provisions alone suffice to defend.[^8] The genuinely damaging facts — a two-day sign-in block against 95 days of live cloud access, 240 downloads across five sessions, a deprovisioning script that silently failed, and three missing timestamps — all come from Apple's own declarations. That is the article's central claim and also its main vulnerability: it rests on a filing record 25 days old, in a case where the defendants have not yet said a word under oath. The first real test arrives on 17 August, and the first ruling on 1 October.

:::references
- {id: 1, title: "Apple is getting this wrong", url: "https://openai.com/index/apple-is-getting-this-wrong/", source: OpenAI, date: "2026-08-03"}
- {id: 2, title: "Docket, Apple Inc. v. Liu, No. 5:26-cv-07078 (N.D. Cal.)", url: "https://www.courtlistener.com/docket/73602437/apple-inc-v-liu/", source: "CourtListener / RECAP", date: "2026-08-04"}
- {id: 3, title: "OpenAI rebuts Apple trade secrets allegations in new response with receipts", url: "https://9to5mac.com/2026/08/03/openai-rebuts-apple-trade-secrets-allegations-in-new-response-and-evidence/", source: 9to5Mac, date: "2026-08-03"}
- {id: 4, title: "Apple sues OpenAI alleging trade secret theft, says scheme was 'at every level'", url: "https://www.cnbc.com/2026/07/10/apple-openai-lawsuit-trade-secrets.html", source: CNBC, date: "2026-07-10"}
- {id: 5, title: "Declaration of Roffman in support of motion for preliminary injunction (Dkt. 45)", url: "https://storage.courtlistener.com/recap/gov.uscourts.cand.474095/gov.uscourts.cand.474095.45.0.pdf", source: "N.D. Cal. via RECAP", date: "2026-08-03"}
- {id: 6, title: "Rockwell Graphic Systems, Inc. v. DEV Industries, Inc., 925 F.2d 174 (7th Cir. 1991)", url: "https://law.resource.org/pub/us/case/reporter/F2/925/925.F2d.174.90-1499.html", source: "public.resource.org", date: "1991-02-11"}
- {id: 7, title: "Learning Curve Toys, Inc. v. PlayWood Toys, Inc., 342 F.3d 714 (7th Cir. 2003)", url: "https://law.resource.org/pub/us/case/reporter/F3/342/342.F3d.714.02-1916.html", source: "public.resource.org", date: "2003-08-18"}
- {id: 8, title: "InteliClear, LLC v. ETC Global Holdings, Inc., 978 F.3d 653 (9th Cir. 2020)", url: "https://cdn.ca9.uscourts.gov/datastore/opinions/2020/10/15/19-55862.pdf", source: "U.S. Court of Appeals, Ninth Circuit", date: "2020-10-15"}
- {id: 9, title: "18 U.S.C. § 1836 — Civil proceedings", url: "https://www.law.cornell.edu/uscode/text/18/1836", source: "Cornell Legal Information Institute"}
- {id: 10, title: "Apple Inc. v. Rivos Inc. — joint update and proposed order re settlement", url: "https://fingfx.thomsonreuters.com/gfx/legaldocs/znpnkxmnavl/APPLE%20RIVOS%20LAWSUIT%20settlement.pdf", source: "Reuters Legal Documents", date: "2024-02-09"}
- {id: 11, title: "Docket, Apple Inc. v. Rivos Inc., No. 5:22-cv-02637 (N.D. Cal.)", url: "https://www.courtlistener.com/docket/63277771/apple-inc-v-rivos-inc/", source: "CourtListener / RECAP", date: "2024-03-19"}
- {id: 12, title: "Complaint, Apple Inc. v. Liu (Dkt. 1)", url: "https://storage.courtlistener.com/recap/gov.uscourts.cand.474095/gov.uscourts.cand.474095.1.0.pdf", source: "N.D. Cal. via RECAP", date: "2026-07-10"}
- {id: 13, title: "Apple Inc.'s motion for preliminary injunction, redacted (Dkt. 38)", url: "https://storage.courtlistener.com/recap/gov.uscourts.cand.474095/gov.uscourts.cand.474095.38.0.pdf", source: "N.D. Cal. via RECAP", date: "2026-08-03"}
- {id: 14, title: "Declaration of James Pooley in support of motion for preliminary injunction (Dkt. 46)", url: "https://storage.courtlistener.com/recap/gov.uscourts.cand.474095/gov.uscourts.cand.474095.46.0.pdf", source: "N.D. Cal. via RECAP", date: "2026-08-03"}
- {id: 15, title: "18 U.S.C. § 1839 — Definitions", url: "https://www.law.cornell.edu/uscode/text/18/1839", source: "Cornell Legal Information Institute"}
- {id: 16, title: "California Civil Code §§ 3426.1, 3426.7 (Uniform Trade Secrets Act)", url: "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=3426.1", source: "California Legislative Information"}
- {id: 17, title: "E.I. duPont deNemours & Co. v. Christopher, 431 F.2d 1012 (5th Cir. 1970)", url: "https://law.justia.com/cases/federal/appellate-courts/F2/431/1012/140093/", source: Justia, date: "1970-07-20"}
- {id: 18, title: "Samuel Sherbrooke Corporate, Ltd. v. Mayer, No. 24-2173 (4th Cir. 2025)", url: "https://www.ca4.uscourts.gov/opinions/242173.P.pdf", source: "U.S. Court of Appeals, Fourth Circuit", date: "2025-11-18"}
- {id: 19, title: "Restatement (Third) of Unfair Competition (extracts), §§ 39, 43", url: "https://www.wipo.int/edocs/lexdocs/laws/en/us/us216en.pdf", source: "WIPO Lex US216", date: "1995"}
- {id: 20, title: "Yellowfin Yachts, Inc. v. Barker Boatworks, LLC, 898 F.3d 1279 (11th Cir. 2018)", url: "https://static.case.law/f3d/898/html/1279-01.html", source: "Caselaw Access Project", date: "2018-08-07"}
- {id: 21, title: "Snyder v. Beam Technologies, Inc., No. 24-1136 (10th Cir. 2025)", url: "https://www.ca10.uscourts.gov/sites/ca10/files/opinions/010111277234.pdf", source: "U.S. Court of Appeals, Tenth Circuit", date: "2025-08-05"}
- {id: 22, title: "Turret Labs USA, Inc. v. CargoSprint, LLC (2d Cir. 2022) (summary order)", url: "https://www.courtlistener.com/opinion/6449299/turret-labs-v-cargosprint/", source: CourtListener, date: "2022-03-09"}
- {id: 23, title: "Oomnitza / YouGov 2022 State of Offboarding Process Automation Report", url: "https://salestechstar.com/sales-engagement/oomnitza-survey-reveals-over-a-quarter-of-enterprises-lose-more-than-10-of-their-technology-assets-when-offboarding-workers/", source: SalesTechStar, date: "2022-11-16"}
- {id: 24, title: "Endpoint devices go missing when employees depart", url: "https://www.ciodive.com/news/endpoint-devices-employee-departure-oomnitza-saas-offboarding/636996/", source: "CIO Dive", date: "2022-11-21"}
- {id: 25, title: "OneLogin research: ex-employees retaining access to corporate applications", url: "https://www.prweb.com/releases/new_research_from_onelogin_finds_more_than_half_of_ex_employees_still_have_access_to_corporate_applications/prweb14502632.htm", source: PRWeb, date: "2017-07-13"}
- {id: 26, title: "Employee offboarding by the numbers", url: "https://www.nudgesecurity.com/post/employee-offboarding-by-the-numbers", source: "Nudge Security", date: "2023-06-14"}
- {id: 27, title: "Understanding the offboarding process in companies from an IT security perspective (USENIX SOUPS 2025)", url: "https://www.usenix.org/system/files/soups2025-detsika.pdf", source: "USENIX SOUPS", date: "2025-08-11"}
- {id: 29, title: "2026 Cost of Insider Risks Global Report", url: "https://ponemon.dtex.ai/", source: "Ponemon Institute / DTEX Systems", date: "2026-02-24"}
- {id: 30, title: "The wildest allegations in Apple's trade secrets lawsuit against OpenAI", url: "https://techcrunch.com/2026/07/13/the-wildest-allegations-in-apples-trade-secrets-lawsuit-against-openai/", source: TechCrunch, date: "2026-07-13"}
- {id: 31, title: "California Code of Civil Procedure § 2019.210", url: "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=2019.210", source: "California Legislative Information"}
- {id: 32, title: "Quintara Biosciences, Inc. v. Ruifeng Biztech, Inc., 149 F.4th 1081 (9th Cir. 2025)", url: "https://cdn.ca9.uscourts.gov/datastore/opinions/2025/08/12/23-16093.pdf", source: "U.S. Court of Appeals, Ninth Circuit", date: "2025-08-12"}
- {id: 33, title: "Judge tosses xAI claims that OpenAI stole trade secrets", url: "https://www.courthousenews.com/judge-tosses-xai-claims-that-openai-stole-trade-secrets/", source: "Courthouse News Service", date: "2026-06-15"}
- {id: 34, title: "Hooked Media Group, Inc. v. Apple Inc., 55 Cal. App. 5th 323 (2020)", url: "https://law.justia.com/cases/california/court-of-appeal/2020/h044395.html", source: Justia, date: "2020-09-30"}
- {id: 35, title: "Apple lawsuit reveals how many former employees now work at OpenAI", url: "https://9to5mac.com/2026/07/13/apple-lawsuit-reveals-how-many-former-employees-now-work-at-openai/", source: 9to5Mac, date: "2026-07-13"}
- {id: 36, title: "The DTSA turns ten: what a decade of litigation tells us", url: "https://foleyhoag.com/news-and-insights/publications/alerts-and-updates/2026/may/the-dtsa-turns-ten-what-a-decade-of-litigation-tells-us/", source: "Foley Hoag (reporting Lex Machina data)", date: "2026-05"}
- {id: 37, title: "Trade Secret Litigation Watch, February 2026", url: "https://media.crai.com/wp-content/uploads/2026/02/24150746/Trade-Secret-Lit-Watch-Feb-2026.pdf", source: "Charles River Associates", date: "2026-02-24"}
- {id: 38, title: "Lex Machina 2026 Trade Secret Litigation Report", url: "https://www.lexisnexis.com/community/pressroom/b/news/posts/lex-machina-2026-trade-secret-litigation-report-federal-trade-secret-filings-hit-an-all-time-high-in-2025", source: "LexisNexis / Lex Machina", date: "2026-01-29"}
- {id: 39, title: "Apple v. Gerard Williams III — request for dismissal", url: "https://regmedia.co.uk/2023/05/01/apple_gerald_williams_dismissal.pdf", source: "The Register (court document)", date: "2023-04-26"}
- {id: 40, title: "Docket, Apple Inc. v. Lancaster (N.D. Cal.)", url: "https://www.courtlistener.com/docket/59723605/apple-inc-v-lancaster/", source: "CourtListener / RECAP", date: "2022-11-01"}
- {id: 41, title: "Apple and Masimo trade secret lawsuit ends in mistrial", url: "https://www.macrumors.com/2023/05/01/apple-masimo-trade-secret-lawsuit-mistrial/", source: MacRumors, date: "2023-05-01"}
- {id: 42, title: "Docket, Musk v. Altman, No. 4:24-cv-04722 (N.D. Cal.)", url: "https://www.courtlistener.com/docket/69013420/musk-v-altman/", source: "CourtListener / RECAP", date: "2026-05-18"}
- {id: 43, title: "Uber and Waymo settlement statement", url: "https://www.uber.com/it/en/newsroom/uber-waymo-settlement", source: Uber, date: "2018-02-09"}
- {id: 44, title: "Sea-Land Service, Inc. v. Lozen International, LLC, 285 F.3d 808 (9th Cir. 2002)", url: "https://openjurist.org/285/f3d/808/sea-land-service-inc-v-lozen-international-llc", source: OpenJurist, date: "2002"}
- {id: 45, title: "Federal Rule of Civil Procedure 26 — Duty to disclose; general provisions governing discovery", url: "https://www.law.cornell.edu/rules/frcp/rule_26", source: "Cornell Legal Information Institute"}
- {id: 46, title: "Federal Rule of Evidence 502 — Attorney-client privilege and work product; limitations on waiver", url: "https://www.law.cornell.edu/rules/fre/rule_502", source: "Cornell Legal Information Institute"}
- {id: 47, title: "Federal Rule of Evidence 106 — Remainder of or related statements", url: "https://www.law.cornell.edu/rules/fre/rule_106", source: "Cornell Legal Information Institute"}
- {id: 48, title: "Order re motion for preliminary injunction, Epic Games, Inc. v. Apple Inc. (Dkt. 118)", url: "https://storage.courtlistener.com/recap/gov.uscourts.cand.364265/gov.uscourts.cand.364265.118.0.pdf", source: "N.D. Cal. via RECAP", date: "2020-10-09"}
- {id: 49, title: "Will OpenAI IPO by December 31, 2026?", url: "https://gamma-api.polymarket.com/events?slug=openai-ipo-by", source: "Polymarket Gamma API", date: "2026-08-04"}
- {id: 50, title: "Apple sends legal preservation letters to dozens of former employees now at OpenAI", url: "https://www.macrumors.com/2026/07/17/apple-sends-legal-letters-openai/", source: MacRumors, date: "2026-07-17"}
- {id: 51, title: "Encompass Services, PLLC v. Maser Consulting P.A., 2021 NCBC 40", url: "https://www.nccourts.gov/assets/documents/opinions/2021%20NCBC%2040.pdf", source: "North Carolina Business Court", date: "2021-06-28"}
- {id: 52, title: "Polymarket CLOB price history — OpenAI IPO by 31 December 2026", url: "https://clob.polymarket.com/prices-history", source: "Polymarket CLOB API", date: "2026-08-04"}
:::
