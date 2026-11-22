WATSON 66 — puzzle orientation, not a goal vocabulary (2026-11-22)

ISAIAH'S REFRAME: "what winning looks like" is really puzzle solving. Puzzles have hidden rules,
inputs, outputs, signs that reveal constraints, signals of momentum and regression, pattern
recognition, composition of sequences, quirks to learn, a total space of possible moves, and
conditional moves/states that unlock sequencing. Humans and animals solve unfamiliar puzzles
beyond mere leverage. Brute force is fine when permutations are below a threshold, not when they
are not. Deep audit into puzzle types and human/animal reasoning, culminating in what must change.

This corrects my earlier "goal-shape vocabulary" framing (WATSON 65's third capability): the
missing thing is not a list of goal shapes, it is ORIENTATION in an unfamiliar problem space.

QUESTION (effect terms): what does a solver DO when handed a new puzzle, that this agent does not,
and which of those moves are already present but starved vs genuinely missing?

DOMAIN CENSUS:
- R: arity = (solver, problem space, ground); symmetry = more search can help or drown; scale =
  one puzzle attempt across a lineage.
- domains: problem-space reading (actors: signs/constraints / currency: surprise / anchor: the
  board); momentum (actors: progress signal / currency: residual trend / anchor: ground outcome);
  search control (actors: moves / currency: actions / anchor: the space's size); structure (actors:
  operations/conditions / currency: composition / anchor: Fig 12 bonds).
- order (Fig 3): perception -> vocabulary -> objective -> planning -> carry; and Fig 3 :19-21 a
  break upstream starves everything below.

TETHER (primary, verbatim from source SVGs):
- Fig 3 : "it has terms for what things afford: what can be moved, opened, joined, blocked" (link 2)
  ; "it can say what would count as progress here, in its own terms" (link 3) ; "a route to that
  objective, chosen under incomplete information" (link 4). : "Optimising a link that already
  works cannot rescue one that does not." -> the agent's measured links: perception 6/6,
  goal 6/6, planning/subgoal 0/6. The break is at link 4, not at "goal vocabulary."
- Fig 5 : "is there anything to explain, before the search starts" ; "a term whose residual
  PERSISTS AND DOES NOT TREND DOWN is the one to point the refusal at, which is the same shrinking
  test the selector already runs, read with the opposite sign." -> the momentum/regression signal
  EXISTS in the agent (shrinking/trend/MIN_REPEAT) and has an opposite-sign reading for refusals.
- Fig 6 : "some unreachability is depth and some is genuine absence, and from inside the frame the
  two look the same." "The question is not whether a sensor could exist. It is whether anything,
  at any resolution, is already returning something that fails to resolve." -> the puzzle's
  "hidden rules" are not a separate vocabulary; they are whatever the current instruments fail to
  resolve. Orientation = telling depth from absence, not inventing sensors.
- Fig 8 : "Residual first, frame second." "Two frames together reach what neither reaches alone."
- Fig 10 : "When the question changes, the room should change. A room that stays fixed while the
  question moves is the failure." -> when the puzzle's constraint changes, the comparison set must
  change; a fixed panel is the named failure.
- Fig 11 : "capability is a property of agent-and-habitat" ; "You do not invent the list. You read
  it off the world, and what you cannot perceive or measure yet is the residual."
- Fig 12 : "A vocabulary without bonds can name a state and cannot name a route to one." ; "is the
  second operand's absence the point? Yes." -> the seven bonds include subtraction (absence) and
  sequence, so conditional/absent/unlocked moves are sayable in the grammar already.

WORLD (secondary, each read):
- Newell & Simon (Human Problem Solving 1972; CMG chapter): problem space + means-ends analysis +
  operator subgoaling ("if an operator cannot be applied, set up a subgoal to reach a state where it
  can"). "Weak methods ... often suffice to solve a problem, if the space is not large or if
  extensive search is undertaken." "One key facet of intelligence lies in the ability to search
  such spaces selectively rather than exhaustively." "Selection and revision of problem spaces is
  a higher form of heuristic search" (and they note it is under-researched). -> PREDICTS: brute
  force is a budget decision, and subgoaling is the move when an operator cannot apply. Matches
  Fig 3 link 4 and Fig 5's budget kind. CORROBORATES.
- Insight research (Ohlsson 1992 constraint relaxation; Luo/Knoblich neuroscience review; Sarathy
  & Scheutz 2024 puzzle taxonomy): insight = restructuring a wrong initial representation;
  "limiting the number of moves available helps solution"; people give accurate feeling-of-warmth
  on analytical problems but "are virtually unable to rate their progress on insight problems."
  -> PREDICTS: when the progress signal is flat, the move is not more of the same but a change of
  representation (constraint relaxation). This is the agent's `arrived_no_clear`: its goal was met
  and the board did not clear — its own feeling-of-warmth was high and the ground disagreed.
  CORROBORATES Fig 10's "when the question changes, the room should change."
- Jazayeri/MIT (hierarchical + counterfactual heuristics): "break down the maze into subsections,
  solve each with relatively simple algorithms ... clever heuristics chained together." ->
  PREDICTS hierarchical decomposition of a large space. CORROBORATES Fig 12 composition.
- Comparative cognition (detour paradigm; New Caledonian crow tool use; Taylor et al "an end to
  insight? crows solve without planning"; WCST set-shifting): animals restructure (detour =
  inhibit the direct approach), shift sets when contingencies change, and solve flexibly without
  explicit planning. -> PREDICTS: the core moves are inhibit-the-obvious, set-shift, and try an
  alternative route — not a library of goal shapes. CORROBORATES Fig 10/11.

VERDICT (from the figures, corroborated): Isaiah is right — the capability is ORIENTATION in a
problem space, and the tether already names its parts:
1. READ CONSTRAINTS from surprises (Fig 6 "anything ... returning something that fails to
   resolve") — the agent already perceives per-slot residual; what is missing is treating a
   PERSISTENT, non-trending residual as a constraint sign (Fig 5's opposite-sign reading) rather
   than another goal to satisfy.
2. MOMENTUM/REGRESSION signal — already present (shrinking/trend/MIN_REPEAT); its refusal reading
   is the missing half.
3. POSSIBLE/IMPOSSIBLE and CONDITIONAL moves — "what things afford" (Fig 3), contact/known-effects
   (interface), and the seven bonds including absence and sequence (Fig 12) already say these.
4. BRUTE FORCE vs STRUCTURE — a budget decision (Fig 5/6); bounded exhaustive search when the space
   is small, import/restructure when it is not (Fig 6 "depth vs genuine absence").
5. RESTRUCTURE on a flat progress signal — Fig 10 "when the question changes, the room should
   change"; the insight literature's constraint relaxation. This is the precise Fig 9 loop that
   WATSON 43 located as unbuilt, and Isaiah's "quirks of a puzzle."

The single change the figures license: when a residual PERSISTS AND DOES NOT TREND DOWN (the
opposite-sign reading Fig 5 already names), treat it as a CONSTRAINT SIGN and change the
comparison room (Fig 10) — i.e. restructure — instead of renewing the same goal. This needs no
external frame, no LLM, no answer encoding: it is the agent reading its own non-progress as the
direction. The goal-shape frontload (WATSON 65) is NOT required for this move; it becomes relevant
only if restructuring still cannot find a frame.

COST IF WRONG: a restructure triggered by a noisy flat reading changes the comparison set needlessly;
guard with MIN_REPEAT and a ranked, reversible change (Fig 13), not a delete. UNDOABLE: arm-guarded,
OFF byte-identical, row carries the trigger. REVERSED BY: a per-game run where the restructure does
not raise clear above 0/6.

A read-only audit of the agent's puzzle-orientation machinery is running in parallel; this WATSON
is the figure/world derivation and will be reconciled with it before any build. No code changed.

FIGURE CENSUS: Fig 1 · Fig 3 · Fig 5 · Fig 6 · Fig 8 · Fig 9 · Fig 10 · Fig 11 · Fig 12 · Fig 13
(verbatim from SVGs). Strained: none.

Sources (world, corroboration only): Newell & Simon, Human Problem Solving (1972) and "The problem
space" chapter; Ohlsson (1992) constraint relaxation; Luo & Knoblich, insight neuroscience review;
Sarathy & Scheutz (2024) puzzle taxonomy; Jazayeri (MIT) hierarchical/counterfactual heuristics;
detour paradigm review (PMC5756264); Taylor et al. (2012) crow tool use.


## RECONCILIATION (2026-11-22) — puzzle-orientation audit ↔ WATSON 66

A read-only audit of the agent's puzzle machinery and my own write-site verification agree. The
reframe is correct: the missing thing is ORIENTATION in an unfamiliar problem space, not a
vocabulary of goal shapes. But the audit shows almost all of orientation is already BUILT and
REACHED. What follows is the honest "what must change" map, by puzzle type.

PUZZLE-TYPE TAXONOMY → AGENT MECHANISM → VERDICT (write sites verified):
- RULE/CONSTRAINT puzzles (Sudoku, logic): read constraints from signs, propagate. Agent:
  `interface.action_kinds` (interface.py:2265-2273) + `interface.audit` (2018-2029, conditional-vs-
  changed is SIGNED) + per-slot residual + `known_forms` (1443-1462, "unknown never reads as moves
  nothing"). BUILT + REACHED.
- PATTERN-COMPLETION (jigsaw, Raven, ARC): recognize repeated structure. Agent: shape/kind canon,
  `recognize.py` (built, deliberately NOT reached on the decision path), rule cards, `read_pairs`
  (composer.py:675-705). BUILT on form; win-condition frame NOT BUILT.
- TRANSFORMATION/SEQUENCE (Rubik's, planning): means-ends subgoaling + operator sequencing.
  Agent: `routine.py` algebra (Act/Seq/When/Until/Choose/Try, advance) + `_htn_push`
  (tether.py:16800-16854). BUILT at routine layer, STARVED at subgoal layer (subgoal 0/6).
- INSIGHT/RESTRUCTURING (riddles, Duncker candle): when the progress signal is flat, CHANGE THE
  REPRESENTATION. Literature: Ohlsson constraint relaxation; people cannot feel warmth on insight
  problems. Fig 10: "when the question changes, the room should change." Agent: the opposite-sign
  reading EXISTS as `stuck()` (tether.py:11416-11420, "not shrinking") but is used only to PARK or
  STALL — never to trigger a restructure. THE ONE GENUINE GAP.
- SEARCH/NAVIGATION (mazes): brute force when the space is small, structure when large. Agent:
  `STEP_BUDGET`, `work_budget`, `enumerate_closure`'s honest `budget_spent`/`depth_exhausted`
  stops, residual-directed pruning (gamma.py:2592-2604 "orders, never admits"). BUILT. The
  brute-force-vs-structure META-DECIDER is NOT BUILT and is not warranted (a threshold would be a
  magic number; caps already decide it).
- CONDITIONAL/UNLOCK (keys-doors): learn which move unlocks which. Agent: `can_ledger` crossings
  (opened/discovered, can_ledger.py:48-68), `OpenerBook` ("A then B", 78-102),
  `ProductionBook` ("A=>B", 105-145), latch cause (tether.py:13809). BUILT, REACHED as readings —
  and RECORD-ONLY ("nothing here changes a choice", can_ledger.py:20). `_cap_read` (26943-26950)
  partly wires "you can now... those routes are tried again".

HUMAN/ANIMAL MOVES BEYOND BRUTE FORCE → figure mapping:
- Constraint relaxation / restructuring (insight) → Fig 10 "change the room". NOT a trigger yet.
- Set-shifting when contingencies change (WCST, comparative cognition) → Fig 10. Recorded in
  `can_ledger` crossings but record-only.
- Detour / inhibit-the-obvious (animals, detour paradigm) → the `arrived_no_clear` correction
  ("my met goal was not the win" = inhibit the first obvious goal). Built as subtext steer.
- Means-ends subgoaling (Newell & Simon 1972) → `_htn_push(when="refused")` at tether.py:11585,
  16812. Built, starved.
- Hierarchical decomposition (Jazayeri) → `routine.py`. Built, starved.
- Counterfactual "what else could count" → no generator over win conditions. NEEDS the frame.

WHAT MUST CHANGE FOR THE AGENT — the honest list:
1. THE EXTERNAL FRAME CONTENT (anchor's role, the single dependency): a provenance-stamped,
   offline frontload of "what clearing looks like" shapes / puzzle schemas, built from
   walkthroughs and nature, no standing until the board pays. I cannot generate these without
   choosing what counts as winning — answer-encoding, forbidden. This is the bridge Isaiah
   described and the only thing that unblocks the counterfactual/restructure move.
2. THE RESTRUCTURE TRIGGER (Fig 10, figure-derived, partly wireable): route `stuck()`'s
   non-trending reading into "change the comparison room" instead of only park/stall. It needs
   item 1's alternative frames to switch to; without them, "restructure" has nowhere to go.
3. STARVED WIRING (built, needs a habitat that pays, NOT invention): subgoal 0/6 on the 1800s
   boards is largely because no-clear is RARE (ka59 c7 once; the rest 0) and the repair's candidate
   filter (`arrival == OPEN`, tether.py:16818) finds nothing qualifying. This is a thin-signal
   problem on THIS panel, not a missing mechanism — per the "null carrying a causal story" and
   "panel precondition" disciplines, do not fit a fix to it.

EXHAUSTED-LINE VERDICT (Fig 13): kind = "requires external frame content"; scope = "win-condition
orientation on unseen boards". I will not manufacture a goal heuristic, a laxer OPEN filter, or a
brute-force threshold — each is a fitted guess / magic number / answer-encoding wearing a fix's
clothes. The figures decide that the frame is the missing term; supplying it is meaning, which is
the anchor's role. Everything else is built-but-starved wiring. No code changed this session.

Write sites verified directly: can_ledger.py:20,48-68,78-113; tether.py:2516-2534 (arrival/shrinking),
11409-11420 (stuck/arrived_no_clear), 11567-11607 (repair_at_refusal), 11609-11629 (contact
candidates), 16800-16854 (_htn_push). Ledger: ka59 c7 repair_at_refusal pushed=False.
