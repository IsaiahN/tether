import sys

sys.dont_write_bytecode = True
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
anchor = "- **C1 (A), THE OVERRUN SAFETY NET, SINGLE AGENT"
i = s.index(anchor)
j = s.index("\n", i) + 1
LINES = (
    "- **ITEM 4, THE LEARNING WRITTEN ON AN AGENT FAULT (TETHER_ERROR_CARRY, default ON; the design "
    "post 2026-10-22 15:14, the reviewer 15:17 (C3), 16:35).** arc_holdout.play catches an Exception from "
    "ag.step(). A traceback with a frame inside arc_agi/ or arcengine/ is the game's, not ours, and is "
    "re-raised at once as before (note_fault). Otherwise: one \"@run\" \"agent_fault\" row (type, "
    "message, the innermost repo frame, the cycle) and the whole traceback beside the ledger "
    "(<ledger>.fault<k>.txt); the loop ends into the end path, each part guarded (a failure is a "
    "\"carry_refused\" row, never a second raise); end_run(ledger.AGENT_FAULT) (tether._TERM_KIND maps it "
    "to \"cap\": read at the code, an unknown word would set Termination's bounded_seen and teach the "
    "agent the world is bounded); the library (when play was given one) replaced only by a save that "
    "loads back into a fresh Gamma (checked_save); the lineage generation marked \"ended\": "
    "\"agent_fault\" with the error, WITHOUT the faulted cycle's own stamped entries ((C3): a term whose "
    "residual is stamped \"@<cycle>\", an invention born in it -- never deleted, never carried), and "
    "written only if lineage._readback passes (the stored bytes decompress to the same bytes, the same "
    "name hash, the same record -- it shows the bytes decode to what was built, not that a step cut "
    "halfway left the library consistent); then the fault re-raised, so game_one records the error as "
    "before. UNSTAMPED, so written as built: kind episodes and the counters. tether_agent.py (the Kaggle "
    "loop) is NOT touched: its catch is the held runner item 4b. tests/test_fault_carry.py: F1, C3, RB, "
    "OFF.\n"
    "- **THE FIRST SEAT EDIT UNDER library/ (2026-10-22; accepted by the reviewer 16:35, no revert).** "
    "1d4c4c8 edited library/library_runtime.py directly: a guarded import of cap.head as _cap_head "
    "(lines 59-63: a no-op when the library is read alone) and 8 heads (lines 349, 351, 361, 375, 379, "
    "400, 403, 405: Library.light, Library.produces, Library.molecules_lit), C1 (A)'s census work. Every "
    "earlier change to that file came as a reviewer package placed by Isaiah (v4 8afeb0e, v5 0fd55fa, "
    "v6 e48ec3b, v7 89c6049, v9.1 6b2e2e0); the standing rule was that the seat does not edit library/. "
    "The change is code, not library content. Its consequence, read by the line: library_runtime.py is "
    "in instruments.Attribution.LIBRARY_FILES, so library_sha and library_blob change; their only readers "
    "are the @run header (written, \"nothing reads this to decide\"), harness/log_index.py (an index "
    "field) and conform/arms.py (named); the lineage load checks compile_term.signature(atoms), not the "
    "library's source, so a load from the S3O point is unaffected (no re-index, rebuild or refusal). For "
    "the Kaggle step: the bundle ships library/ whole, so its library_sha changes too (beside K7).\n")
assert "ITEM 4, THE LEARNING WRITTEN ON AN AGENT FAULT" not in s
s = s[:j] + LINES + s[j:]
with open(p, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(s)
print("ok")
