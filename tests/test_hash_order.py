"""Sets of strings iterate in a per-process hash order (the reviewer 2026-11-07 r1371, r1375; no
arm, r1297): what the agent writes or sums over one must not depend on PYTHONHASHSEED. Each check
runs a child per hash seed, each in its own process.

check_muse  _muse_choose: 8 walked kinds (strings), called three times in one cycle, so each kind's
            ("muse", kind) standing crosses under its witnesses on the third read and writes one
            standing_freed row. Precondition: the kind set iterates in a different order under the
            two seeds (printed). The rows come out in one order under both. MUST-FAIL, run: the old
            loop over the set, compiled back in, gives the rows in two orders
check_gcw   _gcw_score: every (class, delta kind, nouns read) case under both seeds sums equal bit
            for bit. The old loop over `hit` could not differ either: one class per entry, so verb
            and filler never meet and hit holds at most two terms, and a + b == b + a. That bound
            is asserted; the old-line MF cannot fail and is not claimed

    python tests/test_hash_order.py [check ...]
"""
from __future__ import annotations

import inspect
import json
import os
import subprocess
import sys
import textwrap

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

SEEDS = ("0", "1")
KINDS = [f"kind_{c}" for c in "abcdefgh"]
NEW_LOOP = "        for kind in sorted(walked, key=lambda k: (k is None, str(k))):\n"
OLD_LOOP = "        for kind in walked:\n"


def _child(check: str, mode: str) -> None:
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    if check == "muse":
        if mode == "old":
            src = inspect.getsource(tether.Agent._muse_choose)
            old = src.replace(NEW_LOOP, OLD_LOOP)
            assert old != src, "MF: the new loop was not found to revert"
            ns: dict = {}
            exec(textwrap.dedent(old), tether.__dict__, ns)
            tether.Agent._muse_choose = ns["_muse_choose"]
        env = world.bind(gridworld.family("default", 0))
        ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
        assert "muse" in ag._reflexes, "precondition: TETHER_MUSING_CHOSEN on"
        targets = {f"p{i}": {"kind": k, "gain": 0.0} for i, k in enumerate(KINDS)}
        run = {"terms": {}, "paying": [], "walked": list(targets)}
        for _ in range(3):
            ag._muse_choose(run, targets)
        rows = [r["detail"]["situation"] for r in ag.led.rows() if r["event"] == "standing_freed"
                and r["detail"].get("form") == "muse"]
        print(json.dumps({"set_order": list(set(KINDS)), "rows": rows}))
    else:
        ps = {"verb": 0.1, "noun": 0.2, "filler": 0.3}
        stub = type("S", (), {"_gcw_win": {}})()
        classes = tether._gcw_classes()
        names = {}
        for e, c in classes.items():
            names.setdefault(c, e)
        out, most = [], 0
        for cls, e in sorted(names.items()):
            for has_dk in (False, True):
                for n in (0, 1, 3):
                    reads = {f"r{i}" for i in range(n)}
                    post = {e: frozenset(reads)}
                    v = tether.Agent._gcw_score(stub, e, reads, post, has_dk, ps)
                    most = max(most, len(stub._gcw_win[e]))
                    out.append([cls, has_dk, n, float(v).hex()])
        print(json.dumps({"sums": out, "most_terms": most}))


def child(check: str, mode: str, seed: str) -> dict:
    env = {**os.environ, "PYTHONHASHSEED": seed, "PYTHONDONTWRITEBYTECODE": "1"}
    p = subprocess.run([sys.executable, "-B", __file__, "--child", check, mode], env=env,
                       capture_output=True, text=True, stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-2000:]
    return json.loads(p.stdout.strip().splitlines()[-1])


def check_muse() -> None:
    a, b = (child("muse", "new", s) for s in SEEDS)
    assert a["set_order"] != b["set_order"], ("precondition: the two seeds order the set alike",
                                              a["set_order"])
    assert len(a["rows"]) == len(KINDS), a["rows"]
    assert a["rows"] == b["rows"], (a["rows"], b["rows"])
    oa, ob = (child("muse", "old", s) for s in SEEDS)
    assert len(oa["rows"]) == len(KINDS) and oa["rows"] != ob["rows"], "MF: the old loop agreed"
    print(f"  seeds {SEEDS}: set orders {a['set_order'][:3]}... / {b['set_order'][:3]}...; "
          f"{len(a['rows'])} standing_freed rows in one order; MF: the old loop's rows differ")


def check_gcw() -> None:
    a, b = (child("gcw", "new", s) for s in SEEDS)
    assert a["sums"] == b["sums"], "the sums differ across hash seeds"
    assert a["most_terms"] <= 2, a["most_terms"]
    print(f"  {len(a['sums'])} cases equal bit for bit under seeds {SEEDS}; hit holds at most "
          f"{a['most_terms']} terms, so the old loop's order could not change a sum")


def main() -> int:
    if sys.argv[1:2] == ["--child"]:
        _child(*sys.argv[2:4])
        return 0
    want = set(sys.argv[1:])
    for c in (check_muse, check_gcw):
        if not want or c.__name__ in want:
            c()
            print("ok  ", c.__name__)
    print("test_hash_order OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
