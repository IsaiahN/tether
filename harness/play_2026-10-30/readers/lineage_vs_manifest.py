"""Read-only, bytes only (never sqlite): every file in the live lineage hashed and compared with a
backup's manifest (name, size, sha256). Reports files equal / differing / only-live / only-backup, and
the live folder's extra wal/shm/journal files with their sizes. argv: lineage dir, manifest path."""
import hashlib
import os
import sys

sys.dont_write_bytecode = True
d, man = sys.argv[1], sys.argv[2]
want = {}
for ln in open(man, encoding="utf-8"):
    parts = ln.rstrip("\n").split("\t")
    if len(parts) == 3:
        want[parts[0]] = (int(parts[1]), parts[2])
live = {}
for name in sorted(os.listdir(d)):
    p = os.path.join(d, name)
    if os.path.isfile(p):
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        live[name] = (os.path.getsize(p), h.hexdigest())
same = [n for n in want if n in live and live[n] == want[n]]
diff = [n for n in want if n in live and live[n] != want[n]]
only_live = [n for n in live if n not in want]
only_bak = [n for n in want if n not in live]
print(f"manifest {len(want)} files, {sum(v[0] for v in want.values())} bytes")
print(f"live {len(live)} files, {sum(v[0] for v in live.values())} bytes")
print(f"equal {len(same)}; differing {len(diff)} {diff[:5]}; only live {only_live}; only backup "
      f"{only_bak[:5]}")
for n in only_live:
    print(f"  only live: {n} {live[n][0]} bytes")
