"""The old pool's pre-empty check, part 2, READ ONLY: the tombstone list (docs/tombstones/2026-10-15_old_pool.jsonl)
against the disk. Each entry's holding path present, its bytes and sha256 equal to the list; files in the pool the list
does not name; and every ledger of the list with a row in C:/TETHER_RUNS/LOG_INDEX.jsonl (its summary kept after any
deletion). argv: tombstone_jsonl log_index out_json"""
import ctypes
import hashlib
import json
import os
import sys

sys.dont_write_bytecode = True
ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000)
TOMB, IDX, OUT = sys.argv[1:4]
ROOT = "C:/TETHER_HOLDING/2026-10-16_old_pool"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


rows = [json.loads(x) for x in open(TOMB, encoding="utf-8") if x.strip()]
head, ents = rows[0], rows[1:]
print(f"LIST header files {head.get('files')} bytes {head.get('bytes')}; entries {len(ents)}, bytes "
      f"{sum(e['bytes'] for e in ents)}")
key = lambda p: os.path.normcase(os.path.abspath(p))  # noqa: E731
named = {key(e["holding"]) for e in ents}
missing, size, shabad, ok = [], [], [], 0
for i, e in enumerate(ents):
    p = e["holding"]
    if not os.path.exists(p):
        missing.append(p)
    elif os.path.getsize(p) != e["bytes"]:
        size.append(p)
    elif sha(p) != e["sha256"]:
        shabad.append(p)
    else:
        ok += 1
    if (i + 1) % 200 == 0:
        print(f"  {i + 1} read", flush=True)
extra = []
for root, _d, fs in os.walk(ROOT):
    for f in fs:
        p = os.path.join(root, f)
        if key(p) not in named:
            extra.append(p)
print(f"DISK equal (present, bytes, sha256) {ok} / {len(ents)}; missing {len(missing)} {missing[:3]}; size differs "
      f"{len(size)} {size[:3]}; sha differs {len(shabad)} {shabad[:3]}; files in the pool the list does not name "
      f"{len(extra)} {extra[:3]}")
kinds = {}
for e in ents:
    kinds[e["kind"]] = kinds.get(e["kind"], 0) + 1
idx = set()
with open(IDX, encoding="utf-8") as fh:
    for ln in fh:
        if "2026-10-16_old_pool" in ln:
            idx.add(key(json.loads(ln)["path"]))
led = [e for e in ents if e["kind"] == "ledger"]
unidx = [e["holding"] for e in led if key(e["holding"]) not in idx]
print(f"KINDS {kinds}; ledgers with a LOG_INDEX row {len(led) - len(unidx)} / {len(led)}; without {unidx[:3]}")
cited = sum(1 for e in ents if e.get("n_citations"))
print(f"CITED at the tombstone {cited} / {len(ents)} (n_citations > 0; their citations carried in the list)")
json.dump({"ok": ok, "missing": missing, "size": size, "sha": shabad, "extra": extra, "unindexed": unidx,
           "kinds": kinds}, open(OUT, "w", encoding="utf-8"), indent=1)
