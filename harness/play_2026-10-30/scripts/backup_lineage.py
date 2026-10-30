"""One verified backup of the lineage (the standing rule: one per test, every earlier kept, a RESTORE_LOG row).
Copies every file, hashes source and copy, refuses on any mismatch, writes the manifest, marks the copy
read-only, appends the RESTORE_LOG row. argv: utc stamp, expected head (16 hex), note."""
import hashlib
import os
import shutil
import stat
import sys

sys.dont_write_bytecode = True
stamp, head, note = sys.argv[1], sys.argv[2], sys.argv[3]
SRC = "C:/TETHER_RUNS/E4_2026-10-18/lineage"
DST = f"C:/TETHER_RUNS/E4_2026-10-18/lineage.bak-{stamp}"
MAN = f"{DST}.manifest.tsv"
LOG = "C:/TETHER_RUNS/RESTORE_LOG.tsv"
assert not os.path.exists(DST) and not os.path.exists(MAN), "the backup target exists"
names = sorted(os.listdir(SRC))
assert any(n.startswith(f"gen_{head}") for n in names), f"gen_{head} is not in the lineage"
for n in ("memory.db-wal", "memory.db-shm", "memory.db-journal"):
    assert n not in names, f"{n} present: the store is open or was not closed cleanly"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


os.makedirs(DST)
rows, total = [], 0
for n in names:
    s, d = os.path.join(SRC, n), os.path.join(DST, n)
    assert os.path.isfile(s), f"not a file: {n}"
    shutil.copy2(s, d)
    a, b = sha(s), sha(d)
    assert a == b and os.path.getsize(s) == os.path.getsize(d), f"copy differs: {n}"
    rows.append(f"{n}\t{os.path.getsize(s)}\t{a}")
    total += os.path.getsize(s)
assert sorted(os.listdir(DST)) == names, "file lists differ"
text = "\n".join(rows) + "\n"
with open(MAN, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(text)
msha = hashlib.sha256(text.encode()).hexdigest()[:16]
for n in names:
    os.chmod(os.path.join(DST, n), stat.S_IREAD)
with open(LOG, "a", encoding="utf-8", newline="\n") as fh:
    fh.write(f"{stamp}\tbackup\t{SRC}\t{DST} files {len(names)} bytes {total} manifest "
             f"lineage.bak-{stamp}.manifest.tsv sha {msha} head {head} ({note}); read-only; "
             f"every earlier backup kept\n")
print(f"BACKUP OK {DST} files {len(names)} bytes {total} manifest sha {msha} head {head}")
