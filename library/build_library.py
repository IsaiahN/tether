"""Build the ONE library from its parts, and derive every index from it.

Run from the repo root:   python library/build_library.py [--check]

WHAT THIS IS (reviewer seat, 2026-10-08, at Isaiah's order: "everything the agent is preloaded
with, atoms or recipes -> library"). The library is the single store. Every index is DERIVED
here and regenerated, never edited by hand (Figure 6: "What is recorded only grows. What is
reachable is derived").

INPUTS (all in library/):
    atoms.json          1,748 GIVEN atoms (586 defined, 42 attribute-only, 1,120 implicit)
    molecules.json      2,294 GIVEN molecules (recipes over atoms and molecules)
    agent_atoms.json    the agent's executable atoms (BUILT; kept separate for the ablation)
    grid_groundings.json  key -> what the atom is in a 2D grid world (reviewer, 2026-10-08)
    readings.json       the floor: every quantity perceived or told (readings `reads` may name)
    relations.json      the relation vocabulary (RELATIONS.md Parts 1-5) as data
    grammar.json        operators, qualifiers, NSM frames, symbols, substrate (from the figures)
    domains.json        61 domains
OUTPUTS (library/, overwritten):
    atoms.json, molecules.json, agent_atoms.json, relations.json   each entry gains:
        kind      PRIMITIVE | PERCEPT | COMPOSITE | RELATION
        grid      {meaning, terms, status, lineage}
        reads     readings whose CHANGE lights the entry (it is affected by them)
        affects   readings the entry changes when it holds (operations only)
        substrate Figure 13's six, as reached through its readings
        run       exactly ONE way to run -- see RUN ROUTES below
    index.json      DERIVED: by_reading, by_tag, by_grid_term, by_substrate, by_kind, by_domain,
                    by_attribute, ingredient_of, isomers, identity_candidates
    BUILD_REPORT.md counts and every unresolved item, named

RUN ROUTES -- one per entry, and no entry is a hand-written function:
    PRIMITIVE  an agent atom: arc_atoms builds the callable; this file only names it.
    GROUNDED   a PERCEPT or RELATION: lit when any of `reads` changes (the mutation observer's
               cue); held as the AGENT'S hypothesis -- a condition over `reads`, priced, kept only
               if it pays (ruling 5, 2026-09-22; Figure 5). The term is the PAIR (entry, grounding)
               (Figure 13). `condition_text` is the source's prose, a candidate the condition
               compiler may parse; nothing here asserts it true.
    COMPOSED   a molecule: an ordered tree over library keys; each junction carries its bond, and
               '?' (UNKNOWN) where the source wrote '+' (Isaiah 2026-09-22; Figure 12: "which one
               holds is not recoverable from the operands"). It runs through ONE bind(bond, l, r).

`reads`/`affects` are DERIVED by rule from the grid meaning's terms, the entry's cluster tags and
its encodings -- tables below, data not logic -- with lineage `derived:<rule>`. They order and
narrow; they never exclude (inherited.py's ORDER, NEVER EXCLUDE).
"""
from __future__ import annotations

import collections
import json
import os
import re
import sys
from pathlib import Path

LIB = Path(os.environ.get("LIBRARY_DIR") or Path(__file__).parent)

# --- the derivation tables (data, pinned and movable) ------------------------------------------
GRID_TERM_READS = {
    "contact": ["touching", "contact"], "inside": ["inside", "bbox"], "colour": ["colour", "colour_changed"],
    "shape": ["shape", "dholes", "dperimeter"], "size": ["h", "w", "dh", "dw", "dcells", "filled"],
    "position": ["row", "col"], "move": ["drow", "dcol"], "appear": ["came"], "disappear": ["gone"],
    "repeat": ["prev", "stability", "age"], "count": ["came", "gone"], "line_path": ["row", "col", "drow", "dcol"],
    "region": ["bbox", "inside", "row", "col", "h", "w"], "barrier": ["touching", "drow", "dcol", "action"],
    "boundary": ["dperimeter", "touching"], "hole_gap": ["dholes", "inside"], "time": ["age", "stability", "prev"],
    "action": ["action", "press"], "controlled": ["drow", "dcol", "action"], "goal": ["completed", "level"],
    "spread": ["dcells", "came", "colour_changed"], "direction": ["drow", "dcol"], "align": ["row", "col"],
    "same_diff": ["colour", "shape"], "compare": ["h", "w", "row", "col"], "hidden": ["came", "gone"],
    "follow": ["drow", "dcol"], "rule_model": [], "record": ["prev", "age"], "symmetry": ["shape"],
    "resource": ["allowance", "completed"],
}
TAG_READS = {
    "ACTION": ["action"], "SPEED": ["drow", "dcol"], "TIME": ["age", "stability", "prev"],
    "FORCE": ["touching", "drow", "dcol"], "CHANGE": ["drow", "dcol", "dh", "dw", "dcells", "colour_changed"],
    "EXTENT": ["h", "w", "filled"], "STRUCTURE": ["shape", "row", "col"], "STATE": ["stability", "colour"],
    "CONTACT": ["touching", "contact", "bbox"], "DIRECTION": ["drow", "dcol"], "COUNT": ["came", "gone"],
    "POSITION": ["row", "col"], "SHAPE": ["shape", "dholes", "dperimeter"], "MOTION": ["drow", "dcol"],
    "IDENTITY": ["shape", "colour"], "COLOUR": ["colour", "colour_changed"], "SIGNAL": ["came", "gone", "colour_changed"],
}
ENC_READS = {
    "POSITION": ["row", "col"], "EXTENT": ["h", "w"], "COLOUR": ["colour"], "COUNT": ["came", "gone"],
    "SHAPE": ["shape"], "RELATION": ["touching", "contact", "inside", "bbox"], "TEMPORAL": ["prev", "age", "stability"],
    "EVENT": ["came", "gone", "colour_changed"], "STATE": ["stability"], "BEHAVIOURAL": ["action"],
}
AFFECT_VERBS = [   # word in the grid meaning -> readings an entry that holds would change
    (r"\b(move|moves|moving|moved|push|pushes|pull|fall|falls|slide|slides|drift|travel|shift)", ["drow", "dcol"]),
    (r"\b(recolou?r|colou?r (change|changes|changing)|turn(s|ed)? .* colou?r)", ["colour", "colour_changed"]),
    (r"\b(grow|grows|growing|shrink|shrinks|expand|contract|stretch|adds? cells|loses? cells)", ["h", "w", "dcells"]),
    (r"\b(remov|disappear|consum|destroy|erase|vanish|eat)", ["gone"]),
    (r"\b(appear|produc|creat|copy|copies|spawn|replicat|emerge)", ["came"]),
    (r"\b(rotat|reflect|mirror|deform|reshape|bend|break apart|split)", ["shape", "dholes", "dperimeter"]),
    (r"\b(join|attach|merge|stick|bind)", ["touching", "gone"]),
    (r"\b(complete|completes|goal reached|level complete)", ["completed"]),
    (r"\b(pass|passes|passing|transfer|transfers|spread|spreads|spreading|infect|contaminat|propagat)", ["colour_changed", "dcells"]),
]

IN_TYPE_READS = {"SHAPE": ["shape"], "CELLS": ["shape"], "CELL": ["shape"], "DELTA": ["drow", "dcol"],
                 "POSITION": ["row", "col"], "EXTENT": ["h", "w"], "COLOUR": ["colour"], "OBJECT": [], "PRED": [],
                 "OBJ": [], "val": [], "BOOL": []}

AGENT_MEANINGS = {
    "above": "is one position above/before another (comparison over POSITION)", "abs_delta": "size of a signed change",
    "age": "frames since the object was first tracked", "aligned": "two objects share a row or column",
    "all": "every member satisfies", "all_same": "every member has the same value", "any": "some member satisfies",
    "any_same": "some two members share a value", "area": "number of filled cells", "bbox": "bounding-box overlap of two objects",
    "bbox_area": "height times width", "both": "both predicates hold", "canonical": "the outline normalised under rotation/reflection",
    "centroid": "the centre cell", "col": "left column", "colour": "colour index", "colour_changed": "colour differs from last frame",
    "completed": "the board's progress count", "contact": "shared cell faces with another object", "corners": "corner cells of the outline",
    "count": "how many members", "dcells": "change in filled cells", "dcol": "columns moved", "dh": "height change",
    "dholes": "change in holes", "distinct": "number of different values", "dperimeter": "change in outline length",
    "drow": "rows moved", "dw": "width change", "either": "at least one predicate holds", "h": "height",
    "holes": "enclosed background regions", "idn": "the value unchanged (identity)", "inside": "lies in another's hole",
    "is_max": "is the largest in its group", "is_min": "is the smallest in its group", "is_mode": "is the most common value",
    "is_square": "height equals width and all cells filled", "negate": "the predicate does not hold", "none": "no member satisfies",
    "none_same": "no two members share a value", "orbit_size": "number of distinct outlines under rotation/reflection",
    "other": "differs from", "owner": "the object a cell or slot belongs to", "parity": "even or odd", "perimeter": "outline length",
    "rank_in": "position in an ordering of the group", "recolour": "set the colour", "reflect": "mirror the outline",
    "rotate": "turn the outline by 90 degrees", "row": "top row", "same": "equals", "shape": "outline label",
    "sign": "direction of a signed change", "speed": "cells moved this frame", "stability": "frames unchanged",
    "sum_group": "total over the group", "symmetric": "unchanged under a reflection", "touching": "shares a cell face with another",
    "touching_n": "how many objects it touches", "translate": "move by an offset", "w": "width",
}

RELATION_READS = [
    (r"contact|touch|disjoint|adjacent|intersect|overlap|coincident", ["touching", "contact", "bbox"]),
    (r"contain|nested|tangent|inside", ["inside", "bbox"]),
    (r"collinear|aligned|parallel|perpendicular|concentric|offset", ["row", "col", "h", "w"]),
    (r"symmetric|congruent|similar|rotation|spinning|rolling|interlock|occlud", ["shape"]),
    (r"motion|translation|sliding|orbiting|oscillating|fixed|distance|cable|revolute|prismatic|planar", ["drow", "dcol", "touching"]),
    (r"normal|friction|tension|compression|spring|damping|impact|gravity|electric|buoyancy|radiation", ["drow", "dcol", "touching", "action"]),
    (r"approach|exchange|separate|elastic|inelastic", ["drow", "dcol", "touching"]),
    (r"deformation|fragmentation|merging|accretion|erosion|flow|phase", ["shape", "dcells", "came", "gone", "h", "w"]),
]


def _load(name):
    return json.loads((LIB / name).read_text(encoding="utf-8"))


def _dedup(xs):
    return list(dict.fromkeys(xs))


def _affects(meaning: str) -> list[str]:
    out = []
    for pat, rd in AFFECT_VERBS:
        if re.search(pat, meaning, re.I):
            out += rd
    return _dedup(out)


def _substrate(reads, readings):
    return sorted({s for r in reads for s in readings.get(r, {}).get("substrate", [])})


_SPLIT = re.compile(r"\s*(\+|→|->|⇒|=>|∥|\bor\b|−|(?<=\s)-(?=\s)|≡|⋛|>|<)\s*")
_BOND_OF = {"+": "?", "→": "→", "->": "→", "⇒": "⇒", "=>": "⇒", "∥": "∥", "or": "∥", "−": "−", "-": "−",
            "≡": "≡", "⋛": "⋛", ">": "⋛", "<": "⋛"}


def _junctions(recipe: str, n: int) -> tuple[list[str], str]:
    """The bond at each of the n-1 junctions, read from the recipe text in order; '?' for '+'."""
    depth, ops, buf = 0, [], ""
    for ch in recipe:  # top level only: operators inside parentheses are qualifiers
        depth += ch == "("
        depth -= ch == ")"
        buf += ch if depth == 0 else " "
    ops = [_BOND_OF[m.group(1)] for m in _SPLIT.finditer(buf)]
    if len(ops) == n - 1:
        return ops, "read"
    return ["?"] * max(n - 1, 0), f"unparsed ({len(ops)} operators for {n} ingredients): all junctions UNKNOWN"


def build(check_only: bool = False) -> dict:
    atoms = _load("atoms.json")
    mols = _load("molecules.json")
    agent = _load("agent_atoms.json")
    grid = _load("grid_groundings.json")
    readings = _load("readings.json")["readings"]
    rels = _load("relations.json")
    explicit = _load("reads_explicit.json")["reads"] if (LIB / "reads_explicit.json").exists() else {}
    report = collections.defaultdict(list)

    def tags_of(e):
        return [t.rstrip("*") for t in (e.get("tags", {}).get("primary") or [])]

    # --- atoms (GIVEN) -> PERCEPT, run GROUNDED -------------------------------------------------
    for k, e in atoms["atoms"].items():
        m = grid.get(k)
        if m is None:
            report["atom without grid meaning"].append(k)
            m = ""
        terms = [t for t, p in _TERMS.items() if re.search(p, m, re.I)]
        w = {}
        for src, wt in (([r for t in terms for r in GRID_TERM_READS.get(t, [])], 1.0),
                        ([r for t in tags_of(e) for r in TAG_READS.get(t, [])], 0.5),
                        ([r for enc in e.get("encodings", []) for r in ENC_READS.get(enc, [])], 0.5)):
            for r in src:
                if r in readings:
                    w[r] = max(w.get(r, 0.0), wt)
        for r in explicit.get(k, []):
            if r in readings:
                w[r] = 1.0
        reads = sorted(w, key=lambda r: -w[r])
        e["reads_weight"] = w
        if not reads:
            report["atom with no reading (reachable by name/recipe only)"].append(k)
        e["kind"] = "PERCEPT"
        e["grid"] = {"meaning": m, "terms": terms, "status": "candidate",
                     "lineage": "reviewer seat 2026-10-08, from name and definition; a description, not an instrument"}
        e["reads"], e["affects"] = reads, _affects(m)
        e["substrate"] = _substrate(reads + e["affects"], readings)
        e["run"] = {"route": "GROUNDED", "lit_by": reads, "condition_text": e.get("condition"),
                    "held_as": "the agent's hypothesis over `lit_by`, priced and settled by the ground",
                    "standing": None}

    # --- molecules (GIVEN) -> COMPOSITE, run COMPOSED -------------------------------------------
    allkeys = set(atoms["atoms"]) | set(mols["molecules"])
    for k, e in mols["molecules"].items():
        ings = e["ingredients"]
        for i in ings:
            if i["ref"] not in allkeys:
                report["unresolved ingredient"].append(f"{k} -> {i['ref']}")
        bonds, how = _junctions(e.get("recipe", ""), len(ings))
        if how != "read":
            report["recipe junctions unparsed"].append(f"{k}: {e.get('recipe')} -- {how}")
        e["kind"] = "COMPOSITE"
        e["run"] = {"route": "COMPOSED",
                    "operands": [{"ref": i["ref"], **({"qual": i["qual"]} if i.get("qual") else {})} for i in ings],
                    "junctions": bonds, "junction_source": how,
                    "settles": "each junction by the bond tests over the residual's frames (Figure 12)"}

    # molecules' reads/affects/substrate/grid inherit from their operands, resolved bottom-up
    memo = {}

    def inherit(k, stack=()):
        if k in memo:
            return memo[k]
        if k in atoms["atoms"]:
            a = atoms["atoms"][k]
            memo[k] = (a["reads"], a["affects"], a["grid"]["meaning"])
            return memo[k]
        if k in stack:  # the one mutual cycle (Runaway <-> Positive feedback) is real; stop, do not recurse
            return ([], [], "(cycle)")
        e = mols["molecules"][k]
        r, f = [], []
        for i in e["ingredients"]:
            rr, ff, _ = inherit(i["ref"], stack + (k,))
            r += rr
            f += ff
        f += _affects(e.get("definition") or "")
        memo[k] = (_dedup(r), _dedup(f), None)
        return memo[k]

    for k, e in mols["molecules"].items():
        r, f, _ = inherit(k)
        e["reads"], e["affects"] = [x for x in r if x in readings], [x for x in f if x in readings]
        e["substrate"] = _substrate(e["reads"] + e["affects"], readings)
        parts = []
        for idx, i in enumerate(e["ingredients"]):
            name = i["ref"].split("|", 1)[1] + (f"({i['qual']})" if i.get("qual") else "")
            sub = atoms["atoms"].get(i["ref"], {}).get("grid", {}).get("meaning") or \
                mols["molecules"].get(i["ref"], {}).get("definition") or ""
            parts.append(f"{name} [{sub}]" if sub else name)
            if idx < len(e["run"]["junctions"]):
                parts.append(f" {e['run']['junctions'][idx]} ")
        e["grid"] = {"meaning": "composition: " + "".join(parts), "definition": e.get("definition"),
                     "status": "derived", "lineage": "composed from the operands' grid meanings; '?' = bond UNKNOWN"}

    # --- agent atoms (BUILT) -> PRIMITIVE ---------------------------------------------------------
    for k, e in agent["atoms"].items():
        nm = e["name"]
        intype, outtype = e.get("in_type"), e.get("out_type")
        # an operation is lit by the readings its INPUT type comes from (it computes over them)
        reads = [r for r in IN_TYPE_READS.get(intype, []) if r in readings]
        e["kind"] = "PRIMITIVE"
        e["grid"] = {"meaning": e.get("definition") or AGENT_MEANINGS.get(nm, ""), "status": "built",
                     "lineage": f"{e.get('defined_at', 'arc_atoms')} (executable; meaning from the code's own docstring)"}
        if not e["grid"]["meaning"]:
            report["agent atom without meaning"].append(k)
        e["reads"], e["affects"] = reads, (["drow", "dcol"] if nm == "translate" else ["colour", "colour_changed"]
                                           if nm == "recolour" else ["shape"] if nm in ("rotate", "reflect") else [])
        e["substrate"] = _substrate(e["reads"] + e["affects"], readings)
        e["run"] = {"route": "PRIMITIVE", "impl": f"arc_atoms:{nm}", "in_type": intype, "out_type": outtype}

    # --- relations -> RELATION, run GROUNDED ------------------------------------------------------
    for name, r in rels["relations"].items():
        reads = []
        for pat, rd in RELATION_READS:
            if re.search(pat, name, re.I):
                reads += rd
        r["kind"] = "RELATION"
        r["arity"] = 2
        r["reads"] = [x for x in _dedup(reads) if x in readings]
        r["substrate"] = _substrate(r["reads"], readings)
        r["run"] = {"route": "GROUNDED", "lit_by": r["reads"], "condition_text": r.get("condition"),
                    "held_as": "a two-place frame filled by two objects (NSM_GRAMMAR: TOUCH(X,Y)); settled by the ground"}
        if not r["reads"]:
            report["relation with no reading"].append(name)

    # --- derived index -----------------------------------------------------------------------------
    idx = {k: collections.defaultdict(list) for k in
           ("by_reading_reads", "by_reading_affects", "by_tag", "by_grid_term", "by_substrate", "by_kind",
            "by_domain", "by_attribute", "ingredient_of")}
    every = [("atoms", k, e) for k, e in atoms["atoms"].items()] + \
            [("molecules", k, e) for k, e in mols["molecules"].items()] + \
            [("agent", k, e) for k, e in agent["atoms"].items()] + \
            [("relations", f"RELATION|{n}", e) for n, e in rels["relations"].items()]
    for store, k, e in every:
        if store != "molecules":  # a molecule is lit THROUGH its operands (ingredient_of), never directly
            for r in e.get("reads", []):
                idx["by_reading_reads"][r].append((k, e.get("reads_weight", {}).get(r, 1.0)))
        for r in e.get("affects", []):
            idx["by_reading_affects"][r].append(k)
        for t in tags_of(e):
            idx["by_tag"][t].append(k)
        for t in e.get("grid", {}).get("terms", []) or []:
            idx["by_grid_term"][t].append(k)
        for s in e.get("substrate", []):
            idx["by_substrate"][s].append(k)
        idx["by_kind"][e.get("kind")].append(k)
        idx["by_domain"][e.get("domain", k.split("|")[0])].append(k)
        for a in e.get("attributes", []) or []:
            idx["by_attribute"][a].append(k)
        for i in e.get("ingredients", []) or []:
            idx["ingredient_of"][i["ref"]].append(k)
    fam = collections.defaultdict(list)
    for k, e in mols["molecules"].items():   # same parts AND same qualifiers; written order kept apart
        sig = tuple(sorted((i["ref"], i.get("qual", "")) for i in e["ingredients"]))
        if len(sig) > 1:
            fam[sig].append(k)
    isomers = []
    for s_, m in fam.items():
        if len(m) < 2:
            continue
        orders = {tuple(i["ref"] for i in mols["molecules"][k]["ingredients"]) for k in m}
        oriented = all(mols["molecules"][k].get("orientation") for k in m)
        isomers.append({"ingredients": [x[0] for x in s_], "members": m,
                        "written_order_differs": len(orders) > 1,
                        "told_apart_by": "orientation (draft)" if oriented else
                        ("the order, once the bond is ordered (→ ⇒ − ⋛)" if len(orders) > 1 else "the bond and orientation (Figure 12)")})
    names = collections.defaultdict(list)
    for store, k, e in every:
        names[(e.get("domain"), (e.get("name") or k.split("|", 1)[-1]).lower())].append(k)
    ident = []
    by_dom = collections.defaultdict(list)
    for (dom, nm), ks in names.items():
        by_dom[dom].append(nm)
    for dom, nms in by_dom.items():  # truncated forms: one name a prefix of another in one domain
        s = sorted(nms)
        for a, b in zip(s, s[1:]):
            if len(a) >= 6 and b.startswith(a) and b != a:
                ident.append({"pair": [f"{dom}|{a}", f"{dom}|{b}"], "relation": "≡ candidate (truncated form)",
                              "action": "record ≡ in the retrieval layer; delete neither (Isaiah 2026-09-22)"})
    cross = collections.defaultdict(list)
    for (dom, nm), ks in names.items():
        cross[nm] += ks
    collisions = {nm: ks for nm, ks in cross.items() if len(ks) > 1}
    # domain adjacency, use ranking and mutual cycles -- what ADJACENCY_EDGES / ATOM_RANKING /
    # CHEMISTRY_INSTANCES held, now DERIVED from the recipes so docs/library-closure can retire
    adj = collections.Counter()
    for k, e in mols["molecules"].items():
        for i in e["ingredients"]:
            a, b = e["domain"], i["ref"].split("|")[0]
            if a != b:
                adj[tuple(sorted((a, b)))] += 1
    uses = collections.Counter(i["ref"] for e in mols["molecules"].values() for i in e["ingredients"])
    cycles = sorted({tuple(sorted((k, i["ref"]))) for k, e in mols["molecules"].items() for i in e["ingredients"]
                     if i["ref"] in mols["molecules"] and k in {j["ref"] for j in mols["molecules"][i["ref"]]["ingredients"]}
                     and i["ref"] != k})
    index = {"meta": {"what": "DERIVED by build_library.py from the library. Never edit by hand.",
                      "how_to_query": "a mutation on reading r lights by_reading_reads[r] (entries affected by r); "
                                      "ingredient_of walks lit entries up to the molecules that use them; order by "
                                      "standing then tag weight; never exclude"},
             **{k: {kk: (sorted(set(vv), key=lambda kv: (-kv[1], kv[0])) if k == "by_reading_reads" else sorted(set(vv)))
                    for kk, vv in v.items()} for k, v in idx.items()},
             "isomers": isomers, "identity_candidates": ident,
             "domain_adjacency": [{"domains": list(p_), "edges": n} for p_, n in adj.most_common()],
             "use_ranking": [{"key": k, "uses": n} for k, n in uses.most_common()],
             "mutual_cycles": [list(c) for c in cycles],
             "same_name_across_domains": collisions}

    # --- every entry's ROLE table (Isaiah 2026-10-08: state, process, cause ... for ALL atoms) -------
    # Written after the files, because the views are computed by library_runtime over them.
    roles_written = False

    counts = {"atoms": len(atoms["atoms"]), "molecules": len(mols["molecules"]), "agent_atoms": len(agent["atoms"]),
              "relations": len(rels["relations"]), "readings": len(readings), "isomer_families": len(isomers),
              "identity_candidates": len(ident), "same_name_across_domains": len(collisions)}
    if not check_only:
        for name, obj in (("atoms.json", atoms), ("molecules.json", mols), ("agent_atoms.json", agent),
                          ("relations.json", rels), ("index.json", index)):
            (LIB / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
        lines = ["# BUILD REPORT -- derived by build_library.py", "", "## Counts", ""]
        lines += [f"- {k}: {v}" for k, v in counts.items()]
        lines += ["", "## Every unresolved item, named", ""]
        for key, items in report.items():
            lines += [f"### {key} ({len(items)})", ""] + [f"- {x}" for x in items[:400]] + \
                     ([f"- ... {len(items) - 400} more"] if len(items) > 400 else []) + [""]
        (LIB / "BUILD_REPORT.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
        _write_roles(atoms, mols, agent, rels, index)
    return {"counts": counts, "report": {k: len(v) for k, v in report.items()}}


def _write_roles(atoms, mols, agent, rels, index) -> None:
    sys.path.insert(0, str(LIB))
    from library_runtime import Library  # noqa: E402 -- the views are the runtime's, computed once here
    lib = Library(LIB).load()
    by_role = collections.defaultdict(list)
    stores = [("atoms", atoms["atoms"], lambda k: k), ("molecules", mols["molecules"], lambda k: k),
              ("relations", rels["relations"], lambda n: f"RELATION|{n}"), ("agent", agent["atoms"], lambda k: k)]
    for _store, entries, keyof in stores:
        for k, e in entries.items():
            key = keyof(k)
            e["roles"] = table = lib.role_table(key)   # the SAME generic step a new entry goes through
            by_role[table["default"]].append(key)
    index["by_default_role"] = {r: sorted(v) for r, v in by_role.items()}
    for name, obj in (("atoms.json", atoms), ("molecules.json", mols), ("agent_atoms.json", agent),
                      ("relations.json", rels), ("index.json", index)):
        (LIB / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")


_TERMS = {  # the grid-term tagger, used only where an atom carries no `grid.terms` yet
    "contact": r"\b(touch|touching|contact|adjacent|side by side|next to|meet|overlap|occupy|collid|bump|hit)",
    "inside": r"\b(inside|enclos|contain|nested|within)", "colour": r"\bcolou?r",
    "shape": r"\b(shape|outline|form)\b", "size": r"\b(size|grow|grows|growing|shrink|larger|smaller|extent|big|small|filled cells|number of cells|height|width)",
    "position": r"\b(position|row|column|place|located|where)\b", "move": r"\b(mov|shift|drift|fall|slide|travel|push|pull|changes? position)",
    "appear": r"\b(appear|produc|new object|copy|copies|creat|spawn|emerge)",
    "disappear": r"\b(disappear|remov|destroy|consum|break apart|vanish)",
    "repeat": r"\b(repeat|period|cycle|cyclic|altern|rhythm|again|back and forth)",
    "count": r"\b(count|number|total|how many|tally)", "line_path": r"\b(line|path|route|beam|chain)",
    "region": r"\b(region|area|zone)\b", "barrier": r"\b(wall|block|barrier|obstacle|stop)",
    "boundary": r"\b(boundary|border|edge|outline)", "hole_gap": r"\b(hole|gap|opening|missing)",
    "time": r"\b(turn|turns|delay|later|before|after|duration)", "action": r"\b(action|click|press|act)\b",
    "controlled": r"\b(controlled object|avatar|agent)", "goal": r"\b(goal|target|win|level complete|completes? the level|completed)",
    "spread": r"\b(spread|propagat|flow|diffus)", "direction": r"\b(direction|toward|away|up|down|left|right|diagonal)\b",
    "align": r"\b(align|lined up|same row|same column|parallel)", "same_diff": r"\b(same (colou?r|shape|kind|value)|identical|differ|match|odd one)",
    "compare": r"\b(larger|smaller|more than|less than|compare|exceed|threshold|largest|smallest)",
    "hidden": r"\b(hidden|hide|cover|unseen|invisible)", "follow": r"\b(follow|chase|pursu|flee)",
    "rule_model": r"\b(rule|predict|model|simulat)", "record": r"\b(record|stor|remember|history)",
    "symmetry": r"\b(symmetr|mirror|rotat|reflect)", "resource": r"\b(counter|resource|spend|spent|cost|budget)",
}

def check() -> int:
    """The seat check: rebuild a COPY of the library and confirm every derived file is reproduced
    byte for byte. Derived means checkable (Figure 10)."""
    import shutil, subprocess, tempfile  # noqa: E401
    tmp = Path(tempfile.mkdtemp())
    for f in LIB.iterdir():
        if f.is_file():
            shutil.copy(f, tmp / f.name)
    subprocess.run([sys.executable, str(tmp / "build_library.py")], env={**os.environ, "LIBRARY_DIR": str(tmp)},
                   check=True, capture_output=True)
    bad = [n for n in ("atoms.json", "molecules.json", "agent_atoms.json", "relations.json", "index.json")
           if (tmp / n).read_bytes() != (LIB / n).read_bytes()]
    shutil.rmtree(tmp)
    print("library check:", "OK -- every derived file reproduced" if not bad else f"FAIL -- not reproduced: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--check" in sys.argv:
        raise SystemExit(check())
    out = build()
    print(json.dumps(out, indent=1))
