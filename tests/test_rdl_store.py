"""RDL PIECE 1, THE STORE (rdl_store.py; spec docs/03-DESIGN/RDL_BUILD_SPEC_2026-11-16.md).

  S1     STAGES and the tier <-> stage pairing; the pid is sha256[:16] of the canonical JSON of
         every other field, and changes when any field changes
  S2     head_start (C1) passes a kind-level head start (a WordNet class, a card)
  S3     usable (C2): a bond AND an attach; either missing -> recorded
  S4     dump -> load round trip is exact and deterministic (two dumps byte-identical); the
         header carries the standing note and readers; a tampered field fails the pid check
  MF-S1  planted recordings are REJECTED by head_start: an object name (o12), a move list
         (up, up, left), an action sequence (ACTION1 ACTION3), a coordinate ((3, 4)) and a
         solution handed over -- each prints 'RED as required'
  MF-S2  no field means standing (C3): Preload has no standing/settled/score field

Seconds. python tests/test_rdl_store.py
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path
import rdl_store as S

sys.dont_write_bytecode = True


def _json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

SRC = {"corpus": "test", "corpus_sha": "0" * 64, "parser": "test", "parser_version": "1"}


def _ok(**kw):
    base = {"tier": 1, "source": SRC, "kind": "wn:n01440764",
            "text": "tench: freshwater fish", "bonds": (("≡", "tench", "Tinca_tinca"),),
            "attaches": ("CONNECTION|Membrane boundary",)}
    base.update(kw)
    return S.make(**base)


def check_s1() -> None:
    assert S.STAGES == ("instance", "regularity", "abstraction", "core_rule")
    p = _ok()
    assert p.stage == "instance" and p.tier == 1
    body = {k: v for k, v in dataclasses.asdict(p).items() if k != "pid"}
    want = hashlib.sha256(S.canonical(body).encode("utf-8")).hexdigest()[:16]
    assert p.pid == want and len(p.pid) == 16
    assert _ok(text="tench: other words").pid != p.pid
    assert _ok(tier=4, kind="card:X").stage == "core_rule"
    print("  S1: STAGES, tier <-> stage, pid = sha256[:16] of the canonical other fields")


def check_s2() -> None:
    for p in (_ok(), _ok(tier=4, kind="card:TETHER|Which link first",
                         text="(¬SEE ⇒ ask SEE) → (¬WORDS ⇒ ask WORDS)")):
        ok, why = S.head_start(p)
        assert ok, why
    print("  S2: head_start passes a class and a card")


def check_s3() -> None:
    assert S.usable(_ok())
    assert not S.usable(_ok(bonds=()))
    assert not S.usable(_ok(attaches=()))
    print("  S3: usable needs a bond AND an attach; either missing is recorded")


def check_s4() -> None:
    ps = [_ok(), _ok(kind="wn:n01443537", text="goldfish: fish"),
          _ok(tier=3, kind="wn:n02512053", text="KIND fish", parents=(_ok().pid,))]
    with tempfile.TemporaryDirectory() as d:
        a, b = os.path.join(d, "a.json"), os.path.join(d, "b.json")
        S.dump(ps, a, {"sources": {}, "licences": {}})
        S.dump(list(reversed(ps)), b, {"licences": {}, "sources": {}})
        assert Path(a).read_bytes() == Path(b).read_bytes(), "dump not deterministic"
        back = S.load(a)
        assert sorted(back, key=lambda p: p.pid) == sorted(ps, key=lambda p: p.pid)
        h = S.load_header(a)
        assert h["standing"] == S.STANDING and "readers" in h
        doc = _json(a)
        doc["preloads"][0]["text"] = "tampered"
        with open(b, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False)
        try:
            S.load(b)
        except ValueError:
            pass
        else:
            raise AssertionError("a tampered field passed the pid check")
    print("  S4: dump/load exact and deterministic; standing note + readers; tamper caught")


def check_mf_s1() -> None:
    plants = {
        "object name": _ok(text="tench: o12 moves when pressed"),
        "move list": _ok(text="tench: up, up, left, right"),
        "action sequence": _ok(bonds=(("→", "ACTION1", "ACTION3"),)),
        "coordinate": _ok(text="tench: at (3, 4)"),
        "solution": _ok(refusal=("solution: press the red one",)),
        "object kind": _ok(kind="o7"),
    }
    for what, p in plants.items():
        ok, why = S.head_start(p)
        assert not ok, f"planted {what} passed head_start"
        print(f"  MF-S1 {what}: rejected ({why}) -- RED as required")


def check_mf_s2() -> None:
    names = {f.name for f in dataclasses.fields(S.Preload)}
    bad = names & {"standing", "settled", "score", "trust", "weight", "reachable"}
    assert not bad, f"a field means standing: {bad}"
    print("  MF-S2: no field of Preload means standing (C3)")


if __name__ == "__main__":
    for fn in (check_s1, check_s2, check_s3, check_s4, check_mf_s1, check_mf_s2):
        fn()
    print("test_rdl_store: GREEN")
