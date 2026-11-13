# WATSON 2026-11-03 — problem-solving paradigms (navigation, jigsaw and the rest)

Reviewer, 2026-11-03 ~14:50 CST. Run by a helper under the tether-watson procedure. The figure quotes were spot-checked by the reviewer against docs/FIGURES_TEXT.md. Read-only; nothing in the code was changed.

## QUESTION

Isaiah, 14:29: "The jigsaw paradigm, yes its just one of several types of paradigms, some are navigation. check the prior list to obtain more info on whats expected of humans to be able to solve in their modes etc (you can also do a watson)."

What modes does a human bring to interactive puzzle games? For each, what does it ask of the player? How should the agent hold them, recognise which one a board needs, and switch when one fails?

## THE PRIOR LIST (Isaiah's 10-08 classification files, /mnt/user-data/uploads/)

**DISTRIBUTION_COVERAGE_ANALYSIS**
- 8 cognitive clusters (C1–C8) and 15 algorithm families (F1–F15).
- Offline-50 coverage: NAV 50%, COL 34%, SOK 10%, FPL 6%, GF2 4%, PAR 4%, SLD 2%, SEQ 2%.
- ARC's own profile is cluster C6, Formal-Systemic. The training set's profile is C2/C3: "nearly orthogonal".

**EXPERT_AUDIT_DEEP, "The Eight Solver Modes"**
- The modes: NAVIGATE, COLLECT_ALL, SOKOBAN_PUSH, SLIDE_ROW, FALLING_PIECE, GF2 (lights-out), PAIR_MATCH, SEQUENCE.
- The fallbacks: Explore, and a causal fingerprinter.
- A failure list for each mode, e.g. key→lock ordering, floor switches, memory-match.
- MISSING:EXPERT tags: navigation:prerequisites, memory:flip-pair, path:euler, pattern:grid-transform.

**Other files**
- EXPERT_ALGORITHM_GROUPS: F1 constraint propagation through F15 visual pattern abstraction.
- EXPERT_VECTOR_CLUSTER_MAP: a Spatial-Reflex axis and a Planning-Abstraction axis. Jigsaw sits in C4, circuit routing in C6, memory-match in C2.
- EXPERT_GAPS_NOVEL_ARCHETYPES: 353 archetypes. ARC priority: ChainReaction, Territory, Breakout, MemoryMatch, Sudoku, SingleStrokePath, CircuitRouting, …
- GAME_FAMILY_GRAPH: 10 families. At its branch points, multiple experts must act at once.

COGNITIVE_DEVELOPMENT_MAP is cited by these files but is not on disk.

The jigsaw ruling, from ISAIAH_RULINGS.md:192-199 (10-03): "the player is OUTSIDE the board … Treat it as a JIGSAW PUZZLE, not a map: hold a fuzzy picture of where things go, made concrete by filling gaps, pattern-matching and verifying in a loop."

## DOMAIN CENSUS

**R** (the paradigm) is told apart by three things:
- arity: how many objects the goal binds;
- symmetry: whether order matters;
- scale: one route or the whole board.

**Domains** (actors / currency / anchor):
- D1, the board description: objects / deltas / frames.
- D2, the objective: goal hypotheses / residual / level clear.
- D3, switching: the shapes as rooms / residual trend / ground.
- D4, carry: the shelf / wins / levels.

These are a union, not a partition: ARC games carry several mechanics at once. Dependency order: D1 → D2 → D3 → D4 (Fig 3).

## TETHER (primary, verbatim)

**D1: describe the board, then look it up**
- Fig 9 :25-29: "R's own predicates name the habitat that holds φ* / describe it before you go looking, or / any frame you pick will seem to fit / matching is a one-pass check, not a search".
- Fig 9 :30-32: "describe the effect / rather than the cause / → you get a kind of thing, never the answer itself".
- Fig 11 :43: "The habitat is enumerated, never composed."
- Fig 11 :49-51: "An actor's valence is relative to the residual, not a property it carries." The same box is the goal in Sokoban and an obstacle when navigating.

**D2: the objective is the weak link**
- Fig 3 :9-11: "it can say what would count as progress here, in its own terms".
- Fig 3 :25-27: "A link with no instrument is not a link that works."
- Fig 5 :62-66: "A frame searching for an answer of a particular shape holds that shape as a PREFERENCE rather than as a term … make the sought-for shape an ORDINARY TERM. Write down what an answer would look like, bind it, and let it accrue a residual like anything else."
- So a paradigm is a sought-for answer shape. It must be held as an ordinary, refutable term, never as a hard-wired expert.

**D3: switch on the residual**
- Fig 5 :59: "a term whose residual PERSISTS AND DOES NOT TREND DOWN is the one to point the refusal at".
- Fig 7 :36: "The next room must differ from the last, and match the residual it surfaced." Fig 7 :40: "The room is summoned by the residual rather than composed."
- Fig 9 :40-41: "a wrong cut removes the answer and speeds up / so keep every cut ranked and reversible".
- Fig 9 :54-57: unbundle a union. "a case in two conditions is not a harder case of either … It becomes a specific compound." Navigation plus key-before-door is a compound, not a harder navigation.

**D4: carry**
- Fig 4 :22-24: "Only methods cross up. Only head starts come down … Never a replay of what worked once."
- What carries is which shape paid for which board description.

**Triangulation:** D2 and D3 are triangulated (Figs 3, 5, 7, 9). D1 rests on Figs 9 and 11. A reading of the paradigms as compositions of Fig 13's six terms (space, time, energy, spectrum, gradient, network) is the helper's own, single-source, and waits on Isaiah's ruling.

## WORLD (secondary; each source read)

- **ARC Prize Foundation, "ARC-AGI-3", arXiv 2603.24621 (2026).** "Each environment contains multiple mechanics." Single-mechanic environments are "an anti-pattern". Priors: objectness, geometry/topology, basic physics, agentness. The objective is never told. → Every game is a union of paradigms. Corroborates Fig 9 :54-57.
- **Kinzler & Spelke, "Core systems in human cognition" (2007).** Separate core systems for objects, agents, number and geometry. → Paradigms sit on distinct priors.
- **Lieder & Griffiths, "Strategy selection as rational metareasoning", Psych. Review (2017).** People "learn to predict the accuracy and execution time of each strategy from features of individual problems" and "adaptively switch". → Choosing a paradigm is a lookup from board features to each paradigm's track record. Corroborates Fig 9 with Fig 4.
- **Knoblich, Ohlsson, Haider & Rhenius, JEP:LMC (1999).** "impasses are broken by changing the problem representation". → Switch representation rather than search harder. Corroborates Fig 7 :36 and Fig 5 :65.
- **Tolman, "Cognitive Maps in Rats and Men" (1948).** Over-motivated learning produces narrow, strip-like maps that do not carry over. Latent learning builds the map without reward. → Fixation under pressure, and contact-first exploration supplies the wider map that switching needs.

No world source conflicts with the figures.

## PARADIGMS: what each asks, and whether today's code (development 053ace1) can form its goal

| Paradigm | Human must notice | Goal form | Detect from the board | Today |
|---|---|---|---|---|
| Navigate | what my action moves; a target; walls | contact or position, via an Until routine | one object moves with my action; arity 2, local | YES |
| Navigate with prerequisites (key→door) | the target is blocked; touching X changed the blocker | ordered pair: A then B | navigation stalls flat; a contact changed the blocker (a compound) | PARTIAL (pairs only after all singles fail; not ordered by dependency) |
| Collect-all / clear | same-kind things vanish on contact; the level ends at none | none of kind K remain | a kind's count falls on contact; arity n, order-free | PARTIAL (one contact at a time; all/none atoms are "never a want alone") |
| Jigsaw / placement | loose pieces; holes or slots that match them; a picture to complete | each piece at its place | no avatar; clicks; shapes or colours duplicated between loose and fixed objects | NO |
| Push (Sokoban) | objects move when walked into; targets; trapping corners | every box on a target, no dead states | the avatar's contact displaces an object | PARTIAL (no dead-state reasoning) |
| Pair-match | identical pairs; selecting both removes them | all pairs cleared | duplicates plus removal on the second touch | PARTIAL |
| Sort / order | a gradient in size, colour or position | before/after holds for every adjacent pair | arity n, ordered | PARTIAL (one pair at a time) |
| Toggle / lights-out | one press changes several neighbours | every cell in one state (coupled plan) | one action changes more than one object | PARTIAL (no coupled plan) |
| Sequence / memory | things shown, then hidden; order matters | reproduce the order | the board changes without me, then hides | NO (own-clock subjects are refused, which blocks it) |
| Circuit / connect | endpoints and connectors | connected(A, B) | two endpoints plus n connectors | NO |
| Rule induction / make-like-the-model | a reference region and a target region | target = transform(reference) | two regions sharing structure, one unchanging | PARTIAL |
| Counting / conservation | how many matters | two extents equal | two co-varying quantities | PARTIAL |

**What exists today:**
- GOAL_HYPOTHESES fills TEMPLATES (library_runtime.py:216-240). Each goal is a single relation over one or two objects. Goals are tried one at a time; when every single fails, a pair is tried; then System 0 takes over.
- GOAL_FROM_ACTUATOR covers levers.

So goals form well only for navigate and lever boards. Set-level ("all", "none left"), ordered, coupled and memory goals are missing. That matches the public set's C2/C3 bias.

## VERDICT (from the figures)

1. **Paradigms are NOT hard-coded experts behind a confidence router** (the older brain_moe_v6 design).
   - Each one enters as a goal-SHAPE family: a small, generic template in the same grammar as TEMPLATES.
   - The board fills in K, P and the objects.
   - Each shape is proposed, held unsettled, and refuted like any hypothesis (Fig 5 :62-66).
   - New templates are needed over sets and order:
     - "for every member of K, P holds";
     - "none of K remain";
     - "P(a) before P(b)";
     - "all cells same";
     - "connected(a, b)";
     - "each loose piece matches a fixed one".

2. **Detection is one lookup keyed on the board's description** (arity, symmetry, scale, who moves what), per Fig 9 :25-29.
   - An avatar is present: navigate first.
   - No avatar and click actions: placement or actuator first (Isaiah, 10-03).
   - A kind's count falls on contact: collect.
   - One press changes many objects: toggle.
   - The lookup ranks shapes; it never decides (Fig 9 :32).

3. **Switching is on the residual, not on counts.**
   - A shape whose residual stays flat is refuted for this board. It is demoted, stays reversible, and is never deleted (Fig 5 :59; Fig 9 :41).
   - The next shape must differ AND match what the last one surfaced (Fig 7 :36). Example: navigation stalls at a door that changed when a switch was touched, so the next shape is the prerequisite compound.
   - Two shapes that each work on part of the board become a compound (Fig 9 :54-57). ARC's "multiple mechanics" rule makes this the common case.
   - This is Isaiah's "incentive to solve": repeated failure changes the representation (Knoblich et al.), not the effort.

4. **Carry:** the shelf records which shape paid for which board description (Fig 4 :22-24). A head start, not a route.

5. **Order of work (Fig 3):** this is link 3, the objective. Give it an instrument first: per board, which shape was held, how its residual trended, and when it switched. The NSM trace (if approved) would make that readable.

- **Cost if wrong:** moderate. Wrong shapes waste steps, but each is one refutable hypothesis.
- **Undoable:** yes, behind an armflag like the other goal families.
- **Reversed by:**
  - (a) set-level and ordered shapes fail to raise levels cleared on the boards that need them. Measure beyond the public 25, which is ~50% NAV and ~34% COL; the arc3-synthetic games are the place.
  - (b) switching on a flat residual does worse than today's "next must differ".
  - (c) Isaiah rules that a different figure line governs.

## Sources

- [ARC-AGI-3: A New Challenge for Frontier Agentic Intelligence (arXiv 2603.24621)](https://arxiv.org/abs/2603.24621)
- [Kinzler & Spelke, Core systems in human cognition (2007)](https://www.harvardlds.org/wp-content/uploads/2017/01/Kinzler_CoreSystemsHumanCog-1.pdf)
- [Lieder & Griffiths, Strategy selection as rational metareasoning (2017)](https://cocosci.princeton.edu/falk/Strategy%20selection%20as%20rational%20metareasoning.pdf)
- [Knoblich et al., Constraint relaxation and chunk decomposition in insight problem solving (1999)](https://www.kognition.uni-koeln.de/literature/Knoblich_etal_1999.pdf)
- [Tolman, Cognitive Maps in Rats and Men (1948)](https://psychclassics.yorku.ca/Tolman/Maps/maps.htm)
- [Ohlsson, The Problems with Problem Solving (2012, abstract)](https://docs.lib.purdue.edu/jps/vol5/iss1/7)
