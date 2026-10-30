"""r426 B3 read: per game, PERCEIVE / other per step (repeat rows) beside the boundary record (trace, window_at, bound,
retargets); then sp80 at the start against sp80 at the end, function by function (file, name): the named readers and the
20 largest growths in cumulative s. argv: b3 out dir (holding a3ad3ef/)."""
import json
import os
import pstats
import sys

sys.dont_write_bytecode = True
D = os.path.join(sys.argv[1], "a3ad3ef")
rec = json.load(open(os.path.join(D, "b2.json"), encoding="utf-8"))
wall = {}
for line in open(os.path.join(D, "stream.jsonl"), encoding="utf-8"):
    r = json.loads(line)
    if r.get("event") == "repeat" and isinstance((r.get("detail") or {}).get("wall_s"), dict):
        wall[r["cycle"]] = r["detail"]["wall_s"]
print(f"library {rec['library']}  wall {rec['wall_s']} s")
for g in rec["games"]:
    cs = [c for c in range(g["cycle_start"], g["cycle_end"]) if c in wall]
    pe = sum(wall[c].get("PERCEIVE", 0.0) for c in cs) / max(1, len(cs))
    ot = sum(wall[c].get("other", 0.0) for c in cs) / max(1, len(cs))
    tot = sum(wall[c].get("total", 0.0) for c in cs) / max(1, len(cs))
    h = g["held_at_end"]
    print(f"  {g['i']:2d} {g['game']} c{g['cycle_start']:3d}-{g['cycle_end']:3d}  PERCEIVE {pe:6.2f}  other {ot:5.2f}  "
          f"total {tot:6.2f}  | trace {h['trace']} window_at {h['window_at']} bound {h['bound']} "
          f"retargets {h['retargets']}")


def by_name(i, g):
    out = {}
    for f, v in pstats.Stats(os.path.join(D, f"{i}_{g}.pstats")).stats.items():
        k = (os.path.basename(f[0]), f[2])
        c, ct, tt = out.get(k, (0, 0.0, 0.0))
        out[k] = (c + v[1], max(ct, v[3]), tt + v[2])
    return out


first, last = rec["games"][0], rec["games"][-1]
assert first["game"] == last["game"], (first["game"], last["game"])
a, b = by_name(first["i"], first["game"]), by_name(last["i"], last["game"])
NAMED = ("signature", "_rank_causes", "_diagnose_one", "_self_moving", "_prev_of", "_domain", "history",
         "indistinguishable", "_left", "_eval_ctx", "_record", "perceive", "step_effect", "_narrate_cues")
print(f"== {first['game']} at c{first['cycle_start']} vs c{last['cycle_start']}: cumulative s / calls / own s")
for n in NAMED:
    ks = [k for k in set(a) | set(b) if k[0] == "tether.py" and k[1] == n]
    for k in ks:
        va, vb = a.get(k, (0, 0.0, 0.0)), b.get(k, (0, 0.0, 0.0))
        print(f"  {n:20s} {va[1]:8.2f} -> {vb[1]:8.2f}   calls {va[0]:8d} -> {vb[0]:8d}   own {va[2]:7.2f} -> {vb[2]:7.2f}")
print("== the 20 largest growths in OWN time (tottime), any file")
grow = sorted(set(a) | set(b), key=lambda k: -(b.get(k, (0, 0.0, 0.0))[2] - a.get(k, (0, 0.0, 0.0))[2]))
for k in grow[:20]:
    va, vb = a.get(k, (0, 0.0, 0.0)), b.get(k, (0, 0.0, 0.0))
    print(f"  {vb[2] - va[2]:+8.2f} own  {va[2]:7.2f} -> {vb[2]:7.2f}  cum {va[1]:7.2f} -> {vb[1]:7.2f}  "
          f"calls {va[0]} -> {vb[0]}  {k[0]}({k[1]})")
