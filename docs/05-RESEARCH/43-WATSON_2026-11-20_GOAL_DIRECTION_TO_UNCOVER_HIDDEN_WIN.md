WATSON — how should goal formation be directed to uncover a game's hidden win condition?

QUESTION (effect terms): the T0 chain stops because the agent adopts a goal that is
satisfiable but insufficient (it met `o1.rem_n > 0`; the board did not clear). What change to
GOAL FORMATION would make it uncover the actual win condition of an unseen game/puzzle,
without encoding any game's answer?

DOMAIN CENSUS (before figure lines):
- R: one game's hidden clear condition vs the agent's proposed slot condition; arity = a
  relation between (proposed goal, ground response), symmetry = the goal could be met and
  still fail (asymmetric), scale = one episode's goal sequence.
- domains:
  1. goal formation — actors: the residual, the grammar's condition space, the ground;
     currency: which goals paid (cleared) vs were refused; anchor: the ledger.
  2. the ground's answer — actors: the board, the clear signal; currency: win/no-win;
     anchor: the platform, unmaintained.
  3. the frame's closure — actors: atoms, imports, in-principle vs in-budget; currency:
     reach; anchor: what the vocabulary can express.
  4. world analogues (human goal inference) — actors: observer, actor, hidden goal;
     currency: cost of actions, subgoal statistics; anchor: behavioural data.
- order (Fig 3): ground → residual → goal formation → closure. A goal is downstream of the
  residual and upstream of everything that acts.
- union: "satisfiable" ∩ "is the clear condition" is a compound, not a harder case.

TETHER (primary, verbatim; Fig :line from docs/01-FOUNDATIONS/03-FIGURES_TEXT.md):
- Fig 9 :6-8 "1 the verdict: is I+* in here at all? 2 the lookup: which frame holds it?
  3 the narrowing: which one is it?" → the agent must treat the hidden win condition as a
  REACHABILITY question (is it expressible in my closure?), then a LOOKUP (which prior/import
  frame predicts its shape), then a NARROWING — not as a single guessed goal.
- Fig 9 :27-28 "describe it before you go looking, or any frame you pick will seem to fit"
  and :30-31 "your words are borrowed too, so describe the effect rather than the cause" →
  the residual must be DESCIBED IN EFFECT TERMS ("my goal was met and the board did not
  advance") before any new goal frame is chosen. This is exactly the `arrived_no_clear`
  reading T0 produced.  [triangulated with Fig 11 :48 "You do not invent the list. You read
  it off the world, and what you cannot perceive or measure yet is the residual."]
- Fig 9 :44 "Only a sealed room can be searched to the end, and no frame is a sealed room.
  So searching and finding nothing proves nothing." → more goal proposals within the same
  closure cannot find a win condition that needs a different frame; must LOOK UP / import.
- Fig 9 :53 "Nobody chooses. The gap does, and the gap is only as good as its description." →
  the direction of goal search is set by the described gap, not by a fixed heuristic or a
  game's identity.
- Fig 9 :55-58 "a bundled problem is usually a union of overlapping conditions... a case in
  two conditions is not a harder case of either" → "goal met + no clear" is a union of two
  conditions (my condition insufficient AND some other condition unmet); unbundle before
  searching again. This is the structural reading of T0's stop.
- Fig 8 :39 "a search that finds nothing is never a proof of absence", :20-21 "closures differ,
  so a surplus exists, but no residual is described: nothing was aimed; the union is mute",
  :53 "Residual first, frame second", :54 "underivable is not unknowable [but] the union is
  searchable from contact" → the hidden goal lives in the union of the agent's frame and a
  frame whose closure differs (a prior/import that predicts the win condition's shape);
  find it by contact from the described residual.
- Fig 6 :21-22 "MINT composes inside the closure and can never add an atom. NOVEL means novel
  relative to atoms, not to the world" and :23 "No frame escapes its own closure. The bound
  moves only on contact with a frame whose closure differs" → a win condition needing a new
  atom/reading requires contact with an external frame, never more internal goal proposals.
- Fig 11 :39-40 "capability is a property of agent-and-habitat ... An improvement that does
  not change contact changes nothing."  :70 "A test harness is a substituted habitat. Which
  is why a synthetic solve proves wiring and never capability." → the proof must come from
  real games, and the change must alter what the agent CAN reach, not just what it proposes.
- Fig 13 / Operators: "a wrong cut removes the answer and speeds up / keep every cut ranked
  and reversible" → when narrowing goal candidates, keep them ranked, never delete.
- Verdict triangulation: Fig 9 (leave/lookup/narrow) + Fig 8 (union surplus, residual first)
  + Fig 6 (closure needs external contact) + Fig 11 (contact) are four low-overlap lines
  agreeing: direct goal formation by describing the "met-but-no-clear" residual, then a
  lookup to a frame that predicts the win condition's shape, then narrowing — NOT by adding
  more internal goal variants or tuning to a game.

WORLD (secondary, each read above):
- Infants infer goal value from action cost (Science 2017, aag2132): "infants expected the
  agent to prefer the goal it attained through costlier actions... an abstract variable such
  as force, work, or effort." → PREDICTS the agent should read the COST/persistence of its
  own failed pursuit as evidence about which goal mattered. Corroborates "describe the gap."
- Open-ended sequential inverse plan search / SIPS (Topics in Cognitive Science 2026, 10.1111/
  tops.70075): "combines top-down Bayesian inverse planning with bottom-up sampling based on
  the statistics of co-occurring subgoals... propose goal hypotheses related to the subgoals
  achieved by an agent... then filters out goals that would be irrational given the actions."
  → PREDICTS generate goals from achieved subgoals' statistics, then PRUNE by consistency
  with the observed failure. Directly corroborates subgoal-based generation + ground pruning.
- Goal inference with reward-producing programs (Davidson et al., physics game): represents
  goals as programs in a DSL and does IRL over demonstrations; "far from perfect" but above
  chance → PREDICTS a grammar of goal-programs + ground feedback can recover hidden goals
  without enumerating all of them. Corroborates the grammar-based lookup (Fig 9).
- Plan-predictability bias (Zhang et al. 2018, ar5iv 1805.06248): humans use "predictable"
  plans, not full inverse planning, under bounded rationality; model correlation 0.916 vs
  0.765 → PREDICTS rank goal candidates by simple predictability (a cheap structural reading)
  rather than exhaustive evaluation. Corroborates ranked, reversible narrowing.

VERDICT (from the figures): do NOT add a "goal discovery" heuristic or tune to games. Change
goal formation to run the Fig 9 loop on the `arrived_no_clear` residual:
1. DESCRIBE the gap in effect terms — "I met my own condition and the ground did not clear" —
   as a first-class row (it already exists as `arrived_no_clear`; make it the trigger).
2. UNBUNDLE it (Fig 9 :55-58): the compound is (my condition was insufficient) ∪ (another
   condition is unmet). Do not treat it as one harder goal.
3. LOOK UP a frame whose closure predicts the win condition's shape — the library/imports/
   priors (word_map shape_bridge, tether rule cards, RDL preloads) — by residual shape
   (arity/symmetry/scale), one-pass matching (Fig 9 :29), not a search. Fig 8 :53-54.
4. NARROW the candidate goal conditions by consistency with the observed failure (the ground
   refused my met goal), keeping every cut ranked and reversible (Fig 13).
5. Contact, not proposal-count: if the win condition needs a reading the closure lacks, the
   answer is an import/instrument (Fig 6 :23, Fig 8 :46), never more internal goals.

This turns goal formation from "propose a satisfiable proxy" into "read the ground's refusal
as the direction." The world literature (SIPS, cost-inference, DSL goal programs) corroborates
that this is how goal-directed agents actually find hidden goals: generate from subgoals'
statistics, prune by observed failure, infer from effort.

cost if wrong: a bad lookup frame could steer goals toward a plausible-but-wrong shape —
mitigated by ground pruning (every candidate must survive the recorded refusal) and by
keeping cuts reversible. undoable: yes, each is behind its own arm with an OFF identity row.
reversed by: a game where `arrived_no_clear` is followed by a clear under the current single
goal formation (then the gap is not structural); or Isaiah ruling that lookup should draw
on a specific source we have not included.

NOT done: no ARC-game tuning, no code changed, no answer encoded. This is a design verdict
for the next L1 item, to be implemented behind a switch with must-fails and a DECIDES line.
