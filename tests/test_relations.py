"""tests/test_relations.py -- library/build_relations.py's two files (Isaiah 2026-11-16: "use
WordNet and then subtract NSM, you get the subjects and verbs, and then import
verbnet/conceptnet"). Reads the committed JSON; --check needs the data folder and is skipped,
said, without it.

  R0  both headers: standing none, readers []
  R1  vocabulary excludes something/move/do/happen/see; includes ball/throw/opponent
  R2  ConceptNet: ball has roll/bounce/throw/kick among its CapableOf/ReceivesAction/UsedFor verbs
  R3  VerbNet: throw's class includes toss or hurl
  MF  a planted 'o12' (no WordNet lemma) is refused -- RED as required
  R4  --check byte-identical
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(ROOT, "library")
sys.path.insert(0, LIB)
import build_relations as br  # noqa: E402


def _load(name: str) -> dict:
    with open(os.path.join(LIB, name), encoding="utf-8") as f:
        return json.load(f)


def check_r0(v: dict, r: dict | None) -> None:
    for d in (v, r) if r else (v,):
        assert d["header"]["standing"] == "none" and d["header"]["readers"] == []
    print("  R0: standing none, readers []")


def check_r1(v: dict) -> None:
    voc = v["vocabulary"]
    out = [w for w in ("something", "move", "do", "happen", "see") if w in voc]
    assert not out, f"NSM primes left in the vocabulary: {out}"
    missing = [w for w in ("ball", "throw", "opponent") if w not in voc]
    assert not missing, f"missing: {missing}"
    print(f"  R1: {v['header']['counts']['before']['lemmas']} -> {len(voc)} lemmas; primes out, "
          f"ball/throw/opponent in")


def check_r2(r: dict) -> None:
    acts = r["concept_actions_cn"].get("ball", {})
    hit = [a for a in ("roll", "bounce", "throw", "kick") if a in acts]
    assert hit, f"ball has none of roll/bounce/throw/kick: {sorted(acts)}"
    print(f"  R2: ball -> {hit} of {len(acts)} action verbs")


def check_r3(v: dict) -> None:
    classes, _by_verb, _files = br.verbnet()
    vn = v["vocabulary"]["throw"].get("vn", [])
    members = {m["name"] for c in vn for m in classes[c]["members"]}
    assert members & {"toss", "hurl"}, f"throw's classes {vn} hold neither toss nor hurl"
    print(f"  R3: throw in {vn}; toss/hurl among members")


def check_lemmas(voc: dict, lemmas: set) -> None:
    """Every vocabulary key is a WordNet noun or verb lemma (nothing invented)."""
    bad = sorted(w for w in voc if w not in lemmas)
    assert not bad, f"not WordNet lemmas: {bad[:5]}"


def check_mf(v: dict) -> None:
    lemmas = set(br.wn_index("noun")) | set(br.wn_index("verb"))
    check_lemmas(v["vocabulary"], lemmas)
    planted = dict(v["vocabulary"], o12={"n": ["noun.artifact"]})
    try:
        check_lemmas(planted, lemmas)
    except AssertionError as e:
        print(f"  MF: planted 'o12' refused -- RED as required ({e})")
        return
    raise AssertionError("MF: the planted 'o12' was not refused")


def check_r4() -> None:
    if not os.path.exists(br.WN):
        print("  R4: SKIPPED -- the data folder is absent here")
        return
    p = subprocess.run([sys.executable, "-B", os.path.join(LIB, "build_relations.py"), "--check"],
                       capture_output=True, text=True, timeout=280)
    assert p.returncode == 0, p.stdout + p.stderr
    print(f"  R4: {p.stdout.strip()}")


def test_relations() -> None:
    v = _load("vocabulary.json")
    r = _load("relations.json") if os.path.exists(os.path.join(LIB, "relations.json")) else None
    check_r0(v, r)
    check_r1(v)
    if r is not None:
        check_r2(r)
    else:
        print("  R2: SKIPPED -- no relations.json (ConceptNet not built)")
    if v["header"]["sources"]["verbnet"].get("classes"):
        check_r3(v)
    else:
        print("  R3: SKIPPED -- VerbNet not built")
    check_mf(v)
    check_r4()


if __name__ == "__main__":
    test_relations()
    print("test_relations: PASS")
