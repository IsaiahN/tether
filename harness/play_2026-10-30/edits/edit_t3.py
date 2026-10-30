import sys
sys.dont_write_bytecode = True
p = "c:/Users/Admin/Documents/GitHub/tether/tests/test_stop_rules.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
pairs = [
('def _none_survive(judgeable: bool, after=None, no_split: bool = False) -> tuple:\n',
 'def _none_survive(judgeable: bool, after=None, no_split=None) -> tuple:\n'),
('    if no_split:\n'
 '        ag._none_cause = lambda _prev, _low: "bound"     # a spy: no cause split\n',
 '    if no_split is not None:\n'
 '        ag._none_cause = no_split                        # a spy: another cause rule\n'),
('    assert d["cause"] == "bound" and d["owes"] and len(d["bound_rose"]) == 2, d\n',
 '    assert d["cause"] == "bound" and d["owes"] and len(d["bound_rose"]) == 2, d\n'
 '    assert d["reached_bar"] == sorted(d["bound_rose"]) and d["invalid_cells"] == 0, d\n'),
('def _bar_only(no_split: bool) -> tuple:\n'
 '    a, b = _term("stop_test_a"), _term("stop_test_b")\n'
 '    return _none_survive(True, after=([(a, 1.0), (b, 1.5)], 0.5), no_split=no_split)\n',
 'def _bar_only(no_split=None) -> tuple:\n'
 '    a, b = _term("stop_test_a"), _term("stop_test_b")\n'
 '    return _none_survive(True, after=([(a, 1.0), (b, 1.5)], 0.5), no_split=no_split)\n\n\n'
 'def _any_rise(prev, low, _bar_before):\n'
 '    """r339\'s first rule, before r340: any rise at all is evidence."""\n'
 '    return "bound" if any(n in low and low[n] > b for n, b in prev.items()) else "bar"\n'),
('    rows, slot, ag = _bar_only(False)\n', '    rows, slot, ag = _bar_only()\n'),
('    rows, slot, ag = _bar_only(True)\n',
 '    rows, slot, ag = _bar_only(lambda _prev, _low, _bar: "bound")\n'),
('    print(f"  MUST-FAIL: {slot}, no cause split (spy): the same bar move owes")\n',
 '    print(f"  MUST-FAIL: {slot}, no cause split (spy): the same bar move owes")\n\n\n'
 'def _small_rise(rule=None) -> tuple:\n'
 '    a, b = _term("stop_test_a"), _term("stop_test_b")\n'
 '    return _none_survive(True, after=([(a, 1.1), (b, 1.5)], 0.5), no_split=rule)\n\n\n'
 'def check_ii_small_rise() -> None:\n'
 '    rows, slot, ag = _small_rise()\n'
 '    d = rows[0]["detail"]\n'
 '    assert d["cause"] == "bar" and d["bound_rose"] and not d["reached_bar"], d\n'
 '    assert slot not in ag.owed_import, "a rise under the old bar is the cut, not evidence"\n'
 '    print(f"  {slot}: 1.0 -> 1.1 under a bar 2.0 -> 0.5: cause bar, nothing owed; rose "\n'
 '          f"{d[\'bound_rose\']}")\n\n\n'
 'def check_ii_mustfail_small_rise() -> None:\n'
 '    rows, slot, ag = _small_rise(_any_rise)\n'
 '    assert rows and rows[0]["detail"]["bound_rose"], ("occasion: a small rise", rows)\n'
 '    assert slot in ag.owed_import, ("MUST-FAIL: under \'any rise\' the small rise owes", slot)\n'
 '    print(f"  MUST-FAIL: {slot}, the any-rise rule (r339) owes on the same small rise")\n\n\n'
 'def check_ii_stale_cells() -> None:\n'
 '    rows, slot, ag = _none_survive(True, after=([], 2.0))\n'
 '    d = rows[0]["detail"]\n'
 '    assert d["cause"] == "stale" and d["invalid_cells"] == d["last_survivors"] == 2, d\n'
 '    assert slot not in ag.owed_import, "a record that cannot judge its survivors owes nothing"\n'
 '    print(f"  {slot}: every last survivor\'s cell invalid: cause stale, nothing owed")\n'),
('  check_ii_mustfail_bar_only      MUST-FAIL: the same with no cause split (a spy): it owes\n',
 '  check_ii_mustfail_bar_only      MUST-FAIL: the same with no cause split (a spy): it owes\n'
 '  check_ii_small_rise             r340: 1.0 -> 1.1 while the bar falls 2.0 -> 0.5: cause "bar"\n'
 '  check_ii_mustfail_small_rise    MUST-FAIL: under r339\'s any-rise rule the same reading owes\n'
 '  check_ii_stale_cells            r340: every last survivor\'s cell invalid: cause "stale"\n'),
]
for a, b in pairs:
    a, b = a.replace("\n", nl), b.replace("\n", nl)
    assert s.count(a) == 1, (a[:70], s.count(a))
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
