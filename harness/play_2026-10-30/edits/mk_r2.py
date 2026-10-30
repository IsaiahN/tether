"""Write r15_read2.py from r15_read.py: round as argv, compare against PLAY14 r1 and PLAY15 r1,
add derived-want exhausts and PLAN wall_s (the reviewer r260 items 2 and 3). Each edit asserted once."""
import sys

src, dst = sys.argv[1], sys.argv[2]
t = open(src, encoding="utf-8").read()


def edit(old, new):
    global t
    assert t.count(old) == 1, (t.count(old), old[:60])
    t = t.replace(old, new)


edit('B = "C:/TETHER_RUNS/S6_2026-10-19"\n',
     'B = "C:/TETHER_RUNS/S6_2026-10-19"\nRND = sys.argv[1]   # e.g. round_02\n')
edit('def games(r):\n    out = {}\n    for ln in open(f"{B}/{r}/round_01/switch.tsv", encoding="utf-8"):',
     'def games(r, rnd="round_01"):\n    out = {}\n    for ln in open(f"{B}/{r}/{rnd}/switch.tsv", encoding="utf-8"):')
edit('a, b = games("PLAY14"), games("PLAY15")\n',
     'a, b, p1 = games("PLAY14"), games("PLAY15", RND), games("PLAY15")\n')
edit('for ln in open(f"{B}/PLAY15/round_01/stream.jsonl", encoding="utf-8"):',
     'for ln in open(f"{B}/PLAY15/{RND}/stream.jsonl", encoding="utf-8"):')
edit('''    print(f"{g} {v['steps']}/{v['first']}{'*' if v['ext'] else ''}({apm15:.2f}) | "''',
     '''    dw = []
    for c in cs:
        asked = {r["slot"] for r in ev(c, "derived_asked")}
        dw.append(sum(1 for r in ev(c, "park") if r["slot"] in asked
                      and (r.get("detail") or {}).get("budget_exhausted")))
    plan_w = [round((r.get("detail") or {}).get("wall_s"), 1) for c in cs for r in rows.get(c, ())
              if r.get("step") == "PLAN" and "wall_s" in (r.get("detail") or {})]
    q = p1[g]
    tot.update(dw_steps=sum(1 for x in dw if x), dw_total=sum(dw))
    print(f"{g} [PLAY15 r1 {q['steps']}/{q['first']}] derived-want exhausts: steps {sum(1 for x in dw if x)} "
          f"total {sum(dw)} per step max {max(dw)} mean {statistics.mean(dw):.2f}; PLAN wall_s {plan_w}")
    print(f"{g} {v['steps']}/{v['first']}{'*' if v['ext'] else ''}({apm15:.2f}) | "''')
open(dst, "w", encoding="utf-8").write(t)
print("written")
