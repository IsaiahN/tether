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
    if "quantifier" in cand:
        return C.QUANTIFIED
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


def relation_set_arm() -> tuple[int, dict, dict]:
    """Step 4 (i) (the reviewer 2026-10-11 13:31 CDT): the census with TETHER_RELATION_SET ON --
    `below` in the atom set, pair readings stated -- beside the OFF base. In a FRESH process: the
    arm admits `below` at import (ADMITTED), so it cannot be switched on inside this one."""
    import json
    import os
    import subprocess
    code = ("import json, compile_census as M; lib = M.LR.Library('library').load(); "
            "a = M.arc_atoms_wired(); "
            "print(json.dumps([len(a), M.library_census(lib, a), M.closure(a)]))")
    env = dict(os.environ, TETHER_RELATION_SET="1", PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env=env,
                       cwd=str(Path(__file__).parent), timeout=1200)
    if p.returncode:
        raise RuntimeError(p.stderr[-2000:])
    n, census, close = json.loads(p.stdout.strip().splitlines()[-1])
    return n, census, {int(k): v for k, v in close.items()}


# The call-family items (the reviewer 2026-10-11 14:17 CDT), keyed by their OFF refusal.
FAMILY_ITEM = {"quantified over the group": "2, the group row",
               "no pairwise atom: contact(o, x)": "5, contact",
               "no pairwise atom: bbox(o, x)": "6, bbox",
               "no pairwise atom: inside(o, x)": "7, inside",
               "no template for the observer pair inside": "7, inside",
               "a BOOL is 0 or 1": "7, inside",
               "holds does not accept EXTENT": "9, EXTENT == 0"}


def families(census: dict) -> collections.Counter:
    """Refusals summed over roles, the if:/then: side folded away."""
    fam: collections.Counter = collections.Counter()
    for r in census.values():
        for why, k in r["refused"].items():
            fam[why.split(": ", 1)[-1] if why.startswith(("if: ", "then: ")) else why] += k
    return fam


def widenings(_atoms: dict) -> dict[str, tuple[dict, dict]]:
    """Proposed widenings not yet built, each an atom set and the compile rows it would use.
    None pending: 7a, touches<x> and 7b (the bridge atom holds, the reviewer 2026-10-08 23:54Z,
    over every PRED atom accepting BOOL) are built and in the base."""
    return {}


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
    notes: list[str] = []
    base_ok = sum(r["compiled"] for r in base.values())
    import test_compile
    for name, (wa, rows) in widenings(atoms).items():
        keep = {k: C.TABLE[k] for k in rows}
        C.TABLE.update(rows)
        try:
            census = library_census(lib, wa)
            wrong = len(test_compile.disagreements(wa)[0])
        finally:
            C.TABLE.update(keep)
        ok = sum(r["compiled"] for r in census.values())
        cl = closure(wa)
        notes.append(f"- {name}: {wrong} template-frame disagreement(s) with condition.evaluate "
                     f"among the rows it compiles")
        growth = " / ".join(f"x{cl[d] / base_close[d]:.2f}" if base_close[d] else "n/a"
                            for d in DEPTHS)
        lines.append(f"| {name} | {ok} | +{ok - base_ok} | {cl[2]} / {cl[3]} / {cl[4]} "
                     f"| {growth} |")
    n_on, on, on_close = relation_set_arm()
    on_ok = sum(r["compiled"] for r in on.values())
    growth = " / ".join(f"x{on_close[d] / base_close[d]:.2f}" if base_close[d] else "n/a"
                        for d in DEPTHS)
    lines.append(f"| TETHER_RELATION_SET ON ({n_on} atoms) | {on_ok} | "
                 f"+{on_ok - base_ok} | {on_close[2]} / {on_close[3]} / {on_close[4]} "
                 f"| {growth} |")
    lines += ["", "## TETHER_RELATION_SET: compiled / refused per role, OFF -> ON", "",
              "| role | compiled OFF | compiled ON | refused OFF | refused ON |",
              "|---|---|---|---|---|"]
    for role in base:
        b, a = base[role], on[role]
        lines.append(f"| {role} | {b['compiled']} | {a['compiled']} | "
                     f"{b['candidates'] - b['compiled']} | {a['candidates'] - a['compiled']} |")
    lines += ["", "BASE DRIFT since the 2026-10-08 census (3a59b23): RELATION compiled 57,386 -> "
              "55,535 OFF. The 1,851 rows are exactly the family 'a change reading compared "
              "across objects reads no slot', introduced at 4dcb447 (2026-10-09, the M4 reach "
              "wire's CHANGE_OF route) -- a compile_term change, not step 2 and not the arm.",
              "", "Bounded by design (the reviewer 2026-10-11 14:17 CDT): events are not slots "
              "(an event is a transition, carried by the change readings); action(o, x) (the "
              "agent's own action is not a perceived slot); the board is not an object slot (only "
              "@goal.completed is); a change reading compared across objects.",
              "", "## Refusal families OFF -> ON (summed over roles; a refusal that moves to "
              "another reason is counted under each)", "",
              "| family | item | refused OFF | refused ON | change |",
              "|---|---|---|---|---|"]
    fam_off, fam = families(base), families(on)
    for why in sorted(set(fam_off) | set(fam), key=lambda w: (-fam_off.get(w, 0), w)):
        item = next((v for k, v in FAMILY_ITEM.items() if why.startswith(k)), "")
        a, b = fam_off.get(why, 0), fam.get(why, 0)
        lines.append(f"| {why} | {item} | {a} | {b} | {b - a:+d} |")
    fell = sum(fam_off[w] - fam.get(w, 0) for w in fam_off if fam_off[w] > fam.get(w, 0))
    rose = sum(fam[w] - fam_off.get(w, 0) for w in fam if fam[w] > fam_off.get(w, 0))
    lines += ["", f"A fall is not a compiled row: a refusal can move to another reason. Refusals "
              f"that fell {fell}, refusals that rose {rose}; {fell} - {rose} = {fell - rose}, "
              f"the compiled gain over all roles is {on_ok - base_ok}."]
    lines += ["", "Family 2 (the RULE role, the reviewer 2026-10-11 14:50 CDT; "
              "docs/cohesion/GROUP_ROW_NOTE.md, measured at 22d8273): a RULE row is a LAW, not a "
              "goal. ROUTABLE, NO CONSUMER: 40,835 (20,043 all_same + 2,477 distinct + 18,315 "
              "per-object AND over peers) -- no reader asks for the RULE role, so no routing is "
              "built; VACUOUS AS WRITTEN: 35,132 (an order over all ordered pairs); the rest "
              "(12,400 one-object, 1,619 board) stay in their own families."]
    lines += ["", "Correctness of what each form would compile (the equivalence fixture run "
              "under it):",
              ""] + notes
    lines += ["", "## The merge percept (record for the census, not a fixture)", "",
              merge_percept(lib)]
    lines += ["", "Record-only. 7a, touches<x> and holds are in the base above (the reviewer's "
              "rulings 2026-10-08 23:23Z and 23:54Z); no widening is pending."]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
