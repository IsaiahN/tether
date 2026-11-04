"""A LIT SEVERAL-JUNCTION MOLECULE IS JUDGED WHOLE (TETHER_LIT_COVER; the reviewer 2026-11-04
r1130). On ls20 the 44 molecules cut B refuses ("a junction of a several-junction molecule") were
disjoint from the cover route's candidates -- composer.candidates admits by held atom NAMES -- so
the place where r966 judges a whole never saw them. Now the cover route walks them first, once,
when every ingredient resolves, and offers only a whole whose every junction settles. Seconds: the
fixture of
tests/test_molecule_apply.py (hand-built window, forced verdicts).

MF-C1  a lit 2-junction molecule (inc → dec) → neg, no cover candidate: offered WHOLE,
       inc . dec . neg at o1.z read from o1.row, prov source "cover", junctions 2, lit;
       lit_cover {walked 1, offers 1}; arm forced OFF: only the lookup count, no offer
MF-C2  (a) an ingredient that does not resolve: never judged, counted "lit: an ingredient does not
       resolve: <name> (<how>)", lit_cover {unresolved 1}, nothing offered
MF-C3  (b) a junction that does not settle: counted with the junction that failed, nothing offered
The red is behavioural, the arm OFF on this tree: TETHER_LIT_COVER=0 fails MF-C1.

    python tests/test_lit_cover.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import composer  # noqa: E402
import test_molecule_apply as tm  # noqa: E402
import tether  # noqa: E402

LIT = "ZZZ|Lit"


def run(node, per_object, flag=None):
    """the pass with one LOOKUP pair lighting LIT (2 junctions) and no cover candidate."""
    ag, led = tm.agent()
    keep = (composer.candidates, composer.recipe_rows, composer.light, tether._mol_junctions,
            tether.Agent.__dict__["_per_object"], tether._LIT_COVER)
    try:
        composer.candidates = lambda *_a, **_k: []
        composer.recipe_rows = lambda: {LIT: {}}
        composer.light = lambda _row, _standing=None: node
        tether._mol_junctions = lambda: {LIT: 2}
        tether.Agent._per_object = staticmethod(per_object)
        if flag is not None:
            tether._LIT_COVER = flag
        ag.trace = [(tm.FR[t], "ACTION1", tm.FR[t + 1]) for t in range(4)]
        ag._window_at, ag._mol_key = 0, None
        ag.bound = {"o1.row": "inc", "o2.row": "inc", "o1.col": "dec", "o2.col": "dec",
                    "o3.x": "idn", "o1.z": "neg"}
        ag._lookup_pairs = {"o1.col": [{"molecule": LIT, "left": "a", "right": "b",
                                        "left_reading": "o1.row", "right_reading": "o1.col",
                                        "held": ["→"], "via": [], "occasions": {}}]}
        ag._molecule_pass()
    finally:
        (composer.candidates, composer.recipe_rows, composer.light, tether._mol_junctions,
         tether.Agent._per_object, tether._LIT_COVER) = keep
    row = [r.get("detail", r) for r in led.rows() if r.get("event") == "molecule_apply"][-1]
    return getattr(ag, "_mol_order", []), row


def main():
    whole = composer.Bonded(composer.UNKNOWN, composer.Bonded(composer.UNKNOWN, "inc", "dec"),
                            "neg")
    order, row = run(whole, tm.only({"→"}))
    lit = [p for p in order if p.get("lit")]
    assert lit and all(p["source"] == "cover" and p["junctions"] == 2 for p in lit) \
        and any(p["offer"] == "inc . dec . neg" and p["right"] == "o1.z" and p["left"] == "o1.row"
                for p in lit) and row.get("lit_cover", {}).get("walked") == 1, (
        "MF-C1: the lit 2-junction molecule is not offered whole", order, row.get("lit_cover"))
    off, row_off = run(whole, tm.only({"→"}), flag=False)
    assert not [p for p in off if p["molecule"] == LIT] and row_off["not_offered"].get(
        "lookup: a junction of a several-junction molecule") == 1 and "lit_cover" not in row_off, (
        "MF-C1 OFF: the lit molecule is offered or not counted", off, row_off)
    print(f"  MF-C1 offered whole: {[(p['offer'], p['left'], p['right']) for p in lit]}; "
          f"lit_cover {row['lit_cover']}; OFF: no offer, counted once")
    bad = composer.Bonded(composer.UNKNOWN, composer.Bonded(composer.UNKNOWN, "inc", "dec"),
                          "zzz_no_such_ingredient")
    order, row = run(bad, tm.only({"→"}))
    why = [k for k in row["not_offered"] if k.startswith("lit: an ingredient does not resolve: "
                                                         "zzz_no_such_ingredient")]
    assert why and not [p for p in order if p["molecule"] == LIT] and \
        row.get("lit_cover") == {"unresolved": 1}, (
        "MF-C2", row["not_offered"], row.get("lit_cover"))
    print(f"  MF-C2 unresolved: {why[0]!r}; lit_cover {row['lit_cover']}")
    order, row = run(whole, tm.only({"→"}, unless="o1.z"))
    why = [k for k in row["not_offered"] if k.startswith("lit: junction ")]
    assert why and not [p for p in order if p["molecule"] == LIT], ("MF-C3", row["not_offered"])
    print(f"  MF-C3 a junction not settled: {why[0]!r}")
    print("test_lit_cover OK")


if __name__ == "__main__":
    main()
