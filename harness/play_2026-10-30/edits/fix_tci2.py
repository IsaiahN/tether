import sys

sys.dont_write_bytecode = True
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
R = [
    ('''PHASES = [("P1", "_present"), ("P2", "note_goals"), ("P5", "choose"), ("P7", "route"),
          ("P8", "_d5_splits"), ("P10", "_event_prices"), ("P12", "settle"),
          ("P14", "_settle_routine"), ("P15", "indistinguishable")]
PRESSED_FROM = {"P7", "P8", "P10", "P12", "P14", "P15"}''',
     '''PHASES = [("P0", "_size_fold", 8), ("P1", "_present", 8), ("P2", "note_goals", 8),
          ("P5", "choose", 8), ("P6", "_utter", 8), ("P7", "route", 8), ("P8", "_d5_splits", 8),
          ("P10", "_event_prices", 8), ("P11", "_flush_probe", 24), ("P12", "settle", 8),
          ("P14", "_settle_routine", 8), ("P15", "indistinguishable", 8)]
PRESSED_FROM = {"P7", "P8", "P10", "P11", "P12", "P14", "P15"}'''),
    ('''out = None
for _ in range(8):
    n0 = len(ag.led)''',
     '''out = None
for _ in range(int(sys.argv[3])):
    n0 = len(ag.led)'''),
    ('''        out = {"fired": fired[0], "acted": acted, "cut": ag._cut,''',
     '''        out = {"fired": fired[0], "acted": acted, "cut": ag._cut,
               "ruin_on": tether._RUIN_RECORD, "ruin": repr(ag._ruin_step),'''),
    ('''    for ph, fn in PHASES:
        r = run_child(PH_CHILD, fn)
        assert r is not None, f"PH {ph}: precondition: {fn} was never entered in 8 steps"''',
     '''    for ph, fn, n in PHASES:
        r = run_child(PH_CHILD, fn, str(n))
        assert r is not None, f"PH {ph}: precondition: {fn} was never entered in {n} steps"'''),
    ('''        assert c["acted"] == (ph in PRESSED_FROM), (ph, "acted", c)''',
     '''        assert c["acted"] == (ph in PRESSED_FROM), (ph, "acted", c)
        if c["acted"] and r["ruin_on"]:      # RS-15:40: a cut after the press keeps the press's key
            assert r["ruin"] != "None", (ph, "ruin-step: the press's key is lost", r)'''),
    ('''        print(f"  PH {ph} {fn}: cut at {c['site']} (at {c['at']}, acted {c['acted']}); AC ok")''',
     '''        ruin = f"; ruin key kept {r['ruin'][:40]}" if c["acted"] else ""
        print(f"  PH {ph} {fn}: cut at {c['site']} (at {c['at']}, acted {c['acted']}); AC ok{ruin}")'''),
    ('''    r = run_child(PH_CHILD, "note_goals", TETHER_CAP_INNER="0")''',
     '''    r = run_child(PH_CHILD, "note_goals", "8", TETHER_CAP_INNER="0")'''),
]
for a, b in R:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
with open(p, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(s)
print("ok")
