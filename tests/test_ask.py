"""1b ASK (TETHER_ASK, default ON; the reviewer 2026-10-29 r279, r322, r325). Each check runs in its
own process, under 5 minutes.
  check_split_rule        the interface, given a split: the press whose LARGEST block is smallest;
                          a tie goes to more blocks; every press leaving one block abstains
  check_occasion_fake     the fake ARC game, 24 steps: asks happen (a young gap with two or more
                          survivors); each ask row names gaps_eligible, gap_asked and survivors >= 2
  check_split_chosen      a constructed gap whose two survivors differ only under the first offered
                          action: the ask takes that action, partition [1, 1]
  check_split_mustfail    MUST-FAIL: the same gap with TETHER_ASK off writes no ask and realises
                          the board-level DISTINGUISH
  check_hold_no_gap       MUST-HOLD: gridworld, the steps before its first ask: ON
                          writes the same ledger as OFF (wall timings masked)
  check_off_identity_grid, check_off_identity_fake   TETHER_ASK=0 writes the same ledger as dad9d2b
    python tests/test_ask.py [check ...]
"""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

BASE = "dad9d2b"      # general-agent after 1a, the tree before the arm
HOLD = 10             # gridworld default seed 0 first asks at cycle 12 under bargain S1 (r327)


def _agent(which: str, steps: int):
    import tether
    tether._AGENT_SEED = False
    if which == "fake":
        import arc_holdout
        from test_entry import FakeWrapper
        env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
    else:
        import gamma
        import gridworld
        import ledger
        import world
        env = world.bind(gridworld.family("default", 0))
        led = ledger.Ledger()
        ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), led)
    for _ in range(steps):
        if which == "fake":
            env.observe()
        ag.step()
        if which == "fake" and env.terminal():
            break
    return env, ag, led


def check_split_rule() -> None:
    import interface as IFace
    env, ag, _led = _agent("grid", 2)
    acts = tuple(ag.actions)
    assert len(acts) >= 3, ("occasion: fewer than three actions", acts)
    a, b, c = acts[:3]
    before, ctx = env.observe(), IFace.Interface.context(env)
    want = IFace.Intent(IFace.DISTINGUISH, subject="o0.row")

    def take(split):
        r = ag.iface.realise(want, acts, ctx, before, env, split=split)
        return None if r is None else r.action
    got = take({a: [3], b: [2, 1], c: [1, 1, 1]})
    assert got == c, ("the smallest largest block", got)
    got2 = take({a: [2, 2], b: [2, 1, 1], c: [4]})
    assert got2 == b, ("a tie goes to more blocks", got2)
    got3 = take({a: [4], b: [4], c: [4]})
    assert got3 is None, ("no press splits: abstain", got3)
    print(f"  split rule: {{3}}/{{2,1}}/{{1,1,1}} -> {c}; {{2,2}}/{{2,1,1}}/{{4}} -> {b}; all one "
          "block -> abstain")


def _reset_split(known: bool):
    import interface as IFace
    IFace._RESET_KNOWN = known
    env, ag, _led = _agent("fake", 2)
    acts = tuple(ag.actions)
    assert IFace.RESET in acts and ag.iface.alive, ("occasion: a live board offering RESET", acts)
    a, b = [x for x in acts if x != IFace.RESET][:2]
    split = {IFace.RESET: [1, 1, 1], a: [2, 1], b: [3]}
    r = ag.iface.realise(IFace.Intent(IFace.DISTINGUISH, subject="o0.shape"), acts,
                         IFace.Interface.context(env), env.observe(), env, split=split)
    return None if r is None else r.action, a


def check_split_reset() -> None:
    got, a = _reset_split(True)
    assert got == a, ("D-WIN-RESET: a live board's RESET splits nothing", got)
    print(f"  live board: RESET's split {{1,1,1}} is not taken; {a}'s {{2,1}} is")


def check_split_reset_mustfail() -> None:
    import interface as IFace
    got, _a = _reset_split(False)
    assert got == IFace.RESET, ("MUST-FAIL: TETHER_RESET_KNOWN off and RESET not taken", got)
    print("  MUST-FAIL: TETHER_RESET_KNOWN off, RESET's {1,1,1} is taken")


def _rows(led, ev: str) -> list:
    return [r for r in led.rows() if r["event"] == ev]


def check_occasion_fake() -> None:
    _env, _ag, led = _agent("fake", 24)
    asks = _rows(led, "ask")
    assert asks, "occasion: no ask on the fake game in 24 steps"
    for r in asks:
        d = r["detail"]
        assert r["step"] == "PLAN", ("the ask row's step", r["step"])
        assert d["gaps_eligible"] >= 1 and d["gap_asked"] == r["slot"] and d["survivors"] >= 2, d
    print(f"  fake, 24 steps: {len(asks)} asks, e.g. {asks[0]['slot']} with "
          f"{asks[0]['detail']['survivors']} survivors, {asks[0]['detail']['vectors']} prediction "
          f"vectors, chosen {asks[0]['detail']['chosen']}")


def _constructed(ask: bool):
    """A gridworld agent, one open gap: two survivors that differ only under the first action."""
    import gamma
    import tether
    tether._ASK = ask
    env, ag, led = _agent("grid", 3)
    acts = tuple(ag.actions)
    slot = "o0.row"
    first = acts[0]
    step_ = gamma.Atom("ask_test_step", lambda v, c: v + 1 if c.action == first else v, "val",
                       "val")
    still = gamma.Atom("ask_test_still", lambda v, _c: v, "val", "val")
    terms = [gamma.Term((step_,)), gamma.Term((still,))]
    ag._space = {slot: {"kind": (), "opened": ag.cycle, "mints": 1, "base": None}}
    ag._survivors = lambda s: terms if s == slot else []
    ag._ask_cyc = (None, None)
    n0 = len(led.rows())
    before = env.observe()
    if tether._ASK and tether._DIVIDE:                 # choose's path: the aimed ask first
        r, gap = ag._ask_aimed(before)
    else:
        import interface as IFace
        r, gap = ag.iface.realise(IFace.Intent(IFace.DISTINGUISH), acts,
                                  IFace.Interface.context(env), before, env), None
    return first, r, gap, led.rows()[n0:]


def _s1_case(below: bool):
    """r327: a term wrong on one residual row, its stored bound just under (or at) the bar."""
    import gamma
    from tether import IDN
    _env, ag, _led = _agent("grid", 6)

    def live():
        for s in sorted(ag._space):
            h = ag.gamma.library[ag.bound.get(s, IDN)]
            if s in ag._tally and ag._tally[s][0] == ag._divide_key(s, h):
                return s, h
        return None, None
    slot, held = live()
    for _ in range(18):
        if slot is not None:
            break
        ag.step()
        slot, held = live()
    assert slot is not None, "occasion: no open space with a current key in 24 gridworld steps"
    seen = ag._tally[slot]
    bar = ag._bar(slot, held)
    unit = __import__("math").log2(ag.alphabet[slot])
    atom = gamma.Atom("s1_test", lambda v, _c: v, "val", "val")
    t = gamma.Term((atom,))
    cost = bar - unit - (1.0 if below else 0.0)          # bound = cost + unit x 1 row charged
    seen[1][t] = (1, 1, 0, None, 1, None, cost)          # one row covered, charged, REFUTED there
    return t in ag._survivors(slot), slot, bar, cost + unit


def check_s1_bargain_hold() -> None:
    got, slot, bar, bound = _s1_case(True)
    assert got, ("S1 MUST-HOLD: a term wrong on a row, its bound under the bar, is a survivor",
                 slot, bar, bound)
    print(f"  S1 must-hold: {slot}, a term refuted on one row with bound {bound:.3f} under the "
          f"bar {bar:.3f} is a survivor (strict consistency would have cut it)")


def check_s1_bargain_mustfail() -> None:
    got, slot, bar, bound = _s1_case(False)
    assert not got, ("S1 MUST-FAIL: a bound at the bar is still a survivor", slot, bar, bound)
    print(f"  S1 must-fail: {slot}, the same term with bound {bound:.3f} at the bar {bar:.3f} is "
          "not a survivor")


def check_split_chosen() -> None:
    first, r, gap, rows = _constructed(True)
    asks = [x for x in rows if x["event"] == "ask"]
    assert asks, "occasion: no ask on the constructed gap"
    d = asks[0]["detail"]
    assert gap == "o0.row" and r is not None and r.action == first, (gap, r)
    assert d["chosen"] == first and d["partition"] == [1, 1] and d["survivors"] == 2, d
    print(f"  constructed gap o0.row, 2 survivors split only by {first}: the ask takes {first}, "
          f"partition {d['partition']}")


def check_split_mustfail() -> None:
    _first, r, gap, rows = _constructed(False)
    assert not [x for x in rows if x["event"] == "ask"], "MUST-FAIL: an ask with TETHER_ASK off"
    assert gap is None, ("MUST-FAIL: a gap was asked with the arm off", gap)
    print(f"  MUST-FAIL: TETHER_ASK off, the same gap writes no ask; DISTINGUISH realised at the "
          f"board ({None if r is None else r.action})")


PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
tree, which, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
if which == "fake":
    import arc_holdout
    from test_entry import FakeWrapper
    env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
else:
    import gamma, gridworld, ledger, tether, world
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
for _ in range(n):
    ag.step()
ag.end_run("cap")
print(json.dumps({"rows": ag.led.rows()}, default=str))
'''


def _child(tree: str, which: str, extra: dict | None = None, n: int | None = None) -> list:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               **(extra or {}))
    n = n or {"fake": 16, "grid": 24}[which]
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, tree, which, str(n)], env=env,
                         capture_output=True, text=True, timeout=900, cwd=str(_repo.ROOT),
                         stdin=subprocess.DEVNULL)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])["rows"]


def _norm(rows: list) -> list:
    sys.path.insert(0, os.path.join(str(_repo.ROOT), "conform"))
    from identity_mod_rows import mask_timings
    return [(r["cycle"], r["step"], r["slot"], r["event"],
             json.dumps(r["detail"], sort_keys=True, default=str))
            for r in mask_timings(json.loads(json.dumps(rows))) if r["event"] != "arms"]


def _same(a: list, b: list, what: str) -> None:
    diff = sum(1 for x, y in zip(a, b, strict=False) if x != y) + abs(len(a) - len(b))
    assert len(a) > 50 and diff == 0, (what, len(a), len(b), next(
        (i for i, (x, y) in enumerate(zip(a, b, strict=False)) if x != y), None))


def check_hold_no_gap() -> None:
    root = str(_repo.ROOT)
    on = _child(root, "grid", n=HOLD)
    assert not [r for r in on if r["event"] == "ask"], "occasion: gridworld asked; not a no-gap run"
    off = _child(root, "grid", {"TETHER_ASK": "0"}, n=HOLD)
    _same(_norm(on), _norm(off), "MUST-HOLD: no gap, ON differs from OFF")
    print(f"  MUST-HOLD: gridworld {HOLD} steps, no ask yet: ON = OFF, {len(on)} rows")


def _off_identity(w: str) -> None:
    root = str(_repo.ROOT)
    with tempfile.TemporaryDirectory() as d:
        tar = subprocess.run(["git", "-C", root, "archive", BASE], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        base = _norm(_child(d, w))
    cur = _norm(_child(root, w, {"TETHER_ASK": "0"}))
    _same(base, cur, f"OFF identity {w}")
    print(f"  OFF identity (TETHER_ASK=0, {w}): {len(base)} rows against {BASE}, 0 differences")


def check_off_identity_grid() -> None:
    _off_identity("grid")


def check_off_identity_fake() -> None:
    _off_identity("fake")


def main() -> int:
    want = sys.argv[1:]
    names = [k for k in globals() if k.startswith("check_") and (not want or k in want)]
    assert not want or len(names) == len(want), ("unknown check name", sorted(want))
    if len(names) == 1:
        globals()[names[0]]()
        print("ok  ", names[0])
        return 0
    for n in names:
        r = subprocess.run([sys.executable, "-B", __file__, n], cwd=str(_repo.ROOT),
                           stdin=subprocess.DEVNULL)
        assert r.returncode == 0, n
    print(f"ask: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
