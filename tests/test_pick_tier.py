"""8a-0, THE PICK-TIER FIELD (TETHER_PICK_TIER, default OFF; 8d sets it ON; r1789, r1796, r1812):
the library row's tier_offered (each offered entry's K1 tier) and tier_landed (each landed
entry's tier).

  P1    gridworld 12 and the dc22 capture (acts forced), arm ON vs OFF: identical once the two
        fields are taken off the library rows -- the record moves nothing. gw12 loads no library
        and writes no library row, so there it is the identity alone; dc22 carries the fields.
  P2    THE LABELS ARE TRUE (r1812 2): a spy on _tiers rebuilds each entry's tier from the call's
        own output -- put() is out's only writer and n holds each tier's count in call order --
        and every label must equal it, after every call; every library row's tier_offered and
        tier_landed must equal its lookup's rebuilt map ("untiered" where none placed it).
        MF2 every label T3, and every label shifted one tier down: each goes RED.
        The tier distribution on dc22, a reading; a tier with no entry is named (T2 reads the
        carried store, and the replay runs without a lineage).
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
TIERS = ("T1a", "T1b", "T1c", "T2", "T3", "T1d", "T4", "T5")

SPY = r'''
import atexit, sys as _sys
_PLANT = os.environ.get("PT_PLANT", "")
_SHIFT = {"T1a": "T1b", "T1b": "T1c", "T1c": "T2", "T2": "T3", "T3": "T1d", "T1d": "T4",
          "T4": "T5", "T5": "T5"}
LAB = {"calls": 0, "bad": [], "main": []}
class _Planted(dict):
    def __setitem__(self, k, v):
        super().__setitem__(k, "T3" if _PLANT == "mislabel" else _SHIFT.get(v, v))
_t = tether.Agent._tiers
def _tiers(self, lib, lit, dk, mine, *a, **k):
    if _PLANT and self._tier_of is not None and not isinstance(self._tier_of, _Planted):
        self._tier_of = _Planted(self._tier_of)
    out, n = _t(self, lib, lit, dk, mine, *a, **k)
    if self._tier_of is not None:
        exp, i = {}, 0
        for tier, c in n.items():
            for kk, _w in out[i:i + c]:
                exp[kk] = tier
            i += c
        LAB["calls"] += 1
        bad = [[kk, t, self._tier_of.get(kk)] for kk, t in exp.items()
               if self._tier_of.get(kk) != t]
        if bad or i != len(out):
            LAB["bad"].append([self.cycle, len(bad), i, len(out), bad[:2]])
        if _sys._getframe(1).f_code.co_name == "_library_reach":
            LAB["main"].append([len(self.led), exp])
    return out, n
tether.Agent._tiers = _tiers
atexit.register(lambda: print("LABELS", json.dumps(LAB)))
'''


def _env(arm: bool, plant: str = "") -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith(("TETHER_", "PT_"))}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")
    if arm:
        env["TETHER_PICK_TIER"] = "1"
    if plant:
        env["PT_PLANT"] = plant
    return env


def run(code: str, args: list, arm: bool, path: str, plant: str = "") -> tuple[list, dict]:
    p = subprocess.run([sys.executable, "-B", "-c", code, *args], capture_output=True, text=True,
                       env=_env(arm, plant), cwd=HERE, stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    with open(path, encoding="utf-8") as fh:
        rows = [json.loads(x) for x in fh if x.strip()]
    lab = next((json.loads(x[len("LABELS "):]) for x in p.stdout.splitlines()
                if x.startswith("LABELS ")), None)
    return rows, lab


def same(off: list[dict], on: list[dict]) -> list[str]:
    for rows in (off, on):
        for r in rows:
            if r.get("slot") == "@run" and r["event"] == "arms":
                r["detail"].pop("on", None)
                r["detail"].pop("off", None)
    return pg.compare(off, on, set(), FIELDS)


def truth(rows: list[dict], lab: dict) -> tuple[int, int, list]:
    """(calls whose labels were wrong, library rows checked, library rows wrong)."""
    main = sorted(lab["main"], key=lambda m: m[0])
    checked, wrong = 0, []
    for r in rows:
        d = r["detail"]
        if r["event"] != "library" or "tier_offered" not in d:
            continue
        exp = next((e for n, e in reversed(main) if n <= r["seq"]), {})
        checked += 1
        for f in ("tier_offered", "tier_landed"):
            off = {k: t for k, t in d[f].items() if exp.get(k, "untiered") != t}
            if off:
                wrong.append([r["seq"], f, dict(list(off.items())[:2])])
    return len(lab["bad"]), checked, wrong


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
    replay = pg.REPLAY.replace("tether._AGENT_SEED = False\n",
                               "tether._AGENT_SEED = False\n" + SPY, 1)
    assert SPY in replay

    def dc(arm: bool, plant: str = "") -> tuple[list, dict]:
        p = os.path.join(tmp, f"dc{arm}{plant}.jsonl")
        return run(replay, [data, "25", p], arm, p, plant)

    gw = {a: run(pg.GW, [os.path.join(tmp, f"gw{a}.jsonl"), "none"], a,
                 os.path.join(tmp, f"gw{a}.jsonl"))[0] for a in (False, True)}
    d_off, _ = dc(False)
    d_on, lab = dc(True)
    for name, off, on in (("gw12", gw[False], gw[True]), ("dc22 c0-24 forced", d_off, d_on)):
        lib_on = [r for r in on if r["event"] == "library"]
        with_f = [r for r in lib_on if "tier_offered" in r["detail"]]
        assert not any("tier_offered" in r["detail"] for r in off if r["event"] == "library")
        bad = same(off, on)
        print(f"P1 {name}: OFF {len(off)} rows, ON {len(on)}; library rows "
              f"{len(lib_on)}, {len(with_f)} carry the fields: "
              f"{'IDENTICAL' if not bad else bad[:3]}"
              + ("" if lib_on else " (no library here: identity only, the fields cannot show)"))
        assert not bad and len(with_f) == len(lib_on), bad[:5]
    assert any(r["event"] == "library" for r in d_on), "dc22 wrote no library row"

    nbad, checked, wrong = truth(d_on, lab)
    print(f"P2 labels: {lab['calls']} _tiers calls checked, {nbad} with a wrong label; "
          f"{checked} library rows checked against their lookup's map, {len(wrong)} wrong")
    assert lab["calls"] and checked and not nbad and not wrong, (lab["bad"][:2], wrong[:2])
    for plant in ("mislabel", "shift"):
        rows_p, lab_p = dc(True, plant)
        nb, ch, wr = truth(rows_p, lab_p)
        print(f"MF2 {plant} planted: " + (f"RED -- {nb} calls with wrong labels (e.g. "
              f"{lab_p['bad'][0][4][:1]}), {len({w[0] for w in wr})} of {ch} library rows wrong"
              if nb or wr else "GREEN (the plant went unseen)"))
        assert nb and wr, f"the {plant} plant left the labels check green"

    rows = [r["detail"] for r in d_on if r["event"] == "library"]
    off_t = Counter(t for r in rows for t in r["tier_offered"].values())
    land_t = Counter(t for r in rows for t in r["tier_landed"].values())
    print(f"   dc22 offered entries by tier: {dict(sorted(off_t.items()))}")
    print(f"   landed entries by tier: {dict(sorted(land_t.items()))}")
    for t in TIERS:
        if not off_t.get(t) and not land_t.get(t):
            why = (" (T2 reads the carried store; the replay runs without a lineage: 8d, on a copy "
                   "of central, is where T2 is read)" if t == "T2" else "")
            print(f"   {t}: 0 offered, 0 landed on this capture -- {t} path not exercised{why}")
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
