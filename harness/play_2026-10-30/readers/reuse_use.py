"""Read-only (the reviewer r263 (a)): each reuse_install's term, and every LATER row in the same life that names
it (detail.term / fit / held / bound), by event; whether its operand names objects; and in-game vs later-game use."""
import collections
import json
import re
import sys

sys.dont_write_bytecode = True
B = sys.argv[1]
c2g = {}
for ln in open(f"{B}/switch.tsv", encoding="utf-8"):
    f = ln.rstrip("\n").split("\t")
    if len(f) > 17 and f[0].isdigit():
        for c in range(int(f[3]), int(f[3]) + int(f[5])):
            c2g[c] = f[1]
inst, later = {}, collections.defaultdict(list)
for ln in open(f"{B}/stream.jsonl", encoding="utf-8"):
    try:
        r = json.loads(ln)
    except ValueError:
        continue
    d, e, c = r.get("detail") or {}, r.get("event"), r.get("cycle")
    if e == "reuse_install":
        inst.setdefault(d.get("term"), (c, r.get("slot"), d.get("partial")))
        continue
    for k in ("term", "fit", "held", "bound", "winner"):
        v = d.get(k)
        if isinstance(v, str) and v in inst and isinstance(c, int) and c >= inst[v][0]:
            later[v].append((c, e))
obj = re.compile(r"o\d+")
used = {t for t in inst if later[t]}
same, other = 0, 0
ev = collections.Counter()
for t in used:
    g0 = c2g.get(inst[t][0])
    gs = {c2g.get(c) for c, _ in later[t]}
    same += g0 in gs
    other += bool(gs - {g0})
    ev.update(e for _, e in later[t])
print(f"reuse_install terms: {len(inst)}; with object ids in the term: {sum(1 for t in inst if obj.search(t or ''))}; "
      f"partial: {sum(1 for t in inst if inst[t][2])}")
print(f"named again later in the life: {len(used)}; idle: {len(inst) - len(used)}; used in its own game: {same}; "
      f"used in a LATER game: {other}")
print("later rows naming them, by event:", dict(ev.most_common(12)))
