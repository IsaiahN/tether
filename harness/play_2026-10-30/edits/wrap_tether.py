import sys

sys.dont_write_bytecode = True
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
R = [
    ("# C1 (A) (Isaiah 2026-10-22 12:36-12:37; the reviewer 15:17, 15:34): a head at every growing loop (cap.py), and\n"
     "# the end-path reserve: thinking stops at the deadline less the agent's own latest measured end-path wall\n",
     "# C1 (A) (Isaiah 2026-10-22 12:36-12:37; the reviewer 15:17, 15:34): a head at every growing\n"
     "# loop (cap.py), and the end-path reserve: thinking stops at the deadline less the agent's own\n"
     "# latest measured end-path wall\n"),
    ("# The runner's deadline passed between two lookups or at a growing loop's head: cap.CapReached (a\n"
     "# BaseException), caught at step's route call for the route's own rows and at step for every other cut\n",
     "# The runner's deadline passed between two lookups or at a growing loop's head: cap.CapReached\n"
     "# (a BaseException), caught at step's route call for the route's own rows and at step for every\n"
     "# other cut\n"),
    ("    _cut = False               # C1 (A): a cut ended thinking; no step runs after it (the reviewer 15:34 (a))\n",
     "    _cut = False               # C1 (A): a cut ended thinking; no step runs after it (15:34 (a))\n"),
    ("    _end_reserve = None        # the end-path reserve R, s: the latest measured end-path wall (None: unmeasured)\n",
     "    _end_reserve = None        # the end-path reserve R, s (None: unmeasured, none taken)\n"),
    ("            self._cut_scope = self._cut_scope or step     # the innermost scope a cut unwound through\n",
     "            self._cut_scope = self._cut_scope or step     # the innermost scope a cut left\n"),
    ('''        """One turn (_step_body). C1 (A), the overrun safety net (Isaiah 2026-10-22 12:36; the reviewer 12:37,
        15:17, 15:34): the thinking deadline (_think_until) is cap.AT for the step and cleared after it, so the
        end path is never cut. A cut at any growing loop's head ends the step with one row naming where. After
        a cut, or once the thinking deadline has passed, no step runs again: only the end path reads what a
        cut left (the reviewer 15:34 (a))."""
        until = self._think_until()
        if not self._cut and until is not None and _CAP_INNER and time.time() >= until:
            self._cut = True       # the end-path reserve: the agent stops thinking, the end path is kept
            self.led.record(self.cycle, "SETTLE", "@cap", "stopped_for_end_path", acted=False,
                            reserve_s=self._end_reserve, reads="the thinking deadline passed before the "
                            "step: the reserve is kept for the game's end path")
            return False''',
     '''        """One turn (_step_body). C1 (A), the overrun safety net (Isaiah 2026-10-22 12:36; the
        reviewer 12:37, 15:17, 15:34): the thinking deadline (_think_until) is cap.AT for the step
        and cleared after it, so the end path is never cut. A cut at any growing loop's head ends
        the step with one row naming where. After a cut, or once the thinking deadline has passed,
        no step runs again: only the end path reads what a cut left (the reviewer 15:34 (a))."""
        until = self._think_until()
        if not self._cut and until is not None and _CAP_INNER and time.time() >= until:
            self._cut = True       # the reserve: the agent stops thinking, the end path is kept
            self.led.record(self.cycle, "SETTLE", "@cap", "stopped_for_end_path", acted=False,
                            reserve_s=self._end_reserve, reads="the thinking deadline passed "
                            "before the step: the reserve is kept for the game's end path")
            return False'''),
    ('''        """The thinking deadline: the runner's deadline less the end-path reserve (the agent's own latest
        measured end-path wall, _end_reserve; None when unmeasured, then no reserve is taken)."""''',
     '''        """The thinking deadline: the runner's deadline less the end-path reserve (the agent's own
        latest measured end-path wall, _end_reserve; None when unmeasured: no reserve taken)."""'''),
    ('''        """A cut at a growing loop's head (cap.head): one "@cap" row naming the step scope and the site, whether
        the press had gone out; "unreached at this budget", never a verdict (Fig 9 :60, Fig 13 :134)."""''',
     '''        """A cut at a growing loop's head (cap.head): one "@cap" row naming the step scope, the
        site and whether the press had gone out; "unreached at this budget", never a verdict
        (Fig 9 :60, Fig 13 :134)."""'''),
    ('''                        reads="unreached at this budget: the agent stopped at a loop's head, between whole "
                              "units of work, and ran none of the rest of this step")''',
     '''                        reads="unreached at this budget: the agent stopped at a loop's head, "
                              "between whole units of work, and ran none of the rest of this step")'''),
]
for a, b in R:
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("applied", len(R))
