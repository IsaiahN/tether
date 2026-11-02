"""NO GAME-SPECIFIC CODE (Isaiah 2026-11-01 23:09, "keep stuff applicable to any game"; the reviewer
r751): the shipped modules -- the agent's own import set, read from sys.modules after a fake run,
never the harness, kaggle, conform or tests -- carry no game id ([a-z]{2}[0-9]{2}), no ACTION<n>
literal and none of the solution coordinates measured today, in CODE. Read with the tokenizer, so
a comment or a docstring (which cite measurements) is exempt and a string in code is not. The
must-fail: a code line naming a game id fires it.

    python tests/test_no_game_specific.py
"""
from __future__ import annotations

import io
import os
import re
import sys
import tokenize

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = re.compile(r"(?<![A-Za-z0-9_])[a-z]{2}[0-9]{2}(?![A-Za-z0-9_])")
ACT = re.compile(r"(?<![A-Za-z0-9_])ACTION[0-9](?![0-9])")
COORDS = {(4, 32), (58, 32), (30, 16), (1, 8)}      # r751: the solution cells measured today
SKIP = ("tests", "harness", "kaggle", "conform")
# exemptions as data, each with its reason (a table can be pinned; logic widens quietly)
EXEMPT = {("interface.py", "ACTION"): "below the seam (r727): the interface is where button names "
                                      "live (POSITIONED, 2026-09-28)",
          ("arc_holdout.py", "game"): "the seat's local-run defaults (play / controlled / __main__ "
                                      "default to one game), read by no agent decision"}


def shipped() -> list[str]:
    import arc_holdout
    from test_entry import FakeWrapper
    _env, ag, *_ = arc_holdout.wire(FakeWrapper(), "fake")
    for _ in range(3):
        ag.step()
    out = []
    for m in list(sys.modules.values()):
        f = getattr(m, "__file__", None) or ""
        f = os.path.abspath(f)
        rel = os.path.relpath(f, ROOT) if f.startswith(ROOT) else None
        if rel and rel.endswith(".py") and rel.split(os.sep)[0] not in SKIP \
                and not rel.startswith("."):
            out.append(rel)
    return sorted(set(out))


def hits(src: str) -> list[tuple[int, str]]:
    out, toks = [], list(tokenize.generate_tokens(io.StringIO(src).readline))
    prev_doc = True                                  # a string first in a block is a docstring
    for i, t in enumerate(toks):
        if t.type == tokenize.STRING:
            doc = prev_doc
            if not doc and GAME.search(t.string):
                out.append((t.start[0], "game", t.string[:60]))
            if not doc and ACT.search(t.string):
                out.append((t.start[0], "ACTION", t.string[:60]))
        elif t.type == tokenize.NAME and GAME.fullmatch(t.string):
            out.append((t.start[0], "game", t.string))
        elif t.type == tokenize.OP and t.string == "(" and i + 4 < len(toks):
            a, c, b, e = toks[i + 1], toks[i + 2], toks[i + 3], toks[i + 4]
            if (a.type == b.type == tokenize.NUMBER and c.string == "," and e.string == ")"
                    and a.string.isdigit() and b.string.isdigit()
                    and (int(a.string), int(b.string)) in COORDS):
                out.append((t.start[0], "coord", f"({a.string}, {b.string})"))
        if t.type not in (tokenize.NL, tokenize.NEWLINE, tokenize.COMMENT, tokenize.INDENT,
                          tokenize.DEDENT):
            prev_doc = t.type == tokenize.OP and t.string == ":" or (
                t.type == tokenize.STRING and prev_doc)
        elif t.type in (tokenize.NEWLINE,) and toks[i - 1].type == tokenize.STRING and prev_doc:
            prev_doc = True
    return out


def main():
    mods = shipped()
    assert len(mods) >= 10 and "tether.py" in mods, ("occasions: the import set", mods)
    bad = {}
    for rel in mods:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
            h = [x for x in hits(fh.read()) if (rel, x[1]) not in EXEMPT]
        if h:
            bad[rel] = h[:5]
    assert not bad, ("game-specific literals in shipped code", bad)
    must = hits('x = 1\nif game == "lp85":\n    y = ("ACTION6", (4, 32))\n')
    assert len(must) == 3, ("must-fail: a code line naming a game id fires", must)
    assert not hits('"""lp85 cleared at (4, 32) with ACTION6"""\n# vc33 at (30, 16)\nx = 1\n'), \
        "a docstring and a comment are exempt"
    print(f"test_no_game_specific: {len(mods)} shipped modules clean ({', '.join(mods)}); "
          f"the must-fail fires 3 of 3")


if __name__ == "__main__":
    main()
