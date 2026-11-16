# WATSON 2026-11-16: Recursive Diffusion Learning, the design (builds on 40)

Status: PARTLY BUILT. This write-up carries [40](40-WATSON_2026-11-13_RECURSIVE_DIFFUSION_LEARNING.md) forward. Write-up 40 set out the idea and its constraints (C1-C6) as a future state. On 2026-11-16 the first layers were built, and the design gained the layers that go from a board pattern to a word, a concept, its actions and back to the board. Everything 40 says still holds. This page says what was built, what was added, and the whole design in one place. The interfaces are fixed in `docs/03-DESIGN/RDL_BUILD_SPEC_2026-11-16.md`.

## Isaiah's words (2026-11-16, spelling corrected)

> There is no next session. RDL, recursive diffusion learning, matters most to me, so start working on it.

> ImageNet shouldn't require training at all. If you look at write-up 40 you will see that no pretraining is needed. That's what makes Recursive Diffusion Learning cool and fast.

> I will eventually want the agent to fully leverage the entire dataset of ImageNet and WordNet, but as you said, that's a different layer, a step later on.

> We have primitives and atoms in the library, but if we can connect them to other words, that might, in tandem with a dictionary (an actual dictionary), let us derive word or concept -> action. For instance, right now does the agent know how to identify a ball versus a rectangle? We need to give it all the basic shapes in its visualizer. These are likely atoms, but they need to connect those atoms to those visual things. We also need to go into the library and define whether something is a thing, a shape, an action, etc. Categorize, so that helps make search faster too. For instance: opponent -> deception, trick, adversary.

> I want the agent to be like "it's a ball (shaped like a ball, acts like a ball)", and let's see: balls can roll, does this roll? That type of fluency, to be possible with this RDL system.

> But it would need to also do circle -> ball. That 2D-3D, or abstraction.

> We need a way to derive, or perhaps generate, a separate list of each core shape or concept and its core actions (that we might have words for in our library already), which is why I hoped a dictionary would help. A list of verbs or actions associated with the word or concept, like Ball (throw, catch, roll, etc).

> Maybe if you use WordNet and then subtract NSM, you get the subjects and verbs. And then import VerbNet, ConceptNet, etc., if they exist.

> Keep the switches on by default for what you make, and we test all together when the full build is done, so that we can tweak and refine.

## What changed from 40

1. **The door is built.** Preload, stamps, tiers, the release bridle, codified reach and the agent's wiring exist in code, behind a switch, on by default.
2. **The meaning chain is added.** Write-up 40 went corpus -> library. Isaiah's "it's a ball, does this roll?" needs the other direction too: board pattern -> shape name -> (flat to solid) -> concept -> its actions -> a prediction the board tests -> a sentence. 40's affordance and visual-lexicon sections named this; it is now a chain of built and planned links.
3. **Flat to solid is its own link.** "Circle -> ball" is neither synonymy nor a relation between roles. It is an abstraction across dimensions: a flat shape stands for a solid one. Write-up 40's "reversed development" section says it: the agent learns "this flat pattern means depth". On flat boards it can be held and cannot settle as depth. What settles is behaviour.
4. **Vocabulary = WordNet minus NSM.** The NSM primes are the agent's own explanation layer. Everything WordNet holds that is not a prime is the vocabulary to ground: the subjects (nouns) and the verbs. Each grounded word still unpacks into primes.
5. **Concept -> actions has several sources, ranked by agreement.** WordNet read forwards and backwards, ConceptNet's relations, VerbNet's classes. The board is the only one with standing.
6. **Categories set search priority.** Object, shape, action, relation, property, measure, rule. They are a filter for the budget, never a verdict.

## The three quantities, never blurred (from 40)

- **reachable**: yes or no, by derivation. RDL never sets it.
- **search priority**: where to look first. The ONLY thing tiers, release, categories and the reach policy set.
- **standing**: only a term's own record with the board. RDL never writes it.

## The design, whole

### Layer A: the door (built)

The forward shed, the release and the reverse step of 40's loop.

| Piece | What it does | Code | Status |
|---|---|---|---|
| Preload store | every preload is stamped with its stage and source (C6); recordings are refused (C1); a preload with no bond or no attach is recorded, never offered (C2); there is no standing field anywhere (C3) | `rdl_store.py` | built (`fa208f3`) |
| Parser | the lexicon, the attribute index and the Tether cards into four tiers, each lossier than the one below: instances (1000), regularities (36), abstractions (445), core rules (13); 191 usable. Attached to library entries by cluster, never by raw name | `rdl_parse.py`, `library/rdl_preload.json` | built (`fa208f3`) |
| Release (the bridle, C4) | tier 1 opens at once, because the inherited library counts as settled; tier k opens when the board has settled 2 entries of tier k-1 (MIN_REPEAT reused); age is only a tiebreak | `rdl_release.py` | built (`cd557b0`) |
| Codified reach | what settled and what was refused, by source and tier, turned into an ordered validity table, the same form as the agent's own cue order; no weights | `rdl_release.reach_policy` | built (`cd557b0`) |
| The agent (C5, the reverse step) | released preloads break ties in the described lookup's ranking (`Agent._topk`), search priority only; `rdl_offer` / `rdl_settle` / `rdl_refuse` rows carry the stamp; the counts carry in the lineage as `rdl_n`; OFF is identical row for row | `tether.py`, TETHER_RDL | built (`0b1245c`) |
| The parser's loss set by contact (C5) | a source and tier the board refused more than it settled is shed one tier coarser at the next build | `rdl_parse.parse(stats=...)` | built; the rebuild is not yet triggered between generations |

### Layer B: the meaning chain, "it's a ball, does this roll?"

Each link consumes what the one above produces (Fig 3 :20).

| # | The thought | Link | Code / data | Status |
|---|---|---|---|---|
| B1 | "shaped like a ball" | **shape names in perception**: each object's own cells read as dot, line, square, rectangle, ring, plus, L, T, diamond, disc or irregular, each a declared geometric rule (Fig 10); colour and position never read; disc, line and square tied to library shape atoms | `arc_percept.py`, TETHER_SHAPE_NAMES | built (`0f625e3`) |
| B2 | "a circle stands for a ball" | **the shape bridge, flat to solid**: disc/circle/disk -> sphere -> ball, globe, marble; square -> cube -> block, box, die; rectangle -> parallelepiped/box -> brick, block; ring -> torus -> ring, hoop, tire; line -> cylinder -> stick, rod, pole; triangle -> cone/pyramid -> cone, pyramid. A declared table resolved to WordNet 3.0 synsets, stamped `abstraction`, no standing | `shape_bridge` in `library/word_map.json` | built (`cc6607c`, `eac67bc`) |
| B3 | "it's a ball" | **the word map**: every library entry's words -> WordNet senses, chosen by the entry's domain and clusters, never by spelling alone (ties kept, never resolved silently); a category per entry; a synonym index (`opponent` -> `TRANSFORMATION\|Adversary` through a shared synset) | `library/word_map.json` | built (`cc6607c`): 3,025 of 4,048 entries mapped |
| B4 | "balls can roll" | **concept -> actions**, ranked by how many sources agree (the next section) | word map, relations | partly built: WordNet forwards (3,577 priors) built; WordNet backwards, ConceptNet, VerbNet in progress 2026-11-16 |
| B5 | "does this roll?" | **the affordance bet**: at a new kind's first sighting, the prior's prediction is written; the first press on that kind tests it; the board settles it, or refuses it and the rule is split by the condition read ("round things roll, except when touching a wall"); nothing deleted | `affordance.py`, TETHER_AFFORDANCE | built (`16a4ef2`); settle and refuse seen only on fixtures so far |
| B6 | saying it | NSM lines over those rows: "THIS IS LIKE `ball` (`disc -> sphere -> ball`). `ball` CAN MOVE. ... I TOUCH THIS. THIS MOVES." Only listed primes; the word is a filler that unpacks to primes | `nsm.py` | built (`16a4ef2`) |
| B7 | "the ball rolls to the right" | direction from the DIRECTION cluster and manner of motion (keeps moving between presses = rolls; moves only when pressed = is pushed) | -- | not built |
| B8 | recognition from pictures | the ImageNet images through a swappable recognition front end at the edge; photos are not grids, structure transfers through the shared clusters (SHAPE, COLOUR, CONTACT, MOTION) | -- | later; the images are downloading (train and validation) |

**The rule for B1-B6 (from 40):** a name carries predictions, and a name that stops paying is refused. On a flat board, "ball" is earned only by acting like one; a disc that never moves drops back to "disc", with the refusal recorded.

### Layer C: words, verbs and relations

**Vocabulary = WordNet minus NSM.** The NSM primes (I, YOU, SOMEONE, SOMETHING, DO, HAPPEN, MOVE, TOUCH, ...) are the explanation layer the agent already speaks. WordNet's nouns and verbs minus the primes and their allolexes is the vocabulary to be grounded: the subjects and the verbs. Every grounded word stays unpackable into primes, which is what keeps it auditable (40: "the primes remain underneath, to unpack and check a word when asked").

**Concept -> actions: the sources, best first.**

| Source | Gives | For "ball" | Standing |
|---|---|---|---|
| WordNet read backwards: verbs whose definition or example sentence names the noun | catch ("Catch the ball!"), bounce ("bounce a ball"), dribble, pass | high | none |
| WordNet read forwards: verbs in the noun's own definition | "a round object that is hit or thrown or kicked" | medium | none |
| WordNet derivation links and one level of inheritance | noun <-> verb (decoy -> to decoy); "soccer ball" gets "ball"'s verbs | narrow | none |
| ConceptNet (CapableOf, ReceivesAction, UsedFor, IsA, HasProperty) | ball CapableOf roll, bounce; ReceivesAction thrown, kicked, caught | highest; supplies "roll", which no WordNet sentence ties to ball | none |
| VerbNet classes | one found verb brings its class: throw, toss, hurl, fling | widens the list | none |
| **the board** (the agent's delta table, through B5) | what each action actually did to objects of this kind | the only verdict | **the only standing** |

Each verb is mapped through the word map to the library's action entries, so a found verb lands on something the agent can test. Each carries its sources, a stamp and no standing, and is ranked by how many sources agree.

**Two different jumps, two different tools (from 40).**
- Same thing, different names (bait = decoy = lure; opponent = adversary): the **thesaurus**. WordNet synsets, which keep senses apart; the zaibacu thesaurus is the same data, one line per sense. Fig 12 :92, "k operands have k! spellings and one term."
- Different things in a role (bait -> target; adversary -> deception, trick, decoy): the **relation layer**, a bond. ConceptNet's relations and VerbNet's thematic roles. Fig 12 :111, "A vocabulary without bonds can name a state and cannot name a route to one."
- A third, added here: flat shape -> solid form (circle -> sphere -> ball). The **shape bridge** (B2). Not synonymy, not a role: an abstraction across dimensions.

**Senses are picked by context, never by spelling.** "Bait" the lure and "bait" the taunt are different senses (40; the 11-08 work on words with many meanings). The word map chooses a sense by the entry's domain and clusters and keeps ties; the agent's own sense clusters (step 8) choose at run time.

**Categories.** Every entry gets one of object, shape, action, relation, property, measure, rule, cross-checked with the library's own kind (PERCEPT, COMPOSITE, PRIMITIVE, RELATION) and default role (STATE, PROCESS, ...). Disagreements are flagged, never overridden (2,148 today). Their use is search priority: when the residual is a motion, look among actions first. A filter for the budget, never a verdict (Fig 9 :60).

### Layer D: the boards widen (from 40, unchanged)

Grids (today: relations settle) -> photographs (depth cues read flat) -> video (motion and consequence) -> simulated 3D (occlusion, support, tested by contact) -> the physical world. Each stage settles what the one before could only hold. Concepts that need depth can be held from day one (Fig 12 :104, "there is no bottom") and settle only on a board with depth.

### Layer E: dictionary and voice (from 40, unchanged)

cmudict pronunciations (hop 5), a rule-based synthesizer (hop 6). Speaking is not talking: talking needs an ear, and the listener as the board.

## The constraints

C1-C6 from 40 hold for every layer: head starts only, never recordings (C1); usable only with bonds and an attach (C2); the parser is a filter, only the board settles (C3); release follows what the board settled, not the clock (C4); the parser's loss is set by contact, and every turn of the recursion passes through the board (C5); every preload is stamped with stage and source (C6). Three rules added on 2026-11-16, each from what the build met:

- **C7, exact joins between pieces.** Pieces built apart join on exact keys; a mismatch is fixed at the source, never with a fuzzy match. (The shape names said "disc" and the bridge said "disk"; the bridge gained "disc".)
- **C8, declared conventions are visible.** Every hand-set table (the shape predicates, the shape bridge, the category map, the 25-verb cap) is marked as a convention in its file (Fig 10): visible, movable, never claimed correct.
- **C9, imports are recorded and licensed.** Every imported corpus carries its source, sha256 and licence in the file's header. ConceptNet is CC BY-SA 4.0, so a file derived from it carries that licence. Importing a corpus is Isaiah's decision alone (40); WordNet, the ImageNet label list, ConceptNet and VerbNet were approved on 2026-11-16.

## How to tell it works (measures, unchanged in spirit from 40)

- **The affordance settle rate** against the baseline measured on 2026-11-13: of first presses on a new kind, 0.417 changed the pressed object (median, board 1, 18 games). Priors that predict well should beat it.
- **Primes per explanation** should fall as words ground, at the same meaning, with every word unpackable on request.
- **Presses to settle** the first terms in a new domain should fall with each domain already learned.
- **The ladder moves:** `rdl_settle` rows appear, a tier above 1 opens, and the reach policy orders something.
- **T1-T4 from 40:** format (raw versus parsed with bonds), schedule (all at once versus bridled), reach policy versus uniform search, the drift guard. T0, the agent alone clearing a level through its own goal, refusal, repair and return, is still the gate before them.

## Where it stood at the end of 2026-11-16

- Built and on by default: the door (A), shape names (B1), the shape bridge (B2), the word map (B3), WordNet-forward actions (part of B4), the affordance bet and its sentences (B5, B6).
- Being built at the cutoff: WordNet read backwards (B4), ConceptNet and VerbNet with the vocabulary of WordNet minus NSM (layer C).
- The together-test (T0e, everything on, six games at 5 minutes each): lp85 cleared level 1; RDL released tier 1 on every level and changed a lookup order twice; no RDL material had yet settled or been refused, so the ladder has not moved; no object had a shape name on those boards that reached an affordance prior yet.
- Next, in order: B7 (direction and manner), the categories as a search filter, a live settle of a prior, then B8 (recognition from pictures).

## Files

`rdl_store.py`, `rdl_parse.py`, `rdl_release.py`, `affordance.py`, `arc_percept.py` (shape names), `library/rdl_preload.json`, `library/lexicon_imagenet_wordnet.json`, `library/word_map.json`, `library/build_lexicon.py`, `library/build_word_map.py`; interfaces in `docs/03-DESIGN/RDL_BUILD_SPEC_2026-11-16.md`; switches TETHER_RDL, TETHER_SHAPE_NAMES, TETHER_AFFORDANCE in `conform/arms.py`.
