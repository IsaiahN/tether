"""Scratch: compare the dumped ON/OFF ledgers. Strip the added rows/fields, then list every
(event, field) that still differs, with the first example, after mapping ON positions to OFF.
argv: scratch dir, draft tree"""
import collections
import json
import os
import sys

S, tree = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(tree, "tests"))
sys.dont_write_bytecode = True
import test_r4_record as t  # noqa: E402

on = json.load(open(os.path.join(S, "r4_rows_1.json"), encoding="utf-8"))
off = json.load(open(os.path.join(S, "r4_rows_0.json"), encoding="utf-8"))
print("rows on", len(on), "off", len(off))
print("seq contiguous off:", [r.get("seq") for r in off[:3]], off[-1].get("seq"), len(off))
kept = [r for r in on if r["event"] not in t.ADDED_ROWS]
print("kept on", len(kept))
added_seqs = sorted(r["seq"] for r in on if r["event"] in t.ADDED_ROWS)


def pos(p):
    """an ON ledger position -> the OFF position: the non-added ON rows before it"""
    import bisect
    return p - bisect.bisect_left(added_seqs, p)


diffs = collections.Counter()
ex = {}
for a, b in zip(off, kept, strict=False):
    if (a["cycle"], a["step"], a["slot"], a["event"]) != (b["cycle"], b["step"], b["slot"], b["event"]):
        print("ROW KEY DIFF", a["seq"], (a["cycle"], a["step"], a["slot"], a["event"]),
              (b["cycle"], b["step"], b["slot"], b["event"]))
        break
    da, db = dict(a["detail"]), dict(b["detail"])
    for k in t.ADDED_FIELDS.get(a["event"], ()):
        db.pop(k, None)
    for k in set(da) | set(db):
        if k in ("wall_s", "overrun_s") or a["event"] == "arms":
            continue
        if da.get(k) != db.get(k):
            diffs[(a["event"], k)] += 1
            ex.setdefault((a["event"], k), (a["seq"], json.dumps(da.get(k))[:200],
                                            json.dumps(db.get(k))[:200]))
for k, n in sorted(diffs.items()):
    print(n, k, ex[k])
# does pos() explain the int-valued diffs?
for k in diffs:
    print("--", k)
