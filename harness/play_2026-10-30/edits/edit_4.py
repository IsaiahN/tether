"""4 PLAN_NARROW (r325 ASK 3, r365) on the 1e tree. argv: repo root, 1e's short sha."""
import sys

sys.dont_write_bytecode = True
R, E1 = sys.argv[1].rstrip("/"), sys.argv[2]


def load(rel):
    p = f"{R}/{rel}"
    s = open(p, encoding="utf-8", newline="").read()
    return p, s, ("\r\n" if "\r\n" in s else "\n")


def edit(rel, pairs):
    p, s, nl = load(rel)
    for a, b in pairs:
        a, b = a.replace("\n", nl), b.replace("\n", nl)
        assert s.count(a) == 1, (rel, a[:80], s.count(a))
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8", newline="").write(s)


# the filter loop becomes _admit(items), re-indented by four, appending to its own list
p, s, nl = load("tether.py")
head = "        for text, s in src.items():" + nl + "            cap.head()" + nl
tail = "            cands.append(((0 if won else 1, round(bits, 6)), text, c, tk, s))" + nl
i, j = s.index(head), s.index(tail)
assert s.count(head) == 1 and s.count(tail) == 1 and i < j
block = s[i:j + len(tail)]
lines = block.split(nl)
body = nl.join(("    " + ln) if ln else ln for ln in lines)
body = body.replace("                cands.append(((0 if won else 1", "                out.append(((0 if won else 1")
fl = "            for text, s in src.items():" + nl
assert body.count(fl) == 1
body = body.replace(fl, "            for text, s in items.items():" + nl)
cc = "                c = self._compile_cache.get(text)" + nl
assert body.count(cc) == 1
body = body.replace(cc, "                compiled[0] += 1" + nl + cc)
new = (
    "        # 4 PLAN_NARROW (r325 ASK 3, r365): the shelf-won texts are known before compiling, and" + nl
    + "        # every won group ranks above every other; compile them first and the rest only if they" + nl
    + "        # yield no pick -- the same pick, by construction. OFF, or nothing won: one phase, as before" + nl
    + "        won_src = ({t: k for t, k in src.items()" + nl
    + "                    if self._goal_shelf.get(k, {}).get(\"record\", {}).get(\"won\", 0)}" + nl
    + "                   if _PLAN_NARROW else {})" + nl
    + "        phases = ([won_src, {t: k for t, k in src.items() if t not in won_src}]" + nl
    + "                  if won_src and len(won_src) < len(src) else [src])" + nl
    + "        compiled = [0]" + nl + nl
    + "        def _admit(items: dict) -> list:" + nl
    + "            out = []" + nl
    + body
    + "            return out" + nl + nl
    + "        cands = _admit(phases[0])" + nl
)
s = s[:i] + new + s[j + len(tail):]
open(p, "w", encoding="utf-8", newline="").write(s)

edit("tether.py", [
 ("_NAMED_REMAINDER = armflag.arm(\"TETHER_NAMED_REMAINDER\", default=True)\n",
  "_NAMED_REMAINDER = armflag.arm(\"TETHER_NAMED_REMAINDER\", default=True)\n"
  "# 4 PLAN_NARROW (the reviewer 2026-10-29 r325 ASK 3, r365; Fig 12 :127): the planner compiles the\n"
  "# shelf-won texts first and the rest only if they yield no pick -- what the life learned ranks and\n"
  "# cuts the work, never widens it. Exact: the same pick. The goal_hypotheses row says how many were\n"
  "# compiled and left. ON; conform/arms.py\n"
  "_PLAN_NARROW = armflag.arm(\"TETHER_PLAN_NARROW\", default=True)\n"),
 ("        n0, self._hyp_open = self._hyp_n, None\n",
  "        n0, self._hyp_open, self._hyp_phases = self._hyp_n, None, 0\n"),
 ("                            capped={\"at\": \"goal_hypothesis\", \"checked\": checked,\n"
  "                                    \"unreached\": None if opened is None else opened - checked})\n",
  "                            capped={\"at\": \"goal_hypothesis\", \"checked\": checked,\n"
  "                                    \"unreached\": None if opened is None else opened - checked,\n"
  "                                    **({\"phases\": self._hyp_phases} if _PLAN_NARROW else {})})\n"),
 ("        cands = _admit(phases[0])\n"
  "        cands.sort(key=lambda x: x[0])\n"
  "        ranked_all = list(cands)                # the pick's rank is read against this order\n"
  "        self._hyp_open = len(cands)              # C1 item 1: a cut's record counts against it\n",
  "        cands = _admit(phases[0])\n"
  "        cands.sort(key=lambda x: x[0])\n"
  "        ranked_all = list(cands)                # the pick's rank is read against this order\n"
  "        self._hyp_open = len(cands)              # C1 item 1: a cut's record counts against it\n"
  "        self._hyp_phases, pending = 1, phases[1:]\n"),
 ("        while cands and pick is None:\n"
  "            cap.head()\n"
  "            group = [x for x in cands if x[0] == cands[0][0]]\n",
  "        while pick is None:\n"
  "            if not cands:\n"
  "                if not pending:\n"
  "                    break\n"
  "                cands = _admit(pending.pop(0))  # 4: the won group held no route; the rest now\n"
  "                cands.sort(key=lambda x: x[0])\n"
  "                ranked_all += cands\n"
  "                self._hyp_open += len(cands)\n"
  "                self._hyp_phases += 1\n"
  "                continue\n"
  "            cap.head()\n"
  "            group = [x for x in cands if x[0] == cands[0][0]]\n"),
 ("        detail.update(checked=checked, refused=dict(refused))\n",
  "        detail.update(checked=checked, refused=dict(refused))\n"
  "        if _PLAN_NARROW:\n"
  "            detail.update(compiled=compiled[0], uncompiled=sum(len(p) for p in pending),\n"
  "                          phases=self._hyp_phases, wall_s=round(time.perf_counter() - t0, 4))\n"),
])

edit("conform/arms.py", [
 ("    \"TETHER_NAMED_REMAINDER\": \"1e NAMED_REMAINDER (the reviewer 2026-10-29 r325, r364; Fig 13 \"\n",
  "    \"TETHER_PLAN_NARROW\": \"4 PLAN_NARROW (the reviewer 2026-10-29 r325 ASK 3, r365; Fig 12 :127). \"\n"
  "                          \"_hyp_propose_body admits candidates in two phases when the goal shelf \"\n"
  "                          \"holds a won record: the shelf-won texts first (known before \"\n"
  "                          \"compiling), the rest only if the won groups yield no pick. Every won \"\n"
  "                          \"group ranks above every other and the walk stops at the first group \"\n"
  "                          \"with a route, so the pick is today's. The goal_hypotheses row carries \"\n"
  "                          \"compiled, uncompiled, phases and wall_s; open, ranked and refused cover \"\n"
  "                          \"the phases run; the cap record carries phases. The kind-scoped cut is a \"\n"
  "                          \"later item. OFF, or nothing won: one phase, as before. default ON\",\n"
  "    \"TETHER_NAMED_REMAINDER\": \"1e NAMED_REMAINDER (the reviewer 2026-10-29 r325, r364; Fig 13 \"\n"),
])

edit("tests/_batch.py", [
 ("    (\"TETHER_NAMED_REMAINDER\", None),        # 1e; its sha comes with the next arm\n",
  f"    (\"TETHER_NAMED_REMAINDER\", \"{E1}\"),        # 1e\n"
  "    (\"TETHER_PLAN_NARROW\", None),            # 4; its sha comes with the next arm\n"),
])
print("ok")
