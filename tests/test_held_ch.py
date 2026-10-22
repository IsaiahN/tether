"""C-S1e-1, A HELD CANDIDATE HASHED ONCE (the reviewer 2026-10-15 13:01). WRITTEN, NOT RUN: it
runs in the end-of-step-7 checklist. The harness is the 12:38 carry read's: the 3-action fake game
through tether_agent.run with a lineage folder, all defaults, each process its own.

  (a)  process 1 writes a folder; process 2 runs on two copies of it, once with lineage._held_ch
       as built and once with it replaced by _ch itself (no cache): the resolved / unresolved
       counts of every family (index, bm_, bs_) and every slot answer process 2 is given, in order,
       are identical.
  MF   MUST-FAIL: a cache keyed WITHOUT the signature (and with no identity check) hands back the
       hash of another signature's candidate at the same (entry, role, position); the real
       _held_ch does not.

    python tests/test_held_ch.py
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import lineage  # noqa: E402

CHILD = r"""
import hashlib, json, sys
sys.dont_write_bytecode = True
import lineage, tether, tether_agent
from test_entry import FakeWrapper
from test_index_hold import _form
MODE, D = {mode!r}, {d!r}
if MODE == "off":
    lineage._held_ch = lambda sig, key, role, i, cand: lineage._ch(cand)
digest = hashlib.sha256()
real = tether.Agent._compiled
def compiled(self, lib, key, role, o, x, comp, atoms, sig, slot=None):
    got = real(self, lib, key, role, o, x, comp, atoms, sig, slot=slot)
    if slot is not None:
        got = list(got)
        digest.update(repr((key, role, o, x, slot,
                            [(_form(a), _form(b)) for _c, a, b in got])).encode("utf-8"))
    return got
tether.Agent._compiled = compiled
tether_agent.run(FakeWrapper(), "g0", 3, lineage_dir=D)
print("OUT " + json.dumps({{"resolve": [dict(lineage._RESOLVE), dict(lineage._MEMO_RESOLVE),
                                        dict(lineage._BS_RESOLVE)],
                            "answers": digest.hexdigest()}}))
"""


def _child(mode: str, d: Path) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env["TETHER_CARRY_RECORD"] = "0"   # S1g: tests the bm_/bs_ carry the asked record replaces
    r = subprocess.run([sys.executable, "-B", "-c", CHILD.format(mode=mode, d=str(d))], env=env,
                       capture_output=True, text=True, check=False, stdin=subprocess.DEVNULL)
    assert r.returncode == 0, f"{mode} failed:\n{r.stderr[-3000:]}"
    out = [ln for ln in r.stdout.splitlines() if ln.startswith("OUT ")]
    return json.loads(out[-1][4:])


def mf() -> None:
    a, b = {"condition": "A"}, {"condition": "B"}
    sig_a, sig_b = ("arm", ("x",)), ("arm", ("y",))
    stale: dict = {}

    def nosig(_sig, key, role, i, cand):
        if (key, role, i) not in stale:
            stale[(key, role, i)] = lineage._ch(cand)
        return stale[(key, role, i)]
    nosig(sig_a, "k", "STATE", 0, a)
    assert nosig(sig_b, "k", "STATE", 0, b) != lineage._ch(b), "MF MUST-FAIL did not fail"
    lineage._held_ch(sig_a, "k", "STATE", 0, a)
    assert lineage._held_ch(sig_b, "k", "STATE", 0, b) == lineage._ch(b), "the real cache is stale"
    print("  MF must-fail fired: a cache keyed without the signature hands back a stale hash; "
          "_held_ch does not")


def main() -> None:
    d = Path(tempfile.mkdtemp(prefix="hch_")) / "lineage"
    d.mkdir()
    _child("on", d)       # process 1 writes the folder
    on_d, off_d = (Path(tempfile.mkdtemp(prefix=f"hch_{m}_")) / "lineage" for m in ("on", "off"))
    shutil.copytree(d, on_d)
    shutil.copytree(d, off_d)
    on, off = _child("on", on_d), _child("off", off_d)
    # THE PANEL PRECONDITION: process 2 resolved something from each carried family it read
    assert on["resolve"][0]["resolved"] > 0 and on["resolve"][1]["resolved"] > 0, on
    assert on == off, ("(a) the cache changed a resolve count or an answer", on, off)
    print(f"  (a) process 2 with and without the cache: resolve {on['resolve']}, answers "
          f"{on['answers'][:16]} identical")
    mf()
    print("held ch: OK")


if __name__ == "__main__":
    main()
