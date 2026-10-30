"""One verified backup of a finished run directory (the reviewer r286: sizes and hashes). Copies every file,
hashes source and copy, refuses on any mismatch, writes the manifest, marks the copy read-only, appends the
RESTORE_LOG row. Refuses while the chain could still write (no PLAY_END line). argv: run dir, utc stamp, note."""
import hashlib
import os
import shutil
import stat
import sys

sys.dont_write_bytecode = True
src, stamp, note = sys.argv[1].rstrip("/"), sys.argv[2], sys.argv[3]
DST = f"{src}.bak-{stamp}"
MAN = f"{DST}.manifest.tsv"
LOG = "C:/TETHER_RUNS/RESTORE_LOG.tsv"
assert not os.path.exists(DST) and not os.path.exists(MAN), "the backup target exists"
assert "PLAY_END" in open(f"{src}/chain.log", encoding="utf-8").read(), "the chain has not ended"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


rows, total, n_files = [], 0, 0
for root, dirs, files in os.walk(src):
    dirs.sort()
    rel = os.path.relpath(root, src)
    os.makedirs(os.path.join(DST, rel), exist_ok=True)
    for n in sorted(files):
        s, d = os.path.join(root, n), os.path.join(DST, rel, n)
        shutil.copy2(s, d)
        a, b = sha(s), sha(d)
        assert a == b and os.path.getsize(s) == os.path.getsize(d), f"copy differs: {s}"
        rows.append(f"{os.path.join(rel, n).replace(os.sep, '/')}\t{os.path.getsize(s)}\t{a}")
        total += os.path.getsize(s)
        n_files += 1
text = "\n".join(rows) + "\n"
with open(MAN, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(text)
msha = hashlib.sha256(text.encode()).hexdigest()[:16]
for root, _dirs, files in os.walk(DST):
    for n in files:
        os.chmod(os.path.join(root, n), stat.S_IREAD)
with open(LOG, "a", encoding="utf-8", newline="\n") as fh:
    fh.write(f"{stamp}\tbackup\t{src}\t{DST} files {n_files} bytes {total} manifest "
             f"{os.path.basename(MAN)} sha {msha} ({note}); read-only\n")
print(f"RUNDIR BACKUP OK {DST} files {n_files} bytes {total} manifest sha {msha}")
