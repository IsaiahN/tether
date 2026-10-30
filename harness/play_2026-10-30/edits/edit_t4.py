import sys
sys.dont_write_bytecode = True
p = "c:/Users/Admin/Documents/GitHub/tether/tests/test_stop_rules.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
pairs = [
('def _none_survive(judgeable: bool, after=None, no_split=None) -> tuple:\n',
 'def _none_survive(judgeable: bool, after=None, no_split=None, stamp_off=None,\n'
 '                  sync_spy: bool = False) -> tuple:\n'),
('    if no_split is not None:\n'
 '        ag._none_cause = no_split                        # a spy: another cause rule\n',
 '    if no_split is not None:\n'
 '        ag._none_cause = no_split                        # a spy: another cause rule\n'
 '    if sync_spy:\n'
 '        ag._rows_synced = lambda _cells, _bar: True      # a spy: no sync test\n'),
('    table[slot] = ((after or ([(a, 2.5), (b, 3.0)], 2.0)) if judgeable else None)\n',
 '    table[slot] = ((after or ([(a, 2.5), (b, 3.0)], 2.0)) if judgeable else None)\n'
 '    if judgeable and stamp_off is not None:             # each cell priced over the bar\'s rows + off\n'
 '        h = len(ag.history(slot)) + stamp_off\n'
 '        table[slot] = (*table[slot][:2], {a.name: h, b.name: h})\n'),
('def check_ii_none_survive() -> None:\n'
 '    rows, slot, ag = _none_survive(True)\n',
 'def check_ii_none_survive() -> None:\n'
 '    rows, slot, ag = _none_survive(True, stamp_off=0)    # synced: the same rows on both sides\n'),
('    assert d["reached_bar"] == sorted(d["bound_rose"]) and d["invalid_cells"] == 0, d\n',
 '    assert d["reached_bar"] == sorted(d["bound_rose"]) and d["invalid_cells"] == 0, d\n'
 '    assert d["cell_rows"] == [d["bar_rows"]], d\n'),
('def _small_rise(rule=None) -> tuple:\n',
 'def check_ii_unsynced() -> None:\n'
 '    rows, slot, ag = _none_survive(True, stamp_off=1)    # the cells re-priced a row ahead\n'
 '    d = rows[0]["detail"]\n'
 '    assert d["cause"] == "unsynced" and not d["owes"], d\n'
 '    assert d["cell_rows"] == [d["bar_rows"] + 1], d\n'
 '    assert slot not in ag.owed_import, "an unsynced reading owes nothing (r342 5)"\n'
 '    print(f"  {slot}: bounds rose, but the cells were priced over {d[\'cell_rows\']} rows and the "\n'
 '          f"bar over {d[\'bar_rows\']}: cause unsynced, nothing owed")\n\n\n'
 'def check_ii_mustfail_unsynced() -> None:\n'
 '    rows, slot, ag = _none_survive(True, stamp_off=1, sync_spy=True)\n'
 '    d = rows[0]["detail"]\n'
 '    assert len(d["bound_rose"]) == d["last_survivors"], ("occasion: every bound rose", d)\n'
 '    assert d["cause"] == "bound" and slot in ag.owed_import, ("MUST-FAIL: no sync test owes", d)\n'
 '    print(f"  MUST-FAIL: {slot}, the sync test spied off: the same reading owes (cause bound)")\n\n\n'
 'def _small_rise(rule=None) -> tuple:\n'),
('  check_ii_stale_cells            r340: every last survivor\'s cell invalid: cause "stale"\n',
 '  check_ii_stale_cells            r340: every last survivor\'s cell invalid: cause "stale"\n'
 '  check_ii_unsynced               r342 5: the cells priced a row ahead of the bar: cause\n'
 '                                  "unsynced", nothing owed\n'
 '  check_ii_mustfail_unsynced      MUST-FAIL: the same with the sync test spied off: it owes\n'),
]
for a, b in pairs:
    a, b = a.replace("\n", nl), b.replace("\n", nl)
    assert s.count(a) == 1, (a[:70], s.count(a))
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
