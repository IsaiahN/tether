"""S5's WAL MEASUREMENT (the reviewer 2026-10-19 07:12 c, 07:19 3, 08:03 3b): the read cost through a growing WAL, and
its memory, so the WAL's SIZE bound can be derived (from B and this curve) rather than picked. Every *.json of a
lineage archive is hard-linked (never copied, never written) into an empty scratch folder; an empty store is opened
there (lineage_store.open_store: WAL, autocheckpoint 0) and the saves are merged ONE AT A TIME in chain order with NO
checkpoint, as a long game's saves without a sleep would leave it. After each merge, and once more after a final
TRUNCATE checkpoint (the WAL = 0 baseline over the same rows), it records: the WAL's bytes and frames, the -shm
bytes, this process's private bytes, and three fixed reads timed -- (A) 20,000 asked_tally point lookups by key,
drawn once with random.Random(20261019) from the keys present after the LAST save and reused at every point (keys
not yet merged are absent-key lookups, counted apart); (B) the whole pair table; (C) the largest dk cluster's
kind_dk rows by dk IN (...), the cluster fixed at the end and its ids reused. Each read is run twice per point and
both times kept (first and second). Output: rows to <out>/wal_curve.tsv.
argv: repo lineage_dir out_dir"""
import ctypes
import ctypes.wintypes as wt
import json
import os
import random
import sys
import time

REPO, LIN, OUT = sys.argv[1:4]
sys.path = [p for p in sys.path if "scratchpad" not in p]
sys.path.insert(0, REPO)
import lineage_store as ls  # noqa: E402


class _PMC(ctypes.Structure):
    _fields_ = [("cb", wt.DWORD), ("PageFaultCount", wt.DWORD),
                *((n, ctypes.c_size_t) for n in (
                    "PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage", "QuotaPagedPoolUsage",
                    "QuotaPeakNonPagedPoolUsage", "QuotaNonPagedPoolUsage", "PagefileUsage", "PeakPagefileUsage"))]


_k32, _ps = ctypes.WinDLL("kernel32"), ctypes.WinDLL("psapi")
_k32.GetCurrentProcess.restype = wt.HANDLE
_ps.GetProcessMemoryInfo.argtypes = [wt.HANDLE, ctypes.POINTER(_PMC), wt.DWORD]


def private_bytes() -> int:
    c = _PMC()
    c.cb = ctypes.sizeof(_PMC)
    _ps.GetProcessMemoryInfo(_k32.GetCurrentProcess(), ctypes.byref(c), c.cb)
    return int(c.PagefileUsage)


assert not os.path.exists(OUT), "the scratch folder must not exist"
ARCH = os.path.join(OUT, "arch")
os.makedirs(ARCH)
for f in sorted(os.listdir(LIN)):
    if f.endswith(".json"):
        os.link(os.path.join(LIN, f), os.path.join(ARCH, f))
con = ls.open_store(ARCH)
pending = ls.unmerged(con, ARCH)
parent = {}
for h in pending:
    with open(os.path.join(ARCH, f"gen_{h}.json"), encoding="utf-8") as fh:
        parent[h] = json.load(fh).get("parent")
order, last = [], None
while parent:
    nxt = [h for h, q in parent.items() if q == last]
    assert len(nxt) == 1, f"{len(nxt)} saves continue the chain"
    order.append(nxt[0])
    last = nxt[0]
    del parent[last]
print("ORDER", len(order), "saves", flush=True)
rows: list = []
keys = cluster = None


def reads(tag: str, k: int) -> None:
    wal = ls.wal_bytes(ARCH)
    shm = os.path.join(ARCH, f"{ls.DB}-shm")
    rec = {"point": tag, "saves": k, "wal_bytes": wal, "wal_frames": max(0, (wal - 32) // (4096 + 24)),
           "shm_bytes": os.path.getsize(shm) if os.path.exists(shm) else 0, "private_bytes": private_bytes()}
    for rep in ("first", "second"):
        t0 = time.perf_counter()
        hit = sum(1 for kk in keys if con.execute(
            "SELECT 1 FROM asked_tally WHERE entry=? AND role=? AND slot_class=?", kk).fetchone())
        rec[f"A_us_{rep}"] = round((time.perf_counter() - t0) / len(keys) * 1e6, 2)
        rec["A_hits"] = hit
        t0 = time.perf_counter()
        rec["B_rows"] = len(con.execute("SELECT * FROM pair").fetchall())
        rec[f"B_s_{rep}"] = round(time.perf_counter() - t0, 4)
        t0 = time.perf_counter()
        rec["C_rows"] = len(con.execute(f"SELECT * FROM kind_dk WHERE dk IN ({','.join('?' * len(cluster))})",
                                        cluster).fetchall())
        rec[f"C_s_{rep}"] = round(time.perf_counter() - t0, 4)
    rows.append(rec)
    print("POINT", json.dumps(rec), flush=True)


merge_s = []
for h in order:
    with open(os.path.join(ARCH, f"gen_{h}.json"), encoding="utf-8") as fh:
        g = json.load(fh)
    t0 = time.perf_counter()
    ls.merge_save(con, ARCH, h, g)
    merge_s.append(round(time.perf_counter() - t0, 3))
    del g
# the keys and the cluster are fixed from the FINAL store, then the curve is walked by re-merging
all_keys = con.execute("SELECT entry, role, slot_class FROM asked_tally").fetchall()
keys = random.Random(20261019).sample(all_keys, min(20000, len(all_keys)))
sym = dict(con.execute("SELECT id, s FROM sym"))
by: dict = {}
for (dk,) in con.execute("SELECT DISTINCT dk FROM kind_dk"):
    try:
        d = json.loads(sym[dk])
    except (ValueError, KeyError):
        continue
    if isinstance(d, list) and d:
        by.setdefault(str(d[0]), []).append(dk)
cluster = max(by.values(), key=len)
con.close()
print("FIXED", f"keys {len(keys)}", f"cluster dk ids {len(cluster)}", f"merge_s {merge_s}", flush=True)
# second pass, the measured one: a fresh store in its OWN folder (pass 1's is kept, never deleted),
# the same order, a reading after every merge
ARCH = os.path.join(OUT, "arch2")
os.makedirs(ARCH)
for f in sorted(os.listdir(LIN)):
    if f.endswith(".json"):
        os.link(os.path.join(LIN, f), os.path.join(ARCH, f))
con = ls.open_store(ARCH)
for k, h in enumerate(order, 1):
    with open(os.path.join(ARCH, f"gen_{h}.json"), encoding="utf-8") as fh:
        g = json.load(fh)
    ls.merge_save(con, ARCH, h, g)
    del g
    reads(f"after_save_{k}", k)
t0 = time.perf_counter()
con.execute("PRAGMA wal_checkpoint(TRUNCATE)")
print("CHECKPOINT_S", round(time.perf_counter() - t0, 3), flush=True)
reads("after_checkpoint", len(order))
cols = list(rows[0])
with open(os.path.join(OUT, "wal_curve.tsv"), "w", encoding="utf-8") as fh:
    fh.write("\t".join(cols) + "\n")
    for r in rows:
        fh.write("\t".join(str(r.get(c, "")) for c in cols) + "\n")
con.close()
