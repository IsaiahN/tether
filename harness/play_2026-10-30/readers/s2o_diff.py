import json, sys
def rows(p):
    out = []
    for x in open(p, encoding="utf-8"):
        if not x.strip():
            continue
        r = json.loads(x); d = r.get("detail") or {}
        if r.get("event") == "arms" and r.get("slot") == "@run":
            for k in ("blob_n_files", "files_blob", "files_sha", "on", "off", "head", "tree"):
                d.pop(k, None)
        elif r.get("event") == "goal_hypotheses":
            d.pop("wall_s", None)
        elif r.get("event") == "books":
            for k in ("fit_dedup_agree", "fit_dedup_disagree"):
                d.pop(k, None)
        out.append(r)
    return out
a, b = rows(sys.argv[1]), rows(sys.argv[2])
print(len(a), len(b))
for i, (x, y) in enumerate(zip(a, b)):
    if x != y:
        print("FIRST DIFF at", i)
        for j in range(max(0, i - 3), min(i + 4, len(a), len(b))):
            print(" A", j, json.dumps(a[j])[:600])
            print(" B", j, json.dumps(b[j])[:600])
        break
else:
    print("prefix equal")
