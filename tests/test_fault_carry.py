"""ITEM 4, THE LEARNING WRITTEN ON AN AGENT FAULT (TETHER_ERROR_CARRY; the design post 2026-10-22
15:14, the reviewer 15:17 (C3)). arc_holdout.play's real loop on the fake game (FakeWrapper
through a stub Arcade), over a two-game fake lineage, with a step that raises KeyError at step K.

  F1   ON: the KeyError still reaches the caller; one "@run" "agent_fault" row (type, site, cycle)
       and the whole traceback beside the ledger; ONE new generation, "ended": "agent_fault", which
       a fresh load reads as its head
  C3   the faulted cycle's own stamped entries are not in that generation: a term whose residual is
       stamped "@<faulted cycle>" and an invention born in it are left out; the ones stamped one
       cycle earlier are written (the planted pair is the precondition)
  PE   (C3)'s load row: the next life's load writes ONE "parent_ended" row naming the faulted tip
       and its error; the play's own load over normal parents writes none (the control), and one
       normal game later the next load writes none; on the store path and on the chain path
  RB   a generation that does not read back (lineage._readback planted False) is not written
  OFF  TETHER_ERROR_CARRY off: the KeyError reaches the caller and no generation is written (the
       defect)

    python tests/test_fault_carry.py
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
K = 3

SEED = r'''
import os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
sys.path.insert(1, os.path.join(sys.argv[1], "tests"))
import arc_holdout, lineage, tether
from test_entry import FakeWrapper
tether._AGENT_SEED = False
d = sys.argv[2]
for _g in range(2):
    env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake", lineage_dir=d)
    for _ in range(4):
        env.observe()
        ag.step()
    ag.end_run("cap")
    lineage.write(d, ag, "fake")
print("seeded")
'''

CHILD = r'''
import glob, json, os, pathlib, sys
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
sys.path.insert(1, os.path.join(sys.argv[1], "tests"))
import arc_holdout, lineage, lineage_store as ls, tether
from test_entry import FakeWrapper
tether._AGENT_SEED = False
d, led, k, mode = sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]


class Arc:
    def make(self, _game):
        return FakeWrapper(script={})


before = set(os.listdir(d))
real = tether.Agent.step
calls = [0]
plants = {}


def step(self, *a, **kw):
    calls[0] += 1
    if calls[0] == k and mode == "c3":
        # (C3)'s plants, REAL (the reviewer 16:52): two new 2-atom chains accepted, one stamped
        # with the faulted cycle and one with the cycle before; two invention records with a real
        # template, born in each. The generation must carry the earlier pair only, and still load.
        c = self.cycle
        new = [t for t in self.gamma.enumerate_closure("val", "val", 2, 4000, {})
               if len(t.atoms) == 2 and t.name not in self.gamma.library][:2]
        assert len(new) == 2, "C3: precondition: two new chains to plant"
        self.gamma.accept(new[0], seq=len(self.led), residual=f"o1.x@{c}")
        self.gamma.accept(new[1], seq=len(self.led), residual=f"o1.x@{c - 1}")
        plants["terms"] = {"now": new[0].name, "before": new[1].name}
        for nm, b in (("planted_now", c), ("planted_before", c - 1)):
            self._inv_carry.append({"name": nm, "template": "{o}.{r} > 0", "affects": [],
                                    "reading": "x", "term": nm, "then": [], "game": "fake",
                                    "born": b, "kind": "condition"})
    if calls[0] == k:
        raise KeyError("planted fault")
    return real(self, *a, **kw)


tether.Agent.step = step
if mode == "refuse":
    lineage._readback = lambda *_a: False
raised = None
try:
    arc_holdout.play("fake", 12, arc=Arc(), led_path=led, lineage_dir=d)
except KeyError as e:
    raised = str(e)
new = sorted(set(os.listdir(d)) - before)
gens = [n for n in new if n.startswith("gen_")]
out = {"raised": raised, "new_gens": gens, "faults": [], "tb": None, "gen": None, "head": None}
with open(led, encoding="utf-8") as fh:
    rows = [json.loads(x) for x in fh if x.strip()]
out["faults"] = [r["detail"] for r in rows if r["event"] == "agent_fault"]
out["tb"] = os.path.exists(led + ".fault1.txt")
if gens:
    g = json.loads(ls.file_bytes(pathlib.Path(d, gens[0])))
    out["gen"] = {"ended": g.get("ended"), "error": g.get("error"),
                  "inv": [r.get("name") for r in g.get("inventions", [])],
                  "terms": [r.get("residual") for r in g.get("terms", [])
                            if str(r.get("residual") or "").startswith("o1.x@")]}
    out["plants"] = plants
    tether.Agent.step = real
    env, ag, *_, loaded = arc_holdout.wire(FakeWrapper(script={}), "fake", lineage_dir=d)
    out["head"] = ag.lineage_parent
    out["lib_terms"] = sorted(n for n in plants.get("terms", {}).values() if n in ag.gamma.library)
    out["reinvented"] = ((loaded or {}).get("lineage") or {}).get("inventions_in")
    out["gen_hash"] = gens[0][4:20]
    out["inv_carried"] = [{k: e.detail.get(k) for k in ("reinvented", "refused")}
                          for e in ag.led.by_event("invention_carried")]
    out["pe_fresh"] = [e.detail for e in ag.led.by_event("parent_ended")]
    out["pe_play"] = sum(r["event"] == "parent_ended" for r in rows)
    if mode == "on":
        # PE's must-fail: one more game, ended normally, on top; its next load names no fault
        if getattr(ag, "_dk_snap", None) is not None:
            ag._dk_snap.close()
        arc_holdout.play("fake", 12, arc=Arc(), led_path=led + ".next", lineage_dir=d)
        env, ag2, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake", lineage_dir=d)
        out["next_head"] = ag2.lineage_parent
        out["pe_next"] = len(ag2.led.by_event("parent_ended"))
print(json.dumps(out))
'''


def run(code: str, *args: str, **arms) -> object:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0", **arms)
    p = subprocess.run([sys.executable, "-B", "-c", code, HERE, *args], capture_output=True,
                       text=True, env=env, cwd=HERE, stdin=subprocess.DEVNULL, timeout=900)
    assert p.returncode == 0, p.stderr[-3000:]
    return p.stdout.strip().splitlines()[-1]


def fresh() -> str:
    d = tempfile.mkdtemp(prefix="fault_")
    assert run(SEED, d) == "seeded"
    return d


def pe_check(r: dict, tag: str) -> None:
    assert r["pe_play"] == 0, (f"{tag}: control: a load over normal parents wrote parent_ended", r)
    pe = r["pe_fresh"]
    assert len(pe) == 1 and pe[0]["parent"] == r["gen_hash"], (f"{tag}: the fresh load", r)
    assert pe[0]["ended"] == "agent_fault" and "planted fault" in pe[0]["error"], (tag, pe)
    assert r["next_head"] not in (None, r["gen_hash"]) and r["pe_next"] == 0, (f"{tag}: next", r)
    print(f"  {tag} the play's load over normal parents: 0 parent_ended rows; the fresh load over "
          f"the faulted one: 1, naming {pe[0]['parent']} and its error; one normal game later "
          f"(head {r['next_head']}): 0")


def main() -> int:
    d = fresh()
    led = os.path.join(tempfile.mkdtemp(), "f.jsonl")
    r = json.loads(run(CHILD, d, led, str(K), "on"))
    assert r["raised"] and "planted fault" in r["raised"], ("F1: the fault did not reach", r)
    assert len(r["faults"]) == 1 and r["faults"][0]["type"] == "KeyError", r["faults"]
    assert r["faults"][0]["site"] and r["tb"], ("F1: site / traceback file", r)
    assert len(r["new_gens"]) == 1 and r["gen"]["ended"] == "agent_fault", ("F1", r)
    assert r["head"] == r["gen_hash"], ("F1: a fresh load does not read it as head", r)
    print(f"  F1 the KeyError reached the caller; agent_fault row at {r['faults'][0]['site']}; "
          f"traceback kept; generation {r['gen_hash']} ended agent_fault, read as the head")
    pe_check(r, "PE (store)")
    d = fresh()
    led = os.path.join(tempfile.mkdtemp(), "f.jsonl")
    r = json.loads(run(CHILD, d, led, str(K), "on", TETHER_MEMORY_STORE="0"))
    pe_check(r, "PE (chain)")
    d = fresh()
    led = os.path.join(tempfile.mkdtemp(), "f.jsonl")
    r = json.loads(run(CHILD, d, led, str(K), "c3"))
    assert r["gen"] is not None, ("C3: precondition: no generation written", r)
    inv, terms = r["gen"]["inv"], r["gen"]["terms"]
    assert "planted_before" in inv and "planted_now" not in inv, ("C3 inventions", inv)
    assert len(terms) == 1, ("C3 terms: the earlier one written, the faulted one not", terms)
    pl = r["plants"]["terms"]
    assert r["head"] == r["gen_hash"], ("C3: the generation with real plants must load", r)
    assert r["lib_terms"] == [pl["before"]], ("C3: a fresh load holds the earlier term only", r)
    print(f"  C3 the faulted cycle's own entries left out (inventions {inv}; terms {terms}); a "
          f"fresh load reads it as the head and holds {pl['before']} and not {pl['now']}; "
          f"re-invented {r['reinvented']}; the invention_carried row {r['inv_carried']}")
    d = fresh()
    led = os.path.join(tempfile.mkdtemp(), "f.jsonl")
    r = json.loads(run(CHILD, d, led, str(K), "refuse"))
    assert r["raised"] and r["new_gens"] == [], ("RB: an unreadable generation was written", r)
    print("  RB a generation that does not read back is not written")
    d = fresh()
    led = os.path.join(tempfile.mkdtemp(), "f.jsonl")
    r = json.loads(run(CHILD, d, led, str(K), "on", TETHER_ERROR_CARRY="0"))
    assert r["raised"] and r["new_gens"] == [] and not r["faults"], ("MF-OFF", r)
    print("  OFF TETHER_ERROR_CARRY off: the KeyError reached the caller, no generation")
    print("fault carry: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
