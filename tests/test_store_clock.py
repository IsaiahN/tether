"""PIECE 1, THE STORE CLOCK (the reviewer r1679, r1681, r1711; Isaiah 2026-11-10 12:19-13:33), arms
TETHER_FADE_BY_STORE and TETHER_FADE_SHARE.

  T1  a still board (no writes) ages nothing, 50 reads. MF: the cycle clock ages it
  T2  a write ages an unused item (a failure and a paid habit); a use resets the habit
  T3  share form: the same 10 writes age a small store's item more than a large store's.
      MF: the raw form ages them equally
  T4  a carried evidence row with no clock reading (written on the cycle clock) replays as a fresh
      start (age 0), never as store units
  T5  a cleared store never lowers W; what it gains again counts
  T7  path-independence: the same events read at every write vs once at the end give the same
      presented value. MF: the in-place decay with the share age (100/200/400: 1.0 vs 0.75)
  T8  own time across contexts (r1713): two failures the present categorizer puts in different
      contexts fade separately, the older lower
  T9  reassessment (r1713): an old failure in the same present context as a new one is presented
      from the new one's W. MF: per-event stamps alone (r1711) leave it faded
  T10a (r1714) the same failure on two boards, its objects named differently, groups together.
      MF: a name-keyed context puts them apart
  T10b the present self sorts: remap the categorizer between two reads and the grouping follows.
      MF: a label kept from record time keeps the old grouping
  T11 C1 part 2 on the store clock: a miss counted as a refusal keeps its own stamp and contact,
      and misses + refusals == rejections. MF: moved at the current stamp, it would read unfaded
  T12 a failure's contact on an owner one of whose slots has no published attribute (None):
      read without raising, the pair [None, type] kept, sorted last (the E2E's fault on sp80,
      cycle 29). MF: the bare sorted() raises "'<' not supported ... 'NoneType' and 'str'"
  T13 before the seed converts (r1730, r1733): a newborn's failure stamped in cycle 1, read at
      cycle 3, with W growing in cycle 2 only, has aged exactly 1 active cycle: 0.5^(1/8).
      MF: r1711's "no fade" reads raw (1.0); cycles since the stamp, flat ones counted, read 2
  T14 a still board ages nothing before conversion either: W flat over cycles 3-8, a failure
      stamped in cycle 3 reads raw at cycle 8. MF: counting every cycle fades it (0.5^(5/8))
  (T6, zero-is-off, is gw12 with TETHER_FADE_BY_STORE=0 against the previous head)

    python tests/test_store_clock.py
"""
from __future__ import annotations

import os
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402
from gamma import Standing  # noqa: E402


class _Arms:
    """set gamma's and tether's fade arms for one check, and put them back"""

    def __init__(self, store: bool, share: bool = True) -> None:
        self.want = {(gamma, "_FADE_BY_STORE"): store, (gamma, "_FADE_SHARE"): share,
                     (tether, "G_FADE_BY_STORE"): store}

    def __enter__(self):
        self.keep = {k: getattr(*k) for k in self.want}
        for (m, n), v in self.want.items():
            setattr(m, n, v)

    def __exit__(self, *a):
        for (m, n), v in self.keep.items():
            setattr(m, n, v)


def _refuted(w: float, h: float) -> Standing:
    st = Standing()
    st.refute(w, h)
    return st


def check_t1() -> None:
    with _Arms(True):
        st = _refuted(100, 0.5)
        for _ in range(50):
            st.decay(100, 0.5)
        still = st.rejections
    with _Arms(False):
        st = _refuted(0, 8.0)
        st.decay(50, 8.0)
        cyc = st.rejections
    assert still == 1.0, still
    assert cyc < 1.0, f"MUST-FAIL: the cycle clock did not age it: {cyc}"
    print(f"  T1: no writes, 50 reads: {still} on the store clock; the cycle clock, 50 cycles: "
          f"{cyc:.4f}")


def _agent() -> tether.Agent:
    env = world.bind(gridworld.family("default", 0))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="store_clock"), tether.Config(),
                        ledger.Ledger())


def check_t2() -> None:
    with _Arms(True):
        st = _refuted(100, 0.5)
        st.decay(200, 0.5)
        fail = st.rejections
        ag = _agent()
        g = ag.gamma
        g.book["store_writes"], g.store_seed = 100, 0.5
        rec = ag._rf_standing("orient", ("x",))
        rec["paid"] += 3
        p0 = ag._rf_standing("orient", ("x",))["paid"]
        g.book["store_writes"] = 200
        aged = ag._rf_standing("orient", ("x",))["paid"]
        rec = ag._rf_standing("orient", ("x",))
        rec["paid"] += 1
        back = ag._rf_standing("orient", ("x",))["paid"]
    assert fail < 1.0, fail
    assert p0 == 3 and aged < 3, (p0, aged)
    assert back == 4, f"a use did not bring the habit back: {back}"
    print(f"  T2: 100 writes (W 100 -> 200): a failure 1 -> {fail:.4f}; a paid habit 3 -> "
          f"{aged:.4f}; one use -> {back}")


def check_t3() -> None:
    with _Arms(True):
        small, large = _refuted(10, 0.5), _refuted(1000, 0.5)
        small.decay(20, 0.5)
        large.decay(1010, 0.5)
        s, ln = small.rejections, large.rejections
    with _Arms(True, share=False):
        small, large = _refuted(10, 5.0), _refuted(1000, 5.0)
        small.decay(20, 5.0)
        large.decay(1010, 5.0)
        rs, rl = small.rejections, large.rejections
    assert s < ln, (s, ln)
    assert rs == rl, f"MUST-FAIL: the raw form aged them differently: {rs} {rl}"
    print(f"  T3: 10 writes: share form small store {s:.4f}, large {ln:.4f}; raw form {rs:.4f}, "
          f"{rl:.4f}")


def check_t4() -> None:
    with _Arms(True):
        ag = _agent()
        g = ag.gamma
        name = "store_clock_t4"         # a learned term (gridworld's library is innate only)
        g.library[name] = next(iter(g.library.values()))
        g.book["store_writes"], g.store_seed = 500, 0.5
        g.replay([["refute", name, None, None, 3]])          # written on the cycle clock
        st = g.standing[name]
        g.replay([["refute", name, None, None, 4, {"w": 250}]])
        fresh = st.ev[0][0]
        st.decay(*g._fade_at())
        own = st.rejections
    assert fresh == 500, f"a cycle-clock row was read as store units: stamped {fresh}"
    assert 1.0 < own < 2.0, own
    print(f"  T4: a row with no reading is stamped at W now ({fresh}); a row with one at its own "
          f"(250): presented {own:.4f} of 2")


def check_t5() -> None:
    with _Arms(True):
        ag = _agent()
        ag._store_tick()
        w0 = ag.gamma.book["store_writes"]
        ag._thought_note("k", ["a", "b"], set())
        ag._store_tick()
        w1 = ag.gamma.book["store_writes"]
        ag._thought = {"tried": {}, "paid": {}}
        ag._kind_landed_dk.clear()
        ag._store_tick()
        w2 = ag.gamma.book["store_writes"]
        ag._thought_note("k", ["a"], set())
        ag._store_tick()
        w3 = ag.gamma.book["store_writes"]
    assert w1 == w0 + 2 and w2 == w1 and w3 == w2 + 1, (w0, w1, w2, w3)
    print(f"  T5: W {w0} -> {w1} (2 new entries) -> {w2} (stores cleared) -> {w3} (1 again)")


def check_t7() -> None:
    marks = [100, 150, 200, 300, 400]
    with _Arms(True):
        every = _refuted(100, 0.5)
        every.refute(200, 0.5)
        for w in marks:
            every.decay(w, 0.5)
        once = _refuted(100, 0.5)
        once.refute(200, 0.5)
        once.decay(400, 0.5)
    assert abs(every.rejections - once.rejections) < 1e-12, (every.rejections, once.rejections)
    # MF: the in-place decay with the share age, the same item read at 200 and 400 vs once
    x2 = 0.5 ** ((1 - 100 / 200) / 0.5) * 0.5 ** ((1 - 200 / 400) / 0.5)
    x1 = 0.5 ** ((1 - 100 / 400) / 0.5)
    assert abs(x2 - x1) > 1e-6, "MUST-FAIL: the in-place share decay composed"
    print(f"  T7: read at every write {every.rejections:.6f} = once at the end "
          f"{once.rejections:.6f}; in-place share decay {x2:.4f} vs {x1:.4f}")


OLD, NEW = 0.5 ** ((1 - 100 / 400) / 0.5), 0.5 ** ((1 - 300 / 400) / 0.5)
# raw contacts as _fail_contact writes them: attribute, type, before, after, owner pairs, code
RED_UP = ["row", "POSITION", 3, 4, [["col", "POSITION"], ["colour", "COLOUR"], ["row", "POSITION"]],
          None]
RED_UP_2 = ["row", "POSITION", 7, 8, [["col", "POSITION"], ["colour", "COLOUR"],
                                     ["row", "POSITION"]], None]
GREY_SHAPE = ["shape", "SHAPE", 1, 2, [["shape", "SHAPE"]], None]
CAT = (tether._fail_context, "today")


def _two(c1, c2, cat):
    st = Standing()
    st.refute(100, 0.5, cat=cat, contact=c1)
    st.refute(300, 0.5, cat=cat, contact=c2)
    st.decay(400, 0.5, cat)
    return st.rejections


def check_t8() -> None:
    with _Arms(True):
        got = _two(RED_UP, GREY_SHAPE, CAT)
    assert tether._fail_context(RED_UP) != tether._fail_context(GREY_SHAPE)
    assert abs(got - (OLD + NEW)) < 1e-12 and OLD < NEW, (got, OLD, NEW)
    print(f"  T8: two contexts, failures at W 100 and 300, read at 400: {OLD:.4f} + {NEW:.4f} = "
          f"{got:.4f}")


def check_t9() -> None:
    with _Arms(True):
        got = _two(RED_UP, RED_UP_2, CAT)
        own = _two(RED_UP, RED_UP_2, None)          # r1711: per-event stamps alone
    assert tether._fail_context(RED_UP) == tether._fail_context(RED_UP_2)
    assert abs(got - 2 * NEW) < 1e-12, got
    assert own < got, f"MUST-FAIL: per-event stamps alone reassessed it: {own}"
    print(f"  T9: one present context: the old failure presented from the new one's W, {got:.4f} "
          f"(= 2 x {NEW:.4f}); per-event stamps alone {own:.4f}")


def check_t10a() -> None:
    import re
    with _Arms(True):
        got = _two(RED_UP, RED_UP_2, CAT)

        def by_name(c):                             # MF: a context keyed on an instance name
            return (c[-1],)
        named_a, named_b = [*RED_UP, "o3"], [*RED_UP_2, "o11"]
        apart = _two(named_a, named_b, (by_name, "named"))
    import inspect
    src = inspect.getsource(tether._fail_context)
    assert not re.search(r"o\d+", src.split('"""')[-1]), "the context function reads a name"
    assert abs(got - 2 * NEW) < 1e-12 and abs(apart - (OLD + NEW)) < 1e-12, (got, apart)
    print(f"  T10a: two boards, objects named differently, one present kind and change: grouped "
          f"({got:.4f}); keyed on a name: apart ({apart:.4f}); _fail_context reads no o<n>")


def check_t10b() -> None:
    with _Arms(True):
        st = Standing()
        cat1 = (tether._fail_context, "v1")
        st.refute(100, 0.5, cat=cat1, contact=RED_UP)
        st.refute(300, 0.5, cat=cat1, contact=GREY_SHAPE)
        st.decay(400, 0.5, cat1)
        before = st.rejections
        cat2 = (lambda _c: "one kind now", "v2")     # the present self's categories changed
        st.decay(400, 0.5, cat2)
        after = st.rejections
        st.decay(400, 0.5, (lambda _c: "one kind now", "v1"))    # MF: the record-time token
        kept = st.rejections
    assert abs(before - (OLD + NEW)) < 1e-12 and abs(after - 2 * NEW) < 1e-12, (before, after)
    assert abs(kept - (OLD + NEW)) < 1e-12, f"MUST-FAIL: a kept label regrouped: {kept}"
    print(f"  T10b: read under v1 {before:.4f} (apart); categorizer remapped, v2 {after:.4f} "
          f"(together); the v1 labels kept: {kept:.4f}")


def check_t11() -> None:
    with _Arms(True):
        ag = _agent()
        g = ag.gamma
        name = "store_clock_t11"
        g.library[name] = next(iter(g.library.values()))
        g.book["store_writes"], g.store_seed = 100, 0.5
        g.refute(name, contact=RED_UP)
        g.book["store_writes"] = 200
        moved = g.refusal_from_miss(name, 100)
        st = g.standing[name]
        refs = [e for e in st.ev if e[2] == "ref"]
    assert abs(moved - 0.5) < 1e-12, moved
    assert refs and refs[0][0] == 100 and refs[0][4] == RED_UP, st.ev
    assert abs(st.misses + st.refusals - st.rejections) < 1e-9 and abs(st.refusals - 0.5) < 1e-12
    unfaded = 1.0                                   # MF: the same move stamped at W 200
    assert unfaded != st.refusals, "MUST-FAIL: the moved refusal read unfaded"
    print(f"  T11: miss at W 100, counted as a refusal at W 200: moved {moved}, its stamp "
          f"{refs[0][0]} and contact kept; misses {st.misses} + refusals {st.refusals} = "
          f"rejections {st.rejections}")


def check_t12() -> None:
    ag = _agent()
    real = ag.env.attribute_of
    own = ag.env.slot_owner() if hasattr(ag.env, "slot_owner") else {}
    by: dict = {}
    for s in ag.slots:
        by.setdefault(own.get(s, s.split(".")[0]), []).append(s)
    mates = next((m for m in by.values() if len(m) >= 2), [])
    assert len(mates) >= 2, ("precondition: an owner with two slots", by)
    slot = mates[0]
    gone = next(s for s in mates if s != slot)
    ag.env.attribute_of = lambda: {k: v for k, v in real().items() if k != gone}
    contact = ag._fail_contact(slot)
    obs = contact[4]
    assert obs[-1][0] is None and any(p[0] is not None for p in obs), obs
    pairs = [[ag.env.attribute_of().get(s), str(ag.slot_types.get(s))] for s in mates]
    try:
        sorted(pairs)
        raised = None
    except TypeError as e:
        raised = str(e)
    assert raised and "NoneType" in raised, ("MUST-FAIL: the bare sort did not raise", raised)
    print(f"  T12: an owner with slot {gone} unpublished: contact read, {len(obs)} pairs, the "
          f"None pair last ({obs[-1]}); MF the bare sort raises: {raised}")


def _pre_seed(rec, tick):
    """A newborn's Gamma before its seed converts, with this W-by-cycle record, read at `tick`."""
    g = _agent().gamma
    g.w_cycles, g.tick, g.store_seed = [list(r) for r in rec], tick, None
    g.book["store_writes"] = rec[-1][1]
    _now, h = g._fade_at()
    assert isinstance(h, gamma.SeedCycles), ("precondition: the seed in cycles", h)
    return g, h


def check_t13() -> None:
    with _Arms(True):
        # W: 0 at the start, 10 after cycle 0, flat in cycle 1, 20 after cycle 2; read in cycle 3.
        # A failure in cycle 1 is stamped 10 (the W of the step before it)
        g, h = _pre_seed([[-1, 0], [0, 10], [1, 10], [2, 20]], 3)
        got = gamma._store_fade(10, g.clock(), h)
        st = gamma.Standing()
        st._ev_add(10, "ref", None, None)
        st.decay(*g._fade_at())
    want = 0.5 ** (1 / gamma.REJECTION_HALFLIFE)
    raw, every = 1.0, 0.5 ** (2 / gamma.REJECTION_HALFLIFE)
    assert abs(got - want) < 1e-12 and abs(st.rejections - want) < 1e-12, (got, st.rejections)
    assert raw != got and every != got, "MUST-FAIL: the rejected rules read the same"
    print(f"  T13: stamped in cycle 1, read at cycle 3, W grew in cycle 2 only: {got:.6f} = "
          f"0.5^(1/8) (a Standing reads {st.rejections:.6f}); MF no fade {raw}, every cycle "
          f"counted {every:.6f}")


def check_t14() -> None:
    with _Arms(True):
        rec = [[-1, 0], [0, 10], [1, 15], [2, 20]] + [[c, 20] for c in range(3, 9)]
        g, h = _pre_seed(rec, 8)
        got = gamma._store_fade(20, g.clock(), h)
    every = 0.5 ** (5 / gamma.REJECTION_HALFLIFE)
    assert got == 1.0 and every != got, (got, every)
    print(f"  T14: W flat over cycles 3-8, a failure stamped in cycle 3 read at cycle 8: {got} "
          f"(raw); MF every cycle counted: {every:.6f}")


def main() -> int:
    for check in (check_t1, check_t2, check_t3, check_t4, check_t5, check_t7, check_t8,
                  check_t9, check_t10a, check_t10b, check_t11, check_t12, check_t13, check_t14):
        check()
    print("store_clock: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
