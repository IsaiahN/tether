import sys

sys.dont_write_bytecode = True
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
a0 = s.index("    if calls[0] == k and mode == \"c3\":")
a1 = s.index("    if calls[0] == k:\n        raise KeyError(\"planted fault\")")
NEW_PLANT = '''    if calls[0] == k and mode == "c3":
        # (C3)'s plants, REAL (the reviewer 16:52): two new 2-atom chains accepted, one stamped
        # with the faulted cycle and one with the cycle before; two invention records with a real
        # template, born in each. The generation must carry the earlier pair only, and still load.
        c = self.cycle
        new = [t for t in self.gamma.enumerate_closure("val", "val", 2, 4000, {})
               if len(t.atoms) == 2 and t.name not in self.gamma.library][:2]
        assert len(new) == 2, "C3: precondition: two new chains to plant"
        self.gamma.accept(new[0], seq=len(self.led), residual=f"o1.x@{c}")
        self.gamma.accept(new[1], seq=len(self.led), residual=f"o1.x@{c - 1}")
        plants["terms"] = {"now": new[0].name, "before": new[1].name}
        for nm, b in (("planted_now", c), ("planted_before", c - 1)):
            self._inv_carry.append({"name": nm, "template": "{o}.{r} > 0", "affects": [],
                                    "reading": "x", "term": nm, "then": [], "game": "fake",
                                    "born": b, "kind": "condition"})
'''
s = s[:a0] + NEW_PLANT + s[a1:]
R = [
    ('''real = tether.Agent.step
calls = [0]
''', '''real = tether.Agent.step
calls = [0]
plants = {}
'''),
    ('''    out["gen"] = {"ended": g.get("ended"), "error": g.get("error"),
                  "inv": [r.get("name") for r in g.get("inventions", [])],
                  "terms": [r.get("residual") for r in g.get("terms", [])
                            if str(r.get("residual") or "").startswith("o1.x@")]}''',
     '''    out["gen"] = {"ended": g.get("ended"), "error": g.get("error"),
                  "inv": [r.get("name") for r in g.get("inventions", [])],
                  "terms": [r.get("residual") for r in g.get("terms", [])
                            if str(r.get("residual") or "").startswith("o1.x@")]}
    out["plants"] = plants'''),
    ('''    if mode != "c3":     # the planted rows are no real terms: their generation is read, not loaded
        tether.Agent.step = real
        env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake", lineage_dir=d)
        out["head"] = ag.lineage_parent''',
     '''    tether.Agent.step = real
    env, ag, *_, loaded = arc_holdout.wire(FakeWrapper(script={}), "fake", lineage_dir=d)
    out["head"] = ag.lineage_parent
    out["lib_terms"] = sorted(n for n in plants.get("terms", {}).values() if n in ag.gamma.library)
    out["reinvented"] = ((loaded or {}).get("lineage") or {}).get("inventions_in")'''),
    ('''    assert "planted_before" in inv and "planted_now" not in inv, ("C3 inventions", inv)
    assert len(terms) == 1, ("C3 terms: the earlier one written, the faulted one not", terms)
    print(f"  C3 the faulted cycle's own entries left out (inventions {inv}; terms {terms})")''',
     '''    assert "planted_before" in inv and "planted_now" not in inv, ("C3 inventions", inv)
    assert len(terms) == 1, ("C3 terms: the earlier one written, the faulted one not", terms)
    pl = r["plants"]["terms"]
    assert r["head"] == r["gen_hash"], ("C3: the generation with real plants must load", r)
    assert r["lib_terms"] == [pl["before"]], ("C3: a fresh load holds the earlier term only", r)
    print(f"  C3 the faulted cycle's own entries left out (inventions {inv}; terms {terms}); a "
          f"fresh load reads it as the head and holds {pl['before']} and not {pl['now']}; "
          f"re-invented {r['reinvented']}")'''),
]
for a, b in R:
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)
with open(p, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(s)
print("ok")
