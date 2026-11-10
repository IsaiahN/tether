"""30 SPREADING ACTIVATION (TETHER_SPREAD, default ON; the reviewer 2026-11-05 r1285, r1286).
gridworld default seed 0, the agent seed pinned, 6 steps; the lit sets and edge standings PLANTED
where a check is about the spread. Each check its own process.
  check_p1_partial_tail     a molecule with 3 of 4 operands lit outranks one with 1 of 4
  check_p2_personal         two different lit sets give different top sets, neither the degree
                            ranking's (personalized; an undamped walk converges both to it)
  check_p2b_collapse_control  P2's predicate is red at the undamped fixed point (r1286)
  check_p3_edge_paid        an edge that paid raises its molecule's activation next lookup
  check_p4_window_one       a 32-entry no-fit window books one against per edge
  check_p5_paid_crosses     edge paid crosses at edge level through the real lineage write and
                            read; against does not
  check_p6_bounded          the summed activation stays under seed / (1 - max p)
    python tests/test_spread.py [check ...]
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True


def _agent():
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    assert tether._SPREAD, "TETHER_SPREAD is OFF"
    tether._AGENT_SEED = False
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    for _ in range(6):
        ag.step()
    ag._reflexes["sa_edge"]["standing"].clear()     # the warm-up's edge witnesses aside
    return ag


def _lib():
    import tether
    return tether._library()


def _down(lib):
    out: dict = {}
    for k, ms in lib.ingredient_of.items():
        for m in ms:
            out.setdefault(m, []).append(k)
    return out


def _two_molecules(lib):
    """two molecules with >= 4 operands each and no operand in common"""
    down = _down(lib)
    big = sorted(m for m, ops in down.items() if len(set(ops)) >= 4)
    a = big[0]
    b = next(m for m in big[1:] if not set(down[m]) & set(down[a]))
    return a, sorted(set(down[a])), b, sorted(set(down[b]))


def check_p1_partial_tail() -> None:
    ag, lib = _agent(), _lib()
    a, oa, b, ob = _two_molecules(lib)
    act = ag._sa_spread(lib, frozenset(oa[:3] + ob[:1]))
    assert act.get(a, 0) > act.get(b, 0) > 0, (act.get(a), act.get(b))
    assert a in ag._sa_into and b in ag._sa_into
    print(f"  3-of-{len(oa)} lit {act[a]:.4f} > 1-of-{len(ob)} lit {act[b]:.4f}")


def _personal(ta: list, tb: list, lib) -> str | None:
    """P2's predicate: each lit set's top set is its own -- neither is the degree ranking's top set
    (the stationary distribution an undamped walk ends at, whatever the seed), and they differ.
    Read as SETS: at the fixed point equal-degree entries tie, and a tie broken by residual noise
    would make two collapsed orders look different."""
    import heapq
    down = _down(lib)
    deg = {k: len(lib.ingredient_of.get(k, ())) + len(down.get(k, ())) for k in
           set(lib.ingredient_of) | set(down)}
    top = set(heapq.nsmallest(len(ta), deg, key=lambda e: (-deg[e], e)))
    if set(ta) == top or set(tb) == top:
        return "a lit set's top set is the degree ranking's: the spread lost its seed"
    if set(ta) == set(tb):
        return "two lit sets, one top set"
    return None


def check_p2_personal() -> None:
    import heapq

    import tether
    ag, lib = _agent(), _lib()
    a, oa, b, ob = _two_molecules(lib)

    def top(seeds):
        ag._sa_cache = None
        act = ag._sa_spread(lib, frozenset(seeds))
        return heapq.nsmallest(tether.TOPK_K, act, key=lambda e: (-act[e], e))
    ta, tb = top(oa[:3]), top(ob[:3])
    bad = _personal(ta, tb, lib)
    assert bad is None, bad
    print(f"  two lit sets: top-{tether.TOPK_K} overlap {len(set(ta) & set(tb))} of "
          f"{tether.TOPK_K}, neither the degree top set")


def check_p2b_collapse_control() -> None:
    """r1286: P2 must FAIL under the collapse -- per-hop p 1.0 run to a fixed point. The same
    graph and 1/degree splits, undamped and lazy (so the walk cannot oscillate), 200 hops: P2's
    predicate is red there. Arm-independent: a control on the predicate, not on the arm."""
    import heapq

    import tether
    lib = _lib()
    a, oa, b, ob = _two_molecules(lib)
    down = _down(lib)

    def fixed(seeds):
        x = {s: 1.0 / len(seeds) for s in seeds}
        for _ in range(200):
            y: dict = {}
            for k, v in x.items():
                nb = list(lib.ingredient_of.get(k, ())) + down.get(k, [])
                y[k] = y.get(k, 0.0) + v / 2
                for m in nb:
                    y[m] = y.get(m, 0.0) + v / 2 / len(nb)
            x = y
        return heapq.nsmallest(tether.TOPK_K, x, key=lambda e: (-x[e], e))
    bad = _personal(fixed(oa[:3]), fixed(ob[:3]), lib)
    assert bad is not None, "the undamped fixed point passed P2: the guard cannot see the collapse"
    print(f"  undamped fixed point: P2 red ({bad})")


def check_p3_edge_paid() -> None:
    ag, lib = _agent(), _lib()
    a, oa, _b, _ob = _two_molecules(lib)
    seeds = frozenset(oa[:1])
    a0 = ag._sa_spread(lib, seeds).get(a, 0)
    board = getattr(ag, "_bond_board", 0)
    ag._reflexes["sa_edge"]["standing"][(oa[0], a, board)] = {"paid": 5, "against": 0.0,
                                                              "tick": ag.cycle}
    ag._sa_cache = None
    a1 = ag._sa_spread(lib, seeds).get(a, 0)
    assert a1 > a0 > 0, (a0, a1)
    print(f"  the edge {oa[0]} -> {a} paid 5: activation {a0:.5f} -> {a1:.5f}")


def check_p4_window_one() -> None:
    ag = _agent()
    ag._reflexes["gcw"]["standing"].clear()
    edge = ("x", "m")
    ag._gcw_win = {f"e{i}": set() for i in range(32)}
    ag._sa_into = {f"e{i}": {edge} for i in range(32)}
    ag._gcw_credit(list(ag._gcw_win), "against")
    st = ag._rf_standing("sa_edge", (*edge, getattr(ag, "_bond_board", 0)))
    assert st["against"] == 1, st
    print(f"  a 32-entry no-fit window over one edge: against {st['against']}")


def check_p5_paid_crosses() -> None:
    import lineage
    a = _agent()
    a._reflexes["sa_edge"]["standing"][("x", "m", 0)] = {"paid": 3, "against": 2.0,
                                                         "tick": a.cycle}
    with tempfile.TemporaryDirectory() as d:
        lineage._write(d, a, "g", False, [])
        recs = [x for g in lineage._read(Path(d)).values() for x in g.get("inventions", ())
                if x.get("kind") == "reflex"]
    assert recs and "against" not in json.dumps(recs), recs
    b = _agent()
    b._reinvent_carried(json.loads(json.dumps(recs)))
    assert b._rf_in("sa_edge", ("x", "m", 9)) == 3, b._rf_carried
    print(f"  edge paid 3 crossed to board 9; against stayed home "
          f"(p {b._sa_edge_p('x', 'm', 9):.3f})")


def check_p6_bounded() -> None:
    ag, lib = _agent(), _lib()
    a, oa, b, ob = _two_molecules(lib)
    act = ag._sa_spread(lib, frozenset(oa + ob))
    pmax = 2 / 3            # every edge fresh after the clear: the seed p
    assert sum(act.values()) <= 1.0 / (1 - pmax) + 1e-9, sum(act.values())
    print(f"  summed activation {sum(act.values()):.3f} <= {1 / (1 - pmax):.3f}")


def main() -> int:
    want = sys.argv[1:]
    names = [k for k in globals() if k.startswith("check_") and (not want or k in want)]
    if len(names) == 1:
        globals()[names[0]]()
        print("ok  ", names[0])
        return 0
    bad = [n for n in names if subprocess.run([sys.executable, "-B", __file__, n],
                                              cwd=str(_repo.ROOT),
                                              stdin=subprocess.DEVNULL).returncode]
    assert not bad, bad
    print(f"spread: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
