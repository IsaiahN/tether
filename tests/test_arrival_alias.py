"""10 ARRIVAL_ALIAS (TETHER_ARRIVAL_ALIAS, default ON; the reviewer r428, r431).
Minimal gates: one must-fail (with the occasion), one must-hold, each in its own process.
  check_mustfail_alias  a gridworld agent whose Agency holds counts on two board objects and three
                        that left at a break: ON's turnover keeps the board's counts, carries the
                        object whose form is unique on both sides (o1 -> o9), rests the two that
                        share a form, and contingent() no longer reads a slot off the board; OFF
                        (no turnover call) still reads o1.col
  check_off_identity    MUST-HOLD: TETHER_ARRIVAL_ALIAS=0 (off_env) byte-equal to b0489bf on the
                        fake whole run; ON's run is compared too and its arrival_alias rows counted
    python tests/test_arrival_alias.py [check ...]
"""
from __future__ import annotations

import io
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
from test_contact_first import _child, _norm  # noqa: E402  the same probe and masks

sys.dont_write_bytecode = True

BASE = "b0489bf"        # wip/finish3 after 9 CONTINGENT_ONE_PASS


def _agent():
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    tether._AGENT_SEED = False
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    ag.slots = ["o5.row", "o9.col"]                         # the board after the break
    env.forms = lambda: {"o5": 333, "o9": 444}
    t, m = ag.agency.tried, ag.agency.moved
    t[("o1.col", "ACTION1")], t[("o1.col", "ACTION2")], m[("o1.col", "ACTION1")] = 2, 2, 2
    t[("o2.row", "ACTION1")], t[("o3.row", "ACTION1")] = 1, 1
    t[("o5.row", "ACTION1")] = 3
    ag._aa_due, ag._aa_form, ag._aa_succ = 7, {"o1": 444, "o2": 222, "o3": 222}, {"o1": "o5"}
    return ag


def _totals(a) -> tuple:
    return (sum(a.tried.values()) + sum(a.dormant_tried.values()),
            sum(a.moved.values()) + sum(a.dormant_moved.values()))


def _row(ag) -> dict:
    rows = [r for r in ag.led.rows() if r["event"] == "arrival_alias"]
    assert len(rows) == 1, rows
    return rows[0]["detail"]


def check_mustfail_alias() -> None:
    off = _agent().agency.contingent()                     # MUST-FAIL: OFF reads o1.col
    assert off == ["o1.col"], off
    ag = _agent()
    before = _totals(ag.agency)
    ag._arrival_alias()
    on = ag.agency.contingent()
    assert on == ["o9.col"], on
    owners = {s.split(".")[0] for s, _a in ag.agency.tried}
    assert owners <= {"o5", "o9"}, owners
    assert ag.agency.tried[("o5.row", "ACTION1")] == 3     # the board's own count, unchanged
    assert ag.agency.dormant_tried == {("o2.row", "ACTION1"): 1, ("o3.row", "ACTION1"): 1}
    assert _totals(ag.agency) == before, (before, _totals(ag.agency))   # moved, never copied
    d = _row(ag)
    assert (d["aliases_by_form"], d["aliases_by_successor"], d["alias"]) == (1, 0, {"o1": "o9"}), d
    assert (d["kept"], d["aliased"], d["dormant"], d["alias_collision"]) == (1, 2, 2, 0), d
    col = _agent()                                         # the board already wrote o9.col ACTION1
    col.agency.tried[("o9.col", "ACTION1")] = 1
    before_c = _totals(col.agency)
    col._arrival_alias()
    dc = _row(col)
    assert (dc["aliased"], dc["alias_collision"]) == (1, 1), dc
    assert col.agency.tried[("o9.col", "ACTION1")] == 1, col.agency.tried    # never merged
    assert col.agency.dormant_tried[("o1.col", "ACTION1")] == 2, col.agency.dormant_tried
    assert _totals(col.agency) == before_c, (before_c, _totals(col.agency))
    print(f"  off: contingent {off}; on: contingent {on}, alias {d['alias']}, kept {d['kept']}, "
          f"aliased {d['aliased']}, dormant {d['dormant']}, collision {d['alias_collision']}; "
          f"tried+dormant and moved+dormant equal before and after {before}; the collision "
          f"fixture: aliased {dc['aliased']}, alias_collision {dc['alias_collision']}, not merged")


def check_off_identity() -> None:
    import tarfile
    import tempfile

    from _batch import off_env
    root = str(_repo.ROOT)
    with tempfile.TemporaryDirectory() as d:
        tar = subprocess.run(["git", "-C", root, "archive", BASE], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        base = _norm(_child(d))
    off = _norm(_child(root, off_env("TETHER_ARRIVAL_ALIAS")))
    diff = sum(1 for x, y in zip(base, off, strict=False) if x != y) + abs(len(base) - len(off))
    assert len(base) > 50 and diff == 0, ("OFF", len(base), len(off), next(
        (i for i, (x, y) in enumerate(zip(base, off, strict=False)) if x != y), None))
    on_rows = _child(root)
    on = _norm(on_rows)
    aa = sum(1 for r in on_rows if r["event"] == "arrival_alias")
    on_diff = sum(1 for x, y in zip(base, on, strict=False) if x != y) + abs(len(base) - len(on))
    assert aa > 0 or on_diff == 0, ("ON differs with no arrival_alias row", on_diff)
    print(f"  OFF (TETHER_ARRIVAL_ALIAS=0, fake): {len(base)} rows against {BASE}, 0 differences; "
          f"ON: {aa} arrival_alias rows, {on_diff} rows differ")


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
    print(f"arrival_alias: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
