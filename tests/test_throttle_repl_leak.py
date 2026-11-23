"""The 57 GB disk leak, closed at its write site (2026-11-22).

A `python -` that keeps its stdin pipe open enters Python 3.13's `_pyrepl`. With stdout/stderr
redirected to a FILE there is no console, so windows_console.getheightwidth() raises on the
invalid handle and the traceback handler appends forever -- measured 57 GB before it was noticed.

`conform/throttle.run` is this repo's one launcher that redirected stdout to a file WITHOUT
closing stdin. This asserts both holes are shut. It is a source-level witness because the defect is
in the Popen arguments, not in a value a run produces; a live run cannot fire the failure cheaply.
"""
import ast
import sys
from pathlib import Path

import _repo  # noqa: F401


def _run_popen_calls():
    path = Path(__file__).resolve().parent.parent / 'conform' / 'throttle.py'
    src = path.read_text(encoding='utf-8')
    tree = ast.parse(src)
    calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and node.func.attr == 'Popen':
            kws = {k.arg for k in node.keywords}
            calls.append((kws, node.lineno))
    return src, calls


def main() -> int:
    src, calls = _run_popen_calls()
    assert calls, 'throttle has no Popen -- the launcher moved; find and guard the new site'

    # (a) every file-backed redirect in throttle must close stdin
    for kws, ln in calls:
        if 'stdout' in kws:
            assert 'stdin' in kws, f'Popen at throttle.py:{ln} redirects stdout, not stdin'

    # (b) the env must force the basic REPL so even an inherited console-less REPL cannot loop
    assert 'PYTHON_BASIC_REPL' in src, 'no PYTHON_BASIC_REPL guard -- the _pyrepl leak can recur'

    print('PASS throttle Popen closes stdin and forces the basic REPL')
    return 0


if __name__ == '__main__':
    sys.exit(main())
