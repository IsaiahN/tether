"""Q2: every string CONSTANT (not a docstring, not a comment) in the agent's modules that equals or contains one of
the 25 game ids, with file:line and the enclosing function. argv: repo files_list"""
import ast
import os
import re
import sys

R, LST = sys.argv[1:3]
ids = sorted(os.listdir(os.path.join(R, "environment_files")))
pat = re.compile(r"\b(" + "|".join(ids) + r")\b")
for rel in [x.strip() for x in open(LST) if x.strip()]:
    tree = ast.parse(open(os.path.join(R, rel), encoding="utf-8").read())
    docs = set()
    for n in ast.walk(tree):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.body:
            b = n.body[0]
            if isinstance(b, ast.Expr) and isinstance(b.value, ast.Constant) and isinstance(b.value.value, str):
                docs.add(id(b.value))
    funcs = [(n.lineno, getattr(n, "end_lineno", n.lineno), n.name) for n in ast.walk(tree)
             if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in docs and pat.search(n.value):
            fn = min((f for f in funcs if f[0] <= n.lineno <= f[1]), key=lambda f: f[1] - f[0], default=(0, 0, "<module>"))
            print(f"{rel}:{n.lineno}  in {fn[2]}  {n.value[:90]!r}")
