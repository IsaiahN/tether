"""2c's lens. Offer coarse views of a board, and offer NONE unless one is near-lossless.

`ARC_AGENT` §5: detect a board, **commit only if the round trip is near-lossless, and return
`None` otherwise**, with `1 - fidelity` as `R_T`.

WHY THIS IS 2b's INSTRUMENT AND NOT A SENSOR. The loud/silent split is 2b's characteristic
failure -- an object-level view of a sub-object rule reads zero residual while the world moves
underneath it -- and `DECOMPOSITION` names what would catch it: *its round-trip gap on the
fleck cell would have been positive on every one of them.* The detector is R_T, so the
channel has to be fed before 2b can see its own worst failure. `never_live` cannot do it:
it needs `misses == 0`, and the loud/silent case has other slots live by construction.

THE VIEWS ARE BUILT FROM SHAPE ALONE. A stride divides the side or it does not; nothing here
is shown a rule, a colour's meaning, or an outcome. That is the same guarantee `snaps._views`
states for itself -- *a view cannot be chosen for resolving a rule it has never been shown* --
and it is what keeps offering a view from being answering the question.
"""
from __future__ import annotations

import sys
from collections.abc import Callable

sys.dont_write_bytecode = True

# anchor: INHERITED WITH ITS PROVENANCE, not chosen here. `logical_grid`'s calibration is the
# one constant in the tree that records the measurement that forced it AND the value that
# would have been wrong: a true 5-px grid scored 0.818 while a spurious 2-px tiling scored
# 0.946 -- THE WRONG ANSWER SCORED HIGHER -- so fidelity alone cannot discriminate, the gate
# sits high, and the stride is taken from motion rather than from a static tiling.
FIDELITY_GATE = 0.98


def _strides(side: int) -> list[int]:
    """Candidate cell sizes: the proper divisors of the side, coarsest first.

    Shape only. 1 is excluded because it is the identity and the loop already carries
    `full`; `side` is excluded because a one-cell board holds nothing to lose."""
    return [k for k in range(side - 1, 1, -1) if side % k == 0]


def _blocks(names: list[str], k: int) -> dict[str, str]:
    """Which block each cell belongs to, from the NAME's coordinates and nothing else."""
    out = {}
    for n in names:
        r, c = int(n[1]), int(n[2])
        out[n] = f"b{r // k}{c // k}"
    return out


def views(names: list[str], side: int) -> list[tuple[str, Callable]]:
    """The coarse views this board offers: one per stride, plus `full`.

    Each is a T_A -- a many-to-one map from the full reading to a coarser one. `T_E` is the
    coarse value taken literally, which the loop's `_round_trip` applies, so `x <= T_E(T_A(x))`
    holds and the gap is what the view discarded.
    """
    out: list[tuple[str, Callable]] = [("full", dict)]
    for k in _strides(side):
        member = _blocks(names, k)

        def t_a(state: dict[str, int], m=member) -> dict[str, int]:
            # the block takes its first member's value: a representative, so the round trip
            # returns that value for every cell in the block and the gap is what the other
            # cells differed by. Not a mean -- averaging would invent a value no cell held.
            rep: dict[str, int] = {}
            for slot, block in m.items():
                rep.setdefault(block, state[slot])
            return {slot: rep[block] for slot, block in m.items() if slot in state}

        out.append((f"stride:{k}", t_a))
    return out


def lens(names: list[str], side: int, fidelity: Callable[[Callable], float],
         gate: float = FIDELITY_GATE) -> list[tuple[str, Callable]] | None:
    """The offer, or NOTHING.

    `fidelity` scores one view in [0, 1] -- `1 - R_T/ceiling` at the caller's ceiling, which
    keeps this file from owning the units. **If no view clears the gate, this returns None
    and the bracket channel reports closed**, which is the honest state for a board that is
    not a rendering of anything coarser.

    RETURNING `None` IS A READING, NOT AN ABSENCE. `transform()` returning None already means
    *no coarse view is defined*, and the loop records it as `channel_closed` with the reason
    on the row. A lens that offered views nothing could commit to would report a channel that
    is open and carrying noise, which is worse than one that says it found nothing.
    """
    offered = views(names, side)
    committed = [(n, f) for n, f in offered
                 if n == "full" or fidelity(f) >= gate]
    return committed if len(committed) > 1 else None
