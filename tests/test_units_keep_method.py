"""F325 / WATSON 54 -- promotion must carry the SETTLED METHOD, not just its ingredients.

Fig 12 :103-106 "a settled molecule becomes an atom for whatever composes over it", and
:5-14 "the ingredients are recorded and the arrangement is not ... the parts are not the
thing". Fig 4: carry the METHOD, never the per-board BINDING.

These are must-fail refuters: each would go red if gamma.units() again rebuilt a promoted
term from `.atoms` alone. The OFF arm reproduces the old behavior byte-for-byte.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.dont_write_bytecode = True

import gamma  # noqa: E402


def _atoms():
    return [gamma.Atom(n, lambda v, _c: v, "val", "val") for n in ("f", "g", "h")]


def _settled_gamma(tree=False):
    f, g, h = _atoms()
    gm = gamma.Gamma([f, g, h])
    t = (gamma.Term((f,), operand_term=gamma.Term((g,)))      # f<g(:ANY)>
         if tree else gamma.Term((f, g)))                     # f . g
    gm._install(t, 1, None)
    gm.settle(t.name)
    return gm, t


def test_01_promoted_tree_keeps_method():
    """The emitted unit keeps operand_term and its schema name, not just the atom list."""
    if not gamma._UNITS_KEEP_METHOD:
        return
    gm, t = _settled_gamma(tree=True)
    promoted = [u for u in gm.units() if u.name == t.name]
    assert len(promoted) == 1, f"schema-named unit missing; got {[u.name for u in gm.units()]}"
    assert promoted[0].operand_term is not None, "the settled method was dropped on promotion"
    assert promoted[0].operand_term.name == "g", "the inner branch was lost"


def test_02_two_branches_stay_distinct():
    """Two settled trees with the same outer atom but different branches yield TWO units.

    This is the mutation control: reverting gamma.py:2478 to Term(t.atoms, origin=...) collapses
    both to bare `f`, so this assertion goes red. That is the F325 promotion collapse.
    """
    if not gamma._UNITS_KEEP_METHOD:
        return
    f, g, h = _atoms()
    gm = gamma.Gamma([f, g, h])
    for inner in (g, h):
        t = gamma.Term((f,), operand_term=gamma.Term((inner,)))
        gm._install(t, 1, None)
        gm.settle(t.name)
    names = [u.name for u in gm.units() if "<" in u.name]
    assert len(names) == 2, f"two settled methods collapsed into one: {names}"


def test_03_flat_chain_unchanged():
    """A flat (non-tree) settled chain still promotes to its atom sequence -- no behavior drift."""
    gm, t = _settled_gamma(tree=False)
    promoted = [u for u in gm.units() if u.name == t.name]
    assert len(promoted) == 1 and promoted[0].operand_term is None


def test_04_binding_not_carried():
    """A per-board operand BINDING must not cross -- only the schema (Fig 4)."""
    if not gamma._UNITS_KEEP_METHOD:
        return
    f, g, h = _atoms()
    gm = gamma.Gamma([f, g, h])
    t = gamma.Term((f,), operand_term=gamma.Term((g,)), operand="o0.col")
    gm._install(t, 1, None)
    gm.settle(t.name)
    promoted = [u for u in gm.units() if "<" in u.name]
    assert promoted and promoted[0].operand is None, "a per-board binding leaked into the unit"


if __name__ == "__main__":
    print(f"arm TETHER_UNITS_KEEP_METHOD = {gamma._UNITS_KEEP_METHOD}")
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"{name}: OK")
    print("units_keep_method: all OK")
