# E7 — Multiple instances of the agent: how they would work together (a future feature; nothing implemented)

Reviewer draft, 2026-10-22 CDT. Isaiah's request (10-17): "If the agent had multiple instances, how would it interact with them? (this can be a stub or document to explain how they would collab, and you can borrow highlight notes from ouroboros v1-v4) but nothing needs to be implemented, just a doc."

Isaiah's guideline for it (10-22, 10:47 CDT): "what makes dumb agents or cold start agents smart, is having generations of agents or a multi agent system that has a shared repository for communication, storage and categorization of communal knowledge, then the agent must weigh its own self reliance vs the common crowd wisdom." The early paper (Nwukor, "Role based Multi-Agent Reasoning Frameworks", IJCA 187(78), Feb 2026; the Ouroboros v1-v4 line) is direction: "that approach DID work". The Tether supersedes it, so every borrowed idea below is ranged against the figures.

The proctor reads this and corrects every claim it makes about today's code (section 7 is marked for that).

**HOW TO READ THIS DOCUMENT (Isaiah, 12:06 CDT).** "remember that i said that the mutli agent part was just a doc? we dont have to retroactively make it fit, its already covered in the tether. the specifics are domain details and nuances of the problem nature that the ground maintainer supplies right? ... that w formula is a crude representation but on the multi agent level its a representation of some gradient that is occuring in all agents, that is what makes the room collapsible (coherent drift) if they converge to the average".
- The architecture is the Tether's, and it is already complete. Nothing here is to be retrofitted onto the single agent.
- The SPECIFICS below (per-trial vote rates, decay rates, staged introductions, room rules, starting spreads) are DOMAIN DETAILS. The ground maintainer supplies them for a given problem: its office holds "external contact: people, literature, instruments outside the arrangement", produces "imports carried with citation", and in the maintained habitat may "choose the instruments, distil the impactful actors, introduce what was not there" (THE_SEAT_MAP, Seat 3 and the habitat; Fig 11 :58-61). They are imports for a domain, not new architecture.
- w is a CRUDE representation, and at the multi-agent level it stands for a GRADIENT across all agents: the spread between how much each leans on itself and how much on the crowd. A gradient is "a difference that can be spent" (Fig 13 :45-47). If every agent's w converges to the average, the gradient is spent, and the room collapses into coherent drift: "everything drifts together, and the drift is coherent, which is why nobody notices" (Fig 2 :34); "a chain of mirrors is one long room" (Fig 7 :36). Keeping that spread alive is what keeps a room able to find anything.
- For one agent there is no crowd, so the crowd rules (and this w) do not apply. The Tether's rules always do.
- Isaiah, 12:12, refining: "its more like the collective is a continuum (if you think about it non linearly) and then the individuals have the gradients ... the 'w' was representing the cross of those two things + some state or composition which made 'w' nebulous." Checked against Fig 13 (12:15):
  - A spectrum is a member ("ordering, so more and less can be said", 13:20). A continuum is NOT a member: it "was the seventh and was removed ... it is a spectrum without gaps, or smoothness over space and time" (13:43-44), and "Spectrum and gradient compose a continuum" (13:75). So the collective, read as a smooth field over many agents, is a continuum, a composition that already holds the individuals' gradients. A finite group ordered from self-reliant to crowd-reliant is a spectrum with gaps. Frozen without direction, that spread is only "a distribution ... a fact that stays put" (13:45-46).
  - The agents relate, so the collective is also a network, and "Network and gradient compose a flow" (13:75): the individuals' gradients over the collective's network compose the flow of knowledge between agents.
  - Why w felt nebulous: it is a composition (an agent's state, its history, crossed with structures: the collective's continuum and its own gradient) written as ONE symbol. That is Fig 12's flat formula: "the ingredients are recorded and the arrangement is not" (12:14). A molecule written as an atom.
  - The collapse: when individuals converge on the average, the spectrum loses its ordering, the gradients are spent, and the flow stops. Witnesses: Fisher's fundamental theorem (1930), where the rate of adaptation equals the population's variance in fitness, so no spread means no adaptation; and Keller-Segel chemotaxis, where individuals each climb a shared gradient while diffusing, the population is modelled as a continuous density, and when gradient-following outweighs diffusion (above a critical mass, 8π in 2D) the density blows up into a point in finite time, "chemotactic collapse" (Blanchet, Dolbeault & Perthame 2006). w, in that picture, is the balance between following the shared gradient and independent spread.
  - A gap in the figure, for Isaiah: Fig 13 :74 says "Everything else is a composition across the two kinds, never within one", but the three examples on :75 each pair two members of the SAME kind (space+time are states; spectrum+gradient and network+gradient are structures).
- Isaiah, 12:07: "their separation as frames make them viable vantage points to range against an unmoveable verifying ground that they tether to". This is Fig 2 :45-46: "Frames range against the ground. They do not negotiate with it ... Each frame is corrected by it separately, and what makes the correction sound is that neither frame can move it." The agents' worth as a population IS their separation. Each is a vantage point only while it stays a separate frame, tethered to a ground none of them can move.

---

## 1. The residual, in effect terms

A fresh agent with no saved learning is very slow: its first move on lf52 took about 8 minutes (measured while a stray process held one core, so not a clean number). One agent learns only from its own games. The question is how several agents, or generations of agents, can share what they learned so that a new one starts smart, without the sharing making them all wrong together. Each agent has to decide, case by case, how far to trust its own experience and how far to trust the crowd's.

## 2. Domain census (written before any figure line was chosen)

R: arity 3 (one agent; the shared store; the ground) · symmetry: the agents are NOT interchangeable, they differ by history and by their weighting, and that difference is what makes them worth having · scale: step, game, lifetime, generation, population.

| Domain | Actors | Currency | Anchor |
|---|---|---|---|
| D1 One agent (the kernel) | slots, terms, the agent's library | bits and actions | the game board |
| D2 The commons (the shared store) | agents, a shared library, something that ranks what they produce | reapplicable methods | ground outcomes when OTHER agents reuse a method |
| D3 The membrane (between D1 and D2) | what is carried up, what is sent down | the round-trip gap | the gap measured when a carried method lands somewhere new |
| D4 Independence | frames and their evidence | evidence overlap | provenance: where each entry came from |
| D5 The maintainer and the habitat | the seat that curates the store | conventions (schema, tags) | an unauthored pool |
| D6 Generations | the lineage (generator) and each instance | variation and selection | the ground's votes across generations |

- Union, not partition: D1 ∩ D2 is Isaiah's "self reliance vs crowd wisdom". It is a compound with its own loop: a weighting learned from how past weightings turned out.
- D2 ∩ D4: the crowd is only wise to the extent its members are independent.
- Order (Fig 3, by dependency): the ground → D1 → D3 → D2 → D4 → D5 → D6. A commons cannot help an agent whose own loop does not run, and a population cannot select what its members never produced.

## 3. What the Tether says, per domain (verbatim, then the reading)

### D1: the kernel does not change with size
- Fig 4 :19-20: "The kernel is the part that does not change with size: the same loop and the same rule for naming what worked, whether one agent is running it or a thousand. Only the actors, the currency and the anchor change."
- READING: a multi-agent system is NOT a new architecture. Each instance runs today's loop unchanged. What is new is one more scale above it, with its own actors (agents), currency (methods) and anchor (outcomes of reuse elsewhere). [triangulated with Fig 10 :67-68, "The seat above is not a larger copy of this one. Different actors, a different currency, a different ground"]

### D2 + D3: what may be shared, and in which direction
- Fig 4 :4-5: "the population: many agents, a shared library, and something that ranks what they produce". That is Isaiah's shared repository, drawn in the figure.
- Fig 4 :22-26: "Only methods cross up. Only head starts come down. ... A recording carried upward looks like knowledge and is a description of one occasion. Replayed downward, it produces a system that repeats a past success and cannot produce a new one."
- Fig 4 :9: carry up "a method that can be reapplied, verified, and compressed to its essentials".
- Fig 4 :30, :36-37: "take the round trip and measure the gap ... using the size of the gap to decide when a new term is worth minting."
- READING: the commons holds METHODS (kinds, templates, canonical forms, recipes WITH their bonds, refusals), each settled by the ground before upload. Never action traces, game ids, positions or colours. What comes down is a head start: a candidate that makes the next search cheaper. It is never a script to replay. The gap between what was uploaded and how it fares in a new agent's game is recorded, and it says how much the abstraction gave up. [triangulated: Fig 4 + Fig 12 :104, "A settled molecule becomes an atom for whatever composes over it"]
- THE CORE REASON A COMMONS PAYS (added in the 11:20 audit), Fig 12 :107-110: "Settling compresses the description and not what it cost to establish. Whether that cost must be paid again depends on the substrate: where the arrangement is recorded, re-deriving it is a lookup and the actions were spent once. Where it is not, the result carries forward and the deriving does not, so every lineage pays again. Which boundary matters is the one the record does not cross." A newborn agent with no commons pays again, in actions, for everything its predecessors settled. The commons is the record that crosses the lineage boundary, so those actions are spent once. This is Isaiah's thesis in the figure's own words.

### D2 ∩ D1: self-reliance against the crowd, the weighting w
- The Formula, Symbols (-:20-26): b, the belief, is "Formed from its own history and from what it inherited, mixed by w ... w_A + w_B = 1, and w is learnable from the outcomes of past weightings. Two frames with identical architecture diverge because their histories and their w diverge."
- READING: Isaiah's guideline is already in the formula, as w. Three consequences:
  - w is LEARNED, never set. If trusting the crowd paid in past decisions of this kind, lean on the crowd here; if it misled, lean on yourself.
  - w is best kept per kind of question, not as one global dial. An agent can be expert in pushing and a novice in gravity. (Single-source reading; the formula does not say per-kind. Put to Isaiah, OPEN 1.)
  - Different w is a SOURCE of independence ("diverge because their histories and their w diverge"). A population with one shared w is less independent than one where w varies.
- Fig 6 :24: "Import from a live peer is debited against that frame's independence. A wrong atom costs more than starting from primitives." Taking from the crowd is not free: it spends the agent's independence, and a wrong import costs more than none. So w has a price on the crowd side too, not only on the self side. [triangulated: Formula + Fig 6]

### D4: the crowd is only wise if its members are independent
- Fig 2 :13-21: collapse 1, "no anchor; each updates on the others ... they converge, and what they converge on is whoever had the most influence"; collapse 2, "one evidence pool ... the agreement is the pool talking".
- Fig 2 :40: correlation is "disqualifying for a verdict: agreement about the world is worthless when the agreeing frames share an evidence pool".
- Fig 6 :53-54: "searchers drawing on the same evidence are one searcher wearing many names. Independence decides whether more of them buy more search or only more spelling".
- Fig 8 :50-52: "Two frames can hold the same atom by convergence, reaching it separately, which is corroboration at maximum independence. Convergent derivation and adopted import look identical in the contents. Only the record of where each came from separates them".
- READING:
  - A commons that ranks entries by HOW MANY AGENTS USE THEM rewards popularity, not truth. That is collapse 1 at population scale.
  - The ranking that counts is INDEPENDENT ground settlements. Every entry carries provenance. An agent that downloaded an entry and then found it paid is a weaker confirmation than an agent that derived the same entry on its own and found it paid. The second is the strongest evidence a population can produce.
  - More agents help only if their evidence differs: different games, orders, seeds, histories, w. Ten clones on the same games are one agent with ten names. [triangulated: Figs 2, 6, 8]
- Fig 1 :24-27: "These do not count: coverage, and compression achieved; predicates minted, and credibility accrued. They are frame-internal." So a shared "credibility score" that the population computes from its own usage cannot be the success measure. The ground is.

### D5: who looks after the store
- Fig 10 :43-46: the maintainer is "Never a player, never a proxy, never the author of a verdict or an atom ... It does author conventions ... The seat may author what has no truth value and nothing that does."
- Fig 10 :73-74: "the pool must be unauthored first and examined second."
- Fig 11 :39-40: "capability is a property of agent-and-habitat, never of the agent alone. A system cannot be made more capable by improving the agent in isolation."
- Fig 11 :61: "Introduction is available; exclusion is not."
- READING:
  - Isaiah's guideline is Fig 11's capability claim stated from the agent's side: a newborn agent is made capable by the habitat it is born into, and the commons is that habitat.
  - Whoever curates the commons (a person, a seat, a script) sets its CONVENTIONS: the schema, the tags, the categories, which Isaiah names as "categorization". It never writes or edits entries, and never decides which entries are true. The ground does that, through the agents.
  - Nothing is removed from the commons. A refuted method gets a refusal added, and its reach falls. Fig 6 :42-46: "What is recorded only grows ... A store that deleted instead would have neither property, and could not tell never-held from held-and-given-up."

### D6: generations, and why cold-start agents still matter
- Fig 7 :33-36: "variation inside, selection between ... A room's agreement is variation, not a verdict. Selection between rooms is where the ground votes. A chain of mirrors is one long room. The next room must differ from the last, and match the residual it surfaced."
- Fig 10 :80-81: "Frames whose independence is renewed by separate experience can be maintained; frames whose correlation is fixed at origin can only be rotated, because no amount of use makes them less alike and replacement is the only refresh."
- Fig 13 :126-130: "WHY THE LINEAGE IS THE PROOF ... A term carries the atoms it was built from and the bonds that joined them. That record is not documentation of the term. It is the term." And :142: "The seed was always the seedline."
- READING:
  - Generations are the evolution lens applied directly: the lineage is the generator, each run is an instance, variation happens inside a generation and the ground selects between them.
  - Instances copied from one lineage are correlated at origin. They either renew their independence through different experience (different games and orders), or they must be rotated out for fresh ones.
  - So some FRESH, cold-start agents are part of a healthy population, not a defect. They are the only members whose evidence owes nothing to the commons, which makes them the population's independent learners (see Rogers' paradox, section 5).
  - Each generation is booked against the residual the last one surfaced, never as a copy of it.

## 4. The Ouroboros paper (v1-v4), ranged against the Tether

The paper's direction holds up, and much of it is the Tether in an earlier form. Where they differ, the Tether governs.

| From the paper | Tether verdict | Why |
|---|---|---|
| Shared persistent database of knowledge packages (5.2) | KEEP | Fig 4 :4-5, the population's shared library |
| Private memory plus network, mixed by w_i (Def 5.2) | KEEP | It is the Formula's w, almost symbol for symbol |
| w adapts by success: trust self more if private memory succeeded (5.4) | KEEP, refine | The Formula: "learnable from the outcomes of past weightings". Refine: per kind, and debit imports (Fig 6 :24) |
| Success must be externally verifiable, RLVR (Assumption 5) | KEEP | Fig 1 :23 "The ground enters as the only metric"; Fig 2's anchor |
| Stage-5 meta-packages by anti-unification / MDL (7.3) | KEEP | Fig 4: methods cross up, compressed; Fig 5 :45, the same MDL bargain |
| Resonance: roles that independently discover the same pattern score high (7.4) | KEEP, tighten | Fig 8 :50, convergence is corroboration at maximum independence. Tighten: "independent" is proven by provenance (the discoverer had not read the package), not assumed from different roles |
| Role specialisation: pioneer, optimizer, generalist (3.3) | KEEP the idea, change the basis (mapping corrected in the 11:20 audit) | It maps onto Fig 3's chain: Q1 "what is changing vs fixed" is perception; Q3 "what happens if I interact with X" is vocabulary, "what things afford" (Fig 3 :7), tested causally; Q2 "what punishes / rewards me" feeds the objective, "what would count as progress" (:10); Q4 is learn-and-carry. The paper has NO planning link (Fig 3 link 4), a gap to fill. Specialise by WHICH LINK an agent's residual sits at, read from the ledger, not by a fixed role |
| Fixed role parameters (initial w 0.7, budgets 1000/200/500/300; query rates 1%/10%/30%/5%; pariah tolerance 80/30/0%) | KEEP the self-determination, REPLACE the hand-set starting values (revised 10:58, section 4b) | The values were starting points, then learned. The figures object only to the hand-set start (Fig 10 :48). Fig 10 :76 names an unauthored replacement: "a lottery". Draw each new agent's starting w and tolerance from the population's own current spread |
| Credibility by use-and-outcome votes, up when useful, down when not, plus decay (5.3; Isaiah 10:58) | KEEP, refine (REVISED 10:58; my first verdict, REPLACE, was wrong) | Each vote is an outcome the ground returned in some agent's game, so it IS a ground settlement: Fig 7 :35, "Selection between rooms is where the ground votes". Refine against two known failures: count outcomes per TRIAL, not totals (Salganik et al. 2006), and weight votes by independence through provenance (Fig 8 :51). Section 4b |
| Packages carrying actions and positions: "ACTION6 at position (31,2) when color_14 present" (6.3); "ACTION6 tends to help on this level" (6.2) | SPLIT (revised 11:08): KEEP inside a ROOM working on one question; REPLACE in the COMMONS | Isaiah 11:08: "not conducive to learning on an individual agent basis in a generalized way, its only conducive to solving a mutual problem COLLECTIVELY faster". Inside a room, recordings are working state: "Inside a run the arrangement persists and nothing is re-earned" (Fig 12 :109). Across the membrane they are recordings, not methods (Fig 4 :23-26), so only the distilled method crosses up. Section 4c |
| Pariah patterns, shared in the same lane as positive knowledge, whose toxicity decays (5.5; Isaiah 10:58) | KEEP, decay as RE-TEST priority (REVISED 10:58) | Same lane: Fig 5 :54-56, "A term that refuses another pays the same bargain ... Same mint operator, same three guards". Decay is NEEDED: an option you avoid is never retried, so no new evidence can ever arrive (the hot stove effect, Denrell & March 2001). The Tether form: decay lowers a refusal's weight until it becomes worth RE-TESTING (a probe). The record never leaves. Reach returns only if the re-test pays and settles a new term, which is growth (Fig 6 :45-46). This answers Fig 6 :47's open case, "a world that changed". Section 4b |
| Valence engine: valence held at two levels, the agent's own and the collective's, with each agent holding them in different amounts (4.2; Isaiah 10:58) | KEEP the concept, refine (REVISED 10:58; my first verdict, REPLACE, read it as one stored value per stimulus) | Fig 11 :49-51: valence is relative to a residual, never a fixed property of a stimulus. With two residuals (Fig 4: each scale has its own loop and anchor), a stimulus carries a valence for each, and w blends them (the Formula). The paper's "valence drift" (11.3) is not a failure when the two agents differ in residual or in blend; that is what Isaiah's clustering reads off. It IS a finding when two agents give opposite valence to the same actor for the SAME residual: a contradiction for the ground to settle, not a personality (11:20 audit). Section 4b |
| Package author field "for prestige tracking" (Def 5.3) | REPLACE the prestige use; KEEP the author as provenance (11:20 audit) | "evidence bearing on the residual is admissible; evidence bearing only on its maker is a stake-inducing channel, and the verifier is denied it" (Fig 9 :51). Who made an entry may be read only to decide whether a vote is INDEPENDENT of it, never to weight the entry by its maker's standing |
| Maturity-aware queries: cold start exact-match only, mature abstraction-first (11.4) | KEEP as a reading, derive the thresholds | Right shape; "3+ diverse wins" is a constant. Derive it from w and the independent-settlement count |
| Strongly consistent central database (Assumption 1, 11.1) | KEEP, and it is more than a convention (revised 11:08) | For a population working on ONE question, the shared substrate is the room. It lets many agents try many things against one ground without re-sweeping what another already swept (Fig 6 :49-50, Fig 7, Fig 10 :71-72). Isaiah's example: the Navier–Stokes result (section 4c). The one limit stands: the database is never the ground (Fig 2 :47); the ground is the checker of the question |
| Cold start is "unavoidable (Plato's Cave phase)" (11.4) | KEEP | Isaiah 10-22: "like asking a newborn to take the mcat". And it is where the population's independence comes from (D6) |

## 4b. Isaiah's corrections (10:58 CDT), and what WATSON says about them

Isaiah, verbatim: "the collective validated the credibility by using what the other agents found. if it was useful it was upvoted essentially or downvoted to a point its never referenced etc, but there was also decay as well in case the idea ever needed to be tried again because the environment changed ... you have to examine pariahs in the same lane. because species have natural predators and competitors for resources. they can be both prey and predator etc. ... residuals exist on multipe levels, the residual of the collective vs the residual of the individual agent. the valence came from the adherence of both or hold both in different amounts which can cause unique agents that you can cluster and group".

**1. Credibility by votes on outcomes: my REPLACE was wrong; KEEP, with two refinements.**
- I read "usage × success" as counting how often an entry was used. Isaiah's mechanism counts what HAPPENED when it was used. That vote comes from the ground in the user's game, so it is a ground settlement: "Selection between rooms is where the ground votes" (Fig 7 :35).
- Refinement A, per trial rather than totals. In an experimental music market, stronger social influence "increased both inequality and unpredictability of success" (Salganik, Dodds & Watts 2006, Science 311). The entries tried most collect the most votes, so ranking by vote TOTALS locks in early leaders whatever their quality. Use the outcome RATE per trial, and keep some trials on entries that have been tried little.
- Refinement B, independence. A vote from an agent that derived the entry on its own counts more than one from an agent that tried it because it ranked high (Fig 8 :51; Lorenz et al. 2011). Provenance carries the difference.
- Refinement C, indexed by context, not one global rate (11:20 audit). "The residual is indexed by object slot, not aggregated ... Aggregating across slots is how a live signal disappears into an average" (Fig 1 :19, :22). At population scale the slots are the kinds of residual an entry is used against. A method that pays strongly in one kind of situation and fails in others must not be drowned by a pooled rate: its outcome rate is kept per kind of residual, and one live context keeps it alive (Fig 1 :13).
- The votes are the ground's; the credibility SCORE built from them is frame-internal (Fig 1 :24-27, "credibility accrued" does not count). It is a filter for what to try first, never the population's measure of success, which stays on the ground (section 6, item 13).
- "Downvoted to a point its never referenced": compatible with the Tether as long as the entry stays in the record and only its reach falls (Fig 6 :42-46).

**2. Decay: WATSON supports Isaiah, and it fills a gap my draft left.**
- In the social-learning tournament, "the most successful strategies" weighed information by its AGE (St Andrews summary of Rendell et al. 2010), because the environment kept changing.
- The hot stove effect (Denrell & March 2001, Organization Science 12(5)): a learner that avoids an option after a bad outcome never samples it again, so the avoidance can never be corrected. My draft said a refusal is lifted "only by new evidence", but avoidance PREVENTS new evidence. Without decay, a refusal is permanent by construction, which is the paralysis Isaiah built decay to prevent.
- A population fixes this better than one agent can. Conformist social learning with a weak minority influence produced "collective behavioural rescue", where the group kept re-trying what individuals had wrongly given up (Toyokawa & Gaissmaier 2022, eLife 11:e75308). Isaiah's per-role pariah tolerance (exploiters 80%, generalists 0%) is that minority: a few agents keep testing what the rest avoid.
- THE TETHER FORM: decay lowers a refusal's WEIGHT over time until re-testing it is worth a probe. The refusal stays in the record. If the re-test pays, a new term is settled ("the world changed"), and reach comes back through growth, as Fig 6 :45-46 requires. If it fails, the refusal is re-confirmed and its weight restored. Fig 6 :47 leaves "a world that changed" open; decay-driven re-testing is a mechanism for it.
- WHICH refusal to re-test first (11:20 audit): rank by the curiosity drive's own quantity, "the gap that is large and compressible" (Fig 5 :18, :46-47), not by age alone. Age only lowers the weight.
- The decay RATE is not set by hand: "a convention nothing can check is a constant the seat authored" (Fig 10 :48). It is derived from how often the population's re-tests actually find "the world changed"; a world that changes often earns fast decay.
- Decay applies to POSITIVE entries' standing as well: "standing is a stake that survives the outcome it was earned on" (Fig 10 :61). An old high-ranked method keeps its rank after the world moves unless its votes age too.

**3. Pariahs in the same lane, and predator and prey: the Tether agrees.**
- Same lane: "A term that refuses another pays the same bargain ... Same mint operator, same three guards, same bargain. Only the direction of the residual differs" (Fig 5 :54-56). Negative knowledge is shared, voted and decayed through the same path as positive knowledge.
- Predator and prey: "The same actor is a benefactor to one residual and a malfactor to another, so mutualism and parasitism are relations rather than kinds" (Fig 11 :50). One species is prey to one and predator to another, so a pariah is "bad for THIS residual", never bad in itself.
- WATSON: animals learn what to fear from others cheaply. Monkeys acquire a fear of snakes by watching another monkey's fear (Mineka and Cook's experiments), and humans learn fear by observation through the same amygdala circuit as direct experience (Olsson & Phelps 2007, Nature Neuroscience 10). Socially learned avoidance is the most self-sealing kind, because nobody who avoids ever tests it. So shared pariahs need decay even more than private ones.

**4. The valence engine with two levels of residual: KEEP the concept. My REPLACE read it as one fixed value per stimulus, which is not what it was.**
- The Tether has residuals at two scales. Fig 4 :19-20: the same loop at each size, "Only the actors, the currency and the anchor change". So there is an agent residual and a population residual, each with its own anchor.
- Valence is relative to a residual (Fig 11 :49). A stimulus therefore has a valence for MY residual and a valence for THE COLLECTIVE'S residual, and the agent's w blends them (the Formula, b mixed from private history and inherited prior by w).
- WHAT "THE COLLECTIVE'S RESIDUAL" MEANS (11:20 audit; it decides whether this holds): what the population's methods fail to predict when agents meet their OWN grounds, indexed by kind. It is ranged against the ground at population scale (outcomes of reuse across agents' games). It is NEVER the collective's consensus. Adhering to what the collective believes would be Fig 2's collapse 1, "each updates on the others ... what they converge on is whoever had the most influence" (:13-15). Adhering to the collective's residual is adhering to what the population has measured against the world.
- Unique agents follow directly. "Two frames with identical architecture diverge because their histories and their w diverge" (the Formula, -:25-26). Clustering agents by how they blend the two levels is Isaiah's manual grouping, made automatic.
- The limit (11:20 audit): divergence is healthy when agents differ in residual or in blend. Two agents giving opposite valence to the same actor for the SAME residual is a contradiction, and it goes to the ground to settle (Fig 6 :47; the agent's 3a DIAGNOSE), not into a cluster. The paper's own example, red as danger for one agent and reward for another, needs this test before it is called personality.
- WATSON:
  - Animal personalities. Stable individual differences, "behavioral syndromes", are found across species (Sih, Bell & Johnson 2004, TREE 19). Life-history trade-offs favour their evolution (Wolf, van Doorn, Leimar & Weissing 2007, Nature 447).
  - Self against others, as a stable individual trait. In wild birds, individuals hold consistent producer (find it yourself) or scrounger (take others' finds) tendencies, which covary with sociability and learning speed (Aplin & Morand-Ferron 2017, Proc. R. Soc. B, "Stable producer–scrounger dynamics in wild birds"). Individual differences in how much people rely on social learning are a recognised field of study (Mesoudi, Chang, Dall & Thornton 2016, TREE, "The evolution of individual and cultural variation in social learning").
  - The producer–scrounger game is frequency-dependent: scrounging pays less as more agents scrounge. So the population's mix of self-reliant and crowd-reliant agents can regulate itself instead of being set as a ratio. That is the "regulatory engine" the paper left open (13.4), with a mechanism.
- The magic numbers: the starting values were hand-set, then learned. Only the hand-set start conflicts with Fig 10 :48. Fig 10 :76 names the unauthored alternative, "a lottery": draw each new agent's starting w and tolerances from the population's current spread of learned values. Different agents then start differently with no one choosing how.

**Net effect on the design (section 6 updated):** credibility by per-trial outcome votes with provenance weighting; refusals shared in the same lane, decaying into re-tests; valence per residual at two levels, blended by w; starting values drawn, not set; the self-and-crowd mix regulated by frequency dependence.

## 4c. Isaiah, 11:08: the shared substrate as the ROOM for one question (the Navier–Stokes case)

Isaiah, verbatim: "think back to the navier stokes solution. it was solved via multi agent systems. it was required because the substrate of the shared info let them try alot of things against the ground of the problem to find the fitness which was the answer collectively. evolution pays in bodies and does the same thing that why this works. its not useful for an individual agent but when there is multiple agents its useful. the parallel is the shared room from the tether for a particular question." And on action packages: "its only conducive to solving a mutual problem COLLECTIVELY faster."

**The case, as reported (September 2026; still being checked).**
- OpenAI reported that roughly 10,000 autonomous agents on an unreleased model reached a proof for the Navier–Stokes Millennium problem in about 88 hours, exchanging about 2.7 million messages. A separate step took about 17 more hours to formalize it in Lean, a machine proof checker (Quanta; Simon Willison; Tufts Daily).
- Its status is preliminary. The Clay Institute recognizes a solution only after peer-reviewed publication and vetting, and priority is disputed: the approach leaned heavily on Córdoba and Martínez-Zoroa's earlier work, and a parallel human-and-AI team (Buckmaster, Alpöge) published neighbouring results.
- The reports do not describe how the agents shared state, so the design reading below does not depend on that detail.

**Against the Tether: it supports Isaiah, point by point.**
1. **The room is a function of the question.** "The room composition is a function of the question. When the question changes, the room should change" (Fig 10 :71-72). A shared substrate for ONE problem is the room. It does not have to be general, because it serves one question and closes with it.
2. **Evolution pays in bodies, and the Tether prices them.** "Bits price the description. Actions price finding out whether it holds ... the budget is what decides how much of the space is reached at all" (Fig 12 :126-127). Many agents buy many tests per hour. That is the third reachability question, "more search at the same reach: is it in here and unfound? ... Distribute the search, and keep the searchers independent" (Fig 6 :49-50).
3. **Why it worked: the answer was in the closure.** "Unreachable-at-budget: the term is already in the closure and was not found, so the remedy is more search, not another atom" (Fig 8 :41-42). The proof built on existing mathematics (Córdoba and Martínez-Zoroa's approach, an import from outside the agents). The swarm's job was the search inside that closure, and a shared substrate is what makes ten thousand searchers one distributed search rather than ten thousand re-sweeps: "Fails by spending budget on a region already swept" (Fig 6 :50).
4. **The ground settled it, not the agents' agreement.** Lean is the anchor: "pinned: it does not update on A or B" (Fig 2 :25). "A room's agreement is variation, not a verdict. Selection between rooms is where the ground votes" (Fig 7 :35). The breeder's equation in Fig 7, R = h² × S (:26), reads directly: S is the checker's pressure, h² is how faithfully a partial result passes between agents through the substrate. Zero either and the room runs in place (:37-39). Lean made S sharp.
5. **Who uses it and to what end, as Isaiah says, the Tether also covers.** Inside the room, everything is working state, recordings included (Fig 12 :109, "Inside a run the arrangement persists and nothing is re-earned"). When the room closes, only the reapplicable method crosses up to the population's library: "Only methods cross up" (Fig 4 :22). Provenance decides credit, which the priority dispute shows is not a formality (Fig 8 :51; Fig 10 :62-66).

**Three refinements from the 11:20 audit, applied to the case.**
- WHAT A ROOM IS, at the right scale. A room is not a third scale. It is ONE question's run at the agent scale, carried out in many bodies at once: "evolution pays in bodies". That is why recordings are legal inside it: "Inside a run the arrangement persists and nothing is re-earned" (Fig 12 :109). Fig 4's membrane sits between the room and the commons. A single agent's game is a room of one body, and the same membrane applies to it.
- WHAT A POPULATION OF ONE KIND BUYS. Agents sharing one core library share their atoms, so their closures differ only in what each has composed. Together they buy SEARCH inside one closure, which is exactly what Navier–Stokes needed (point 3). They do not buy REACH: "No frame escapes its own closure. The bound moves only on contact with a frame whose closure differs" (Fig 6 :23). A new atom needs a member with a different closure: different priors or instruments, a corpus, or a human's prior work, as Córdoba and Martínez-Zoroa's was here.
- THE QUESTION ITSELF. The Lean statement is the room's sought-for shape written down as an ordinary term, which Fig 5 :65-66 asks for ("Write down what an answer would look like, bind it"). Whether it is the RIGHT question is outside the room: "check the direction of the question separately, because this figure cannot see it" (Fig 5 :67-68). The reports note that humans must still confirm the Lean statement matches the intended problem. That check is this line, in practice.

**One point of pushback, from the Tether and WATSON together.** A room only beats one agent if its members stay different. "Searchers drawing on the same evidence are one searcher wearing many names" (Fig 6 :53), and "A chain of mirrors is one long room" (Fig 7 :36). Agents that read each other's partial results converge, on the outside evidence as well:
- in human groups, social influence narrowed estimates without making them more accurate (Lorenz et al. 2011);
- in model debate, agents settled into "degeneration of thought" (Liang et al. 2023).

So a room's substrate needs a rule that keeps variation inside: agents start from different points (drawn, per section 4b) and are not all steered to the current best partial result. How the Navier–Stokes run handled this is not in the reports.

**Net effect on the design: two stores, not one.**
- **The ROOM**, one per question, opened when the question opens and closed with it. Agents working that question share EVERYTHING there, action recordings and partial results included, to solve it together faster. The room's ground is that question's checker (for ARC, the game). Its record is kept with provenance after it closes.
- **The COMMONS**, across questions. It holds only methods distilled from closed rooms, settled by the ground and carried up through the membrane, ranked by per-trial outcome votes weighted by independence (section 4b). It is what a newborn agent inherits.
- The membrane between them is Fig 4's: recordings stay in the room; methods cross up; head starts come down.

**Isaiah's boundary on this (11:13), verbatim:** "only on the collective multiagent system is this possible but the architecture structure like shared info, communication, decay, etc have to be there in order for it to work. this doesnt all of a sudden mean that our singular agent can share with itself direct answers, its just that collectively you can store way more data in a different external form than one agent can hold alone".
- **THE ROOM IS A POPULATION-SCALE STRUCTURE ONLY.** It needs the collective infrastructure: a shared substrate, communication, outcome votes and decay. Without those, the handoff fidelity in Fig 7's R = h² × S is zero, and "Zero either and the chain runs in place" (:37).
- **THE SINGLE AGENT GETS NO ROOM.** One agent carrying answers from its own past games is a recording replayed downward, "a system that repeats a past success and cannot produce a new one" (Fig 4 :25-26). Today's agent therefore keeps the rule it has: its lineage carries methods only (kinds, templates, canonical forms), with no action traces, game ids or answers (E8 Q2 checks this). Its working state inside one game is ordinary in-run memory, not a room, and it does not cross the game boundary as a recording.
- **WHY THE COLLECTIVE CAN DO WHAT ONE AGENT CANNOT:** capacity, held in a different, external form. The room is the population's external memory, larger than any member's and outside every member. That is Fig 11's point that capability belongs to agent-and-habitat, never the agent alone (:39-40). The room is part of the habitat, and it exists only where a population maintains it.

## 5. Outward witnesses (WATSON)

The outside literature converges with the reading above on four points: copying pays only when it is selective; individual learners must remain; crowds lose their wisdom once members watch each other; and the reliability of the crowd versus the self is tracked and learned, not fixed.

- **Animal behaviour and evolution, why copy at all.** Rendell et al. 2010 (Science 328, 208-213), "Why copy others? Insights from the social learning strategies tournament". Strategies that relied heavily on copying won, partly because the agents being copied had already filtered what was worth doing. That is Fig 4's "verified, compressed" upload rule seen from outside.
- **Evolution, why the population still needs self-reliant learners.**
  - Rogers 1988 (American Anthropologist 90): when everyone copies, copying stops raising the population's fitness in a changing world, because nobody is tracking the change any more.
  - Enquist, Eriksson & Ghirlanda 2007 (American Anthropologist 109, "Critical social learning: a solution to Rogers's paradox of nonadaptive culture"): the fix is the CRITICAL social learner, who copies first and switches to learning on its own when the copied behaviour fails.
  - That is the paper's "self-directed exploration when network sequences fail" (6.2), and it is the w loop: a failed import moves w toward self.
  - Laland 2004 (Learning & Behavior 32), "Social learning strategies": "copy when uncertain" and "copy if better" are the strategies animals use. They are rules for setting w from the agent's own uncertainty and the source's record.
- **Human crowds, independence is the whole effect.**
  - Lorenz, Rauhut, Schweitzer & Helbing 2011 (PNAS 108(22), 9020-9025), "How social influence can undermine the wisdom of crowd effect": once people saw each other's estimates, their answers narrowed without getting more accurate, and their confidence rose. That is Fig 2's collapse 1, measured.
  - Bikhchandani, Hirshleifer & Welch 1992 (Journal of Political Economy 100(5)), information cascades: agents who follow predecessors' choices instead of their own signals lock a population onto a choice its private evidence does not support. That is the usage-ranked commons failure.
  - Henrich 2004 (American Antiquity 69(2), 197-214), demography and cultural evolution, the Tasmanian case: a population that is too small or too cut off LOSES skills over generations, because there are too few skilled models to learn from. The commons must never drop a method, and its effective size is its number of independent learners, not its number of copies.
- **Neuroscience, how a brain weighs self against others.** Behrens, Hunt, Woolrich & Rushworth 2008 (Nature 456, 245-249), "Associative learning of social value": people track how reliable another person's advice has been, separately from how reliable their own experience has been, and combine the two by those learned reliabilities, in distinct brain circuits. That is a per-source, learned w.
- **AI systems.**
  - Population-based training (Jaderberg et al. 2017, arXiv:1711.09846): a population shares and selects working settings during training. Selection between members is by measured performance, which corresponds to the ground here.
  - Voyager (Wang et al. 2023, arXiv:2305.16291): a lifelong agent keeps a growing library of reusable, verified SKILLS (methods) rather than trajectories (recordings). That is Fig 4's rule, arrived at independently.
  - Multi-agent debate among language models suffers "degeneration of thought": agents settle on a shared answer and stop exploring (Liang et al. 2023, arXiv:2305.19118). That is Fig 7's mirror chain and Fig 2's collapse 1 again, in today's AI systems.

Where the witnesses do not reach: none of them gives the provenance rule, telling a convergent discovery from an adopted copy by the record. That is the Tether's own contribution here (Fig 8 :51; Fig 13 :126-130).

## 6. The design, in one page (nothing built)

1. **Each instance runs today's agent, unchanged** (Fig 4 :19-20). Its own lineage stays its own.
2. **Two shared stores (revised 11:08, section 4c):** a ROOM per open question, where agents share everything, recordings included, to solve that one question together; and the COMMONS across questions, described below, holding only methods distilled from closed rooms. **Both exist ONLY in a multi-agent population with the shared infrastructure (Isaiah 11:13).** A single agent has neither: its lineage carries methods only, never answers.
   **The commons, beside the lineages:**
   - Entries are methods: kinds, templates, canonical forms, recipes with their bonds, and refusals.
   - Each entry carries provenance: which instance, which generation, what kind of game, and the ground rows that settled it.
   - No action ids, game ids, positions or colours.
   - CATEGORIZATION (11:20 audit): each entry is indexed by the residual it explains, described in effect terms by arity, symmetry and scale (Fig 9 :21-22, :30-31). A lookup starts from the asking agent's own described residual, and "matching is a one-pass check, not a search" (Fig 9 :29). A commons pooled without described residuals is "the undirected union ... nothing was aimed; the union is mute" (Fig 8 :6, :19-21).
   - The public general-agent repo would hold only the core library. A commons built from ARC play is ARC-specific and lives with the ARC side (Isaiah 10-22).
3. **Up (carry):** an instance uploads an entry only after the ground settled it in its own play, compressed to its reusable form.
4. **Down (head start):**
   - An agent takes an entry as a CANDIDATE, through the import gates: provenance, and "explains a gap in MY residual" (Fig 6 :12-13).
   - It is debited against the agent's independence (Fig 6 :24).
   - Taking it is a bet; the ground then settles it in this agent's own play.
   - The gate's strictness scales with what a wrong import would cost: "Buy independence in proportion to the cost of being wrong" (Fig 2 :42). A cheap-to-test entry needs little support; one that would take many actions to refute needs several independent settlements first.
5. **Ranking (revised 10:58):**
   - Isaiah's use-and-outcome votes, up when an entry paid in a user's game and down when it did not, read as a RATE per trial, never as a total of uses.
   - Votes are weighted by independence through provenance: an instance that derived the entry without reading it counts fully; one that imported it and found it paid counts as a confirmation.
   - Some trials go to entries that have been tried little, so early leaders do not lock in.
   - Votes decay with age (section 4b), at a rate derived from how often the world was found to change.
   - The rate is kept per kind of residual, not pooled (Fig 1 :19-22).
   - An entry's outcome rate and its test cost in actions are two readings, held apart, never summed (Fig 12 :126-130).
   - The rank is a FILTER for what to try first, never a verdict: "Use filters for the budget and witnesses for the verdict" (Fig 9 :60).
6. **w, self against crowd:**
   - Learned per agent (and per kind, if Isaiah agrees) from how past weightings turned out.
   - A failed import moves w toward self, the critical social learner.
   - An import that pays where the agent's own search found nothing moves w toward the crowd.
   - A fresh agent's w is not set by hand. It starts from what the commons can show: entries with many independent settlements earn trust first, and single-source entries earn little.
7. **Refusals (pariahs) are shared in the same lane (revised 10:58).**
   - They are scoped to the residual they refuse: prey to one, predator to another.
   - Their weight decays until a re-test is worth a probe. Some agents (the high-tolerance ones) re-test what the rest avoid.
   - The record never leaves. A re-test that pays settles a new term ("world changed"); one that fails restores the refusal's weight.
8. **Valence at two levels (revised 10:58):** each actor carries a valence per residual, the agent's own and the collective's. Each agent blends them by its w, so agents differ, and their blends can be clustered into types.
9. **Starting values are drawn, not set (revised 10:58):** a new agent's starting w and tolerances are drawn from the population's current spread of learned values (Fig 10 :76, "a lottery"), then learned. The mix of self-reliant and crowd-reliant agents regulates itself, as in the producer–scrounger game.
9b. **Rooms (11:20 audit):** a room is opened for one question, with that question's checker as its ground and the sought-for answer written down as a term (Fig 5 :65-66). Its members are "summoned by the residual rather than composed", from "a pool ... unauthored" (Fig 7 :40-41): everyone who qualifies, or a lottery among them (Fig 10 :76-77). Members start from different points and are not all steered to the current best partial result (Fig 7 :36).
10. **The round trip:** for each downloaded entry, the gap between how it did where it was made and how it does here is recorded. That gap is what tells the population which abstractions travel (Fig 4 :30, :36-37).
11. **Population health:**
   - Keep instances independent: different games, orders, seeds and histories; w left free to differ.
   - Keep some fresh cold-start learners in every generation (Rogers; Fig 10 :80-81).
   - Never delete from the commons (Henrich; Fig 6 :42-46).
12. **The maintainer:** curates the commons' conventions only (schema, tags, categories) and authors no entries or verdicts (Fig 10 :43-46). It is never an agent whose own standing the commons' rank measures: "Whoever is measured by a reading cannot own it" (Fig 10 :86).
12b. **Introductions are staged (11:20 audit):** a newly uploaded entry goes to a few agents first, and its second-order effects (what else the agents then do differently) are read before it spreads: "contact cascades" (Fig 11 :52). An entry spread population-wide with its cascade unenumerated is the cane-toad move (Fig 11 :65). The drawn spread of w (item 9) already does most of this.
12c. **The same design one scale up (11:20 audit):** a whole population, with its commons, is one member at the next scale (populations of populations; the paper's 13.5). The kernel is the same; only the actors, currency and anchor change (Fig 4 :19-20), and "there is no top" (Fig 4 :33). Nothing new is needed to describe it.
13. **Measures of success, all from the ground:**
    - Does a new agent born into the commons reach its first level in fewer actions than a fresh agent alone? This is Isaiah's "dumb agents become smart" claim, made testable.
    - Does that advantage hold on game KINDS the commons has never seen? That separates transfer from replay.
    - Does adding agents with DIFFERENT evidence help more than adding clones? That is Fig 6 :53-54, tested.
    - WHAT OUROBOROS SHOWED, AND WHAT THE TETHER EXPLAINS (Isaiah 13:04, 13:10, 13:15, verbatim):
      - 13:04: "ive proven it works from cold start via ouroboros v1-v4. i did not train any agents myself it was all evolution and generations and their shared mediums etc they eventually easily beat the preview games, but i didnt know how they learned what they knew and they couldnt do anything else they werent generalized and they were still black box".
      - 13:10: "the ouroboros v1-v4 just proved that collective intelligence works, not that what is learned transfers. it has nothing to do with the tether. our current agent is generalized ... it being in a collective would merely exponentially raise its affectiveness, as long as the learning is mutually shared by all participants".
      - 13:15: "it proved that the tether explained why ouroboros worked for collective intel and why it that system alone is insufficent for generalized agents (it only creates average workers who all have nearly the same capabilities (they averaged to the mean of the collective or ranged against it with their 'w'). versus, an agent that has full autonomy and control over its reasoning and can program itself (outside of the core architecture/kernel)".
      - WHAT OUROBOROS SHOWED: collective intelligence works from a cold start. No agent was trained by hand; generations and shared mediums beat the ARC-AGI-3 preview games. It came BEFORE the Tether, so it is not a test of the Tether, and it says nothing about transfer.
      - WHY IT WORKED, per the Tether (derived afterwards, partly by ranging against Ouroboros, section 8c): the ground voted between generations, "Selection between rooms is where the ground votes" (Fig 7 :35); and the shared mediums made many searchers one search (Fig 6 :49-50).
      - WHY IT IS NOT ENOUGH FOR A GENERAL AGENT, per the Tether:
        - members updating on the collective "converge, and what they converge on is whoever had the most influence" (Fig 2 :13-15);
        - members drawn from one origin are "frames whose correlation is fixed at origin" (Fig 10 :80-81);
        - a population of one closure buys search, not reach (section 4c; Fig 6 :23).
        The result is average workers with nearly the same capabilities, which is what Isaiah observed. It is the w collapse in this document's HOW TO READ note, observed.
      - WHAT THE CURRENT AGENT ADDS: autonomy over its own reasoning, and it programs itself above a fixed kernel. The kernel "does not change with size" (Fig 4 :19-20). Above it, the agent mints and invents its own terms, and "A settled molecule becomes an atom for whatever composes over it" (Fig 12 :104).
      - GENERAL, NOT UNLIMITED (Isaiah 13:15: "any is too strong. humans cant learn to grow wings"): it can learn whatever its instruments let it perceive and act on, and whatever its operators can reach.
        - "Composition explores what the operators reach; instruments extend what can be represented at all" (Fig 6 :26).
        - "MINT composes inside the closure and can never add an atom" (Fig 6 :21). Learning does not grow a new instrument, as a person cannot learn to grow wings.
        - "The bound moves only on contact with a frame whose closure differs" (Fig 6 :23).
      - So a collective of THESE agents is a magnifier on an agent that is already general within its reach. Section 8d covers how large a magnifier. The three measures above are how a Tether-built collective would be tested; none has been run.

## 7. What exists today (FOR THE PROCTOR TO CORRECT, from the code)

My reading only. Each line is to be confirmed or corrected with file:line.
- Today's agent is already a one-member population over time. Each run's lineage generation inherits from the last ("the seed was always the seedline"): kinds carry, and inventions outlive the game (M7-INV, 60d1498).
- Provenance per library entry: E8 Q23 asks whether every entry's origin (session, game, generation) can be proven. Needed before ranking by independent settlement is possible.
- w: CONFIRMED by the proctor (2026-10-22 11:34, R3): NOT IMPLEMENTED and NOT RULED. No code mixes an own-history belief with an inherited prior under a learnable weight. Isaiah's 10-01 ruling in gamma.py:756-771 ("no weighting is needed while the consumer is a tie-break"; "Revisit when RELEVANCE is built") is about whether a failure taken in another game or level weighs differently. It is a different question, and does not speak to w. Carried inventions are re-invented "on trial ... standing is earned here", which resets an inherited entry's standing rather than weighting it. w is the first piece a multi-instance step would build.
- Refusals with scope: the 3a DIAGNOSE verdicts ("world changed", "two scopes", "stale expectation") are the lifting conditions above. Confirm they are recorded per kind.
- No commons, no second instance, no upload or download path exists. Nothing in this document is to be built before Isaiah decides.

## 8. Open for Isaiah

- **OPEN 1.** w per kind of question, or one w per agent? (The formula writes one w; the brain witnesses track it per source and per context.)
- **OPEN 2.** Where does a commons built from ARC play live: in the planned "Arc Solver Agent" repo, private, beside the ARC lineage?
- **OPEN 3.** Population health: how many fresh learners per generation? I would derive it rather than set it: add fresh learners while the population's independent-settlement rate is falling.
- **OPEN 4.** When does this get built: after Kaggle, as the first step of the general agent's next phase?

## 8b. The single-agent safety fixes, and their population-scale forms (Isaiah 12:37-12:40)

Before the freeze, three single-agent fixes go into today's agent (Isaiah 12:37: "we need the single agent versions of those fixes in place"). Each has a population-scale form, which belongs here and not in the build. Today's only population is the Kaggle runner's K workers, which are separate copies of the agent, one per core, each forking the lineage. Their forms are held for the Kaggle step, and in a true multi-agent system they would be the commons' forms.

| Concern | Single agent (before the freeze) | Population form (Kaggle runner now; a multi-agent system later) | Tether line |
|---|---|---|---|
| A move that never ends | The agent reads its OWN deadline at every loop that grows with the board, and records "unreached at this budget", never a verdict | An OUTSIDE wall: the runner (or the maintainer) ends a member that overruns, records its task as cut, and the rest of the population keeps its time | Fig 9 :60, filters for the budget, never a verdict; the clock is the ground's wall, not the agent's anchor (budgets derivation) |
| A crash in the agent's own machinery | Record it in the agent's own grammar; save only if the state passes the checks; DISCARD the possibly half-updated agent and load a fresh one from the last valid save; carry on in the same game; the same fault twice ends the game | The population survives a member's failure: the member's task is recorded as faulted, its checked learning is kept, and a fresh member (or the next task) goes on. In a commons, a member that keeps faulting is a refutation of ITS state, never of the commons | Fig 10 :24, "the ground does not decay, the channel does"; :28-29, "you have lost touch -> keep the anchor reachable"; Fig 6 :42-46, nothing deleted, reach recomputed |
| Memory | The agent's own budget, min(8 GiB, half the RAM, the container limit), with soft and hard folds (W, built and proven) | A SHARED, finite resource: each of K members gets min(8 GiB, RAM/(2K)), so the population as a whole never asks for more than the habitat holds | Fig 13 :13-14, energy is "conserved, finite"; Fig 11, members are each other's habitat and competitors |

A note on the K workers: each forks the lineage and learns alone, with no commons between them. So the Kaggle runner today is a population of K separate frames with no shared room. That is safe, since none can pull the others into coherent drift, but none learns from the others during the run. Whether their K forked lineages are merged afterwards is a Kaggle-step question (the parked runner refactor), not an agent one.

## 8c. An agent on a loop is a population in time (Isaiah 12:40)

Isaiah, verbatim: "an agent on a loop, is not too dissimilar to a multi agent system ((non-linearly) as its dynamic, but their ability to range against their past self is limited and only benefits with wide gaps between start and current - does that make sense?"

It does. The Tether says why it is limited, and why a wide gap helps.
- **A past self is another frame, and a weak one.** Independence is "how little they draw on the same evidence" (Fig 2 :31). The current self carries everything the past self saw ("What is recorded only grows", Fig 6 :42). So a recent past self shares almost all its evidence with the present one, and agreement between them is "the pool talking" (Fig 2 :20-21). Its closure also sits inside the present one's, so there is no union surplus to draw on: it cannot hand back an atom the present self lacks (Fig 6 :23; Fig 8 :48-49, "Two frames that overlap almost completely are one frame wearing two names").
- **Why a wide gap helps.** Two things grow with the gap.
  - DRIFT: a long run of small updates can carry the whole self somewhere coherent and wrong, which only a comparison with a distant earlier self can show. That is Fig 4's round trip: "take the round trip and measure the gap. Without it you are navigating by dead reckoning" (:30).
  - REACH THAT WAS GIVEN UP: reach is not monotone, and the present self may have refused terms the earlier self could still compose over (Fig 6 :41-46). A distant past self is where abandoned reach can be found again, which is the same job decay-driven re-testing does (section 4b).
  - What a past self can never be is the ground: "A ground listed as one of the parties has already become a frame" (Fig 2 :47). It is a vantage point, not a verdict.
- **WATSON, it holds across fields:**
  - STATISTICS. Consecutive states of a running process are autocorrelated. Samples only count as roughly independent when they are spaced further apart than the process's autocorrelation time, which is why sampled chains are thinned. Fig 2 :44 names the same arithmetic, "the effective-sample-size correction for correlated observations". A gap wider than the agent's own autocorrelation time is what turns a past self into a second frame.
  - EVOLUTION. Time-shift experiments pit hosts against parasites from past, present and future time points (Gaba & Ebert 2009, TREE). Resurrection studies revive dormant eggs from dated lake sediment (Decaestecker et al. 2007, Nature, Daphnia and its parasites). Adaptation that is invisible when contemporaries meet shows up when time-separated populations are compared. The time gap is the instrument.
  - AI. AlphaStar trained in a LEAGUE that kept past versions of itself as opponents, so the current agent could not forget how to beat old strategies or cycle between them (Vinyals et al. 2019, Nature). The past selves in the league were chosen to differ, not just the most recent ones.
  - HUMANS. People rate distant past selves as worse than recent ones and so perceive more improvement across wider gaps (temporal self-appraisal, Wilson & Ross 2001). It is a reminder that a self judging its own past is not the ground: the comparison needs an anchor, or it flatters.
- **The ship of Theseus (Isaiah, 12:42).** Verbatim: "its the reason why both ships are the ship of thesseus. when viewed non-linearly they both exist. only in terms of time does it seem like a paradox, when the answer is just one was the ship of thessesus, and the other also the ship but is in use currently. I had to range against my past self to get this tether theory derived".
  - The Tether locates identity in the lineage, not in a single timeline: "A term carries the atoms it was built from and the bonds that joined them. That record is not documentation of the term. It is the term" (Fig 13 :130).
  - The rebuilt ship is the ship read by its parts (the original planks and their record). The ship in use is the ship read by its arrangement carried forward (continuous repair, the same role): "The arrangement is the substance" (Fig 12 :94).
  - Both lineages are traceable. The paradox appears only when both are forced onto one line of time with one owner of the name. Viewed non-linearly they are two branches from one seed: "If levels were copies there would be one lineage drifting and no branches. The tree of life is what a non-invertible transform looks like from outside" (Fig 10 :70).
  - Isaiah's own derivation of the Tether, from Ouroboros v1-v4, is a wide-gap comparison of this kind: the earlier self is a real second frame only because of the distance.
- **Refinement.** "Wide gap" can be measured instead of guessed. The useful distance is wide enough that the two selves no longer draw on the same evidence, past the autocorrelation time, and the anchor stays the ground, never either self.

## 8d. How much does a collective magnify an agent? (Isaiah 13:15)

Isaiah, verbatim: "i cant quantify it but its a magnifier on its current intelligence im sure there are studies or research that might have caculated 'how much smarter' or how much better peformance'. i bet GPUs and RAM mathmatics about CORES would apply here or provide you the mathematical analogues." His condition (13:10): "as long as the learning is mutually shared by all participants".

There is no single number. Parallel computing and statistics give the SHAPE, and each term has a Tether line. N members:

| Analogue | Formula | What limits the gain | Tether line |
|---|---|---|---|
| Independence (Kish 1965, effective sample size) | N_eff = N / (1 + (N−1)ρ); ρ = how alike the members' evidence is | A ceiling of 1/ρ however many join; clones (ρ = 1) count as one | Fig 2 :44, "the effective-sample-size correction for correlated observations"; Fig 6 :53-54, "one searcher wearing many names" |
| Fixed problem, work shared (Amdahl 1967) | S = 1 / (σ + (1−σ)/N); σ = the share only one member can do at a time | A ceiling of 1/σ | Reading: Fig 3's links are ordered by dependency, so a link waiting on the one before is serial work |
| The problem grows with the team (Gustafson 1988) | S = N − σ(N−1) | Grows in step with N, because more members search a LARGER space rather than the same one faster | Fig 6 :49-50, "more search at the same reach ... Distribute the search"; the Navier–Stokes room (4c) |
| Sharing has a cost (Gunther 2008, Universal Scalability Law) | C(N) = N / (1 + σ(N−1) + κN(N−1)); peak at N* = √((1−σ)/κ) | κ = the cost of keeping every member coherent with every other. Past N*, adding members makes the group WORSE | Fig 4 :9, carry up a method "compressed to its essentials"; the room/commons split (4c) |

Readings:
- **"Mutually shared by all participants" is both the precondition and the κ term.** If every member synchronises every other member's raw state, the exchanges grow as N². The design keeps κ small in two ways:
  - only compressed methods cross into the commons (Fig 4 :9, :22);
  - full sharing is confined to one room, for one question (4c).
  This is why a commons of methods can scale where a shared database of recordings would choke.
- **In headcount, the magnifier is at most linear.** It grows in step with N at best (Gustafson), in practice it is bounded (Amdahl, Kish), and past a peak it declines (USL). Isaiah's "exponentially" is not a property of headcount.
- **Where compounding lives: across generations.** Each settled method becomes an atom the next generation composes over (Fig 12 :104). Re-deriving it "is a lookup and the actions were spent once" (Fig 12 :107-110). That is compounding in time, the cumulative-culture ratchet.
  - Witnesses: larger groups maintain more complex culture and improve it more often (Derex et al. 2013, Nature 503:389-391); too small or cut-off populations lose skills (Henrich 2004, section 5).
  - If growth is exponential anywhere, the analogues place it in generations, not in members. [reading; not measured]
- **What measurements show:**
  - Human groups. A single collective-intelligence factor c explained roughly 30-50% of group performance across tasks. It was NOT strongly predicted by the members' average or maximum intelligence; it tracked social sensitivity and equal turn-taking (Woolley, Chabris, Pentland, Hashmi & Malone 2010, Science). The arrangement, not the members: "The arrangement is the substance" (Fig 12 :94).
  - LLM agents. Performance rises with agent count under simple sampling-and-voting, by an amount that depends on task difficulty (Li et al. 2024, TMLR, "More agents is all you need"). In networked collaboration it follows LOGISTIC growth with agent count, a rise and then a plateau, and irregular networks beat regular ones (Qian et al. 2024, ICLR 2025, MacNet). Logistic growth is the rising part of the USL shape: a magnifier with a ceiling.
- **So the magnifier's size is set by the population's own quantities:** independence ρ, the serial share σ, the cost of coherence κ, and time, through which settled work compounds. None is a constant to set; each is measurable on a running population. This is the same rule as the budgets derivation: the agent's own rates, never magic numbers.

## 9. The whole document run through all thirteen figures and the Formula (11:20 CDT audit, Isaiah 11:14: "run your whole doc through all the tether figures collectively and recursively")

Method:
- Each figure is applied to the design at BOTH scales (the agent, and the population), and then to THIS DOCUMENT as a frame. That is the recursive pass: Fig 4 :19-20 says the same rules hold at every size.
- A finding that changed the body is marked with the section it changed.
- "Holds" means the figure was checked and the design already met it.

| Fig | Checked against | Result |
|---|---|---|
| 1 | Per-slot residual; no self-scored success | FIXED: credibility rate kept per kind of residual, not pooled (4b, item 5); the credibility score is a filter, never the success measure (4b) |
| 2 | Anchor; the two collapses; independence; cost of being wrong | FIXED: "the collective's residual" defined against the ground, never consensus (4b point 4); import gate scales with the cost of being wrong (item 4). Holds: the database is never the ground |
| 3 | The dependency chain | FIXED: the paper's question-to-link mapping corrected; the paper lacks the planning link (section 4 table). Holds: order of domains; roles by which link a residual sits at |
| 4 | The membrane; no top | FIXED: a room is one question's agent-scale run in many bodies, and the membrane sits between room and commons (4c); the same design recurs one scale up (12c). Holds: methods up, head starts down, round trip |
| 5 | The mint bins; curiosity; refusal in the same lane; the direction of the question; settled is not usable | FIXED: re-test priority uses the curiosity drive's quantity, not age (4b point 2); the room's question written as a term, its direction checked outside (4c). Holds: refusals in the same lane. Noted: commons growth is not reach growth (Fig 5 :72), so success stays on the ground (item 13) |
| 6 | Closure, import, recorded-only-grows, the third question | FIXED: a population of one core library buys search, not reach; new atoms need a member with a different closure (4c). Holds: no deletion; import debited against independence; Fig 6 :47 answered by re-test-then-growth |
| 7 | Room chain; R = h² × S; summoned, unauthored rooms | FIXED: room membership summoned by the residual from an unauthored pool (9b). Holds: variation inside; the ground votes; zero handoff fidelity means no progress |
| 8 | Union surplus; provenance; the mute union | FIXED: commons indexed by the residual each entry explains, so the union is aimed (item 2). Holds: provenance separates convergence from copying |
| 9 | Describe the residual first; filters vs witnesses; what the verifier may see | FIXED: author kept only as provenance, never as prestige (section 4 table, Fig 9 :51); rank is a filter, never a verdict (item 5) |
| 10 | The maintainer; constants; standing; who may hold the seat | FIXED: decay rate derived, not set; decay also ages positive standing (4b point 2, Fig 10 :61); the maintainer is never measured by the commons (item 12). Holds: conventions only; lottery for starting values |
| 11 | Habitat; valence relative to the residual; cascades; substituted habitats | FIXED: staged introductions (12b); opposite valence on the SAME residual is a contradiction, not a personality (4b point 4). Holds: capability is agent-and-habitat; measures on real grounds only |
| 12 | Bonds; two currencies; settling and the boundary the record does not cross | FIXED: Fig 12 :107-110 added as the core reason a commons pays (D2+D3); outcome rate and test cost held apart (item 5). Holds: methods carry their bonds |
| 13 | Lineage as proof; unreachable as a verdict | Holds: provenance per entry; "no entry explains this residual" is a reportable shape that tells an agent to look outside |
| Formula | b, w, divergence | Holds: w is the self-against-crowd weight, learned; divergence by history and w. OPEN 1 (w per kind) stays open |

The recursive pass, with the figures applied to this document itself:
- **Fig 2, collapse 1, on my own revisions.** I reversed three verdicts after Isaiah pushed back, which is the pattern collapse 1 warns about: a frame moving toward whoever has the most influence. Each reversal was checked for what drove it.
  - Credibility: Isaiah corrected a FACT about the mechanism (votes on outcomes, not counts of use), and Fig 7 :35 then decides it.
  - Decay: an independent witness, the hot stove effect, which I had not considered, plus Fig 6 :47's open case.
  - Valence: Fig 11 :49 plus Fig 4's two scales.
  - None rests on deference alone. Where I had over-accepted, the audit pulled back: valence drift on the same residual is a contradiction, not a personality; "the collective" is its residual against the ground, not its consensus.
- **Fig 8 / Fig 2, the independence of my witnesses.** They come from separate fields and methods: laboratory crowds, a field study of birds, an agent tournament, an organisational learning model, brain imaging, archaeology and AI systems. One is weaker than the rest: the claim that the tournament's best strategies weighed information by its age comes from a university press summary, not from the paper itself, which was unreachable this session. It is marked so.
- **Fig 10 :42, :50-52, the reviewer's seat.** The document makes no verdict about today's code; section 7 is left to the proctor to correct from the code. Its claims about the world (the Navier–Stokes case) are reported with their status: preliminary, priority disputed.
- **Fig 1 :24-27 / Fig 5 :48-49, on the design's own success.** The measures in item 13 are all read from the ground: actions to the first level, transfer to unseen KINDS, different evidence against clones. None is a count of entries, votes or mints.
- **Fig 9 :30, the residual in section 1.** Stated in effect terms; the lf52 number is now marked as taken beside a stray process.

Verdict: after the fixes above, no figure is contradicted by the design. Strained: none. Open: OPEN 1-4 (section 8).

## Sources
- Nwukor, I. (2026). Role based Multi-Agent Reasoning Frameworks. IJCA 187(78). (attachment)
- [Rendell et al. 2010, Why copy others? (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2989663)
- [Lorenz et al. 2011, How social influence can undermine the wisdom of crowd effect (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3107299)
- [Rogers' paradox and Enquist et al. 2007, critical social learning (Mesoudi tutorial)](https://bookdown.org/amesoudi/ABMtutorial_bookdown/model18.html)
- [Behrens et al. 2008, Associative learning of social value (Nature)](https://www.doi.org/10.1038/NATURE07538)
- [Henrich 2004, Demography and cultural evolution: the Tasmanian case (Cambridge)](https://cambridge.org/core/journals/american-antiquity/article/abs/demography-and-cultural-evolution-how-adaptive-cultural-processes-can-produce-maladaptive-lossesthe-tasmanian-case/8CD08CC61E6FACF59EC02659B2BDA43C)
- [Wang et al. 2023, Voyager (arXiv)](https://arxiv.org/abs/2305.16291v2)
- [Liang et al. 2023/2024, Encouraging divergent thinking through multi-agent debate (ACL Anthology)](https://preview.aclanthology.org/setup/2024.emnlp-main.992)
- [Salganik, Dodds & Watts 2006, inequality and unpredictability in an artificial cultural market](https://www.cs.toronto.edu/~bor/303s19/docs/salganik_dodds_watts.pdf)
- [St Andrews news on Rendell et al. 2010: the most successful strategies weighed information by its age](https://news.st-andrews.ac.uk/archive/the-art-of-copying/)
- [Denrell & March 2001, Adaptation as information restriction: the hot stove effect](https://ideas.repec.org/a/inm/ororsc/v12y2001i5p523-538.html)
- [Toyokawa & Gaissmaier 2022, conformist social learning and collective behavioural rescue (eLife)](https://pubmed.ncbi.nlm.nih.gov/35535494/)
- [Olsson & Phelps 2007, Social learning of fear](https://pubmed.ncbi.nlm.nih.gov/17726475/)
- [Aplin & Morand-Ferron 2017, Stable producer–scrounger dynamics in wild birds](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5394662/)
- [Mesoudi, Chang, Dall & Thornton 2016, The evolution of individual and cultural variation in social learning](https://ore.exeter.ac.uk/repository/handle/10871/19047)
- [Quanta, Sept 2026: AI has solved one of math's Millennium Prize problems](https://www.quantamagazine.org/ai-has-solved-one-of-maths-1-million-millennium-prize-problems-20260908/)
- [Simon Willison, Sept 2026: Some thoughts on the Navier–Stokes Millennium Prize Problem](https://simonwillison.net/2026/Sep/8/on-navier-stokes/)
- [Tufts Daily, Sept 2026: Mathematicians still checking the Navier–Stokes proof](https://www.tuftsdaily.com/article/2026/09/mathematicians-still-checking-the-navier-stokes-proof-that-openai-claims-to-have-solved)
- [Gaba & Ebert 2009, Time-shift experiments as a tool to study antagonistic coevolution](https://edoc.unibas.ch/5711/)
- [DeepMind 2019, AlphaStar: Grandmaster level in StarCraft II using multi-agent reinforcement learning](https://deepmind.google/discover/blog/alphastar-grandmaster-level-in-starcraft-ii-using-multi-agent-reinforcement-learning/)
- [Temporal self-appraisal (Wilson & Ross 2001), summary](https://concepts.dsebastien.net/concept/temporal-self-appraisal/)
- [Kish 1965, Survey Sampling: design effect and effective sample size (summary)](https://en.wikipedia.org/wiki/Design_effect)
- [Gunther 2008, A general theory of computational scalability based on rational functions (USL)](https://arxiv.org/abs/0808.1431); [USL explained, WSO2](https://wso2.com/blog/research/scalability-modeling-using-universal-scalability-law)
- [Woolley et al. 2010, Evidence for a collective intelligence factor in the performance of human groups (summary)](https://acawiki.org/Evidence_for_a_collective_intelligence_factor_in_the_performance_of_human_groups)
- [Derex, Beugin, Godelle & Raymond 2013, Experimental evidence for the influence of group size on cultural complexity, Nature 503](https://ideas.repec.org/a/nat/nature/v503y2013i7476d10.1038_nature12774.html)
- [Li et al. 2024, More agents is all you need (TMLR)](https://arxiv.org/abs/2402.05120v1)
- [Qian et al. 2024, Scaling large language model-based multi-agent collaboration (ICLR 2025)](https://arxiv.org/abs/2406.07155v3)
- Cited from standing knowledge, not fetched this session: Amdahl 1967, AFIPS Spring Joint Computer Conference; Gustafson 1988, Communications of the ACM 31(5), "Reevaluating Amdahl's law"; Decaestecker et al. 2007, Nature (Daphnia–parasite resurrection); Bikhchandani, Hirshleifer & Welch 1992, JPE 100(5); Laland 2004, Learning & Behavior 32; Jaderberg et al. 2017, arXiv:1711.09846; Sih, Bell & Johnson 2004, TREE 19; Wolf et al. 2007, Nature 447; Mineka & Cook's observational fear-conditioning studies in rhesus monkeys.

## Figure census
- Bearing: Fig 4 :4-5, :9, :19-20, :22-26, :30, :36-37; Fig 2 :13-21, :40, :47; Fig 6 :12-13, :24, :42-47, :53-54; Fig 8 :50-52; Fig 1 :23-27; Fig 7 :33-36; Fig 10 :43-48, :67-68, :73-74, :80-81; Fig 11 :39-40, :49-51, :61; Fig 12 :104; Fig 13 :126-130, :142; the Formula's symbols (b, w).
- Added 10:58: Fig 7 :35 (votes are the ground's); Fig 5 :54-56 (refusals in the same lane); Fig 6 :45-47 (re-test then growth; a world that changed); Fig 11 :50 (predator and prey); Fig 10 :76 (a lottery); Formula -:25-26 (divergence by w).
- CORRECTIONS, owned: three first-draft verdicts (credibility, pariah decay, valence) were too strict. Isaiah's account of what the mechanisms did, and the witnesses, moved each from REPLACE to KEEP-and-refine.
- Added 11:08: Fig 10 :71-72 (the room is a function of the question); Fig 6 :49-50, :53 (distributed search; searchers on one evidence pool are one searcher); Fig 8 :41-42 (more search, not another atom); Fig 7 :26, :35-39 (R = h² × S; the ground votes); Fig 2 :25 (the pinned anchor: Lean); Fig 12 :109, :126-127 (inside a run; actions price testing).
- Added 11:20 (the audit): Fig 1 :13, :19-22; Fig 2 :13-15, :42; Fig 3 :7, :10; Fig 4 :33; Fig 5 :18, :65-68, :72; Fig 6 :23; Fig 7 :40-41; Fig 8 :6, :19-21; Fig 9 :21-22, :29-31, :51, :60; Fig 10 :61, :76-77, :86; Fig 11 :52, :65; Fig 12 :107-110, :126-130. All thirteen figures and the Formula are now checked (section 9).
- Added 13:04-13:15 (Isaiah on Ouroboros, generality and the magnifier): Fig 2 :13-15, :44; Fig 4 :9, :19-20; Fig 6 :21, :23, :26, :49-50, :53-54; Fig 7 :35; Fig 10 :80-81; Fig 12 :94, :104, :107-110. Amdahl's row in 8d rests on a reading of Fig 3, not a verbatim line.
- CORRECTION, owned (13:04-13:15): the first versions said the group approach's benefit was unshown. They then framed the Tether as fixing Ouroboros's gaps. Isaiah: Ouroboros proved collective intelligence works and is not a test of the Tether; the Tether explains why it worked and why it is insufficient for a general agent.
- Single-source: w per kind (OPEN 1).
- Strained: none.
