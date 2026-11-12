"""8a-0, THE REACHED-AND-PAID FIELD (TETHER_REACH_PAID, default OFF; 8d sets it ON; r1795, r1796,
r1812 4, r1815): reached (offered in a lookup), minted (the mint's winner came from that offer;
the mint row's from_offer), settled (that term later held out-of-fit; the settle row's
from_offer), each with the entry's K1 tier, and the run-end reached_paid row (settled first).

  P1    gridworld 12 and the dc22 capture (acts forced, run ended), arm ON vs OFF: identical once
        reached_paid is dropped and from_offer is taken off the mint / settle rows.
  P2    REACHED IS TRUE: each reached record's tier equals its lookup's rebuilt tier map (the
        pick-tier rebuild); MF2a every tier shifted one down, through the agent's own map: RED.
        THE CHAIN: every minted record names an entry reached on that slot no later than its
        mint, every settled record a term with a mint record. On today's captures no offer is
        minted (the 0-mint stop), so the chain runs on zero agent records -- printed as not
        exercised -- and the CHECKER is proven on planted rows: MF2b a minted record whose entry
        was never reached, MF2c a settled record with no mint record: each RED.
        The run-end row: its counts agree with the records; settled first; the drop-offs named;
        its scope (this process; not across runs or the lineage) printed as not tracked.
        BOUND_BY (r1816 3): every accepted settle row's bound_by equals the first path the
        ledger names the term by (reuse_install / pull / rebind / the mint row, from_offer when
        it carries one) on that slot, else on any; MF2d the paths rotated in _rp_bind: RED.
  P3    no reader: only the reached-and-paid writers touch its records; MF3 a planted reader.

    python tests/test_reach_paid.py
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
import test_pick_tier as pt

sys.dont_write_bytecode = True
HERE = _repo.ROOT
FIELDS = {"mint:from_offer", "settle:from_offer", "settle:bound_by"}
ATTRS = ("_rp_reached", "_rp_minted", "_rp_settled", "_rp_summary", "_rp_bound")
ALLOWED = {"_library_reach", "_mint", "settle", "end_run", "_rp_summary", "_rp_bind", "__init__"}

DUMP = r'''
_lr = tether.Agent._library_reach
REACH = []
def _library_reach(self, *a, **k):
    before, n0 = set(self._rp_reached), len(LAB["main"])
    out = _lr(self, *a, **k)
    if len(LAB["main"]) > n0:
        exp = LAB["main"][-1][1]
        for key in set(self._rp_reached) - before:
            REACH.append([key[0], key[1], self._rp_reached[key][1], exp.get(key[1], "untiered")])
    return out
tether.Agent._library_reach = _library_reach
if os.environ.get("PT_PLANT") == "bound":
    _ROT = {"route_pull": "rebind", "rebind": "reuse_install", "reuse_install": "route_pull",
            "mint": "route_pull", "from_offer": "route_pull"}
    _rb = tether.Agent._rp_bind
    tether.Agent._rp_bind = lambda self, s, t, p: _rb(self, s, t, _ROT.get(p, p))
atexit.register(lambda: print("REACHED", json.dumps(
    {"checked": REACH, "all": [[s, e, c, t] for (s, e), (c, t) in ag._rp_reached.items()]})))
'''


def _env(arm: bool, plant: str = "") -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith(("TETHER_", "PT_"))}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")
    if arm:
        env["TETHER_REACH_PAID"] = "1"
    if plant:
        env["PT_PLANT"] = plant
    return env


def run(code: str, args: list, arm: bool, path: str, plant: str = "") -> tuple[list, dict]:
    p = subprocess.run([sys.executable, "-B", "-c", code, *args], capture_output=True, text=True,
                       env=_env(arm, plant), cwd=HERE, stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    with open(path, encoding="utf-8") as fh:
        rows = [json.loads(x) for x in fh if x.strip()]
    rch = next((json.loads(x[len("REACHED "):]) for x in p.stdout.splitlines()
                if x.startswith("REACHED ")), None)
    return rows, rch


def same(off: list[dict], on: list[dict]) -> list[str]:
    for rows in (off, on):
        for r in rows:
            if r.get("slot") == "@run" and r["event"] == "arms":
                r["detail"].pop("on", None)
                r["detail"].pop("off", None)
    return pg.compare(off, on, {"reached_paid"}, FIELDS)


def chain(rows: list[dict], reached: list) -> tuple[int, int, list]:
    """(minted records, settled records, broken links): a minted record must name an entry reached
    on its slot no later than its cycle; a settled record a term some mint row minted from an
    offer."""
    first = {(s, e): c for s, e, c, _t in reached}
    minted = {r["detail"].get("term") or r["detail"].get("winner"): r for r in rows
              if r["event"] == "mint" and "from_offer" in r["detail"]}
    bad, n_m, n_s = [], 0, 0
    for r in rows:
        fo = r["detail"].get("from_offer")
        if fo is None:
            continue
        if r["event"] == "mint":
            n_m += 1
            c = first.get((r["slot"], fo["entry"]))
            if c is None or c > r["cycle"]:
                bad.append(["minted, never reached", r["seq"], r["slot"], fo["entry"]])
        elif r["event"] == "settle":
            n_s += 1
            if r["detail"].get("term") not in minted:
                bad.append(["settled, never minted", r["seq"], r["detail"].get("term")])
    return n_m, n_s, bad


PATH = {"reuse_install": "reuse_install", "pull": "route_pull", "rebind": "rebind"}


def bound(rows: list[dict]) -> tuple[Counter, list]:
    """(accepted settles by bound_by, mismatches): the first path the ledger names each term by,
    on the settle's slot, else on any slot -- the agent's own rule (_rp_bind), rebuilt from rows."""
    first: dict = {}
    seen, wrong = Counter(), []
    for r in sorted(rows, key=lambda x: x["seq"]):
        d, ev = r["detail"], r["event"]
        if ev in PATH or ev == "mint":
            t = d.get("term") or d.get("winner")
            p = PATH.get(ev) or ("from_offer" if "from_offer" in d else "mint")
            first.setdefault((r["slot"], t), p)
            first.setdefault((None, t), p)
        elif ev == "settle" and d.get("status") == "accepted":
            t = d.get("term")
            want = first.get((r["slot"], t), first.get((None, t), "none recorded"))
            seen[d.get("bound_by")] += 1
            if d.get("bound_by") != want:
                wrong.append([r["seq"], r["slot"], t, d.get("bound_by"), want])
    return seen, wrong


def readers(src: str) -> list[str]:
    out = []

    def walk(node, fn):
        for ch in ast.iter_child_nodes(node):
            f = ch.name if isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef)) else fn
            if (isinstance(ch, ast.Attribute) and ch.attr in ATTRS
                    and f not in ALLOWED and not (f or "").startswith("cell")):
                out.append(f"{f}:{ch.lineno}")
            walk(ch, f)
    walk(ast.parse(src), None)
    return out


def main() -> int:
    tmp = tempfile.mkdtemp()
    data = os.path.join(HERE, "tests", "data", "cue_key_path", "dc22_c24.json.gz")
    replay = pg.REPLAY.replace("tether._AGENT_SEED = False\n",
                               "tether._AGENT_SEED = False\n" + pt.SPY + DUMP, 1)
    replay = replay.replace("wall = time.perf_counter() - t0\n",
                            "ag.end_run('cap')\nwall = time.perf_counter() - t0\n", 1)
    assert pt.SPY in replay and "ag.end_run('cap')" in replay

    def dc(arm: bool, plant: str = "", cycles: int = 25) -> tuple[list, dict]:
        p = os.path.join(tmp, f"dc{arm}{plant}.jsonl")
        return run(replay, [data, str(cycles), p], arm, p, plant)

    gw = {a: run(pg.GW, [os.path.join(tmp, f"gw{a}.jsonl"), "none"], a,
                 os.path.join(tmp, f"gw{a}.jsonl"))[0] for a in (False, True)}
    d_off, _ = dc(False)
    d_on, rch = dc(True)
    for name, off, on in (("gw12", gw[False], gw[True]), ("dc22 c0-24 forced", d_off, d_on)):
        n_rp = sum(1 for r in on if r["event"] == "reached_paid")
        bad = same(off, on)
        print(f"P1 {name}: OFF {len(off)} rows, ON {len(on)} ({n_rp} reached_paid): "
              f"{'IDENTICAL' if not bad else bad[:3]}")
        assert not bad and n_rp == 1, bad[:5]

    wrong = [c for c in rch["checked"] if c[2] != c[3]]
    print(f"P2 reached: {len(rch['all'])} (slot, entry) records, {len(rch['checked'])} checked "
          f"against their lookup's tier map, {len(wrong)} wrong")
    assert rch["checked"] and not wrong, wrong[:3]
    _r, rch_p = dc(True, "shift", cycles=9)
    wrong_p = [c for c in rch_p["checked"] if c[2] != c[3]]
    print("MF2a tier shift planted (c0-8): " + (f"RED -- {len(wrong_p)} of "
          f"{len(rch_p['checked'])} reached records name the wrong tier (e.g. {wrong_p[0]})"
          if wrong_p else "GREEN (the plant went unseen)"))
    assert wrong_p, "the tier shift left the reached check green"

    n_m, n_s, broken = chain(d_on, rch["all"])
    print(f"   chain on the agent's records: {n_m} minted from an offer, {n_s} settled from an "
          f"offer, {len(broken)} broken")
    assert not broken, broken[:3]
    if not n_m:
        print("   minted / settled from an offer: 0 on this capture -- the chain's agent records "
              "are not exercised here (no offer reaches the mint today: the 0-mint stop); the "
              "checker is proven on planted rows below")
    s0, e0 = rch["all"][0][0], rch["all"][0][1]
    plant_b = [{"event": "mint", "seq": 10 ** 9, "cycle": 0, "slot": s0,
                "detail": {"term": "planted<x>", "from_offer": {"entry": "NEVER|reached"}}}]
    plant_c = [{"event": "settle", "seq": 10 ** 9 + 1, "cycle": 99, "slot": s0,
                "detail": {"term": "never<minted>", "status": "accepted",
                           "from_offer": {"entry": e0}}}]
    for tag, extra in (("MF2b minted, never reached", plant_b),
                       ("MF2c settled, never minted", plant_c)):
        _m, _s, b2 = chain(d_on + extra, rch["all"])
        print(f"{tag} planted: " + (f"RED -- {b2[0]}" if b2 else "GREEN (the plant went unseen)"))
        assert b2, f"{tag}: the checker left it green"

    seen, wrong_b = bound(d_on)
    print(f"   bound_by on the {sum(seen.values())} accepted settles: {dict(seen)}; "
          f"{len(wrong_b)} differ from the ledger's first naming path")
    assert seen and not wrong_b, wrong_b[:3]
    rows_b, _rb = dc(True, "bound", cycles=15)
    seen_b, wrong_bp = bound(rows_b)
    print("MF2d bound_by paths rotated (c0-14): " + (f"RED -- {len(wrong_bp)} of "
          f"{sum(seen_b.values())} settles name the wrong path (e.g. {wrong_bp[0]})"
          if wrong_bp else "GREEN (the plant went unseen)"))
    assert wrong_bp, "the bound_by rotation left the check green"

    rp = next(r["detail"] for r in d_on if r["event"] == "reached_paid")
    by = rp["by_tier"]
    want = Counter(t for _s, _e, _c, t in rch["all"])
    assert {t: c["reached"] for t, c in by.items()} == dict(want), (by, want)
    assert rp["headline"] == "settled" and rp["order"][:3] == ["settled", "minted", "reached"], rp
    assert all(c["reached_never_minted"] == c["reached"] - c["minted"] and
               c["minted_never_settled"] == c["minted"] - c["settled"] for c in by.values()), by
    assert rp["settled_by_path"] == dict(seen) and \
        rp["none_recorded"] == seen.get("none recorded", 0), (rp["settled_by_path"], seen)
    print(f"   run-end reached_paid by tier: {by}")
    print(f"   run-end settled_by_path: {rp['settled_by_path']} (none recorded "
          f"{rp['none_recorded']}: a non-zero count is a binding path not yet named, r1817)")
    print(f"   not tracked: {rp['scope']}")

    with open(os.path.join(HERE, "tether.py"), encoding="utf-8") as fh:
        src = fh.read()
    found = readers(src)
    print(f"P3 readers of the reached-and-paid records outside their writers: {found or 'none'}")
    assert not found, found
    hit = readers(src + "\n\ndef _planted(self):\n    return self._rp_minted\n")
    print(f"MF3 a planted reader: {hit}")
    assert len(hit) == 1 and hit[0].startswith("_planted:"), hit
    print("reach_paid: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
