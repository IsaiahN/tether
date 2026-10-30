"""For every Agent method whose name matches argv[2:] (substrings), whether _cap_due is reachable through
self.<m> calls/references (static), and the shortest chain. argv: tether.py substrings..."""
import ast
import collections
import sys

tree = ast.parse(open(sys.argv[1], encoding="utf-8").read())
agent = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Agent")
meths = {f.name: f for f in agent.body if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef))}
calls = {m: {n.attr for n in ast.walk(f) if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name)
             and n.value.id == "self" and n.attr in meths} for m, f in meths.items()}
for start in sorted(m for m in meths if any(s in m for s in sys.argv[2:])):
    prev, q = {start: None}, collections.deque([start])
    while q:
        m = q.popleft()
        for c in sorted(calls[m]):
            if c not in prev:
                prev[c] = m
                q.append(c)
    hit = next((m for m in prev if "_cap_due" in calls[m]), None)
    chain = []
    while hit:
        chain.append(hit)
        hit = prev[hit]
    print(f"{start:28s} reach {len(prev):4d}  cap {'YES via ' + ' <- '.join(chain) if chain else 'NO'}")
