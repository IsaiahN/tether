"""r424 B2 read: per tree, per game, the repeat rows' wall_s by phase per step; then per game the cumulative time of
the PERCEIVE-side functions on both trees; the largest per-function differences at the last game; and the memo_sizes
rows as written. argv: b2 out dir (holding 7b9a90f/ and a3ad3ef/)."""
import json
import os
import pstats
import sys

sys.dont_write_bytecode = True
O = sys.argv[1]
TREES = ("7b9a90f", "a3ad3ef")
PH = ("total", "PERCEIVE", "other", "MINT", "ROUTE", "PLAN")
FN = ("perceive", "indistinguishable", "_left", "_eval_ctx", "_record", "_narrate_cues", "see", "_frame_vector",
      "derive", "_g1_wants", "_derived_wants", "track_of", "_carry_w_note", "_contact_fp", "_note_progress")


def cum(st, name):
    return max((v[3] for f, v in st.items() if f[2] == name), default=0.0)


games = {}
for t in TREES:
    rec = json.load(open(os.path.join(O, t, "b2.json"), encoding="utf-8"))
    wall, memo = {}, []
    for line in open(os.path.join(O, t, "stream.jsonl"), encoding="utf-8"):
        r = json.loads(line)
        if r.get("event") == "repeat" and isinstance((r.get("detail") or {}).get("wall_s"), dict):
            wall[r["cycle"]] = r["detail"]["wall_s"]
        elif r.get("event") == "memo_sizes":
            memo.append((r.get("cycle"), r["detail"].get("at"), r["detail"].get("agent")))
    print(f"== {t}  library {rec['library']}  wall {rec['wall_s']} s")
    for g in rec["games"]:
        cs = [c for c in range(g["cycle_start"], g["cycle_end"]) if c in wall]
        m = {p: sum(wall[c].get(p, 0.0) for c in cs) / max(1, len(cs)) for p in PH}
        print(f"  {g['i']} {g['game']} cycles {g['cycle_start']}-{g['cycle_end']} steps {len(cs)}  "
              + "  ".join(f"{p} {m[p]:6.2f}" for p in PH) + f"  probe walls {g['step_wall_s']}")
        games[(t, g["i"])] = (g["game"], pstats.Stats(os.path.join(O, t, f"{g['i']}_{g['game']}.pstats")).stats)
    print("  memo_sizes rows (cycle, at, agent):", memo if memo else "none written")
print("== cumulative s per function, per game (7b9a90f / a3ad3ef)")
for i in range(4):
    g = games[(TREES[0], i)][0]
    a, b = games[(TREES[0], i)][1], games[(TREES[1], i)][1]
    print(f"  {i} {g}: " + "  ".join(f"{n} {cum(a, n):.1f}/{cum(b, n):.1f}" for n in FN if cum(a, n) or cum(b, n)))
def by_name(st):
    # line numbers differ between the trees, so a function is (file, name): calls summed, cumulative the max
    out = {}
    for f, v in st.items():
        k = (os.path.basename(f[0]), f[2])
        c, ct = out.get(k, (0, 0.0))
        out[k] = (c + v[1], max(ct, v[3]))
    return out


for i in (0, 3):
    a, b = by_name(games[(TREES[0], i)][1]), by_name(games[(TREES[1], i)][1])
    diff = sorted(set(a) | set(b), key=lambda k: -abs(b.get(k, (0, 0.0))[1] - a.get(k, (0, 0.0))[1]))
    print(f"== game {i} {games[(TREES[0], i)][0]}, the 15 largest differences in cumulative s (a3ad3ef - 7b9a90f)")
    for k in diff[:15]:
        va, vb = a.get(k, (0, 0.0)), b.get(k, (0, 0.0))
        print(f"  {vb[1] - va[1]:+8.2f}  {va[1]:8.2f} / {vb[1]:8.2f}  calls {va[0]} / {vb[0]}  {k[0]}({k[1]})")
