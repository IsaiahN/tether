import ast, os, sys
root = sys.argv[1]
mods = {f[:-3] for f in os.listdir(root) if f.endswith(".py") and not f.startswith("test_")}
graph = {}
for m in mods:
    t = ast.parse(open(os.path.join(root, m + ".py"), encoding="utf-8").read())
    deps = set()
    for n in ast.walk(t):
        if isinstance(n, ast.Import):
            deps |= {a.name.split(".")[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom) and n.module:
            deps.add(n.module.split(".")[0])
    graph[m] = deps & mods
entries = ["tether_agent", "arc_holdout", "tether_runner", "kaggle_agent", "kaggle_bundle", "demo", "gate", "arc_run", "arc_online"]
seen, todo = set(), [e for e in entries if e in mods]
while todo:
    m = todo.pop()
    if m in seen:
        continue
    seen.add(m)
    todo += list(graph[m])
print("entries:", [e for e in entries if e in mods])
print("reached:", len(seen), "of", len(mods))
print("NOT reached from the entries:", sorted(mods - seen))
