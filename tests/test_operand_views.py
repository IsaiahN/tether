"""BUILD 3 ITEM 8a, THE OPERAND READS EVERY HELD VIEW (TETHER_OPERAND_VIEWS; the reviewer 2026-11-04
r1085). Measured at 0075509 (census18, ls20): no live operand read a change reading (drow, dcol,
dcells, ...), because _entry_operand read one role per entry (STATE for 3985 of 4048) and only its
first side, while drow is read by 3118 entries' PROCESS views and CAUSE then-sides. The fixture is
a gridworld agent calling _entry_operand with ARC's atoms on REAL library entries of that shape.
Seconds.

MF-V1  on every fixture entry the operand reads drow and _read_terms["drow"] is set (> 0 entries)
MF-V2  first-seen terms stay: over the fixture, every reading that had a term with the arm OFF has
       the SAME term with it ON; the arm only adds terms for readings that had none
The red is behavioural, the arm OFF on this tree: TETHER_OPERAND_VIEWS=0 fails MF-V1.

    python tests/test_operand_views.py
"""
from __future__ import annotations

import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import arc_atoms  # noqa: E402
import arc_predict  # noqa: E402
import compile_term  # noqa: E402
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

READS = ("row", "col", "drow", "dcol", "age", "stability", "h", "w", "filled", "colour", "shape",
         "dcells", "dw", "dh", "dperimeter", "dcontact")
FRAME = {f"o0.{r}" for r in READS}


def agent():
    env = world.bind(gridworld.family("default", 0))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                        ledger.Ledger())


def first_side_reads(lib, k, role, atoms):
    out = set()
    for cand in lib.view(k, role, tether.PH_O, tether.PH_X):
        if "quantifier" in cand:
            continue
        cond = cand["if" if role == "CAUSE" else "condition"]
        c = compile_term.compile_candidate({"condition": cond}, atoms, subject=tether.PH_O)
        if isinstance(c, compile_term.Compiled):
            out |= {s.split(".", 1)[1] for s in (c.slot, c.operand)
                    if s and "." in s and s.split(".", 1)[0] in (tether.PH_O, tether.PH_X)}
    return out


def main():
    arc = arc_atoms.three_spaces(arc_predict.predict())
    g = gamma.Gamma(gamma.primitives_once(arc), game="arc")
    atoms = {a.name: a for a in g.atoms}
    sig = compile_term.signature(atoms)
    lib = tether._library()
    # the fixture: STATE entries whose own view reads row and no drow (the census18 shape), the
    # first eight in seed order, ZOOLOGICAL|Celestial (15 views) among them by name
    fix = ["ZOOLOGICAL|Celestial"]
    for k in lib.seed:
        if len(fix) >= 8:
            break
        if k in fix or ((lib.get(k) or {}).get("role_of", {}).get("role") or "STATE") != "STATE":
            continue
        own = first_side_reads(lib, k, "STATE", atoms)
        if "row" in own and "drow" not in own:
            fix.append(k)
    assert len(fix) > 1, ("the fixture has no entry", fix)

    on = agent()
    for k in fix:
        on._entry_operand([k], FRAME, lib, atoms, sig)
    had = []
    for k in fix:
        a = agent()
        got, how, _why = a._entry_operand([k], FRAME, lib, atoms, sig)
        had.append((k, how, sorted({s.split(".", 1)[1] for ss in (got or {}).values() for s in ss}),
                    "drow" in a._read_terms))
    bad = [h for h in had if "drow" not in h[2] or not h[3]]
    assert not bad, ("MF-V1: an entry's operand reads no drow, or no drow term", len(bad), bad[:3])
    print(f"  MF-V1 {len(fix)} entries (ZOOLOGICAL|Celestial first): each operand reads drow and "
          f"sets _read_terms['drow']; e.g. {had[0][0]} reads {had[0][2]}")

    was = tether._OPERAND_VIEWS
    try:
        tether._OPERAND_VIEWS = False
        off = agent()
        for k in fix:
            off._entry_operand([k], FRAME, lib, atoms, sig)
    finally:
        tether._OPERAND_VIEWS = was
    assert off._read_terms, "MF-V2 has no OFF term to compare"
    moved = [r for r, t in off._read_terms.items() if on._read_terms.get(r) != t]
    assert not moved, ("MF-V2: a reading's term changed under the arm", moved)
    added = sorted(set(on._read_terms) - set(off._read_terms))
    assert "drow" in added and "drow" not in off._read_terms, ("MF-V2: drow not added", added)
    print(f"  MF-V2 OFF had terms for {sorted(off._read_terms)}; ON keeps each the same and adds "
          f"{added}")
    print("test_operand_views OK")


if __name__ == "__main__":
    main()
