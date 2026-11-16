"""CATEGORY ORDER (TETHER_CATEGORY_ORDER, default ON; Isaiah 2026-11-16 "categorize the library ...
so that helps make search faster"; WATSON 42 layer C "Categories"). library/word_map.json gives each
library entry a category; the residual's reading wants one (tether.CATEGORY_OF_READING, a declared
Fig 10 table). Categories set SEARCH PRIORITY ONLY (Fig 9 :60): one more LAST field in the described
lookup's rank (Agent._topk), after RDL's -- same candidate set, different order; nothing added,
removed, made reachable or given standing.

  C1    a fixture word map (tether.WORD_MAP pointed at a temp file): for a motion residual (col) an
        action-category entry is ranked ahead of an equal property-category entry, and one
        category_order row is written (wanted, entry_category, source)
  C2    the same candidate set ON and OFF, a different order
  MF-C1 TETHER_CATEGORY_ORDER off -> order unchanged, no category rows -> RED as required
  C3    gridworld 12 steps ON (the real library/word_map.json) and OFF: both pass gate.check
  C4    no word map -> inert, exactly one category_inert row saying why, order as OFF

Seconds.

    python tests/test_category_order.py
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from collections import Counter

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gate  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

SLOT = "o1.col"


def agent(led=None):
    env = world.bind(gridworld.family("default", 0))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                        led if led is not None else ledger.Ledger())


def cat_rows(led, n0=0):
    return [r for r in led.rows()[n0:] if str(r.get("event", "")).startswith("category_")]


def rank(ag, reading="col"):
    """The described lookup's rank over two entries every other field leaves equal."""
    lit = [("eA", 1.0), ("eB", 1.0)]
    win, _nxt = ag._topk(lit, lit, {"T1a": 2}, {SLOT: reading}, (SLOT,),
                         (SLOT, None, (), (), (SLOT,)))
    ag._tk_off.clear()
    return [k for k, _w in win]


def main() -> int:
    assert tether._CATEGORY_ORDER is True, "the arm defaults ON"
    assert tether._category_wanted({"col"}) == "action"
    assert tether._category_wanted({"dcol_o2"}) == "action"
    assert tether._category_wanted({"shape"}) == "shape"
    assert tether._category_wanted({"touches_o1"}) == "relation"
    assert tether._category_wanted({"colour"}) is None
    assert tether._category_wanted({"col", "shape"}) is None
    td = tempfile.mkdtemp(prefix="cat_")
    keep = tether.WORD_MAP
    fx = os.path.join(td, "word_map.json")
    with open(fx, "w", encoding="utf-8") as fh:
        json.dump({"entries": {"eA": {"category": "property"}, "eB": {"category": "action"}}}, fh)
    tether.WORD_MAP = fx

    led = ledger.Ledger()
    ag = agent(led)
    on = rank(ag)
    rows1 = cat_rows(led)
    again = rank(ag)
    rows2 = cat_rows(led)
    d = rows1[0]["detail"] if rows1 else {}
    ok1 = (on == ["eB", "eA"] and again == on and len(rows1) == 1 and len(rows2) == 1
           and rows1[0]["event"] == "category_order" and d.get("wanted") == "action"
           and d.get("entry") == "eB" and d.get("entry_category") == "action"
           and d.get("source") == "library/word_map.json")
    print(f"C1 action eB ranked ahead of equal property eA for a motion residual: {on}; "
          f"category_order rows {len(rows1)} then {len(rows2)} {d.get('wanted')}/"
          f"{d.get('entry_category')}: {'GREEN' if ok1 else 'RED'}")

    cat = ag._cat
    ag._cat = None
    off = rank(ag)
    ag._cat = cat
    nopref = rank(ag, "colour")
    ok2 = set(on) == set(off) and on != off and len(on) == len(off) and nopref == off
    print(f"C2 the same set ON {on} / OFF {off}, a different order (no preference: {nopref}): "
          f"{'GREEN' if ok2 else 'RED'}")

    tether._CATEGORY_ORDER = False
    led_off = ledger.Ledger()
    ag_off = agent(led_off)
    off2 = rank(ag_off)
    tether._CATEGORY_ORDER = True
    red = ag_off._cat is None and off2 == ["eA", "eB"] and not cat_rows(led_off)
    verdict = "RED as required" if red else "GREEN (the arm did not switch off)"
    print(f"MF-C1 TETHER_CATEGORY_ORDER off: order {off2}, category rows "
          f"{len(cat_rows(led_off))} -> {verdict}")

    tether.WORD_MAP = keep
    ok3 = True
    for arm in (True, False):
        tether._CATEGORY_ORDER = arm
        led3 = ledger.Ledger()
        ag3 = agent(led3)
        for _ in range(12):
            ag3.step()
        ag3.end_run("cap")
        v = gate.check(led3.rows())["verdict"]
        evs = dict(Counter(r["event"] for r in cat_rows(led3)))
        print(f"  C3 gw12 CATEGORY_ORDER {'ON' if arm else 'OFF'} "
              f"({os.path.basename(tether.WORD_MAP)}): gate {v}, category rows {evs}, "
              f"rows {len(led3.rows())}")
        ok3 = ok3 and v == "pass" and (arm or not evs)
    tether._CATEGORY_ORDER = True
    print(f"C3 gridworld 12 steps ON and OFF both pass the gate: {'GREEN' if ok3 else 'RED'}")

    tether.WORD_MAP = os.path.join(td, "absent.json")
    led4 = ledger.Ledger()
    ag4 = agent(led4)
    got4 = rank(ag4)
    inert = cat_rows(led4)
    ok4 = (got4 == ["eA", "eB"] and len(inert) == 1 and inert[0]["event"] == "category_inert"
           and "no word map" in inert[0]["detail"]["why"])
    rank(ag4)
    ok4 = ok4 and len(cat_rows(led4)) == 1
    print(f"C4 no word map: inert, {len(inert)} category_inert row, order {got4}: "
          f"{'GREEN' if ok4 else 'RED'}")
    tether.WORD_MAP = keep

    assert ok1 and ok2 and red and ok3 and ok4
    print("category_order: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
