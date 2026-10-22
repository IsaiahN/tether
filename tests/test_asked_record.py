"""C-S1g-1, THE ASKED RECORD (Isaiah 2026-10-15 13:26, option B; the reviewer 13:27). WRITTEN, NOT
RUN: it runs in the end-of-step-7 checklist. The harness is the 12:38 carry read's: the 3-action
fake game through tether_agent.run with a lineage folder, all defaults, each process its own.

  W    process 1 plays and writes: ak_ entries > 0; bm_ and bs_ write nothing. It saves a digest
       of every WHOLE it held, by (entry, role, o, x), in a side file.
  R    process 2 loads and plays: bound_slot_from_record > 0 (precondition); every whole it holds
       for a pair process 1 held equals process 1's whole, digest for digest; index unresolved 0.
  MF   in a fresh wired agent, for one held pair: a CONTROL rebuild with the full atoms equals
       process 1's digest (so the comparison can pass), and two MUST-FAILS differ from it: the
       rebuild under a swapped (o, x), and the rebuild under a WRONG SIGNATURE (one atom the whole
       uses removed from the atoms the held view is compiled from).
  R1   a record written under one signature still pends and rebuilds under another (process 2
       with one atom no recorded whole uses removed): from_record > 0, each whole equal to a fresh
       named compile under the new atoms. MF-R1: the old signature-filtered load pends nothing.

    python tests/test_asked_record.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

CHILD = r"""
import hashlib, json, sys
sys.dont_write_bytecode = True
import lineage, tether, tether_agent
from test_entry import FakeWrapper
from test_index_hold import _form
ROLE, D, SIDE = {role!r}, {d!r}, {side!r}
r = tether_agent.run(FakeWrapper(), "g0", 3, lineage_dir=D)
def digest(whole):
    return hashlib.sha256(repr([(_form(a), _form(b)) for _c, a, b in whole]).encode()).hexdigest()
wholes = {{json.dumps(list(k[2:])): digest(v) for k, v in tether._BOUND_MEMO.items()}}
used = {{json.dumps(list(k[2:])): sorted({{t.name for _c, a, _b in v
                                          if a is not None and hasattr(a, "term")
                                          for t in a.term.atoms}})
        for k, v in tether._BOUND_MEMO.items()}}
gen = r.get("lineage") or {{}}
out = {{"asked": (gen.get("asked") or {{}}).get("entries"),
        "bm": (gen.get("memo") or {{}}).get("entries"),
        "bs": (gen.get("slot_memo") or {{}}).get("entries"),
        "from_record": tether._INDEX_N["bound_slot_from_record"],
        "index": dict(lineage._RESOLVE), "wholes": len(wholes)}}
if ROLE == "w":
    json.dump({{"wholes": wholes, "used": used}}, open(SIDE, "w"))
else:
    w = json.load(open(SIDE))["wholes"]
    common = [k for k in wholes if k in w]
    out.update(common=len(common), differ=sum(1 for k in common if wholes[k] != w[k]))
print("OUT " + json.dumps(out, default=repr))
"""

MFCHILD = r"""
import hashlib, json, sys
sys.dont_write_bytecode = True
from functools import partial
import arc_holdout, compile_term, tether
from test_entry import FakeWrapper
from test_index_hold import _form
SIDE = {side!r}
side = json.load(open(SIDE))
k = next(k for k, u in side["used"].items() if u)
key, role, o, x = json.loads(k)
env, ag, *_ = arc_holdout.wire(FakeWrapper(), "g0")
lib = tether._library()
def rebuild(atoms, o, x):
    held = ag._held_index(lib, key, role, atoms, compile_term.signature(atoms))
    sub = partial(tether._ph_sub, o=o, x=x)
    return tuple((c, tether._bound(a, sub, atoms), tether._bound(b, sub, atoms))
                 for c, a, b in held)
def digest(whole):
    return hashlib.sha256(repr([(_form(a), _form(b)) for _c, a, b in whole]).encode()).hexdigest()
full = {{a.name: a for a in ag.gamma.atoms}}
want = side["wholes"][k]
gone = side["used"][k][0]
narrow = {{n: a for n, a in full.items() if n != gone}}
try:
    sig_differs = digest(rebuild(narrow, o, x)) != want
except KeyError:   # a term naming the removed atom cannot be rebuilt at all: it differs
    sig_differs = True
print("OUT " + json.dumps({{"control_equal": digest(rebuild(full, o, x)) == want,
                            "swap_differs": digest(rebuild(full, x, o)) != want,
                            "sig_differs": sig_differs, "pair": k, "gone": gone}}))
"""

RSCHILD = r"""
import json, sys
sys.dont_write_bytecode = True
import arc_holdout, gamma, lineage, tether
from test_entry import FakeWrapper
from test_index_hold import _form, _named
D, SIDE, MF = {d!r}, {side!r}, {mf!r}
used = {{n for u in json.load(open(SIDE))["used"].values() for n in u}}
real_init, gone = gamma.Gamma.__init__, []
def init(self, atoms, *a, **k):
    atoms = list(atoms)
    if not gone:
        gone.append(next(t.name for t in reversed(atoms) if t.name not in used))
    real_init(self, [t for t in atoms if t.name != gone[0]], *a, **k)
gamma.Gamma.__init__ = init
if MF:   # the defect reintroduced: the signature-filtered load
    real_mb = lineage._memo_bodies
    lineage._memo_bodies = lambda p, f, sig, chain, rep, any_sig=False: real_mb(p, f, sig,
                                                                               chain, rep)
env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "g0", lineage_dir=D)
pending = len(lineage._AK_PENDING)
for _ in range(30):
    ag.step()
memo = tether._BOUND_MEMO if ag._atoms_token else ag._bound_cache
lib = tether._library()
atoms = {{a.name: a for a in ag.gamma.atoms}}
bad = 0
for (_t, _sig, key, role, o, x), v in memo.items():
    if ([(_form(a), _form(b)) for _c, a, b in v]
            != [(_form(a), _form(b)) for _c, a, b in _named(lib, key, role, o, x, atoms)]):
        bad += 1
print("OUT " + json.dumps({{"gone": gone[0] if gone else None, "pending": pending,
                            "from_record": tether._INDEX_N["bound_slot_from_record"],
                            "checked": len(memo), "bad": bad}}))
"""


def _run(code: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    r = subprocess.run([sys.executable, "-B", "-c", code], env=env, capture_output=True,
                       text=True, check=False, stdin=subprocess.DEVNULL)
    assert r.returncode == 0, r.stderr[-3000:]
    out = [ln for ln in r.stdout.splitlines() if ln.startswith("OUT ")]
    return json.loads(out[-1][4:])


def main() -> None:
    d = Path(tempfile.mkdtemp(prefix="ak_"))
    side = str(d.parent / (d.name + "_wholes.json"))
    w = _run(CHILD.format(role="w", d=str(d), side=side))
    assert w["asked"] and not w["bm"] and not w["bs"], ("W: ak_ written, bm_/bs_ empty", w)
    print(f"  W: ak_ {w['asked']} entries; bm_ {w['bm']}, bs_ {w['bs']}; {w['wholes']} wholes")
    r = _run(CHILD.format(role="r", d=str(d), side=side))
    assert r["from_record"] > 0, ("precondition: no whole was rebuilt from the record", r)
    assert r["common"] > 0 and r["differ"] == 0, ("R: a rebuilt whole differs", r)
    assert r["index"]["unresolved"] == 0, r
    print(f"  R: {r['from_record']} wholes rebuilt from the record; {r['common']} compared with "
          "process 1, all equal")
    mf = _run(MFCHILD.format(side=side))
    assert mf["control_equal"], ("the control rebuild differs: the MF cannot discriminate", mf)
    assert mf["swap_differs"], ("MF MUST-FAIL did not fail: a swapped (o, x) rebuilt the same", mf)
    assert mf["sig_differs"], ("MF MUST-FAIL did not fail: a wrong signature rebuilt the same", mf)
    print(f"  MF must-fail fired on {mf['pair']}: the control equals process 1; a swapped (o, x) "
          f"and a signature without {mf['gone']} differ")
    # R1 (the reviewer 2026-10-15 13:47): a record written under one signature pends and rebuilds
    # under another (here one atom no recorded whole uses is removed); the old signature-filtered
    # load leaves it unpended
    rs = _run(RSCHILD.format(d=str(d), side=side, mf=False))
    assert rs["gone"] and rs["pending"] > 0 and rs["from_record"] > 0, ("R1: not rebuilt", rs)
    assert rs["checked"] > 0 and rs["bad"] == 0, ("R1: a rebuild differs from a fresh compile", rs)
    rm = _run(RSCHILD.format(d=str(d), side=side, mf=True))
    assert rm["pending"] == 0 and rm["from_record"] == 0, ("MF-R1 MUST-FAIL did not fail", rm)
    print(f"  R1: without {rs['gone']} the record still pends ({rs['pending']}) and rebuilds "
          f"({rs['from_record']}), each equal to a fresh compile; MF-R1 fired: the filtered "
          "load pends nothing")
    print("asked record: OK")


if __name__ == "__main__":
    main()
