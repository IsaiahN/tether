"""Fill the Q16-Q25 draft's placeholders from files and literals. argv: draft table out"""
import sys

d = open(sys.argv[1], encoding="utf-8").read()
table = open(sys.argv[2], encoding="utf-8").read().split("planning 0 in")[0].rstrip("\n")
q21 = (" - Lookups: ROUTE \"library\" rows 2,093 in E4a, of which 905 carry \"unreached\" (43.2%): a lookup that did not reach,"
       " recorded as such.\n"
       " - Indistinct: \"indistinct\" rows 195, of which 85 carry \"unreached\" (43.6%).\n"
       " - Invention: 1,233 \"invent\" rows, park verdict \"budget_spent\" on 1,233 (100.0%): every invention search ended"
       " as unreachable at its budget, never as absent (Fig 8 :40-42 honoured there).\n"
       " - A reach verdict carried once: contradiction_routed (ar25 c4) remedy verdict \"unreached\", closure 4, composable 0.")
for k, v in (("__TIME__", "11:16"), ("__UTC__", "16:16:03Z"), ("__MIN__", "10+"), ("__TABLE__", table), ("__Q21__", q21)):
    assert d.count(k) == 1, k
    d = d.replace(k, v)
open(sys.argv[3], "w", encoding="utf-8", newline="\n").write(d)
print(len(d))
