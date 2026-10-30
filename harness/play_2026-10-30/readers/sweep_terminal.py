"""4d-x sweep (the reviewer 2026-10-22 08:47 (1)), read-only: every comparison, in a git-tracked *.py outside tests/,
of terminal()'s result (the call itself, or a name / attribute it was assigned to in the same scope) against a string
literal, or against a ledger constant other than WIN and DEATH (a tuple / list / set of them included). Prints every
hit as path:line: source, then the count. Also prints every terminal() ASSIGNMENT site, so the population is visible.
argv: repo"""
import ast
import os
import subprocess
import sys

R = sys.argv[1]
OK = {"WIN", "DEATH"}
files = [f for f in subprocess.run(["git", "-C", R, "ls-files", "*.py"], capture_output=True, text=True,
                                   check=True).stdout.split() if not f.startswith("tests/")]
assert files, "no files"


def is_term_call(n):
    return isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "terminal"


def bad_other(n):
    if isinstance(n, ast.Constant) and isinstance(n.value, str):
        return True
    if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id == "ledger":
        return n.attr not in OK
    if isinstance(n, (ast.Tuple, ast.List, ast.Set)):
        return any(bad_other(e) for e in n.elts)
    return False


hits, assigns = [], []
for f in files:
    p = os.path.join(R, f)
    src = open(p, encoding="utf-8", errors="replace").read()
    lines = src.splitlines()
    tree = ast.parse(src)
    scopes = [tree] + [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    for sc in scopes:
        body = list(ast.walk(sc))
        held = set()
        for n in body:
            if isinstance(n, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):
                val = n.value
                tg = n.targets if isinstance(n, ast.Assign) else [n.target]
                if val is not None and is_term_call(val):
                    for t in tg:
                        held.add(ast.unparse(t))
                        assigns.append(f"{f}:{n.lineno}: {lines[n.lineno - 1].strip()}")
        for n in body:
            if not isinstance(n, ast.Compare):
                continue
            ops = [n.left, *n.comparators]
            ours = [o for o in ops if is_term_call(o) or ast.unparse(o) in held]
            if ours and any(bad_other(o) for o in ops if o not in ours):
                hits.append(f"{f}:{n.lineno}: {lines[n.lineno - 1].strip()}")
for a in sorted(set(assigns)):
    print("ASSIGN", a)
for h in sorted(set(hits)):
    print("HIT", h)
print(f"files {len(files)} | assignment sites {len(set(assigns))} | hits {len(set(hits))}")
