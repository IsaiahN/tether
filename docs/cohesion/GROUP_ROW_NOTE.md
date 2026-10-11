# Family 2, the group row -- a design note (no build)

Seat, 2026-10-11, for the reviewer's 14:17 CDT ruling ("design note first"). Measured on the
library at 22d8273 with the ARC atom set; the arm OFF unless stated.

## What the family is

The RULE role is 89,986 candidates, and every one is an ordinary condition with
`quantifier: "ALL objects, every frame"` beside it. compile_term refuses any candidate that
carries a quantifier ("quantified over the group: needs a group row (not ruled)"), so the whole
role compiles to 0. Set the quantifier aside and the conditions split three ways:

| kind | rows | the condition alone compiles |
|---|---|---|
| one object (`o1.h > 0`) | 30,715 | 18,315 yes, 12,400 no (their own families: events, board) |
| two objects (`o1.col < o2.col`) | 57,652 | 57,652 yes |
| board (`board.completed > 0`) | 1,619 | 0 (the board is not an object slot) |

## (a) What a "group row" is, concretely

There is no quantifier in the condition grammar: the candidate is a plain condition over role
variables (`o1`, `o2`) and the quantifier is a separate field. Read literally, a RULE row says
*for every object (and every ordered pair), at every frame, the condition holds* -- an invariant
of the world, not a state to reach. A "group row" is therefore the condition evaluated over the
population the world declares (`env.peers()`: the same attribute on every other object) and
combined with AND, on each frame.

## (b) Can RULE rows compile onto what the agent already holds, without a new reading?

By template, measured:

- **Two objects, `same` / `level` (20,043):** "every pair is equal" is "every object shares the
  value" -- the existing group atom `all_same`. ROUTING, no new reading.
- **Two objects, `other` (2,477):** "every pair differs" is "all values distinct" -- the existing
  `distinct` count equal to the group size. ROUTING, with one comparison.
- **Two objects, `more` / `less` / `before` / `after` (35,132):** UNSATISFIABLE as quantified --
  over all ordered pairs, a > b and b > a cannot both hold. These rows say nothing true of any
  world; they are a template applied to a quantifier it cannot carry. Proposed: BOUNDED, recorded
  as vacuous, never compiled.
- **One object that compiles (18,315):** "every object satisfies P" is the compiled per-object
  term applied to every peer slot and ANDed. The term already exists (e.g. `sign` on `o1.h`); the
  group row is an evaluation over `env.peers()`. ROUTING -- an n-ary form of the goal chain's
  two-part `_Pair`, no new atom.
- **One object that does not compile (12,400) and board (1,619):** they stay in their own
  families (events, board); the quantifier adds nothing to fix. The board rows' quantifier is
  vacuous (no object variable).

So (b) is YES for 40,835 rows (20,043 + 2,477 + 18,315) -- routing, not vocabulary -- and the
remaining 49,151 are vacuous (35,132) or refused for their own reasons (12,400 one-object +
1,619 board). 40,835 + 35,132 + 12,400 + 1,619 = 89,986.

## (c) The cost in closure

Routing adds no atom: `all_same`, `distinct`, `sign` and the comparison atoms are already in the
set, so the closure is unchanged (x1.00 at d2/d3/d4). The cost is evaluation: one compiled term
per peer slot per frame, i.e. the group's size, at the site that holds the goal or tests the law.

## (d) Ten RULE rows by hand (random sample, seed 7)

| entry | template | condition | compiles (quantifier aside) | under the group row |
|---|---|---|---|---|
| DESIRE\|Addictive loop | before | o1.col < o2.col | above on o2.col <o1.col> | vacuous (all ordered pairs) |
| PATHOLOGICAL\|Compassion | more | o1.w > o2.w | above on o1.w <o2.w> | vacuous |
| HABIT\|The inertial self | present | o1.h > 0 | sign on o1.h | every peer's h > 0: routing |
| THOUGHT\|Framing | more | o1.age > o2.age | above on o1.age <o2.age> | vacuous |
| CURIOSITY\|Answer | present | o1.age > 0 | sign on o1.age | every peer's age > 0: routing |
| EMOTION\|Emotion | present | board.completed > 0 | refused: board | vacuous quantifier; board family |
| NOETIC\|Deep flow | other | o1.shape != o2.shape | other on o1.shape <o2.shape> | all shapes distinct: `distinct` |
| LEARNING\|Aha | less | o1.residual < o2.residual | above on o2.residual <o1.residual> | vacuous |
| EMBODIMENT\|Resource gauge | present | o1.stability > 0 | sign on o1.stability | every peer's stability > 0: routing |
| PHENOMENOLOGICAL\|The lifeworld | present | board.completed > 0 | refused: board | vacuous quantifier; board family |

## Ruled (the reviewer 2026-10-11 14:50 CDT)

1. A RULE row is a LAW, not a goal: "for all objects, every frame, P" is a regularity of the
   world, held as the agent's hypothesis and priced against the ground (Fig 5). It becomes a goal
   only through the objective machinery that already exists (completion sweep -> goal condition),
   never by being a library RULE row.
2. The 35,132 ordered-pair rows are RECORDED as vacuous-as-written ("an order over ALL ordered
   pairs is unsatisfiable") and never re-read as "for SOME pair" in code. A re-reading is a
   library-package change (the reviewer's, a v9 candidate), made in the data with the old text
   kept.
3. The 40,835 routable rows are built ONLY if a consumer exists, named first.

## The consumer finding (seat, 2026-10-11, at 4416ab7 + 6/7 staged)

Every reader of a compiled library condition today, by grep of `compile_candidate` / `run`:

| reader | what it reads | takes a RULE row? |
|---|---|---|
| `tether._index_reach` (lookup / fit offers) | `lib.view` over `reach.SINGLE` = STATE, TEST, PROCESS, MEASURE, RELATION, and CAUSE | no: RULE is not a role it asks for; a view is kept only if it lands on the residual's ONE slot (`c.slot == slot`), and a group condition lands on none |
| `tether._goal_condition` (objective build 2) | `_inv_conditions`: the library's TEMPLATES filled over the state's readings | no: never a library row |
| `tether._invent` (7c M6) | the same `_inv_conditions` | no |
| `reach.py` (the offline offer census) | `compile_candidate` on SINGLE / CAUSE sides | no |

The quantifier guard at `tether._index_reach` (`"quantifier" in cand`) sits on the SINGLE roles;
the census counts the QUANTIFIED refusal only in RULE (89,986), so it never fires there.

**No consumer: the routing is NOT built** (no inert arm). Recorded as **routable, no consumer:
40,835** (20,043 all_same + 2,477 distinct + 18,315 per-object AND over peers), beside the 10
UNBOUND settled entries in the ALL-ON orphan list. What would make one: a site that prices a
law (predicted every frame over the peers, refuted on one) -- the agent has no such site today.

## Open for the ruling (as posted, now ruled above)

1. Whether a RULE row is a GOAL (held as a want) or a LAW (predicted, refuted per frame). The
   quantifier "every frame" reads as a law; the goal chain is where the agent holds conditions
   today. The routing above serves either.
2. Whether the 35,132 ordered-pair rows are recorded as vacuous (proposed) or re-read as "for SOME
   pair" -- the latter changes the library's meaning and is not the seat's.
