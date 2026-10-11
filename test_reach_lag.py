"""The lag-row repair (the reviewer 2026-10-11 12:35 CDT, ruled ungated): a reach-history row
carries the transition's before-values as `slot~1`, so a goal condition comparing a slot with
its own earlier reading -- CHANGE_OF's `colour_changed` -- runs to True or False, not None.

  r1 on a reach row "o0.colour_changed == 1" / "== 0" run to booleans, and exactly one holds;
  r2 MUST-FAIL: on the bare after-state (the row before the repair) both read None;
  r3 the row is the after-state plus every before-value under `~1`, and no slot carried a lag.

    python test_reach_lag.py
"""
from __future__ import annotations

import sys

import compile_term as C
from test_goal_condition import _agent

sys.dont_write_bytecode = True


def main() -> int:
    ag = _agent()
    for _ in range(3):
        ag.step()
    atoms = {a.name: a for a in ag.gamma.atoms}
    step = ag.trace[-1]
    row = ag._reach_row(step)
    on, off = (C.compile_candidate({"condition": f"o0.colour_changed == {v}"}, atoms)
               for v in (1, 0))
    assert isinstance(on, C.Compiled) and isinstance(off, C.Compiled), (on, off)
    got = [C.run(on, row), C.run(off, row)]
    assert all(isinstance(x, bool) for x in got) and got.count(True) == 1, got
    print(f"  r1 on a reach row: colour_changed == 1 -> {got[0]}, == 0 -> {got[1]}")
    bare = [C.run(on, step[2]), C.run(off, step[2])]
    assert bare == [None, None], bare
    print("  r2 must-fail: on the bare after-state both read None")
    assert {k: v for k, v in row.items() if not k.endswith("~1")} == step[2], "after-state moved"
    assert {k[:-2]: v for k, v in row.items() if k.endswith("~1")} == step[0], "before-values"
    print(f"  r3 row = after-state ({len(step[2])}) + before-values as ~1 ({len(step[0])})")
    print("reach lag: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
