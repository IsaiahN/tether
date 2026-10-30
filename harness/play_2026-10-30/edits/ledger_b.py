import sys

sys.dont_write_bytecode = True
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
anchor = "- **ITEM 4 (C3), THE PARENT'S FAULT VISIBLE AT LOAD"
i = s.index(anchor)
j = s.index("\n", i) + 1
LINE = (
    "- **(B), IN-GAME RECOVERY AFTER AN AGENT FAULT (TETHER_FAULT_RECOVER, default ON; Isaiah "
    "2026-10-22 12:36-12:37; the design post 15:13, approved 15:17 with (C3), (C4); r2's cache "
    "ruled 18:20).** arc_holdout.step_or_recover at play's step and at harness/mem_store/"
    "e4_stream.py's (tether_agent.run's call is HELD with the runner items). An Exception from the "
    "agent's own code (never a BaseException, so a cut is never a fault; never one with a frame "
    "under arc_agi/ or arcengine/, re-raised as before) is item 4's agent_fault row (now with k, "
    "its number in the game, and repeat). The same fault again (fault_key: the type and the "
    "innermost repo frame; a MemoryError by its type alone, (C4)), or the switch OFF: the game "
    "ends into item 4's end path. Else: the faulted agent's end path (end_path(), lifted from "
    "play: end_run agent_fault, the checked library save, the stop-loss, the lineage generation "
    "without the faulted cycle's entries); a fresh world on the SAME ResetGuard-wrapped wrapper "
    "(world_on(): ArcWorld takes the wrapper's observation_space, so no RESET; measured: board "
    "RESETs and guard refusals [1, 0] before and after) and a fresh agent on the SAME ledger "
    "object (wire_agent(), wire()'s agent half; wire() opens a new Ledger, which truncates), "
    "loading what was written, with the harness's clock (the cycle after the faulted one, the "
    "deadline) set before its load writes a row; one \"@run\" \"fault_recovered\" row (fault, "
    "parent). The game-start fold (tether._consolidate) clears what the faulted agent left in "
    "the process's bound stores. READ APART (the reviewer 18:20 (i)): tether._INDEX_STORE, the "
    "process's compile cache, keeps the faulted agent's compiles (8 entries in the test; a cold "
    "load 0); every write to it is one assignment of a list built whole (tether.py:5810, "
    "lineage.py:1485, 1508), and r2b shows the next step equal to a cold process's. gate.py "
    "_faults refuses any agent_fault row (a recovered game still fails the gate). "
    "tests/test_fault_recover.py: a (+ the no-RESET read), b, b2, C4, c (OFF), e, r1, r2, r2b, "
    "r3 + MF (keep_faulted), r4 + MF (the old wire() path); test_gate test_agent_fault (f). "
    "(d), the identity replay on sp80, vc33 and sc25, stays owed.\n")
assert "(B), IN-GAME RECOVERY AFTER AN AGENT FAULT" not in s
nl = "\r\n" if "\r\n" in s[:2000] else "\n"
s = s[:j] + LINE.replace("\n", nl) + s[j:]
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
