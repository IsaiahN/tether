import json, sys
g = json.load(open(sys.argv[1], encoding="utf-8"))
print("top keys", sorted(g)[:60])
print("game", g.get("game"), "parent", g.get("parent"))
t = g.get("terms") or []
print("n terms", len(t)); print("term[0] keys", sorted(t[0]) if t else None)
print("term[0]", json.dumps(t[0])[:600] if t else None)
for k in ("episodes", "kinds_landed_dk", "unit_used", "status"):
    v = g.get(k); print(k, type(v).__name__, (json.dumps(v)[:300] if v else v))
