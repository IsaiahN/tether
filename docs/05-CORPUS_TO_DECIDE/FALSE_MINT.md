# The 42% — read

Three hypotheses, measured in order. The first two were mine and the audit's, and both
are dead. 20 worlds x 4 slots x 30 steps, first mint per slot, graded extensionally over
the whole finite domain by `snaps._same`.

## 0 — a measurement error of my own, first

`mint` fires for a term that PAYS and for a term that CLOSES, and I graded both as
claims. Half of all first-mints (26 of 52) paid without closing. Those leave the slot in
`owed_import`; they are not a claim to be the mechanism, and they are extensionally
partial by construction.

They also cluster in the long-history buckets, because `|φ| + |R|φ| < |R|` gets *easier*
to satisfy as `|R|` accumulates — a term explaining any positive fraction eventually
pays. Grading them produced a curve where more history looked like it caused more error:
46% → 10% → 0% correct. The whole inversion was the conflation.

    PAYS IS NOT CLOSES, and a grader that forgets it manufactures a trend.

## 1 — COUNT: a term fitted to few observations is wrong

Dead. Closing first-mints: mean 5.1 observations when correct, 4.8 when wrong.

## 2 — COVERAGE: a term fitted to few distinct (value, action) conditions is wrong

Dead. 4.5 conditions when correct, 4.2 when wrong. This was the audit's phrasing —
`SUPPORT counts observations, not coverage of the conditions under which a term would
fail` — asserted, never measured. It does not hold.

## 3 — AMBIGUITY: several terms close the same history and the agent takes the first

Dead as a *cause*, though the ambiguity is real. `mint` breaks at `best[0] == 0.0`, so it
never learns a second term also closes. It usually does: mean 10 closers, 16 of 27 mints
had 8 or more.

But selection is not where the error is:

    correct term among the closers      15 mints    14 picked right    93%
    correct term NOT among them         12 mints     0 picked right     0%

A blind pick among the closers would have scored 90%. The agent scored 93%. Selection
contributes nothing, because the closers are mostly extensionally equivalent variants.

## What it actually is

    closing first-mints          minted right   minted wrong
    in closure  (reachable)                11              1
    out of closure (not)                    3             12

Twelve of thirteen wrong mints are on slots whose rule has no explanation in the closure
at all. **The false mint is not a fitting failure. It is abstention failure.** These are
the slots the agent is supposed to decline, and it closes R on every one of them instead.

Families: hidden 4, regime 2, lagged 2, quadratic 2, chain 2, action 1. `hidden` and
`lagged` read state the agent has no accessor for, and are permanently out of reach —
`_same` says so in its own note.

And the three that were minted right while out of closure are not noise. `key` measures
reach over ATOMS at depth 3; the agent enumerates over UNITS — atoms plus settled terms.
Those three were reached by composing on the library. That is the thesis, measured.

## What it teaches step 6 and step 7

`left == 0` means NOTHING OBSERVED CONTRADICTS THIS. The agent reads it as I HAVE FOUND
THE MECHANISM. Between those two is the whole of the alignment failure, and the agent
currently has no instrument that separates them — which is why the answer is not more
history. More history was measured and it does not separate them either.

The instrument it needs already half exists. A close is decisive only if no reachable
action and state would separate the closing term from its rivals, and the rivals are
enumerable — there are ten of them on average, and `choose` already computes exactly
this spread for the discriminate branch.

So:

    a close makes a CANDIDATE, never a settlement          (candidate != settled)
    PROMOTE is what turns one into the other
    and the ground it settles against is SURVIVAL OF A DISCRIMINATING EXPERIMENT,
    not accumulation of passive history

When the discriminating experiment kills every closer, the agent has positive causal
evidence that nothing reachable explains the slot — `I tried and a bound stopped me`,
not `I have never been there`. That is the abstention, and it is the one the twelve
false mints should have produced.

This also answers the standing caution that the six NO-BEHAVIOUR checks need `a second
ground to settle against`. They are unimplementable because promote and import have no
behaviour, and promote has no behaviour because there is no second ground. The second
ground is the experiment.

---

# Prereg — promote by held-out, staged

Written before the build. The falsifier is the number, and the panel is fixed: seeds
0..19, 4 slots, 30 steps, graded by `snaps.grade`.

## Before

    slots            80
    claimed          25      false_mint 9       rate 36%
    abstained        40      false_abstention 1  accuracy 97.5%
    unresolved       15

**The metric is two-sided and cannot be gamed by declining more.** A slot that owes is
graded against `in_closure`, so abstaining on a reachable slot scores `false_abstention`.
Any drop in false-mint rate bought by abstaining indiscriminately shows up immediately as
a collapse in abstention accuracy.

## The diagnosis being tested

`grade` reads a claim as `bound and not owed`. `mint` retires the debt the instant
`left == 0`:

    closes = left == 0.0
    if closes:
        self.candidates[term.name] = self.cycle
        self.owed_import.discard(slot)          # <- the claim, made here

So the agent asserts a mechanism the moment a term closes a SLICE, before `settle`'s
held-out test has ever run. `candidate != settled` is implemented inside Gamma and has no
bearing on what the agent claims. That is A3's sibling and B16 in operation: R is always
a slice, and a slice closing is not R closing.

## Stages, measured separately

A single blob that moves the number teaches nothing about which part moved it.

    STAGE 1   the claim moves from MINT to SETTLE. A close binds and makes a candidate;
              the slot keeps owing until the bound term holds out on a transition it was
              not fitted to.

    STAGE 2   mint stops breaking at the first closer and records the RIVALS -- the other
              terms that close the same history, within the same declared budget. The
              break was destroying the evidence that the close was not decisive.

    STAGE 3   `choose` discriminates among the bound term and its rivals rather than the
              whole closure, so the one held-out transition STAGE 1 requires is spent
              where the candidates disagree.

    STAGE 4   when the candidate and every rival have been refuted, the slot abstains on
              positive causal evidence -- a verdict distinct from `depth_exhausted`,
              which reports only that nothing was found.

## Predictions

STAGE 1 alone should move false-mint rate down and cost abstention accuracy something,
because a correct term also has to survive a transition it may not get in 30 steps.
STAGE 3 is what should pay that cost back.

If the rate does not move, the diagnosis is wrong and the finding is elsewhere.

---

# Results — every design died, and the last one explains the rest

Same panel throughout: seeds 0..19, 4 slots, graded by `snaps.grade`.

## STAGE 1 — the claim moves from MINT to SETTLE

    before   claimed 25   false 9    36.0%
    after    claimed 26   false 10   38.5%

Null. The mechanism, checked directly rather than inferred: the held-out test fired on
all ten wrong terms and **all ten survived it. Zero demotions.** One more incidental
transition is one more observation, and hypotheses 1 and 2 already showed observations do
not separate.

`provisional` stayed at 0 in every seed sampled, so the new path was barely reached at
all — which is the second reason the stage reads null and the first reason to look
somewhere else.

*(The first STAGE 1 run reported 44%, and it was confounded: I had bundled a `route`
change into it that woke 15 previously untouched slots and produced 11 new claims, 7 of
them wrong. Two changes, one measurement. Separated and re-run.)*

## STAGE 2 and 3 — rivals, and the discriminating action — killed before building

The premise is that some action exposes the wrong term. Replaying every recorded
`(before, prev, tick)` under every action, varying only the action:

    exposable at a state it stood in           3/10
      ...by an action it never tried there     2/10

**Seven of ten wrong terms agree with the truth everywhere the agent can reach, under
every action.** No policy over actions catches them. And `choose`'s own docstring already
said why steering by the current model is suspect; here it is not even available.

The wrong terms were fitted on **12.2 of 21 conditions — 58% of the domain.** Not thin.

## Shadow then echo — right mechanism, wrong panel

    WRONG: echoes another slot   1/10
    right: echoes another slot   0/16

Echo fires once in 26 and it fires on a wrong term. As a promotion gate here it would
reject all sixteen correct terms. That is a property of the panel, not of echo: four
slots with mostly independent rules means no second slot casts the same shadow. Echo
needs the ladder's cross-level structure, and this panel has none.

## The contradiction test — nothing to find

If a rule reads the tick or the previous state, the same `(value, action, operand)` must
eventually give different outcomes — a contradiction in the agent's own record, needing
no answer key.

    contradiction already in the record        0/10
    contradiction reachable in the episode     0/10

Zero, and zero even in principle across the whole episode.

## What that adds up to

**The ten wrong terms are consistent with every observation the episode admits.** No
action reaches a state that separates them, no return visit contradicts them, no rival
test distinguishes them, no second slot echoes them. They are wrong only against domain
regions the trajectory never enters — and for slots driven by the tick, the agent has no
control over the trajectory at all.

That is underdetermination, not overcommitment, and **no mechanism the agent could run
would catch it.** Which is why the falsifier came back negative for every design: the
prereg was sound and the diagnosis it was testing was not.

## And the reason more evidence cannot answer it

    steps   claimed  false   rate    abst  f.abst    acc   unres
       30        26     10  38.5%      39       1  97.4%      15
       60        26     10  38.5%      39       1  97.4%      15

Identical in every cell. The loop is stationary:

    MINT verdicts       depth_exhausted 1094      pays 62      no_support 1

Ninety-five percent of mint attempts enumerate the whole space at depth 3, find nothing
that pays, and record the honest verdict — then do it again next step, and every step
after. `sweep` has `stale()` for exactly this (`depth_exhausted` means *at this unit
set*, so an unchanged unit set cannot change the answer). **`mint` has no such guard.**
Nothing changed between the 1094 enumerations, so nothing could.

Sampling three seeds: seed 0 holds at 2 bound / 3 owed for fifty steps while live mass
keeps arriving; seed 7 mints nothing at all in sixty steps with three slots owing, its
library frozen at the atom count.

Of 80 slots: 38 correctly abstained, 16 correctly claimed, 10 wrongly claimed, **15 never
routed to at all.**

## Open, and not mine to decide

`grade` asks extensional equality over the whole finite domain. The episode exposes part
of it. A term correct on everything observable and wrong off-trajectory is graded as a
false claim, and the agent has no evidence by which it could have known.

Whether that is the agent failing or the panel asking a question the episode cannot
answer is a question about what the metric means, and changing a grader to move a number
is the one move that would invalidate every reading above.

---

# The ladder read — carried is not zero, and the bottleneck is opportunity

A single-seed ladder showed `carried = 0` at every level and it was reported here as the
first transfer measurement. **It was an artifact.** `carried` is counted only among
CLAIMED slots and seed 0 claimed nothing after level 0, so the zero was arithmetic over
an empty denominator rather than a fact about transfer.

Twelve seeds, four levels, forty steps, DS 0.4:

    lv  claimed  false  abst  f.abst  opp  uptake  carried  lib  lib ok here
     0       13      4    25       1    0       0        0   34            9
     1       15      5    28       0    3       3        3   74           10
     2       16      6    26       0    6       4        4  112           13
     3       13      4    30       0    4       3        3  163            9

    claimed 57   false 19   opportunity 13   uptake 10   carried 10
    false-mint rate over the ladder: 33%

**Transfer happens, and the reuse machinery is not the problem.** Where a library term
explains a later level's slot the agent takes it 10 times in 13 -- 77% uptake.

## The bottleneck

**Opportunity is 13 across roughly 144 later-level slots: 9%.** Transfer is not failing,
it is rarely available. And the last two columns say why:

    library grows                                   34 -> 74 -> 112 -> 163
    terms that are the mechanism of any slot here    9 -> 10 ->  13 ->   9

**The library quintuples and the count of terms that are actually a mechanism stays flat
at about ten.** By level 3 some 93% of it is terms that closed a slice without being the
mechanism -- the population the false-mint read characterised, accumulating.

## What that unifies

A false mint does not only cost the level it happens on. It is carried, and it dilutes
every later level's opportunity: it is ~90% of what the agent brings forward. So the
33-48% false-mint rate and the scarcity of transfer are one finding, not two.

**And it sharpens the target.** `false_mint_rate` is the symptom; the quantity to move is
`lib ok here / lib` -- what fraction of the library is a mechanism of anything -- with
`opportunity` as the downstream number that would confirm it moved. Both are measured now
and neither is frame-internal: `lib ok here` is graded extensionally by the harness
against the ground's own rules.

---

# Prereg — step 6, PROMOTE by shadow then echo

## Before (12 seeds x 4 levels x 40 steps, DS 0.4)

    lv   lib   lib ok here      ratio
     0    34             9       26%
     1    74            10       14%
     2   112            13       12%
     3   163             9        6%

    claimed 57   false 19   rate 33%
    opportunity 13   uptake 10   carried 10

## The mechanism

`settle` is held-out payment ON THE SLOT THE TERM WAS MINTED FOR, and the false-mint read
showed it does not discriminate: all ten wrong terms fired the held-out test and all ten
survived it. So SETTLED cannot be what licenses a term to cross a scale boundary.

    SETTLE   (step 5)  held out here      -> the debt on THIS slot is retired
    PROMOTE  (step 6)  shadow then echo   -> the term is a PRIMITIVE and crosses upward

    shadow   a residual recorded BEFORE the term existed, provable by ledger seq
    echo     the term closes it, on a slot or level it was not minted for

**Both, or neither.** Echo alone is apophenia -- a structure found and given somewhere to
live. Shadow alone is a local hack promoted as a primitive.

`sweep` already computes exactly this and throws the verdict away: it re-runs a newly
accepted term against every outstanding parked residual and records a retro ACCEPT. What
is missing is that the event licenses nothing.

## What changes

**A term that has not been promoted does not cross a level boundary as settled.**
`retarget` reverts it to candidate -- defeasibly, and it stays in the library, because
nothing is deleted. Chunking is untouched: `units()` still composes over settled terms
within a level, so the ladder slot's falsifier still works.

Earlier I measured echo firing 1 time in 26 and called it unusable. That was a
SINGLE-LEVEL panel of four slots with independent rules -- no second slot casts the same
shadow and there are no parked residuals from anywhere. The ladder is where echo has
something to echo, and it is the panel this is measured on.

## Predictions

    lib at later levels        falls
    lib ok here / lib          rises -- the target
    opportunity                may FALL: fewer carryable terms is fewer chances
    opportunity / carryable    rises, and this is the honest rate
    false-mint rate            falls if a cleaner library means cleaner composition

**If lib ok here / lib does not rise, the mechanism does not do what it is for**, and no
amount of the other numbers moving redeems it.

---

# Step 6 result — the prereg target did not move

    lv    lib          lib ok here        ratio
          before after  before after   before after
     0     34    34      9     9        26%   26%
     1     74    75     10     9        14%   12%
     2    112   116     13     9        12%    8%
     3    163   172      9    11         6%    6%

**`lib ok here / lib` is unchanged.** The prereg said: *if it does not rise, the mechanism
does not do what it is for, and no amount of the other numbers moving redeems it.* It did
not rise.

## The mechanism fires. It gates the wrong thing.

    promote rows        6        of which cross-level   5
    terms reverted     29        at 18 boundaries
    library at end    172        primitives             6

So shadow-then-echo is not inert on the ladder -- it fired six times, five of them across
a level boundary. That is the measurement that overturns the earlier `echo fires 1 in 26`
null, and it overturns it for the reason predicted: **that panel was single-level and had
nothing to echo.**

**The design error is mine and it is precise.** Promotion gates SETTLED-NESS, so it
controls `units()` and therefore composition. But `lib`, `opportunity` and `carried` are
all computed over LIBRARY MEMBERSHIP, which promotion does not touch -- `_library_fit`
can still bind any library term at any level. I gated composition and measured carrying.

Two ways out and neither is free. Pruning the library at a boundary contradicts
`defeasible, never deleted`. Redefining `carryable` as `primitives` inside `grade` would
be moving the grader to make the number move, which invalidates every reading in this
document.

## A side effect that was not predicted

    claimed      57 -> 48        false mints    19 -> 11        rate  33% -> 23%
    abstained   109 -> 118       false abst      1 ->  2

Nine fewer claims, eight fewer of them wrong, one more false abstention. **The agent
declined more and was wrong less**, which is this project's stated goal in one line.

**It is not the preregistered target and it does not count as a pass.** A result that
arrives unpredicted needs its own prereg before it is evidence -- swapping to the number
that moved is the anchor-that-updates failure, and it is the one this document exists to
avoid. Recorded, not claimed.

---

# Prereg 2 — opportunity, and a replication of what moved

## First: the previous target was defective, and that is not a reason step 6 passed

`lib ok here / lib` **cannot rise.** Checked rather than argued: `gamma.library` has two
write sites and **zero removal sites**, so the denominator is monotone non-decreasing by
construction. The numerator counts terms that are the mechanism of some slot on the
CURRENT level, so it is bounded by slots times extensional variants -- flat at about ten
against four slots, which is what the data showed. The ratio falls whatever the loop does.

**That is the SINGLETON defect: a measure whose clean state is structurally unreachable.**
It is a fault in the metric I chose, and it is recorded as that. **Step 6 remains failed
against its original prereg. That record is not edited.**

## Target: opportunity

How often a term already in the library explains a later level's slot. Extensional,
graded by the harness against the ground's rules, and **it can rise** -- a better library
produces more openings without needing the denominator to shrink.

    CONTROL: uptake. Currently 9 of 12. If opportunity rises and uptake holds, transfer
    improved. If uptake falls, something else changed and the rise is not what it looks
    like.

This registers the target for the NEXT mechanism. No build is claimed against it here.

## Secondary, registered now rather than retrofitted

Step 6 produced an unpredicted claim/abstention shift. Before-numbers, seeds 0-11:

                    without step 6      with step 6
    claimed                 57              48
    false mints             19              11
    rate                    33%             23%
    abstained              109             118
    false abstentions        1               2

**The test is a held-out panel: seeds 12-23, both arms.** Step 6 is ablated by neutering
`demote_unpromoted` -- the only site its licence is read at, so the ablation is exact and
promotion still records while licensing nothing.

**Prediction: if the effect is real it replicates in direction on seeds it was never
measured on** -- fewer claims, a lower false-mint rate, abstention accuracy holding above
95%. If it does not replicate, 33% -> 23% was seed selection and the honest reading is
that step 6 changed nothing at all.

---

# Replication result — the secondary did not survive it

Held-out seeds 12-23, never measured before, both arms:

                        without step 6   with step 6
    claimed                         54            53
    false_mint                      14            11
    rate                           26%           21%
    abstained                      103           104
    false_abstention                 0             0
    opportunity                     20            18
    uptake                          11             9
    carried                         11             9

## The claim/abstention shift did not replicate

    seeds 0-11    claimed 57 -> 48   (-9)     abstained 109 -> 118   (+9)
    seeds 12-23   claimed 54 -> 53   (-1)     abstained 103 -> 104   (+1)

**That was seed selection.** The prereg predicted fewer claims and it did not happen on a
panel it had not been measured on. `the agent declined more and was wrong less` was the
sentence I refused to claim as a pass, and refusing it was correct: it does not hold.

## The rate difference is inside the noise

    seeds 0-11    33% -> 23%
    seeds 12-23   26% -> 21%
    pooled        29.7% -> 21.8%     difference 7.9%, SE 6.0%   =  1.3 SE

Same direction on both panels, and **1.3 standard errors is not a result.** With 111 and
101 claims a swing of this size arrives by chance often enough that reporting it as an
improvement would be exactly the invented number this document is a record of avoiding.
Suggestive, unresolved, and it would need several times the panel to settle.

## And transfer went DOWN, in both panels

    opportunity   13 -> 12    and    20 -> 18
    uptake        10 ->  9    and    11 ->  9
    carried       10 ->  9    and    11 ->  9

**Consistent in direction across both panels, and it is the one thing that moved the same
way twice.** Step 6 reverts unpromoted terms at the boundary, so fewer settled terms cross
-- and the openings a later level had came from those terms. It bought nothing measurable
and it cost transfer.

## Reading

**Step 6 failed its own prereg, its unpredicted side effect failed replication, and the
only consistent effect is a cost.** The mechanism does fire -- six and nine promotions,
mostly cross-level -- so shadow-then-echo is real on a ladder. What is not established is
that licensing on it helps anything.

That is not an argument for deleting it. It is an argument that **the licence is currently
attached to the wrong thing**: reverting settled-ness at a boundary removes good terms
along with bad, because settled-ness was never the property that distinguished them. The
next mechanism has to raise `opportunity`, which is what prereg 2 registered, and this run
is its before-number: **20 and 18 on held-out seeds, uptake 11 and 9.**

---

# Narrowing read — the residual does name the candidates, and one edge costs capability

407 mint calls over 8 worlds x 25 steps, each replayed under three arms. Nothing in
`tether.py` changed; this is a read.

    arm  full evaluations   per mint    vs A   lost a term
    A    exhaustive             1945   100.0%            0
    B    witness                 287    14.7%            2
    C    witness + enables       201    10.3%            3

## B is sound for CLOSES and unsound for PAYS

The residual names one observation the current model got WRONG. A term that does not fix
that observation cannot close R, so it is rejected in O(1) instead of O(history).

**Zero closing terms lost in 407 mints. A 6.8x reduction.**

The two it lost are both `pays only`:

    B  s2:  A found 'dec . dec . idn'   (pays only)     B found None
    B  s1:  A found 'inc . take<s0>'    (pays only)     B found None

**PAYS IS NOT CLOSES, and the filter lands exactly on that line.** A closing term must fix
every observation including the witness; a term that merely pays need not fix that
particular one. So the narrowing is a necessary condition for the thing it was derived
for and not for the other thing the same search returns.

## C loses a closing term, and that is the finding

    C  s0:  A found 'take . inc . neg . act . neg . dbl<s2>'  (CLOSES)   C found None

The ENABLES gate -- skip operand-reading terms unless the residual shows dependence on
another slot -- **is not sound, measured.** A term can read an operand and, on the
observed slice, not vary with it; excluding it loses an explanation that closes.

**The distinction that matters: a narrowing derived as a NECESSARY CONDITION from the
residual costs nothing, and a narrowing that reasons about which atoms ought to be needed
costs capability.** B is the first; C is the second. Same intuition, opposite results, and
only the measurement separates them.

## What it does NOT do

**B reduces the cost per candidate, not the number of candidates.** The closure is still
enumerated and every operand binding is still constructed -- B only skips the walk over
history. Per-candidate cost falls from O(history) to O(1), so at history 30 it is roughly
a 30x saving on the dominant term, but **the slot count still drives `_bindings` and the
scaling is unchanged.**

Against the 64x64 figure: 13 hours a step becomes tens of minutes. That is a constant, not
a decomposition. **Stopping the enumeration would need terms INDEXED by their effect so
the residual's shape retrieves them, which is a different structure and is not what this
measured.**

---

# The residual bounds the search — taken, and it needed no scope

Scoping the witness filter to closes was not necessary, because a stronger filter is
sound for both verdicts. `correction_bits` is binary, so `|R|phi|` is `log2(V)` times the
count of observations phi gets wrong, and `base` is that count over R. A term wrong on k
of R is wrong at least k times overall, so

    cost + log2(V) * k  >=  base    ->    it cannot pay, at any history length

**Necessary, therefore lossless -- for pays and for closes.** It subsumes the witness
test, which was only the special case `k == |R|`. And `k` only grows, so the walk stops
the moment the bound is crossed: with term cost already near the bargain's ceiling that
is usually the first miss.

    A  exhaustive          1945 full evaluations per mint
    D  residual-bounded      18 full evaluations per mint     0.9% of A
       observation-touches   14.9% of A                        6.7x less work
       terms lost                 0     over 407 mint calls

**Wall clock over eight worlds: 17.5s -> 5.5s, 3.2x**, and the runs are identical --
same bindings, same debts, same library size, same ledger length. The gap between 6.7x
and 3.2x is Python the filter does not avoid: terms are still constructed and the closure
is still enumerated.

## Both edges pinned

`test_the_residual_bound_loses_nothing` in the shipped seat. Neutering `_cannot_pay` must
change nothing about a run -- not a binding, not a debt, not one row. **And the property
must be able to go red**, so the unsound narrowing is substituted into it: skip
operand-reading terms when R shows no dependence on another slot. If the property cannot
see that, it pins nothing.

    pin passes with the real bound
    pin fires: the residual bound changed the run: a term was lost

## The counterexample, kept

    C  s0:  A found 'take . inc . neg . act . neg . dbl<s2>'  (CLOSES)   C found None

**A term can read an operand and not vary with it on the observed slice.** So `R shows no
dependence on another slot` is a fact about what was seen, not about what the term needs,
and excluding on it drops an explanation that closes.

**The line: a narrowing derived as a NECESSARY CONDITION from the residual costs nothing;
a narrowing that reasons about which atoms ought to be needed costs capability.** The two
are indistinguishable in a design note and differ by a lost term.

## What is still true about scale

The closure is still enumerated and every binding still constructed. This is a constant,
not a decomposition, and 4096 slots is not moot. The thing that would make it moot is an
INDEX -- terms retrieved by their effect rather than filtered after construction -- which
is a different structure and is not measured here.

    ruff ok · lint ok · kernel ok · stateful ok · shipped ok · demo ok · gate ok · tests ok
    8/8 seats clean

---

# Scoping the effect-index — before building

## Two numbers decide it

**COLLAPSE.** An index keyed on effect is only smaller than the closure if terms collapse
into extension classes.

    depth 2:  72 terms ->  29 distinct extensions   2.5x
    depth 3: 584 terms ->  92 distinct extensions   6.3x
    largest class at depth 3: 98 terms, all extensionally identical
                              ('take', 'idn . take', 'inc . take', ...)

**RETRIEVAL.** Over real residuals from live runs, 11 residuals carrying 5.5 distinct
constraints each:

    unary terms consistent with R:  18.8  of 399 in the closure   = 4.7%

**So a lookup returns about nineteen candidates where the mint currently walks 1945.**
That is a different quantity from the residual bound, which still touched all 1945 and
only made each touch cheaper. This is the decomposition; that was the constant.

## Three objects, and only one is a store

    the EXTENSION of a term        derived from the term      a view, no registry
    extension -> terms             derived from units()       a view, no registry
    (value, action, out) -> classes  derived from the above   an INVERTED INDEX, stored

The first two are functions of things Gamma already owns. Only the third is a structure
that exists to be looked up in -- and it is what makes retrieval O(constraints) instead
of O(closure), so it is the one worth having and the one that carries the risk.

**It is a memo with exactly one writer if Gamma owns it and it is invalidated whenever
`units()` changes** -- which is on settle, the only thing that adds a unit. Then it cannot
drift from the generator, because it is rebuilt from the generator.

## The A1 tension, named rather than dodged

A1 is *closure generated, never stored*, and its static rule is *a name holding closure
must be a generator or callable, never a `set` field*. **An effect-index materialises the
closure.** That is the tension and it does not go away by calling the index a cache.

What makes it defensible is the reason A1 exists: storing the closure conflates the
library with the reach, so `accept()` stops being the library's only writer and `mint()`
starts requiring membership in a stored set. An index that memoises the GENERATOR, with
`enumerate_closure` still the only thing that produces terms, does not do that.

**A1 is currently STRUCTURAL and unimplemented, so nothing would catch it either way.**
Building the index is what would make A1 checkable and load-bearing for the first time,
and the check has to distinguish *a memo of the generator, invalidated with the
generator's inputs* from *a stored closure the loop treats as the library*. **That check
should exist before the index does.**

## Where the slot count actually goes

The 13-hour figure came from `_bindings` trying every slot as an operand for every
candidate. An index keyed on operand VALUE rather than operand SLOT inverts it: for a
retrieved term and a residual observation, solve for the operand value that would satisfy
the constraint, then ask which slots held that value -- a lookup over V, not a scan over
slots.

**That is what removes the slot factor, and it is not the indexing itself -- it is
indexing the value instead of the binding.** Worth separating, because the second is
cheap and the first is the part that argues with A1.

## What I would build first, and it is not the index

**The A1 check.** It is the thing that decides whether the index is a memo or a second
registry, it does not exist, and building it after the index means grading the index with
a rule written to fit it.
