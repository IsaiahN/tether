"""T2 BY TARGET (the reviewer r1774 3b): the store load's T2 candidates bucketed by target once
(lineage.t2_buckets), and tether's T2 reading ko's bucket alone, give the list the scan of every
candidate gave -- element for element, in order -- for every target and this run's dk landings.

  B1  bucketed == scanned for every target of a mixed fixture (CAUSE and other roles, several
      entries per target, run dk landings filtering some). MF: buckets sorted differ; a bucket
      missing one candidate differs
  B2  every candidate sits in exactly its own target's bucket (the buckets partition the dict)

    python tests/test_t2_buckets.py
"""
from __future__ import annotations

import random
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
sys.path.insert(0, _repo.ROOT)

import lineage  # noqa: E402


def scanned(cand: dict, ko, run_dk: set) -> list:
    """The comprehension tether's T2 ran before r1774 3b, over every candidate."""
    return [(k, r, o, x) for (k, r, o, x) in cand
            if (x if r == "CAUSE" else o) == ko
            and (k, x if r == "CAUSE" else o) not in run_dk]


def bucketed(by: dict, ko, run_dk: set) -> list:
    """tether's T2 now (store path)."""
    return [(k, r, o, x) for (k, r, o, x) in by.get(ko, ()) if (k, ko) not in run_dk]


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
    print("t2_buckets: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
