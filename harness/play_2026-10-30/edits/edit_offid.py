import sys
sys.dont_write_bytecode = True
R = "c:/Users/Admin/Documents/GitHub/tether/tests/"
for f, a, b in [
 ("test_ask.py", '    cur = _norm(_child(root, w, {"TETHER_ASK": "0"}))\n',
  '    # the batch\'s later arms off too (1d, 1c), so the tree reads as it stood before this arm\n'
  '    cur = _norm(_child(root, w, {"TETHER_ASK": "0", "TETHER_OWED_REJUDGE": "0",\n'
  '                                 "TETHER_STOP_RULES": "0"}))\n'),
 ("test_owed_rejudge.py", '    cur = _norm(_child(root, w, {"TETHER_OWED_REJUDGE": "0"}))\n',
  '    # the batch\'s later arm off too (1c), so the tree reads as it stood before this arm\n'
  '    cur = _norm(_child(root, w, {"TETHER_OWED_REJUDGE": "0", "TETHER_STOP_RULES": "0"}))\n'),
]:
    p = R + f
    s = open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in s else "\n"
    a2, b2 = a.replace("\n", nl), b.replace("\n", nl)
    assert s.count(a2) == 1, (f, s.count(a2))
    open(p, "w", encoding="utf-8", newline="").write(s.replace(a2, b2))
print("ok")
