"""PF's write check, between two games on the REAL lineage (the reviewer 2026-10-23 00:20 (i)). Byte reads only: the folder
is listed, and only the gen_ files the game added are read (rb), as the loader reads them (zlib or plain bytes, the name
hash = sha256 of the bytes [:16]); memory.db* is never opened.
  before LIN OUT              OUT/names_before.json = the folder's names
  after  LIN OUT GAME HEAD    the game's write VERIFIED, else rc 3: result.json readable with an empty error; the
                              supervisor's ending EXIT; the gen_ files added since names_before each decode and hash to
                              their names; they form ONE chain whose first parent is HEAD (the last verified head) and
                              whose tip is the generation result.json names. OUT/write_check.json holds the reading;
                              OUT/../head.txt the new head (written only when verified)."""
import hashlib
import json
import os
import re
import sys
import zlib

sys.dont_write_bytecode = True
MODE, LIN, OUT = sys.argv[1:4]
if MODE == "before":
    with open(os.path.join(OUT, "names_before.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(sorted(os.listdir(LIN)), fh)
    print(f"BEFORE {len(os.listdir(LIN))} names")
    sys.exit(0)
assert MODE == "after", MODE
GAME, HEAD = sys.argv[4:6]
before = set(json.load(open(os.path.join(OUT, "names_before.json"), encoding="utf-8")))
names = os.listdir(LIN)
added = sorted(n for n in names if n not in before)
gone = sorted(n for n in before if n not in set(names))
why = []
try:
    res = json.load(open(os.path.join(OUT, f"{GAME}.result.json"), encoding="utf-8"))
except Exception as x:  # noqa: BLE001 -- no result row is the reading
    res = None
    why.append(f"no readable result.json: {x!r}")
try:
    sup = json.load(open(os.path.join(OUT, "sup", "sup.json"), encoding="utf-8"))
except Exception as x:  # noqa: BLE001
    sup = {}
    why.append(f"no readable sup.json: {x!r}")
if res is not None and res.get("error") not in (None, ""):
    why.append(f"result.json error: {res.get('error')}")
if sup.get("ending") != "EXIT":
    why.append(f"supervisor ending {sup.get('ending')}")
m = re.search(r"'hash': '([0-9a-f]{16})'", str((res or {}).get("lineage") or ""))
wrote = m.group(1) if m else None
gens, bad = {}, []
for n in added:
    if not n.startswith("gen_"):
        continue
    raw = open(os.path.join(LIN, n), "rb").read()
    try:
        b = zlib.decompress(raw) if raw[:1] == b"\x78" else raw
        h = hashlib.sha256(b).hexdigest()[:16]
        if n != f"gen_{h}.json":
            bad.append((n, f"hashes to {h}"))
            continue
        gens[h] = json.loads(b)
    except Exception as x:  # noqa: BLE001 -- a generation that does not decode is the reading
        bad.append((n, repr(x)[:120]))
kids = {g.get("parent"): h for h, g in gens.items()}
roots = [h for h, g in gens.items() if g.get("parent") not in gens]
chain, h = [], (roots[0] if len(roots) == 1 else None)
while h is not None and len(chain) <= len(gens):
    chain.append(h)
    h = kids.get(h)
if bad:
    why.append(f"generations that do not verify: {bad}")
if gone:
    why.append(f"names gone from the folder: {gone[:5]}")
if not gens:
    why.append("no generation written")
elif len(chain) != len(gens):
    why.append(f"the new generations are not one chain: roots {roots}")
else:
    if gens[chain[0]].get("parent") != HEAD:
        why.append(f"the chain's first parent {gens[chain[0]].get('parent')} is not the last head {HEAD}")
    if chain[-1] != wrote:
        why.append(f"the chain's tip {chain[-1]} is not the generation result.json names ({wrote})")
ok = not why
rec = {"game": GAME, "head_in": HEAD, "added": added, "chain": chain, "wrote": wrote, "verified": ok, "why": why}
with open(os.path.join(OUT, "write_check.json"), "w", encoding="utf-8", newline="\n") as fh:
    json.dump(rec, fh, indent=1)
if ok:
    with open(os.path.join(os.path.dirname(OUT), "head.txt"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(chain[-1] + "\n")
print(f"{'WRITE VERIFIED' if ok else 'WRITE NOT VERIFIED'} {GAME}: head {HEAD} -> chain {chain}; added "
      f"{len(added)} names; why {why}")
sys.exit(0 if ok else 3)
