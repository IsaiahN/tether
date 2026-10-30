"""Scratch: run test_r4_record's two children once (draft tree) and keep both ledgers, so the
position mapping is worked out offline. argv: draft tree, out dir."""
import json
import os
import sys

tree, out = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(tree, "tests"))
sys.dont_write_bytecode = True
import test_r4_record as t  # noqa: E402

for arm in ("1", "0"):
    rows = t.child(arm)
    with open(os.path.join(out, f"r4_rows_{arm}.json"), "w", encoding="utf-8") as fh:
        json.dump(rows, fh)
    print(arm, len(rows))
