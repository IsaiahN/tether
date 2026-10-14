"""7e the view hold, R7e-3 the ROUND TRIP (the reviewer 2026-10-14 00:49, 00:57, 01:16, 01:30).
Game-free library checks, on a REAL agent built through __init__ over a gridworld (as test_vanish
does), because a hand-made object (Agent.__new__) hid a method shadowed by an instance attribute
(R7e-0, 01:29). It gates any run of TETHER_VIEW_HOLD.

  s1-s3 the agent as built: "_lib_view" is not an instance attribute and resolves to Agent's method;
     "_view_hold" and "_view_hold_n" are instance attributes of the declared types.
  s4 MUST-FAIL: the existing attribute self._view (tether 1756, 2032) is the tuple, not callable, on
     the same agent, so this fixture sees what __init__ set.
  h2 OFF: with the arm off, _lib_view is lib.view and holds nothing, counts nothing.
  h1 MUST-PASS: for every library entry, STATE, TEST, PROCESS and CAUSE, and every pair of the name
     panel, the held view put back under the names equals the NAMED view, field for field.
  h3 MUST-PASS (flipped by package v9, 2026-10-14): RELATION at (o20, o2) put back from the
     placeholder form equals the named view on every entry, because library 504 now names the
     partner as a WHOLE id (_names). Before v9 it was a substring test and 2,724 entries differed.
     RELATION and MEASURE stay out of _HELD_ROLES: holding them is its own change.
  h5 MUST-FAIL: a name with a brace (a synthetic id, here only) takes the bypass.
  h4 bypass half: at o == x _lib_view takes the bypass (counted once per entry and role).
  -- GATE line (s1-s4, h1, h2, h3, h5, h4's bypass half) --
  h4 occurrence half, NON-BLOCKING (the reviewer 01:07): some held entry's placeholder form differs
     from the named view at o == x.

    python test_view_hold.py
"""
from __future__ import annotations

import sys
from collections import Counter

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

PANEL = [("o1", "o2"), ("o1", "o12~o3"), ("o12~o3", "o1"), ("@goal", "o1"), ("o3", "o3"),
         ("o20", "o2"), ("o3", "o35"), ("o12~o3", "o3")]


def main() -> None:
    lib = tether._library()
    assert lib is not None, "no library"
    keys = list(dict.fromkeys([*lib.seed, *lib.runtime, *lib.learnings]))
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="view_hold"), tether.Config(),
                      ledger.Ledger())
    # s1-s3
    assert "_lib_view" not in ag.__dict__, "an instance attribute shadows _lib_view"
    assert ag._lib_view.__func__ is tether.Agent._lib_view
    assert isinstance(ag.__dict__.get("_view_hold"), dict) and not ag._view_hold
    assert isinstance(ag.__dict__.get("_view_hold_n"), Counter) and not ag._view_hold_n
    # s4
    assert isinstance(ag._view, tuple) and not callable(ag._view), ag._view
    # h2
    tether._VIEW_HOLD = False
    k0 = next(k for k in keys if lib.view(k, "STATE", "o1", "o2"))
    named0 = lib.view(k0, "STATE", "o1", "o2")
    assert ag._lib_view(lib, k0, "STATE", "o1", "o2") == named0
    assert not ag._view_hold and not ag._view_hold_n, (ag._view_hold_n,)
    # h1
    tether._VIEW_HOLD = True
    checked, nonempty = 0, set()
    for k in keys:
        for role in tether._HELD_ROLES:
            for o, x in PANEL:
                named = lib.view(k, role, o, x)
                got = ag._lib_view(lib, k, role, o, x)
                assert got == named, (k, role, o, x)
                checked += 1
                if named:
                    nonempty.add((k, role))
    assert nonempty, "no non-empty view: the round trip examined nothing"
    # h3
    rel = [k for k in keys
           if tether._restore(lib.view(k, "RELATION", "{o}", "{x}"), "o20", "o2")
           != lib.view(k, "RELATION", "o20", "o2")]
    assert not rel, f"RELATION at (o20, o2) differs on {len(rel)} entries: v9's filter is not in"
    # h5
    n0 = ag._view_hold_n["bypass_brace"]
    braced = lib.view(k0, "STATE", "o{1}", "o2")
    assert ag._lib_view(lib, k0, "STATE", "o{1}", "o2") == braced
    assert ag._view_hold_n["bypass_brace"] == n0 + 1
    # h4, the bypass half: _lib_view takes the bypass at o == x (once per entry and role in h1)
    assert ag._view_hold_n["bypass_same"] == len(keys) * len(tether._HELD_ROLES)
    print(f"test_view_hold: GATE pass (real agent; s1-s4 held; {checked} calls over {len(keys)} "
          f"entries x {len(tether._HELD_ROLES)} roles x {len(PANEL)} pairs; "
          f"{len(nonempty)} non-empty "
          f"(entry, role); held {ag._view_hold_n['held']}, served {ag._view_hold_n['served']}, "
          f"bypass {({k: v for k, v in ag._view_hold_n.items() if k.startswith('bypass')})}; "
          f"h3 RELATION at (o20, o2) restores exactly on all {len(keys)} entries)", flush=True)
    # h4, the occurrence half (non-blocking)
    same = [(k, r) for k in keys for r in tether._HELD_ROLES
            if tether._restore(lib.view(k, r, "{o}", "{x}"), "o3", "o3")
            != lib.view(k, r, "o3", "o3")]
    assert same, "o == x restores exactly for every entry: the bypass guards nothing"
    print(f"test_view_hold: h4 pass (o == x differs on {len(same)} (entry, role), first {same[0]})")


if __name__ == "__main__":
    main()
