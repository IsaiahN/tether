"""Item-1 integrity checks, read-only, independent of the reviewer's: refs resolve, keys agree,
the index covers every entry, the dedup log's removed names are gone, status / bond tallies, and
the open-item counts. argv: TREE"""
import json
import os
import sys
from collections import Counter

L = os.path.join(sys.argv[1], "library")


def j(n):
    with open(os.path.join(L, n), encoding="utf-8") as fh:
        return json.load(fh)


atoms, mols = j("atoms.json")["atoms"], j("molecules.json")["molecules"]
agent, rels = j("agent_atoms.json")["atoms"], j("relations.json")["relations"]
idx, tag, grid = j("index.json"), j("tag_index.json"), j("grid_groundings.json")
rex, ded, roles = j("reads_explicit.json"), j("DEDUP_LOG.json"), j("ROLES_LOG.json")
orient, readings = j("orientation_draft.json"), j("readings.json")["readings"]
keys = set(atoms) | set(mols) | set(agent) | {f"RELATION|{n}" for n in rels}
print("entries: atoms", len(atoms), "molecules", len(mols), "agent", len(agent), "relations",
      len(rels), "union", len(keys), "overlaps", len(atoms) + len(mols) + len(agent) + len(rels) - len(keys))
bad_ing = [(k, i.get("ref")) for k, m in mols.items() for i in m.get("ingredients", ())
           if i.get("ref") not in keys]
bad_calls = [(k, c) for k, m in mols.items() for c in m.get("calls", ()) if c not in keys]
print("molecule ingredient refs not resolving:", len(bad_ing), bad_ing[:3])
print("molecule calls not resolving:", len(bad_calls), bad_calls[:3])
print("grid_groundings keys == atoms keys:", set(grid) == set(atoms), len(grid), len(atoms),
      "extra", sorted(set(grid) - set(atoms))[:3], "missing", sorted(set(atoms) - set(grid))[:3])
rr = rex.get("reads", {})
bad_rex_k = [k for k in rr if k not in keys]
bad_rex_r = sorted({r for v in rr.values() for r in (v if isinstance(v, list) else v.get("reads", []))
                    if isinstance(r, str) and r not in readings})
print("reads_explicit:", len(rr), "keys not resolving", len(bad_rex_k), bad_rex_k[:3],
      "readings not in readings.json", len(bad_rex_r), bad_rex_r[:5])
covered = set(idx.get("by_kind", {}).get("PERCEPT", [])) if isinstance(idx.get("by_kind"), dict) else set()
bk = idx.get("by_kind", {})
allk = set()
for v in bk.values():
    allk |= set(v if isinstance(v, list) else v.keys())
print("index.by_kind kinds:", {k: len(v) for k, v in bk.items()}, "| covers atoms",
      len(set(atoms) & allk), "molecules", len(set(mols) & allk), "agent", len(set(agent) & allk),
      "| keys in by_kind not held", len(allk - keys))
dangling_tag = set()
for v in tag.get("by_tag", {}).values():
    for kind_list in (v.values() if isinstance(v, dict) else [v]):
        dangling_tag |= {x for x in kind_list if isinstance(x, str) and "|" in x and x not in keys}
print("tag_index.by_tag names not held:", len(dangling_tag), sorted(dangling_tag)[:3])
removed = ded.get("removed", [])
rn = [r.get("removed") or r.get("key") or r.get("name") if isinstance(r, dict) else r for r in removed]
still = [x for x in rn if x in keys]
print("DEDUP_LOG.removed:", len(removed), "still present:", len(still), still[:3],
      "| sample", json.dumps(removed[:1])[:200])
print("DEDUP_LOG held_for_ruling", len(ded.get("held_for_ruling", [])), "unresolved_pairs",
      json.dumps(ded.get("unresolved_pairs"))[:300])
print("atom status:", dict(Counter(a.get("status") for a in atoms.values())))
print("molecule bond_status:", dict(Counter(m.get("bond_status") for m in mols.values())))
print("ROLES_LOG: assigned", len(roles.get("roles_assigned", [])), "unclassified",
      len(roles.get("unclassified", [])))
print("orientation_draft molecules", len(orient.get("molecules", {})), "of which in molecules.json",
      len(set(orient.get("molecules", {})) & set(mols)))
none_keys = [k for k in keys if k.startswith("None|")]
print("held keys starting None|:", none_keys)
print("identity_candidates:", len(idx.get("identity_candidates", [])),
      "| None| in them:", [x for x in idx.get("identity_candidates", []) if "None|" in json.dumps(x)][:2])
print("readings.json readings:", len(readings))
