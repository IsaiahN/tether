"""15 RETIRE_HOLDER (TETHER_RETIRE_HOLDER, default ON; the reviewer r466 1(c), r470). The fixture is
test_instance_retire's: a fake game, one "reuse:" composition per object, then a board on which only
o4 is re-found. A FIXTURE-ONLY SPY, just before the break's retire, plants o1's instance (which the
break retires) in D5's three holders on surviving slots of o4: a pending split's incumbent, a cut
candidate's incumbent, and a split's part A -- as round 8 had it, a cut confirmed the cycle before
the break. Then the break's step (its D5 split runs) and one more step (its _present reads bound).
Each check runs in its own process.
  check_mustfail_off  OFF: the pending split writes the retired name back into bound and the next
                      _present raises KeyError at its orphan scan
  check_hold_on       ON: all three holders name the instance's kind (the split kept, part A
                      re-pointed, never dropped while the kind is live), bound names the kind,
                      dangling [], both steps run, gate pass
  check_off_identity  MUST-HOLD: TETHER_RETIRE_HOLDER=0 (off_env) byte-equal to 9eb4012 on the fake
                      whole run
    python tests/test_retire_holder.py [check ...]
"""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
from test_contact_first import _child, _norm  # noqa: E402  the same probe and masks

sys.dont_write_bytecode = True

BASE = "9eb4012"        # 12 STOP_READ_STEP, before 15

PROBE = r'''
import json, sys, traceback
sys.dont_write_bytecode = True
tree = sys.argv[1]
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import numpy as np
from arcengine import GameState
import arc_holdout, gate, tether
from gamma import Term
from test_entry import FakeWrapper

def after_board():
    g = np.zeros((64, 64), dtype=int)
    g[5:9, 5:9] = 1          # the static piece, recoloured: not re-found
    g[50:52, 50:56] = 4      # left exactly in place: re-found
    g[15:20, 40:45] = 5
    g[20:22, 20:30] = 6
    return g

class Two(FakeWrapper):
    def __init__(self):
        self.new = None
        super().__init__()

    def _frame(self, state):
        f = super()._frame(state)
        if self.new is None:
            g = f.frame[0].copy()
            g[40:43, 10:15] = 2
            g[50:52, 50:56] = 4
        else:
            g = self.new()
        f.frame = [g]
        return f

w = Two()
env, ag, led, *_ = arc_holdout.wire(w, "fake")
for _ in range(3):
    ag.step()
ag.gamma.keep_evidence = True
lib = ag.gamma.library
atoms = lib["translate"].atoms + lib["recolour"].atoms
owners = sorted({s.split(".")[0] for s in ag.slots if "." in s and "~" not in s
                 and not s.startswith("@")})
names = {}
for o in owners:
    if f"{o}.row" in ag.slots and f"{o}.col" in ag.slots:
        names[o] = ag._install_reuse(Term(atoms, operand=f"{o}.row"), f"{o}.col")
        ag.gamma.settle(names[o], "w", f"{o}.col")
kind = Term(atoms).name
inst = names["o1"]
other = [s for s in sorted(ag.slots) if s.startswith("o4.") and s not in ("o4.col", "o4.row")][0]
real_retire = type(ag)._retire_instances

def spied(self, *a, **k):
    # FIXTURE-ONLY SPY (never an arm): D5's three holders name the instance the break retires
    self._d5_pending["o4.col"] = (tether.ACTED_SELF, {}, inst)
    self._d5_candidates["o4.row"] = (tether.ACTED_SELF, {}, inst)
    self._parts[other] = {"P": tether.ACTED_SELF, "A": inst, "B": None}
    res = real_retire(self, *a, **k)
    out["after_retire"] = {
        "pending": {s: c[2] for s, c in self._d5_pending.items()},
        "candidate": {s: c[2] for s, c in self._d5_candidates.items()},
        "parts": {s: [p.get("A"), p.get("B")] for s, p in self._parts.items()}}
    return res

out = {"inst": inst, "kind": kind, "other": other}
type(ag)._retire_instances = spied
w.new = after_board
w._frame(GameState.NOT_FINISHED)
assert env.arrive()
out["identity"] = env.identity("o1")
for i in range(2):
    try:
        ag.step()
    except KeyError as e:
        tb = traceback.extract_tb(e.__traceback__)[-1]
        out["raised"] = [i, repr(e), f"{tb.name}:{tb.lineno}"]
        break
    if i == 0:
        out["split_o4col"] = [ag.bound.get("o4.col"), (ag._parts.get("o4.col") or {}).get("A")]
rows = ag.led.rows()
out["retired"] = sorted(ag.gamma.retired)
out["kind_live"] = kind in ag.gamma.library
out["ir"] = [r["detail"] for r in rows if r["event"] == "instance_retired"]
out["splits"] = [r["detail"] for r in rows if r["event"] == "split"]
v = gate.check(rows)
out["gate"] = [v["verdict"], v.get("check"), v.get("token")]
print(json.dumps(out, default=str))
'''


def _probe(arm: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               TETHER_RETIRE_HOLDER=arm)
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, str(_repo.ROOT)], env=env,
                         capture_output=True, text=True, timeout=900, cwd=str(_repo.ROOT),
                         stdin=subprocess.DEVNULL)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def check_mustfail_off() -> None:
    r = _probe("0")
    assert r["inst"] in r["retired"], ("occasion: the planted instance was not retired", r)
    # the retired name comes back out of a D5 holder; where it is first read depends on whether
    # the slot bets this step (_d5_select writes A into bound before the bet) or not (the split's
    # restore, read by the next _present, as in round 8)
    assert r.get("raised") and r["inst"] in r["raised"][1], (
        "MUST-FAIL: OFF should raise KeyError on the retired name", r.get("raised"))
    print(f"  OFF: {r['inst']!r} retired at the break, then read back out of a D5 holder; "
          f"step {r['raised'][0] + 1} from the break raised {r['raised'][1]} at {r['raised'][2]}")


def check_hold_on() -> None:
    r = _probe("1")
    k, a = r["kind"], r["after_retire"]
    assert r["inst"] in r["retired"] and r["kind_live"], ("occasion", r["retired"], r["kind_live"])
    assert not r.get("raised"), ("ON raised", r["raised"])
    assert r["ir"] and r["ir"][-1]["dangling"] == [], r["ir"]
    # at the break: every holder names the kind, none dropped while the kind is live
    assert a["pending"].get("o4.col") == k and a["candidate"].get("o4.row") == k, a
    assert a["parts"].get(r["other"]) == [k, None], ("the live split kept, A re-pointed", a)
    assert not any(r["inst"] in json.dumps(v) for v in a.values()), a
    # the pending split then ran on the kind, and the slot's binding names it
    sp = [d for d in r["splits"] if d["split_slot"] == "o4.col"]
    assert sp and sp[0]["part_a"] == k, ("the split ran on the kind", sp, k)
    assert r["split_o4col"][0] == k, ("bound o4.col names the kind", r["split_o4col"], k)
    assert r["gate"][0] == "pass", r["gate"]
    print(f"  ON: {r['inst']!r} retired; at the break pending o4.col, candidate o4.row and part "
          f"{r['other']} all name {k!r} (kept, not dropped); the split ran with A = bound = kind; "
          f"dangling []; both steps ran; repointed {r['ir'][-1]['repointed']}, dropped "
          f"{r['ir'][-1]['dropped']}; gate pass")


def check_off_identity() -> None:
    import tarfile
    import tempfile

    from _batch import off_env
    root = str(_repo.ROOT)
    with tempfile.TemporaryDirectory() as d:
        tar = subprocess.run(["git", "-C", root, "archive", BASE], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        base = _norm(_child(d))
    off = _norm(_child(root, off_env("TETHER_RETIRE_HOLDER")))
    diff = sum(1 for x, y in zip(base, off, strict=False) if x != y) + abs(len(base) - len(off))
    assert len(base) > 50 and diff == 0, ("OFF", len(base), len(off), next(
        (i for i, (x, y) in enumerate(zip(base, off, strict=False)) if x != y), None))
    print(f"  OFF (TETHER_RETIRE_HOLDER=0, fake): {len(base)} rows against {BASE}, 0 differences")


def main() -> int:
    want = sys.argv[1:]
    names = [k for k in globals() if k.startswith("check_") and (not want or k in want)]
    assert not want or len(names) == len(want), ("unknown check name", sorted(want))
    if len(names) == 1:
        globals()[names[0]]()
        print("ok  ", names[0])
        return 0
    for n in names:
        r = subprocess.run([sys.executable, "-B", __file__, n], cwd=str(_repo.ROOT),
                           stdin=subprocess.DEVNULL)
        assert r.returncode == 0, n
    print(f"retire_holder: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
