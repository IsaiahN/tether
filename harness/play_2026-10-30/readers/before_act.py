import collections, json, sys

stream, switch, game = sys.argv[1], sys.argv[2], sys.argv[3]
row = next(line.rstrip("\n").split("\t") for line in open(switch, encoding="utf-8")
           if line.split("\t")[0].isdigit() and line.split("\t")[1] == game)
seq0, seq1 = int(row[10]), int(row[12])
steps = collections.Counter()
ev = collections.Counter()
slots = set()
first_act = None
n = 0
with open(stream, encoding="utf-8") as f:
    for line in f:
        try:
            r = json.loads(line)
        except Exception:
            continue
        s = r.get("seq")
        if not isinstance(s, int) or s < seq0 or s >= seq1:
            continue
        if r.get("step") == "ACT":
            first_act = (s, r.get("cycle"), r.get("event"))
            break
        n += 1
        steps[r.get("step")] += 1
        ev[(r.get("step"), r.get("event"))] += 1
        if r.get("slot") not in (None, "*") and not str(r.get("slot")).startswith("@"):
            slots.add(r.get("slot"))
print(game, "seq", seq0, seq1, "rows before first ACT", n, "first ACT", first_act)
print(" steps:", dict(steps.most_common()))
print(" slots named:", len(slots))
for k, v in ev.most_common(14):
    print("  ", v, k)
print(" ROUTE reach", ev[("ROUTE", "reach")], "reach_failed", ev[("ROUTE", "reach_failed")],
      "MINT mint rows", sum(v for (st, e), v in ev.items() if st == "MINT"))
