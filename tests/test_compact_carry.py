"""C-S1f-1, THE LINEAGE WRITTEN COMPACT (the reviewer 2026-10-15 13:01). WRITTEN, NOT RUN: it
runs in the end-of-step-7 checklist. The harness is the 12:38 carry read's: the 3-action fake
game through tether_agent.run with a lineage folder, all defaults, each process its own.

  (a)  W_old writes a folder with lineage._dumps in the old indented form; W_new writes one as
       built (compact). A reader process loads each: the name-hash check passes on both (nothing
       unreadable, no raise), every load report (index installed, bm_ and bs_ pending, signature
       differences) is equal apart from its byte count, and the resolve counts of every family and
       a digest of every slot answer the reader is given, in order, are equal.
  (b)  the compact folder's idx / bm_ / bs_ files are smaller than the indented ones.

    python tests/test_compact_carry.py
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
MODE, D = {mode!r}, {d!r}
if MODE == "old":
    lineage._dumps = lambda x: json.dumps(x, sort_keys=True, indent=1).encode("utf-8")
digest = hashlib.sha256()
real = tether.Agent._compiled
def compiled(self, lib, key, role, o, x, comp, atoms, sig, slot=None, tally=None):
    got = real(self, lib, key, role, o, x, comp, atoms, sig, slot=slot, tally=tally)
    if slot is not None:
        got = list(got)
        digest.update(repr((key, role, o, x, slot,
                            [(_form(a), _form(b)) for _c, a, b in got])).encode("utf-8"))
    return got
tether.Agent._compiled = compiled
r = tether_agent.run(FakeWrapper(), "g0", 3, lineage_dir=D)
lin = (r.get("loaded") or {{}}).get("lineage") or {{}}
rep = {{k: ({{f: v for f, v in (lin.get(k) or {{}}).items() if f != "bytes"}}
            if isinstance(lin.get(k), dict) else lin.get(k))
       for k in ("index", "memo", "slot_memo")}}
print("OUT " + json.dumps({{"load": rep, "parent": lin.get("parent"),
                            "resolve": [dict(lineage._RESOLVE), dict(lineage._MEMO_RESOLVE),
                                        dict(lineage._BS_RESOLVE)],
                            "answers": digest.hexdigest()}}))
"""


def _child(mode: str, d: Path) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env["TETHER_CARRY_RECORD"] = "0"   # S1g: tests the bm_/bs_ carry the asked record replaces
    env["TETHER_AGENT_SEED"] = "0"     # C-seed-X: two writers' folders compared, one temperament
    r = subprocess.run([sys.executable, "-B", "-c", CHILD.format(mode=mode, d=str(d))], env=env,
                       capture_output=True, text=True, check=False, stdin=subprocess.DEVNULL)
    assert r.returncode == 0, f"{mode} failed:\n{r.stderr[-3000:]}"
    out = [ln for ln in r.stdout.splitlines() if ln.startswith("OUT ")]
    return json.loads(out[-1][4:])


def _sizes(d: Path) -> dict:
    return {fam: sum(f.stat().st_size for f in d.glob(f"{fam}*.json")) for fam in ("idx_", "bm_",
                                                                                 "bs_")}


def main() -> None:
    old_d = Path(tempfile.mkdtemp(prefix="cc_old_"))
    new_d = Path(tempfile.mkdtemp(prefix="cc_new_"))
    _child("old", old_d)
    _child("new", new_d)
    old_r, new_r = _child("new", old_d), _child("new", new_d)
    # THE PANEL PRECONDITION: each reader loaded a generation and resolved from the index and bm_
    for r in (old_r, new_r):
        assert r["parent"] and r["resolve"][0]["resolved"] and r["resolve"][1]["resolved"], r
        assert not (r["load"]["memo"] or {}).get("unreadable"), r
        assert not (r["load"]["slot_memo"] or {}).get("unreadable"), r
    assert old_r["load"] == new_r["load"], ("(a) the load reports differ", old_r, new_r)
    assert old_r["resolve"] == new_r["resolve"], ("(a) the resolve counts differ", old_r, new_r)
    assert old_r["answers"] == new_r["answers"], ("(a) the answers differ", old_r, new_r)
    print(f"  (a) indented and compact folders load and resolve identically: {new_r['resolve']}")
    so, sn = _sizes(old_d), _sizes(new_d)
    assert all(sn[f] < so[f] for f in so if so[f]), ("(b) compact is not smaller", so, sn)
    print(f"  (b) bytes indented {so} vs compact {sn}")
    print("compact carry: OK")


if __name__ == "__main__":
    main()
