"""library/word_map.json (library/build_word_map.py), checked in seconds.

  W0     no agent module names the word map (readers: [])
  W1     'opponent' -> TRANSFORMATION|Adversary through a shared synset (opponent.n and adversary.n)
  W2     TOPOLOGICAL|Circle is category shape; ACTION|Feint is category action
  W3     ball-like lexicon classes carry priors, at least one verb.motion/verb.contact from a gloss
  W4     every prior carries a stamp {stage, corpus, sha} and standing none
  W5     shape_bridge: disc -> sphere -> ball -> a verb.motion/verb.contact action, stamped
  W6     concept_actions for ball (n02778669): catch/bounce/dribble from reverse-example AND
         throw or kick; every action has a source; every row stamped, standing none
  MF     a planted 'o12' or move-list entry name is refused by the builder
  MF6    the ball row rebuilt WITHOUT the reverse index fails W6 (RED as required)
  CHECK  --check rebuilds byte-identical (skipped when the WordNet data root is absent)

    python -B tests/test_word_map.py
"""
from __future__ import annotations

import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "library"))
import build_word_map as bwm  # noqa: E402

PATH = os.path.join(ROOT, "library", "word_map.json")
MOTION_CONTACT = ("verb.motion", "verb.contact")


def _load() -> dict:
    with open(PATH, encoding="utf-8") as f:
        return json.load(f)


# the root modules admitted to read the word map, as data (each RECORD-ONLY: rows, no action
# choice): affordance.py, TETHER_AFFORDANCE (Isaiah 2026-11-16 "does this roll?"; its priors are
# bets with no standing, judged by the first press). The header's "readers" is the builder's and
# still [] -- to be brought level at the next rebuild.
READERS_RECORD_ONLY = ("affordance.py", "tether.py")  # tether.py: TETHER_CATEGORY_ORDER, order only


def check_w0(doc: dict) -> None:
    assert doc["header"]["readers"] == [] and doc["header"]["standing"] == "none"
    files = glob.glob(os.path.join(ROOT, "*.py"))
    hits = []
    for p in files:
        with open(p, encoding="utf-8", errors="replace") as fh:
            if "word_map" in fh.read() and os.path.basename(p) not in READERS_RECORD_ONLY:
                hits.append(p)
    assert not hits, f"an agent module reads the word map: {hits}"
    print(f"  W0: readers [] and no reader among {len(files)} root modules but the record-only "
          f"{READERS_RECORD_ONLY}")


def check_w1(doc: dict) -> None:
    rows = doc["synonym_index"].get("opponent", [])
    hit = [r for r in rows if r["entry"] == "TRANSFORMATION|Adversary"]
    assert hit, f"opponent does not reach TRANSFORMATION|Adversary: {rows}"
    sid = hit[0]["synset"]
    assert sid in doc["entries"]["TRANSFORMATION|Adversary"]["chosen"]
    lem = doc["synonym_index"].get("adversary", [])
    assert any(r["synset"] == sid for r in lem), "adversary does not share the synset"
    print(f"  W1: opponent -> TRANSFORMATION|Adversary via synset {sid}")


def check_w2(doc: dict) -> None:
    c = doc["entries"]["TOPOLOGICAL|Circle"]
    assert c["category"] == "shape", c["category"]
    f = doc["entries"]["ACTION|Feint"]
    assert f["category"] == "action", f["category"]
    print(f"  W2: Circle shape ({c['status']} {c['chosen']}), Feint action ({f['chosen']})")


def check_w3(doc: dict) -> None:
    balls = ("soccer ball", "basketball", "golf ball", "tennis ball", "volleyball",
             "rugby ball", "croquet ball", "ping-pong ball")
    got = {}
    for p in doc["priors"]:
        if p["concept"].startswith("imagenet:"):
            label = p["concept"].split(":", 2)[2].split(",")[0]
            if label in balls:
                got.setdefault(label, []).append(p)
    assert set(got) == set(balls), f"ball classes without priors: {set(balls) - set(got)}"
    for label, ps in got.items():
        mc = [p for p in ps if p["source"] == "gloss" and p["verb_lexname"] in MOTION_CONTACT]
        assert mc, f"{label}: no verb.motion/verb.contact gloss prior: {ps}"
    s = sorted({(p["action_verb"], p["verb_lexname"]) for p in got["soccer ball"]})
    print(f"  W3: {len(balls)} ball classes have motion/contact gloss priors; soccer ball {s}")


def check_w4(doc: dict) -> None:
    for p in doc["priors"]:
        st = p.get("stamp") or {}
        assert st.get("stage") == "regularity" and st.get("corpus") and st.get("sha"), p
        assert p["standing"] == "none" and p["source"] in ("gloss", "derivation"), p
    print(f"  W4: {len(doc['priors'])} priors, every one stamped, standing none")


def check_w5(doc: dict) -> None:
    row = next(r for r in doc["shape_bridge"] if any(s["name"] == "disk" for s in r["shape_2d"]))
    assert any(f["name"] == "sphere" for f in row["form_3d"])
    ball = next(o for o in row["objects"] if o["name"] == "ball")
    acts = [a for a in ball["actions"] if a["verb_lexname"] in MOTION_CONTACT]
    assert acts, ball
    assert row["stamp"]["stage"] == "abstraction" and row["standing"] == "none"
    print(f"  W5: disk -> sphere -> ball {ball['synset']} -> "
          f"{[(a['verb'], a['verb_lexname']) for a in acts]}")


REVERSE_VERBS = ("catch", "bounce", "dribble")
FORWARD_VERBS = ("throw", "kick")


def w6_row(row: dict) -> list[str]:
    acts = row["actions"]
    assert all(a["sources"] and a["n_sources"] == len(a["sources"]) for a in acts), row
    rev = sorted({a["verb"] for a in acts if a["verb"] in REVERSE_VERBS
                  and "reverse-example" in a["sources"]})
    fwd = sorted({a["verb"] for a in acts if a["verb"] in FORWARD_VERBS})
    assert rev, f"ball: none of {REVERSE_VERBS} from reverse-example"
    assert fwd, f"ball: none of {FORWARD_VERBS}"
    return rev + fwd


def check_w6(doc: dict) -> None:
    rows = doc["concept_actions"]
    for r in rows:
        assert r["stamp"]["stage"] == "regularity" and r["stamp"]["sha"], r["concept"]
        assert r["standing"] == "none" and all(a["sources"] for a in r["actions"]), r["concept"]
    ball = [r for r in rows if r["synset"] == "n02778669"]
    assert ball, "no concept_actions row for ball n02778669"
    got = [w6_row(r) for r in ball]
    print(f"  W6: ball n02778669 ({[r['concept'] for r in ball]}) -> {got}; "
          f"{len(rows)} concept rows, every action sourced")


def check_mf6(doc: dict) -> None:
    if not os.path.isdir(os.path.join(bwm.data_root(), "wordnet", "dict")):
        print("  MF6: skipped (WordNet data root absent)")
        return
    wn = bwm.WordNet(bwm.data_root())
    row = next(r for r in doc["concept_actions"] if r["synset"] == "n02778669")
    pri = [p for p in doc["priors"] if p["concept"] == row["concept"]
           and p["concept_synset"] == row["synset"]]
    stamp = row["stamp"]
    same, _ = bwm.concept_actions(wn, bwm.reverse_index(wn), row["concept"], row["synset"], [],
                                  pri, stamp, doc["synonym_index"])
    assert same == row, "the ball row does not rebuild from its own inputs"
    blind, _ = bwm.concept_actions(wn, {}, row["concept"], row["synset"], [], pri, stamp,
                                   doc["synonym_index"])
    try:
        w6_row(blind)
    except AssertionError as e:
        print(f"  MF6: without the reverse index W6 fails ({e}): RED as required")
        return
    raise AssertionError("MUST-FAIL: W6 passed without the reverse index")


def check_mf() -> None:
    for planted in (["GAME|o12"], ["GAME|up, up, left"], ["GAME|ACTION1,ACTION3"]):
        try:
            bwm.refuse_names(["TOPOLOGICAL|Circle", *planted])
        except SystemExit as e:
            assert "REFUSED" in str(e)
            continue
        raise AssertionError(f"MUST-FAIL: planted {planted} was accepted")
    bwm.refuse_names(["TOPOLOGICAL|Circle", "ACOUSTIC|20kHz"])  # the real names pass
    print("  MF: planted 'o12' and move lists refused: RED as required")


def check_rebuild() -> None:
    if not os.path.isdir(os.path.join(bwm.data_root(), "wordnet", "dict")):
        print("  CHECK: skipped (WordNet data root absent)")
        return
    assert bwm.main(["--check"]) == 0, "--check differs"
    print("  CHECK: byte-identical")


def main() -> int:
    doc = _load()
    check_w0(doc)
    check_w1(doc)
    check_w2(doc)
    check_w3(doc)
    check_w4(doc)
    check_w5(doc)
    check_w6(doc)
    check_mf()
    check_mf6(doc)
    check_rebuild()
    print("word_map: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())


def test_word_map() -> None:
    assert main() == 0
