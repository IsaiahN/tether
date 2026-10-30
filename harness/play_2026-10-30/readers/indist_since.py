import json, sys, collections
sys.dont_write_bytecode = True
rows, since, steps, keys = 0, collections.Counter(), set(), collections.Counter()
for line in open(sys.argv[1], encoding="utf-8"):
    r = json.loads(line)
    if r.get("event") == "indistinct":
        rows += 1
        d = r.get("detail") or {}
        s = d.get("since"); since["none" if s is None else (r.get("cycle") or 0) - s] += 1; keys[("pairs>0" if d.get("pairs") else "pairs0",)] += 1
        keys[tuple(sorted(d.keys()))] += 1
    if r.get("step") == "REPEAT":
        steps.add(r.get("cycle"))
print("indistinct rows", rows, "| cycles with a REPEAT row", len(steps))
print("cycle - since:", dict(sorted(since.items(), key=str)))
print("detail keys:", dict(keys))
