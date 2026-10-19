"""A snapshot's manifest: every file's bytes and sha256, and the totals. argv: dir"""
import hashlib, os, sys
root = sys.argv[1]
n = b = 0
lines = []
for dp, _dn, fn in os.walk(root):
    for f in sorted(fn):
        p = os.path.join(dp, f)
        if os.path.basename(p) == "MANIFEST.tsv":
            continue
        data = open(p, "rb").read()
        n += 1
        b += len(data)
        lines.append(f"{os.path.relpath(p, root)}\t{len(data)}\t{hashlib.sha256(data).hexdigest()}")
open(os.path.join(root, "MANIFEST.tsv"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
print(f"{root}: {n} files, {b} bytes")
