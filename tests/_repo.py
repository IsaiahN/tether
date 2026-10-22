"""The repo root on sys.path for a test run from tests/ (4d; the reviewer 2026-10-22 04:03, 07:40).
Every test imports this first. ROOT is the repo root: the agent's modules, harness/, conform/ and
environment_files/ live there. The root and tests/ also go on PYTHONPATH, so a "python -c"
child (cwd the root) still imports test_entry and its siblings; a "-I" child ignores it, as
test_entry's isolation check needs."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
_have = [p for p in os.environ.get("PYTHONPATH", "").split(os.pathsep) if p]
os.environ["PYTHONPATH"] = os.pathsep.join(
    [p for p in (ROOT, os.path.join(ROOT, "tests")) if p not in _have] + _have)
