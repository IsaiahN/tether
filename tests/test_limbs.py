"""The limbs' fixtures (r250 item 3; Isaiah 2026-10-26 08:24, the reviewer 08:30, 08:34, 08:47).

Each shows the new behaviour fires and the old failure cannot recur, on a gridworld agent with the
one site under test isolated:
  - THE GOVERNOR: closer_found; urgent past the commit bar (must-fail: idle 0 is not urgent);
    probe_first while an action is untried, the same answer within one cycle, probe_declined at a
    later cycle with the same open set, probe_first again when the set changes; OFF walks;
  - L2: the delta order keeps EVERY candidate (the cut that lost a closing term cannot recur), on
    every slot of a stepped agent, with occasions counted;
  - L3: a type-mismatched closer is deferred, walked late after the typed candidates, and closes
    (typed_late closed 1); MUST-FAIL: with the governor saying act, the same lookup finds nothing;
  - L4: in a real mint with a widened stream, no base stream draws after the first widened draw,
    and the widened stream did draw (occasions > 0).

    python tests/test_limbs.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
import gamma
import gridworld
import ledger
import tether
import world

sys.dont_write_bytecode = True


def _agent() -> tether.Agent:
    env = world.bind(gridworld.family("default", 0, 4))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="limbs_fixture"),
                        tether.Config(), ledger.Ledger())


def check_governor() -> None:
    ag = _agent()
    keep = tether._THINK_OR_ACT
    try:
        tether._THINK_OR_ACT = True
        ag._can_probe = None
        ag.actions = ("A1", "A2")
        ag.iface.table = {"A1": {}}
        ag._last_progress = ag._last_commit = 0
        ag._relief_rate = lambda: (1.0, 0)
        assert ag._think_or_act("s", closer=True) == (False, "closer_found")
        ag.cycle = 10
        assert ag._think_or_act("s", closer=False) == (False, "urgent")
        ag.cycle = 0                                         # idle 0: not urgent
        assert ag._think_or_act("s", closer=False) == (False, "probe_first")
        assert ag._think_or_act("s", closer=False) == (False, "probe_first")   # same cycle
        ag._relief_rate = lambda: (1e9, 0)                   # never urgent from here
        ag.cycle = 1
        assert ag._think_or_act("s", closer=False) == (True, "probe_declined")
        ag.actions = ("A1", "A2", "A3")                      # the open set changed
        assert ag._think_or_act("s", closer=False) == (False, "probe_first")
        ag.iface.table = {"A1": {}, "A2": {}, "A3": {}}      # every action tried
        assert ag._think_or_act("s", closer=False) == (True, "ok")
        tether._THINK_OR_ACT = False
        ag.iface.table = {}
        assert ag._think_or_act("s", closer=True) == (True, "ok")
    finally:
        tether._THINK_OR_ACT = keep


def check_l2_the_order_keeps_every_candidate() -> None:
    ag = _agent()
    for _ in range(12):
        ag.step()
    tiered = 0
    for slot in sorted(ag.slots):
        robs = ag._residual_obs(slot, ag.gamma.library[ag.bound.get(slot, tether.IDN)],
                                ag.history(slot))
        others = [s for s in sorted(ag.slots) if s != slot]
        got = ag._delta_narrowed(others, robs)
        assert sorted(got) == others, (slot, others, got)
        tier = ag._delta_tier(others, robs)
        tiered += bool(tier)
        assert [tier.get(x, 3) for x in got] == sorted(tier.get(x, 3) for x in got), (slot, got)
    assert tiered, "no slot had a moved delta: the order was never exercised"


def _late_lookup(walk: bool) -> tuple:
    """`_library_fit` on a stepped agent with two candidates: A, whose head does not accept the
    slot type and which closes, and B, typed, which does not pay. Returns the pull, the order of
    the candidates' `_left` calls, and the typed_late row."""
    ag = _agent()
    for _ in range(6):
        ag.step()
    slot = next(s for s in sorted(ag.slots) if ag.history(s))
    ag.bound.pop(slot, None)
    held = ag.gamma.library[tether.IDN]
    a_name, b_name = [n for n in sorted(ag.gamma.library) if n != tether.IDN][:2]
    a, b = ag.gamma.library[a_name], ag.gamma.library[b_name]
    left = {id(held): 5.0, id(a): 0.0, id(b): 10.0}
    called: list = []

    def _left(term, _slot, _hist):
        if term is not held:
            called.append(term.name)
        return left.get(id(term), 5.0)

    ag._left = _left
    ag._bits = lambda _x: 1.0
    ag._units_for = lambda _s: ()
    ag._rebindings = lambda term, _s, _g=None, _r=None: iter([term])
    ag._take_pull = lambda n, _cand, _slot, **_k: n
    ag._carry_credit = lambda *_a: False
    ag._think_or_act = lambda _s, **_k: (True, "ok") if walk else (False, "urgent")
    keep = (tether._TYPED_BIND, tether._head_accepts, tether._may_bind,
            tether.retrieval.retrieve)
    try:
        tether._TYPED_BIND = True
        tether._head_accepts = lambda cand, _t: cand is not a
        tether._may_bind = lambda _c, _t: True
        tether.retrieval.retrieve = lambda *_a, **_k: iter([a_name, b_name])
        n0 = len(ag.led.rows())
        got = ag._library_fit(slot, None)
    finally:
        (tether._TYPED_BIND, tether._head_accepts, tether._may_bind,
         tether.retrieval.retrieve) = keep
    rows = [r for r in ag.led.rows()[n0:] if r.get("event") == "typed_late"]
    assert len(rows) == 1, rows
    return got, a_name, b_name, called, rows[0]["detail"]


def check_l3_a_type_mismatched_closer_is_walked_late_and_closes() -> None:
    got, a_name, b_name, called, row = _late_lookup(walk=True)
    assert got == a_name, (got, a_name)
    assert called == [b_name, a_name], called           # the typed one first, A last
    assert (row["deferred"], row["walked"], row["gate"], row["closed"]) == (1, 1, "ok", 1), row


def check_l3_must_fail_no_late_round_finds_nothing() -> None:
    got, _a, b_name, called, row = _late_lookup(walk=False)
    assert got is None, got
    assert called == [b_name], called
    assert (row["walked"], row["gate"], row["closed"]) == (0, "urgent", 0), row


def check_l4_base_streams_stop_before_a_widened_stream_draws() -> None:
    ag = _agent()
    ag.step()
    slot = max(sorted(ag.slots), key=lambda s: ag.alphabet.get(s, 0))
    stype = ag.slot_types.get(slot)
    assert stype, slot
    wide_t = next(t for t in sorted(set(ag.slot_types.values()), key=str)
                  if t and t not in ("val", tether.OBJ_TYPE, stype))
    base = dict(ag.trace[-1][0])
    seq = [1, 2, 3, 5, 6] + [4, 4, 7] * 4
    states = [{**base, slot: v} for v in seq]
    ag.trace = [(states[i], "A", states[i + 1], tether.NO_INTENT, None)
                for i in range(len(seq) - 1)]
    ag._trace_pos = None
    ag.bound.pop(slot, None)
    ag.cfg.max_depth = 2
    ag._think_or_act = lambda _s, **_k: (True, "ok")
    draws: list = []
    enum = ag.gamma.enumerate_closure

    def spy(in_t, out_t, *a, **k):
        for c in enum(in_t, out_t, *a, **k):
            draws.append(out_t == wide_t)
            yield c

    char = tether.retrieval.characterise

    def widen(*a, **k):
        g = char(*a, **k)
        return {**g, "varies_types": [wide_t, *(g.get("varies_types") or ())]}

    keep = (tether._STREAM_WIDEN, tether.retrieval.characterise)
    try:
        tether._STREAM_WIDEN = True
        tether.retrieval.characterise = widen
        ag.gamma.enumerate_closure = spy
        n0 = len(ag.led.rows())
        ag.mint(slot)
    finally:
        tether._STREAM_WIDEN, tether.retrieval.characterise = keep
        ag.gamma.enumerate_closure = enum
    assert any(draws), "the widened stream never drew: the order was never exercised"
    first = draws.index(True)
    assert not any(not w for w in draws[first:]), draws
    rows = [r for r in ag.led.rows()[n0:] if r.get("step") == "MINT" and r.get("slot") == slot
            and "widen" in (r.get("detail") or {})]
    assert rows and 1 in rows[-1]["detail"]["widen"]["gate"], rows


def main() -> int:
    checks = [v for k, v in globals().items() if k.startswith("check_")]
    for c in checks:
        c()
        print("ok  ", c.__name__)
    print(f"test_limbs: {len(checks)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
