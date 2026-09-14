"""The self-graded curriculum (TRAINING_PLAN.md Stage 1; reviewer-steered 2026-09-14).

The library-closure IS a curriculum. Grow the parts bin by promoting reused parts from a TRAIN
split, and measure the cost of expressing HELD-OUT composites as the bin grows. Held-out cost
FALLING as the bin grows = the parts-bin flywheel compounds; FLAT = the central thesis does not
compound over this substrate -- found in a sandbox, not on the board.

A different HABITAT (Figure 11), not an instrument: the composer's cost model (a settled
sub-composition costs ONE unit) run over a domain with no spatial content. Fitness is re-derivation
inside the held-out library, never target-game performance -- the random split carries no board
information (Isaiah's contamination defence).

COMPOUNDING BY CONSTRUCTION: proper set-Re-Pair. A composite is a SET of current symbols (initially
atoms). Repeatedly merge the most-frequent co-occurring symbol PAIR into a new symbol -- and a
merged symbol can itself be merged again, so parts-of-parts DO form. Without this the flywheel is
suppressed by the harness and a flat result is uninterpretable.
"""
from __future__ import annotations

import collections
import itertools
import json
import random

HELDOUT = 0.3            # anchor: fraction held out, random ACROSS TIERS (reviewer's constraint)
MAX_PROMOTIONS = 200     # anchor: bin-size cap, the x-axis of the flywheel curve


def load_composites(path: str = "docs/library-closure/WORKING_SET.json") -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    out = []
    for c in d.get("set_b_level2", []):
        r = c.get("recipe")
        if not r:
            continue
        atoms = frozenset(x.strip() for x in r.split("+") if x.strip())
        if len(atoms) >= 2:
            out.append({"name": c.get("name"), "atoms": atoms})
    return out


def cost_in_symbols(atomset: frozenset, symbols: dict) -> int:
    """Minimum symbols to cover this atom set, greedy largest-first. A promoted symbol (a merged
    atom-subset) covers all its atoms for ONE unit -- the units-pricing over a set."""
    remaining = set(atomset)
    cost = 0
    for members in sorted(symbols.values(), key=len, reverse=True):
        if members <= remaining:
            remaining -= members
            cost += 1
    cost += len(remaining)
    return cost


def run(seed: int = 0) -> dict:
    comps = load_composites()
    rng = random.Random(seed)
    rng.shuffle(comps)
    n_test = int(len(comps) * HELDOUT)
    test, train = comps[:n_test], comps[n_test:]
    # each TRAIN composite as a mutable set of current symbol-ids; sym[id] = frozenset of atoms
    symbols: dict[int, frozenset] = {}
    train_syms = [set(c["atoms"]) for c in train]     # symbols start as atom names
    sym_atoms = {a: frozenset((a,)) for c in train for a in c["atoms"]}  # atom -> its own set

    def test_cost():
        return sum(cost_in_symbols(c["atoms"], symbols) for c in test)
    base = test_cost()
    traj = [(0, base)]
    ids = itertools.count()
    for k in range(1, MAX_PROMOTIONS + 1):
        # most-frequent co-occurring pair of CURRENT symbols across train composites
        pair_freq = collections.Counter()
        for s in train_syms:
            for a, b in itertools.combinations(sorted(s), 2):
                pair_freq[(a, b)] += 1
        if not pair_freq:
            break
        (a, b), f = pair_freq.most_common(1)[0]
        if f < 2:                                  # nothing reused -> nothing to compound
            break
        nid = f"U{next(ids)}"
        merged = sym_atoms[a] | sym_atoms[b]       # parts-of-parts: union of member atoms
        sym_atoms[nid] = merged
        symbols[nid] = merged                      # a promoted unit in the bin
        for s in train_syms:                       # replace the pair with the new symbol
            if a in s and b in s:
                s.discard(a)
                s.discard(b)
                s.add(nid)
        if k in (1, 5) or k % 20 == 0:
            traj.append((k, test_cost()))
    final = test_cost()
    traj.append((len(symbols), final))
    return {"n_test": len(test), "n_train": len(train),
            "base_test_cost": base, "final_test_cost": final,
            "reduction_pct": round(100 * (base - final) / base, 1) if base else 0,
            "bin": len(symbols), "trajectory": traj}


if __name__ == "__main__":
    for seed in (0, 1, 2):
        r = run(seed)
        print(f"seed {seed}: heldout cost {r['base_test_cost']} -> {r['final_test_cost']} "
              f"({r['reduction_pct']}% down) | bin {r['bin']}")
        print("   (bin, cost):", " ".join(f"{k}:{c}" for k, c in r["trajectory"]))
