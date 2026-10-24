"""R-A + R-B, PROGRESS AND THE ROUTE (TETHER_ROUTE_REFUSE, default OFF; WATSON, Isaiah 2026-10-23
19:21 "Approved"; the build design accepted by the reviewer 22:12). Each case runs at the real
sites -- trend_of / shrinking, _goal_choice, _goal_split, _test_row -- on the wired fake agent, ON
and OFF, in its own process; each asserts its occasions and that OFF (today's code) shows the
defect. The interface is a stub that realises the first action offered, so the route is the
agent's and the pick is fixed.
  R-A OWN   a gap held at 6 while the alphabet grows: OFF shrinking, ON not
  RANK      a held gap under a growing alphabet against a gap that truly shrinks: OFF can pick
            the first, ON never does
  CASE 2    wall: "no change" every press. OFF retakes the route past MIN_REPEAT; ON refuses it
            at MIN_REPEAT (route_refused, no_shrink) and takes another
  CASE 7    farther: OFF retakes it; ON refuses after one (route_refused, farther)
  CASE 4    no route: every action reads "no change". OFF still realises one; ON reaches
            route_exhausted and the held hypothesis ends by="routes"
  CASE 3    detour (must not break): a route refused in one contact context is offered again
            once the context changes, ON and OFF
  OFF ID    the current tree with the switch OFF against the last commit without it, through
            conform/identity_mod_rows.compare: 0 differences
  NOT HERE  R-E's delayed effects (a stub, later); R-D's carry across a death (open)
    python tests/test_route_refuse.py
"""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.path.insert(0, os.path.join(str(_repo.ROOT), "conform"))
from identity_mod_rows import compare  # noqa: E402  the one identity reader

sys.dont_write_bytecode = True

STEPS = 12

CASES = r'''
import collections, json, sys
sys.dont_write_bytecode = True
tree, steps = sys.argv[1], int(sys.argv[2])
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import arc_holdout, tether
import interface as IFace
from test_entry import FakeWrapper
env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
for _ in range(steps):
    ag.step()
MR = tether.MIN_REPEAT
out = {"arm": tether._ROUTE_REFUSE, "min_repeat": MR}
ordered = sorted(s for s, t in ag.slot_types.items() if t in tether.ORDERED_TYPES)
out["ordered_slots"] = len(ordered)
a, b = ordered[0], ordered[1]

# R-A OWN: the gap held at 6, the alphabet (R_goal's denominator) growing
gaps, res = [6] * (MR + 1), [6 / (9 + 3 * i) for i in range(MR + 1)]
out["ra_shrinking"] = tether.shrinking(tether.trend_of(res, gaps))

# RANK: a holds its gap while R_goal falls fast; b's gap truly shrinks, R_goal falls slower
ag._hyp = None
ag._res = {a: list(res), b: [(10 - i) / 20 for i in range(MR + 1)]}
ag._gap = {a: list(gaps), b: [10 - i for i in range(MR + 1)]}
out["rank_today_r_goal_shrink"] = [res[0] - res[-1], ag._res[b][0] - ag._res[b][-1]]
out["rank_pick"] = ag._goal_choice()
out["rank_a"], out["rank_b"] = a, b

# THE GOAL EXIT, stubbed above and below the sites under test
sl = a
ag._goal_choice = lambda why=None, book=False: sl
ag._goal_target = lambda s, bf: 20
ag.slot_types[sl] = "POSITION"
ended = []
ag._hyp_end = lambda why, **k: ended.append([why, k.get("by")])
ag.iface.realise = (lambda want, offered, ctx, state=None, env=None,
                    withheld=IFace.NO_WITHHELD, cell=True:
                    IFace.Realisation(offered[0], why="probe: first offered") if offered else None)
CTX = [(("probe", 1),)]
IFace.Interface.context = staticmethod(lambda env, actor=None: CTX[0])


def press(after_of, n):
    taken = []
    for _ in range(n):
        before = {sl: 10}
        act = ag._goal_split(before)
        taken.append(act)
        if act is None or ag._test is None:
            ag._test = None
            continue
        ag.trace.append((act, before, {sl: after_of(10)}))
        ag._test_row()
    return taken


def rows(ev):
    return [r["detail"] for r in ag.led.rows() if r["event"] == ev]


def fresh():
    ag._route_refused, ag._route_run, ag._test = {}, {}, None
    del ended[:]


n_act = len(ag.actions)
fresh()
out["case2"] = press(lambda v: v, MR + 3)
out["case2_refused"] = [r["why"] for r in rows("route_refused")]
fresh()
k0 = len(rows("route_refused"))
out["case7"] = press(lambda v: v - 1, 3)
out["case7_refused"] = [r["why"] for r in rows("route_refused")[k0:]]
fresh()
ag._hyp = {"slots": [sl], "acted": collections.Counter()}
out["case4"] = press(lambda v: v, MR * n_act + 2)
out["case4_exhausted"] = len(rows("route_exhausted"))
out["case4_ended"] = list(ended)
ag._hyp = None
fresh()
first = press(lambda v: v, MR)                  # refused here, in the door's contact context
CTX[0] = (("probe", 2),)                        # the door is gone: a new contact configuration
out["case3"] = [first, press(lambda v: v + 1, 1)]
out["n_actions"] = n_act
print(json.dumps(out, default=str))
'''

PLAIN = r'''
import json, sys
sys.dont_write_bytecode = True
tree, steps = sys.argv[1], int(sys.argv[2])
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import arc_holdout
from test_entry import FakeWrapper
env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
for _ in range(steps):
    ag.step()
print(json.dumps({"rows": ag.led.rows()}, default=str))
'''


def child(script: str, tree: str, arm: str | None, steps: int) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")
    if arm is not None:
        env["TETHER_ROUTE_REFUSE"] = arm
    out = subprocess.run([sys.executable, "-B", "-c", script, tree, str(steps)], env=env,
                         capture_output=True, text=True, timeout=1800, cwd=tree,
                         stdin=subprocess.DEVNULL)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def cases() -> None:
    root = str(_repo.ROOT)
    on, off = child(CASES, root, "1", STEPS), child(CASES, root, "0", STEPS)
    print("  ON :", json.dumps(on, default=str)[:900])
    print("  OFF:", json.dumps(off, default=str)[:900])
    mr, n = on["min_repeat"], on["n_actions"]
    assert on["arm"] is True and off["arm"] is False, "the switch did not reach the module"
    assert on["ordered_slots"] >= 2 and n >= 2, ("occasions: ordered slots / actions", on)
    # R-A OWN
    assert off["ra_shrinking"] is True, "R-A: today's trend should read the held gap as shrinking"
    assert on["ra_shrinking"] is False, "R-A ON: a held raw gap is not progress"
    # RANK
    a, b = on["rank_a"], on["rank_b"]
    assert off["rank_pick"] == a, ("RANK: today's R_goal shrink should outrank", off["rank_pick"])
    assert on["rank_pick"] == b, ("RANK ON: the held gap outranked the shrinking one",
                                  on["rank_pick"])
    # CASE 2, wall
    assert len(set(off["case2"])) == 1 and len(off["case2"]) > mr, ("CASE 2: today repeats",
                                                                   off["case2"])
    assert not off["case2_refused"], "CASE 2 OFF: a route_refused row"
    assert on["case2_refused"][:1] == ["no_shrink"], ("CASE 2 ON: no no_shrink refusal",
                                                     on["case2_refused"])
    assert len(set(on["case2"][:mr])) == 1 and on["case2"][mr] != on["case2"][0], (
        "CASE 2 ON: the refused route was retaken", on["case2"])
    # CASE 7, farther
    assert len(set(off["case7"])) == 1, ("CASE 7: today retakes after farther", off["case7"])
    assert on["case7_refused"][:1] == ["farther"], ("CASE 7 ON: no farther refusal",
                                                   on["case7_refused"])
    assert on["case7"][1] != on["case7"][0], ("CASE 7 ON: retaken after farther", on["case7"])
    # CASE 4, no route here
    assert None not in off["case4"] and not off["case4_ended"], ("CASE 4: today holds on",
                                                                 off["case4"])
    assert on["case4_exhausted"] >= 1 and None in on["case4"], ("CASE 4 ON: no exhaustion",
                                                                on["case4"])
    assert on["case4_ended"][:1] == [["stalled", "routes"]], ("CASE 4 ON: the hypothesis did not "
                                                              "end by routes", on["case4_ended"])
    # CASE 3, detour: the refusal binds only in its own context
    for arm in (on, off):
        first, second = arm["case3"]
        assert second[0] == first[0], ("CASE 3: the direct route was not offered again once the "
                                       "context changed", arm["arm"], arm["case3"])
    print(f"  cases: R-A own, RANK, 2, 7, 4, 3 -- ON and OFF as required (MIN_REPEAT {mr}, "
          f"{n} actions)")


def off_identity() -> None:
    root = str(_repo.ROOT)
    with tempfile.TemporaryDirectory() as d:
        # the tree before R-A/R-B: the last first-parent commit whose tether.py lacks the switch
        rev = next(h for h in subprocess.run(
            ["git", "-C", root, "log", "--first-parent", "--format=%H"], capture_output=True,
            text=True, check=True).stdout.split()
            if "TETHER_ROUTE_REFUSE" not in subprocess.run(
                ["git", "-C", root, "show", f"{h}:tether.py"], capture_output=True,
                text=True, check=True).stdout)
        tar = subprocess.run(["git", "-C", root, "archive", rev], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        base = child(PLAIN, d, None, 30)["rows"]
    cur = child(PLAIN, root, None, 30)["rows"]
    for rows in (base, cur):        # the arm lists differ by the switch itself
        for r in rows:
            if r["slot"] == "@run" and r["event"] == "arms":
                r["detail"].pop("on", None)
                r["detail"].pop("off", None)
    bad = compare(base, cur, set())
    print(f"  OFF identity against {rev[:12]}: {len(base)} base rows, {len(cur)} current, "
          f"{len(bad)} difference(s)" + "".join(f"\n    {x}" for x in bad))
    assert len(base) > 50 and not bad, ("OFF identity", len(bad))
    assert not any(r["event"] in ("route_refused", "route_exhausted") for r in cur), "OFF rows"


if __name__ == "__main__":
    cases()
    off_identity()
    print("route_refuse: OK")
