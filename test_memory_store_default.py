"""TETHER_MEMORY_STORE, DEFAULT ON (Isaiah 2026-10-19 17:03 "turn it on"; the reviewer 17:04).

  D1  the env unset (every TETHER_ variable stripped): lineage._MEMORY_STORE reads True
  D2  MUST-FAIL, TETHER_MEMORY_STORE=0: it reads False, and two fake games on a fresh lineage
      folder take the old path -- the saves are written and NO memory.db is ever created
  D3  the env unset, a FIRST-EVER run on a fresh folder (no store): the load finds no store,
      open_store creates it, catch_up merges nothing, and _store_view returns the root view
      (no tip, no blob read -- the crash this test found at its first run); the run's save
      merges in; a second run loads from it and adds its own save -- the store then holds
      exactly the folder's saves (2), and its cheap check passes

    python test_memory_store_default.py
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))

CHILD = r'''
import sys
sys.dont_write_bytecode = True
import lineage, tether, tether_agent
from test_entry import FakeWrapper
tether._AGENT_SEED = False
print("ARM", lineage._MEMORY_STORE, flush=True)
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


def main() -> int:
    import lineage_store as ls
    out = child(None)
    assert "ARM True" in out, out                                                    # D1
    print("D1 the env unset: lineage._MEMORY_STORE is True")
    off = tempfile.mkdtemp(prefix="ms_off_")
    for _ in range(2):
        out = child({"TETHER_MEMORY_STORE": "0"}, off)
        assert "ARM False" in out and "RAN" in out, out
    gens = sorted(f for f in os.listdir(off) if f.startswith("gen_"))
    assert len(gens) == 2 and not os.path.exists(os.path.join(off, ls.DB)), (gens, os.listdir(off))
    print("D2 MUST-FAIL =0: False, 2 saves written, no memory.db (the old path)")       # D2
    on = tempfile.mkdtemp(prefix="ms_on_")
    child(None, on)
    assert os.path.exists(os.path.join(on, ls.DB)), "D3: the first-ever run built no store"
    child(None, on)
    gens = sorted(f[4:-5] for f in os.listdir(on) if f.startswith("gen_") and f.endswith(".json"))
    con = ls.open_store(on)
    try:
        held = sorted(r[0] for r in con.execute("SELECT h FROM saves"))
    finally:
        con.close()
    assert len(gens) == 2 and held == gens, (gens, held)
    assert ls.header_ok(on) == (True, "ok"), ls.header_ok(on)
    print("D3 a first-ever run built the store; after two runs it holds exactly the 2 saves; "
          "check ok")                                                                     # D3
    print("memory_store_default: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
