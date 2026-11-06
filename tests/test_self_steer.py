"""27 SELF-READ STEERS (TETHER_SELF_STEER, default ON; the reviewer 2026-11-05 r1272, r1273).
gridworld default seed 0, the agent seed pinned, 6 steps; the stops planted where the check is not
about writing them. Each check its own process.
  check_s1_written_at_stop  a stalled hypothesis writes self_stop with the narrator OFF and no
                            ledger path: the agent counts it, not the narrator
  check_s2_hyp_price        two close stops at one goal shape read the steer and price THAT shape
                            up on that slot kind only
  check_s3_walk_weight      two 7f stops at a slot kind lower the walk's gain for that kind only
  check_s3b_price_out_stop  a price-out ("priced_out_at_depth") is a mint stop at "vocabulary"
                            (r1274): the site writes it, and two read the steer for that kind
  check_s3c_warmup_price_outs  the six warm-up steps alone write self_stop rows from real
                            price-outs and the steer reads p < 1 for that kind (r1276)
  check_s4_routine_order    the routine reader is a WEIGHT on the paths ordering's failure count
                            (r1274): a stopped form strongly better there still goes first; equal
                            otherwise, the unstopped one does
  check_s5_pay_restores     a pay after the stops restores the reading (1 + paid >= against)
  check_s6_one_reader       each key's line kind has one reader, no new exit, no board name in a
                            key (AST)
    python tests/test_self_steer.py [check ...]
"""
from __future__ import annotations

import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True


def _agent():
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    assert tether._SELF_STEER, "TETHER_SELF_STEER is OFF"
    tether._AGENT_SEED = False
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    for _ in range(6):
        ag.step()
    return ag


def _rows(ag, event):
    return [r["detail"] for r in ag.led.rows() if r["event"] == event]


def _slot(ag):
    return max((s for s in ag.slots if not s.startswith("@")), key=ag.outstanding)


def check_s1_written_at_stop() -> None:
    import narrate
    import tether
    narrate._NARRATE = False
    ag = _agent()
    assert getattr(ag.led, "_path", None) is None, "precondition: no ledger path"
    slot = _slot(ag)
    ag._hyp = {"key": ("planted",), "tkey": ("o3.row rises", slot, None), "slots": [slot],
               "steps": 4, "touches": 1, "losses": 0, "held_unreadable": 0, "reads": {},
               "acted": tether.Counter(), "text": "planted", "source": "library",
               "displaced": {}, "seg": {}}
    ag._goal_links[("planted",)] = ()
    ag._hyp_end("stalled", by="trend")
    r = _rows(ag, "self_stop")[-1]
    assert r["link"] == "plan" and r["line"] == "hyp" and "o3" not in r["kind"], r
    print(f"  narrator OFF, no ledger path: self_stop {r['link']}/{r['line']}, kind {r['kind']}")


def check_s2_hyp_price() -> None:
    ag = _agent()
    slot = _slot(ag)
    shape = ag._ss_form("o3.row rises")
    for _ in range(2):
        ag._ss_stop("plan", "hyp", (shape, ag._kind_key(slot)))
    here = ag._ss_hyp_price("o5.row rises", slot)       # the same shape, ids aside
    other = ag._ss_hyp_price("o3.col falls", slot)
    assert here > 0 and other == 0.0, (here, other)
    print(f"  the stopped shape priced up {here:.3f} bits; another shape 0")


def check_s3_walk_weight() -> None:
    ag = _agent()
    slot = _slot(ag)
    kind = ag._kind_key(slot)
    ag._outstanding[slot] = 10.0
    ag._tc_rho = lambda: 0.0
    ag._reflexes["walk"]["standing"].clear()       # the warm-up's walk witnesses aside
    ag._reflexes["steer"]["standing"].clear()      # the planted part starts fresh (r1276)
    ag._ss_stop("vocabulary", "mint", ("another kind",))
    ag._ss_stop("vocabulary", "mint", ("another kind",))
    ag._tc_walk(slot, closer=False)
    g0 = _rows(ag, "think_choice")[-1]["gain"]
    ag._ss_stop("vocabulary", "mint", kind)
    ag._ss_stop("vocabulary", "mint", kind)
    ag._tc_walk(slot, closer=False)
    g1 = _rows(ag, "think_choice")[-1]["gain"]
    assert g0 == 10.0 * ag._tc_need(slot) and 0 < g1 < g0, (g0, g1)
    print(f"  another kind's stops: gain {g0}; this kind's: {g1}")


def check_s3c_warmup_price_outs() -> None:
    ag = _agent()
    slot = _slot(ag)
    kind = ag._kind_key(slot)
    stops = [r for r in _rows(ag, "self_stop") if r["line"] == "mint"
             and r["link"] == "vocabulary" and r["kind"] == str(kind)]
    parks = [r for r in _rows(ag, "park") if r.get("verdict") == "priced_out_at_depth"]
    p = ag._ss_reads("vocabulary", "mint", kind)
    assert parks and stops and p is not None and p < 1, (len(parks), len(stops), p)
    print(f"  the warm-up alone: {len(parks)} price-outs, {len(stops)} self_stop rows, the steer "
          f"reads p {p:.2f} for that kind")


def check_s4_routine_order() -> None:
    import routine as Rt
    ag = _agent()
    a, b = Rt.Act("first"), Rt.Act("second")
    for _ in range(2):
        ag._ss_stop("plan", "routine", ag._ss_form(Rt.render(a)))
    fails = {"first": 0, "second": 3}
    better = ag._ss_routine_order([b, a], lambda c: fails[Rt.render(c)])
    equal = ag._ss_routine_order([a, b], lambda _c: 0)
    assert [Rt.render(x) for x in better] == ["first", "second"], better
    assert [Rt.render(x) for x in equal] == ["second", "first"], equal
    assert _rows(ag, "self_steer_read")[-1]["weighed"] == 1
    print("  stopped, 0 failures vs unstopped, 3: the stopped form first (a weight, not a tier); "
          "equal otherwise: the unstopped first")


def check_s3b_price_out_stop() -> None:
    import ast
    import inspect

    import tether
    ag = _agent()
    src = inspect.cleandoc("\n" + inspect.getsource(tether.Agent._mint))
    hits = [n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.If)
            and "priced_out_at_depth" in ast.unparse(n.test) and "_SELF_STEER" in
            ast.unparse(n.test) and "_ss_stop('vocabulary', 'mint'" in ast.unparse(n)]
    assert hits, "the price-out is not a mint stop"
    slot = _slot(ag)
    for _ in range(2):        # two price-outs on this slot kind, as the site writes them
        ag._ss_stop("vocabulary", "mint", ag._kind_key(slot))
    assert ag._ss_reads("vocabulary", "mint", ag._kind_key(slot)) is not None
    print("  the price-out site writes the mint stop; two of them read the steer for that kind")


def check_s5_pay_restores() -> None:
    ag = _agent()
    kind = ("k",)
    ag._ss_stop("plan", "hyp", kind)
    ag._ss_stop("plan", "hyp", kind)
    on = ag._ss_reads("plan", "hyp", kind)
    ag._ss_pay("plan", "hyp", kind)
    off = ag._ss_reads("plan", "hyp", kind)
    assert on is not None and off is None, (on, off)
    print(f"  two stops read p {on:.3f}; one pay after: nothing to read")


def check_s6_one_reader() -> None:
    import ast
    import inspect

    import tether
    assert tether._SELF_STEER, "TETHER_SELF_STEER is OFF"
    tree = ast.parse(inspect.cleandoc("\n" + inspect.getsource(tether.Agent)))
    readers: dict = {}
    for fn in ast.walk(tree):
        if not isinstance(fn, ast.FunctionDef):
            continue
        for n in ast.walk(fn):
            if isinstance(n, ast.Call) and ast.unparse(n.func).endswith("_ss_reads"):
                line = n.args[1].value if isinstance(n.args[1], ast.Constant) else "?"
                readers.setdefault(line, set()).add(fn.name)
    assert readers == {"hyp": {"_ss_hyp_price"}, "mint": {"_tc_walk"},
                       "routine": {"_ss_routine_order"}}, readers
    for f in (tether.Agent._ss_hyp_price, tether.Agent._ss_routine_order):
        rets = [n for n in ast.walk(ast.parse(inspect.cleandoc("\n" + inspect.getsource(f))))
                if isinstance(n, ast.Return)]
        assert len(rets) <= 2, f.__name__
    assert tether.Agent._ss_form("o12~o3.row") == "o~o.row"
    print(f"  readers { {k: sorted(v) for k, v in readers.items()} }; keys drop object ids")


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
    print(f"self_steer: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
