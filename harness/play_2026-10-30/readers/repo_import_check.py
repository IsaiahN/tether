"""4d: which tests/test_*.py have NO real top-level `import _repo` statement (ast, not grep). argv: tests_dir"""
import ast
import os
import sys

d = sys.argv[1]
bad = []
names = sorted(f for f in os.listdir(d) if f.startswith("test_") and f.endswith(".py"))
for f in names:
    tree = ast.parse(open(os.path.join(d, f), encoding="utf-8").read())
    if not any(isinstance(n, ast.Import) and any(a.name == "_repo" for a in n.names) for n in tree.body):
        bad.append(f)
print("tests", len(names), "| no real import _repo:", len(bad))
for f in bad:
    print(" ", f)
