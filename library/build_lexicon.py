"""THE LEXICON, groundwork: the 1000 ImageNet-1k classes mapped onto WordNet 3.0, as provenanced
library data that NOTHING in the agent reads yet ("readers": [] in the header; the same rule as
library/tether_rules.json, kept apart from lookups).

README Future state, "a voice, by mapping rather than training" (Isaiah): an ImageNet class id IS
a WordNet noun offset, so a label carries its synonym set, its definition and its hypernym chain
up to entity without anything being trained. This file builds only that mapping.

Inputs (read-only, outside the repo; root from --data or env LEXICON_DATA_DIR):
  wordnet/dict/data.noun, wordnet/dict/index.noun   Princeton WordNet 3.0 (WNdb-3.0.tar.gz)
  imagenet-1k/classes.py                            the HF ILSVRC/imagenet-1k label list
  thesaurus/en_thesaurus.jsonl                      zaibacu thesaurus (extracted from WordNet)

Derivation, per class i: the label's first lemma is looked up in index.noun; the candidate
synset whose full lemma list equals the label's comma list is the derived wnid ("lemmas"). Where
more than one candidate fits (crane the bird, crane the machine), the ILSVRC rule that index
order is ascending wnid order picks the one between its neighbours ("lemmas+order"). The derived
wnid is compared with classes.py's published id; any class that does not derive, or derives to a
different id, is listed in header.unmatched and never guessed.

    python library/build_lexicon.py            write library/lexicon_imagenet_wordnet.json
    python library/build_lexicon.py --check    rebuild in memory, compare sha256, exit 1 on diff
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import sys
from itertools import pairwise

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "lexicon_imagenet_wordnet.json")
DATA_DEFAULT = r"C:\TETHER_RUNS\DATA_2026-11-16"
BUILD_DATE = "2026-11-16"  # fixed, so --check is byte-for-byte
ENTITY = "n00001740"

INPUTS = {  # role -> path under the data root (forward slashes in the header)
    "wordnet_data_noun": "wordnet/dict/data.noun",
    "wordnet_index_noun": "wordnet/dict/index.noun",
    "wordnet_tarball": "wordnet/WNdb-3.0.tar.gz",
    "imagenet_classes": "imagenet-1k/classes.py",
    "thesaurus": "thesaurus/en_thesaurus.jsonl",
}

WORDNET_LICENSE = (
    "WordNet Release 3.0 This software and database is being provided to you, the LICENSEE, by "
    "Princeton University under the following license. By obtaining, using and/or copying this "
    "software and database, you agree that you have read, understood, and will comply with these "
    "terms and conditions.: Permission to use, copy, modify and distribute this software and "
    "database and its documentation for any purpose and without fee or royalty is hereby "
    "granted, provided that you agree to comply with the following copyright notice and "
    "statements, including the disclaimer, and that the same appear on ALL copies of the "
    "software, database and documentation, including modifications that you make for internal "
    "use or for distribution. WordNet 3.0 Copyright 2006 by Princeton University. All rights "
    "reserved. THIS SOFTWARE AND DATABASE IS PROVIDED \"AS IS\" AND PRINCETON UNIVERSITY MAKES "
    "NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED. BY WAY OF EXAMPLE, BUT NOT "
    "LIMITATION, PRINCETON UNIVERSITY MAKES NO REPRESENTATIONS OR WARRANTIES OF MERCHANT- "
    "ABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF THE LICENSED SOFTWARE, "
    "DATABASE OR DOCUMENTATION WILL NOT INFRINGE ANY THIRD PARTY PATENTS, COPYRIGHTS, "
    "TRADEMARKS OR OTHER RIGHTS. The name of Princeton University or Princeton may not be used "
    "in advertising or publicity pertaining to distribution of the software and/or database. "
    "Title to copyright in this software, database and any associated documentation shall at "
    "all times remain with Princeton University and LICENSEE agrees to preserve same."
)

IMAGENET_NOTE = (
    "ImageNet (ILSVRC2012, HF ILSVRC/imagenet-1k, license imagenet-agreement): the database is "
    "for non-commercial research and educational purposes only. Only the 1000-class LABEL LIST "
    "(classes.py: wnid -> label) is used here; no image, and nothing derived from an image, is "
    "in this file or in the repository."
)


def data_root(arg: str | None = None) -> str:
    return arg or os.environ.get("LEXICON_DATA_DIR") or DATA_DEFAULT


def _sha(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def parse_data_line(line: str) -> dict:
    """One data.noun line (Princeton wndb(5)): offset lex_filenum ss_type w_cnt word lex_id ...
    p_cnt [ptr offset pos src/tgt]... | gloss."""
    head, _, gloss = line.partition(" | ")
    f = head.split()
    w_cnt = int(f[3], 16)
    words = [f[4 + 2 * k] for k in range(w_cnt)]
    words = [w.split("(")[0] if w.endswith(")") else w for w in words]  # adj markers (none in n.)
    at = 4 + 2 * w_cnt
    p_cnt = int(f[at])
    ptrs = [(f[at + 1 + 4 * k], f[at + 2 + 4 * k], f[at + 3 + 4 * k]) for k in range(p_cnt)]
    hyper = [off for sym, off, pos in ptrs if sym in ("@", "@i") and pos == "n"]
    return {"offset": f[0], "lemmas": words, "hypernyms": hyper, "gloss": gloss.strip()}


def load_wordnet(root: str) -> tuple[dict, dict]:
    data, index = {}, {}
    with open(os.path.join(root, INPUTS["wordnet_data_noun"]), encoding="utf-8") as f:
        for line in f:
            if not line.startswith("  "):
                rec = parse_data_line(line.rstrip("\n"))
                data[rec["offset"]] = rec
    with open(os.path.join(root, INPUTS["wordnet_index_noun"]), encoding="utf-8") as f:
        for line in f:
            if line.startswith("  "):
                continue
            g = line.split()
            p_cnt = int(g[3])
            synset_cnt = int(g[2])
            index[g[0]] = g[4 + p_cnt + 2:4 + p_cnt + 2 + synset_cnt]
    return data, index


def load_classes(root: str) -> list[tuple[str, str]]:
    """classes.py's OrderedDict literal, read by ast (never executed)."""
    with open(os.path.join(root, INPUTS["imagenet_classes"]), encoding="utf-8") as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and getattr(node.func, "id", "") == "OrderedDict":
            d = node.args[0]
            return [(k.value, v.value) for k, v in zip(d.keys, d.values, strict=True)]
    raise SystemExit("classes.py: no OrderedDict literal found")


def load_thesaurus(root: str, wanted: set[str]) -> dict:
    """noun entries keyed by lower-cased word, only for the words asked about."""
    out: dict[str, list] = {}
    with open(os.path.join(root, INPUTS["thesaurus"]), encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            w = rec["word"].lower()
            if rec["pos"] == "noun" and w in wanted:
                out.setdefault(w, []).append(rec)
    return out


def _norm(s: str) -> str:
    return s.replace("_", " ").strip().lower()


def derive(classes: list, data: dict, index: dict) -> list[dict]:
    """Label -> wnid by lemma match, then the ascending rule for ties. Returns one row per
    class: derived wnid (or None) and the method."""
    rows = []
    for _wnid, label in classes:
        names = [_norm(p) for p in label.split(", ")]
        cands = index.get(names[0].replace(" ", "_"), [])
        full = [o for o in cands if [_norm(w) for w in data[o]["lemmas"]] == names]
        rows.append({"cands": sorted(full), "fit": sorted(full), "derived": None,
                     "match": "unmatched"})
    for r in rows:
        if len(r["cands"]) == 1:
            r["derived"], r["match"] = "n" + r["cands"][0], "lemmas"
    for i, r in enumerate(rows):
        if len(r["cands"]) > 1:
            lo = next((rows[j]["derived"] for j in range(i - 1, -1, -1) if rows[j]["derived"]),
                      "n00000000")
            hi = next((rows[j]["derived"] for j in range(i + 1, len(rows))
                       if rows[j]["derived"]), "n99999999")
            fit = r["fit"] = [c for c in r["cands"] if lo < "n" + c < hi]
            if len(fit) == 1:
                r["derived"], r["match"] = "n" + fit[0], "lemmas+order"
    return rows


def chain(offset: str, data: dict) -> list[list[str]]:
    """Hypernym chain from the synset's first listed hypernym (@ or @i) up to entity."""
    out, seen = [], {offset}
    cur = data[offset]
    while cur["hypernyms"]:
        nxt = cur["hypernyms"][0]
        if nxt in seen:
            break
        seen.add(nxt)
        cur = data[nxt]
        out.append(["n" + nxt, cur["lemmas"][0]])
    return out


def thesaurus_for(lemma: str, rec: dict, thes: dict) -> dict | None:
    """The thesaurus entry for this sense of the first lemma: same word, noun, and its first
    definition equal to the WordNet 3.0 gloss's first segment (the thesaurus's wordnet_id is
    another release's offset, so ids are not compared)."""
    first = rec["gloss"].split("; ")[0].strip()
    for t in thes.get(lemma.lower(), []):
        if t["desc"] and t["desc"][0].strip() == first:
            syn = sorted(t["synonyms"])
            mine = {_norm(w) for w in rec["lemmas"]} - {_norm(lemma)}
            theirs = {_norm(s) for s in syn} - {_norm(lemma)}
            return {"key": t["key"], "synonyms": syn, "agrees_with_wordnet": theirs == mine}
    return None


def build(root: str) -> bytes:
    data, index = load_wordnet(root)
    classes = load_classes(root)
    rows = derive(classes, data, index)
    firsts = {data[w[1:]]["lemmas"][0].lower() for w, _ in classes if w[1:] in data}
    thes = load_thesaurus(root, firsts)
    entries, unmatched = [], []
    for i, ((wnid, label), r) in enumerate(zip(classes, rows, strict=True)):
        rec = data.get(wnid[1:])
        match = r["match"] if r["derived"] == wnid and rec is not None else "unmatched"
        if match == "unmatched" and r["derived"] is None and wnid[1:] in r["fit"]:
            match = "ambiguous"
        if match in ("unmatched", "ambiguous"):
            unmatched.append({"index": i, "label": label, "published_wnid": wnid, "kind": match,
                              "derived_wnid": r["derived"],
                              "candidates": ["n" + c for c in r["cands"]],
                              "candidates_in_order": ["n" + c for c in r["fit"]]})
        e = {"index": i, "label": label, "wnid": wnid, "match": match}
        if rec is not None:
            e["lemmas"] = rec["lemmas"]
            e["gloss"] = rec["gloss"]
            e["hypernym_chain"] = chain(rec["offset"], data)
            e["thesaurus"] = thesaurus_for(rec["lemmas"][0], rec, thes)
        entries.append(e)
    wnids = [w for w, _ in classes]
    sources = {}
    for role, rel in INPUTS.items():
        p = os.path.join(root, rel)
        sources[role] = {"file": rel, "bytes": os.path.getsize(p), "sha256": _sha(p)}
    sources["imagenet_classes"]["origin"] = (
        "https://huggingface.co/datasets/ILSVRC/imagenet-1k (classes.py)")
    sources["wordnet_tarball"]["origin"] = "https://wordnetcode.princeton.edu/3.0/WNdb-3.0.tar.gz"
    sources["wordnet_data_noun"]["origin"] = "WNdb-3.0.tar.gz dict/data.noun"
    sources["wordnet_index_noun"]["origin"] = "WNdb-3.0.tar.gz dict/index.noun"
    sources["thesaurus"]["origin"] = (
        "https://raw.githubusercontent.com/zaibacu/thesaurus/master/en_thesaurus.jsonl "
        "(extracted from WordNet; its wordnet_id values are NOT WordNet 3.0 offsets, e.g. tench "
        "01443405 there, 01440764 in 3.0, so senses are matched by word + first definition)")
    header = {
        "what": "ImageNet-1k class index -> WordNet 3.0 noun synset (wnid = 'n' + 8-digit "
                "data.noun offset): lemmas, gloss, hypernym chain to entity, thesaurus synonyms. "
                "Groundwork for README Future state 'a voice, by mapping rather than training'.",
        "readers": [],
        "readers_note": "NOTHING in the agent reads this file (tests/test_lexicon.py L3); "
                        "kept apart from lookups like library/tether_rules.json.",
        "build": "python library/build_lexicon.py (--check rebuilds and compares sha256)",
        "build_date": BUILD_DATE,
        "sources": sources,
        "wordnet_license": WORDNET_LICENSE,
        "imagenet_terms": IMAGENET_NOTE,
        "fields": {
            "index": "ILSVRC2012 class index (0-999)",
            "label": "the imagenet label string, verbatim from classes.py",
            "wnid": "the published wnid (classes.py); index order is ascending wnid order",
            "match": "how the label derived this wnid from WordNet: 'lemmas' (the one synset "
                     "whose lemma list equals the label), 'lemmas+order' (several did; the "
                     "ascending rule picked one), 'ambiguous' (several synsets carry exactly these "
                     "lemmas and the published one is among those the ascending rule allows; "
                     "WordNet alone cannot choose, so it is listed, not guessed), 'unmatched' "
                     "(no synset carries the label's lemmas; listed)",
            "lemmas": "the WordNet 3.0 synset's lemmas, verbatim (underscores kept)",
            "gloss": "the WordNet 3.0 gloss, verbatim",
            "hypernym_chain": "[wnid, first lemma] from the first listed @/@i hypernym of each "
                              "synset up to entity n00001740",
            "thesaurus": "zaibacu entry for the first lemma's sense: key, synonyms, and whether "
                         "they equal the synset's other lemmas; null if no sense matched",
        },
        "counts": {
            "classes": len(entries),
            "matched_unique": len(entries) - len(unmatched),
            "match_lemmas": sum(e["match"] == "lemmas" for e in entries),
            "match_lemmas_order": sum(e["match"] == "lemmas+order" for e in entries),
            "ambiguous": sum(e["match"] == "ambiguous" for e in entries),
            "unmatched": sum(e["match"] == "unmatched" for e in entries),
            "wnids_strictly_ascending": all(a < b for a, b in pairwise(wnids)),
            "chains_reach_entity": sum(bool(e.get("hypernym_chain"))
                                       and e["hypernym_chain"][-1][0] == ENTITY
                                       for e in entries),
            "thesaurus_found": sum(e.get("thesaurus") is not None for e in entries),
            "thesaurus_agrees": sum(bool(e.get("thesaurus"))
                                    and e["thesaurus"]["agrees_with_wordnet"]
                                    for e in entries),
        },
        "unmatched": unmatched,
    }
    doc = {"header": header, "classes": entries}
    return (json.dumps(doc, sort_keys=True, indent=1, ensure_ascii=False) + "\n").encode("utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="rebuild in memory and compare sha256")
    ap.add_argument("--data", default=None, help=f"data root (default {DATA_DEFAULT})")
    a = ap.parse_args(argv)
    blob = build(data_root(a.data))
    new = hashlib.sha256(blob).hexdigest()
    if a.check:
        with open(OUT, "rb") as f:
            old = hashlib.sha256(f.read()).hexdigest()
        if old != new:
            print(f"lexicon --check: DIFFERS committed {old} rebuilt {new}")
            return 1
        print(f"lexicon --check: OK sha256 {new}")
        return 0
    with open(OUT, "wb") as f:
        f.write(blob)
    c = json.loads(blob)["header"]["counts"]
    print(f"wrote {OUT} {len(blob)} B sha256 {new}")
    print(json.dumps(c, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
