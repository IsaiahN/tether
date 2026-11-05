"""24 MUSING CHOSEN (TETHER_MUSING_CHOSEN, default ON; the reviewer 2026-11-05 r1250-r1252).
gridworld default seed 0, the agent seed pinned, 6 steps; parks planted in self.parked, each with
the recorded gain and kind item 24 writes at a level end. Each check its own process.
  check_m1_parks_game     a park survives an ADVANCE retarget; a NEW_BOARD retarget closes every
                          park with a muse_park_closed row and empties the store
  check_m1b_kind_host     a level-0 park whose slot name is gone is read on level 1 through
                          today's slot of its kind; a kind absent here is skipped, not refuted
  check_m2b_m3_order      gain x need orders the walk: the ls20-shaped parks put (48, need 1)
                          before (96, need 0); OFF the key order
  check_m4_rival          the best paying entry is offered as a by=muse rival on its host; a kind
                          walked with nothing paying is one witness against its muse weight
  check_m6_no_identity    no game id and no family name at the musing-chosen sites (AST)
    python tests/test_musing_chosen.py [check ...]
"""
from __future__ import annotations

import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True


def _agent():
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    assert tether._MUSING_CHOSEN, "TETHER_MUSING_CHOSEN is OFF"
    tether._AGENT_SEED = False
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    for _ in range(6):
        ag.step()
    return ag


def _park(ag, key: str, slot: str, gain: float, level: int = 0) -> dict:
    rec = {"slot": slot, "level": level, "hist": ag.history(slot) if slot in ag.slots else [],
           "slots": list(ag.slots), "gain": gain, "kind": ag._kind_key(slot),
           "owner_kind": ag._kind_str(slot.split(".", 1)[0])}
    ag.parked[key] = rec
    return rec


def check_m1_parks_game() -> None:
    import ledger
    import tether
    ag = _agent()
    slot = sorted(s for s in ag.slots if "." in s and not s.startswith("@"))[0]
    _park(ag, f"L0:{slot}", slot, 5.0)
    ag.retarget(ag.env, 1, how=ledger.ADVANCE)
    kept = sorted(ag.parked)
    ag.retarget(ag.env, 1, how=tether.NEW_BOARD)
    rows = [r["detail"] for r in ag.led.rows() if r["event"] == "muse_park_closed"]
    closed = {r["park"] for r in rows}
    assert f"L0:{slot}" in kept and not ag.parked and f"L0:{slot}" in closed, (kept, rows)
    print(f"  after ADVANCE kept {kept}; after NEW_BOARD empty, {len(rows)} closed rows")


def check_m1b_kind_host() -> None:
    ag = _agent()
    slot = sorted(s for s in ag.slots if s.endswith(".col") and not s.startswith("@"))[0]
    rec = _park(ag, "L0:gone.col", slot, 5.0)
    rec["slot"] = "gone.col"                       # the level-0 name means nothing here
    ag.level = 1
    host = ag._muse_host(rec)
    assert host is not None and ag._kind_key(host) == rec["kind"] and ag._muse_skip(rec) is None
    rec2 = dict(rec, kind=("NO SUCH KIND",))
    why = ag._muse_skip(rec2)
    assert why == "no slot of this kind here", why
    print(f"  level-0 park of kind {rec['kind']} read on level 1 through {host}; absent kind: "
          f"'{why}'")


def check_m2b_m3_order() -> None:
    import tether
    ag = _agent()
    cols = sorted(s for s in ag.slots if s.endswith(".col") and not s.startswith("@"))
    rows = sorted(s for s in ag.slots if s.endswith(".row") and not s.startswith("@"))
    ag._kind_key = lambda s: ("K", s.rsplit(".", 1)[-1])     # gridworld has one slot kind
    tether._GOAL_HYP = True
    ag._hyp = {"slots": [cols[0]], "key": "planted"}           # the held comparison: a .col
    t = {}
    t["L0:a"] = _park(ag, "L0:a", rows[0], 96.0)               # ls20's o2.rem_n: need 0
    t["L0:b"] = _park(ag, "L0:b", cols[0], 48.0)               # ls20's o10.add_n: need 1
    t["L0:c"] = _park(ag, "L0:c", cols[0], 12.0)               # ls20's o16.add_n: need 1
    on = [pk for pk, _r in ag._muse_order(t)]
    needs = {pk: ag._muse_need(r) for pk, r in t.items()}
    tether._MUSING_CHOSEN = False                              # MUSING's own order
    off = [pk for pk, _r in sorted(t.items())]
    assert on == ["L0:b", "L0:c", "L0:a"] and off == ["L0:a", "L0:b", "L0:c"], (on, off, needs)
    print(f"  needs {needs}; ON order {on} (48 x 1 first); OFF {off}")


def check_m4_rival() -> None:
    from gamma import Term
    ag = _agent()
    col = sorted(s for s in ag.slots if s.endswith(".col") and not s.startswith("@"))[0]
    row = sorted(s for s in ag.slots if s.endswith(".row") and not s.startswith("@"))[0]
    ag._kind_key = lambda s: ("K", s.rsplit(".", 1)[-1])     # gridworld has one slot kind
    ag._hyp = {"slots": [col], "key": "planted"}
    t = {"L0:b": _park(ag, "L0:b", col, 48.0), "L0:a": _park(ag, "L0:a", row, 96.0)}
    cand = Term(ag.gamma.library[sorted(ag.gamma.library)[0]].atoms)
    run = {"paying": [{"parked": "L0:b", "method": "m"}], "terms": {("L0:b", "m"): (cand, col)},
           "walked": ["L0:b", "L0:a"]}
    ag._mol_offers.clear()
    ag._muse_choose(run, t)
    offer = ag._mol_offers[col][-1]
    st = ag._rf_standing("muse", (t["L0:a"]["kind"],))
    assert offer["prov"]["by"] == "muse" and offer["prov"]["park"] == "L0:b", offer["prov"]
    assert st["against"] == 1.0, st
    row_ = [r["detail"] for r in ag.led.rows() if r["event"] == "muse_chosen"][-1]
    print(f"  offered {row_['offered']['park']} on {row_['offered']['host']} by=muse; kind walked "
          f"with nothing paying: against {st['against']}")


def check_m6_no_identity() -> None:
    import ast
    import inspect

    import tether
    fams = set(tether._DESC_SEED) | set(tether._DESC_SEED.values())
    fs = (tether.Agent._muse_need, tether.Agent._muse_order, tether.Agent._muse_host,
          tether.Agent._muse_skip, tether.Agent._muse_choose, tether.Agent._muse_close_parks)
    for f in fs:
        for n in ast.walk(ast.parse(inspect.cleandoc("\n" + inspect.getsource(f)))):
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                assert n.value not in fams, (f.__name__, n.value)
            name = n.attr if isinstance(n, ast.Attribute) else getattr(n, "id", "")
            assert "game" not in name.lower(), (f.__name__, name)
    print(f"  {len(fs)} sites: no game id, none of {len(fams)} family names")


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
    print(f"musing_chosen: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
