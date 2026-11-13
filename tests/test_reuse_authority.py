"""H7's KEY FIX (step 10; r1849, the seat's 16:24 note): the reuse book counts HEADS (settled
terms by name, library entries); the idea walk scores CHAINS of atoms. Keyed by atom name,
authority scored almost nothing. Agent._reuse_head_names maps a chain to the heads whose own
atoms it starts with.

RA1  a chain starting with a head's atoms (translate . recolour) scores that head's paid
     contexts (2)
RA2  a chain that does not start with it scores 0
MF-RA1 the old keying (each atom's name): the same chain scores 0 -> RA1's score is lost -> RED
Seconds, no game.

    python tests/test_reuse_authority.py
"""
from __future__ import annotations

import sys
import types

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import arc_predict  # noqa: E402
import reuse  # noqa: E402
import tether  # noqa: E402
from gamma import Term  # noqa: E402


def main() -> int:
    held = {a.name: a for a in arc_predict.predict()}
    tr, rc = held["translate"], held["recolour"]
    head = Term((tr, rc))
    book = reuse.ReuseBook()
    for ctx in (("SELF", "K", "d1", "*"), ("BY:X", "K", "d1", "*")):
        book.note_chance(ctx, head.name)
        book.note_use(ctx, head.name, paid=True)
    ag = types.SimpleNamespace(_reuse=book,
                               gamma=types.SimpleNamespace(library={head.name: head}))
    names = tether.Agent._reuse_head_names(ag)
    score = book.authority(names)
    on = score((tr, rc, held["translate"]))
    off_chain = score((rc, tr))
    old = book.authority()((tr, rc, held["translate"]))
    print(f"  head {head.name}: contexts paid {book.contexts_paid(head.name)}")
    print(f"  keyed by heads: starts-with chain {on}, other chain {off_chain}; by atom names {old}")
    ok1, ok2 = on == book.contexts_paid(head.name) and on > 0, off_chain == 0
    print(f"RA1 the chain built on a paid head scores it: {'GREEN' if ok1 else 'RED'}")
    print(f"RA2 a chain not built on it scores 0: {'GREEN' if ok2 else 'RED'}")
    red = old == 0
    print(f"MF-RA1 the old atom-name keying scores it {old}: "
          f"{'RED (as required)' if red else 'GREEN'}")
    assert ok1 and ok2 and red
    print("reuse_authority: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
