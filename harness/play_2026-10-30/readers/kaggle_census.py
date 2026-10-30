"""Read-only: every importer of the Kaggle modules (AST, all .py in the tree incl. tests/, harness/,
conform/, library/), every other file that names them (any text file), and the Kaggle-named files.
argv: TREE"""
import ast
import hashlib
import os
import sys

TREE = sys.argv[1]
MODS = ("tether_runner", "kaggle_bundle", "kaggle_agent")
SKIP = {".git", ".venv", "__pycache__", "runs", "node_modules"}
py, other = [], []
for root, dirs, files in os.walk(TREE):
    dirs[:] = [d for d in dirs if d not in SKIP]
    for f in files:
        p = os.path.join(root, f)
        (py if f.endswith(".py") else other).append(p)


def rel(p):
    return os.path.relpath(p, TREE).replace("\\", "/")


print("== Kaggle-named files")
for p in py + other:
    if "kaggle" in os.path.basename(p).lower() or os.path.basename(p).startswith("tether_runner"):
        with open(p, "rb") as fh:
            b = fh.read()
        print(f"  {rel(p)}  {len(b):,} B  sha256 {hashlib.sha256(b).hexdigest()[:16]}  "
              f"lines {b.count(b'\n')}")
print("== AST imports of", MODS)
for p in py:
    try:
        tree = ast.parse(open(p, encoding="utf-8", errors="replace").read())
    except SyntaxError as e:
        print("  UNPARSED", rel(p), e)
        continue
    for n in ast.walk(tree):
        names = []
        if isinstance(n, ast.Import):
            names = [a.name for a in n.names]
        elif isinstance(n, ast.ImportFrom) and n.module:
            names = [n.module]
        for m in names:
            if m.split(".")[0] in MODS:
                print(f"  {rel(p)}:{n.lineno}: import {m}")
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "__import__":
            print(f"  {rel(p)}:{n.lineno}: __import__ call")
print("== every other mention (text, any file type), by line")
for p in py + other:
    try:
        with open(p, encoding="utf-8", errors="strict") as fh:
            lines = fh.read().splitlines()
    except (UnicodeDecodeError, OSError):
        continue
    for i, line in enumerate(lines, 1):
        if any(m in line for m in MODS):
            print(f"  {rel(p)}:{i}: {line.strip()[:140]}")
