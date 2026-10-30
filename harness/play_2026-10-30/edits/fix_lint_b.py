import sys
from pathlib import Path

sys.dont_write_bytecode = True
root = Path(sys.argv[1])


def edit(rel, pairs):
    p = root / rel
    s = p.read_text(encoding="utf-8")
    crlf = "\r\n" in s
    s = s.replace("\r\n", "\n")
    for a, b in pairs:
        assert s.count(a) == 1, (rel, a[:80], s.count(a))
        s = s.replace(a, b)
    if crlf:
        s = s.replace("\n", "\r\n")
    p.write_bytes(s.encode("utf-8"))
    print("ok", rel)


edit("arc_holdout.py", [
    ('    """wire()\'s world half. (B) builds a fresh one on the SAME ResetGuard-wrapped wrapper: '
     "ArcWorld's\n    constructor takes the wrapper's observation_space, so a live wrapper is never "
     'reset by it."""\n',
     '    """wire()\'s world half. (B) builds a fresh one on the SAME ResetGuard-wrapped wrapper:\n'
     "    ArcWorld's constructor takes the wrapper's observation_space, so a live wrapper is never\n"
     '    reset by it."""\n'),
    ('    return False, (f"{os.path.relpath(mine[-1].filename, root)}:{mine[-1].lineno}" '
     'if mine else None)\n',
     '    site = f"{os.path.relpath(mine[-1].filename, root)}:{mine[-1].lineno}" if mine else None\n'
     '    return False, site\n'),
    ('        saved = part(checked_save, ag.gamma, library, env, game) if fault else '
     'ag.gamma.save(library)\n',
     '        saved = (part(checked_save, ag.gamma, library, env, game) if fault\n'
     '                 else ag.gamma.save(library))\n'),
])
edit("conform/arms.py", [
    ('"2026-10-22 15:13; the reviewer 15:17 (C3), (C4)): arc_holdout.step_or_recover, "\n'
     '                            "at play\'s',
     '"2026-10-22 15:13; the reviewer 15:17 (C3), (C4)): "\n'
     '                            "arc_holdout.step_or_recover, at play\'s'),
])
edit("tests/test_fault_recover.py", [
    ("import os\nimport shutil\nimport subprocess\n", "import os\nimport subprocess\n"),
    ('    print(f"  r1 two fresh agents from copies of the save on copies of the board: '
     '{r1[\'rows\']} rows "\n          f"equal, last calls',
     '    print(f"  r1 two fresh agents from copies of the save on copies of the board: "\n'
     '          f"{r1[\'rows\']} rows equal, last calls'),
])
