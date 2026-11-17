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
  priors         object concept -> action verbs named in its gloss or derivationally related ('+'),
                 each with moves_object / moves_via (its sense is verb.motion or its '@' chain
                 reaches one)
  shape_bridge   a DECLARED 2D shape -> 3D form -> object table (a convention), each resolved to
                 a verified synset and attached to the objects' priors
  concept_actions  object/shape concept -> ranked verbs from the REVERSE dictionary read (verb
                 synsets whose gloss or quoted example names the noun) merged with the priors,
                 each verb mapped to library entries sharing its sense (library_atoms)

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
# concept_actions: DECLARED conventions (Figure 10), visible and movable, not derived
ACTIONS_CAP = 25  # actions kept per concept after ranking
ACTION_LEXNAMES = ("verb.motion", "verb.contact", "verb.change", "verb.creation",
                   "verb.consumption", "verb.possession", "verb.competition", "verb.perception",
                   "verb.social")
REVERSE_NGRAM = 4  # longest noun collocation looked up in a verb gloss/example
PLURAL_STRIP = (("ies", "y"), ("es", ""), ("s", ""))
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


# DECLARED conventions (Figure 10), visible and movable: what counts as a physical object concept,
# the verb lexnames that fit one, and the plausibility test on a reverse-index example hit
OBJECT_NOUN_LEXNAMES = ("noun.artifact", "noun.object")
OBJECT_VERB_LEXNAMES = ("verb.contact", "verb.motion")
EXAMPLE_VERB_LEXNAMES = ("verb.contact", "verb.motion", "verb.possession", "verb.competition",
                         "verb.consumption", "verb.creation", "verb.change")
EXAMPLE_NOUN_LEXNAMES = ("noun.artifact", "noun.object", "noun.shape", "noun.animal",
                         "noun.plant", "noun.food", "noun.body")


def verb_sense(wn: WordNet, verb: str, concept_ctx: set[str], physical: bool = False) -> dict:
    """The verb's sense for a concept: when the concept is a physical object (artifact/object),
    a sense whose lexname is in OBJECT_VERB_LEXNAMES is preferred over any other (in that
    order: contact, then motion) and among those WordNet sense order decides (gloss overlap
    picked figurative senses); for any other concept the most context-word overlap, then WordNet
    sense order. The reason is recorded."""
    best = None
    for rank, sid in enumerate(wn.index["v"].get(verb, [])):
        score = len(concept_ctx & wn.context_words(sid))
        ln = wn.syn[sid]["lexname"]
        fit = physical and ln in OBJECT_VERB_LEXNAMES
        order = len(OBJECT_VERB_LEXNAMES) - OBJECT_VERB_LEXNAMES.index(ln) if fit else 0
        key = (order, 0 if fit else score, -rank)
        if best is None or key > best[0]:
            best = (key, rank, sid)
    (order, score, _), rank, sid = best
    fit = order > 0
    reason = (f"object concept: lexname {wn.syn[sid]['lexname']} fits a physical object "
              "(preferred over other lexnames; contact before motion), then sense order" if fit else
              f"context overlap {score}, then sense order")
    return {"verb_synset": sid, "verb_lexname": wn.syn[sid]["lexname"],
            "verb_sense_order": rank + 1, "verb_sense_reason": reason, **moves_object(wn, sid)}


MOVES_LEXNAME = "verb.motion"


def moves_object(wn: WordNet, vsid: str) -> dict:
    """Does acting on an object with this verb sense predict that the object moves? True when the
    sense's own lexname is verb.motion, or when its WordNet hypernym chain ('@' pointers in
    data.verb, followed breadth-first in pointer order to the root, every branch) reaches a
    verb.motion synset: a cause-to-move verb (throw -> propel -> move, displace). moves_via is the
    path from the sense to the first verb.motion synset reached; when none is reached it is every
    ancestor searched, in visit order (the closure named, so the False is readable). Read from
    WordNet's own hierarchy, never a hand list."""
    def tag(s: str) -> str:
        return f"{s} {wn.syn[s]['lemmas'][0].lower()} ({wn.syn[s]['lexname']})"
    parent: dict[str, str | None] = {vsid: None}
    queue, order = [vsid], []
    while queue:
        cur = queue.pop(0)
        order.append(cur)
        if wn.syn[cur]["lexname"] == MOVES_LEXNAME:
            path = []
            while cur is not None:
                path.append(tag(cur))
                cur = parent[cur]
            return {"moves_object": True, "moves_via": path[::-1]}
        for sym, tgt, _, _ in wn.syn[cur]["ptrs"]:
            if sym == "@" and tgt in wn.syn and tgt not in parent:
                parent[tgt] = cur
                queue.append(tgt)
    return {"moves_object": False, "moves_via": [tag(s) for s in order]}


def example_noun_sense(wn: WordNet, noun: str, vsid: str) -> str | None:
    """The noun's sense in a verb's example: the noun synset with most context-word overlap with
    the verb synset; ties go to WordNet sense order. None when the noun is a word of the verb's
    own multi-word lemma (an idiom such as 'have a ball': the noun names no object there)."""
    for lem in wn.syn[vsid]["lemmas"]:
        toks = lem.lower().split("_")
        if len(toks) > 1 and noun in toks:
            return None
    vctx = wn.context_words(vsid)
    best = None
    for rank, nsid in enumerate(wn.index["n"].get(noun.replace(" ", "_"), [])):
        key = (len(vctx & wn.context_words(nsid)), -rank)
        if best is None or key > best[0]:
            best = (key, nsid)
    return best[1] if best else None


def concept_priors(wn: WordNet, concept: str, sid: str, stamp: dict) -> list[dict]:
    s = wn.syn[sid]
    ctx = wn.context_words(sid)
    phys = s["lexname"] in OBJECT_NOUN_LEXNAMES
    rows, seen = [], set()
    for verb, how in gloss_verbs(wn, s["gloss"]):
        if (verb, "gloss") in seen:
            continue
        seen.add((verb, "gloss"))
        rows.append({"concept": concept, "concept_synset": sid, "action_verb": verb,
                     **verb_sense(wn, verb, ctx, phys), "source": "gloss", "evidence": how,
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
                         **verb_sense(wn, verb, ctx, phys), "source": "gloss",
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
                         "verb_sense_order": None, **moves_object(wn, tgt),
                         "source": "derivation",
                         "evidence": f"'+' from {s['lemmas'][src - 1 if src else 0]}",
                         "stamp": stamp, "standing": "none"})
    return rows


def _ngrams_text(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:[-'][a-z0-9]+)*", (text or "").lower())


def reverse_index(wn: WordNet) -> dict[str, list[tuple[str, str]]]:
    """THE REVERSE DICTIONARY READ: noun lemma -> [(verb synset, 'gloss'|'example')] for every verb
    synset whose definition or quoted example sentence names that noun lemma. Each verb gloss is
    split into its definition (before the first quote) and its quoted examples; each is tokenized
    at word boundaries, lower-cased, and every 1..REVERSE_NGRAM-token span is looked up in the noun
    index (multi-word lemmas joined by spaces), as written and with a simple plural strip of the
    last token (-ies -> -y, -es, -s). STOP words are never indexed."""
    nouns = {k.replace("_", " ") for k in wn.index["n"] if k not in STOP}
    out: dict[str, list[tuple[str, str]]] = {}
    for sid in sorted(s for s in wn.syn if s.startswith("v")):
        g = wn.syn[sid]["gloss"]
        parts = [("gloss", g.split('"')[0])] + [("example", x) for x in re.findall(r'"([^"]*)"', g)]
        seen = set()
        for where, text in parts:
            toks = _ngrams_text(text)
            for i in range(len(toks)):
                for n in range(1, REVERSE_NGRAM + 1):
                    if i + n > len(toks):
                        break
                    span = toks[i:i + n]
                    last = span[-1]
                    forms = [last] + [last[: -len(s)] + r for s, r in PLURAL_STRIP
                                      if last.endswith(s) and len(last) > len(s) + 2]
                    for f in forms:
                        lem = " ".join(span[:-1] + [f])
                        if lem in nouns and (lem, where) not in seen:
                            seen.add((lem, where))
                            out.setdefault(lem, []).append((sid, where))
                            break
    return out


SOURCE_RANK = {"reverse-example": 0, "reverse-gloss": 1}


def concept_actions(wn: WordNet, rev: dict, concept: str, sid: str, extra: list[str],
                    prior_rows: list[dict], stamp: dict, lemma_entries: dict
                    ) -> tuple[dict, int, int]:
    """One concept: the verbs from the reverse index (its synset's lemmas plus any extra names,
    e.g. an ImageNet label's head noun) merged with its forward priors, keyed by verb synset;
    kept by ACTION_LEXNAMES, ranked, capped at ACTIONS_CAP. Returns (row, dropped by lexname)."""
    names = sorted({lem.lower().replace("_", " ") for lem in wn.syn[sid]["lemmas"]}
                   | {e.lower() for e in extra if e})
    acts: dict[str, dict] = {}

    def add(vsid: str, verb: str, source: str, matched: str | None = None) -> None:
        a = acts.get(vsid)
        if a is None:
            a = acts[vsid] = {"verb": verb, "verb_synset": vsid,
                              "verb_lexname": wn.syn[vsid]["lexname"],
                              "verb_lemmas": [x.lower().replace("_", " ")
                                              for x in wn.syn[vsid]["lemmas"]],
                              "sources": [], "matched": []}
        if source not in a["sources"]:
            a["sources"].append(source)
        if matched and matched not in a["matched"]:
            a["matched"].append(matched)

    implausible = 0
    for name in names:
        for vsid, where in rev.get(name, []):
            if where == "example":
                nsid = example_noun_sense(wn, name, vsid)
                if (wn.syn[vsid]["lexname"] not in EXAMPLE_VERB_LEXNAMES or nsid is None
                        or wn.syn[nsid]["lexname"] not in EXAMPLE_NOUN_LEXNAMES):
                    implausible += 1
                    continue
            add(vsid, wn.syn[vsid]["lemmas"][0].lower().replace("_", " "),
                f"reverse-{where}", f"{name}@{where}")
    for p in prior_rows:
        vsid = p["verb_synset"]
        if vsid not in wn.syn:
            continue
        src = ("derivation" if p["source"] == "derivation" else
               f"hypernym:{p['via_hypernym']}" if p.get("via_hypernym") else "gloss-forward")
        add(vsid, p["action_verb"], src)
    kept, dropped = [], 0
    for a in acts.values():
        if a["verb_lexname"] not in ACTION_LEXNAMES:
            dropped += 1
            continue
        a["sources"].sort(key=lambda s: (SOURCE_RANK.get(s, 2), s))
        a["n_sources"] = len(a["sources"])
        a["matched"].sort()
        atoms = set()
        for w in a["verb_lemmas"]:
            for r in lemma_entries.get(w, []):
                if r["synset"] == a["verb_synset"]:   # a shared sense, never a spelling alone
                    atoms.add(r["entry"])
        a["library_atoms"] = sorted(atoms)
        kept.append(a)
    kept.sort(key=lambda a: (-a["n_sources"], min(SOURCE_RANK.get(s, 2) for s in a["sources"]),
                             a["verb"], a["verb_synset"]))
    # the merge never loses an existing forward prior: every action carrying a forward source is
    # kept, and the cap's remaining slots go to reverse-only actions in rank order
    fwd = [a for a in kept if any(s not in SOURCE_RANK for s in a["sources"])]
    room = max(0, ACTIONS_CAP - len(fwd))
    rev_only = [a for a in kept if all(s in SOURCE_RANK for s in a["sources"])]
    chosen = {id(a) for a in fwd + rev_only[:room]}
    out = [a for a in kept if id(a) in chosen]
    row = {"concept": concept, "synset": sid, "names_matched": names, "stamp": stamp,
           "standing": "none", "actions": out, "actions_total": len(kept),
           "actions_capped": len(kept) - len(out), "dropped_by_lexname": dropped,
           "dropped_implausible_example": implausible}
    return row, dropped, implausible


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
                                        "verb_lexname": p["verb_lexname"], "source": p["source"],
                                        "moves_object": p["moves_object"],
                                        "moves_via": p["moves_via"]}
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

    # concept_actions: the reverse dictionary read merged with the forward priors above
    rev = reverse_index(wn)
    prior_of: dict[tuple[str, str], list[dict]] = {}
    for p in priors:
        prior_of.setdefault((p["concept"], p["concept_synset"]), []).append(p)
    todo: list[tuple[str, str, list[str]]] = []
    for sid, rows in sorted(by_concept_sid.items()):
        todo.append((rows[0]["concept"] if rows else
                     f"bridge:{wn.syn[sid]['lemmas'][0].lower()}", sid, []))
    for c in lib["lexicon"]["classes"]:
        sid = "n" + c["wnid"][1:]
        if sid in wn.syn:
            head = re.findall(r"[a-z0-9'-]+", c["label"].split(",")[0].lower())
            todo.append((f"imagenet:{c['index']}:{c['label']}", sid,
                         [lem.replace("_", " ") for lem in c.get("lemmas") or []]
                         + head[-1:]))
    for full, e in sorted(entries.items()):
        if e["category"] in ("object", "shape"):
            for sid in e["chosen"]:
                todo.append((full, sid, []))
    actions_rows, dropped_lex, dropped_ex = [], 0, 0
    for concept, sid, extra in todo:
        row, d, dx = concept_actions(wn, rev, concept, sid, extra, prior_of.get((concept, sid), []),
                                 stamp, synonym_index)
        actions_rows.append(row)
        dropped_lex += d
        dropped_ex += dx
    actions_rows.sort(key=lambda r: (r["concept"], r["synset"]))
    rev_hits = [h for hs in rev.values() for h in hs]
    act_src = Counter(s for r in actions_rows for a in r["actions"] for s in a["sources"])
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
            "priors_moves_object": dict(sorted(Counter(
                ("own_lexname" if p["verb_lexname"] == MOVES_LEXNAME else "via_hypernym")
                if p["moves_object"] else "false" for p in priors).items())),
            "shape_bridge_rows": len(bridge),
        },
        "concept_actions_method": (
            "REVERSE DICTIONARY READ: every verb synset in data.verb is split into its definition "
            "and its quoted example sentences; each is tokenized at word boundaries, lower-cased, "
            f"and every 1..{REVERSE_NGRAM}-token span is looked up in index.noun (as written, then "
            "with the last token's plural stripped: -ies->-y, -es, -s); STOP words never indexed. "
            "A concept (each shape_bridge object; each lexicon class, by its synset lemmas, its "
            "lemmas and its label's head noun; each entry of category object or shape, by its "
            "chosen synsets' lemmas) collects the verb synsets naming any of its names "
            "('reverse-example' / 'reverse-gloss'), merged by verb synset with its forward priors "
            "('gloss-forward', 'derivation', 'hypernym:<sid>'). The noun's SENSE in the verb text "
            "is disambiguated only for example hits: the noun sense with most context overlap with "
            "the verb synset; an example hit is kept only when the verb's lexname is in "
            "example_verb_lexnames AND that noun sense's lexname is in example_noun_lexnames "
            "(a noun inside the verb's own multi-word lemma is an idiom with no object sense: "
            "'have a ball' drops; counted in dropped_implausible_example); every row "
            "has standing none. Forward priors of an artifact/object concept prefer a verb sense "
            "in object_verb_lexnames (verb_sense_reason). Kept: verb_lexname in "
            "concept_actions_lexnames; ranked n_sources desc, "
            "then best source (reverse-example > reverse-gloss > others), then verb, then synset; "
            "capped: every action with a forward source (an existing prior) is kept, and the "
            "remaining slots up to the cap go to reverse-only actions in rank order, so the merge "
            "never loses an existing prior (a concept whose forward priors alone exceed the cap "
            "keeps them all). library_atoms: entries whose chosen sense IS the verb synset, "
            "reached through the synonym index by the verb's lemmas (every tie carried; a "
            "spelling alone never attaches)."),
        "concept_actions_cap": ACTIONS_CAP,
        "concept_actions_cap_note": "a DECLARED CONVENTION (build_word_map.ACTIONS_CAP), "
                                    "visible and movable, not derived; actions_total and "
                                    "actions_capped per row show what it cut",
        "concept_actions_lexnames": list(ACTION_LEXNAMES),
        "object_noun_lexnames": list(OBJECT_NOUN_LEXNAMES),
        "object_verb_lexnames": list(OBJECT_VERB_LEXNAMES),
        "moves_object_rule": (
            "every prior (and every shape_bridge object action) carries moves_object: True when "
            f"its verb sense's lexname is {MOVES_LEXNAME}, or when its WordNet hypernym chain "
            "('@' pointers in data.verb, followed breadth-first to the root, every branch) "
            f"reaches a {MOVES_LEXNAME} synset (a cause-to-move verb: throw -> propel -> move, "
            "displace); moves_via is the path to that synset, or every ancestor searched when "
            "none is reached. Read from WordNet's hierarchy, never a hand list; a prediction "
            "with no standing, the board tests it"),
        "example_verb_lexnames": list(EXAMPLE_VERB_LEXNAMES),
        "example_noun_lexnames": list(EXAMPLE_NOUN_LEXNAMES),
        "concept_actions_counts": {
            "concepts": len(actions_rows),
            "concepts_with_actions": sum(bool(r["actions"]) for r in actions_rows),
            "actions_kept": sum(len(r["actions"]) for r in actions_rows),
            "actions_capped": sum(r["actions_capped"] for r in actions_rows),
            "dropped_by_lexname": dropped_lex,
            "dropped_implausible_example": dropped_ex,
            "actions_by_source": dict(sorted(act_src.items())),
            "actions_with_library_atoms": sum(bool(a["library_atoms"]) for r in actions_rows
                                              for a in r["actions"]),
            "reverse_index_noun_lemmas": len(rev),
            "reverse_index_hits": len(rev_hits),
            "reverse_index_hits_by_where": dict(sorted(Counter(w for _, w in rev_hits).items())),
            "reverse_index_verb_synsets": len({s for s, _ in rev_hits}),
        },
    }
    doc = {"header": header, "entries": entries, "synonym_index": dict(sorted(
        synonym_index.items())), "priors": priors, "shape_bridge": bridge,
        "shape_bridge_dropped": dropped, "concept_actions": actions_rows}
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
