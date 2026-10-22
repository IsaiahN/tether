"""THE CAP ENDS A STEP BETWEEN LOOKUPS, TETHER_CAP_MIDSTEP (the reviewer 2026-10-17 10:47, 11:35).
gridworld_s2 (C-seed-X): an agent steps until its library route runs, then its deadline is set in
the past and it steps again.

  P1 the step ends between lookups: no exception escapes, one ROUTE "@cap" cap_mid_step row with
     its overrun_s (wall at the cap minus the deadline, >= 0), and no library row after the deadline
  P2 the record still flushes: lineage.write after the cap writes a generation carrying entry_use,
     and a fresh agent loads equal counts. The generation is read through lineage._read (the
     files are zlib under TETHER_COMPRESS); MF-P2: the old raw text read of the same file fails
  P3 the capped ledger passes gate.py: every live slot the cap left unsorted has its route row
     (CAP_UNREACHED), so the routing check still accounts for every residual
  MF-P1 TETHER_CAP_MIDSTEP=0: the same deadline is ignored inside the step (no cap row, library
     rows written after it)
  P4 THE CAP IN THE NON-LOOKUP REST (the reviewer 2026-10-17 16:56): budget 1 evaluation; the
     deadline passes as settle returns: the tail's read writes a cap row (at "tail") and the work
     after it (_promote) does not run -- the overrun is one unit of work
  P5 the deadline passes during the first mint: a cap row follows (at "mint" or "tail") and no
     further mint runs; each slot written cap_unminted OWES (in owed_import), and the cap row
     lists what the skipped rest carries and what it loses
  MF-P4 the cap read only at the lookup point (as before this fix): no cap row in that step, and
     the tail runs past the deadline

    python test_cap_midstep.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True

CHILD = r'''
import json, os, sys, tempfile
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.getcwd(), "conform"))
import gamma, ledger, lineage, panel, tether, world
g, seed = panel._gridworld("gridworld_s2")
env = world.bind(g)
d = tempfile.mkdtemp()
led = os.path.join(d, "gw.jsonl")
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"gate_{seed}"), tether.Config(),
                  ledger.Ledger(path=led))
def rows():
    return [json.loads(x) for x in open(led, encoding="utf-8")]
n = 0
while n < 12 and not any(r.get("event") == "library" for r in rows()):
    ag.step(); n += 1
before = len(rows())
ag.deadline = 0.0
acted = None
for _ in range(4):
    acted = ag.step()
after = rows()[before:]
cap = [r for r in after if r.get("event") == "cap_mid_step"]
libs = [r for r in after if r.get("event") == "library"]
out = {"warm_steps": n, "cap_rows": len(cap), "lib_after": len(libs), "acted": acted,
       "overrun": [r["detail"].get("overrun_s") for r in cap],
       "cap_slot": cap[0]["slot"] if cap else None, "led": led,
       "unreached": sum(1 for r in after if r.get("event") == "route"
                        and r["detail"].get("why_not") == tether.CAP_UNREACHED)}
if tether._ENTRY_USE and tether._CAP_MIDSTEP:
    ld = os.path.join(d, "lin")
    lineage.write(ld, ag, "gw")
    from pathlib import Path
    gens = lineage._read(Path(ld))      # the lineage's own reader: decompressed, hash-checked
    eu = next(iter(gens.values())).get("entry_use", {})
    raw = os.path.join(ld, next(f for f in os.listdir(ld) if f.startswith("gen_")))
    try:                                # MF-P2: the old raw text read of the same file
        json.loads(open(raw, encoding="utf-8").read())
        out["raw_read"] = "ok"
    except (UnicodeDecodeError, ValueError) as e:
        out["raw_read"] = type(e).__name__
    ag2 = tether.Agent(world.bind(panel._gridworld("gridworld_s2")[0]),
                       gamma.Gamma(env.atoms(), game=f"gate_{seed}"), tether.Config(),
                       ledger.Ledger(path=os.devnull))
    lineage.load(ld, ag2)
    out.update(written=len(eu), loaded=len(ag2._entry_use_in),
               equal=all(ag2._entry_use_in.get(k, {}).get(f) == v for k, c in ag._entry_use.items()
                         for f, v in c.items()))
print(json.dumps(out))
'''


CHILD_REST = r'''
import json, os, sys, tempfile
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.getcwd(), "conform"))
import gamma, gate, ledger, panel, tether, world
mode = sys.argv[1]
tether._AGENT_SEED = False
tether.STEP_BUDGET = 1
g, seed = panel._gridworld("gridworld_s2")
env = world.bind(g)
led = os.path.join(tempfile.mkdtemp(), "r.jsonl")
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"gate_{seed}"), tether.Config(),
                  ledger.Ledger(path=led))
for _ in range(4):
    ag.step()
calls = {"promote_after": 0, "mint_after": 0}
fired = {"on": False}
if mode in ("tail", "lookup_only"):
    real_settle = tether.Agent.settle
    def settle(self, res):
        out = real_settle(self, res)
        self.deadline, fired["on"] = 0.0, True
        return out
    tether.Agent.settle = settle
if mode == "mint":
    real_mint = tether.Agent.mint
    def mint(self, slot, *a, **k):
        if fired["on"]:
            calls["mint_after"] += 1
        else:
            self.deadline, fired["on"] = 0.0, True
        return real_mint(self, slot, *a, **k)
    tether.Agent.mint = mint
real_promote = tether.Agent._promote
def promote(self, *a, **k):
    if fired["on"]:
        calls["promote_after"] += 1
    return real_promote(self, *a, **k)
tether.Agent._promote = promote
if mode == "lookup_only":
    real_due = tether.Agent._cap_due
    def due(self):
        return real_due(self) if sys._getframe(1).f_code.co_name == "_library_fit" else False
    tether.Agent._cap_due = due
n = 0
while not fired["on"] and n < 12:
    ag.step(); n += 1
rows = [json.loads(x) for x in open(led, encoding="utf-8")]
cap = [r for r in rows if r.get("event") == "cap_mid_step"]
print(json.dumps({"fired": fired["on"], "steps": n, "cap": [r["detail"].get("at") for r in cap],
                  "unminted": sum(1 for r in rows if r.get("event") == "cap_unminted"),
                  "owes": all(r["slot"] in ag.owed_import for r in rows
                              if r.get("event") == "cap_unminted"),
                  "lost": [r["detail"].get("lost") for r in cap][:1],
                  "gate": gate.check(rows)["verdict"], **calls}))
'''


def rest(mode: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    p = subprocess.run([sys.executable, "-B", "-c", CHILD_REST, mode], capture_output=True,
                       text=True, env=env, cwd=os.path.dirname(os.path.abspath(__file__)),
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-2000:]
    return json.loads(p.stdout.strip().splitlines()[-1])


def child(extra: dict) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", **extra})
    p = subprocess.run([sys.executable, "-B", "-c", CHILD], capture_output=True, text=True,
                       env=env, cwd=os.path.dirname(os.path.abspath(__file__)),
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-2000:]
    return json.loads(p.stdout.strip().splitlines()[-1])


def main() -> int:
    on = child({})
    assert on["cap_rows"] >= 1 and on["lib_after"] == 0 and on["cap_slot"] == "@cap", on   # P1
    assert all(isinstance(x, float) and x >= 0 for x in on["overrun"]), on["overrun"]
    assert on["written"] > 0 and on["loaded"] == on["written"] and on["equal"], on       # P2
    assert on["raw_read"] != "ok", on                                                     # MF-P2
    print("P1 cap row", on["cap_rows"], "library rows after the deadline", on["lib_after"],
          "; P2 entry_use written", on["written"], "loaded", on["loaded"], "equal", on["equal"],
          "; MF-P2 the raw text read of the generation fails:", on["raw_read"])
    g = subprocess.run([sys.executable, "-B", "gate.py", on["led"]], capture_output=True, text=True,
                       cwd=os.path.dirname(os.path.abspath(__file__)), stdin=subprocess.DEVNULL,
                       env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    verdict = json.loads(g.stdout)["verdict"]
    assert verdict == "pass", g.stdout[-600:]                                         # P3
    print("P3 gate on the capped ledger:", verdict, "; unreached route rows", on["unreached"])
    off = child({"TETHER_CAP_MIDSTEP": "0"})
    assert off["cap_rows"] == 0 and off["lib_after"] > 0, off                            # MF-P1
    print("MF-P1 OFF: cap rows", off["cap_rows"], "library rows after the deadline",
          off["lib_after"])
    t = rest("tail")
    assert t["fired"] and t["cap"] == ["tail"] and t["promote_after"] == 0, t           # P4
    assert t["gate"] == "pass", t
    print("P4 deadline passed at settle: cap row at", t["cap"], "; _promote after it:",
          t["promote_after"], "; gate", t["gate"])
    m = rest("mint")
    assert m["fired"] and m["cap"] and m["cap"][0] in ("mint", "tail") and m["mint_after"] == 0, m
    assert m["gate"] == "pass" and m["owes"] and m["lost"] and m["lost"][0], m
    print("P5 deadline passed in the first mint: cap row at", m["cap"], "; mints after it:",
          m["mint_after"], "; slots marked unminted:", m["unminted"], "; gate", m["gate"])  # P5
    lo = rest("lookup_only")
    assert lo["fired"] and not lo["cap"] and lo["promote_after"] > 0, lo               # MF-P4
    print("MF-P4 read at the lookup point only: cap rows", lo["cap"], "; _promote ran after the "
          "deadline", lo["promote_after"], "time(s)")
    print("cap_midstep: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
