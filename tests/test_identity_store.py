"""THE OFF IDENTITY ON THE STORE PATHS (step (1)'s landing; the reviewer 2026-10-24 12:26-12:34,
design approved with d1-d4): arc_holdout.play("fake", N) -- wire()'s lineage load, the boundary
write, the library= save and the lineage write, all through store -- in a BASE revision and in this
tree, each play in its own child (seeds pinned, TETHER_* cleared), compared play by play:
  lineage  play 1 into an empty lineage_dir, play 2 from it (cold -> warm)
  library  play 1 with library=<tmp>/lib.json absent, play 2 reading it (cold -> warm)
  absent   one play in copies of both trees WITHOUT library/, TETHER_LIBRARY_REQUIRED=0
Per play: the ledger rows (led_path) by identity_mod_rows.compare, the arms row's tree ids and
code provenance dropped by name as in test_identity_short (DROP); the play's returned dict; and
every file it wrote, by name and git blob id -- memory.db by its tables' rows, read immutable=1
from a copy. A field that differs by construction is PRINTED WHOLE and fails: a mask is added only
by name, on a ruling (c3). Every lineage_dir / library= / led_path is a fresh path under the temp
root, asserted and printed (c1). The whole run stops itself at CAP seconds with OVER-CAP (d1).
--self compares BASE against itself: the determinism control (d4), run before anything else.
THE SEED (WATSON ruling 4, 12:47): every play reads its seed from ONE record the test writes under
the temp root, {"slot": "@run", "event": "seed", "detail": {"seed": "0000000000000000",
"generation": 0, "seed_source": "birth"}}, through TETHER_SEED_FROM (the replay path, the seed arm
at its default ON). TETHER_AGENT_SEED=0 is the constant seed, under which gamma.draw_seed is None
and every minted handle's suffix is random; the replay's handles are blake2b(seed:name).
A differing ledger field prints its two values whole (P2).
    python tests/test_identity_store.py BASE_REV MODE N [--self]   # lineage | library | absent
Must-fails (in scratch clones; plant lines in the commit that carries them): MF-2a
store.lineage_write passes game + "_mf"; MF-2b store.library_save writes to path + ".mf"; MF-3
store.read_json reads an absent file from another repo's library/."""
import ast
import io
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tarfile
import tempfile
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path[:0] = [ROOT, HERE, os.path.join(ROOT, "conform")]
from identity_mod_rows import compare  # noqa: E402

import instruments  # noqa: E402
from test_identity_short import DROP  # noqa: E402

CAP, T0 = 600, time.time()
TMP = os.path.realpath(tempfile.gettempdir())
SEED: list = []          # the fixed seed record's path, written under the temp root in main()
SEED_ROW = {"slot": "@run", "event": "seed",
            "detail": {"seed": "0000000000000000", "generation": 0, "seed_source": "birth"}}
PLAY = r'''
import json, os, sys
sys.dont_write_bytecode = True
tree, out, mode, n, which = sys.argv[1:6]
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
os.chdir(tree)
import arc_holdout, cap
from test_entry import FakeWrapper
class Arc:
    def make(self, _game):
        return FakeWrapper()
agents, wire0 = [], arc_holdout.wire
def wire(*a, **k):                      # read-only: keeps each agent so its deadline is read
    got = wire0(*a, **k)
    agents.append(got[1])
    return got
arc_holdout.wire = wire
kw = {"lineage": {"lineage_dir": os.path.join(out, "lineage")},
      "library": {"library": os.path.join(out, "lib.json")}, "absent": {}}[mode]
r = arc_holdout.play("fake", int(n), arc=Arc(), led_path=os.path.join(out, which + ".jsonl"), **kw)
r["_witness"] = {"deadline": [a.deadline for a in agents], "cap_AT": cap.AT, "agents": len(agents)}
with open(os.path.join(out, which + ".result.json"), "w", encoding="utf-8") as fh:
    json.dump(r, fh, default=str, sort_keys=True)
print("played")
'''


# THE TIMING MASK, BY NAME (WATSON ruling 5, the reviewer 2026-10-24 13:00): wall seconds the store
# measures around its own writes. Applied ONLY when the play's witness reads deadline None and
# cap.AT None, because reserve_s IS read under a deadline.
ROW_MASK = (("end_path", "stored"),     # {s, sleep_s}: wall seconds of the end-path store
            ("end_path", "wall_s"),     # wall seconds of the end path
            ("end_path", "reserve_s"))  # the carried end_path.s; read by _think_until UNDER A
#                                         DEADLINE (lineage.py 973-976, tether.py 15939-15944)
STORE = ("persistence", "lineage", "store")
RESULT_MASK = (STORE + ("end_path",),            # {s, sleep_s}, the same wall seconds
               STORE + ("s_commit",),            # wall seconds of the commit
               STORE + ("s_fsync",),             # wall seconds of the fsync
               STORE + ("s_read",),              # wall seconds of the reads
               STORE + ("s_statements",),        # wall seconds of the statements
               STORE + ("sleep", "s_checkpoint"),   # wall seconds of the checkpoint
               STORE + ("sleep", "s_quick_check"))  # wall seconds of the quick check
DB_MASK = (("meta", "end_path"),)   # the meta row keyed 'end_path': the same {s, sleep_s}


def _witness(res: dict, label: str) -> None:
    w = res.get("_witness") or {}
    print(f"  {label} deadline: {w.get('deadline')}, cap.AT: {w.get('cap_AT')}, "
          f"agents {w.get('agents')}", flush=True)
    assert w.get("agents") and all(x is None for x in w["deadline"]) and w.get("cap_AT") is None, (
        "a deadline is set: the timing mask must not apply (WATSON ruling 5)", label, w)


def _mask_result(res: dict) -> dict:
    for path in RESULT_MASK:
        d = res
        for k in path[:-1]:
            d = d.get(k) if isinstance(d, dict) else None
        if isinstance(d, dict):
            d.pop(path[-1], None)
    return res


def _under_tmp(p: str) -> str:
    rp = os.path.realpath(p)
    assert os.path.commonpath([rp, TMP]) == TMP, ("not under the temp root", rp, TMP)
    return rp


def _child(tree: str, out: str, mode: str, n: int, which: str) -> None:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    # THE SEED FROM A FIXED RECORD (P1): TETHER_AGENT_SEED=0 is the constant seed, under which
    # gamma.draw_seed is None and every handle suffix is random; the replay path is reproducible
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_SEED_FROM=SEED[0])
    if mode == "absent":
        env["TETHER_LIBRARY_REQUIRED"] = "0"
    left = CAP - (time.time() - T0)
    try:
        r = subprocess.run([sys.executable, "-B", "-c", PLAY, tree, out, mode, str(n), which],
                           env=env, capture_output=True, text=True, timeout=max(left, 1), cwd=tree,
                           stdin=subprocess.DEVNULL, check=False)
    except subprocess.TimeoutExpired:
        print(f"identity_store OVER-CAP: {which} in {tree} passed {CAP} s; stopped", flush=True)
        sys.exit(3)
    assert r.returncode == 0, r.stderr[-3000:]


def _db_rows(path: str, scratch: str) -> dict:
    copy = os.path.join(scratch, "memory.copy.db")
    shutil.copyfile(path, copy)
    con = sqlite3.connect(f"file:{copy}?immutable=1", uri=True)
    try:
        names = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table' "
                                           "ORDER BY name")]
        masked = {t: {k for tt, k in DB_MASK if tt == t} for t in names}
        return {t: sorted(repr(r) for r in con.execute(f'SELECT * FROM "{t}"')
                          if not (r and r[0] in masked[t])) for t in names}
    finally:
        con.close()


def _files(out: str, scratch: str) -> dict:
    got = {}
    for dp, _dirs, fs in os.walk(out):
        for f in fs:
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, out).replace("\\", "/")
            if rel.endswith(".jsonl") or rel.endswith(".result.json"):
                continue                       # the ledger and result, compared on their own
            if f == "memory.db":
                got[rel] = _db_rows(p, scratch)
            elif not f.endswith(("-shm", "-wal")):
                with open(p, "rb") as fh:
                    got[rel] = instruments.Attribution.blob_id(fh.read())
    return got


def _leaves(b, c, path: str) -> list:
    """The differing leaves of two JSON values, each with its key path (P2: values whole)."""
    if isinstance(b, dict) and isinstance(c, dict):
        return [x for k in sorted(set(b) | set(c), key=str) if b.get(k) != c.get(k)
                for x in _leaves(b.get(k), c.get(k), f"{path}.{k}")]
    return [(path, b, c)]


def _library_state(path: str) -> str | None:
    """The @run arms row's library state ("present", "absent (ablation)", ...) as written."""
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            r = json.loads(ln)
            if r.get("slot") == "@run" and r.get("event") == "arms":
                return (r.get("detail") or {}).get("library")
    return None


def _rows(path: str) -> list:
    with open(path, encoding="utf-8") as fh:
        rows = [json.loads(x) for x in fh]
    for r in rows:
        if r.get("slot") == "@run" and r.get("event") == "arms":
            for k in DROP:
                r["detail"].pop(k, None)
        for ev, f in ROW_MASK:
            if r.get("event") == ev and isinstance(r.get("detail"), dict):
                r["detail"].pop(f, None)
    return rows


def _tree_copy(src_rev: str | None, src_dir: str | None, dst: str, mode: str) -> str:
    os.makedirs(dst)
    if src_rev is not None:
        tar = subprocess.run(["git", "-C", ROOT, "archive", src_rev], capture_output=True,
                             check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(dst, filter="data")
    else:
        shutil.copytree(src_dir, dst, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns(".git", ".venv", "runs", "__pycache__"))
    if mode == "absent":
        shutil.rmtree(os.path.join(dst, "library"))   # a copy under the temp root, never a tree
    return dst


def main() -> None:
    rev, mode, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
    self_check = "--self" in sys.argv
    assert mode in ("lineage", "library", "absent"), mode
    plays = ("cold", "warm") if mode != "absent" else ("one",)
    with tempfile.TemporaryDirectory() as d:
        d = _under_tmp(d)
        base = _tree_copy(rev, None, os.path.join(d, "base"), mode)
        if self_check:
            cur = _tree_copy(rev, None, os.path.join(d, "cur"), mode)
        elif mode == "absent":
            cur = _tree_copy(None, ROOT, os.path.join(d, "cur"), mode)
        else:
            cur = ROOT
        if mode == "absent":
            assert not os.path.exists(os.path.join(base, "library"))
            assert not os.path.exists(os.path.join(cur, "library"))
        print(f"base {rev} at {base}\ncurrent {'(self) ' if self_check else ''}{cur}\n"
              f"MODE {mode}, N {n}, plays {plays}, temp root {TMP}", flush=True)
        # ONE output path for both trees, run in turn, so no temp path differs by construction
        SEED.append(_under_tmp(os.path.join(d, "seed.jsonl")))
        with open(SEED[0], "w", encoding="utf-8") as fh:
            fh.write(json.dumps(SEED_ROW) + "\n")
        print(f"seed record {SEED[0]}: {json.dumps(SEED_ROW)}", flush=True)
        out = _under_tmp(os.path.join(d, "out"))
        seen: dict = {}
        for side, tree in (("base", base), ("current", cur)):
            os.makedirs(out)
            seen[side] = {}
            for which in plays:
                _child(tree, out, mode, n, which)
                with open(os.path.join(out, which + ".result.json"), encoding="utf-8") as fh:
                    res = json.load(fh)
                _witness(res, f"{side} {which}")      # before any mask applies (ruling 5)
                state = _library_state(os.path.join(out, which + ".jsonl"))
                print(f"  {side} {which} @run library: {state!r}", flush=True)
                if mode == "absent":                  # the ablation, read from each tree's header
                    assert state == "absent (ablation)", (side, which, state)
                seen[side][which] = {"rows": _rows(os.path.join(out, which + ".jsonl")),
                                     "files": _files(out, d), "result": _mask_result(res)}
                print(f"  {side} {which}: {len(seen[side][which]['rows'])} rows, files "
                      f"{sorted(seen[side][which]['files'])}, {time.time() - T0:.0f} s", flush=True)
            shutil.move(out, os.path.join(d, f"out_{side}"))
        bad = []
        for which in plays:
            b, c = seen["base"][which], seen["current"][which]
            rbad = compare(b["rows"], c["rows"], set())
            for x in rbad:              # P2: each differing field's two values, whole (D)
                m = re.match(r"seq (\d+) .*\['detail'\] (\[.*\])$", x)
                if m and int(m.group(1)) < min(len(b["rows"]), len(c["rows"])):
                    i, fields = int(m.group(1)), ast.literal_eval(m.group(2))
                    for f in fields:
                        print(f"    seq {i} {f}: {b['rows'][i]['detail'].get(f)!r} -> "
                              f"{c['rows'][i]['detail'].get(f)!r}")
            print(f"{which}: rows {len(b['rows'])} / {len(c['rows'])}, {len(rbad)} differing"
                  + "".join(f"\n    {x}" for x in rbad[:20]))
            bad += [f"{which} rows: {x}" for x in rbad]
            for k in sorted(set(b["result"]) | set(c["result"])):
                if b["result"].get(k) != c["result"].get(k):
                    for path, bv, cv in _leaves(b["result"].get(k), c["result"].get(k), k):
                        print(f"  {which} result {path}: {json.dumps(bv, default=str)[:600]}"
                              f"\n      -> {json.dumps(cv, default=str)[:600]}")
                    bad.append(f"{which} result {k}")
            for f in sorted(set(b["files"]) | set(c["files"])):
                if b["files"].get(f) != c["files"].get(f):
                    bv, cv = b["files"].get(f), c["files"].get(f)
                    if isinstance(bv, dict) and isinstance(cv, dict):
                        diff = sorted(t for t in set(bv) | set(cv) if bv.get(t) != cv.get(t))
                        print(f"  {which} file {f}: tables differing {diff}")
                        for tb in diff:         # the rows themselves, each side's own (D)
                            only_b = sorted(set(bv.get(tb, ())) - set(cv.get(tb, ())))
                            only_c = sorted(set(cv.get(tb, ())) - set(bv.get(tb, ())))
                            for r in only_b[:10]:
                                print(f"      {tb} base only:    {r[:300]}")
                            for r in only_c[:10]:
                                print(f"      {tb} current only: {r[:300]}")
                    else:
                        print(f"  {which} file {f}: {bv} -> {cv}")
                    bad.append(f"{which} file {f}")
        assert len(seen["base"][plays[0]]["rows"]) > 50, "too few rows to compare"
        assert not bad, ("identity_store: differences", bad[:20])
    print(f"identity_store: OK ({mode}, N {n}{', self' if self_check else ''}, "
          f"{time.time() - T0:.0f} s)")


if __name__ == "__main__":
    main()
