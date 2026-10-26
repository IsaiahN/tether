"""THINK OR ACT AT THE STEP (Isaiah 2026-10-26 11:25; the reviewer 11:33): A1 TETHER_STEP_ACT and
A2 TETHER_WALK_BUDGET, on a stepped gridworld agent.

  (a) A1: with an untried action, route defers the slot's lookup (lookup_deferred probe_first), the
      slot is owed, and the next cycle with the same untried set walks it (probe_declined);
  (b) A1 MUST-FAIL: with the arm OFF the lookup runs at once;
  (c) A2: with STEP_BUDGET forced to 1 the index walk stops at an entry boundary (walk_cut), the
      truncated index is not memoised, the slot is owed, and the next route asks it first;
  (d) A2 MUST-HOLD: with the budget never reached the lookup offers the same as with the arm OFF,
      each arm in its own fresh process;
  (e) A1 under urgency: deferred "urgent" at cycle c, walked at c+1 (urgent_declined), deferred
      again at c+2 -- the library every other step, never zero (the reviewer 11:52 item 3);
  (f) route runs in the ROUTE step scope; its MUST-FAIL calls route without the decorator.

    python tests/test_act.py [check names]
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
import gamma
import gridworld
import ledger
import tether
import world

sys.dont_write_bytecode = True


def _agent(steps: int = 3) -> tether.Agent:
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="act_fixture"), tether.Config(),
                      ledger.Ledger())
    for _ in range(steps):
        ag.step()
    return ag


def _res(slot: str) -> dict:
    return {slot: tether.SlotResidual(slot, "x", 0, 1, 1.0)}


def _rows(ag: tether.Agent, n0: int, event: str) -> list:
    return [r for r in ag.led.rows()[n0:] if r.get("event") == event]


def _gate_case(on: bool) -> tuple:
    ag = _agent()
    slot = sorted(ag.slots)[0]
    ag.actions = ("A1", "A2")
    ag.iface.table = {"A1": {}}                    # A2 never tried: a probe is open
    ag._can_probe = None
    ag._relief_rate = lambda: (1e9, 0)             # never urgent
    calls: list = []
    ag._library_fit = lambda s, _ex: calls.append((ag.cycle, s)) or None
    keep = tether._STEP_ACT
    try:
        tether._STEP_ACT = on
        c0 = ag.cycle
        n0 = len(ag.led.rows())
        ag.route(_res(slot))
        first = (list(calls), _rows(ag, n0, "lookup_deferred"), slot in ag._owed_q,
                 slot in ag.owed_import)
        ag.cycle = c0 + 1                          # a later cycle, the same untried set
        n1 = len(ag.led.rows())
        ag.route(_res(slot))
        second = (list(calls), _rows(ag, n1, "lookup_deferred"), _rows(ag, n1, "step_act"))
    finally:
        tether._STEP_ACT = keep
    return slot, first, second


def check_a_untried_action_defers_then_probe_declined_walks() -> None:
    slot, (calls1, rows1, owed, owes), (calls2, rows2, act2) = _gate_case(True)
    assert calls1 == [], calls1                                  # not looked up this step
    assert [r["detail"]["why"] for r in rows1] == ["probe_first"], rows1
    assert owed and owes, (owed, owes)                           # owed, asked first next step
    assert len(calls2) == 1 and calls2[0][1] == slot, calls2     # the next cycle walks it
    assert rows2 == [], rows2
    assert act2 and act2[-1]["detail"]["lookups_walked"] == 1, act2


def check_b_must_fail_arm_off_looks_up_at_once() -> None:
    slot, (calls1, rows1, _o, _w), _second = _gate_case(False)
    assert len(calls1) == 1 and calls1[0][1] == slot, calls1
    assert rows1 == [], rows1


def check_c_walk_budget_cuts_at_an_entry_and_owes() -> None:
    ag = _agent()
    keep = tether.STEP_BUDGET, tether._STEP_ACT
    try:
        tether._STEP_ACT = False                   # the walk is the subject here
        tether.STEP_BUDGET = 1
        cut = None
        for slot in sorted(ag.slots):
            ag._spent = 0
            n0 = len(ag.led.rows())
            ag._library_fit(slot, None)
            got = _rows(ag, n0, "walk_cut")
            if got:
                cut = (slot, got[0]["detail"])
                break
        assert cut is not None, "no slot's index walk had a second entry: nothing was cut"
        slot, d = cut
        assert d["unreached"] >= 1 and d["budget"] == 1, d
        assert ag._k1_trunc, "the truncated walk must not be memoised"
        assert slot in ag._owed_q and slot in ag.owed_import, slot
        other = next(s for s in sorted(ag.slots) if s != slot)
        tether.STEP_BUDGET = 10 ** 9
        ag._library_fit = lambda _s, _ex: None
        ag.route({other: tether.SlotResidual(other, "x", 0, 1, 1.0),
                  slot: tether.SlotResidual(slot, "x", 0, 1, 1.0)})
        assert ag._route_order[0] == slot, ag._route_order   # the owed lookup is asked first
    finally:
        tether.STEP_BUDGET, tether._STEP_ACT = keep


def _offers(on: bool) -> dict:
    ag = _agent()
    tether._WALK_BUDGET, tether._STEP_ACT, tether.STEP_BUDGET = on, False, 10 ** 9
    out = {}
    for slot in sorted(ag.slots):
        ag._spent = 0
        ag._library_fit(slot, None)
        out[slot] = [sorted(map(repr, ag._lib_offers.get(slot, []))),
                     sorted(map(repr, (ag._named.get(slot) or {}).items()))]
    return out


def check_d_must_hold_budget_never_reached_equals_off() -> None:
    # each arm in its own fresh process: two agents in one process share state (the reviewer
    # 2026-10-26 12:12; OFF against OFF in one process differed on 160 of 196 slots)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TETHER_AGENT_SEED="0")

    def run(arm: str) -> dict:
        p = subprocess.run([sys.executable, __file__, "--offers", arm], env=env,
                           capture_output=True, text=True, timeout=240)
        assert p.returncode == 0, (arm, p.returncode, p.stderr[-2000:])
        return json.loads(p.stdout.strip().splitlines()[-1])
    on, off = run("on"), run("off")
    assert on == off, [s for s in on if on[s] != off.get(s)]
    assert any(v[0] or v[1] for v in on.values()), "no slot was offered anything: vacuous"


def check_e_urgent_defers_then_urgent_declined_walks() -> None:
    ag = _agent()
    slot = sorted(ag.slots)[0]
    ag._last_progress = ag._last_commit = 0
    ag._relief_rate = lambda: (1.0, 0)             # idle / 1 >= _QUORUM_HALF: urgent
    calls: list = []
    ag._library_fit = lambda s, _ex: calls.append((ag.cycle, s)) or None
    keep = tether._STEP_ACT, tether._THINK_OR_ACT
    try:
        tether._STEP_ACT = tether._THINK_OR_ACT = True
        c = ag.cycle = 100
        whys = []
        for k in range(3):
            ag.cycle = c + k
            n0 = len(ag.led.rows())
            ag.route(_res(slot))
            whys.append([r["detail"]["why"] for r in _rows(ag, n0, "lookup_deferred")])
        assert whys == [["urgent"], [], ["urgent"]], whys            # every other step
        assert calls == [(c + 1, slot)], calls                       # walked at c+1 only
        ag.cycle = c + 1
        ag._urgent_wait[slot] = (c + 1, "urgent_declined")
        assert ag._think_or_act(slot, closer=False) == (True, "urgent_declined")  # same cycle
    finally:
        tether._STEP_ACT, tether._THINK_OR_ACT = keep


def check_f_route_runs_in_the_route_step() -> None:
    ag = _agent()
    slot = sorted(ag.slots)[0]
    seen: list = []
    ag._library_fit = lambda _s, _ex: seen.append(ag._running_step) or None
    keep = tether._STEP_ACT
    try:
        tether._STEP_ACT = False                   # the lookup runs, so the spy is reached
        ag.route(_res(slot))
        assert seen == ["ROUTE"], seen
        seen.clear()
        tether.Agent.route.__wrapped__(ag, _res(slot))   # MUST-FAIL: route without its scope
        assert seen and seen != ["ROUTE"], seen
    finally:
        tether._STEP_ACT = keep


def main() -> int:
    if sys.argv[1:2] == ["--offers"]:
        print(json.dumps(_offers(sys.argv[2] == "on")))
        return 0
    want = set(sys.argv[1:])
    checks = [v for k, v in globals().items() if k.startswith("check_")
              and (not want or k in want)]
    assert not want or len(checks) == len(want), ("unknown check name", sorted(want))
    for c in checks:
        c()
        print("ok  ", c.__name__)
    print(f"test_act: {len(checks)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
