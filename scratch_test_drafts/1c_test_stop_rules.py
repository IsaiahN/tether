"""1c STOP_RULES (TETHER_STOP_RULES, default ON; the reviewer 2026-10-29 r325, r327, r337, r338).
On a stepped gridworld agent (default seed 0, birth seed pinned) whose space record is replaced by a
stub S1, so each rule meets exactly its occasion. Each check runs in its own process, under 5
minutes.
  check_i_held                    one survivor with a risky settle under the space's current key:
                                  a stop_rule row "held"
  check_i_mustfail_not_risky      MUST-FAIL: the same survivor with no risky settle: no stop
  check_i_mustfail_old_key        MUST-FAIL (r338): the risky settle predates the current key:
                                  no stop
  check_ii_none_survive           survivors, then none, on a current key: "none_survive", and the
                                  slot owes (owed_import)
  check_ii_mustfail_stale_key     MUST-FAIL: the same with the record unable to judge: no row
  check_ii_bar_only               r339: bounds unchanged, the bar moved: none_survive, cause "bar",
                                  nothing owed
  check_ii_mustfail_bar_only      MUST-FAIL: the same with no cause split (a spy): it owes
  check_ii_small_rise             r340: 1.0 -> 1.1 while the bar falls 2.0 -> 0.5: cause "bar"
  check_ii_mustfail_small_rise    MUST-FAIL: under r339's any-rise rule the same reading owes
  check_ii_stale_cells            r340: every last survivor's cell invalid: cause "stale"
  check_ii_unsynced               r342 5: the cells priced a row ahead of the bar: cause
                                  "unsynced", nothing owed
  check_ii_mustfail_unsynced      MUST-FAIL: the same with the sync test spied off: it owes
  check_iii_split_refused         an abstention with two survivors: ask_unsplit, the gap in the
                                  probe's aim set
  check_iii_mustfail_off          MUST-FAIL: TETHER_STOP_RULES off, the same abstention aims nowhere
  check_iii_owner_read_anew       the owner's readings move: split_aim_left "owner read anew"
  check_iii_spent                 r338: a probe press at an unmoved owner spends the aim ("probed"),
                                  and the same refusal does not re-enter
  check_iii_mustfail_no_spend     MUST-FAIL: with no press, the unmoved owner's aim stays K steps
  check_bound_fake                r325 (3): over 24 fake steps the aim map's peak is at most the
                                  refusals made (printed)
  check_off_identity_grid, check_off_identity_fake   TETHER_STOP_RULES=0 against 20cc52a
    python tests/test_stop_rules.py [check ...]
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

BASE = "20cc52a"      # wip/ask-stop after 1d, the tree before the arm
K = 3


def _agent(steps: int = 6):
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    tether._AGENT_SEED = False
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="stop_rules_fixture"), tether.Config(),
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


def _stub(ag, slot: str, table: dict) -> None:
    """The space record replaced: slot -> ([(term, stored bound)], bar), or None for 'the record
    cannot judge'; S1 and 1c read it through _space_bounds."""
    ag._space_bounds = lambda s: table.get(s) if s == slot else None


def _rows(ag, n0: int, ev: str) -> list:
    return [r for r in ag.led.rows()[n0:] if r["event"] == ev]


def _held(risky_key) -> list:
    _env, ag = _agent()
    slot = _gap(ag)
    t = _term("stop_test_one")
    _stub(ag, slot, {slot: ([(t, 1.0)], 2.0)})
    if risky_key is not None:
        ag._risky[(slot, t.name)] = risky_key(ag, slot)
    n0 = len(ag.led.rows())
    ag._stop_rules()
    return [r for r in _rows(ag, n0, "stop_rule") if r["slot"] == slot], slot


def check_i_held() -> None:
    rows, slot = _held(lambda ag, s: ag._tally[s][0])
    assert [r["detail"]["rule"] for r in rows] == ["held"], rows
    print(f"  {slot}: one survivor, a risky settle under the current key: stop_rule held")


def check_i_mustfail_not_risky() -> None:
    rows, slot = _held(None)
    assert not rows, ("MUST-FAIL: no risky settle, no stop", rows)
    print(f"  MUST-FAIL: {slot}, one survivor and no risky settle: no stop_rule row")


def check_i_mustfail_old_key() -> None:
    rows, slot = _held(lambda ag, s: ("an earlier key", ag._tally[s][0]))
    assert not rows, ("MUST-FAIL: a risky settle before the current key does not hold", rows)
    print(f"  MUST-FAIL: {slot}, the risky settle predates the current key: no stop_rule row")


def _none_survive(judgeable: bool, after=None, no_split=None, stamp_off=None,
                  sync_spy: bool = False) -> tuple:
    """Two survivors under the bar 2.0, then a reading with none: by default their bounds ROSE
    past an unchanged bar (r339's evidence); `after` gives another reading."""
    _env, ag = _agent()
    slot = _gap(ag)
    a, b = _term("stop_test_a"), _term("stop_test_b")
    table = {slot: ([(a, 1.0), (b, 1.5)], 2.0)}
    _stub(ag, slot, table)
    if no_split is not None:
        ag._none_cause = no_split                        # a spy: another cause rule
    if sync_spy:
        ag._rows_synced = lambda _cells, _bar: True      # a spy: no sync test
    ag._stop_rules()
    table[slot] = ((after or ([(a, 2.5), (b, 3.0)], 2.0)) if judgeable else None)
    if judgeable and stamp_off is not None:             # each cell priced over the bar's rows + off
        h = len(ag.history(slot)) + stamp_off
        table[slot] = (*table[slot][:2], {a.name: h, b.name: h})
    ag.owed_import.discard(slot)
    n0 = len(ag.led.rows())
    ag._stop_rules()
    return [r for r in _rows(ag, n0, "stop_rule") if r["slot"] == slot], slot, ag


def check_ii_none_survive() -> None:
    rows, slot, ag = _none_survive(True, stamp_off=0)    # synced: the same rows on both sides
    assert [r["detail"]["rule"] for r in rows] == ["none_survive"], rows
    d = rows[0]["detail"]
    assert d["cause"] == "bound" and d["owes"] and len(d["bound_rose"]) == 2, d
    assert d["reached_bar"] == sorted(d["bound_rose"]) and d["invalid_cells"] == 0, d
    assert d["cell_rows"] == [d["bar_rows"]], d
    assert slot in ag.owed_import, "the slot owes"
    print(f"  {slot}: two survivors, their bounds rose past the bar: none_survive, cause bound, "
          f"owes; rose {d['bound_rose']}")


def _bar_only(no_split=None) -> tuple:
    a, b = _term("stop_test_a"), _term("stop_test_b")
    return _none_survive(True, after=([(a, 1.0), (b, 1.5)], 0.5), no_split=no_split)


def _any_rise(prev, low, _bar_before):
    """r339's first rule, before r340: any rise at all is evidence."""
    return "bound" if any(n in low and low[n] > b for n, b in prev.items()) else "bar"


def check_ii_bar_only() -> None:
    rows, slot, ag = _bar_only()
    d = rows[0]["detail"] if rows else {}
    assert [r["detail"]["rule"] for r in rows] == ["none_survive"], rows
    assert d["cause"] == "bar" and not d["owes"] and not d["bound_rose"], d
    assert slot not in ag.owed_import, "a bar move owes nothing (r339)"
    print(f"  {slot}: bounds unchanged, the bar fell 2.0 -> 0.5: none_survive, cause bar, nothing "
          "owed")


def check_ii_mustfail_bar_only() -> None:
    rows, slot, ag = _bar_only(lambda _prev, _low, _bar: "bound")
    assert rows and rows[0]["detail"]["cause"] == "bound", ("occasion: the spy took", rows)
    assert slot in ag.owed_import, ("MUST-FAIL: without the cause split a bar move owes", slot)
    print(f"  MUST-FAIL: {slot}, no cause split (spy): the same bar move owes")


def check_ii_unsynced() -> None:
    rows, slot, ag = _none_survive(True, stamp_off=1)    # the cells re-priced a row ahead
    d = rows[0]["detail"]
    assert d["cause"] == "unsynced" and not d["owes"], d
    assert d["cell_rows"] == [d["bar_rows"] + 1], d
    assert slot not in ag.owed_import, "an unsynced reading owes nothing (r342 5)"
    print(f"  {slot}: bounds rose, but the cells were priced over {d['cell_rows']} rows and the "
          f"bar over {d['bar_rows']}: cause unsynced, nothing owed")


def check_ii_mustfail_unsynced() -> None:
    rows, slot, ag = _none_survive(True, stamp_off=1, sync_spy=True)
    d = rows[0]["detail"]
    assert len(d["bound_rose"]) == d["last_survivors"], ("occasion: every bound rose", d)
    assert d["cause"] == "bound" and slot in ag.owed_import, ("MUST-FAIL: no sync test owes", d)
    print(f"  MUST-FAIL: {slot}, the sync test spied off: the same reading owes (cause bound)")


def _small_rise(rule=None) -> tuple:
    a, b = _term("stop_test_a"), _term("stop_test_b")
    return _none_survive(True, after=([(a, 1.1), (b, 1.5)], 0.5), no_split=rule)


def check_ii_small_rise() -> None:
    rows, slot, ag = _small_rise()
    d = rows[0]["detail"]
    assert d["cause"] == "bar" and d["bound_rose"] and not d["reached_bar"], d
    assert slot not in ag.owed_import, "a rise under the old bar is the cut, not evidence"
    print(f"  {slot}: 1.0 -> 1.1 under a bar 2.0 -> 0.5: cause bar, nothing owed; rose "
          f"{d['bound_rose']}")


def check_ii_mustfail_small_rise() -> None:
    rows, slot, ag = _small_rise(_any_rise)
    assert rows and rows[0]["detail"]["bound_rose"], ("occasion: a small rise", rows)
    assert slot in ag.owed_import, ("MUST-FAIL: under 'any rise' the small rise owes", slot)
    print(f"  MUST-FAIL: {slot}, the any-rise rule (r339) owes on the same small rise")


def check_ii_stale_cells() -> None:
    rows, slot, ag = _none_survive(True, after=([], 2.0))
    d = rows[0]["detail"]
    assert d["cause"] == "stale" and d["invalid_cells"] == d["last_survivors"] == 2, d
    assert slot not in ag.owed_import, "a record that cannot judge its survivors owes nothing"
    print(f"  {slot}: every last survivor's cell invalid: cause stale, nothing owed")


def check_ii_mustfail_stale_key() -> None:
    rows, slot, ag = _none_survive(False)
    assert not rows and slot not in ag.owed_import, ("MUST-FAIL: a stale record judges nothing",
                                                     rows)
    print(f"  MUST-FAIL: {slot}, the record cannot judge: no row, nothing owed")


def _refuse(ag, slot: str) -> list:
    """An abstention: two survivors that predict alike under every press (one vector)."""
    _stub(ag, slot, {slot: ([(_term("stop_test_c"), 1.0), (_term("stop_test_d"), 1.0)], 2.0)})
    ag._predict_with = lambda _t, _s, _st, _a: 0
    ag._ask_cyc = (None, None)
    n0 = len(ag.led.rows())
    ag._ask_aimed(ag.env.observe())
    return _rows(ag, n0, "ask_unsplit")


def check_iii_split_refused() -> None:
    _env, ag = _agent()
    slot = _gap(ag)
    rows = _refuse(ag, slot)
    assert rows and rows[0]["slot"] == slot and not rows[0]["detail"]["spent"], rows
    assert slot in ag._aims(), ("the gap joins the probe's aims", ag._aims())
    print(f"  {slot}: no press splits 2 survivors: ask_unsplit, aims {sorted(ag._aims())}")


def check_iii_mustfail_off() -> None:
    import tether
    _env, ag = _agent()
    slot = _gap(ag)
    tether._STOP_RULES = False
    rows = _refuse(ag, slot)
    asks = [r for r in ag.led.rows() if r["event"] == "ask" and r["slot"] == slot]
    assert asks and asks[-1]["detail"]["chosen"] is None, ("occasion: the ask abstained", asks)
    assert not rows and slot not in ag._aims(), ("MUST-FAIL: OFF aims nowhere", rows)
    print(f"  MUST-FAIL: OFF, {slot}'s ask abstains and nothing is aimed")


def _leave(ag, slot: str, now: dict) -> list:
    n0 = len(ag.led.rows())
    last = list(ag.trace[-1])
    last[2] = now                                  # this frame's after-state, the rest kept
    ag.trace[-1] = type(ag.trace[-1])(last)
    ag._stop_rules()
    return [r for r in _rows(ag, n0, "split_aim_left") if r["slot"] == slot]


def check_iii_owner_read_anew() -> None:
    _env, ag = _agent()
    slot = _gap(ag)
    _refuse(ag, slot)
    owner = slot.rsplit(".", 1)[0]
    reads, _rk = ag._split_aim[slot]
    moved = dict(ag.trace[-1][2])
    k = sorted(reads)[0]
    moved[k] = (reads[k] or 0) + 1
    rows = _leave(ag, slot, moved)
    assert [r["detail"]["why"] for r in rows] == ["owner read anew"], rows
    print(f"  {owner}'s {k} moved: split_aim_left 'owner read anew'")


def _unmoved(ag, slot: str) -> dict:
    reads, _rk = ag._split_aim[slot]
    return {**ag.trace[-1][2], **reads}


def check_iii_spent() -> None:
    _env, ag = _agent()
    slot = _gap(ag)
    _refuse(ag, slot)
    ag._split_probed[slot] = dict(ag._split_aim[slot][0])     # the probe pressed at the owner
    rows = _leave(ag, slot, _unmoved(ag, slot))
    assert [r["detail"]["why"] for r in rows] == ["probed"], rows
    assert rows[0]["detail"]["before"] == rows[0]["detail"]["after"], rows[0]
    again = _refuse(ag, slot)
    assert again and again[0]["detail"]["spent"] and slot not in ag._aims(), again
    print(f"  {slot}: probed at an unmoved owner -> 'probed', the aim spent; the same refusal "
          "does not re-enter")


def check_iii_mustfail_no_spend() -> None:
    _env, ag = _agent()
    slot = _gap(ag)
    _refuse(ag, slot)
    left = []
    for _ in range(K):
        left += _leave(ag, slot, _unmoved(ag, slot))
    assert not left and slot in ag._aims(), ("MUST-FAIL: no press, the aim stays", left)
    print(f"  MUST-FAIL: no press at an unmoved owner, the aim stays {K} steps: {slot}")


def check_bound_fake() -> None:
    import arc_holdout
    import tether
    from test_entry import FakeWrapper
    tether._AGENT_SEED = False
    env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
    peak = 0
    for _ in range(24):
        env.observe()
        ag.step()
        peak = max(peak, len(ag._split_aim))
        if env.terminal():
            break
    refused = [r for r in led.rows() if r["event"] == "ask_unsplit"
               and not r["detail"]["spent"]]
    left = [r["detail"]["why"] for r in led.rows() if r["event"] == "split_aim_left"]
    assert peak <= len(refused), (peak, len(refused))
    print(f"  fake, 24 steps: aim map peak {peak}; refusals {len(refused)}; leaves {left}")


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
    cur = _norm(_child(root, w, {"TETHER_STOP_RULES": "0"}))
    diff = sum(1 for x, y in zip(base, cur, strict=False) if x != y) + abs(len(base) - len(cur))
    assert len(base) > 50 and diff == 0, (w, len(base), len(cur), next(
        (i for i, (x, y) in enumerate(zip(base, cur, strict=False)) if x != y), None))
    print(f"  OFF identity (TETHER_STOP_RULES=0, {w}): {len(base)} rows against {BASE}, "
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
    print(f"stop_rules: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
