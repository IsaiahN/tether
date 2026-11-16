"""THE LEXICON (library/lexicon_imagenet_wordnet.json, built by library/build_lexicon.py):
ImageNet-1k class index -> WordNet 3.0 noun synset. Library data that nothing in the agent reads.

  L1     1000 entries, index i at position i, wnids strictly ascending with index, and every
         wnid resolves in WordNet 3.0 data.noun (its offset is the byte offset of its line);
         the header names its sources with sha256, carries the WordNet license, readers []
  L2     spot checks: 0 tench n01440764, 1 goldfish n01443537, 207 golden retriever n02099601,
         999 toilet tissue n15075141
  L3     no agent module names the lexicon (root *.py -- tether.py, gamma.py, arc_*.py among
         them -- and library/*.py other than its builder)
  MF-L1  corrupt one wnid in memory: the ascending / resolve check goes RED

The data.noun resolve needs the WordNet dict (LEXICON_DATA_DIR or the builder's default
root); without it that one half is skipped and says so. Runs in seconds.

    python tests/test_lexicon.py
"""
from __future__ import annotations

import copy
import glob
import json
import os
import sys
from itertools import pairwise

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

ROOT = _repo.ROOT
LEX = os.path.join(ROOT, "library", "lexicon_imagenet_wordnet.json")
sys.path.insert(0, os.path.join(ROOT, "library"))
import build_lexicon  # noqa: E402


def _load() -> dict:
    with open(LEX, encoding="utf-8") as f:
        return json.load(f)


def _data_noun() -> str | None:
    p = os.path.join(build_lexicon.data_root(),
                     *build_lexicon.INPUTS["wordnet_data_noun"].split("/"))
    return p if os.path.exists(p) else None


def problems(classes: list, data_noun: str | None) -> list[str]:
    """Everything L1 requires of the class list; empty means GREEN."""
    out = []
    if len(classes) != 1000:
        out.append(f"{len(classes)} entries, not 1000")
    for i, e in enumerate(classes):
        if e["index"] != i:
            out.append(f"position {i} holds index {e['index']}")
    for a, b in pairwise(classes):
        if not a["wnid"] < b["wnid"]:
            out.append(f"not ascending: {a['index']} {a['wnid']} !< {b['index']} {b['wnid']}")
    if data_noun:
        with open(data_noun, "rb") as f:
            for e in classes:
                off = e["wnid"][1:]
                f.seek(int(off))
                line = f.readline().decode("utf-8", "replace")
                if not line.startswith(off + " ") or line.split()[2] != "n":
                    out.append(f"{e['index']} {e['wnid']} does not resolve in data.noun")
    return out


def check_l1(doc: dict, dn: str | None) -> None:
    bad = problems(doc["classes"], dn)
    assert not bad, bad[:5]
    h = doc["header"]
    assert h["readers"] == [], h["readers"]
    assert "Princeton University" in h["wordnet_license"] and "ALL copies" in h["wordnet_license"]
    for role in ("wordnet_data_noun", "wordnet_index_noun", "imagenet_classes", "thesaurus"):
        s = h["sources"][role]
        assert len(s["sha256"]) == 64 and s["bytes"] > 0, (role, s)
    half = "resolved in " + dn if dn else "data.noun ABSENT, resolve half skipped"
    print(f"  L1: 1000 entries, wnids strictly ascending, {half}; header readers [] OK")


def check_l2(doc: dict) -> None:
    want = {0: ("tench", "n01440764"), 1: ("goldfish", "n01443537"),
            207: ("golden retriever", "n02099601"), 999: ("toilet tissue", "n15075141")}
    for i, (name, wnid) in want.items():
        e = doc["classes"][i]
        assert e["wnid"] == wnid and e["label"].split(", ")[0] == name, (i, e["label"], e["wnid"])
        assert e["hypernym_chain"][-1][0] == "n00001740", (i, e["hypernym_chain"][-1])
    print("  L2: tench, goldfish, golden retriever, toilet tissue at their wnids; chains end at "
          "entity")


def check_l3() -> None:
    files = glob.glob(os.path.join(ROOT, "*.py")) + glob.glob(os.path.join(ROOT, "library", "*.py"))
    # the builders, not the agent: build_lexicon writes it; rdl_parse (RDL Piece 1, spec
    # docs/03-DESIGN/RDL_BUILD_SPEC_2026-11-16.md) parses it into library/rdl_preload.json,
    # imports no agent module, and the agent reads only that output (Piece 3)
    builders = ("build_lexicon.py", "rdl_parse.py")
    files = [p for p in files if os.path.basename(p) not in builders]
    named = ("tether.py", "gamma.py")
    assert all(os.path.join(ROOT, n) in files for n in named), "agent modules not found"
    assert any(os.path.basename(p).startswith("arc_") for p in files), "no arc_*.py found"
    hits = []
    for p in files:
        with open(p, encoding="utf-8", errors="replace") as f:
            if "lexicon_imagenet" in f.read():
                hits.append(os.path.relpath(p, ROOT))
    assert not hits, f"an agent module reads the lexicon: {hits}"
    print(f"  L3: no reader among {len(files)} modules (tether.py, gamma.py, arc_*.py included)")


def check_mf_l1(doc: dict, dn: str | None) -> None:
    c = copy.deepcopy(doc["classes"])
    c[500]["wnid"] = "n00000001"  # out of order
    bad = problems(c, dn)
    assert any("not ascending" in b for b in bad), "MUST-FAIL: an out-of-order wnid passed"
    if dn:
        c = copy.deepcopy(doc["classes"])
        w = int(c[500]["wnid"][1:]) + 1  # in order, but mid-line: not a synset offset
        c[500]["wnid"] = f"n{w:08d}"
        bad = problems(c, dn)
        assert any("does not resolve" in b for b in bad), "MUST-FAIL: a bogus wnid resolved"
    print(f"  MF-L1: corrupted wnid at 500 -> {len(bad)} problem(s): RED as required")


def main() -> int:
    doc = _load()
    dn = _data_noun()
    check_l1(doc, dn)
    check_l2(doc)
    check_l3()
    check_mf_l1(doc, dn)
    print("lexicon: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
