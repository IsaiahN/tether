"""BUILD 2, MOLECULE APPLY (TETHER_MOLECULE_APPLY; the reviewer 2026-11-03 r962, r963). A lit
molecule whose junction settles on operands resolved on this board is offered to the bargain as a
library offer at the slot it predicts, priced by the one loop; seen objects first, then
generalised. About 10 s.

MF-M1  a settled → (inc then dec, held on o1 only) becomes the chain inc . dec offered at o1.col
       read from o1.row (seen) and at o2.col read from o2.row (generalised), in that order; RED on
       HEAD
MF-M2  an ambiguous junction (+ and → both True) is not offered
MF-M3  a ⇒-settled junction is not offered: "⇒: bond has no atom (r896)"
MF-M3b a +-settled junction is not offered: "bond +: implemented_by AGENT|both not wired as a
       term", counted per bond (r966)
MF-M4  the offer enters the library stream: _library_chains yields inc . dec at o1.col with o1.row
       first among its operands, as the plain library offer of the same chain does -- one door, one
       price
MF-M5  several junctions, every one settled: (inc → dec) → neg offers exactly ONE chain carrying
       every bond, inc . dec . neg at o1.z read from o1.row -- never the leaf pairs inc . neg,
       dec . neg (r966); with the inner junction settled on + it is not offered, "inner bond +
       has no term form"
MF-M6  one inner junction not settled: nothing offered, "a junction of several: not settled"
MF-OFF the arm OFF: no pass, no offers, no molecule rows

    python tests/test_molecule_apply.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import composer  # noqa: E402
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

FR = [{"o1.row": r, "o1.col": c, "o1.z": 0, "o2.row": 5, "o2.col": 5, "o3.x": 0}
      for r, c in ((0, 0), (1, 0), (1, 1), (2, 1), (2, 2))]


def agent():
    env = world.bind(gridworld.family("default", 0))
    led = ledger.Ledger()
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
    ag.step()
    return ag, led


def run(per_object=None, node=None):
    """the pass over the hand-built window with one molecule (inc ? dec unless given) -> (agent,
    the offers in order, the pass's row)."""
    ag, led = agent()
    mols = [{"molecule": "ZZZ|M",
             "node": node or composer.Bonded(composer.UNKNOWN, "inc", "dec")}]
    was = (composer.candidates, tether.Agent._per_object)
    try:
        composer.candidates = lambda *_a, **_k: mols
        if per_object is not None:
            tether.Agent._per_object = staticmethod(per_object)
        ag.trace = [(FR[t], "ACTION1", FR[t + 1]) for t in range(4)]
        ag._window_at, ag._mol_key = 0, None
        ag.bound = {"o1.row": "inc", "o2.row": "inc", "o1.col": "dec", "o2.col": "dec",
                    "o3.x": "idn", "o1.z": "neg"}
        ag._molecule_pass()
    finally:
        composer.candidates, tether.Agent._per_object = was
    row = [r.get("detail", r) for r in led.rows() if r.get("event") == "molecule_apply"][-1]
    return ag, getattr(ag, "_mol_order", []), row


def only(bonds, unless=None):
    """a forced verdict: True for the bonds named, None otherwise -- and None for every bond on a
    junction whose right operand reads the slot `unless`."""
    def f(bond, _left, right, objs, _frames, _bound, _skip, seen=None):
        hit = bond in bonds and not (unless and any(unless in v for v in right.values()))
        if hit and seen is not None:
            seen.append(objs[0])
        return (True if hit else None, "forced", "TEST",
                {"occasions": 1, "deciding": [], "specific": []})
    return f


def main():
    if "--off" in sys.argv:
        assert not tether._MOLECULE_APPLY
        ag, led = agent()
        for _ in range(5):
            ag.step()
        ev = {r.get("event") for r in led.rows()}
        assert not ev & {"molecule_apply", "molecule_offer"} and not ag._mol_offers, ev
        print("off ok")
        return
    assert tether._MOLECULE_APPLY, "the arm is ON by default"
    ag, order, row = run()
    got = [(p["object"], p["seen"], p["left"], p["right"], p["offer"]) for p in order]
    assert got == [("o1", True, "o1.row", "o1.col", "inc . dec"),
                   ("o2", False, "o2.row", "o2.col", "inc . dec")], ("MF-M1", got, row)
    _a, o2, r2 = run(only({"+", "→"}))
    assert not o2 and r2["not_offered"].get("ambiguous") == 1, ("MF-M2", r2)
    _a, o3, r3 = run(only({"⇒"}))
    assert not o3 and r3["not_offered"].get("⇒: bond has no atom (r896)") == 1, ("MF-M3", r3)
    _a, o3b, r3b = run(only({"+"}))
    assert not o3b and r3b["not_offered"] == {
        "bond +: implemented_by AGENT|both not wired as a term": 1}, ("MF-M3b", r3b)
    two = composer.Bonded(composer.UNKNOWN, composer.Bonded(composer.UNKNOWN, "inc", "dec"),
                          "neg")
    _a, o5, r5 = run(only({"→"}), two)
    got5 = sorted((p["left"], p["right"], p["offer"], p["junctions"]) for p in o5)
    assert got5 == [("o1.row", "o1.z", "inc . dec . neg", 2)], ("MF-M5", got5, r5)

    def inner_plus(bond, _left, right, objs, _frames, _bound, _skip, seen=None):
        inner = any("o1.col" in v for v in right.values())
        hit = bond == ("+" if inner else "→")
        if hit and seen is not None:
            seen.append(objs[0])
        return (True if hit else None, "forced", "TEST",
                {"occasions": 1, "deciding": [], "specific": []})
    _a, o5b, r5b = run(inner_plus, two)
    assert not o5b and r5b["not_offered"] == {"inner bond + has no term form": 1}, ("MF-M5b", r5b)
    _a, o6, r6 = run(only({"→"}, unless="o1.col"), two)
    assert not o6 and r6["not_offered"] == {"a junction of several: not settled": 1}, ("MF-M6", r6)
    stats, ops = {"yielded": 0, "beyond_depth": 0}, {}
    chains = ag._library_chains("o1.col", "val", "val", stats, ops)
    mol = [c.name for c in chains]
    plain_ops = {}
    ag._lib_offers["o1.col"] = [dict(o_, prov={"entries": 1}) for o_ in ag._mol_offers["o1.col"]]
    saved, ag._mol_offers = ag._mol_offers, {}
    plain = [c.name for c in ag._library_chains("o1.col", "val", "val", dict(stats), plain_ops)]
    ag._mol_offers = saved
    assert mol == plain == ["inc . dec"] and ops["inc . dec"][0] == "o1.row" == \
        plain_ops["inc . dec"][0], ("MF-M4", mol, plain, ops, plain_ops)
    import os
    import subprocess
    env = {**os.environ, "TETHER_MOLECULE_APPLY": "0", "PYTHONDONTWRITEBYTECODE": "1"}
    out = subprocess.run([sys.executable, "-B", __file__, "--off"], env=env, capture_output=True,
                         text=True, timeout=300)
    assert out.returncode == 0, out.stderr[-2000:]
    print(f"  MF-M1 offers in order: {got}; pass {row['cost_ms']} ms")
    print(f"  MF-M2 ambiguous: {r2['not_offered']}")
    print(f"  MF-M3 => settled: {list(r3['not_offered'])}".encode("ascii", "replace").decode())
    print(f"  MF-M3b + settled: {r3b['not_offered']}")
    print(f"  MF-M4 library stream yields {mol} (plain offer {plain}), operand {ops['inc . dec']}")
    print(f"  MF-M5 two junctions, both settled: {got5}; inner + : {r5b['not_offered']}")
    print(f"  MF-M6 the inner one not settled: {r6['not_offered']}")
    print(f"  MF-OFF {out.stdout.strip().splitlines()[-1]}")
    print("test_molecule_apply OK")


if __name__ == "__main__":
    main()
