"""The shuffle seed is a dial on the spacing sweep, not a hidden constant.

Context: `chunk_order` already takes `seed`, but `watch`/`sweep` did not thread it, so a ladder
could only ever run at the fixed 1618. The code's own falsifier says a reading that moves when the
seed changes was seed noise and the sweep owes a result across seeds, not one.

This test: (1) the seed reaches the tape (different seeds -> different frame order, SAME frame
set), (2) the default is byte-identical to the old hard-coded 1618, (3) `sweep` records the seed.
No game-specific content; assertions are on order identity, not on mint counts.
"""
import sys

import _repo  # noqa: F401
import feeder


def main() -> int:
    game = "cd82"  # smallest full replay (18 chunks) -- cheap, not a fitted choice

    # (1) the seed reaches chunk_order: same chunks, different order
    _, a, na = feeder.chunk_order(game, spacing=1, seed=1618)
    _, b, nb = feeder.chunk_order(game, spacing=1, seed=1619)
    assert na == nb, "different seeds must not change the frame SET"
    assert sorted(a) == sorted(b), "different seeds must permute, not alter, the frames"
    assert a != b, "the seed is inert: two seeds gave byte-identical order"

    # (2) the default used by watch/sweep is exactly the old hard-coded seed
    _, d, _ = feeder.chunk_order(game, spacing=1)  # no seed arg
    assert d == a, "default seed changed: OFF is no longer byte-identical to 1618"

    # (3) sweep stamps the seed on its result (and threads it to every rung)
    out = feeder.sweep(game, rungs=(1,), cycles=3, seed=1619)
    assert out["shuffle_seed"] == 1619, "sweep did not record the seed it ran"
    assert out["rows"][0]["spacing"] == 1

    print("PASS seed reaches tape; default OFF identical to 1618; sweep records seed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
