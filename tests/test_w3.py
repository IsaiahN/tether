"""W-3, THE HELD INDEX LAZY (TETHER_W_HELD_LAZY; the reviewer 2026-10-22 05:14 a, b, 06:37). The
fake ARC game, C-seed-X, on a two-game lineage built in a temp folder; each child plays a fresh COPY
of it.

  H1   OFF (every held entry decoded at load) vs ON (keys at load, items at the first ask from the
       load-time snapshot): the two runs' ledgers are equal (compare(), the one mask) and the load
       report's index line is equal (installed, the same count from the keys alone, amendment b)
  H2   ON, in process: entries resolved from the snapshot carry a verdict; a hard W-2 eviction
       drops them from _INDEX_STORE and keeps a planted entry with no verdict (this life's own
       compile is never evicted)
  H3   MF (a): an evicted entry asked again is re-read from the snapshot with NO _ch hashing (a
       counter on lineage._ch), and its held view equals the one before the eviction (by repr)

    python tests/test_w3.py
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
HERE = _repo.ROOT
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "conform"))
from identity_mod_rows import compare  # noqa: E402  the one identity reader

CHILD = r'''
import json, os, sys, tempfile
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
sys.path.insert(1, os.path.join(sys.argv[1], "tests"))
import tether, tether_agent
from test_entry import FakeWrapper
tether._AGENT_SEED = False
led = os.path.join(tempfile.mkdtemp(), "r.jsonl")
rep = tether_agent.run(FakeWrapper(script={}), "fake", max_actions=12, led_path=led,
                       lineage_dir=sys.argv[2])
lin = ((rep.get("loaded") or {}).get("lineage") or {}) if isinstance(rep, dict) else {}
idx = {"index": lin.get("index"), "kinds_known_dk": lin.get("kinds_known_dk")}
print(json.dumps({"led": led, "index": idx}, default=str))
'''


def _run(lin: str, lazy: bool) -> tuple[list[dict], object]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               TETHER_W_HELD_LAZY="1" if lazy else "0")
    p = subprocess.run([sys.executable, "-B", "-c", CHILD, HERE, lin], capture_output=True,
                       text=True, env=env, cwd=HERE, stdin=subprocess.DEVNULL, timeout=600)
    assert p.returncode == 0, p.stderr[-2000:]
    out = json.loads(p.stdout.strip().splitlines()[-1])
    with open(out["led"], encoding="utf-8") as fh:
        rows = [json.loads(x) for x in fh if x.strip()]
    for r in rows:      # the arm lists differ by the switch itself
        if r["slot"] == "@run" and r["event"] == "arms":
            r["detail"].pop("on", None)
            r["detail"].pop("off", None)
    return rows, out["index"]


def agent(lineage_dir):
    import arc_holdout
    import tether
    from test_entry import FakeWrapper
    tether._AGENT_SEED = False
    env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake", lineage_dir=lineage_dir)
    return env, ag


def main() -> int:
    import lineage
    import tether
    root = tempfile.mkdtemp(prefix="w3_")
    d0 = os.path.join(root, "lin")
    for _g in range(2):
        env, ag = agent(d0)
        for _ in range(6):
            env.observe()
            ag.step()
        ag.end_run("cap")
        lineage.write(d0, ag, "fake")

    copies = {}
    for name in ("off", "on", "inproc"):
        copies[name] = os.path.join(root, name)
        shutil.copytree(d0, copies[name])
    off, ioff = _run(copies["off"], lazy=False)
    on, ion = _run(copies["on"], lazy=True)
    bad = compare(off, on, set())
    assert not bad, bad[:3]
    assert ioff == ion and ion["index"] and ion["index"].get("installed"), (ioff, ion)
    print(f"  H1: OFF vs ON, {len(on)} rows equal (compare()); the load report's index line equal "
          f"({ion})")

    assert tether._W_HELD_LAZY and tether._W_CACHES
    assert isinstance(tether._INDEX_STORE, tether._Kept)
    # a fresh process, as the children are: building the lineage here filled the process stores
    for m in (tether._INDEX_STORE, lineage._PENDING, lineage._LAZY, lineage._VERDICT,
              lineage._CH_HELD):
        m.clear()
    lineage._CARRIED.clear()
    env, ag = agent(copies["inproc"])
    assert ag._dk_snap is not None and lineage._LAZY, "PRECONDITION: held keys lazily at load"
    for _ in range(6):
        env.observe()
        ag.step()
    sig_keys = [k for k in tether._INDEX_STORE if k in lineage._VERDICT]
    assert sig_keys, "PRECONDITION: no entry was resolved from the snapshot"
    k = sig_keys[0]
    before = repr(tether._INDEX_STORE[k])
    planted = ("planted-sig", "planted-key", "CAUSE")
    tether._INDEX_STORE[planted] = []
    ag._w_evict(hard=True, why="test_w3")
    assert k not in tether._INDEX_STORE and planted in tether._INDEX_STORE
    gone = [b for b in ag._body_rows if b.get("event") == "w_evict"][-1]["evicted"]["INDEX_STORE"]
    print(f"  H2: {len(sig_keys)} entries resolved from the snapshot hold a verdict; a hard "
          f"eviction dropped {gone} from _INDEX_STORE and kept the planted entry with no verdict")
    del tether._INDEX_STORE[planted]

    calls = [0]
    real_ch = lineage._ch

    def counted(c):
        calls[0] += 1
        return real_ch(c)
    lineage._ch = counted
    try:
        sig, key, role = k
        lib = (ag._inv_lib if tether._M7_INV and ag._inv_lib is not None
               else tether._library())
        n0 = lineage._VERDICT_N["refetched"]
        again = ag._held_index(lib, key, role, {a.name: a for a in ag.gamma.atoms}, sig)
    finally:
        lineage._ch = real_ch
    assert calls[0] == 0, ("MF (a): the re-read hashed", calls[0])
    assert lineage._VERDICT_N["refetched"] == n0 + 1
    assert repr(again) == before, "the re-read held view differs from the first"
    print("  H3: the evicted entry asked again was re-read from the snapshot with 0 _ch calls (the "
          "verdict held), and its held view equals the first (repr)")
    ag._dk_snap.close()
    print("w3: OK")
    return 0


if __name__ == "__main__":
    tempfile.tempdir = tempfile.mkdtemp(prefix="w3t_")
    sys.exit(main())
