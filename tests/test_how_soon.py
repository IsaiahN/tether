"""23 THE HOW-SOON READING (TETHER_HOW_SOON, default ON; the reviewer 2026-11-05 r1245, r1246).
gridworld default seed 0, the agent seed pinned, 6 steps, then a planted read over a synthetic
state; the death record, the subject, the settled standing and the one-press predictor are
planted (the predictor is the settled model's, stubbed here so the arithmetic is the reading's).
Each check its own process; TETHER_HOW_SOON=0 in the environment turns every check red.
  check_h0_context     contact_points_at(observe()) == contact_points(), gridworld and the fake
                       ARC board; context == context_of(contact_points())
  check_h1_none_inf    no death record: inf, no evaluation spent; an unsettled slot: None
  check_h2_reading     a death record (hazard kind, orthogonal) and a mover 3 cells off: 2
  check_h3_dodge       ON by="reflex" (dodge) takes the furthest offer; OFF no dodge (H3);
                       every offer finite, one strictly further: taken (H3b); none further: no
                       fire and the row (H3c)
  check_h4_mint        ON the predictor kind heads the queue for the hazard slot, finite (H4)
                       and None (H4b); OFF the existing order
  check_h5_witness     non-arrival by j+w: against (H5a); a death at j+1, w 1: paid (H5b); a
                       death at 40 with j 2, w 0: against (H5c); the course broken: no verdict
  check_h6_no_identity no game id and no family name at the reading's sites (AST)
    python tests/test_how_soon.py [check ...]
"""
from __future__ import annotations

import subprocess
import sys
from collections import Counter

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
MOVE = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}


def _agent():
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    assert tether._HOW_SOON, "TETHER_HOW_SOON is OFF: no how-soon reading"
    tether._AGENT_SEED = False
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    for _ in range(6):
        ag.step()
    return ag


def _plant(ag, at: dict, settled: bool = True) -> tuple:
    """o0 the subject at `at["o0"]`, the others where `at` puts them (far by default); one death
    record on (the hazard kind, orthogonal), terminal frame; every slot settled (or not)."""
    import tether
    before = dict(ag.env.observe())
    for i in range(6):
        r, c = at.get(f"o{i}", (100 + 10 * i, 100 + 10 * i))
        before[f"o{i}.row"], before[f"o{i}.col"] = r, c
    hk = ag._kind_str("o2")
    k = ("planted", "right", ())
    ag._death_n[k] = 1
    ag._loss_rel = {k: Counter({("death", "terminal", ((hk, "orthogonal"),)): 1})}
    ag._hs_subject = lambda: {"o0"}
    ag._hs_open, ag._hs_read = [], None
    ag._spent = tether.STEP_BUDGET - 20000
    ag.gamma.is_settled = (lambda _n, _s: True) if settled else (lambda _n, _s: False)
    for s in before:
        ag.bound.setdefault(s, tether.IDN)

    def step(st, action, preds, _unread, used, _coord=None):
        out = dict(st)
        used[0] += len(preds)
        dr, dc = MOVE.get(action, (0, 0))
        out["o0.row"], out["o0.col"] = st["o0.row"] + dr, st["o0.col"] + dc
        return out
    ag._la_predict = step
    ag._rf_out = {s: v for s, v in ag._outstanding.items() if v > 0}
    ag._last_press_key, ag._rf_pending = None, []
    return before, (hk, "orthogonal")


def check_h0_context() -> None:
    import arc_holdout
    import interface as IFace
    from test_entry import FakeWrapper
    ag = _agent()
    env = ag.env
    assert env.contact_points_at(env.observe()) == env.contact_points()
    assert IFace.Interface.context(env) == IFace.Interface.context_of(env.contact_points())
    aenv = arc_holdout.wire(FakeWrapper(script={}), "fake")[0]
    aenv.observe()
    n = len(aenv._decompose.tracked)
    assert aenv.contact_points_at(aenv.observe()) == aenv.contact_points()
    print(f"  gridworld: {len(env.contact_points())} contacts equal; fake ARC: "
          f"{n} tracked, {len(aenv.contact_points())} contacts equal")


def check_h1_none_inf() -> None:
    import math

    import tether
    ag = _agent()
    before = dict(ag.env.observe())
    s0 = ag._spent
    assert ag._how_soon("right", before) == (math.inf, 0, None, math.inf) and ag._spent == s0
    before, _rel = _plant(ag, {"o0": (5, 1), "o2": (5, 4)}, settled=False)
    j, _w, _r, _h = ag._how_soon("right", before)
    assert j is None, j
    before, _rel = _plant(ag, {"o0": (5, 1), "o2": (5, 4)})
    ag._spent = tether.STEP_BUDGET - 1             # a purse too small for one press
    j0, _w, _r, h0 = ag._how_soon("up", before)
    assert j0 is None and h0 == 0, (j0, h0)
    print(f"  no death record: inf, 0 evaluations spent; unsettled: {j}; nothing rolled "
          f"(purse < one press): {j0}")


def check_h2_reading() -> None:
    ag = _agent()
    before, rel = _plant(ag, {"o0": (5, 1), "o2": (5, 4)})
    j, w, met, _h = ag._how_soon("right", before)
    assert j == 2 and met == (rel,), (j, met)
    print(f"  hazard 3 cells off on the course: reading {j}, lag {w}, met {met}")


def _choose(ag, before):
    ag.env.observe = lambda: dict(before)
    return ag.choose(before)


def check_h3_dodge() -> None:
    ag = _agent()
    before, _rel = _plant(ag, {"o0": (5, 1), "o2": (5, 4)})
    ag._last_action = "right"
    act, by = _choose(ag, before)
    row = [r["detail"] for r in ag.led.rows() if r["event"] == "reflex"][-1]
    assert by == "reflex" and row["form"] == "dodge" and act == "down", (by, act, row)
    # H3b: every offer finite, one strictly further (left, up, down: 3; right: 2) -> down
    ag = _agent()
    before, _rel = _plant(ag, {"o0": (10, 10), "o2": (10, 13), "o3": (10, 6), "o4": (6, 10),
                               "o5": (14, 10)})
    ag._last_action = "right"
    reads = {a: ag._how_soon(a, before)[0] for a in ("down", "left", "right", "up")}
    act_b, by_b = _choose(ag, before)
    assert reads == {"down": 3, "left": 3, "right": 2, "up": 3} and (by_b, act_b) == (
        "reflex", "down"), (reads, by_b, act_b)
    # H3c: none further (all four at 2) -> no fire, the row
    ag = _agent()
    before, _rel = _plant(ag, {"o0": (10, 10), "o2": (10, 13), "o3": (10, 7), "o4": (7, 10),
                               "o5": (13, 10)})
    ag._last_action = "right"
    _act_c, by_c = _choose(ag, before)
    rows = [r["detail"] for r in ag.led.rows() if r["event"] == "reflex"
            and r["detail"].get("form") == "dodge"]
    assert by_c != "reflex" and rows[-1]["reads"] == "no offer further than the course", (
        by_c, rows[-1:])
    print(f"  ON dodge took {act}; H3b readings {reads}, took {act_b}; H3c by={by_c}, "
          f"row '{rows[-1]['reads']}'")


def check_h3_off() -> None:
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    tether._AGENT_SEED, tether._HOW_SOON = False, False      # MUST-FAIL: the arm off
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    for _ in range(6):
        ag.step()
    assert "dodge" not in ag._reflexes
    before, _rel = _plant(ag, {"o0": (5, 1), "o2": (5, 4)})
    ag._last_action = "right"
    _act, _by = _choose(ag, before)
    assert not any(r["event"] == "reflex" and r["detail"].get("form") == "dodge"
                   for r in ag.led.rows())
    print("  OFF: no dodge form, no dodge row")


def check_h4_mint() -> None:
    import tether
    ag = _agent()
    before, _rel = _plant(ag, {"o0": (5, 1), "o2": (5, 4)})
    ag._last_action = "right"
    ag.env.observe = lambda: dict(before)
    by_kind = {"objective": (1.0, 0, 1.0, "obj"), "predictor": (2.0, 0, 2.0, "pred")}
    head = ag._rank_by_consequence(by_kind, by_kind["objective"], "o2.col")[0]
    assert head == by_kind["predictor"], head
    ag2 = _agent()                                   # H4b: unsettled -> None -> still urgent
    before2, _rel = _plant(ag2, {"o0": (5, 1), "o2": (5, 4)}, settled=False)
    ag2._last_action = "right"
    ag2.env.observe = lambda: dict(before2)
    assert ag2._hs_course(before2)[1] is None
    head_b = ag2._rank_by_consequence(by_kind, by_kind["objective"], "o2.col")[0]
    assert head_b == by_kind["predictor"], head_b
    tether._HOW_SOON = False                         # MUST-FAIL: the existing order
    head_off = ag._rank_by_consequence(by_kind, by_kind["objective"], "o2.col")[0]
    assert head_off == by_kind["objective"], head_off
    print(f"  ON finite: head {head[3]}; ON None: head {head_b[3]}; OFF: head {head_off[3]}")


def check_h5_witness() -> None:
    ag = _agent()
    situ = ("k", "dodge", (("h", "orthogonal"),))

    def run(j, w, n, alive, last="right"):
        st = ag._rf_standing("dodge", situ)
        st["paid"], st["against"] = 0, 0.0
        ag._hs_open = [{"situ": situ, "course": "right", "j": j, "w": w, "n0": ag._act_n()}]
        ag._acts["right"] = ag._acts.get("right", 0) + n
        ag._alive, ag._last_action = alive, last
        ag._hs_settle()
        ag._alive = True
        v = [r["detail"] for r in ag.led.rows() if r["event"] == "how_soon_settled"][-1]
        return v["verdict"], st["paid"], round(st["against"], 3)
    a = run(2, 0, 2, True)
    b = run(2, 1, 3, False)
    c = run(2, 0, 40, False)
    d = run(2, 0, 1, True, last="left")
    assert a == ("against", 0, 1.0) and b == ("paid", 1, 0.0), (a, b)
    assert c == ("against", 0, 1.0), c
    assert d == ("course not kept", 0, 0.0), d
    print(f"  H5a {a}; H5b {b}; H5c {c}; broken {d}")


def check_h6_no_identity() -> None:
    import ast
    import inspect

    import tether
    fams = set(tether._DESC_SEED) | set(tether._DESC_SEED.values())
    fs = (tether.Agent._how_soon, tether.Agent._hs_course, tether.Agent._hs_settle,
          tether.Agent._hs_rel, tether.Agent._hs_fatal, tether.Agent._hs_subject,
          tether.Agent._urgent)
    for f in fs:
        tree = ast.parse(inspect.cleandoc("\n" + inspect.getsource(f)))
        for n in ast.walk(tree):
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                assert n.value not in fams, (f.__name__, n.value)
            name = n.attr if isinstance(n, ast.Attribute) else getattr(n, "id", "")
            assert "game" not in name.lower(), (f.__name__, name)
    print(f"  {len(fs)} sites: no game id, none of {len(fams)} family names")


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
    print(f"how_soon: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
