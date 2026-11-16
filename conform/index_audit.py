"""index_audit: every filing in library/index.json checked against the entry it points at (step 5).

    python conform/index_audit.py            the audit, a summary to stdout
    python conform/index_audit.py --json P   also every classified filing, written to P
    python conform/index_audit.py --md P     also the report (counts + every MISFILED / ORPHAN /
                                             STALE / QUESTIONED filing with its evidence)

READ-ONLY: it opens given.json and index.json and writes only the paths it is given. Under 1 min.

A FILING is one (map, value, key): index.<map>[value] lists key -- e.g. by_reading_affects["gone"]
lists ADHERENCE|Unbreakable, i.e. the entry is filed as PRODUCING the reading `gone` (its described
effect; library_runtime.Library.produces reads exactly this map, and default_role reads `affects`).

Each filing gets ONE class:

    OK          the source entry declares it
    ORPHAN      the key names no entry in given.json
    STALE       the index and the entry disagree: the entry's own field (or the build's rule re-run
                on the entry's SOURCE text) no longer gives this filing, or the entry declares a
                value the index does not file it under (counted as STALE, reported as "unfiled")
    MISFILED    filed under a described effect its source does not declare: every phrase in the
                source that produced the filing is NEGATED ("an object no action can change or
                remove") or is a word that is not the effect at all (the noun "appearance", "turns"
                as the time step). For a molecule: every route to the filing (its own definition,
                its operands' filings) is MISFILED.
    QUESTIONED  a judgement call, never fixed here: the only producing phrase is a TRIGGER ("deforms
                when pushed": the push is what happens TO it) or HYPOTHETICAL ("an object would
                fall"). Listed for Isaiah.

The structural maps (by_reading_reads, by_tag, by_grid_term, by_substrate, by_kind, by_domain,
by_attribute, ingredient_of, by_default_role, and the tag section's by_tag / by_pair / by_attribute)
are checked for ORPHAN and STALE against the entry's declared field. The semantic check (MISFILED /
QUESTIONED) is on by_reading_affects -- the described effect -- and carried to by_default_role,
whose PROCESS default is read off `affects` (library_runtime.default_role).

The phrase rules below are DATA (tables), and the build's own AFFECT_VERBS are read from
build_library, never restated, so the audit judges the same matches the build made.
"""
from __future__ import annotations

import collections
import json
import re
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "library"
sys.path.insert(0, str(LIB))
import build_library as B  # noqa: E402 -- the build's tables, read only (importing writes nothing)
from library_runtime import _MEASURE_START  # noqa: E402 -- default_role's MEASURE test

# --- the phrase rules (data) ------------------------------------------------------------------
# a clause ends at punctuation or at one of these words; a negator/trigger only reaches its clause
CLAUSE_END = re.compile(r"[,.;:()]|\b(but|until|while|so that|then|whereas|instead)\b", re.I)
NEGATOR = re.compile(r"\b(not|no|never|nothing|none|nor|cannot|without)\b|n't\b", re.I)
NEG_REACH = 6          # words between the negator and the matched verb, same clause
# a negator that heads a PLACE or is itself a noun negates nothing after it: "an object with
# nothing below it falls" (it falls), "the nothing from which being emerges" (it emerges)
NOT_A_NEGATOR = re.compile(r"\b(no|nothing)\s+(below|under|underneath|beneath|above|behind|beside)"
                           r"\b|\b(the|a)\s+nothing\b", re.I)
TRIGGER = re.compile(r"\b(when|whenever|if|once|after|on being|despite)\b", re.I)
HYPOTHETICAL = re.compile(r"\b(would|could|can|may|might|able to)\b", re.I)
# words the build's stems catch that are not the effect: noun / adjective senses, plainly
NOT_THE_EFFECT = {"appearance", "appearances", "passage", "passages"}
# the colour rule `turn(s|ed)? .* colou?r` is greedy: a "turn" that is the TIME STEP is no recolour
TURN_AS_TIME = re.compile(r"\b(across|per|each|every|over|between|of|by|a|the|one|two|few|many)"
                          r"\s+turns?\b", re.I)


def _clause_before(text: str, pos: int) -> str:
    """The text of the clause the match at `pos` sits in, up to the match."""
    head = text[:pos]
    cut = 0
    for m in CLAUSE_END.finditer(head):
        cut = m.end()
    return head[cut:]


def classify_span(text: str, m: re.Match) -> tuple[str, str]:
    """One match of an AFFECT_VERBS pattern -> (status, reason). status: AFFIRMED | NEGATED |
    NOT_THE_EFFECT | TRIGGER | HYPOTHETICAL."""
    word = re.match(r"\w+", text[m.start():]).group(0).lower()
    clause = _clause_before(text, m.start())
    if word in NOT_THE_EFFECT:
        return "NOT_THE_EFFECT", f"'{word}' is a noun, not the effect"
    if word.startswith("turn") and TURN_AS_TIME.search(text[max(0, m.start() - 12):m.start() + 6]):
        return "NOT_THE_EFFECT", "'turn' is the time step, not a recolour (greedy `turn .* colour`)"
    skip = [(n.start(), n.end()) for n in NOT_A_NEGATOR.finditer(clause)]
    negs = [n for n in NEGATOR.finditer(clause)
            if not any(a <= n.start() < b for a, b in skip)]
    if negs:
        between = clause[negs[-1].end():].split()
        if len(between) <= NEG_REACH:
            return "NEGATED", f"'{negs[-1].group(0)} ... {word}' in one clause"
    if TRIGGER.search(clause):
        return "TRIGGER", f"'{TRIGGER.search(clause).group(0)} ... {word}': what happens to it"
    if HYPOTHETICAL.search(clause):
        return "HYPOTHETICAL", f"'{HYPOTHETICAL.search(clause).group(0)} ... {word}'"
    return "AFFIRMED", f"'{word}'"


def spans_for(text: str, reading: str) -> list[dict]:
    """Every phrase in `text` the build's AFFECT_VERBS turn into `reading`, classified."""
    out = []
    for pat, rd in B.AFFECT_VERBS:
        if reading not in rd:
            continue
        for m in re.finditer(pat, text or "", re.I):
            st, why = classify_span(text, m)
            s = max(0, m.start() - 40)
            out.append({"status": st, "why": why,
                        "at": ("..." if s else "") + text[s:m.end() + 30].replace("\n", " ")})
    return out


def _verdict(spans: list[dict]) -> str:
    sts = {s["status"] for s in spans}
    if "AFFIRMED" in sts:
        return "OK"
    if sts & {"TRIGGER", "HYPOTHETICAL"}:
        return "QUESTIONED"
    return "MISFILED" if sts else "STALE"


# --- loading ------------------------------------------------------------------------------------
def load():
    given = json.loads((LIB / "given.json").read_text(encoding="utf-8"))
    index = json.loads((LIB / "index.json").read_text(encoding="utf-8"))
    return given["entries"], index["index"], index["tag"]


def source_of(entries: dict, key: str) -> dict | None:
    if key in entries:
        return entries[key]
    if key.startswith("RELATION|"):
        e = entries.get(key.split("|", 1)[1])
        return e if e is not None and e.get("kind") == "RELATION" else None
    return None


def keys_of(entries: dict):
    for k, e in entries.items():
        yield (f"RELATION|{k}" if e.get("kind") == "RELATION" else k), e


# --- the declared value set of every structural map, from the entry's own fields ----------------
def declared(entries: dict, name_match: dict) -> dict[str, dict[str, set]]:
    d: dict[str, dict[str, set]] = collections.defaultdict(lambda: collections.defaultdict(set))
    for k, e in keys_of(entries):
        if e.get("kind") != "COMPOSITE":
            for r in e.get("reads") or []:
                d["by_reading_reads"][r].add((k, (e.get("reads_weight") or {}).get(r, 1.0)))
        for r in e.get("affects") or []:
            d["by_reading_affects"][r].add(k)
        for t in (e.get("tags") or {}).get("primary") or []:
            d["by_tag"][t.rstrip("*")].add(k)
        for t in (e.get("grid") or {}).get("terms") or []:
            d["by_grid_term"][t].add(k)
        for s in e.get("substrate") or []:
            d["by_substrate"][s].add(k)
        d["by_kind"][e.get("kind")].add(k)
        d["by_domain"][e.get("domain", k.split("|")[0])].add(k)
        for a in e.get("attributes") or []:
            d["by_attribute"][a].add(k)
        for i in e.get("ingredients") or []:
            d["ingredient_of"][i["ref"]].add(k)
        if e.get("roles"):
            d["by_default_role"][e["roles"]["default"]].add(k)
    for k, a in name_match.items():
        d["by_attribute"][a].add(k)
    return d


def structural(entries, idx, tag) -> list[dict]:
    rows = []
    dec = declared(entries, idx.get("name_match") or {})
    for mp, want in dec.items():
        got = idx.get(mp) or {}
        for v, posting in got.items():
            for item in posting:
                k, w = (item[0], item[1]) if mp == "by_reading_reads" else (item, None)
                src = source_of(entries, k)
                if src is None:
                    rows.append({"map": mp, "value": v, "key": k, "class": "ORPHAN",
                                 "evidence": "no entry in given.json"})
                    continue
                probe = (k, w) if mp == "by_reading_reads" else k
                ok = probe in want.get(v, ())
                rows.append({"map": mp, "value": v, "key": k, "class": "OK" if ok else "STALE",
                             "evidence": "" if ok else "the entry's field does not declare it"})
        for v, ks in want.items():
            have = {tuple(x)[0] if mp == "by_reading_reads" else x for x in got.get(v, ())}
            for p in ks:
                k = p[0] if mp == "by_reading_reads" else p
                if k not in have:
                    rows.append({"map": mp, "value": v, "key": k, "class": "STALE",
                                 "evidence": "unfiled: the entry declares it, the index lacks it"})
    # the tag section (tag_index v5): by_tag over tags.scored, by_pair over tags.pairs, by_attribute
    for t, kinds in (tag.get("by_tag") or {}).items():
        for _kd, ks in kinds.items():
            for k in ks:
                e = source_of(entries, k)
                ok = e is not None and t in {r["tag"] for r in (e.get("tags") or {}).get("scored")
                                             or []}
                rows.append({"map": "tag.by_tag", "value": t, "key": k,
                             "class": "OK" if ok else ("ORPHAN" if e is None else "STALE"),
                             "evidence": "" if ok else "tags.scored does not carry it"})
    for p, kinds in (tag.get("by_pair") or {}).items():
        for _kd, ks in kinds.items():
            for k in ks:
                e = source_of(entries, k)
                ok = e is not None and p in {"+".join(x) for x in (e.get("tags") or {}).get(
                    "pairs") or []}
                rows.append({"map": "tag.by_pair", "value": p, "key": k,
                             "class": "OK" if ok else ("ORPHAN" if e is None else "STALE"),
                             "evidence": "" if ok else "tags.pairs does not carry it"})
    nm = idx.get("name_match") or {}
    for a, ks in (tag.get("by_attribute") or {}).items():
        for k in ks:
            e = source_of(entries, k)
            ok = e is not None and (a in (e.get("attributes") or []) or nm.get(k) == a)
            rows.append({"map": "tag.by_attribute", "value": a, "key": k,
                         "class": "OK" if ok else ("ORPHAN" if e is None else "STALE"),
                         "evidence": "" if ok else "attributes / name_match do not carry it"})
    return rows


# --- the described effect: by_reading_affects, against the source text ------------------------
def described_effect(entries, idx) -> tuple[list[dict], dict]:
    """Every by_reading_affects filing classified against the SOURCE that produced it."""
    memo: dict = {}

    def filing(k: str, r: str, stack=()) -> tuple[str, list]:
        """(class, evidence) for 'k produces r', from k's source. Molecules: routes via operands."""
        if (k, r) in memo:
            return memo[(k, r)]
        e = source_of(entries, k)
        if e is None:
            return "ORPHAN", [{"why": "no entry in given.json"}]
        kind = e.get("kind")
        if kind == "PERCEPT":
            src = e.get("@grounding") if e.get("@grounding") is not None else ""
            if (e.get("grid") or {}).get("meaning", "") != src:
                out = ("STALE", [{"why": "grid.meaning differs from its @grounding source"}])
            elif r not in B._affects(src):
                out = ("STALE", [{"why": "the build's rule on the source no longer gives it"}])
            else:
                sp = spans_for(src, r)
                out = (_verdict(sp), [{"route": "grounding", **s} for s in sp])
        elif kind == "PRIMITIVE":
            nm = e.get("name")
            table = {"translate": ["drow", "dcol"], "recolour": ["colour", "colour_changed"],
                     "rotate": ["shape"], "reflect": ["shape"]}
            out = (("OK", [{"route": "build table", "why": f"{nm} -> {table[nm]}"}])
                   if r in table.get(nm, []) else
                   ("STALE", [{"why": "not in the build's PRIMITIVE affects table"}]))
        elif kind == "COMPOSITE":
            if k in stack:
                return "CYCLE", []
            ev, classes = [], []
            for i in e.get("ingredients") or []:
                ie = source_of(entries, i["ref"])
                if ie is not None and r in (ie.get("affects") or []):
                    c, _ = filing(i["ref"], r, stack + (k,))
                    if c != "CYCLE":
                        classes.append(c)
                        ev.append({"route": f"operand {i['ref']}", "status": c, "why": c})
            for s in spans_for(e.get("definition") or "", r):
                cl = _verdict([s])
                classes.append(cl)
                ev.append({"route": "definition", **s})
            if not classes:
                out = ("STALE", [{"why": "no operand files it and the definition does not say it"}])
            elif "OK" in classes:
                out = ("OK", ev)
            elif "QUESTIONED" in classes:
                out = ("QUESTIONED", ev)
            elif "STALE" in classes:
                out = ("STALE", ev)
            else:
                out = ("MISFILED", ev)
        else:
            out = ("STALE", [{"why": f"a {kind} carries no affects in the build"}])
        memo[(k, r)] = out
        return out

    rows = []
    for r, ks in (idx.get("by_reading_affects") or {}).items():
        for k in ks:
            c, ev = filing(k, r)
            rows.append({"map": "by_reading_affects", "value": r, "key": k,
                         "class": "STALE" if c == "CYCLE" else c, "evidence": ev})
    return rows, memo


def role_check(entries, idx, aff_rows) -> list[dict]:
    """by_default_role PROCESS read off `affects` (default_role): if every affects filing of the
    entry is MISFILED (or QUESTIONED), the PROCESS default rests on it too."""
    by_key = collections.defaultdict(list)
    for row in aff_rows:
        by_key[row["key"]].append(row["class"])
    out = []
    for k in (idx.get("by_default_role") or {}).get("PROCESS", []):
        e = source_of(entries, k)
        if e is None or (e.get("role_of") or {}).get("role") or e.get("kind") in ("RELATION",
                                                                                   "PRIMITIVE"):
            continue
        if _MEASURE_START.search((e.get("grid") or {}).get("meaning") or ""):
            continue
        cls = set(by_key.get(k, []))
        if cls and "OK" not in cls and "STALE" not in cls:
            c = "MISFILED" if cls == {"MISFILED"} else "QUESTIONED"
            out.append({"map": "by_default_role", "value": "PROCESS", "key": k, "class": c,
                        "evidence": f"PROCESS rests only on affects filings that are {sorted(cls)}"
                                    "; with none it is STATE"})
    return out


def run() -> dict:
    t0 = time.time()
    entries, idx, tag = load()
    rows = [r for r in structural(entries, idx, tag) if r["map"] != "by_reading_affects"]
    aff, _ = described_effect(entries, idx)
    unfiled = [r for r in structural(entries, idx, tag)
               if r["map"] == "by_reading_affects" and r["class"] != "OK"]
    roles = role_check(entries, idx, aff)
    role_keys = {r["key"] for r in roles}
    rows = [r for r in rows if not (r["map"] == "by_default_role" and r["key"] in role_keys
                                    and r["class"] == "OK")]
    allrows = rows + aff + [u for u in unfiled if u["class"] != "OK"] + roles
    counts = collections.Counter(r["class"] for r in allrows)
    per_map = collections.defaultdict(collections.Counter)
    for r in allrows:
        per_map[r["map"]][r["class"]] += 1
    return {"rows": allrows, "counts": dict(counts),
            "per_map": {k: dict(v) for k, v in sorted(per_map.items())},
            "secs": round(time.time() - t0, 1)}


def _ev_text(ev) -> str:
    if isinstance(ev, str):
        return ev
    bits = []
    for x in ev:
        if x.get("route", "").startswith("operand"):
            bits.append(f"{x['route']}: {x['status']}")
        else:
            bits.append(f"{x.get('route', '')} {x.get('status', '')} {x.get('why', '')}"
                        + (f" -- \"{x['at']}\"" if x.get("at") else ""))
    return "; ".join(bits).replace("|", "\\|")


def report_md(out: dict) -> str:
    L = ["## Counts, per map (every filing, one class each)", "",
         "| map | OK | MISFILED | QUESTIONED | ORPHAN | STALE |", "|---|---|---|---|---|---|"]
    for mp, c in out["per_map"].items():
        L.append(f"| {mp} | " + " | ".join(str(c.get(k, 0)) for k in
                                           ("OK", "MISFILED", "QUESTIONED", "ORPHAN", "STALE"))
                 + " |")
    t = out["counts"]
    L.append("| **all** | " + " | ".join(f"**{t.get(k, 0)}**" for k in
                                          ("OK", "MISFILED", "QUESTIONED", "ORPHAN", "STALE"))
             + " |")
    for cls in ("ORPHAN", "STALE", "MISFILED", "QUESTIONED"):
        sel = [r for r in out["rows"] if r["class"] == cls]
        L += ["", f"## {cls} ({len(sel)})", ""]
        if not sel:
            L.append("None.")
            continue
        # atoms first (the source of the filing), then molecules that only inherit it
        sel.sort(key=lambda r: (r["map"], all(x.get("route", "").startswith("operand")
                                               for x in r["evidence"])
                                if isinstance(r["evidence"], list) else False,
                                r["key"], r["value"]))
        L += ["| map | filed under | entry | evidence |", "|---|---|---|---|"]
        for r in sel:
            L.append(f"| {r['map']} | {r['value']} | {r['key'].replace('|', chr(92) + '|')} | "
                     f"{_ev_text(r['evidence'])} |")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    out = run()
    print(f"index_audit: {sum(out['counts'].values())} filings in {out['secs']}s -- "
          + ", ".join(f"{k} {v}" for k, v in sorted(out["counts"].items())))
    for mp, c in out["per_map"].items():
        print(f"  {mp:22s} " + ", ".join(f"{k} {v}" for k, v in sorted(c.items())))
    if "--json" in sys.argv:
        Path(sys.argv[sys.argv.index("--json") + 1]).write_text(
            json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    if "--md" in sys.argv:
        Path(sys.argv[sys.argv.index("--md") + 1]).write_text(report_md(out), encoding="utf-8")
    raise SystemExit(1 if out["counts"].get("ORPHAN") or out["counts"].get("STALE") else 0)
