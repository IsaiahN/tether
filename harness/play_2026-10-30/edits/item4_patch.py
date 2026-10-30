"""Item 4, THE CHECKED SAVE ON AN AGENT FAULT (the design post 2026-10-22 15:14, approved 15:17 with (C3))."""
import sys

sys.dont_write_bytecode = True
root = sys.argv[1]


def patch(rel, pairs):
    p = f"{root}/{rel}"
    s = open(p, encoding="utf-8").read()
    for a, b in pairs:
        assert s.count(a) == 1, (rel, a[:70])
        s = s.replace(a, b)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(s)


patch("ledger.py", [(
    'WIN, DEATH, RESET, ADVANCE, CAP = "game_win", "death", "reset", "level_advance", "cap"\n',
    'WIN, DEATH, RESET, ADVANCE, CAP = "game_win", "death", "reset", "level_advance", "cap"\n'
    '# item 4 (2026-10-22): the game ended because the agent\'s own code raised, never the world\n'
    'AGENT_FAULT = "agent_fault"\n')])

patch("tether.py", [
    ('_TERM_KIND = {"death": "death", "cap": "cap", "time": "cap", "run_end": "cap"}\n',
     '_TERM_KIND = {"death": "death", "cap": "cap", "time": "cap", "run_end": "cap",\n'
     '              "agent_fault": "cap"}    # item 4: a fault is no fact about the world\n'),
    ('_END_RESERVE = armflag.arm("TETHER_END_RESERVE", default=True)\n',
     '_END_RESERVE = armflag.arm("TETHER_END_RESERVE", default=True)\n'
     '# item 4 (the design post 2026-10-22 15:14; the reviewer 15:17 (C3)): an agent fault in play\n'
     '# writes the game\'s learning only if it reads back, without the faulted cycle\'s own entries\n'
     '_ERROR_CARRY = armflag.arm("TETHER_ERROR_CARRY", default=True)\n'),
    ('    _end_path_t0 = None        # set by the end block: the end path is timed whole\n',
     '    _end_path_t0 = None        # set by the end block: the end path is timed whole\n'
     '    _fault_cycle = None        # item 4: the cycle an agent fault was raised in (None: none)\n'
     '    _fault_text = None         # item 4: the fault, type and message\n'),
])

patch("lineage.py", [
    ('''        rid = (c.get("born"), c.get("handle"))
        if rid not in prev:
            terms.append(r)''',
     '''        rid = (c.get("born"), c.get("handle"))
        if fc is not None and str(r.get("residual") or "").endswith(f"@{fc}"):
            continue    # (C3): the faulted step's own term never met its next observation
        if rid not in prev:
            terms.append(r)'''),
    ('''    written = getattr(ag, "_lineage_written", {}) if _BOUNDARY else {}
    marks = getattr(ag, "_lineage_marks", {}) if _BOUNDARY else {}
    new_names = []''',
     '''    written = getattr(ag, "_lineage_written", {}) if _BOUNDARY else {}
    marks = getattr(ag, "_lineage_marks", {}) if _BOUNDARY else {}
    new_names = []
    fc = getattr(ag, "_fault_cycle", None)     # item 4: a write after an agent fault'''),
    ('''                             for r in ag._inv_carry[ag._inv_carry_written:]]''',
     '''                             for r in ag._inv_carry[ag._inv_carry_written:]
                             if fc is None or r.get("born") != fc]     # (C3)'''),
    ('''    raw = _dumps(gen)
    h = hashlib.sha256(raw).hexdigest()[:16]
    try:
        with open(p / f"{PREFIX}{h}.json", "xb") as fh:
            fh.write(_store_bytes(raw))
    except FileExistsError:
        if store_con is not None:
            store_con.close()
        return {"refused": f"{PREFIX}{h}.json exists; a generation is never overwritten"}''',
     '''    if fc is not None:
        # item 4: the generation names how its game ended; the faulted cycle's stamped entries
        # are not in it (above); its unstamped structures (kind episodes, counters) are as built
        gen["ended"], gen["error"] = "agent_fault", str(ag._fault_text)[:500]
    raw = _dumps(gen)
    h = hashlib.sha256(raw).hexdigest()[:16]
    if fc is not None and not _readback(_store_bytes(raw), raw, h):
        return {"refused": "item 4: the fault's generation did not read back; nothing written"}
    try:
        with open(p / f"{PREFIX}{h}.json", "xb") as fh:
            fh.write(_store_bytes(raw))
    except FileExistsError:
        if store_con is not None:
            store_con.close()
        return {"refused": f"{PREFIX}{h}.json exists; a generation is never overwritten"}'''),
    ('''def _store_bytes(raw: bytes) -> bytes:''',
     '''def _readback(stored: bytes, raw: bytes, h: str) -> bool:
    """Item 4: the bytes a fault's generation would be written as, read back as the loader reads
    them (lineage_store.file_bytes, _read): the same bytes, the same name hash, parsing to the same
    record. It shows the bytes decode to what was built, not that a step cut halfway left the
    library consistent (the design post's own limit, 2026-10-22 15:14)."""
    import zlib
    back = zlib.decompress(stored) if stored[:1] == b"\\x78" else stored
    return (back == raw and hashlib.sha256(back).hexdigest()[:16] == h
            and json.loads(back) == json.loads(raw))


def _store_bytes(raw: bytes) -> bytes:'''),
])
print("patched")
