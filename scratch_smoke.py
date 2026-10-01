"""SMOKE: does FIXTURE A actually swap? Seconds, at the WORLD level, before any agent run.

*A three-second live smoke run is part of BUILDING an arm, before any tape measurement of
it is reported* -- and `remap_after` had never once been constructed, so nothing has ever
established that it does what its comment says.

**IT TESTS THE WORLD, NOT THE AGENT.** Press `up` from a known cell before and after the
swap point and compare the DISPLACEMENT. If Fixture A works, `up` moves the mover one way
early and the opposite way late, with the button's NAME unchanged -- which is the whole
point of the fixture: the board stays lawful and the MAPPING moves.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True
sys.path.insert(0, r"C:\Users\Admin\Documents\GitHub\tether")

import gridworld  # noqa: E402


def press(w, action):
    before = (w.state["o0.row"], w.state["o0.col"])
    w.step(action)
    after = (w.state["o0.row"], w.state["o0.col"])
    return (after[0] - before[0], after[1] - before[1])


def main() -> int:
    # anchor: not chosen here -- the swap must be crossed inside the probe, so the run length
    # is the smallest that gives presses on BOTH sides of a midpoint.
    cycles = 8
    w = gridworld.family("remap_after", seed=0, cycles=cycles)
    print(f"constructed: remap_after={w.remap_after!r}, actions={w.actions()}")

    moves = []
    for i in range(cycles):
        d = press(w, "up")
        moves.append(d)
        print(f"  step {i}  press 'up'  displacement {d}")

    # THE BOUNDARY IS `remap_after - 1`, NOT `remap_after` -- F392, and this script's own
    # first output is what exposed it. `GridWorld.step` does `self._steps += 1` as its FIRST
    # line and `_delta` then tests the ALREADY-INCREMENTED counter, so press index
    # `remap_after - 1` is the first SWAPPED one. Bucketing at `remap_after` put index 3's
    # `(-4, 0)` -- row 4 -> row 0, which is DOWN with wrap -- into the `early` list and read
    # it as an up-wrap. **The verdict was right and the bucketing was one late.**
    first_swapped = w.remap_after - 1
    early = [m for m in moves[:first_swapped] if m != (0, 0)]
    late = [m for m in moves[first_swapped:] if m != (0, 0)]
    print()
    print(f"  early (before index {first_swapped}) non-zero displacements: {early}")
    print(f"  late  (index {first_swapped} on)     non-zero displacements: {late}")

    if not early or not late:
        print("  INCONCLUSIVE -- the mover was blocked on one side of the swap, so this "
              "probe has no contrast. NOT a verdict on the fixture.")
        return 2
    if set(early) == set(late):
        print("  THE SWAP DID NOT CHANGE 'up'. Fixture A is declared and inert.")
        return 1
    print("  THE SWAP FIRED: 'up' displaces differently after the swap point, same name.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
