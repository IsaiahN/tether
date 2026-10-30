"""4d: move the root's test_*.py into tests/ (git mv), give each the repo root, and fix every reference. One-shot; it
refuses to run twice (tests/_repo.py must not exist). argv: repo"""
import re
import subprocess
import sys
from pathlib import Path

R = Path(sys.argv[1])
T = R / "tests"
assert not (T / "_repo.py").exists(), "already migrated"
names = sorted(p.name for p in R.glob("test_*.py"))
assert len(names) == 148, len(names)

(T / "_repo.py").write_text(
    '"""The repo root on sys.path for a test run from tests/ (4d; the reviewer 2026-10-22 04:03, 07:40). Every\n'
    'test imports this first; ROOT is the repo root, where the agent\'s modules, harness/, conform/ and\n'
    'environment_files/ live."""\n'
    "import os\nimport sys\n\n"
    "ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n"
    "if ROOT not in sys.path:\n    sys.path.insert(0, ROOT)\n", encoding="utf-8", newline="\n")
subprocess.run(["git", "mv", *names, "tests/"], cwd=R, check=True)

GEN = [  # every form that meant "the folder this test sits in", which was the repo root
    ("os.path.dirname(os.path.abspath(__file__))", "_repo.ROOT"),
    ("pathlib.Path(__file__).resolve().parent", "pathlib.Path(_repo.ROOT)"),
    ("Path(__file__).resolve().parent", "Path(_repo.ROOT)"),
    ("pathlib.Path(__file__).parent", "pathlib.Path(_repo.ROOT)"),
    ("Path(__file__).parent", "Path(_repo.ROOT)"),
]
KEEP = {("test_gate.py", "    here = pathlib.Path(__file__).parent\n    env = {k: v for k, v in os.environ.items()")}
CHILD_OLD = "sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])"
CHILD_NEW = ("sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])\n"
             "sys.path.insert(1, os.path.join(sys.argv[1], \"tests\"))")
counts = {}
for n in names:
    p = T / n
    s = p.read_text(encoding="utf-8")
    raw = s
    keep_spans = []
    for f, frag in KEEP:
        if f == n and frag in s:
            s = s.replace(frag, "\0KEEP\0")
            keep_spans.append(frag)
    k = 0
    for old, new in GEN:
        k += s.count(old)
        s = s.replace(old, new)
    for frag in keep_spans:
        s = s.replace("\0KEEP\0", frag, 1)
    if CHILD_OLD in s:
        s = s.replace(CHILD_OLD, CHILD_NEW)
        k += 1
    # the bootstrap: one import, the first import of the module (after `from __future__` if any)
    lines = s.split("\n")
    i = next(j for j, ln in enumerate(lines) if re.match(r"(import |from )", ln))
    if lines[i].startswith("from __future__"):
        i += 1
        while i < len(lines) and lines[i].strip() == "":
            i += 1
    lines.insert(i, "import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)")
    s = "\n".join(lines)
    # usage lines in docstrings: "python test_x.py" -> "python tests/test_x.py"
    s = re.sub(r"(python(?:\.exe)?(?: -B)? )(" + re.escape(n) + r")", r"\1tests/\2", s)
    counts[n] = k
    assert s != raw
    p.write_text(s, encoding="utf-8", newline="\r\n" if "\r\n" in raw else "\n")

print("moved", len(names), "; path rewrites in", sum(1 for v in counts.values() if v), "files,", sum(counts.values()),
      "sites")
