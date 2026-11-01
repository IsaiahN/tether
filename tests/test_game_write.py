"""26 GAME_WRITE (TETHER_GAME_WRITE, default ON; the reviewer 2026-10-31 r575). The stream
(e4_stream) over 3 games, 4 steps each, offline, each arm on its own fresh lineage folder, then
each folder loaded by a fresh agent.
  check_must_hold   r575's three: (1) ON's generations are ONE chain (each hashes to its name;
                    2 game writes + the end write) and every game_write row verified; (2) the end
                    write is the chain's tip and the one result.json names; (3) the library a
                    fresh agent loads is the same ON and OFF (library_n and the term keys). OFF
                    writes one generation and no game_write rows. And the agent's own ledger is
                    the same ON and OFF, row for row (timings masked): a write changes no decision
    python tests/test_game_write.py [check ...]
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import zlib

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

LOAD = r'''
import json, sys
sys.dont_write_bytecode = True
tree, lin = sys.argv[1], sys.argv[2]
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import arc_holdout
from test_entry import FakeWrapper
env, ag, *_ = arc_holdout.wire(FakeWrapper(), "fake", lineage_dir=lin)
print(json.dumps({"parent": ag.lineage_parent, "library_n": len(ag.gamma.library),
                  "keys": sorted(map(str, ag.gamma.library))}))
'''


def _env(extra: dict | None = None) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               **(extra or {}))
    return env


def _json(*p: str):
    with open(os.path.join(*p), encoding="utf-8") as fh:
        return json.load(fh)


def _stream(d: str, extra: dict | None = None) -> tuple[str, str]:
    root = str(_repo.ROOT)
    lin, out = os.path.join(d, "lineage"), os.path.join(d, "out")
    os.makedirs(lin)
    cmd = [sys.executable, "-B", os.path.join(root, "harness", "mem_store", "e4_stream.py"),
           root, out, "--seed", "26a26a26", "--lineage", lin, "--n-games", "3",
           "--slice-steps", "4"]
    r = subprocess.run(cmd, env=_env(extra), capture_output=True, text=True, timeout=3600,
                       cwd=root, stdin=subprocess.DEVNULL)
    assert r.returncode == 0, r.stderr[-3000:]
    return lin, out


def _gens(lin: str) -> dict:
    out = {}
    for n in os.listdir(lin):
        if n.startswith("gen_"):
            with open(os.path.join(lin, n), "rb") as fh:
                raw = fh.read()
            b = zlib.decompress(raw) if raw[:1] == b"\x78" else raw
            assert n == f"gen_{hashlib.sha256(b).hexdigest()[:16]}.json", ("bad hash", n)
            out[n[4:20]] = json.loads(b)
    return out


def _chain(gens: dict) -> list:
    kids = {g.get("parent"): h for h, g in gens.items()}
    roots = [h for h, g in gens.items() if g.get("parent") not in gens]
    assert len(roots) == 1, ("not one chain", roots)
    chain, h = [], roots[0]
    while h is not None and len(chain) <= len(gens):
        chain.append(h)
        h = kids.get(h)
    assert len(chain) == len(gens), ("not one chain", chain, sorted(gens))
    return chain


def _load(lin: str) -> dict:
    r = subprocess.run([sys.executable, "-B", "-c", LOAD, str(_repo.ROOT), lin], env=_env(),
                       capture_output=True, text=True, timeout=1800, cwd=str(_repo.ROOT),
                       stdin=subprocess.DEVNULL)
    assert r.returncode == 0, r.stderr[-3000:]
    return json.loads(r.stdout.strip().splitlines()[-1])


def check_must_hold() -> None:
    with tempfile.TemporaryDirectory() as d_on, tempfile.TemporaryDirectory() as d_off:
        lin_on, out_on = _stream(d_on)
        lin_off, out_off = _stream(d_off, {"TETHER_GAME_WRITE": "0"})
        with open(os.path.join(out_on, "game_write.jsonl"), encoding="utf-8") as fh:
            rows = [json.loads(x) for x in fh]
        res_on, res_off = _json(out_on, "stream.result.json"), _json(out_off, "stream.result.json")
        g_on, g_off = _gens(lin_on), _gens(lin_off)
        chain = _chain(g_on)
        for r in rows:
            print(f"  game write after {r['idx']} {r['game']}: {r['s']} s, peak "
                  f"{r['peak_commit_mb']} MB, names {r['names_before']} -> {r['names_after']}, "
                  f"terms {r['terms']}, verified {r['verified']} {r['why']}")
        print(f"  ON chain {chain}; OFF generations {sorted(g_off)}")
        assert len(rows) == 2 and all(r["verified"] for r in rows), rows
        assert res_on["game_writes"] == 2 and res_on["game_writes_refused"] == 0, res_on
        assert len(chain) == 3 and [r["hash"] for r in rows] == chain[:2], (chain, rows)
        assert f"'hash': '{chain[-1]}'" in res_on["lineage"], ("end write not the tip", res_on)
        assert len(g_off) == 1 and res_off["game_writes"] == 0
        assert not os.path.exists(os.path.join(out_off, "game_write.jsonl"))
        a, b = _load(lin_on), _load(lin_off)
        print(f"  loaded: ON library_n {a['library_n']} parent {a['parent']}; OFF library_n "
              f"{b['library_n']} parent {b['parent']}; keys only ON "
              f"{len(set(a['keys']) - set(b['keys']))}, only OFF "
              f"{len(set(b['keys']) - set(a['keys']))}")
        assert a["parent"] == chain[-1]
        assert a["library_n"] == b["library_n"] and a["keys"] == b["keys"], "library differs"
        la, lb = _rows(out_on), _rows(out_off)
        n = sum(1 for x, y in zip(la, lb, strict=False) if x != y) + abs(len(la) - len(lb))
        end_terms = res_on["lineage"].split("'terms': ")[1].split(",")[0]
        print(f"  the agent's ledger ON vs OFF: {len(la)} rows ON, {len(lb)} OFF, {n} differences; "
              f"terms carried by the game writes {sum(r['terms'] or 0 for r in rows)}, by the end "
              f"write {end_terms}")
        assert len(la) > 100 and n == 0, "a game write changed what the agent did"


def _rows(out: str) -> list:
    sys.path.insert(0, os.path.join(str(_repo.ROOT), "conform"))
    from identity_mod_rows import mask_timings
    with open(os.path.join(out, "stream.jsonl"), encoding="utf-8") as fh:
        rows = [json.loads(x) for x in fh]
    return [(r["cycle"], r["step"], r["slot"], r["event"],
             json.dumps(r["detail"], sort_keys=True, default=str))
            for r in mask_timings(rows) if r["event"] != "arms"]


def main() -> int:
    want = sys.argv[1:]
    names = [k for k in globals() if k.startswith("check_") and (not want or k in want)]
    assert not want or len(names) == len(want), ("unknown check name", sorted(want))
    if len(names) == 1:
        globals()[names[0]]()
        print("ok  ", names[0])
        return 0
    for n in names:
        r = subprocess.run([sys.executable, "-B", __file__, n], cwd=str(_repo.ROOT),
                           stdin=subprocess.DEVNULL)
        assert r.returncode == 0, n
    print(f"game_write: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
