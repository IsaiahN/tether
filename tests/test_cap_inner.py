"""C1 (A), THE OVERRUN SAFETY NET (TETHER_CAP_INNER, TETHER_END_RESERVE; Isaiah 2026-10-22
12:36-12:37;
the reviewer 12:37, 15:17, 15:24, 15:34, 15:40). The fake ARC game (test_entry.FakeWrapper).

  PH   per phase family (12, P0-P15): the deadline passed as a phase is entered (its entry set
       cap.AT past) ends the step at the next growing loop's head: one "@cap" "cap_mid_step" row
       with a site, acted False before the press and True after; ag._cut set (MF: the same hook
       with TETHER_CAP_INNER off writes no such row, the step runs to its end)
  AC   after a cut no step runs: step() returns False with one "after_cut" row and changes nothing
  SW   the swallow: interface._is_relational's "except Exception" swallows an Exception-based cut
       (the hazard, shown) and lets cap.CapReached (a BaseException) through
  DA   diagnose atomicity: a cut inside one diagnosis (in hazard.credited) through __wrapped__ (the
       hold off) leaves the hazard record a MIX; held, no cut lands inside and the record is whole;
       a deadline passed before the unit cuts at its entry and leaves the record as it was
  RG   the ruin-key gap (15:40): perceive is held with NO entry head (cap.holding), so no cut lands
       between step's _ruin_step key and the press (MF: cap.held's code is not perceive's)
  H1   item 1: a cut inside the goal-hypothesis proposal writes the goal_hypotheses row with pick
       None, capped and "unreached at this budget", and never sets _hyp_exhausted
  RS   the reserve: the store keeps the end path's wall (meta) and reads it back; an agent whose
       deadline less its reserve has passed stops before thinking, one "stopped_for_end_path" row;
       a boundary write never lowers the reserve (MF: TETHER_END_RESERVE off, the agent steps)
  ID   identity: no deadline, ON vs OFF (both arms off): the ledgers equal (the heads are inert)
  ES   e4_stream sets no deadline (the reviewer 15:24: none to be added), so no head fires there

    python tests/test_cap_inner.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
HERE = _repo.ROOT
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "conform"))
from identity_mod_rows import compare  # noqa: E402  the one identity reader

# one always-reached entry per phase family (the census's phases); hooked to pass the deadline
PHASES = [("P0", "_size_fold", 8), ("P1", "_present", 8), ("P2", "note_goals", 8),
          ("P5", "choose", 8), ("P6", "_utter", 8), ("P7", "route", 8), ("P8", "_d5_splits", 8),
          ("P10", "_event_prices", 8), ("P11", "_flush_probe", 24), ("P12", "settle", 8),
          ("P14", "_settle_routine", 8), ("P15", "indistinguishable", 8)]
PRESSED_FROM = {"P7", "P8", "P10", "P11", "P12", "P14", "P15"}


def env_for(**arms) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0", **arms)
    return env


def run_child(code: str, *args: str, **arms) -> object:
    p = subprocess.run([sys.executable, "-B", "-c", code, HERE, *args], capture_output=True,
                       text=True, env=env_for(**arms), cwd=HERE, stdin=subprocess.DEVNULL,
                       timeout=600)
    assert p.returncode == 0, p.stderr[-2000:]
    return json.loads(p.stdout.strip().splitlines()[-1])


PH_CHILD = r'''
import json, os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
sys.path.insert(1, os.path.join(sys.argv[1], "tests"))
import arc_holdout, cap, tether
from test_entry import FakeWrapper
tether._AGENT_SEED = False
env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake")
fn = sys.argv[2]
fired = []
real = getattr(tether.Agent, fn)
def hooked(self, *a, **k):
    if not fired:
        fired.append(self.cycle)
        cap.AT = 0.0
    return real(self, *a, **k)
setattr(tether.Agent, fn, hooked)
out = None
for _ in range(int(sys.argv[3])):
    n0 = len(ag.led)
    env.observe()
    acted = ag.step()
    if fired:
        rows = ag.led.rows()[n0:]
        out = {"fired": fired[0], "acted": acted, "cut": ag._cut,
               "ruin_on": tether._RUIN_RECORD, "ruin": repr(ag._ruin_step),
               "caps": [dict(e["detail"], event=e["event"]) for e in rows
                        if e["slot"] == "@cap" and e["event"] == "cap_mid_step"]}
        if ag._cut:
            n1, c1, lib1 = len(ag.led), ag.cycle, len(ag.gamma.library)
            again = ag.step()
            out["after"] = {"returned": again, "rows": [e["event"] for e in ag.led.rows()[n1:]],
                            "cycle_same": ag.cycle == c1, "lib_same": len(ag.gamma.library) == lib1}
        break
print(json.dumps(out))
'''


def phases() -> None:
    for ph, fn, n in PHASES:
        r = run_child(PH_CHILD, fn, str(n))
        assert r is not None, f"PH {ph}: precondition: {fn} was never entered in {n} steps"
        assert r["cut"] and len(r["caps"]) == 1, (ph, fn, r)
        c = r["caps"][0]
        if "site" in c:       # step's catch
            assert c["site"] and c["reads"].startswith("unreached at this budget"), (ph, c)
        else:                 # route's own catch (its rows kept, 15:34): _cap_end's row
            assert c["at"] in ("route", "mint", "tail"), (ph, c)
            c["site"] = f"_cap_end {c['at']}"
        assert c["acted"] == (ph in PRESSED_FROM), (ph, "acted", c)
        if c["acted"] and r["ruin_on"]:      # RS-15:40: a cut after the press keeps the press's key
            assert r["ruin"] != "None", (ph, "ruin-step: the press's key is lost", r)
        a = r["after"]
        assert a["returned"] is False and a["rows"] == ["after_cut"], (ph, "AC", a)
        assert a["cycle_same"] and a["lib_same"], (ph, "AC", a)
        ruin = f"; ruin key kept {r['ruin'][:40]}" if c["acted"] else ""
        print(f"  PH {ph} {fn}: cut at {c['site']} (at {c['at']}, acted {c['acted']}); AC ok{ruin}")
    r = run_child(PH_CHILD, "note_goals", "8", TETHER_CAP_INNER="0")
    assert r is not None and not r["cut"] and not r["caps"], ("MF-PH", r)
    print("  MF-PH TETHER_CAP_INNER off: the hooked step ran to its end, no cut row")


def swallow() -> None:
    import cap
    import interface

    class OldCut(Exception):
        """the old base, an Exception"""

    class Env:
        def __init__(self, exc):
            self.exc = exc

        def relational_slots(self):
            raise self.exc

    assert interface._is_relational("o1.dist_o2", Env(OldCut())) is False   # swallowed: hazard
    try:
        interface._is_relational("o1.dist_o2", Env(cap.CapReached()))
    except cap.CapReached:
        print("  SW an Exception cut is swallowed at interface:214; CapReached passes through")
        return
    raise AssertionError("SW: CapReached was swallowed")


def atomic() -> None:
    import cap
    import diagnose
    rows = [(0, {"o1.x": 1}, "A", {"o1.x": 1}, None, None),
            (1, {"o1.x": 1}, "A", {"o1.x": 2}, None, None),
            (2, {"o1.x": 2}, "A", {"o1.x": 3}, None, None)]

    def state(hz):
        return json.dumps([hz.near, hz.away, hz.world], sort_keys=True, default=dict)

    def run(fn, at_entry):
        hz = diagnose.Hazard()
        real = hz.credited

        def credited(a, m):
            cap.head()                    # a callee reaching a head, as _left does in play
            return real(a, m)

        def predicts(r):
            cap.AT = 0.0                  # the deadline passes inside the diagnosis
            return r[0] == 0
        hz.credited = credited
        before = state(hz)
        cap.AT = 0.0 if at_entry else None
        try:
            fn(rows, "o1.x", "o1", persists=True, predicts=predicts,
               predicts_with=lambda _r, _a: False, alt_predicts=lambda _r: False,
               changed_of=lambda _i: {"o2"}, touching_now=set(), kind="k", kind_of=lambda c: c,
               moved_to=lambda _v: None, hazard=hz, min_repeat=2)
            cut = False
        except cap.CapReached:
            cut = True
        finally:
            cap.AT = None
        return cut, before, state(hz), hz

    cut, _b, a, hz = run(diagnose._diagnose.__wrapped__, False)       # the hold off
    assert cut and hz.near and not hz.world["spot"], ("MF-DA: the mix was not produced", a)
    print("  MF-DA hold off: a cut inside the diagnosis split the record (near counted, world "
          "not): a mix")
    cut, _b, a, hz = run(diagnose._diagnose, False)                   # held
    assert not cut and hz.near and hz.world["spot"], ("DA", cut, a)
    cut, b, a, hz = run(diagnose._diagnose, True)                     # passed before the unit
    assert cut and a == b, ("DA entry", cut, a)
    print("  DA held: inside, no cut and the record whole; passed at entry, cut before the unit "
          "and the record as it was")


def ruin_gap() -> None:
    import cap
    import tether
    hold_code = cap.holding(lambda: None).__code__
    held_code = cap.held(lambda: None).__code__
    assert tether.Agent.perceive.__code__ is hold_code, "RG: perceive is not held by cap.holding"
    assert held_code is not hold_code, "MF-RG: cap.held and cap.holding are not told apart"
    print("  RG perceive: cap.holding (no entry head); MF-RG: cap.held is a different code")


H1_CHILD = r'''
import json, os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
sys.path.insert(1, os.path.join(sys.argv[1], "tests"))
import arc_holdout, cap, tether
from test_entry import FakeWrapper
tether._AGENT_SEED = False
env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake")
real = tether.Agent._hyp_propose_body
def hooked(self, before):
    cap.AT = 0.0
    return real(self, before)
tether.Agent._hyp_propose_body = hooked
out = None
for _ in range(12):
    n0 = len(ag.led)
    env.observe()
    ag.step()
    if ag._cut:
        out = {"rows": [e["detail"] for e in ag.led.rows()[n0:] if e["event"] == "goal_hypotheses"],
               "exhausted": ag._hyp_exhausted}
        break
print(json.dumps(out))
'''


def item1() -> None:
    r = run_child(H1_CHILD)
    assert r is not None, "H1: precondition: the proposal was never entered in 12 steps"
    capped = [d for d in r["rows"] if d.get("capped")]
    assert len(capped) == 1 and capped[0]["pick"] is None, r
    assert capped[0]["why"] == "unreached at this budget", capped[0]
    assert r["exhausted"] is None, ("H1: _hyp_exhausted was set", r)
    print(f"  H1 the proposal cut: goal_hypotheses capped {capped[0]['capped']}; not exhausted")


RS_CHILD = r'''
import json, os, sys, time
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
sys.path.insert(1, os.path.join(sys.argv[1], "tests"))
import arc_holdout, tether
from test_entry import FakeWrapper
tether._AGENT_SEED = False
env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake")
ag.deadline, ag._end_reserve, ag._end_sleep_s = time.time() + 100.0, 200.0, 5.0
env.observe()
acted = ag.step()
ev = [e["event"] for e in ag.led.rows() if e["slot"] == "@cap"]
ag._note_boundary_wall(1.0)
low = ag._end_reserve
ag._note_boundary_wall(300.0)
print(json.dumps({"acted": acted, "cut": ag._cut, "caps": ev, "low": low, "high": ag._end_reserve}))
'''


def reserve() -> None:
    import lineage_store as ls
    con = ls.open_store(tempfile.mkdtemp())
    try:
        assert ls.read_end_path(con) is None
        ls.note_end_path(con, 34.6, 9.5)
        assert ls.read_end_path(con) == {"s": 34.6, "sleep_s": 9.5}
    finally:
        con.close()
    r = run_child(RS_CHILD)
    assert r["acted"] is False and r["cut"] and r["caps"] == ["stopped_for_end_path"], r
    assert r["low"] == 200.0 and r["high"] == 305.0, r
    print("  RS the store keeps and returns the wall; deadline - reserve passed: the agent stopped "
          "before thinking; a boundary never lowers the reserve (1+5 < 200; 300+5)")
    r = run_child(RS_CHILD, TETHER_END_RESERVE="0")
    assert not r["cut"] and "stopped_for_end_path" not in r["caps"], ("MF-RS", r)
    print("  MF-RS TETHER_END_RESERVE off: the same agent stepped")


ID_CHILD = r'''
import json, os, sys, tempfile
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
sys.path.insert(1, os.path.join(sys.argv[1], "tests"))
import tether, tether_agent
from test_entry import FakeWrapper
tether._AGENT_SEED = False
led = os.path.join(tempfile.mkdtemp(), "r.jsonl")
tether_agent.run(FakeWrapper(script={}), "fake", max_actions=10, led_path=led)
print(json.dumps(led))
'''


def identity() -> None:
    out = []
    for arms in ({}, {"TETHER_CAP_INNER": "0", "TETHER_END_RESERVE": "0"}):
        led = run_child(ID_CHILD, **arms)
        with open(led, encoding="utf-8") as fh:
            rows = [json.loads(x) for x in fh if x.strip()]
        for r in rows:      # the arm lists differ by the check switches themselves
            if r["slot"] == "@run" and r["event"] == "arms":
                r["detail"].pop("on", None)
                r["detail"].pop("off", None)
        out.append(rows)
    assert len(out[0]) > 50, ("ID: precondition: too few rows to compare", len(out[0]))
    bad = compare(out[1], out[0], set())      # base OFF, new ON
    assert not bad, ("ID", bad[:5])
    print(f"  ID no deadline: ON and OFF ledgers equal ({len(out[0])} rows)")


def e4_stream() -> None:
    with open(os.path.join(HERE, "harness", "mem_store", "e4_stream.py"), encoding="utf-8") as fh:
        src = fh.read()
    assert "deadline" not in src, "ES: e4_stream now sets a deadline (15:24: none to be added)"
    print("  ES e4_stream sets no deadline: no head fires across its slices")


def main() -> int:
    swallow()
    atomic()
    ruin_gap()
    reserve()
    item1()
    phases()
    identity()
    e4_stream()
    print("cap inner: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
