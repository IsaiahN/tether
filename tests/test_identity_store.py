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
    python tests/test_identity_store.py BASE_REV MODE N [--self]   # lineage | library | absent
Must-fails (in scratch clones; plant lines in the commit that carries them): MF-2a
store.lineage_write passes game + "_mf"; MF-2b store.library_save writes to path + ".mf"; MF-3
store.read_json reads an absent file from another repo's library/."""
import io
import json
import os
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
PLAY = r'''
import json, os, sys
sys.dont_write_bytecode = True
tree, out, mode, n, which = sys.argv[1:6]
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
os.chdir(tree)
import arc_holdout
from test_entry import FakeWrapper
class Arc:
    def make(self, _game):
        return FakeWrapper()
kw = {"lineage": {"lineage_dir": os.path.join(out, "lineage")},
      "library": {"library": os.path.join(out, "lib.json")}, "absent": {}}[mode]
r = arc_holdout.play("fake", int(n), arc=Arc(), led_path=os.path.join(out, which + ".jsonl"), **kw)
with open(os.path.join(out, which + ".result.json"), "w", encoding="utf-8") as fh:
    json.dump(r, fh, default=str, sort_keys=True)
print("played")
'''


def _under_tmp(p: str) -> str:
    rp = os.path.realpath(p)
    assert os.path.commonpath([rp, TMP]) == TMP, ("not under the temp root", rp, TMP)
    return rp


def _child(tree: str, out: str, mode: str, n: int, which: str) -> None:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")
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
        return {t: sorted(map(repr, con.execute(f'SELECT * FROM "{t}"'))) for t in names}
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


def _rows(path: str) -> list:
    with open(path, encoding="utf-8") as fh:
        rows = [json.loads(x) for x in fh]
    for r in rows:
        if r.get("slot") == "@run" and r.get("event") == "arms":
            for k in DROP:
                r["detail"].pop(k, None)
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
        out = _under_tmp(os.path.join(d, "out"))
        seen: dict = {}
        for side, tree in (("base", base), ("current", cur)):
            os.makedirs(out)
            seen[side] = {}
            for which in plays:
                _child(tree, out, mode, n, which)
                seen[side][which] = {"rows": _rows(os.path.join(out, which + ".jsonl")),
                                     "files": _files(out, d)}
                with open(os.path.join(out, which + ".result.json"), encoding="utf-8") as fh:
                    seen[side][which]["result"] = json.load(fh)
                print(f"  {side} {which}: {len(seen[side][which]['rows'])} rows, files "
                      f"{sorted(seen[side][which]['files'])}, {time.time() - T0:.0f} s", flush=True)
            shutil.move(out, os.path.join(d, f"out_{side}"))
        bad = []
        for which in plays:
            b, c = seen["base"][which], seen["current"][which]
            rbad = compare(b["rows"], c["rows"], set())
            print(f"{which}: rows {len(b['rows'])} / {len(c['rows'])}, {len(rbad)} differing"
                  + "".join(f"\n    {x}" for x in rbad[:20]))
            bad += [f"{which} rows: {x}" for x in rbad]
            for k in sorted(set(b["result"]) | set(c["result"])):
                if b["result"].get(k) != c["result"].get(k):
                    bv = json.dumps(b["result"].get(k), default=str)[:600]
                    cv = json.dumps(c["result"].get(k), default=str)[:600]
                    print(f"  {which} result[{k!r}]: {bv}\n      -> {cv}")
                    bad.append(f"{which} result {k}")
            for f in sorted(set(b["files"]) | set(c["files"])):
                if b["files"].get(f) != c["files"].get(f):
                    bv, cv = b["files"].get(f), c["files"].get(f)
                    if isinstance(bv, dict) and isinstance(cv, dict):
                        diff = sorted(t for t in set(bv) | set(cv) if bv.get(t) != cv.get(t))
                        print(f"  {which} file {f}: tables differing {diff}")
                    else:
                        print(f"  {which} file {f}: {bv} -> {cv}")
                    bad.append(f"{which} file {f}")
        assert len(seen["base"][plays[0]]["rows"]) > 50, "too few rows to compare"
        assert not bad, ("identity_store: differences", bad[:20])
    print(f"identity_store: OK ({mode}, N {n}{', self' if self_check else ''}, "
          f"{time.time() - T0:.0f} s)")


if __name__ == "__main__":
    main()
