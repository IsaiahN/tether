"""THE REFLEX CARRY (TETHER_REFLEX_CARRY, default ON; owed from r1244; the reviewer 2026-11-05
r1248, r1248a). gridworld default seed 0, the agent seed pinned, 6 steps; game A's standing and
loss relation planted, written through lineage._write into a temp dir, read back from the file,
and seeded into a fresh game B through _reinvent_carried. Each check its own process; a run with
TETHER_REFLEX_CARRY=0 in the environment turns the checks red.
  check_k1_paid_crosses     paid crosses the boundary, against does not; a second write sends
                            only the increment
  check_k2_loss_crosses     a carried loss relation makes _how_soon finite in B before any loss
  check_k3_no_kind          the same carry where B has no partner of that kind: inf, no roll
  check_k4_head_start       carried paid 1: no stop after 2 misses, a stop after 3 (n + 2)
  check_k5_freeze           freeze carries as (goal kind, "freeze"), no button; no fire in B
                            without B's own vote
  check_k6_no_names         no carried key holds an action name or a board object name
    python tests/test_reflex_carry.py [check ...]
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
ORIENT = ("K", "orient")


def _agent():
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    assert tether._REFLEX_CARRY, "TETHER_REFLEX_CARRY is OFF: nothing carried"
    tether._AGENT_SEED = False
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    for _ in range(6):
        ag.step()
    return ag


def _written(ag) -> list:
    """Game A's generation written by the real lineage write; the reflex records read back."""
    import lineage
    with tempfile.TemporaryDirectory() as d:
        lineage._write(d, ag, "g", False, [])
        gens = lineage._read(Path(d))
        return [r for g in gens.values() for r in g.get("inventions", ())
                if r.get("kind") == "reflex"]


def _plant_a(ag, paid=2, against=1.5):
    ag._reflexes["orient"]["standing"][ORIENT] = {"paid": paid, "against": against,
                                                  "tick": ag.cycle}


def check_k1_paid_crosses() -> None:
    a = _agent()
    _plant_a(a)
    recs = _written(a)
    assert len(recs) == 1, recs
    rec = recs[0]
    assert rec["paid"] == [["orient", list(ORIENT), 2]] and "against" not in json.dumps(rec), rec
    a._reflexes["orient"]["standing"][ORIENT]["paid"] = 3
    again = a._reflex_carry()
    assert again["paid"] == [["orient", list(ORIENT), 1]], again        # the increment only
    b = _agent()
    b._reinvent_carried(json.loads(json.dumps(recs)))
    st = b._rf_standing("orient", ORIENT)
    assert b._rf_in("orient", ORIENT) == 2 and st["against"] == 0.0, (b._rf_carried, st)
    print(f"  written {rec['paid']}, no against; increment {again['paid']}; B carried "
          f"{b._rf_in('orient', ORIENT)}, B against {st['against']}")


def _plant_loss(ag):
    hk = ag._kind_str("o2")
    k = ("planted", "right", ())
    ag._game_loss_n[k] = 1
    ag._loss_rel = {k: Counter({("game_loss", "terminal", ((hk, "orthogonal"),)): 1})}
    return hk


def _stub(ag, at, subject="o0"):
    import tether
    before = dict(ag.env.observe())
    for i in range(6):
        r, c = at.get(f"o{i}", (100 + 10 * i, 100 + 10 * i))
        before[f"o{i}.row"], before[f"o{i}.col"] = r, c
    ag._hs_subject = lambda: {subject}
    ag._spent = tether.STEP_BUDGET - 20000
    ag.gamma.is_settled = lambda _n, _s: True
    for s in before:
        ag.bound.setdefault(s, tether.IDN)

    def step(st, action, preds, _unread, used, _coord=None):
        out = dict(st)
        used[0] += len(preds)
        if action == "right":
            out[f"{subject}.col"] = st[f"{subject}.col"] + 1
        return out
    ag._la_predict = step
    return before


def check_k2_loss_crosses() -> None:
    a = _agent()
    _plant_loss(a)
    recs = _written(a)
    assert recs and recs[0]["loss"], recs
    b = _agent()
    assert not b._game_loss_n and b._how_soon("right", dict(b.env.observe()))[0] == float("inf")
    b._reinvent_carried(json.loads(json.dumps(recs)))
    before = _stub(b, {"o0": (5, 1), "o2": (5, 4)})
    j = b._how_soon("right", before)[0]
    assert j == 2 and not any(b._game_loss_n.values()), (j, dict(b._game_loss_n))
    print(f"  carried {recs[0]['loss']}; B, no loss of its own: reading {j}")


def check_k3_no_kind() -> None:
    a = _agent()
    _plant_loss(a)
    recs = json.loads(json.dumps(_written(a)))
    recs[0]["loss"][0][2][0][0] = "A-KIND-B-DOES-NOT-HAVE"
    b = _agent()
    b._reinvent_carried(recs)
    before = _stub(b, {"o0": (5, 1), "o2": (5, 4)})
    s0 = b._spent
    out = b._how_soon("right", before)
    assert out[0] == float("inf") and out[3] == float("inf") and b._spent == s0, (out, b._spent)
    print(f"  B without the kind: reading {out[0]}, no roll (spent {b._spent - s0})")


def check_k4_head_start() -> None:
    b = _agent()
    situ = ("EXTENT", "dodge", (("EXTENT", "orthogonal"),))
    b._rf_carried[("dodge", situ)] = 1
    fired = []
    for _miss in range(4):
        st = b._rf_standing("dodge", situ)
        fired.append(1 + b._rf_in("dodge", situ) + st["paid"] >= st["against"])
        st["against"] += 1                         # a non-arrival, taken close together
    assert fired == [True, True, True, False], fired
    print(f"  carried paid 1: fires before each miss {fired} -- no stop after 2, stop after 3")


def check_k5_freeze() -> None:
    a = _agent()
    a._reflexes["freeze"]["standing"][("GK", "freeze", "up")] = {"paid": 1, "against": 0.0,
                                                                "tick": a.cycle}
    rec = a._reflex_carry()
    assert rec["paid"] == [["freeze", ["GK", "freeze"], 1]], rec
    b = _agent()
    b._reinvent_carried(json.loads(json.dumps([rec])))
    assert b._rf_in("freeze", ("GK", "freeze", "left")) == 1
    b._last_press_key = None
    b._rf_out = {s: v for s, v in b._outstanding.items() if v > 0}
    _act, by = b.choose(b.env.observe())
    rows = [r["detail"] for r in b.led.rows() if r["event"] == "reflex"
            and r["detail"].get("form") == "freeze"]
    assert not rows, rows
    print(f"  freeze carried as {rec['paid'][0][1]}; B with no vote: no freeze read (by={by})")


def check_k6_no_names() -> None:
    a = _agent()
    _plant_a(a)
    _plant_loss(a)
    a._reflexes["freeze"]["standing"][("GK", "freeze", "up")] = {"paid": 1, "against": 0.0,
                                                                "tick": a.cycle}
    rec = a._reflex_carry()
    keys = [k for _f, k, _n in rec["paid"]] + [r for _lk, _fr, r, _n in rec["loss"]]
    flat = re.findall(r'"([^"]*)"', json.dumps(keys))
    acts = set(a.actions)
    bad = [x for x in flat if x in acts or re.fullmatch(r"o\d+(\.\w+)?", x)]
    assert not bad and flat, (bad, keys)
    print(f"  {len(keys)} carried keys, {len(flat)} names: none an action or a board object")


def main() -> int:
    want = sys.argv[1:]
    names = [k for k in globals() if k.startswith("check_") and (not want or k in want)]
    assert not want or len(names) == len(want), ("unknown check name", sorted(want))
    if len(names) == 1:
        globals()[names[0]]()
        print("ok  ", names[0])
        return 0
    bad = []
    for n in names:
        r = subprocess.run([sys.executable, "-B", __file__, n], cwd=str(_repo.ROOT),
                           stdin=subprocess.DEVNULL)
        if r.returncode:
            bad.append(n)
    assert not bad, bad
    print(f"reflex_carry: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
