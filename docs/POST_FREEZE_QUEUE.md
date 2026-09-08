# THE POST-FREEZE QUEUE — for review before anything is lifted

**Status.** `arc-freeze-01` intact. 92 commits since the tag, all documentation, no build file
differing. Nothing below has been applied.

**How to read it.** Four kinds of item, and they are not the same size of decision:

    MECHANICAL   a defect with a candidate fix and a reintroduce-the-defect test. No ruling needed
    VOCABULARY   new atoms. Needs an ENTRY CLAUSE written, because none satisfies the existing two
    TYPING       the graph the composer walks. Code, but it changes what is reachable
    DOCTRINE     touches the firewall or the terminal condition. Yours alone

---

## 1 · MECHANICAL — six system errors, fixes written, none applied

| | defect | scope | candidate fix |
|---|---|---|---|
| **S1** | `probe.choose` divides by zero on an empty action tuple | 6 of 25 games | take the existing no-action outcome where `self.actions` is empty |
| **S2** | `arc_holdout.play` crashes assembling its report — `by` is a `str` on action rows and a `dict` on the `mode` row | every run | key the counter on one type, or stop reusing the field name |
| **S3** | four of eight gates in `_mint_routine` return with no ledger row | every board | a `routine_refused` row at each, carrying that gate's own reason |
| **S4** | `_install_reuse` admits 19 of 21 terms the bargain would refuse | 5 of 5 boards | consult `pays` on that path, as its own docstring proposes |
| **S5** | `by == "discriminate"` excludes `discriminate:learned` by exact match | 6 of 10 boards | match the family, `by.startswith("discriminate")` |
| **S6** | probe rotation coverage requires `gcd(7, n) == 1`; collapses to ONE action at `n = 7` | latent — max surfaced is 6, advertised reaches 7 | a step coprime to `n` by construction, or a per-run permutation |

**S1 gates every zero-action game, which is what an IQ item is.** Nothing else on this list matters
for static puzzles until it is fixed.

**S4 carries a held question that is yours:** whether a REUSED term should be priced at full
`term_bits` at all. If reuse is properly cheaper, nineteen refusals are nineteen correct admissions
at a wrong price. The measurement is unambiguous; the interpretation is not.

---

## 2 · VOCABULARY — seven atoms, all implementable, all needing an entry clause

`SHAPE` is a `frozenset` of normalised `(row, col)` offsets — the literal cell set — so everything
below is computable from what perception already yields.

    holes      SHAPE    -> EXTENT     §12.4's own worked example
    perimeter  SHAPE    -> EXTENT     same class; boundary length from the cell set
    parity     POSITION -> BOOL       §12.4's other worked example
    rotate     SHAPE    -> SHAPE      FIRST CYCLE in the OBJECT component
    reflect    SHAPE    -> SHAPE      likewise
    inside     OBJECT   -> BOOL       not derivable from `touching`
    count      group    -> EXTENT     see §5 — needs the group fold to produce a value

**`rotate` and `reflect` are more than vocabulary.** A `SHAPE → SHAPE` self-loop makes the OBJECT
component cyclic for the first time, so `rotate . reflect . rotate` is a valid chain and `max_depth`
starts binding instead of being decoration.

> **THE ENTRY CLAUSE MUST BE WRITTEN, NOT INVOKED.** `CLAUDE.md`'s rule has two clauses — *the loop
> cannot run without it*, or *the agent minted a crude version and we are promoting it*. **None of
> these satisfies either.** The loop RUNS without `holes`; it cannot EXPRESS it. That is a third
> clause, and it must be **stamped per atom at entry**, because the ablation partition cannot be
> rebuilt from a `prior` stamp afterwards.

---

## 3 · TYPING — two fixes, both code

**3a · The sensor registry consumes no attribute type.**

    components  (FRAME,)                -> OBJECT
    colour      (OBJECT,)               -> COLOUR
    position    (OBJECT,)               -> POSITION
    extent      (OBJECT,)               -> EXTENT
    shape       (OBJECT,)               -> SHAPE
    overlap     (OBJECT_BEFORE, OBJECT) -> RATIO
    delta       (OBJECT_BEFORE, OBJECT) -> DELTA
    touching    (OBJECT, OBJECT)        -> BOOL
    changed     (FRAME, FRAME)          -> REGION

Inputs are `FRAME`, `OBJECT`, `OBJECT_BEFORE` and nothing else, so the longest chain is
`FRAME → OBJECT → attr`. **`closure=4, composable=0, verdict=unreached` on every board is a TYPING
ARTEFACT, not a verdict about composition** — and §12.4's INWARD branch cannot run at all.

**3b · The atom graph terminates.** `OBJECT → attr → PRED → OBJ`, three arrows, `OBJ` terminal,
no back-edge. `max_depth = 3` matches the graph exactly, which is why the bound has never bound and
`budget_exhausted` has never fired.

---

## 4 · STRUCTURE — the largest item, and it should be ruled on BEFORE the atoms

**A `Term` is a linear chain with one operand slot.** Its own docstring: *"A composition of atoms
applied left to right… **a chain has no branch**."* The operand is *another slot's value* — a raw
reading, never another term's output.

**So the term space cannot express:**

    ∥   alternatives          a chain has no branch
    +   joining two COMPUTED  the operand is a slot reading, not a computation
    ⇒   a second arrow kind   there is one
        disjoint outputs      a term returns one value

**And the act space already has the tree algebra the concept space needs** — `Seq` / `When` / `Until`
— though `When` has no else, so `∥` is absent on both sides.

> **THE SEVEN ATOMS DO NOT BEAR ON ANY OF THIS.** If DAG-shaped concepts are the target, the honest
> move is making the term space a tree the way the routine space already is. **That decision should
> come first, so vocabulary does not land and read as progress toward it.**

---

## 5 · NEW GAPS — found by reading the library, this pass

**G1 · No boolean algebra.** There is no `PRED → PRED` atom. `all`/`any`/`none` are quantifiers
(`PRED → OBJ`), not connectives. **An objective is always ONE predicate quantified** — *all objects
are red AND square* is not expressible.

**G2 · No cardinality.** There is no `count` atom anywhere. **`sensors.py:58` declares a `COUNT`
type and nothing produces or consumes it.**

**G3 · No arithmetic beyond `translate`.** No ratio, product, divide or modulo.

**G4 · Two orphaned sensor types.** `RATIO` and `REGION` are produced by sensors and **consumed by no
atom.** `overlap` and `changed` compute readings the composer cannot touch.

**G5 · No literals.** `Term.operand` is *which slot fills operand 0* — a slot, never a constant. A
rule keyed to a specific value needs a slot that happens to hold it.

### And the finding that ties §12.4 to all of this

**§12.4 gives three worked examples of INWARD composition, presented as *"inside the closure, priced
by the same bargain"* — i.e. as things already reachable. Checked one by one:**

    parity(position)              parity  ABSENT
    ratio(count(a), count(b))     count   ABSENT · ratio ABSENT · RATIO orphaned
    holes(shape)                  holes   ABSENT

**None of the three is reachable, and the middle one needs two primitives that exist nowhere in
either the sensor set or the atom set.** The section describes a closure the build does not have.

---

## 6 · DOCTRINE — yours alone

**6a · The group constructor, and it is a firewall question.**

    arc_world.peers()
      "{slot: the SAME attribute on every OTHER object}. **The loop may not derive this**
       -- it would have to split the slot name, which is reading domain structure."

**The group is handed by the environment, is one fixed partition, and the loop is forbidden from
deriving it.** Six separate gaps — group-to-group relations, centroids, rank mapping, regrouping by
predicate, symmetry axes, group-scoped rules — **have this one cause.** A group constructor the loop
can drive *is* the loop reading domain structure, which is what `peers()` was declared in `arc_world`
to prevent.

**6b · The only fold over a group produces `PRED`.** No `group → element` (ranking) and no
`group → scalar` (counting, centroids). One missing arrow, several missing capabilities.

**6c · `_group` is one attribute column.** Collinearity and equidistance need `row` and `col`
jointly; nothing zips two columns.

**6d · No transitive fold over a relation.** Containment *depth* needs a fold over a chain of
relations; every relation atom ends at `PRED`.

**6e · No sequence type.** `_group` is ordered by peer iteration, not by position — no index, no
permutation operator.

---

## 7 · OWED IN A WORKING FILE

**`CLAUDE.md` carries a prohibition this window attributed to §12.4 for four sweeps.** §12.4 forbids
nothing — it lists `holes(shape)` as the INWARD remedy. `CLAUDE.md` is working and repairable at
source; **that repair is owed and is mine.**

---

## 8 · HELD OUT UNTIL MEASURED

**The cost wall.** On `lf52`, per-call cost rose ~60% while `_cannot_pay` calls stayed **flat at
7801** for twelve cycles. That contradicts `LOG 3`'s *the wall is a growing candidate space*. **One
board is not enough** and it stays out of `LOG 3` until a second board agrees or refuses.

---

## 9 · WHAT THE WINDOW ESTABLISHED THAT BEARS ON ALL OF IT

    composition works        20 composed terms across 3 boards, one at depth 3
    chunking works           6 chunks settled unaided; units 23 and 25 against 21 atoms
    the search is exhaustive budget never binds; max yields 1884 against a 4000 cap
    the trigger fires        tr87 unaided, 2 of 9 gate evaluations
    the route mechanism      passes on 4 of 8 boards when reached
    the genuine negative     B fires 2 of 4 on tr87 UNAIDED, and 0 of 29 under override

**`levels_completed` is 0 and `done` is 0.** Everything above is mechanism, and the capability
position is unchanged.
