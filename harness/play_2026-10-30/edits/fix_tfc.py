import sys

sys.dont_write_bytecode = True
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
R = [
    ('''    if calls[0] == k:
        c = self.cycle
        self._inv_carry.extend(''',
     '''    if calls[0] == k and mode == "c3":
        c = self.cycle
        self._inv_carry.extend('''),
    ('''        self.gamma.blob = planted_blob
        raise KeyError("planted fault")''',
     '''        self.gamma.blob = planted_blob
    if calls[0] == k:
        raise KeyError("planted fault")'''),
    ('''if gens:
    g = json.loads(ls.file_bytes(__import__("pathlib").Path(d) / gens[0]))''',
     '''if gens:
    g = json.loads(ls.file_bytes(os.path.join(d, gens[0])))'''),
    ('''    tether.Agent.step = real
    env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake", lineage_dir=d)
    out["head"] = ag.lineage_parent''',
     '''    if mode != "c3":     # the planted rows are no real terms: their generation is read, not loaded
        tether.Agent.step = real
        env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake", lineage_dir=d)
        out["head"] = ag.lineage_parent'''),
    ('''    print(f"  F1 the KeyError reached the caller; agent_fault row at {r['faults'][0]['site']}; "
          f"traceback kept; generation {r['gen_hash']} ended agent_fault, read as the head")
    inv, terms = r["gen"]["inv"], r["gen"]["terms"]''',
     '''    print(f"  F1 the KeyError reached the caller; agent_fault row at {r['faults'][0]['site']}; "
          f"traceback kept; generation {r['gen_hash']} ended agent_fault, read as the head")
    d = fresh()
    led = os.path.join(tempfile.mkdtemp(), "f.jsonl")
    r = json.loads(run(CHILD, d, led, str(K), "c3"))
    assert r["gen"] is not None, ("C3: precondition: no generation written", r)
    inv, terms = r["gen"]["inv"], r["gen"]["terms"]'''),
    ('''    assert len(terms) == 1, ("C3 terms: the earlier-stamped one written, the faulted one not", terms)''',
     '''    assert len(terms) == 1, ("C3 terms: the earlier one written, the faulted one not", terms)'''),
    ('''    print("  OFF TETHER_ERROR_CARRY off: the KeyError reached the caller, no generation (the defect)")''',
     '''    print("  OFF TETHER_ERROR_CARRY off: the KeyError reached the caller, no generation")'''),
]
for a, b in R:
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)
with open(p, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(s)
print("ok")
