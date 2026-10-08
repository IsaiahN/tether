# Metaprogramming — the design the seat builds from

Reviewer seat, 2026-10-08. Read against `seat-act` e50406d: `gamma.Atom` / `Ctx` / `Term` /
`Gamma` (construction, `promote`, `units`, `save` / `load`); `arc_atoms` (the 50 operations and
27 extract atoms, per the seat's export); `composer` (`bind`, `Bonded`, `settle`, `holds`,
`settle_tree`, `lookup`); `condition` (`parse`, `evaluate`); the reach site at `tether.py` ~1692
(`retrieval.characterise` → `composer.lookup` → `read_pairs`); `Agent.cue` (`_narrate_cues`, no
consumer on the reach path). The library and its runtime are in `library/` (cohesion v2).
**No game testing while this is built** (Isaiah 2026-10-08). Every step is proven on fixtures.

---

## 0. The one decision everything follows from

**The library is REACH; Γ is what the agent HOLDS. Nothing enters Γ's alphabet by being
preloaded.** A library entry becomes something the agent can bet with only as a **TERM over Γ's
existing atoms**, compiled from the entry's candidate, adopted by the mint, and held under the
same rules as every other term.

Why, by the figures and the code's own record:
- **Price.** Figure 12 / the Operators table: |φ| = (k+1)·log₂(|atoms|+1) + (k−1)·log₂(|bonds|).
  Registering 4,000 entries as atoms would raise every term's price by about log₂(4,000/77) bits
  per atom slot. That is the alphabet inflation F503 already measured on ten unpublished atoms.
- **Loading is not entering.** `Gamma.__init__`'s own docstring retires the `molecules` parameter
  as "the one route by which a term could enter Γ without being earned". The visible set
  replaces it: "a term is visible, aimed at, and enters only when regenerated".
- **Figure 12:** *"A settled molecule becomes an atom for whatever composes over it"*. Γ already
  does this through `units()` and `promote()`. A compiled library term that settles becomes a unit
  by the existing path, with no new registry.

**So `Gamma.register` is NOT built** (this revises LIBRARY_SPEC §5 #3). What is built is a
**compiler** from library candidates to Terms. The 4,000 entries never become 4,000 functions:
each is compiled, on demand, into a composition of the 77 atoms Γ already has.

## 1. What exists and is reused unchanged

| piece | where | role here |
|---|---|---|
| `Term` (atom chain, `operand`, `operand_term`, `guard`) | gamma.py | the compiled form of every grounded candidate |
| the 50 operations + 27 extract atoms | arc_atoms / arc_predict | the alphabet everything compiles into |
| `composer.bind(bond, l, r)`, `Bonded`, `settle`, `holds`, `settle_tree` | composer.py | molecules and CAUSE/RESULT views: the ONE bond constructor; ⇒ and − are TESTED over frames by `holds` |
| `condition.parse` / `evaluate` (three-valued) | condition.py | the reference semantics every compiled term is checked against |
| `retrieval.characterise` | retrieval.py | the residual's scoped description: the query that ranks what is lit |
| `Gamma.promote`, `units`, `Standing` | gamma.py | settled → unit → atom-for-what-composes-over-it |
| `Gamma.save` / `load` | gamma.py | carrying; extended with `carry_check` (§6) |
| `observer.Live` → `Agent.cue` | arc_world / tether | the change that lights the library |

## 2. New pieces (four modules, small)

| module | public interface | size |
|---|---|---|
| `library/library_runtime.py` | `Library(root).load()`, `.light(changed)`, `.molecules_lit(lit)`, `.view(key, role, o, x)`, `.role_table(key)`, `.invent_atom(...)`, `.mint_recipe(...)`, `.carry(key, game)`, `.save_runtime()`; `carry_check(cond, readings)`, `axis_forms(cond)` | exists (reference; the seat owns it) |
| `compile_term.py` | `compile_candidate(cand, slots) -> Term \| Refusal`; `compile_view(entry, role, o, x, slots) -> list[Term \| Bonded \| Refusal]`; `compile_molecule(entry, lit_terms) -> Bonded \| Refusal` | new, about 200 lines, pure |
| `cue_bridge.py` | `changed_readings(cue) -> dict[reading, n]` | new, about 40 lines, pure |
| tether.py reach site | about 30 lines at the existing `composer.lookup` call | wire |

## 3. The compile table — every template, its Term, or its named refusal

Slots are as `arc_world` publishes them: `o1.h`, `o1~o2.contact`, `@goal.completed`. A term runs
on ONE slot's value; a second object arrives as the OPERAND (another slot's value, never a
constant). This is the existing `Term` contract.

| template (reading type) | condition | compiled Term | status |
|---|---|---|---|
| DELTA moves | `o.r != 0` | on `o.r`: `abs_delta . sign` | compiles |
| DELTA up | `o.r > 0` | on `o.r`: `sign` | compiles |
| DELTA down | `o.r < 0` | on `o.r`: `both` with operand_term `abs_delta . sign`, applied to `sign . negate` | compiles as a tree |
| DELTA with / unlike | `o.r == x.r` / `!=` | on `o.r`: `same<x.r>` / `other<x.r>` | compiles |
| EXTENT, POSITION more / before | `o.r > x.r` | on `o.r`: `above<x.r>` | compiles |
| EXTENT, POSITION less / after | `o.r < x.r` | on `x.r`: `above<o.r>` (binding reversed) | compiles |
| EXTENT, POSITION same / level | `o.r == x.r` | on `o.r`: `same<x.r>` | compiles |
| EXTENT present | `o.r > 0` | — | **REFUSED: no zero-test on EXTENT** (§7, item a) |
| COLOUR, SHAPE same / other | `o.r == x.r` / `!=` | on `o.r`: `same<x.r>` / `other<x.r>` | compiles (nominal: no `above`, refused by type) |
| BOOL holds / fails | `o.r == 1` / `== 0` | on `o.r`: `idn` / `negate` | compiles if BOOL flows into PRED (fixture decides; §7, item b) |
| BOOL both | `o.r == x.r` | on `o.r`: `same<x.r>` | compiles |
| PRED pair holds / fails | `touching(o, x) == 1` / `== 0` | on any `o.*`: `owner . touching` / `owner . touching . negate` | compiles |
| pair EXTENT present / absent | `contact(o, x) > 0` | — | **REFUSED: no zero-test on EXTENT** (§7a) |
| pair DELTA up / down / moves | `dcontact(o, x) > 0` | on `o~x.dcontact`, as DELTA above | compiles once the observer publishes it |
| board present | `board.completed > 0` | — | **REFUSED: no zero-test on EXTENT** (§7a) |
| event occurs | `frame.came > 0` | — | **REFUSED: events are not slots** (§7c) |
| CAUSE / AGENT / RESULT | `A ⇒ B` | `composer.bind("⇒", term_A, term_B)`; settled by `holds` over the residual's frames | compiles as a Bonded |
| INSTRUMENT | `touching(o, x) == 1` + `B` | `composer.bind("+", owner.touching, term_B)` | compiles as a Bonded |
| a molecule | operands with junctions | `bind(j1, t1, bind(j2, t2, …))`, `?` junctions stay UNKNOWN | compiles as a Bonded |

**THE EQUIVALENCE RULE.** For every row that compiles, the Term, evaluated on a fixture frame,
must give the same three-valued answer as `condition.evaluate` on the same frame. Two
independently written evaluators agreeing is the check that the compiler means what the library
says (Figure 10: a convention nothing can check is a constant the seat authored).

## 4. The reach step, per frame

1. `changed = cue_bridge.changed_readings(self.cue)`: which readings moved this frame, with
   counts. Blind frame → `{}`, an abstention, not an empty reading.
2. `lit = lib.light(changed)`: entries ranked by the share of the change they read. **Order,
   never exclude.**
3. Re-rank `lit` by the residual's scoped description (`retrieval.characterise`): an entry
   reading a slot the residual is on comes first. This is the description Figure 9 says decides.
4. For the top entries, while the step's search allowance lasts (the same allowance the term
   enumeration already spends; no new constant):
   - `view(entry, role)` for EVERY role: no rule picks one. Each role's candidates are ranked
     by how well they fit the residual's description: a value residual favours STATE, a change
     favours PROCESS, a change after contact favours CAUSE. Accumulated, never chosen by an
     ordered rulebook (Isaiah 2026-09-25: "ACCUMULATION + THRESHOLD, NOT A RULEBOOK");
   - `compile_view(...)` gives the Terms;
   - add them to the mint's candidates, ORDERED after contact (F510's order), each stamped with
     provenance `{library: key, role, template}`.
5. `lib.molecules_lit(confirmed)` → `compile_molecule` → Bonded candidates, priced like any
   composition (`composer.node_length`).
6. **The mint decides, unchanged.** The bargain prices every candidate; the library offers and
   never chooses (Isaiah 2026-09-28: reasoning offers, the agent chooses).
7. A refusal is recorded per frame (`book["library_refused:<reason>"]`), so §7's gaps are
   measured, not guessed.

## 5. When a library term is adopted

- **The term is held like any minted term,** with origin `MINTED` and its stamp carrying
  `library: <key>`. That is the pair Figure 13 names: *"That record is not documentation of the
  term. It is the term."*
- **Standing, settling, refutation and promotion are the existing machinery.** Promotion to a unit
  is Figure 12's "settled molecule becomes an atom". No special path, no head start.
- **The library runtime records the adoption** (`runtime.json`: entry, game, cycle), so the next
  game's lighting prefers entries this agent has used (by track record, not by a price discount:
  Isaiah 2026-09-29).

## 6. INVENTED and IMPORTED

- **INVENTED.**
  - **Trigger:** an abstention receipt (searched, the change recurred, and nothing lit expresses
    it), the 2026-10-04 conditions.
  - **What it is:** the agent's own condition over the readings that moved, compiled to a Term,
    held with origin `INVENTED` and a generated handle as its name. Its library entry comes from
    `Library.invent_atom` (reads parsed from the condition, role table generated).
  - **Why it does not contradict 2026-10-06 decision 6** ("invented atoms skipped on load"): that
    ruling is about the old invented atoms, which were replayed effect tables, recordings
    (Figure 4). An invention that passes `carry_check` is a method made only of relations, and it
    carries. One that names a raw value stays in its episode, refused with its reason.
  - **Decision 6 stands for recordings.** This line goes to Isaiah to confirm (RULINGS_CHECK B1).
- **IMPORTED** (across games). `Gamma.save` writes each held library-derived and invented term
  with its condition. `Gamma.load` applies `carry_check` and offers `axis_forms` (turned and
  mirrored) as candidate rebindings at the destination. Standing is re-decided there.

## 7. Gaps the census will measure; the seat proposes, the reviewer rules

- **(a) No zero-test on EXTENT.** `sign` takes DELTA only, so "present", "absent", contact > 0 and
  progress > 0 do not compile.
  - **Smallest candidate:** `sign` gains `also_accepts=(EXTENT,)` (a type widening, no new atom).
    It also gives "came this frame" as `age . sign . negate` once `age` is published.
  - **Process:** measure first how many library candidates the widening makes compile, then rule.
- **(b) BOOL into PRED.** Whether `negate` (PRED → PRED) accepts a BOOL slot is a type question
  the equivalence fixture answers. If it refuses, the gap is named, not patched.
- **(c) Events as slots.** came/gone are frame events, not slots. Proposal: none until (a) lands,
  since `age == 0` covers "came".

## 8. Commits, in order — each its own, through the fast gate, with fixtures

| # | commit | must PASS | must FAIL (the mutation is caught) |
|---|---|---|---|
| M1 | `cue_bridge.py` | a planted cue (`o1` moved, `o2` changed colour) → `{drow:1, dcol:…, colour_changed:1}`; blind cue → `{}` | a cue with an unknown attribute raises, it is not dropped silently |
| M2 | `compile_term.py`, table rows only | **the equivalence fixture:** every compiling row agrees with `condition.evaluate` on 12 hand-built frames (planted values, both objects, both signs, zero) | swap `above`'s binding in the "less" row → disagreement caught |
| M3 | the compile census (record-only) | over the library: share compiled / refused, by reason, per role; posted, not gated | — |
| M4 | the reach wire (§4) behind NO new arm (ruled ON; the library is the plan of record) | on the fake world, a planted contagion (touching ⇒ colour change) puts `Contagion`'s CAUSE term in the mint's candidates with provenance | with the library emptied, the same frame offers nothing from it, and the old path is unchanged byte for byte |
| M5 | adoption records (§5) | an accepted library term carries `library:` in its stamp and appears in `runtime.json` | a term adopted twice is one record, not two |
| M6 | invent (§6) | an abstention receipt plus a recurring change → an INVENTED term held, whose condition compiles and agrees with `evaluate` | an invention whose condition names a colour index is refused for carry; one with no reading is refused at creation |
| M7 | carry (§6) | save → load: a relational term arrives with its turned and mirrored forms offered | a raw-value term does not arrive, and the refusal is counted in the load report |
| M8 | Kaggle bundle ships `library/` | the bundle lists every library file; a load from the bundle reproduces `index.json` | removing one file from the bundle fails the bundle check |

**Order after M8:** the doc deletions (DOCS_CONSOLIDATION) and the retirements (`detectors.py`'s
hand-written predicates, `sensors_heavy.py`, `inherited.reach`, superseded by M4). Only then is a
game run considered, and that is Isaiah's call.

## 9. Figure census
- **Figure 6:** *"What is recorded only grows. What is reachable is derived, and it can fall."* The
  library is the record; what is offered is derived per frame.
- **Figure 9:** *"Nobody chooses. The gap does, and the gap is only as good as its description."*
  The residual's description ranks what is lit (§4.3).
- **Figure 12:** the price formula (§0); *"A settled molecule becomes an atom for whatever
  composes over it"* (§0, §5); the bond as one parameter (`bind`).
- **Figure 13:** *"That record is not documentation of the term. It is the term."* (§5).
- **Figure 4:** *"A recording carried upward looks like knowledge and is a description of one
  occasion."* (§6).
- **Figure 10:** *"a convention nothing can check is a constant the seat authored"* (the
  equivalence rule, §3).

**Strained:** §4.4's "top entries while the allowance lasts" uses the existing search allowance.
If measurement shows the library's candidates crowd out the existing path, that is a finding for
Figure 8 (unreachable at this budget), not a cap to invent.
