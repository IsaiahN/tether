"""OFF identity for the Kaggle deletion: the same fixed FakeWrapper run (test_route_refuse's own PLAIN
probe and child: TETHER_AGENT_SEED=0, PYTHONHASHSEED=0, no TETHER_* arms) in the BASE tree and the
CURRENT tree, every ledger row compared by conform/identity_mod_rows.compare. The arms row's tree
provenance is dropped by name; its ON / OFF switch lists are ASSERTED equal (the deletion moves no
switch). argv: BASE_TREE CUR_TREE STEPS"""
import sys

sys.dont_write_bytecode = True
BASE, CUR, STEPS = sys.argv[1], sys.argv[2], int(sys.argv[3])
sys.path[:0] = [CUR, CUR + "/tests", CUR + "/conform"]
import test_route_refuse as t  # noqa: E402
from identity_mod_rows import compare  # noqa: E402

base = t.child(t.PLAIN, BASE, None, STEPS)["rows"]
cur = t.child(t.PLAIN, CUR, None, STEPS)["rows"]
tree_ids = ("blob_n_files", "dirty", "files_blob", "files_sha", "git_unknown", "head", "tree")
arms = [next(r["detail"] for r in rows if r["slot"] == "@run" and r["event"] == "arms")
        for rows in (base, cur)]
on = [set(a.get("on") or ()) for a in arms]
off = [set(a.get("off") or ()) for a in arms]
print(f"arms: ON {len(on[0])} / {len(on[1])}, OFF {len(off[0])} / {len(off[1])}, ON diff "
      f"{sorted(on[0] ^ on[1])}, OFF diff {sorted(off[0] ^ off[1])}")
assert on[0] == on[1] and off[0] == off[1], "the switch lists differ"
for a in arms:
    for k in tree_ids + ("on", "off"):
        a.pop(k, None)
bad = compare(base, cur, set())
print(f"OFF identity: {len(base)} base rows, {len(cur)} current, {min(len(base), len(cur))} "
      f"compared, {len(bad)} differing" + "".join(f"\n  {x}" for x in bad[:20]))
assert len(base) > 50 and not bad
print("kdel_identity: OK")
