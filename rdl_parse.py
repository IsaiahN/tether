"""RECURSIVE DIFFUSION LEARNING, PIECE 1: THE PARSER -- the forward shed (40, "The loop" 1).

Spec: docs/03-DESIGN/RDL_BUILD_SPEC_2026-11-16.md, Piece 1. Design: docs/05-RESEARCH/
40-WATSON_2026-11-13_RECURSIVE_DIFFUSION_LEARNING.md (C1-C6, the tier ladder). No import of
tether; no weights; every hop is a lookup on a key that exists or one written down here.

    parse(lexicon_path, attribute_index_path, rules_path, stats=None) -> list[Preload]
    build(out_path, stats=None) writes library/rdl_preload.json;  python rdl_parse.py --check
    rebuilds in memory and compares byte for byte (exit 1 on any difference).

THE TIER LADDER, each tier LOSSIER than the one below (Fig 4 :27-28):
  1 instance     one per lexicon class, kind wn:<wnid>; text = its lemmas and its gloss;
                 bonds = '≡' between the synset's own lemmas (grammar.json: "two names, one
                 referent" -- a WordNet synset is exactly that); attached by cluster (below).
  2 regularity   kind wn-group:<key>; text = only the set. Two kinds of group:
                 name:<word>    a name (a WordNet lemma or a thesaurus synonym, lower-cased)
                                carried by 2+ classes; bonds '∥' between the classes ("either
                                suffices": the word picks out one MAYBE the other);
                 cluster:<C>    the classes the route below reached cluster C from; bonds '∥'
                                between them (each alone reaches C: remove one, it still works).
                 parents = their tier-1 pids.
  3 abstraction  kind wn:<hypernym wnid>, every hypernym 2+ classes share; text = only the
                 stratum (KIND <its lemma>); bonds '∥' between its distinct immediate children
                 (a hypernym is satisfied by any of its kinds -- the grammar's disjunction test
                 "remove one. Does it still work? Yes."). The grammar has NO "is a kind of" bond:
                 the operators are + ∥ ≡ → ⇒ − ⋛ (and unary ¬), so the hypernym relation is
                 written as the disjunction of its kinds, never forced into ⇒ or ≡.
                 parents = the tier-1 pids under it and the tier-2 pids whose classes all are.
  4 core rule    each card of library/tether_rules.json, kind card:<id>; text = its `do` (the
                 rule in operators and NSM primes); bonds = the card's own operators as written
                 in `do` (below); refusal = "NOT card:<id> WHEN <refuted_by>".

THE CLUSTER-ATTACH ROUTE (spec: BY CLUSTER, never raw-name intersection). Written once here and
copied into the output header:
  (1) the cluster vocabulary: for every entry FILED in ATTRIBUTE_INDEX.by_cluster under cluster
      C, its attributes (atom_attributes[entry].attributes, lower-cased, whole) are words of C.
      Entries filed under no cluster contribute nothing (they cannot be reached by cluster).
  (2) the preload's own words: [a-z]+ tokens of its text source -- tier 1 the lemmas and the
      gloss; tier 2 the group's name word (cluster groups: the members' reach, below); tier 3
      the hypernym's lemma; tier 4 the card's `when` and `do`. Exact match, no stemming, no
      synonym expansion, no hypernym chain at tier 1 (the chain is tier 3's material).
  (3) attach: word w of the preload that is a word of cluster C reaches C; the attaches are the
      entries filed under by_cluster[C] that carry w. One word at a time -- never an
      intersection of several raw names (the index's own caution).
  A preload whose words reach no cluster has no attach; under C2 it is RECORDED, not usable.
  Known weakness, stated: exact spelling does not separate senses ("states" in "United States"
  meets the attribute "states"); every attach is a candidate with no standing (C3), traceable
  through the stamp (C6), and refused by the ground if wrong.

BONDS FROM A CARD'S `do`. Only grammar.json's binary operators are bonds (¬ is unary and is
not). The `do` is cut into clauses at ';' and at the NSM clause words IF / THEN / BECAUSE /
AND and at commas, outside parentheses (a clause word directly between an operator and its
operand, as in "describe(R) by effect → THEN lookup(...)", is skipped, not a cut); within a
clause the loosest operator present splits first (→, ⇒, ≡, ∥, +, ⋛, − in that order, a
declared convention), each operand is the verbatim span of the card's text, and grouping
parentheses are entered; a call's parentheses (a name before the bracket, e.g. step(k−1))
are not. Symbols the grammar does not define (∧, <, >, =,
≠) stay inside operand text and are never emitted as bonds.

C5, STATS. stats = {(corpus, tier): {"settled": n, "refused": m}} from the agent's ledger. A
(corpus, tier) the ground refused MORE than it settled is shed one tier coarser in this build:
its preloads are not emitted at that tier (the tier above already abstracts them), and anything
that named them as a parent names their parents instead. A corpus with no coarser tier keeps
its tier and the header says so. Every decision is written in the header. Never the parser's
own taste: with stats=None nothing is shed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

import rdl_store as S

sys.dont_write_bytecode = True

PARSER = "rdl_parse"
PARSER_VERSION = "1"
ROOT = Path(__file__).resolve().parent
LEXICON = "lexicon_imagenet_wordnet.json"
INDEX = "ATTRIBUTE_INDEX.json"
RULES = "tether_rules.json"
GRAMMAR = "grammar.json"
OUT = "rdl_preload.json"
OP_ORDER = ("→", "⇒", "≡", "∥", "+", "⋛", "−")   # loosest first: a declared convention
_CLAUSE_WORDS = re.compile(r"\b(?:IF|THEN|BECAUSE|AND)\b")
_WORD = re.compile(r"[a-z]+")
_SIZE_CAP = 5_000_000   # over ~5 MB: keep usable preloads only, counts of the rest in the header

ROUTE = ("cluster vocabulary = the attributes (lower-cased, whole) of the entries FILED in "
         "ATTRIBUTE_INDEX.by_cluster under each cluster; a preload's words ([a-z]+ tokens of: "
         "tier 1 lemmas + gloss; tier 2 name groups the shared name; tier 2 cluster groups the "
         "members' reach in that cluster; tier 3 the hypernym lemma; tier 4 the card's when + "
         "do) reach cluster C when a word equals an attribute of an entry filed under C; the "
         "attaches are those filed entries of C carrying that word. One word at a time, exact "
         "match, no stemming, never an intersection of raw names. No cluster reached -> no "
         "attach -> recorded, not usable (C2).")
BOND_ROUTE = ("tier 1 '≡' between a synset's own WordNet lemmas (two names, one referent); "
              "tier 2 '∥' between classes sharing a name, and between classes reaching the "
              "same cluster; tier 3 '∥' between a shared hypernym's distinct immediate "
              "children (grammar.json has no 'is a kind of' bond; a hypernym is the "
              "disjunction of its kinds); tier 4 the card's own binary operators as written "
              "in its do (grammar.json's binary operators only; ¬ is unary).")


def data_dir() -> Path:
    """The input directory: RDL_DATA_DIR if set, else the repo's library/."""
    d = os.environ.get("RDL_DATA_DIR")
    return Path(d) if d else ROOT / "library"


def _sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _read(path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _words(*texts: str) -> set[str]:
    out: set[str] = set()
    for t in texts:
        out |= set(_WORD.findall(t.lower()))
    return out


# ---- the cluster-attach route ---------------------------------------------------------------

def cluster_vocab(index: dict) -> dict[str, dict[str, set[str]]]:
    """word -> {cluster: entries filed under that cluster carrying the word}."""
    atoms = index["atom_attributes"]
    vocab: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for cluster, entries in index["by_cluster"].items():
        for e in entries:
            for a in atoms.get(e, {}).get("attributes", []):
                vocab[a.lower()][cluster].add(e)
    return vocab


def attach(words: set[str], vocab) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """(attaches, clusters) reached by the words, one word at a time."""
    ents: set[str] = set()
    clusters: set[str] = set()
    for w in sorted(words):
        for c, es in vocab.get(w, {}).items():
            clusters.add(c)
            ents |= es
    return tuple(sorted(ents)), tuple(sorted(clusters))


# ---- bonds from a card's do ------------------------------------------------------------------

def _top_level(s: str):
    """Yield (index, char, depth) with depth the parenthesis depth BEFORE the char."""
    depth = 0
    for i, ch in enumerate(s):
        if ch == ")":
            depth -= 1
        yield i, ch, depth
        if ch == "(":
            depth += 1


def _split_top(s: str, seps) -> list[str]:
    parts, last = [], 0
    for i, ch, d in _top_level(s):
        if d == 0 and ch in seps:
            parts.append(s[last:i])
            last = i + 1
    parts.append(s[last:])
    return parts


def _clauses(s: str) -> list[str]:
    out = []
    for part in _split_top(s, ";,"):
        # the NSM clause words, outside parentheses
        depth_at = {i: d for i, _ch, d in _top_level(part)}
        last = 0
        for m in _CLAUSE_WORDS.finditer(part):
            if depth_at.get(m.start(), 0) == 0:
                out.append(part[last:m.start()])
                last = m.end()
        out.append(part[last:])
    # a clause word standing between an operator and its operand ("A → THEN B") is not a cut
    merged: list[str] = []
    for frag in (c.strip() for c in out):
        if merged and (merged[-1].endswith(OP_ORDER) or frag.startswith(OP_ORDER)):
            merged[-1] = f"{merged[-1]} {frag}".strip()
        elif frag:
            merged.append(frag)
    return merged


def _unwrap(s: str) -> str:
    s = s.strip()
    while s.startswith("(") and s.endswith(")"):
        depth = 0
        for i, ch in enumerate(s):
            depth += ch == "("
            depth -= ch == ")"
            if depth == 0 and i < len(s) - 1:
                return s
        s = s[1:-1].strip()
    return s


def _descend(s: str, ops: tuple[str, ...], out: list) -> None:
    s = _unwrap(s)
    for op in ops:
        parts = [p.strip() for p in _split_top(s, op)]
        if len(parts) > 1:
            for a, b in zip(parts, parts[1:], strict=False):
                if a and b:
                    out.append((op, a, b))
            for p in parts:
                _descend(p, ops, out)
            return
    # no top-level operator: enter grouping parentheses (not a call's: a name before the bracket)
    depth, start = 0, None
    for i, ch in enumerate(s):
        if ch == "(":
            if depth == 0 and (i == 0 or not (s[i - 1].isalnum() or s[i - 1] in "_)")):
                start = i
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0 and start is not None:
                _descend(s[start + 1:i], ops, out)
                start = None


def card_bonds(do: str, binary_ops) -> tuple[tuple[str, str, str], ...]:
    ops = tuple(o for o in OP_ORDER if o in binary_ops)
    out: list = []
    for clause in _clauses(do):
        _descend(clause, ops, out)
    return tuple(out)


def _chain(bond: str, kinds) -> tuple:
    ks = sorted(set(kinds))
    return tuple((bond, a, b) for a, b in zip(ks, ks[1:], strict=False))


# ---- the parser ------------------------------------------------------------------------------

def parse(lexicon_path, attribute_index_path, rules_path, stats=None, grammar_path=None,
          report: dict | None = None) -> list[S.Preload]:
    """The forward shed: tiers 1-4 from the inputs; `report` (if given) receives the counts
    and decisions the header records."""
    lexicon_path, rules_path = Path(lexicon_path), Path(rules_path)
    grammar_path = Path(grammar_path) if grammar_path else Path(rules_path).parent / GRAMMAR
    lex, index, rules, grammar = (_read(lexicon_path), _read(attribute_index_path),
                                  _read(rules_path), _read(grammar_path))
    binary = {k for k, v in grammar["operators"].items() if v.get("arity") == 2}
    vocab = cluster_vocab(index)
    lex_src = {"corpus": lexicon_path.name, "corpus_sha": _sha(lexicon_path), "parser": PARSER,
               "parser_version": PARSER_VERSION}
    card_src = dict(lex_src, corpus=rules_path.name, corpus_sha=_sha(rules_path))
    rep = report if report is not None else {}

    # C5: which (corpus, tier) the ground refused more than it settled
    shed_set: set[tuple[str, int]] = set()
    decisions = []
    for (corpus, tier), v in sorted((stats or {}).items()):
        settled, refused = int(v.get("settled", 0)), int(v.get("refused", 0))
        if refused <= settled:
            continue
        top = 4 if corpus == rules_path.name else 3
        if tier < top:
            shed_set.add((corpus, tier))
            decision = f"shed: tier {tier} not emitted, carried by tier {tier + 1}"
        else:
            decision = "kept: no coarser tier for this corpus"
        decisions.append({"corpus": corpus, "tier": tier, "settled": settled,
                          "refused": refused, "decision": decision})
    rep["shed"] = decisions
    gone: dict[str, tuple] = {}   # shed pid -> the parents it hands on

    def parents_of(pids) -> tuple:
        out: list[str] = []
        for p in pids:
            out.extend(parents_of(gone[p]) if p in gone else [p])
        return tuple(sorted(set(out)))

    def emit(level: list, corpus: str, tier: int) -> list:
        if (corpus, tier) in shed_set:
            for p in level:
                gone[p.pid] = p.parents
            return []
        return level

    classes = lex["classes"]
    # tier 1
    t1, t1_by_wnid, reach = [], {}, defaultdict(dict)   # reach[C][wnid] = entries
    for c in classes:
        lemmas = c["lemmas"]
        words = _words(c["gloss"], *lemmas)
        ents, _cl = attach(words, vocab)
        for w in sorted(words):
            for cl, es in vocab.get(w, {}).items():
                reach[cl].setdefault(c["wnid"], set()).update(es)
        p = S.make(1, lex_src, f"wn:{c['wnid']}", f"{', '.join(lemmas)}: {c['gloss']}",
                   bonds=_chain("≡", lemmas), attaches=ents)
        t1.append(p)
        t1_by_wnid[c["wnid"]] = p
    t1 = emit(t1, lex_src["corpus"], 1)
    rep["tier1_no_cluster"] = sum(1 for p in t1_by_wnid.values() if not p.attaches)
    rep["tier1_no_bond"] = sum(1 for p in t1_by_wnid.values() if not p.bonds)

    # tier 2: shared names (lemmas and thesaurus synonyms), then same-cluster groups
    names: dict[str, set[str]] = defaultdict(set)
    for c in classes:
        syn = (c.get("thesaurus") or {}).get("synonyms") or []
        for n in list(c["lemmas"]) + list(syn):
            names[n.lower()].add(c["wnid"])
    t2, t2_members = [], {}
    for name in sorted(names):
        members = sorted(names[name])
        if len(members) < 2:
            continue
        kinds = [f"wn:{w}" for w in members]
        ents, _cl = attach(_words(name), vocab)
        p = S.make(2, lex_src, f"wn-group:name:{name}",
                   f"name {name}: {' ∥ '.join(kinds)}", bonds=_chain("∥", kinds),
                   attaches=ents, parents=parents_of(t1_by_wnid[w].pid for w in members))
        t2.append(p)
        t2_members[p.pid] = set(members)
    for cl in sorted(reach):
        members = sorted(reach[cl])
        if len(members) < 2:
            continue
        kinds = [f"wn:{w}" for w in members]
        ents = tuple(sorted(set().union(*(reach[cl][w] for w in members))))
        p = S.make(2, lex_src, f"wn-group:cluster:{cl}",
                   f"cluster {cl}: {' ∥ '.join(kinds)}", bonds=_chain("∥", kinds),
                   attaches=ents, parents=parents_of(t1_by_wnid[w].pid for w in members))
        t2.append(p)
        t2_members[p.pid] = set(members)
    rep["cluster_reach"] = {cl: len(reach[cl]) for cl in sorted(reach)}
    t2_all = list(t2)
    t2 = emit(t2, lex_src["corpus"], 2)

    # tier 3: hypernym strata shared by 2+ classes
    under: dict[str, set[str]] = defaultdict(set)
    children: dict[str, set[str]] = defaultdict(set)
    lemma_of: dict[str, str] = {}
    for c in classes:
        path = [c["wnid"]] + [h for h, _l in c["hypernym_chain"]]
        for h, lem in c["hypernym_chain"]:
            lemma_of[h] = lem
        for below, h in zip(path, path[1:], strict=False):
            under[h].add(c["wnid"])
            children[h].add(below)
    t3 = []
    for h in sorted(under):
        members = under[h]
        if len(members) < 2:
            continue
        lem = lemma_of[h]
        ents, _cl = attach(_words(lem), vocab)
        pids = [t1_by_wnid[w].pid for w in sorted(members)]
        pids += [p.pid for p in t2_all if t2_members[p.pid] <= members]
        t3.append(S.make(3, lex_src, f"wn:{h}", f"KIND {lem}",
                         bonds=_chain("∥", [f"wn:{k}" for k in children[h]]),
                         attaches=ents, parents=parents_of(pids)))
    t3 = emit(t3, lex_src["corpus"], 3)

    # tier 4: the Tether cards
    t4 = []
    for cid in sorted(rules["entries"]):
        e = rules["entries"][cid]
        ents, _cl = attach(_words(e["when"], e["do"]), vocab)
        kind = f"card:{cid}"
        t4.append(S.make(4, card_src, kind, e["do"], bonds=card_bonds(e["do"], binary),
                         refusal=(f"NOT {kind} WHEN {e['refuted_by']}",), attaches=ents))
    t4 = emit(t4, card_src["corpus"], 4)
    return t1 + t2 + t3 + t4


def counts(preloads) -> dict:
    out = {}
    for t, stage in enumerate(S.STAGES, 1):
        ps = [p for p in preloads if p.tier == t]
        u = sum(1 for p in ps if S.usable(p))
        out[f"{t} {stage}"] = {"total": len(ps), "usable": u, "recorded": len(ps) - u}
    return out


def _licences(lex: dict, rules: dict) -> dict:
    h = lex["header"]
    return {
        LEXICON: {"wordnet_license": h.get("wordnet_license"),
                  "imagenet_terms": h.get("imagenet_terms"),
                  "thesaurus": "the zaibacu thesaurus row carries no licence field in "
                               "the lexicon header; carried as the lexicon states it"},
        INDEX: "no licence field in the file; Isaiah's corpus, read only and hash-checked by "
               "inherited.py (K1)",
        RULES: {k: rules["meta"].get(k) for k in ("source", "status", "what")},
        GRAMMAR: "no licence field; the grammar every entry is written in (its meta.what)",
    }


def render(stats=None, data: Path | None = None) -> str:
    """The full output text, deterministic."""
    d = data or data_dir()
    lx, ix, rl, gr = d / LEXICON, d / INDEX, d / RULES, d / GRAMMAR
    rep: dict = {}
    pre = parse(lx, ix, rl, stats=stats, grammar_path=gr, report=rep)
    for p in pre:
        ok, why = S.head_start(p)
        if not ok:
            raise ValueError(f"C1: {p.kind}: {why}")
    header = {
        "what": "RDL Piece 1: the forward shed of the lexicon and the Tether cards up the tier "
                "ladder (instance, regularity, abstraction, core_rule) as head starts. Search "
                "priority only, never reach, never standing.",
        "spec": "docs/03-DESIGN/RDL_BUILD_SPEC_2026-11-16.md",
        "design": "docs/05-RESEARCH/40-WATSON_2026-11-13_RECURSIVE_DIFFUSION_LEARNING.md",
        "build": "python rdl_parse.py (--check rebuilds in memory and compares byte for byte)",
        "parser": PARSER, "parser_version": PARSER_VERSION,
        "sources": {n: S.file_source(p, f"library/{n}") for n, p in
                    ((LEXICON, lx), (INDEX, ix), (RULES, rl), (GRAMMAR, gr))},
        "licences": _licences(_read(lx), _read(rl)),
        "attach_route": ROUTE, "bond_route": BOND_ROUTE,
        "counts": counts(pre),
        "tier1_no_cluster": rep["tier1_no_cluster"], "tier1_no_bond": rep["tier1_no_bond"],
        "cluster_reach_classes": rep["cluster_reach"],
        "stats": ("none: no contact statistics yet, nothing shed" if stats is None else
                  [{"corpus": c, "tier": t, **v} for (c, t), v in sorted(stats.items())]),
        "shed": rep["shed"],
        "readers": [],
        "readers_note": "nothing in the agent reads this file yet; Piece 3 (the agent's RDL "
                        "switch) is its declared reader. A preload is recorded unless usable "
                        "(C2); only usable ones may ever be offered.",
        "kept": "all preloads",
    }
    text = S.dumps(pre, header)
    if len(text.encode("utf-8")) > _SIZE_CAP:
        header["kept"] = "usable preloads only (file over ~5 MB); recorded ones are counted"
        text = S.dumps([p for p in pre if S.usable(p)], header)
    return text


def build(out_path=None, stats=None) -> Path:
    out = Path(out_path) if out_path else ROOT / "library" / OUT
    out.write_bytes(render(stats).encode("utf-8"))
    return out


def check(out_path=None, stats=None) -> bool:
    out = Path(out_path) if out_path else ROOT / "library" / OUT
    return out.exists() and out.read_bytes() == render(stats).encode("utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="rebuild in memory, compare bytes")
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)
    if a.check:
        ok = check(a.out)
        print("rdl_preload: byte-identical" if ok else "rdl_preload: DIFFERS from a rebuild")
        return 0 if ok else 1
    p = build(a.out)
    print(f"wrote {p} ({p.stat().st_size} bytes)")
    print(json.dumps(S.load_header(p)["counts"], indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
