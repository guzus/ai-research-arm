---
eyebrow: REPORT · AI AGENTS · COMPUTER-USE
title: "Cua's local, encrypted memory for computer-use agents: the crypto holds up, the 'first' claim doesn't quite"
deck: Computer History gives Cua Driver a way to remember what it already tried, without a screenshot or a network call. The engineering is sound. The priority claim is not — and OpenAI shipped an identically-named, oppositely-architected feature five days earlier.
lede: |
  On August 18, 2026, the open-source computer-use project Cua announced "Computer History" for Cua Driver — an encrypted, local, cross-session log of what an AI agent did on a machine, built so a new agent session can recover context a prior one already established. The standards underneath it (CBOR Sequences, COSE_Encrypt0, ChaCha20-Poly1305, HKDF, OS-native keychains) are real, current, and mostly well-matched to the problem. What doesn't hold up as cleanly is the framing: Cua's founder called it "the first open-source Computer History," open-source local action recording with optional at-rest encryption predates it by roughly three years, and OpenAI shipped a feature with the identical name — built on the opposite architecture — five days before Cua's post went up.
domain: software
stats:
  - {label: Announced, value: "Aug 18, 2026", note: "nightly channel, off by default"}
  - {label: Default retention, value: "7 days", note: "100 MiB quota"}
  - {label: GitHub stars, value: "21.7k", note: "as of Aug 20, 2026"}
  - {label: Company founded, value: "2025", note: "YC X25 batch"}
---

## 01. What Cua actually shipped

Cua is an open-source framework for letting AI agents drive real operating systems — macOS, Windows, and Linux desktops, not just browser tabs — and "Cua Driver" is the client that runs on the machine being controlled[^1]. On August 18, 2026, the project's account posted a nine-tweet thread announcing "Computer History": an early-preview, opt-in feature that gives a Cua Driver session an encrypted local record of what actions a prior session took, so a new session — or a different, compatible agent — can pick up where the last one left off instead of starting blind[^1].

The company's own framing of the problem is specific: "an agent often starts a run without knowing what a prior run did," and the usual workarounds — re-scanning screenshots, application logs, or full-disk state — are wasteful and privacy-invasive in their own right[^2]. Computer History's answer is a bounded, structured event log: timestamps, an opaque session and action identifier, a fixed capability name, an optional application bundle identifier and display name, and a fixed outcome/delivery/route/evidence/escalation category per action[^2]. It is explicitly *not* a session recorder — no screenshots, no keystrokes, no clipboard contents, no raw tool arguments, no file paths, no URLs[^2].

The feature ships only in Cua Driver's nightly channel and is off by default; turning it on is a deliberate CLI action (`cua-driver channel set nightly`, `cua-driver update --apply`, `cua-driver history enable`), and disabling, pausing, or cryptographically deleting the store are equally explicit, user-only commands[^2][^3]. That matters for how to read everything that follows: this is a preview of engineering intent, not a shipped, audited, enterprise-supported product.

:::callout(kind=warn, label=Unverified)
The thread's own headline evidence — ==unverified: "completed the task with 33.3% fewer actions" on a macOS chess-move test, versus three failed routes without history== — could not be independently corroborated anywhere beyond the original announcement thread itself; a dedicated search found no vendor documentation, blog post, or third-party writeup that restates or reproduces this specific figure. Treat it as an unverified, single-source demo claim on an unspecified sample size, not a measured effect size.
:::

## 02. The cryptography is real, current, and mostly well-matched

Cua's technical preview describes the on-disk format precisely: each event is authenticated-encrypted individually as a COSE_Encrypt0 record, sealed with ChaCha20-Poly1305, and the records are framed as a CBOR Sequence — with a CloudEvents 1.0 JSON envelope as the plaintext schema inside each encrypted payload[^2][^4]. Every named standard checks out against its own specification.

RFC 8742 defines a CBOR Sequence as nothing more than the concatenation of zero or more encoded CBOR data items, with no wrapping array required — a format designed explicitly so a sequence of values "might grow at the end by just appending further CBOR data items"[^5]. For an append-only local log that a background writer seals hourly[^2], that is close to the textbook use case.

RFC 9052 defines COSE_Encrypt0 as the structure to use "when a recipient structure is not needed because the key to be used is known implicitly" — as opposed to the heavier COSE_Encrypt, which carries a `recipients` array built for multi-party key distribution[^6]. A single-machine log with one implicit local key is exactly the case COSE_Encrypt0 was built for; reaching for the multi-recipient variant would have been the actual over-engineering.

ChaCha20-Poly1305 (RFC 8439) is a real, standards-track authenticated-encryption cipher with a 96-bit nonce, and the RFC's own security considerations are blunt about the one thing that can break it: "the most important security consideration in implementing this document is the uniqueness of the nonce used in ChaCha20"[^7]. Cua's docs describe per-chunk keys derived via HKDF (RFC 5869) — a standard, boringly-correct two-stage extract-and-expand key derivation function built for exactly this job[^8] — off a namespace root key, but the public description doesn't state whether nonces are also independently randomized or monotonic per record[^2]. That's the one open verification gap in an otherwise sound design, not a flaw in the primitives themselves.

:::kv
- {term: Framing, def: "CBOR Sequence (RFC 8742)"}
- {term: Encryption, def: "COSE_Encrypt0 + ChaCha20-Poly1305 (RFC 9052, RFC 8439)"}
- {term: Key derivation, def: "HKDF per chunk off a namespace root key (RFC 5869)"}
- {term: Key custody, def: "OS-native credential store — never on disk in the clear"}
- {term: Default retention, def: "7 days"}
- {term: Default quota, def: "100 MiB, 200 events per query"}
:::

The keys themselves never touch application-visible storage. On macOS the namespace root key lives in Keychain, where Apple's own security guide documents that "this device only" items are "always protected with the UID when being copied from the device during a backup, rendering it useless if it's restored to a different device" — the secret half of a Keychain item requires a round trip through the Secure Enclave to decrypt[^9]. On Windows, Credential Manager sits on top of DPAPI, and Microsoft's own docs are equally direct: encryption and decryption "usually must be done on the same computer," because the session key derives from the encrypting user's logon credentials — the existence of a separate DPAPI-NG extension for cross-machine scenarios is itself evidence that plain DPAPI was never designed to travel[^10][^11]. On Linux, the target is the freedesktop.org Secret Service API, jointly designed by the GNOME and KDE projects and implemented by GNOME Keyring and KWallet; its spec defines a locked state in which "the secret may not be read" until a client explicitly unlocks the collection over D-Bus, and every operation is a D-Bus method call on a live service object — there is no offline decryption path defined anywhere in the standard[^12]. Cua's claim that the Linux path "fails closed if no unlocked Secret Service is available" is therefore a correct reading of the spec's actual behavior, not an invented caveat — though it also means the Linux implementation is structurally the least reliable of the three, since headless servers, CI runners, and minimal container images routinely run no keyring daemon at all.

The one component that doesn't fit as cleanly is CloudEvents. It's a real, CNCF-graduated specification (graduated January 2024) whose entire stated purpose is "interoperability across services, platforms, and systems"[^13] — which is a strange property to reach for inside a payload that is, by construction, encrypted with a single implicit local key and never leaves the machine. RFC 9052's own rationale for COSE_Encrypt0 — a recipient structure is unneeded because the key is already known — sits awkwardly next to CloudEvents' rationale for existing at all, which is cross-system schema routing for messages multiple parties will read. A plain JSON object with the same field names, written one per line, would carry identical information with less parsing surface. It's the one place Cua's design reaches for machinery its own use case doesn't need.

## 03. What's excluded is the real design decision

The interesting engineering choice in Computer History isn't the crypto stack — it's the allowlist. Cua's schema is a strict allowlist, not a blocklist: seven event types (control, action_started, action_completed, session_started, session_ended, access, health), each carrying only timestamps, opaque session/action identifiers, a fixed capability name, an optional application bundle identifier and display name, and fixed outcome categories[^3]. Everything else — screenshots, video, audio, typed text, raw keystrokes, clipboard contents, raw tool arguments or results, accessibility trees, file paths, window titles, URLs, and free-form diagnostics — is architecturally impossible to write into the store, not merely discouraged[^2][^3].

Agents themselves get a narrower slice still: two read-only tools, `history_status` and `history_query`, each behind its own permission (`history.status`, `history.query`), because "permission for status does not imply permission to query events"[^3]. A permitted query returns at most 200 metadata events, cannot access the ciphertext or the key, and — deliberately — is not idempotent: "a successful non-empty read appends an encrypted access record," so even the agent's own act of remembering is itself logged[^3]. The RFC that specifies this considered and rejected three looser alternatives: giving agents direct encrypted-store access (too much filesystem/key-custody surface for every integrator to get right), a single umbrella `history` capability (status and query expose different privacy sensitivities and shouldn't be gated together), and model-generated summaries of history (deferred, because it "adds a model trust boundary and may require network egress")[^3].

That last rejection is worth sitting with. The single hardest constraint Cua imposed on itself — no network I/O, ever, in the capture path[^4] — rules out the most capability-rich version of this feature (an agent that can ask "summarize what I was doing yesterday" in natural language) in favor of the most privacy-preserving one (bounded metadata, locally encrypted, agent-readable only through an audited API). That's a real tradeoff, not a free lunch, and it's the correct one for a feature whose entire value proposition is that it doesn't require trusting a server.

## 04. Does "the first open-source Computer History" hold up?

Cua's founder, Francesco Bonacci, framed the announcement in a LinkedIn post the same day: "we're releasing the first open-source Computer History for Cua Driver"[^14]. Cua's own engineering documentation — the README, the technical preview, the RFC — makes no comparable priority claim anywhere; the "first" framing exists only in the marketing post, not the spec[^2][^3]. That gap is itself informative: the people who wrote the code didn't stake the claim the company's announcement did.

It also doesn't survive a look at prior art. OpenAdapt.AI, an MIT-licensed open-source project with copyright coverage dating to 2023, is explicitly "local-first": recording, compilation, and replay "run entirely on the operator machine," with raw recordings staying local by default and no required cloud round-trip[^15][^16]. It offers optional AES-256-GCM authenticated encryption at rest — but only for compiled bundles and durable checkpoints, not the raw recordings themselves, which the project's own security page states plainly "are not encrypted for you" by default[^15]. That's a real, meaningful distinction from Cua's design, where encryption is mandatory and applies to the log directly rather than to a downstream compiled artifact — but it also means "open-source, local, action-recording software with optional at-rest encryption" is not a new category. It's roughly three years old.

A wider survey of the open-source computer-use ecosystem finds nothing that combines Cua's specific configuration — mandatory encryption, local-only storage, a fixed computer-use action schema, and an agent-readable-but-key-inaccessible API — but also nothing that squarely contradicts it either. browser-use's core library has no persistent, cross-session, encrypted action-history feature; "persistent filesystem and memory" is a paid, cloud-hosted-tier bullet, not something in the open-source core[^17]. Skyvern has an action-history window and per-session debug logging, but it's Postgres-backed operational logging, not a client-side encrypted store[^39]. Agent-S (Simular AI) explicitly builds in "internal experience retrieval" from past runs, but its public documentation doesn't specify whether that experience store is local, persistent, or encrypted — an open question, not evidence either way[^40]. The cloud sandbox providers E2B and Browserbase both persist session state, but on their own servers: Browserbase's "Contexts" are "encrypted at rest"[^18], and E2B's pause/resume preserves "not only state of the sandbox's filesystem but also the sandbox's memory," kept indefinitely and managed entirely through remote API calls rather than any local file[^41] — the opposite custody model from Cua's, where the whole point is that nothing is server-side to encrypt. General-purpose agent-memory frameworks — Letta/MemGPT's tiered core/recall/archival memory[^42], mem0's vector-graph-KV hybrid store[^43] — are built for conversational and semantic memory, and while mem0 can run fully offline, neither targets a structured, timestamped, computer-use action schema the way Cua's does.

The honest version of the claim, then, is narrower than the one Cua published: not "first open-source local action history," which OpenAdapt.AI already occupies, but something closer to "first open-source, mandatory-encrypted, agent-facing action-history log purpose-built for cross-session computer-use context recovery, with a strict allowlist and a key the agent itself can never touch." That's a real, defensible, and reasonably specific claim. It's also a much smaller headline than "first."

## 05. How the incumbents actually handle this — and a naming collision

The three largest computer-use vendors solve a version of this problem, but not the same version.

Anthropic shipped computer use in public beta on October 22, 2024, as "the first frontier AI model to offer computer use in public beta," alongside an upgraded Claude 3.5 Sonnet[^19]. Its answer to state persistence has two parts that are often conflated but solve different problems. Context editing, in beta since mid-2025, clears stale tool-call results from a growing context window automatically, server-side, once a session passes 100,000 input tokens by default — that's a within-session problem, an agent running out of room to remember what it already tried in one long conversation[^20]. The memory tool, in public beta since September 29, 2025, is the cross-session piece: Claude writes and reads files under `/memories`, but "the memory tool operates client-side: Claude requests file operations, and your application executes them. You control where and how the data is stored"[^21][^22]. Client-side here means the *developer's* infrastructure, not necessarily the end user's own machine — a SaaS built on the memory tool could still centralize every user's memory files in one cloud database, which is a materially different privacy posture than Cua's device-bound design. And the memory tool's persistence is voluntary and narrative: Claude chooses what to write in prose, rather than the platform automatically appending a tamper-evident record of every action taken. Anthropic's own internal benchmark on a 100-turn agentic task found the combination cut token consumption 84% and improved task performance 39% over baseline — Anthropic's own numbers, on Anthropic's own chosen workload, not independently replicated, and not specific to computer-use tasks[^23].

OpenAI's and Google's computer-use tools are both explicitly stateless per call: the developer's own harness has to capture and resend the current screenshot every turn, chaining requests via a response or interaction ID, with no server-side persistent action log documented for either[^24][^25].

Here's the finding worth pausing on: on August 13, 2026 — five days before Cua's Computer History thread went up — OpenAI shipped a feature in the ChatGPT Mac desktop app with the *identical name*, "Computer History," replacing an earlier screenshot-based preview called Chronicle[^26]. It is architecturally close to the inverse of Cua's design. It records macOS accessibility events (clicks, typing, keyboard shortcuts, app switches) rather than screenshots, which is a genuine privacy improvement over Chronicle — but it "temporarily stores interaction events on the Mac for up to 48 hours," then those events "are processed on its servers to generate memories," and the resulting output is saved back to disk as "plain-text memory files," unencrypted, held locally until the user deletes them[^26]. Cua's Computer History never touches a network and is always encrypted at rest; OpenAI's routes through OpenAI's servers and writes its output in the clear. Two products, same name, opposite architecture, five days apart — a reader searching "computer history AI agent" in the weeks after August 2026 will find both, and conflating them would misstate what either one actually does.

:::timeline
- {date: "2024-10", headline: "Anthropic ships computer use", body: "Public beta with an upgraded Claude 3.5 Sonnet — the first frontier model with computer-use in public beta."}
- {date: "2025-01", headline: "trycua/cua repo created", body: "Public GitHub launch of the open-source computer-use framework; YC X25 batch."}
- {date: "2025-09", headline: "Anthropic ships the memory tool", body: "Client-side, developer-controlled persistent memory files for Claude, paired with context editing."}
- {date: "2026-08-13", headline: "OpenAI ships 'Computer History' (ChatGPT Mac)", body: "Replaces the Chronicle preview; local accessibility-event capture, server-side processing, unencrypted local output."}
- {date: "2026-08-18", headline: "Cua ships 'Computer History' (Cua Driver)", body: "Local-only, mandatory-encrypted, nightly-channel preview — same name as OpenAI's feature, opposite architecture."}
:::

:::callout(kind=info, label="Naming collision")
Two unrelated products named "Computer History" shipped five days apart in August 2026 — Cua's fully local and encrypted, OpenAI's cloud-touching and unencrypted at rest. Searching the term alone will not disambiguate them.
:::

The clean way to frame the four approaches side by side:

| Vendor / feature | Cross-session action history? | Storage location | Encrypted at rest | Network I/O to capture |
|---|---|---|---|---|
| Cua — Computer History | Yes, structured metadata log | Local device only | Always (COSE_Encrypt0) | *None* |
| Anthropic — memory tool | Yes, but narrative/voluntary, not an action log | Developer's infrastructure | Developer-controlled | Depends on developer's storage |
| OpenAI — Computer History (ChatGPT Mac) | Yes, accessibility-event log | Local, but round-trips through OpenAI servers | *No* — plain-text Markdown | Yes, to generate memories |
| OpenAI / Google — computer-use APIs | No; stateless per call | Developer harness | N/A | N/A |

Anthropic's memory tool + context editing combination arguably still comes closest to matching Computer History's *token-efficiency* motivation, even though it targets a different problem (within-session context growth versus cross-session recovery):

:::rank-list
- {label: "Context editing alone", value: "29%", pct: 29}
- {label: "Memory tool + context editing", value: "84%", pct: 84, highlight: true}
:::

:::source
Anthropic's own 100-turn web-search agentic benchmark; token-consumption reduction vs. an unmodified baseline. Not independently replicated, not a computer-use-specific workload.
:::

## 06. Who is actually building this

Cua is a genuinely early-stage company. It's the product of Y Combinator's Spring 2025 (X25) batch, founded by Francesco Bonacci and Alessandro Puppo as a two-to-three-person team[^27][^28]. A funding figure of roughly $500,000 circulates on startup-database aggregators, but no primary press release, SEC Form D, or company statement corroborates the amount, round type, or exact date — Crunchbase's own listing returned an access error on direct check, and this research found no dedicated TechCrunch, VentureBeat, or The Information coverage of the company at all[^29][^30]. That absence is a documented gap, not proof the funding claim is false — but it means the number should be read as unverified, not established.

:::callout(kind=warn, label=Unverified)
The ~$500K funding figure comes from a single secondary aggregator (Tracxn), not a primary source. No press release, filing, or company statement was found to corroborate it.
:::

Set against that thin corporate footprint, the open-source signal is real and organically large. The trycua/cua repository was created January 31, 2025, is MIT-licensed, and had accumulated 21,702 stars, 1,485 forks, and 679 open issues as of this writing — a live figure that will have moved by the time this article is read[^31]. Release cadence has been aggressive: over 500 tagged releases across component prefixes (agent, computer, sandbox, fleet, the Swift-based original driver and its newer cross-platform Rust port) since the first tag in May 2025, including automated nightly builds published the same day as this research[^32]. The Python package `cua-computer` was pulling roughly 435,000 PyPI downloads a month as of August 2026 — a number that, like all package-download telemetry, includes CI and mirror traffic and isn't a clean proxy for unique human users, but is nonetheless a order of magnitude beyond what GitHub stars alone would suggest[^33][^34].

Put together, the picture is neither "thin wrapper hype" nor "mature funded platform." It's a young, YC-backed, organically popular open-source project with a small team, unverified funding, no major-outlet press coverage, and a technically serious feature that is explicitly labeled preview, nightly-only, and off by default. All three of those things can be true at once, and the article's job is to hold them together rather than collapse into either "impressive traction" or "just a startup announcement."

## 07. Enterprise context: why local, encrypted action logs matter beyond one startup

The problem Computer History targets — agents that lose all context the moment a session ends — has a name in the industry conversation and some real numbers behind it. A Camunda survey of enterprises running agentic AI in 2026 found 71% of organizations already use AI agents, but only 11% of agentic AI use cases reached production in the prior year, with 84% citing business risk and 66% citing compliance concerns as reasons work stalls before deployment[^35]. That's a single vendor's survey with an obvious commercial interest in "governance is the blocker" framing, so treat the specific percentages as directional — but the shape of the finding, that trust and auditability rather than raw model capability are gating enterprise agent rollout, is consistent with why a feature like Computer History would matter commercially even in preview form.

Regulation is starting to formalize exactly this kind of logging requirement. The EU AI Act requires high-risk AI systems to "technically allow for the automatic recording of events (logs) over the lifetime of the system," and separate articles obligate deployers to retain those logs for a minimum of six months[^36][^37]. SOC 2 has no AI-specific criteria yet, so auditors are applying existing access-control (CC6) and system-operations (CC7) criteria to agent action logs in the meantime — an informal but real convergence on "agents need auditable, tamper-resistant logs" as baseline enterprise hygiene, independent of any one vendor's product decisions[^38].

Cua's specific design choice — an agent-readable, agent-unmodifiable, cryptographically sealed, locally-custodied log, where even a read leaves its own audit trail[^3] — maps onto that emerging requirement more directly than either "no logging at all" (the OpenAI/Google stateless-API default) or "logging that transits a third party's servers" (OpenAI's own ChatGPT Computer History, or any developer-hosted backend for Anthropic's memory tool). Whether that becomes a genuine competitive differentiator for Cua specifically, or gets absorbed as table-stakes design across the industry once the feature graduates out of nightly preview, is the open question — not whether the underlying need is real.

## 08. What could break this thesis

Several things could undercut the case that Computer History is a meaningfully different approach rather than a well-marketed one.

First, it may never leave preview. Nightly-channel, off-by-default features at small startups don't reliably graduate to stable, supported products — Cua would need to both keep the encryption scheme unchanged (or migrate it cleanly) and hold the "no network I/O" guarantee as the company inevitably looks for revenue, which for an open-source, VC-funded company with unverified seed-stage funding is not guaranteed.

Second, the Linux story is genuinely weaker than the macOS and Windows ones. Because Secret Service requires a live, unlocked D-Bus daemon with no offline decryption path defined anywhere in the spec[^12], any headless server, CI runner, or minimal container — exactly the environments where a lot of production computer-use automation actually runs — will have Computer History fail closed by design. That's not a bug, but it does mean the feature's real-world coverage on Linux is narrower than the "macOS, Windows, and Linux" framing in the launch thread implies[^1].

Third, no independent security review of the actual implementation exists yet. Every claim about the encryption scheme, the key-custody model, and the "cryptographic deletion" behavior comes from Cua's own documentation. The primitives are correctly named and appropriately chosen on paper — that much is verifiable against the RFCs directly — but whether the Rust and Swift implementations correctly derive unique per-record nonces, correctly implement the HKDF chunking, and correctly fail closed on every locked-keychain edge case is not something a documentation review can establish.

Fourth, and most simply: "first" claims about developer tooling rarely survive scrutiny, and this one didn't either. That doesn't diminish the engineering — COSE_Encrypt0 over ChaCha20-Poly1305 with OS-keychain key custody is a defensible, standards-correct design regardless of who did it first — but it's a reminder to read startup announcement language and startup engineering documentation as two different registers, with two different relationships to the truth.

## 09. Why this matters

The computer-use agent market spent 2024 and 2025 competing almost entirely on raw capability — can the model click the right pixel, read the right screenshot, complete the right multi-step task. Computer History, and the fact that Anthropic, OpenAI, and now Cua have all shipped some version of cross-session persistence within the same twelve months, is a signal that the next axis of competition is state: what an agent remembers, where that memory lives, who can read it, and what it costs in trust to get the benefit.

Cua's specific answer — local-only, mandatory-encrypted, agent-readable-but-key-inaccessible, zero network I/O — is the most privacy-preserving of the three architectures surveyed here, and the standards underneath it are real and mostly well-chosen. It is not, on the evidence, the first open-source project to record local agent actions, and it is not yet a shipped, audited, stable product. Both things belong in the same sentence about it. The interesting question for the next twelve months isn't whether Cua's crypto is sound — it is — but whether "local and encrypted by default" becomes the norm the rest of the computer-use agent market converges on, or stays a preview-channel feature at one well-starred, thinly-funded open-source project while the larger vendors keep routing state through their own servers.

:::references
- {id: 1, title: "Cua (@trycua) — Computer History announcement thread", url: "https://x.com/trycua/status/2089770780053643397", source: "X/Twitter", date: "2026-08-18"}
- {id: 2, title: "Computer History — technical preview", url: "https://github.com/trycua/cua/blob/main/libs/cua-driver/docs/computer-history-preview.md", source: "Cua GitHub", date: "2026-08-18"}
- {id: 3, title: "Computer History — agent integration RFC", url: "https://github.com/trycua/cua/blob/main/libs/cua-driver/docs/computer-history-agent-integration-rfc.md", source: "Cua GitHub", date: "2026-08-18"}
- {id: 4, title: "Use Computer History", url: "https://cua.ai/docs/how-to-guides/driver/use-computer-history", source: "Cua docs"}
- {id: 5, title: "RFC 8742 — CBOR Sequences", url: "https://www.rfc-editor.org/rfc/rfc8742", source: "IETF RFC Editor", date: "2020-06"}
- {id: 6, title: "RFC 9052 — CBOR Object Signing and Encryption (COSE): Structures and Process", url: "https://www.rfc-editor.org/rfc/rfc9052", source: "IETF RFC Editor", date: "2022-08"}
- {id: 7, title: "RFC 8439 — ChaCha20 and Poly1305 for IETF Protocols", url: "https://www.rfc-editor.org/rfc/rfc8439", source: "IETF RFC Editor", date: "2018-06"}
- {id: 8, title: "RFC 5869 — HMAC-based Extract-and-Expand Key Derivation Function (HKDF)", url: "https://www.rfc-editor.org/rfc/rfc5869", source: "IETF RFC Editor", date: "2010-05"}
- {id: 9, title: "Keychain data protection", url: "https://support.apple.com/guide/security/keychain-data-protection-secb0694df1a/web", source: "Apple Platform Security"}
- {id: 10, title: "CryptProtectData function (dpapi.h)", url: "https://learn.microsoft.com/en-us/windows/win32/api/dpapi/nf-dpapi-cryptprotectdata", source: "Microsoft Learn", date: "2026-05-15"}
- {id: 11, title: "DPAPI and DPAPI-NG", url: "https://learn.microsoft.com/en-us/windows/win32/seccng/cng-dpapi", source: "Microsoft Learn", date: "2023-06-06"}
- {id: 12, title: "Secret Service API — Session and Collections", url: "https://specifications.freedesktop.org/secret-service/latest/ch03.html", source: "freedesktop.org"}
- {id: 13, title: "CloudEvents specification", url: "https://github.com/cloudevents/spec", source: "CNCF CloudEvents", date: "2024-01"}
- {id: 14, title: "Introducing the first open-source Computer History for Cua Driver", url: "https://www.linkedin.com/pulse/introducing-first-open-source-computer-history-cua-driver-bonacci-iks1e", source: "LinkedIn / Francesco Bonacci", date: "2026-08-18"}
- {id: 15, title: "OpenAdapt — Security", url: "https://openadapt.ai/security", source: "OpenAdapt.AI"}
- {id: 16, title: "OpenAdaptAI/OpenAdapt", url: "https://github.com/OpenAdaptAI/OpenAdapt", source: "GitHub"}
- {id: 17, title: "browser-use/browser-use", url: "https://github.com/browser-use/browser-use", source: "GitHub"}
- {id: 18, title: "Browserbase Contexts", url: "https://docs.browserbase.com/platform/browser/core-features/contexts", source: "Browserbase docs"}
- {id: 19, title: "Claude 3.5 Sonnet and computer use", url: "https://www.anthropic.com/news/3-5-models-and-computer-use", source: "Anthropic", date: "2024-10-22"}
- {id: 20, title: "Context editing", url: "https://platform.claude.com/docs/en/build-with-claude/context-editing", source: "Anthropic docs"}
- {id: 21, title: "Memory tool", url: "https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool", source: "Anthropic docs"}
- {id: 22, title: "Effective context engineering for AI agents", url: "https://claude.com/blog/context-management", source: "Anthropic", date: "2025-09-29"}
- {id: 23, title: "Effective context engineering for AI agents (benchmark)", url: "https://claude.com/blog/context-management", source: "Anthropic", date: "2025-09-29"}
- {id: 24, title: "Computer use tool", url: "https://developers.openai.com/api/docs/guides/tools-computer-use", source: "OpenAI docs"}
- {id: 25, title: "Gemini computer use", url: "https://ai.google.dev/gemini-api/docs/interactions/computer-use", source: "Google AI docs"}
- {id: 26, title: "ChatGPT for Mac adds opt-in 'Computer History' feature, replacing Chronicle", url: "https://9to5mac.com/2026/08/13/chatgpt-for-mac-adds-opt-in-computer-history-feature-replacing-chronicle/", source: "9to5Mac", date: "2026-08-13"}
- {id: 27, title: "Cua — Y Combinator company profile", url: "https://www.ycombinator.com/companies/cua", source: "Y Combinator"}
- {id: 28, title: "Launch HN: Cua (YC X25) — Open-Source Docker Container for Computer-Use Agents", url: "https://news.ycombinator.com/item?id=43773563", source: "Hacker News", date: "2025"}
- {id: 29, title: "Cua AI — company profile", url: "https://tracxn.com/d/companies/cua-ai/__o8YYWID0aTrulrJn7F3L4KMrye__2TwaEKHVrhpDFjY", source: "Tracxn"}
- {id: 30, title: "Launch HN: Cua (YC X25)", url: "https://news.ycombinator.com/item?id=43773563", source: "Hacker News", date: "2025"}
- {id: 31, title: "trycua/cua — repository", url: "https://api.github.com/repos/trycua/cua", source: "GitHub API", date: "2026-08-20"}
- {id: 32, title: "trycua/cua — releases", url: "https://api.github.com/repos/trycua/cua/releases?per_page=100", source: "GitHub API", date: "2026-08-20"}
- {id: 33, title: "cua-computer", url: "https://pypi.org/project/cua-computer/", source: "PyPI"}
- {id: 34, title: "cua-computer download stats", url: "https://pypistats.org/api/packages/cua-computer/recent", source: "pypistats.org", date: "2026-08-20"}
- {id: 35, title: "Closing the agentic AI vision-reality gap: Camunda 2026 State of Agentic Orchestration & Automation Report", url: "https://camunda.com/blog/2026/01/closing-agentic-ai-vision-reality-gap-camunda-2026-state-of-agentic-orchestration-automation-report/", source: "Camunda", date: "2026-01-15"}
- {id: 36, title: "Article 12: Record-Keeping", url: "https://artificialintelligenceact.eu/article/12/", source: "EU AI Act"}
- {id: 37, title: "EU AI Act logging requirements", url: "https://www.helpnetsecurity.com/2026/04/16/eu-ai-act-logging-requirements/", source: "Help Net Security", date: "2026-04-16"}
- {id: 38, title: "SOC 2 compliance for AI agents", url: "https://policylayer.com/blog/soc2-compliance-ai-agents", source: "PolicyLayer"}
- {id: 39, title: "Skyvern-AI/skyvern", url: "https://github.com/Skyvern-AI/skyvern", source: "GitHub"}
- {id: 40, title: "simular-ai/Agent-S", url: "https://github.com/simular-ai/Agent-S/blob/main/README.md", source: "GitHub"}
- {id: 41, title: "Sandbox persistence", url: "https://docs.e2b.dev/sandbox/persistence", source: "E2B docs"}
- {id: 42, title: "letta-ai/letta", url: "https://github.com/letta-ai/letta", source: "GitHub"}
- {id: 43, title: "mem0ai/mem0", url: "https://github.com/mem0ai/mem0", source: "GitHub"}
:::
