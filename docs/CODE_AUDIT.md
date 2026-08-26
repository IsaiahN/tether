# Root code and toyworld, against the doctrine

Everything below was found by running the code, not by reading it. Each item names how it
was demonstrated.

---

## A · The record says something the code does not do

**Legibility is the instrument.** These are the ones that matter most, because each makes
the agent's own account of itself false.

### A1 · `speak.py` cites a field REPAIRS 1 deleted

`Drive.err` went when the EMA went. `speak.py:73` still reads `d.get('probe_err')`, so
the utterance renders:

    Nothing has surprised me for a while -- my own error is None over 54 observations.

### A2 · The probe records a perturbation that never happens

`Drive.choose` increments `fires` when bored and then returns **the identical draw**:

    bored() == True   fires == 6
    draw when awake : ['A', 'B', 'C', 'A', 'B', 'C']
    draw when bored : ['A', 'B', 'C', 'A', 'B', 'C']
    the draw actually changed: False

The module docstring promises `nothing is surprising -> perturb`; the ledger row says
`perturbing`. Seed 7 logged 54 fires, none of which changed an action.

### A3 · `starving()` is computed, reported, and wired to nothing

It IS called -- by `Drive.report()`, so it reaches the ledger. Nothing branches on it.
The module announces `Two triggers, on two channels`; one has a branch, and that branch
is A2.

### A4 · The contract says eight and enforces ten

`REQUIRED` has ten members since `actions` and `alphabet` were added. Seven sites still
say "eight", and `demo.py:52` prints a hardcoded

    env contract: 8/8 members

immediately after `bind` enforced ten. The demo asserts a falsehood about the check it
just ran.

---

## B · Dead code

    ledger.Ledger.origin_of      0 references
    instruments.STAGES           dead -- its 3 "refs" are conform/check.py's own STAGES
    snaps.ladder                 never called

`snaps.ladder` is the DS level sequence. Per the module's own docstring, DS is *the only
reason transfer is measurable at all*. Nothing runs it.

---

## C · Why the checker did not say so

Three separate holes in ISOLATED, and every one of them is the class the five laws are
about.

### C1 · Every word in every string literal counts as a reference

`_scan`:

    elif isinstance(n, ast.Constant) and isinstance(n.value, str):
        for w in n.value.split():
            refs[w] += 1           # registries and __all__ name by string

So a function whose name is an ordinary English word can never be flagged, because the
codebase's own prose mentions it. `snaps.ladder` has four "references" and all four are
the word *ladder* in docstrings. **In a codebase written to be this prose-heavy, the
comment style disables the dead-code rule.**

### C2 · Only `tree.body` is examined

    defined = {n.name: n for n in tree.body if isinstance(n, (FunctionDef, ...))}

Module level only. Methods are invisible -- `Ledger.origin_of` has 0 references and is
never reported.

### C3 · Names are matched bare, across the whole package

`instruments.STAGES` is cleared by `conform/check.py`'s unrelated `STAGES`. Any name
reused anywhere is exempt everywhere.

---

## D · Denominators and keys

### D1 · `Gamma.units()` dedups on a key it does not emit

`seen` tracks `t.name`, which carries `<operand>`. `out` appends `Term(t.atoms)`, which
drops it. Two settled terms differing only in binding both become the same unit:

    settled: ['inc . wrap<a>', 'inc . wrap<b>']
    units  : [... 'inc . wrap', 'inc . wrap']      duplicate units: 1

`len(units)` feeds `space_estimate`, which is the denominator of `coverage` on every mint
row. *Witness the boundary, not the decision -- exemptions and denominators.*

### D2 · A default that asserts the strongest claim

`tether.mint` seeds `stats = {..., "depth_exhausted": True, ...}`. Nothing reads that key.
A dead default claiming *I saw the whole space* is dead in the dangerous direction.

### D3 · `world.unreachable_slots` sweeps a diagonal, not a grid — latent

    st = {s: (v if s == slot else (v + 1) % M) for s in slots}

Every other slot gets the same value, so no two operand bindings are distinguishable and
the sweep is one line through the state space. It can only over-report reachability.

**Checked against an exhaustive grid sweep on the toy world: they agree (`opaque` both
times).** So this is a hazard, not a live defect -- but it is the harness's answer key,
and `snaps._same` already does it properly with a real grid.

---

## E · The toyworld

### E1 · DS rungs do not deviate as labelled

`_pick` samples from `FAMILIES` and can return the family the slot already has:

    DS 0.4  left every family unchanged           in  55/300 rungs (18%)
            -- the rung labelled "one new family introduced"
    DS 0.8  changed fewer than half the families  in  41/300 rungs (14%)
            -- the rung labelled "half the rules change"

The ladder's entire justification is that *the relationship between consecutive levels is
known*. On roughly one rung in six it is not the stated one.

### E2 · `sys.dont_write_bytecode` sits below the imports

In `snaps.py` it is set after the imports and after `_atoms()`. Every other module sets it
immediately after its imports. Hard rule, and the placement looks like edit drift.

---

## F · What the automated seats actually cover

    ruff        the whole repo including root and snaps        clean
    lint        the whole repo                                  4/4, subject to C1-C3
    kernel      conform/kernel.py's own record                  14 checks
    stateful    kernel.Frame ONLY

**`conform/` never imports `tether` or `snaps`.** The hypothesis harness generates
histories for the reference loop inside `conform/kernel.py`. `tether.py` and `snaps.py`
have zero generated-history coverage -- which is A9 in the audit's own words: *the
reference is not the subject*.

---

## G · Can snaps run on a 64x64 grid?

**The contract: yes, unmodified.** A `Grid` filling the ten members binds with no changes
and no branching -- a cell is a slot like any other, and R indexed per slot is exactly
right for a board.

**The cost: no.** `_bindings(slot)` returns every other slot as a candidate operand, so a
mint is O(candidates x slots) and a step mints per owing slot -- O(slots^2).

     board  slots   8 steps
     3x3        9     2.26s
     5x5       25    14.90s
     7x7       49    54.88s
    10x10     100   227.75s

Quadratic, confirmed: 11x the slots for 100x the time. Extrapolating 28.5 s/step at 100
slots to 4096 gives roughly **13 hours per step**.

The blocker is one line. It is not the architecture and it is not the loop.

---

# C · closed

Fixtures before changes, in every step.

**C1** -- a string literal counts as a reference only when the WHOLE string is an
identifier. `{"ladder": _ladder}` still counts; `"a DS-controlled level ladder"` no
longer does.

**C2** -- class bodies are walked one level down, so methods are subjects. Found
`ledger.origin_of` immediately.

**C3** -- references are scoped per module. And the scope had to SPLIT, which the first
attempt got wrong:

    a module-level name must be IMPORTED to be used   -> scoped to importers
    a method is reached through an OBJECT              -> package-wide

Scoping methods by imports invented dead code rather than finding it:
`agent.phases.level_done()` names `instruments` from a file that never imports it, and
`world.bind` reaches a `Snap` method by `getattr` over a string. Four false positives,
all from that one conflation.

**The witness gained two things it did not have.**

`n_found` pins how many findings the `bad` fixture produces, not merely that it produces
some. Nothing above that line moves when a rule quietly stops catching one shape: the
denominator holds and findings are still non-empty.

`bad_other` / `ok_other` give the rule a SECOND FILE. `ISOLATED` was declared
`crossfile=True` and `selftest` had always handed it `others=()` -- so the half of the
rule that reads other files had never been witnessed at all, by its own fixture, since it
was written.

## What the closed holes found

    ledger.py: `origin_of`   referenced nowhere in the package
    snaps.py:  `ladder`      referenced nowhere in any module that imports it

`ladder` is the finding that motivated all three. It was cleared by three string literals
in `world.py` naming an unrelated `ladder` SLOT -- and both uses are legitimate, so only
name-scoping separates them.

**The board is now honestly red: 6/7, `check.py` exits 1.** `origin_of` is unused and can
go. `ladder` is dead because nothing calls it, and the repair is to wire it up, not to
delete it -- it is the DS level sequence.

---

# D1 · closed, and it had never fired

`units()` now dedups on the unit it EMITS rather than on the settled term's name. The
operand binding is re-decided per slot at mint and `enumerate_closure` composes over
`.atoms` alone, so the chunk IS the atom sequence and the binding has no business in the
key.

Against the case that produced it:

    settled : ['inc . wrap<a>', 'inc . wrap<b>']
    units   : [... 'inc . wrap']      duplicates: 0     (was 1)
    space_estimate over 9 units -> 819                  (was 10 units -> 1110)

**Latent, not live.** Across the 20-world panel, 0 runs had two settled terms sharing an
atom sequence, so no `coverage` figure already written was inflated by it. The trigger
needs two slots settling the same atoms under different bindings, which gets likelier as
the library fills and as slot counts rise -- it was a defect waiting for the runs to get
longer, not one that had been quietly wrong.

`ledger.origin_of` deleted.

**Board: 6/7, `check.py` exits 1, `ladder` alone.** The hook blocks until E1 wires it.

---

# F · closed — the harness now has the shipped code as a subject

`conform/stateful.py` gains a second state machine, `Shipped`, which drives
`tether.Agent` over a generated `snaps` world and asserts the same fourteen checks. The
checks are not rewritten; `Linter.run` takes plain rows and `snaps.Snap` already fills
the ten-member contract, so this was wiring rather than machinery.

**The spec is drawn STRUCTURALLY, not by seed.** `spec_for(seed)` is one integer to
shrink, and shrinking an integer walks toward seed 0 rather than toward a smaller world
-- the minimal failing case would be a number instead of a shape.

**Two seats, not one.** A shared seat would conflate `kernel regressed` with `tether's
record has known gaps`. The second is already true, so a shared seat would be permanently
red and a kernel regression would arrive as no change at all.

    stateful   kernel.Frame     ok
    shipped    tether.Agent     FAIL

## What it found, on the first run

    AssertionError: {'A4': ['@bracket: zero mass, cause=None']}
                    after 1 steps on {'s0': 'action', 's1': 'action'}

**One step, two slots.** The bracket row already carries

    inert="env.transform() is None; no coarse view defined"

which IS `CHANNEL_CLOSED` -- the cause stated in prose where the check wants a field.
That is the whole genus in one row, and the generator shrank to it in seconds. Compare
the A5 cross-slot hole, which needed a slot built by hand before it appeared.

A 30-step record also fails **B2**: `settle` rows carry no `asked` / `ground_said`, so a
frame that never asked the ground is indistinguishable from one the ground paid. `tether`
settles on `r.mass == 0.0` over a held-out transition, so the ground WAS asked -- the row
just cannot prove it. Three checks additionally read UNRUNNABLE (`of`, `from_value`, the
repeat integral): honest field gaps, not silent passes.

**The seat currently fails at step 1, so nothing past A4 is reachable.** Fixing A4 is
what lets the generator start doing generative work rather than reporting the same row
every run.

## Board

    ruff ok · lint FAIL · kernel ok · stateful ok · shipped FAIL · demo ok · gate ok · tests ok
    6/8 seats clean, exit 1

Two true reds: `ladder` (E1) and `A4` (the A-items).

---

# The second generator, pinned — and one line removed for not being able to fire

`snap_specs` was a generator with no pinned width, three inches under a docstring saying
`THE GENERATOR IS AN EXEMPTION, and gets the same treatment as any other`. It now has
`snap_coverage` and `test_shipped_generator_reaches_the_hard_cases`, and the `--tether`
branch runs its own coverage test rather than skipping the other one's.

The shapes pinned are the families the false-mint read named as out of closure:

     200  worlds        51  regime      44  quadratic     39  lagged
      68  slots=3       36  hidden      30  chain

Each narrowing was reintroduced rather than reasoned about. Dropping `hidden` fires;
dropping the RELATIONAL families fires on `lagged`; collapsing the slot range fires.

## The line that could not fire

A fourth assertion, `a relational slot > 0`, was written and then deleted. Three attempts
to make it fail:

    RELATIONAL = ()                  did NOT fire -- `_acyclic` repopulates `reads` on any
                                     chain slot regardless, so bindings still appear
    RELATIONAL = (), no `chain`      fired on `chain`, from the family loop above it
    a relational family, reads=None  KeyError: None -- dies in the world before any
                                     history exists to check

`chain` and `lagged` are asserted above and both are relational, so every narrowing that
empties the bindings trips a family assertion first. **The line could never be the
finding.** That is not a weaker check; it reads as coverage that is not there, which is
the same objection as VACUOUS and as a control that examines nothing.

## Three smaller ones

`snap_specs` handed `_acyclic` a `random.Random(draw(...))` -- a shrinkable integer, and
shrinking one walks toward 0 rather than toward a smaller world. That is the objection
that kept `spec_for(seed)` out of this generator, surviving in the one place it was easy
to miss. The repair's rng is now fixed: the spec is drawn, only the repair of an illegal
spec is not.

The `sys.path.insert` seam now names the three deferred imports that depend on it, none
of which is near it.

**`INCOMPLETE` no longer reads as a finding in the summary.** The three states are kept
apart inside a seat and were collapsing to clean-vs-not in the count, which put
`ran and could not check everything` back on the side of `found something` -- the exact
reading INCOMPLETE was added to prevent:

    1/3 seats clean, 0 found something
    1 stage(s) reported INCOMPLETE: ran and could not check everything, which is not a
      finding about the code.
    1 stage(s) reported DID-NOT-RUN: has not passed; it was not asked.

---

# The record answers five more checks, and the fifth one fails

    A4   zero-mass bet rows name which of the three causes      -> PASS
    B2   settle/demote carry `asked` and `ground_said`          -> PASS
    B3   bet rows carry `from_value`                            -> PASS
    B6   repeat rows carry the monotone integral                -> PASS
    A7   magnitude-carrying rows carry `of`                     -> FAIL, truthfully

    exercised on tether's record:  9 -> 12        UNRUNNABLE:  3 -> 0

Each was a field the frame already had and was not writing. A4's cause is derived from
`tether`'s own state rather than transcribed from `kernel`'s branches -- `len(trace) < 2`
is SLICE_TOO_SMALL, `slot in owed_import` is CHANNEL_CLOSED, which is the distinction
OWES already makes at step 2, moved onto the row.

`of` is a ROW-level key, so `Ledger.Entry` carries it and it is ABSENT rather than None
when a row carries no magnitude: `this row makes no claim` and `this row claims and will
not say` are different readings.

## A7 · the reward channel is an average across slots

    A7  FAIL  seq 5: ['mass'] derived from ('s0', 's1')

The `@objective` row's `mass` is `1 - degree`, and `degree` is `hit / len(slots)`. Naming
one slot in `of` would have made the check pass and would have been the record lying
about where the number came from, so it names all of them and the check says what it
says.

**The aggregation is not in the loop. It is in the contract.** `env.objective()` returns
`(name, degree)` -- one scalar -- so the loop could not index the reward residual per
slot even if it wanted to. That makes this a question about the Env contract rather than
a bug in `tether`:

    widen the contract so objective() reports per slot   an eleventh member, and by the
                                                         doctrine's own reading a step-7
                                                         IMPORT rather than an edit

    accept that the reward channel is global             then its magnitude is not R, and
                                                         it should not be keyed `mass`

The first is the architectural answer and it costs a contract change. The second is
cheap and needs to be true rather than convenient.

**Not decided here.**

## The two VACUOUS are a step that does not emit

`A5` and `B5` examine zero rows because **`tether` writes no `cite` rows at all.** The
citation discipline -- `you can propose on a candidate, you cannot stand on one`, the one
`kernel`'s A5 caught keyed on the wrong thing -- is not upheld-and-unexercised on the
shipped code. It is **unobservable**. `tether` may or may not be standing on candidates
and nothing in the record can tell.

Same shape as A9: a discipline the reference loop demonstrates and the product does not
record.

## Board

    ruff ok · lint FAIL · kernel ok · stateful ok · shipped FAIL · demo ok · gate ok · tests ok
    6/8 seats clean, 2 found something

---

# The citation discipline is now observable, and A7 renamed

## cite / hold

`tether` wrote no `cite` rows, so A5 and B5 examined nothing and the discipline was not
upheld-and-unexercised but UNOBSERVABLE. The reference emits two row types and that is
the whole distinction:

    bound + settled      cite   (allowed=True)
    bound + unsettled    hold   (status=candidate, ground_said=False)

`tether` now does the same at step 1, where the bet is derived from the bound term. Atoms
are exempt: the ground never owed anything for a primitive.

**Read at the bet, written at step 6.** Writing a PROMOTE-step row from step 1 put a
ROUTE row after a PROMOTE row inside the cycle and **the gate refused the record** --
`step-order: chase: ROUTE after PROMOTE`. But the settled-ness has to be READ at the bet:
a term that settles later in the same cycle was still a candidate when the bet stood on
it, and recording it as cited would be the record flattering the loop by one step.

    586 cite rows, 564 hold rows over the 20-world panel
    A5 PASS in 14/20 worlds, VACUOUS in 6 (nothing settled there)

**The cross-slot shape is unobserved.** A term cited on two slots -- the case the
`(slot, term)` keying was repaired for -- occurred zero times. It is reachable via
REBIND, so this is absence of evidence and not evidence of absence.

## B5 · a live defect the panel reached

    seed 10: 1 no_support park on ['s3'] -> B5 FAIL  s3: support at zero and no probe followed
             probe rows recorded against: ['@probe']

`tether`'s mint sets `no_support` PER SLOT; the probe row is recorded against `@probe`,
so it can never match the park's slot. Two of thirty seeds at 40 steps.

**And the row it would have to match is the one that does nothing.** `bored()` fires and
returns the identical draw, so even a correctly-labelled probe row would be claiming a
perturbation that never happens. That is audit A2, and B5 is the check that walks into
it. **Not fixed here: it is a behaviour gap, not a field.**

**The fast seat does not reach it** -- 25 examples at 6 steps, and this needs ~40. A known
failure outside the hook's reach is worth saying out loud.

## A7 · renamed, and the reader moved with it

The reward channel's `1 - degree` is `hit / len(slots)`: a score over the whole board, not
a gap between a prediction and an outcome at a slot. **R is always a slice, and a quantity
that cannot be sliced is not R.** Keyed `shortfall`, not `mass`.

Per-slot reporting would not have repaired it -- dividing a global score by slot
manufactures a slice rather than finding one, which is the same defect installed
deliberately. The contract keeps returning one scalar.

`gate._routing` decided what must be routed by reading `mass`, and the reward channel IS
routed, so it now reads `mass` or `shortfall`. The check is preserved rather than widened:
both mean the row carried a live reading that owes a routing.

## Where the record stands

    30 steps, 599 rows:   PASS 13   UNIMPL 12   VACUOUS 1   FAIL 0
    exercised on tether's record:  9 -> 13

    ruff ok · lint FAIL · kernel ok · stateful ok · shipped ok · demo ok · gate ok · tests ok
    7/8 seats clean, 1 found something

---

# The probe, and the gate divergence

## The probe fired 441 times and changed nothing

    before   bored=True   by=draw 415   by=discriminate 26
    after    bored=True   by=probe 436

**The missing thing was not a different draw.** The uninformed draw was already the
default on 415 of 441 bored steps, which is why a counter could report 441 perturbations
that moved no action. And a different arbitrary action would have been a draw with extra
steps -- while a discriminating one is forbidden by the module's own stated safety
property: *a probe chosen by the current model can only confirm the current model*.

**What was missing is that boredom must refuse the model the wheel.** `bored()` means no
slot carried live mass -- the model explains everything it can currently see -- and on 26
of those steps `Agent.choose` was still steering by it, because the DISCRIMINATE branch
was tried first. Now boredom short-circuits it.

**The trajectory moved**, which is how you tell this from the previous version:
awake steps 359 -> 364, bored 441 -> 436. Different actions, different states.

## B5 · the probe row names the slot that asked for it

`no_support` is set PER SLOT by the mint; the probe row was recorded against `@probe`, so
it could never match. Starved slots now queue and the probe names them when it takes the
wheel.

    seed 10  ->  B5 PASS   probe rows recorded against ['@probe', 's3']
    seed 29  ->  B5 PASS

## gate._settlement · a repair that never crossed

`kernel`'s A5 was repaired to key on `(slot, term)` -- *the ground settles a term FOR A
SLOT, so a settlement on one licenses nothing on another*. The shipped checker still
keyed on the term alone. **Two checkers of the same record disagreeing about what it
means is worse than either being wrong**, and it is A9's shape again: a repair that landed
in the reference and did not cross to the product.

Keyed on `(slot, term)` now, with its own defect test -- and the witness is the useful
part:

    with the term-only keying reintroduced:
      the NEW fixture fires
      the ORIGINAL fixture still passes -- it never reached this case

The existing test could not have caught it. **`valid()`'s settle row IS its accepted
row**, so the first fixture I wrote moved both sides of the comparison and witnessed
nothing; the case needs a second slot.

## Board

    ruff ok · lint FAIL · kernel ok · stateful ok · shipped ok · demo ok · gate ok · tests ok
    7/8 seats clean, 1 found something

---

# E1 · the ladder has a caller, and the rungs are the deviation they claim

## The rungs

    DS 0.0 (a reskin)                   200/200 left every rule untouched
    DS 0.4 (one new family introduced)    0/300 fall short     was 18%
    DS 0.8 (half the rules change)        0/300 fall short     was 14%

`deviate` sampled the whole family set, so a rung could redraw a slot's family and get
the one it already had. And the fix took two passes: excluding the CURRENT family got
0.8 from 14% to 7%, because the 0.8 edit runs after the 0.4 edit and can land on the same
slot -- `A -> B -> A` is a rung that reports a change and made none. It excludes the
family the level was deviated FROM as well now.

**DS 0.0 still touches nothing but the start state.** That is the ladder's top anchor and
a rung that re-rolls it leaves the curve with nothing to fall away from.

## The caller

`snaps.py` had no `__main__`. Its own docstring calls DS *the only reason transfer is
measurable at all*, and nothing ran it -- and the dead-code rule could not say so, because
`ladder` is an ordinary English word and the package's own prose mentions it. That is C1
and E1 turning out to be the same finding from two directions.

    python snaps.py <seed> <ds>

    DS 0.4 ladder from seed 0
      lv  claimed  false  abst  f.abst  carried  uptake       end  used
       0        1      0     3       0        0    0.00 exhausted    40
       1        0      0     4       0        0    0.00 exhausted    40
       2        0      0     4       0        0    0.00 exhausted    40
       3        0      0     4       0        0    0.00 exhausted    40

**Carried is zero at every level, and that is the first time the number has ever been
read.** It is the only transfer figure on the row -- a term MINTED on an earlier level and
reused on this one -- and everything else describes one level in isolation. A flat zero is
not a dead direction, but it is also not nothing: the ladder now measures, and what it
measures is that nothing transferred at DS 0.4 over four levels.

## speak.py

The probe sentence had diverged from the mechanism twice: it cited `probe_err`, deleted
with the EMA, and rendered *my own error is None*; and it described perturbing, when the
draw was always the default and what changed is that the model no longer gets to choose.

    On s3 nothing is live. Over 11 observations no slot carried mass, so my model
    explains everything I can currently see -- and an action I picked from that model
    could only confirm it. So I am not picking this one: the draw is uninformed, and
    what comes back is an ordinary observation.

    speak.verify: traceable=True   sentences=234   orphans=0

## Board

    ruff ok · lint ok · kernel ok · stateful ok · shipped ok · demo ok · gate ok · tests ok
    8/8 seats clean, 0 found something

**Every red was closed by repairing the subject, never by widening a check.**

Still open, and both cosmetic: `Drive.starving()` is computed and reported and nothing
branches on it, and seven sites still say the contract has eight members when `bind`
enforces ten.

---

# A1 · checked, and it is the property rather than the proxy

A1 was `closure generated, never stored`, filed NOT-EXPRESSIBLE in the static seat and
STRUCTURAL in the record seat -- unchecked in both. **The reason lint gave for not
expressing it was correct and was about the proxy:** *keying on the identifier `closure`
goes blind on a rename, silently.*

**`nothing is stored` was never the property.** It stood in for one, and it is the
stand-in an effect-index breaks while leaving the guarantee intact. What A1 protects is:

    accept() is the library's ONLY writer
    enumerate_closure is the ONLY producer of reach

Both are behaviours, both are checkable, and neither keys on a name.

## The rule

`REACH` in `conform/lint.py`, crossfile:

    clause 1   a subscript-assignment into `.library[...]` -- counted across the package,
               because a second writer would appear in the LOOP reaching past accept(),
               and per-file counting sees one writer in each file and reports nothing.

    clause 2   a BinOp that extends an `.atoms` sequence must sit in a function that
               yields. Extending atom sequences IS producing reach.

The real code satisfies both: one write site (`_install`), one composition site
(`chain + u.atoms`) inside a generator.

## The discrimination, tested on the real code and not on fixtures

    as it stands                       passes
    + a memo of the generator          passes      <- the proxy forbids this
    + a second producer of reach       FIRES
    + a second writer of the library   FIRES

**The middle row is the whole point.** A memo stores what the generator produced: it
composes nothing and writes nothing, so reach still has one producer and the library one
writer. That is the shape the effect-index needs, and it is now permitted by a rule that
predates it rather than by one written to accommodate it.

## Bookkeeping

A1 is out of lint's NOT-EXPRESSIBLE table -- 26 unseen properties became 25. The record
seat keeps its entry, because a record genuinely cannot prove this, but the entry now
names where it IS caught so `this pass cannot see it` stops reading as `nobody checks it`.

    ANCHOR PASS · ISOLATED PASS · NOFAIL PASS · REACH PASS · SINGLETON PASS
    8/8 seats clean
