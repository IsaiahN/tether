"""reach: M4, the library's reach at the Figure 9 lookup site (METAPROGRAMMING_DESIGN section 4;
the reviewer 2026-10-08 00:57Z home (c), 07:14Z and 07:23Z 2026-10-09).

Pure functions over the agent's own recorded frames. The library OFFERS and the mint decides:
nothing here binds, mints or prices. A CAUSE pair is tested where bonds are tested (composer.holds),
and a compiled view whose term reads a ~1 operand is offered only with TETHER_PREV_OFFER ON --
otherwise it is kept and recorded with why (the swing seal, 2026-10-09).
"""
from __future__ import annotations

import sys
from collections.abc import Callable
from typing import Any

sys.dont_write_bytecode = True

import compile_term as C  # noqa: E402
import composer  # noqa: E402

PREV_OFF = "TETHER_PREV_OFFER off: term reads ~1"
SINGLE = ("STATE", "TEST", "PROCESS", "MEASURE", "RELATION")


def frames(trace: list, records: Callable[[dict], dict]) -> list[dict]:
    """Each trace row's before-state as a frame `compile_term.run` reads: the slot values, each
    slot's value one frame earlier under `slot~1` (None on the first frame -- there is none), and
    each object's record under its own name, reassembled from that same state."""
    out, prev = [], None
    for before, _a, _af, _i, _l in trace:
        f = dict(before)
        for k in before:
            f[k + C.PREV] = prev.get(k) if prev is not None else None
        f.update(records(before))
        out.append(f)
        prev = before
    return out


def reads_prev(c: C.Compiled) -> bool:
    """The gate's one test: the compiled term's own operand reads a slot one frame earlier."""
    return bool(c.operand) and c.operand.endswith(C.PREV)


def cause(if_c: C.Compiled, then_c: C.Compiled, frs: list[dict]) -> dict:
    """`if => then` read by composer.holds over the frames. Asked only where the then-side
    happened (Fig 12: "is there a B before A fires? No."); SUPPORTED when it held on some asked
    frame and failed on none. `if_now` is the if-side on the latest frame (Amendment A)."""
    a = [C.run(if_c, f) for f in frs]
    b = [C.run(then_c, f) for f in frs]
    got = composer.holds("⇒", a, b)
    seen = [got[t] for t, y in enumerate(b) if y is True]
    return {"supported": bool(seen) and False not in seen and True in seen,
            "asked": len(seen), "held": seen.count(True), "refuted": seen.count(False),
            "if_now": a[-1] if a else None}


def compile_cause(cand: dict, atoms: dict) -> tuple[C.Compiled, C.Compiled] | str:
    """Both sides compiled, or the first side's refusal as a reason string."""
    sides = []
    for side in ("if", "then"):
        c = C.compile_candidate({"condition": cand[side]}, atoms)
        if isinstance(c, C.Refusal):
            return f"{side}: {c.reason}"
        sides.append(c)
    return sides[0], sides[1]


def offer_or_withhold(c: C.Compiled, prev_offer: bool) -> tuple[bool, str | None]:
    """(offered, why-not). A ~1-reading term is offered only with the arm ON."""
    if reads_prev(c) and not prev_offer:
        return False, PREV_OFF
    return True, None


def bits(c: C.Compiled, term_bits: Callable[[Any], float]) -> float:
    """A compiled side's description length, for the record beside an offer (Amendment B)."""
    return round(term_bits(c.term), 3)
