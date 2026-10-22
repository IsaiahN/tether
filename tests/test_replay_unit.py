"""R7i, THE REPLAY REACHES BOUND AND GUARDED TERMS, TETHER_REPLAY_UNIT (the reviewer 2026-10-17
19:50).

  R   process 1 plays the fake ARC game (12 actions, C-seed-X) into a lineage folder; the agent
      settles and refutes its own guarded, bound terms there (recolour<o0.colour>?ACTED_SELF ...).
      Process 2 loads it: no settle / refute row is not_held, and each reloaded term holds the paid
      of every process-1 term that reloaded onto it
  D   none of the replayed targets is innate (7i 1a / 1b: learned, revisable), and a process-1
      term the evidence left unsettled arrives unsettled -- on the fake all three end settled, so
      that half is vacuous here; test_settled_core I6b demotes a bound learned recipe exactly
  MF  TETHER_REPLAY_UNIT=0 (by name, as before): every settle / refute row is not_held and process 2
      holds no paid

    python tests/test_replay_unit.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
HERE = _repo.ROOT

CHILD = r'''
import json, os, sys, tempfile
sys.dont_write_bytecode = True
import arc_holdout, lineage, tether
from test_entry import FakeWrapper
tether._AGENT_SEED = False
mode, d = sys.argv[1], sys.argv[2]
led = os.path.join(tempfile.mkdtemp(), "r.jsonl")
env, ag, _l, _b, _p, loaded = arc_holdout.wire(FakeWrapper(script={}), "fake", led_path=led,
                                               lineage_dir=d)
g = ag.gamma
out = {}
if mode == "p1":
    for _ in range(12):
        env.observe()
        ag.step()
        if env.terminal():
            break
    ev = [r for r in g.evidence if r[0] in ("settle", "refute")]
    names = sorted({r[1] for r in ev})
    out.update(rows=len(ev), terms={n: {"paid": sum(g.standing[n].paid.values()),
                                        "settled": g.is_settled(n)} for n in names})
    ag.end_run("cap")
    lineage.write(d, ag, "fake")
else:
    rep = loaded.get("lineage", loaded)
    out["replayed"] = rep.get("replayed")
    out["renamed"] = dict(g.renamed)
    out["held"] = {n: {"paid": sum(st.paid.values()), "settled": st.settled,
                       "innate": n in g.innate}
                   for n, st in g.standing.items() if n in set(g.renamed.values())}
print("RESULT", json.dumps(out))
'''


def child(mode: str, d: str, arm: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "TETHER_REPLAY_UNIT": arm})
    p = subprocess.run([sys.executable, "-B", "-c", CHILD, mode, d], capture_output=True,
                       text=True, env=env, cwd=HERE, stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    line = next(x for x in p.stdout.splitlines() if x.startswith("RESULT "))
    return json.loads(line[len("RESULT "):])


def main() -> int:
    d = tempfile.mkdtemp()
    p1 = child("p1", d, "1")
    assert p1["rows"] and any(t["paid"] for t in p1["terms"].values()), p1                # pre
    p2 = child("p2", d, "1")
    rp, ren = p2["replayed"], p2["renamed"]
    assert rp["not_held"] == 0 and rp["settle"] + rp["refute"] == p1["rows"], (rp, p1["rows"])  # R
    want: dict = {}
    for n, t in p1["terms"].items():
        want[ren.get(n, n)] = want.get(ren.get(n, n), 0) + t["paid"]
    got = {n: h["paid"] for n, h in p2["held"].items()}
    assert all(got.get(n, 0) == w for n, w in want.items()), (want, got)
    print("R", p1["rows"], "settle/refute rows from process 1 on", len(p1["terms"]), "bound "
          "terms; process 2 replayed", rp, "; paid by reloaded term", got)
    uns = [n for n, t in p1["terms"].items() if not t["settled"]]
    assert all(not p2["held"][ren[n]]["settled"] for n in uns if ren.get(n) in p2["held"]), p2
    assert not any(h["innate"] for h in p2["held"].values()), p2["held"]                   # D
    print("D", len(uns), "process-1 terms left unsettled arrive unsettled; no replayed target is "
          "innate")
    d0 = tempfile.mkdtemp()
    child("p1", d0, "0")
    q2 = child("p2", d0, "0")
    qr = q2["replayed"]
    assert qr["settle"] == qr["refute"] == 0 and qr["not_held"] == p1["rows"], qr          # MF
    print("MF by name only: replayed", qr, "-- every row not_held, as before")
    print("replay_unit: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
