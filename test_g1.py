"""G1, RELATIONAL WANTS PER EVENT (TETHER_G1_WANT; the reviewer 2026-10-17 15:30, 23:04, 23:17).

  P             the fake ARC game (12 actions, C-seed-X): an event that moved a derived slot forms
                ONE want there, with its origin, and _objective_of reads it (goal_residual computes)
  DIR           a derived slot moves 0 -> 2; "== 0" is listed first and "> 0" second: the want is
                "> 0" (sign . all), the condition the change made TRUE. MF-DIR: ladder-first takes
                "== 0", true only BEFORE the change
  MF-FREE       a condition of quantifier atoms alone that became true is refused and counted
  MF-UNRELATED  an event whose derived slots did not change forms no want and asks nothing
  MF-ONE        two events changing the same derived slot form one want; the second finds it held
  B             a boundary (retarget) writes one row listing each held G1 want with its origin and
                outcome, and clears them
  MF-OFF        (run apart) the arm off gives the fake ledger byte-identical to f631977's

    python test_g1.py
"""
from __future__ import annotations

import sys
from collections import Counter

sys.dont_write_bytecode = True


def agent():
    import arc_holdout
    import tether
    from test_entry import FakeWrapper
    tether._AGENT_SEED = False
    env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake")
    return tether, env, ag


def rows_of(ag) -> list:
    out = []
    real = ag.led.record

    def spy(cycle, step, slot, event, **d):
        out.append((event, slot, d))
        return real(cycle, step, slot, event, **d)
    ag.led.record = spy
    return out


def planted(tether, env, ag, d: str, before: int, after: int, conds: list, events: dict):
    import compile_term
    atoms = {a.name: a for a in ag.gamma.atoms}
    views = {}
    for i, chain in enumerate(conds):
        c = compile_term.Compiled(slot=d, term=tether.Term(tuple(atoms[n] for n in chain)),
                                  operand=None)
        views[f"v{i}"] = (c, {"library": f"TEST|{'.'.join(chain)}", "role": "STATE"})
    owner = d.split(".")[0]
    env.derived = lambda: {d: (f"{owner}.row",)}
    own = {d: owner, f"{owner}.row": owner, f"{owner}.col": owner}
    env.slot_owner = lambda: own
    env.attribute_of = lambda: {d: "drow", f"{owner}.row": "row", f"{owner}.col": "col"}
    ag._events = events
    ag.trace = [({d: before, f"{owner}.row": 5}, "ACTION1", {d: after, f"{owner}.row": 5 + after},
                 None, None)]
    ag._index_reach = lambda *_a, **_k: (views, {}, Counter())
    return views


def main() -> int:
    tether, env, ag = agent()
    for _ in range(12):
        env.observe()
        ag.step()
        if env.terminal():
            break
    g1 = dict(ag._g1)
    assert g1, "P: no G1 want formed on the fake"
    d, rec = next(iter(sorted(g1.items())))
    name, term = ag._objective_of(d)
    assert ag.wants[d] == rec["want"] == name and rec["origin"] == "derived-change", (d, rec, name)
    gr = ag.goal_residual(d, ag.trace[-1][2])
    print(f"P {len(g1)} G1 wants on the fake, e.g. {d} -> {rec['want']} (event {rec['obj_event']},"
          f" dk {rec['dk']}, entry {rec['entry']}); _objective_of reads it; goal_residual {gr}")

    tether, env, ag = agent()
    rows = rows_of(ag)
    views = planted(tether, env, ag, "o1.drow", 0, 2, [("holds", "negate"), ("sign",)],
                    {"o1": ("o1.row", "o1.col")})
    ag._g1_wants()
    first = next(iter(views.values()))[0].term.name
    assert ag.wants.get("o1.drow") == "sign . all", ag.wants.get("o1.drow")              # DIR
    assert first == "holds . negate", first                                              # MF-DIR
    print(f"DIR 0 -> 2: the want is {ag.wants['o1.drow']!r} (made true); MF-DIR ladder-first is "
          f"{first!r}, true only before")

    tether, env, ag = agent()
    rows = rows_of(ag)
    planted(tether, env, ag, "o1.drow", 0, 2, [("none",)], {"o1": ("o1.row", "o1.col")})
    ag._g1_wants()
    g = [d_ for e, _s, d_ in rows if e == "g1"]
    assert "o1.drow" not in ag.wants and g and g[0]["refused_free"] == 1, (ag.wants, g)  # MF-FREE
    print("MF-FREE a bare quantifier ('none') that became true is refused and counted")

    tether, env, ag = agent()
    rows = rows_of(ag)
    planted(tether, env, ag, "o1.drow", 2, 2, [("sign",)], {"o1": ("o1.row", "o1.col")})
    ag._g1_wants()
    asked = [1 for e, _s, _d in rows if e == "g1"]
    assert "o1.drow" not in ag.wants and not asked, rows                                 # MF-UNREL
    print("MF-UNRELATED the derived slot did not change: no question, no want")

    tether, env, ag = agent()
    rows = rows_of(ag)
    planted(tether, env, ag, "o1.drow", 0, 2, [("sign",)],
            {"o1": ("o1.row", "o1.col"), "o9": ("o1.row", "o9.col")})
    ag._g1_wants()
    g = [d_ for e, _s, d_ in rows if e == "g1"]
    assert len(ag._g1) == 1 and [x.get("held_want") for x in g] == [None, "sign . all"], g  # MF-ONE
    print("MF-ONE two events changing o1.drow: one want, the second finds it held")

    ag.retarget(env, 1, how=tether.ADVANCE)
    end = [d_ for e, _s, d_ in rows if e == "g1_outcomes"]
    assert end and end[0]["wants"][0]["slot"] == "o1.drow" and not ag._g1, end            # B
    print(f"B the boundary lists {len(end[0]['wants'])} held G1 want(s) with origin and outcome "
          f"({end[0]['wants'][0]}) and clears them")
    print("g1: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
