"""TETHER_MEMORY_STORE, DEFAULT ON (Isaiah 2026-10-19 17:03 "turn it on"; the reviewer 17:04).
Step (5a): the store's form is TETHER_STORE_DB, default ON = learned.db (Isaiah 16:48); the reviewer
2026-10-25 01:06: the env-unset run proves the DEFAULT, the two explicit-arm runs are additions.

  D1  the env unset (every TETHER_ variable stripped): lineage._MEMORY_STORE and lineage._STORE_DB
      read True
  D2  MUST-FAIL, TETHER_MEMORY_STORE=0: it reads False, and two fake games on a fresh lineage
      folder take the old path -- the saves are written and NEITHER store file is ever created
  D3  a FIRST-EVER run on a fresh folder (no store): the load finds no store, open_store creates
      it, catch_up merges nothing, and the view returns the root view (no tip, no blob read -- the
      crash this test found at its first run); the run's save merges in; a second run loads from
      it and adds its own save -- the store then holds exactly the folder's saves (2), its cheap
      check passes, and the other form's store file is never created. Three times: the env unset
      (the default: learned.db), TETHER_STORE_DB=1 (learned.db) and TETHER_STORE_DB=0 (memory.db)

    python tests/test_memory_store_default.py
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
import sys
sys.dont_write_bytecode = True
import lineage, tether, tether_agent
from test_entry import FakeWrapper
tether._AGENT_SEED = False
print("ARM", lineage._MEMORY_STORE, "DB", lineage._STORE_DB, flush=True)
if len(sys.argv) > 1:
    tether_agent.run(FakeWrapper(script={}), "fake", max_actions=6, lineage_dir=sys.argv[1])
    print("RAN", flush=True)
'''


def child(extra: dict | None, *args: str) -> str:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", **(extra or {})})
    p = subprocess.run([sys.executable, "-B", "-c", CHILD, *args], capture_output=True, text=True,
                       env=env, cwd=HERE, stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-2000:]
    return p.stdout


def held_saves(m, folder: str) -> list:
    con = m.open_store(folder)
    try:
        if m.__name__ == "lineage_store":
            return sorted(r[0] for r in con.execute("SELECT h FROM saves"))
        return sorted(json.loads(k)[0] for (k,) in
                      con.execute("SELECT key FROM learned WHERE section = 'saves'"))
    finally:
        con.close()


def d3(label: str, extra: dict | None, m, other: str) -> None:
    on = tempfile.mkdtemp(prefix="ms_on_")
    out = child(extra, on)
    want = "DB False" if m.__name__ == "lineage_store" else "DB True"
    assert want in out and "RAN" in out, (label, out)
    assert os.path.exists(os.path.join(on, m.DB)), f"D3 {label}: the first-ever run built no {m.DB}"
    child(extra, on)
    gens = sorted(f[4:-5] for f in os.listdir(on) if f.startswith("gen_") and f.endswith(".json"))
    held = held_saves(m, on)
    assert len(gens) == 2 and held == gens, (label, gens, held)
    assert m.header_ok(on) == (True, "ok"), (label, m.header_ok(on))
    assert not os.path.exists(os.path.join(on, other)), (label, "a stray", other, os.listdir(on))
    print(f"D3 {label}: a first-ever run built {m.DB}; after two runs it holds exactly the 2 "
          f"saves; check ok; no {other}")


def main() -> int:
    import lineage_store
    import store_fold
    out = child(None)
    assert "ARM True" in out and "DB True" in out, out                                  # D1
    print("D1 the env unset: lineage._MEMORY_STORE and lineage._STORE_DB are True")
    off = tempfile.mkdtemp(prefix="ms_off_")
    for _ in range(2):
        out = child({"TETHER_MEMORY_STORE": "0"}, off)
        assert "ARM False" in out and "RAN" in out, out
    gens = sorted(f for f in os.listdir(off) if f.startswith("gen_"))
    stores = [f for f in (lineage_store.DB, store_fold.DB) if os.path.exists(os.path.join(off, f))]
    assert len(gens) == 2 and not stores, (gens, os.listdir(off))
    print("D2 MUST-FAIL =0: False, 2 saves written, neither memory.db nor learned.db (the old "
          "path)")                                                                        # D2
    d3("the env unset (the default)", None, store_fold, lineage_store.DB)              # D3
    d3("TETHER_STORE_DB=1", {"TETHER_STORE_DB": "1"}, store_fold, lineage_store.DB)
    d3("TETHER_STORE_DB=0", {"TETHER_STORE_DB": "0"}, lineage_store, store_fold.DB)
    print("memory_store_default: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
