# Conformance record — gamma.py promotion carries the settled method

A conformance change is NOT an amendment of the kernel. It is a repair where the CODE
contradicted a figure the kernel already states. This document records exactly where the
violation was, why it is a violation, and which figure lines — quoted verbatim from the
source SVGs — authorize the fix. Committed as `a75e543d`; the reasoning is also in WATSON 54.

---

## 1. WHERE the code violated the figure

**Write site:** `gamma.py`, `Gamma._units_built()`, the loop over `self.settled_terms`
(lines 2474-2481 before the fix; 2484-2501 after).

Before (verbatim, from `git show a75e543d^:gamma.py`):

```python
if len(t) <= 1:
    continue
unit = Term(t.atoms, origin=t.origin)      # <-- the violation
if unit.name not in seen:
    seen.add(unit.name)
    out.append(unit)
```

`Term` has five identity fields — `atoms, origin, operand, guard, operand_term` — and
`Term.name` includes `operand_term` and `guard` (`gamma.py:702-714`). A settled tree
`f<g(s)>` is keyed under a name that carries the branch. Promotion rebuilt it from
`atoms` alone, emitting bare `f`. The method the ground paid for was discarded on the way
back into the closure.

**After:** behind `TETHER_UNITS_KEEP_METHOD` (default ON), promotion carries
`operand_term=t.operand_term, guard=t.guard` and leaves only the per-board bindings
(`operand`, `guard_ref`) unset. OFF reproduces the old bytes exactly (verified: promoted
unit is bare `f`, `operand_term is None`).

This is the site F325 named in `docs/03-DESIGN/06-INDEX_MECHANISM_TO_SOURCE.md:46147`:
> "**A TERM SETTLES UNDER ONE IDENTITY AND IS PROMOTED UNDER ANOTHER.** `f<g(s)>?act` settles
> as itself and re-enters the search as bare `f` -- **the reusable chunk is a different
> computation from the one the ground paid for.**"

F325 said it "has never bitten … because nothing yet carries meaning outside the atom
sequence … `operand_term` is dead (`F324`)." That premise expired: trees are live (F470/F348),
and the must-fail test shows two settled trees with the same outer atom but different inner
branches now exist and previously collapsed into one unit.

---

## 2. WHY it is a violation (the effect, in the figure's own terms)

The contract being broken is: **what settles is what becomes available to compose over.**
A term earns standing by paying the bargain under a specific composition (the arrangement:
which operand tree, which guard). If promotion then hands the search a *different*
computation — the atom list with the arrangement stripped — the ground paid for one thing
and the agent received another. Three consequences, all visible without a run:

1. **The arrangement is lost.** `f<g(s)>` and `f<h(s)>` share the outer atom `f`, so both
   promoted to bare `f`. Two computations that the ground settled separately became one unit
   — F325's "two computations sharing one unit, executing as each other."
2. **The next level cannot inherit the method.** Fig 12 says a settled molecule becomes an
   atom *for whatever composes over it*. It cannot compose over a method it no longer holds.
   Inheritance of methods (Fig 4) was silently broken at this one line.
3. **The dedup key was keyed on the wrong identity.** `seen` used `unit.name`, but the emitted
   `unit` was built without the fields that make `name` distinctive — so a key that should
   separate schemas collapsed them. The figure calls this "the ingredients are recorded and
   the arrangement is not."

None of this is a matter of degree or a threshold. It is a discrete mismatch between the
identity a term settles under and the identity it re-enters with.

---

## 3. HOW the figure backs the fix — verbatim from the source SVGs

Extracted with the derive-first recipe (tspans joined, base64 metadata stripped) from
`figures/Figure_12_The_Bond.svg`, `Figure_4_The_Membrane.svg`,
`Figure_5_The_Mint_Pipeline_REV.svg`, `Figure_13_The_Minimum_Viable_Set.svg`.

**Fig 12 — The Bond** (the authorization, triangulated):
> "A set of ingredients is not one. The bond is the rest of the information, and it is the
> half nothing was recording."
> "the ingredients are recorded and the arrangement is not → the parts are not the thing"
> "The arrangement is the substance."
> "**A settled molecule becomes an atom for whatever composes over it.** So irreducible is a
> fact about a level and never about the world, and there is no bottom"

The fix carries the arrangement (operand tree + guard) across promotion; the old code carried
only the ingredients. Fig 12 states the contract and the violation together.

**Fig 4 — The Membrane** (the bound on what crosses):
> "The kernel is the part that does not change with size: the same loop and the same rule for
> naming what worked... Only the actors, the currency and the anchor change."
> "Only methods cross up. Only head starts come down."
> "upward: a method that can be reapplied. Never the recording of a particular success."

This both authorizes the change (a method must cross) and bounds it: the fix carries the
*method* (schema) and drops the *binding* (`operand`, `guard_ref` — per-board recordings).
It is why the fix is conformance, not amendment — the kernel rule ("a settled molecule
becomes an atom") is unchanged; the code is made to obey it.

**Fig 5 — The Mint Pipeline** (settling is necessary, not sufficient):
> "AMENDMENT · settling is necessary for a term to be composed over, and it is not sufficient."
> "A term is settled when the ground pays for it. A term is usable when something can compose
> over it. Those are two conditions and this figure names one."

The old code satisfied *settled* and failed *usable* — exactly the insufficiency Fig 5 names.

**Fig 13 — The Minimum Viable Set** (recursion of promotion):
> "And each composition becomes an atom for whatever composes over it."
> "A settled composition enters the library as a term, and is then an operand like any other."
> "The set is closed. The arrangements are not."

---

## 4. Conformance boundary — what this fix is NOT

- It does **not** change the bargain, any threshold, `max_depth`, or any atom. A term made
  representable by the fix still has to pass `_cannot_pay` and `pays` to be paid. No number
  was made greener.
- It does **not** change the kernel rule. The rule is exactly Fig 12's "a settled molecule
  becomes an atom for whatever composes over it"; the fix makes code match it.
- It does **not** add hidden state or route around the loop. Promoted units are plain `Term`
  objects in the ledger-visible library; the arm, its entry in `conform/arms.py`, and four
  must-fail tests (incl. the F325 mutation control) are all in the record.

Contrast with the change that was **retracted** in WATSON 54: editing the routine price
(`tether.py:25864`) would amend "the rule for naming what worked" (Fig 4) — a species
change, not conformance. That is the line this fix stays on the correct side of.

## 5. Falsification (what would show the fix is wrong)

- Zero settled terms with `operand_term` on the panel → no occasions; the change is inert
  (the wall is then price, not representation).
- Every representable depth-2 candidate still fails `pays` → correct abstention, not a
  representation defect.
- Any decision/binding/bargain change with the arm OFF → a filter/verdict change slipped in;
  reject. The OFF arm is byte-identical and tested.

---

FIGURE CENSUS: Fig 1 mint-if-pays · Fig 4 kernel/only-methods-cross · Fig 5 settled-necessary-
not-sufficient · Fig 6 same-reach-more-search · Fig 9 filters-not-verdicts · Fig 11 contact ·
Fig 12 arrangement-is-the-substance / settled-molecule-becomes-atom · Fig 13 closed-set-open-
arrangements. Strained: none. All figure quotes above are from the source SVGs, not a summary.
