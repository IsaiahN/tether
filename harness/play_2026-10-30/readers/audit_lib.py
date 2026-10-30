"""Item-1 audit, read-only: every file in TREE/library -- size, sha256, entry counts per top-level
section, the same file on TREE2 (byte-equal or not), and every NON-TEST code line in TREE that
names the file (by its basename). argv: TREE TREE2"""
import hashlib
import json
import os
import re
import sys

TREE, TREE2 = sys.argv[1], sys.argv[2]
LIB = os.path.join(TREE, "library")


def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def counts(p):
    if not p.endswith(".json"):
        with open(p, encoding="utf-8", errors="replace") as fh:
            return {"lines": sum(1 for _ in fh)}
    with open(p, encoding="utf-8") as fh:
        d = json.load(fh)
    if isinstance(d, list):
        return {"<list>": len(d)}
    return {k: (len(v) if isinstance(v, (dict, list)) else type(v).__name__) for k, v in d.items()}


code = []
for root, dirs, files in os.walk(TREE):
    dirs[:] = [d for d in dirs if d not in (".git", ".venv", "__pycache__", "tests", "runs")]
    for f in files:
        if f.endswith(".py"):
            code.append(os.path.join(root, f))
texts = {}
for c in code:
    with open(c, encoding="utf-8", errors="replace") as fh:
        texts[c] = fh.read().splitlines()

for f in sorted(os.listdir(LIB)):
    p = os.path.join(LIB, f)
    if not os.path.isfile(p):
        continue
    p2 = os.path.join(TREE2, "library", f)
    same = os.path.exists(p2) and sha(p2) == sha(p)
    print(f"=== {f}  {os.path.getsize(p):,} B  sha256 {sha(p)[:16]}  other-branch "
          f"{'IDENTICAL' if same else ('DIFFERS' if os.path.exists(p2) else 'ABSENT')}")
    try:
        print("    counts:", json.dumps(counts(p))[:400])
    except Exception as e:  # noqa: BLE001
        print("    counts: unreadable", e)
    pat = re.compile(re.escape(f))
    for c, lines in texts.items():
        rel = os.path.relpath(c, TREE).replace("\\", "/")
        if rel == f"library/{f}":
            continue
        for i, line in enumerate(lines, 1):
            if pat.search(line):
                print(f"    {rel}:{i}: {line.strip()[:150]}")
extra = sorted(set(os.listdir(os.path.join(TREE2, "library"))) - set(os.listdir(LIB)))
print("files only on the other branch:", extra)
