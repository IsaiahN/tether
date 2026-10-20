"""C-7jk-1, 7j and 7k (the reviewer 2026-10-15 17:32, 20:27).

  J1  on the fake game every goal-exit step writes exactly one hypothesis_test row on its slot,
      with the 7h root; the count is the non-vacuity reading, stated even if 0
  J2  _test_outcome: reached, closer, farther, no change, slot gone on an ordered slot; on a
      categorical one a 3 -> 4 move toward 5 reads "not reached", never "closer" (J-a); MF the
      outcome computed against the before value instead of the target is wrong on "closer"
  K1  ELICIT's fresh pick: two fresh actions equal in reach, pressed 5 and 1 times; the 1-press
      action is picked; MF with the arm off the draw picks the other (built so they disagree)
  K2  dead-board coherence (S1): ELICIT on a dead board with RESET fresh picks RESET (the gate
      keeps the only action with reach > 0)

    python test_7jk.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True

RUN = r"""
import json, sys
sys.dont_write_bytecode = True
import tether, tether_agent
from arcengine import GameState
from test_entry import FakeWrapper
goals, tests = [], []
real_choose, real_row = tether.Agent.choose, tether.Agent._test_row
def choose(self, before):
    a, by = real_choose(self, before)
    if by == "discriminate:goal":
        goals.append([self.cycle, (self._test or {}).get("slot")])
    return a, by
def row(self):
    tests.append([self.cycle, self._test["slot"]])
    return real_row(self)
tether.Agent.choose, tether.Agent._test_row = choose, row
w = FakeWrapper(script={2: GameState.GAME_OVER})
tether_agent.run(w, "fake", max_actions=8)
print("OUT " + json.dumps({"goals": goals, "tests": tests}))
"""


def _run(code: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env["TETHER_AGENT_SEED"] = "0"
    r = subprocess.run([sys.executable, "-B", "-c", code], env=env, capture_output=True,
                       text=True, check=False, stdin=subprocess.DEVNULL)
    assert r.returncode == 0, r.stderr[-3000:]
    return json.loads([ln for ln in r.stdout.splitlines() if ln.startswith("OUT ")][-1][4:])


def main() -> None:
    run = _run(RUN)
    assert run["goals"] == run["tests"], ("J1", run)
    print(f"  J1 goal-exit steps {len(run['goals'])}, hypothesis_test rows {len(run['tests'])},"
          " one each on the same slot")

    from tether import _test_outcome
    cases = [((2, 5, 5, True), "reached"), ((2, 4, 5, True), "closer"),
             ((4, 2, 5, True), "farther"), ((2, 2, 5, True), "no change"),
             ((2, None, 5, True), "slot gone"), ((3, 4, 5, False), "not reached"),
             ((3, 5, 5, False), "reached"),
             ((2, 4, None, True), "not reached"), ((2, (1, 2), 5, True), "not reached")]
    for args, want in cases:
        assert _test_outcome(*args) == want, ("J2", args, _test_outcome(*args), want)
    assert _test_outcome(2, 4, 2, True) != "closer", "J2 MF did not fail"
    print("  J2 ordered and categorical outcomes; 3 -> 4 toward 5 on a colour reads not reached;"
          " MF against the before value is not closer")

    import frontier as FR
    import interface as I
    ctx = ("c",)
    acts = ("ACTION1", "ACTION2")
    i = I.Interface()
    seed = getattr(i, "draw_seed", None)
    d, _by, _f = FR.frontier_pick([(b, None, None) for b in acts], dict.fromkeys(acts, 0),
                                  dict.fromkeys(acts, 0), f"pick:{i.audits}:{ctx!r}", seed)
    few = acts[1] if d == acts[0] else acts[0]
    i.table = {b: {"by_ctx": {("other",): {()}}, "n": 1 if b == few else 5, "delta": {}}
               for b in acts}
    got = i.realise(I.Intent(I.ELICIT), acts, ctx).action
    I._7K_LEARN = False
    try:
        off = i.realise(I.Intent(I.ELICIT), acts, ctx).action
    finally:
        I._7K_LEARN = True
    assert got == few and off == d and few != d, ("K1", got, off, few, d)
    print(f"  K1 the less-pressed {few} picked; MF arm off, the draw picks {off}")

    j = I.Interface()
    j.table = {b: {"by_ctx": {("other",): {()}}, "n": 1, "delta": {}}
               for b in ("ACTION1", "ACTION2", I.RESET)}
    j.situate(1, False)
    dead = j.realise(I.Intent(I.ELICIT), ("ACTION1", "ACTION2", I.RESET), ctx).action
    assert dead == I.RESET, ("K2", dead)
    print("  K2 dead board, all fresh: ELICIT picks RESET (S1's reach gate)")
    print("7jk: OK")


if __name__ == "__main__":
    main()
