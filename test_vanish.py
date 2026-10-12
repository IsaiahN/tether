"""A slot bet on before an action and no longer listed after it (the reviewer 2026-10-12 16:12 CDT).
Game-free: a gridworld whose listing drops one slot after its first step. The miss is charged at
the alphabet the bet was made under; the alphabet re-read after the step (F507) still governs
every slot listed now.

  v1 MUST-PASS: the step runs; the vanished slot's bet row is marked vanished, its alphabet field
     is the pre-step alphabet for that slot, and its mass is log2 of it.
  v2 every slot still listed is priced under the re-read alphabet (F507's half kept).
  v3 MUST-FAIL, the defect reintroduced: the same world on a tree whose gone branch reads the
     post-step alphabet (the pinned 016770e worktree, passed as argv[1]) raises KeyError on the
     vanished slot. Skipped, and said so, when no such tree is given.

    python test_vanish.py [path-to-a-tree-with-the-defect]
"""
from __future__ import annotations

import json
import math
import os
import subprocess
import sys

sys.dont_write_bytecode = True

SLOT = "o4.row"

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
tree, slot = sys.argv[1], sys.argv[2]
sys.path = [tree] + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")]
import gamma, gridworld, ledger, tether, world

class Vanish(gridworld.GridWorld):
    """After its first step this world no longer lists one slot."""
    def _hide(self):
        return self._steps >= 1
    def slots(self):
        return [s for s in super().slots() if not (self._hide() and s == slot)]
    def alphabet(self):
        a = super().alphabet()
        if isinstance(a, dict) and self._hide():
            a = {k: v for k, v in a.items() if k != slot}
        return a
    def observe(self):
        o = super().observe()
        if self._hide():
            o.pop(slot, None)
        return o

g = gridworld.family("default", 0)
pre = dict(g.alphabet()) if isinstance(g.alphabet(), dict) else None
g.__class__ = Vanish
env = world.bind(g)
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="vanish"), tether.Config(), ledger.Ledger())
err = None
try:
    ag.step()
except KeyError as e:
    err = repr(e)
rows = [r for r in ag.led.rows() if r.get("event") == "bet" and r.get("cycle") == 0]
post = dict(env.alphabet()) if isinstance(env.alphabet(), dict) else None
print(json.dumps({"err": err, "rows": rows, "pre": pre, "post": post}, default=str))
'''


def _run(tree: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    out = subprocess.run([sys.executable, "-c", PROBE, tree, SLOT], env=env,
                         capture_output=True, text=True, timeout=300)
    assert out.returncode == 0, out.stderr[-2000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    new = _run(here)
    assert new["err"] is None, new["err"]
    assert new["pre"] is not None and SLOT in new["pre"] and SLOT not in new["post"], "panel"
    gone = [r for r in new["rows"] if r["slot"] == SLOT]
    assert len(gone) == 1, f"the vanished slot was not bet on at cycle 0 ({len(gone)})"
    d = gone[0]["detail"]
    # v1
    assert d.get("vanished") is True, d
    assert d["alphabet"] == new["pre"][SLOT], (d["alphabet"], new["pre"][SLOT])
    assert abs(d["mass"] - math.log2(new["pre"][SLOT])) < 1e-9, d
    # v2
    listed = [r for r in new["rows"] if r["slot"] != SLOT and r["slot"] in new["post"]]
    assert listed and all(r["detail"]["alphabet"] == new["post"][r["slot"]] for r in listed)
    # v3
    if len(sys.argv) > 1:
        old = _run(sys.argv[1])
        assert old["err"] is not None and SLOT in old["err"], old["err"]
        v3 = f"the defect tree raises {old['err']}"
    else:
        v3 = "v3 SKIPPED (no defect tree given)"
    print(f"test_vanish: pass ({SLOT} priced at log2({new['pre'][SLOT]}) = {d['mass']:.3f}; "
          f"{len(listed)} listed slots under the re-read; {v3})")


if __name__ == "__main__":
    main()
