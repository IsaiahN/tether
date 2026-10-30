"""4d closure checks (the reviewer 2026-10-22 09:21 (1)), read-only, by ast.
 (a) DOCSTRINGS: every module/class/function docstring (ast.get_docstring) of each tests/test_*.py in the AFTER tree
     against the same file at BEFORE_REF (git show <ref>:<name>, the root layout). Prints each file whose docstrings
     differ, with the differing lines, so deliberate path edits are listed and anything else stands out.
 (b) _repo FIRST: in each test, every import of a REPO module (a name resolving to a .py or package in the root,
     tests/, conform/, harness/, harness/mem_store/) sits after the top-level `import _repo`; __future__ and anything
     not in the repo may come before it.
argv: after_tree before_ref"""
import ast
import difflib
import os
import subprocess
import sys

TREE, REF = sys.argv[1:3]
T = os.path.join(TREE, "tests")
DIRS = ["", "tests", "conform", "harness", os.path.join("harness", "mem_store")]
names = sorted(f for f in os.listdir(T) if f.startswith("test_") and f.endswith(".py"))
assert len(names) == 148, len(names)


def docs(src):
    out = {}
    tree = ast.parse(src)
    out["<module>"] = ast.get_docstring(tree, clean=False)
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out[f"{n.name}@{n.lineno}"] = ast.get_docstring(n, clean=False)
    return out


def repo_module(name):
    parts = name.split(".")
    if parts[0] in ("_repo", "__future__"):
        return False
    for d in DIRS:
        base = os.path.join(TREE, d, parts[0])
        if os.path.isfile(base + ".py") or os.path.isfile(os.path.join(base, "__init__.py")):
            return True
    return False


diff_files = []
for f in names:
    with open(os.path.join(T, f), encoding="utf-8") as fh:
        after = docs(fh.read())
    before_src = subprocess.run(["git", "-C", TREE, "show", f"{REF}:{f}"], capture_output=True, text=True,
                                encoding="utf-8", check=True).stdout
    before = docs(before_src)
    a_list = [v for v in after.values()]           # by order: line numbers shift by the inserted import
    b_list = [v for v in before.values()]
    if a_list != b_list:
        diff_files.append(f)
        print(f"(a) DIFFER {f}: {len(b_list)} docstrings before, {len(a_list)} after")
        for b, a in zip(b_list, a_list):
            if a != b:
                for ln in difflib.unified_diff((b or "").splitlines(), (a or "").splitlines(), lineterm="", n=0):
                    if not ln.startswith(("---", "+++", "@@")):
                        print("      " + ln[:150])
print(f"(a) files {len(names)} | docstrings differing: {len(diff_files)}")

late = []
for f in names:
    with open(os.path.join(T, f), encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    top = [n for n in tree.body if isinstance(n, ast.Import) and any(a.name == "_repo" for a in n.names)]
    if not top:
        late.append((f, "no top-level import _repo"))
        continue
    at = top[0].lineno
    early = sorted({a.name for n in ast.walk(tree) if isinstance(n, ast.Import) and n.lineno < at for a in n.names
                    if repo_module(a.name)}
                   | {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.lineno < at
                      and n.module and not n.level and repo_module(n.module)})
    if early:
        late.append((f, f"repo imports before _repo (line {at}): {early}"))
for f, why in late:
    print(f"(b) {f}: {why}")
print(f"(b) files {len(names)} | _repo not first: {len(late)}")
