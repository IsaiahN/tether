import sys
sys.dont_write_bytecode = True
p = "c:/Users/Admin/Documents/GitHub/tether/tether.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
pairs = [
("    @staticmethod\n"
 "    def _none_cause(prev: dict, low: dict) -> str:\n"
 "        \"\"\"1c (ii), r339: 'bound' when a last survivor's stored bound ROSE -- the ground charged\n"
 "        it, evidence (Fig 5 :14) -- else 'bar': only the cut moved (Fig 9 :40-41).\"\"\"\n"
 "        return (\"bound\" if any(low.get(n) is not None and low[n] > b for n, b in prev.items())\n"
 "                else \"bar\")\n",
 "    @staticmethod\n"
 "    def _none_cause(prev: dict, low: dict, bar_before: float) -> str:\n"
 "        \"\"\"1c (ii), r339, r340: 'bound' when a last survivor's bound rose to the bar it last\n"
 "        survived under -- the ground's charge alone would have removed it (Fig 5 :14); 'stale'\n"
 "        when no last survivor's cell is still valid (P2 at the survivor grain); else 'bar': the\n"
 "        cut moved (Fig 9 :40-41).\"\"\"\n"
 "        if not any(n in low for n in prev):\n"
 "            return \"stale\"\n"
 "        return \"bound\" if any(n in low and low[n] >= bar_before for n in prev) else \"bar\"\n"),
("                cause = self._none_cause(prev[0], low)\n",
 "                cause = self._none_cause(prev[0], low, prev[1])\n"),
("                extra = {\"cause\": cause, \"owes\": cause == \"bound\", \"last_survivors\": len(prev[0]),\n"
 "                         \"bound_rose\": rose, \"low_before\": round(min(prev[0].values()), 4),\n",
 "                extra = {\"cause\": cause, \"owes\": cause == \"bound\", \"last_survivors\": len(prev[0]),\n"
 "                         \"bound_rose\": rose,\n"
 "                         \"reached_bar\": sorted(n for n in prev[0] if n in low and low[n] >= prev[1]),\n"
 "                         \"invalid_cells\": sum(1 for n in prev[0] if n not in low),\n"
 "                         \"low_before\": round(min(prev[0].values()), 4),\n"),
]
for a, b in pairs:
    a, b = a.replace("\n", nl), b.replace("\n", nl)
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
