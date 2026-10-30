"""The red's cause, read on the 1c tree (argv: repo root): check_s1_mustfail_reprice's setup, then the
memo's state for the gap, then the stubbed read with the memo kept vs cleared."""
import sys

sys.dont_write_bytecode = True
root = sys.argv[1]
sys.path[:0] = [root, root + "/tests"]
import test_ask as T  # noqa: E402

ag, s, _held, robs, behind = T._stale_gap()
stored = ag._s1_of(*ag._space_bounds(s, "stale"))
memo = ag._reprice_memo.get(s)
kept = sum(1 for t, c in behind if memo and memo[1].get(t) is not None and memo[1][t][0] is c
           and memo[1][t][1] == len(robs))
print("gap", s, "rows", len(robs), "behind", len(behind), "stored S1", len(stored),
      "| memo kept at this length for", kept, "of the behind cells")
ag._row_wrong = lambda _t, _s, _row: False
print("stubbed, memo kept: S1", len(ag._survivors(s)))
ag._reprice_memo = {}
print("stubbed, memo cleared: S1", len(ag._survivors(s)), "(stored", len(stored), ")")
