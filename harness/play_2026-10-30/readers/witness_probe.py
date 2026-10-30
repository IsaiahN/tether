import sys
sys.dont_write_bytecode = True
sys.path[:0] = ["C:/TETHER_RUNS/S6_2026-10-19/FLIP/tests"]
from test_identity_short import arms_witness
b = {"on": ["a.X"], "off": ["a.Y"]}
c = {"on": ["a.X", "lineage._STORE_DB"], "off": ["a.Y"]}
for new in ([], ["lineage._NOT_AN_ARM"], ["lineage._STORE_DB"]):
    try:
        arms_witness(b, c, new, " probe")
        print("PASS", new)
    except AssertionError as e:
        print("RED", new, [x[:3] for x in e.args[0][1]])
