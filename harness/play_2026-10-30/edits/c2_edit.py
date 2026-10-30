"""4d-x's edits, each an exact replacement asserted to occur once. argv: repo"""
import sys
from pathlib import Path

R = Path(sys.argv[1])


def rep(rel, old, new):
    p = R / rel
    s = p.read_bytes().decode("utf-8")
    assert s.count(old) == 1, (rel, old, s.count(old))
    p.write_bytes(s.replace(old, new).encode("utf-8"))
    print("edited", rel)


rep("harness/mem_store/e4_stream.py", '        if end == "win":\n            ending = "win"\n',
    "        if end == ledger.WIN:\n            ending = ledger.WIN\n")
rep("harness/game_one.py", 'if self.env.terminal() == "game_win":', "if self.env.terminal() == ledger.WIN:")
rep("harness/game_one.py", "import arc_holdout  # noqa: E402\nimport tether  # noqa: E402\n",
    "import arc_holdout  # noqa: E402\nimport ledger  # noqa: E402\nimport tether  # noqa: E402\n")
