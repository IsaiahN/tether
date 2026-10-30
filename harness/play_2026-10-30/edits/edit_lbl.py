import sys
sys.dont_write_bytecode = True
R = "c:/Users/Admin/Documents/GitHub/tether/tests/"
edits = {
 "test_step_mint.py": ("def check_a_one_exhausting_mint_then_owed_first() -> None:\n",
   "def check_a_one_exhausting_mint_then_owed_first() -> None:\n"
   "    \"\"\"OFF path: owed first, 1d OFF (TETHER_OWED_REJUDGE=0). ON, the step's mints go by\n"
   "    _understanding: test_owed_rejudge check_h_on_first_mint_by_rank.\"\"\"\n"),
 "test_step_derived.py": ("def check_e_owed_derived_slot_asked_first_next_step() -> None:\n",
   "def check_e_owed_derived_slot_asked_first_next_step() -> None:\n"
   "    \"\"\"OFF path: owed first, 1d OFF (TETHER_OWED_REJUDGE=0). ON, owed and fresh asks go by\n"
   "    A1: test_owed_rejudge check_i_on_derived_a1_order.\"\"\"\n"),
}
for f, (a, b) in edits.items():
    p = R + f
    s = open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in s else "\n"
    a, b = a.replace("\n", nl), b.replace("\n", nl)
    assert s.count(a) == 1, (f, s.count(a))
    s = s.replace(a, b)
    open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
