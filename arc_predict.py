"""ARC's PREDICT atoms — DERIVED from `ARC_AGENT`'s eight-member table, not designed here.

**THE CORPUS NAMES SIX** and the row is a lookup rather than a decision:

    | atoms | grid transforms: translate, recolour, reflect, rotate, appear, vanish |

**AND FOUR OF THE SIX CANNOT BE EXPRESSED AGAINST THE SIGNATURE THE LOOP HAS.** This is
pre-registered as a structural finding rather than worked around, because working around it
is where an invented atom set would come from:

    signature    Ctx carries `action` and `operands` (other slots' values). Nothing else.
    a slot IS    one int -- `{obj}.row | .col | .h | .w | .colour`
    an atom IS   val x action x operands -> val, for ONE slot

| atom | expressible? | why |
|---|---|---|
| **translate** | **yes** | `v + operand`. The delta is another slot's value |
| **recolour** | **yes** | `v -> operand`. The target is another slot's value |
| **appear** | **no** | existence is not a slot VALUE. The slot SET changes and
  `_present` already sees it -- an event, not a transform |
| **vanish** | **no** | same, from the other side |
| **reflect** | **no** | needs the BOARD EXTENT (`W - col - w`); `Ctx` has no
  accessor and the board is not a slot |
| **rotate** | **no** | couples row and col, and an atom returns ONE slot's value |

**SO THE ATOM SET IS TWO, NOT SIX, AND THE GAP IS IN `Ctx` RATHER THAN IN THE LIST.** Naming
it here rather than inventing substitutes: a `reflect` that quietly reflected about the
object's own box would be a different operator wearing the corpus's word, and it would have
passed every check.

**NEITHER DELTA IS CHOSEN.** Both atoms read an OPERAND, following `take`'s established
pattern — *the one atom that makes an interaction expressible at all* — so the step size and
the target colour are **discovered by binding**, never fixed here. A `translate` hardcoded to
`+1` would be this file choosing the world's step size.

**PRE-REGISTERED, BEFORE ANY RUN, so a later reading cannot be fitted to what happened:**

1. `λ < V` on the three-space Γ. `ARC_AGENT` Stage D: *here the type graph is genuinely
   sparse, so unlike the toy world the number should mean something.* **If `λ = V`, either
   the typing is wrong or Stage D's claim is.**
2. **Both atoms must BIND.** An atom that never appears in a bound term over a real run is
   not part of the world's vocabulary, and that is a reading about the atom set, not about
   the loop.
3. **No claim is made about mint COUNT.** The stall was `REUSE_UNWIRED` and these atoms do
   not touch reuse. **Predicting improvement here would be fitting a build to a run**, which
   is the leak the whole firewall exists for — *a game showing you something is broken is
   legitimate; a game telling you what to build is not.*

**AND THE SIZE OF THIS SET IS NOT PRINCIPLED, WHICH THE CORPUS ALREADY SAYS.** Ashby's
inequality gives `closure(Γ)` *a lower bound the environment imposes rather than one the
designer picks* — and `ARC_BUILD_PLAN` records that **nothing computes it.** Six was a list,
two is what the signature admits, and neither number is derived from the environment's
disturbance variety. Stated so the count is not mistaken for a measurement.
"""
from __future__ import annotations

import sys

from gamma import SAME_AS_TARGET, Atom, Ctx

sys.dont_write_bytecode = True


def _idn(v: int, _c: Ctx) -> int:
    """THE IDENTITY, AND THE CORPUS'S SIX OMIT IT.

    Not a choice: `_predict` falls back to `self.bound.get(slot, IDN)`, so **a Γ without
    `idn` raises `KeyError` on the first unbound slot** -- which is what the first run with
    this set did. It is `the loop cannot run without it` in the most literal available sense,
    so it enters under §11 clause one and the ablation stays blind to it.

    **Every working atom set in the repo already had one and none said why**, which is why
    the omission survived into a named six-atom list.
    """
    return v


def _translate(v: int, c: Ctx) -> int:
    """`v + operand`. The displacement is another slot's value, never a constant here."""
    return v + c.operands[0] if c.operands else v


def _recolour(v: int, c: Ctx) -> int:
    """`v -> operand`. The target colour is another slot's value."""
    return c.operands[0] if c.operands else v


def predict() -> list[Atom]:
    """The two of the corpus's six that the per-slot signature admits.

    Passed INTO `arc_atoms.three_spaces(predict)`, which takes PREDICT as an argument
    precisely so that file does not choose what the agent may bet on. **The hole was left
    deliberately and had never been filled by any caller.**
    """
    return [Atom("idn", _idn, "val", "val"),
            # `v + operand` is meaningful only between commensurable quantities, so the
            # operand must be whatever the target is. A row plus a colour is arithmetic
            # that type-checks and means nothing.
            Atom("translate", _translate, "val", "val", reads_operand=True,
                 operand_type=SAME_AS_TARGET),
            # `v -> operand` puts the operand IN the slot, so it must be a colour whatever
            # the target is. THIS IS THE DEFECT'S OWN SITE: `idn . recolour<o11.h>`.
            Atom("recolour", _recolour, "val", "val", reads_operand=True,
                 operand_type="colour")]


def unexpressible() -> dict[str, str]:
    """The four the signature cannot carry, with the reason. **Reported, never substituted.**"""
    return {
        "appear": "existence is not a slot value; the slot SET changes and `_present` sees it",
        "vanish": "same, from the other side",
        "reflect": "needs the board extent; `Ctx` has no accessor and the board is not a slot",
        "rotate": "couples row and col; an atom returns one slot's value",
    }
