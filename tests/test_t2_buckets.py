"""T2 BY TARGET (the reviewer r1774 3b): the store load's T2 candidates bucketed by target once
(lineage.t2_buckets), and tether's T2 reading ko's bucket alone, give the list the scan of every
candidate gave -- element for element, in order -- for every target and this run's dk landings.

  B1  bucketed == scanned for every target of a mixed fixture (CAUSE and other roles, several
      entries per target, run dk landings filtering some). MF: buckets sorted differ; a bucket
      missing one candidate differs
  B2  every candidate sits in exactly its own target's bucket (the buckets partition the dict)
  B3  the AGENT's own store-path T2 (Agent._tiers, tether.py's line, r1775 2): on a _kind_store
      with candidates on 3 targets, each target's entries its own, and a run dk landing on one
      candidate, the T2 tier for every target is exactly the entries the scan of every candidate
      keeps. External MFs (tether.py mutated in a scratch worktree): no target filter, and the
      run-dk clause removed, each fail here. The bucket ORDER is not observable at this tier
      (n_ sums, l_ maxes, _draw_ties sorts), so it is pinned by B1 alone

    python tests/test_t2_buckets.py
"""
from __future__ import annotations

import random
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
sys.path.insert(0, _repo.ROOT)

import arc_holdout  # noqa: E402
import lineage  # noqa: E402
import tether  # noqa: E402
from test_entry import FakeWrapper  # noqa: E402

tether._AGENT_SEED = False


def scanned(cand: dict, ko, run_dk: set) -> list:
    """The comprehension tether's T2 ran before r1774 3b, over every candidate."""
    return [(k, r, o, x) for (k, r, o, x) in cand
            if (x if r == "CAUSE" else o) == ko
            and (k, x if r == "CAUSE" else o) not in run_dk]


def bucketed(by: dict, ko, run_dk: set) -> list:
    """tether's T2 now (store path)."""
    return [(k, r, o, x) for (k, r, o, x) in by.get(ko, ()) if (k, ko) not in run_dk]


class Lib(dict):
    """The library as _tiers reads it: get, and no molecule over the lit keys."""

    def molecules_lit(self, _keys) -> list:
        return []


def fixture(seed: int = 7) -> tuple[dict, list, set]:
    rng = random.Random(seed)
    kinds = [("COLOUR", "SHAPE", f"form={i}") for i in range(6)] + [("COLOUR", "SHAPE")]
    ents = [f"LIB|E{i}" for i in range(9)]
    t2: dict = {}
    while len(t2) < 400:
        e = (rng.choice(ents), rng.choice(("CAUSE", "PROCESS", "STATE")), rng.choice(kinds),
             rng.choice(kinds))
        t2.setdefault(e, (rng.randint(1, 5), (None, None, None, -1)))
    run_dk = {(rng.choice(ents), rng.choice(kinds)) for _ in range(12)}
    return t2, kinds + [("NONE",)], run_dk


def main() -> int:
    t2, targets, run_dk = fixture()
    by = lineage.t2_buckets(t2)
    for ko in targets:
        assert bucketed(by, ko, run_dk) == scanned(t2, ko, run_dk), ko
    n = sum(len(scanned(t2, ko, run_dk)) for ko in targets)
    srt = {k: sorted(v) for k, v in by.items()}
    mf_sort = [ko for ko in targets if bucketed(srt, ko, run_dk) != scanned(t2, ko, run_dk)]
    big = max(by, key=lambda k: len(by[k]))
    short = {**by, big: by[big][:-1]}
    mf_drop = [ko for ko in targets if bucketed(short, ko, run_dk) != scanned(t2, ko, run_dk)]
    assert mf_sort and mf_drop, (mf_sort, mf_drop)
    print(f"B1 bucketed == scanned for all {len(targets)} targets ({len(t2)} candidates, {n} "
          f"kept after {len(run_dk)} run dk landings); MF sorted buckets differ on "
          f"{len(mf_sort)} targets, a dropped candidate on {len(mf_drop)}")
    assert set(by) == {(e[3] if e[1] == "CAUSE" else e[2]) for e in t2}
    assert sum(map(len, by.values())) == len(t2)
    print(f"B2 t2_buckets: {len(by)} targets, every candidate in exactly its target's bucket")

    # B3: the agent's own line
    _env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake", lineage_dir=None)
    tg = {i: ("COLOUR", f"form={i}") for i in range(3)}
    t2b: dict = {}
    for i, t in tg.items():
        for j in range(4):
            role = "CAUSE" if j % 2 else "PROCESS"
            o, x = (("SHAPE",), t) if role == "CAUSE" else (t, ("SHAPE",))
            t2b[(f"LIB|T{i}E{j}", role, o, x)] = (1, (None, None, None, -1))
    ag._kind_store = {"pairs": {}, "nocount": set(), "t2": t2b, "t2_by": lineage.t2_buckets(t2b)}
    ag._kind_landed_dk.clear()
    ag._kind_landed_dk[(("OTHER", "+", 1), "LIB|T1E2", tg[1])] = 1
    run = {e[1:] for e in ag._kind_landed_dk}
    lib = Lib({e[0]: {"key": e[0]} for e in t2b})
    got = {}
    for i, t in tg.items():
        ag._kind = lambda _mine, t=t: t
        out, n = ag._tiers(lib, [], ("MOTION", "+", 1), "o1", {}, {})
        want = {e[0] for e in scanned(t2b, t, run)}
        names = {k for k, _w in out}
        assert n.get("T2") == len(want) and want <= names, (i, n, want, names)
        assert not (names & ({e[0] for e in t2b} - want)), (i, names - want)
        got[i] = n["T2"]
    assert got == {0: 4, 1: 3, 2: 4}, got
    print(f"B3 the agent's own T2 (Agent._tiers, store path) per target = the entries the scan "
          f"keeps: {got} (target 1 loses the entry its run dk landing filters); no other target's")
    print("t2_buckets: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
