import sys
sys.dont_write_bytecode = True
p = "c:/Users/Admin/Documents/GitHub/tether/tests/test_stop_rules.py"
s = open(p, encoding="utf-8", newline="").read()
for a, b in [
 ('"""1c STOP_RULES (TETHER_STOP_RULES, default ON; the reviewer 2026-10-29 r325, r327, r337, r338). On a\nstepped',
  '"""1c STOP_RULES (TETHER_STOP_RULES, default ON; the reviewer 2026-10-29 r325, r327, r337, r338).\nOn a stepped'),
 ("  check_i_mustfail_old_key        MUST-FAIL (r338): the risky settle predates the current key: no stop\n",
  "  check_i_mustfail_old_key        MUST-FAIL (r338): the risky settle predates the current key:\n                                  no stop\n"),
 ('  check_ii_none_survive           survivors, then none, on a current key: "none_survive", and the slot\n                                  owes (owed_import)\n',
  '  check_ii_none_survive           survivors, then none, on a current key: "none_survive", and the\n                                  slot owes (owed_import)\n'),
 ("  check_iii_mustfail_no_spend     MUST-FAIL: with no press, the unmoved owner's aim stays for K steps\n",
  "  check_iii_mustfail_no_spend     MUST-FAIL: with no press, the unmoved owner's aim stays K steps\n"),
]:
    assert s.count(a) == 1, a[:50]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
