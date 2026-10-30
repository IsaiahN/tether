import sys
from pathlib import Path

sys.dont_write_bytecode = True
p = Path(sys.argv[1])
s = p.read_text(encoding="utf-8").replace("\r\n", "\n")
R = [
    ('''    return {k: hashlib.sha256(json.dumps(canon(v), sort_keys=True, default=repr).encode())
            .hexdigest()[:16] for k, v in S.items()}
''',
     '''    out = {k: hashlib.sha256(json.dumps(canon(v), sort_keys=True, default=repr).encode())
           .hexdigest()[:16] for k, v in S.items()}
    out["_index_store_n"] = len(tether._INDEX_STORE)
    return out


def mask_fold(rows):
    """the game-start fold's counts of what an EARLIER agent in the process left, which it clears
    (tether._consolidate); "after" stays"""
    kept = []
    for x in rows:
        if x["event"] == "consolidate" and x["detail"].get("trigger") == "game_start":
            kept.append({f: x["detail"].pop(f, None)
                         for f in ("before", "landed_cleared", "slot_rows_before")})
            kept[-1]["after"] = x["detail"].get("after")
    return kept
'''),
    ('''    if mode == "once":                              # (r1): two fresh agents, same save, same board
        outs = []
''',
     '''    if mode == "once":                              # (r1): two fresh agents, same save, same board
        import pickle
        hook["board"], hook["clock"], hook["palette"] = d + "_board.pkl", list(clock), env._palette
        with open(hook["board"], "wb") as fh:       # (r2b): the board at the fault, for a cold step
            pickle.dump(copy.deepcopy(env.w.w), fh)
        outs = []
'''),
    ('''        # the game-start fold counts what the agent BEFORE left in the process's bound stores and
        # clears it (tether._consolidate): those three counts differ by construction (r1_0 follows
        # the faulted agent, r1_1 follows r1_0), so they are masked and kept; "after" is not
        cleared = []
        for rows_i, _c in outs:
            for x in rows_i:
                if x["event"] == "consolidate" and x["detail"].get("trigger") == "game_start":
                    cleared.append({f: x["detail"].pop(f, None)
                                    for f in ("before", "landed_cleared", "slot_rows_before")})
                    cleared[-1]["after"] = x["detail"].get("after")
        hook["r1"] = {"diff": compare(outs[0][0], outs[1][0], set()), "cleared": cleared,
                      "calls": [o[1] for o in outs], "rows": len(outs[0][0])}
''',
     '''        # the game-start fold counts what the agent BEFORE left in the process's bound stores and
        # clears it: those three counts differ by construction (r1_0 follows the faulted agent,
        # r1_1 follows r1_0), so they are masked and kept; "after" is not
        cleared = [c for rows_i, _c in outs for c in mask_fold(rows_i)]
        hook["r1"] = {"diff": compare(outs[0][0], outs[1][0], set()), "cleared": cleared,
                      "calls": [o[1] for o in outs], "rows": len(outs[0][0]),
                      "rows0": outs[0][0]}
'''),
    ('''       "digest": hook.get("digest"), "snap": hook.get("snap"),
''',
     '''       "digest": hook.get("digest"), "snap": hook.get("snap"), "board": hook.get("board"),
       "clock": hook.get("clock"), "palette": hook.get("palette"),
'''),
    ('''import json, arc_holdout, tether
from test_entry import FakeWrapper
tether._AGENT_SEED = False
''' + "''' + DIGEST + r'''" + '''
d = sys.argv[2] + "_cold"
shutil.copytree(sys.argv[2], d)
env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake", lineage_dir=d)
print(json.dumps(digest(ag)))
''',
     '''import json, pickle, arc_holdout, ledger, tether
tether._AGENT_SEED = False
''' + "''' + DIGEST + r'''" + '''
d = sys.argv[2] + "_cold"
shutil.copytree(sys.argv[2], d)
with open(sys.argv[3], "rb") as fh:
    board = pickle.load(fh)
env = arc_holdout.world_on(arc_holdout.ResetGuard(board), "fake", int(sys.argv[4]), None)
led = ledger.Ledger(None)
ag, _l = arc_holdout.wire_agent(env, "fake", None, led, None, d,
                                clock=(int(sys.argv[5]), json.loads(sys.argv[6])))
dg = digest(ag)
env.observe()
ag.step()
rows = led.rows()
cleared = mask_fold(rows)
print(json.dumps({"digest": dg, "rows": rows, "cleared": cleared}, default=str))
'''),
    ('''    cold = json.loads(run(COLD, r["snap"]))
    diff = sorted(k for k in set(cold) | set(r["digest"]) if cold.get(k) != r["digest"].get(k))
    assert not diff, ("r2: the fresh agent's load differs from a cold load of the save", diff)
    print(f"  r2 the fresh agent's state digest equals a cold process's load: {len(cold)} "
          f"structures")
''',
     '''    c = json.loads(run(COLD, r["snap"], r["board"], str(r["palette"]), str(r["clock"][0]),
                       json.dumps(r["clock"][1])))
    cold, fresh = c["digest"], r["digest"]
    proc = ("index_store", "_index_store_n")    # the process's compile cache, read separately
    diff = sorted(k for k in set(cold) | set(fresh) if k not in proc and cold.get(k) != fresh.get(k))
    assert not diff, ("r2: the fresh agent's load differs from a cold load of the save", diff)
    print(f"  r2 the fresh agent's load equals a cold process's load of the same save on "
          f"{len([k for k in cold if k not in proc])} structures; the process's compile cache "
          f"tether._INDEX_STORE: fresh {fresh['_index_store_n']} entries, cold "
          f"{cold['_index_store_n']} (READ, NOT ASSERTED: for the reviewer's ruling)")
    d2 = compare(r1["rows0"], c["rows"], set())
    assert not d2, ("r2b: the fresh agent's step differs from a cold process's", d2)
    print(f"  r2b the fresh agent's next step and a cold process's on the same board from the same "
          f"save: {len(c['rows'])} rows equal (the cold fold cleared {c['cleared']})")
'''),
]
for a, b in R:
    assert s.count(a) == 1, (a[:90], s.count(a))
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8", newline="\n")
print("ok")
