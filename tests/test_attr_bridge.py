"""BUILD 3 ITEM 9, THE A4.6 ATTRIBUTE BRIDGE (TETHER_ATTR_BRIDGE; the reviewer 2026-11-04 r1151;
r793). A PERCEPT atom gains the readings its ATTRIBUTE_INDEX clusters name (by_cluster,
hash-checked; K1's reading -> cluster table inverted) at the tags' weak weight 0.5, never over a
reading it holds. Seconds: the real library, loaded with the arm (tether._library) and as built
(library_runtime, no bridge).

MF-B1  some atom gains a reading it lacked as built, at weight 0.5, and is indexed under it; no
       reading the atom held as built changes weight
MF-B2  only PERCEPT entries change; the count of readings gained matches the bridge's tally (> 0)
MF-B3  compile_term.signature carries the arm: ON != OFF, so a compile made without the bridge is
       never served with it
The red is behavioural, the arm OFF on this tree: TETHER_ATTR_BRIDGE=0 fails MF-B1.

    python tests/test_attr_bridge.py
"""
from __future__ import annotations

import os
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import compile_term  # noqa: E402
import tether  # noqa: E402


def main():
    on = tether._library()
    import library_runtime  # noqa: E402  on sys.path once _library ran
    raw = library_runtime.Library(os.path.join(tether.LIBRARY_HOME, "library")).load()
    tally = getattr(on, "attr_bridge", {})
    gained, changed_kind, weight_moved = 0, set(), []
    for k in raw.seed:
        a, b = raw.get(k) or {}, on.get(k) or {}
        new = set(b.get("reads") or []) - set(a.get("reads") or [])
        if not new:
            continue
        changed_kind.add(b.get("kind"))
        gained += len(new)
        wa, wb = a.get("reads_weight") or {}, b.get("reads_weight") or {}
        weight_moved += [(k, r) for r in wa if wa[r] != wb.get(r)]
        assert all(wb.get(r) == 0.5 for r in new), ("MF-B1: a bridged reading not at 0.5", k, new)
        assert all(k in {x for x, _w in on.by_reading[r]} for r in new), ("MF-B1: not indexed", k)
    assert gained > 0 and not weight_moved, ("MF-B1: no reading gained, or a held one moved",
                                             gained, weight_moved[:3], tally)
    assert changed_kind == {"PERCEPT"} and gained == tally.get("readings added"), (
        "MF-B2", changed_kind, gained, tally)
    print(f"  MF-B1 {tally.get('atoms gaining')} atoms gain {gained} readings at 0.5; "
          f"no held weight moved")
    print(f"  MF-B2 only PERCEPT entries changed; tally {tally}")
    was = compile_term._ATTR_BRIDGE
    try:
        compile_term._ATTR_BRIDGE = True
        s_on = compile_term.signature({})
        compile_term._ATTR_BRIDGE = False
        s_off = compile_term.signature({})
    finally:
        compile_term._ATTR_BRIDGE = was
    assert s_on != s_off and ("ATTR_BRIDGE",) in s_on, ("MF-B3", s_on, s_off)
    print("  MF-B3 the signature carries the arm (ON != OFF)")
    print("test_attr_bridge OK")


if __name__ == "__main__":
    main()
