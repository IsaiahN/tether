"""Read-only (the reviewer r262): which state grows over the one agent's life. Per game: the memo_sizes row at its
switch (agent memos, cleared there; exempt memos, kept), whether a frame_break lands at the switch, and the REPEAT
row's sizes at the game's first step; then Spearman of each against position and first action. argv: PLAY, round."""
import json
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, "C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/"
                   "b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad")
from pos_read import spearman  # noqa: E402

B = f"C:/TETHER_RUNS/S6_2026-10-19/{sys.argv[1]}/{sys.argv[2]}"
games = {}
for ln in open(f"{B}/switch.tsv", encoding="utf-8"):
    f = ln.rstrip("\n").split("\t")
    if len(f) > 17 and f[0].isdigit() and f[14] != "None":
        games[f[1]] = {"pos": int(f[0]), "c0": int(f[3]), "first": float(f[14])}
by_c0 = {v["c0"]: k for k, v in games.items()}
memo, fb, rep = {}, set(), {}
for ln in open(f"{B}/stream.jsonl", encoding="utf-8"):
    if '"memo_sizes"' not in ln and '"frame_break"' not in ln and '"event": "repeat"' not in ln:
        continue
    try:
        r = json.loads(ln)
    except ValueError:
        continue
    c, e, d = r.get("cycle"), r.get("event"), r.get("detail") or {}
    if e == "memo_sizes":
        memo.setdefault(c, d)
    elif e == "frame_break":
        fb.add(c)
    elif e == "repeat":
        rep.setdefault(c, d)
cols = {}
names = sorted(games, key=lambda k: games[k]["pos"])
print("pos game c0 first | frame_break@switch | agent(sum) exempt: pairs_seen bound_slot_memo bound_memo "
      "bound_slot_map bound_term | carried | gamma_size owed integral reach (REPEAT at step 1)")
for k in names:
    v = games[k]
    m = memo.get(v["c0"], {})
    ag = sum(x for x in (m.get("agent") or {}).values() if isinstance(x, int))
    ex = m.get("exempt") or {}
    rp = rep.get(v["c0"], {})
    row = {"agent_sum": ag, "pairs_seen": ex.get("pairs_seen"), "bound_slot_memo": ex.get("bound_slot_memo"),
           "bound_memo": ex.get("bound_memo"), "bound_slot_map": ex.get("bound_slot_map"),
           "bound_term": ex.get("bound_term"), "gamma_size": rp.get("gamma_size"), "owed": rp.get("owed"),
           "integral": rp.get("integral"), "reach": rp.get("reach")}
    for kk, vv in row.items():
        cols.setdefault(kk, []).append(vv)
    print(f"{v['pos']:>2} {k} c{v['c0']} {v['first']:>6} | {'yes' if v['c0'] in fb else 'NO'} | "
          f"{m.get('at')} agent {ag} exempt {ex.get('pairs_seen')} {ex.get('bound_slot_memo')} "
          f"{ex.get('bound_memo')} {ex.get('bound_slot_map')} {ex.get('bound_term')} | {m.get('carried')} | "
          f"{rp.get('gamma_size')} {rp.get('owed')} {rp.get('integral')} {rp.get('reach')}")
pos = [games[k]["pos"] for k in names]
first = [games[k]["first"] for k in names]
print("== Spearman (position, first action) per quantity; n = games with the value")
for kk, vs in cols.items():
    idx = [i for i, x in enumerate(vs) if isinstance(x, (int, float))]
    if len(idx) < 5:
        print(f"  {kk}: too few values ({len(idx)})")
        continue
    xs = [vs[i] for i in idx]
    print(f"  {kk}: n {len(idx)} min {min(xs)} max {max(xs)}; vs position "
          f"{spearman([pos[i] for i in idx], xs):+.2f}; vs first action {spearman(xs, [first[i] for i in idx]):+.2f}")
extra = sorted(set(memo) - set(by_c0))
print(f"memo_sizes rows not at a game's first cycle: {extra}; frame_breaks not at a switch: "
      f"{sorted(fb - set(by_c0))}; switches with no frame_break: {sorted(by_c0[c] for c in by_c0 if c not in fb)}")
