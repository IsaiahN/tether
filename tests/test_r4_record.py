"""THE R4 RECORD (TETHER_R4_RECORD, default ON; the reviewer 2026-10-23 18:19, 18:28, 18:37,
18:43, 19:10, 19:52). The must-fail the reviewer ruled at 18:43: the same world and seed with the
arm ON and OFF.
  OCCASIONS  each addition carries a non-empty value at least once ON (tests_read_by, None by
             design, by presence), a realisation carries table evidence ("tier") at least once,
             and none appears OFF
  NO CARRY   a REPEAT row whose exit took no realisation reads realised None even when the row
             before it had one (the reset at choose's top, tether.py's choose), at least once
  DECISIONS  conform/identity_mod_rows.compare(OFF, ON): the "audit" rows dropped, the seven added
             fields named, every position field mapped through the row shift; any other difference
             fails (the chosen action, the intent, the withheld rows and the bet values are rows of
             the ledger, so all are compared). The arms row's on/off lists differ by the switch
             itself and are removed, as test_cap_inner does
  UNTESTED   completion_sweep.segment_rows: the fake world never completes (occasions 0 here);
             identity_mod_rows counts it as a COUNT, with its own must-fail
    python tests/test_r4_record.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.path.insert(0, os.path.join(str(_repo.ROOT), "conform"))
from identity_mod_rows import compare  # noqa: E402  the one identity reader

sys.dont_write_bytecode = True

STEPS = 30
ADDED_ROWS = {"audit"}
ADDED_FIELDS = {"repeat": ("offered", "withheld", "realised"),
                "goal_hypotheses": ("self_moving",),
                "goal_series": ("span",),
                "goal_hypothesis_end": ("tests", "tests_read_by")}

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
tree, steps = sys.argv[1], int(sys.argv[2])
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import arc_holdout
from test_entry import FakeWrapper
env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
for _ in range(steps):
    ag.step()
print(json.dumps({"rows": ag.led.rows()}, default=str))
'''


def child(arm: str) -> list:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               TETHER_R4_RECORD=arm)
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, str(_repo.ROOT), str(STEPS)],
                         env=env, capture_output=True, text=True, timeout=1800,
                         cwd=str(_repo.ROOT), stdin=subprocess.DEVNULL)
    assert out.returncode == 0, out.stderr[-3000:]
    rows = json.loads(out.stdout.strip().splitlines()[-1])["rows"]
    for r in rows:      # the arm lists differ by the switch itself
        if r["slot"] == "@run" and r["event"] == "arms":
            r["detail"].pop("on", None)
            r["detail"].pop("off", None)
    return rows


def main() -> None:
    on, off = child("1"), child("0")
    # OCCASIONS first: each addition is present ON and absent OFF
    # counted by VALUE, not presence (the reviewer 20:38): a field written empty is no occasion;
    # tests_read_by is the reader flag, None by design, so it is counted by presence
    seen = {e: sum(1 for r in on if r["event"] == e) for e in ADDED_ROWS}
    first: dict = {}
    for ev, fields in ADDED_FIELDS.items():
        for f in fields:
            key = f"{ev}.{f}"
            if f == "tests_read_by":
                seen[key] = sum(1 for r in on if r["event"] == ev and f in r["detail"])
                continue
            vals = [r["detail"][f] for r in on if r["event"] == ev
                    and r["detail"].get(f) not in (None, {}, [], "")]
            seen[key] = len(vals)
            first[key] = vals[0] if vals else None
    real = [r["detail"].get("realised") for r in on if r["event"] == "repeat"]
    tiers = [v for v in real if isinstance(v, dict) and "tier" in v]
    seen["repeat.realised.tier"] = len(tiers)
    first["repeat.realised.tier"] = tiers[0] if tiers else None
    print("  occasions ON (non-empty values):", json.dumps(seen, sort_keys=True))
    for k in sorted(first):
        print(f"    first {k}: {json.dumps(first[k], default=str)[:200]}")
    missing = sorted(k for k, n in seen.items() if not n)
    assert not missing, ("R4 occasion: an addition never carried a value ON", missing)
    rep = [r["detail"] for r in on if r["event"] == "repeat"]
    carry = sum(1 for p, r in zip(rep, rep[1:], strict=False)
                if p.get("realised") is not None and r.get("realised") is None)
    print(f"  NO CARRY: {carry} REPEAT rows read realised None right after a row that had one")
    assert carry, "R4 occasion: no REPEAT row without a realisation follows one with it"
    assert not any(r["event"] in ADDED_ROWS for r in off), "R4 OFF: an added row"
    assert not any(f in r["detail"] for r in off for f in ADDED_FIELDS.get(r["event"], ())), (
        "R4 OFF: an added field")
    # DECISIONS: the one identity reader, every difference listed; empty is the pass
    named = {f"{ev}:{f}" for ev, fields in ADDED_FIELDS.items() for f in fields}
    bad = compare(off, on, ADDED_ROWS, named)
    print(f"  identity_mod_rows.compare(OFF, ON, drop {sorted(ADDED_ROWS)}, {len(named)} named "
          f"fields): {len(bad)} difference(s)" + "".join(f"\n    {b}" for b in bad))
    assert len(off) > 50 and not bad, ("R4: the arm changed a decision or a row", len(bad))
    acts = [r["detail"].get("action") for r in on if r["event"] == "repeat"]
    assert acts == [r["detail"].get("action") for r in off if r["event"] == "repeat"], "actions"
    print(f"  DECISIONS: {len(off)} OFF rows, {len(on)} ON ({len(on) - len(off)} added); actions "
          f"{len(acts)} cycles, identical. completion_sweep.segment_rows UNTESTED here (occasions "
          f"{sum(1 for r in on if r['event'] == 'completion_sweep')})")
    print("r4_record: OK")


if __name__ == "__main__":
    main()
