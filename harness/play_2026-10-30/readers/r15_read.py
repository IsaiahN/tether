"""Read-only PLAY15 r1 line (the reviewer r250-r259): per game against PLAY14 r1, the B1 owed columns,
bp35's step 1, and ft09 / tr87 / lf52 rows. argv: none. Reads switch.tsv and stream.jsonl only."""
import collections
import json
import statistics
import sys

sys.dont_write_bytecode = True
B = "C:/TETHER_RUNS/S6_2026-10-19"


def games(r):
    out = {}
    for ln in open(f"{B}/{r}/round_01/switch.tsv", encoding="utf-8"):
        f = ln.rstrip("\n").split("\t")
        if len(f) > 17 and f[0].isdigit():
            out[f[1]] = {"idx": int(f[0]), "c0": int(f[3]), "wall": float(f[4]), "steps": int(f[5]),
                         "lv": int(f[6]), "first": float(f[14]) if f[14] != "None" else None,
                         "ext": f[15] == "True", "seq0": int(f[10]), "seq1": int(f[12])}
    return out


a, b = games("PLAY14"), games("PLAY15")
rows = collections.defaultdict(list)          # cycle -> rows
for ln in open(f"{B}/PLAY15/round_01/stream.jsonl", encoding="utf-8"):
    try:
        r = json.loads(ln)
    except ValueError:
        continue
    if isinstance(r.get("cycle"), int):
        rows[r["cycle"]].append(r)


def cyc(g):
    v = b[g]
    return list(range(v["c0"], v["c0"] + v["steps"]))


def ev(c, name):
    return [r for r in rows.get(c, ()) if r.get("event") == name]


print("== PER GAME: PLAY15 steps/first(apm) | PLAY14 steps/first(apm); owed at step start max/mean; "
      "owed minted / dropped; unpaid deferred+capped; oldest-owed age (RECONSTRUCTED)")
tot = collections.Counter()
for g in sorted(b, key=lambda g: b[g]["idx"]):
    v, w = b[g], a[g]
    apm15 = 60 * v["steps"] / v["wall"] if v["wall"] else 0
    apm14 = 60 * w["steps"] / w["wall"] if w["wall"] else 0
    cs = cyc(g)
    owed_at = []
    minted = dropped = 0
    prev = set()
    run = {}
    oldest = 0
    capped = False
    for c in cs:
        owed_at.append(len(prev))
        dfr = {r["slot"] for r in ev(c, "mint_deferred")}
        ran = {r["slot"] for r in rows.get(c, ()) if r.get("event") in ("park", "mint")
               and r.get("step") == "MINT"}
        minted += len(prev & ran - dfr)
        dropped += len(prev - ran - dfr)
        if ev(c, "cap_unminted"):
            capped = True
        run = {s: run.get(s, c) for s in dfr}
        prev = dfr
    last = cs[-1] if cs else None
    unpaid_d = len(ev(last, "mint_deferred")) if last is not None else 0
    unpaid_c = len(ev(last, "cap_unminted")) if last is not None else 0
    if run and not capped:
        oldest = max(last - s + 1 for s in run.values())
    sm = sum(len(ev(c, "step_mint")) for c in cs)
    md = sum(len(ev(c, "mint_deferred")) for c in cs)
    tot.update(steps15=v["steps"], steps14=w["steps"], minted=minted, dropped=dropped,
               unpaid_d=unpaid_d, unpaid_c=unpaid_c, step_mint=sm, mint_deferred=md)
    print(f"{g} {v['steps']}/{v['first']}{'*' if v['ext'] else ''}({apm15:.2f}) | "
          f"{w['steps']}/{w['first']}{'*' if w['ext'] else ''}({apm14:.2f}); owed max {max(owed_at)} "
          f"mean {statistics.mean(owed_at):.1f}; minted {minted} dropped {dropped}; unpaid "
          f"{unpaid_d}+{unpaid_c}; oldest {'capped' if capped else oldest}; step_mint {sm} "
          f"mint_deferred {md}; levels {v['lv']}")
print("TOTALS", dict(tot))
for g in ("bp35", "tr87", "lf52", "ft09"):
    print(f"== {g} per step")
    for c in cyc(g):
        rs = rows.get(c, ())
        steps = collections.Counter(r.get("step") for r in rs)
        parks = [r for r in rs if r.get("event") == "park"]
        ex = [r["slot"] for r in parks if (r.get("detail") or {}).get("budget_exhausted")]
        sm = [r.get("detail") for r in ev(c, "step_mint")]
        wall = [(r.get("step"), r.get("event"), (r.get("detail") or {}).get("wall_s"))
                for r in rs if "wall_s" in (r.get("detail") or {})]
        ld = collections.Counter((r.get("detail") or {}).get("why") for r in ev(c, "lookup_deferred"))
        routed = len(ev(c, "route"))
        print(f"  c{c}: rows by step {dict(steps)}; route rows {routed}; parks {len(parks)} "
              f"(exhausted {ex}); step_mint {sm}; lookup_deferred {dict(ld)}; walk_cut "
              f"{len(ev(c, 'walk_cut'))}; wall_s rows {wall[:6]}")
        for r in parks:
            d = r.get("detail") or {}
            print(f"     park {r['slot']}: seen {d.get('candidates_seen')} tried "
                  f"{d.get('candidates_tried')} exhausted {d.get('budget_exhausted')} "
                  f"verdict {d.get('verdict')}")
