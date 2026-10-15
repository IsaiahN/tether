"""C-DECAY-1, the decay class S1, S2, S5, S11 (Isaiah 2026-10-15 15:54; the reviewer 16:18,
18:13 D1-D4).

  RD-1  the captured stranded birth (scratchpad DRESET/birth_1.jsonl, seed d2f79069488af4c3),
        replayed by its record, presses RESET after its death and is not stranded;
        precondition: the same replay with the four arms OFF strands, so RD-1 can fail
  RD-2  fresh births (each its own seed) on test_entry's death game, as many as fit the budget, the
        number stated: none is stranded; per birth, the presses between the death and RESET
  RD-3  no term loses standing (the reviewer 16:10): at the death of the RD-1 replay the standings
        are identical ON and OFF, and situate() changes no Gamma field
  D1    the record only grows: across every situate() no by_ctx, "to", ep, to_ep, clicked or
        clicked_at count falls
  RD-4  MUST-FAIL, a planted fault inside S1, the arm still ON: a press other than the restart
        read on a dead board as it would be alive, AND a dead press priced into the restart
        (either alone still resets; both counted executing); RD-1 strands again.
        Measured: S1 alone frees this birth
        (S1 off alone strands; S1 alone on resets), so S2, S5 and S11 are checked directly:
  S2    an observation stamped in an earlier epoch: a no-effect lapses (unknown), a change
        carries, a destination lapses (reach 1); within an epoch the latest decides; OFF
        reads the old no-effect (the control)
  S5    a reach verdict's key carries alive
  S11   a coordinate clicked in an earlier epoch excludes nothing; within the epoch the
        unclicked object comes first

    python test_decay.py [record]
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time

sys.dont_write_bytecode = True

RECORD = (r"C:\Users\Admin\AppData\Local\Temp\claude\c--Users-Admin-Documents-GitHub-tether"
          r"\2043231f-437e-4548-ac19-702f1efcfb71\scratchpad\DRESET\birth_1.jsonl")
ARMS = ("TETHER_DEAD_PRICE", "TETHER_SITUATED_EFFECT", "TETHER_SITUATED_REACH",
        "TETHER_SITUATED_CLICK")
RD2_BUDGET_S = 190   # a test's wall bound (the reviewer: every test under 5 minutes), never a prior

CHILD = """
import json, sys, time
sys.dont_write_bytecode = True
from arcengine import GameState
import interface, tether, tether_agent
from test_entry import FakeWrapper
plant, births, budget = {plant}, {births}, {budget}
PLANTED = {{"n": 0}}
if plant:
    # the dead board's reach rule removed alone: a press other than the restart is read as it
    # would be alive; the rest of S1 kept. PLANTED counts the calls it changed
    real_reach = interface.Interface.reach
    def live(self, a, ctx, offered):
        if self.alive or a == interface.RESET:
            return real_reach(self, a, ctx, offered)
        PLANTED["n"] += 1
        self.alive = True
        try:
            return real_reach(self, a, ctx, offered)
        finally:
            self.alive = False
    interface.Interface.reach = live
    # and a press on a dead board adds to the restart's price again. Either half alone still
    # resets this birth (measured): unpriced, RESET is cheapest; under the dead reach rule it
    # is the only press that reaches. The fault is both together, with the arm still ON
    dead = {{"n": 0}}
    real_step, real_ck = tether.Agent.step, tether.Agent._choose_known
    def step(self, *a, **k):
        was = self._alive
        got = real_step(self, *a, **k)
        dead["n"] = 0 if self._alive else dead["n"] + (not was and bool(got))
        return got
    def ck(self, known):
        keep = self._attempt_actions
        self._attempt_actions += dead["n"]
        PLANTED["priced"] = PLANTED.get("priced", 0) + (dead["n"] > 0)
        try:
            return real_ck(self, known)
        finally:
            self._attempt_actions = keep
    tether.Agent.step, tether.Agent._choose_known = step, ck
grows, shrunk, gamma_moved = [], [], []
def counts(i):
    t = i.table.values()
    return [sum(len(v) for e in t for v in e.get("by_ctx", {{}}).values()),
            sum(len(v) for e in t for v in e.get("to", {{}}).values()),
            sum(len(v) for e in t for v in e.get("ep", {{}}).values()),
            sum(len(s) for e in t for v in e.get("to_ep", {{}}).values() for s in v.values()),
            len(i.clicked), len(getattr(i, "clicked_at", {{}}))]
AG = {{}}
def gdig(g):
    return repr((sorted((k, repr(v)) for k, v in g.standing.items()), sorted(g.library),
                 sorted((k, repr(v)) for k, v in g.stamps.items())))
real_sit = interface.Interface.situate
def sit(self, epoch, alive):
    c = counts(self)
    if grows and any(a < b for a, b in zip(c, grows[-1])):
        shrunk.append([grows[-1], c])
    grows.append(c)
    ag = AG.get("ag")
    before = gdig(ag.gamma) if ag is not None else None
    real_sit(self, epoch, alive)
    if ag is not None and gdig(ag.gamma) != before:
        gamma_moved.append(epoch)
interface.Interface.situate = sit
real_rt = tether.Agent.retarget
std = {{}}
def rt(self, env, level, how=tether.ADVANCE):
    AG["ag"] = self
    if how == "death" and "at_death" not in std:
        std["at_death"] = sorted((k, repr(v)) for k, v in self.gamma.standing.items())
    return real_rt(self, env, level, how)
tether.Agent.retarget = rt
out = []
t0 = time.perf_counter()
for b in range(births):
    if b and time.perf_counter() - t0 > budget:
        break
    w = FakeWrapper(script={{2: GameState.GAME_OVER}})
    r = tether_agent.run(w, "fake", max_actions=8)
    acts = [c for c in w.calls[1:]]
    k = [i for i, c in enumerate(acts) if c != "RESET"]
    death_at = k[1] if len(k) > 1 else None
    after = acts[death_at + 1:] if death_at is not None else []
    before_reset = next((i for i, c in enumerate(after) if c == "RESET"), None)
    out.append({{"end": r["end"], "deaths": r["deaths"], "resets": r["agent_resets"],
                 "presses_before_reset": before_reset if before_reset is not None else len(after),
                 "calls": w.calls}})
c = counts(AG["ag"].iface) if AG.get("ag") else None
print("OUT " + json.dumps({{"births": out, "shrunk": shrunk, "situates": len(grows),
                            "gamma_moved": gamma_moved, "planted": PLANTED["n"],
                            "priced": PLANTED.get("priced", 0), "std": std.get("at_death"),
                            "last": c,
                            "seed_source": AG["ag"].seed_source if AG.get("ag") else None}},
                          default=repr))
"""


def _child(env_add: dict, plant: bool = False, births: int = 1, budget: float = 0) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(env_add)
    r = subprocess.run([sys.executable, "-B", "-c",
                        CHILD.format(plant=plant, births=births, budget=budget)], env=env,
                       capture_output=True, text=True, check=False, stdin=subprocess.DEVNULL)
    assert r.returncode == 0, r.stderr[-3000:]
    out = [ln for ln in r.stdout.splitlines() if ln.startswith("OUT ")]
    return json.loads(out[-1][4:])


def direct() -> None:
    """S2, S5 and S11 on an interface and a key, in process."""
    from types import SimpleNamespace

    import interface
    import tether
    i = interface.Interface()
    mv = (("o0.row", 1),)
    i.table = {"A": {"by_ctx": {"c": {()}}, "ep": {"c": [(0, ())]},
                     "to": {"c": {"d"}}, "to_ep": {"c": {"d": {0}}}},
               "B": {"by_ctx": {"c": {mv}, "d": {()}},
                     "ep": {"c": [(0, mv)], "d": [(0, ())]}},
               "C": {"by_ctx": {"c": {mv, ()}}, "ep": {"c": [(0, mv), (0, ())]}}}
    assert i._known_now("A", "c") == interface.NO_EFFECT
    assert i._known_now("C", "c") == interface.NO_EFFECT, "S2: within an epoch the latest decides"
    assert i.reach("A", "c", ("B",)) == 0
    i.situate(1, True)
    assert i._known_now("A", "c") is None, "S2: an earlier no-effect did not lapse"
    assert i._known_now("B", "c") == interface.CHANGES, "S2: an earlier change did not carry"
    assert i.reach("A", "c", ("B",)) == 1, "S2: an earlier destination did not lapse"
    interface._SITUATED_EFFECT = False
    try:
        assert i._known_now("A", "c") == interface.NO_EFFECT, "S2 control: OFF reads the old"
    finally:
        interface._SITUATED_EFFECT = True
    print("  S2 a no-effect and a destination from an earlier epoch lapse, a change carries,"
          " the latest decides within one; OFF reads the old no-effect")
    k = tether.Agent._reach_key(SimpleNamespace(_alive=False), ("slot",))
    assert tether._SITUATED_REACH and k == (("slot",), False), ("S5", k)
    print("  S5 a reach verdict watched dead is filed apart from one watched alive")
    st = {"o1.row": 5, "o1.col": 6, "o2.row": 7, "o2.col": 8}
    i.situate(2, True)
    i.clicked.add((6, 5))
    i.clicked_at[(2, (6, 5))] = 1
    assert i._unclicked(st, ()) == (8, 7), "S11: the unclicked object is not first"
    i.situate(3, True)
    assert i._unclicked(st, ()) == (6, 5), "S11: an earlier epoch's click still excludes"
    print("  S11 within an epoch the unclicked object comes first; a new epoch excludes nothing")


def main() -> None:
    rec = sys.argv[1] if len(sys.argv) > 1 else RECORD
    assert os.path.exists(rec), f"the captured record is missing: {rec}"
    replay = {"TETHER_SEED_FROM": rec}
    t0 = time.perf_counter()
    off = _child(replay | dict.fromkeys(ARMS, "0"))
    on = _child(replay)
    b_off, b_on = off["births"][0], on["births"][0]
    print(f"  replay ({on['seed_source']}): OFF end {b_off['end']} resets {b_off['resets']};"
          f" ON end {b_on['end']} resets {b_on['resets']},"
          f" presses before RESET {b_on['presses_before_reset']}")
    assert b_off["deaths"] == 1 and b_off["end"] == "death", (
        "RD-1 precondition: the replay with the arms OFF does not strand", b_off)
    assert b_on["deaths"] == 1 and b_on["resets"] >= 1 and b_on["end"] != "death", (
        "RD-1: the replay strands with the arms ON", b_on)
    print("  RD-1 the captured birth presses RESET after its death (OFF strands)")
    assert on["std"] is not None and on["std"] == off["std"], "RD-3: standings differ at the death"
    assert not on["gamma_moved"], ("RD-3: situate() moved a Gamma field", on["gamma_moved"])
    print(f"  RD-3 {len(on['std'])} standings identical ON and OFF at the death; situate() moved"
          f" no Gamma field over {on['situates']} calls")
    assert on["situates"] >= 2 and not on["shrunk"], ("D1: a record count fell", on["shrunk"])
    print(f"  D1 no record count fell across {on['situates']} situate() calls; last {on['last']}")
    bad = _child(replay, plant=True)
    b_bad = bad["births"][0]
    assert bad["planted"] > 0 and bad["priced"] > 0, ("RD-4: the planted fault never executed",
                                                      bad["planted"], bad["priced"])
    assert b_bad["end"] == "death", ("RD-4 MUST-FAIL did not fail: the dead reach rule removed,"
                                     " still resets", b_bad)
    print(f"  RD-4 must-fail fired: the dead board read as live ({bad['planted']} reads) and"
          f" dead presses priced ({bad['priced']} picks) strand the replay again")
    direct()
    left = 300 - (time.perf_counter() - t0) - 30
    fresh = _child({}, births=40, budget=min(RD2_BUDGET_S, max(left, 0)))
    n = len(fresh["births"])
    stranded = [b for b in fresh["births"] if b["end"] == "death"]
    print(f"  RD-2 {n} fresh births: stranded {len(stranded)}; presses between the death and RESET"
          f" {[b['presses_before_reset'] for b in fresh['births']]}")
    assert n >= 1 and not stranded, ("RD-2: a fresh birth acted into a dead game", stranded[:1])
    print(f"decay: OK ({time.perf_counter() - t0:.0f} s)")


if __name__ == "__main__":
    main()
