"""The boundary rows' own chains (the reviewer 2026-10-10 08:11Z, 09:40Z). A level end and a death
restart used to be written at cycle = self.level on "@loop", behind that cycle's REPEAT row, and the
21.3 credit (SETTLE) behind the IMPORT rows on the same key, so gate check 1 refused every one.

  1. a gridworld run with a death + restart and an advance (credit written), then end_run: the FULL
     gate passes;
  2. must-fail: the same run with _BOUNDARY_CHAIN False (the old keying) is refused by check 1;
  3. must-fail: the credit row alone moved onto "@boundary" (same cycle, after the two IMPORT rows)
     is refused -- so "@credit" is needed, not only "@boundary".

    python test_boundary_chain.py
"""
from __future__ import annotations

import sys

import gamma
import gate
import gridworld
import ledger
import tether
import world

sys.dont_write_bytecode = True


def _run(chain: bool) -> list[dict]:
    tether._BOUNDARY_CHAIN = chain
    env = world.bind(gridworld.family("default", 1, 12))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="boundary_fixture"), tether.Config(),
                      ledger.Ledger())
    for _ in range(4):
        ag.step()
    ag.retarget(env, ag.level, how="death")
    ag.restarted(env)
    for _ in range(3):
        ag.step()
    ag.retarget(env, ag.level + 1, how="advance")
    for _ in range(3):
        ag.step()
    ag.end_run("cap")
    tether._BOUNDARY_CHAIN = True
    return ag.led.rows()


if __name__ == "__main__":
    rows = _run(True)
    events = [(r["slot"], r["event"]) for r in rows
              if r["event"] in ("boundary", "ending", "credit", "restart")]
    assert ("@credit", "credit") in events and ("@boundary", "restart") in events, events
    out = gate.check(rows)
    assert out["verdict"] == gate.PASS, out
    print(f"  own chains: {len(rows)} rows, boundary rows {events}; full gate passes")
    old = gate.check(_run(False))
    assert old["verdict"] == gate.REFUSE and old["check"] == "steps", old
    print(f"  must-fail, the old keying: refused ({old['check']}: {old['note']})")
    moved = [dict(r) for r in rows]
    for r in moved:
        if r["event"] == "credit":
            r["slot"] = "@boundary"
    m = gate.check(moved)
    assert m["verdict"] == gate.REFUSE and m["check"] == "steps", m
    print(f"  must-fail, credit on @boundary: refused ({m['check']}: {m['note']})")
    print("ok")
