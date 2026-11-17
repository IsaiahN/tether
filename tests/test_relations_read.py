"""TETHER_RELATIONS_READ (default ON; write-up 42 handoff item 5: library/relations.json and
library/vocabulary.json were read by nothing). affordance's prior lookup merges a concept's
ConceptNet verbs beside the word map's.

  RR1  ball (the landed shape bridge, word-map verbs hit/throw/kick/play): its merged priors now
       include roll from ConceptNet (CapableOf), which predicts "moves"; push (ReceivesAction)
       predicts it too; kick, in both sources, ranks above the ConceptNet-only verbs
  RR2  every merged prior keeps its source and stamp (word map: gloss/wordnet; ConceptNet:
       conceptnet-5.7) and carries standing none; the offered rows carry no standing field
  RR3  a concept absent from relations.json is unchanged (the same list, no new fields)
  RR4  CN_READING only for an object concept: a fixture non-object concept with CapableOf roll
       gets no reading; OBJECT_LEXNAMES agrees with word_map.json's category_map "object"
  MF   TETHER_RELATIONS_READ OFF: word-map-only priors (no roll, no ConceptNet row) -> RED as
       required
Seconds.
    python tests/test_relations_read.py
"""
from __future__ import annotations

import json
import sys

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import affordance  # noqa: E402


def ball_chain():
    _atoms, bridge, priors, why = affordance.load_sources()
    assert why is None and bridge, f"the word map's shape bridge is needed here: {why}"
    return affordance.resolve("disc", None, bridge, priors)


def main() -> int:
    assert affordance._RELATIONS_READ is True, "the arm defaults ON"
    acts, nouns, stamp = affordance.cn_sources()
    assert acts and nouns and stamp, "library/relations.json / vocabulary.json not readable"

    ch = ball_chain()
    assert ch and ch["concept"] == "ball" and ch["via"] == "shape_bridge", ch
    ps = ch["priors"]
    roll = [p for p in ps if p["action_verb"] == "roll"]
    assert roll and roll[0]["source"] == "conceptnet" and "CapableOf" in roll[0]["relations"], roll
    assert affordance.readings(roll[0]) == ["moves"], roll[0]
    push = next(p for p in ps if p["action_verb"] == "push")
    assert affordance.readings(push) == ["moves"] and push["relations"] == ["ReceivesAction"], push
    ranks = [len(p["found_in"]) for p in ps]
    assert ranks == sorted(ranks, reverse=True), ranks
    kick = [i for i, p in enumerate(ps) if p["action_verb"] == "kick"]
    first_cn_only = next(i for i, p in enumerate(ps) if p["found_in"] == ["conceptnet"])
    assert kick and max(kick) < first_cn_only, (kick, first_cn_only)
    assert all(ps[i]["found_in"] == ["word_map", "conceptnet"] for i in kick)
    bk = affordance.Book()
    rows = bk.offer("kind<disc>", "o1", ch)
    assert {r["property"] for r in rows} == {"moves"}, rows
    assert "roll" in bk.verbs["kind<disc>"], bk.verbs
    assert affordance.manner(True, bk.verbs["kind<disc>"]) == "rolls"
    print("RR1 ball:", [(p["action_verb"], p["source"], p["found_in"], affordance.readings(p))
                        for p in ps if affordance.readings(p) or len(p["found_in"]) == 2],
          "; roll from ConceptNet predicts moves; the moves row:",
          (rows[0]["action_verb"], rows[0]["found_in"]), "GREEN")

    for p in ps:
        assert p.get("standing") in ("none", None) and p.get("source"), p
        st = affordance._stamp(p)
        if p["source"] == "conceptnet":
            assert st["corpus"] == "conceptnet-5.7", st
            assert st["stage"] == "regularity" and st["sha"], st
        else:
            assert (st["source"] == "gloss" and st.get("corpus") != "conceptnet-5.7"), st
    assert all(p["standing"] == "none" for p in ps if p["source"] == "conceptnet")
    assert not any("standing" in r for r in rows), "an offered prior carries no standing"
    print("RR2 every merged prior keeps its source and stamp, standing none: ConceptNet",
          affordance._stamp(roll[0]), "word map", affordance._stamp(ps[0]), "GREEN")

    _a, _b, priors, _w = affordance.load_sources()
    absent = next(p["concept"] for p in priors
                  if affordance.cn_key(p["concept"]) not in acts and affordance.readings(p))
    mine = [p for p in priors if p["concept"] == absent]
    assert affordance.merge(absent, mine) == mine
    fx = [{"concept": "FIXTURE|Zzqx", "action_verb": "push", "verb_lexname": "verb.motion",
           "source": "gloss", "stamp": {"corpus": "fixture", "sha": "0", "stage": "regularity"}}]
    assert affordance.merge("FIXTURE|Zzqx", fx) == fx
    on = affordance.resolve("zzqx-shape", {"zzqx-shape": (absent,)}, None, priors)
    affordance._RELATIONS_READ = False
    try:
        off = affordance.resolve("zzqx-shape", {"zzqx-shape": (absent,)}, None, priors)
    finally:
        affordance._RELATIONS_READ = True
    assert on is not None and on == off, (on, off)
    print(f"RR3 a concept absent from relations.json ({absent!r}) is unchanged (merge and "
          f"resolve, ON == OFF): GREEN")

    cn = ({"widget": {"roll": {"relations": ["CapableOf"], "vn": []}}},
          {"widget": ["noun.cognition"]}, {"corpus": "fixture", "sha": "0", "stage": "regularity"})
    m = affordance.merge("widget", [], cn)
    assert len(m) == 1 and affordance.readings(m[0]) == [], m
    cn_obj = (cn[0], {"widget": ["noun.artifact"]}, cn[2])
    assert affordance.readings(affordance.merge("widget", [], cn_obj)[0]) == ["moves"]
    with open(affordance.WORD_MAP, encoding="utf-8") as f:
        cmap = json.load(f)["header"]["category_map"]
    want = {k for k, v in cmap.items() if v == "object"}
    assert want == affordance.OBJECT_LEXNAMES, cmap
    print("RR4 CN_READING only for an object concept (noun.cognition: none; noun.artifact: "
          "moves); OBJECT_LEXNAMES == word_map category_map 'object': GREEN")

    affordance._RELATIONS_READ = False
    try:
        off = ball_chain()
    finally:
        affordance._RELATIONS_READ = True
    po = off["priors"] if off else []
    assert not any(p.get("source") == "conceptnet" for p in po), po
    assert "roll" not in [p["action_verb"] for p in po] and not any("found_in" in p for p in po)
    print("MF TETHER_RELATIONS_READ OFF: word-map-only priors",
          [p["action_verb"] for p in po], "(no roll, no ConceptNet row) -> RED as required")
    print("relations read: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())