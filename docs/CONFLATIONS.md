# The conflations — a linter specification

Every entry is a **pair the formula gives two names, which code tends to collapse into
one.** That is the whole failure mode. Not sloppiness: the distinctions are fine enough
to slip past someone actively holding them in mind, which is evidenced below by the fact
that a third of them have already happened, twice by me while looking for them.

Columns: **cited** — where the formula says it. **observed** — has it actually bitten.
**check** — `static` (source), `ledger` (the record), `neither` (needs a human or an
experiment).

No scores. Every check is a yes/no invariant.

---

## A. Observed — these have already happened in this repo

| | the pair | collapsing it produces | cited | check |
|---|---|---|---|---|
| **A1** | **Γ** vs **closure(Γ)** — the library vs the reach | store the closure → `accept()` is its only writer and `mint()` requires membership → **the loop cannot fire once, at any input**. Search the closure where the library was meant → routes REBINDING forever, **never mints** | SYMBOLS: *"closure(Γ) — everything expressible by combining the primitives, at any depth"* | `static`: a name holding closure must be a generator/callable, never a `set` field. `ledger`: a REBIND must cite a term with an ACCEPT row |
| **A2** | **the bargain** vs **a threshold** | `leftover` as a constant fraction of R → `\|φ\|+\|R\|φ\| < \|R\|` reduces to `cost < kR`. Cost from the identifier's spelling → renaming a term flips the verdict | Step 3: *"a bargain, not a threshold"* · *"DECLARE THE CODE"* | `static`: leftover must be computed from history, not from R. `ledger`: every mint row carries base, cost and leftover, and `cost+left < base` must hold |
| **A3** | **pays** vs **closes** | a term that pays but leaves residual clears the slot's debt → step 7 never fires and the slot silently stops owing | Step 3: *"PAYS IS NOT CLOSES… step 7 fires on failure to CLOSE R, never on failure to PAY"* | `ledger`: a mint row with `left > 0` must leave the slot in `owed` |
| **A4** | **the three causes of a low reading** — genuine / channel closed / instrument never reached | all three branches write the same state → the diagnosis is computed and discarded | Step 1: *"a low reading has three causes and only two of them are about R stopping"* | `ledger`: a zero-mass PERCEIVE row must name which of the three |
| **A5** | **candidate** vs **settled** | `settle()`'s verdict is printed/returned and the term sits in the library either way → nothing prevents citation | Step 5: *"it may be held and it may not be cited"* | `ledger`: a term cited in a DERIVE must have a prior SETTLE row *(gate check 6 already)* |
| **A6** | **a bin** vs **a bin with its discriminator** | a label is attached to behaviour that does not differ → the instrument reports a distinction the mechanism does not make | Step 2: *"A bin without its discriminator is a label, not a diagnosis"* | `ledger`: **a label must partition its call sites.** Two labels reaching an identical set of producing sites = one is decoration |
| **A7** | **R per slot** vs **R aggregated** | one scalar fed from inside a per-slot loop → a live signal is diluted by `1/n` and both the probe trigger and steps-to-model read the average | SYMBOLS + Step 1, twice: *"never as a single global number"* · *"averaging across slots is how a live signal disappears"* | `static`: no shared scalar may be mutated inside a `for slot in …` loop. `ledger`: any recorded quantity names the slot it came from |
| **A8** | **origin** vs **time** in a stamp | stamping only *when* → a derived term and an adopted one become indistinguishable, which is the one thing the stamp exists for | Step 4: *"stamped with where it came from and when"* | `static`: every `accept()` call site passes both. `ledger`: every ACCEPT row carries `origin` ∈ {prior, minted, imported} |
| **A9** | **the reference** vs **the thing it checks** | a checker sharing mutable state with its subject → the answer key drifts as the subject learns, silently, in the flattering direction | Step 2 generalised: *"the sorter must not be the composer"* · Step 5: *"a build whose only evidence is its own test is a candidate"* | `static`: no module-level mutable singleton; a reference is constructed per call or is frozen |

---

## B. Latent — in the formula, not yet violated here

| | the pair | collapsing it produces | cited | check |
|---|---|---|---|---|
| **B1** | **unreached** vs **unreachable** | a budget exhaustion reported as an absence proof | Step 3: *"REACHABILITY HAS NO NEGATIVE"* | `ledger`: gate checks 8 + 9 already |
| **B2** | **the gate** vs **the ground** | a passing test reported as a settlement | Step 5: *"A gate passing is not the ground"* | `static`: the settling callable must not be constructed by the frame it settles |
| **B3** | **the bet on b** vs **the bet on o′** | predicting from what was just seen → no model that can be wrong | Step 1: *"a system that predicts from what it just saw has no model to be wrong"* | `static`: the predict path may not read the post-action observation |
| **B4** | **guards as a product** vs **as a checklist** | two of three passing lets the search proceed | Step 3: *"a product, not a checklist. Any factor at zero forces inertness"* | `ledger`: a mint row with any guard false must be a park |
| **B5** | **support-at-zero as instruction** vs **as stop** | the loop halts where it should perturb | Step 3: *"SUPPORT AT ZERO IS AN INSTRUCTION, NOT A STOP"* | `ledger`: a zero-support park must be followed by a probe row |
| **B6** | **outstanding residual** vs **the surprise integral** | explaining a surprise reduces the record of having been surprised → the agent can look calm by forgetting | Notes: *"a drive may read it and may never reduce it"* | `static`: the integral is append-only — no assignment except `+=`. `ledger`: it is non-decreasing across rows |
| **B7** | **T_A/T_E** (between scales) vs **F** (one scale, needs a pose) | one transform doing two jobs; F run without a pose | Step 6: *"AND THIS IS NOT THE ONLY TRANSFORM… cannot run without a pose"* | `static`: F's signature requires a pose argument that is not defaultable |
| **B8** | **shadow** vs **echo** | echo alone is apophenia; shadow alone is a local hack promoted as a primitive | Step 6: *"shadow then echo is a primitive"* | `ledger`: a PROMOTE row carries both verdicts, and `primitive` requires both |
| **B9** | **generator** vs **playback**; **prior** vs **replay** | a recording crosses the membrane and is replayed as knowledge | Step 6: *"Generators cross upward; playback never does"* | `static`: what crosses the promote boundary must be a callable, never a captured trace |
| **B10** | **import (outward)** vs **instrument (inward)** | reading one against the other; or an import that adds a world primitive | Step 7: *"Never read one against the other"* · *"IMPORT ADDS NO ATOM TO THE WORLD"* | `static`: **an import must pass through step 7 — a language-level `import` of a domain fact is a step-7 IMPORT executed by the wrong machinery** |
| **B11** | **library extended** vs **restructured** | Γ only ever grows and accrues the debt minting was meant to avoid | Step 4: *"Accepting only ever adds"* | `neither` — nothing to check until a refactor operator exists |
| **B12** | **habitat enumerated** vs **composed** | the field of contact treated as a term algebra | SYMBOLS: *"Enumerated, never composed"* | `static`: the habitat type is a sequence, not a library |
| **B13** | **the ground is not a frame** | the loop modifies its own anchor | SYMBOLS: *"Not in the library; the loop cannot modify it"* | `static`: the ground is injected, never imported; no write path to it |
| **B14** | **a seat** vs **a person** | a checking position defined by who holds it, not by what it can see | SYMBOLS, two-words note | `neither` |
| **B15** | **mode** — general / specified / grounded | an unmeasured number read as a measured one | DECLARING THE MODE: *"the mode must be stated"* | `ledger`: gate check 6 already; plus every module constant carries its basis |
| **B16** | **R as a slice** vs **R as complete** | a low reading read as an absence of residual | SYMBOLS: *"There is no state in which R is fully known"* | `neither` — this is a reading discipline, not a code property |

---

## The genus, and the mechanism it has

Every defect this list caught in its own machinery went wrong in the same place, and
the direction was always the same.

> **A repair validated on the case that prompted it, generalised silently.**
> A false positive announces itself. A false negative looks like a clean run.

Six instances, one class, all of them widening something that was true of the instance:

| | what widened | went |
|---|---|---|
| `# design check` returning True | a check with no failing path | green |
| PASS over an empty subject | a denominator counting the wrong population | green |
| `flat` as the spread at `actions[0]` | a baseline that could only be one thing | green |
| the settled set keyed on terms, not (slot, term) | one settlement licensing every slot | green |
| the convention scope collecting any `startswith` | an exemption swallowing a real finding | green |
| `seen` incrementing only inside the finding branch | subject and violation the same set | green |

**All six went green.** That is the whole reason the class is dangerous: a rule that fires
wrongly gets fixed the day it fires, and a rule that stops firing gets fixed when someone
happens to remember what it used to catch.

### The rule that follows

> **A rule's fixtures must pin BOTH edges of every exemption it grants.**

Not *the exemption is correct now* but *the exemption cannot silently widen or vanish*.
Widen it and the fixture's examined count rises; drop it and the count falls. Either way
the declared count stops matching and the rule suppresses itself.

### A change and its witness are not commutative

Fixtures before the change is not discipline. It is **the only order in which the
intermediate state is detectable.**

Demonstrated by accident: a patch adding the fixtures raised before writing the
widening, leaving the tree with fixtures present and exemption absent -- and `selftest`
correctly refused, `the control produced 1`. Land the widening first and the same
partial application is **invisible**, because a widened rule with no fixture to
contradict it looks exactly like a finished one.

So the two orders are not two routes to one place:

| order | a partial application looks like |
|---|---|
| **witness, then change** | a failure. `UNWITNESSED`, immediately |
| change, then witness | a completed change |

### And the witness does not belong on the rule

Three defects in this repo's own checkers were found by their witnesses rather than by
review, and **all three sat at the same two sites**:

| | site |
|---|---|
| the convention scope swallowing a real finding | an **exemption** |
| SINGLETON counting only violations | a **denominator** |
| the package scan cached on `id()` of a transient | a **denominator**, poisoned across fixtures |

**None was in the rule's logic.** The rules were correct; the boundaries around them were
not. Which fixes where a witness has to sit:

> **Witness what the rule EXCUSES and what it COUNTED — not what it decides.**

A rule's decision is the part a reader checks. Its exemptions and its denominator are the
parts nobody reads, and they are where every one of these lived.

### And one mechanical check that catches the sixth for free

> **A control that examines nothing cannot demonstrate a clean state.**

If a rule's `ok` fixture examines zero candidates, its subject and its violations are the
same set, `PASS` is unreachable, and `VACUOUS` quietly does the work `PASS` should. That
reads straight off the fixture declaration -- no analysis -- and it is enforced in both
`kernel.Linter.selftest` and `lint.selftest`.

---

## What this yields

**25 pairs. 9 already violated. 19 have a mechanical check** — 11 static, 8 ledger.
Three (B11, B14, B16) are not automatable and should be marked as such rather than
faked, because a check that cannot fail is worse than no check.

**A6 is the highest-value single check** — *a label must partition its call sites* —
because it generalises: it catches any case where the code names a distinction it does
not make, which is the shape of the worst defect in the current build.

**B10 is the one that will matter most in ARC** — a language-level import of a domain
fact is a step-7 IMPORT routed around step 7.

**A9 is not in the formula in so many words** and should probably be added to it. It is
step 2's independence clause applied to the checker rather than to the sorter, and it has
already produced one silent measurement drift here.
