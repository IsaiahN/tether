import sys

sys.dont_write_bytecode = True
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
a0 = s.index("def atomic() -> None:")
a1 = s.index("def ruin_gap() -> None:")
NEW = '''def atomic() -> None:
    import cap
    import diagnose
    rows = [(0, {"o1.x": 1}, "A", {"o1.x": 1}, None, None),
            (1, {"o1.x": 1}, "A", {"o1.x": 2}, None, None),
            (2, {"o1.x": 2}, "A", {"o1.x": 3}, None, None)]

    def state(hz):
        return json.dumps([hz.near, hz.away, hz.world], sort_keys=True, default=dict)

    def run(fn, at_entry):
        hz = diagnose.Hazard()
        real = hz.credited

        def credited(a, m):
            cap.head()                    # a callee reaching a head, as _left does in play
            return real(a, m)

        def predicts(r):
            cap.AT = 0.0                  # the deadline passes inside the diagnosis
            return r[0] == 0
        hz.credited = credited
        before = state(hz)
        cap.AT = 0.0 if at_entry else None
        try:
            fn(rows, "o1.x", "o1", persists=True, predicts=predicts,
               predicts_with=lambda _r, _a: False, alt_predicts=lambda _r: False,
               changed_of=lambda _i: {"o2"}, touching_now=set(), kind="k", kind_of=lambda c: c,
               moved_to=lambda _v: None, hazard=hz, min_repeat=2)
            cut = False
        except cap.CapReached:
            cut = True
        finally:
            cap.AT = None
        return cut, before, state(hz), hz

    cut, _b, a, hz = run(diagnose._diagnose.__wrapped__, False)       # the hold off
    assert cut and hz.near and not hz.world["spot"], ("MF-DA: the mix was not produced", a)
    print("  MF-DA hold off: a cut inside the diagnosis split the record (near counted, world "
          "not): a mix")
    cut, _b, a, hz = run(diagnose._diagnose, False)                   # held
    assert not cut and hz.near and hz.world["spot"], ("DA", cut, a)
    cut, b, a, hz = run(diagnose._diagnose, True)                     # passed before the unit
    assert cut and a == b, ("DA entry", cut, a)
    print("  DA held: inside, no cut and the record whole; passed at entry, cut before the unit "
          "and the record equals its before state")


'''
s = s[:a0] + NEW + s[a1:]
old = '''        with open(led, encoding="utf-8") as fh:
            rows = [json.loads(x) for x in fh if x.strip()]
        for r in rows:      # the arm lists differ by the check switches themselves'''
assert s.count(old) == 1
old2 = '''    src = open(os.path.join(HERE, "harness", "mem_store", "e4_stream.py"), encoding="utf-8").read()'''
new2 = '''    with open(os.path.join(HERE, "harness", "mem_store", "e4_stream.py"), encoding="utf-8") as fh:
        src = fh.read()'''
assert s.count(old2) == 1
s = s.replace(old2, new2)
open(p, "w", encoding="utf-8", newline="\\n").write(s)
print("ok")
