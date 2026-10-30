import sys
from pathlib import Path

p = Path(sys.argv[1]) / "tests" / "_repo.py"
s = p.read_bytes().decode("utf-8")
old = ('environment_files/ live there. The root and tests/ also go on PYTHONPATH, so a "python -c" child (cwd the\n'
       'root) still imports test_entry and its siblings; a "-I" child ignores it, as test_entry\'s isolation check needs."""\n')
new = ('environment_files/ live there. The root and tests/ also go on PYTHONPATH, so a "python -c"\n'
       'child (cwd the root) still imports test_entry and its siblings; a "-I" child ignores it, as\n'
       'test_entry\'s isolation check needs."""\n')
assert s.count(old) == 1
p.write_bytes(s.replace(old, new).encode("utf-8"))
print("ok")
