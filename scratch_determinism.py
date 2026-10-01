"""IS A RUN REPRODUCIBLE WITHIN ONE PROCESS? The control my detector probe did not have.

The detector probe reported `up` entering `changed` at cycle 29 on the control and 36 on the
treatment. **Those arms are the SAME WORLD until the swap at cycle 30** -- one world step per
agent cycle, verified -- so a pre-swap difference is impossible if the runs are deterministic.

`gamma.py:416` builds a term handle with `random.choices` on the GLOBAL RNG, and `retrieve`'s
sort key ends in `name`. Two arms in one process therefore start from different RNG states.

**THIS TESTS THE SAME ARM TWICE, so the only possible difference is nondeterminism.** If the
two books differ, the detector's control-vs-treatment contrast is not attributable to the
swap and its reading is withdrawn.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True
sys.path.insert(0, r"C:\Users\Admin\Documents\GitHub\tether")

import gamma as G  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

CYCLES = 60   # anchor: THE DETECTOR'S OWN HORIZON. 15 was too short -- `changed` was EMPTY
              # in both runs, so the one quantity under suspicion was never exercised and
              # "identical" was vacuous for it. A control that examines nothing cannot
              # demonstrate a clean state.


def run() -> dict:
    """THE DETECTOR'S CONTROL ARM, VERBATIM -- same family, same seed, same cycles, and the
    same per-cycle entry recording. Anything else would be testing a different program."""
    env = world.bind(gridworld.family("default", 0, CYCLES))
    ag = tether.Agent(env, G.Gamma(env.atoms()), tether.Config(max_depth=2), ledger.Ledger())
    entry: dict[str, int] = {}
    for cyc in range(CYCLES):
        ag.step()
        for act in sorted(ag.iface.changed):
            entry.setdefault(act, cyc)
    return {"book": dict(ag.gamma.book),
            "names": sorted(ag.gamma.library),
            "changed": sorted(ag.iface.changed),
            "entry": entry}


def main() -> int:
    a, b = run(), run()
    print(f"TWO IDENTICAL RUNS, same process, same arm, same seed, {CYCLES} cycles.")
    same_book = a["book"] == b["book"]
    same_changed = a["changed"] == b["changed"]
    same_names = a["names"] == b["names"]
    print(f"  book identical     {same_book}")
    print(f"  changed identical  {same_changed}   {a['changed']} vs {b['changed']}")
    print(f"  names identical    {same_names}  ({len(a['names'])} vs {len(b['names'])})")
    same_entry = a["entry"] == b["entry"]
    print(f"  ENTRY CYCLES identical {same_entry}")
    print(f"    run1 {a['entry']}")
    print(f"    run2 {b['entry']}")
    if not same_entry:
        same_book = False
    if not same_book:
        for k in sorted(set(a["book"]) | set(b["book"])):
            if a["book"].get(k) != b["book"].get(k):
                print(f"    {k:28} {a['book'].get(k)} vs {b['book'].get(k)}")
    print()
    if same_book and same_changed:
        print("  DETERMINISTIC on these readings -- the detector's pre-swap difference")
        print("  needs another explanation and is NOT closed by this.")
        return 0
    print("  NONDETERMINISTIC. Two runs of the SAME arm differ, so a control-vs-treatment")
    print("  difference cannot be attributed to the treatment. The detector reading is")
    print("  WITHDRAWN until both arms are seeded identically.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
