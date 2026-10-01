"""THE BIN CENSUS: which residual bin does each slot land in, and does it ever reach a minting one?

`mint` has two call sites (`tether.py:6972`, `6974`), reachable only from `MECHANISM` or from
`REFUTED` with no competitor. `bargain_bounded_out` reads 0 on `click_only`, so the hypothesis
is that no slot ever reaches either. **This counts it instead of inferring it.**

**AND IT CAPTURES `support` BESIDE THE BIN, which is what makes the test sharp.** The classifier
at `tether.py:3001` is literally:

    elif len(self.trace) < 2:  b, fit = NOVEL, None

so `NOVEL` IS "trace shorter than 2", and the ROUTE row records that length as `support`. If
`click_only`'s slots are stuck in NOVEL the support distribution says so directly.

**TALLIED AT THE RECORDING SITE, not re-derived.** A spy on `led.record` counts every ROUTE row
the agent actually writes, so there is no second implementation of the classifier to disagree
with the first.

ONE ARM PER PROCESS -- the arms share no module-level mutable.

    python scratch_bins.py click_only   -> bins_click_only.json
    python scratch_bins.py default      -> bins_default.json
    python scratch_bins.py compare
"""
from __future__ import annotations

import collections
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

CYCLES = 60   # anchor: the panel's population, so this sits beside those rows
SEED = 0      # anchor: the panel's first seed
MINTING = ("mechanism", "refuted")   # the two bins that can reach a mint call
HERE = Path(__file__).parent


def run(arm: str) -> dict:
    bins: collections.Counter = collections.Counter()
    # THE PARK VERDICT IS THE ACTUAL GATE, and it is recorded rather than inferred.
    # `mint` runs its whole search behind `if guards["support"] and base > floor`, and when
    # it parks it writes WHICH of those stopped it: `no_support` (base <= 0) or
    # `under_floor` (base <= the cheapest term's cost), against `budget_spent` /
    # `depth_exhausted`, which mean the search RAN and found nothing.
    verdicts: collections.Counter = collections.Counter()
    base_by_verdict: dict[str, list] = collections.defaultdict(list)
    support: collections.Counter = collections.Counter()
    per_slot: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    env = world.bind(gridworld.family(arm, SEED, CYCLES))
    led = ledger.Ledger()
    real = led.record

    def spy(*a, **kw):
        # *args, NOT a named signature. `record` is called with `kind` positionally at some
        # sites and by keyword at others, and a fixed signature collided on the second kind.
        # The spy must not care how the real call is shaped -- it only reads `bin`.
        if "bin" in kw:
            bins[kw["bin"]] += 1
            slot = a[2] if len(a) > 2 else kw.get("slot")
            per_slot[str(slot)][kw["bin"]] += 1
            if "support" in kw:
                support[kw["support"]] += 1
        if "verdict" in kw:
            verdicts[kw["verdict"]] += 1
            if "base_bits" in kw:
                base_by_verdict[kw["verdict"]].append(kw["base_bits"])
        return real(*a, **kw)

    led.record = spy
    ag = tether.Agent(env, G.Gamma(env.atoms()), tether.Config(max_depth=2), led)
    err = ""
    try:
        for _ in range(CYCLES):
            ag.step()
    except Exception as exc:                                  # noqa: BLE001
        err = f"{type(exc).__name__}: {exc}"
    return {"arm": arm, "error": err, "bins": dict(bins), "support": dict(support),
            "verdicts": dict(verdicts),
            "base_by_verdict": {k: {"n": len(v), "min": min(v), "max": max(v)}
                                for k, v in base_by_verdict.items() if v},
            "per_slot": {k: dict(v) for k, v in per_slot.items()},
            "bargain_paid": ag.gamma.book.get("bargain_paid", 0),
            "bounded_out": ag.gamma.book.get("bargain_bounded_out", 0)}


def show(r: dict) -> None:
    total = sum(r["bins"].values())
    print(f"  ARM {r['arm']}   ROUTE rows {total}   "
          f"bargain_paid {r['bargain_paid']}   bounded_out {r['bounded_out']}")
    if r["error"]:
        print(f"    ERROR {r['error']}")
    if total == 0:
        print("    NO ROUTE ROWS AT ALL -- the classifier never ran. Nothing to census.")
        return
    for b, n in sorted(r["bins"].items(), key=lambda kv: -kv[1]):
        mark = "  <- CAN REACH mint" if b in MINTING else ""
        print(f"    {b:12} {n:6d}  {100.0 * n / total:5.1f}% of {total}{mark}")
    reach = sum(n for b, n in r["bins"].items() if b in MINTING)
    print(f"    minting-capable {reach} of {total} = {100.0 * reach / total:.1f}%")
    v = r.get("verdicts") or {}
    if v:
        vt = sum(v.values())
        print(f"    MINT PARK VERDICTS -- why the search did not run, {vt} parks:")
        for k, n in sorted(v.items(), key=lambda kv: -kv[1]):
            bb = (r.get("base_by_verdict") or {}).get(k)
            rng = f"   base_bits {bb['min']}..{bb['max']}" if bb else ""
            gate = "  <- SEARCH NEVER RAN" if k in ("no_support", "under_floor") else ""
            print(f"      {k:16} {n:6d}  {100.0 * n / vt:5.1f}% of {vt}{rng}{gate}")
    else:
        print("    MINT PARK VERDICTS: none recorded -- mint never parked.")
    sup = r["support"]
    if sup:
        st = sum(sup.values())
        lo = sum(n for k, n in sup.items() if int(k) < 2)
        print(f"    support < 2 (the NOVEL condition): {lo} of {st} "
              f"= {100.0 * lo / st:.1f}%   distribution {dict(sorted(sup.items()))}")


def main(argv: list[str]) -> int:
    arm = argv[1] if len(argv) > 1 else "compare"
    if arm == "compare":
        print(f"WORLD gridworld seed {SEED}, no ARC board. {CYCLES} cycles. "
              f"ONE ARM PER PROCESS.")
        print("POPULATION: every ROUTE row the agent wrote. Tallied at the recording site.\n")
        for a in ("default", "click_only"):
            p = HERE / f"bins_{a}.json"
            if not p.exists():
                print(f"  {a}: NOT RUN")
                continue
            show(json.loads(p.read_text(encoding="utf-8")))
            print()
        return 0
    r = run(arm)
    (HERE / f"bins_{arm}.json").write_text(json.dumps(r, indent=1), encoding="utf-8")
    show(r)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
