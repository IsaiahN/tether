"""ALPHA-LAST (TETHER_ALPHA_LAST; the reviewer 2026-10-18 19:47, 20:02; E4a g50t, ka59). The
fake ARC game, C-seed-X.

  MF   a slot with history is dropped from the CURRENT alphabet (a departure) and priced as
       sweep prices it (_left over its history). Arm OFF: KeyError. Arm ON: no raise, and the
       value equals the one computed before the drop. A slot never seen still raises with the
       arm ON
  ID   a short same-seed run, arm ON vs OFF: every ledger row but the arm-state header is
       identical in sequence (no departed-slot read occurs in it, so nothing may differ), with
       the timings masked by the shared list (conform/identity_mod_rows.TIMINGS, imported)
  MF-ID a non-timing field changed in one row (goal_hypotheses' checked, beside wall_s) is still
       a difference after the mask

    python tests/test_alpha_last.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
HERE = _repo.ROOT
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "conform"))
from identity_mod_rows import mask_timings  # noqa: E402

CHILD = r'''
import os, sys, tempfile
sys.dont_write_bytecode = True
import tether, tether_agent
from test_entry import FakeWrapper
led = os.path.join(tempfile.mkdtemp(), "r.jsonl")
tether_agent.run(FakeWrapper(script={}), "fake", max_actions=12, led_path=led)
print(led)
'''


def child(on: bool) -> list[dict]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "TETHER_AGENT_SEED": "0",
                "TETHER_ALPHA_LAST": "1" if on else "0"})
    p = subprocess.run([sys.executable, "-B", "-c", CHILD], capture_output=True, text=True, env=env,
                       cwd=HERE, stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-2000:]
    led = p.stdout.strip().splitlines()[-1]
    with open(led, encoding="utf-8") as fh:
        rows = [json.loads(x) for x in fh if x.strip()]
    return [r for r in rows if r.get("event") not in ("header", "arms")]


def same(a: list[dict], b: list[dict]) -> tuple[bool, object]:
    """Equal row for row once the shared timings are masked, else the first difference."""
    a, b = (mask_timings(json.loads(json.dumps(x))) for x in (a, b))
    da, db = ([json.dumps(r, sort_keys=True) for r in x] for x in (a, b))
    return da == db, next(((i, x, y) for i, (x, y) in enumerate(zip(da, db, strict=False))
                           if x != y), (len(da), len(db)))


def main() -> int:
    import arc_holdout
    import tether
    from test_entry import FakeWrapper
    tether._AGENT_SEED = False
    env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake")
    for _ in range(6):
        env.observe()
        ag.step()
    cands = [s for s in ag.slots if ag.history(s) and s in ag.alphabet]
    assert cands, "precondition: no slot with history"
    s = cands[0]
    hist = ag.history(s)
    term = ag.gamma.library[ag.bound.get(s, tether.IDN)]
    v0 = ag._left(term, s, hist)
    cur = {k: v for k, v in ag.alphabet.items() if k != s}       # the refresh after s departed
    ag.alphabet = ag._with_last(cur)
    assert s not in ag.alphabet, "the departure did not drop the slot from the current alphabet"
    v1 = ag._left(term, s, hist)
    assert v1 == v0, (v0, v1)
    try:
        ag.alphabet["never.seen"]
    except KeyError:
        pass
    else:
        raise AssertionError("a slot never seen did not raise with the arm ON")
    print(f"  MF ON: {s} departed, _left over {len(hist)} history rows = {v1} "
          f"(before the drop {v0}); a never-seen slot still raises")
    tether._ALPHA_LAST = False
    ag.alphabet = ag._with_last(cur)
    try:
        ag._left(term, s, hist)
    except KeyError as e:
        print(f"  MF OFF: KeyError {e} (today's crash)")
    else:
        raise AssertionError("MF did not fail: the arm OFF priced a departed slot")
    on, off = child(True), child(False)
    ok, diff = same(on, off)
    assert ok, diff
    print(f"  ID: {len(on)} ledger rows identical, arm ON vs OFF (same seed; timings masked)")
    hyp = [i for i, r in enumerate(off) if r["event"] == "goal_hypotheses"]
    assert hyp, "PRECONDITION: no goal_hypotheses row to plant in"
    planted = json.loads(json.dumps(off))
    planted[hyp[0]]["detail"]["checked"] = planted[hyp[0]]["detail"].get("checked", 0) + 1
    assert not same(on, planted)[0], "MF-ID: a non-timing change passed the mask"
    print(f"  MF-ID: goal_hypotheses' checked changed in one of {len(hyp)} such rows -> a "
          "difference after the mask")
    print("alpha_last: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
