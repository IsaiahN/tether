"""r350: TETHER_S1_REPRICE as its own arm (OFF byte-equal to 20cc52a) and the cross-cycle re-price
cache. argv: the worktree root."""
import sys

sys.dont_write_bytecode = True
W = sys.argv[1].rstrip("/")


def edit(rel, pairs):
    p = f"{W}/{rel}"
    s = open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in s else "\n"
    for a, b in pairs:
        a, b = a.replace("\n", nl), b.replace("\n", nl)
        assert s.count(a) == 1, (rel, a[:80], s.count(a))
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8", newline="").write(s)


edit("tether.py", [
 ("_ASK = armflag.arm(\"TETHER_ASK\", default=True)\n",
  "_ASK = armflag.arm(\"TETHER_ASK\", default=True)\n"
  "# 1b's S1 RE-PRICED ON READ (the reviewer 2026-10-29 r346, r347, r349, r350): a cell under the bar\n"
  "# charged on fewer residual rows than its gap now holds is charged on the rows it missed, by the\n"
  "# bound's one row test, before 1b counts it a survivor; eligibility is lazy in rank order. OFF\n"
  "# restores the stale-S1 asks -- a measuring setting, not a safe one. ON; conform/arms.py\n"
  "_S1_REPRICE = armflag.arm(\"TETHER_S1_REPRICE\", default=True)\n"),
 ("        self._repriced: tuple = (0, 0, 0.0)  # 1b: the last S1 read's (cells, rows, secs) re-priced\n",
  "        self._repriced: tuple = (0, 0, 0.0, 0)  # 1b: the last S1 read's (cells, rows, secs, hits)\n"
  "        self._reprice_memo: dict = {}  # 1b: slot -> ((tally key, decoder size), term -> charges)\n"),
 ("        r346, r347: read on a CURRENT record -- the bounds re-priced on read (_space_bounds).\"\"\"\n"
  "        got = self._space_bounds(slot, \"reprice\")\n",
  "        r346, r347: read on a CURRENT record -- the bounds re-priced on read (_space_bounds).\"\"\"\n"
  "        got = self._space_bounds(slot, \"reprice\" if _S1_REPRICE else \"stale\")\n"),
 ("        rewritten. A cell already at or above the bar is out either way.\"\"\"\n"
  "        self._repriced = (0, 0, 0.0)\n",
  "        rewritten. A cell already at or above the bar is out either way. r350: the charges on\n"
  "        the missed rows are kept per cell across cycles and served while the cell, the residual\n"
  "        list's length, the tally key and the decoder size are all unchanged (_reprice_hit).\"\"\"\n"
  "        self._repriced = (0, 0, 0.0, 0)\n"),
 ("        t0, robs, cells_n, rows_n = time.perf_counter(), None, 0, 0\n",
  "        t0, robs, cells_n, rows_n, hits = time.perf_counter(), None, 0, 0, 0\n"),
 ("                    if robs is None:\n"
  "                        robs = self._residual_obs(slot, held, self.history(slot))\n",
  "                    if robs is None:\n"
  "                        robs = self._residual_obs(slot, held, self.history(slot))\n"
  "                        memo = self._reprice_memo.get(slot)\n"
  "                        mkey = (seen[0], self._decoder_size())\n"
  "                        if memo is None or memo[0] != mkey:\n"
  "                            memo = self._reprice_memo[slot] = (mkey, {})\n"),
 ("                    if c[0] < len(robs):\n"
  "                        miss = robs[c[0]:]\n"
  "                        bound += unit * sum(1 for row in miss if self._row_wrong(t, slot, row))\n"
  "                        cells_n, rows_n = cells_n + 1, rows_n + len(miss)\n"
  "                out.append((t, bound))\n"
  "        self._repriced = (cells_n, rows_n, time.perf_counter() - t0)\n"
  "        return out, bar\n",
  "                    if c[0] < len(robs):\n"
  "                        hit = memo[1].get(t)\n"
  "                        if self._reprice_hit(hit, c, len(robs)):\n"
  "                            k, hits = hit[2], hits + 1\n"
  "                        else:\n"
  "                            miss = robs[c[0]:]\n"
  "                            k = sum(1 for row in miss if self._row_wrong(t, slot, row))\n"
  "                            memo[1][t] = (c, len(robs), k)\n"
  "                            cells_n, rows_n = cells_n + 1, rows_n + len(miss)\n"
  "                        bound += unit * k\n"
  "                out.append((t, bound))\n"
  "        self._repriced = (cells_n, rows_n, time.perf_counter() - t0, hits)\n"
  "        return out, bar\n\n"
  "    @staticmethod\n"
  "    def _reprice_hit(hit: tuple | None, cell: tuple, n: int) -> bool:\n"
  "        \"\"\"r350: a kept charge is served only for the SAME cell (a rewrite is a new tuple) over\n"
  "        the same residual list length, the list only extending under the key.\"\"\"\n"
  "        return hit is not None and hit[0] is cell and hit[1] == n\n"),
 ("        order, skipped, slot, sv, rp = list(elig), [], None, [], [0, 0, 0.0]\n",
  "        order, skipped, slot, sv, rp = list(elig), [], None, [], [0, 0, 0.0, 0]\n"),
 ("            rp = [rp[0] + self._repriced[0], rp[1] + self._repriced[1], rp[2] + self._repriced[2]]\n",
  "            rp = [a + b for a, b in zip(rp, self._repriced)]\n"),
 ("                            skipped=skipped, repriced_cells=rp[0], repriced_rows=rp[1],\n"
  "                            reprice_s=round(rp[2], 4),\n",
  "                            skipped=skipped, repriced_cells=rp[0], repriced_rows=rp[1],\n"
  "                            reprice_s=round(rp[2], 4), reprice_hits=rp[3],\n"),
 ("        self._ask_abstained = None if r is not None else (slot, len(sv))\n"
  "        self.led.record(self.cycle, \"PLAN\", slot, \"ask\", gaps_eligible=len(elig), gap_asked=slot,\n"
  "                        survivors=len(sv), stored_survivors=elig[slot], skipped=skipped,\n"
  "                        repriced_cells=rp[0], repriced_rows=rp[1], reprice_s=round(rp[2], 4),\n"
  "                        vectors=len(set(vec.values())),\n",
  "        self._ask_abstained = None if r is not None else (slot, len(sv))\n"
  "        # OFF, S1 is the stored one and every eligible gap holds its two: the 20cc52a ask, its row\n"
  "        rep = (dict(stored_survivors=elig[slot], skipped=skipped, repriced_cells=rp[0],\n"
  "                    repriced_rows=rp[1], reprice_s=round(rp[2], 4), reprice_hits=rp[3])\n"
  "               if _S1_REPRICE else {})\n"
  "        self.led.record(self.cycle, \"PLAN\", slot, \"ask\", gaps_eligible=len(elig), gap_asked=slot,\n"
  "                        survivors=len(sv), **rep, vectors=len(set(vec.values())),\n"),
])

edit("conform/arms.py", [
 ("    \"TETHER_DIVIDE_CREDIT\": \"1a CREDIT (the reviewer 2026-10-29 r312 ask 3; Fig 12 :108, Fig 6 \"\n",
  "    \"TETHER_S1_REPRICE\": \"1b's S1 re-priced on read (the reviewer 2026-10-29 r346, r347, r349, \"\n"
  "                         \"r350). Under TETHER_ASK, a cell under the current bar charged on fewer \"\n"
  "                         \"residual rows than its gap now holds (its own c[0] against the list, \"\n"
  "                         \"which only extends under the tally key) is charged on exactly the rows \"\n"
  "                         \"it missed, by the bound's one row test (_row_wrong, which _cannot_pay \"\n"
  "                         \"calls), before it counts as a survivor; a moved key or a shrunk list \"\n"
  "                         \"cannot judge (no ask). Eligibility is read on the stored S1 (an upper \"\n"
  "                         \"set) and re-priced lazily in rank order; a gap under two is skipped \"\n"
  "                         \"with its count, and none left writes PLAN 'ask_none' on '@ask'. The \"\n"
  "                         \"charges are kept per cell across cycles (same cell, list length, key, \"\n"
  "                         \"decoder size). The reason: r346 found 8 of 13 asks reading a stale \"\n"
  "                         \"record, and re-pricing cuts gridworld's stored survivors 45,384 -> \"\n"
  "                         \"0/38 and 70,620 -> 37 at 5.17 s max, 0.51 s median per ask (24 steps). \"\n"
  "                         \"OFF restores the stale-S1 asks, byte-equal to 20cc52a: a measuring \"\n"
  "                         \"setting, not a safe one. default ON\",\n"
  "    \"TETHER_DIVIDE_CREDIT\": \"1a CREDIT (the reviewer 2026-10-29 r312 ask 3; Fig 12 :108, Fig 6 \"\n"),
])

edit("tests/_batch.py", [
 ("    (\"TETHER_OWED_REJUDGE\", \"20cc52a\"),      # 1d\n",
  "    (\"TETHER_OWED_REJUDGE\", \"20cc52a\"),      # 1d\n"
  "    (\"TETHER_S1_REPRICE\", None),             # 1b's re-price (r350): its sha is filled by 1c's append\n"),
 ("    (\"TETHER_ASK\", \"2a8045c\"),               # 1b, and its S1 re-price on read (same arm)\n",
  "    (\"TETHER_ASK\", \"2a8045c\"),               # 1b\n"),
])

edit("tests/test_ask.py", [
 ("  check_off_identity_grid, check_off_identity_fake   TETHER_ASK=0 writes the same ledger as dad9d2b\n",
  "  check_reprice_cache_hold    r350: a second read serves kept charges and equals a fresh re-price\n"
  "  check_reprice_cache_mustfail   MUST-FAIL: the kept charge served WITHOUT the list length: after\n"
  "                          new residual rows the stale charge differs from a fresh re-price\n"
  "  check_off_identity_grid, check_off_identity_fake   TETHER_ASK=0 writes the same ledger as dad9d2b\n"
  "  check_reprice_off_identity_grid, _fake   TETHER_S1_REPRICE=0 writes the same ledger as 20cc52a\n"),
 ("BASE = \"dad9d2b\"      # general-agent after 1a, the tree before the arm\n",
  "BASE = \"dad9d2b\"      # general-agent after 1a, the tree before the arm\n"
  "REPRICE_BASE = \"20cc52a\"   # 1d, the tree before TETHER_S1_REPRICE (r350)\n"),
 ("def check_s1_bargain_hold() -> None:\n",
  "def _fresh(ag, s):\n"
  "    ag._reprice_memo = {}\n"
  "    return ag._space_bounds(s, \"reprice\")\n\n\n"
  "def check_reprice_cache_hold() -> None:\n"
  "    ag, s, _held, _robs, _behind = _stale_gap()\n"
  "    ag._reprice_memo = {}                                # the steps' own asks may have kept some\n"
  "    first = ag._space_bounds(s, \"reprice\")\n"
  "    n1 = ag._repriced[0]\n"
  "    again = ag._space_bounds(s, \"reprice\")\n"
  "    hits, n2 = ag._repriced[3], ag._repriced[0]\n"
  "    assert n1 > 0 and hits == n1 and n2 == 0, (n1, hits, n2)\n"
  "    assert again == first == _fresh(ag, s)\n"
  "    print(f\"  {s}: second read serves {hits} kept charges, recomputes 0; equal to a fresh re-price\")\n\n\n"
  "def _grown(ag, s, robs, hit):\n"
  "    \"\"\"The residual list grown by its own rows again, then a re-price with `hit` as the cache\n"
  "    test, against a fresh one; with the occasion: cells whose charge on the new rows is > 0.\"\"\"\n"
  "    ag._reprice_memo = {}\n"
  "    ag._space_bounds(s, \"reprice\")                      # charges kept at len(robs)\n"
  "    grown = robs + robs\n"
  "    ag._residual_obs = lambda _s, _h, _hist: grown\n"
  "    ag._reprice_hit = hit\n"
  "    served = dict(ag._space_bounds(s, \"reprice\")[0])\n"
  "    ag._reprice_hit = type(ag)._reprice_hit\n"
  "    fresh = dict(_fresh(ag, s)[0])\n"
  "    return served, fresh\n\n\n"
  "def check_reprice_cache_mustfail() -> None:\n"
  "    ag, s, _held, robs, _behind = _stale_gap()\n"
  "    served, fresh = _grown(ag, s, robs, lambda hit, c, _n: hit is not None and hit[0] is c)\n"
  "    occ = sum(1 for t in fresh if fresh[t] != served[t])\n"
  "    assert occ > 0, \"MUST-FAIL: a length-blind cache served nothing stale (no occasion)\"\n"
  "    ag2, s2, _h2, robs2, _b2 = _stale_gap()\n"
  "    served2, fresh2 = _grown(ag2, s2, robs2, type(ag2)._reprice_hit)\n"
  "    assert served2 == fresh2, \"the length-checked cache must equal a fresh re-price\"\n"
  "    print(f\"  MUST-FAIL: {s}, the cache blind to the list length serves {occ} stale charges after \"\n"
  "          f\"{len(robs)} new rows; with the length checked it equals a fresh re-price\")\n\n\n"
  "def check_s1_bargain_hold() -> None:\n"),
 ("def _off_identity(w: str) -> None:\n"
  "    root = str(_repo.ROOT)\n"
  "    with tempfile.TemporaryDirectory() as d:\n"
  "        tar = subprocess.run([\"git\", \"-C\", root, \"archive\", BASE], capture_output=True, check=True)\n",
  "def _off_identity(w: str, arm: str = \"TETHER_ASK\", base_sha: str = BASE) -> None:\n"
  "    root = str(_repo.ROOT)\n"
  "    with tempfile.TemporaryDirectory() as d:\n"
  "        tar = subprocess.run([\"git\", \"-C\", root, \"archive\", base_sha], capture_output=True,\n"
  "                             check=True)\n"),
 ("    cur = _norm(_child(root, w, off_env(\"TETHER_ASK\")))      # and every later batch arm\n"
  "    _same(base, cur, f\"OFF identity {w}\")\n"
  "    print(f\"  OFF identity (TETHER_ASK=0, {w}): {len(base)} rows against {BASE}, 0 differences\")\n",
  "    cur = _norm(_child(root, w, off_env(arm)))      # and every later batch arm\n"
  "    _same(base, cur, f\"OFF identity {w}\")\n"
  "    print(f\"  OFF identity ({arm}=0, {w}): {len(base)} rows against {base_sha}, 0 differences\")\n"),
 ("def check_off_identity_fake() -> None:\n"
  "    _off_identity(\"fake\")\n",
  "def check_off_identity_fake() -> None:\n"
  "    _off_identity(\"fake\")\n\n\n"
  "def check_reprice_off_identity_grid() -> None:\n"
  "    _off_identity(\"grid\", \"TETHER_S1_REPRICE\", REPRICE_BASE)\n\n\n"
  "def check_reprice_off_identity_fake() -> None:\n"
  "    _off_identity(\"fake\", \"TETHER_S1_REPRICE\", REPRICE_BASE)\n"),
])
print("ok")
