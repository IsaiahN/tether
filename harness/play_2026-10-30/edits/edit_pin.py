"""Pin TETHER_OWED_REJUDGE off in the two checks that assert B1/B2's owed-first order (1d retires it)."""
import sys
sys.dont_write_bytecode = True
R = "c:/Users/Admin/Documents/GitHub/tether/tests/"
edits = {
    "test_step_mint.py": [
        ("    keep = tether._STEP_MINT\n    try:\n        tether._STEP_MINT = True\n",
         "    keep, keep_r = tether._STEP_MINT, tether._OWED_REJUDGE\n    try:\n        tether._STEP_MINT = True\n"
         "        tether._OWED_REJUDGE = False     # B1's owed-first order; 1d (r281) replaces it by rank\n"),
        ("        assert second and second[0] in three[1:], second      # an owed slot is minted first\n"
         "    finally:\n        tether._STEP_MINT = keep\n",
         "        assert second and second[0] in three[1:], second      # an owed slot is minted first\n"
         "    finally:\n        tether._STEP_MINT, tether._OWED_REJUDGE = keep, keep_r\n"),
    ],
    "test_step_derived.py": [
        ("def check_e_owed_derived_slot_asked_first_next_step() -> None:\n    rows = _run(True, budget=40).led.rows()\n",
         "def check_e_owed_derived_slot_asked_first_next_step() -> None:\n"
         "    keep = tether._OWED_REJUDGE\n"
         "    tether._OWED_REJUDGE = False     # B2's owed-first order; 1d (r281) replaces it by A1\n"
         "    try:\n        rows = _run(True, budget=40).led.rows()\n    finally:\n"
         "        tether._OWED_REJUDGE = keep\n"),
    ],
}
for f, pairs in edits.items():
    p = R + f
    s = open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in s else "\n"
    for a, b in pairs:
        a, b = a.replace("\n", nl), b.replace("\n", nl)
        assert s.count(a) == 1, (f, a[:70], s.count(a))
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
