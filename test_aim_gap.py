"""TETHER_AIM_GAP (the reviewer 2026-10-12 15:26 CDT, stage 1b): audit keeps what a press at a
coordinate did per pre-press context, and an explore (ELICIT) press at a click site aims first at
an object not yet pressed in this context; a want (BECOME) keeps the known knob.

  a1 UNIT: _unpressed_here lists object positions with no (coordinate, context) record, skips the
     avoided ones, and a record in ANOTHER context does not count as pressed here.
  a2 MUST-PASS, arm: at the pinned call the press goes to an unpressed object, and the row says so
     ("aimed at ... where its effect here is unknown"), with today's aim beside it.
  a3 MUST-FAIL, today's order: the same row's "today's aim" is a coordinate already recorded as
     moving the subject, i.e. the old order would have re-pressed a known knob.
  a4 before the pin no row diverged (the first divergence is the pin).
  a5 MUST-FAIL MUTANT: the record never written -> the pinned row no longer aims at the pinned
     unpressed object.

    python test_aim_gap.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True

# Found by search (aim_search, every ELICIT positioned row under the arm): on gridworld click_only
# seed 0 the first row where the arm aimed somewhere today's aim did not is cycle 4 -- subject
# o0.colour, 4 objects unpressed here, today's aim (2, 2), the arm's (3, 3). 5 steps.
FAMILY, SEED, CYCLE, STEPS, TODAY, ARM = "click_only", 0, 4, 5, "(2, 2)", "(3, 3)"

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
import gamma, gridworld, interface, ledger, tether, world
FAMILY, SEED, STEPS, MODE = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
interface._AIM_GAP = True
if MODE == "mutant":
    orig_audit = interface.Interface.audit
    def audit(self, *a, **k):
        out = orig_audit(self, *a, **k)
        self.aimed_by_ctx.clear()
        return out
    interface.Interface.audit = audit
env = world.bind(gridworld.family(FAMILY, SEED))
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"t_{SEED}"), tether.Config(), ledger.Ledger())
for _ in range(STEPS):
    ag.step()
rows = [r for r in ag.led.rows() if "unpressed here:" in json.dumps(r)]
moves = {str(tuple(c)): sorted(v) for c, v in ag.iface.aimed_effect.items()}
print(json.dumps({"rows": rows, "aimed_effect": moves}, default=str))
'''


def _run(mode: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    # THE REGIME THE PIN WAS FOUND IN (B 2026-10-18 O1): the aim by the first unpressed cell, not
    # A1's recorded draw (TETHER_A1_TIES, 0996891), and one temperament (cab5bd5). An OLD regime
    env.update(TETHER_A1_TIES="0", TETHER_AGENT_SEED="0")
    here = os.path.dirname(os.path.abspath(__file__))
    out = subprocess.run([sys.executable, "-c", PROBE, FAMILY, str(SEED), str(STEPS), mode],
                         cwd=here, env=env, capture_output=True, text=True, timeout=300)
    assert out.returncode == 0, out.stderr[-2000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def _row(run: dict) -> str:
    hit = [json.dumps(r["detail"]) for r in run["rows"] if r["cycle"] == CYCLE]
    assert len(hit) == 1, f"pinned row not found ({len(hit)}): re-run the search"
    return hit[0]


def a1_unit() -> None:
    import interface as IF
    t = IF.Interface()
    state = {"o0.row": 2, "o0.col": 2, "o1.row": 3, "o1.col": 3, "o2.row": 1, "o2.col": 4}
    ctx, other = (("orthogonal", 1),), (("diagonal", 1),)
    assert t._unpressed_here(state, ctx) == [(2, 2), (3, 3), (4, 1)], t._unpressed_here(state, ctx)
    t.aimed_by_ctx[((2, 2), ctx)] = {("o0.colour",)}
    t.aimed_by_ctx[((3, 3), other)] = {("o1.colour",)}
    assert t._unpressed_here(state, ctx) == [(3, 3), (4, 1)], "another context is not here"
    assert t._unpressed_here(state, ctx, {(3, 3)}) == [(4, 1)], "avoided coordinates are skipped"


def main() -> None:
    a1_unit()
    on, mut = _run("on"), _run("mutant")
    row = _row(on)
    # a2
    assert f"aimed at {ARM} where its effect here is unknown" in row, row
    assert f"today's aim: {TODAY}" in row, row
    # a3
    assert "o0.colour" in on["aimed_effect"].get(TODAY, []), on["aimed_effect"]
    # a4
    before = [json.dumps(r["detail"]) for r in on["rows"] if r["cycle"] < CYCLE]
    assert not any("where its effect here is unknown" in s and "today's aim: None" not in s
                   for s in before), before
    # a5
    assert f"aimed at {ARM} where its effect here is unknown" not in _row(mut), _row(mut)
    print(f"test_aim_gap: 5/5 (pinned {FAMILY} s{SEED} c{CYCLE}: arm aims {ARM}, today's aim "
          f"{TODAY} moved the subject; the mutant does not aim {ARM})")


if __name__ == "__main__":
    main()
