# Repairs — the eleven findings, fixed to the letter

Plan only. Nothing built.

The result that decides the order: **most of these fixes delete code and delete magic
numbers.** Every deviation was a shortcut that added something the formula did not ask
for. Going back to the letter is a subtraction, not an addition — which also means the
repairs are cheap and low-risk, and should come before the linter rather than after.

---

## The one that dissolves three magic numbers

`probe.EPS = 0.02` and `instruments.Clocks.eps = 0.05` are two different thresholds for
the same idea, which is how I knew neither was derived. Both exist to answer *"is the
residual small enough to count as nothing?"*

**The formula never asks that question.** SUPPORT is:

> `SUPPORT   |R⁺_s| > 0 for some slot s`

A **boolean over slots**, not a magnitude over an average. There is no epsilon in the
specification because none is needed: either some slot has live mass or none does.

So implementing SUPPORT to the letter:

| goes away | why |
|---|---|
| `EPS = 0.02` | the guard is `any(mass > 0)`, not `mean < eps` |
| `Clocks.eps = 0.05` | "modelled" is `no slot owes`, not an averaged error |
| `ALPHA = 0.1` | the EMA existed only to smooth the average that shouldn't exist |
| `Drive.err` | the aggregate itself — finding A7 |

**Four deletions, one boolean.** `WARM = 12` probably follows: it guards against a fresh
model calling itself bored, but with `any(mass > 0)` a fresh model has live mass by
construction. `REJECTION_HALFLIFE` stays — the formula requires demotion to be clocked
and defeasible, so a halflife is specified; only its *value* needs a provenance line.

---

## The full table

| # | finding | letter-faithful fix | formula | net |
|---|---|---|---|---|
| **A7 / #2** | `Drive.err` aggregates across slots | SUPPORT becomes `any(r.mass > 0 for r in res.values())`. Probe fires when **no** slot owes. `steps_to_model` becomes per-slot, and any scalar summary is `max` — the last slot to settle — never a mean | *"never as a single global number"* · *"a global R near zero with one live slot is a legal state and not an inert one"* | **−40** |
| **#4** | `focal` chosen alphabetically | `focal = max(slots, key=live_mass)`. The quantity is already defined and already computed | `R⁺_s`, the live mass | **−1** |
| **#3** | WANT hardcoded to `ALL(BECOME(slot,0))` | `env.objective()` already returns the name and it is **discarded on the next line**. Have the env return a grammar term instead of a string, and compose the WANT from it | Step 2: *"the sorter must not be the composer"* | **≈0** |
| **#5** | `from world import M` | the env declares its own code: `env.code()` returns the correction cost. The code is a property of the domain, not of the loop | Step 3: *"DECLARE THE CODE"* | **≈0** |
| **#5** | `from world import ACTIONS` | add `actions()` to the eight-member contract, making it nine. Growth in the returned set is an **IMPORT event with a stamp**, which is what it already is | Step 7: *"Gated on: where it came from"* | **+5** |
| **#8** | identity default is an unstamped prior | bind every slot to `idn` **explicitly at init**, stamped `prior`. It already behaves as a prior; it just is not recorded as one | Step 4: *"stamped with where it came from and when"* | **+3** |
| **#9** | `PAY` carries a step count | pass the bits the mint already computed: `price(term_bits, n_observations)` | Step 3: the bargain's halves are lengths | **≈0** |
| **#10** | five unanchored constants | three dissolve above. `REJECTION_HALFLIFE` gains a provenance line. `Config.budget` gains one | DECLARING THE MODE | **−3** |
| **#6** | `snaps` imports `_atoms` | the generator takes an atom set as an argument instead of reaching into `world` | B10 | **≈0** |

**Net: the codebase gets smaller.**

---

## The two that are builds, not repairs

### #1 — the action policy

`Γ` is the controller *"which produces the prediction and therefore the next action."*
Right now every action is `drive.choose`, a deterministic sweep, and the DIRECTED label
is attached to it.

Two honest options, and they are not the same size:

**(a) Delete the label — free, today.** A bin without its discriminator is a label, not a
diagnosis. If nothing discriminates DIRECTED from PROBE, do not emit DIRECTED. The phase
report becomes `probe: 1.0`, which is true, and the histogram starts reading correctly
the moment a real policy exists. This is the doctrine's own remedy and it costs nothing.

**(b) Build the directed path.** The formula gives its shape without giving an
algorithm: the probe is *"uninformed by construction"* and *"a probe that is read is an
experiment."* The complement of an uninformed draw is an action chosen because the bound
terms predict **different** outcomes for it — that is what makes the result readable.
Selecting the maximally discriminating action is derivable from Γ, domain-general, and
encodes no answer.

**Do (a) now regardless.** It is the difference between an instrument that is silent and
one that lies, and (b) does not depend on it.

### #11 — the bracket channel

`R_T = gap(x, (T_E ∘ T_A)(x))`, and `env.transform()` returns `None` in both worlds, so
one of R's three channels has never run. `snaps` can supply a real coarse view — how many
slots sit at the objective's target is an honest `T_A`, and the round trip back is `T_E`.
Then the channel carries, and the Galois property (`R_T ≥ 0` by construction) becomes
checkable rather than asserted.

Not urgent, but it is the only way step 6 stops being inert — which is the same condition
the four kernel drafts were in, and it went unnoticed there for the same reason.

---

## Order

1. **The four subtractions** — SUPPORT as a boolean, focal by live mass, the three
   constants, the WANT. Small, letter-faithful, and they remove the two worst instruments'
   ability to lie.
2. **Delete the DIRECTED label.** One line. Stops a false number being published.
3. **The contract: `actions()` and `code()`.** This is the one that matters for ARC,
   because those are the two facts ARC varies per level.
4. **Stamps and PAY.** Small.
5. *Then* the linter — against a codebase that already conforms, so a failing check means
   a new defect rather than a known one.
6. Later: the directed path, and the bracket channel.

Doing the repairs first also gives the linter something the four kernels cannot: **a
known-good corpus.** A check that fires on conforming code is broken, and there is no way
to notice that if everything available to test against is already broken.
