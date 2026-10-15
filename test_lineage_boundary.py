"""C-lineage-1, THE BOUNDARY WRITE (the reviewer 2026-10-15 07:30, 07:32). WRITTEN, NOT RUN: it runs
in the end-of-step-7 checklist (Isaiah 05:25). Real gridworld Agents; each role its own process with
TETHER_LINEAGE_CARRY, TETHER_LINEAGE_BOUNDARY and TETHER_INDEX_HOLD set at start. Gridworld has no
level edge, so a role crosses K boundaries by calling lineage.boundary between plays, as both
runners do at a level clear or a terminal edge.

  L1   one game: generations written == K boundaries + 1 for the game end.
  L2   one line: each generation's parent is the one written before it; _chain loads with no N3.
  L3   no duplicates: the fold holds each term the instance wrote once, and its evidence equals
       the instance's evidence list, in order.
  L4   a stop after boundary k (no game-end write) loses at most the current level: a new
       instance loads the tip written at k; every term written up to k is taken at load
       (loaded + already_held == the terms the reps wrote; the reviewer 2026-10-15 07:41); and at
       least one memo entry is pending when the stopped game had bound answers.
  MF-L MUST-FAIL: the parent left at the loaded one after each write -> N3 (L2 red).
  MF-D MUST-FAIL: the written map cleared after each write -> a term written twice (L3 red).

    python test_lineage_boundary.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import lineage  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

K, N = 3, 8


def _agent(seed):
    env = world.bind(gridworld.family("default", seed))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game=f"fam_default_{seed}"),
                        tether.Config(), ledger.Ledger())


def role_game(d, stop, mf):
    """Play K levels with a boundary after each; `stop` >= 0 stops after that boundary with no
    game-end write. `mf` removes the parent move ("parent") or the written map ("written")."""
    assert lineage._BOUNDARY and lineage._CARRY and tether._INDEX_HOLD, "arms must be ON at start"
    ag = _agent(0)
    lineage.load(d, ag)
    loaded = ag.lineage_parent
    reps = []
    for k in range(K):
        for _ in range(N):
            ag.step()
        reps.append(lineage.boundary(d, ag, "default", "level"))
        if mf == "parent":
            ag.lineage_parent = loaded
        elif mf == "written":
            ag._lineage_written = {}
        if k == stop:
            break
    else:
        ag.end_run("cap")
        reps.append(lineage.write(d, ag, "default"))
    print("REPORT " + json.dumps({"reps": [{k: r.get(k) for k in ("hash", "parent", "terms",
                                                                   "refused")} for r in reps],
                                  "evidence": ag.gamma.evidence,
                                  "bound": len(ag._bound_cache) + len(tether._BOUND_MEMO)}),
          flush=True)


def role_load(d):
    ag = _agent(1)
    rep = lineage.load(d, ag)
    print("LOAD " + json.dumps({"parent": rep.get("parent"), "loaded": rep.get("loaded", 0),
                                "already_held": rep.get("already_held", 0),
                                "deduped": rep.get("deduped_onto_composition", 0),
                                "onto_atom": rep.get("destroyed_on_carry", 0),
                                "memo_pending": (rep.get("memo") or {}).get("pending", 0)}),
          flush=True)


def _child(*args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(TETHER_LINEAGE_CARRY="1", TETHER_LINEAGE_BOUNDARY="1", TETHER_INDEX_HOLD="1")
    return subprocess.run([sys.executable, "-B", __file__, "--role", *map(str, args)], env=env,
                          stdin=subprocess.DEVNULL, capture_output=True, text=True, check=False)


def _out(r, tag):
    assert r.returncode == 0, r.stderr[-3000:]
    return json.loads(next(ln for ln in r.stdout.splitlines() if ln.startswith(tag + " "))
                      [len(tag) + 1:])


def _l3(d, evidence):
    chain = lineage._chain(Path(d))
    f = lineage.fold(chain)
    rids = [lineage._rid(r) for r in f["terms"]]
    assert len(rids) == len(set(rids)), ("L3: a term written twice", len(rids) - len(set(rids)))
    keys = [lineage._key(r) for r in f["terms"]]
    assert len(keys) == len(set(keys)), ("L3: one composition in two rows",
                                         len(keys) - len(set(keys)))
    assert f["evidence"] == evidence, ("L3: evidence differs", len(f["evidence"]), len(evidence))
    return chain


def main():
    tmp = Path(tempfile.mkdtemp(prefix="bound_"))
    out = _out(_child("game", tmp / "full", -1, "none"), "REPORT")
    hs = [r["hash"] for r in out["reps"]]
    gens = sorted(Path(tmp / "full").glob(f"{lineage.PREFIX}*.json"))
    assert len(gens) == K + 1 and all(hs), ("L1", len(gens), out["reps"])
    print(f"  L1 one game, {K} boundaries: {len(gens)} generations")
    assert [r["parent"] for r in out["reps"]] == [None, *hs[:-1]], ("L2", out["reps"])
    chain = _l3(tmp / "full", out["evidence"])
    print(f"  L2 one line, {len(chain)} generations load in order; L3 no term twice, evidence "
          f"equal ({len(out['evidence'])} rows)")

    k = 1
    out = _out(_child("game", tmp / "stop", k, "none"), "REPORT")
    assert len(out["reps"]) == k + 1, ("L4: boundaries written before the stop", out["reps"])
    got = _out(_child("load", tmp / "stop"), "LOAD")
    assert got["parent"] == out["reps"][-1]["hash"], ("L4: the tip is not boundary k", got)
    _l3(tmp / "stop", out["evidence"])   # the stop came right after boundary k
    wrote = sum(r["terms"] or 0 for r in out["reps"])
    assert got["loaded"] + got["already_held"] == wrote, ("L4: terms written vs taken", wrote,
                                                          got)
    assert out["bound"] == 0 or got["memo_pending"] > 0, ("L4: no memo carried", out, got)
    print(f"  L4 stopped after boundary {k}: the next instance loads its tip and all {wrote} "
          f"terms written ({got['loaded']} installed; already held {got['already_held']}: "
          f"{got['deduped']} onto a composition, {got['onto_atom']} onto an atom); "
          f"memo pending "
          f"{got['memo_pending']} (the stopped game bound {out['bound']})")

    r = _child("game", tmp / "mfl", -1, "parent")
    assert r.returncode != 0 and "tip" in r.stderr, "MF-L MUST-FAIL did not fail: no N3"
    print("  MF-L must-fail fired: the parent left behind gives two tips (N3)")
    out = _out(_child("game", tmp / "mfd", -1, "written"), "REPORT")
    try:
        _l3(tmp / "mfd", out["evidence"])
    except AssertionError as e:
        print(f"  MF-D must-fail fired: {e.args[0][0]}")
    else:
        raise AssertionError("MF-D MUST-FAIL did not fail: the written map is not what dedups")
    print("lineage boundary: OK")


if __name__ == "__main__":
    if "--role" in sys.argv:
        a = sys.argv[sys.argv.index("--role") + 1:]
        if a[0] == "game":
            role_game(a[1], int(a[2]), a[3])
        else:
            role_load(a[1])
    else:
        main()
