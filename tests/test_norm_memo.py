"""_norm_name memoised (the reviewer 2026-11-07 r1361 (A); a pure cost fix, no arm, r1297): the
cache returns exactly what the uncached function returns, and a run with it is the run without it.
ft09, 4 cycles, offline, cold, no lineage (about 90 s): on gridworld the name join never reaches a
row, so a wrong normalisation leaves its ledger as it was and could not fail there.

check_pure      every library key's tail and every atom name: cached == the uncached function
                (_norm_name.__wrapped__); the cache is bounded (maxsize set)
check_identity  ft09 4 cycles with _norm_name uncached against cached: identical
                (identity_mod_rows.compare, TIMINGS masked), and the cache was hit. MUST-FAIL: a
                normalisation that keeps case and punctuation (x itself) makes a run that differs

    python tests/test_norm_memo.py [check ...]
"""
from __future__ import annotations

import json
import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import subprocess  # noqa: E402
import tempfile  # noqa: E402

import arc_holdout  # noqa: E402
import gridworld  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402
from conform.identity_mod_rows import compare, mask_timings  # noqa: E402

MEMO = tether._norm_name
RAW = MEMO.__wrapped__


MODES = {"memo": MEMO, "raw": RAW, "wrong": lambda x: x}     # wrong: the MF's join


def run(mode: str, n: int = 4) -> tuple:
    """ft09, n cycles, cold, no lineage, under the named join, each in its own process (a second
    in-process run reads the first's process state: the consolidate row's "before"); its ledger."""
    with tempfile.TemporaryDirectory() as d:
        led = os.path.join(d, "run.jsonl")
        p = subprocess.run([sys.executable, "-B", __file__, "--child", mode, led, str(n)],
                           capture_output=True, text=True, stdin=subprocess.DEVNULL)
        assert p.returncode == 0, p.stderr[-2000:]
        with open(led, encoding="utf-8") as f:
            rows = [json.loads(x) for x in f if x.strip()]
    hits = int(p.stdout.strip().splitlines()[-1])
    return [r for r in rows if r["event"] not in ("header", "arms")], hits


def child(mode: str, led: str, n: str) -> None:
    tether._norm_name = MODES[mode]
    arc_holdout.play("ft09", int(n), led_path=led)
    print(MEMO.cache_info().hits)


def check_pure() -> None:
    lib = tether._library()
    env = world.bind(gridworld.family("default", 0))
    keys = tether.Agent._lib_keys(lib)
    names = [k.split("|")[-1] for k in keys] + list(keys)
    names += [a.name for a in env.atoms()]
    bad = [x for x in names if MEMO(x) != RAW(x)]
    assert not bad, bad[:5]
    assert MEMO.cache_info().maxsize, MEMO.cache_info()
    stale = tether.lru_cache(maxsize=8)(lambda x: RAW(x[:1]))      # MF: a wrong memo is caught
    assert [x for x in names if stale(x) != RAW(x)], "MF: no name differs"
    print(f"  {len(names)} names: cached == uncached; {MEMO.cache_info()}")


def check_identity() -> None:
    memo, hits = run("memo")
    raw, _h = run("raw")
    bad = compare(mask_timings(raw), mask_timings(memo), set())
    assert not bad and hits > 0, (bad[:3], hits)
    wrong, _h = run("wrong")
    assert compare(mask_timings(raw), mask_timings(wrong), set()), "MF: no difference"
    print(f"  {len(memo)} rows identical cached / uncached ({hits} cache hits); MF: a "
          "normalisation that keeps the name as written differs")


def main() -> int:
    if sys.argv[1:2] == ["--child"]:
        child(*sys.argv[2:5])
        return 0
    want = set(sys.argv[1:])
    for c in (check_pure, check_identity):
        if not want or c.__name__ in want:
            c()
            print("ok  ", c.__name__)
    print("test_norm_memo OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
