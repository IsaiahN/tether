import sys
sys.dont_write_bytecode = True
p = "c:/Users/Admin/Documents/GitHub/tether/tests/test_stop_rules.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
pairs = [
('def _stub(ag, slot: str, table: dict) -> None:\n'
 '    """S1 replaced: slot -> survivors, or None for \'the record cannot judge\'."""\n'
 '    ag._space_survivors = lambda s: table.get(s) if s == slot else None\n',
 'def _stub(ag, slot: str, table: dict) -> None:\n'
 '    """The space record replaced: slot -> ([(term, stored bound)], bar), or None for \'the record\n'
 '    cannot judge\'; S1 and 1c read it through _space_bounds."""\n'
 '    ag._space_bounds = lambda s: table.get(s) if s == slot else None\n'),
('    _stub(ag, slot, {slot: [t]})\n', '    _stub(ag, slot, {slot: ([(t, 1.0)], 2.0)})\n'),
('def _none_survive(judgeable: bool) -> tuple:\n'
 '    _env, ag = _agent()\n'
 '    slot = _gap(ag)\n'
 '    table = {slot: [_term("stop_test_a"), _term("stop_test_b")]}\n'
 '    _stub(ag, slot, table)\n'
 '    ag._stop_rules()\n'
 '    table[slot] = [] if judgeable else None\n',
 'def _none_survive(judgeable: bool, after=None, no_split: bool = False) -> tuple:\n'
 '    """Two survivors under the bar 2.0, then a reading with none: by default their bounds ROSE\n'
 '    past an unchanged bar (r339\'s evidence); `after` gives another reading."""\n'
 '    _env, ag = _agent()\n'
 '    slot = _gap(ag)\n'
 '    a, b = _term("stop_test_a"), _term("stop_test_b")\n'
 '    table = {slot: ([(a, 1.0), (b, 1.5)], 2.0)}\n'
 '    _stub(ag, slot, table)\n'
 '    if no_split:\n'
 '        ag._none_cause = lambda _prev, _low: "bound"     # a spy: no cause split\n'
 '    ag._stop_rules()\n'
 '    table[slot] = ((after or ([(a, 2.5), (b, 3.0)], 2.0)) if judgeable else None)\n'),
('    assert [r["detail"]["rule"] for r in rows] == ["none_survive"], rows\n'
 '    assert slot in ag.owed_import, "the slot owes"\n'
 '    print(f"  {slot}: two survivors, then none on a current key: none_survive, and it owes")\n',
 '    assert [r["detail"]["rule"] for r in rows] == ["none_survive"], rows\n'
 '    d = rows[0]["detail"]\n'
 '    assert d["cause"] == "bound" and d["owes"] and len(d["bound_rose"]) == 2, d\n'
 '    assert slot in ag.owed_import, "the slot owes"\n'
 '    print(f"  {slot}: two survivors, their bounds rose past the bar: none_survive, cause bound, "\n'
 '          f"owes; rose {d[\'bound_rose\']}")\n\n\n'
 'def _bar_only(no_split: bool) -> tuple:\n'
 '    a, b = _term("stop_test_a"), _term("stop_test_b")\n'
 '    return _none_survive(True, after=([(a, 1.0), (b, 1.5)], 0.5), no_split=no_split)\n\n\n'
 'def check_ii_bar_only() -> None:\n'
 '    rows, slot, ag = _bar_only(False)\n'
 '    d = rows[0]["detail"] if rows else {}\n'
 '    assert [r["detail"]["rule"] for r in rows] == ["none_survive"], rows\n'
 '    assert d["cause"] == "bar" and not d["owes"] and not d["bound_rose"], d\n'
 '    assert slot not in ag.owed_import, "a bar move owes nothing (r339)"\n'
 '    print(f"  {slot}: bounds unchanged, the bar fell 2.0 -> 0.5: none_survive, cause bar, nothing "\n'
 '          "owed")\n\n\n'
 'def check_ii_mustfail_bar_only() -> None:\n'
 '    rows, slot, ag = _bar_only(True)\n'
 '    assert rows and rows[0]["detail"]["cause"] == "bound", ("occasion: the spy took", rows)\n'
 '    assert slot in ag.owed_import, ("MUST-FAIL: without the cause split a bar move owes", slot)\n'
 '    print(f"  MUST-FAIL: {slot}, no cause split (spy): the same bar move owes")\n'),
('    _stub(ag, slot, {slot: [_term("stop_test_c"), _term("stop_test_d")]})\n',
 '    _stub(ag, slot, {slot: ([(_term("stop_test_c"), 1.0), (_term("stop_test_d"), 1.0)], 2.0)})\n'),
('  check_ii_mustfail_stale_key     MUST-FAIL: the same with the record unable to judge: no row\n',
 '  check_ii_mustfail_stale_key     MUST-FAIL: the same with the record unable to judge: no row\n'
 '  check_ii_bar_only               r339: bounds unchanged, the bar moved: none_survive, cause "bar",\n'
 '                                  nothing owed\n'
 '  check_ii_mustfail_bar_only      MUST-FAIL: the same with no cause split (a spy): it owes\n'),
]
for a, b in pairs:
    a, b = a.replace("\n", nl), b.replace("\n", nl)
    assert s.count(a) == 1, (a[:70], s.count(a))
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
