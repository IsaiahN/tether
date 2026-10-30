"""R2: every string constant matching ^ACTION\d+$ or == "RESET" in the agent modules (list file), with file:line,
the enclosing function, and its syntactic ROLE: compared (in a Compare), a dict key / subscript, an argument to a
call (and the callee), or other. argv: repo list"""
import ast
import collections
import os
import re
import sys

R, LST = sys.argv[1:3]
pat = re.compile(r"^(ACTION\d+|RESET)$")
roles = collections.Counter()
for rel in [x.strip() for x in open(LST) if x.strip()]:
    tree = ast.parse(open(os.path.join(R, rel), encoding="utf-8").read())
    parent = {}
    for n in ast.walk(tree):
        for c in ast.iter_child_nodes(n):
            parent[c] = n
    funcs = [(n.lineno, n.end_lineno, n.name) for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and pat.match(n.value):
            p = parent.get(n)
            if isinstance(p, ast.Compare):
                role = "COMPARED"
            elif isinstance(p, (ast.Tuple, ast.List, ast.Set)) and isinstance(parent.get(p), ast.Compare):
                role = "COMPARED(in)"
            elif isinstance(p, ast.Subscript) or isinstance(p, ast.Dict):
                role = "key"
            elif isinstance(p, ast.Call):
                f = p.func
                role = "arg:" + (f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "?"))
            elif isinstance(p, ast.keyword):
                role = "kwarg:" + str(p.arg)
            else:
                role = type(p).__name__
            fn = min((f for f in funcs if f[0] <= n.lineno <= f[1]), key=lambda f: f[1] - f[0], default=(0, 0, "<module>"))
            roles[role.split(":")[0]] += 1
            print(f"{rel}:{n.lineno}  {fn[2]:28s} {n.value:8s} {role}")
print("ROLES", dict(roles))
