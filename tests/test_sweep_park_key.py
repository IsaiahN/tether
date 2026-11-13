"""7a, THE SWEEP'S PAYS-ARM ROWS ON THE PARK (the reviewer r1745, r1900; 8464907's LIMIT).
An earlier level's park whose slot name is a live slot ("L0:y" beside this level's y), swept
after y's ACCEPT this cycle, files its pull and reuse_install rows under the park's key, as
reuse_refused already does; so the gate's step order holds.

  K1  the sweep closes the park: pull (and reuse_install, when the term is new) rows carry
      slot "L0:y", held "L0:y"; the gate's step order passes.
  MF-K1 the same rows filed under the live slot "y" (the old key): "y: MINT after ACCEPT" -> RED.
  K2  a this-level target (y owed, no park) is keyed "y" as before.

    python tests/test_sweep_park_key.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gate  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

SEQ = [0, 3, 5, 1, 6, 2, 7, 4] * 2          # y's next value is x's value now (as P2's fixture)
KINDS = ("pull", "reuse_install")


def _agent() -> tether.Agent:
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="sweep_park_key"),
                      tether.Config(), ledger.Ledger())
    states = [{"x": SEQ[i], "y": SEQ[i - 1] if i else 7} for i in range(len(SEQ))]
    ag.trace = [(states[i], "A", states[i + 1], None, None) for i in range(len(SEQ) - 1)]
    ag._trace_pos = None
    ag.slots = [*ag.slots, "x", "y"]
    ag.alphabet["x"] = ag.alphabet["y"] = 8
    ag.bound = {}
    return ag


def _swept(park: bool) -> tuple[list, list]:
    """(this sweep's pull/reuse_install rows, every row) after y's ACCEPT in this cycle."""
    ag = _agent()
    term = ag.gamma.build(("take",), operand="w")
    ag.gamma.accept(term, seq=len(ag.led), residual="fixture")
    if park:
        ag.parked["L0:y"] = {"slot": "y", "hist": ag.history("y"), "slots": list(ag.slots),
                             "level": 0, "verdict": "unreached", "units_then": 0}
    else:
        ag.owed_import.add("y")
    ag.led.record(ag.cycle, "ACCEPT", "y", "accept", term="y_own")   # y's turn is done
    n0 = len(ag.led)
    ag._running_step = "MINT"
    ag.sweep(term, "w")
    return [r for r in ag.led.rows(n0) if r["event"] in KINDS], ag.led.rows()


def main() -> int:
    rows, every = _swept(True)
    print(f"   park swept: {[(r['event'], r['slot'], r['detail'].get('held')) for r in rows]}")
    ok = (rows and all(r["slot"] == "L0:y" for r in rows)
          and all(r["detail"].get("held", "L0:y") == "L0:y" for r in rows))
    steps = gate._steps(every)
    print(f"   gate step order: {steps}")
    print("K1 the park's rows are filed on the park: " + ("GREEN" if ok and steps is None
                                                          else "RED"))
    assert ok and steps is None
    old = [{**r, "slot": "y"} if r in rows else r for r in every]
    red = gate._steps(old)
    print(f"   the plant (filed under the live slot y): {red}")
    print("MF-K1 the old key breaks the step order: " + ("RED" if red
                                                        else "GREEN (the plant went unseen)"))
    assert red is not None and "y: MINT after ACCEPT" in red["note"]
    here, _ = _swept(False)
    print(f"   this-level target: {[(r['event'], r['slot']) for r in here]}")
    ok2 = here and all(r["slot"] == "y" for r in here)
    print("K2 a this-level target keeps its own slot: " + ("GREEN" if ok2 else "RED"))
    assert ok2
    print("sweep_park_key: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
