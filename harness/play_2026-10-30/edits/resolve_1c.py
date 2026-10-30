"""1c's rebase onto 2855932: resolve the 7 conflict blocks in tether.py (argv: repo root). Block i is
replaced by RES[i](ours, theirs); every block is asserted present and the file keeps its CRLF."""
import re
import sys

sys.dont_write_bytecode = True
p = sys.argv[1].rstrip("/") + "/tether.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n"
assert nl in s
pat = re.compile(r"<<<<<<< ours\r\n(.*?)=======\r\n(.*?)>>>>>>> theirs\r\n", re.S)
blocks = pat.findall(s)
assert len(blocks) == 7, len(blocks)


def L(text: str) -> str:
    return text.replace("\n", nl)


SPACE_SURV = L(
    "        on a row may still be the best there is (Fig 9 :40). Ranked by deficit, lowest first.\n"
    "        r346, r347: read on a CURRENT record -- the bounds re-priced on read (_space_bounds).\"\"\"\n"
    "        got = self._space_bounds(slot, \"reprice\" if _S1_REPRICE else \"stale\")\n"
    "        return [] if got is None else self._s1_of(*got)\n"
    "\n"
    "    def _space_survivors(self, slot: str) -> list | None:\n"
    "        \"\"\"1c: S1 on a CURRENT record (re-priced on read, r346), else None where the record cannot\n"
    "        judge (no space, a moved key) -- so 1c (ii) tells 'none survive' from 'cannot say'.\"\"\"\n"
    "        got = self._space_bounds(slot, \"reprice\")\n"
    "        return None if got is None else self._s1_of(*got)\n"
    "\n"
    "    @staticmethod\n"
    "    def _s1_of(bounds: list, bar: float) -> list:\n"
    "        \"\"\"S1 from a space's bounds: each term with a bound under the bar, by deficit.\"\"\"\n")
NONE_CAUSE = L(
    "    @staticmethod\n"
    "    def _none_cause(prev: dict, low: dict, bar_before: float) -> str:\n"
    "        \"\"\"1c (ii), r339, r340: 'bound' when a last survivor's bound rose to the bar it last\n"
    "        survived under -- the ground's charge alone would have removed it (Fig 5 :14); 'stale'\n"
    "        when no last survivor's cell is still valid (P2 at the survivor grain); else 'bar': the\n"
    "        cut moved (Fig 9 :40-41). Read on re-priced bounds, so over the gap's current rows.\"\"\"\n"
    "        if not any(n in low for n in prev):\n"
    "            return \"stale\"\n"
    "        return \"bound\" if any(n in low and low[n] >= bar_before for n in prev) else \"bar\"\n"
    "\n")
HELD = L(
    "            if _STOP_RULES and self._stop.get(s) == \"held\":\n"
    "                continue                         # 1c (i): asking has stopped on this gap\n")
RES = [
    lambda o, t: o + t,                 # the arm flags: both
    lambda o, t: o + t,                 # Agent state: both
    lambda o, t: SPACE_SURV,            # _survivors + 1c's _space_survivors on the re-priced record
    lambda o, t: NONE_CAUSE + o,        # _none_cause, then the re-price's _space_bounds head
    lambda o, t: o,                     # _space_bounds' locals: the re-price's
    lambda o, t: o,                     # _space_bounds' loop, _reprice_hit, _row_wrong: the re-price's
    lambda o, t: HELD + o,              # _ask: 1c's held skip, then the stored eligibility
]
it = iter(range(7))
s = pat.sub(lambda m: RES[next(it)](m.group(1), m.group(2)), s)
assert "<<<<<<<" not in s and ">>>>>>>" not in s
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
