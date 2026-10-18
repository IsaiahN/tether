"""THE ASKED RECORD ON THE SLOT PATH, ACROSS PROCESSES (the reviewer 2026-10-18 07:15; Isaiah 04:20
"rebuilt ... from general"). Under C4's REACH-SHARE (5987421) no pair is promoted, so no whole is
held and the record's whole path (test_asked_record) has nothing to rebuild; a recorded question is
met on the SLOT path and rebuilt from the carried, live-checked held index. The 3-action fake game
through tether_agent.run with a lineage folder, all defaults, each process its own.

  W    process 1 plays and writes; a digest of every slot answer it held, by (entry, role, o, x,
       slot), in a side file. --fold: a level advance before the write, so the answers a fold
       cleared are digested at the fold (the asked keys the fold kept are in the record).
  R    process 2 loads and plays: recorded slot questions met at their first ask > 0
       (precondition); every slot answer it holds for a question process 1 held equals process
       1's, digest for digest; the count and process 2's play time reported.
  MF   process 2 again with (o, x) swapped where answers are bound: the comparison goes red.

    python test_asked_slot.py [--fold]
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

CHILD = r"""
import hashlib, json, sys, time
sys.dont_write_bytecode = True
import lineage, tether, tether_agent
tether._AGENT_SEED = False   # C-seed-X: two separately born agents, one temperament
from test_entry import FakeWrapper
from test_index_hold import _form
ROLE, D, SIDE, FOLD = {role!r}, {d!r}, {side!r}, {fold!r}
digests = {{}}
def digest(rows):
    return hashlib.sha256(repr([(_form(a), _form(b)) for _c, a, b in rows]).encode()).hexdigest()
def snap():
    for k, v in list(tether._BOUND_SLOT_MEMO.items()):
        digests[json.dumps(list(k[2:]))] = digest(v)
if hasattr(tether.Agent, "_consolidate"):
    real_fold = tether.Agent._consolidate
    def fold(self, trigger):
        snap()   # the answers a fold clears, digested before it clears them
        return real_fold(self, trigger)
    tether.Agent._consolidate = fold
if ROLE == "mf":   # the defect planted: answers bound with o and x swapped
    real_sub = tether._ph_sub
    tether._ph_sub = lambda t, o, x: real_sub(t, o=x, x=o)
class Advance(FakeWrapper):
    def _frame(self, state):
        f = super()._frame(state)
        if FOLD and self.n >= 2:
            f.levels_completed = 1
        return f
t0 = time.perf_counter()
r = tether_agent.run(Advance(), "g0", 3, lineage_dir=D)
wall = round(time.perf_counter() - t0, 2)
snap()
out = {{"slots": len(digests), "slot_met": lineage._AK_N["slot"],
        "whole_met": lineage._AK_N["whole"],
        # every key this process wrote to ak_, over all its generations (a boundary write after
        # a level end records the kept keys; the last write then holds only the new ones)
        "asked": len(lineage._AK_CARRIED.get(str(__import__("pathlib").Path(D).resolve()), ())),
        "asked_last": ((r.get("lineage") or {{}}).get("asked") or {{}}).get("entries"),
        "wall_s": wall}}
if ROLE == "w":
    json.dump(digests, open(SIDE, "w"))
else:
    w = json.load(open(SIDE))
    common = [k for k in digests if k in w]
    out.update(common=len(common), differ=sum(1 for k in common if digests[k] != w[k]))
print("OUT " + json.dumps(out, default=repr))
"""


def _run(code: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    r = subprocess.run([sys.executable, "-B", "-c", code], env=env, capture_output=True,
                       text=True, check=False, stdin=subprocess.DEVNULL,
                       cwd=os.path.dirname(os.path.abspath(__file__)))
    assert r.returncode == 0, r.stderr[-3000:]
    out = [ln for ln in r.stdout.splitlines() if ln.startswith("OUT ")]
    return json.loads(out[-1][4:])


def main() -> None:
    fold = "--fold" in sys.argv
    d = Path(tempfile.mkdtemp(prefix="aks_"))
    side = str(d.parent / (d.name + "_slots.json"))
    w = _run(CHILD.format(role="w", d=str(d), side=side, fold=fold))
    assert w["asked"] and w["slots"], ("W: nothing recorded or held", w)
    print(f"  W{' (with a level-end fold before the write)' if fold else ''}: ak_ {w['asked']} "
          f"entries; {w['slots']} slot answers digested")
    r = _run(CHILD.format(role="r", d=str(d), side=side, fold=False))
    assert r["slot_met"] > 0, ("precondition: no recorded slot question met at its first ask", r)
    assert r["common"] > 0 and r["differ"] == 0, ("R: a rebuilt slot answer differs", r)
    print(f"  R: {r['slot_met']} recorded slot questions met at their first ask; "
          f"{r['common']} slot "
          f"answers compared with process 1, all equal; process 2 played in {r['wall_s']} s")
    mf = _run(CHILD.format(role="mf", d=str(d), side=side, fold=False))
    assert mf["common"] > 0 and mf["differ"] > 0, ("MF MUST-FAIL did not fail: (o, x) swapped", mf)
    print(f"  MF must-fail fired: with (o, x) swapped, {mf['differ']} of {mf['common']} differ")
    print("asked slot: OK")


if __name__ == "__main__":
    main()
