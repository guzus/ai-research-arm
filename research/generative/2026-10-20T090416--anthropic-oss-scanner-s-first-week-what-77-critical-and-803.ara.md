---
eyebrow: DEEP RESEARCH · OPEN-SOURCE SECURITY
title: "880 reports, not 880 vulnerabilities: what OSS Scanner's first eleven days prove"
deck: "Anthropic's free scanner sent 77 critical and 803 high model-rated findings to open-source maintainers. The count shows the pipeline works. It does not yet show how severe the bugs are, how many are distinct, or how much safer the code is."
lede: |
  On 19 October 2026, eleven days after launch, Anthropic said its OSS Scanner had "reported 77 critical and 803 high model-rated findings to maintainers" and that scanning was still under way. The post was widely shared, and its qualifier mostly was not. This report traces each number to its source and tests it against everything published about Anthropic's earlier vulnerability work: its own pilot audit and disclosure dashboard, independent audits by VulnCheck and Echo, curl's advisory and its maintainer's write-ups, and the first account from an enrolled project, Pion. The verdict is narrower than the headline. Most of these reports are probably real bugs. Their severity labels have historically run about one band high. And the stage that turns a finding into security, a fix that ships, is the one nobody has measured for the scanner yet.
domain: software
stats:
  - {label: Reports sent (model-rated), value: "880", note: "77 critical + 803 high, as of 2026-10-19"}
  - {label: Projects accepted, value: "114", note: "of ~650 that applied"}
  - {label: Pilot audit valid, value: "88%", note: "85 of 97, chosen by Anthropic"}
  - {label: Mythos "Critical" labels that held, value: "1 of 8", note: "Echo, 27 CVEs"}
  - {label: Disclosed findings patched, value: "8.4%", note: "516 of 6,157, as of 2026-10-02"}
---

:::callout(kind=info, label="Short answer")
- **What it proves:** Anthropic's pipeline can deliver at scale. It sent 880 model-generated, model-graded reports to a curated set of about 114 projects in 11 days, with scanning still incomplete [^5,6].
- **Probably true:** most of the reports are real bugs. Anthropic's pilot audit found 85 of 97 met its disclosure bar, and outside firms confirmed 92.7% of the findings they reviewed. Anthropic chose both samples [^1,9].
- **Not shown:** that the severity labels are right, that the bugs are distinct, or that anything has been fixed. Only 1 of 8 Mythos "Critical" ratings held up, 11% of the pilot findings were duplicates, and 8.4% of Anthropic's disclosed findings had been patched as of 2026-10-02 [^13,1,9].
- **The flagship curl CVE was reported 23 days before launch**, from a project that is not enrolled. It shows what the tool can do. It is not evidence about the first-week stream [^16,4].
- **What to watch:** the maintainer-confirmed rate, maintainer-assigned severity, and merged patches for scanner reports.
:::

## 01. What the 880 actually counts

The 880 figure is a vendor's count of reports sent out after about 11 days of scanning a hand-picked set of projects. Anthropic itself calls the findings "model-rated" and says the scanning is not finished. That makes 880 a measure of throughput: how many reports went out. It is not a measure of outcomes, meaning bugs confirmed, severities agreed or fixes shipped.

:::stats
- {label: Projects applied, value: "~650", note: "Shah, as of 2026-10-19"}
- {label: Projects accepted, value: "114", note: "not all scanned yet"}
- {label: Critical (model-rated), value: "77", note: "reported as of 2026-10-19"}
- {label: High (model-rated), value: "803", note: "reported as of 2026-10-19"}
:::

### Where the numbers come from

All four figures come from one X post. Punit Shah of Anthropic's Frontier Red Team posted on 2026-10-19 that "~650 projects applied", "114 accepted", and "77 critical and 803 high model-rated findings reported", with the parenthetical "we haven't scanned all projects yet" [^5]. Two hours later the @ClaudeDevs account repeated the totals: "The first scans have already reported 77 critical and 803 high model-rated findings to maintainers," adding that scanning was continuing on more projects [^6]. So the total has no fixed denominator. It covers some unstated subset of the 114 accepted projects, and it will keep growing whether or not any single report holds up [^5,6].

Three words in those posts matter more than the numbers. "Reported" means a report was sent to a maintainer. It does not mean the maintainer confirmed it. The launch post describes the reports as "fully model-generated, without human review or triage," produced by "our strongest models (including Claude Mythos)" [^1]. "Model-rated" means the Critical and High labels are the model's own judgement, applied before anyone outside Anthropic looked [^1,5]. Anthropic's launch post says so directly: "it is possible reports will be incorrect or invalid," and some maintainers have said "severity ratings can be inflated or the scanner misunderstood the project's threat model" [^1]. "First" means this is a snapshot of a pipeline that is still running [^6].

The "first week" framing is also loose. OSS Scanner launched on 2026-10-08 and the totals were posted on 2026-10-19, so the window is 11 days, not 7 [^1,5]. The extra days do not change the conclusion, but they show the gap between the framing and the record.

The qualifier also reached far fewer readers than the headline. By one rough count, the @ClaudeDevs launch-recap post drew about 610K–625K views. The post containing the words "model-rated" drew about 70K, and Shah's own post about 25K [^5,6,7]. These view counts come from a single observation and should be read as an order of magnitude, not a measurement. The recap post said the scans are "free" and "periodic", and that each finding comes with a proof of concept and, where possible, a patch [^7]. It did not repeat the caveat.

### Simple arithmetic on the totals

By our arithmetic, 880 reports across 114 accepted projects is about 7.7 per accepted project [^5]. Since not every project has been scanned, the average per scanned project is higher by an unknown amount. Critical findings are 77 of 880, or 8.75%; the other 91.25% are labelled High [^5]. No Medium or Low figures were published [^5,6]. A total that only includes the top two severity bands describes the severity filter as much as it describes the code.

### The enrollment funnel

Projects enroll by opening a pull request that adds a `projects/<name>/project.yaml` file to the `anthropics/oss-scanner` repository, which was created on launch day [^3,4]. Eligibility follows the OSS-Fuzz model: projects with "critical impact on infrastructure and user security," decided case by case [^1,2]. A GitHub snapshot taken 2026-10-20 shows how selective that has been.

:::bars
- {label: "Closed unmerged (468)", value: "55.4%", pct: 55.4}
- {label: "Still open (~233)", value: "27.6%", pct: 27.6}
- {label: "Merged (144)", value: "17.0%", pct: 17.0}
:::

The repository had 845 enrollment PRs in total. 468 were closed without merging, about 233 were still open and 144 were merged, as of 2026-10-20 [^4]. The `projects/` directory held 128 entries at that point [^4]. PRs, directories and Shah's 114 do not line up one-to-one, since one project can file more than one PR and acceptance can lag a merge. They do point the same way, though: most applicants were not admitted [^4,5]. The admitted set leans heavily toward security-mature infrastructure: cpython, openssl, openssh, nss, wolfssl, wasmtime, spidermonkey, harfbuzz and coreutils, along with web stacks such as rails, wordpress and drupal [^4]. Three projects often cited in the AI-bug-report debate are not in `projects/`: curl, PostgreSQL and the Linux kernel [^4].

So the 880 is not a sample of open source in general. It comes from projects that applied, passed a criticality screen and, in many cases, already run fuzzing and coordinated disclosure [^1,4]. Neither the per-project distribution nor the share of the 114 already scanned has been published, so a handful of large codebases could account for most of the total [^5,6].

### What would weaken this reading

The curation cuts both ways. Projects chosen for their impact on infrastructure are where a real High finding matters most. If those projects have also already been fuzzed and audited, the easy bugs are gone, and whatever the scanner still finds is more likely to be new and harder to find [^1,2]. On that reading, each report from this sample could mean more than a report from a random sample of GitHub repositories, not less. Anthropic's pre-launch pilot points the same way: in that audit, 85 of 97 critical and high findings met the bar for its coordinated disclosure process [^1]. But that pilot measured whether findings were valid, not whether their severity was right. It also cannot tell anyone which of these 880 reports are real until maintainers say so.

Why it matters: when a count of reports is read as a count of vulnerabilities, it sets public expectations, and the maintainers who receive the reports are the ones left to meet them. Every number later in this article has to be read against what the 880 actually counts.

## 02. A pipeline with no human between model and maintainer

OSS Scanner deliberately removes the human-confirmation step that Anthropic's own disclosure policy treats as the norm, and hands the job of verification to the maintainers who receive the reports. Anthropic's coordinated vulnerability disclosure (CVD) policy says: "Every report we send generally reflects a finding that a human security researcher has reviewed and confirmed." [^10] The scanner's launch post says the opposite about its own output: reports are "fully model-generated, without human review or triage" [^1]. The Cyber Mission announcement published the same day repeats it: "The reports are model-generated and sent without human review." [^8] Anthropic says the service is modeled on Google's OSS-Fuzz [^1,2]. Structurally that is the right comparison, but OSS Scanner lacks the two properties that make OSS-Fuzz's auto-filing safe to run without a human.

### What a report contains, and what it does not prove

According to Anthropic, each report comes from "our strongest models (including Claude Mythos)" and includes a self-contained reproducer, an explanation, a bisection to the introducing commit where possible, and a candidate patch when one is available [^1]. Enrollment is a pull request adding `projects/<name>/project.yaml`, which names the repository, a primary contact and a Dockerfile, with an optional threat model, PGP key and CC list [^2,3]. The image is built with network access and then scanned offline [^2,3]. Results arrive as an email bundle with tracking IDs such as ANT-2026-ABCD1234, not as GitHub private security advisories [^2]. Issue #540 asks for GHSA delivery, and Anthropic says it is aiming for that [^2,3]. The only human check in the loop happens at signup and confirms the maintainer's identity, not any finding [^2,3]. Fast-track findings carry no 90-day embargo. A 90-day clock starts only if a human later validates a finding through the standard CVD process [^2].

A reproducer is strong evidence, but it is not verification. It shows that some behavior occurs in the maintainer-supplied build. It does not show that the behavior crosses a security boundary the project cares about, that the severity label is right, or that nobody has reported the bug before. Those are the failure modes Anthropic itself names. The FAQ says that without a `threat_model.md` the scanner "will make guesses" [^2]. The launch post concedes that "it is possible reports will be incorrect or invalid" and that "some have told us severity ratings can be inflated or the scanner misunderstood the project's threat model" [^1]. The pilot audit fits that picture. Of 12 failures among 97 pentester-checked findings, 11 were real bugs that duplicated known issues or other scan findings, and only one was invalid [^1]. The reproducers settle whether a bug is real. Who checks severity, threat model and duplicates is left open.

### The OSS-Fuzz contrast

OSS-Fuzz also files bugs with no human in the loop. Its ClusterFuzz backend files them automatically and verifies fixes automatically [^36], and issues become public after the fix is released or after 90 days, whichever comes first [^37]. Google credits it with helping identify and fix over 13,000 vulnerabilities and 50,000 bugs across 1,000 projects as of May 2025 [^36]. Removing the human works there because a sanitizer-detected crash is ground truth a machine can check, and because the same machine can re-run the crash against a patched build to confirm the fix. A model finding is a claim with a reproducer attached. Nobody outside the model runs that reproducer before the report is sent [^1], and the launch materials describe no loop that re-runs it against a patch [^1,2].

| Path | Human check before sending | Ground truth | Severity source | Disclosure clock | Delivery |
|---|---|---|---|---|---|
| Anthropic standard CVD | Yes; a human researcher "reviewed and confirmed" [^10] | Human confirmation [^10] | Generally defers to maintainer [^10] | 90 days or patch; 7 days if actively exploited [^10] | Coordinated report from Anthropic [^10] |
| *OSS Scanner fast track | None on findings; identity check at signup only [^2,3] | Model-written reproducer, unchecked before sending [^1] | Model-rated [^1] | None, unless a human later validates via CVD [^2] | Email bundle; GHSA requested in issue #540 [^2,3] |
| Google OSS-Fuzz | None; bugs filed automatically [^36] | Machine-checkable crash; fixes auto-verified [^36] | Not addressed in the cited guidelines [^37] | Fix release or 90 days [^37] | Automatically filed bug [^36] |

### Chronology

:::timeline
- {date: 2026-09-15, headline: "curl UAF reported", body: "Anthropic reports the HTTP/2 upload use-after-free later assigned CVE-2026-92392, 23 days before launch [^16]."}
- {date: 2026-10-02, headline: "CVD dashboard snapshot", body: "29,439 candidates; 4,824 reports sent direct to maintainers, labeled 'May contain false positives' [^9]."}
- {date: 2026-10-08, headline: "OSS Scanner launch", body: "Opt-in service launched alongside the Cyber Mission; reports 'sent without human review' [^1,8]."}
- {date: 2026-10-13, headline: "FAQ updated", body: "FAQ revised; covers delivery, threat models and the absence of a fast-track embargo [^2]."}
- {date: 2026-10-14, headline: "curl 8.23.0", body: "Fixes CVE-2026-92392, rated High by curl [^16]."}
- {date: 2026-10-16, headline: "Pion report goes public", body: "Pion advisory published; maintainer describes 36 bugs and a day of manual triage on HN [^30,31]."}
- {date: 2026-10-19, headline: "First results", body: "77 critical and 803 high model-rated findings reported; not all projects scanned yet (as of 2026-10-19) [^5]."}
- {date: 2026-10-26, headline: "curl policy change (scheduled)", body: "curl will route LOW/MEDIUM reports to public GitHub issues, announced 2026-10-20 [^19]."}
:::

In this design, opting in is the consent mechanism. A project that files `project.yaml` agrees to receive raw model output [^2,3]. That is a meaningful safeguard, because nobody receives these reports unasked. But consent at signup is not consent to any particular report. The Pion maintainer reported that neither Claude nor Codex would help verify or triage the bundle he received, so he worked through it by hand [^30].

### The strongest counterargument

For projects that asked for everything, removing the human bottleneck is the point. Over six months Anthropic generated more than 29,000 candidate vulnerabilities and manually reviewed only about 6,000 of them [^1]. Nearly 5,000 unverified reports had already gone to maintainers who asked for all findings [^1]. By our arithmetic on those figures, human triage covered roughly a fifth of the candidates [^1]. The realistic alternative to unreviewed reports is therefore not "triaged reports". For most candidates, it is no report at all. The pilot's 85 of 97 CVD-grade findings suggests the raw stream is mostly real [^1]. This argument loses force where maintainers lack the capacity the design assumes they have, or where the scanner has to guess a project's threat model [^2].

This matters because it decides who pays the cost of verification. OSS-Fuzz pays it in compute. OSS Scanner pays it in maintainer hours.

## 03. Validity: the evidence that most reports are real

On validity the evidence is genuinely good: every externally audited sample Anthropic has published lands between roughly 88% and 93% real, but every one of those samples was chosen by Anthropic, and the much larger unreviewed stream carries Anthropic's own label, "May contain false positives" [^1,9]. Both halves of that sentence matter, and the second does not cancel the first.

### The pilot audit, read as a statistic

The core number comes from the pilot. Anthropic says outside pentesters checked "97 critical and high-severity vulnerabilities from the scanner across 48 projects", and that "85 (88%) met the bar for our CVD process" [^1]. Of the remaining 12, "11 were real but duplicated known issues or other findings from the scan, and only one was invalid" [^1].

:::donut(center-label="97 audited")
- {label: CVD-ready, value: 85}
- {label: Real but duplicate, value: 11}
- {label: Invalid, value: 1}
:::

Ninety-seven is a small sample. By ARA arithmetic on the [^1] figures, 85/97 is 87.6%, with a Wilson 95% confidence interval of about 79.6% to 92.8%. If the 880 first-week reports were a random draw from the same population, that interval implies roughly 700 to 817 CVD-grade reports (ARA arithmetic on [^1,5]). Two conditions in that sentence are doing heavy lifting. Anthropic has not disclosed how the 97 were selected [^1], and the pilot's 48 projects need not resemble the 114 accepted in October [^1,5]. The interval measures sampling noise, not selection bias.

The audit also separates two words that public coverage tends to merge. Counting duplicates, 96 of 97 findings were real bugs, but only 85 were *distinct* and new (ARA arithmetic on [^1]). The duplicate share is 11/97 = 11.3% (CI ≈ 6.4%–19.2%) by our arithmetic [^1]. That rate should not be expected to hold flat as volume grows. Some of those duplicates "duplicated... other findings from the scan" [^1], so the scanner was reporting the same root cause more than once. The more scans run against the same code, and the more other AI scanners point at the same popular projects, the higher the chance that a given true finding has already been filed. That is a structural reason the distinct-bug rate should fall as volume rises, and it is an inference from mechanism, not a measured trend. The audit also tested validity, not severity: a finding can be real and still be rated one band too high, which is Section 04's subject [^1].

### The trend across reviewed subsets

The externally reviewed numbers are consistent and slightly improving: {sparkline:90.6,90.8,92.7} from 90.6% in May to 92.7% on the October 2 dashboard [^15,13,9].

:::bars
- {label: "Late May 2026 update (1,587/1,752)", value: 90.6%, pct: 90.6}
- {label: "Echo, May data (1,726/1,900)", value: 90.8%, pct: 90.8}
- {label: "CVD dashboard, as of 2026-10-02", value: 92.7%, pct: 92.7}
- {label: "OSS Scanner pilot (85/97)", value: 87.6%, pct: 87.6}
- {label: "wolfSSL reports (72/74)", value: 97.3%, pct: 97.3}
:::

The single best maintainer datapoint is wolfSSL: "of the 74 reports we received, all but two were valid, and five became CVEs" [^1]. That is 72/74 = 97.3% valid, but only 5/74 = 6.8% CVE-worthy (ARA arithmetic on [^1]), and the gap between those two numbers is the gap between "real" and "severe." The quotes from wolfSSL, PostgreSQL, OpenSSL and HotCRP were all picked by Anthropic for its launch post [^1]. They are real testimony, but they are not a survey.

### What sits outside the reviewed set

The dashboard shows how small the checked fraction is. As of 2026-10-02 it lists 29,439 candidates, of which 6,123 were reviewed by external security firms and 5,674 confirmed valid [^9]. That is 20.8% of candidates reviewed (ARA arithmetic on [^9]). Of the 6,157 findings disclosed across 591 projects, 4,824 were "Reported direct to maintainers by Anthropic" under the heading "May contain false positives" [^9], or 78% of disclosures going out without firm triage (ARA arithmetic on [^9]). Anthropic's launch post describes the same backdrop: "over 29,000 candidate vulnerabilities", about 6,000 manually reviewed, and nearly 5,000 unverified reports sent to maintainers who asked for everything [^1].

Echo's analysis is blunt about why the reviewed rate cannot simply be projected onto the rest. As of May 22, 21,119 of 23,019 candidates "have not been reviewed by anyone outside Anthropic", and the reviewed set was probably not random, so it may show "how good the best candidates were" [^13]. OSS Scanner's first-week reports are, by design, in the unreviewed category: Anthropic describes them as "fully model-generated, without human review or triage" [^1].

:::callout(kind=info, label="What the 92.7% is and is not")
It is the confirmation rate on the ~21% of candidates that external firms reviewed, as of 2026-10-02 [^9]. It is not a measured rate for the 4,824 direct-to-maintainer reports, and not for OSS Scanner's 880 [^9,5].
:::

The capability history explains why the prior is still favorable. In February, Anthropic said Opus 4.6 "found and validated more than 500 high-severity vulnerabilities" [^12]. At the Mythos launch, contractors agreed exactly with Claude's severity in 89% of 198 manually reviewed reports [^11]. Both figures are self-reported; Echo's later outside look at the 27 Mythos findings that became CVEs found real bugs but inflated severity calls [^13].

### Counterpoint: the independent evidence agrees

The strongest argument against over-discounting comes from people Anthropic did not quote. Greg Kroah-Hartman said in March: "Something happened a month ago, and the world switched. Now we have real reports." [^43]. curl's confirmed-report rate, which had collapsed below 5% in 2025 [^21], was back to about 15–16% by April 2026, when Stenberg wrote "The slop situation is not a problem anymore" [^20]. Pion's maintainer spent a day triaging OSS Scanner output by hand and published a Critical advisory from it [^30,31]. Seth Larson's 2024 description of slop reports, which "appear at first-glance to be potentially legitimate and thus require time to refute" [^55], no longer describes the median AI report these maintainers see. Kroah-Hartman's caveat travels with the endorsement, though: "These are tiny things, they're not major things" [^43].

What would weaken the validity case is a random audit of the 4,824 untriaged reports, or of the 880, that comes in well below 80%. Nobody has published one. This matters because validity is the only one of the three claims (real, distinct, severe) the evidence actually supports: the 880 are probably mostly real bugs, and that is a smaller claim than the headline suggests.

## 04. Severity: where model ratings break

The "77 critical and 803 high" labels are the weakest part of the claim: every independent comparison we found shows Anthropic's models rating findings more severe than the maintainers who own the code, and severity is what sets a maintainer's triage order. The labels are explicitly "model-rated," and the scanner sends them out "without human review or triage" [^5,1]. Anthropic concedes the issue: "Some have told us severity ratings can be inflated or the scanner misunderstood the project's threat model" [^1]. Taking that admission seriously means treating severity as a property of a bug *in a deployment*, not of the bug alone.

### Why severity is not an intrinsic property

A use-after-free is a fact about memory. Whether it is Critical depends on who controls the input, what privileges they already hold, which build and allocator ship, and whether the vulnerable path is reachable in common configurations. Echo's analysis of Mythos findings put it this way: "Severity turns on deployment assumptions, privilege boundaries and attack preconditions" [^13]. A model reading source code in an offline Docker image sees the code but not the deployment. The scanner's own FAQ says that without a `threat_model.md` it "will make guesses" [^2,3]. Every guess about attacker position that errs toward the attacker pushes the label up.

### The independent comparisons

Echo looked at the 27 Mythos findings that became CVEs and compared Mythos's rating with the final CVSS or maintainer rating [^13]. Mythos called 8 of them Critical; "One of the eight Critical ratings held" [^13]. Fourteen of the 27 ratings disagreed, 13 of them overstated and one understated (jq) [^13]. Temporal received a Mythos Critical that maintainers scored 2.3, Low; MinIO went from Critical (model) to High (external firm) to Medium (maintainer) [^13]. The chart below shows both distributions as a percentage of the 27 CVEs.

:::stack-rows
categories: [Critical, High, Medium, Low]
rows:
  - {label: "Mythos rating (27 CVEs)", values: [29.6, 55.6, 14.8, 0]}
  - {label: "Final CVSS / maintainer", values: [3.7, 59.3, 29.6, 7.4]}
:::

VulnCheck audited Anthropic's public ledger and reached the same conclusion on a larger set. Among findings that carried both a Claude rating and a maintainer rating, Claude called 91.5% critical or high, against 51.3% for the maintainers [^14]. VulnCheck concluded that "Claude's assessment of the vulnerability severity appears to be overestimated" [^14]. By our arithmetic, maintainers kept about 0.56 of the model's critical-plus-high share [^14]. The slope chart puts both comparisons side by side.

:::slope(left-label="Model-rated", right-label="Maintainer / final", unit=%)
| Item | Model-rated | Maintainer / final |
|------|------|------|
| Critical+High, VulnCheck ledger | 91.5 | 51.3 |
| Critical+High, Echo 27 CVEs | 85.2 | 63.0 |
| Critical only, Echo 27 CVEs | 29.6 | 3.7 |
:::

Base rates make the comparison sharper. Across all 2024 NVD CVEs, 47.2% were High or Critical (13.7% Critical, 33.5% High) [^47]. curl rates its own history far lower: about 18% of its 239 CVEs are High or Critical, and only 2 are Critical (our tally, medium confidence) [^26]. Of 73 confirmed bounty CVEs through 2024, 3 were High and none Critical, and Stenberg wrote that researchers rate problems "several degrees worse" than the curl team does [^29]. A scanner that labels nine in ten findings critical or high is well above every human baseline we have.

:::rank-list
- {label: "Claude-rated findings (VulnCheck)", value: 91.5%, pct: 91.5, highlight: true}
- {label: "Same findings, maintainer-rated", value: 51.3%, pct: 51.3}
- {label: "NVD 2024, all CVEs", value: 47.2%, pct: 47.2}
- {label: "curl historical self-rating", value: "~18%", pct: 18}
:::

### Anthropic's agreement number measures something else

Anthropic's CVD dashboard reports, as of 2026-10-02, "83.0% exact agreement, 97.1% within one band" between Claude and external security firms over 1,337 findings [^9]. At the Mythos launch the figure was 89% exact on 198 reviewed reports, with 98% within one level [^11]. Two caveats apply. First, exact agreement fell from 89% to 83% as the sample grew [^11,9]. Second, the comparison is with firms Anthropic hires, not with the maintainers who make the final call [^9]. The MinIO case shows those can be different steps of a downgrade [^13]. Agreement between two outside readers of the same code says little about what someone who knows the deployment would rate.

The rubrics also differ. curl rejects CVSS outright, saying "We believe CVSS is a broken system" [^27], and published "CVSS is dead to us" after CISA scored CVE-2024-11053 a 9.1 Critical that curl rated Low [^28]. curl's own scale reserves Critical for flaws easily exploited by a remote unauthenticated attacker to run code in common setups, and defines High as serious, real-world impact that is not hard to trigger [^27]. A model trained on CVSS-style reasoning is scoring against a different question than curl asks.

### Counterpoint: humans disagree too, and over-rating is the safe error

Severity disagreement is common among humans. In 2023, 56% of roughly 25,000 dual-scored CVEs had conflicting NVD and vendor scores [^46], and a 2026 study found divergence across 288 CNAs "widespread, not uniform" [^56]. LLMs are measurably noisy at the same task, with mean per-element CVSS accuracy of 0.738 and at most 0.48 on Privileges Required, the field that encodes attacker position [^48]. The 97.1% within-one-band figure also shows the model is rarely far off [^9]. For a defender, over-rating is the conservative error, because it costs triage time but does not hide a bug. What would weaken our thesis is maintainer-side data showing the first-week ratings hold up better than the Mythos-era samples did.

:::callout(kind=warn, label="Why it matters")
Even a conservative error has a cost when it is applied 880 times. Only about 6% of published CVEs are ever seen exploited [^50], and CISA's KEV catalog lists 1,748 entries as of 2026-10-20 [^49]. Inflated labels push real but low-risk bugs to the top of the queue for maintainers whose time is the scarce resource. The headline count is a count of model opinions about severity, and the evidence so far suggests those opinions run about one band high.
:::

## 05. The curl exemplar, read closely

The curl use-after-free is the strongest single data point in Anthropic's favour, and it holds up: the bug is real, serious by curl's unusually strict standards, and well reported. But it was reported 23 days before OSS Scanner launched, curl is not an enrolled project, and curl rated it High rather than Critical. It shows what the tool can do. It tells us nothing direct about the quality of the 880 first-week reports.

### What the advisory says

:::kv
- {term: CVE, def: "CVE-2026-92392 [^16]"}
- {term: Title / class, def: "HTTP/2 upload Use-After-Free; CWE-416 [^16]"}
- {term: Affected versions, def: "curl 8.12.0 through 8.22.0 [^16]"}
- {term: Fixed in, def: "curl 8.23.0, released 2026-10-14 [^16]"}
- {term: Reported, def: "2026-09-15 [^16]"}
- {term: Published, def: "2026-10-14 [^16,17]"}
- {term: Credit line, def: "\"Reported-by: Luna with Claude, Anthropic\"; patch by Stefan Eissing [^16]"}
- {term: curl severity, def: "High (not Critical) [^16]"}
:::

The trigger is a malicious server that sends an HTTP/2 RST_STREAM frame (with HTTP_1_1_REQUIRED or REFUSED_STREAM) while curl is uploading [^16]. Lead developer Daniel Stenberg wrote that the issue was "found and reported by Luna Tong at Anthropic using their new OSS Scanner", that "the report and the reproducible are awesome", and that it is "one of the worst vulnerabilities in curl in a long time" [^17]. The project shortened its release cycle to six weeks [^17,16]. Stenberg has a long record of public criticism of AI-generated "slop" reports [^22], so this praise counts for something.

His own write-up also puts limits on the exploit. Getting from the use-after-free to code execution needs the exact build, architecture, allocator and heap layout, plus an upload of about 135 KB, after which the attacker gets a command of roughly 23 bytes [^17]. He sums it up himself:

:::quote(attr="Daniel Stenberg, curl lead developer, 2026-10-14")
The most likely outcome of an attempted attack is rather just a crash.
:::

That sentence is the reason for the severity label [^17]. curl's rubric reserves Critical for flaws that a remote, unauthenticated attacker can easily exploit to run code in common setups; High means serious real-world impact that is not hard to trigger [^27]. A heap-layout-dependent RCE meets the second definition and misses the first. The project does not hand out High lightly either. Before October 2026, curl's most recent High CVE dated from October 2023 [^18], and by our tally of its security table only about 18% of its 239 CVEs are High or Critical (41 High, 2 Critical) [^26]. Its bug-bounty history shows the same habit: of 73 confirmed bounty CVEs up to 2024, three were High and none Critical, and Stenberg says researchers tend to rate problems "several degrees worse" than the curl team does [^29].

### Why it is not first-week evidence

The date settles this. The bug was reported on 2026-09-15 [^16], and OSS Scanner launched on 2026-10-08 [^1]. By our arithmetic that is 23 days earlier. In a follow-up post in his thread, Punit Shah describes the curl find as the work of "an early version of OSS Scanner" [^57]. curl also has no directory in the enrollment repository's `projects/` tree as of the 2026-10-20 snapshot [^4]. So the flagship example came from a pre-launch run against a project that never went through the opt-in funnel. It is not one of the 77 Critical and 803 High reports [^5,6], and it carries curl's severity rating, not the model's.

Anthropic is also a small presence in curl's recent CVE record:

:::rank-list
- {label: Aisle Research, value: "24 CVEs", pct: 100}
- {label: Other finders, value: "7 CVEs", pct: 29}
- {label: Anthropic, value: "2 CVEs (1 High, 1 Low)", pct: 8.3, highlight: true}
:::

Those 33 CVEs make up curl's September–October 2026 release batches [^25]. Anthropic's two, CVE-2026-92392 and one Low, come to about 6% by our arithmetic [^25]. Aisle, by Stenberg's account, "has found more CVEs in curl than any other group or individual ever did before", with 35 in the past year [^24]. In curl, AI-assisted discovery is a crowded field, and Anthropic is not leading it on volume.

### A verdict that moved with the evidence

Stenberg's view has changed with the evidence. In May 2026, reviewing a Mythos scan of curl run by a third party, he found that five "confirmed" vulnerabilities came down to one Low CVE: three were false positives and one was "just a bug". He called the exercise "An amazingly successful marketing stunt" [^23]. Five months later he called an Anthropic report awesome [^17]. Both judgments came from the same person using the same rubric [^27], which makes them a fair natural experiment: when the reports improved, his assessment improved too.

On oss-security the case has already become a proxy fight. Peter Gutmann, writing satirically, complained of "more and more obscure issues that require extraordinary combinations of circumstances to trigger" and said this CVE "required among other things at least three planets to be lined up right" [^32]. David A. Wheeler answered that "AI is *EXTREMELY* good at patiently crafting and chaining a sequence of defects" and pointed projects to Anthropic's scanner [^33]. Readers should also know that Anthropic funds part of the ecosystem making this case: $2.5M of its Glasswing donations went to Alpha-Omega/OpenSSF through the Linux Foundation [^52]. That does not make Wheeler's argument wrong, but the broader endorsement is not entirely neutral. Both men are partly right. Gutmann is right about the preconditions [^17], and Wheeler is right that a careful chain of defects is exactly what the exploit sketch shows [^17,33].

### What would weaken this reading

The best counterargument is that curl is one of the hardest targets in open source. Aisle alone produced 35 CVEs there in a year [^24], the project ran a paid bounty that confirmed 87 vulnerabilities before it closed [^21], and a fresh High in such a heavily audited codebase is a real signal of capability [^18,17]. If the enrolled projects get reports of similar quality, the 880 will look better than our framing suggests. But that is a forecast about the first-week stream, and the curl case cannot test it.

Why it matters: curl is the best-documented find credited to OSS Scanner [^16,17], so readers will naturally use it to interpret the 880 [^5,6]. The evidence supports carrying its quality over as a claim about capability, not about the first-week stream.

## 06. The cost lands on the receiving end

OSS Scanner makes discovery free for maintainers, but it does not make triage free, and the first independent first-week account plus curl's policy change the same month both suggest the receiving side is the constraint.

### One project's first week

Pion's maintainer posted the first independent account of an enrolled project's first week[^30]. About a week after enrolling, its maintainer received "a report with 36 bugs, including 6 security vulnerabilities: 2 critical, 3 high, and 1 moderate," some of them more than four years old[^30]. One resulting pion/dtls advisory is rated Critical at CVSS 9.1 and credits "Anthropic's OSS Scanner"[^31]. That counts as a success for the scanner: real bugs that had sat unnoticed for years.

The cost side is the part to notice. The maintainer reviewed the bundle manually "one by one" and spent the whole day on it, because "Both Claude and Codex refused to help verify, triage, or develop proof-of-concept reproductions"[^30]. A comparison run on GLM 5.3 found mostly panics and none of the CVEs[^30]. So a model found the bugs, and the same vendors' assistants would not help the person on the other end sort through them.

:::kv
- {term: Project, def: "pion/dtls (Pion WebRTC)"}
- {term: Time from enrollment, def: "~1 week"}
- {term: Bugs reported, def: "36"}
- {term: Security vulnerabilities, def: "6 (2 critical, 3 high, 1 moderate)"}
- {term: Oldest bug, def: ">4 years"}
- {term: Triage, def: "Manual, one full day"}
- {term: Model help, def: "Claude and Codex refused"}
:::

### curl: volume, quality, and a new policy

curl is not enrolled in OSS Scanner[^4], but it is the best-instrumented receiving end in open source. In May 2026 Daniel Stenberg wrote that the report rate was "4-5 times higher than it was in 2024 and double the speed of 2025"[^18]. Quality had already recovered by April. "The slop situation is not a problem anymore," he wrote, with the confirmed rate back to about 15–16%[^20]. The chart below tracks that rate. The 2025 point is an upper bound ("below 5%"), and the April 2026 point is the midpoint of the stated 15–16% range[^29,21,20].

:::line-chart(title="curl: share of security reports confirmed", subtitle="Stenberg's tallies; 2025 is 'below 5%'", y-unit=%)
x: 2019–24 bounty stats,2025,Apr 2026
Confirmed: 15.4,5,15.5
:::

The rate recovered, but the load stayed high. Each report "engages 3-4 persons. Perhaps for 30 minutes, sometimes up to an hour or three. Each."[^22]. On 2026-10-20 Stenberg said that from October 26, LOW and MEDIUM reports go to public GitHub issues instead of the private security channel, since more than 90% of submissions are assessed below HIGH[^19]. The post does not name Anthropic or any scanner[^19]. Its stated reason is capacity, not quality:

:::quote(attr="Daniel Stenberg, curl, 2026-10-20")
all key maintainers feel strained, overloaded and brought to the brink of what we can muster.
:::

He added, "We must act to survive"[^19]. The project is changing its disclosure process because of volume, even though by its own account the slop problem has passed[^20].

### The same signal elsewhere

Other parts of the ecosystem report the same strain. The oss-security list now caps per-project traffic at "up to 20-something messages, but not 30+" a day, and its moderator says the churn is "still much higher than it had been 'before AI'"[^34]. Tidelift's 2024 survey found 60% of maintainers are unpaid, and that security work rose from 4% of their time in 2021 to 11%[^41]. Elastic received more than 1,390 bug-bounty reports in H1 2026, against a historical 600–850 a year, and rejected about 70% at analysis[^42]. Greg Kroah-Hartman says kernel reports are now real, but "These are tiny things, they're not major things"[^43]. The Linux Foundation's $12.5M grant announcement describes "an unprecedented influx of security findings, many of which are generated by automated systems"[^51]. In the same release Kroah-Hartman warned that "Grant funding alone is not going to help solve the problem that AI tools are causing today on open source security teams"[^51].

Projects are also building defenses into policy. Django closes "unverified AI output" without response and requires a proof of concept[^53]. The kernel's CNA assigns CVEs to every bug fix and declines to rate severity at all[^54]. Seth Larson warned in 2024 that low-quality reports "appear at first-glance to be potentially legitimate and thus require time to refute"[^55]. FFmpeg put the fairness question bluntly when Google's Big Sleep reported a bug: "is it really fair that trillion dollar corporations run AI to find security issues on people's hobby code? Then expect volunteers to fix"[^45].

### What 880 reports might cost

To give a sense of scale, apply curl's own per-report cost to the first-week total. curl's 3–4 people at 30 minutes to 3 hours each works out to 1.5–12 person-hours per report[^22]. By our arithmetic (ARA arithmetic), 880 reports would take roughly 1,300–10,600 person-hours of triage[^5,22]. This is an illustration, not a measurement. Reports that ship with a reproducer, as OSS Scanner's do[^2], should land toward the low end, and a project with a smaller team pays fewer person-hours per report but loses more of its total capacity.

### What would weaken this

Two counterpoints carry weight. First, enrollment is opt-in: each project files a pull request accepting the terms, including model-generated reports with no human review[^2,3]. A maintainer who enrolled has agreed to the cost. Second, triage itself can be automated. Elastic's triage agent agreed with human analysts 85% of the time across 764 reports, at about $2 per report[^42]. On those numbers the bottleneck looks solvable. The complication is who has that tooling. Elastic built its agent in-house[^42], while Pion, the project that most needed help, found that Claude and Codex refused to do the work[^30]. Until the vendor that generates the reports also provides, or permits, the model help to process them, the cost of triage stays with the maintainer.

This matters because the 880 figure counts output from the side of the pipeline that just became cheap. Whether those reports improve security depends on the side that did not.

## 07. Discovery is cheap; repair is the bottleneck

The number of findings that turn into fixes drops sharply at every stage after discovery, and the ecosystem's vulnerability plumbing is already saturated, so OSS Scanner should be judged on fixes shipped, not findings sent. Anthropic's own disclosure dashboard, as of 2026-10-02, shows 29,439 candidate vulnerabilities, of which 6,123 were reviewed by external security firms and 5,674 were confirmed valid [^9]. The same dashboard counts 6,157 findings reported across 591 projects, 5,103 acknowledged by maintainers, and 516 patched upstream [^9]. By our arithmetic that is 516 of 6,157, or 8.4%, as of 2026-10-02 [^9].

:::exhibit(num="Exhibit 1", title="Anthropic's disclosure funnel", subtitle="Findings, as of 2026-10-02", source="Anthropic CVD dashboard")
:::bar-chart(title="Disclosure funnel", orientation=horizontal)
categories: Candidates, Reviewed by firms, Confirmed valid, Reported to maintainers, Acknowledged, Patched upstream
Findings: 29439, 6123, 5674, 6157, 5103, 516
:::
:::

The funnel is not monotonic, and the bump is informative. More findings were reported (6,157) than were confirmed valid (5,674) because 4,824 reports went "direct to maintainers by Anthropic" without firm review, under a dashboard label reading "May contain false positives"; only 1,333 were reported after firm triage [^9]. By our arithmetic, 78% of disclosed findings therefore reached maintainers with no outside human check [^9]. The steep drop sits between acknowledgment and patch: maintainers accepted most reports as worth replying to, but about one in twelve had been fixed upstream by the dashboard date [^9].

### The ledger is thinner than the dashboard

An independent count shows even less repair. VulnCheck's audit of Anthropic's public ledger found 202 fixes across 113 projects, against the 421 fixes the dashboard claimed at the time [^14]. The same audit found 18 findings that were patched before Anthropic reported them [^14]. Those are rediscoveries, and a fix-rate metric credits them to the scanner although they added no security. The gap between 202 and 421 may be explained by how each side defines and dates a "fix", but it shows that even the repair numerator is contested. The discovery numerator is not.

| Program | Found / disclosed | Fixed | How "fixed" is established |
|---|---|---|---|
| AIxCC finals, synthetic vulns | 54 of 63 | 43 patched [^38] | Competition scoring harness |
| AIxCC finals, real (non-synthetic) vulns | 18 | 11 patches [^38] | Competition scoring harness |
| *Anthropic CVD dashboard (as of 2026-10-02) | 6,157 disclosed | 516 patched (8.4%) [^9] | Self-reported upstream status |
| VulnCheck ledger audit | 2,736 in ledger (of 26,153 claimed findings) | 202 fixed [^14] | Third-party check of public records |
| OSS-Fuzz (as of May 2025) | 13,000+ vulns "identify and fix" | Fixes verified automatically [^36,37] | ClusterFuzz re-runs the reproducer |

The comparison shows that conversion depends on who owns the repair loop. DARPA's AIxCC finalists found 54 of 63 synthetic vulnerabilities and patched 43, and produced 11 patches for the 18 real, non-synthetic vulnerabilities they found, at an average of about 45 minutes and roughly $152 per task [^38]. In other words, machines can now produce candidate repairs cheaply [^38]. OSS-Fuzz says it has helped "identify and fix over 13,000 vulnerabilities and 50,000 bugs across 1,000 projects" as of May 2025 [^36]. Its key design choice is that ClusterFuzz files bugs automatically and also verifies fixes automatically [^36], with disclosure at fix release or at 90 days [^37]. A fuzzer crash is a machine-checkable reproducer, so the system that found the bug can confirm when it is gone [^36]. OSS Scanner's reports also carry reproducers, but nobody outside the model checks them before they are sent, and no published loop confirms closure [^2,4].

### The downstream plumbing is already saturated

The repair stage is not the only queue under strain. CVE publication volume nearly tripled between 2020 and 2024 and has kept climbing [^39].

:::line-chart(title="CVE records published per year", subtitle="2026 is year-to-date through 2026-10-19", y-unit="")
x: 2020,2021,2022,2023,2024,2025,2026 YTD
CVEs: 14274,19862,24647,28312,39718,47803,81927
:::

By our arithmetic, 2026's 81,927 records through 2026-10-19 already exceed all of 2025 by 71% [^39]. NIST reported that submissions grew 263% from 2020 to 2025, and it moved CVEs backlogged before 2026-03-01 to a "Not Scheduled" status [^40]. In plain terms, the national enrichment database has stopped promising to analyze part of its queue [^40]. Bug-bounty data show a similar pattern for automated finders. Of XBOW's roughly 1,060 HackerOne submissions, 208 were closed as duplicates and 209 as informative, about 39% by our arithmetic, while 130 were resolved [^44]. Each of those closures cost a program owner triage time without producing a fix [^44].

The lever that addresses this is already in OSS Scanner's design. Anthropic says each report includes a reproducer, a bisection where possible, and "a candidate patch when available" [^1,2]. A ready patch moves work from the scarce side of the pipeline (maintainer repair time) to the cheap side (model compute). That makes "patches merged upstream" the metric that would show the design is working, and Anthropic has not yet published it for the scanner [^5,6].

:::callout(kind=info, label="What would weaken this")
Patch lag is normal, and a snapshot understates eventual fix rates. The dashboard mixes findings months old with findings only weeks old, and under 90-day disclosure windows many reports dated 2026-10-02 had not yet reached their deadline [^9,10]. So 8.4% is a lower bound, not a steady state [^9]. Shipping candidate patches could also give OSS Scanner better conversion than the human-reviewed program behind the dashboard, which this section cannot measure yet [^1]. If merged-patch rates for scanner reports come in well above 8.4% within a quarter, the bottleneck argument weakens.
:::

This matters because counting findings rewards the cheapest part of the pipeline. Security improves only when a fix ships, and both the funnel and the CVE queue show that shipping fixes is where capacity runs out [^9,40].

## 08. Reading the 880: what it proves, and what would prove more

Read honestly, the 880 supports "hundreds of real bugs in critical open-source code found in eleven days" and does not support "77 critical vulnerabilities"; five disclosures from Anthropic would turn the claim into a measurement. Punit Shah's own wording was "77 critical and 803 high model-rated findings", and the qualifier "model-rated" carries most of the meaning [^5].

### Three ways to read one number

The cards below are ARA arithmetic on figures from Anthropic's pilot audit [^1], Shah's post [^5], and Echo's review of the Mythos CVEs [^13]. They are not forecasts, only what the 880 would mean if one earlier rate carried over unchanged.

:::compare
- {role: LOWEST, name: "Critical labels surviving at Echo's 1-in-8 rate", value: "~10 of 77"}
- {role: HIGHEST, name: "Reports as announced", value: "880"}
- {role: SUBJECT, name: "Valid if the pilot's 87.6% held on a random draw", value: "~771"}
:::

The validity card is the stronger of the two estimates. Anthropic's pentesters found that 85 of 97 critical and high scanner findings across 48 projects met its CVD bar, with 11 of the remaining 12 real but duplicated and one invalid [^1]. By our arithmetic, that is 87.6% with a 95% interval of roughly 79.6% to 92.8%, or about 700 to 817 valid reports if you apply it to the 880 [^1,5]. Two caveats matter. The pilot sample was drawn the same way as the 880 (critical and high findings only), but Anthropic did not say how it chose the sample, so "held on a random draw" is an assumption and not a property of the data [^1]. The pilot also tested validity, not severity.

The severity card rests on far less. Echo found that "one of the eight Critical ratings held" among the 27 Mythos findings that became CVEs [^13]. Eight is a tiny sample. By our arithmetic, the 95% interval on 1-in-8 runs from about 2% to 47%, so the honest range for surviving criticals is roughly 2 to 36 of 77, not "about 10" [^5,13]. Echo's eight also came from an earlier model and passed through CVE assignment, so the card shows only the direction of the error.

Other ratios from the same evidence base, each a back-of-envelope figure and not an estimate:

- **Density.** 880 reports across 114 accepted projects is about 7.7 per project, by our arithmetic [^5]. Because not every accepted project has been scanned, the true rate per scanned project is higher by an unknown amount [^5].
- **Critical share.** 77 of 880 is 8.75% [^5]. Mythos had rated 8 of its 27 CVE'd findings Critical, about 30%, so the October batch is labeled more conservatively. That could mean a better-calibrated scanner or a different mix of projects [^13,5].
- **A severity haircut, as illustration only.** VulnCheck found Claude rated 91.5% of findings critical or high, against 51.3% for maintainers on the same findings, a ratio of about 0.56 [^14]. Applied to the 880, that ratio would suggest roughly 493 findings that maintainers would call critical or high, by our arithmetic [^14,5]. The mechanism is shaky: the 880 are critical or high by construction, so the 0.56 ratio describes a population shift, not a per-finding survival rate.
- **One project's view.** Pion's maintainer described one report of 36 bugs containing 6 security vulnerabilities, rated 2 critical, 3 high and 1 moderate [^30]. That is 5 critical or high among 36 bugs, and at least one critical was published as a CVSS 9.1 advisory [^31]. It is a single project, and its 36 bugs sit far above the 7.7 average, which hints that the 880 are concentrated [^30,5].
- **The most optimistic counter-figure.** Anthropic's dashboard reports 83.0% exact severity agreement between Claude and external firms (n=1,337) as of 2026-10-02 [^9]. Firms are not maintainers, though, and maintainers hold the deployment context that Echo found decisive [^9,13].

### What the 880 proves and does not prove

| Claim | Status | Basis |
|---|---|---|
| Throughput at scale | Proves | 880 reports to accepted projects within about 11 days [^5,6] |
| Most reports are real bugs | Likely | Pilot 85/97 valid; dashboard 92.7% of reviewed [^1,9] |
| Distinct bugs | Not shown | 11 of 97 pilot findings were duplicates [^1] |
| Severity as labeled | Not shown | 1 of 8 Mythos criticals held; 91.5% vs 51.3% [^13,14] |
| Exploitability | Not shown | Only a small share of CVEs is ever exploited [^49,50] |
| Security gained / fixes shipped | Not shown | 516 of 6,157 disclosed findings patched as of 2026-10-02 [^9] |
| Better than human researchers | Not tested | No controlled comparison published |

:::statement(attr="ARA Research")
The honest unit of OSS Scanner's value is the maintainer-confirmed fix, not the model-rated finding.
:::

### Five numbers that would settle it

Anthropic's public CVD dashboard already tracks candidates, reviews, acknowledgements, patches and identifiers [^9]. Extending it to OSS Scanner is bookkeeping, not research, and five fields would do most of the work:

1. **Maintainer-confirmed rate per report.** This replaces a 97-finding pilot, whose sampling method is undisclosed, with the full population [^1].
2. **Maintainer-assigned severity next to model severity**, broken down by band. This tests directly whether the 77 criticals are 77 or closer to Echo's 1-in-8 [^13].
3. **Distinct root causes after deduplication.** The pilot's 11% duplicate rate suggests the bug count is lower than the report count [^1].
4. **Fixes shipped and median time-to-fix.** The dashboard's 8.4% patch rate on earlier disclosures is the baseline to beat [^9].
5. **Per-project distribution.** How many of the 114 have been scanned, and what share of the 880 the top five projects hold [^5,30].

What would weaken this framing: insisting on maintainer confirmation before giving credit may be unfair. Maintainers are slow, often unpaid, and short on capacity, and a real bug exists whether or not anyone has triaged it yet [^41,19]. Missing confirmation is not evidence of invalidity, and on that reading the lowest card mostly measures a triage backlog. That objection is fair to the bugs but not to the claim. "77 critical" is a claim about severity, and a claim only becomes measured when someone other than the model has checked it.

This matters because the 880 will be quoted as a security result. Until the five numbers exist, it is a delivery result: strong evidence that the pipeline works, and weak evidence about what it has changed.

## 09. What could break this thesis

The argument so far comes down to this: the 880 measures delivery, not security. Here are the strongest reasons that reading could turn out wrong, each with what would show it.

### The model may have learned to rate more modestly

The severity case rests on samples from the Mythos and Glasswing era. Those are Echo's 27 CVEs and VulnCheck's ledger, and neither covers OSS Scanner output [^13,14]. The October batch already looks more conservative. Critical was 8.75% of the 880, against about 30% of Echo's CVE'd Mythos findings (ARA arithmetic on [^5,13]). The scanner also lets projects supply a threat model, which should cut down the guessing about deployment context [^2,3]. If maintainer-assigned severities for the first-week reports keep most of the 77 Critical labels, the main severity critique in this report fails, and the headline was closer to right than we have allowed.

### Unconfirmed is not invalid

A report that no maintainer has confirmed may simply be stuck in a triage backlog. curl's maintainers say they are "brought to the brink" [^19], and 60% of maintainers are unpaid [^41]. Every independent account we found says the 2026 generation of AI reports is mostly real: curl's confirmed rate recovered to 15–16% [^20], Greg Kroah-Hartman says "the world switched" [^43], and Pion published a Critical advisory from its bundle [^30,31]. Read this way, the low patch counts in Section 07 measure how long fixes take, not how good the findings are.

### The right comparison is with no report at all

No human team could have produced 880 serious-looking reports for critical infrastructure code in 11 days. Anthropic's own human review covered only about 6,000 of more than 29,000 candidates in six months [^1]. Pion's maintainer reported bugs that had sat in the codebase for over four years, which OpenAI's review and a GLM 5.3 pass had both missed [^30]. Even if only half of the 880 survive triage and their severities drop by a band, that is still hundreds of bugs fixed before attackers find them. Wheeler's point is that attackers now have the same patient, chaining capability [^33]. The cost of a false alarm should be weighed against the cost of a bug that nobody reports.

### Consent and selection were by design

Every enrolled project opted in through a public pull request and accepted model-generated reports without human review [^2,3]. The selection toward security-mature projects is the OSS-Fuzz eligibility model, not a flaw [^1]. If enrolled maintainers report, a quarter from now, that the reports were worth the triage time, then the cost-shifting critique applies only to projects that enrolled without the capacity to handle reports. That is a narrower complaint.

### Our own evidence is thinner than we would like

Several of our load-bearing figures come from single sources:
- The first-week totals come from two posts by Anthropic staff and accounts [^5,6].
- The 97-finding pilot and the maintainer quotes were chosen by Anthropic [^1].
- The ledger critiques come from VulnCheck and Echo, and Echo's is relayed through Help Net Security [^13,14].
- Only one enrolled project, Pion, has described its experience in public [^30].
- The view-count gap between the headline post and its qualifier is an approximate observation [^7].

A random audit of first-week reports, published by Anthropic or by maintainers, would outweigh everything here.

:::note
Red-team pass: 3/3 top claims unbroken. An adversarial reviewer tried to falsify the first-week totals, Echo's one-in-eight Critical survival figure, and the 8.4% patch rate, and found no contradicting primary or secondary source. A separate verifier marked several smaller attributions weak; those were corrected.
:::

:::references
- {id: 1, title: "Anthropic, 'Launching an opt-in vulnerability-finding service for open source' (2026-10-08)", url: "https://www.anthropic.com/research/launching-opt-in-vuln-finding-service-for-open-source", source: "anthropic.com", date: "2026-10-08"}
- {id: 2, title: "Anthropic Frontier Red Team, OSS Scanner page + FAQ (2026-10-08, FAQ upd. 2026-10-13)", url: "https://red.anthropic.com/oss-scanner", source: "red.anthropic.com", date: "2026-10-08"}
- {id: 3, title: "anthropics/oss-scanner GitHub repo README / project.yaml template", url: "https://github.com/anthropics/oss-scanner", source: "github.com"}
- {id: 4, title: "GitHub API search of anthropics/oss-scanner PRs + projects/ dir (snapshot 2026-10-20 ~08:40 UTC)", url: "https://api.github.com/search/issues?q=repo:anthropics/oss-scanner+is:pr", source: "api.github.com"}
- {id: 5, title: "Punit Shah (@thepunit, Anthropic Frontier Red Team) X post, 2026-10-19 19:38 UTC", url: "https://x.com/thepunit/status/2112267286237384738", source: "x.com"}
- {id: 6, title: "@ClaudeDevs X post (results), 2026-10-19 21:47 UTC", url: "https://x.com/ClaudeDevs/status/2112299603634860121", source: "x.com"}
- {id: 7, title: "@ClaudeDevs X post (launch recap), 2026-10-19", url: "https://x.com/ClaudeDevs/status/2112299602510749992", source: "x.com"}
- {id: 8, title: "Anthropic, 'Anthropic's Cyber Mission' (2026-10-08)", url: "https://www.anthropic.com/news/anthropic-cyber-mission", source: "anthropic.com", date: "2026-10-08"}
- {id: 9, title: "Anthropic CVD dashboard (as of 2026-10-02)", url: "https://red.anthropic.com/2026/cvd/", source: "red.anthropic.com"}
- {id: 10, title: "Anthropic Coordinated Vulnerability Disclosure policy (upd. 2026-03-06)", url: "https://www.anthropic.com/coordinated-vulnerability-disclosure", source: "anthropic.com"}
- {id: 11, title: "Anthropic, Claude Mythos Preview research post (2026-04-07)", url: "https://www.anthropic.com/research/mythos-preview", source: "anthropic.com", date: "2026-04-07"}
- {id: 12, title: "Anthropic, 'Evaluating and mitigating the growing risk of LLM-discovered 0-days' / zero-days (2026-02-05)", url: "https://www.anthropic.com/research/zero-days", source: "anthropic.com", date: "2026-02-05"}
- {id: 13, title: "Help Net Security, Echo analysis of Mythos findings (2026-09-04)", url: "https://helpnetsecurity.com/2026/09/04/echo-claude-mythos-vulnerability-findings", source: "helpnetsecurity.com", date: "2026-09-04"}
- {id: 14, title: "VulnCheck (Patrick Garrity), 'Anthropic Glasswing receipts' (2026-09-08)", url: "https://www.vulncheck.com/blog/anthropic-glasswing-receipts", source: "vulncheck.com", date: "2026-09-08"}
- {id: 15, title: "CSO Online, 'Project Glasswing has uncovered 10,000 vulnerabilities' (2026-05-25)", url: "https://www.csoonline.com/article/4176865/project-glasswing-has-uncovered-10000-vulnerabilities-anthropic.html", source: "csoonline.com", date: "2026-05-25"}
- {id: 16, title: "curl advisory CVE-2026-92392 (2026-10-14)", url: "https://curl.se/docs/CVE-2026-92392.html", source: "curl.se", date: "2026-10-14"}
- {id: 17, title: "Daniel Stenberg, 'A UAF turned RCE' (2026-10-14)", url: "https://daniel.haxx.se/blog/2026/10/14/a-uaf-turned-rce/", source: "daniel.haxx.se", date: "2026-10-14"}
- {id: 18, title: "Stenberg, 'The pressure' (2026-05-26)", url: "https://daniel.haxx.se/blog/2026/05/26/the-pressure/", source: "daniel.haxx.se", date: "2026-05-26"}
- {id: 19, title: "Stenberg, 'Do minor curl vulnerabilities in the open' (2026-10-20)", url: "https://daniel.haxx.se/blog/2026/10/20/do-minor-curl-vulnerabilities-in-the-open/", source: "daniel.haxx.se", date: "2026-10-20"}
- {id: 20, title: "Stenberg, 'High quality chaos' (2026-04-22)", url: "https://daniel.haxx.se/blog/2026/04/22/high-quality-chaos/", source: "daniel.haxx.se", date: "2026-04-22"}
- {id: 21, title: "Stenberg, 'The end of the curl bug bounty' (2026-01-26)", url: "https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/", source: "daniel.haxx.se", date: "2026-01-26"}
- {id: 22, title: "Stenberg, 'Death by a thousand slops' (2025-07-14)", url: "https://daniel.haxx.se/blog/2025/07/14/death-by-a-thousand-slops/", source: "daniel.haxx.se", date: "2025-07-14"}
- {id: 23, title: "Stenberg, 'Mythos finds a curl vulnerability' (2026-05-11)", url: "https://daniel.haxx.se/blog/2026/05/11/mythos-finds-a-curl-vulnerability/", source: "daniel.haxx.se", date: "2026-05-11"}
- {id: 24, title: "Stenberg, 'A curl audit by Aisle' (2026-10-14)", url: "https://daniel.haxx.se/blog/2026/10/14/a-curl-audit-by-aisle/", source: "daniel.haxx.se", date: "2026-10-14"}
- {id: 25, title: "curl vuln.json (2026 entries)", url: "https://curl.se/docs/vuln.json", source: "curl.se"}
- {id: 26, title: "curl security vulnerability table", url: "https://curl.se/docs/security.html", source: "curl.se"}
- {id: 27, title: "curl vulnerability disclosure policy / severity levels", url: "https://curl.se/dev/vuln-disclosure.html", source: "curl.se"}
- {id: 28, title: "Stenberg, 'CVSS is dead to us' (2025-01-23)", url: "https://daniel.haxx.se/blog/2025/01/23/cvss-is-dead-to-us/", source: "daniel.haxx.se", date: "2025-01-23"}
- {id: 29, title: "Stenberg, 'curl bug bounty stats' (2024-10-09)", url: "https://daniel.haxx.se/blog/2024/10/09/curl-bug-bounty-stats/", source: "daniel.haxx.se", date: "2024-10-09"}
- {id: 30, title: "Hacker News, 'Tell HN: Anthropic found 36 bugs (6 CVEs) in Pion, OpenAI missed them' by JoTurk (2026-10-16)", url: "https://news.ycombinator.com/item?id=50124600", source: "news.ycombinator.com", date: "2026-10-16"}
- {id: 31, title: "Pion DTLS advisory GHSA-7c2r-jhm9-43vf (2026-10-16)", url: "https://github.com/pion/dtls/security/advisories/GHSA-7c2r-jhm9-43vf", source: "github.com", date: "2026-10-16"}
- {id: 32, title: "oss-security list, Peter Gutmann (2026-10-18)", url: "https://www.openwall.com/lists/oss-security/2026/10/18/5", source: "openwall.com", date: "2026-10-18"}
- {id: 33, title: "oss-security list, David A. Wheeler (2026-10-18)", url: "https://www.openwall.com/lists/oss-security/2026/10/18/6", source: "openwall.com", date: "2026-10-18"}
- {id: 34, title: "oss-security list, Solar Designer on per-project caps (2026-10-17)", url: "https://www.openwall.com/lists/oss-security/2026/10/16/39", source: "openwall.com", date: "2026-10-17"}
- {id: 35, title: "LinuxSecurity.com coverage of OSS Scanner (2026-10-09)", url: "https://linuxsecurity.com/news/security-projects/anthropic-ai-vulnerability-scanner-open-source", source: "linuxsecurity.com", date: "2026-10-09"}
- {id: 36, title: "google/oss-fuzz README", url: "https://github.com/google/oss-fuzz", source: "github.com"}
- {id: 37, title: "OSS-Fuzz bug disclosure guidelines", url: "https://google.github.io/oss-fuzz/getting-started/bug-disclosure-guidelines/", source: "google.github.io"}
- {id: 38, title: "DARPA, AIxCC final results (Aug 2025)", url: "https://www.darpa.mil/news/2025/aixcc-results", source: "darpa.mil"}
- {id: 39, title: "CRACI, CVE publication trends (snapshot 2026-10-19)", url: "https://craci.com/resources/CVE-publication-trends", source: "craci.com"}
- {id: 40, title: "NIST, 'NIST updates NVD operations to address record CVE growth' (2026-04-15)", url: "https://www.nist.gov/news-events/news/2026/04/nist-updates-nvd-operations-address-record-cve-growth", source: "nist.gov", date: "2026-04-15"}
- {id: 41, title: "The Register on Tidelift 2024 maintainer survey (2024-09-18)", url: "https://www.theregister.com/2024/09/18/open_source_maintainers_underpaid/", source: "theregister.com", date: "2024-09-18"}
- {id: 42, title: "Elastic Security Labs, AI vulnerability triage for bug bounty (2026-08-04)", url: "https://www.elastic.co/security-labs/blog/ai-vulnerability-triage-bug-bounty-hackerone", source: "elastic.co", date: "2026-08-04"}
- {id: 43, title: "The Register, Greg Kroah-Hartman interview (2026-03-26)", url: "https://www.theregister.com/2026/03/26/greg_kroahhartman_ai_kernel/", source: "theregister.com", date: "2026-03-26"}
- {id: 44, title: "XBOW, 'Top 1: how XBOW did it' (2025-06-24)", url: "https://xbow.com/blog/top-1-how-xbow-did-it", source: "xbow.com", date: "2025-06-24"}
- {id: 45, title: "FFmpeg X post on Big Sleep report (2025-10-31)", url: "https://x.com/FFmpeg/status/1984207514389586050", source: "x.com", date: "2025-10-31"}
- {id: 46, title: "VulnCheck, CVSS accuracy issues (2023-02-02)", url: "https://www.vulncheck.com/blog/cvss-accuracy-issues", source: "vulncheck.com", date: "2023-02-02"}
- {id: 47, title: "Cybersecurity News, 2024 CVE review (Jan 2025)", url: "https://cybersecuritynews.com/2024-cve-review/", source: "cybersecuritynews.com"}
- {id: 48, title: "Marchiori et al., LLMs predicting CVSS vectors, arXiv 2504.10713 (Apr 2025)", url: "https://arxiv.org/abs/2504.10713", source: "arxiv.org"}
- {id: 49, title: "CISA Known Exploited Vulnerabilities catalog (fetched 2026-10-20)", url: "https://www.cisa.gov/known-exploited-vulnerabilities-catalog", source: "cisa.gov"}
- {id: 50, title: "Cyentia / EPSS research", url: "https://www.cyentia.com/epss/", source: "cyentia.com"}
- {id: 51, title: "Linux Foundation, $12.5M open-source security grants (2026-03-17)", url: "https://www.linuxfoundation.org/press/linux-foundation-announces-12.5-million-in-grant-funding-from-leading-organizations-to-advance-open-source-security", source: "linuxfoundation.org", date: "2026-03-17"}
- {id: 52, title: "Anthropic, Project Glasswing (2026-04-07)", url: "https://www.anthropic.com/glasswing", source: "anthropic.com", date: "2026-04-07"}
- {id: 53, title: "Django security policy (AI-assisted reports)", url: "https://docs.djangoproject.com/en/dev/internals/security/", source: "docs.djangoproject.com"}
- {id: 54, title: "Linux kernel CVE process doc", url: "https://www.kernel.org/doc/html/latest/process/cve.html", source: "kernel.org"}
- {id: 55, title: "Seth Larson, 'New era of slop security reports for open source' (2024-12-03)", url: "https://sethmlarson.dev/slop-security-reports", source: "sethmlarson.dev", date: "2024-12-03"}
- {id: 56, title: "Zhang, Massacci, Zhang, CVSS divergence across CNAs, arXiv 2607.05670 (2026-07-06)", url: "https://arxiv.org/abs/2607.05670", source: "arxiv.org", date: "2026-07-06"}
- {id: 57, title: "Punit Shah, follow-up post in OSS Scanner first-week thread (2026-10-19)", url: "https://x.com/thepunit/status/2112267290096111896", source: "x.com", date: "2026-10-19"}
:::
