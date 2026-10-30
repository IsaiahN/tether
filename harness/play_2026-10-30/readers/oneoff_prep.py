"""r342 1(c): the one-off after-check's inputs, beside round_01 (which is left as it is): names_before minus
EXACTLY memory.db-shm and memory.db-wal, and copies of stream.result.json and sup/sup.json. argv: play dir."""
import json
import os
import shutil
import sys

sys.dont_write_bytecode = True
P = sys.argv[1]
src, dst = os.path.join(P, "round_01"), os.path.join(P, "round_01_oneoff_r342")
assert not os.path.exists(dst), "the one-off dir exists"
os.makedirs(os.path.join(dst, "sup"))
before = json.load(open(os.path.join(src, "names_before.json"), encoding="utf-8"))
drop = {"memory.db-shm", "memory.db-wal"}
assert drop <= set(before), ("both names in names_before", sorted(drop - set(before)))
kept = [n for n in before if n not in drop]
assert len(kept) == len(before) - 2
with open(os.path.join(dst, "names_before.json"), "w", encoding="utf-8", newline="\n") as fh:
    json.dump(kept, fh)
shutil.copy2(os.path.join(src, "stream.result.json"), os.path.join(dst, "stream.result.json"))
shutil.copy2(os.path.join(src, "sup", "sup.json"), os.path.join(dst, "sup", "sup.json"))
print(f"names_before {len(before)} -> {len(kept)} (dropped exactly {sorted(drop)}); copied stream.result.json, sup/sup.json")
