"""TETHER_DESCRIBE_BY_SOURCE (the reviewer 2026-11-06 r1326-r1328): a derived reading enters a
lookup's description only if a source outside the described object changed across the lookup's
frames, or it is a relational surprise; the member's own slot always stays (Fig 13, as E0b reads
it for bets).

check_unit (seconds)  a stepped gridworld agent's _by_source on a planted derived map and frames
  (r1331: METRIC relations by source, CONTACT relations kept while they hold or change):
  MF       a.rel_b whose other party b never changed is DROPPED (a's own readings explain it)
  CONTROL  a.rel_c whose other party c changed STAYS
  CONTROL  a.rel_d, a relational surprise (_rel_subjects), STAYS though d never changed
  CONTROL  the member's own slot (itself derived) STAYS
check_lookup (seconds)  the MF through _lookup itself (r1329): one slot's description planted to
  vary with 12 pair readings of its object, only one other party (x0) changing across the frames:
  ON keeps that pair and the member's own slot, and the lookup row's by_source_dropped is 11;
  OFF keeps all 12 and writes no new field. RED at f33ac6e (all 12 kept, no field)
bp35 c4, the slow step the arm was built for, is the WITNESS run (minutes, the game's files), in
the commit body, not a gate test (r1329)

    python tests/test_describe_by_source.py [check ...]
"""
from __future__ import annotations

import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def check_unit() -> None:
    assert hasattr(tether.Agent, "_by_source"), "MF: no describe-by-source (f33ac6e)"
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="dbs"), tether.Config(), ledger.Ledger())
    ag.step()
    der = {"a.rel_b": ("a.col", "b.col"), "a.rel_c": ("a.col", "c.col"),
           "a.rel_d": ("a.col", "d.col"), "a.speed": ("a.row", "a.col"),
           "a.dcol_g": ("a.col", "g.col"), "a.touches_e": ("a.col", "e.col"),
           "a.touches_f": ("a.col", "f.col")}
    f0 = {"a.col": 1, "b.col": 5, "c.col": 7, "d.col": 9, "g.col": 4, "e.col": 2, "f.col": 8,
          "a.touches_f": 0}
    # a moves; c moves; every other party is static; a touches e in the middle frame only
    hm = [({**f0, "a.col": k, "c.col": 7 + k, "a.touches_e": int(k == 1)}, None, None, None, None)
          for k in range(3)]
    ag._rel_subjects = {"a.rel_d"}
    desc = {"a.speed": "DELTA", "a.col": "POSITION", "a.rel_b": "DELTA", "a.rel_c": "DELTA",
            "a.rel_d": "DELTA", "a.dcol_g": "DELTA", "a.touches_e": "BOOL", "a.touches_f": "BOOL"}
    n = ag._by_source("a.speed", desc, hm, der)
    gone = {"a.rel_b", "a.dcol_g", "a.touches_f"}
    assert n == 3 and not gone & set(desc), ("MF: rel_b, dcol_g, touches_f drop", n, sorted(desc))
    assert "a.rel_c" in desc, "CONTROL: the moved party's relation dropped"
    assert "a.rel_d" in desc, "CONTROL: the relational surprise dropped"
    assert "a.touches_e" in desc, "CONTROL: a contact with a static partner, holding once, dropped"
    assert "a.speed" in desc and "a.col" in desc, "CONTROL: the member or a non-derived dropped"
    print("  unit: metric a.rel_b and a.dcol_g (static partners) and contact a.touches_f (0 "
          "throughout) dropped; a.rel_c (party moved), a.rel_d (relational surprise), "
          "a.touches_e (static partner, in contact once), a.speed (the member) kept")


def check_lookup() -> None:
    """The MF through _lookup itself (r1329: a short forcing fixture): a stepped gridworld agent,
    one slot whose description is planted to vary with N pair readings of its object (env.derived
    lists each from both boxes), only ONE other party changing across the frames."""
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="dbs"), tether.Config(), ledger.Ledger())
    for _ in range(3):
        ag.step()
    slot = next(s for s in sorted(ag.slots) if s.endswith(".col") and not s.startswith("@"))
    obj = slot.split(".", 1)[0]
    others = [f"x{i}" for i in range(12)]
    pairs = {f"{obj}.dcol_{o}": (f"{obj}.col", f"{o}.col") for o in others}
    hist = [({slot: k, **{f"{o}.col": 3 for o in others}, "x0.col": 3 + k}, "A1", k, None, None)
            for k in range(4)]
    real_owner, real_der = env.slot_owner, getattr(env, "derived", None)
    env.slot_owner = lambda: {**real_owner(), **dict.fromkeys(pairs, obj)}
    env.derived = lambda: dict(pairs)
    for r in pairs:
        ag.slot_types[r] = "DELTA"
    real_char = tether.retrieval.characterise
    tether.retrieval.characterise = lambda *_a, **_k: {"arity": 2, "varies": tuple(pairs),
                                                     "invariant": (), "n": 4}
    ag._reach_timed = lambda *_a, **_k: None
    rows = {}
    keep = getattr(tether, "_DESCRIBE_BY_SOURCE", True)   # set, never read, at f33ac6e
    try:
        for on in (True, False):
            tether._DESCRIBE_BY_SOURCE = on
            ag._ev_done, ag._event_of = {}, {}
            n0 = len(ag.led.rows())
            ag._lookup(slot, hist)
            rows[on] = [r["detail"] for r in ag.led.rows()[n0:] if r["event"] == "lookup"][-1]
    finally:
        tether._DESCRIBE_BY_SOURCE = keep
        tether.retrieval.characterise = real_char
        env.slot_owner = real_owner
        if real_der is None:
            del env.derived
        else:
            env.derived = real_der
    on, off = rows[True], rows[False]
    kept = sorted(r for r in on["described"] if r in pairs)
    assert kept == [f"{obj}.dcol_x0"], ("MF: ON should keep only the moved party's pair", kept)
    assert slot in on["described"], ("CONTROL: the member's own slot dropped", on["described"])
    assert on.get("by_source_dropped") == len(pairs) - 1, ("MF: by_source_dropped", on)
    assert sorted(r for r in off["described"] if r in pairs) == sorted(pairs), "OFF: not all kept"
    assert "by_source_dropped" not in off, ("OFF wrote the new field", off)
    print(f"  lookup: ON kept {kept} + {slot}, by_source_dropped {on['by_source_dropped']}; "
          f"OFF kept all {len(pairs)}, no new field")


def main() -> int:
    want = set(sys.argv[1:])
    checks = [check_unit, check_lookup]
    for c in checks:
        if not want or c.__name__ in want:
            c()
            print("ok  ", c.__name__)
    print("test_describe_by_source OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
