"""r396 profile probe: one cold agent (no library, no lineage) at the tree given, one offline ARC
game, N agent steps under cProfile, a wall deadline checked before each step. Writes
<out>/<game>.pstats, <out>/<game>.json (per step: route rows, mint walks, slots, changed-object
slots, wall) and <out>/<game>.txt (top 15 by cumulative + caller chains up to Agent.step).
argv: tree game steps deadline_s out_dir"""
import cProfile
import io
import json
import logging
import os
import pstats
import sys
import time

sys.dont_write_bytecode = True
tree, game, steps, deadline, out = (sys.argv[1], sys.argv[2], int(sys.argv[3]),
                                    float(sys.argv[4]), sys.argv[5])
os.chdir(tree)
sys.path = [tree] + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")]
t_start = time.time()
logging.disable(logging.INFO)
import arc_holdout  # noqa: E402
from arc_agi import Arcade  # noqa: E402

arc = Arcade(operation_mode=arc_holdout._mode())
w = arc.make(game)
assert w is not None, arc_holdout.missing_game(game)
env, ag, led, board, palette, loaded = arc_holdout.wire(w, game)
setup_s = time.time() - t_start
print("loaded", loaded, "library", len(ag.gamma.library), "setup_s", round(setup_s, 1), flush=True)


def owner(slot):
    return slot.split(".", 1)[0] if "." in slot else slot


prof = cProfile.Profile()
per = []
prev = env.observe()
for i in range(steps):
    if time.time() - t_start > deadline:
        print("DEADLINE before step", i + 1, flush=True)
        break
    before = env.observe()
    n0 = len(led.rows())
    c0 = ag.cycle
    t0 = time.time()
    prof.enable()
    acted = ag.step()
    prof.disable()
    wall = time.time() - t0
    after = env.observe()
    rows = led.rows()[n0:]
    routes = [r for r in rows if r["event"] == "route"]
    sm = [r["detail"] for r in rows if r["event"] == "step_mint"]
    walks = sum(d.get("mints_run", 0) for d in sm)
    deferred = sum(d.get("mints_deferred", 0) for d in sm)
    mint_rows = sum(1 for r in rows if r["event"] in ("mint", "minted", "mint_park", "park"))
    keys = set(before) | set(after)
    changed_owners = {owner(k) for k in keys if before.get(k) != after.get(k)}
    slots_now = list(ag.slots)
    slots_changed = sum(1 for s in slots_now if owner(s) in changed_owners)
    per.append({"step": i + 1, "cycle": c0, "acted": bool(acted), "wall_s": round(wall, 2),
                "route_rows": len(routes),
                "route_bins": dict(__import__("collections").Counter(
                    r["detail"].get("bin") for r in routes)),
                "mints_run": walks, "mints_deferred": deferred, "mint_like_rows": mint_rows,
                "slots": len(slots_now), "owners": len({owner(s) for s in slots_now}),
                "changed_owners": len(changed_owners), "slots_of_changed": slots_changed})
    print("STEP", json.dumps(per[-1]), flush=True)

os.makedirs(out, exist_ok=True)
prof.dump_stats(os.path.join(out, f"{game}.pstats"))
st = pstats.Stats(prof)
total = st.total_tt
buf = io.StringIO()
ps = pstats.Stats(prof, stream=buf)
ps.sort_stats("cumulative").print_stats(15)
raw = st.stats   # func -> (cc, nc, tt, ct, callers)


def label(f):
    return f"{os.path.basename(f[0])}:{f[1]}({f[2]})"


step_keys = [f for f in raw if f[2] == "step" and f[0].endswith("tether.py")]
items = sorted(raw.items(), key=lambda kv: -kv[1][3])
top = []
for f, (cc, nc, tt, ct, callers) in items:
    if f[0] == "~" or "cProfile" in f[0] or "profile" in f[2]:
        continue
    top.append(f)
    if len(top) == 15:
        break


def chain(f):
    out_, seen, cur = [label(f)], {f}, f
    for _ in range(40):
        if cur in step_keys:
            break
        callers = raw.get(cur, (0, 0, 0, 0, {}))[4]
        if not callers:
            break
        nxt = max(callers.items(), key=lambda kv: kv[1][3])[0]
        if nxt in seen:
            break
        seen.add(nxt)
        out_.append(label(nxt))
        cur = nxt
    return " <- ".join(out_)


step_ct = max((raw[f][3] for f in step_keys), default=0.0)
lines = [f"GAME {game} cold library={len(ag.gamma.library)} steps_done={len(per)} "
         f"profiled_total_ct(Agent.step)={step_ct:.2f}s tt_sum={total:.2f}s setup_s={setup_s:.1f}"]
lines.append("TOP15 by cumulative (share of Agent.step cumulative; calls)")
for f in top:
    cc, nc, tt, ct, _c = raw[f]
    lines.append(f"  {ct / step_ct if step_ct else 0:6.1%}  calls {nc:>10}  {label(f)}")
lines.append("CHAINS (largest-cumulative caller each hop, up to Agent.step)")
for f in top:
    lines.append("  " + chain(f))
lines.append("PSTATS")
lines.append(buf.getvalue())
with open(os.path.join(out, f"{game}.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))
with open(os.path.join(out, f"{game}.json"), "w", encoding="utf-8") as fh:
    json.dump({"game": game, "per_step": per, "setup_s": setup_s,
               "library": len(ag.gamma.library)}, fh)
print("DONE", game, "steps", len(per), "wall", round(time.time() - t_start, 1), flush=True)
