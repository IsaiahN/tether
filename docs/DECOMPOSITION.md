# The interface as a decomposition — a scoping read

One board, described three ways, measured rather than argued. No task, no puzzle: the
shape of a problem class only.

## The contract does not care. The loop does, in two places.

    decomposition  slots  binds  operand pairs   20 steps
    cells             36    yes           1260       4.0s
    objects            3    yes              6       0.2s
    relations          3    yes              6       0.0s

**All three bind unmodified.** A slot is a name holding an integer and the ten members are
filled the same way whatever the name means, so the interface really is a separate layer
and can be chosen and revised.

Two things the loop assumes anyway, and neither is stated anywhere:

**1 · The slot set is fixed for a level.** `self.slots = env.slots()` is read at
construction and at retarget, and nowhere else. A second object appearing on step 3 is not
an error -- it is **invisible**:

    slots at bind: ['o0.x']        env after six steps: ['o0.x', 'o1.x']
    the agent's slot set is still ['o0.x']
    rows mentioning o1: 0

No bet, no residual, no row. **Cells never do this and objects always will**, so an
objects interface needs the slot set to be reopenable, which today only a level boundary
does.

**2 · One alphabet covers every slot.** `correction_bits` charges `log2(alphabet)` per
miss for all of them:

    a position on a 30-wide board    true 4.91 bits    charged 4.91
    a colour                         true 3.32 bits    charged 4.91
    a boolean relation               true 1.00 bits    charged 4.91

A boolean relation is charged 4.9x its own code. `base` is a count of misses times that
unit, so a narrow slot's residual is inflated and **the bargain becomes far easier to
satisfy on exactly the slots that carry least information.** A relations interface would
mint aggressively and wrongly, and the false-mint read is what that would look like.

## What each decomposition makes inexpressible

Two worlds over the same board. MOVER: the block shifts with the action -- an
object-level rule. FLECK: a cell no object covers changes -- a sub-object rule.

    world  view      slots  live-mass steps   reading
    mover  cells        25               15   LOUD -- live residual, and it owes
    mover  objects       3               14   LOUD -- live residual, and it owes
    fleck  cells        25                2   explained it
    fleck  objects       3                0   SILENT -- reads zero on a moving world

**A loss is LOUD when the residual stays live and the agent abstains** -- it can see
something it cannot explain, which is the honest state and the one abstention exists for.

**A loss is SILENT when the residual reads ZERO**, because then the agent believes it has
explained a world that is still moving underneath it. That is the objects view of a
sub-object rule, and it ran twenty steps without a single live reading.

**This is arm C at the level of perception.** A narrowing derived as a necessary condition
costs nothing; a narrowing that reasons about what is usually relevant costs capability --
and here the excluded thing does not even reach the residual, so nothing downstream can
report it.

## The architecture already names this, and the predicate is scoped wrong

`CHANNEL_CLOSED` is *the instrument never reached it* -- the third cause of a low reading,
the permanent condition, and its stated remedy is **step 7 INWARD**. So the decomposition
question is not outside the frame: it is the one step of the loop that is not built.

And the trigger is already counted. `Drive` keeps `n` and `misses`, so the live fraction
is there: 15/20, 14/20, 2/20, **0/20**.

**But `bored()` reads one step, not the run.** It was true in all four rows above,
including the two with live residual on fourteen of twenty steps, because it is
`not self.live` over the LAST step. A momentary quiet and an instrument that has never
once registered anything are the same value.

**A decomposition failure is a PERSISTENT zero, and the predicate that would catch it is
a fraction over the run rather than a boolean over the step.** That is a small change to
something already measured, and it is the first thing to build here -- before any
interface work, because it is what would tell the agent its interface is wrong.

## Consequence for the effect-index

The closure is downstream of the interface. The same board is 1260 operand pairs as cells
and 6 as objects -- **and that is a change in the exponent, where the residual bound was a
change in the constant.**

But the choice cannot be made on cost. Objects are cheaper AND blind to a whole class of
rule, and the blindness is the silent kind. So the interface is not a decision to take on
the numbers above; it is a decision the agent has to be able to make, revise, and be
WRONG about detectably.

**Which puts persistent-zero-support before the index, and the index after an interface
that can change.** If the interface can change, the index is invalidated whenever it does
-- one more invalidation trigger for the memo, alongside `settle`.

---

# Built: persistent zero support

`bored()` reads the last step. The persistent form is a PREDICATE, not a fraction under a
threshold -- which matters, because REPAIRS 1 deleted EPS and WARM for being thresholds
standing in for predicates, and reintroducing one here would undo that.

    never_live(n_actions)   n > 0  AND  misses == 0  AND  every advertised action drawn

**The action clause is what makes it positive rather than absential.** `I drew every
action on offer and nothing I can see has ever moved` is a bound reporting back.
`nothing has moved yet` is true on step one of every run there has ever been.

It fires on the silent case and on nothing else:

    world  view      never_live   rows
    mover  cells         False       0
    mover  objects       False       0
    fleck  cells         False       0
    fleck  objects       True        1     tried=['A', 'B', 'C']

## What it does NOT claim

**It cannot tell a static world from an instrument that does not reach one.** Those are
the same reading from inside, and the row says so rather than picking the flattering half.
The remedy for the second is step 7 INWARD -- a slot set that reaches what moves -- and
the row records `built: False`, because that step does not exist.

The utterance carries it, which is the point of having one:

    I have drawn every action I was offered (A, B, C) over 3 observations, and nothing in
    blk.colour, blk.x, blk.y has ever moved. Either this world is still, or what moves is
    not something I am built to see -- from here those are the same reading. The second is
    answered by a different set of slots, and I do not have a way to change mine.

**That is the hardest sentence in the vocabulary and the frame could not form it before.**
Not `I cannot explain this`, which abstention already covered, but `there may be nothing
here that I can see`.

    8/8 seats clean

---

# Scoping step 7 INWARD

## The doctrine forbids the thing I was going to worry about

> INWARD  Is our representation adequate to hold it? Extend the instrument. **An
> instrument is improved from a worse one already returning something, never built from a
> description.** So the question is not whether a sensor could exist, but whether
> anything, at any resolution, already returns something that fails to resolve.

**So there is no menu of decompositions to hand the agent.** A representation swap built
from a description is exactly what that sentence rules out, and it is what I would have
built. INWARD is a REFINEMENT of something already reading, not a choice between
alternatives.

Which fixes the direction: **the agent starts coarse and sharpens.** And the coarse view
is the one that fails silently -- so `never_live` is not merely a diagnostic, it is the
trigger for the remedy. The loop closes.

## The measurement already has a name and a formula

    R_T  =  gap( x , (T_E . T_A)(x) )        x concrete

Send it up, bring it back, compare against what was sent. T_A and T_E form a Galois
connection, so `x <= T_E(T_A(x))` always: the round trip can only lose precision.
**R_T is non-negative by construction, and it is not an error to eliminate -- it is the
measurement of what the coarser level cannot hold.**

**That is exactly the instrument that would have made the silent loss loud.** The objects
view of a sub-object rule read zero residual for twenty steps; its round-trip gap on the
fleck cell would have been positive on every one of them.

## The socket existed and was not being read

`transform()` is the tenth contract member and **nothing ever called it.** Its only
occurrence in the package was inside a STRING asserting that it returns None -- so a world
that did define a coarse view would have had the channel reported closed anyway. A cause
stated without being observed, in the one row that exists to report this exact condition.

Now read:

    transform() -> None              cause=channel_closed  coarse_view=False
        env.transform() returned None; no coarse view defined
    transform() -> a coarse view     cause=genuine         coarse_view=True
        a coarse view IS defined and the bracket is not built:
        R_T = gap(x, T_E(T_A(x))) has no site

The second row is the honest NO-BEHAVIOUR: the channel is not closed, the machinery is
absent, and those are different facts.

## The crux, and it is a world-building problem rather than a loop problem

To build or test INWARD there must be a world that offers more than one resolution. **And
a world offering exactly two resolutions, one of which is right, IS the answer encoded --
in the harness rather than in the loop, which is worse because nothing checks the
harness.**

**The precedent that resolves it is `actions()`.** The env advertises A, B and C without
saying which matters; the agent draws and finds out. A world can advertise resolutions the
same way: several, most of them useless, none labelled. Then choosing is the agent's work
and the harness has encoded nothing -- and `snaps` is already a generator that can produce
them without anyone choosing.

**What must NOT happen: the generator producing a coarse view that is always the right
one.** That is the DS-rung defect one level up -- a ladder whose rungs are not the
deviation they claim -- and it would be measured the same way: how often is the offered
resolution the one that resolves? If that number is high, the harness is answering.

## Order

    1  a world that advertises resolutions the way it advertises actions, with the
       measured guarantee that most of them do not resolve
    2  the bracket channel: R_T over T_A / T_E, which is a real reading rather than 0.0
    3  INWARD itself: never_live or an unresolvable live residual asks for a sharper
       instrument, and the bracket says whether the new one holds more

Nothing in 2 or 3 can be graded before 1, and 1 is the piece that can encode the answer.

---

# Item 1 built — a world that advertises resolutions

`snaps.transform()` now returns a set of coarse views, offered the way `actions()` offers
A, B and C: several, unlabelled, and which of them resolves anything is not stated.

    full · parity · half · merge:<a>+<b> · drop:<slot>          10 per world at 4 slots

## The guarantee is structural, not a rate

`_views(names)` is handed the SLOT NAMES and nothing else. It never sees `spec.rules`, so
**the offered set cannot have been selected for resolving anything.** A rate can drift; a
constructor that was never shown the rules cannot encode them at any rate, and the test
asserts the signature rather than the number.

## What the offered set actually contains

A view is LOSSY when the coarse dynamics stop being a function of the coarse state -- two
readings with the same coarse image and different coarse successors. The agent can see
this in its own record with no key: the same (state, action) giving two outcomes.

    40 worlds, 400 views offered

    lose the dynamics   183  (46%)        hold it   217  (54%)
    parity 36/4    half 26/14    merge 48/72    drop 60/100    full 13/27

## The pin was wrong first, and the substitution found it

`lossy > 0` looked like the right edge and is not. **`full` is itself lossy in 13 of 40
worlds** -- wherever a rule reads the tick or the previous state, and no resolution over
the slots recovers that. So counting lossy views is satisfied by the WORLD'S OWN
unreachability rather than by a coarse view losing something a finer one holds.

Found by substituting a view set of only `full` and watching the assertion pass anyway.
The property INWARD needs is narrower:

    SHARPENABLE   a coarse view loses what the full view holds  -> sharpening can succeed
    CHOOSABLE     not every coarse view is lossy                -> there is a choice

Both fire when removed:

    only `full` offered           fires: no world has a coarse view that loses what the
                                         full view holds
    every coarse view lossy       fires: every coarse view loses the dynamics in every
                                         world: the offered set is not a set

## And a third outcome the generator produces on its own

`full` lossy in 13 of 40 means **INWARD correctly fails on roughly a third of worlds** --
sharpened as far as the slot set goes, and it still does not resolve. That is genuine
absence rather than depth, which the doctrine says look identical from inside, and it is
the state the agent must be able to reach and report rather than an error.

    8/8 seats clean

---

# Item 2 built — R_T is a reading

    R_T = gap( x , (T_E . T_A)(x) )

**T_E is not a canonical concretisation, and inventing one would have been choosing a
representative on the agent's behalf.** The Galois form does not need it: `T_E(T_A(x))` is
the SET of readings sharing x's coarse image, `x <= T_E(T_A(x))` holds by construction,
and the gap is the size of that set.

    R_T = log2 | { y : T_A(y) == T_A(x) } |     in bits, the unit everything else is in

Checked against hand-computed values on a three-slot reading at M=7, rather than checked
for producing a number:

    view            R_T bits   expected
    full               0.000   0                        nothing lost
    parity             5.585   5.585                    |{v: v%2==p}| per slot
    half               2.000   2.000                    |{v: v//2==h}| per slot
    merge:s0+s1        2.807   2.807 = log2(7)          a sum fixes M pairs
    drop:s0            2.807   2.807 = log2(7)          one slot free

Every one exact. Non-negative throughout, and zero only at `full`.

## Unmeasured is not small

The pre-image is counted by sweeping the domain, capped by the same declared budget the
closure search uses -- this is a search over readings rather than over terms, and the
frame already has an idiom for a capped search that says so. Past the cap the row reports
`measured: False` and `cause: channel_closed`, because **a sweep that stopped is not a
small R_T and the row must not report the first as the second.** At 7 slots and M=7 the
domain is 823,543 and the honest answer is that it was not measured.

## The current view is `full`, measured rather than assumed

The agent holds a view and it is the finest the env offers, so R_T is zero -- and it is
zero because the sweep returned 1, not because the code assumed it. **Starting it on a
coarse view would be picking the agent's perception for it**, which is what INWARD exists
to let the agent do instead.

That is also why item 2 is thin on its own: with `full` in use the bracket reports zero
every step. It becomes informative the moment something can move the view, which is item
3.

    8/8 seats clean, 26s

---

# Item 3 — the falsifier pinned, and two blockers found by pinning it

## The four outcomes, and why they must be distinguishable

A green run must not be able to mean two things:

    1  NOT TRIGGERED     the current view resolves; INWARD had no reason to fire
    2  SHARPENED, HELD   a finer view holds what the current one lost -- the success case
    3  SHARPENED, STILL  it moved and the finest still does not resolve
    4  NOTHING FINER     it fired and there was nowhere to go

**`INWARD did not fire` and `INWARD fired and correctly found nothing` are states 1 and
3/4, and both should be reachable in one run** -- which the generator already supplies,
since `full` is lossy in about a third of worlds.

Pinning that turned up two things that have to be settled first.

## Blocker 1 · the starting view decides which outcomes exist

    start at full     R_T  0.00   views strictly finer: 0
    start at parity   R_T  5.58   views strictly finer: 7

**At `full` there is nowhere to sharpen to, so INWARD can only ever reach states 1 and 4.
Its success case is unreachable by construction.** The agent starts at `full` today
because I put it there, and I said so at the time; moving it to the coarsest offered view
would make states 2 and 3 reachable and is equally a choice.

There is a derived rule rather than a preference -- *start where R_T is maximal and
sharpen only on evidence* -- and it is defensible as the doctrine's `improved from a worse
one already returning something`. **But it deliberately handicaps the agent, and every
other number would move: false mints, opportunity, carried. That cost has to be measured,
not assumed away.**

## Blocker 2 · a coarse view changes the value range and `alphabet()` is one number

    full     values 0..6   true range 7   charged log2(7) = 2.81 bits per miss
    parity   values 0,1    true range 2   charged log2(7) = 2.81 bits per miss
    half     values 0..3   true range 4   charged log2(7) = 2.81 bits per miss

A parity slot carries one bit and is charged 2.81. **This is the audit's one-alphabet
finding, arriving where it actually bites:** `base` is a miss-count times that unit, so a
coarsened slot's residual is inflated by the same factor its information was reduced --
and the bargain gets loosest exactly where the view is coarsest. **An agent that sharpened
would see the bargain tighten for reasons that have nothing to do with the world.**

The contract has one `alphabet()`. A view that changes the value range needs its own, and
that is a contract question rather than a loop question.

## And a direction question I would rather raise than build past

INWARD sharpens: coarse to fine, because the representation was inadequate to HOLD the
residual. That is the right mechanism for a view that lost information.

**The shape a grid needs may be the opposite.** The finest view holds everything -- no
information is lost by looking at cells -- and the difficulty is that the rule is not
EXPRESSIBLE over cells at reachable depth. Nothing is missing from the representation;
the closure does not reach the term. Coarsening to objects would not recover lost
information, it would change what a term has to say.

**Those are two different mechanisms and the doctrine names one of them.** `R_T` measures
what a coarser level cannot hold, which is the first; it says nothing about what a coarser
level makes expressible. Whether the second is INWARD, chunking at a different grain, or
something with no entry in the formula is not something I should decide by building it.

---

# Blocker 2 closed — each slot is charged its own alphabet

The contract's own words already allowed it: *the loop declares the code's FORM -- uniform
over the alphabet -- and THE DOMAIN SUPPLIES ITS SIZE.* A domain whose slots differ
supplies a size per slot. `alphabet()` now returns one number or one per slot, and the
loop normalises either into a per-slot map.

Eleven use sites, and every one had its slot already in scope except the domain sweep,
which becomes a product.

## Two checks, because a change like this can be wrong in two directions

**It must be a no-op where the domain declares one size:**

    uniform worlds, 8 seeds x 25 steps -- identical: True

Bindings, debts, library size and ledger length, compared against the previous
implementation loaded side by side.

**And it must actually charge differently where the slots differ:**

    slot       charged now   charged before
    colour            3.32             4.91
    flag              1.00             4.91
    pos               4.91             4.91

    masses written: [0.0, 1.0, 3.32, 4.91]

Three distinct units in one world, one per range. A miss on a boolean costs one bit.

## Why it was blocking both directions

`base` is a miss-count times the unit, so a slot's residual was inflated by exactly the
factor its information was reduced -- **the bargain came out loosest where the least was
at stake.** An agent that sharpened would have watched the bargain tighten for reasons
that were not about the world, and an agent that coarsened would have watched it loosen.
**Neither movement could have been measured through that.**

It is also the audit's one-alphabet finding closed, which was filed as cosmetic and was
not.

    8/8 seats clean

---

# The direction question — measured, and the null is VACUOUS provably

**Does a coarser view ever make a rule EXPRESSIBLE that the full view cannot state?**
`R_T` says what a view cannot HOLD; this is the other quantity, and they are not the same.

    5 worlds analysed, 9 skipped (a slot reads the tick or the previous state)

    view lossy                              24
    coarse slot expressible                 11
    coarse slot not                         11
    WIN: coarse says what full could not     0

**Zero. And it is vacuous, for a reason that can be stated rather than suspected.**

## M is prime, so Z_M has no non-trivial quotient

    M = 7, prime.  divisors: [1, 7]

    is the coarse image of a rule a function of the coarse image of its input?
                             parity    half
    v + 1        (affine)     False   False
    2v + 1       (affine)     False   False
    v*v + 3   (quadratic)     False   False
    v          (identity)      True    True

**Only identity survives.** Mod 7 then mod 2 is not a homomorphism because 2 does not
divide 7, so **every non-trivial coarsening of this value space breaks the arithmetic the
atoms are made of.** That is why 24 of the offered views came back lossy: not because
coarsening is a bad idea, but because there is no coarsening of Z_7 that preserves
anything.

My candidate case was `quadratic`: `v*v` is outside a closure of affine atoms, and
`v*v == v mod 2`, so under parity it should have become affine. **The arithmetic does not
work** -- `(v*v + k) mod 7 mod 2` is not a function of `v mod 2`, and the reduction I had
in mind needs 2 to divide the modulus.

## What that means

**The null is about snaps and says nothing about grids.** The two readings the caveat
named are distinguishable here, and this is the second:

    the mechanism has no case        <- NOT what was measured
    this world cannot discriminate   <- what was measured, and provably so

`M = 7` is anchored as *prime, and small enough that the harness can sweep the whole
domain exhaustively* -- chosen for exhaustive grading, and it makes the coarsening
question structurally unanswerable in the same breath. **A constant chosen for one reason
foreclosing a question asked much later**, which is the same shape as the one-alphabet
finding: a fact about a constant whose cost appeared only when something needed to move
across it.

## What would answer it

A value space with non-trivial quotients -- a composite M -- or a world whose structure is
not per-slot arithmetic at all. **A grid is the second kind:** cells are not a quotient of
anything, and an object is a sub-structure over many slots rather than a coarser reading
of one.

**Which is itself the answer to the direction question, arrived at from the other side.**
The thing a grid needs is not a coarser reading of each slot -- that is what these views
are and it is why they lose. It is a REGROUPING of which slots there are, and no view of
the form `T_A: reading -> reading` expresses that.

**So the second mechanism is not a coarser alphabet. It is a different slot set**, and
nothing measured here bears on it either way.
