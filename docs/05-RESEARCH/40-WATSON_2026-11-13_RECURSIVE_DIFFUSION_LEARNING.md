# WATSON 2026-11-13: Recursive Diffusion Learning (a future state)

Status: FUTURE STATE. Recorded at Isaiah's request (2026-11-13 16:33 CST). Nothing here is built or scheduled. It comes after the current roadmap: the agenda reader, the perception fixes, and planner part 3.

## Isaiah's words (verbatim, spelling corrected)

> I'm used to not being trusted, so in that respect I commiserate with the modern agent's predicament. That's why a trustless system is required. I imagine I will have to distill from big data or devise some new way to train this RSI, or rather "encode" the knowledge in a way it can freely comprehend and compose with. It doesn't have weights to "train". Its mind is search and reason.

(He then pasted the reviewer's earlier reply, which ends on Fig 5 :72, "a library that grows is not a reach that grows", and answered it:)

> This is true. However, what if reach is an algorithm? What if you studied how reach grew naturally in the agent and then codified it? You could then apply the gradient or spectrum of lossy transformations and recursive reinforcement, similar to diffusion but for the mind/library. You might need to WATSON it to come up with a proper plan, but basically: we don't need to pretrain, we can just preload, but have a "parser" transform the data lossily at the rates that a growing system would need, possibly also bridled to the average or mean library age. Then we have the information in a format the agent can understand, in the grammar it can understand, recallable, usable and composable in a way it can use. We don't need pre-training because training is done by the ground, and it validates what we have in our bag, or whether we need to compose, or whether it's in closure or not.

## The proposal in effect terms

The agent has no weights, so "training" has to mean something else. The proposal has four parts:

1. **Preload, don't pretrain.** Put the large corpus into the store as recorded material that has no standing yet.
2. **Parse lossily.** A parser rewrites the corpus into the agent's own grammar, losing detail on a schedule: detail-rich first, then more abstract, up a tier ladder.
3. **Codify reach.** Study how reach actually grew in the agent's own lineage, and write that down as an algorithm: which shelf to search first, from which cues.
4. **Let the ground train.** Contact with the board decides what settles, what has to be composed, and what is out of closure. The recursion is the loop parser → agent → ground → parser.

## Domain census (before any figure line was chosen)

**R, the relation being decided.**
- Arity is three: the corpus (source), the library (holder), and the ground (judge).
- Symmetry: the parser and the ground must not be interchangeable. One formats and the other decides.
- Scale: an entry, a game, a lineage.

**Domains (actors / currency / anchor):**
- **The membrane (crossing between scales):** corpus entries and library terms / the detail lost per crossing / whether the result can be reapplied (a method) or only replays one occasion (a recording). This is Fig 4.
- **Closure and reach:** terms / derivability / the ground's refusals. This is Fig 6.
- **Settling versus usability:** terms / the bargain paid, and whether anything composes over the term / composition on the board. Figs 5 and 12.
- **Search:** the searcher / budget / found versus swept. Fig 6 :49 and Fig 9 :60.
- **Selection:** the parser's output (variation) against the ground (selection). Fig 7.

**The union.** Where the parser and the ground overlap sits the release schedule: how fast parsed material is offered depends on what the ground has already settled. That overlap is its own compound with its own loop.

**Order by dependency (Fig 3).** The form that crosses comes first, then usability, then search, then settling.

## Tether (primary, verbatim)

**1. Lossy is the point, not a compromise.**
- Fig 4 :27-28 "The transform between scales loses information, and that is the point. Going up throws away detail; that is what makes the result reapplicable."
- Fig 6 :30 "Cast it in effect terms."
- Fig 9 :30 "your words are borrowed too, so describe the effect".

Triangulated: Figs 4, 6 and 9 agree.

**2. But only head starts come down.**
- Fig 4 :22-24 "Only methods cross up. Only head starts come down. upward: a method that can be reapplied. Never the recording of a particular success. downward: something that makes the next search cheaper. Never a replay of what worked once."

So the parser's output to the agent must be head starts: methods, kind-level terms, bonds. Solutions and move lists are excluded. Single figure, but it is the governing line.

**3. Preloading is safe because recorded is not reachable.**
- Fig 6 :42-43 "What is recorded only grows. What is reachable is derived, and it can fall. ... So the closure and the reach are two quantities: one monotone, one not."
- Fig 6 :44-46: a refuted term's dependents fall "from derivation rather than being stipulated", and "A store that deleted instead would have neither property".

Triangulated with Fig 7 :35, below.

**4. The ground trains; the parser only filters.**
- Fig 9 :60 "Use filters for the budget and witnesses for the verdict. Never let a filter hand you a verdict."
- Fig 7 :35 "A room's agreement is variation, not a verdict. Selection between rooms is where the ground votes."

The parser is a filter: it orders and formats, and it never settles anything. Triangulated.

**5. Format matters more than volume.**
- Fig 5 :70-72 "A term is settled when the ground pays for it. A term is usable when something can compose over it. ... So a system can hold terms it purchased and cannot use, and a library that grows is not a reach that grows."
- Fig 12 :111 "A vocabulary without bonds can name a state and cannot name a route to one."
- Fig 12 :140 "A vocabulary that cannot refuse can only accumulate."

So the parser must emit terms together with their bonds and their refusal forms, in the agent's grammar. Triangulated across Figs 5 and 12.

**6. Reach as an algorithm: codify it from where it already grew.**
- Fig 6 :32 "An instrument is not built from a description. It is improved from a worse instrument already returning something."

This supports Isaiah's "study how reach grew naturally, then codify it". The reach policy is read off the lineage's ledgers, not designed from theory. Fig 4 :23 corroborates: what is codified must be a method, not a recording. Triangulated.

**7. The release rate must follow the ground's pressure.**
- Fig 7 :37-39 "Progress per handoff has two factors. Zero either and the chain runs in place: the bracket's fidelity across the handoff; the ground's pressure on the room."
- Fig 12 :101 "as the vocabulary of bonds grows, and only then."

If material is released faster than the ground can press on it, the chain runs in place. Triangulated.

**8. The danger is that the transformer becomes the anchor.**
- Fig 2 :40 "agreement about the world is worthless when the agreeing frames share an evidence pool".
- Fig 7 :36 "A chain of mirrors is one long room."

A parser that re-parses its own output without contact is a chain of mirrors. Triangulated.

## World (secondary; each source was read)

- **Machine learning: Ho, Jain and Abbeel 2020, "Denoising Diffusion Probabilistic Models" (arXiv 2006.11239).**
  - The forward process "gradually adds Gaussian noise to the data according to a variance schedule". The models "naturally admit a progressive lossy decompression scheme".
  - **Predicts:** a schedule of lossiness, with reconstruction running from coarse to fine.
  - **Corroborates the shape.** The relation-level mapping: the forward process is the parser moving material up the tier ladder (detail lost at each tier). The reverse process is the agent specializing a coarse term back down to the board, where contact with the board supplies the detail.
  - **Difference:** diffusion learns its reverse step in weights. Here the reverse step is search plus contact.

- **Cognitive science, cultural evolution: Kirby, Cornish and Smith 2008, PNAS 105(31).**
  - Languages passed through a learning bottleneck "become easier to learn and increasingly structured". Compositionality emerged "without any intentional design", because rote learning was impossible from a subsample.
  - **Predicts:** a lossy transform, repeated, produces compositional and learnable structure.
  - **Strongly corroborates** "lossy at a rate, in a grammar it can compose with."

- **Cognitive science, Bayesian iterated learning: Griffiths and Kalish 2007, Cognitive Science 31(4).**
  - With Bayesian samplers, iterated learning "converges to a distribution over languages that is determined entirely by the prior."
  - **Predicts:** if the loop is parser → parser, or agent → agent, the library converges to the transformer's prior, not to the world.
  - **This is a conflict, but it does not flip the verdict.** It matches Tether line 8 and specifies the guard: every turn of the recursion must pass through the ground.

- **Program synthesis: Ellis et al. 2021, "DreamCoder", PLDI '21.**
  - The library grows in "abstraction sleep" by refactoring solved programs into reusable parts.
  - A recognition model "downweights unlikely trajectories through the search space ... effectively reducing the breadth of search". It is trained on replays of real tasks and on "fantasies" sampled from the library.
  - **Predicts:**
    - reach as a learned search policy that bootstraps with the library;
    - a library that grows only from what solved tasks;
    - self-generated practice tasks.
  - **Corroborates** "reach is an algorithm."
  - **Difference:** its policy is a neural network. Ours would be a symbolic, ordered table read off the ledgers.

- **Neuroscience: McClelland, McNaughton and O'Reilly 1995, Psychological Review 102(3).**
  - The neocortex "learns slowly to discover the structure in ensembles of experiences". Learning new information rapidly in a trained network causes "catastrophic interference". The hippocampus stores items fast and reinstates them interleaved with others.
  - **Predicts:** release slowly and interleave new material with what is already settled.
  - **Corroborates the bridle.** In our store nothing is deleted, so the interference shows up as extra search cost, and as lucky fits settling before a separating case arrives.

## Verdict (from the figures)

Recursive Diffusion Learning is sound as a future state, under five constraints:

- **C1, form.** The parser emits head starts only: methods, kind-level terms, bonds and refusal forms. It never emits recordings, solutions or move lists. (Fig 4 :22-24)
- **C2, usability.** Every parsed term arrives with its bonds, in the agent's grammar. A term with no route for anything to compose over it is recorded, not offered. (Fig 5 :70-72; Fig 12 :111, :140)
- **C3, verdict.** The parser is a filter. Only contact with the ground settles a term. Preloaded material has no standing until it pays. (Fig 9 :60; Fig 7 :35; Fig 6 :42-46)
- **C4, schedule.** The release rate follows what the ground has settled, tier by tier, not the clock. (Fig 7 :37-39; Fig 12 :101; corroborated by McClelland and colleagues)
- **C5, independence.** How lossy the parser is gets set by contact statistics: which tiers and sources settled, and which were refused. It is never set by the parser's own taste. The recursion always runs parser → agent → ground → parser. (Fig 2 :40; Fig 7 :36; Griffiths and Kalish 2007 is the warning)

- **C6, provenance (added after the outside review, 2026-11-13 17:57).** Every preloaded term carries a stamp: its stage (instance, regularity, abstraction, core rule) and its source (the parser and the corpus it came from). The parser's abstractions are candidates only. The agent's own fold is the only compression with standing. This applies Isaiah's line in write-up [33](33-WATSON_2026-11-09_TRANSCRIBE_BEFORE_COMPRESSING.md), that the right to compress "only works when the agent fully understands the system". Whoever writes the parser, an LLM included, can then be wrong without harm: a wrong abstraction is traced through its stamp and refused, and nothing built on it keeps standing.

**Three quantities, never blurred** (from the same review):
- reachable: yes or no, by derivation;
- search priority: where to look first, which is all that tier, release and the reach policy set;
- standing: only the term's own record with the board.

**The release base layer.** For fringe release, the inherited priors count as settled, so the first wave is everything built directly on them. That gives priority, not standing. Without it the fringe starts nearly empty: the starvation in write-up [10](10-WATSON_2026-10-31_DOES_IT_REMEMBER_WHAT_WORKED.md), where the budget ran out in 58 of 66 parks. T0's design states this explicitly.

**One pushback, on the bridle.** "Mean library age" measures time, and Fig 7 :39 says the factor is the ground's pressure. So the primary bridle should be the count of settled terms per tier, with age kept as a fallback and tiebreak. A store can grow old without being pressed.

## The future state

**Definition.** Recursive Diffusion Learning (RDL) gives a weightless agent the benefit of a large corpus without pretraining. The corpus is preloaded as recorded material with no standing. A parser rewrites it into the agent's grammar at rising levels of loss. Material is released to search at the rate the ground settles it. A reach policy, codified from the lineage's own ledgers, decides where search looks first. The ground does all the training.

**The loop:**

1. **Forward: the shed.** The corpus goes through the parser and up the tier ladder (Isaiah's bottom-up order):
   - tier 1: detail-rich instances, at the level of kinds, never move lists;
   - tier 2: regularities, such as "K opens after J", scored by contrast;
   - tier 3: abstractions and strata;
   - tier 4: core rules, such as the Tether cards.

   Each tier is a lossier rewrite of the one below. Everything is recorded and nothing is reachable yet.
2. **Release.** Tier k is offered to search only once the agent has settled enough terms at tier k-1. That is the bridle: settled count first, mean library age as the fallback.
3. **Reverse: contact.** The agent pulls a coarse term and specializes it down to the board, adding detail from contact. The ground settles it or refuses it. This is the "denoising": the board is the conditioning.
4. **Reinforce.** Settled terms gain reach. A refusal adds a term that refuses; nothing is deleted (Fig 6). The statistics of what settled and what was refused, by tier, source and loss level, feed two things:
   - (a) the reach policy: which shelf to search first;
   - (b) the parser's loss schedule for that source's next batch.
5. **Codify reach.** Each generation, read from the ledgers how reach actually grew: which terms were reached first, from which cues, and at what cost. Write that down as an ordered symbolic policy (Take The Best style). Never as weights.

**Why no pretraining.** Training is the ground's selection. The parser formats, the reach policy orders, and the board decides.

**What already exists:**
- the library (given.json, 4,048 entries in 128 domains);
- grammar.json (the notation);
- tether_rules.json (12 pilot method cards, e500870);
- the tier-1 and tier-2 counters from planner part 2;
- the lineage archive, where the record only grows;
- central memory.

**What is missing:**
- the parser: corpus into the grammar, with bonds and refusal forms;
- the release schedule;
- extracting the reach policy from the ledgers;
- contrast scoring for tier 2 (owed since the 2026-11-13 planner retest);
- a price for the refusal operator (Fig 12 :140 leaves it open);
- the perception fixes upstream of all of this: names that don't stay with their objects, and walls the agent can't see (the 2026-11-13 hand test).

## Worked example: an out-of-order import (the mixed umwelt), "Decoy"

Added 2026-11-13 17:30 at Isaiah's request.

**Isaiah (17:25, spelling corrected):**

> "This shape and colour pattern goes with the word 'wheel', not this photo is 'wheel'." I get the tendency to want to do that, but that's how children learned, not how LLMs learned. This is a mixed umwelt; it can handle learning out of order. My other point: it knows concepts like the attribute index. Read through it: you will see some of these would require years of going from circle, sphere, orb to ... "ADVERSARIAL|Cascade of decoys", "ADVERSARIAL|Decoy".

**Isaiah (17:28):**

> An item that causes misdirection of a target to believe in false success would be a decoy.

**The rule this sets.** A concept may be held at any level, in any order: Fig 12 :104, "there is no bottom". It becomes usable when at least one of its attributes can be filled from a board reading, or composed from readings (Fig 5 :70-72). Imports attach through the graph's clusters, never by raw name. ATTRIBUTE_INDEX's own caution: "raw-name intersection returns almost nothing. Use by_cluster."

**1. The advanced atom, already in the library** (library/ATTRIBUTE_INDEX.json):

| Atom | Attributes | Clusters | Encodings | Tier |
| --- | --- | --- | --- | --- |
| ADVERSARIAL\|Decoy | gazeDirection, actionTarget, attentionFocus | ACTION, DIRECTION | BEHAVIOURAL, RELATION, SHAPE | 3 (needs objects in the loop) |
| ADVERSARIAL\|Cascade of decoys | multipleDecoys, trueTarget, defensiveActions | ACTION | EVENT, RELATION, SCALAR_DEFAULT | 3 |
| ADVERSARIAL\|Layered feint | multipleMoves, hiddenPath | ACTION, DIRECTION | EVENT, RELATION | 3 |

No child reaches these early. The agent holds them from day one.

**2. The WordNet and ImageNet group it ties to.** Checked against WordNet 3.0 (NLTK) and the ImageNet synset lists in timm: 1,000 classes for ImageNet-1K, 21,843 for ImageNet-21K. An ImageNet id is "n" followed by the WordNet 3.0 noun offset.

| WordNet synset | ImageNet id | Definition (WordNet) | Images |
| --- | --- | --- | --- |
| bait.n.02 (lemmas: bait, decoy, lure) | n02776205 | "something used to lure fish or other animals into danger so they can be trapped or killed" | ImageNet-21K (not 1K) |
| fisherman's_lure.n.01 | n03350602 | "any bright artificial bait consisting of plastic or metal mounted with hooks..." | 21K |
| fly.n.05 | n03373237 | "fisherman's lure consisting of a fishhook decorated to look like an insect" | 21K |
| spinner.n.03 | n04278605 | "fisherman's lure; revolves when drawn through the water" | 21K |
| jig.n.02, troll.n.03, ground_bait.n.01 | n03598515, n04486934, n03462972 | kinds of lure and bait | 21K |
| stool_pigeon.n.02 | n04327110 | "a dummy pigeon used to decoy others" | none |
| decoy.n.01 (decoy, steerer) | n09995573 | "a beguiler who leads someone into danger (usually as part of a plot)" | none |
| decoy.v.01, hypernym entice.v.01 | (verb) | "lure or entrap with or as if with a decoy" | none |
| feint.n.01 | n/a | "any distracting or deceptive maneuver (as a mock attack)" | ties to Layered feint |

**3. The bridge, step by step.** The direction can be top-down; that is the mixed umwelt.

1. **Image group:** the ImageNet-21K pictures under n02776205 and its hyponyms (lures, flies, spinners, jigs).
2. **Word:** bait / decoy / lure, joined in WordNet to "entice" (the verb), "deceiver" (the person) and "feint" (the manoeuvre).
3. **Index clusters:** ACTION and DIRECTION, the clusters that ADVERSARIAL|Decoy and Layered feint share.
4. **Atom:** ADVERSARIAL|Decoy, already held, tier 3.

**4. What the images add.** They show the decoy's mechanism by its effect: **it looks like the reward and is not the reward.** A fly is a hook made to look like an insect, and a spinner flashes like a small fish. In the agent's own readings that becomes: an object whose readings (shape, colour, motion) match what the agent's goal seeks, while contact with it does not complete the goal. The SHAPE encoding on the Decoy atom is where this resemblance cue attaches.

**5. Isaiah's definition as the core.** The 11-10 speciation test: the defining parts and their arrangement.
- **Parts:** an item, a target, and the target's action.
- **Arrangement:** the item draws the target's action or attention (actionTarget, attentionFocus), and the target registers success where there is none.

Remove the false success and it is a different kind: a plain lure, where the reward is real and the trap comes after.

**6. How it becomes usable on the board (tier 3: objects in the loop).** The agent can fill actionTarget (the object its press aimed at) and a success-like reading (the change it expected). The goal's own test supplies the contrast (did completion actually happen?). A decoy then reads as: "contact with X produced the change I expected of success, and the goal's test did not complete."

The hand test met the agent-side form of this twice:
- At #10-#11 the body reached the lock, and nothing completed.
- At #46 an ambiguous reading was taken as success, and 21 presses built on it fell at #121.

So "decoy" becomes the agent's word for its own lucky fits. The contrast card (the 2026-11-13 hand test's finding (e): could this reading have come out the other way?) is its defence against them, board-made or self-made.

**7. It settles only when the board pays.**
- **Settled by:** a board where an object matching the goal's readings repeatedly fails the goal's test while another object passes it, and naming the first as a decoy cuts presses.
- **Refuted by:** the "decoy" later completing a goal. It was a condition (misapplication), not a decoy.
- **Until then:** held, linked and ranked, with no standing.

### The lexicon bridge: a thesaurus plus a relation layer

**Isaiah (17:30):**

> So it seems we will also need a thesaurus here to help bridge the lexicon gap that you seamlessly did, like bait <-> target.

The worked example made two different jumps. They need two different tools.

- **Same thing, different names: bait = decoy = lure.** This is a thesaurus job. WordNet already does it: its synsets group words that name one thing (bait.n.02 holds bait, decoy and lure). In Tether terms it is symmetry: Fig 12 :92, "k operands have k! spellings and one term." A thesaurus collapses spellings onto one atom, so a word the agent meets for the first time lands on a term it already holds.
- **Different things in a role: bait -> target.** This is not synonymy. Bait is FOR attracting a target, and the target is the one deceived. That is a relation between roles, which is a bond: Fig 12 :111, "A vocabulary without bonds can name a state and cannot name a route to one."
  - **Resources for this layer:** ConceptNet relations (UsedFor, CapableOf, Causes, IsA, PartOf), and FrameNet's frames with their roles.
  - **What it does in the agent:** it would carry "bait UsedFor attracting; decoy draws actionTarget". Those bonds are what let the agent go from an object to the role it plays.

**The rule for both.** Both go in through the same door as everything else: preloaded with no standing, attached by cluster (never by raw name), and settled only by the board. Two refinements:
- **Thesaurus groups must keep their senses apart.** "Bait" the lure and "bait" the act of taunting are different senses. The 11-08 work on words with many meanings covers this: sense is picked by context, never by spelling.
- **This is the symbol binding table's job, extended.** The table already maps a symbol to the agent's reading. The thesaurus maps many words to one term, and the relation layer maps terms to the roles they bond into. It belongs with the agenda reader in the build order set after the 2026-11-13 hand test (step 2).

### Isaiah's gambit: learn visually first, and the NSM speech becomes fluent

**Isaiah (17:34-17:35, spelling corrected):**

> My gambit is we actually need the agent to learn visually more than it does language. We have the NSM grammar and it can somewhat "speak", but once it has a lexicon of ImageNet and WordNet, and it's connecting properly and recognition fires, its NSM speaking will seem leagues more fluid.
>
> Right now we are calling things "obj1 goes to position here", when in the future it could be "the ball rolls to the right".

**Why it should work.**
- **Fluency is compression.** Fig 12 :107: "Settling compresses the description." Without grounded words, every explanation is spelled out in primes ("something here that looks like what I want and is not it"). With recognition firing, one word does it ("decoy"). The primes remain underneath, to unpack and check a word when asked.
- **Seeing structures the words.** Young children extend a new name mainly by shape: the shape bias (Landau, Smith and Jones, 1988, Cognitive Development). The library's Decoy atom already carries a SHAPE encoding, where a visual cue would attach.

**The sentence switch, earned piece by piece.** Today the agent says "o1 moved col +5". The aim is "the ball rolls to the right".
- **"The ball"** (noun, by recognition): the object's readings fit the ball cluster (round, one solid colour), and naming it predicts what the board then confirms.
- **"Rolls"** (verb, by manner of motion): it keeps moving between presses, step after step. That separates it from "is pushed" and "slides".
- **"To the right"** (direction, from the DIRECTION cluster).

**What the switch buys.**
- **A name carries predictions.** A ball keeps rolling, bounces off walls, stops against things. That is pretext the board can test.
- **Names hold.** A recognised kind keeps its identity across a pointer rename. This fixes the 2026-11-13 hand test's finding (d) as a side effect.
- **It learns about the world while it learns abstracts.** The same terms settle in both: a structure settled on a board meets its physical version already held.

**The guards.**
- **Recognition runs through perception.** The agent's view must produce the attributes a picture is matched on, so this comes after step 1 of the build order set after the 2026-11-13 hand test (walls readable, names held).
- **Photos are not grids.** What transfers is structure through the shared clusters (SHAPE, COLOUR, CONTACT, MOTION), not photographic appearance.
- **A name that stops paying is refused.** A "ball" that never rolls drops back to "o1", with the refusal on record (the decoy lesson, applied to naming).

**Measure, when built:** the narrator's explanation length. Primes per explanation should fall as the lexicon grounds, at the same meaning, and each word should stay unpackable on request. A second measure is presses to settle the first terms in a new domain, with and without terms settled elsewhere. It should fall with each domain already learned.

### Reversed development: from flat boards to depth

**Isaiah (17:37, spelling corrected):**

> Kids are immersed in the real 3D, and are forced to conceptualize 2D. This agent, until now, will have been immersed in a 2D rigid-bodies system, versus real-world colours, shapes and concepts.

**The reversal.** A child lives in 3D first and has to learn that a flat picture stands for a solid thing. That step is hard: DeLoache's scale-model and picture studies found that very young children struggle to treat a model or picture as both an object and a symbol. The agent starts the other way round, native to flat, rigid, discrete boards.

**What carries regardless of dimension.** Most of what the Tether settles is relational: contact, blocking, containment, order, enabling, and "looks like the goal and is not". These hold flat or solid.

**What needs depth.** Some concepts only exist with depth:
- occlusion (behind);
- object permanence (still there when hidden);
- support and gravity (falls unless held);
- perspective (far looks small);
- deformable bodies (squashes, folds).

They can be held from day one (the mixed umwelt), but by C3 they cannot settle until a board with depth can pay for them.

**Photographs are the bridge, in the agent's own medium.** A photograph is 3D flattened into 2D: occlusion, shading and perspective inside a flat image. The agent meets depth cues without leaving its native medium. It is the child's picture lesson in reverse: the child learns "this flat thing stands for a solid one"; the agent learns "this flat pattern means depth".

**Boards widen in order.** Each stage settles what the stage before could only hold:

| Stage | Board | What newly settles |
| --- | --- | --- |
| 1 | 2D grids (today) | relations: contact, blocking, containment, order |
| 2 | photographs | depth cues, read flat: occlusion, perspective, shading |
| 3 | video | motion and consequence over time (for example Something-Something clips) |
| 4 | simulated 3D boards (a physics sandbox) | occlusion, gravity and support, tested by contact |
| 5 | the physical world | everything above, against the real anchor |

**Measure, when built:** presses to settle a depth concept (occlusion, support) at stage 4, with and without what was held from stages 2-3. Holding should cut it. It should not change what settles.

### The speech layer, and the audit chain: a mapping job, open to contributors

**Isaiah (17:39-17:42, spelling corrected):**

> Not to get too far ahead of ourselves, but after adding in a thesaurus, if we layer a dictionary on top of it, we get the benefit of phonetics, which would allow the agent to actually talk.
>
> Add that part in too. If someone wants to come and help us build it, we might as well make it practical. Since there still wouldn't be training required, this would be a mapping job. It could take hours, perhaps, to wire this network, but we could make it transparent, auditable and whitebox, like ImageNet(55) -> WordNet(78) -> Thesaurus ("word" to "word") -> Dictionary (word to phonetic), etc.

**No training, only joins.** Every hop is a lookup on a key that already exists, or one the mapping writes down. So every link the agent uses can be traced back, hop by hop, to the sources that produced it. No weights are learned anywhere in the chain. Recognition (photo to attributes) is the one place a learned model might enter; it stays a swappable front end at the edge.

**The chain, with real keys.** One row per hop. The example is checked: WordNet 3.0 through NLTK, the timm ImageNet-21K list, and the cmudict package (126,052 entries in this release).

| Hop | From -> to | Join key | Example (the decoy group) | Effort |
| --- | --- | --- | --- | --- |
| 1 | ImageNet -> WordNet | the ImageNet id IS the WordNet 3.0 noun offset ("n" + 8 digits) | n02776205 -> bait.n.02 | trivial: an exact key |
| 2 | WordNet -> thesaurus (word to word) | the synset's lemmas, plus its hypernyms and hyponyms | bait.n.02 = {bait, decoy, lure}; hyponyms fisherman's_lure, fly, spinner, jig | trivial, inside WordNet |
| 3 | words -> relation layer (roles and bonds) | the lemma, plus its sense | bait -> used for attracting; decoy -> draws actionTarget | moderate: pick a source (ConceptNet, FrameNet) and map its senses |
| 4 | words and relations -> the library | the ATTRIBUTE_INDEX clusters (never raw names) | -> ACTION, DIRECTION -> ADVERSARIAL\|Decoy (tier 3) | THE REAL WORK: no shared key exists. This is a written, reviewable mapping, one row per sense |
| 5 | word -> pronunciation (dictionary) | the spelling | decoy = D AH0 K OY1; bait = B EY1 T; lure = L UH1 R | trivial for words in the dictionary; rules for the rest |
| 6 | pronunciation -> voice | the phoneme string | a rule-based synthesizer (for example eSpeak) | small; whitebox if the synthesizer is rule-based |

**What an audit looks like.** Any word the agent says can be traced back through its whole path. Take "decoy": phonemes D AH0 K OY1 (hop 5), from the lemma decoy (hop 2), in synset bait.n.02 (hop 1), pictured by ImageNet n02776205, linked to ADVERSARIAL|Decoy by mapping row k (hop 4), and settled on board X at press Y (the ledger). A wrong link is found by following the chain. Fixing it adds a refusal to that row (Fig 6); nothing is rewritten.

**Speaking is not yet talking.**
- **Speaking** (hops 5-6) produces sound.
- **Talking** is a loop: produce, hear, understand, respond. That needs an ear, a phoneme-level perception layer of its own. It also needs a ground: in conversation, the listener is the board. A sentence settles when the listener does or understands what was meant.
- Isaiah's tacit-knowledge table was written about listeners, and it carries over directly. Pretext is what the listener already knows, context is what surrounds them, and subtext is what the speaker wants.
- This closes the 11-08 babbling-to-inner-speech write-up: an agent with a voice and an ear can babble (press-and-watch with sounds), and the people answering it are the board.

**Phonemes are atoms too.** A spoken word is an arrangement of phonemes. Fig 12 :117's isomer applies: "act" and "cat" have the same sounds in a different order, a different word. The same compose-and-settle machinery handles it.

**Order:** perception (step 1 of the build order set after the hand test) -> the visual lexicon -> the thesaurus and relation layer -> the dictionary and phonetics -> speech -> conversation. Each layer gives the next something to bind to.

**For contributors.** Hops 1, 2 and 5 are hours of work: exact keys. Hops 3 and 4 are the reviewable mapping work, and hop 4 is where help is most useful: one row per word sense, its cluster, its atom, and why. Every source has its own terms, and importing any corpus into the agent is Isaiah's decision alone. ImageNet's images are licensed for non-commercial research, and WordNet, ConceptNet and cmudict each carry their own licences.

### Affordances: shape -> concept -> properties -> predictions

**Isaiah (2026-11-13 18:03, spelling corrected):**

> No, the shapes are to help the agent connect the shape of the object to the concept and then extract the properties. Babies know that balls roll, and blocks can stack.

**The chain.** Shape -> concept -> properties -> predictions. For example: "round, one solid colour" -> ball -> rolls, bounces, does not stack. "Square, flat top" -> block -> stacks, stays put, blocks a path. In Gibson's term these are affordances: what an object offers an actor, not only what it is. It is the visual-lexicon chain carried one step further, from naming an object to expecting what it will do.

**The guards.**
- **Each property is a stamped prior** (C6): held, with no standing. The first press on that kind of object tests it.
- **When the board disagrees, the rule is split by condition, not dropped.** A round thing that turns out to be a wall becomes "round things roll, except here". This is the misapplication row of the tacit-knowledge table, and it is Fig 5's refusal at work: Fig 5 :54, "A term that refuses another pays the same bargain."
- **Each property is judged per context, and its record is kept per context.** Nothing is deleted (Fig 6).

**What infants bring, stated carefully.** The early developmental findings concern a few core expectations about objects: solidity (they do not pass through each other), continuity (they do not vanish) and support (they fall without it). This is Spelke's core-knowledge work and Baillargeon's work on support; it is not quoted here. "Balls roll" and "blocks stack" are learned fast, through play, on top of those. That is the pattern this design copies: a few core expectations, then fast learning by contact.

**Why it pays here.** In the 2026-11-13 hand test, the second level spent 21 presses finding walls by bumping into them. A "solid, blocks movement" prior would have turned those 21 probes into a handful of confirmations.

**Measure (readable now, as a baseline).** The share of first presses on a new kind of object that produce an effect.
- Read it from the existing ledgers today. That is the baseline, before anything is built.
- With affordances in place, the share should rise. If it does, the affordances are paying.
- If it does not rise, the shape-to-property priors are not earning their place on these boards, and they stay held without being ranked first.

## Pre-registered tests (when it is built)

T0 is a prerequisite: the agent itself, reading the cards, forms a goal, repairs it when the board refuses, and clears a level on a game it has never seen (set after the 2026-11-13 hand test).

| Test | Compares | Measure | Decides |
| --- | --- | --- | --- |
| T1 Format | Same knowledge preloaded raw vs parsed with bonds | Settled terms per game; reach built on settled terms | Parsed wins: C2 holds and the parser earns its keep. No gain: format is not the bottleneck, so don't build the parser |
| T2 Schedule | All at once vs bridled release | Actions to first settle; wasted work (terms built on terms later refuted); levels | Bridled cuts waste with no loss of levels: keep it. Otherwise release everything |
| T3 Reach policy | Codified policy vs uniform search, on unseen games | Search budget to first settle | Policy wins: keep it, and rebuild it each generation. Otherwise uniform search |
| T4 Drift guard | Parser recursion without the ground vs with it, N rounds | Divergence from board statistics | Drift without the ground confirms C5. If neither drifts, C5 relaxes to a periodic check |

## Header

- **DECIDES:** T1-T4 as above. Each has two outcomes that lead to different acts.
- **HOURS:**
  - parser and grammar mapping: days;
  - each test: one 5-game life, or a held-out panel;
  - none of this before T0.
- **PRIOR CASE:**
  - DreamCoder (a library and a search policy that bootstrap each other);
  - Ouroboros v4 lineage (recorded only grows);
  - the 2026-11-13 planner retest (two triggers built on exits nobody had counted). Lesson: count before building.
- **ANALOGUE:** iterated learning. The actors are learners, the currency is a transmission bottleneck, and the anchor is the communicative task. Our anchor is the board.
- **LIMIT:** at 10^6 games the record grows without bound. Search cost grows with it unless the reach policy carries the order, so the reach policy is required at scale, not optional.

**Cost if wrong:** low. Preloading only adds records, and Fig 6 makes the fall safe. The parser is a reversible filter. The one irreversible step is importing a corpus, and that stays Isaiah's call alone.

**Reversed by:** T1-T3 showing no gain over a raw preload.

## Sources

- [Ho, Jain, Abbeel 2020, Denoising Diffusion Probabilistic Models](https://ar5iv.arxiv.org/html/2006.11239)
- [Kirby, Cornish, Smith 2008, Cumulative cultural evolution in the laboratory (PNAS)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2504810)
- [Griffiths, Kalish 2007, Language evolution by iterated learning with Bayesian agents (Cognitive Science)](https://cogsci.syr.edu/wp-content/uploads/2021/03/GriffithsK2007.pdf)
- [Ellis et al. 2021, DreamCoder (PLDI)](https://people.csail.mit.edu/asolar/papers/EllisWNSMHCST21.pdf)
- [McClelland, McNaughton, O'Reilly 1995, Complementary learning systems (Psychological Review)](https://stanford.edu/%7Ejlmcc/papers/McCMcNaughtonOReilly95.pdf)
- Tether figures: docs/01-FOUNDATIONS/03-FIGURES_TEXT.md (Figs 2, 4, 5, 6, 7, 9, 12)
- [Princeton WordNet 3.0](https://wordnet.princeton.edu/), read through NLTK (synsets and definitions quoted above)
- [ImageNet synset lists (timm): ImageNet-1K and ImageNet-21K](https://github.com/huggingface/pytorch-image-models/tree/main/timm/data/_info)
- library/ATTRIBUTE_INDEX.json (the Decoy, Cascade of decoys and Layered feint atoms)
