"""THE SIBLING MERGE ORDER (the reviewer 2026-11-04 r1064, r1065, r1066; remedy (i), script only).
lineage._topo breaks ties by hash, and lineage_store._continue takes new saves only when the merged
chain is a prefix of _topo's order. So two sibling saves merged one at a time with the LARGER hash
first leave the chain off _topo's order and catch_up rebuilds the whole store (the 287 x "rebuild",
3 h 8 min, of 2026-11-04). Copying every save of a run into the folder FIRST and calling catch_up
ONCE lets the store append them in _topo's own order. A root and two siblings on gridworld, minutes.

MF-M1  (the RED, today's case) siblings merged one at a time, larger hash first: catch_up rebuilds
MF-M2  (the GREEN, remedy (i)) both copied, then one catch_up: every entry "continue", 0 "rebuild"
       side reading toward remedy (ii): the two stores' fold blobs, equal or not, printed

    python tests/test_merge_order.py
"""
from __future__ import annotations

import os
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import lineage  # noqa: E402
import lineage_store as ls  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

STEPS = 3


def play(d: Path, seed: int) -> str:
    env = world.bind(gridworld.family("default", seed))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"fam_default_{seed}"), tether.Config(),
                      ledger.Ledger())
    lineage.load(str(d), ag)
    for _ in range(STEPS):
        ag.step()
    ag.end_run("cap")
    return lineage.write(str(d), ag, "default")["hash"]


def gens(d: Path) -> set:
    return {f.stem[4:] for f in d.glob("gen_*.json")}


def bring(src: Path, dst: Path, h: str) -> None:
    for f in [src / f"gen_{h}.json", *src.glob(f"ak_{h}_*.json"), *src.glob(f"idx_{h}_*.json")]:
        shutil.copy2(f, dst / f.name)


def merge(d: Path) -> list:
    con = ls.open_store(str(d))
    try:
        return [(r.get("save"), r.get("dag")) for r in ls.catch_up(con, str(d))]
    finally:
        con.close()


def blob(d: Path) -> list:
    con = sqlite3.connect(f"file:{d / 'memory.db'}?immutable=1", uri=True)
    try:
        return sorted(con.execute("SELECT * FROM blob").fetchall(), key=repr)
    finally:
        con.close()


def main():
    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        root = t / "root"
        root.mkdir()
        h0 = play(root, 0)
        sibs = []
        for seed in (1, 2):
            c = t / f"arm{seed}"
            shutil.copytree(root, c)
            sibs.append((play(c, seed), c))
        assert all(h != h0 for h, _c in sibs) and sibs[0][0] != sibs[1][0], (h0, sibs)
        small, big = sorted(sibs)
        # MF-M1: today's order -- the LARGER hash merged first, then the smaller
        a = t / "central_a"
        shutil.copytree(root, a)
        bring(big[1], a, big[0])
        first = merge(a)
        bring(small[1], a, small[0])
        second = merge(a)
        assert any(dag == "rebuild" for _h, dag in second), ("MF-M1: no rebuild", first, second)
        # MF-M2: remedy (i) -- both copied, then ONE catch_up
        b = t / "central_b"
        shutil.copytree(root, b)
        bring(big[1], b, big[0])
        bring(small[1], b, small[0])
        once = merge(b)
        assert once and all(dag == "continue" for _h, dag in once), ("MF-M2", once)
        assert sorted(h for h, _d in once) == sorted([small[0], big[0]]), ("MF-M2 saves", once)
        assert gens(a) == gens(b)
        same = blob(a) == blob(b)
    print(f"  root {h0}; siblings {small[0]} < {big[0]}")
    print(f"  MF-M1 larger first: first catch_up {first}; second {len(second)} entries, "
          f"{sum(d == 'rebuild' for _h, d in second)} rebuild")
    print(f"  MF-M2 both, one catch_up: {once}")
    print(f"  side reading (remedy ii): fold blob of (a) {'==' if same else '!='} (b)")
    print("test_merge_order OK")


if __name__ == "__main__":
    main()
