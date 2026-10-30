"""Isaiah 2026-10-08: atoms act as noun or verb by position (effect / affect). The held pairs are
re-expressed as ONE base entry plus a ROLE: the long form gains `role_of` {base, role, marker}.
Nothing is deleted. Markers that are only a domain tag or a cut-off word are listed, not guessed.
Also applies orientation_draft.json (status: draft for Isaiah)."""
import json
ROLE_OF_MARKER = {
 "PROCESS": "flow cascade process loop cycle formation transfer update build spread habituation feedback delay windup break switch override contagion escalation development growth".split(),
 "CAUSE": "drive urge cue signal call thrill trigger source".split(),
 "RESULT": "effect wins outcome consequence".split(),
 "MEASURE": "rate freq frequency limit threshold reach field fatigue capacity level degree".split(),
 "TEST": "test check judge analysis calc inquiry assessment".split(),
 "INSTRUMENT": "material grammar map tool device mechanism".split(),
 "RELATION": "bind network net link relationship".split(),
 "STATE": "crisis dilemma anxiety lock hold maintenance burden situation task".split(),
 "RULE": "law heuristic pattern principle theorem".split(),
 "AGENT": "carver maker".split(),
}
MARK = {w: r for r, ws in ROLE_OF_MARKER.items() for w in ws}
A = json.load(open("atoms.json")); M = json.load(open("molecules.json")); L = json.load(open("DEDUP_LOG.json"))
E = {**A["atoms"], **M["molecules"]}
done, unclassified = [], []
for h in L["held_for_ruling"]:
    a, b = h["pair"]
    if a not in E or b not in E:
        continue
    s, l = (a, b) if len(E[a]["name"]) <= len(E[b]["name"]) else (b, a)
    rest = E[l]["name"][len(E[s]["name"]):].strip()
    first = rest.lower().split()[0] if rest else ""
    role = MARK.get(first)
    if role:
        E[l]["role_of"] = {"base": s, "role": role, "marker": rest, "status": "draft (reviewer 2026-10-08)"}
        done.append((s, l, role))
    else:
        unclassified.append({"pair": [s, l], "added": rest})
O = json.load(open("orientation_draft.json"))["molecules"]
for k, o in O.items():
    e = M["molecules"][k]
    e["orientation"] = {**o, "status": "draft (reviewer 2026-10-08) for Isaiah to confirm"}
    if o.get("role_of"):
        e["role_of"] = {"base": o["role_of"], "role": o["role"], "marker": "", "status": "draft (reviewer 2026-10-08)"}
    if "operands" in o:
        e["run"]["operands"] = [{"ref": r, **({"qual": q} if q else {})} for r, q in o["operands"]]
        e["run"]["junctions"] = list(o["junctions"])
        e["run"]["junction_source"] = "orientation draft 2026-10-08 (pending Isaiah)"
json.dump(A, open("atoms.json", "w"), ensure_ascii=False, indent=1)
json.dump(M, open("molecules.json", "w"), ensure_ascii=False, indent=1)
json.dump({"roles_assigned": done, "unclassified": unclassified}, open("ROLES_LOG.json", "w"), ensure_ascii=False, indent=1)
print("roles assigned", len(done), "| unclassified", len(unclassified), "| oriented", len(O))
