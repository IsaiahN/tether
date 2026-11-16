"""THE WORD MAP, groundwork: the library's entries connected to WordNet 3.0 words, so that with a
dictionary a reader can go word/concept -> entry -> category -> action. Provenanced library data
that NOTHING in the agent reads yet ("readers": [] in the header, the rule of
library/build_lexicon.py), and every row carries NO standing (C3): a prior is a prediction to be
tested by the board, never a finding.

Write-up docs/05-RESEARCH/40-WATSON_2026-11-13_RECURSIVE_DIFFUSION_LEARNING.md: "shape -> concept
-> properties -> predictions"; thesaurus groups keep their senses apart (a sense is a synset,
never a spelling); attach by cluster, never by raw name; preloaded with no standing; C6 stamps.

Sections:
  entries        library entry -> name words -> ranked WordNet candidate senses (with reasons) ->
                 chosen sense(s) -> category (WordNet lexname) beside the library's own
                 by_kind/by_default_role category; disagreements flagged, never overridden
  synonym_index  word -> library entries through a shared synset of a chosen sense
  priors         object concept -> action verbs named in its gloss or derivationally related ('+')
  shape_bridge   a DECLARED 2D shape -> 3D form -> object table (a convention), each resolved to
                 a verified synset and attached to the objects' priors

Inputs (read-only, outside the repo; root from --data or env WORDMAP_DATA_DIR):
  wordnet/dict/data.{noun,verb,adj,adv}, index.{noun,verb,adj,adv}   Princeton WordNet 3.0
  library/given.json, library/ATTRIBUTE_INDEX.json, library/index.json,
  library/lexicon_imagenet_wordnet.json                                (in the repo)

    python library/build_word_map.py            write library/word_map.json
    python library/build_word_map.py --check    rebuild in memory, compare sha256, exit 1 on diff
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "word_map.json")
DATA_DEFAULT = r"C:\TETHER_RUNS\DATA_2026-11-16"
BUILD_DATE = "2026-11-16"  # fixed, so --check is byte-for-byte
POS_FILES = {"n": "noun", "v": "verb", "a": "adj", "r": "adv"}
INPUTS = {f"wordnet_{k}_{p}": f"wordnet/dict/{k}.{p}" for p in POS_FILES.values()
          for k in ("data", "index")}
LIBRARY = {"given": "given.json", "attribute_index": "ATTRIBUTE_INDEX.json",
           "index": "index.json", "lexicon": "lexicon_imagenet_wordnet.json"}

# the 45 lexicographer files of WordNet 3.0 (lexnames(5WN)); the lexnames file is not in the
# data drop, so the published table is carried verbatim, indexed by lex_filenum
LEXNAMES = [
    "adj.all", "adj.pert", "adv.all", "noun.Tops", "noun.act", "noun.animal", "noun.artifact",
    "noun.attribute", "noun.body", "noun.cognition", "noun.communication", "noun.event",
    "noun.feeling", "noun.food", "noun.group", "noun.location", "noun.motive", "noun.object",
    "noun.person", "noun.phenomenon", "noun.plant", "noun.possession", "noun.process",
    "noun.quantity", "noun.relation", "noun.shape", "noun.state", "noun.substance", "noun.time",
    "verb.body", "verb.change", "verb.cognition", "verb.communication", "verb.competition",
    "verb.consumption", "verb.contact", "verb.creation", "verb.emotion", "verb.motion",
    "verb.perception", "verb.possession", "verb.social", "verb.stative", "verb.weather",
    "adj.ppl"]

CATEGORY_OF_LEXNAME = {
    "noun.shape": "shape",
    **{f"noun.{x}": "object" for x in ("artifact", "object", "animal", "person", "plant", "food",
                                        "body", "substance", "possession")},
    "noun.act": "action", "noun.event": "action", "noun.process": "action",
    "noun.phenomenon": "action",
    "noun.relation": "relation", "noun.location": "relation", "adj.pert": "relation",
    "noun.attribute": "property", "noun.state": "property", "noun.feeling": "property",
    "adj.all": "property", "adj.ppl": "property", "adv.all": "property",
    "noun.quantity": "measure", "noun.time": "measure",
    "noun.cognition": "rule",
    "noun.Tops": "other", "noun.communication": "other", "noun.group": "other",
    "noun.motive": "other",
    **{n: "action" for n in LEXNAMES if n.startswith("verb.")},
}
CATEGORY_OF_LIBRARY = {  # the library's own by_default_role (and kind RELATION) -> category
    "PROCESS": "action", "CAUSE": "action", "MEASURE": "measure", "RULE": "rule",
    "TEST": "rule", "RELATION": "relation", "INSTRUMENT": "object", "AGENT": "object",
    "STATE": "property", "RESULT": "property",
}
CLUSTER_LEXNAMES = {  # ATTRIBUTE_INDEX cluster (or a DOMAIN of the same name) -> lexnames it fits
    "ACTION": ["noun.act"] + [n for n in LEXNAMES if n.startswith("verb.")],
    "FORCE": ["verb.contact", "noun.phenomenon"],
    "SPEED": ["noun.attribute", "noun.quantity", "verb.motion"],
    "TIME": ["noun.time", "noun.event"],
    "CHANGE": ["verb.change", "noun.process", "noun.event"],
    "SIGNAL": ["noun.communication", "verb.communication", "verb.perception"],
    "CONTACT": ["verb.contact"],
    "EXTENT": ["noun.quantity", "noun.attribute", "noun.shape"],
    "STRUCTURE": ["noun.artifact", "noun.shape", "noun.group", "noun.relation"],
    "STATE": ["noun.state", "adj.all", "noun.attribute"],
    "DIRECTION": ["noun.location", "adv.all", "verb.motion"],
    "COUNT": ["noun.quantity"],
    "POSITION": ["noun.location", "noun.relation"],
    "SHAPE": ["noun.shape"],
    "IDENTITY": ["noun.cognition", "noun.relation"],
    "MOTION": ["verb.motion", "noun.act", "noun.event"],
    "COLOUR": ["noun.attribute", "adj.all"],
    "TOPOLOGICAL": ["noun.shape", "noun.relation"],
    "GEOMETRIC": ["noun.shape"],
}
STOP = set(re.findall(r"[a-z]+", """
a an the of and or in on at to for by with from as is are was be been being it its
this that these those which who whom what when where how not no into over under than then e g
eg ie etc vs via per one two any some all each such their his her our your used use"""))
LIGHT_VERBS = {"be", "have", "do", "get", "use", "make", "become", "seem", "go", "take", "give"}
# morphy detachment rules (morphy(7WN)); exception lists are not in the data drop, so -n/-en
# participles (thrown, broken) get the two extra rules below, marked as an extension
MORPHY = {"n": [("s", ""), ("ses", "s"), ("xes", "x"), ("zes", "z"), ("ches", "ch"),
                ("shes", "sh"), ("men", "man"), ("ies", "y")],
          "v": [("s", ""), ("ies", "y"), ("es", "e"), ("es", ""), ("ed", "e"), ("ed", ""),
                ("ing", "e"), ("ing", ""), ("n", ""), ("en", "")],
          "a": [("er", ""), ("est", ""), ("er", "e"), ("est", "e")], "r": []}
SENSE_RULE = (
    "Candidates: the entry name's head word (the last content word, or the last before 'of'), "
    "or the whole name as a WordNet collocation when it is one, looked up in index.* of every "
    "part of speech through morphy. Each candidate synset scores 2 per context lexname fit "
    "(the entry's DOMAIN and ATTRIBUTE_INDEX clusters against CLUSTER_LEXNAMES) plus 1 per "
    "context word (domain, clusters, tag names, definition and grid meaning; never the name's "
    "own words) found among the synset's gloss words, lemmas and hypernym lemmas. Chosen: the "
    "top-scoring synset(s) when the top score is > 0; every synset tied at the top is recorded "
    "(status 'tie'), none dropped. A sole candidate is chosen as 'sole_sense' (no choice to "
    "make). Several candidates and no context evidence: status 'no_context', nothing chosen -- "
    "never a pick by spelling or by frequency rank.")
FLAT_NOTE = ("held on flat boards, settles as depth only on boards with depth; settles as "
             "behaviour on any board")

# DECLARED convention (Figure 10): the 2D -> 3D -> object table is authored here, visible and
# movable; each name resolves to the first sense in index order whose lexname is the one named
# (and whose gloss holds the cue, when one is given); a name that does not resolve is dropped and
# listed, never guessed
SHAPE_BRIDGE = [
    {"shape_2d": [("circle", "noun.shape", "ellipse"), ("disk", "noun.shape", ""),
                  ("disc", "noun.shape", "")],   # "disc": arc_percept's shape_name spelling
     "form_3d": [("sphere", "noun.shape", "")],
     "objects": [("ball", "noun.artifact", "round"), ("globe", "noun.artifact", "map"),
                 ("marble", "noun.artifact", "ball")]},
    {"shape_2d": [("square", "noun.shape", "")],
     "form_3d": [("cube", "noun.shape", "")],
     "objects": [("block", "noun.artifact", ""), ("box", "noun.artifact", "container"),
                 ("die", "noun.artifact", "cube")]},
    {"shape_2d": [("rectangle", "noun.shape", "")],
     "form_3d": [("parallelepiped", "noun.shape", ""), ("box", "noun.shape", "")],
     "objects": [("brick", "noun.artifact", ""), ("block", "noun.artifact", "")]},
    {"shape_2d": [("ring", "noun.shape", "")],
     "form_3d": [("torus", "noun.shape", ""), ("hoop", "noun.shape", "")],
     "objects": [("ring", "noun.artifact", "band"), ("hoop", "noun.artifact", ""),
                 ("tire", "noun.artifact", "")]},
    {"shape_2d": [("line", "noun.shape", "")],
     "form_3d": [("cylinder", "noun.shape", ""), ("rod", "noun.shape", "")],
     "objects": [("stick", "noun.artifact", ""), ("rod", "noun.artifact", ""),
                 ("pole", "noun.artifact", "")]},
    {"shape_2d": [("triangle", "noun.shape", "")],
     "form_3d": [("cone", "noun.shape", ""), ("pyramid", "noun.shape", "")],
     "objects": [("cone", "noun.artifact", ""), ("pyramid", "noun.artifact", "")]},
]

# names the builder refuses: an observation id ('o12') or a move list is a recording, not a
# concept, and must never be given a word (the membrane lets only methods cross)
REFUSE = [re.compile(r"^[a-z]{1,2}\d+$", re.I),
          re.compile(r"^(?:(?:up|down|left|right|action\d+|click|noop|[udlr])[\s,;>]+)+"
                     r"(?:up|down|left|right|action\d+|click|noop|[udlr])$", re.I)]

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


def data_root(arg: str | None = None) -> str:
    return arg or os.environ.get("WORDMAP_DATA_DIR") or DATA_DEFAULT


def _sha(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _words(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z]+", (text or "").lower()) if w not in STOP]


class WordNet:
    """data.* and index.* of all four parts of speech; a synset id is pos letter + offset."""

    def __init__(self, root: str):
        self.syn: dict[str, dict] = {}
        self.index: dict[str, dict[str, list[str]]] = {p: {} for p in POS_FILES}
        for p, name in POS_FILES.items():
            with open(os.path.join(root, f"wordnet/dict/data.{name}"), encoding="utf-8") as f:
                for line in f:
                    if not line.startswith("  "):
                        self._data_line(p, line.rstrip("\n"))
            with open(os.path.join(root, f"wordnet/dict/index.{name}"), encoding="utf-8") as f:
                for line in f:
                    if line.startswith("  "):
                        continue
                    g = line.split()
                    p_cnt, n = int(g[3]), int(g[2])
                    self.index[p][g[0]] = [p + o for o in g[4 + p_cnt + 2:4 + p_cnt + 2 + n]]

    def _data_line(self, p: str, line: str) -> None:
        head, _, gloss = line.partition(" | ")
        f = head.split()
        w_cnt = int(f[3], 16)
        words = [re.sub(r"\(.*\)$", "", f[4 + 2 * k]) for k in range(w_cnt)]
        at = 4 + 2 * w_cnt
        p_cnt = int(f[at])
        ptrs = []
        for k in range(p_cnt):
            sym, off, pos, st = f[at + 1 + 4 * k: at + 5 + 4 * k]
            ptrs.append((sym, ("a" if pos == "s" else pos) + off, int(st[:2], 16),
                         int(st[2:], 16)))
        self.syn[p + f[0]] = {"id": p + f[0], "lexname": LEXNAMES[int(f[1])],
                              "lemmas": words, "ptrs": ptrs, "gloss": gloss.strip()}

    def morphy(self, word: str, p: str) -> list[tuple[str, str]]:
        """[(lemma, rule)] for a surface form in part of speech p: the form itself, then the
        detachment rules."""
        out = []
        if word in self.index[p]:
            out.append((word, "base"))
        for suf, rep in MORPHY[p]:
            if word.endswith(suf) and len(word) > len(suf) + 1:
                base = word[: len(word) - len(suf)] + rep
                if base in self.index[p] and base not in [b for b, _ in out]:
                    out.append((base, f"-{suf}+{rep}" if rep else f"-{suf}"))
        return out

    def context_words(self, sid: str) -> set[str]:
        s = self.syn[sid]
        ws = set(_words(s["gloss"]))
        for lem in s["lemmas"]:
            ws.update(_words(lem.replace("_", " ")))
        for sym, tgt, _, _ in s["ptrs"]:
            if sym in ("@", "@i") and tgt in self.syn:
                for lem in self.syn[tgt]["lemmas"]:
                    ws.update(_words(lem.replace("_", " ")))
        return {_norm_noun(self, w) for w in ws}


def _norm_noun(wn: WordNet, w: str) -> str:
    m = wn.morphy(w, "n") or wn.morphy(w, "v")
    return m[0][0] if m else w


def head_word(name: str) -> tuple[str | None, list[str]]:
    toks = re.findall(r"[a-z]+", name.lower())
    if "of" in toks and toks.index("of") > 0:
        cand = [t for t in toks[: toks.index("of")] if t not in STOP]
    else:
        cand = [t for t in toks if t not in STOP]
    return (cand[-1] if cand else None), toks


def refuse_names(names: list[str]) -> None:
    for full in names:
        name = full.split("|", 1)[-1].strip()
        for rx in REFUSE:
            if rx.match(name):
                raise SystemExit(f"word_map: REFUSED planted name {full!r} (an observation id or "
                                 f"move list is a recording, not a concept)")


def entry_senses(wn: WordNet, full: str, rec: dict, clusters: list[str]) -> dict:
    domain, _, name = full.partition("|")
    head, toks = head_word(name)
    ctx_keys = sorted({domain.upper(), *clusters})
    fit = {ln for k in ctx_keys for ln in CLUSTER_LEXNAMES.get(k, [])}
    ctx_text = " ".join([domain, " ".join(clusters), " ".join((rec.get("tags") or {})
                                                              .get("primary") or []),
                         rec.get("definition") or "", (rec.get("grid") or {}).get("meaning") or ""])
    ctx = {_norm_noun(wn, w) for w in _words(ctx_text)} - set(toks) - {head}
    phrase = "_".join(toks)
    looked: list[tuple[str, str, str]] = []  # (synset, lemma, morphy rule)
    if len(toks) > 1:
        for p in POS_FILES:
            if phrase in wn.index[p]:
                looked += [(s, phrase, "collocation") for s in wn.index[p][phrase]]
    if not looked and head:
        for p in POS_FILES:
            for lem, rule in wn.morphy(head, p):
                looked += [(s, lem, rule) for s in wn.index[p][lem]]
    seen, cands = set(), []
    for rank, (sid, lem, rule) in enumerate(looked):
        if sid in seen:
            continue
        seen.add(sid)
        s = wn.syn[sid]
        hits = sorted(ctx & wn.context_words(sid))
        lexfit = s["lexname"] in fit
        cands.append({"synset": sid, "lemma": lem, "morphy": rule, "lexname": s["lexname"],
                      "score": 2 * lexfit + len(hits), "lexname_fits_context": lexfit,
                      "gloss_hits": hits, "sense_order": rank + 1})
    cands.sort(key=lambda c: (-c["score"], c["sense_order"]))
    if not cands:
        status, chosen = "no_sense", []
    elif len(cands) == 1:
        status, chosen = "sole_sense", [cands[0]["synset"]]
    elif cands[0]["score"] == 0:
        status, chosen = "no_context", []
    else:
        top = [c["synset"] for c in cands if c["score"] == cands[0]["score"]]
        status, chosen = ("tie" if len(top) > 1 else "context"), top
    return {"head_word": head, "context_keys": ctx_keys, "candidates": cands[:8],
            "candidates_total": len(cands), "status": status, "chosen": chosen}


def gloss_verbs(wn: WordNet, gloss: str) -> list[tuple[str, str]]:
    """Verbs a gloss names: an inflected form morphy takes to a verb (-ed/-ing/-s/-n), a word
    after 'to' or after a form of 'be', a word coordinated ('or'/'and') with one already taken,
    or a word that is a verb and no other part of speech. Light verbs are skipped."""
    toks = re.findall(r"[a-z]+", gloss.split('"')[0].lower())
    out, prev_verb = [], False
    for i, t in enumerate(toks):
        before = toks[i - 1] if i else ""
        vm = wn.morphy(t, "v")
        hit = None
        if vm:
            infl = [(b, r) for b, r in vm if r != "base"]
            participle = [(b, r) for b, r in infl if not r.startswith(("-s", "-es", "-ies"))]
            plural_noun = any(r != "base" for _, r in wn.morphy(t, "n"))
            if participle:  # -ed/-ing/-n/-en: a verb form even where WordNet also lists it
                hit = (participle[0][0], "inflected " + participle[0][1])
            elif infl and not plural_noun and t not in wn.index["n"] and t not in wn.index["a"]:
                hit = (infl[0][0], "inflected " + infl[0][1])
            elif before == "to" and vm[0][1] == "base":
                hit = (t, "after 'to'")
            elif before in ("is", "are", "was", "be", "been", "being") and infl:
                hit = (infl[0][0], "after 'be' " + infl[0][1])
            elif before in ("is", "are", "be") and vm[0][1] == "base":
                hit = (t, "after 'be'")
            elif before in ("or", "and") and prev_verb:
                hit = (vm[0][0], "coordinated")
            elif vm[0][1] == "base" and all(t not in wn.index[p] for p in ("n", "a", "r")):
                hit = (t, "verb only")
        if hit and hit[0] not in LIGHT_VERBS:
            out.append(hit)
            prev_verb = True
        elif t not in ("or", "and"):
            prev_verb = False
    return out


def verb_sense(wn: WordNet, verb: str, concept_ctx: set[str]) -> dict:
    best = None
    for rank, sid in enumerate(wn.index["v"].get(verb, [])):
        score = len(concept_ctx & wn.context_words(sid))
        if best is None or score > best[0]:
            best = (score, rank, sid)
    _, rank, sid = best
    return {"verb_synset": sid, "verb_lexname": wn.syn[sid]["lexname"],
            "verb_sense_order": rank + 1}


def concept_priors(wn: WordNet, concept: str, sid: str, stamp: dict) -> list[dict]:
    s = wn.syn[sid]
    ctx = wn.context_words(sid)
    rows, seen = [], set()
    for verb, how in gloss_verbs(wn, s["gloss"]):
        if (verb, "gloss") in seen:
            continue
        seen.add((verb, "gloss"))
        rows.append({"concept": concept, "concept_synset": sid, "action_verb": verb,
                     **verb_sense(wn, verb, ctx), "source": "gloss", "evidence": how,
                     "stamp": stamp, "standing": "none"})
    # one level of inheritance (shape -> concept -> properties): the first hypernym's gloss verbs
    # are carried as gloss priors with the hypernym named (a soccer ball is a ball: hit, kick)
    hyp = next((t for sym, t, _, _ in s["ptrs"] if sym in ("@", "@i") and t in wn.syn), None)
    if hyp:
        for verb, how in gloss_verbs(wn, wn.syn[hyp]["gloss"]):
            if (verb, "gloss") in seen:
                continue
            seen.add((verb, "gloss"))
            rows.append({"concept": concept, "concept_synset": sid, "action_verb": verb,
                         **verb_sense(wn, verb, ctx), "source": "gloss",
                         "evidence": f"{how}; via hypernym {hyp} "
                                     f"{wn.syn[hyp]['lemmas'][0]}",
                         "via_hypernym": hyp, "stamp": stamp, "standing": "none"})
    for sym, tgt, src, dst in s["ptrs"]:
        if sym == "+" and tgt.startswith("v") and tgt in wn.syn:
            t = wn.syn[tgt]
            verb = t["lemmas"][dst - 1 if dst else 0].lower()
            if (verb, "derivation") in seen or verb in LIGHT_VERBS:
                continue
            seen.add((verb, "derivation"))
            rows.append({"concept": concept, "concept_synset": sid, "action_verb": verb,
                         "verb_synset": tgt, "verb_lexname": t["lexname"],
                         "verb_sense_order": None, "source": "derivation",
                         "evidence": f"'+' from {s['lemmas'][src - 1 if src else 0]}",
                         "stamp": stamp, "standing": "none"})
    return rows


def resolve(wn: WordNet, lemma: str, lexname: str, cue: str) -> str | None:
    for sid in wn.index["n"].get(lemma, []):
        s = wn.syn[sid]
        if s["lexname"] == lexname and (not cue or cue in _words(s["gloss"])):
            return sid
    return None


def build(root: str) -> bytes:
    wn = WordNet(root)
    lib = {}
    for k, v in LIBRARY.items():
        with open(os.path.join(HERE, v), encoding="utf-8") as fh:
            lib[k] = json.load(fh)
    given = lib["given"]["entries"]
    refuse_names(list(given))
    atom_attr = lib["attribute_index"]["atom_attributes"]
    ix = lib["index"]["index"]
    kind_of = {e: k for k, es in ix["by_kind"].items() for e in es}
    role_of = {e: r for r, es in ix["by_default_role"].items() for e in es}
    wn_sha = _sha(os.path.join(root, INPUTS["wordnet_data_noun"]))
    stamp = {"stage": "regularity", "corpus": "wordnet-3.0", "sha": wn_sha[:16]}

    entries, synonym_index, priors = {}, {}, []
    disagree = 0
    for full in sorted(given):
        rec = given[full]
        clusters = sorted((atom_attr.get(full) or {}).get("clusters") or [])
        m = entry_senses(wn, full, rec, clusters)
        cats = sorted({CATEGORY_OF_LEXNAME[wn.syn[s]["lexname"]] for s in m["chosen"]})
        cat_wn = cats[0] if len(cats) == 1 else (None if not cats else "other")
        kind, role = kind_of.get(full), role_of.get(full)
        cat_lib = "relation" if kind == "RELATION" else CATEGORY_OF_LIBRARY.get(role)
        flag = bool(cat_wn and cat_lib and cat_wn != cat_lib)
        disagree += flag
        m.update({"clusters": clusters, "category_wordnet": cat_wn,
                  "category_wordnet_candidates": cats, "library_kind": kind,
                  "library_default_role": role, "category_library": cat_lib,
                  "category": cat_wn or cat_lib or "other",
                  "category_source": "wordnet" if cat_wn else ("library" if cat_lib else "none"),
                  "disagreement": flag})
        entries[full] = m
        for sid in m["chosen"]:
            for lem in wn.syn[sid]["lemmas"]:
                w = lem.lower().replace("_", " ")
                synonym_index.setdefault(w, []).append({"entry": full, "synset": sid})
            if cat_wn == "object":
                priors += concept_priors(wn, full, sid, stamp)
    for c in lib["lexicon"]["classes"]:
        sid = "n" + c["wnid"][1:]
        if sid in wn.syn:
            priors += concept_priors(wn, f"imagenet:{c['index']}:{c['label']}", sid, stamp)

    by_concept_sid: dict[str, list[dict]] = {}
    bridge, dropped = [], []
    bstamp = {"stage": "abstraction", "corpus": "declared+wordnet", "sha": wn_sha[:16]}
    for row in SHAPE_BRIDGE:
        out = {}
        for part in ("shape_2d", "form_3d", "objects"):
            got = []
            for lem, lexname, cue in row[part]:
                sid = resolve(wn, lem, lexname, cue)
                if sid is None:
                    dropped.append({"part": part, "lemma": lem, "lexname": lexname, "cue": cue})
                    continue
                item = {"name": lem, "synset": sid, "lexname": lexname,
                        "gloss": wn.syn[sid]["gloss"]}
                if part == "objects":
                    if sid not in by_concept_sid:
                        by_concept_sid[sid] = concept_priors(wn, f"bridge:{lem}", sid, stamp)
                    item["actions"] = [{"verb": p["action_verb"], "verb_synset": p["verb_synset"],
                                        "verb_lexname": p["verb_lexname"], "source": p["source"]}
                                       for p in by_concept_sid[sid]]
                got.append(item)
            out[part] = got
        if all(out[p] for p in ("shape_2d", "form_3d", "objects")):
            bridge.append({**out, "stamp": bstamp, "standing": "none", "note": FLAT_NOTE})
        else:
            dropped.append({"row_dropped": [x[0] for x in row["shape_2d"]]})
    for _sid, rows in sorted(by_concept_sid.items()):
        priors += rows

    for w in synonym_index:
        synonym_index[w].sort(key=lambda r: (r["entry"], r["synset"]))
    priors.sort(key=lambda p: (p["concept"], p["source"], p["action_verb"]))
    hist = Counter(e["category"] for e in entries.values())
    sources = {}
    for role, rel in INPUTS.items():
        p = os.path.join(root, rel)
        sources[role] = {"file": rel, "bytes": os.path.getsize(p), "sha256": _sha(p),
                         "origin": f"WNdb-3.0.tar.gz dict/{rel.split('/')[-1]}"}
    for role, rel in LIBRARY.items():
        p = os.path.join(HERE, rel)
        sources[f"library_{role}"] = {"file": f"library/{rel}", "bytes": os.path.getsize(p),
                                      "sha256": _sha(p)}
    header = {
        "what": "library entry -> WordNet 3.0 senses -> category; word -> entry by shared synset; "
                "object concept -> action verbs (gloss and '+' derivation); a declared 2D -> 3D -> "
                "object shape bridge. Groundwork for word/concept -> action.",
        "readers": [],
        "readers_note": "NOTHING in the agent reads this file (tests/test_word_map.py W0).",
        "standing": "none",
        "standing_note": "every row is a preloaded prediction with NO standing (C3); stamps "
                         "(C6) name the stage and corpus; the board tests them",
        "build": "python library/build_word_map.py (--check rebuilds and compares sha256)",
        "build_date": BUILD_DATE,
        "sources": sources,
        "wordnet_license": WORDNET_LICENSE,
        "lexnames": LEXNAMES,
        "sense_choice_rule": SENSE_RULE,
        "category_map": CATEGORY_OF_LEXNAME,
        "category_library_map": {**CATEGORY_OF_LIBRARY, "kind RELATION": "relation"},
        "category_rule": "category = the chosen senses' lexname category when they agree "
                         "(several -> 'other', candidates listed); else the library's by_kind/"
                         "by_default_role category; both written, a difference flagged "
                         "'disagreement', never overridden",
        "cluster_lexnames": CLUSTER_LEXNAMES,
        "morphy": {k: [f"-{a}+{b}" for a, b in v] for k, v in MORPHY.items()},
        "morphy_note": "verb.exc etc. are not in the data drop; -n/-en are added verb rules so "
                       "participles like 'thrown' reach 'throw'",
        "refused_names": [r.pattern for r in REFUSE],
        "shape_bridge_note": "shape_bridge is a DECLARED CONVENTION (authored in "
                             "build_word_map.SHAPE_BRIDGE, visible and movable), not derived; each "
                             "name resolves to the first index-order sense with the named lexname "
                             "(and gloss cue); unresolved names are listed in shape_bridge_dropped",
        "counts": {
            "entries": len(entries),
            "entries_mapped": sum(bool(e["chosen"]) for e in entries.values()),
            "status": dict(sorted(Counter(e["status"] for e in entries.values()).items())),
            "categories": dict(sorted(hist.items())),
            "category_source": dict(sorted(Counter(e["category_source"]
                                                   for e in entries.values()).items())),
            "disagreements": disagree,
            "synonym_index_words": len(synonym_index),
            "priors": len(priors),
            "priors_by_source": dict(sorted(Counter(p["source"] for p in priors).items())),
            "priors_concepts": len({p["concept"] for p in priors}),
            "shape_bridge_rows": len(bridge),
        },
    }
    doc = {"header": header, "entries": entries, "synonym_index": dict(sorted(
        synonym_index.items())), "priors": priors, "shape_bridge": bridge,
        "shape_bridge_dropped": dropped}
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
            print(f"word_map --check: DIFFERS committed {old} rebuilt {new}")
            return 1
        print(f"word_map --check: OK sha256 {new}")
        return 0
    with open(OUT, "wb") as f:
        f.write(blob)
    print(f"wrote {OUT} {len(blob)} B sha256 {new}")
    print(json.dumps(json.loads(blob)["header"]["counts"], sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
