import sys
sys.dont_write_bytecode = True
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
R = [
 ("Items 5 (dcol) and 6 (zlib tests) wait on R1 and BEFORE.",
  "Item 5 (dcol): nothing to build (R1, \"not reproduced in 10 min from S3O\", your 14:27). Item 6 (the zlib tests): the tests that read a zlib generation as text (UnicodeDecodeError 0x9c: test_7lm and test_index_carry in the re-run, test_lineage_carry in read box B) decode it as the lineage does; a test-only change, built with the rest."),
 ("so a step can overrun by minutes (E4a: steps of 104-269 s on g50t, 23-113 s on ka59, against games of 518 and 370 s).",
  "so a step can overrun by minutes (E4a: single steps of up to 269 s on g50t and 113 s on ka59, in games of 518 and 370 s; R1: both games cut by the supervisor after the deadline)."),
 ("so nothing between a head and step's catch can swallow the cut. The 36 calls into other modules are not given heads (below), so a raise never crosses their own handlers.",
  "so nothing in tether.py between a head and step's catch can swallow the cut. Heads also go into 75 loops in other modules (below), and there ONE broad handler exists (interface.py:214); that is why the cut is re-based on BaseException.\n - CHECK 1 (your 13:07): bare \"except:\" and \"except BaseException\" on the step path, which would still catch a BaseException cut: 0 in tether.py (grep over the whole file), 0 in the 120 functions of the cross-module walk (its handler census listed every bare or Exception-family handler and found only interface.py:214's \"except Exception\"). Scope named: the walk does not follow calls through untyped variables."),
 ("   - Agent sets cap.AT = self.deadline at each step's start and clears it at the step's end.",
  "   - Agent sets cap.AT = its thinking deadline (the deadline minus the end-path reserve R, below) at each step's start and clears it at the step's end."),
 (" - Plus one identity fixture: a deadline never reached gives a ledger byte-equal to OFF's.",
  " - Plus one identity fixture: a deadline never reached gives a ledger byte-equal to OFF's.\n - Plus the swallow must-fail (your 13:07): a cut planted under interface.py:214's try. With CapReached on Exception (the old base) it is swallowed (_is_relational returns False and the step runs on). With BaseException it reaches step and is recorded as a cut."),
 ("  (r3) nothing carried over: a planted marker in the faulted agent's episode state (a binding, a want) is absent from the fresh agent;",
  "  (r3) nothing carried over: a planted marker in the faulted agent's episode state (a binding, a want) is absent from the fresh agent. A real must-fail (your 13:07): with the discard step disabled the marker SURVIVES and the check fires; enabled, it is gone;"),
 ("  (r4) your second check: an injected fault truncates or rewrites no earlier ledger row (the rows before the fault byte-equal before and after recovery).",
  "  (r4) your second check: an injected fault truncates or rewrites no earlier ledger row (the rows before the fault byte-equal before and after recovery). A real must-fail: the ledger reopened through the old wire() path (which truncates) FAILS the check; the split passes it."),
 (" 5 and 6 per R1 and BEFORE.",
  " 6: the zlib tests (5 has nothing to build)."),
]
for a, b in R:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("applied", len(R))
