"""TETHER_DEST_GAP (the reviewer 2026-10-12 12:41, 13:04 CDT, stage 1a): the interface keeps where a
press LED beside the context it was taken in, and among equal-price reaching options ELICIT prefers
one seen to lead where an offered action's effect is unknown.

ONE 30-step run under the arm (the reviewer 13:23 CDT: tests under 5 minutes). At every chooser call
the arm's pick, today's pick (the same options handed as pairs, as OFF hands them) and the mutant's
pick (gap ranked after least-seen) are all taken from the same options.

  d1 UNIT: the gap predicate on a hand-built table -- no destination record is no gap; a destination
     where every offered action is mapped is no gap; one unmapped action is a gap; RESET never is.
  d2 MUST-PASS, arm: at the pinned call the gapped option is taken over the least-seen one, and the
     intent row says so ("toward an unknown knob", the gap flags).
  d3 MUST-FAIL, today's key: the same options as pairs take the least-seen option.
  d4 every chooser call before the pinned one picks the same option under the arm and today's key,
     so the arm changed nothing the being did before it. Full-ledger identity with the arm OFF is
     the OFF-identity check (s0/s1@20), not repeated here.
  d5 MUST-FAIL MUTANT: gap ranked after least-seen takes today's option.

    python test_dest_gap.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True

# Found by search (every _choose_known call under the arm, today's pick beside the new one): on
# gridworld_s0 the first call the gap changes is in cycle 29 -- four 'changes the board' options at
# price 1, seen (2, 2, 3, 1), gaps (F, T, T, F): today takes index 3, the arm index 1. 30 steps.
MEMBER, CYCLE, STEPS, OLD, NEW = "gridworld_s0", 29, 30, 3, 1

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
import gamma, interface, ledger, tether, world
from conform import panel
MEMBER, STEPS = sys.argv[1], int(sys.argv[2])
interface._DEST_GAP = True
orig = tether.Agent._choose_known
def mutant(self, known):
    def price(e):
        return 1 + self._attempt_actions if e == interface.RESTARTS else 1
    def reaches(e):
        return e == interface.CHANGES or (e == interface.RESTARTS and self._attempt_actions > 0)
    gap = [len(k) > 2 and bool(k[2]) for k in known]
    return min(range(len(known)), key=lambda j: (not reaches(known[j][0]), price(known[j][0]),
                                                 known[j][1], not gap[j], j))
calls = []
def spy(self, known):
    i, why = orig(self, known)
    if known and len(known[0]) == 2:      # the interface's own today's-key call
        return i, why
    calls.append({"cycle": self.cycle, "known": [list(k) for k in known], "pick": i,
                  "today": orig(self, [(k[0], k[1]) for k in known])[0],
                  "mutant": mutant(self, known)})
    return i, why
tether.Agent._choose_known = spy
g, seed = panel._gridworld(MEMBER)
env = world.bind(g)
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"t_{seed}"), tether.Config(), ledger.Ledger())
for _ in range(STEPS):
    ag.step()
rows = [r for r in ag.led.rows() if r["event"] == "intent"]
print(json.dumps({"calls": calls, "rows": rows}, default=str))
'''


def _run() -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    here = os.path.dirname(os.path.abspath(__file__))
    out = subprocess.run([sys.executable, "-c", PROBE, MEMBER, str(STEPS)], cwd=here, env=env,
                         capture_output=True, text=True, timeout=600)
    assert out.returncode == 0, out.stderr[-2000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def d1_unit() -> None:
    import interface as IF
    t = IF.Interface()
    a, b, ctx, d = "up", "down", (("orthogonal", 1),), (("orthogonal", 2),)
    t.table = {a: {"by_ctx": {ctx: {()}}}, b: {"by_ctx": {ctx: {()}}}}
    assert not t.leads_to_gap(a, ctx, (a, b)), "no destination record must read no gap"
    t.table[a]["to"] = {ctx: {d}}
    assert t.leads_to_gap(a, ctx, (a, b)), "a destination where nothing is mapped is a gap"
    t.table[a]["by_ctx"][d] = {()}
    assert t.leads_to_gap(a, ctx, (a, b)), "one offered action unmapped there is a gap"
    t.table[b]["by_ctx"][d] = {()}
    assert not t.leads_to_gap(a, ctx, (a, b)), "every offered action mapped there is no gap"
    assert not t.leads_to_gap(a, ctx, (a, b, IF.RESET)), "RESET is never an unknown knob"


def main() -> None:
    d1_unit()
    run = _run()
    hit = [c for c in run["calls"] if c["cycle"] == CYCLE]
    assert len(hit) == 1, f"pinned chooser call not found ({len(hit)}): re-run the search"
    c = hit[0]
    # d2
    assert c["known"][NEW][2] and not c["known"][OLD][2], c
    assert c["pick"] == NEW, c
    row = [r for r in run["rows"]
           if r["cycle"] == CYCLE and "nothing unknown here" in json.dumps(r)]
    assert len(row) == 1 and "toward an unknown knob" in json.dumps(row[0]), row
    assert "gaps {" in json.dumps(row[0]), row
    names = [p.split(":")[0].strip(" ,'") for p in row[0]["detail"]["reads"][1]
             .split("; gaps {", 1)[1].split("}", 1)[0].split(",")]
    assert f"today's key: {names[OLD]}" in row[0]["detail"]["reads"][1], (names, row)
    # d3
    assert c["today"] == OLD, c
    # d4
    before = [x for x in run["calls"] if x["cycle"] < CYCLE]
    assert before and all(x["pick"] == x["today"] for x in before), before
    # d5
    assert c["mutant"] == OLD, "the mutant must take today's option, or the gap slot is idle"
    print(f"test_dest_gap: 5/5 (pinned {MEMBER} c{CYCLE}: arm picks {NEW}, today's key and the "
          f"mutant {OLD}; {len(before)} earlier chooser call(s) unchanged by the arm)")


if __name__ == "__main__":
    main()
