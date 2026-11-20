"""The structure hash: one key per FORM, never per occasion.

  python tests/test_structure.py

  1. same atoms in a different order -> different hash
  2. same structure on different slots / instances -> IDENTICAL hash
  3. operand and guard structure change the hash
  4. deterministic across two fresh processes
  5. must-fail: a deliberately instance-leaking hash fails check (2) and prints
     'RED as required'
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
import gamma
import structure

sys.dont_write_bytecode = True


def _atom(name: str, it: str = "val", ot: str = "val", **kw) -> gamma.Atom:
    return gamma.Atom(name=name, fn=lambda v, _c: v, in_type=it, out_type=ot, **kw)


def _chain(names, operand=None, guard=None, guard_ref=None, origin=None, operand_term=None):
    kw = {} if origin is None else {"origin": origin}
    return gamma.Term(
        atoms=tuple(_atom(n) for n in names),
        operand=operand,
        guard=guard,
        guard_ref=guard_ref,
        operand_term=operand_term,
        **kw,
    )


def _same_structure_different_slots():
    """One form, two occasions: different slot names, object names, provenance."""
    a = _chain(["col", "row"], operand="o0.colour", guard="ACTED_ON", guard_ref="o0",
               origin=gamma.MINTED)
    b = _chain(["col", "row"], operand="o3.h", guard="ACTED_ON", guard_ref="o7",
               origin=gamma.IMPORTED)
    return a, b


def _term_a():
    """A fixed term with a nested operand tree, used by the fresh-process check."""
    inner = _chain(["parity"], operand="o0.colour")
    return _chain(["col", "row"], operand="o0.colour", operand_term=inner,
                  guard="ACTED_ON", guard_ref="o0")


def _assert_same_structure_same_hash(hasher, a, b):
    """Check (2), shared with the must-fail so it fails the SAME assertion."""
    assert hasher(a) == hasher(b), "identical structures must hash identically"


# ---------------------------------------------------------------------------
# 1. order
# ---------------------------------------------------------------------------
def test_order_changes_hash():
    a = _chain(["col", "row"])
    b = _chain(["row", "col"])
    assert structure.structure_hash(a) != structure.structure_hash(b)


# ---------------------------------------------------------------------------
# 2. instances do not move the hash
# ---------------------------------------------------------------------------
def test_same_structure_different_slots_identical():
    a, b = _same_structure_different_slots()
    _assert_same_structure_same_hash(structure.structure_hash, a, b)

    # the nested operand tree carries instances too, which must not move it either
    x = _chain(["col"], operand="o0.x", operand_term=_chain(["parity"], operand="o0.colour"))
    y = _chain(["col"], operand="o9.y", operand_term=_chain(["parity"], operand="o5.row"))
    assert structure.structure_hash(x) == structure.structure_hash(y)


# ---------------------------------------------------------------------------
# 3. operand and guard structure move the hash
# ---------------------------------------------------------------------------
def test_operand_and_guard_change_hash():
    base = structure.structure_hash(_chain(["col", "row"]))
    variants = [
        _chain(["col", "row"], operand="o0.colour"),                     # operand appears
        _chain(["col", "row"], operand_term=_chain(["parity"])),         # operand tree appears
        _chain(["col", "row"], guard="ACTED_SELF"),                      # guard appears
        _chain(["col", "row"], guard="ACTED_ON", guard_ref="o0"),        # referent appears
        _chain(["col", "row"], operand="o0", operand_term=_chain(["parity"])),
        _chain(["col", "row"], operand="o0", operand_term=_chain(["reflect"])),  # tree differs
    ]
    for t in variants:
        assert structure.structure_hash(t) != base

    # guard KIND is part of the structure
    assert (structure.structure_hash(_chain(["col"], guard="ACTED_SELF"))
            != structure.structure_hash(_chain(["col"], guard="INVENTED")))
    # same guard kind, referent present vs absent
    assert (structure.structure_hash(_chain(["col"], guard="ACTED_ON"))
            != structure.structure_hash(_chain(["col"], guard="ACTED_ON", guard_ref="o0")))


# ---------------------------------------------------------------------------
# 4. deterministic across processes
# ---------------------------------------------------------------------------
def test_deterministic_across_processes():
    root = pathlib.Path(__file__).resolve().parent.parent
    tests = pathlib.Path(__file__).resolve().parent
    code = (
        "import sys;"
        f"sys.path.insert(0, {str(root)!r});"
        f"sys.path.insert(0, {str(tests)!r});"
        "import test_structure as t;"
        "print(t.structure.structure_hash(t._term_a()))"
    )
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    out = []
    for _ in range(2):
        out.append(subprocess.check_output(
            [sys.executable, "-c", code], cwd=root, env=env, text=True
        ).strip())
    assert out[0] == out[1], "two fresh processes disagreed"
    assert out[0] == structure.structure_hash(_term_a()), "subprocess disagreed with in-process"


# ---------------------------------------------------------------------------
# 5. must-fail: an instance-leaking hash is caught by check (2)
# ---------------------------------------------------------------------------
def _instance_leaking_hash(term) -> str:
    """Deliberately WRONG: folds the slot / object names into the structure.

    This is the failure mode check (2) exists to catch — kept here so the guard
    is exercised rather than merely written down.
    """
    struct = structure._term_struct(term)
    struct["slot"] = str(getattr(term, "operand", None))       # LEAK: slot name
    struct["object"] = str(getattr(term, "guard_ref", None))   # LEAK: object name
    return hashlib.sha256(
        json.dumps(struct, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def test_must_fail_instance_leak():
    a, b = _same_structure_different_slots()
    try:
        _assert_same_structure_same_hash(_instance_leaking_hash, a, b)
    except AssertionError:
        print("RED as required")
    else:
        raise AssertionError("the instance-leaking hash was NOT caught by check (2)")


if __name__ == "__main__":
    import pathlib as _pathlib
    import re as _re

    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    src = _pathlib.Path(__file__).read_text(encoding="utf-8")
    declared = len(_re.findall(r"^def (test_\w+)", src, _re.M))
    if len(fns) != declared:
        missed = sorted(set(_re.findall(r"^def (test_\w+)", src, _re.M)) - set(globals()))
        raise AssertionError(
            f"{declared} tests defined in the source and {len(fns)} collected -- "
            f"{missed} are defined after the runner and would never run")
    for fn in fns:
        fn()
    print(f"{len(fns)} structure-hash checks pass ({declared} defined)")
