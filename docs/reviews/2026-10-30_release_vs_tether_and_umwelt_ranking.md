# The released agent vs the Tether, and its Umwelt ranking

Reviewer, 2026-10-30. Release reviewed: general-agent cba1dd5 and arc-solver-agent 7b44592.

The two branches are one agent. Every Fig 3 link is built, and the PLAY24 runs show the chain
breaking between the objective and planning. As built, it has roughly a 12-18-month-old's
sensorimotor toolkit, plus formal-style hypothesis testing, and no social learning. As measured
in its habitat, it cannot be ranked yet.

## The two branches

They are one agent, not two. `git diff cba1dd5 7b44592` changes README.md only. Every line of
code, the library and the harness are byte-identical.

| | general-agent `cba1dd5` | arc-solver-agent `7b44592` |
| --- | --- | --- |
| What it says it is | "The agent itself, with no domain attached" | "the general agent applied to ARC-AGI-3" |
| Code | the whole tree, ARC adapter and harness included | the same tree |
| README covers | the loop, the intent/interface split, what ships, the six checks | how ARC is met (`arc_world`, `arc_percept`, `arc_holdout`), what is not ours to ship, Kaggle notes |
| Learned data | none; the lineage lives outside the repo | none; the same |

- **The split is right as ruled on 10-23.** It is two branches with two READMEs, and nothing is
  pulled out. The agent decides intent and the swappable layers carry it out. So ARC lives in
  an adapter and a harness, not in the reasoning.
- **"No domain attached" is a statement about the reasoning, not the tree.** general-agent still
  carries the ARC adapter and harness, and its README says so.
- **The release is clean as a package.**
  - No machine paths, no CLAUDE.md and no run output; a strict path scan finds nothing.
  - 70 of 71 checks pass on a clean Linux machine. The one failure is an old one.

## Against the Tether: where the chain stops

Every link of Fig 3 is now built. By PLAY24's own rows, the chain breaks between link 3 (the
objective) and link 4 (planning).

- Fig 3 :20 orders the links by dependency: "Each link consumes what the one above produces".
- Fig 3 :18 says where a chain stops "is a reading, never a property of the chain". So the
  right-hand column below is what was measured.

| Fig 3 link (verbatim) | In the release | Measured, PLAY24 rounds 1-3 |
| --- | --- | --- |
| 1 perception: "tell what is in front of it, and tell it apart from what was there before" | every same-colour region an exact object; position, size, shape, colour and their changes, plus contact; kind by shape code; frame-break turnover with arrival aliases | works: 0 faults in 4 rounds, 0 alias collisions, look time flat |
| 2 vocabulary: "terms for what things afford: what can be moved, opened, joined, blocked" | 4,048 inherited library entries; the affordance recorder fed its mover; action kinds; cheap probes; the contingency test (what moves with which press) | built; no instrument read it in PLAY24 |
| 3 objective: "say what would count as progress here, in its own terms" | goal hypotheses from the library's condition grammar; level clears counted; the progress shelf | 44-52 hypotheses a round; 4 reached in 3 rounds, all "arrived, no clear"; 12-14 a round end "no object of its kind" |
| 4 planning: "a route to that objective, chosen under incomplete information" | routes, subgoals as routes, routines (act, sequence, when, until), re-engage after "unreachable at budget", the DISTINGUISH ask | 21-32 a round end "stalled"; about 6-7 actions per game slice |
| 5 learn and carry: "name what worked, verify it, and carry it to the next problem" | lineage written and verified every round, saved by kind and never by instance | +3 names a round (388, 391, 394); nothing that cleared a level to carry |

What the figures say about this reading:

- **The break is in the middle, where Fig 3 says chains usually break.**
  - Fig 3 :25-26: the link between perception and planning "has neither [obvious failures nor
    tests], so it attracts the least attention and the fewest instruments".
  - Link 2 has no live reading, and link 3 forms goals that, when reached, do not clear.
- **Link 5 cannot be judged yet.** Fig 3 :22: "A step whose input never arrives cannot be
  diagnosed, only its predecessor can."
- **The goal grammar is the right kind of thing.**
  - Fig 12 :112: "A plan is a sequence. A goal is a comparison. Progress is a subtraction."
  - The open question is which comparisons it proposes.
- **There are too few actions for the ground to vote.**
  - Fig 12 :126: "Bits price the description. Actions price finding out whether it holds."
  - About 6-7 presses per slice is a tight action budget.

The figures it now satisfies, triangulated:

- the per-slot residual (Fig 1 :19);
- the compression bargain (Fig 5 :43);
- "unreachable" as a verdict (Fig 13 :134);
- "a generator crosses, an instance does not" (Fig 10 :68);
- the whitebox record (Fig 13 :130).

## The 10-25 Umwelt gaps: what the release closed

Nine of the twelve gaps from the 10-25 review now have an arm, every one ON in the release. A
tenth, A10, stays as ruled, and two, A7 and A8, are still open. Built and ON is not the same as
shown to help: no level has cleared since.

| Gap (10-25) | Arm in the release | Status |
| --- | --- | --- |
| A1 own effect vs the world's | `OWN_CLOCK`, `OWN_CLOCK_SUBJECT`; Agency's contingency test | in part |
| A2 touch is not a sense | `TOUCH_FELT` | closed |
| A3 affordance sense blind | `AFF_MOVER` | closed |
| A4 attention does not steer | `SURPRISE_NOMINATES` | closed |
| A5 the limb forgets its intent | `IA_SERVED` | closed |
| A6 "couldn't" has no reason | `UNREALISED_WHY` | closed |
| A7 touch aim may miss the object | none found | open, not measured |
| A8 BE_AT declared, unused | none | open, minor |
| A9 refusals rarely recur | `SITUATED_REFUSAL` | closed |
| A10 no learning from a no-change | ruled 10-11 (the downrate arm was deleted: harmful where it ran, idle where it did not) | stays as ruled |
| A11 improvement unused | `STEER`, `REENGAGE` | closed |
| A12 danger shapes nothing | `DEATH_VOTE`, `DEATH_KEEPS` | closed |

## The Umwelt: what it notices, what it can do, how fast the circle turns

Uexküll's frame: "all that a subject perceives becomes his perceptual world and all that he
does, his effector world". The two join in "a self-contained periodic cycle", the
function-circle. Fig 11 :39 is the rule for reading it: "capability is a property of
agent-and-habitat, never of the agent alone".

**What it notices:**

- Every same-colour region is an object, the background included, read exactly.
- For each object: position, size, colour, shape, and their frame-to-frame changes; cells added
  and removed; age, speed and stability; contact; and relations between objects.
- An object that is covered is not deleted. Its slots read "not resolved", and judgement resumes
  when it shows again.
- What it learned about an object that left is handed to a successor of the same form (the
  arrival alias).

**What it can do:**

- It acts with whatever the game offers: a handful of plain actions, one positioned click, and
  RESET (never two in a row).
- It acts in intents (`ELICIT`, `TOUCH`, `BE_AT`, `BECOME`, `DISTINGUISH`). The interface turns
  each intent into a press and reports back what the press did.

**How fast the circle turns:**

- PLAY24 round 3: 174 steps in 4,276 s, about 25 s per step and about 7 steps per game slice.
- Fig 11 :40: "An improvement that does not change contact changes nothing, however much it
  improves."

## The ladder: each capability beside animals and children

| Capability | In the release | In play (PLAY24) | Human benchmark | Animal benchmark |
| --- | --- | --- | --- | --- |
| Habituation | route refusal after two non-closing outcomes, keyed by situation | built; not read separately | from birth | Aplysia, C. elegans: "the simplest form of learning" |
| Contingency: "did my press move that?" | Agency's test: controlled when it moves with one action always and another never | read every step | 2 months: Watson's infants "learned to move their heads to activate a mobile" | rats and pigeons, operant box |
| Repeat an interesting effect (stage 3) | ELICIT and explore presses; repeating routines | about 7 presses per slice | 4-8 months | operant learning |
| Means and ends (stage 4) | routines; subgoals as routes | 4 goals reached in 3 rounds | 8-12 months | crows: meta-tool use |
| Object permanence | covered objects kept; successor alias by form | 3-4 aliases a round, 0 collisions | search 8-12 months; invisible displacement 18-24 months | dogs, cats: visible only; great apes, some birds: invisible |
| Surprise steers exploration | surprise nominates the subject | ON | 11 months: infants "explored those objects more" | - |
| Active experiment (stage 5) | the DISTINGUISH ask | rare: 3, 0, 1, 0 asks in rounds 1-4 | 12-18 months; 3-4 years: blicket "Can you make it stop?" | crows on water displacement, "rivalling that of 5-7 year old children" |
| Same/different and kinds | kinds by shape; residual split; saved by kind | carried each round | 7-11 years: classification | honeybees: "sameness" and "difference" |
| Causal structure, explicit hypotheses | library cause terms; goal grammar; compression bargain; refute without deleting | 44-52 hypotheses a round | 2-4 years: causal Bayes nets; 12+: hypothetico-deductive | none explicitly |
| Insight (stage 6) | predicts each action's outcome per hypothesis before acting | in part | 18-24 months | Köhler's chimpanzees |
| Imitation | none | none | stage 6: deferred imitation | apes understand intentional action |
| Scaffolding (ZPD) | none by design | none | Vygotsky: "under adult guidance or in collaboration with more capable peers" | - |
| Private speech | every decision row says why | in part | 4-7 years | none |
| Cultural tools | 4,048 inherited library entries | used every step | Vygotsky's mental tools | none |
| Shared intentionality | none (multi-agent is a design doc) | none | the human difference (Tomasello) | apes lack it |

- **The contact rate is far below even an infant's.** A 3-month-old learns the mobile contingency
  "within 1 minute". In a minute the agent makes 2-3 presses.
- **Most of the core-knowledge priors ARC is built on are present.**
  - The agent has objects, number and geometry.
  - Its weakest is agents. It tells what moves with its own press from what moves on its own,
    but it gives other things no goals.

Scaffolding is out by design. This is the first agent of its kind, so there is no other of its
kind to teach it. It teaches itself, or learns from examples of other Umwelts (Isaiah,
2026-10-30).

## How it ranks

It gets two ranks, kept apart.

- **As built:** an upper-sensorimotor learner with a logician's notebook and no social line.
- **As measured in its habitat:** not rankable yet, because no goal it reaches has cleared a
  level.

The figures that require two ranks, triangulated (Figs 1, 3 and 11):

- **Fig 11 :39** "capability is a property of agent-and-habitat, never of the agent alone."
- **Fig 1 :22** "Aggregating across slots is how a live signal disappears into an average."
- **Fig 3 :22-23** "A step whose input never arrives cannot be diagnosed ... It is a reading of
  nothing."
- **Fig 11 :70** "A test harness is a substituted habitat. Which is why a synthetic solve proves
  wiring and never capability."

The world corroborates the mosaic: development runs in separate lines on different clocks. It
also corroborates the bottleneck: every child benchmark rests on many contacts.

This reading is reversed by any of:

- a level cleared;
- a live link-2 reading that puts the break there;
- contact rising with no change in reached goals.

What it points at: more presses per game and better goal choice, not more mechanism.

## Sources

Primary: the Tether figures (`docs/FIGURES_TEXT.md`, `figures/`); the code at cba1dd5 and
7b44592; the PLAY24 round reports.

- [Ay & Löhr 2015, The Umwelt of an embodied agent (quoting Uexküll 1926, 1934)](https://arxiv.org/pdf/1603.08389)
- [McLeod, Sensorimotor Stage, Simply Psychology](https://www.simplypsychology.org/sensorimotor.html)
- [Piaget's theory of cognitive development, Wikipedia](https://en.wikipedia.org/wiki/Piaget%27s_theory_of_cognitive_development)
- [McDonough, Object permanence, Britannica](https://britannica.com/science/object-permanence)
- [Cacchione & Rakoczy 2017, Comparative metaphysics](https://www.psych.uni-goettingen.de/de/development/pdfs/cacchione_rakoczy_2017.pdf)
- [Butko & Movellan 2010, Detecting contingencies (on Watson 1972)](https://mplab.ucsd.edu/46/media/2010-ButkoMovellan-NeuNet-Contingency.pdf)
- [Mobile conjugate reinforcement, Lancaster University glossary](https://www.lancaster.ac.uk/fas/psych/glossary/mobile_conjugate_reinforcement/)
- [Gopnik et al. 2004, A theory of causal learning in children](https://www.cmu.edu/dietrich/philosophy/docs/glymour/gopnikglymouretal2004.pdf)
- [Stahl & Feigenson 2015, Observing the unexpected, Science](https://pmc.ncbi.nlm.nih.gov/articles/PMC5861377)
- [Kinzler & Spelke 2007, Core systems in human cognition](https://www.harvardlds.org/wp-content/uploads/2017/01/Kinzler_CoreSystemsHumanCog-1.pdf)
- [Chollet 2019, On the Measure of Intelligence](https://arxiv.org/abs/1911.01547v2)
- [Vygotsky on the zone of proximal development, via New Learning](https://newlearningonline.com/new-learning/chapter-8/vygotsky-on-the-zone-of-proximal-development)
- [Stone 1998, The metaphor of scaffolding](https://www.sfu.ca/~jcnesbit/EDUC220/ThinkPaper/Stone1998.htm)
- [Tomasello et al. 2005, Understanding and sharing intentions](https://dornsife.usc.edu/mid-la/wp-content/uploads/sites/317/2023/11/Tomasello_et_alll.pdf)
- [Jelbert et al. 2014, Aesop's fable paradigm in crows, PLoS ONE](https://www.plosone.org/article/info%3Adoi%2F10.1371%2Fjournal.pone.0092895)
- [Giurfa et al. 2001, Sameness and difference in an insect, Nature](https://ideas.repec.org/a/nat/nature/v410y2001i6831d10.1038_35073582.html)
- [Esdin, Pearce & Glanzman 2010, habituation](https://www.frontiersin.org/articles/10.3389/fnbeh.2010.00181/pdf)
- [Wolfgang Köhler, New World Encyclopedia](https://www.newworldencyclopedia.org/entry/Wolfgang_Kohler)
