"""L, THE LOOKUP STREAMED (the reviewer 2026-10-19 20:40): composer's streamed twins give exactly
what the lists gave.

  U1   lookup_iter yields lookup's pairs in lookup's order, and lookup_query is lookup's query,
       for descriptions with and without the DELTA link and one that lights nothing
  U2   read_iter's rows equal read_pairs' rows, row for row, on a real description's pairs over
       planted frames where many pairs share a reading pair; the cache holds one entry per distinct
       (left_reading, right_reading), fewer than the pairs
  MFb  MUST-FAIL: a read_iter whose cache keys on left_reading only gives a different held set on
       two pairs sharing a left reading

    python tests/test_lookup_stream.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
import composer  # noqa: E402

D = {"o3.row": "POSITION", "o3.col": "POSITION", "o3.drow": "DELTA", "o3.n": "COUNT"}
FRAMES = [{"o3.row": r, "o3.col": c, "o3.drow": d, "o3.n": n}
          for r, c, d, n in ((0, 0, 0, 1), (1, 0, 1, 1), (1, 1, 0, 2), (2, 1, 1, 2), (2, 2, 0, 3))]


def main() -> int:
    for d, link in ((D, True), (D, False), ({"o3.colour": "COLOUR"}, True)):
        got = composer.lookup(d, link)
        assert list(composer.lookup_iter(d, link)) == got["pairs"], (d, link)
        assert composer.lookup_query(d, link) == got["query"], (d, link)
    pairs = composer.lookup(D)["pairs"]
    print(f"U1 lookup_iter = lookup ({len(pairs)} pairs on the linked description), "
          "lookup_query = its query, with and without the link and on an unlit one")

    cache: dict = {}
    want = composer.read_pairs(pairs, FRAMES)
    got = list(composer.read_iter(iter(pairs), FRAMES, cache))
    assert got == want, "read_iter differs from read_pairs"
    keys = {(p["left_reading"], p["right_reading"]) for p in pairs}
    assert len(cache) == len(keys) < len(pairs), (len(cache), len(keys), len(pairs))
    assert any(r["held"] for r in got) and any(not r["held"] for r in got), "a one-sided plant"
    print(f"U2 read_iter = read_pairs row for row over {len(pairs)} pairs; "
          f"{len(cache)} bond readings computed (one per reading pair); "
          f"{sum(1 for r in got if r['held'])} held")

    def wrong_key(ps, frames, c):
        for p in ps:
            k = p["left_reading"]
            if k not in c:
                c[k] = composer._read_two(p["left_reading"], p["right_reading"], frames)
            occ, held = c[k]
            yield dict(p, occasions=dict(occ), held=list(held),
                       undecided=dict(composer.UNDECIDED_HERE))
    two = [{"left_reading": "a", "right_reading": "b"}, {"left_reading": "a", "right_reading": "c"}]
    fr = [{"a": x, "b": y, "c": 0} for x, y in ((0, 0), (1, 0), (1, 1), (2, 1), (2, 2))]
    right = [r["held"] for r in composer.read_iter(two, fr, {})]
    bad = [r["held"] for r in wrong_key(two, fr, {})]
    assert right == [r["held"] for r in composer.read_pairs(two, fr)] and right != bad, (right, bad)
    print(f"MFb a cache keyed on the left reading alone reads the second pair wrong: {ascii(bad)} "
          f"against {ascii(right)}")
    print("lookup_stream: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
