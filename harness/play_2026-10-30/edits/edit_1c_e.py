import sys
sys.dont_write_bytecode = True
p = "c:/Users/Admin/Documents/GitHub/tether/tether.py"
s = open(p, encoding="utf-8", newline="").read()
for a, b in [("# 1c: (slot, term) -> the space key of its latest risky settle", "# 1c: (slot, term) -> the key of its last risky settle"),
             ("# 1c (iii): gap -> the owner's readings when the probe pressed", "# 1c (iii): gap -> owner readings at the probe's press"),
             ("# 1c: slot -> the stop rule it is in (held / broken)", "# 1c: slot -> the stop rule it is in (held / none_survive)")]:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
