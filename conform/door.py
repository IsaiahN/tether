"""M7, THE ONE DOOR (Isaiah 2026-10-24 08:30 "one service that fetches and stores data"; the
reviewer 08:49, 08:56, 08:58): outside the door set, no module opens, reads, writes, copies or
moves a knowledge file -- the library, the learned store (lineage saves, memory.db, library=
saves) -- or connects sqlite to one, or calls today's learned backends (lineage, lineage_store)
directly. A static read of every non-test .py: an I/O call whose source text names a knowledge
token, or a name that is TAINTED (assigned from such an expression, per function, to a fixpoint:
the indirect path `path = ROOT / name; path.read_text()`), is a violation unless its module is in
DOOR, every row with its reason. The table tightens to store.py (and library_runtime reading
through it) after step 5; that tightening is its own must-fail row then.
    python conform/door.py              # rc 0 clean, rc 1 with every violation printed
    python conform/door.py --must-fail  # planted violations in a scratch copy must fail it"""
from __future__ import annotations

import ast
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent

# THE DOOR, as data: module -> why it may touch knowledge files
DOOR = {
    "store.py": "the one door (steps 1-5)",
    "library/library_runtime.py": "the library's model; reads through store when importable",
    "lineage.py": "today's learned backend (gen_ / ak_ / idx_), folded in at steps 4-5",
    "lineage_store.py": "today's learned backend (memory.db), folded in at steps 4-5",
    "gamma.py": "today's learned backend (Gamma.save / load: library=), folded in at 4-5",
    # by ROLE: tools and checks that read GIVEN as tools, never as the agent
    "library/build_library.py": "the builder (runs standalone, the repo root not importable)",
    "conform/libagree.py": "a check over the GIVEN library",
    "compile_census.py": "a census tool",
    "instruments.py": "hashes LIBRARY_FILES for attribution",
    "conform/door.py": "this check (its planted violations)",
}
# by ROLE, whole folders: seat-side probes and launchers, never imported by the agent
DOOR_DIRS = {"harness/": "seat-side probes and launchers over the lineage, not the agent path"}
SKIP_DIRS = {".git", ".venv", "__pycache__", "runs", "tests"}    # tests: Isaiah 08:48
# the file I/O calls, by attribute or name
IO = {"open", "read_text", "read_bytes", "write_text", "write_bytes", "load", "dump", "connect",
      "copyfile", "copy2", "replace", "rename", "unlink", "glob", "rglob", "iterdir", "listdir",
      "save"}
# what names a knowledge file in an expression's own source text
TOKENS = ("library", "lineage", "memory.db", "atoms.json", "molecules.json", "readings.json",
          "index.json", "domains.json", "relations.json", "gen_", "ak_", "idx_", "bm_", "bs_",
          "LIB", "CORPUS_INDEX", "given.json", "frame.json", "grammar.json")
# a call THROUGH the door is the point: its receiver's root name is the door
DOOR_NAMES = {"store", "door", "library_runtime"}
# today's learned backends: ANY call into them from outside the door is a violation
BACKENDS = {"lineage", "lineage_store", "ls"}
# backend calls that touch no file, as data with the reason (every other backend call is flagged)
BACKEND_PURE = {
    "_ak_source": "the asked keys, read from the in-memory bound caches",
    "_ak_rows": "the times-asked counter re-keyed in memory",
    "_ak_class": "a slot's class, a string split",
}


class _Src:
    """Source segments in O(1) per node: line starts precomputed (ast.get_source_segment
    rescans the file per call, 2.5 min on tether.py)."""

    def __init__(self, src: str):
        self.src = src
        self.starts = [0] + [i + 1 for i, c in enumerate(src) if c == "\n"]

    def seg(self, n: ast.AST) -> str:
        if getattr(n, "end_lineno", None) is None:
            return ""
        a = self.starts[n.lineno - 1] + n.col_offset
        b = self.starts[n.end_lineno - 1] + n.end_col_offset
        return self.src[a:b]


def _ids(seg: str) -> set[str]:
    return set(re.findall(r"[A-Za-z_]\w*", seg))


def _callee(n: ast.Call) -> str | None:
    return n.func.attr if isinstance(n.func, ast.Attribute) else getattr(n.func, "id", None)


def _root(n: ast.Call) -> str | None:
    x = n.func
    while isinstance(x, (ast.Attribute, ast.Call, ast.Subscript)):
        x = x.value if isinstance(x, (ast.Attribute, ast.Subscript)) else x.func
    return x.id if isinstance(x, ast.Name) else None


def _own(body: list) -> list:
    """The nodes of a scope's body, nested function and class bodies excluded (their own
    scopes)."""
    out, todo = [], list(body)
    while todo:
        n = todo.pop()
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        out.append(n)
        todo.extend(ast.iter_child_nodes(n))
    return out


def _taint(nodes: list, s: _Src, seed: set[str]) -> set[str]:
    pairs = []
    for n in nodes:
        if isinstance(n, (ast.Assign, ast.AnnAssign)) and n.value is not None:
            tg = n.targets if isinstance(n, ast.Assign) else [n.target]
            names = {t.id for t in tg if isinstance(t, ast.Name)}
            if names:
                seg = s.seg(n.value)
                pairs.append((names, any(t in seg for t in TOKENS), _ids(seg)))
    bad = set(seed) | {x for names, tok, _ in pairs if tok for x in names}
    grew = True
    while grew:
        grew = False
        for names, _tok, ids in pairs:
            if not names <= bad and ids & bad:
                bad |= names
                grew = True
    return bad


def _check(nodes: list, s: _Src, bad: set[str], rel: str, out: list) -> None:
    for n in nodes:
        if not isinstance(n, ast.Call):
            continue
        fn, rt = _callee(n), _root(n)
        if rt in DOOR_NAMES:
            continue
        seg = s.seg(n)
        if rt in BACKENDS and isinstance(n.func, ast.Attribute) and fn not in BACKEND_PURE:
            out.append(f"{rel}:{n.lineno}: {rt}.{fn}(...) outside the door: {seg[:110]!r}")
            continue
        if fn not in IO:
            continue
        hit = [t for t in TOKENS if t in seg] + sorted(_ids(seg) & bad)
        if hit:
            out.append(f"{rel}:{n.lineno}: {fn}(...) names {hit}: {seg[:110]!r}")


def scan(rel: str, src: str, out: list) -> None:
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        out.append(f"{rel}: unparsed ({e})")
        return
    s = _Src(src)
    top = _own(tree.body)
    mod_bad = _taint(top, s, set())
    _check(top, s, mod_bad, rel, out)
    for f in ast.walk(tree):
        if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            mine = _own(f.body)
            _check(mine, s, _taint(mine, s, mod_bad), rel, out)


def violations(root: Path) -> list[str]:
    out: list[str] = []
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if not f.endswith(".py"):
                continue
            rel = Path(dirpath, f).relative_to(root).as_posix()
            if rel in DOOR or any(rel.startswith(d) for d in DOOR_DIRS):
                continue
            scan(rel, Path(dirpath, f).read_text(encoding="utf-8", errors="replace"), out)
    return sorted(out, key=lambda x: (x.split(":")[0],
                                      int(x.split(":")[1]) if x.split(":")[1].isdigit() else 0))


PLANTED = {
    "planted_direct.py": ('import json\n'
                          'X = json.load(open("library/atoms.json", encoding="utf-8"))\n'),
    "planted_indirect.py": ("from pathlib import Path\nROOT = Path(__file__).parent / 'library'\n"
                            "def f(name):\n    path = ROOT / name\n    return path.read_text()\n"),
    "planted_backend.py": "import lineage\ndef f(d, ag):\n    return lineage.load(d, ag)\n",
}


def must_fail() -> None:
    """Planted violations in a scratch copy -- a direct path, an indirect one through a tainted
    name, a backend call -- must each FAIL the check (occasions > 0)."""
    with tempfile.TemporaryDirectory() as d:
        dst = Path(d) / "tree"
        shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns(".git", ".venv", "runs",
                                                                  "__pycache__"))
        for name, text in PLANTED.items():
            (dst / name).write_text(text, encoding="utf-8")
        v = violations(dst)
        for name in PLANTED:
            got = [x for x in v if x.startswith(name)]
            assert got, f"M7 must-fail: the planted {name} was not caught"
            print(f"door --must-fail: {name} caught: {got[0][:110]}")


if __name__ == "__main__":
    if "--must-fail" in sys.argv:
        must_fail()
        sys.exit(0)
    v = violations(ROOT)
    for x in v:
        print("  ", x)
    print(f"door: {len(v)} violation(s) outside the door set ({len(DOOR)} modules, "
          f"{len(DOOR_DIRS)} folders)")
    sys.exit(1 if v else 0)
