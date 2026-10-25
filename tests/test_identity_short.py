"""THE OFF IDENTITY WITH ITS CODE-PROVENANCE WITNESSES (the reviewer 2026-10-24 11:05 A; WATSON
ruling 2, 12:02; committed per 12:09): the same fixed FakeWrapper PLAIN probe (test_route_refuse's
PLAIN and child) in a BASE revision (git archive into a temp dir) and in this tree, every ledger row
compared by conform/identity_mod_rows.compare. STEPS 3 is the quick set (about 379 rows); STEPS 30
is the landing's full identity (about 4787 rows).
The arms row's code provenance moves by construction when code changes, so it is dropped by name,
and each dropped field has a witness that can fail:
  (ii) every non-code file under library/, in both trees, has the same git blob id (absent in both
       is equal, absent in one is different); library.db (a build output, ignored) is not a tree
       file. Must-fail: one byte of library/grammar.json -> RED naming that file, no child run.
  (iii) the project modules imported inside the child differ by EXACTLY the set the step states.
       Must-fail: `import cue_bridge` added to store.py -> RED, added ['cue_bridge.py', 'store.py'].
The switch lists are asserted equal, never dropped -- except by EXACTLY the arms this tree adds:
  (iv) --new-arms A,B (NEW_ARMS; the reviewer 2026-10-25 02:24, ruling (c)): no NEW_ARMS entry in
       the base's on/off; each named exactly once in this tree's; and the on/off differences ARE
       set(NEW_ARMS). Every failed clause is collected and named in one failure. Must-fails:
       NEW_ARMS empty -> RED on (3) alone; ['lineage._NOT_AN_ARM'] -> RED on (2) and (3).
--moved FILE (store step 3's landing only; WATSON ruling 9 A6): FILE names the moved and added
library files. (ii) skips exactly those, by name, printed with the count (a moved file's .dead-<UTC>
tombstone with it); a moved file must be on the base and gone from this tree (index.json, REPLACED,
is on both), an added one absent on the base. In the same process the run then holds the step's
two gates, and is RED unless both are green:
  I2 (A4) every moved file rebuilt from this tree's layout (library_runtime.old_files) equals the
     base's file read by `git show BASE_REV:library/<f>`, by VALUE and by git BLOB; a bytes-only
     difference is allowed only for a file named in BYTES_ONLY, with its reason printed.
  I4 each GIVEN loader's in-memory result (inherited.load, compile_term.readings, the
     library_runtime.Library's tables) equals the base tree's, including every dict's KEY ORDER.
    python tests/test_identity_short.py BASE_REV STEPS NEW_MODULES [--moved FILE] [--new-arms A,B]
"""
import io
import json
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

NOT_TREE = {"library/library.db", "library/library.db.part"}   # build outputs, .gitignore'd
# a file whose rebuild may differ from the base in bytes only, with the reason (A4)
BYTES_ONLY = {"orientation_draft.json": "a hand-written draft, not in the build's indent-1 form"}
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
LOADERS = r'''
import json, os, sys
sys.dont_write_bytecode = True
tree, out = sys.argv[1], sys.argv[2]
sys.path[:0] = [tree, os.path.join(tree, "library")]
os.chdir(tree)
import compile_term, inherited, library_runtime
lib = library_runtime.Library(os.path.join(tree, "library")).load()
got = {"inherited": inherited.load(), "readings": compile_term.readings(),
       "library": {a: getattr(lib, a) for a in ("seed", "readings", "by_reading", "by_affects",
                                                "ingredient_of", "runtime", "learnings")}}
with open(out, "w", encoding="utf-8") as fh:
    json.dump(got, fh, ensure_ascii=False, default=list)
print("loaded")
'''


def _blob(path: str) -> str | None:
    if not os.path.exists(path):
        return None
    with open(path, "rb") as fh:
        return instruments.Attribution.blob_id(fh.read())


def _data_files(tree: str) -> set:
    lib = os.path.join(tree, "library")
    if not os.path.isdir(lib):
        return set()
    return {f"library/{f}" for f in os.listdir(lib)
            if os.path.isfile(os.path.join(lib, f)) and not f.endswith(".py")} - NOT_TREE


def library(base: str, cur: str, moved: dict | None = None) -> None:
    moved = moved or {"moved": [], "added": []}
    skip = {f"library/{f}" for f in moved["moved"] + moved["added"]}
    tomb = {f for f in _data_files(cur)
            if any(f.startswith(f"library/{m}.dead-") for m in moved["moved"])}
    if skip:
        print(f"(ii) skips {len(skip)} moved/added file(s) by name: {sorted(skip)}"
              + (f"; and {len(tomb)} tombstone(s): {sorted(tomb)}" if tomb else ""))
    bad = []
    for f in sorted((_data_files(base) | _data_files(cur)) - skip - tomb):
        ids = [_blob(os.path.join(tr, f)) for tr in (base, cur)]
        print(f"library {f}: {ids[0]} / {ids[1]}")
        if ids[0] != ids[1]:
            bad.append(f)
    assert not bad, ("a library data file differs", bad)


def modules(base: str, cur: str, new: set) -> None:
    got = [set(t.child(t.PLAIN + MODS, tr, None, 1)) for tr in (base, cur)]
    print(f"modules: {len(got[0])} / {len(got[1])}, added {sorted(got[1] - got[0])}, "
          f"removed {sorted(got[0] - got[1])}")
    assert len(got[0]) > 20 and got[1] - got[0] == new and not got[0] - got[1], "module set"


def new_arms_arg(argv: list) -> list:
    """--new-arms A,B: the module-qualified arms this tree adds (NEW_ARMS); empty if absent."""
    if "--new-arms" not in argv:
        return []
    return [x for x in argv[argv.index("--new-arms") + 1].split(",") if x]


def arms_witness(b: dict, c: dict, new: list, label: str = "") -> None:
    """(iv) The switch lists differ by EXACTLY NEW_ARMS: never in the base, each once here."""
    on = [set(b.get("on") or ()), set(c.get("on") or ())]
    off = [set(b.get("off") or ()), set(c.get("off") or ())]
    where = {a: [x for x in ("on", "off") if a in (c.get(x) or ())] for a in new}
    print(f"arms{label}: ON {len(on[0])} / {len(on[1])}, OFF {len(off[0])} / {len(off[1])}, ON "
          f"diff {sorted(on[0] ^ on[1])}, OFF diff {sorted(off[0] ^ off[1])}; NEW_ARMS "
          f"{new}: {where}")
    failed = []                 # every clause checked; one failure naming all (the reviewer 02:42)
    if (on[0] | off[0]) & set(new):
        failed.append(f"(1) a NEW_ARMS entry is in the base: {sorted((on[0] | off[0]) & set(new))}")
    if not all(list(c.get("on") or ()).count(a) + list(c.get("off") or ()).count(a) == 1
               for a in new):
        failed.append(f"(2) a NEW_ARMS entry is not named exactly once here: {where}")
    diff = (on[0] ^ on[1]) | (off[0] ^ off[1])
    if diff != set(new):
        failed.append(f"(3) the switch lists differ by other than NEW_ARMS: {sorted(diff)} vs "
                      f"{new}")
    assert not failed, (f"arms witness{label}", failed)


def identity(base: str, cur: str, steps: int, new_arms: list) -> None:
    rows = [t.child(t.PLAIN, tr, None, steps)["rows"] for tr in (base, cur)]
    arms = [next(r["detail"] for r in rs if r["slot"] == "@run" and r["event"] == "arms")
            for rs in rows]
    arms_witness(arms[0], arms[1], new_arms)
    for a in arms:
        for k in DROP + ("on", "off"):
            a.pop(k, None)
    bad = compare(rows[0], rows[1], set())
    print(f"OFF identity: {len(rows[0])} base rows, {len(rows[1])} current, "
          f"{min(len(rows[0]), len(rows[1]))} compared, {len(bad)} differing"
          + "".join(f"\n  {x}" for x in bad[:20]))
    assert len(rows[0]) > 50 and not bad, ("OFF identity", len(bad))


def read_moved(path: str) -> dict:
    out: dict = {"moved": [], "added": []}
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.split("#", 1)[0].strip()
            if ln:
                kind, name = ln.split()
                out[kind].append(name)
    return out


def moved_present(base: str, cur: str, moved: dict) -> None:
    lib = [os.path.join(tr, "library") for tr in (base, cur)]
    for m in moved["moved"]:
        on_base, on_cur = (os.path.exists(os.path.join(x, m)) for x in lib)
        replaced = m == "index.json"
        assert on_base and (on_cur if replaced else not on_cur), (
            "a moved file is not on the base and gone from this tree", m, on_base, on_cur)
    for a in moved["added"]:
        assert not os.path.exists(os.path.join(lib[0], a)), ("an added file is on the base", a)
        assert os.path.exists(os.path.join(lib[1], a)), ("an added file is absent here", a)
    print(f"--moved: {len(moved['moved'])} moved (index.json replaced in place), "
          f"{len(moved['added'])} added")


def i2(rev: str, moved: dict) -> list:
    """Every moved file rebuilt from this tree's layout against `git show REV:library/<f>`."""
    sys.path.insert(0, os.path.join(ROOT, "library"))
    import library_runtime as lr
    new = lr.old_files(os.path.join(ROOT, "library"), moved["moved"])
    bad = []
    for m in moved["moved"]:
        raw = subprocess.run(["git", "-C", ROOT, "show", f"{rev}:library/{m}"],
                             capture_output=True, check=True).stdout
        base_v = raw.decode("utf-8") if m.endswith(".txt") else json.loads(raw)
        nv = new.get(m)
        value = nv == base_v
        nb = b"" if nv is None else (nv if m.endswith(".txt") else lr.dumps(nv)).encode("utf-8")
        blob = instruments.Attribution.blob_id(nb) == instruments.Attribution.blob_id(raw)
        why = "" if blob or not value else f"  (bytes only: {BYTES_ONLY.get(m, 'NO REASON')})"
        print(f"I2 {m}: value {'EQUAL' if value else 'DIFFERS'}, blob "
              f"{'EQUAL' if blob else 'differs'}{why}")
        if not value or (not blob and m not in BYTES_ONLY):
            bad.append(m)
    return bad


def _first_diff(a, b, path="") -> str:
    if type(a) is not type(b):
        return f"{path}: type {type(a).__name__} -> {type(b).__name__}"
    if isinstance(a, dict):
        if list(a) != list(b):
            i = next((i for i, (x, y) in enumerate(zip(a, b, strict=False)) if x != y),
                     min(len(a), len(b)))
            return f"{path}: key order/set differs at position {i} ({len(a)} vs {len(b)} keys)"
        for k in a:
            if a[k] != b[k]:
                return _first_diff(a[k], b[k], f"{path}.{k}")
    if isinstance(a, list) and a != b:
        if len(a) != len(b):
            return f"{path}: length {len(a)} -> {len(b)}"
        i = next(i for i, (x, y) in enumerate(zip(a, b, strict=True)) if x != y)
        return _first_diff(a[i], b[i], f"{path}[{i}]")
    return f"{path}: {str(a)[:120]} -> {str(b)[:120]}"


def i4(base: str, cur: str, scratch: str) -> list:
    """The GIVEN loaders' results, base tree against this one, compared WITH key order."""
    got = []
    for name, tree in (("base", base), ("current", cur)):
        out = os.path.join(scratch, f"loaders_{name}.json")
        r = subprocess.run([sys.executable, "-B", "-c", LOADERS, tree, out], capture_output=True,
                           text=True, cwd=tree, env={**os.environ, "PYTHONHASHSEED": "0"},
                           check=False)
        assert r.returncode == 0, r.stderr[-2000:]
        with open(out, encoding="utf-8") as fh:
            got.append(json.load(fh))
    bad = []
    for part in ("inherited", "readings", "library"):
        same = got[0][part] == got[1][part] and json.dumps(got[0][part]) == json.dumps(got[1][part])
        print(f"I4 {part}: {'EQUAL (values and key order)' if same else 'DIFFERS'}"
              + ("" if same else f" -- first: {_first_diff(got[0][part], got[1][part], part)}"))
        if not same:
            bad.append(part)
    return bad


if __name__ == "__main__":
    rev, steps = sys.argv[1], int(sys.argv[2])
    new = set(sys.argv[3].split(",")) if sys.argv[3] else set()
    moved = read_moved(sys.argv[sys.argv.index("--moved") + 1]) if "--moved" in sys.argv else None
    with tempfile.TemporaryDirectory() as d:
        base = os.path.join(d, "base")
        os.makedirs(base)
        tar = subprocess.run(["git", "-C", ROOT, "archive", rev], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(base, filter="data")
        print(f"base {rev}, current {ROOT}, STEPS {steps}, expected new modules {sorted(new)}")
        if moved:
            moved_present(base, ROOT, moved)
            gates = {"I2": i2(rev, moved), "I4": i4(base, ROOT, d)}
            assert not any(gates.values()), ("step (3)'s gates", gates)
        library(base, ROOT, moved)
        modules(base, ROOT, new)
        identity(base, ROOT, steps, new_arms_arg(sys.argv))
    print("identity_short: OK")
