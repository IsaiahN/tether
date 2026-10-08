"""compile_census: M3, record-only (METAPROGRAMMING_DESIGN section 8; the reviewer
2026-10-08 21:58Z).

    python compile_census.py      writes docs/cohesion/COMPILE_CENSUS.md and prints its summary

Two readings, both records, neither a gate:
1. THE LIBRARY: every seed entry's candidates in every role, compiled by compile_term against
   the atoms the ARC wiring builds -- compiled / refused by reason, per role, and how many
   entries each role can offer at least one compiled term for. A CAUSE / RESULT candidate is a
   pair (if, then) and counts as compiled only when both sides compile.
2. THE COST OF EACH PROPOSED WIDENING (7a, 7b, a pair atom): library rows gained, and the growth
   in the chains enumerate_closure would type-check at depths 2-4 (Gamma.space_exact, summed
   over every type pair the atoms produce). Measured on the ARC atom set: gridworld's 13 atoms
   hold none of sign / negate / touching, so a gridworld measurement could not show a change.
"""
from __future__ import annotations

import collections
import dataclasses
import sys
from pathlib import Path

sys.dont_write_bytecode = True

import arc_atoms  # noqa: E402
import arc_percept  # noqa: E402
import arc_predict  # noqa: E402
import compile_term as C  # noqa: E402
import gamma  # noqa: E402
import tether  # noqa: E402

sys.path.insert(0, str(Path(__file__).parent / "library"))
import library_runtime as LR  # noqa: E402

OUT = Path(__file__).parent / "docs" / "cohesion" / "COMPILE_CENSUS.md"
DEPTHS = (2, 3, 4)


def arc_atoms_wired() -> dict[str, gamma.Atom]:
    """The atom set the ARC path builds, wired as arc_holdout.wire wires it."""
    arc_atoms._ITERATE = True
    tether._SHAPE_DECODE = True
    arc_percept._SHAPE_DELTA = True
    return {a.name: a for a in arc_atoms.three_spaces(arc_predict.predict())}


def _one(cand: dict, atoms: dict) -> str | None:
    """None when the candidate compiles, else its refusal reason."""
    if "condition" in cand:
        r = C.compile_candidate(cand, atoms)
        return r.reason if isinstance(r, C.Refusal) else None
    for side in ("if", "then"):
        if side in cand:
            r = C.compile_candidate({"condition": cand[side]}, atoms)
            if isinstance(r, C.Refusal):
                return f"{side}: {r.reason}"
    return None if ("if" in cand or "then" in cand) else "no condition in the candidate"


def library_census(lib: LR.Library, atoms: dict) -> dict:
    per_role = {}
    for role in LR.ROLES:
        n = ok = 0
        reasons: collections.Counter = collections.Counter()
        offering = 0
        for key in lib.seed:
            any_ok = False
            for cand in lib.view(key, role):
                n += 1
                why = _one(cand, atoms)
                if why is None:
                    ok += 1
                    any_ok = True
                else:
                    reasons[why] += 1
            offering += any_ok
        per_role[role] = {"candidates": n, "compiled": ok, "refused": dict(reasons.most_common()),
                          "entries_offering": offering}
    return per_role


def closure(atoms: dict) -> dict[int, int]:
    """Chains enumerate_closure would type-check, per depth, over every (in, out) type pair."""
    g = gamma.Gamma(list(atoms.values()), game="compile_census")
    units = g.units()
    ins = sorted({t for a in atoms.values() for t in a.accepts})
    outs = sorted({a.out_type for a in atoms.values()})
    return {d: sum(g.space_exact(units, i, o, d) for i in ins for o in outs) for d in DEPTHS}


def widenings(atoms: dict) -> dict[str, dict]:
    """Each proposed change as a modified atom set (section 7a, 7b, the pair atom)."""
    w7a = dict(atoms)
    w7a["sign"] = dataclasses.replace(atoms["sign"],
                                      also_accepts=atoms["sign"].also_accepts + ("EXTENT",))
    w7b = dict(atoms)
    for k, a in atoms.items():
        if a.in_type == "PRED" and "BOOL" not in a.accepts:
            w7b[k] = dataclasses.replace(a, also_accepts=a.also_accepts + ("BOOL",))
    wpair = dict(atoms)
    wpair["touches"] = gamma.Atom("touches", lambda _v, _c: gamma.NOT_RESOLVED, "OBJECT", "BOOL",
                                  reads_operand=True, operand_type="OBJECT",
                                  reads_ctx=("operands",))
    return {"7a sign accepts EXTENT": w7a, "7b PRED atoms accept BOOL": w7b,
            "pair atom touches<x>": wpair}


def merge_percept(lib: LR.Library) -> str:
    """What the library lights when two touching objects take one colour: the habitat merges
    them into one component (one grows, one vanishes), measured on a real observer frame."""
    import cue_bridge
    import observer

    def board(objs):
        g = [[0] * 10 for _ in range(10)]
        for (r, c, h, w, col) in objs:
            for i in range(h):
                for j in range(w):
                    g[r + i][c + j] = col
        return g
    live = observer.Live()
    live.see(board([(1, 2, 2, 2, 3), (1, 4, 2, 2, 5)]))
    cue = live.see(board([(1, 2, 2, 2, 3), (1, 4, 2, 2, 3)]))
    unmapped: dict = {}
    changed = cue_bridge.changed_readings(cue, unmapped)
    lit = lib.light(changed)
    return (f"Two touching objects take one colour: the cue reads {cue['mutations']}; the bridge "
            f"gives {changed} (unmapped {unmapped}); {len(lit)} library entries light, top "
            f"{[k for k, _ in lit[:5]]}. This is how absorption / merging reads today.")


def main() -> int:
    lib = LR.Library("library").load()
    atoms = arc_atoms_wired()
    base = library_census(lib, atoms)
    base_close = closure(atoms)
    lines = ["# Compile census (M3) -- record-only", "",
             f"Library: {len(lib.seed)} seed entries x {len(LR.ROLES)} roles, compiled against "
             f"the {len(atoms)} atoms the ARC wiring builds. Generated by `compile_census.py`.", "",
             "| role | candidates | compiled | refused | entries offering a compiled term |",
             "|---|---|---|---|---|"]
    for role, r in base.items():
        lines.append(f"| {role} | {r['candidates']} | {r['compiled']} | "
                     f"{r['candidates'] - r['compiled']} | {r['entries_offering']} |")
    lines += ["", "## Refusals, by reason, per role", ""]
    for role, r in base.items():
        if r["refused"]:
            parts = "; ".join(f"{why} -- {n}" for why, n in r["refused"].items())
            lines.append(f"- **{role}**: {parts}")
    lines += ["", "## Each proposed widening: gain in library rows, cost in search", "",
              "Closure = chains `enumerate_closure` would type-check (`Gamma.space_exact`, "
              "summed over "
              "every in/out type pair), per depth.", "",
              f"Base closure: {base_close}", "",
              "| change | compiled candidates (all roles) | gain | closure d2 / d3 / d4 | growth |",
              "|---|---|---|---|---|"]
    base_ok = sum(r["compiled"] for r in base.values())
    for name, wa in widenings(atoms).items():
        census = library_census(lib, wa)
        ok = sum(r["compiled"] for r in census.values())
        cl = closure(wa)
        growth = " / ".join(f"x{cl[d] / base_close[d]:.2f}" if base_close[d] else "n/a"
                            for d in DEPTHS)
        lines.append(f"| {name} | {ok} | +{ok - base_ok} | {cl[2]} / {cl[3]} / {cl[4]} "
                     f"| {growth} |")
    pair_refused = sum(n for r in base.values() for why, n in r["refused"].items()
                       if "no pairwise atom" in why)
    lines += ["", f"The pair atom's library gain reads +0 because compile_term has no row that "
              f"routes a pair call to a pair atom, so adding the atom changes no compile. Its "
              f"POTENTIAL: {pair_refused} candidate refusals name a missing pairwise atom (an "
              f"upper bound: a CAUSE candidate refused on one side may still fail the other)."]
    lines += ["", "## The merge percept (record for the census, not a fixture)", "",
              merge_percept(lib)]
    lines += ["", "Record-only: nothing here is built. The pair atom is measured as a declared "
              "signature (OBJECT with an OBJECT operand -> BOOL); its reading would come from the "
              "cue's pairs, which the relation commit publishes."]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
