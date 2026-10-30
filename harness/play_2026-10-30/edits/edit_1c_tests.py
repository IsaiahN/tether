"""1c's rebase onto 2855932: test_stop_rules (mode-aware stub, the unsynced checks out, the current-record
pair in, base 2855932 via off_env) and _batch.py (S1_REPRICE's sha, STOP_RULES appended). argv: repo root."""
import sys

sys.dont_write_bytecode = True
R = sys.argv[1].rstrip("/")


def edit(rel, pairs, crlf=True):
    p = f"{R}/{rel}"
    s = open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in s else "\n"
    for a, b in pairs:
        a, b = a.replace("\n", nl), b.replace("\n", nl)
        assert s.count(a) == 1, (rel, a[:80], s.count(a))
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8", newline="").write(s)


edit("tests/_batch.py", [
 ("    (\"TETHER_S1_REPRICE\", None),             # 1b's re-price (r350); its sha comes with 1c\n",
  "    (\"TETHER_S1_REPRICE\", \"2855932\"),        # 1b's re-price (r350)\n"
  "    (\"TETHER_STOP_RULES\", None),             # 1c; its sha comes with the next arm\n"),
])

edit("tests/test_stop_rules.py", [
 ("  check_ii_unsynced               r342 5: the cells priced a row ahead of the bar: cause\n"
  "                                  \"unsynced\", nothing owed\n"
  "  check_ii_mustfail_unsynced      MUST-FAIL: the same with the sync test spied off: it owes\n",
  "  check_ii_reads_current          r346, r349: the stored bounds keep two survivors, the re-priced\n"
  "                                  (current) ones price both out: 1c reads the current record --\n"
  "                                  none_survive, cause bound, owes\n"
  "  check_ii_mustfail_reads_stale   MUST-FAIL: the record served stale whatever the mode: the two\n"
  "                                  stay survivors, no row\n"),
 ("  check_off_identity_grid, check_off_identity_fake   TETHER_STOP_RULES=0 against 20cc52a\n",
  "  check_off_identity_grid, check_off_identity_fake   TETHER_STOP_RULES=0 (and every later batch\n"
  "                                  arm, off_env) against 2855932\n"),
 ("import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)\n",
  "from _batch import off_env  # noqa: E402  the batch's arms (r348)\n"
  "\n"
  "import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)\n"),
 ("BASE = \"20cc52a\"      # wip/ask-stop after 1d, the tree before the arm\n",
  "BASE = \"2855932\"      # wip/ask-stop after 1b's re-price, the tree before the arm\n"),
 ("    \"\"\"The space record replaced: slot -> ([(term, stored bound)], bar), or None for 'the record\n"
  "    cannot judge'; S1 and 1c read it through _space_bounds.\"\"\"\n"
  "    ag._space_bounds = lambda s: table.get(s) if s == slot else None\n",
  "    \"\"\"The space record replaced: slot -> ([(term, bound)], bar), or None for 'the record cannot\n"
  "    judge'; S1 and 1c read it through _space_bounds, the same in either mode.\"\"\"\n"
  "    ag._space_bounds = lambda s, _mode: table.get(s) if s == slot else None\n"),
 ("def _none_survive(judgeable: bool, after=None, no_split=None, stamp_off=None,\n"
  "                  sync_spy: bool = False) -> tuple:\n",
  "def _none_survive(judgeable: bool, after=None, no_split=None) -> tuple:\n"),
 ("    if sync_spy:\n"
  "        ag._rows_synced = lambda _cells, _bar: True      # a spy: no sync test\n", ""),
 ("    if judgeable and stamp_off is not None:             # each cell priced over the bar's rows + off\n"
  "        h = len(ag.history(slot)) + stamp_off\n"
  "        table[slot] = (*table[slot][:2], {a.name: h, b.name: h})\n", ""),
 ("    rows, slot, ag = _none_survive(True, stamp_off=0)    # synced: the same rows on both sides\n",
  "    rows, slot, ag = _none_survive(True)\n"),
 ("    assert d[\"cell_rows\"] == [d[\"bar_rows\"]], d\n", ""),
 ("def check_ii_unsynced() -> None:\n"
  "    rows, slot, ag = _none_survive(True, stamp_off=1)    # the cells re-priced a row ahead\n"
  "    d = rows[0][\"detail\"]\n"
  "    assert d[\"cause\"] == \"unsynced\" and not d[\"owes\"], d\n"
  "    assert d[\"cell_rows\"] == [d[\"bar_rows\"] + 1], d\n"
  "    assert slot not in ag.owed_import, \"an unsynced reading owes nothing (r342 5)\"\n"
  "    print(f\"  {slot}: bounds rose, but the cells were priced over {d['cell_rows']} rows and the \"\n"
  "          f\"bar over {d['bar_rows']}: cause unsynced, nothing owed\")\n"
  "\n"
  "\n"
  "def check_ii_mustfail_unsynced() -> None:\n"
  "    rows, slot, ag = _none_survive(True, stamp_off=1, sync_spy=True)\n"
  "    d = rows[0][\"detail\"]\n"
  "    assert len(d[\"bound_rose\"]) == d[\"last_survivors\"], (\"occasion: every bound rose\", d)\n"
  "    assert d[\"cause\"] == \"bound\" and slot in ag.owed_import, (\"MUST-FAIL: no sync test owes\", d)\n"
  "    print(f\"  MUST-FAIL: {slot}, the sync test spied off: the same reading owes (cause bound)\")\n",
  "def _by_mode(mode_blind: bool) -> tuple:\n"
  "    \"\"\"Two survivors under the bar 2.0; then the stored record still holds them while the record\n"
  "    re-priced to the gap's current rows has both past the bar. `mode_blind`: served stale.\"\"\"\n"
  "    _env, ag = _agent()\n"
  "    slot = _gap(ag)\n"
  "    a, b = _term(\"stop_test_a\"), _term(\"stop_test_b\")\n"
  "    stored = ([(a, 1.0), (b, 1.5)], 2.0)\n"
  "    table = {\"stale\": stored, \"reprice\": stored}\n"
  "    ag._space_bounds = lambda s, mode: (table[\"stale\" if mode_blind else mode] if s == slot\n"
  "                                        else None)\n"
  "    ag._stop_rules()\n"
  "    table[\"reprice\"] = ([(a, 2.5), (b, 3.0)], 2.0)\n"
  "    ag.owed_import.discard(slot)\n"
  "    n0 = len(ag.led.rows())\n"
  "    ag._stop_rules()\n"
  "    return [r for r in _rows(ag, n0, \"stop_rule\") if r[\"slot\"] == slot], slot, ag, table\n"
  "\n"
  "\n"
  "def check_ii_reads_current() -> None:\n"
  "    rows, slot, ag, table = _by_mode(False)\n"
  "    assert table[\"stale\"] != table[\"reprice\"], \"occasion: the stored and current records differ\"\n"
  "    d = rows[0][\"detail\"] if rows else {}\n"
  "    assert [r[\"detail\"][\"rule\"] for r in rows] == [\"none_survive\"], rows\n"
  "    assert d[\"cause\"] == \"bound\" and d[\"owes\"] and slot in ag.owed_import, d\n"
  "    print(f\"  {slot}: stored bounds keep 2 survivors, the current rows price both out: 1c reads \"\n"
  "          \"the current record -- none_survive, cause bound, owes\")\n"
  "\n"
  "\n"
  "def check_ii_mustfail_reads_stale() -> None:\n"
  "    rows, slot, ag, table = _by_mode(True)\n"
  "    assert table[\"stale\"] != table[\"reprice\"], \"occasion: the stored and current records differ\"\n"
  "    assert not rows and slot not in ag.owed_import, (\"MUST-FAIL: a stale read sees survivors\", rows)\n"
  "    print(f\"  MUST-FAIL: {slot}, the record served stale: the 2 stay survivors, no row, nothing \"\n"
  "          \"owed\")\n"),
 ("    cur = _norm(_child(root, w, {\"TETHER_STOP_RULES\": \"0\"}))\n",
  "    cur = _norm(_child(root, w, off_env(\"TETHER_STOP_RULES\")))   # and every later batch arm\n"),
])
print("ok")
