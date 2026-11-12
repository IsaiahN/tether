"""8a-0, THE PICK-TIER FIELD (TETHER_PICK_TIER, default OFF; r1789, r1796): the library row's
tier_offered (each offered entry's K1 tier) and tier_landed (each landed entry's tier).

  P1    gridworld 12 and the dc22 capture (acts forced), arm ON vs OFF: identical once the two
        fields are taken off the library rows -- the record moves nothing. gw12 loads no library
        and writes no library row, so there it is the identity alone; dc22 carries the fields.
  P2    with the arm ON the fields are written and name real tiers (not vacuous); the tier
        distribution of offered and landed entries on dc22, a reading.
  P3    no reader: only _tiers (the writer), _land_kind, the lookup's reset and the library row
        touch the map; MF3 a planted reader fails the check.

    python tests/test_pick_tier.py
"""
from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
import tempfile
from collections import Counter

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
import test_pay_gap as pg

sys.dont_write_bytecode = True
HERE = _repo.ROOT
FIELDS = {"library:tier_offered", "library:tier_landed"}
ALLOWED = {"_tiers", "put", "_land_kind", "_library_reach", "__init__"}


def _env(arm: bool) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")
    if arm:
        env["TETHER_PICK_TIER"] = "1"
    return env


def run(code: str, args: list, arm: bool, path: str) -> list[dict]:
    p = subprocess.run([sys.executable, "-B", "-c", code, *args], capture_output=True, text=True,
                       env=_env(arm), cwd=HERE, stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    with open(path, encoding="utf-8") as fh:
        return [json.loads(x) for x in fh if x.strip()]


def same(off: list[dict], on: list[dict]) -> list[str]:
    for rows in (off, on):
        for r in rows:
            if r.get("slot") == "@run" and r["event"] == "arms":
                r["detail"].pop("on", None)
                r["detail"].pop("off", None)
    return pg.compare(off, on, set(), FIELDS)


def readers(src: str) -> list[str]:
    out = []

    def walk(node, fn):
        for ch in ast.iter_child_nodes(node):
            f = ch.name if isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef)) else fn
            if (isinstance(ch, ast.Attribute) and ch.attr in ("_tier_of", "_tier_land")
                    and f not in ALLOWED):
                out.append(f"{f}:{ch.lineno}")
            walk(ch, f)
    walk(ast.parse(src), None)
    return out


def main() -> int:
    tmp = tempfile.mkdtemp()
    data = os.path.join(HERE, "tests", "data", "cue_key_path", "dc22_c24.json.gz")
    gw = {a: run(pg.GW, [os.path.join(tmp, f"gw{a}.jsonl"), "none"], a,
                 os.path.join(tmp, f"gw{a}.jsonl")) for a in (False, True)}
    dc = {a: run(pg.REPLAY, [data, "25", os.path.join(tmp, f"dc{a}.jsonl")], a,
                 os.path.join(tmp, f"dc{a}.jsonl")) for a in (False, True)}
    for name, d in (("gw12", gw), ("dc22 c0-24 forced", dc)):
        lib_on = [r for r in d[True] if r["event"] == "library"]
        with_f = [r for r in lib_on if "tier_offered" in r["detail"]]
        assert not any("tier_offered" in r["detail"] for r in d[False] if r["event"] == "library")
        bad = same(d[False], d[True])
        print(f"P1 {name}: OFF {len(d[False])} rows, ON {len(d[True])}; library rows "
              f"{len(lib_on)}, {len(with_f)} carry the fields: "
              f"{'IDENTICAL' if not bad else bad[:3]}"
              + ("" if lib_on else " (no library here: identity only, the fields cannot show)"))
        assert not bad and (with_f or not lib_on), bad[:5]
        assert len(with_f) == len(lib_on), "a library row without the fields, arm ON"
    assert any(r["event"] == "library" for r in dc[True]), "dc22 wrote no library row"
    rows = [r["detail"] for r in dc[True] if r["event"] == "library"]
    off_t = Counter(t for r in rows for t in r["tier_offered"].values())
    land_t = Counter(t for r in rows for t in r["tier_landed"].values())
    print(f"P2 dc22 offered entries by tier: {dict(sorted(off_t.items()))}")
    print(f"   landed entries by tier: {dict(sorted(land_t.items()))}")
    assert off_t and any(t != "untiered" for t in off_t), "no offered entry carries a tier"

    with open(os.path.join(HERE, "tether.py"), encoding="utf-8") as fh:
        src = fh.read()
    found = readers(src)
    print(f"P3 readers of the tier map outside its writers: {found or 'none'}")
    assert not found, found
    hit = readers(src + "\n\ndef _planted(self):\n    return self._tier_of\n")
    print(f"MF3 a planted reader: {hit}")
    assert len(hit) == 1 and hit[0].startswith("_planted:"), hit
    print("pick_tier: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
