"""THE OFF IDENTITY WITH ITS CODE-PROVENANCE WITNESSES (the reviewer 2026-10-24 11:05 A; WATSON
ruling 2, 12:02; committed per 12:09): the same fixed FakeWrapper PLAIN probe (test_route_refuse's
PLAIN and child) in a BASE revision (git archive into a temp dir) and in this tree, every ledger row
compared by conform/identity_mod_rows.compare. STEPS 3 is the quick set (about 379 rows); STEPS 30
is the landing's full identity (about 4787 rows).
The arms row's code provenance moves by construction when code changes, so it is dropped by name,
and each dropped field has a witness that can fail:
  (ii) per file of instruments.Attribution.LIBRARY_FILES, the blob id is equal in both trees
       (absent in both is equal, absent in one is different), library/library_runtime.py excepted
       (code, covered by its own diff). Must-fail: one byte of library/domains.json -> RED naming
       that file, no child run.
  (iii) the project modules imported inside the child differ by EXACTLY the set the step states.
       Must-fail: `import cue_bridge` added to store.py -> RED, added ['cue_bridge.py', 'store.py'].
The switch lists are asserted equal, never dropped.
    python tests/test_identity_short.py BASE_REV STEPS NEW_MODULES   # comma-separated, or ""
"""
import io
import os
import subprocess
import sys
import tarfile
import tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path[:0] = [ROOT, HERE, os.path.join(ROOT, "conform")]
from identity_mod_rows import compare  # noqa: E402

import instruments  # noqa: E402
import test_route_refuse as t  # noqa: E402

CODE_IN_LIBRARY = {"library/library_runtime.py"}    # code, covered by its own diff
DROP = ("blob_n_files", "dirty", "files_blob", "files_sha", "git_unknown", "head",  # tree ids
        "tree",
        "n_files",          # imported project modules: a new module moves it; witness (iii)
        "library_sha",      # hashes LIBRARY_FILES, library_runtime.py (code) in it; witness (ii)
        "library_blob",     # the same files as git blobs; witness (ii)
        "library_n_files")  # the count of those files; witness (ii) reads each one
MODS = ('\nimport os as _o, json as _j\n_r = _o.path.normcase(_o.path.abspath(tree)) + _o.sep\n'
        'print(_j.dumps(sorted(_o.path.relpath(f, tree) for m in list(sys.modules.values()) '
        'if isinstance(f := getattr(m, "__file__", None), str) and f.endswith(".py") '
        'and _o.path.normcase(_o.path.abspath(f)).startswith(_r) and ".venv" not in f)))\n')


def _blob(path: str) -> str | None:
    if not os.path.exists(path):
        return None
    with open(path, "rb") as fh:
        return instruments.Attribution.blob_id(fh.read())


def library(base: str, cur: str) -> None:
    bad = []
    for f in instruments.Attribution.LIBRARY_FILES:
        ids = [_blob(os.path.join(tr, f)) for tr in (base, cur)]
        print(f"library {f}: {ids[0]} / {ids[1]}")
        if f not in CODE_IN_LIBRARY and ids[0] != ids[1]:
            bad.append(f)
    assert not bad, ("a library data file differs", bad)


def modules(base: str, cur: str, new: set) -> None:
    got = [set(t.child(t.PLAIN + MODS, tr, None, 1)) for tr in (base, cur)]
    print(f"modules: {len(got[0])} / {len(got[1])}, added {sorted(got[1] - got[0])}, "
          f"removed {sorted(got[0] - got[1])}")
    assert len(got[0]) > 20 and got[1] - got[0] == new and not got[0] - got[1], "module set"


def identity(base: str, cur: str, steps: int) -> None:
    rows = [t.child(t.PLAIN, tr, None, steps)["rows"] for tr in (base, cur)]
    arms = [next(r["detail"] for r in rs if r["slot"] == "@run" and r["event"] == "arms")
            for rs in rows]
    on = [set(a.get("on") or ()) for a in arms]
    off = [set(a.get("off") or ()) for a in arms]
    print(f"arms: ON {len(on[0])} / {len(on[1])}, OFF {len(off[0])} / {len(off[1])}, ON diff "
          f"{sorted(on[0] ^ on[1])}, OFF diff {sorted(off[0] ^ off[1])}")
    assert on[0] == on[1] and off[0] == off[1], "the switch lists differ"
    for a in arms:
        for k in DROP + ("on", "off"):
            a.pop(k, None)
    bad = compare(rows[0], rows[1], set())
    print(f"OFF identity: {len(rows[0])} base rows, {len(rows[1])} current, "
          f"{min(len(rows[0]), len(rows[1]))} compared, {len(bad)} differing"
          + "".join(f"\n  {x}" for x in bad[:20]))
    assert len(rows[0]) > 50 and not bad, ("OFF identity", len(bad))


if __name__ == "__main__":
    rev, steps = sys.argv[1], int(sys.argv[2])
    new = set(sys.argv[3].split(",")) if sys.argv[3] else set()
    with tempfile.TemporaryDirectory() as d:
        tar = subprocess.run(["git", "-C", ROOT, "archive", rev], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        print(f"base {rev}, current {ROOT}, STEPS {steps}, expected new modules {sorted(new)}")
        library(d, ROOT)
        modules(d, ROOT, new)
        identity(d, ROOT, steps)
    print("identity_short: OK")
