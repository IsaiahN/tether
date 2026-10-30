import sys

sys.dont_write_bytecode = True
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
anchor = "- **THE FIRST SEAT EDIT UNDER library/"
i = s.index(anchor)
j = s.index("\n", i) + 1
LINE = (
    "- **ITEM 4 (C3), THE PARENT'S FAULT VISIBLE AT LOAD (the reviewer 2026-10-22 15:17 (C3); "
    "accepted 17:27).** lineage_store.merge_save writes meta 'ended' = {h, ended, error} when the "
    "merged generation carries \"ended\"; keyed by the save's hash, it is trusted only while that "
    "hash is the tip, so nothing ever clears it and a later normal generation is never mislabelled. "
    "lineage._note_parent_ended (gated on TETHER_ERROR_CARRY) writes one \"@lineage\" IMPORT "
    "\"parent_ended\" row (parent, ended, error) on both load paths: the store's (the meta read "
    "after catch_up) and the chain's (the tip generation's own \"ended\"). "
    "tests/test_fault_carry.py PE, on the store path and the chain path (TETHER_MEMORY_STORE=0): "
    "the play's load over normal parents 0 rows (the control), the fresh load over the faulted tip "
    "exactly 1, and one normal game later 0 (the stale-mark must-fail). C3's invention plant now "
    "takes a real template (as _inv_conditions builds one) and is re-invented at the fresh load; "
    "C3-BAD keeps a malformed one ({r} unfilled), refused WITH its why in the invention_carried "
    "row (library_runtime.invent_atom: \"the condition names no reading\").\n")
assert "ITEM 4 (C3), THE PARENT'S FAULT VISIBLE AT LOAD" not in s
nl = "\r\n" if "\r\n" in s[:2000] else "\n"
s = s[:j] + LINE.replace("\n", nl) + s[j:]
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
