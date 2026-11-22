WATSON 63 — what "boosting intellect" means in this agent's own terms (2026-11-22)

ISAIAH'S QUESTION: no LLM, no massive model, no massive dataset (ImageNet is optional and enough).
How do you boost THIS agent's intellect and fluid reasoning, from its own constitution and umwelt?

This WATSON answers the CONCEPTUAL question from the figures. Two read-only code audits (the
goal-to-clear chain, and the abstraction/self-reasoning machinery) are running in parallel and
will anchor the "where exactly" half. The figures decide what "intellect" means here before any
code answer is attempted.

QUESTION in effect terms: if "smarter" is not a bigger library or model, what changes when a
system becomes more capable, and which of those changes are available inside this architecture?

DOMAIN CENSUS:
- R: arity = (library, reach, ground); symmetry = a bigger library can leave reach unchanged;
  scale = one agent's lineage across games.
- domains: library (actors: terms / currency: bits / anchor: grammar type system); reach (actors:
  compositions / currency: what settles / anchor: the board); lineage (actors: methods / currency:
  head starts / anchor: the next game's ground).
- order (Fig 3): perception -> vocabulary -> objective -> planning -> learn-and-carry; the chain
  is ordered by dependency and a break upstream starves everything below it.

TETHER (primary, verbatim from source SVGs):
- Fig 11 : "Where nothing maintains anything, intelligence is a label applied afterwards to a
  lineage that met its ground. Nothing was intelligent; selection ran. The word does no work
  there." → "intelligence" is not a property to add; capability is a property of agent-and-habitat
  and is observed in a lineage meeting its ground.
- Fig 11 : "A system cannot be made more capable by improving the agent in isolation. An
  improvement that does not change contact changes nothing, however much it improves." → the
  test of any proposal: does it change contact (what the agent can reach and be corrected on)?
- Fig 12 : "a system that cannot settle has one level however large its library. Nothing composes
  over what was never admitted as a part." : "A settled molecule becomes an atom for whatever
  composes over it... there is no bottom." → FLUID REASONING IN THIS SYSTEM = LEVELS OF
  COMPOSITION. A bigger vocabulary at one level is not more intellect; a second level that a
  settled term can enter is. This is the single sharpest figure line for Isaiah's question.
- Fig 3 : "learn and carry: name what worked, verify it, and carry it to the next problem."
  "The break is drawn between three and four as an illustration. Where a given chain stops is a
  reading, never a property of the chain." "Before asking whether a system is good, ask which link
  it currently stops at, and whether the answer was measured or assumed." → the method: FIND THE
  BREAK. T0 measured the break at subgoal 0/6 (planning/decomposition), not at perception.
- Fig 1 : "The residual is indexed by object slot, not aggregated" ; "a global R near zero with
  one live slot residual is a legal state" → the only signal for where to look is per-slot, never
  a global score; intellect is not a summary number.
- Fig 4 : "Only methods cross up. Only head starts come down." "upward: a method that can be
  reapplied. Never the recording of a particular success." → what carries across games is a
  METHOD (a composition rule), never a recorded answer; this is the lineage half of intellect.
- Fig 8 : "two frames together reach what neither reaches alone... that surplus is where imports
  live." → the outside world enters only as a second frame via import, not as bulk data.

VERDICT from the figures (the shape of the answer to Isaiah's question):
"Boosting intellect" in this architecture has exactly three available levers, and none is a bigger
model or dataset:
1. LEVELS (Fig 12): make a settled composition re-enter as an atom for the next composition.
   This is the Fig 12 conformance already identified — representation fixed by Fix 1, the operand
   arm the live gap. Without it the agent has "one level however large its library" — which is
   precisely its current state and why more ImageNet data does nothing for reasoning.
2. THE BREAK (Fig 3): the T0 chain stops at subgoal (0/6). Fluid reasoning in the loop is the
   goal->refusal->repair->subgoal->clear chain; strengthen the link that is measured broken, not
   the links already at 6/6. The two audits locate this write-site precisely.
3. CARRY (Fig 4 + Fig 3 link 5): what transfers across games is a method, not a recording. The
   round trip (T_A/T_E) and the abstraction machinery are the substrate; whether they are read or
   only recorded is the second audit's question.

What is explicitly NOT a lever: a larger corpus (Fig 8/12 — surplus is at the boundary, not in
quantity), a larger model (no model in the decision path by constitution), a global score or proxy
(Fig 1), or an LLM in the loop (Fig 10 — a verifier that can reconstruct the claim cannot verify
it; the agent must remain the verifier).

COST IF WRONG: effort spent above the break arrives at a step that cannot use it (Fig 3); the
cheapest reading is to measure where the chain stops first. UNDOABLE: each lever behind an arm with
OFF identity. REVERSED BY: a per-game run showing the strengthened link did not move clear/subgoal.

This is the conceptual derivation. The concrete "where exactly" comes from the two audits + the
existing measurements: 0/6 clear, subgoal 0/6, operand arm offers only gamma.atoms, priors held
priority-only by design. Those are the three sites the figures point at, in Fig 3 dependency order.

FIGURE CENSUS: Fig 1 · Fig 3 · Fig 4 · Fig 8 · Fig 11 · Fig 12 (verbatim from SVGs). Strained: none.
