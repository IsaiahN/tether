"""W-1 THE BUDGET + W-2 THE CACHES (TETHER_W_BUDGET, TETHER_W_CACHES; the reviewer 2026-10-22
05:14).
The fake ARC game, C-seed-X.

  W5   B is the machine's: min(8 GiB, half the RAM) in the @run header; a planted RAM figure
       (TETHER_W_RAM_BYTES) moves it (MF-W5)
  WS   SOFT, commit past 0.75 B at a step's start: CONSOLIDATION folds and each cache keeps the
       entries read since the last fold and drops the rest; the same commit again folds nothing
       (held back, counted); below the line nothing
  WH   HARD, commit past 0.90 B at a between-lookup point (_cap_due): every cache emptied, once
       per commit high
  W2   MF-W2: evicting every cache at every step (TETHER_W_EVICT_EVERY_STEP) leaves the run's
       ledger equal to a run that never evicts (identity_mod_rows.compare, the fold fields
       masked), with evictions that removed entries (the precondition)
  W3   MF-W3: a planted cache whose miss writes a row makes that same comparison FAIL
  OFF  TETHER_W_BUDGET off: the old size trigger (half the supervisor ceiling) and no eviction

    python tests/test_w12.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
HERE = _repo.ROOT
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "conform"))
from identity_mod_rows import compare, mask_folds  # noqa: E402  the one identity reader

CHILD = r'''
import json, os, sys, tempfile
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
sys.path.insert(1, os.path.join(sys.argv[1], "tests"))
import tether, tether_agent
from test_entry import FakeWrapper
tether._AGENT_SEED = False
if sys.argv[3] == "plant":
    real = tether.Agent._lib_view
    def planted(self, lib, key, role, o, x):
        if (key, role) not in self._view_hold:
            self.led.record(self.cycle, self._running_step, "@w", "planted_miss", entry=key)
        return real(self, lib, key, role, o, x)
    tether.Agent._lib_view = planted
led = os.path.join(tempfile.mkdtemp(), "r.jsonl")
tether_agent.run(FakeWrapper(script={}), "fake", max_actions=int(sys.argv[2]), led_path=led)
print(led)
'''


def _run(evict: bool, plant: bool, n: int = 12) -> tuple[list[dict], list[dict]]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")
    if evict:
        env["TETHER_W_EVICT_EVERY_STEP"] = "1"
    p = subprocess.run([sys.executable, "-B", "-c", CHILD, HERE, str(n), "plant" if plant else "-"],
                       capture_output=True, text=True, env=env, cwd=HERE, stdin=subprocess.DEVNULL,
                       timeout=600)
    assert p.returncode == 0, p.stderr[-2000:]
    led = p.stdout.strip().splitlines()[-1]
    with open(led, encoding="utf-8") as fh:
        rows = [json.loads(x) for x in fh if x.strip()]
    for r in rows:      # the arm lists differ by the check switch itself
        if r["slot"] == "@run" and r["event"] == "arms":
            r["detail"].pop("on", None)
            r["detail"].pop("off", None)
    body = []
    if os.path.exists(led + ".body.jsonl"):
        with open(led + ".body.jsonl", encoding="utf-8") as fh:
            body = [json.loads(x) for x in fh if x.strip()]
    return rows, body


def agent():
    import arc_holdout
    import tether
    from test_entry import FakeWrapper
    tether._AGENT_SEED = False
    env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake")
    return tether, env, ag


def main() -> int:
    import tether
    _, _, ag = agent()
    hdr = next(r for r in ag.led.rows() if r["slot"] == "@run" and r["event"] == "arms")
    ram = tether._ram_bytes()
    assert ram and ram > 0, ram
    assert hdr["detail"]["budget_bytes"] == min(8 * 2**30, ram // 2) == ag._w_budget, hdr["detail"]
    assert hdr["detail"]["ram_bytes"] == ram
    os.environ["TETHER_W_RAM_BYTES"] = str(3 * 2**30)
    try:
        _, _, ag2 = agent()
    finally:
        del os.environ["TETHER_W_RAM_BYTES"]
    h2 = next(r for r in ag2.led.rows() if r["slot"] == "@run" and r["event"] == "arms")
    assert h2["detail"]["budget_bytes"] == 3 * 2**29 and h2["detail"]["ram_bytes"] == 3 * 2**30
    print(f"  W5: B = {ag._w_budget / 2**30:.2f} GiB from {ram / 2**30:.2f} GiB of RAM, in the "
          f"@run header; a planted 3 GiB moves it to 1.50 GiB")

    real = tether._commit_bytes
    now = [0]
    tether._commit_bytes = lambda: now[0]
    try:
        B = ag._w_budget
        folds = []
        real_cons = ag._consolidate
        ag._consolidate = lambda trig: folds.append(trig)
        ag._named_split["read"] = 1
        ag._named_split["unread"] = 2
        ag._view_hold["v"] = 3
        for c in (ag._named_split, ag._view_hold):
            c.seen = set()
        _ = ag._named_split.get("read")
        now[0] = 3 * B // 4 - 1
        ag._size_fold()
        assert not folds and "unread" in ag._named_split, "below the soft line nothing folds"
        now[0] = 3 * B // 4 + 1
        ag._size_fold()
        assert folds == ["size"], folds
        assert "read" in ag._named_split and "unread" not in ag._named_split
        assert "v" not in ag._view_hold
        sup = ag._fold_suppressed
        ag._size_fold()
        assert folds == ["size"] and ag._fold_suppressed == sup + 1
        print("  WS: soft fold past 0.75 B: consolidated once, the read entry kept, the unread "
              "ones dropped; the same commit again held back (counted); below it nothing")
        ag._named_split["a"] = 1
        ag._compile_cache["b"] = 2
        _PT = tether._PAIR_TALLY
        _PT["c"] = 3
        now[0] = 9 * B // 10 + 1
        ag._cap_due()
        assert not ag._named_split and not ag._compile_cache and not _PT
        ag._named_split["a"] = 1
        ag._cap_due()
        assert "a" in ag._named_split, "the same commit again: no second hard fold"
        ev = [b for b in ag._body_rows if b.get("event") == "w_evict"]
        assert [b["why"] for b in ev] == ["soft", "hard"], [b["why"] for b in ev]
        print("  WH: hard fold past 0.90 B at a between-lookup point: every cache emptied, once "
              "per commit high; both evictions in @body, none in the ledger")
        assert not [r for r in ag.led.rows() if r["event"] == "w_evict"]
        ag._consolidate = real_cons
        tether._W_BUDGET = False
        folds.clear()
        ag._consolidate = lambda trig: folds.append(trig)
        ag._fold_last_commit = None
        os.environ["TETHER_CONSOLIDATE_CEILING"] = str(4 * B)
        try:
            ag._size_fold()
        finally:
            del os.environ["TETHER_CONSOLIDATE_CEILING"]
        assert not folds, "OFF: 0.75 B is under half of a ceiling of 4 B, so no fold"
        print("  OFF: the old trigger reads half the supervisor ceiling (no fold at 0.75 B of a "
              "4 B ceiling)")
        tether._W_BUDGET = True
    finally:
        tether._commit_bytes = real

    base, _ = _run(evict=False, plant=False)
    ev, body = _run(evict=True, plant=False)
    gone = sum(sum(b["evicted"].values()) for b in body if b.get("event") == "w_evict")
    steps_ev = sum(1 for b in body if b.get("event") == "w_evict")
    assert steps_ev > 0 and gone > 0, ("PRECONDITION: no eviction removed anything", steps_ev,
                                       gone)
    a, b = mask_folds(base), mask_folds(ev)
    bad = compare(a, b, set())
    assert not bad, bad[:3]
    print(f"  W2: every cache evicted at each of {steps_ev} steps ({gone} entries removed): the "
          f"ledger equals the run that never evicts, {len(b)} rows (compare, fold fields masked)")

    pa, _ = _run(evict=False, plant=True)
    pb, _ = _run(evict=True, plant=True)
    bad = compare(mask_folds(pa), mask_folds(pb), set())
    assert bad, "MF-W3: a planted cache whose miss writes a row was not caught"
    print(f"  W3: a planted miss that writes a row: the comparison FAILS ({bad[0][:80]})")
    print("w12: OK")
    return 0


if __name__ == "__main__":
    tempfile.tempdir = tempfile.mkdtemp(prefix="w12_")
    sys.exit(main())
