"""THE ak_ RELATION (the reviewer 2026-10-19 07:31 item 2, 08:26 item 2, 08:30). READ ONLY. OFF's rows = ON's rows
minus the rows the life already held. OFF wrote 0 here, so the check is: every one of the ON save's ak_ rows is held
in the OLD saves' ak_ files, N/N. A row is (key, role, o, x, slot) -- the identity write_ak skips on (_AK_CARRIED
holds no signature, R1), so an old file of any signature counts. The ON file's rows are the targets; each old ak_
file is parsed alone and its hits removed from the open set; one parse in memory at a time.
argv: lineage_dir on_ak_file"""
import glob
import json
import os
import sys

LIN, ON = sys.argv[1:3]


def rows(f):
    with open(f, encoding="utf-8") as fh:
        body = json.load(fh)
    return {(e["key"], e["role"], e["o"], e["x"], e["slot"]) for e in body["entries"]}, body.get("sig_arm")


target, sig_on = rows(ON)
n = len(target)
todo = set(target)
olds = sorted(f for f in glob.glob(os.path.join(LIN, "ak_*.json")) if os.path.abspath(f) != os.path.abspath(ON))
print("TARGET", f"rows {n}", f"distinct {len(target)}", f"old ak_ files {len(olds)}", sep="\t", flush=True)
for f in olds:
    have, sig = rows(f)
    hit = todo & have
    todo -= hit
    print("OLD", os.path.basename(f), f"rows {len(have)}", f"hits {len(hit)}", f"same sig_arm {sig == sig_on}",
          f"open {len(todo)}", sep="\t", flush=True)
    del have
print("RESULT", f"held {n - len(todo)}/{n}", f"NOT held {len(todo)}", sep="\t", flush=True)
for r in sorted(todo, key=repr)[:20]:
    print("NOT_HELD", json.dumps(r), sep="\t")
