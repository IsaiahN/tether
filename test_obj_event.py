"""E1-E3, OBJECT EVENTS (TETHER_OBJ_EVENT, TETHER_EVENT_SHARED; the reviewer 2026-10-17 12:53,
21:48, 21:53).

  E1    recognition: an owner with two or more live residual slots is an event; a pair owner a~b
        goes under both parties (answered once, by the first); a single-slot owner and a gone or
        silent slot are left alone
  E2    on the fake (12 actions, C-seed-X): each event's members ask ONE lookup (the rest read
        it, "shared"); at the first event's cycle each member's views are a SUPERSET of its own
        per-slot lookup's (the arm off). MF-E2 (run apart): the arm off gives the fake ledger
        byte-identical to 089789e's
  E3    the price: the joint code over the NON-derived members, the cell-change group as its
        largest member, with the rule on the row. MF-E3: a planted sum over every member differs by
        exactly the derived members' bits
  S     a scripted two-member event whose one chain explains both: each member alone would park
        (the chain costs more than either base), the event admits it stated once, and each member
        is bound to its own binding. MF-S: TETHER_EVENT_SHARED off -- nothing admitted
  MF-B  the same event with each binding naming another slot: the honest price (bindings charged)
        parks; a planted price omitting the bindings admits -- so the bindings are charged
  D     (the reviewer 22:10) a scripted diagonal move: row follows translate<o0.drow> (its own
        delta, binding 0) and col translate with an operand tree; one chain, each member alone
        parks, stated once (the tree charged as col's binding) it is admitted. MF-D: the 21:53 key,
        with the operand tree in it, groups nothing (groups_old_key 0)

    python test_obj_event.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from types import SimpleNamespace as NS

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))

CHILD = r'''
import json, os, sys, tempfile
sys.dont_write_bytecode = True
import tether, tether_agent
from test_entry import FakeWrapper
tether._AGENT_SEED = False
led = os.path.join(tempfile.mkdtemp(), "e.jsonl")
tether_agent.run(FakeWrapper(script={}), "fake", max_actions=12, led_path=led)
print("LEDGER", led)
'''


def fake(arms: dict) -> list:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", **arms})
    p = subprocess.run([sys.executable, "-B", "-c", CHILD], capture_output=True, text=True,
                       env=env, cwd=HERE, stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    path = next(x for x in p.stdout.splitlines() if x.startswith("LEDGER "))[7:]
    return [json.loads(x) for x in open(path, encoding="utf-8") if x.strip()]


def agent():
    sys.path.insert(0, HERE)
    import arc_holdout
    import tether
    from test_entry import FakeWrapper
    tether._AGENT_SEED = False
    env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake")
    return tether, env, ag


def e1(env, ag) -> None:
    own = {"o1.row": "o1", "o1.col": "o1", "o2.row": "o2", "o1~o2.contact": "o1~o2",
           "o3.row": "o3", "o4.row": "o4", "o4.col": "o4"}
    env.slot_owner = lambda: own
    live = NS(gone=False, mass=1.0)
    res = {"o1.row": live, "o1.col": live, "o2.row": live, "o1~o2.contact": live,
           "o3.row": live, "o4.row": live, "o4.col": NS(gone=True, mass=1.0)}
    ag._events_now(res)
    assert ag._events == {"o1": ("o1.row", "o1.col", "o1~o2.contact"),
                          "o2": ("o2.row", "o1~o2.contact")}, ag._events               # E1
    assert ag._event_of["o1~o2.contact"] == "o1" and "o3.row" not in ag._event_of
    print("E1 o1 {row, col, o1~o2.contact} and o2 {row, o1~o2.contact} are events; the pair slot "
          "is answered by o1; o3 (one slot) and o4 (its second slot gone) are not")


def e3(tether, env, ag) -> None:
    rows = []
    real = ag.led.record

    def spy(cycle, step, slot, event, **d):
        rows.append((event, d))
        return real(cycle, step, slot, event, **d)
    ag.led.record = spy
    ag._events = {"o9": ("o9.row", "o9.add_n", "o9.add_row", "o9.h")}
    ag._ev_base = {"o9.row": 6.0, "o9.add_n": 5.0, "o9.add_row": 4.0, "o9.h": 7.0}
    env.derived = lambda: {"o9.h": ("o9.shape",)}
    env.attribute_of = lambda: {"o9.row": "row", "o9.add_n": "add_n", "o9.add_row": "add_row",
                                "o9.h": "h"}
    was = tether._EVENT_SHARED
    tether._EVENT_SHARED = False
    try:
        ag._event_prices()
    finally:
        tether._EVENT_SHARED = was
        ag.led.record = real
    d = next(d for e, d in rows if e == "event_price")
    assert d["price"] == 6.0 + 5.0 and d["rule"] == "A+B(cells)" and d["derived_out"] == ["o9.h"], d
    assert sum(ag._ev_base.values()) - d["price"] == 7.0 + 4.0, d                        # MF-E3
    print(f"E3 price {d['price']} = row 6 + the cell group's largest 5 ({d['rule']}), h derived "
          f"out; MF-E3 the sum over all members (22) differs by h's 7 and the cell group's "
          "second member's 4")


def shared(tether, env, ag, operand: str | None, planted_free: bool = False,
           arm: bool = True, terms: tuple | None = None, factor: float = 0.75) -> list:
    rows = []
    real = ag.led.record

    def spy(cycle, step, slot, event, **d):
        rows.append((event, slot, d))
        return real(cycle, step, slot, event, **d)
    m1, m2 = "o0.row", "o0.col"
    chain = tuple(ag.gamma.atoms[1:3])      # two atoms: a composition, not a held atom
    t1, t2 = terms or (tether.Term(chain, operand=operand), tether.Term(chain, operand=operand))
    cost = ag._bits((tether.Term(t1.atoms), ag._units_for(m1)))
    base = cost * factor             # each member alone: the chain costs more than its base
    ag._events = {"o0": (m1, m2)}
    ag._event_of = {m1: "o0", m2: "o0"}
    ag._ev_base = {m1: base, m2: base}
    ag._lib_offers = {m1: [{"term": t1}], m2: [{"term": t2}]}
    env.derived = lambda: {}
    env.attribute_of = lambda: {m1: "row", m2: "col"}
    left, bind = ag._left, ag._bind_bits
    ag._left = lambda *_a, **_k: 0.0
    if planted_free:
        ag._bind_bits = lambda *_a: 0.0
    was = tether._EVENT_SHARED
    tether._EVENT_SHARED = arm
    ag.led.record = spy
    try:
        ag._event_prices()
    finally:
        ag.led.record, ag._left, ag._bind_bits = real, left, bind
        tether._EVENT_SHARED = was
    assert cost > base, (cost, base)
    return rows


def main() -> int:
    tether, env, ag = agent()
    e1(env, ag)
    e3(tether, env, ag)
    tether, env, ag = agent()
    r = shared(tether, env, ag, None)
    em = [d for e, _s, d in r if e == "event_mint"]
    assert em and em[0]["covered"] == ["o0.col", "o0.row"] and all(
        ag.bound[m] for m in ("o0.row", "o0.col")), r                                     # S
    print(f"S each member's base {em[0]['price_bits'] / 2:.3f} < the chain's {em[0]['cost_bits']} "
          f"(alone it parks); stated once {em[0]['total_bits']} < joint {em[0]['price_bits']}: "
          "admitted, each member bound")
    tether, env, ag = agent()
    r = shared(tether, env, ag, None, arm=False)
    assert not [1 for e, _s, _d in r if e in ("event_mint", "event_bound")], r            # MF-S
    print("MF-S TETHER_EVENT_SHARED off: nothing admitted")
    tether, env, ag = agent()
    other = "o1.row"
    r = shared(tether, env, ag, other)
    assert not [1 for e, _s, _d in r if e == "event_mint"], r
    tether, env, ag = agent()
    r = shared(tether, env, ag, other, planted_free=True)
    assert [1 for e, _s, _d in r if e == "event_mint"], r                                # MF-B
    print(f"MF-B bound to {other}: the honest price (each binding log2({len(ag.slots)} + 1) bits) "
          "parks; a planted price omitting the bindings admits")
    tether, env, ag = agent()
    tr = next(a for a in ag.gamma.atoms if a.name == "translate")
    neg = next(a for a in ag.gamma.atoms if a.name == "negate")
    d_row = tether.Term((tr,), operand="o0.drow")
    d_col = tether.Term((tr,), operand="o0.dcol", operand_term=tether.Term((neg,)))
    r = shared(tether, env, ag, None, terms=(d_row, d_col), factor=0.9)
    em = [d for e, _s, d in r if e == "event_mint"]
    es = [d for e, _s, d in r if e == "event_shared"]
    assert em and em[0]["binding_bits"]["o0.row"] == 0.0 and em[0]["binding_bits"]["o0.col"] > 0, r
    assert es and es[0]["groups"] == 1 and es[0]["groups_old_key"] == 0, es              # MF-D
    print(f"D row -> translate<o0.drow> (binding 0), col -> translate<negate(o0.dcol)> (binding "
          f"{em[0]['binding_bits']['o0.col']}, the tree); chain {em[0]['cost_bits']} stated once, "
          f"total {em[0]['total_bits']} < joint {em[0]['price_bits']}: admitted; MF-D the 21:53 "
          f"key groups {es[0]['groups_old_key']}, the new key {es[0]['groups']}")
    on = fake({})
    ev = [r for r in on if r["event"] == "event"]
    lk = [r for r in on if r["event"] == "lookup"]
    asked: dict = {}
    for r in lk:
        e_ = r["detail"].get("obj_event")
        if e_ is not None and not r["detail"].get("shared"):
            asked[(r["cycle"], e_)] = asked.get((r["cycle"], e_), 0) + 1
    assert ev and all(n == 1 for n in asked.values()), asked                              # E2
    c0 = min(r["cycle"] for r in ev)
    off = fake({"TETHER_OBJ_EVENT": "0"})
    mem = {m for r in ev if r["cycle"] == c0 for m in r["detail"]["members"]}

    def views(rows):
        return {r["slot"]: r["detail"]["views"] for r in rows
                if r["event"] == "library" and r["cycle"] == c0 and r["slot"] in mem}
    v_on, v_off = views(on), views(off)
    assert v_off and all(v_on.get(s, 0) >= n for s, n in v_off.items()), (v_on, v_off)
    print(f"E2 {len(ev)} events; each asked one lookup ({sum(asked.values())} asked, "
          f"{sum(1 for r in lk if r['detail'].get('shared'))} shared); at cycle {c0} every "
          f"member's views ON >= OFF ({v_on} against {v_off})")
    sh = [r["detail"] for r in on if r["event"] == "event_shared"]
    print(f"READ fake: {len(ev)} events, {len(sh)} cleared the floor and were searched; events "
          f"with >= 2 offered members {sum(1 for d in sh if d['offered_members'] >= 2)}; candidate "
          f"groups new key {sum(d['groups'] for d in sh)}, 21:53 key "
          f"{sum(d['groups_old_key'] for d in sh)}; admitted {sum(d['admitted'] for d in sh)}")
    print("obj_event: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
