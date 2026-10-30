import sys
sys.dont_write_bytecode = True
p = "c:/Users/Admin/Documents/GitHub/tether/tether.py"
s = open(p, encoding="utf-8", newline="").read()
pairs = [("        if b2 is not None and _OWED_REJUDGE:\n", "        if _OWED_REJUDGE:\n"),
         ("            if _STEP_MINT and _OWED_REJUDGE:\n", "            if _OWED_REJUDGE:\n"),
         ("# derived asks (rank 0) after them by A1 -- never owed-first or code order. Needs\n# TETHER_STEP_DERIVED. ON; conform/arms.py",
          "# derived asks (rank 0) after them by A1 -- never owed-first or code order. The releases\n# need TETHER_STEP_DERIVED (asks are owed only under it). ON; conform/arms.py")]
nl = "\r\n" if "\r\n" in s else "\n"
for a, b in pairs:
    a, b = a.replace("\n", nl), b.replace("\n", nl)
    assert s.count(a) == 1, (a[:60], s.count(a))
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
