"""C1a, A PAIR OWNER IS NOT AN OBJECT NAME, TETHER_PAIR_NOT_OBJECT (the reviewer 2026-10-17 14:24).
The fake ARC game, 12 actions, C-seed-X, the arm ON and OFF.

  P1    under a step budget the fixture does not reach (TETHER_STEP_BUDGET_N=10,000,000; peak spent
        < budget asserted on both sides, the claim's occasion), the two ledgers are the same row for
        row, the refusal counts (library, abduce) aside, the budget row's spent aside (the arm saves
        the refused pairs' evaluations), and the timings masked by the shared list
        (conform/identity_mod_rows, imported; the reviewer 2026-10-25 21:52, 23:04 r204): every
        offer, landing, bet and mint is unchanged (exact). Red since 297f951 (10-17, the step
        budget's arrival): its spent differs by the arm at any budget. The budget row's other fields
        (asked, not_asked, owed_*, classes, late_*) read spent only through the threshold
        `self._spent >= STEP_BUDGET` (tether.py, _lookup_slot and the T4/T5 count), so under a
        non-binding budget they are exact and are compared
  MF-ID a non-timing field changed in one row (goal_hypotheses' group_n) still differs
  P1b   at the shipped budget: ON spent <= OFF spent on every cycle's budget row (the inequality
        the aside in P1 gives up), and the named outcome, the lookups left owed (owed_lookups summed
        over the cycles), is not worse ON; MF-SWAP the ledgers swapped fail it
  P2    ON refuses pairings under "a pair owner is not an object name", and no parse refusal
        names a pair owner
  MF-P  OFF: the same pairings refuse per candidate at parse ("cannot tokenize at '~...")

    python tests/test_pair_not_object.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(_repo.ROOT, "conform"))
from identity_mod_rows import mask_timings  # noqa: E402

CHILD = r'''
import json, os, sys, tempfile
sys.dont_write_bytecode = True
import tether, tether_agent
from test_entry import FakeWrapper
tether._AGENT_SEED = False
windows = []                # the compile memo's keys at each memo_sizes row (cleared after it)
_row = tether.Agent._memo_sizes_row
def _snap(self, at, step):
    windows.append([at, sorted(repr(k) for k in self._compile_cache)])
    return _row(self, at, step)
tether.Agent._memo_sizes_row = _snap
led = os.path.join(tempfile.mkdtemp(), "p.jsonl")
tether_agent.run(FakeWrapper(script={}), "fake", max_actions=12, led_path=led)
json.dump(windows, open(led + ".compile.json", "w"))
print(led)
'''
NOT_OBJECT = "a pair owner is not an object name"


def child(extra: dict, windows: list | None = None) -> list:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", **extra})
    p = subprocess.run([sys.executable, "-B", "-c", CHILD], capture_output=True, text=True,
                       env=env, cwd=_repo.ROOT,
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-2000:]
    led = p.stdout.strip().splitlines()[-1]
    if windows is not None:
        with open(led + ".compile.json", encoding="utf-8") as fh:
            windows.extend(json.load(fh))
    return [json.loads(x) for x in open(led, encoding="utf-8") if x.strip()]


def strip(rows: list) -> list:
    out = []
    for r in mask_timings(json.loads(json.dumps(rows))):
        r = {k: v for k, v in r.items() if k not in ("seq", "t", "wall")}
        if r.get("event") in ("library", "abduce"):    # abduce carries the refusal total
            r = {**r, "detail": {k: v for k, v in r["detail"].items() if k != "refused"}}
        if r.get("event") == "budget":                 # the budget row's spent (tether.py, route)
            r = {**r, "detail": {k: v for k, v in r["detail"].items() if k != "spent"}}
        # the compile memo's size, ONE key on the end:cap memo_sizes row (the reviewer 00:18):
        # tether.py:3829 len(self._compile_cache), a pure function's memo, read only as
        # get-or-compile, so its size is work not done (refused before compiled), like spent
        if r.get("event") == "memo_sizes" and r["detail"].get("at") == "end:cap":
            r = {**r, "detail": {**r["detail"], "agent": {
                k: v for k, v in r["detail"]["agent"].items() if k != "compile"}}}
        if r.get("event") in ("header", "arms") or r.get("slot") == "@run":
            continue
        out.append(r)
    return out


def refused(rows: list) -> dict:
    tot: dict = {}
    for r in rows:
        if r.get("event") == "library":
            for k, v in (r["detail"].get("refused") or {}).items():
                tot[k] = tot.get(k, 0) + v
    return tot


def budgets(rows: list) -> list:
    return [r["detail"] for r in rows if r.get("event") == "budget"]


def compiles(rows: list) -> list:
    return [(r["detail"].get("at"), r["detail"]["agent"]["compile"]) for r in rows
            if r.get("event") == "memo_sizes"]


def p1b(on: list, off: list) -> tuple[bool, str]:
    """ON spent <= OFF spent on every cycle, ON compile <= OFF compile on every memo_sizes row
    (each its own window: the memo is cleared after it), and ON leaves no more lookups owed."""
    bo, bf = budgets(on), budgets(off)
    co, cf = compiles(on), compiles(off)
    if not bo or len(bo) != len(bf) or not co or [a for a, _ in co] != [a for a, _ in cf]:
        return False, f"budget rows ON {len(bo)} OFF {len(bf)}; memo_sizes ON {co} OFF {cf}"
    worse = [i for i, (x, y) in enumerate(zip(bo, bf, strict=True)) if x["spent"] > y["spent"]]
    c_worse = [a for (a, x), (_, y) in zip(co, cf, strict=True) if x > y]
    owed = (sum(x["owed_lookups"] for x in bo), sum(y["owed_lookups"] for y in bf))
    return (not worse and not c_worse and owed[0] <= owed[1],
            f"{len(bo)} cycles, ON spent > OFF on {len(worse)}; {len(co)} memo_sizes rows, ON "
            f"compile > OFF on {len(c_worse)} ({[x for _, x in co]} vs {[y for _, y in cf]}); "
            f"owed_lookups ON {owed[0]} OFF {owed[1]}")


def main() -> int:
    big = {"TETHER_STEP_BUDGET_N": str(10_000_000)}
    w_on, w_off = [], []
    on, off = child(big, w_on), child({**big, "TETHER_PAIR_NOT_OBJECT": "0"}, w_off)
    peak = max(d["spent"] for d in budgets(on) + budgets(off))
    assert budgets(on) and peak < 10_000_000, ("P1 occasion: the budget binds", peak)
    a, b = strip(on), strip(off)
    diff = [(i, x, y) for i, (x, y) in enumerate(zip(a, b, strict=False)) if x != y]
    assert len(a) == len(b) and not diff, (len(a), len(b), diff[:2])                     # P1
    print("P1", len(a), "rows identical ON vs OFF under a budget of 10,000,000 (peak spent",
          peak, "); library refusal counts, the budget row's spent and end:cap's agent.compile "
          "aside, timings masked")
    ok, why = p1b(on, off)
    assert ok, ("P1b under the non-binding budget", why)
    print("P1b under the non-binding budget:", why)
    # SUBSET (the reviewer 00:18): fewer compiles of the SAME conditions, per window
    assert [x for x, _ in w_on] == [x for x, _ in w_off] and w_on, (w_on[:1], w_off[:1])
    extra = [(at, sorted(set(k_on) - set(k_off))[:3]) for (at, k_on), (_, k_off)
             in zip(w_on, w_off, strict=True) if not set(k_on) <= set(k_off)]
    assert not extra, ("SUBSET: ON compiled what OFF never did", extra)
    fewer = [(at, len(k_off) - len(k_on)) for (at, k_on), (_, k_off) in zip(w_on, w_off,
                                                                             strict=True)]
    assert any(k_on for _, k_on in w_on) and any(n for _, n in fewer), ("SUBSET occasion", fewer)
    print(f"SUBSET {len(w_on)} windows: ON's compile keys within OFF's in every one; fewer per "
          f"window {fewer}")
    # MF: the aside is one key wide -- another memo_sizes.agent key, and a decision row, read red
    for name, plant in (("memo_sizes end:cap agent.reach_fold + 1",
                         lambda r: r["event"] == "memo_sizes" and r["detail"].get("at") == "end:cap"
                         and r["detail"]["agent"].__setitem__(
                             "reach_fold", r["detail"]["agent"]["reach_fold"] + 1) is None),
                        ("the first repeat row's action changed",
                         lambda r: r["event"] == "repeat" and r["detail"].__setitem__(
                             "action", str(r["detail"].get("action")) + "_X") is None)):
        mf = json.loads(json.dumps(on))
        hit = next((i for i, r in enumerate(mf) if plant(r)), None)
        assert hit is not None and strip(mf) != b, ("MF", name, hit)
        print(f"MF {name} (row {hit}) -> a difference")
    s_on, s_off = child({}), child({"TETHER_PAIR_NOT_OBJECT": "0"})
    ok, why = p1b(s_on, s_off)
    assert ok, ("P1b", why)
    print("P1b at the shipped budget:", why)
    swapped, why_s = p1b(s_off, s_on)
    assert not swapped, ("MF-SWAP: the swapped ledgers pass", why_s)
    print("MF-SWAP the ledgers swapped:", why_s, "-> fails")
    hyp = [i for i, r in enumerate(off) if r.get("event") == "goal_hypotheses"]
    assert hyp, "PRECONDITION: no goal_hypotheses row to plant in"
    planted = json.loads(json.dumps(off))
    planted[hyp[0]]["detail"]["group_n"] = (planted[hyp[0]]["detail"].get("group_n") or 0) + 1
    assert strip(planted) != a, "MF-ID: a non-timing change passed the mask"
    print(f"MF-ID group_n changed in one of {len(hyp)} goal_hypotheses rows -> a difference")
    r_on, r_off = refused(on), refused(off)
    tilde = lambda r: sum(v for k, v in r.items() if "does not parse" in k and "~" in k)  # noqa: E731
    assert r_on.get(NOT_OBJECT, 0) > 0 and tilde(r_on) == 0, (r_on.get(NOT_OBJECT), tilde(r_on))
    print("P2 ON: pairings refused as not an object name", r_on[NOT_OBJECT],
          "; parse refusals naming a pair owner", tilde(r_on))                            # P2
    assert tilde(r_off) > 0 and NOT_OBJECT not in r_off, (tilde(r_off), r_off.get(NOT_OBJECT))
    print("MF-P OFF: parse refusals naming a pair owner", tilde(r_off),
          "; evaluations ON", sum(r_on.values()), "OFF", sum(r_off.values()))           # MF-P
    print("pair_not_object: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
