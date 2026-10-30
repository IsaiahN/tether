import sys
sys.dont_write_bytecode = True
p = "c:/Users/Admin/Documents/GitHub/tether/tests/test_owed_rejudge.py"
s = open(p, encoding="utf-8", newline="").read()
pairs = [
 ("  check_a_mustfail_r281_guard     MUST-FAIL: r281's literal guard (the derived slot's OWN outstanding,\n                                  0 by construction) releases EVERY owed ask on its first\n",
  "  check_a_mustfail_r281_guard     MUST-FAIL: r281's literal guard (the derived slot's OWN\n                                  outstanding, 0 by construction) releases EVERY owed ask on its first\n"),
 ("    print(f\"  {len(rel)} released; {len(back)} raised again by a later frame, e.g. {sorted(back)[0]}\")\n",
  "    print(f\"  {len(rel)} released; {len(back)} raised again by a later frame, e.g. \"\n          f\"{sorted(back)[0]}\")\n"),
 ("    def probe(ag, new):\n        ranks = ", "    def probe(_ag, new):\n        ranks = "),
 ("                1 for r in new if r[\"event\"] == \"derived_deferred\" and r[\"detail\"][\"after\"] in plain)\n",
  "                1 for r in new\n                if r[\"event\"] == \"derived_deferred\" and r[\"detail\"][\"after\"] in plain)\n"),
]
for a, b in pairs:
    assert s.count(a) == 1, (a[:60], s.count(a))
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
