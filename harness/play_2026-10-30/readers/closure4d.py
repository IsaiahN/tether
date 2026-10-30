"""4d closure check (the reviewer 2026-10-22 08:30 (1)), read-only: for each test NOT in the spawn list, the repo modules
it reaches by import (transitively, imports inside functions included), and which of those match the spawn grep. A
module is resolved by name against the root, tests/, conform/, harness/ and harness/mem_store/ (every dir a test puts on
sys.path), and dotted names against the root; a name that resolves nowhere is outside the repo. argv: repo spawn_list"""
import ast
import os
import re
import sys

R, LIST = sys.argv[1:3]
GREP = re.compile(r"subprocess|sys\.executable|os\.system|multiprocessing|runpy|Popen")
DIRS = ["", "tests", "conform", "harness", os.path.join("harness", "mem_store")]
with open(LIST, encoding="utf-8") as fh:
    spawn = {x.strip() for x in fh if x.strip()}
tests = sorted(f for f in os.listdir(os.path.join(R, "tests")) if f.startswith("test_") and f.endswith(".py"))
rest = [t for t in tests if t not in spawn]
assert len(tests) == 148 and len(rest) == 59, (len(tests), len(rest))


def resolve(name):
    parts = name.split(".")
    hits = []
    for d in DIRS:
        base = os.path.join(R, d, *parts)
        for p in (base + ".py", os.path.join(base, "__init__.py")):
            if os.path.isfile(p):
                hits.append(os.path.normpath(p))
    return hits


def imports(path):
    with open(path, encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    out = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            out.update(a.name for a in n.names)
        elif isinstance(n, ast.ImportFrom) and n.module and not n.level:
            out.add(n.module)
            out.update(f"{n.module}.{a.name}" for a in n.names)
    return out


memo = {}


def closure(path):
    seen, todo = set(), [path]
    while todo:
        p = todo.pop()
        if p in seen:
            continue
        seen.add(p)
        if p not in memo:
            memo[p] = [h for m in imports(p) for h in resolve(m)]
        todo.extend(memo[p])
    return seen


def matches(p):
    with open(p, encoding="utf-8") as fh:
        return bool(GREP.search(fh.read()))


for t in rest:
    tp = os.path.normpath(os.path.join(R, "tests", t))
    hit = sorted(os.path.relpath(p, R).replace("\\", "/") for p in closure(tp) if p != tp and matches(p))
    print(t, "\t", " ".join(hit) if hit else "-")
