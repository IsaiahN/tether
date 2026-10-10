"""P3's fixture: a candidate the ground refutes before it ever settles is owed a SETTLE row
(the reviewer 2026-10-10 00:15Z). Recording only: the binding, the standing and the refutation are
what they were without it.

A reuse-installed candidate bound to y mispredicts on its first two bets:
  - one `miss_while_candidate` row per refuted bet, naming the term, status candidate;
  - the binding is untouched (still bound) and the standing records the same rejections the
    refutation already wrote -- the row reports it and changes nothing.

    python test_candidate_miss_row.py
"""
from __future__ import annotations

import sys

import gamma
import gridworld
import ledger
import tether
import world

sys.dont_write_bytecode = True

SEQ = [0, 3, 5, 1, 6, 2, 7, 4] * 2


def _agent() -> tether.Agent:
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="candidate_miss_fixture"),
                      tether.Config(), ledger.Ledger())
    states = [{"x": SEQ[i], "y": SEQ[i - 1] if i else 7} for i in range(len(SEQ))]
    ag.trace = [(states[i], "A", states[i + 1], None, None) for i in range(len(SEQ) - 1)]
    ag._trace_pos = None
    ag.slots = [*ag.slots, "x", "y"]
    ag.alphabet["x"] = ag.alphabet["y"] = 8
    ag.bound = {}
    return ag


if __name__ == "__main__":
    ag = _agent()
    name = ag._library_fit("y", None)
    assert name and name in ag.candidates, f"the fixture did not install a candidate: {name}"
    ag.bound["y"] = name
    for _ in range(2):
        ag.cycle += 1
        ag._pred_by = {"y": name}
        ag.settle({"y": tether.SlotResidual("y", "transition", 1, 2, 3.0)})
    rows = [r for r in ag.led.rows() if r["step"] == "SETTLE" and r["slot"] == "y"]
    ev = [r["event"] for r in rows]
    print(f"  {name}: SETTLE rows {ev}; still bound {ag.bound.get('y') == name}; "
          f"rejections {round(ag.gamma.rejection_of(name), 3)}")
    ok = (ev == ["miss_while_candidate"] * 2 and ag.bound.get("y") == name
          and all(r["detail"]["term"] == name and r["detail"]["status"] == "candidate"
                  for r in rows))
    print("ok" if ok else "FAIL")
    sys.exit(0 if ok else 1)
