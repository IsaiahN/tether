"""7a(10) MC6 muse (TETHER_MC6; R3 part 2; the reviewer 2026-10-10 23:50Z). On a step that owes
nothing, the settled methods are re-tested as chains on an earlier level's parked residuals and a
MUSE row records the gap and the compute spent. snaps.ladder seed 7 (levels 5, steps 60, 4 slots)
is the habitat: its level 4 owes nothing on 42 steps with level 1's death parked.

  must-pass: ON, seed 7 writes MUSE rows, each on a step that owed nothing, each carrying
     compute_ms, installed False;
  MC6-a. no action taken and no bet changed: every row but the MUSE rows is identical ON and OFF;
  MC6-b. a step that owes anything never muses (an agent with one owed slot and a parked target);
  MC6-c. a binding never crosses: only chains are re-bound on the parked slot's own history;
  MC6-d. a muse step leaves every live structure the next step reads unchanged (bound, stamps,
     held candidates, owed, parked, the library, the book): a snapshot before and after.

    python test_mc6.py
"""
from __future__ import annotations

import copy
import json
import sys

import gamma
import gridworld
import ledger
import snaps
import tether
import world

sys.dont_write_bytecode = True

made: list = []
real_init, real_muse = tether.Agent.__init__, tether.Agent._muse


def _init(self, *a, **k):
    real_init(self, *a, **k)
    made.append(self)


def _snap(ag) -> tuple:
    return (dict(ag.bound), json.dumps(ag.gamma.stamps, sort_keys=True, default=str),
            dict(ag.candidates), set(ag.owed_import), sorted(ag.parked),
            sorted(ag.gamma.library), json.dumps(ag.gamma.book, sort_keys=True, default=str))


checked: list = []


def _muse_checked(self):
    owed = set(self.owed_import)
    before = _snap(self)
    n0 = len(self.led)
    real_muse(self)
    wrote = [r for r in self.led.rows()[n0:] if r["event"] == "muse"]
    assert _snap(self) == before, "MC6-d: a muse step changed a live structure"
    if wrote:
        assert not owed, "a muse row on a step that owed something"
    checked.append(len(wrote))


def _ladder(on: bool) -> list:
    was = tether._MC6
    tether._MC6 = on
    made.clear()
    try:
        snaps.ladder(7, levels=5, steps=60, n_slots=4)
    finally:
        tether._MC6 = was
    return made[0].led.rows()


if __name__ == "__main__":
    tether.Agent.__init__ = _init
    tether.Agent._muse = _muse_checked
    on = _ladder(True)
    muses = [r["detail"] for r in on if r["event"] == "muse"]
    assert muses and all(m["installed"] is False and "compute_ms" in m for m in muses), muses[:1]
    ms = sorted(m["compute_ms"] for m in muses)
    lv = sorted({m["level"] for m in muses})
    tried = sum(m["tried"] for m in muses)
    pay = sum(len(m["paying"]) for m in muses)
    print(f"  must-pass: {len(muses)} MUSE rows on seed 7 (levels {lv}); tried {tried} chain "
          f"bindings, {pay} would pay; compute_ms median {ms[len(ms) // 2]}, max {ms[-1]}")
    print(f"  MC6-d: {len(checked)} muse calls, every live structure unchanged across each")
    off = _ladder(False)

    def strip(rows):
        # the arms header names the arm, and `seq` is a row's index, shifted by each MUSE row
        out = []
        for r in rows:
            if r["event"] in ("muse", "arms"):
                continue
            r = {k: v for k, v in r.items() if k != "seq"}
            r["detail"] = {k: v for k, v in r["detail"].items() if k != "seq"}
            out.append(json.dumps(r, sort_keys=True, default=str))
        return out
    a, b = strip(on), strip(off)
    assert a == b, next(i for i, (x, y) in enumerate(zip(a, b, strict=False)) if x != y)
    print(f"  MC6-a: ON and OFF ledgers identical but for the MUSE rows ({len(a)} rows)")
    tether.Agent.__init__ = real_init
    tether._MC6 = True
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="mc6"), tether.Config(), ledger.Ledger())
    ag.step()
    ag.level = 1
    ag.parked["L0:o0.row"] = {"slot": "o0.row", "level": 0, "hist": list(ag.trace),
                              "slots": list(ag.slots)}
    ag.owed_import = {"o0.col"}
    n0 = len(ag.led)
    real_muse(ag)
    assert not [r for r in ag.led.rows()[n0:] if r["event"] == "muse"]
    print("  MC6-b: one owed slot and a parked target: no muse")
    bound0 = copy.deepcopy(ag.bound)
    ag.owed_import = set()
    ag._step_row0 = 0
    real_muse(ag)
    assert ag.bound == bound0
    print("  MC6-c: the parked slot's binding is untouched; methods are chains re-bound on its "
          "own history")
    tether._MC6 = False
    print("ok")
