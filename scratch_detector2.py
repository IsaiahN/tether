"""DOES THE AGENT NOTICE THE MAPPING MOVED? Fixture A, control vs treatment, ONE ARM PER PROCESS.

**THE ARMS NO LONGER SHARE A PROCESS.** The first version ran both in one, and an action
entered `changed` at cycle 29 on the control and 36 on the treatment -- impossible if the
arms are the same world until the swap at 30. I blamed the global RNG; my own determinism
check refuted that. **The cause is still unidentified, so this removes the whole class
rather than the one suspect:** each arm is a separate interpreter, and the only difference
between them is this script's argv.

    python scratch_detector2.py control     -> det2_control.json
    python scratch_detector2.py treatment   -> det2_treatment.json
    python scratch_detector2.py compare     -> the verdict

**THE PRE-SWAP IDENTITY IS CHECKED FIRST AND IT IS A PRECONDITION, NOT A RESULT.** The arms
are the same board until the swap, so every cycle before it must match exactly. If they do
not, nothing after the swap is attributable and the run reports that instead of a verdict.

**AND THE COMPARISON STATES ITS DENOMINATOR**, because the last check I wrote compared two
empty sets and printed `True`. A per-cycle record that is empty everywhere is reported as
EXAMINED NOTHING rather than as agreement.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, r"C:\Users\Admin\Documents\GitHub\tether")

import gamma as G  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

CYCLES = 60            # anchor: the panel's population and the first probe's horizon
SEED = 0               # anchor: a WITHIN-SEED contrast; both arms must be the same board
# anchor: NOT `CYCLES // 2`, and the off-by-one is the point. `family()` sets
# `remap_after = 30`, but `GridWorld.step` does `self._steps += 1` as its FIRST line and
# `_delta` then tests the ALREADY-INCREMENTED counter. So on agent cycle 29 the counter
# reads 30, `30 >= 30` holds, and THE SWAP APPLIES AT CYCLE 29. Reading the guard without
# the increment above it put my boundary one cycle late and made a correct divergence look
# impossible.
SWAP = CYCLES // 2 - 1
SETS = ("changed", "conditional", "unreliable")
HERE = Path(__file__).parent


def run(arm: str) -> dict:
    fam = "remap_after" if arm == "treatment" else "default"
    env = world.bind(gridworld.family(fam, SEED, CYCLES))
    ag = tether.Agent(env, G.Gamma(env.atoms()), tether.Config(max_depth=2), ledger.Ledger())
    # THE WHOLE PER-CYCLE RECORD, not just first-entry. First-entry cannot show whether the
    # arms agreed BEFORE the swap, which is the precondition this version exists to check.
    per_cycle = []
    for _ in range(CYCLES):
        ag.step()
        per_cycle.append({s: sorted(getattr(ag.iface, s)) for s in SETS})
    return {"arm": arm, "family": fam, "per_cycle": per_cycle,
            "actions": list(env.actions()), "book": dict(ag.gamma.book)}


def first_entry(per_cycle: list, s: str) -> dict:
    out: dict[str, int] = {}
    for cyc, row in enumerate(per_cycle):
        for act in row[s]:
            out.setdefault(act, cyc)
    return out


def compare() -> int:
    try:
        c = json.loads((HERE / "det2_control.json").read_text(encoding="utf-8"))
        t = json.loads((HERE / "det2_treatment.json").read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        print(f"  MISSING ARM: {exc}. Run both arms first.")
        return 2

    print(f"WORLD gridworld seed {SEED}, no ARC board. {CYCLES} cycles, swap at {SWAP}.")
    print("ONE ARM PER PROCESS. Only this script's argv differed.\n")

    # ---- the precondition, before any verdict -------------------------------------------
    pre_c, pre_t = c["per_cycle"][:SWAP], t["per_cycle"][:SWAP]
    non_empty = sum(1 for row in pre_c for s in SETS if row[s])
    identical = pre_c == pre_t
    print("  PRECONDITION -- the arms are the same board until the swap:")
    print(f"    cycles compared            {SWAP}")
    print(f"    non-empty set-readings     {non_empty}   <- the DENOMINATOR")
    print(f"    pre-swap records identical {identical}")
    if non_empty == 0:
        print("    EXAMINED NOTHING: every set was empty on every pre-swap cycle, so")
        print("    'identical' here is vacuous and proves no such thing.")
    if not identical:
        for i, (x, y) in enumerate(zip(pre_c, pre_t, strict=True)):
            if x != y:
                print(f"    FIRST DIVERGENCE at cycle {i}: {x} vs {y}")
                break
        print("    SO NOTHING AFTER THE SWAP IS ATTRIBUTABLE. No verdict is read.")
        return 1
    if non_empty == 0:
        print("    No verdict read: the precondition could not be tested.")
        return 1
    print("    PRECONDITION MET on a real population.\n")

    # ---- the three pre-registered verdicts ----------------------------------------------
    ec, et = first_entry(c["per_cycle"], "changed"), first_entry(t["per_cycle"], "changed")
    for s in SETS:
        a, b = first_entry(c["per_cycle"], s), first_entry(t["per_cycle"], s)
        print(f"  {s}:")
        for act in sorted(set(a) | set(b)):
            mark = "  <-- TREATMENT ONLY" if act in b and act not in a else ""
            print(f"    {act:8} control {str(a.get(act)):>5}   "
                  f"treatment {str(b.get(act)):>5}{mark}")
        print()

    n_act = len(t["actions"])
    pre = [k for k, v in ec.items() if v < SWAP]
    only = [k for k in et if k not in ec]
    after = [(et[k] - SWAP, k) for k in only if et[k] >= SWAP]
    print("  VERDICT:")
    if len(pre) == n_act:
        print(f"    SATURATED BEFORE THE SWAP. All {n_act} actions already in `changed` on")
        print("    the CONTROL before the swap, from wrap alone. The detector cannot")
        print("    answer this question on this world -- a finding about the instrument.")
    elif only and after:
        print(f"    TREATMENT-ONLY FLAGS: {sorted(only)}")
        print(f"    First AFTER the swap: {sorted(after)[0][1]} at +{sorted(after)[0][0]} cycles.")
    elif only:
        print(f"    TREATMENT-ONLY FLAGS: {sorted(only)}, but NONE entered after the swap,")
        print("    so the swap is not established as the cause.")
    else:
        print(f"    NO TREATMENT-ONLY FLAG. {len(pre)} of {n_act} were already flagged on")
        print("    the control before the swap; the remap added nothing the detector saw.")
    return 0


def main(argv: list[str]) -> int:
    arm = argv[1] if len(argv) > 1 else "compare"
    if arm == "compare":
        return compare()
    if arm not in ("control", "treatment"):
        print("usage: scratch_detector2.py control|treatment|compare")
        return 2
    r = run(arm)
    (HERE / f"det2_{arm}.json").write_text(json.dumps(r), encoding="utf-8")
    print(f"{arm}: {CYCLES} cycles on {r['family']}, written. "
          f"final changed={sorted(r['per_cycle'][-1]['changed'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
