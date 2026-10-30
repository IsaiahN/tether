"""r361 on the 1c tree (argv: repo root): 1c's re-price wall readable on its own (a per-step stop_read row
under MINT, in TIMINGS), and check_s1_mustfail_reprice clears the memo that remembers the row test."""
import sys

sys.dont_write_bytecode = True
R = sys.argv[1].rstrip("/")


def edit(rel, pairs):
    p = f"{R}/{rel}"
    s = open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in s else "\n"
    for a, b in pairs:
        a, b = a.replace("\n", nl), b.replace("\n", nl)
        assert s.count(a) == 1, (rel, a[:80], s.count(a))
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8", newline="").write(s)


edit("tether.py", [
 ("        for s in sorted(self._space):\n"
  "            got = self._space_bounds(s, \"reprice\")   # r346: 1c reads a CURRENT record only\n"
  "            if got is None:\n",
  "        rp = [0, 0, 0.0, 0]                       # r361: this read's re-price, kept on its own row\n"
  "        for s in sorted(self._space):\n"
  "            got = self._space_bounds(s, \"reprice\")   # r346: 1c reads a CURRENT record only\n"
  "            rp = [a + b for a, b in zip(rp, self._repriced, strict=True)]\n"
  "            if got is None:\n"),
 ("                                  \"(Fig 5 :13-14); nothing binds\")\n"
  "        for s, (reads, rkey) in sorted(self._split_aim.items()):\n",
  "                                  \"(Fig 5 :13-14); nothing binds\")\n"
  "        if self._space:\n"
  "            self.led.record(self.cycle, \"MINT\", \"@stop\", \"stop_read\", spaces=len(self._space),\n"
  "                            repriced_cells=rp[0], repriced_rows=rp[1], reprice_s=round(rp[2], 4),\n"
  "                            reprice_hits=rp[3],\n"
  "                            reads=\"1c: this step's read of every open space, re-priced on read \"\n"
  "                                  \"(r361: its wall apart from the mint's)\")\n"
  "        for s, (reads, rkey) in sorted(self._split_aim.items()):\n"),
])
edit("conform/identity_mod_rows.py", [
 ("           (\"ask_none\", \"reprice_s\"))         # the same, when no gap stays eligible\n",
  "           (\"ask_none\", \"reprice_s\"),          # the same, when no gap stays eligible\n"
  "           (\"stop_read\", \"reprice_s\"))        # 1c's per-step re-price of every open space (r361)\n"),
])
edit("tests/test_ask.py", [
 ("    stored = ag._s1_of(*ag._space_bounds(s, \"stale\"))\n"
  "    ag._row_wrong = lambda _t, _s, _row: False           # a spy: no row charges\n",
  "    stored = ag._s1_of(*ag._space_bounds(s, \"stale\"))\n"
  "    ag._reprice_memo = {}                 # 1c's _stop_rules keeps the real row test's charges\n"
  "    ag._row_wrong = lambda _t, _s, _row: False           # a spy: no row charges\n"),
])
print("ok")
