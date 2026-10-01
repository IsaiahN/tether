"""TIER ACCURACY: does the interface's prediction come true, and from which tier?

**THIS EXISTS BECAUSE THE ORIGINAL DID NOT SURVIVE.** The script that produced
`INDEX:51470`'s figures -- proximity 95.8% at tier 1 and 60.4% at tier 2, row and
col 100% at both -- is not in any scratch directory; `tiercheck.py` is a BRANCH
COUNTER that quotes them. A measurement nobody can re-take is a measurement that
cannot be checked, so this one lives in the tree.

**IT IS SCORED ON THE ACTION ACTUALLY PRESSED, which the first attempt got wrong.**
That version asked *what does SOME action's table say this slot becomes* and scored
it against the outcome of the action the agent pressed -- a prediction about one
press judged by another's result. It read row/col at 48%/56% against a recorded
100%, and its `distance` figure was discarded unreported.

    TIER 1   the pressed action's own entry for (ctx, slot, before)
    TIER 2   the pressed action's entries for (slot, before) in OTHER contexts
    ABSTAIN  neither resolves to a single value

**READ AT `audit` ENTRY**, which is the last moment the table is unpolluted by the
press being judged -- `audit` is the function that writes it.

**IT CALIBRATES BEFORE IT REPORTS.** `--calibrate` prints row/col and proximity
against the recorded figures. A reading from an instrument that cannot reproduce a
known answer is not evidence, and this one says so rather than leaving the reader
to notice.

    python tieracc.py 60              take the reading
    python tieracc.py 60 --calibrate  and judge it against the record
"""
from __future__ import annotations

import sys

# anchor: not chosen here -- seed 11 is the world `INDEX:51470` measured, and a reading
# on another seed is not comparable to the figures in `RECORDED` below.
SEED = 11
# anchor: not chosen here either -- 60 cycles is that reading's POPULATION. Fewer and the
# calibration has too little to reproduce; more and it is a different population from the
# one the recorded figures were taken over.
CYCLES = 60
# anchor: the recorded figures this instrument must reproduce before it is believed.
RECORDED = {("row", "tier1"): 100.0, ("col", "tier1"): 100.0,
            ("proximity", "tier1"): 95.8, ("proximity", "tier2"): 60.4}


def _predict(table: dict, action: str, ctx: tuple, slot: str, before: int):
    """What THE PRESSED ACTION's own table predicts, and from which tier."""
    e = table.get(action) or {}
    lands = e.get("lands", {})
    here = lands.get((ctx, slot, before))
    if here and len(here) == 1:
        return next(iter(here)), "tier1"
    seen = {v for (_c, k, b), vs in lands.items()
            if k == slot and b == before for v in vs}
    if len(seen) == 1:
        return next(iter(seen)), "tier2"
    return None, "abstain"


def take(cycles: int = CYCLES, seed: int = SEED, lift_guard: bool = False) -> dict:
    """Run and tally. `lift_guard` disables the relational guard IN THIS PROCESS only."""
    import gamma
    import gridworld
    import interface as IFace
    import ledger
    import tether
    import world

    tally: dict = {}
    _audit = IFace.Interface.audit

    def spy(self, r, before, after, ctx=(), *a, **k):
        act = getattr(r, "action", None)
        if act and before and after:
            for slot, b in before.items():
                if slot not in after or after[slot] == b:
                    continue
                pred, tier = _predict(self.table, act, ctx, slot, int(b))
                row = tally.setdefault(slot.rsplit(".", 1)[-1], {}).setdefault(
                    tier, {"hit": 0, "miss": 0, "n": 0})
                row["n"] += 1
                if tier != "abstain":
                    row["hit" if pred == after[slot] else "miss"] += 1
        return _audit(self, r, before, after, ctx, *a, **k)

    IFace.Interface.audit = spy
    try:
        env = world.bind(gridworld.GridWorld(seed=seed))
        if lift_guard:
            env.relational_slots = lambda: ()
        ag = tether.Agent(env, gamma.Gamma(env.atoms()),
                          tether.Config(max_depth=2), ledger.Ledger())
        for _ in range(cycles):
            ag.step()
    finally:
        IFace.Interface.audit = _audit
    return tally


def _acc(row: dict) -> float | None:
    d = row["hit"] + row["miss"]
    return 100.0 * row["hit"] / d if d else None


def main(argv: list[str]) -> int:
    n = int(argv[1]) if len(argv) > 1 and argv[1].isdigit() else CYCLES
    tally = take(n, lift_guard=True)
    print(f"WORLD gridworld seed {SEED}, no ARC board. {n} cycles, guard LIFTED.")
    print("POPULATION: every slot that CHANGED, scored against the PRESSED action.")
    print(f"  {'attribute':12} {'tier':8} {'n':>5} {'hit':>5} {'miss':>5} {'acc':>8}")
    for attr in sorted(tally):
        for tier in ("tier1", "tier2", "abstain"):
            row = tally[attr].get(tier)
            if not row:
                continue
            a = _acc(row)
            print(f"  {attr:12} {tier:8} {row['n']:5d} {row['hit']:5d} "
                  f"{row['miss']:5d} {(f'{a:.1f}%' if a is not None else '--'):>8}")
    if "--calibrate" not in argv:
        return 0
    print("\n  CALIBRATION -- against the recorded figures it must reproduce:")
    ok = True
    for (attr, tier), want in sorted(RECORDED.items()):
        row = (tally.get(attr) or {}).get(tier)
        got = _acc(row) if row else None
        near = got is not None and abs(got - want) <= 5.0
        ok = ok and near
        print(f"    {attr:10} {tier:6} recorded {want:5.1f}%   "
              f"measured {(f'{got:.1f}%' if got is not None else '--'):>7}   "
              f"{'OK' if near else 'MISMATCH'}")
    print("\n  " + ("CALIBRATED -- the reading may be believed."
                    if ok else
                    "NOT CALIBRATED -- this instrument cannot reproduce a known\n"
                    "  answer, so NO figure from it is evidence. Do not quote it."))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
