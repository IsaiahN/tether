"""(c), the dormant item written whole (the reviewer 2026-10-22 20:57): lineage.term_form and
lineage.dormant_items; write calls dormant_items; tether's arm. argv: tree root."""
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


edit("lineage.py", [
    ('''_BOUNDARY = armflag.arm("TETHER_LINEAGE_BOUNDARY", default=True)
''',
     '''_BOUNDARY = armflag.arm("TETHER_LINEAGE_BOUNDARY", default=True)
# (c) THE DORMANT ITEM WRITTEN WHOLE (the reviewer 2026-10-22 20:57): a boundary item holds live
# Terms (its want_terms copy), which enc has no form for, so one Term cost the generation the WHOLE
# boundary record. ON: each Term in it is written as its term-row record (dormant_items), the live
# and in-memory record untouched. OFF: the item refused and named, as before.
_DORMANT_TERM_FORM = armflag.arm("TETHER_DORMANT_TERM_FORM", default=True)
'''),
    ('''class Unencodable(TypeError):
''',
     '''def term_form(x: Any) -> Any:
    """x with each gamma.Term in it replaced by its term-row record, {"__term__": name, "atoms",
    "guard", "guard_ref", "operand", "operand_term"} (Fig 13 :130: a term carries the atoms it was
    built from). A RECORD, written by lineage.write only; nothing rebuilds a live Term from it."""
    if isinstance(x, gamma.Term):
        return {"__term__": x.name, "atoms": [a.name for a in x.atoms], "guard": x.guard,
                "guard_ref": x.guard_ref, "operand": x.operand,
                "operand_term": ([a.name for a in x.operand_term.atoms]
                                 if x.operand_term is not None else None)}
    if isinstance(x, dict):
        return {k: term_form(v) for k, v in x.items()}
    if isinstance(x, tuple):
        return tuple(term_form(v) for v in x)
    if isinstance(x, list):
        return [term_form(v) for v in x]
    if isinstance(x, (set, frozenset)) and any(isinstance(v, gamma.Term) for v in x):
        return {"__terms_of_set__": sorted((term_form(v) for v in x), key=repr)}
    return x


def dormant_items(items: list, start: int = 0) -> tuple[list, list]:
    """The write's dormant encoding: (encoded items, refused [{i, type}]). Under (c) a Term inside
    an item is written in its term-row form; anything else enc has no form for refuses the item,
    named."""
    out, refused = [], []
    for i, item in enumerate(items, start):
        try:
            out.append(enc(term_form(item) if _DORMANT_TERM_FORM else item))
        except Unencodable as e:
            refused.append({"i": i, "type": e.type})
    return out, refused


class Unencodable(TypeError):
'''),
    ('''    dormant, refused = [], []
    d0, e0 = marks.get("dormant", 0), marks.get("evidence", 0)
    dormant_all = getattr(ag, "_dormant", [])
    for i, item in enumerate(dormant_all[d0:], d0):
        try:
            dormant.append(enc(item))
        except Unencodable as e:
            refused.append({"i": i, "type": e.type})
''',
     '''    d0, e0 = marks.get("dormant", 0), marks.get("evidence", 0)
    dormant_all = getattr(ag, "_dormant", [])
    dormant, refused = dormant_items(dormant_all[d0:], d0)
'''),
])
