"""MUSE_BOUND (the reviewer 2026-11-02 r841): Agent._muse on a stub after a cleared level -- 5
residuals parked on level 0, 40 settled methods, 2 other slots per record (3 bindings each).
  MF-MB1  ON, with a step budget of 100 evaluations: no step spends past the budget; the muse is
          cut, owed (muse_owed rows) and resumed until done, in 7 steps.
  MF-MB2  ON and OFF reach the SAME paying list and the same count tried (600): a cut changes when
          the work is done, never its result.
  MF-MB3  OFF (before the bound): one step does all 605 evaluations, past the budget (the stall).

    python tests/test_muse_bound.py
"""
from __future__ import annotations

import sys
from collections import Counter
from types import SimpleNamespace

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import ledger  # noqa: E402
import tether  # noqa: E402

A = tether.Agent
METHODS = [f"m{i:02d}" for i in range(40)]


def stub():
    lib = {tether.IDN: SimpleNamespace(atoms=("idn",)),
           **{m: SimpleNamespace(atoms=(m,)) for m in METHODS}}
    gam = SimpleNamespace(library=lib, is_atom=lambda t: t.atoms == ("idn",),
                          is_settled=lambda _n: True)
    parked = {f"p{i}": {"level": 0, "slot": f"o{i}.x", "hist": [1, 2, 3],
                        "slots": [f"o{i}.x", f"o{i}.y", f"o{i}.z"]} for i in range(5)}
    ag = SimpleNamespace(parked=parked, level=1, gamma=gam, _muse_last=None, _muse_run=None,
                         alphabet={f"o{i}.x": 1 for i in range(5)}, led=ledger.Ledger(None),
                         cycle=0, _spent=0, calls=[0])
    ag._owes_nothing = lambda: True

    def left(cand, slot, _hist):
        ag.calls[0] += 1
        name = getattr(cand, "name", "idn")          # the base is the library's identity entry
        return 10.0 if name == "idn" else float(sum(map(ord, name + slot)) % 9)
    ag._left = left
    ag._bits = lambda _x: 1.0
    ag._muse_owe = lambda run, t0: A._muse_owe(ag, run, t0)
    return ag


def muse_steps(on: bool, budget: int) -> tuple:
    tether._MUSE_BOUND, keep_b, keep_t = on, tether.STEP_BUDGET, tether.Term
    tether.STEP_BUDGET = budget
    tether.Term = lambda chain, operand=None: SimpleNamespace(name=f"{chain[0]}|{operand}")
    try:
        ag, per_step = stub(), []
        for _ in range(50):
            ag.cycle, ag._spent, c0 = ag.cycle + 1, 0, ag.calls[0]
            A._muse.__wrapped__(ag)          # the method under its step scope
            per_step.append(ag.calls[0] - c0)
            if any(r["event"] == "muse" for r in ag.led.rows()):
                break
        done = [r["detail"] for r in ag.led.rows() if r["event"] == "muse"][0]
        owed = sum(r["event"] == "muse_owed" for r in ag.led.rows())
        return per_step, done, owed
    finally:
        tether._MUSE_BOUND, tether.STEP_BUDGET, tether.Term = True, keep_b, keep_t


def main():
    assert tether._MUSE_BOUND, "ON by default"
    on_steps, on_done, owed = muse_steps(True, 100)
    off_steps, off_done, off_owed = muse_steps(False, 100)
    assert max(on_steps) <= 100 and len(on_steps) == 7 and owed == 6, ("MF-MB1", on_steps, owed)
    assert on_done["tried"] == off_done["tried"] == 600, ("MF-MB2 tried", on_done["tried"])
    key = Counter(json_key for json_key in (str(sorted(p.items())) for p in on_done["paying"]))
    assert key == Counter(str(sorted(p.items())) for p in off_done["paying"]), "MF-MB2 paying"
    assert off_steps == [605] and off_owed == 0, ("MF-MB3: OFF runs past the budget", off_steps)
    print(f"test_muse_bound: ON {len(on_steps)} steps of at most {max(on_steps)} evaluations "
          f"({owed} owed); OFF one step of {off_steps[0]}; the same {on_done['tried']} tried and "
          f"{len(on_done['paying'])} paying")


if __name__ == "__main__":
    main()
