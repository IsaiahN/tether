"""Pass 4, read by eye (reviewer, 2026-10-08): same recipe, and the names are one name misspelled,
respelled, abbreviated or retitled. KEEP -> DROP. Same mechanics as dedup_2026_10_08.py:
references remapped, the dropped name kept as an alias, the move logged in DEDUP_LOG.json."""
import json
PAIRS = [  # (keep, drop)
 ("ALEATORY|Laplace's demon", "ALEATORY|Bell laplace demon"),
 ("ALEATORY|Law of large numbers", "ALEATORY|Law large numbers"),
 ("ALEATORY|The die is cast", "ALEATORY|The dice is cast"),
 ("ATMOSPHERIC|El Niño", "ATMOSPHERIC|El nino"),
 ("ATMOSPHERIC|La Niña", "ATMOSPHERIC|La nina"),
 ("AUTOMATON|Emergent automaton", "AUTOMATON|Emergent aut"),
 ("AUTOMATON|Process optimisation", "AUTOMATON|Process optimization"),
 ("CHARACTER|Reputation build", "CHARACTER|Rep build"),
 ("CHARACTER|The hero's journey", "CHARACTER|The heroes journey"),
 ("CURIOSITY|The discovery euphoria", "CURIOSITY|The discovery europhoria"),
 ("CYBERNETIC|Gain tuning", "CYBERNETIC|Gain tune"),
 ("LEARNING|Fixed vs growth mindset", "LEARNING|Fixed growth"),
 ("LEARNING|Reflect", "LEARNING|Reflect lea"),
 ("LOGISTICAL|Inventory optimisation", "LOGISTICAL|Inventory optimization"),
 ("LUDOLOGICAL|Metagame theory", "LUDOLOGICAL|Meta game theory"),
 ("MATERIAL|Viscoelasticity", "MATERIAL|Viscelasticity"),
 ("MEDICAL|Precision medicine", "MEDICAL|The precision medicine"),
 ("NUTRITIONAL|Fermentation", "NUTRITIONAL|Ferment nut"),
 ("OPTICAL|Planck constant", "OPTICAL|Plank constant"),
 ("PHENOMENOLOGICAL|The other's interiority", "PHENOMENOLOGICAL|The other's innerity"),
 ("SOCIAL|Norm enforcement", "SOCIAL|Normling"),
 ("SOCIAL|Wisdom of crowds", "SOCIAL|Wisdom crowds"),
 ("TOPOLOGICAL|Fractalise", "TOPOLOGICAL|Fractalize top"),
 ("ZOOLOGICAL|Thanatosis", "ZOOLOGICAL|UNGRATEFUL DEAD (Thanatosis)"),
]
A = json.load(open("atoms.json")); M = json.load(open("molecules.json")); L = json.load(open("DEDUP_LOG.json"))
atoms, mols = A["atoms"], M["molecules"]
remap = {}
for keep, drop in PAIRS:
    e = mols.pop(drop)
    t = mols[keep]
    t.setdefault("aliases", []).append(e["name"])
    t.setdefault("merged_from", []).append({"key": drop, "why": "same recipe; one name misspelled or retitled (read by eye)", "by": "Isaiah 2026-10-08"})
    if len(e.get("definition") or "") > len(t.get("definition") or ""):
        t["definition_long"] = e["definition"]
    remap[drop] = keep
    L["removed"].append({"removed": drop, "kept": keep, "why": "same recipe, name misspelled or retitled (pass 4, by eye)"})
# Reflect's recipe named itself in the source (Reflect = Reflect + Process + Insight): the self-operand is dropped
r = mols["LEARNING|Reflect"]
r["ingredients"] = [i for i in r["ingredients"] if i["ref"] != "LEARNING|Reflect"]
r["source_defect"] = "the source recipe named itself (Reflect + Process + Insight); the self-operand is dropped"
L.setdefault("self_reference_dropped", []).append({"molecule": "LEARNING|Reflect", "dropped_operand": "LEARNING|Reflect", "why": "source recipe names itself"})
keys = set(atoms) | set(mols)
for store in (atoms, mols):
    for k, e in store.items():
        for i in e.get("ingredients", []):
            if i["ref"] in remap:
                i["was"], i["ref"] = i["ref"], remap[i["ref"]]
        for f in ("used_by", "called_by", "calls"):
            if isinstance(e.get(f), list):
                e[f] = list(dict.fromkeys(x2 for x2 in (remap.get(x, x) for x in e[f]) if x2 in keys and x2 != k))
        for i in e.get("ingredients", []):
            assert i["ref"] in keys, (k, i)
json.dump(A, open("atoms.json", "w"), ensure_ascii=False, indent=1)
json.dump(M, open("molecules.json", "w"), ensure_ascii=False, indent=1)
json.dump(L, open("DEDUP_LOG.json", "w"), ensure_ascii=False, indent=1)
print("pass 4 removed", len(PAIRS), "| molecules now", len(mols), "| total removed", len(L["removed"]))
