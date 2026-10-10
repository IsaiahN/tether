"""P1's fixture: a term entered by `_install_reuse` is a CANDIDATE, so the ground can grade it
(the reviewer 2026-10-09 23:01Z).

Before the fix `settle` skipped it (`self.candidates.get(name)` was None): it could never settle,
never be demoted, and stayed bound while wrong. Both callers, each with the module flag on and off:
  - the LIBRARY PULL (`_library_fit` rebinding a held `take` to an operand);
  - the SWEEP (a minted `take` rebound onto an owed slot's operand).
MUST-FAIL (a): the reuse-installed term settles on a later correct prediction.
MUST-FAIL (b): mispredicting after that, it is DEMOTED and UNBOUND (the existing ceiling rules).

    python test_reuse_candidate.py
"""
from __future__ import annotations

import sys

import gamma
import gridworld
import ledger
import tether
import world

sys.dont_write_bytecode = True

SEQ = [0, 3, 5, 1, 6, 2, 7, 4] * 2          # y's next value is x's value now


def _agent() -> tether.Agent:
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="reuse_fixture"),
                      tether.Config(), ledger.Ledger())
    states = [{"x": SEQ[i], "y": SEQ[i - 1] if i else 7} for i in range(len(SEQ))]
    ag.trace = [(states[i], "A", states[i + 1], None, None) for i in range(len(SEQ) - 1)]
    ag._trace_pos = None
    ag.slots = [*ag.slots, "x", "y"]
    ag.alphabet["x"] = ag.alphabet["y"] = 8
    ag.bound = {}
    return ag


def _via_pull(ag: tether.Agent) -> str | None:
    assert "take" in ag.gamma.library      # the held term the pull rebinds to an operand
    return ag._library_fit("y", None)


def _via_sweep(ag: tether.Agent) -> str | None:
    term = ag.gamma.build(("take",), operand="w")
    ag.gamma.accept(term, seq=len(ag.led), residual="fixture")
    ag.owed_import.add("y")
    ag.sweep(term, "w")
    return ag.bound.get("y")


def _grade(ag: tether.Agent, name: str) -> tuple[list[str], bool]:
    ag.bound["y"] = name
    ag.cycle += 1
    ag._pred_by = {"y": name}
    ag.settle({"y": tether.SlotResidual("y", "transition", 1, 1, 0.0)})
    for _ in range(40):
        if "y" not in ag.bound:
            break
        ag.cycle += 1
        ag.gamma.tick += 1
        ag._pred_by = {"y": name}
        ag.settle({"y": tether.SlotResidual("y", "transition", 1, 2, 3.0)})
    ev = [r["event"] for r in ag.led.rows() if r["step"] == "SETTLE" and r["slot"] == "y"]
    return ev, "y" not in ag.bound


def _run(route, flag: bool):
    tether._REUSE_CANDIDATE = flag
    try:
        ag = _agent()
        name = route(ag)
        assert name and "<" in name, f"the route did not reuse-install a rebinding: {name}"
        installs = [r for r in ag.led.rows() if r["event"] == "reuse_install"]
        assert installs, "no reuse_install row: the fixture did not reach _install_reuse"
        return name, _grade(ag, name)
    finally:
        tether._REUSE_CANDIDATE = True


if __name__ == "__main__":
    bad = 0
    for label, route in (("library pull", _via_pull), ("sweep", _via_sweep)):
        name, (ev_off, unbound_off) = _run(route, False)
        _, (ev_on, unbound_on) = _run(route, True)
        print(f"  {label}: {name}; without the fix {ev_off} unbound={unbound_off}; "
              f"with it {ev_on[:2]}...{ev_on[-1:]} ({len(ev_on)} rows) unbound={unbound_on}")
        ok = (ev_off == [] and not unbound_off
              and ev_on[:1] == ["settle"] and "demote" in ev_on and unbound_on)
        print(f"{'ok  ' if ok else 'FAIL'} {label}")
        bad += not ok
    sys.exit(1 if bad else 0)
