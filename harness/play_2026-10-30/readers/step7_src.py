import json, os, sys
sys.dont_write_bytecode = True
m = json.load(open(sys.argv[1], encoding="utf-8"))
gone = {l.strip().rsplit(".dead-", 1)[0].replace("/", "\\").lower() for l in open(sys.argv[2], encoding="utf-8") if l.strip()}
dst_missing = [e for e in m if not os.path.exists(e["dst"])]
logged = [e for e in dst_missing if e["dst"].lower() in gone]
print("manifest entries", len(m), "bytes", sum(e["bytes"] for e in m), "=", round(sum(e["bytes"] for e in m) / 2**30, 3), "GiB")
print("dst missing", len(dst_missing), round(sum(e["bytes"] for e in dst_missing) / 2**30, 3), "GiB; of them in the deleted list (deleteB, LOG_REMOVALS)", len(logged), "; NOT logged", len(dst_missing) - len(logged))
src = [e["src"] for e in m]
print("manifest src present now", sum(os.path.exists(s) for s in src), "/", len(src))
roots = sorted({s.split("\runs\\")[0] for s in src})
print(len(roots), "source roots; present now", sum(os.path.isdir(r) for r in roots), roots[:3])
