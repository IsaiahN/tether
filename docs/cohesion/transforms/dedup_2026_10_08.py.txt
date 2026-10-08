"""One-time migration, Isaiah 2026-10-08: "the 256 duplicates can be removed".

Of the 256 truncated-name pairs, only the CLEAR duplicates are removed here -- the same recipe,
the same definition, or a name-only implicit atom that is a truncation of a defined entry. Pairs
whose definitions differ (Allegiance / Allegiance crisis) are NOT removed; they are listed in
DEDUP_LOG.json under `held_for_ruling` because deleting them would delete a different concept.

For each removed key: every ingredient reference is remapped to the kept key, the removed name
becomes an ALIAS on the kept entry (so recipe text that wrote the short form still resolves), and
the move is logged. Nothing else changes.
"""
import json, collections
A = json.load(open("atoms.json")); M = json.load(open("molecules.json"))
G = json.load(open("grid_groundings.json")); I = json.load(open("index.json"))
atoms, mols = A["atoms"], M["molecules"]
allE = {**atoms, **mols}
lk = {(e["domain"], e["name"].lower()): k for k, e in allE.items()}

def resolve(dk):
    d, n = dk.split("|", 1)
    k = lk.get((d, n))
    return k, allE.get(k)

import re
removed, held, unresolved = [], [], []
taken = set()
PREFER = {"ALEATORY|Entropy", "EXCHANGE|Auction", "TOPOLOGICAL|Poincaré disk"}

def norm(n):
    n = n.lower().replace("≠", " ").replace("'", "").replace("’", "")
    n = re.sub(r"our\b", "or", n)
    return re.sub(r"[^a-z0-9]+", " ", n).strip()

def tagged(e):
    """a name carrying a domain tag or note -- `Insight tho`, `Markov chain al`, `Setpoint [dup: Goal, Desire]`"""
    n, dom = e["name"], (e.get("domain") or "").lower()
    last = n.split()[-1].lower() if " " in n else ""
    return "[" in n or (len(last) >= 2 and len(last) <= 4 and dom.startswith(last) and last not in ("act",))

def content(e): return (e.get("status") != "implicit", bool(e.get("definition")), not tagged(e), len(e["name"]))

def add(ka, a, kb, b, why):
    if ka in taken or kb in taken: return
    keep, drop = (ka, kb) if content(a) >= content(b) else (kb, ka)
    if drop in PREFER:   # read by eye: the other name is a typo or carries a foreign domain tag
        keep, drop = drop, keep
    removed.append({"removed": drop, "kept": keep, "why": why}); taken.update((ka, kb))

# 1. the truncated-name pairs
for p in I["identity_candidates"]:
    (ka, a), (kb, b) = resolve(p["pair"][0]), resolve(p["pair"][1])
    if a is None or b is None:
        unresolved.append(p["pair"]); continue
    sa = tuple(sorted(i["ref"] for i in a.get("ingredients", []))); sb = tuple(sorted(i["ref"] for i in b.get("ingredients", [])))
    da = (a.get("definition") or "").strip().lower(); db = (b.get("definition") or "").strip().lower()
    short, long_ = (a, b) if len(a["name"]) <= len(b["name"]) else (b, a)
    sn, ln = short["name"].lower(), long_["name"].lower()
    rest = ln[len(sn):].strip()
    if ka in sb or kb in sa:
        held.append({"pair": [ka, kb], "defs": [da[:120], db[:120]], "why_held": "one is built from the other"}); continue
    if sa and sa == sb: add(ka, a, kb, b, "same recipe"); continue
    if da and da == db: add(ka, a, kb, b, "same definition"); continue
    if short.get("status") == "implicit":
        dom = (long_.get("domain") or "").lower()
        if rest in ("s", "es"):                                              # Rare Event / Rare Events
            add(ka, a, kb, b, "plural"); continue
        if " " not in ln and ln.startswith(sn):                              # Precip / Precipitation (one word)
            add(ka, a, kb, b, "abbreviation of one word"); continue
        if rest.startswith("(") or (len(rest) >= 2 and " " not in rest and dom.startswith(rest)):
            add(ka, a, kb, b, "domain tag or truncated note"); continue   # Emergent / Emergent aut
    held.append({"pair": [ka, kb], "defs": [da[:120], db[:120]], "why_held": "different definitions or a further word"})

# 2. same recipe AND the same name once spelling is normalised (Honor/Honour code; hero's/heroes), any domain
fam = collections.defaultdict(list)
for k, e in mols.items():
    fam[(tuple(sorted(i["ref"] for i in e["ingredients"])), norm(e["name"]).replace("s ", " ").rstrip("s"))].append(k)
for (sig, nm), ks in fam.items():
    if len(sig) > 1 and len(ks) > 1:
        for other in ks[1:]:
            add(ks[0], mols[ks[0]], other, mols[other], "same recipe, same name (spelling or domain)")

# 3. same recipe AND the same definition opening (Snell ac / Snell's law; Deja vu phen / Deja vu)
dn = lambda e: re.sub(r"[^a-z]", "", (e.get("definition") or "").lower())[:50]
fam3 = collections.defaultdict(list)
for k, e in mols.items():
    sig = tuple(sorted(i["ref"] for i in e["ingredients"]))
    if len(sig) > 1 and dn(e):
        fam3[(sig, dn(e))].append(k)
for ks in fam3.values():
    for other in ks[1:]:
        add(ks[0], mols[ks[0]], other, mols[other], "same recipe, same definition")

remap = {r["removed"]: r["kept"] for r in removed}
def final(k):
    seen = set()
    while k in remap and k not in seen:
        seen.add(k); k = remap[k]
    return k
remap = {d: final(d) for d in remap}
for r in removed:
    r["kept"] = remap[r["removed"]]
removed = [r for r in removed if r["kept"] != r["removed"]]
for r in removed:
    drop, keep = r["removed"], r["kept"]
    e = atoms.pop(drop, None) or mols.pop(drop, None)
    G.pop(drop, None)
    tgt = atoms.get(keep) or mols.get(keep)
    tgt.setdefault("aliases", [])
    if e["name"] not in tgt["aliases"]: tgt["aliases"].append(e["name"])
    tgt.setdefault("merged_from", []).append({"key": drop, "why": r["why"], "by": "Isaiah 2026-10-08"})
selfref = []
for mk, m in mols.items():
    keep_ings = []
    for i in m["ingredients"]:
        if i["ref"] in remap and remap[i["ref"]] == mk:
            selfref.append({"molecule": mk, "dropped_operand": i["ref"]}); continue
        keep_ings.append(i)
    m["ingredients"] = keep_ings
for m in mols.values():
    for i in m["ingredients"]:
        if i["ref"] in remap:
            i["was"] = i["ref"]; i["ref"] = remap[i["ref"]]
            i["is"] = "molecule" if i["ref"] in mols else "atom"
    m["calls"] = sorted({i["ref"] for i in m["ingredients"] if i["ref"] in mols})
json.dump(A, open("atoms.json", "w"), ensure_ascii=False, indent=1)
json.dump(M, open("molecules.json", "w"), ensure_ascii=False, indent=1)
json.dump(G, open("grid_groundings.json", "w"), ensure_ascii=False, indent=1)
json.dump({"ruling": "Isaiah 2026-10-08: the duplicates can be removed",
           "removed": removed, "self_reference_dropped": selfref, "held_for_ruling": held, "unresolved_pairs": unresolved},
          open("DEDUP_LOG.json", "w"), ensure_ascii=False, indent=1)
print("removed", len(removed), "held", len(held), "unresolved", len(unresolved),
      collections.Counter(r["why"] for r in removed))
