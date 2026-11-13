# How a Society of Agents Would Work, in Tether Terms

2026-10-22 · Isaiah Nwukor

## Why one agent is not enough

A brand-new agent starts with almost nothing, so it is slow and clumsy at first. Isaiah's phrase for it: "like asking a newborn to take the MCAT." That is expected, not a flaw.

What turns newborns into capable agents is not a smarter newborn. It is being born into a group that has already learned things: generations of agents, sharing a place where knowledge is stored, sorted and passed on. Each agent then has to decide how far to trust its own experience and how far to trust the crowd.

The Tether already describes this. Figure 11 says "capability is a property of agent-and-habitat, never of the agent alone." A newborn agent is made capable by the surroundings it is born into, and the shared knowledge store is part of those surroundings.

This document explains, in plain terms, how such a group would work under the Tether's rules. It is a design sketch, not something built. Everything here is ranged against the Tether's thirteen figures, which govern wherever they disagree with anything else.

## The core picture: separate agents, one ground

Each agent is a separate point of view, and they all answer to the same judge: the world itself. In the Tether that judge is called the ground. For a game-playing agent it is the game. It does not change its mind because of what any agent thinks.

Isaiah puts it this way: "their separation as frames make them viable vantage points to range against an unmoveable verifying ground that they tether to." Figure 2 says the same: "Frames range against the ground. They do not negotiate with it ... Each frame is corrected by it separately, and what makes the correction sound is that neither frame can move it."

Two things follow, and the rest of this document builds on them.

- **A group is only worth having while its members stay different.** Figure 2 defines independence as "how little they draw on the same evidence." Ten copies watching the same thing are one opinion said ten times.
- **The group's agreement is never the verdict.** Figure 2 warns of two collapses. In the first, agents update on each other until they converge on "whoever had the most influence." In the second, they never talk but share one source, so "the agreement is the pool talking." Only the ground decides.

## What gets shared, and what never does

The group shares methods, never recordings. Figure 4 sets the rule between an individual and the group above it: "Only methods cross up. Only head starts come down."

- **A method** is a reusable pattern: a template, a recipe, a general shape that worked, settled by the ground before it is shared. It travels well because the details of one occasion have been stripped out.
- **A recording** is "press this button at this spot." Figure 4 is blunt about it: "A recording carried upward looks like knowledge and is a description of one occasion. Replayed downward, it produces a system that repeats a past success and cannot produce a new one."

What comes down to a newborn agent is a head start: candidates that make its search cheaper. It still has to test each one in its own world. And when a shared method lands somewhere new, the group measures how well it carried over. Figure 4 calls this taking the round trip: "Without it you are navigating by dead reckoning."

Why is shared knowledge worth so much? Figure 12 gives the reason. Once something is settled and recorded, re-deriving it "is a lookup and the actions were spent once. Where it is not ... every lineage pays again." A shared store means the next agent does not pay again for what its predecessors already learned.

Outside research agrees. In a famous tournament of copying strategies, the winners copied heavily, partly because the agents they copied had already filtered what was worth doing ([Rendell et al. 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2989663)). A lifelong game-playing AI, Voyager, keeps a library of reusable, verified skills rather than recorded play ([Wang et al. 2023](https://arxiv.org/abs/2305.16291v2)).

## The room: many agents on one problem

When many agents work one problem together, they share a room: a common workspace for that one question, opened with it and closed with it. Figure 10: "The room composition is a function of the question. When the question changes, the room should change."

Inside a room, everything can be shared, including exact moves and half-finished results. That is not a contradiction of the "methods only" rule. A room is one problem's work spread across many bodies, and Figure 12 says "Inside a run the arrangement persists and nothing is re-earned." When the room closes, only the general method moves up into the shared library that newborn agents inherit.

So there are two stores:

- **The room**, one per problem. Agents share everything, recordings included, to solve that one problem faster.
- **The commons**, across problems. It holds only methods distilled from finished rooms.

```
                       newborn agent
                            ▲
                            │  head starts only (methods, to be tested again)
                 ┌──────────┴──────────┐
                 │      THE COMMONS     │  methods distilled from finished rooms
                 └──────────▲──────────┘
                            │  when a room closes, only the general method moves up
       ┌────────────┐ ┌─────┴──────┐ ┌────────────┐
       │  room: A   │ │  room: B   │ │  room: C   │  one per problem;
       │ everything │ │ everything │ │ everything │  moves and half-results
       │  shared    │ │  shared    │ │  shared    │  shared inside
       └─────┬──────┘ └─────┬──────┘ └─────┬──────┘
   ══════════╧══════════════╧══════════════╧══════════
                THE GROUND (the game, the checker)
```

The ground sits under all three: no store's agreement replaces it.

Isaiah's example is the Navier-Stokes result reported in September 2026. Roughly 10,000 AI agents reached a proof in about 88 hours, and the proof was then checked by Lean, a program that verifies every step ([Quanta](https://www.quantamagazine.org/ai-has-solved-one-of-maths-1-million-millennium-prize-problems-20260908/); [Simon Willison](https://simonwillison.net/2026/Sep/8/on-navier-stokes/)). Its status is still provisional, and credit is disputed ([Tufts Daily](https://www.tuftsdaily.com/article/2026/09/mathematicians-still-checking-the-navier-stokes-proof-that-openai-claims-to-have-solved)). It shows the room working:

- **Evolution pays in bodies.** In the Tether, actions are the price of finding out whether something holds (Figure 12). Many agents buy many tests at once. That is Figure 6's "more search at the same reach ... Distribute the search."
- **The answer was already reachable.** The proof built on earlier human work, so the remedy was "more search, not another atom" (Figure 8). The shared room is what turns ten thousand searchers into one search, instead of ten thousand people re-checking the same ground.
- **The ground settled it, not the agents' agreement.** Lean was the unmoveable judge. Figure 7's progress formula, R = h² × S, borrowed from breeding, reads directly: how faithfully partial results pass between agents, times how hard the checker selects. "Zero either and the chain runs in place."

Rooms exist only in a real multi-agent system, with the shared infrastructure behind them: shared storage, communication, outcome votes and decay. A single agent never stores answers for itself. As Isaiah puts it, the collective can simply hold "way more data in a different external form than one agent can hold alone."

## Trusting yourself versus the crowd

Every agent in a group leans partly on its own experience and partly on the crowd's. The Tether's formula writes that balance as a single letter, w: belief "formed from its own history and from what it inherited, mixed by w ... w is learnable from the outcomes of past weightings."

Isaiah calls w "a crude representation" of something richer, and Figure 13 shows what it is made of.

- **The collective is a continuum.** Figure 13 says a continuum is not one of its six building blocks: "Spectrum and gradient compose a continuum." A spectrum is an ordering, "so more and less can be said": agents lined up from self-reliant to crowd-reliant.
- **Each individual carries a gradient,** "a difference that can be spent": its own pull in one direction.
- **The agents also relate,** which makes them a network, and "Network and gradient compose a flow." Knowledge flows between agents along those gradients.

That is why w felt nebulous. It is a composition, an agent's own history crossed with the collective's continuum and its own gradient, written as one symbol. Figure 12 calls this the flat formula: "the ingredients are recorded and the arrangement is not."

**How a group collapses.** If every agent's w drifts to the average, the spread is gone and the gradients are spent. The room then slides into what Figure 2 calls coherent drift: "everything drifts together, and the drift is coherent, which is why nobody notices." Two results from outside the Tether say the same:

- **Evolution.** Fisher's fundamental theorem says a population adapts at a rate set by its variance in fitness. With no spread, it cannot adapt ([Fisher's theorem](https://en.wikipedia.org/wiki/Fisher%27s_fundamental_theorem_of_natural_selection)).
- **Slime molds.** The Keller-Segel model describes cells that each climb a shared chemical gradient while also wandering randomly. When following the gradient outweighs wandering, past a critical amount, the whole population collapses into one point. The literature calls this "chemotactic collapse" ([Blanchet, Dolbeault & Perthame 2006](https://www.maths.tcd.ie/EMIS/journals/EJDE/Volumes/2006/44/blanchet.pdf)). In the real slime mold that collapse is useful: the cells become one organism. The difference is whether the ground has settled things first.

For a single agent there is no crowd, so none of this applies to it. The Tether's rules still do.

## Keeping the crowd wise

A shared store only helps if what rises in it is what actually works. Four rules keep it honest.

**1. Votes come from outcomes, not popularity.** When an agent uses a shared method, the result in its own world is a vote: up if it helped, down if it did not. That is the ground voting, which Figure 7 says is where selection belongs: "Selection between rooms is where the ground votes." Two refinements keep the votes fair:

- **Use the success rate per try, not the total.** Whatever gets tried most piles up votes. In an online music-market experiment, letting people see others' choices "increased both inequality and unpredictability of success" ([Salganik, Dodds & Watts 2006](https://www.cs.toronto.edu/~bor/303s19/docs/salganik_dodds_watts.pdf)).
- **Keep the rate per kind of situation.** A method that is brilliant in one setting must not be drowned by an average across all of them. Figure 1: "Aggregating across slots is how a live signal disappears into an average."

**2. Independent discoveries count most.** An agent that found something on its own is far stronger evidence than one that tried it because it ranked high. Figure 8: "Convergent derivation and adopted import look identical in the contents. Only the record of where each came from separates them." So every entry keeps its history. When people could see each other's guesses, their answers narrowed without getting any more accurate ([Lorenz et al. 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3107299)).

**3. Things fade, so they can be tried again.** If a group avoids an idea after one bad result, it never tries it again, so it never learns the idea was fine. This trap is called the hot stove effect ([Denrell & March 2001](https://ideas.repec.org/a/inm/ororsc/v12y2001i5p523-538.html)). Decay solves it: an old verdict slowly loses weight until it is worth re-testing. The record is never deleted. Figure 6: "What is recorded only grows. What is reachable is derived, and it can fall." In the big copying tournament, the best strategies weighed information by its age ([St Andrews summary of Rendell et al. 2010](https://news.st-andrews.ac.uk/archive/the-art-of-copying/)).

**4. Bad news travels in the same lane as good news.** Knowledge of what fails is shared, voted on and faded just like knowledge of what works. Figure 5: a refusal "pays the same bargain ... Same mint operator, same three guards." And nothing is bad in itself, only bad for a given goal, the way one species is both predator and prey. Figure 11: "The same actor is a benefactor to one residual and a malfactor to another." Animals learn what to fear just by watching others ([Olsson & Phelps 2007](https://pubmed.ncbi.nlm.nih.gov/17726475/)). That is exactly why shared fears need decay most: nobody who avoids something ever tests it.

A group also needs some members who keep trying what the rest avoid. One study found that groups rescue what individuals wrongly give up, as long as a minority keeps re-trying ([Toyokawa & Gaissmaier 2022](https://pubmed.ncbi.nlm.nih.gov/35535494/)). And it needs fresh newcomers: a population of pure copiers stops tracking a changing world, because nobody is learning first-hand any more ([Rogers' paradox and its resolution](https://bookdown.org/amesoudi/ABMtutorial_bookdown/model18.html)).

## Who looks after the shared store

Someone has to keep the shared store organised, and in the Tether that is the ground maintainer, the seat in Figure 10. Its job is narrow and strict.

- **It sets conventions, never verdicts.** It decides how things are labelled, sorted and filed. It never writes an entry or decides which one is true. Figure 10: the seat "may author what has no truth value and nothing that does."
- **It brings in the specifics of each problem.** The details of a given setup (how fast things fade, how votes are counted, how rooms are run) are not new architecture. They are domain details the maintainer brings in from outside, with their source cited. The figures already describe the structure.
- **It adds, it never removes.** Figure 11: "Introduction is available; exclusion is not." A new method is introduced to a few agents first, and its knock-on effects are watched before it spreads. Figure 11 names the mistake to avoid: cane toads and kudzu, "the same move with the cascade unenumerated."
- **It is never one of the agents being ranked.** Figure 10: "Whoever is measured by a reading cannot own it."

What goes into a room should also not be hand-picked. Figure 10 lists the honest ways to choose members: "a lottery, everyone who qualifies, a set assembled before the question existed." A carefully chosen room is still a chosen room.

## When a member stalls or crashes

Every safety rule for a single agent has a group version. The single agent protects itself. The group protects the rest of its members from one member's trouble.

| Problem | A single agent | A group of agents |
| --- | --- | --- |
| A move that never ends | The agent checks its own deadline everywhere it thinks, and records "ran out of time here", never "failed" | An outside wall ends a member that overruns. Its task is recorded as cut, and the others keep their time |
| A crash in the agent's own machinery | It records the crash, throws away its possibly broken state, reloads a clean copy and carries on. The same crash twice ends the game | The group survives one member's failure. The member's checked learning is kept, and a fresh member carries on |
| Memory | The agent's own limit, with a clear-out when it runs high | Memory is a shared, finite resource, split so the group never asks for more than the machine has |

The Tether lines behind them:

- **Deadlines are filters, never verdicts.** Figure 9: "Use filters for the budget and witnesses for the verdict. Never let a filter hand you a verdict."
- **A crash is a broken channel, not a broken world.** Figure 10: "the ground does not decay, the channel does." The remedy is to restore contact, not to give up.
- **Resources are finite.** Figure 13 describes energy as "conserved, finite." Members of a group are each other's habitat and each other's competitors (Figure 11).

## One agent over time is a group too

A single agent running over a long time is, in a non-linear sense, a population of its own past selves. Isaiah: "an agent on a loop, is not too dissimilar to a multi agent system ... but their ability to range against their past self is limited and only benefits with wide gaps between start and current."

**Why it is limited.** Independence is "how little they draw on the same evidence" (Figure 2), and the present self carries everything the past self saw. Figure 6: "What is recorded only grows." So a recent past self is, in Figure 8's words, "one frame wearing two names."

**Why a wide gap helps.** Two things grow with distance:

- **Drift.** Many small updates can carry the whole self somewhere wrong, and only a comparison with a distant earlier self shows it. That is Figure 4's round trip: without it "you are navigating by dead reckoning."
- **Ground given up.** As an agent rules things out, its options shrink. Figure 6: "What is reachable is derived, and it can fall." A distant past self is where abandoned options can be found again.

Outside research agrees:

- **Statistics.** Successive states of a running process are correlated. Two snapshots only count as independent once they are further apart than the process's "autocorrelation time." Figure 2 names the same arithmetic, the effective-sample-size correction.
- **Evolution.** Time-shift experiments pit hosts against parasites from different points in time, even eggs revived from old lake sediment. Changes invisible between contemporaries show up across the gap ([Gaba & Ebert 2009](https://edoc.unibas.ch/5711/)).
- **AI.** AlphaStar trained against a league of its own past versions, so it could not forget how to beat old strategies ([DeepMind 2019](https://deepmind.google/discover/blog/alphastar-grandmaster-level-in-starcraft-ii-using-multi-agent-reinforcement-learning/)).
- **People.** We judge distant past selves more harshly than recent ones ([temporal self-appraisal](https://concepts.dsebastien.net/concept/temporal-self-appraisal/)). It is a reminder that a past self is a vantage point, never the judge. The ground stays the anchor.

**The ship of Theseus.** Isaiah: "its the reason why both ships are the ship of theseus. when viewed non-linearly they both exist. only in terms of time does it seem like a paradox." The Tether places identity in the lineage, not on a single timeline. Figure 13: "A term carries the atoms it was built from and the bonds that joined them. That record is not documentation of the term. It is the term."

- The rebuilt ship is the ship read by its parts: the original planks, and their record.
- The ship in use is the ship read by its arrangement carried forward: continuous repair, the same role. Figure 12: "The arrangement is the substance."

Both lineages are real. The paradox only appears when both are forced onto one line of time with one owner of the name. Figure 10: "The tree of life is what a non-invertible transform looks like from outside."

The Tether itself came about this way. Isaiah reached it by ranging against his own earlier work, Ouroboros v1 to v4, across exactly the kind of wide gap described above.

## How much does a group magnify an agent?

Isaiah describes a collective as a magnifier on each agent's own intelligence. He suggested the mathematics of computer cores as the analogue, and it fits. When you add processor cores to a computer, three things decide how much faster it gets, and each one has a twin in the Tether.

- **How different the members are.** Statisticians correct for look-alike samples: N samples that resemble each other by an amount ρ count as only N / (1 + (N−1)ρ) independent ones (Kish 1965). However many members join, the group never counts as more than 1/ρ, and ten clones count as one. Figure 2 names this same correction, "the effective-sample-size correction for correlated observations."
- **How much of the work only one member can do at a time.** Amdahl's law: if a share σ of a job must be done in sequence, no number of cores makes it more than 1/σ times faster (Amdahl 1967). But when the problem grows with the team, more cores search more space, and the gain grows in step with the team (Gustafson 1988). That is the Navier-Stokes room: more searchers, a bigger search.
- **What it costs to stay in sync.** The Universal Scalability Law adds a coherence cost κ for every member keeping up with every other: C(N) = N / (1 + σ(N−1) + κN(N−1)) (Gunther 2008). Past a peak, at about √((1−σ)/κ) members, adding more makes the group slower.

That last point matters for Isaiah's condition, that "the learning is mutually shared by all participants." Sharing is what makes a collective work, and it is also its biggest cost. The Tether keeps that cost low in two ways:

- Only compressed methods go into the shared store. Figure 4: carry up a method "compressed to its essentials."
- Full sharing happens only inside one room, for one question.

**Where compounding lives.** In the number of members, the magnifier grows at most in step with the group, and usually levels off. It can compound over time instead. Each method one generation settles becomes a building block the next generation starts from. Experiments on cultural evolution agree: larger groups keep more complex knowledge and improve it more often (Derex et al. 2013), and small, cut-off groups lose skills over generations (Henrich 2004). If the gain grows exponentially anywhere, these analogues place it across generations, not in headcount.

Measurements line up with this:

- **Human groups.** A single "collective intelligence" factor predicted group performance across many tasks. It was not strongly tied to the members' average intelligence or the smartest member's. It tracked how evenly people took turns and how well they read each other (Woolley et al. 2010). The arrangement mattered more than the members, which is Figure 12's "The arrangement is the substance."
- **AI agents.** Performance rises with the number of agents (Li et al. 2024). In networks of collaborating agents it follows an S-curve, a rise and then a plateau, and irregular networks beat regular ones (Qian et al. 2024).

None of this gives one number for "how much smarter." It gives the dials instead:

- how different the members are;
- how much of the problem must be done in sequence;
- how costly it is to stay in sync;
- how many generations the group keeps building.

Each of these can be measured on a running group. None of them is a constant to pick.

## What this does and does not claim

This is a design sketch, and nothing in it has been built. The agent being entered in ARC Prize 2026 is a single agent. None of the group machinery runs today.

- **It claims** that the Tether's figures already contain the structure of a multi-agent system: separate frames, one ground, methods shared upward, head starts handed down, a room per problem, and a maintainer who sets conventions but never verdicts.
- **What Ouroboros showed.** Isaiah's Ouroboros v1 to v4 showed that collective intelligence works from a cold start. In his words: "i did not train any agents myself it was all evolution and generations and their shared mediums etc they eventually easily beat the preview games." Ouroboros came before the Tether, so it is not a test of the Tether.
- **What the Tether explains about it.**
  - *Why it worked:* the ground voted between generations (Figure 7: "Selection between rooms is where the ground votes"), and the shared mediums turned many searchers into one search (Figure 6: "Distribute the search").
  - *Why it was not enough for a general agent:* members that lean on the collective drift toward its average. Figure 2 describes the pattern: agents updating on each other converge on "whoever had the most influence." In Isaiah's words, the system "only creates average workers who all have nearly the same capabilities (they averaged to the mean of the collective or ranged against it with their 'w')."
- **What the current agent adds.** In Isaiah's words, it "has full autonomy and control over its reasoning and can program itself (outside of the core architecture/kernel)." The kernel is fixed: Figure 4 calls it "the part that does not change with size." On top of it, the agent writes its own new methods, and each one it settles becomes a building block for the next (Figure 12: "A settled molecule becomes an atom for whatever composes over it").
- **General, but not unlimited.** The agent can learn whatever its senses and actions let it reach. Figure 6: "Composition explores what the operators reach; instruments extend what can be represented at all." A person can learn any skill their body allows, but cannot learn to grow wings.
- **So a society of these agents** would be a magnifier on an agent that is already general within its reach. The previous section covers how big a magnifier.
- **What is not claimed.** Nothing here has been measured for a society of Tether agents. Three tests against the ground would settle it:
  - Does an agent born into the shared store reach its first level in fewer moves than one starting alone?
  - Does that hold on kinds of game the store has never seen?
  - Does adding agents with different experience help more than adding copies?
- **The outside research** is supporting evidence from other fields. It does not prove the Tether. Where those fields and the figures disagree, the figures govern.
- **This sketch grew out of Isaiah's earlier paper,** *Role based Multi-Agent Reasoning Frameworks* (IJCA, Feb 2026), the Ouroboros v1 to v4 line. That approach worked in practice. The Tether supersedes it, and every idea borrowed from it here was checked against the figures.

The full technical version, with every figure line and every decision, sits beside this file as `E7_multiple_instances_technical.md`.

## References

**The Tether figures cited**

| Figure | What it contributes here |
| --- | --- |
| 1 The Agent | Signals are kept per object, never averaged away |
| 2 The Ground | Frames range against one unmoveable ground; independence and the effective-sample-size correction; the two collapses |
| 4 The Membrane | Only methods cross up, only head starts come down; the round trip |
| 5 The Mint Pipeline | Refusals pay the same bargain as new terms |
| 6 Closure and Reachability | The record only grows; reach can fall; distributed search; instruments bound what can be learned |
| 7 The Room Chain | The ground votes between rooms; progress R = h² × S |
| 8 The Union Surplus | More search, not another atom; provenance separates finding from copying |
| 9 When Composition Stops | Filters for the budget, never for the verdict |
| 10 The Ground Maintainer | Conventions not verdicts; rooms chosen by lottery; lineages that branch |
| 11 The Habitat | Capability is agent-and-habitat; valence depends on the goal; introduce, never subtract |
| 12 The Bond | The arrangement is the substance; settled work is not re-earned |
| 13 The Minimum Viable Set | Spectrum, gradient, network, continuum, flow; the lineage is the proof |

**Outside research**

- [Rendell et al. 2010, Why copy others? Insights from the social learning strategies tournament](https://pmc.ncbi.nlm.nih.gov/articles/PMC2989663)
- [St Andrews summary of the tournament: the best strategies weighed information by its age](https://news.st-andrews.ac.uk/archive/the-art-of-copying/)
- [Lorenz et al. 2011, How social influence can undermine the wisdom of crowd effect](https://pmc.ncbi.nlm.nih.gov/articles/PMC3107299)
- [Salganik, Dodds & Watts 2006, Inequality and unpredictability in an artificial cultural market](https://www.cs.toronto.edu/~bor/303s19/docs/salganik_dodds_watts.pdf)
- [Denrell & March 2001, Adaptation as information restriction: the hot stove effect](https://ideas.repec.org/a/inm/ororsc/v12y2001i5p523-538.html)
- [Toyokawa & Gaissmaier 2022, Conformist social learning and collective behavioural rescue](https://pubmed.ncbi.nlm.nih.gov/35535494/)
- [Rogers' paradox and Enquist et al. 2007, critical social learning (Mesoudi's tutorial)](https://bookdown.org/amesoudi/ABMtutorial_bookdown/model18.html)
- [Olsson & Phelps 2007, Social learning of fear](https://pubmed.ncbi.nlm.nih.gov/17726475/)
- [Fisher's fundamental theorem of natural selection](https://en.wikipedia.org/wiki/Fisher%27s_fundamental_theorem_of_natural_selection)
- [Blanchet, Dolbeault & Perthame 2006, The two-dimensional Keller-Segel model](https://www.maths.tcd.ie/EMIS/journals/EJDE/Volumes/2006/44/blanchet.pdf)
- [Gaba & Ebert 2009, Time-shift experiments as a tool to study antagonistic coevolution](https://edoc.unibas.ch/5711/)
- [DeepMind 2019, AlphaStar: Grandmaster level in StarCraft II](https://deepmind.google/discover/blog/alphastar-grandmaster-level-in-starcraft-ii-using-multi-agent-reinforcement-learning/)
- [Temporal self-appraisal (Wilson & Ross 2001), summary](https://concepts.dsebastien.net/concept/temporal-self-appraisal/)
- [Wang et al. 2023, Voyager: an open-ended embodied agent](https://arxiv.org/abs/2305.16291v2)
- [Quanta, September 2026: AI has solved one of math's Millennium Prize problems](https://www.quantamagazine.org/ai-has-solved-one-of-maths-1-million-millennium-prize-problems-20260908/)
- [Simon Willison, September 2026: Some thoughts on the Navier-Stokes Millennium Prize Problem](https://simonwillison.net/2026/Sep/8/on-navier-stokes/)
- [Tufts Daily, September 2026: Mathematicians still checking the Navier-Stokes proof](https://www.tuftsdaily.com/article/2026/09/mathematicians-still-checking-the-navier-stokes-proof-that-openai-claims-to-have-solved)
- [Kish 1965, Survey Sampling: the design effect and effective sample size (summary)](https://en.wikipedia.org/wiki/Design_effect)
- Amdahl, G. (1967). Validity of the single processor approach to achieving large scale computing capabilities. AFIPS Spring Joint Computer Conference.
- Gustafson, J. (1988). Reevaluating Amdahl's law. Communications of the ACM 31(5).
- [Gunther 2008, A general theory of computational scalability based on rational functions (the Universal Scalability Law)](https://arxiv.org/abs/0808.1431)
- [Woolley et al. 2010, Evidence for a collective intelligence factor in the performance of human groups (summary)](https://acawiki.org/Evidence_for_a_collective_intelligence_factor_in_the_performance_of_human_groups)
- [Derex et al. 2013, Experimental evidence for the influence of group size on cultural complexity](https://ideas.repec.org/a/nat/nature/v503y2013i7476d10.1038_nature12774.html)
- [Henrich 2004, Demography and cultural evolution: the Tasmanian case](https://cambridge.org/core/journals/american-antiquity/article/abs/demography-and-cultural-evolution-how-adaptive-cultural-processes-can-produce-maladaptive-lossesthe-tasmanian-case/8CD08CC61E6FACF59EC02659B2BDA43C)
- [Li et al. 2024, More agents is all you need](https://arxiv.org/abs/2402.05120v1)
- [Qian et al. 2024, Scaling large language model-based multi-agent collaboration](https://arxiv.org/abs/2406.07155v3)
- Nwukor, I. (2026). *Role based Multi-Agent Reasoning Frameworks.* International Journal of Computer Applications 187(78).
