"""THE _tiers NAME TIE -> THE RECORDED DRAW (TETHER_TIERS_DRAW; the reviewer 2026-10-20 23:55 (ii),
2026-10-21 03:05; Isaiah's 10-15 A1 rule: never a name).

  (1) a planted pair, equal on every number _tiers ranks T1d by (landings, recency), whose NAMES
      sort opposite to their recorded draw: ON lists them in draw order; OFF in name order. The fake
      world, in process.
  (2) gridworld_arc_s1, 15 steps, the agent seed pinned, ON under hash seeds 1 and 2: every row
      identical (the arms row's pythonhashseed and goal_hypotheses' wall_s masked) -- the draw is a
      keyed hash, not a set order.
  (3), OFF identity against 03b793e, is run apart (the ledgers through ident_mask).

    python tests/test_tiers_draw.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from collections import Counter

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
HERE = _repo.ROOT

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
tree = sys.argv[1]
sys.path = ([tree, tree + "/conform"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import gamma, ledger, panel, tether, world

env = world.bind(panel._gridworld("gridworld_arc_s1")[0])
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="draw"), tether.Config(), ledger.Ledger())
for _ in range(15):
    ag.step()
print(json.dumps({"draw": tether._TIERS_DRAW, "rows": ag.led.rows()}, default=str))
'''


def _run(hseed: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED=hseed, TETHER_AGENT_SEED="0")
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, HERE], env=env, capture_output=True,
                         text=True, timeout=1200, cwd=HERE)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def planted() -> None:
    sys.path.insert(0, HERE)
    import arc_holdout
    import frontier as FR
    import tether
    from test_entry import FakeWrapper
    tether._AGENT_SEED = False
    env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake")
    lib = tether._library()
    mine = sorted(set(env.slot_owner().values()))[0]
    ko = ag._kind(mine)
    dk = ("MOTION", "-", 1)
    key = f"{ag.cycle}:{mine}:{dk}:tiers"
    names = [k for k in lib.seed if not lib.seed[k].get("ingredients")][:60]
    # a pair whose names sort OPPOSITE to their draw, so name order and draw order disagree
    pair = next((a, b) for a in names for b in names if a < b
                and FR.draw_key(key, a, ag.draw_seed) > FR.draw_key(key, b, ag.draw_seed))
    ag._kind_landed_dk = Counter({(dk, k, ko): 1 for k in pair})       # T1d: landed, never offered
    ag._kind_offered_dk, ag._kind_known_dk = Counter(), Counter()
    for k in pair:                                                       # equal recency
        ag._kdk_last[(dk, k, ko)] = ("fake", 0, 0, 1)
    was = tether._TIERS_DRAW
    got = {}
    try:
        for on in (True, False):
            tether._TIERS_DRAW = on
            out, n = ag._tiers(lib, [], dk, mine, {}, {})
            got[on] = [k for k, _w in out if k in pair]
    finally:
        tether._TIERS_DRAW = was
    assert n["T1d"] == 2, n
    assert got[True] == [pair[1], pair[0]], (got, pair)       # the draw puts b first
    assert got[False] == [pair[0], pair[1]], (got, pair)      # the name puts a first
    print(f"(1) a tied pair whose names sort opposite to their draw: ON {got[True]} (the draw), "
          f"OFF {got[False]} (the name)")
    # T5 (the reviewer 2026-10-21 04:18): the by_cluster entries for a POSITION reading, ordered by
    # (molecule, score) and then the draw ON / the name OFF; their score runs tie, so the two differ
    import inherited
    att = env.attribute_of()
    slot = next(s for s, a in att.items() if a == "row")
    bc, _why = inherited.by_cluster()
    cls = set(inherited.READING_CLUSTER.get(att.get(slot), ()))
    score = Counter(k for c in cls for k in bc.get(c, ()))
    rows = [(k, m) for k, m in score.items() if lib.get(k) is not None]

    def num(kv):
        return (bool((lib.get(kv[0]) or {}).get("ingredients")), -kv[1])
    key5 = f"{ag.cycle}:{mine}:None:tiers"
    want = {True: [k for k, _m in sorted(rows, key=lambda kv: (
                num(kv), FR.draw_key(key5, kv[0], ag.draw_seed), kv[0]))],
            False: [k for k, _m in sorted(rows, key=lambda kv: (num(kv), kv[0]))]}
    assert want[True] != want[False], "PRECONDITION: no T5 tie whose draw differs from its names"
    got5 = {}
    try:
        for on in (True, False):
            tether._TIERS_DRAW = on
            out, n = ag._tiers(lib, [], None, mine, {slot: "POSITION"}, att)
            got5[on] = [k for k, _w in out][-n["T5"]:]
    finally:
        tether._TIERS_DRAW = was
    assert got5[True] == want[True] and got5[False] == want[False], (got5, want)
    print(f"(1b) T5: {len(rows)} POSITION-filed entries; ON in (molecule, score, draw) order, "
          f"OFF in (molecule, score, name) order, and the two differ")


def main() -> None:
    sys.path.insert(0, os.path.join(HERE, "conform"))
    from identity_mod_rows import compare
    planted()
    a, b = _run("1"), _run("2")
    assert a["draw"] is True
    for rs in (a["rows"], b["rows"]):
        for r in rs:
            if r["event"] == "arms" and r["slot"] == "@run":
                r["detail"].pop("pythonhashseed", None)
    bad = compare(a["rows"], b["rows"], set())
    assert not bad, bad[:3]
    print(f"(2) ON under hash seeds 1 and 2: {len(a['rows'])} rows identical")
    print("test_tiers_draw: pass")


if __name__ == "__main__":
    main()
