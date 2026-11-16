"""build_relations -- WordNet minus NSM, ConceptNet edges, VerbNet classes (Isaiah 2026-11-16:
"use WordNet and then subtract NSM, you get the subjects and verbs, and then import
verbnet/conceptnet"). A builder, not the agent: it imports nsm only for the primes list it
subtracts, and writes two files that are preloaded with NO standing (docs/05-RESEARCH/
40-WATSON_2026-11-13_RECURSIVE_DIFFUSION_LEARNING.md C3, C6) and readers: [].

  library/vocabulary.json   WordNet 3.0 noun+verb lemmas minus the NSM primes/allolexes
                            (case-insensitive; a multi-word prime matched as its WordNet
                            underscore form), each with POS, its senses' lexnames, and for verbs
                            their VerbNet classes.
  library/relations.json    ConceptNet 5.7 /c/en/ -> /c/en/ edges (CapableOf, ReceivesAction,
                            UsedFor, IsA, HasProperty) grouped by concept, only concepts in the
                            vocabulary; concept_actions_cn: the verbs of CapableOf /
                            ReceivesAction / UsedFor normalised by morphy, with VerbNet classes.

The ConceptNet pass streams the .csv.gz (never decompressed to disk) once into a filtered cache
beside the source (keyed by the source's sha256); a rebuild or --check reads that cache.

  python library/build_relations.py           build
  python library/build_relations.py --check   rebuild in memory; exit 1 unless byte-identical
"""

from __future__ import annotations

import argparse
import glob
import gzip
import hashlib
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = r"C:\TETHER_RUNS\DATA_2026-11-16"
WN = os.path.join(DATA, "wordnet", "dict")
CN = os.path.join(DATA, "conceptnet", "conceptnet-assertions-5.7.0.csv.gz")
CN_CACHE = os.path.join(DATA, "conceptnet", "cn_en_filtered.json")
VN = os.path.join(DATA, "verbnet", "cu-clear-verbnet", "verbnet3.4")
OUT_VOCAB = os.path.join(HERE, "vocabulary.json")
OUT_REL = os.path.join(HERE, "relations.json")
RELS = ("CapableOf", "HasProperty", "IsA", "ReceivesAction", "UsedFor")
ACTION_RELS = ("CapableOf", "ReceivesAction", "UsedFor")
AUX = {
    "be",
    "is",
    "are",
    "was",
    "were",
    "been",
    "being",
    "get",
    "gets",
    "got",
    "gotten",
    "to",
    "can",
    "could",
    "will",
    "may",
    "might",
    "often",
    "usually",
    "sometimes",
    "not",
    "a",
    "an",
    "the",
}
VOCAB_CAP = 15_000_000
REL_CAP = 30_000_000


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


# ---------------------------------------------------------------- NSM
def nsm_terms() -> tuple:
    """The NSM primes and allolexes as lowercase WordNet lemma forms: every token primes() gives,
    ALLOLEX's inflections, and each multi-word prime phrase grammar.json writes (underscored)."""
    sys.path.insert(0, ROOT)
    import nsm
    import store

    words = {w.lower() for w in nsm.primes()} | {w.lower() for w in nsm.ALLOLEX}
    g = store.grammar()
    f = g.get("frames_nsm") or {}
    src = [s for k in ("substantives", "frames", "connectives") for s in f.get(k, [])]
    src += [s for v in (f.get("primes_full") or {}).values() if isinstance(v, list) for s in v]
    src += [str(op.get("nsm") or "") for op in (g.get("operators") or {}).values()]
    phrases = set()
    for s in src:
        for part in re.split(r"[/,;]", re.sub(r"[()]", " ", str(s))):
            toks = re.findall(r"[A-Za-z']+", part)
            if len(toks) > 1 and all(t.isupper() for t in toks):
                phrases.add("_".join(t.lower() for t in toks))
    return frozenset(words | phrases), len(words), len(phrases)


# ---------------------------------------------------------------- WordNet
# WordNet 3.0's lexnames file (the dict folder here ships without it): lex_filenum -> name
LEXNAMES = [
    "adj.all",
    "adj.pert",
    "adv.all",
    "noun.Tops",
    "noun.act",
    "noun.animal",
    "noun.artifact",
    "noun.attribute",
    "noun.body",
    "noun.cognition",
    "noun.communication",
    "noun.event",
    "noun.feeling",
    "noun.food",
    "noun.group",
    "noun.location",
    "noun.motive",
    "noun.object",
    "noun.person",
    "noun.phenomenon",
    "noun.plant",
    "noun.possession",
    "noun.process",
    "noun.quantity",
    "noun.relation",
    "noun.shape",
    "noun.state",
    "noun.substance",
    "noun.time",
    "verb.body",
    "verb.change",
    "verb.cognition",
    "verb.communication",
    "verb.competition",
    "verb.consumption",
    "verb.contact",
    "verb.creation",
    "verb.emotion",
    "verb.motion",
    "verb.perception",
    "verb.possession",
    "verb.social",
    "verb.stative",
    "verb.weather",
    "adj.ppl",
]
# The dict folder also ships without verb.exc: the common irregular past forms morphy needs
# for ConceptNet's ReceivesAction targets ('be thrown'), stated here as data.
IRREGULAR = dict(
    p.split(":")
    for p in [
        "threw:throw",
        "thrown:throw",
        "broke:break",
        "broken:break",
        "ate:eat",
        "eaten:eat",
        "rode:ride",
        "ridden:ride",
        "drove:drive",
        "driven:drive",
        "flew:fly",
        "flown:fly",
        "fell:fall",
        "fallen:fall",
        "held:hold",
        "hung:hang",
        "kept:keep",
        "left:leave",
        "made:make",
        "ran:run",
        "sat:sit",
        "saw:see",
        "seen:see",
        "shot:shoot",
        "spun:spin",
        "struck:strike",
        "swam:swim",
        "swum:swim",
        "took:take",
        "taken:take",
        "tore:tear",
        "torn:tear",
        "wore:wear",
        "worn:wear",
        "won:win",
        "wrote:write",
        "written:write",
        "bit:bite",
        "bitten:bite",
        "blew:blow",
        "blown:blow",
        "built:build",
        "caught:catch",
        "dug:dig",
        "drew:draw",
        "drawn:draw",
        "drank:drink",
        "drunk:drink",
        "fed:feed",
        "fought:fight",
        "found:find",
        "gave:give",
        "given:give",
        "got:get",
        "gotten:get",
        "grew:grow",
        "grown:grow",
        "hid:hide",
        "hidden:hide",
        "knew:know",
        "known:know",
        "laid:lay",
        "led:lead",
        "lit:light",
        "lost:lose",
        "meant:mean",
        "met:meet",
        "paid:pay",
        "said:say",
        "sent:send",
        "shook:shake",
        "shaken:shake",
        "shone:shine",
        "sold:sell",
        "sang:sing",
        "sung:sing",
        "slid:slide",
        "spent:spend",
        "stood:stand",
        "stole:steal",
        "stolen:steal",
        "stuck:stick",
        "swung:swing",
        "taught:teach",
        "thought:think",
        "told:tell",
        "understood:understand",
        "woke:wake",
        "woken:wake",
        "went:go",
        "gone:go",
        "did:do",
        "done:do",
        "bought:buy",
        "brought:bring",
        "chose:choose",
        "chosen:choose",
        "came:come",
        "began:begin",
        "begun:begin",
        "bent:bend",
        "bound:bind",
        "bred:breed",
        "burnt:burn",
        "dealt:deal",
        "forgot:forget",
        "forgotten:forget",
        "froze:freeze",
        "frozen:freeze",
        "ground:grind",
        "lent:lend",
        "sank:sink",
        "sunk:sink",
        "spat:spit",
        "sprang:spring",
        "sprung:spring",
        "stung:sting",
        "swept:sweep",
        "wound:wind",
        "wove:weave",
        "woven:weave",
        "sewn:sew",
        "sown:sow",
        "mown:mow",
        "shorn:shear",
        "sought:seek",
        "slept:sleep",
        "wept:weep",
        "fled:flee",
    ]
)


def lexnames() -> dict:
    p = os.path.join(WN, "lexnames")
    if not os.path.exists(p):
        return dict(enumerate(LEXNAMES))
    out = {}
    with open(p, encoding="utf-8") as f:
        for line in f:
            q = line.split()
            if len(q) >= 2:
                out[int(q[0])] = q[1]
    return out


def wn_index(pos: str) -> dict:
    """lemma -> [synset offsets] from index.<pos>."""
    out = {}
    with open(os.path.join(WN, "index." + pos), encoding="utf-8") as f:
        for line in f:
            if line.startswith(" "):
                continue
            p = line.split()
            n_syn, n_ptr = int(p[2]), int(p[3])
            out[p[0]] = p[6 + n_ptr : 6 + n_ptr + n_syn]
    return out


def wn_lexfile(pos: str) -> dict:
    out = {}
    with open(os.path.join(WN, "data." + pos), encoding="utf-8") as f:
        for line in f:
            if line.startswith(" "):
                continue
            p = line.split(" ", 2)
            out[p[0]] = int(p[1])
    return out


def wn_exc(pos: str) -> dict:
    if not os.path.exists(os.path.join(WN, pos + ".exc")):
        return dict(IRREGULAR)
    out = {}
    with open(os.path.join(WN, pos + ".exc"), encoding="utf-8") as f:
        for line in f:
            p = line.split()
            if len(p) >= 2:
                out.setdefault(p[0], p[1])
    return out


VERB_RULES = (
    ("s", ""),
    ("ies", "y"),
    ("es", "e"),
    ("es", ""),
    ("ed", "e"),
    ("ed", ""),
    ("ing", "e"),
    ("ing", ""),
)


def morphy_verb(word: str, verbs: dict, exc: dict) -> str | None:
    """WordNet's morphy for a verb: the exception list, the word itself, then the detachment
    rules (and a doubled final consonant, 'stopped' -> stop)."""
    if word in exc and exc[word] in verbs:
        return exc[word]
    if word in verbs:
        return word
    for suf, rep in VERB_RULES:
        if word.endswith(suf):
            base = word[: len(word) - len(suf)] + rep
            if base in verbs:
                return base
            if rep == "" and len(base) > 2 and base[-1] == base[-2] and base[:-1] in verbs:
                return base[:-1]
    return None


# ---------------------------------------------------------------- VerbNet
def verbnet() -> tuple:
    """(class -> {members: [{name, wn}], roles: [...]}, verb lemma -> [classes]); empty when the
    clone is absent."""
    classes, by_verb = {}, {}
    files = sorted(glob.glob(os.path.join(VN, "**", "*.xml"), recursive=True))

    def walk(node, inherited_roles):
        cid = node.get("ID")
        roles = sorted(
            {r.get("type") for r in node.findall("./THEMROLES/THEMROLE") if r.get("type")}
            | set(inherited_roles)
        )
        members = sorted(
            (
                {"name": m.get("name"), "wn": (m.get("wn") or "").split()}
                for m in node.findall("./MEMBERS/MEMBER")
                if m.get("name")
            ),
            key=lambda m: m["name"],
        )
        classes[cid] = {"members": members, "roles": roles}
        for m in members:
            by_verb.setdefault(m["name"], set()).add(cid)
        for sub in node.findall("./SUBCLASSES/VNSUBCLASS"):
            walk(sub, roles)

    for p in files:
        try:
            root = ET.parse(p).getroot()
        except ET.ParseError:
            continue
        if root.tag == "VNCLASS" and root.get("ID"):
            walk(root, [])
    return classes, {k: sorted(v) for k, v in by_verb.items()}, files


# ---------------------------------------------------------------- ConceptNet
def cn_filter(src_sha: str) -> dict:
    """Stream the assertions .csv.gz once; keep /c/en/ -> /c/en/ edges of RELS with weight and
    surfaceText. Cached beside the source under its sha256 (the cache is data, not the repo)."""
    if os.path.exists(CN_CACHE):
        with open(CN_CACHE, encoding="utf-8") as f:
            c = json.load(f)
        if c.get("source_sha256") == src_sha:
            return c
    keep = {"/r/" + r + "/": r for r in RELS}
    edges, n = [], 0
    with gzip.open(CN, "rt", encoding="utf-8", newline="") as f:
        for line in f:
            n += 1
            p = line.split("\t")
            rel = keep.get(p[1] + "/")
            if rel is None or not p[2].startswith("/c/en/") or not p[3].startswith("/c/en/"):
                continue
            info = json.loads(p[4])
            edges.append(
                [
                    p[2].split("/")[3],
                    rel,
                    p[3].split("/")[3],
                    float(info.get("weight", 1.0)),
                    info.get("surfaceText") or "",
                ]
            )
    edges.sort()
    c = {"source_sha256": src_sha, "lines": n, "edges": edges}
    tmp = CN_CACHE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False)
    os.replace(tmp, CN_CACHE)
    return c


def action_verb(target: str, verbs: dict, exc: dict) -> str | None:
    toks = [t for t in target.split("_") if t]
    while toks and toks[0] in AUX:
        toks = toks[1:]
    if not toks:
        return None
    if len(toks) > 1 and "_".join(toks[:2]) in verbs:
        return "_".join(toks[:2])
    return morphy_verb(toks[0], verbs, exc)


# ---------------------------------------------------------------- build
def dump(doc: dict) -> bytes:
    return (json.dumps(doc, sort_keys=True, ensure_ascii=False, indent=0) + "\n").encode("utf-8")


def build() -> tuple:
    prime_set, n_tok, n_phr = nsm_terms()
    lx = lexnames()
    nouns, verbs = wn_index("noun"), wn_index("verb")
    nlex, vlex = wn_lexfile("noun"), wn_lexfile("verb")
    vexc = wn_exc("verb")
    vn_classes, vn_by_verb, vn_files = verbnet()
    have_vn = bool(vn_classes)

    lemmas = sorted(set(nouns) | set(verbs))
    matched = sorted(w for w in lemmas if w.lower() in prime_set)
    before = {"lemmas": len(lemmas), "noun": len(nouns), "verb": len(verbs)}
    vocab = {}
    for w in lemmas:
        if w.lower() in prime_set:
            continue
        e = {}
        if w in nouns:
            e["n"] = sorted({lx[nlex[o]] for o in nouns[w]})
        if w in verbs:
            e["v"] = sorted({lx[vlex[o]] for o in verbs[w]})
            if w in vn_by_verb:
                e["vn"] = vn_by_verb[w]
        vocab[w] = e
    rule = "all WordNet noun+verb lemmas minus the NSM primes/allolexes"
    vhead = {
        "builder": "library/build_relations.py",
        "standing": "none",
        "readers": [],
        "stamps": "preloaded with no standing (docs/05-RESEARCH/40-WATSON_2026-11-13_"
        "RECURSIVE_DIFFUSION_LEARNING.md C3, C6); Isaiah 2026-11-16 'use WordNet and "
        "then subtract NSM, you get the subjects and verbs, and then import "
        "verbnet/conceptnet'",
        "sources": {
            "wordnet": {
                "path": "WordNet 3.0 dict (index.noun, index.verb, data.noun, data.verb,"
                " verb.exc, lexnames)",
                "sha256": {
                    n: sha256(os.path.join(WN, n))
                    for n in (
                        "index.noun",
                        "index.verb",
                        "data.noun",
                        "data.verb",
                        "verb.exc",
                        "lexnames",
                    )
                    if os.path.exists(os.path.join(WN, n))
                },
                "absent": "lexnames and verb.exc are not in the dict folder: lexnames "
                "are WordNet 3.0's standard 45 (LEXNAMES); morphy's verb "
                "exceptions are the IRREGULAR table in the builder",
                "licence": "WordNet 3.0 licence (Princeton University), permissive",
            },
            "nsm": {
                "path": "library/grammar.json via nsm.primes() and nsm.ALLOLEX",
                "sha256": sha256(os.path.join(HERE, "grammar.json")),
            },
            "verbnet": (
                {
                    "path": "cu-clear/verbnet verbnet3.4 (git clone --depth 1; "
                    "uvi-nlp/verbnet: repository not found)",
                    "files": len(vn_files),
                    "classes": len(vn_classes),
                    "sha256": hashlib.sha256(
                        b"".join(sha256(p).encode() for p in vn_files)
                    ).hexdigest(),
                    "licence": "VerbNet (Kipper Schuler, Palmer et al., University of "
                    "Colorado Boulder), free licence; attribution retained",
                }
                if have_vn
                else {"skipped": "github.com unreachable (DNS) at build"}
            ),
        },
        "counts": {
            "before": before,
            "after": len(vocab),
            "after_noun": sum(1 for e in vocab.values() if "n" in e),
            "after_verb": sum(1 for e in vocab.values() if "v" in e),
            "nsm_terms": len(prime_set),
            "nsm_tokens": n_tok,
            "nsm_phrases": n_phr,
            "primes_matched": len(matched),
        },
        "primes_matched": matched,
        "rule": rule,
        "format": "lemma -> {n: [noun lexnames], v: [verb lexnames], vn: [VerbNet classes]}",
    }
    vdoc = {"header": vhead, "vocabulary": vocab}
    vbytes = dump(vdoc)
    if len(vbytes) > VOCAB_CAP:
        # the stated fallback: only lemmas in word_map's synonym index, the 1000-class
        # lexicon or VerbNet
        with open(os.path.join(HERE, "word_map.json"), encoding="utf-8") as f:
            keep = set(json.load(f)["synonym_index"])
        with open(os.path.join(HERE, "lexicon_imagenet_wordnet.json"), encoding="utf-8") as f:
            lex = json.load(f)["classes"]
        for c in lex.values() if isinstance(lex, dict) else lex:
            for s in str(c.get("label", "")).split(", "):
                keep.add(s.replace(" ", "_").lower())
        keep |= set(vn_by_verb)
        vocab = {w: e for w, e in vocab.items() if w.lower() in keep}
        vhead["rule"] = (
            rule + "; over 15 MB, so only lemmas in word_map.json's synonym_index, "
            "the 1000-class lexicon's labels, or VerbNet members"
        )
        vhead["counts"]["after"] = len(vocab)
        vdoc = {"header": vhead, "vocabulary": vocab}
        vbytes = dump(vdoc)

    rel_bytes = None
    if os.path.exists(CN):
        src_sha = sha256(CN)
        c = cn_filter(src_sha)
        by_concept, seen = {}, set()
        for concept, rel, target, w, surf in c["edges"]:
            if concept not in vocab or (concept, rel, target) in seen:
                continue  # sorted edges: the first of a duplicate triple has the lowest weight
            seen.add((concept, rel, target))
            by_concept.setdefault(concept, []).append(
                {"relation": rel, "target": target, "weight": w, "surface": surf}
            )
        n_edges = sum(len(v) for v in by_concept.values())
        actions = {}
        for concept, rows in by_concept.items():
            acts = {}
            for r in rows:
                if r["relation"] in ACTION_RELS:
                    v = action_verb(r["target"], verbs, vexc)
                    if v:
                        a = acts.setdefault(v, {"relations": set(), "vn": vn_by_verb.get(v, [])})
                        a["relations"].add(r["relation"])
            if acts:
                actions[concept] = {
                    v: {"relations": sorted(a["relations"]), "vn": a["vn"]} for v, a in acts.items()
                }
        rhead = {
            "builder": "library/build_relations.py",
            "standing": "none",
            "readers": [],
            "licence": "this file is licensed CC BY-SA 4.0 (it contains ConceptNet data)",
            "attribution": {
                "conceptnet": "This work includes data from ConceptNet 5 "
                "(https://conceptnet.io), which was compiled by the Commonsense "
                "Computing Initiative. ConceptNet 5 is freely available under the "
                "Creative Commons Attribution-ShareAlike license (CC BY SA 4.0). "
                "Includes data from Wiktionary, WordNet, OMCS and others as "
                "credited at https://github.com/commonsense/conceptnet5/wiki/"
                "Copying-and-sharing-ConceptNet",
                "verbnet": (
                    "VerbNet (Kipper Schuler; Palmer, Bonial, Hwang et al., University "
                    "of Colorado Boulder), https://github.com/cu-clear/verbnet (verbnet3.4)"
                    if have_vn
                    else "VerbNet skipped: github.com unreachable at build"
                ),
                "wordnet": "Princeton WordNet 3.0 (morphy normalisation)",
            },
            "sources": {
                "conceptnet": {
                    "path": "conceptnet-assertions-5.7.0.csv.gz",
                    "sha256": src_sha,
                    "lines": c["lines"],
                    "edges_en_kept_relations": len(c["edges"]),
                }
            },
            "relations": list(RELS),
            "action_relations": list(ACTION_RELS),
            "counts": {
                "concepts": len(by_concept),
                "edges": n_edges,
                "concepts_with_actions": len(actions),
            },
            "dropped": "edges whose concept is not in vocabulary.json; duplicate (concept, "
            "relation, target) triples keep the lowest-weight row",
            "action_rule": "target split on '_', leading auxiliaries dropped (be/is/get/to/...), "
            "first word (or a two-word WordNet verb) normalised by WordNet morphy "
            "for verbs ('be thrown' -> throw); a target with no verb reading is "
            "left out of concept_actions_cn",
        }
        rdoc = {"header": rhead, "edges": by_concept, "concept_actions_cn": actions}
        rel_bytes = dump(rdoc)
        if len(rel_bytes) > REL_CAP:
            for concept in list(by_concept):
                by_concept[concept] = [r for r in by_concept[concept] if r["weight"] >= 1.0]
                if not by_concept[concept]:
                    del by_concept[concept]
            rhead["dropped"] += "; over 30 MB, so edges with weight < 1.0 dropped (actions kept)"
            rhead["counts"]["edges"] = sum(len(v) for v in by_concept.values())
            rhead["counts"]["concepts"] = len(by_concept)
            rel_bytes = dump(rdoc)
    return vbytes, rel_bytes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    vbytes, rbytes = build()
    outs = [(OUT_VOCAB, vbytes)] + ([(OUT_REL, rbytes)] if rbytes is not None else [])
    if a.check:
        bad = []
        for p, b in outs:
            if not os.path.exists(p):
                bad.append(os.path.basename(p))
                continue
            with open(p, "rb") as f:
                if f.read() != b:
                    bad.append(os.path.basename(p))
        print("check:", "byte-identical" if not bad else f"DIFFERS {bad}")
        return 1 if bad else 0
    for p, b in outs:
        with open(p, "wb") as f:
            f.write(b)
        print(p, len(b))
    return 0


if __name__ == "__main__":
    sys.exit(main())
