"""RDL PIECE 1, THE PARSER (rdl_parse.py -> library/rdl_preload.json; spec
docs/03-DESIGN/RDL_BUILD_SPEC_2026-11-16.md).

  P1     tier counts per stage (total / usable / recorded) pinned, and the header's counts
         equal the counts recomputed from the preloads
  P2     every preload passes head_start (C1)
  P3     every usable preload has a bond and an attach (C2); every attach is an entry FILED in
         ATTRIBUTE_INDEX.by_cluster (the route never reaches an unclustered entry); every bond
         is one of grammar.json's binary operators
  P4     each tier lossier: tier 1 keeps lemmas + gloss, tier 2 only the set, tier 3 only the
         stratum, tier 4 only the rule (its do); parents point only at lower tiers
  P5     pids stable across two builds, and equal to the committed file's
  P6     --check passes (byte-identical rebuild); MF-P6 one changed byte -> check False
  P7     C5 stats: a (corpus, tier) with refused > settled is shed one tier coarser (its
         preloads gone, their children re-parented, the decision in the header); refused <=
         settled sheds nothing; a corpus with no coarser tier is kept and says so
  MF-P1  a recording planted in the input (an object name in a card, a move list in a gloss) ->
         the build refuses it (C1) -- 'RED as required'

Seconds. python tests/test_rdl_parse.py
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path
import rdl_parse as R
import rdl_store as S

sys.dont_write_bytecode = True


def _json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

LIB = Path(_repo.ROOT) / "library"
OUT = LIB / R.OUT
PINNED = {"1 instance": (1000, 145, 855), "2 regularity": (36, 17, 19),
          "3 abstraction": (445, 16, 429), "4 core_rule": (13, 13, 0)}


def _parse(stats=None, rep=None):
    return R.parse(LIB / R.LEXICON, LIB / R.INDEX, LIB / R.RULES, stats=stats, report=rep)


def check_p1(pre) -> None:
    got = {k: (v["total"], v["usable"], v["recorded"]) for k, v in R.counts(pre).items()}
    for k, v in got.items():
        print(f"  P1 tier {k}: total {v[0]} / usable {v[1]} / recorded {v[2]}")
    assert got == PINNED, got
    assert S.load_header(OUT)["counts"] == R.counts(pre), "header counts differ"


def check_p2(pre) -> None:
    bad = [(p.kind, S.head_start(p)[1]) for p in pre if not S.head_start(p)[0]]
    assert not bad, bad[:5]
    print(f"  P2: all {len(pre)} preloads pass head_start")


def check_p3(pre) -> None:
    index = _json(LIB / R.INDEX)
    filed = {e for es in index["by_cluster"].values() for e in es}
    grammar = _json(LIB / R.GRAMMAR)
    binary = {k for k, v in grammar["operators"].items() if v.get("arity") == 2}
    for p in pre:
        if S.usable(p):
            assert p.bonds and p.attaches, p.kind
        assert set(p.attaches) <= filed, (p.kind, set(p.attaches) - filed)
        assert all(b[0] in binary and len(b) == 3 for b in p.bonds), (p.kind, p.bonds)
    print("  P3: usable => bonds and attaches; attaches all filed by_cluster; bonds all in "
          "grammar.json's binary set")


def check_p4(pre) -> None:
    lex = _json(LIB / R.LEXICON)
    gloss = {c["wnid"]: c["gloss"] for c in lex["classes"]}
    rules = _json(LIB / R.RULES)["entries"]
    tier = {p.pid: p.tier for p in pre}
    for p in pre:
        if p.tier == 1:
            assert gloss[p.kind[3:]] in p.text
        elif p.tier == 2:
            assert not any(g in p.text for g in gloss.values()) and p.kind.startswith("wn-group:")
        elif p.tier == 3:
            assert p.text.startswith("KIND ") and p.kind.startswith("wn:")
        else:
            assert p.text == rules[p.kind[5:]]["do"] and p.refusal[0].startswith("NOT card:")
        assert all(tier.get(q, 0) < p.tier for q in p.parents), p.kind
    print("  P4: each tier lossier (gloss -> set -> stratum -> rule); parents only below")


def check_p5(pre) -> None:
    again = _parse()
    assert [p.pid for p in again] == [p.pid for p in pre], "pids moved between builds"
    committed = {p.pid for p in S.load(OUT)}
    assert committed == {p.pid for p in pre}, "the committed file's pids differ"
    print(f"  P5: {len(pre)} pids stable across two builds and equal to the committed file")


def check_p6() -> None:
    r = subprocess.run([sys.executable, "-B", str(Path(_repo.ROOT) / "rdl_parse.py"), "--check"],
                       capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stdout + r.stderr
    print(f"  P6: --check exit 0 ({r.stdout.strip()})")
    with tempfile.TemporaryDirectory() as d:
        bad = Path(d) / "x.json"
        raw = bytearray(OUT.read_bytes())
        raw[-3:-2] = b" "
        bad.write_bytes(bytes(raw))
        assert not R.check(bad), "a changed byte passed --check"
    print("  MF-P6: one changed byte -> check False -- RED as required")


def check_p7(pre) -> None:
    corpus = R.LEXICON
    rep: dict = {}
    shed = _parse({(corpus, 1): {"settled": 1, "refused": 3}}, rep)
    assert not [p for p in shed if p.tier == 1], "tier 1 not shed"
    old1 = {p.pid for p in pre if p.tier == 1}
    assert not any(set(p.parents) & old1 for p in shed), "a child still names a shed pid"
    assert rep["shed"][0]["decision"].startswith("shed: tier 1"), rep["shed"]
    print(f"  P7: refused 3 > settled 1 at ({corpus}, 1) -> {rep['shed'][0]['decision']}")
    same = _parse({(corpus, 1): {"settled": 3, "refused": 3}})
    assert [p.pid for p in same] == [p.pid for p in pre], "refused <= settled shed something"
    rep2: dict = {}
    kept = _parse({(R.RULES, 4): {"settled": 0, "refused": 2}}, rep2)
    assert len([p for p in kept if p.tier == 4]) == 13 and rep2["shed"][0]["decision"].startswith(
        "kept"), rep2
    print("  P7: refused <= settled sheds nothing; tier 4 has no coarser tier -> kept, recorded")


def check_mf_p1() -> None:
    with tempfile.TemporaryDirectory() as d:
        for n in (R.LEXICON, R.INDEX, R.RULES, R.GRAMMAR):
            shutil.copy(LIB / n, os.path.join(d, n))
        rules = _json(LIB / R.RULES)
        cid = sorted(rules["entries"])[0]
        rules["entries"][cid]["do"] = "press o12 → press o7"
        with open(os.path.join(d, R.RULES), "w", encoding="utf-8") as f:
            json.dump(rules, f, ensure_ascii=False)
        try:
            R.render(data=Path(d))
        except ValueError as e:
            print(f"  MF-P1 object name planted in a card: build refused ({e}) -- RED as required")
        else:
            raise AssertionError("a planted object name passed the build")
        lex = _json(LIB / R.LEXICON)
        lex["classes"][0]["gloss"] = "go up, up, left, right to win"
        with open(os.path.join(d, R.LEXICON), "w", encoding="utf-8") as f:
            json.dump(lex, f, ensure_ascii=False)
        shutil.copy(LIB / R.RULES, os.path.join(d, R.RULES))
        try:
            R.render(data=Path(d))
        except ValueError as e:
            print(f"  MF-P1 move list planted in a gloss: build refused ({e}) -- RED as required")
        else:
            raise AssertionError("a planted move list passed the build")


if __name__ == "__main__":
    pre = _parse()
    check_p1(pre)
    check_p2(pre)
    check_p3(pre)
    check_p4(pre)
    check_p5(pre)
    check_p6()
    check_p7(pre)
    check_mf_p1()
    print("test_rdl_parse: GREEN")
