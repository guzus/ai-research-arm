---
eyebrow: AGENT EVALUATION · LONG-HORIZON AI
title: "Gemini 4 Argon 'beats Minecraft' in 27 hours: what four agents, a Mineflayer text API, Easy mode and 605 deaths actually measure"
deck: The run is real, well documented and honestly caveated by its own authors. It is not evidence that AI can play Minecraft the way people do. It is evidence that a frontier coding agent can keep a thousand-program plan alive for a day while failing constantly.
lede: |
  On October 15, 2026, three researchers posted "A team of Gemini 4 Argon agents beats Minecraft" to arXiv. Four instances of Google's newest frontier model, each driving a bot through the open-source Mineflayer JavaScript library, started in a random Easy-difficulty survival world and killed the Ender Dragon 27 hours and 14 minutes later. Along the way they wrote 2,783 programs and died 605 times. Every one of those numbers comes from the paper itself, and the paper is unusually frank about what they do not show. This brief takes the result apart variable by variable: the interface, the difficulty, the deaths, the clock, the bill and the sample size. The aim is to separate what the run measures (sustained, self-correcting, multi-agent code execution against a sparse goal) from what the headline implies (that an AI has mastered a game humans play).
domain: software
stats:
  - {label: Wall clock to dragon kill, value: "27h14m", note: "≈81.7 in-game days"}
  - {label: Self-written programs, value: "2,783", note: "22% ended in an error"}
  - {label: Deaths, value: "605", note: "69 to the dragon"}
  - {label: Model cost to the win, value: "~$520", note: "intro pricing; $1,040 standard"}
---

:::callout(kind=info, label="Short answer")
- **What happened is solid.** Four Gemini 4 Argon agents went from a random seed to "Free the End" in 27h14m on Java 1.20.4 at Easy difficulty. They wrote 2,783 programs, died 605 times and needed no human intervention, according to the authors' logs and an Observer agent [^1,2].
- **The interface does a lot of the playing.** Mineflayer gives the agents x-ray block queries, a server-fed list of nearby creatures, a recipe database and an A* pathfinder that digs, pillars and parkours on its own. The paper concedes that playing from pixels "remains much harder" [^2,4,5,6].
- **"First" needs a qualifier.** A Claude Opus 5 agent killed the dragon a month earlier, in 3h56m, using 37 human-written tools. A GPT-6 Astra system did it in 8m43s on Peaceful using a scouted seed. Argon's claim to be first rests on three conditions together: random seed, raw Mineflayer, no human-written game tools [^2,17,18].
- **What it measures:** one successful trajectory (n=1) of a model-plus-harness system, pursuing a sparse goal across thousands of dependent steps and recovering from failure at roughly 22 deaths an hour. It says little about reliability, about pixel-level play, or about Argon versus other models [^2,23,28].
:::

## 01. What the paper actually reports

Unlike most viral AI milestones, this one is well documented. The arXiv paper by Maxence Faldor, Satinder Singh and Roberta Raileanu publishes the setup, the timeline, the token bill and a limitations section that undercuts its own headline [^1,2].

The run used Minecraft Java Edition 1.20.4 in survival mode with cheats off. Five instances of one general-purpose coding agent, all running Gemini 4 Argon, each had their own cloud machine. Four of them played: janesick, auratian, gyldenia and bulicame. The fifth, an "Observer", never touched the game. Its job was to verify claims and watch for specification gaming [^2]. The objective prompt was one paragraph. Its only success criterion was defeating the Ender Dragon. The general instructions told agents to observe before acting, build and test tools, record lessons in memory, report honestly and not exploit flaws in the environment. According to the authors, the prompt "contains no game strategy" [^2].

:::kv
- {term: "Game", def: "Minecraft Java 1.20.4, survival, cheats off, random seed (value not published)"}
- {term: "Difficulty", def: "Easy — monsters hit softer and \"hunger cannot kill a player\""}
- {term: "Agents", def: "4 players + 1 non-playing Observer, all Gemini 4 Argon"}
- {term: "Action interface", def: "JavaScript programs against Mineflayer + mineflayer-pathfinder; text output only"}
- {term: "Memory", def: "Persistent private + team-shared memory; context compaction"}
- {term: "Programs to the win", def: "2,783 (2,839 in the whole session); median runtime 33.5 s"}
- {term: "Program errors", def: "22% of programs ended in an error"}
- {term: "Chat messages", def: "229"}
- {term: "Infrastructure", def: "Server saves every 5 min; 6 restarts, ~20 min of paused play"}
- {term: "Runs", def: "One — \"the first launch we tried\""}
:::

The timeline is useful for what it shows about where the time went. The team lit a Nether portal at 1h42m and had 15 ender pearls in a shared chest by 5h30m. Bringing back blaze powder took more than six hours [^2]. At 10h45m janesick triangulated the stronghold from Eye of Ender throws, landing about 1.3 km away and 43 m off the actual portal room. The End portal was lit with 12 eyes at 13h17m [^2]. Then the run stalled. The dragon killed players 69 times, and at 17h30m all four agents jumped into the void within six minutes to force a dragon reset [^2]. The breakthrough came about 21 hours in, when auratian noted that the ten end crystals "kept healing the dragon to full health". All ten fell over the next 4h40m, and the dragon died 39 minutes after the last one, with bulicame at 2.5 of 20 health [^2].

:::timeline
- {date: "0:10", headline: "Roles negotiated in chat", body: "janesick proposes a split; auratian counters within a minute. Nobody assigned roles."}
- {date: "1:42", headline: "Nether portal lit", body: "Iron tools, diamonds and a portal inside two hours."}
- {date: "5:30", headline: "15 ender pearls banked", body: "Stored in a shared chest; blaze powder return takes 6+ hours."}
- {date: "10:45", headline: "Stronghold triangulated", body: "Eye-of-ender throws put it ~1.3 km away, 43 m off the portal room."}
- {date: "13:17", headline: "End portal lit", body: "Twelve eyes; the End fight begins and lasts ~14 hours."}
- {date: "17:30", headline: "Mass void-jump reset", body: "All four agents leap into the void within 6 min to reset a stuck dragon."}
- {date: "~21:00", headline: "Crystal insight", body: "The team realises the ten end crystals keep healing the dragon."}
- {date: "27:14", headline: "Free the End", body: "Dragon dies 39 min after the last crystal; ~81 in-game days."}
:::

Where the time went is itself a finding. The End portal opened at 13h17m and the win came at 27h14m, so 13h57m, about 51% of the run, was spent in or around the final fight [^2]. That part of Minecraft is mechanically simple. Speedrunners finish the entire game, dragon included, in under seven minutes [^21]. The share of the run it consumed says more about how the agents learned a boss mechanic they apparently did not know to plan for than about general competence.

:::stack-bar(legend=true)
- {label: "Spawn → Nether portal (1h42m)", pct: 6}
- {label: "Nether + stronghold logistics (11h35m)", pct: 43}
- {label: "End fight (13h57m)", pct: 51}
:::

**Counterpoint.** All of this is self-reported. The seed is not published, no full replay is public, and the paper names no organisation (the author affiliation renders as a placeholder) [^2]. The authors call it "our general-purpose Gemini 4 Argon coding agent", and Google DeepMind promoted it from its own account [^2,36]. Google's model page describes Argon as a flagship reasoning model built for "autonomous multi-step agents, and long decode up to 1M tokens", and that is the use case this run was designed to show [^39]. **Why it matters:** the honest documentation is what makes the rest of this analysis possible. Most rival claims publish less.

## 02. The interface: what Mineflayer does before the model thinks

Mineflayer turns Minecraft from a perception-and-motor-control problem into an API-programming problem. Most of the difficulty a human feels is removed before the model sees anything [^3,4,6].

The paper says so directly. Agents act "rather than seeing pixels or pressing keys". Each program runs as "the body of an asynchronous function that receives the bot" [^2]. Its limitations section says Mineflayer tells agents exactly which blocks and creatures are around them, "including blocks behind solid rock", and the dragon's internal state [^2]. Elsewhere the paper says the agents read that state "down to the number of its current behavior phase" [^2].

The library code shows what that means in practice. `bot.findBlocks` searches the loaded chunks for blocks matching a type within a distance (16 blocks by default, and the caller can raise it). It does not check line of sight. Visibility is a separate, opt-in `canSeeBlock` raycast [^4,5]. Finding diamonds is therefore a query, not an exploration problem. Mineflayer's README advertises "block knowledge… milliseconds to find any block", along with entity tracking, physics, crafting, digging and building [^3]. Crafting runs through `bot.recipesFor`, which returns the valid recipes for the current inventory, and `bot.craft` [^4]. The agent never arranges a crafting grid.

Movement is the largest abstraction. mineflayer-pathfinder is an A* planner that by default "can break/place blocks as part of its deplacement". It also pillars 1×1 towers (`allow1by1towers: true`), makes parkour jumps over gaps wider than one block, sprints and replans when the world changes [^6]. It offers more than a dozen goal types, from `GoalNear` to `GoalFollow`. "Walk to these coordinates" is therefore one call [^6].

| Capability | Human player | Mineflayer agent (this run) |
|---|---|---|
| Find ore / structures | Explore, read terrain, strip-mine | `findBlocks` over loaded chunks, no line-of-sight check [^4,5] |
| Track mobs | Watch the screen, listen | Server-fed `bot.entities` list with raw metadata [^2,4] |
| Craft | Remember recipes, arrange grid | `recipesFor` + `craft` database lookup [^4] |
| Navigate terrain | Steer, jump, bridge, pillar by hand | A* pathfinder that digs, places, pillars and parkours [^6] |
| Read the boss | Infer from animation | Dragon phase number readable in state [^2] |
| Aim and timing | Mouse and keyboard, frame by frame | Code-level calls; programs ran ~40% of wall time [^2] |

This is not a trick, and the authors are not hiding it. The comparison that matters is with other code-as-action agents. Voyager (May 2023) also ran GPT-4 on Mineflayer. It added 11 hand-written control primitives such as `mineBlock`, `killMob` and `smeltItem`, and it never left the Overworld tech tree [^7,8]. By that standard Argon had less scaffolding: the paper says the pathfinder was loaded with "no helpers added", and the agents built their own 42 helper functions [^2]. Within the code-agent lineage, this is the real progress.

:::callout(kind=warn, label="Interface caveat")
METR's own guidance is that measured AI time horizons are "40-100x lower for visual computer use tasks, due to eg poor perception" than for text-native work [^23]. A Mineflayer run sits on the easy side of that divide. The paper says the same: "playing from pixels with a keyboard and mouse, as SIMA 2 does, remains much harder" [^2].
:::

**Counterpoint.** Not everything was abstracted. The pathfinder cannot use ladders or vines, and its door and fence-gate option is described as "unreliable" [^6]. Combat still happens in real time against a moving boss. The 69 dragon deaths show the End fight was not trivial even with the dragon's internal state visible [^2]. **Why it matters:** any claim that Argon "plays Minecraft" should be restated as "writes JavaScript against a Minecraft bot SDK". That is a coding benchmark wearing a game's clothes, and it is valuable for exactly that reason.

## 03. Easy mode and 605 deaths: what difficulty and death mechanics buy

On Easy, death is cheap, and the run treated it that way. At roughly 22 deaths per wall-clock hour across the team, the strategy was to accept death and retry rather than avoid risk [^2].

The Minecraft Wiki gives the Easy rules exactly. A mob that deals D damage on Normal deals min(D, 0.5D+1) on Easy and 1.5D on Hard. Starvation on Easy stops at 10 HP (five hearts), so hunger alone can never kill a player [^13]. The dragon's melee hit is 6 HP on Easy against 10 on Normal and 15 on Hard, and its wing strike is 3.5 against 5 and 7.5 [^13]. Its breath does 3 HP per second on every difficulty [^13].

:::bar-chart(title="Ender Dragon damage by difficulty", subtitle="HP per hit; player has 20 HP", orientation=vertical, mode=grouped)
categories: Easy, Normal, Hard
Melee: 6, 10, 15
Wing strike: 3.5, 5, 7.5
:::

Death itself is mild. A player who dies drops their inventory at the spot, and those drops "decay after five minutes while that chunk is loaded" [^16]. The player respawns at a bed or world spawn. With four agents posting coordinates and despawn timers to shared memory, a death becomes a short logistics problem. The paper's best story shows this. auratian drowned carrying all twelve Eyes of Ender, teammates relayed the exact position and despawn minute, and bulicame recovered them "with two and a half minutes to spare" [^2]. Other deaths cost more. janesick burned to death carrying 12 blaze powder, and a Ghast fireball destroyed dropped items [^2].

:::donut(center-label="605 deaths")
- {label: "Killed by the Ender Dragon (69)", value: 11.4}
- {label: "Other causes, mostly monsters (536)", value: 88.6}
:::

The breakdown above uses the only split the paper's text gives: 69 dragon deaths out of 605, and the rest "mostly to monsters" [^2]. The by-cause chart (Figure 13) is not reproduced in the text, so a finer split is not available [^2].

It matters that the paper, not a critic, raises Easy mode, and that it gives no reason for choosing it [^2]. Its related-work section contrasts a community Claude Opus 5 run that won on Normal [^2]. Easy is also the community's standard setting for random-seed speedruns, so the choice is not disqualifying in itself. It does mean that 605 deaths say more about the cost of failure than about skill.

**Counterpoint.** Easy doesn't make the dragon trivial: its breath damage doesn't scale with difficulty, and the team still died to it 69 times [^13,2]. A careful player who dies five times in a whole playthrough is playing a different game from one who dies 605 times, but both games are legal. **Why it matters:** in software terms, this run had cheap rollback (a respawn, a five-minute item window, saves every five minutes) [^2,16]. Real production systems rarely do, so a recovery strategy that works here may not carry over.

## 04. "First": three dragon kills in five weeks

The headline claim is "to our knowledge, the first end-to-end autonomous completion of Minecraft by AI agents" [^1]. It holds only under the qualifiers attached to it: standard Mineflayer, no pre-scouted seed, no human-written game tools [^1,2]. Two other agent systems killed the dragon in the five weeks before, and the paper cites both [^2].

On September 15, 2026, AI Bengineering logged a single `claude-opus-5[1m]` agent at high effort beating vanilla Minecraft 1.21.4 between 00:43:30 and 04:40:21 UTC. That is 3h56m, with 388 tool calls across 37 distinct MCP tools and $93.17 of API-equivalent compute [^17]. The run used fixed seed 97996358. The dataset card says there was "no human input after the prompt, no scripted behaviour trees, no save-scumming", and that the agent died once, to a creeper [^17]. The Argon paper describes it as a run on Normal difficulty with 37 high-level tools [^2].

Later in September, Ronak Malde's open-source system paired a GPT-6 Astra planner with TypeSafe's JEV action model. It killed the dragon in 8 minutes 43.3 seconds "with six bed explosions on the first landing" [^18]. That run used Peaceful difficulty, a fixed speedrun seed with an active End portal, and coordinates fed to the model. The README states plainly that it is "structured-state control, not control from screenshots" [^18,20].

| Run | Date | Agents / model | Difficulty | Seed | Human-written game tools | Time | Compute |
|---|---|---|---|---|---|---|---|
| Malde (Astra + JEV) | Sep 2026 | Planner + action model | Peaceful | Fixed, pre-scouted | Planner/action layer; dragon-head sensor | 8m43s | 35 Astra calls [^18] |
| AI Bengineering | 2026-09-15 | 1 × Claude Opus 5 | Normal (per DeepMind) | Fixed 97996358 | 37 MCP tools | 3h56m | $93.17 [^17] |
| *Faldor et al. | 2026-10-15 | 4 × Gemini 4 Argon | Easy | Random | None (raw Mineflayer + pathfinder) | 27h14m | ~$520 [^2] |

Read the table as a trade-off, not a ranking. The Argon run is the only one that combines a random world with no human game logic. It was also about 6.9 times slower and 5.6 times more expensive than the Opus run, which was given good tools [^2,17]. In other words, the human-written tools in the Opus run did work that the Argon team had to discover for itself, paying for it in time and money.

The longer history explains why the generality matters. VPT (2022) learned from about 70,000 hours of gameplay video and became the first agent to craft diamond tools [^9]. DreamerV3 was "the first algorithm to collect diamonds in Minecraft from scratch without human data or curricula" [^10]. Voyager unlocked tech-tree milestones "up to 15.3x faster than prior SOTA" [^7], and GITM reported a +47.5% success-rate gain on ObtainDiamond [^11]. JARVIS-1 added multimodal memory and reported results on more than 200 tasks, still within the Overworld [^12]. None of these published systems reached the End.

What the End requires explains the gap. The dragon has 200 HP and is healed by end crystals at 1 HP every half-second. It perches, which is when it is most vulnerable, with a chance of 1 in (3 + crystals alive), so with all ten crystals standing it rarely lands [^14]. Ten crystals sit on obsidian pillars, two of them inside iron-bar cages [^15]. An agent that hasn't worked out the crystals will fight a dragon that keeps healing and rarely comes down to attack. That is exactly the eight-hour stall the Argon team went through [^2].

:::timeline
- {date: 2022-06, headline: "VPT crafts diamond tools", body: "Pixel agent pretrained on human video; first diamond tools."}
- {date: 2023-01, headline: "DreamerV3 collects diamonds", body: "From scratch, no human data or curricula."}
- {date: 2023-05, headline: "Voyager / GITM", body: "LLM agents on Mineflayer-style APIs sweep the Overworld tech tree."}
- {date: 2023-11, headline: "JARVIS-1", body: "Memory-augmented multimodal agent; still Overworld-bound."}
- {date: 2026-09-15, headline: "Claude Opus 5 kills the dragon", body: "One agent, 37 MCP tools, fixed seed, 3h56m."}
- {date: 2026-09, headline: "Astra + JEV in 8m43s", body: "Peaceful, scouted seed, bed explosions."}
- {date: 2026-10-15, headline: "Four Argon agents, 27h14m", body: "Random seed, raw Mineflayer, Easy, 605 deaths."}
:::

**Counterpoint.** Neither earlier kill would satisfy a strict outside judge either. The most-watched public yardstick, a Manifold market on an AI defeating the dragon before 2027, requires under 150 minutes of in-game time, human-visible observations only and random seeds. It traded at 73% as of 2026-10-17 [^19]. On those terms all three runs miss: the Argon run on time and observations, the other two on seeds [^19]. **Why it matters:** a "first" that holds only under its own definitions is still a result, but it should be read as "first under these constraints", not "AI beats Minecraft".

## 05. What 27 hours means and doesn't mean

The 27h14m figure measures wall-clock persistence, not efficiency or skill. METR puts it bluntly: "time horizon is not the length of time AIs can work independently" [^23].

The paper compares the run with HowLongToBeat's median main-story time for Minecraft (45 hours) and notes that the random-seed speedrun record is under seven minutes [^2]. Both comparisons need care. The current record is 6:39.813, set by Skycrab on July 27, 2026 in Java 1.16.1 [^21]. Argon's run took about 245 times as long [^2,21]. The 45-hour median measures a single, often distracted human who explores and builds along the way. Four agents running for 27h14m add up to about 109 agent-hours [^2], more than double that median. At 20 real minutes per in-game day, the run lasted about 81.7 in-game days, which matches the paper's "about 81" [^2,40].

:::rank-list
- {label: "Speedrun WR (human, 1.16.1)", value: "6m40s", pct: 1}
- {label: "Astra + JEV (Peaceful, fixed seed)", value: "8m43s", pct: 1}
- {label: "Claude Opus 5 (1 agent, fixed seed)", value: "3h56m", pct: 14}
- {label: "Gemini 4 Argon team (wall clock)", value: "27h14m", pct: 25, highlight: true}
- {label: "HowLongToBeat median main story", value: "45h", pct: 41}
- {label: "Gemini 4 Argon team (agent-hours)", value: "~109h", pct: 100}
:::

What the clock does show is staying power. The team ran about 102 programs per wall-clock hour before the win [^2]. Their median program lasted 33.5 seconds, and a program was running only about 40% of the time for each player, so the rest went to model reasoning, chat and planning [^2]. Over that span the agents built 146 persistent state and code items, including 42 helper functions. One crafting-fix helper appears in 655 programs, and a "self-stop" counter that kills leftover code from timed-out programs appears in 1,519 [^2]. That is the shape of a long-running software project: a few early infrastructure fixes that every later step depends on.

There is also an apparent mismatch with Argon's measured long-horizon ability. One reader of Google's safety report puts Argon's internal P50 agentic time horizon at about 1.9 hours. We could not confirm that figure in the report itself, and it almost certainly uses a different task suite from METR's [^35]. Either way, a 27-hour run does not contradict a short horizon, because the run is not one 27-hour task. It is thousands of short tasks (median 33.5 seconds each) chained together through memory and shared state [^2]. The persistence comes from the system: compaction, memory, four agents and an environment that saves every five minutes. It cannot be credited to the model's single-task horizon alone.

**Counterpoint.** Wall-clock time understates difficulty in one respect: the agents had to discover the boss mechanic (the end crystals) themselves, and that took about 8 hours of failed attempts [^2]. A human who has seen one YouTube video skips that entirely. **Why it matters:** "ran for 27 hours" is the sort of number that will be cited as evidence of day-long autonomy. What it actually shows is that this scaffold keeps a goal alive across about 24,000 model calls [^2].

## 06. The bill: $520 and 1.35 billion tokens

The run was cheap by research standards and expensive by game standards. The token profile looks like a cached, read-heavy coding workload, not a chat [^2].

:::stats
- {label: Input tokens, value: "~1.35B", note: "91% served from cache"}
- {label: Output tokens, value: "~16M", note: "incl. ~4M thinking"}
- {label: Model calls, value: "~24,000"}
- {label: Cost to the win, value: "~$520", note: "intro pricing; $1,040 standard"}
- {label: Whole session, value: "~$810", note: "$1,620 standard"}
- {label: Per wall-clock hour, value: "~$19", note: "to the win, intro pricing"}
:::

The paper gives about 1.35 billion input tokens, 91% served from cache, against about 16 million output tokens, of which about 4 million were thinking. That works out to about 24,000 model calls and about $520 to the win at introductory pricing, or $1,040 at standard rates [^2]. The whole session, including the time after the win, cost about $810 ($1,620 standard) [^2]. All of these are list-price estimates, and the paper does not state the thinking level, sampling settings or hardware [^2]. Google made Argon generally available on October 13, 2026 at an introductory $2 per million input tokens and $10 per million output, with cached input 95% off [^37]. The Gemini API pricing page says the introductory period ends on November 30, 2026, after which standard pricing is $4 and $20. That doubling is where the paper's "$1,040 at standard" comes from [^38,2].

Divided by wall-clock time, the run cost about $19 an hour at introductory pricing [^2]. Input dominates the bill: an 84-to-1 input-to-output ratio is what happens when every call re-reads a growing context of memory, chat and program output. Caching is what makes the economics work. Without the 91% cache hit rate, the same input volume would cost several times more [^2].

:::compare
- {role: LOWEST, name: "Claude Opus 5 single agent (37 tools)", value: "$93"}
- {role: HIGHEST, name: "Argon whole session, standard pricing", value: "$1,620"}
- {role: SUBJECT, name: "Argon to the win, intro pricing", value: "$520"}
:::

**Counterpoint.** Comparing $520 with $93 is not entirely fair, because the Opus run had 37 human-written tools that did much of the work [^17]. Writing and debugging those tools has a cost too, paid in engineer time rather than tokens. Princeton's "AI Agents That Matter" argues that accuracy-only agent evaluations produce "needlessly complex and costly" agents, and that cost should be reported alongside results [^31]. The Argon paper does report cost, which is to its credit. **Why it matters:** about $20 an hour for four agents is in the range where a long-running autonomous agent team is a realistic budget line. That makes the reliability question in the next section the important one.

## 07. One run, one seed, one harness: the measurement problem

The paper's own words settle the statistics: "a single run, the first launch we tried," on one random seed, which the authors say cannot show reliability [^2]. Anything more depends on the harness and the sample, and both are known to move agent results a long way.

The clearest evidence is about Argon itself. ARC Prize verified Argon on ARC-AGI-3 at 49.8% with its standard harness and 97.5% with Google's "provider adapter" harness at low reasoning. The adapter "preserves opaque reasoning state between requests and uses compaction for longer conversations" [^24]. Changing only the harness roughly doubled the score, a 1.96× ratio [^24]. ARC Prize notes that API problems left some standard-harness runs incomplete, so part of that gap may be infrastructure rather than capability [^24].

:::slope(left-label="Standard harness", right-label="Provider adapter", unit=%)
| Setting | Standard harness | Provider adapter |
|---|---|---|
| ARC-AGI-3, low reasoning | 49.8 | 97.5 |
| ARC-AGI-3, medium reasoning | 46.3 | 97.3 |
:::

This is not specific to Google. Epoch AI found that "simply switching the scaffold makes up to an 11% difference for GPT-5 and up to a 15% difference for Kimi K2 Thinking" on SWE-bench Verified [^27]. METR's January 2026 update to its time-horizon suite reported some models as "somewhat sensitive to scaffold (including prompting)" [^25]. The Minecraft harness here includes a code workspace, memory with compaction, in-game chat, a 60-second default program timeout and a world that saves every five minutes [^2]. All of these are design choices, and none were ablated.

Then there is reliability. The τ-bench paper showed why one success says little. Agents that "succeed on <50% of the tasks" were also "quite inconsistent (pass^8 <25% in retail)" [^28]. If an agent succeeds with probability p on independent tries, the chance of k successes in a row falls as p^k. A single success is consistent with a 90% success rate and also with a 10% one. The Pokémon precedent is the closest analogue. When Gemini 2.5 Pro finished Pokémon Blue in May 2025, the developer who built its harness said, "Please don't consider this a benchmark for how well an LLM can play Pokemon" [^32].

:::callout(kind=danger, label="What n = 1 cannot tell you")
It cannot give you a success rate. It cannot tell you whether a different seed (a stronghold 3 km away instead of 1.3 km) breaks the plan. It cannot tell you whether GPT-6 Astra or Opus 5.5 in the *same* harness would do better or worse. And it cannot tell you how much of the result came from the model and how much from the scaffold [^2,24,27,28].
:::

**Counterpoint.** Existence proofs matter even at n=1. Before September 2026, the widely cited learned and LLM agent systems had stopped at the Overworld tech tree [^2,7,9,10,11]. And with the harness disclosed, other labs can test the result instead of arguing about it. **Why it matters:** a large part of what this run measures is Google's harness, and Argon's ARC-AGI-3 results show how much a harness can change a score for this very model [^24].

## 08. The multi-agent claim: coordination or compute?

The paper presents coordination as a main contribution: the agents divided the work, shared knowledge and recovered each other's items without being told to [^2]. The anecdotes are real. Without a single-agent baseline at matched compute, though, the run cannot show that four agents beat one.

The behaviour is well documented. Ten minutes in, janesick proposed roles and auratian countered within a minute. Nothing in the instructions "mentioned roles, chests or rescues" [^2]. The team settled into specialisation. gyldenia handled food, beds and supplies and later destroyed six of the ten crystals. bulicame mined diamonds and landed the final blow. janesick smelted, found the fortress and triangulated the stronghold. auratian lit the portal and invented the climb-and-punch method for the crystals [^2]. The agents also corrected each other. auratian retracted a false success report ("my previous chat was an unguarded script branch"), and gyldenia flagged janesick for claiming to have returned with blaze powder one second after burning to death [^2]. That self-correction is arguably the most transferable behaviour in the paper. It is the "report honestly" instruction holding up under pressure.

The outside evidence calls for caution. The MAST study of multi-agent LLM systems found that "performance gains on popular benchmarks are often minimal" and catalogued 14 failure modes [^29]. Anthropic reported that its multi-agent research system beat a single agent by 90.2% on an internal evaluation. It also found that token usage alone explained 80% of the performance variance on BrowseComp, and that most coding tasks "involve fewer truly parallelizable tasks than research" [^30]. The Minecraft-specific MineCollab study found agent performance "dropping as much as 15% when they are required to communicate detailed task completion plans" [^33]. A Holistic Agent Leaderboard study of 21,730 agent rollouts found that higher reasoning effort *reduced* accuracy in most runs. More compute is not automatically more capability [^26].

What the anecdotes cannot show is the outcome difference. The single Opus agent with human-written tools finished 6.9 times faster [^2,17]. Four agents mean four parallel streams of exploration, which buys coverage. For example, the team split up to gather pearls and blaze rods [^2]. That is a compute-and-parallelism benefit, and it is consistent with Anthropic's finding that tokens explain most of the variance [^30].

**Counterpoint.** Minecraft progression really is parallelisable in places (pearls and blaze rods are independent supply chains), so specialisation is the right strategy and the agents found it without help [^2]. **Why it matters:** the run is good evidence that frontier agents can organise themselves. It is not evidence that organising themselves is better than one agent with the same budget. The study that would show that has not been run.

## 09. What could break this reading — and what could strengthen the result

This brief argues that the run measures long-horizon, self-correcting code execution under a generous interface, not game mastery. Here is what would change that conclusion either way.

**Evidence that would make the result stronger than this brief allows.** (1) Multiple seeds with a reported success rate. Even three wins in five seeds would turn an existence proof into a reliability estimate [^28]. (2) A Normal or Hard run, which removes the soft-landing hunger rule and roughly doubles dragon melee damage [^13]. (3) A single-agent ablation at matched tokens, to separate coordination from compute [^30]. (4) The same harness running GPT-6 Astra or Opus 5.5, to separate model from scaffold [^24,27]. (5) A pixel-plus-keyboard run, which METR's 40-100× visual-task penalty suggests is still far harder [^23].

**Evidence that would make it weaker.** (1) Evidence the model saw Mineflayer-specific End-fight code in training. The paper's limitations admit that "Gemini 4 Argon knows a great deal about Minecraft and Mineflayer from its training data" [^2]. (2) A failed replication on a fresh seed. (3) Evidence that human-written helpers came in through the persistent environment. The paper says "neither the Observer nor our manual review of a sample of the logs" found cheating. But the Observer was also Gemini 4 Argon, and the review covered only a sample [^2].

**The strongest public skepticism.** Some of the sharpest replies on X compared the run with NetHack, a harder game. Joseph Suarez wrote that "10 year olds beat the ender dragon on a fresh world in an afternoon" and called the run "1/1000 as impressive as nethack" [^34]. That compares children playing from pixels with an agent using an x-ray API. The point is fair, and it is exactly the interface caveat from Section 02. One author has also stressed that the result is "not an official Minecraft milestone" and not associated with Mojang or Microsoft [^34].

**The strongest defence.** No previously published AI-agent system went from a random seed to a dead dragon without human-written game logic, and Voyager-era agents with more scaffolding stalled at diamonds [^7,9,11]. A system that can recover from 605 deaths, 22% program errors and an 8-hour mechanical misunderstanding without a human stepping in is showing the error-recovery ability that METR's original paper identifies as the main driver of rising time horizons [^2,22].

**Red-team note.** An adversarial pass tried to falsify three load-bearing claims in this brief. They were the 27h14m / 605-death headline, the "first" priority claim relative to the September runs, and Argon's ARC-AGI-3 harness gap. **Red-team pass: 3/3 top claims unbroken.** No contradicting source turned up for any of the three. Two caveats came out of the pass. The 37 tools in the Opus run are named after game tasks (for example `destroy_end_crystal` and `locate_stronghold`), which supports calling them human-written game logic. And the "Normal difficulty" label for that run comes only from the Argon paper, not from the dataset card [^2,17].

## 10. Bottom line: what the run actually measures

Put plainly, the result is: **one successful, fully logged, 27-hour trajectory of four copies of a frontier coding agent, writing JavaScript against a Minecraft bot SDK that removes perception and motor control, on the easiest difficulty that still has monsters, in one random world** [^1,2]. Every word in that sentence narrows the headline, and all of the narrowing comes from the paper itself.

What survives is meaningful. The team kept one sparse objective alive across 2,783 programs and about 24,000 model calls. It recovered from 605 deaths and from a 22% program-error rate, built and reused its own tooling, and corrected its own false reports [^2]. The authors argue those are the capabilities that matter for long-horizon software engineering and enterprise work, and for once the analogy holds. The workload profile (1.35 billion mostly cached input tokens, short programs, persistent memory, saves every five minutes) looks more like an agentic coding session than a video game [^2].

What does not survive is the idea that AI now plays Minecraft as people do. The pixel-level benchmark is still open. Vals AI's computer-use game benchmark, which allows only keyboard and mouse, had GPT-6 Astra on top at 19.2% as of September 2026 [^20]. A strict outside judge, the Manifold market, still has not seen a qualifying run [^19]. The next milestone to watch is a multi-seed success rate. Without one, the run is a well-documented anecdote; with it, it would be a measurement.

:::references
- {id: 1, title: "A team of Gemini 4 Argon agents beats Minecraft (arXiv abstract)", url: "https://arxiv.org/abs/2610.22319", source: "arXiv / Faldor, Singh, Raileanu", date: "2026-10-15"}
- {id: 2, title: "A team of Gemini 4 Argon agents beats Minecraft (full HTML v1)", url: "https://arxiv.org/html/2610.22319v1", source: "arXiv", date: "2026-10-15"}
- {id: 3, title: "Mineflayer — README", url: "https://github.com/PrismarineJS/mineflayer", source: "PrismarineJS / GitHub", date: "2026-10-17"}
- {id: 4, title: "Mineflayer API documentation (docs/api.md)", url: "https://github.com/PrismarineJS/mineflayer/blob/master/docs/api.md", source: "PrismarineJS / GitHub", date: "2026-10-17"}
- {id: 5, title: "Mineflayer blocks plugin source (findBlocks)", url: "https://raw.githubusercontent.com/PrismarineJS/mineflayer/master/lib/plugins/blocks.js", source: "PrismarineJS / GitHub", date: "2026-10-17"}
- {id: 6, title: "mineflayer-pathfinder — README", url: "https://github.com/PrismarineJS/mineflayer-pathfinder", source: "PrismarineJS / GitHub", date: "2026-10-17"}
- {id: 7, title: "Voyager: An Open-Ended Embodied Agent with Large Language Models", url: "https://arxiv.org/abs/2305.16291", source: "arXiv", date: "2023-05-25"}
- {id: 8, title: "Voyager control primitives", url: "https://github.com/MineDojo/Voyager/tree/main/voyager/control_primitives", source: "MineDojo / GitHub", date: "2023"}
- {id: 9, title: "Video PreTraining (VPT): Learning to Act by Watching Unlabeled Online Videos", url: "https://arxiv.org/abs/2206.11795", source: "arXiv / OpenAI", date: "2022-06-23"}
- {id: 10, title: "Mastering Diverse Domains through World Models (DreamerV3)", url: "https://arxiv.org/abs/2301.04104", source: "arXiv", date: "2023-01-10"}
- {id: 11, title: "Ghost in the Minecraft (GITM)", url: "https://arxiv.org/abs/2305.17144", source: "arXiv", date: "2023-05-25"}
- {id: 12, title: "JARVIS-1: Open-World Multi-task Agents with Memory-Augmented Multimodal Language Models", url: "https://arxiv.org/abs/2311.05997", source: "arXiv", date: "2023-11-10"}
- {id: 13, title: "Difficulty", url: "https://minecraft.wiki/w/Difficulty", source: "Minecraft Wiki", date: "2026-10-17"}
- {id: 14, title: "Ender Dragon", url: "https://minecraft.wiki/w/Ender_Dragon", source: "Minecraft Wiki", date: "2026-10-17"}
- {id: 15, title: "End crystal", url: "https://minecraft.wiki/w/End_crystal", source: "Minecraft Wiki", date: "2026-10-17"}
- {id: 16, title: "Death", url: "https://minecraft.wiki/w/Death", source: "Minecraft Wiki", date: "2026-10-17"}
- {id: 17, title: "aibengineering/beat-the-game-minecraft (dataset card)", url: "https://huggingface.co/datasets/aibengineering/beat-the-game-minecraft", source: "AI Bengineering / Hugging Face", date: "2026-09-15"}
- {id: 18, title: "rmalde/minecraft-agent — Astra and JEV Minecraft agent", url: "https://github.com/rmalde/minecraft-agent", source: "GitHub", date: "2026-09"}
- {id: 19, title: "Will an AI Minecraft Agent defeat the Ender Dragon before 2027?", url: "https://manifold.markets/AdamK/will-an-ai-minecraft-agent-defeat-t-609shENQnu", source: "Manifold Markets", date: "2026-10-17"}
- {id: 20, title: "AI Beats Minecraft in Under 10 Minutes Before 2028? Manifold Bettors Put It at 70%", url: "https://tech-insider.org/ai-minecraft-rsg-speedrun-manifold-odds/", source: "Tech Insider", date: "2026-09-20"}
- {id: 21, title: "Minecraft speedrunner finally sets world record one year after devastating last-second fail", url: "https://www.dexerto.com/minecraft/minecraft-speedrunner-finally-sets-world-record-one-year-after-devastating-last-second-fail-3393560/", source: "Dexerto", date: "2026-07-31"}
- {id: 22, title: "Measuring AI Ability to Complete Long Tasks", url: "https://arxiv.org/abs/2503.14499", source: "arXiv / METR", date: "2025-03-18"}
- {id: 23, title: "Time horizon limitations", url: "https://metr.org/notes/2026-01-22-time-horizon-limitations/", source: "METR", date: "2026-01-22"}
- {id: 24, title: "Gemini 4 Argon — ARC-AGI results", url: "https://arcprize.org/results/google-gemini-4-argon", source: "ARC Prize", date: "2026-10-13"}
- {id: 25, title: "Time Horizon 1.1", url: "https://metr.org/blog/2026-1-29-time-horizon-1-1/", source: "METR", date: "2026-01-29"}
- {id: 26, title: "Holistic Agent Leaderboard (HAL)", url: "https://arxiv.org/abs/2510.11977", source: "arXiv", date: "2025-10-13"}
- {id: 27, title: "Why benchmarking is hard", url: "https://epoch.ai/gradient-updates/why-benchmarking-is-hard", source: "Epoch AI", date: "2025-12-23"}
- {id: 28, title: "τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains", url: "https://arxiv.org/abs/2406.12045", source: "arXiv", date: "2024-06-17"}
- {id: 29, title: "Why Do Multi-Agent LLM Systems Fail? (MAST)", url: "https://arxiv.org/abs/2503.13657", source: "arXiv", date: "2025-03-17"}
- {id: 30, title: "How we built our multi-agent research system", url: "https://www.anthropic.com/engineering/multi-agent-research-system", source: "Anthropic", date: "2025-06-13"}
- {id: 31, title: "AI Agents That Matter", url: "https://arxiv.org/abs/2407.01502", source: "arXiv / Princeton", date: "2024-07-01"}
- {id: 32, title: "Google's Gemini has beaten Pokémon Blue (with a little help)", url: "https://techcrunch.com/2025/05/03/googles-gemini-has-beaten-pokemon-blue-with-a-little-help", source: "TechCrunch", date: "2025-05-03"}
- {id: 33, title: "Collaborating Action by Action: A Multi-agent LLM Framework for Embodied Reasoning (MineCollab)", url: "https://arxiv.org/abs/2504.17950", source: "arXiv", date: "2025-04-24"}
- {id: 34, title: "Four Gemini 4 Argon agents reportedly defeated Minecraft's Ender Dragon", url: "https://digg.com/ai/eh1b7p3i", source: "Digg", date: "2026-10-16"}
- {id: 35, title: "Thread on the Gemini 4 Argon safety and security evaluation", url: "https://x.com/scaling01/status/2110119579829592143", source: "X / @scaling01", date: "2026-10-14"}
- {id: 36, title: "Google DeepMind announcement of the Minecraft run", url: "https://x.com/GoogleDeepMind/status/2111127991401247033", source: "X / @GoogleDeepMind", date: "2026-10-16"}
- {id: 37, title: "Introducing Gemini 4 Argon", url: "https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/", source: "Google", date: "2026-10-13"}
- {id: 38, title: "Gemini API pricing", url: "https://ai.google.dev/gemini-api/docs/pricing", source: "Google AI for Developers", date: "2026-10-17"}
- {id: 39, title: "Gemini 4 Argon model page", url: "https://ai.google.dev/gemini-api/docs/models/gemini-4-argon", source: "Google AI for Developers", date: "2026-10-13"}
- {id: 40, title: "Daylight cycle", url: "https://minecraft.wiki/w/Daylight_cycle", source: "Minecraft Wiki", date: "2026-10-17"}
:::
