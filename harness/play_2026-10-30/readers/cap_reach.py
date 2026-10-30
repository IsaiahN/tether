"""C1(c), read-only: from Agent._goal_hypothesis, which Agent methods are reachable through self.<m>(...)
calls (static, tether.py only), and do any of them call _cap_due? Prints the reachable set's size, every
reachable method that calls _cap_due, and the shortest call chain to each. argv: tether.py"""
import ast
import collections
import sys

tree = ast.parse(open(sys.argv[1], encoding="utf-8").read())
agent = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Agent")
meths = {f.name: f for f in agent.body if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef))}
calls = {}
for name, f in meths.items():
    out = set()
    for n in ast.walk(f):
        if (isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id == "self"
                and n.attr in meths):
            out.add(n.attr)          # a call or a reference (passed as a callback): both can run it
    calls[name] = out
start = "_goal_hypothesis"
prev = {start: None}
q = collections.deque([start])
while q:
    m = q.popleft()
    for c in sorted(calls[m]):
        if c not in prev:
            prev[c] = m
            q.append(c)
capped = [m for m in prev if "_cap_due" in calls[m]]
print(f"reachable from {start}: {len(prev)} methods; of them call _cap_due: {len(capped)}")
for m in capped:
    chain, x = [], m
    while x:
        chain.append(x)
        x = prev[x]
    print("  " + " <- ".join(chain))
print("route reachable:", "route" in prev, "| _library_fit reachable:", "_library_fit" in prev)
