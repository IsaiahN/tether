"""THE DELTA-KIND SORT KEY (E4a 2026-10-18; the reviewer 15:32). ar25's delta kinds came in two
shapes, (str, str, int) and (str, str, str), and lineage.write sorted lists of them element by
element: TypeError, no generation written. The fake ARC game, C-seed-X.

  DK   two mixed-shape keys planted in each dk store: write() then a fresh agent's load() gives
       the same counts and the same latest landing
  MF   the plain sort in their place: write() raises the TypeError

    python tests/test_lineage_dk_shape.py
"""
from __future__ import annotations

import sys
import tempfile

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
sys.path.insert(0, _repo.ROOT)

DKS = (("move", "row", 1), ("move", "row", "up"))


def agent(lineage_dir):
    import arc_holdout
    import tether
    from test_entry import FakeWrapper
    tether._AGENT_SEED = False
    return arc_holdout.wire(FakeWrapper(script={}), "fake", lineage_dir=lineage_dir)[1]


def plant(ag) -> None:
    for i, dk in enumerate(DKS):
        e = (dk, "lib_k", ("obj",))
        ag._kind_landed_dk[e] += i + 2
        ag._kdk_last[e] = ("fake", 0, 5 + i, 10 + i)
        ag._kind_offered_dk[(dk, "lib_k", ("obj",))] += i + 4


def main() -> int:
    import lineage
    d = tempfile.mkdtemp()
    ag = agent(d)
    plant(ag)
    lineage.write(d, ag, "fake")
    ag2 = agent(d)
    for dk in DKS:
        e = (dk, "lib_k", ("obj",))
        assert ag2._kind_known_dk[e] == ag._kind_landed_dk[e], (e, ag2._kind_known_dk[e])
        assert ag2._kind_known_off[e] == ag._kind_offered_dk[e], (e, ag2._kind_known_off[e])
        assert ag2._kdk_last.get(e) == ag._kdk_last[e], (e, ag2._kdk_last.get(e))
    print("DK", len(DKS), "mixed-shape keys round-trip: counts, offers and latest landing equal")
    real = lineage._ksorted
    lineage._ksorted = sorted
    try:
        ag3 = agent(tempfile.mkdtemp())
        plant(ag3)
        lineage.write(tempfile.mkdtemp(), ag3, "fake")
    except TypeError as e:
        assert "'<' not supported" in str(e), e
        print("MF the plain sort raises:", e)
    else:
        raise AssertionError("MF did not fail: the plain sort wrote mixed-shape keys")
    finally:
        lineage._ksorted = real
    print("lineage_dk_shape: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
