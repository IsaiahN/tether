"""4d commit 1's three edits, each an exact replacement asserted to occur once. argv: repo"""
import sys
from pathlib import Path

R = Path(sys.argv[1])


def rep(rel, old, new):
    p = R / rel
    s = p.read_bytes().decode("utf-8")
    assert s.count(old) == 1, (rel, s.count(old))
    p.write_bytes(s.replace(old, new).encode("utf-8"))
    print("edited", rel)


BOOT = "import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)\n"
rep("tests/test_level_edge.py", "levels_completed raised\n" + BOOT + "from 0 to 1 at step CLEAR",
    "levels_completed raised\nfrom 0 to 1 at step CLEAR")
rep("tests/test_level_edge.py", "from __future__ import annotations\n\nimport json\n",
    "from __future__ import annotations\n\n" + BOOT + "import json\n")
rep("tests/test_ending_words.py", '    "test_ending_words.py": "this check names the words it forbids",',
    '    "tests/test_ending_words.py": "this check names the words it forbids",')
rep("tests/_repo.py",
    'environment_files/ live there."""\n',
    'environment_files/ live there. The root and tests/ also go on PYTHONPATH, so a "python -c" child (cwd the\n'
    'root) still imports test_entry and its siblings; a "-I" child ignores it, as test_entry\'s isolation check needs."""\n')
rep("tests/_repo.py", "    sys.path.insert(0, ROOT)\n",
    "    sys.path.insert(0, ROOT)\n"
    '_have = [p for p in os.environ.get("PYTHONPATH", "").split(os.pathsep) if p]\n'
    'os.environ["PYTHONPATH"] = os.pathsep.join(\n'
    '    [p for p in (ROOT, os.path.join(ROOT, "tests")) if p not in _have] + _have)\n')
