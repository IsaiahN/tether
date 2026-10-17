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


def cause_fold(state: list | None, if_c: C.Compiled, then_c: C.Compiled,
               frs: list[dict]) -> tuple[list, dict]:
    """`cause` as a fold over the frames (E1 X1, TETHER_REACH_EXACT): the state carries
    composer.holds' `⇒` reading (seen_a, b_before_a), the counts and the last if-side, so a later
    call reads only the frames after the ones already read. The same verdict as `cause` on the same
    frames: frames already read are recorded, and re-reading them re-spends them (Fig 12 :107-108).
    The caller restarts the fold (state None) whenever the frames themselves may differ."""
    n, seen_a, b_before_a, asked, held, refuted, if_now = state or (0, False, False, 0, 0, 0, None)
    for f in frs[n:]:
        x, y = C.run(if_c, f), C.run(then_c, f)
        if y is True:
            v = not (b_before_a or not seen_a)
            asked += 1
            held += v is True
            refuted += v is False
        if not seen_a and y is True and x is not True:
            b_before_a = True
        seen_a = seen_a or x is True
        if_now = x
    st = [len(frs), seen_a, b_before_a, asked, held, refuted, if_now if frs else None]
    return st, {"supported": asked > 0 and refuted == 0 and held > 0, "asked": asked,
                "held": held, "refuted": refuted, "if_now": st[6]}


def cause_tiers(mine: str, landed: str | None, age: dict, adj: dict, objects,
                boosted=frozenset(), dp=None, constant=frozenset()) -> list[tuple[str, ...]]:
    """E1 part 2 (Isaiah 2026-10-17 06:42, 06:54; the reviewer 06:49, 06:54): WHO may be the CAUSE
    of a change on `mine`, in the order an organism asks, and every other object in some tier -- an
    order for the budget, never a verdict (Fig 9 :60). Tier 0: the object the agent's own act
    landed on (R0, first), then the objects that changed, the most recent first (R1). Tiers 1..:
    the contact cascade out from `mine`, ring by ring (R2; Fig 11 :44). The last tier: every object
    no ring reached, so nothing is excluded (Fig 11 :61). Inside a tier, after R0: the higher the
    contingency of its changes with the effect (`dp`, reach.trail) the earlier, then a kind that
    already caused this kind of effect (`boosted`), then recency; CONSTANT objects last --
    deferred, never cut, since a constant may be an enabling condition (Fig 5 :43-44: a term that
    says nothing about WHEN fails the bargain). `age`: object -> frames since it last changed
    (absent: no change seen); `adj`: object -> what it touches."""
    pool = sorted(o for o in objects if o != mine)
    seen = {mine}
    dp = dp or {}

    def tier(cands, pinned=()) -> tuple[str, ...]:
        out = [o for o in cands if o not in seen]
        seen.update(out)
        rest = [o for o in out if o not in pinned]
        return tuple(o for o in out if o in pinned) + tuple(sorted(   # stable: keeps the order
            rest, key=lambda o: (o in constant, -max(dp.get(o, 0.0), 0.0), o not in boosted,
                                 age.get(o, len(pool)))))

    r0 = (landed,) if landed in pool else ()
    r1 = sorted((o for o in pool if o in age and o not in r0), key=lambda o: (age[o], o))
    tiers = [tier([*r0, *r1], pinned=r0)]
    ring = {mine}
    while True:
        nxt = sorted({n for o in ring for n in adj.get(o, ()) if n in pool and n not in seen})
        if not nxt:
            break
        tiers.append(tier(nxt))
        ring = set(nxt)
    tiers.append(tier(pool))
    return [t for t in tiers if t]


def trail(changed: list, effect: list, objects) -> tuple[dict, frozenset]:
    """Co-variation over the trail as CONTINGENCY on change events (Isaiah 06:54; the reviewer
    07:19; Rescorla 1968): per object, dP = P(it changed in the transition of the effect or the
    one just before | the effect) - P(the same | no effect). `changed`: one set per transition of
    the objects whose readings changed in it; `effect`: one bool per transition, the slot itself
    changed. A timer or noise changes every frame, so its dP is about 0; a trigger that changes
    only before the effect has dP > 0; a constant never changed. (dP per object, the constants).
    Neither is a verdict: the cause test still decides (Fig 9 :60)."""
    n_e = sum(1 for e in effect if e)
    n_o = len(effect) - n_e
    seen = set().union(*changed) if changed else set()
    dp: dict = {}
    for o in objects:
        if o not in seen:
            continue
        on = off = 0
        for t, e in enumerate(effect):
            c = o in changed[t] or (t > 0 and o in changed[t - 1])
            if c and e:
                on += 1
            elif c:
                off += 1
        dp[o] = (on / n_e if n_e else 0.0) - (off / n_o if n_o else 0.0)
    return dp, frozenset(o for o in objects if o not in seen)


def next_ring(ring: int, n_tiers: int, explained: bool) -> tuple[int, bool]:
    """The budget, one ring per step while the slot's change stays unexplained: (the ring to
    reach next step, every tier reached and still nothing). A supported cause stops the advance and
    the ring is kept, so a later failure resumes from it (the blocking guard: a whole tier is
    tested in its step, so a co-cause in the same tier is never cut off)."""
    if explained:
        return ring, False
    last = n_tiers - 1
    return min(ring + 1, last), ring >= last


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
