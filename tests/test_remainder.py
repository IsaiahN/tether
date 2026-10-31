"""1e NAMED_REMAINDER (TETHER_NAMED_REMAINDER, default ON; the reviewer 2026-10-29 r325, r364).
On a stepped gridworld agent (default seed 0, birth seed pinned): the remainder row's three
readings, each check in its own process, under 5 minutes.
  check_a_pair              last survivors with disjoint charged rows: the pair and its row split
  check_a_not_found         no disjoint pair: "no split found among the last survivors", never
                            "one question" (Fig 8 :39)
  check_a_mustfail_overlap  MUST-FAIL: the pair test with disjointness dropped names a pair whose
                            charged sets intersect; the real test names none
  check_a_mustfail_empty    MUST-FAIL (r370): with non-emptiness dropped, a survivor charged on no
                            row pairs with another; the real test names none, uncharged 1
  check_c_budget            the gap's last verdict budget_spent: "unreached at this budget"
  check_c_priced_out        priced_out_at_depth: the mint's own note, verbatim
  check_c_age               a verdict from an earlier mint of the same space carries its own cycle
  check_wired               1c's none_survive writes the remainder row right after its stop_rule
                            row, with 1c's cause
  check_verdict_stored      a stepped agent stores its parked mints' verdicts on their spaces
  check_verdict_mustfail_off   MUST-FAIL: TETHER_NAMED_REMAINDER off stores none
  check_off_identity_grid, check_off_identity_fake   TETHER_NAMED_REMAINDER=0 (and every later
                            batch arm, off_env) against 2dea904
    python tests/test_remainder.py [check ...]
"""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile

from _batch import off_env  # noqa: E402  the batch's arms (r348)

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

BASE = "2dea904"        # wip/ask-stop after (a2), the tree before the arm
ROWS = [0, 1, 2, 3]   # constructed residual rows; the row test is stubbed per term
NOTE = "the whole space at this depth was seen and none paid; not at this depth, NOT unreachable"


def _agent(steps: int = 6):
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    tether._AGENT_SEED = False
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="remainder_fixture"), tether.Config(),
                      ledger.Ledger())
    for _ in range(steps):
        ag.step()
    return env, ag


def _gap(ag) -> str:
    slots = [s for s in sorted(ag._space) if s in ag._tally]
    assert slots, ("occasion: an open space with a tally", sorted(ag._space))
    return slots[0]


def _term(name: str):
    import gamma
    return gamma.Term((gamma.Atom(name, lambda v, _c: v, "val", "val"),))


def _remainder(charged: dict, verdict=None, splits=None) -> dict:
    """The last survivors {name: charged rows}, priced in the gap's tally; the row it writes."""
    _env, ag = _agent()
    slot = _gap(ag)
    terms = {n: _term(n) for n in charged}
    for t in terms.values():
        ag._tally[slot][1][t] = (len(ROWS), 0, None, None, 0, None, 0.0)
    ag._residual_obs = lambda _s, _h, _hist: ROWS
    ag._row_wrong = lambda t, _s, row: row in charged[t.name]
    if verdict is not None:
        ag._space[slot]["verdict"] = verdict(ag)
    if splits is not None:
        ag._splits = splits
    import tether
    n0 = len(ag.led.rows())
    # in the scope the 1c pass opens (12, TETHER_STOP_READ_STEP: ACCEPT; off, MINT), its only caller
    step = "ACCEPT" if tether._STOP_READ_STEP else "MINT"
    with ag._step_scope(step):
        ag._remainder(slot, dict.fromkeys(charged, 1.0), "bound")
    rows = [r for r in ag.led.rows()[n0:] if r["event"] == "remainder"]
    assert len(rows) == 1 and rows[0]["slot"] == slot and rows[0]["step"] == step, rows
    return rows[0]


def check_a_pair() -> None:
    d = _remainder({"rem_a": {0, 1}, "rem_b": {2, 3}, "rem_c": {0, 1, 2}})["detail"]
    s = d["several"]
    assert s["pair"] == ["rem_a", "rem_b"] and s["shared_charged"] == 0, s
    assert s["explained_by_a_only"] == [2, 3] and s["explained_by_b_only"] == [0, 1], s
    assert d["population"] == "last_survivors" and d["last_survivors"] == 3, d
    print(f"  rem_a {{0,1}}, rem_b {{2,3}}, rem_c {{0,1,2}}: pair {s['pair']}, a explains "
          f"{s['explained_by_a_only']}, b explains {s['explained_by_b_only']}")


def check_a_not_found() -> None:
    d = _remainder({"rem_a": {0, 1, 2, 3}, "rem_b": {1, 2}})["detail"]
    assert d["several"] == "no split found among the last survivors", d["several"]
    assert "one question" not in json.dumps(d), d
    print(f"  no disjoint pair among {d['last_survivors']}: '{d['several']}', "
          f"{d['charged_sets']} charged sets")


def check_a_mustfail_overlap() -> None:
    charged = {"rem_a": {0, 1}, "rem_b": {1, 2}}
    real = _remainder(charged)["detail"]["several"]
    assert real == "no split found among the last survivors", real
    broke = _remainder(charged, splits=lambda a, b: a != b)["detail"]["several"]
    assert isinstance(broke, dict) and broke["shared_charged"] > 0, (
        "MUST-FAIL: without disjointness a pair sharing a charged row is named", broke)
    print(f"  MUST-FAIL: disjointness dropped names {broke['pair']} sharing "
          f"{broke['shared_charged']} charged row; the real test names none")


def check_a_mustfail_empty() -> None:
    charged = {"rem_a": set(), "rem_b": {0, 1}}
    real = _remainder(charged)["detail"]
    assert real["several"] == "no split found among the last survivors", real["several"]
    assert real["uncharged"] == 1, real
    broke = _remainder(charged, splits=lambda a, b: not (a & b))["detail"]["several"]
    assert isinstance(broke, dict) and broke["explained_by_b_only"] == [], (
        "MUST-FAIL: without non-emptiness an uncharged survivor pairs with another", broke)
    print(f"  MUST-FAIL: non-emptiness dropped names {broke['pair']} though rem_a explains every "
          "row; the real test names none and reports uncharged 1")


def _vk() -> tuple:
    """The row's keys for the mint's verdict and its cycle (14, TETHER_REMAINDER_VERDICT_KEY)."""
    import tether
    return (("mint_verdict", "mint_verdict_cycle") if tether._REMAINDER_VERDICT_KEY
            else ("verdict", "verdict_cycle"))


def check_c_budget() -> None:
    d = _remainder({"rem_a": {0}}, verdict=lambda ag: ("budget_spent", "stopped early", ag.cycle))
    d, (vk, ck) = d["detail"], _vk()
    assert d[vk] == "budget_spent" and d["reach"] == "unreached at this budget", d
    print(f"  {vk} budget_spent at cycle {d[ck]}: reach '{d['reach']}'")


def check_c_priced_out() -> None:
    d = _remainder({"rem_a": {0}},
                   verdict=lambda ag: ("priced_out_at_depth", NOTE, ag.cycle))["detail"]
    vk = _vk()[0]
    assert d[vk] == "priced_out_at_depth" and d["reach"] == NOTE, d
    print(f"  {vk} priced_out_at_depth: reach is the mint's own note: '{d['reach']}'")


def check_c_age() -> None:
    # an earlier mint's verdict in the SAME space: no older than the space's opening (r365), and
    # older than the row reading it
    row = _remainder({"rem_a": {0}},
                     verdict=lambda ag: ("budget_spent", "stopped early",
                                         ag._space[_gap(ag)]["opened"]))
    d, ck = row["detail"], _vk()[1]
    assert d["opened"] <= d[ck] < row["cycle"], (row["cycle"], d)
    print(f"  a verdict from cycle {d[ck]} read at cycle {row['cycle']} (space opened "
          f"{d['opened']}) carries its own cycle")


def check_wired() -> None:
    _env, ag = _agent()
    slot = _gap(ag)
    a, b = _term("stop_test_a"), _term("stop_test_b")
    table = {slot: ([(a, 1.0), (b, 1.5)], 2.0)}
    ag._space_bounds = lambda s, _mode: table.get(s) if s == slot else None
    ag._stop_rules()
    table[slot] = ([(a, 2.5), (b, 3.0)], 2.0)
    n0 = len(ag.led.rows())
    ag._stop_rules()
    rows = [r for r in ag.led.rows()[n0:] if r["slot"] == slot
            and r["event"] in ("stop_rule", "remainder")]
    assert [r["event"] for r in rows] == ["stop_rule", "remainder"], rows
    assert rows[1]["detail"]["cause"] == rows[0]["detail"]["cause"] == "bound", rows
    print(f"  {slot}: none_survive (cause bound) then its remainder row, cause bound")


def _verdicts(on: bool) -> list:
    import tether
    tether._NAMED_REMAINDER = on
    _env, ag = _agent(12)
    return [(s, sp["verdict"]) for s, sp in sorted(ag._space.items()) if "verdict" in sp], ag


def check_verdict_stored() -> None:
    got, ag = _verdicts(True)
    parks = [r for r in ag.led.rows() if r["event"] == "park" and r["detail"].get("verdict")]
    assert parks, "occasion: a parked mint with a verdict"
    assert got and all(len(v) == 3 and v[2] <= ag.cycle for _s, v in got), got
    print(f"  {len(parks)} parked mints; {len(got)} open spaces carry their last verdict, e.g. "
          f"{got[0][0]}: {got[0][1][0]} at cycle {got[0][1][2]}")


def check_verdict_mustfail_off() -> None:
    got, ag = _verdicts(False)
    parks = [r for r in ag.led.rows() if r["event"] == "park" and r["detail"].get("verdict")]
    assert parks, "occasion: a parked mint with a verdict"
    assert not got, ("MUST-FAIL: OFF stores no verdict", got)
    print(f"  MUST-FAIL: OFF, {len(parks)} parked mints and no space carries a verdict")


PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
tree, which = sys.argv[1], sys.argv[2]
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
if which == "fake":
    import arc_holdout
    from test_entry import FakeWrapper
    env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
    n = 24
else:
    import gamma, gridworld, ledger, tether, world
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    n = 24
for _ in range(n):
    ag.step()
ag.end_run("cap")
print(json.dumps({"rows": ag.led.rows()}, default=str))
'''


def _child(tree: str, which: str, extra: dict | None = None) -> list:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               **(extra or {}))
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, tree, which], env=env,
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


def _off_identity(w: str) -> None:
    root = str(_repo.ROOT)
    with tempfile.TemporaryDirectory() as d:
        tar = subprocess.run(["git", "-C", root, "archive", BASE], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        base = _norm(_child(d, w))
    cur = _norm(_child(root, w, off_env("TETHER_NAMED_REMAINDER")))   # and every later batch arm
    diff = sum(1 for x, y in zip(base, cur, strict=False) if x != y) + abs(len(base) - len(cur))
    assert len(base) > 50 and diff == 0, (w, len(base), len(cur), next(
        (i for i, (x, y) in enumerate(zip(base, cur, strict=False)) if x != y), None))
    print(f"  OFF identity (TETHER_NAMED_REMAINDER=0, {w}): {len(base)} rows against {BASE}, "
          "0 differences")


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
    print(f"remainder: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
