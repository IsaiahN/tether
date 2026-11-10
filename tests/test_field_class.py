"""29 GRAMMATICAL CLASS WEIGHTS (TETHER_FIELD_CLASS, default ON; the reviewer 2026-11-05 r1280,
r1281). gridworld default seed 0, the agent seed pinned, 6 steps; the class standings PLANTED where
a check is about the ranking. Each check its own process.
  check_g1_class_from_grammar  each entry's class read off the grammar (its default role), no
                               class table of ours (AST); all three classes present
  check_g2_verb_paid_board     a board where verbs paid ranks a verb entry above a noun-only one
                               inside one tier; OFF the bare count puts the noun first
  check_g3_nofit_lowers        a no-fit lowers the matched class's weight
  check_g3b_window_is_one      a 32-entry no-fit window is ONE witness per class (r1284)
  check_g3c_paid_only          a window that pays and is judged no-fit for a class books the
                               paid only (r1284)
  check_g4_tier_first          a higher tier still comes first, whatever the fields match
  check_g5_paid_crosses        paid crosses at class level through the real lineage write and
                               read; against does not
  check_g6_no_board_names      every class key is (class, board index): no board name
    python tests/test_field_class.py [check ...]
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True


def _agent():
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    assert tether._FIELD_CLASS, "TETHER_FIELD_CLASS is OFF"
    tether._AGENT_SEED = False
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    for _ in range(6):
        ag.step()
    return ag


def _pair():
    """a noun entry with a reading r, and a verb entry that does not read r"""
    import tether
    cls, post = tether._gcw_classes(), tether._posting_reads()
    e_n = next(e for e in sorted(post) if cls.get(e) == "noun" and post[e])
    r = sorted(post[e_n])[0]
    e_v = next(e for e in sorted(post) if cls.get(e) == "verb" and r not in post[e])
    return e_n, e_v, r


def _plant(ag, cls, paid=0, against=0.0):
    ag._reflexes["gcw"]["standing"][(cls, getattr(ag, "_bond_board", 0))] = {
        "paid": paid, "against": against, "tick": ag.cycle}


def _rank(ag, lit, tiers, r):
    return ag._topk(lit, lit, tiers, {"x": r}, ("x",), ("s", "dk", (), (), ("x",)))[0]


def check_g1_class_from_grammar() -> None:
    import ast
    import collections
    import inspect

    import tether
    assert tether._FIELD_CLASS, "TETHER_FIELD_CLASS is OFF"
    tree = ast.parse(inspect.getsource(tether._gcw_classes))
    assert not [n for n in ast.walk(tree) if isinstance(n, ast.Dict)], "a class table"
    src = ast.unparse(tree)
    assert "grammar.json" in src and "by_default_role" in src and '"roles"' in src.replace("'", '"')
    n = collections.Counter(tether._gcw_classes().values())
    assert n["verb"] and n["noun"] and n["filler"], n
    print(f"  classes read off the grammar's roles: {dict(n)}")


def check_g2_verb_paid_board() -> None:
    ag = _agent()
    e_n, e_v, r = _pair()
    _plant(ag, "verb", paid=5)
    _plant(ag, "noun", against=5.0)
    got = [k for k, _w in _rank(ag, [(e_n, 1), (e_v, 1)], {"T3": 2}, r)]
    assert got[0] == e_v, got
    print(f"  verbs paid here: the verb entry ranks first ({got[0]}), ahead of the noun-only one")


def check_g3_nofit_lowers() -> None:
    ag = _agent()
    ag._reflexes["gcw"]["standing"].clear()          # the warm-up's witnesses aside (isolate)
    p0 = ag._gcw_p("noun")
    ag._gcw_win = {"e": {"noun"}}
    ag._gcw_credit(["e"], "against")
    p1 = ag._gcw_p("noun")
    assert p1 < p0, (p0, p1)
    print(f"  a no-fit on a noun match: p_noun {p0:.3f} -> {p1:.3f}")


def check_g3b_window_is_one() -> None:
    ag = _agent()
    ag._reflexes["gcw"]["standing"].clear()          # the warm-up's witnesses aside (isolate)
    ag._gcw_win = {f"e{i}": {"noun"} for i in range(32)}
    ag._gcw_credit(list(ag._gcw_win), "against")      # a 32-entry window judged no-fit
    st = ag._rf_standing("gcw", ("noun", getattr(ag, "_bond_board", 0)))
    p = ag._gcw_p("noun")
    assert st["against"] == 1 and abs(p - 0.5) < 1e-9, (st, p)
    print(f"  a 32-entry no-fit window: against {st['against']}, p_noun {p:.3f} (as one entry)")


def check_g3c_paid_only() -> None:
    ag = _agent()
    ag._reflexes["gcw"]["standing"].clear()
    ag._gcw_win = {"a": {"noun"}, "b": {"noun"}}
    ag._gcw_credit(["a", "b"], "against")             # judged no-fit, then a pay in the window
    ag._gcw_credit(["a"], "paid")
    ag._gcw_credit(["a", "b"], "against")             # and judged again: still paid only
    st = ag._rf_standing("gcw", ("noun", getattr(ag, "_bond_board", 0)))
    assert st["paid"] == 1 and st["against"] == 0, st
    print(f"  pay and no-fit in one window: paid {st['paid']}, against {st['against']}")


def check_g4_tier_first() -> None:
    ag = _agent()
    e_n, e_v, r = _pair()
    _plant(ag, "verb", against=9.0)                      # verbs failed here
    _plant(ag, "noun", paid=9)
    got = [k for k, _w in _rank(ag, [(e_v, 1), (e_n, 1)], {"T1a": 1, "T3": 1}, r)]
    assert got[0] == e_v, got
    print("  the higher-tier entry still first, though its class failed and the other's paid")


def check_g5_paid_crosses() -> None:
    import lineage
    a = _agent()
    _plant(a, "verb", paid=2, against=1.0)
    with tempfile.TemporaryDirectory() as d:
        lineage._write(d, a, "g", False, [])
        recs = [x for g in lineage._read(Path(d)).values() for x in g.get("inventions", ())
                if x.get("kind") == "reflex"]
    assert recs and "against" not in json.dumps(recs), recs
    b = _agent()
    b._reinvent_carried(json.loads(json.dumps(recs)))
    b._bond_board = 7                                    # another board: the class crosses
    st = b._rf_standing("gcw", ("verb", 7))
    assert b._rf_in("gcw", ("verb", 7)) == 2 and st["against"] == 0.0, (b._rf_carried, st)
    print(f"  paid 2 crossed to board 7 as the class seed; against stayed home "
          f"(p_verb {b._gcw_p('verb'):.3f})")


def check_g6_no_board_names() -> None:
    ag = _agent()
    ag._gcw_win = {"e": {"verb", "noun"}}
    ag._gcw_credit(["e"], "paid")
    import tether
    keys = list(ag._reflexes["gcw"]["standing"])
    # item 30 (TETHER_SPREAD): the spread's own weight shares the store, keyed the same way
    cls = ("verb", "noun", "filler") + (("spread",) if tether._SPREAD else ())
    assert keys and all(len(k) == 2 and k[0] in cls
                        and isinstance(k[1], int) for k in keys), keys
    print(f"  keys {sorted(keys)}: a class and a board index, no name")


def main() -> int:
    want = sys.argv[1:]
    names = [k for k in globals() if k.startswith("check_") and (not want or k in want)]
    if len(names) == 1:
        globals()[names[0]]()
        print("ok  ", names[0])
        return 0
    bad = [n for n in names if subprocess.run([sys.executable, "-B", __file__, n],
                                              cwd=str(_repo.ROOT),
                                              stdin=subprocess.DEVNULL).returncode]
    assert not bad, bad
    print(f"field_class: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
