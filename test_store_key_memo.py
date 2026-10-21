"""W1 / W2, THE STORE'S KEY MEMOS (TETHER_STORE_KEY_MEMO, TETHER_LOAD_KEY_MEMO; the reviewer
2026-10-21 15:38). The fake ARC game; every probe its own process, hash and agent seeds pinned.

  (1) W1's PLANT, the type hazard: 1 == True == 1.0 hash alike and json writes [1], [true],
      [1.0]. One merge's memo gives each of [1], [True], [1.0], (1,), [1] the string json.dumps
      gives it fresh; a memo keyed on the value (tuple(v)) gives [True] the string of [1] --
      shown to FAIL.
  (2) W1, BYTE-IDENTICAL: two fake games written into a fresh lineage (the second merges onto
      the first), memo ON and OFF: every file's bytes equal, and memory.db equal by an ordered
      dump of every table (iterdump; SQLite's page layout is not promised). Python's random is
      seeded per game (a handle's suffix draws from it), and a CONTROL writes OFF twice and
      must be identical first. PRECONDITION: the ON writes reused (hit > 0).
  (3) W2: that lineage loaded ON, OFF and ON+CHECK: the carried stores equal (_kind_known_dk,
      _kdk_last, the offered/known stores, the store's t2 and pairs); CHECK 0 disagree.
      PRECONDITION: hit > 0.
  (4) W2's memo is per load: a second load in one process (a one-game lineage first, then the
      two-game one) equals the two-game lineage loaded alone.

    python test_store_key_memo.py
"""
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))

PROBE = r'''
import hashlib, json, random, sys
sys.dont_write_bytecode = True
tree, mode = sys.argv[1], sys.argv[2]
sys.path = [tree] + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")]
import test_consolidate as tc
import lineage, lineage_store

def stores(ag):
    out = {}
    for n in ("_kind_known_dk", "_kdk_last", "_kind_offered_dk", "_kind_known_n", "_kind_known"):
        v = getattr(ag, n, None)
        if v is not None:
            out[n] = sorted((repr(k), repr(x)) for k, x in dict(v).items())
    st = getattr(ag, "_kind_store", None)
    if st is not None:
        for n in ("t2", "pairs"):
            out["store." + n] = sorted((repr(k), repr(x)) for k, x in dict(st.get(n, {})).items())
    sha = hashlib.sha256(json.dumps(out, sort_keys=True).encode()).hexdigest()
    return sha, {k: len(v) for k, v in out.items()}

if mode == "write":
    d, games = sys.argv[3], int(sys.argv[4])
    for _g in range(games):
        # a handle's suffix is random.choices when the agent seed is off (test_consolidate's
        # agent); the same seed per game makes the ON and OFF writes comparable
        random.seed(1000 + _g)
        tether, env, ag = tc.agent(lineage_dir=d)
        tc.steps(env, ag, 6)
        ag.end_run("cap")
        lineage.write(d, ag, "fake")
    print(json.dumps({"n": lineage_store.KEY_MEMO_N, "on": lineage_store._KEY_MEMO}))
else:
    ds = sys.argv[3:]
    res = None
    for d in ds:
        tether, env, ag = tc.agent(lineage_dir=d)
        res = stores(ag)
    print(json.dumps({"sha": res[0], "sizes": res[1], "n": lineage.LOAD_KEY_MEMO_N,
                      "on": lineage._LOAD_KEY_MEMO}))
'''


def _run(mode: str, *args: str, env_extra: dict | None = None) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               **(env_extra or {}))
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, HERE, mode, *args], env=env,
                         capture_output=True, text=True, timeout=1800, cwd=HERE)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def _files(d: str) -> dict:
    out = {}
    for f in sorted(os.listdir(d)):
        p = os.path.join(d, f)
        if os.path.isfile(p) and not f.startswith("memory.db"):
            with open(p, "rb") as fh:
                out[f] = hashlib.sha256(fh.read()).hexdigest()
    con = sqlite3.connect(f"file:{os.path.join(d, 'memory.db')}?mode=ro", uri=True)
    try:
        out["memory.db:iterdump"] = hashlib.sha256("\n".join(con.iterdump()).encode()).hexdigest()
    finally:
        con.close()
    return out


def plant() -> None:
    sys.path.insert(0, HERE)
    import lineage_store as ls
    vals = [[1], [True], [1.0], (1,), [1], [True, 1.0], [1, True]]
    was = ls._KEY_MEMO
    try:
        ls._KEY_MEMO = True
        j = ls._key_memo()
        got = [j(v) for v in vals]
    finally:
        ls._KEY_MEMO = was
    want = [ls._j(v) for v in vals]
    assert got == want, (got, want)
    bad: dict = {}

    def j_value(v):                     # the defect the ruling names: keyed on the value
        k = tuple(v)
        if k not in bad:
            bad[k] = ls._j(v)
        return bad[k]
    wrong = [j_value(v) for v in vals]
    assert wrong != want, "the plant cannot see a value-keyed memo"
    print(f"(1) the type plant: the memo gives {got[:3]} (each its fresh string); a "
          f"value-keyed memo gives {wrong[:3]}")


def main() -> None:
    plant()
    tmp = tempfile.mkdtemp()
    a, b, c, b2 = (os.path.join(tmp, x) for x in ("on", "off", "one", "off2"))
    for x in (a, b, c, b2):
        os.makedirs(x)
    on = _run("write", a, "2", env_extra={"TETHER_STORE_KEY_MEMO": "1"})
    off = _run("write", b, "2", env_extra={"TETHER_STORE_KEY_MEMO": "0"})
    _run("write", b2, "2", env_extra={"TETHER_STORE_KEY_MEMO": "0"})
    assert _files(b) == _files(b2), "CONTROL: two OFF writes differ, so (2) cannot read W1"
    assert on["on"] is True and off["on"] is False
    assert on["n"]["hit"] > 0, f"PRECONDITION: the ON writes reused nothing: {on['n']}"
    fa, fb = _files(a), _files(b)
    assert fa == fb, [k for k in set(fa) | set(fb) if fa.get(k) != fb.get(k)][:5]        # (2)
    print(f"(2) two games written ON and OFF: {len(fa) - 1} files byte-identical and "
          f"memory.db's dump identical; the ON writes reused {on['n']['hit']} encodings "
          f"({on['n']['bypass']} bypassed)")
    l_on = _run("load", a, env_extra={"TETHER_LOAD_KEY_MEMO": "1"})
    l_off = _run("load", a, env_extra={"TETHER_LOAD_KEY_MEMO": "0"})
    l_chk = _run("load", a, env_extra={"TETHER_LOAD_KEY_MEMO": "1",
                                       "TETHER_LOAD_KEY_MEMO_CHECK": "1"})
    assert l_on["n"]["hit"] > 0, f"PRECONDITION: the ON load reused nothing: {l_on['n']}"
    assert l_on["sha"] == l_off["sha"] == l_chk["sha"], (l_on, l_off, l_chk)             # (3)
    assert l_chk["n"]["disagree"] == 0 and l_chk["n"]["agree"] > 0, l_chk["n"]
    print(f"(3) the lineage loaded ON, OFF and ON+CHECK: carried stores equal {l_on['sizes']}; ON "
          f"reused {l_on['n']['hit']} decodes; CHECK {l_chk['n']['agree']} agree, 0 disagree")
    _run("write", c, "1", env_extra={"TETHER_STORE_KEY_MEMO": "1"})
    two = _run("load", c, a, env_extra={"TETHER_LOAD_KEY_MEMO": "1"})
    assert two["sha"] == l_on["sha"], (two, l_on)                                        # (4)
    print("(4) a second load in one process (a one-game lineage, then the two-game one) equals the "
          "two-game lineage loaded alone")
    print("test_store_key_memo: pass")


if __name__ == "__main__":
    main()
