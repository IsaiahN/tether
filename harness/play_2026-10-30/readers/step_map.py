"""Every self.<method>(...) call in Agent.step, by line, with: does that method reach _cap_due (static), and how many
methods it reaches; plus the step's own _cap_due lines. argv: tether.py"""
import ast
import collections
import sys

tree = ast.parse(open(sys.argv[1], encoding="utf-8").read())
agent = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Agent")
meths = {f.name: f for f in agent.body if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef))}
calls = {m: {n.attr for n in ast.walk(f) if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name)
             and n.value.id == "self" and n.attr in meths} for m, f in meths.items()}


def reach(start):
    seen, q = {start}, collections.deque([start])
    while q:
        for c in calls[q.popleft()]:
            if c not in seen:
                seen.add(c)
                q.append(c)
    return seen


seen_line = set()
for n in ast.walk(meths["step"]):
    if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name)
            and n.func.value.id == "self" and n.func.attr in meths):
        m = n.func.attr
        if (n.lineno, m) in seen_line:
            continue
        seen_line.add((n.lineno, m))
        r = reach(m)
        if len(r) >= 15 or m == "_cap_due":
            print(f"{n.lineno:6d}  {m:28s} reaches {len(r):4d}  cap_due {'yes' if any('_cap_due' in calls[x] for x in r) else 'NO'}")
