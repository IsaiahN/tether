"""VerbNet widening: a found verb's class brings its sisters as NO-STANDING candidates."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import affordance as A  # noqa: E402


def test_vn_sisters():
    # synthetic acts: throw shares a class with toss and hurl; kick has none
    acts = {
        "ball": {
            "throw": {"relations": ["UsedFor"], "vn": ["throw-50.1"]},
            "kick": {"relations": ["CapableOf"], "vn": []},
        },
        "other": {
            "toss": {"relations": [], "vn": ["throw-50.1"]},
            "hurl": {"relations": [], "vn": ["throw-50.1"]},
            "roll": {"relations": [], "vn": ["roll-01.1"]},
        },
    }
    A._VN_INDEX = None
    sisters = A._vn_sisters(["throw"], acts)
    assert "toss" in sisters and "hurl" in sisters, sisters
    assert "throw" not in sisters and "roll" not in sisters
    print("sisters: OK", sisters)


def test_merge_widens_and_arm_off_is_identity():
    acts = {
        "ball": {"throw": {"relations": ["UsedFor"], "vn": ["throw-50.1"]}},
        "other": {"toss": {"relations": [], "vn": ["throw-50.1"]}},
    }
    nouns = {"ball": ["noun.object"]}
    stamp = {"corpus": "test"}
    A._VN_INDEX = None
    A._VN_WIDEN = True
    on = A.merge("ball", [], (acts, nouns, stamp))
    verbs = {p["action_verb"] for p in on}
    assert "throw" in verbs and "toss" in verbs, verbs
    sisters = [p for p in on if p.get("verbnet_widened")]
    assert sisters and all(p["standing"] == "none" for p in sisters)
    assert all(p["source"] == A.CN_SOURCE for p in sisters)
    A._VN_WIDEN = False
    off = A.merge("ball", [], (acts, nouns, stamp))
    assert {p["action_verb"] for p in off} == {"throw"}
    A._VN_WIDEN = True
    print("widen on/off identity: OK")


def test_must_fail_no_declared_class():
    # if the found verb has NO class, no sisters -> the expansion cannot manufacture them
    acts = {"ball": {"kick": {"relations": ["CapableOf"], "vn": []}},
            "other": {"toss": {"relations": [], "vn": ["throw-50.1"]}}}
    A._VN_INDEX = None
    assert A._vn_sisters(["kick"], acts) == []
    print("MF no-class: OK")


def test_real_data_has_classes():
    acts, _nouns, _stamp = A.cn_sources()
    A._VN_INDEX = None
    # throw is a documented example (42:116); find any concept that declares it
    found = [v for c, vs in acts.items() if isinstance(vs, dict)
             for v, a in vs.items() if isinstance(a, dict) and v == "throw"]
    assert found, "throw not in relations data"
    sisters = A._vn_sisters(["throw"], acts)
    assert len(sisters) > 0, "throw has a class but no sisters found"
    print("real-data sisters:", len(sisters), sisters[:8])


if __name__ == "__main__":
    test_vn_sisters()
    test_merge_widens_and_arm_off_is_identity()
    test_must_fail_no_declared_class()
    test_real_data_has_classes()
    print("verbnet-widen: OK")
