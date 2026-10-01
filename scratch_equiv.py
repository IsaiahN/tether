"""EQUIVALENCE: does `family()` build the same three worlds the INLINE version built?

The running panel loaded its script BEFORE the `family()` rewrite, so its numbers come from
the inline constructor. The reviewer asked for proof the two agree rather than a restart.

**COMPARED ON THE WHOLE CONSTRUCTED OBJECT, not on the two fields I happen to have changed.**
Checking only `click_only` and `remap_after` would be checking the thing I already know --
the question is whether anything ELSE about the board differs, and only the full state and
the advertised action set can answer that.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True
sys.path.insert(0, r"C:\Users\Admin\Documents\GitHub\tether")

import gridworld  # noqa: E402

CYCLES = 60          # anchor: the panel's run length -- the only value `family` reads
SEEDS = (0, 1, 2)


def inline(arm: str, seed: int):
    """THE EXACT CONSTRUCTOR THE RUNNING PANEL USED, copied from its first version."""
    if arm == "click_only":
        return gridworld.GridWorld(seed=seed, click_only=True)
    if arm == "remap_after":
        return gridworld.GridWorld(seed=seed, remap_after=CYCLES // 2)
    return gridworld.GridWorld(seed=seed)


def fingerprint(w) -> tuple:
    return (dict(sorted(w.state.items())), w.target, w.click_only, w.remap_after,
            tuple(w.actions()), tuple(sorted(w.slots())),
            tuple(sorted(w.relational_slots())), tuple(sorted(w.slot_owner().items())))


def main() -> int:
    bad = 0
    for arm in gridworld.FAMILIES:
        for seed in SEEDS:
            a, b = inline(arm, seed), gridworld.family(arm, seed, CYCLES)
            fa, fb = fingerprint(a), fingerprint(b)
            same = fa == fb
            bad += 0 if same else 1
            print(f"  {arm:12} seed {seed}  remap={b.remap_after!r:>5} "
                  f"click={b.click_only!r:>5}  {'IDENTICAL' if same else 'DIFFERS'}")
            if not same:
                for i, (x, y) in enumerate(zip(fa, fb, strict=True)):
                    if x != y:
                        print(f"      field {i}: inline={x!r}  family={y!r}")

    print()
    if bad:
        print(f"  {bad} of 9 DIFFER -- the panel's numbers are NOT the committed door's "
              f"worlds, and must be re-taken.")
        return 1
    print("  ALL 9 IDENTICAL on full state, target, both fixture fields, the advertised")
    print("  action set, slots, relational slots and slot owners.")
    print("  The panel's numbers describe the worlds `family()` produces.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
