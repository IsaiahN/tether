def rep(p, old, new):
    s = open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in s else "\n"
    old, new = old.replace("\n", nl), new.replace("\n", nl)
    assert s.count(old) == 1, (p, old[:60], s.count(old))
    open(p, "w", encoding="utf-8", newline="").write(s.replace(old, new))


rep("tether.py",
    '        self._hyp_why = None if self._hyp is None else "a held routine acted first"\n',
    '        self._hyp_why = (None if not _GOAL_HYP or self._hyp is None\n'
    '                         else "a held routine acted first")\n')
rep("tether.py",
    '        keep = set(h["slots"]) | {p.operand for p in parts if getattr(p, "operand", None)}\n',
    '        keep = set(h["slots"]) | {s for p in parts for s in (p.slot, getattr(p, "operand", None))\n'
    '                                  if s}             # both parties, whichever holds the want\n')
rep("test_hyp_hold.py",
    '    sl, op = h["slots"][0], h["cond"].operand\n',
    '    sl = h["slots"][0]\n'
    '    op = next(s for s in (h["cond"].slot, h["cond"].operand) if s != sl)   # the other party\n')
p = "test_hyp_hold.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
i, j = s.index('"""THE TOUCH'), s.index("    python test_hyp_hold.py")
doc = nl.join([
    '"""THE TOUCH HOLD (TETHER_GOAL_HYPOTHESES; the reviewer 2026-10-20 18:40 CDT). gridworld_arc_s1,',
    "the agent seed pinned, one process, each check on a fresh agent stepped until a hypothesis is",
    "held, System 0 forced active in both arms (so OFF is System 0), the arm toggled at the call.",
    "",
    "  H1 a planted touch: the held hypothesis's residual reads 0 exactly while its subject and its",
    "     other party keep the values they had at the touch. ON: the touched cycle's act is a \"hold\"",
    "     with an action the delta table never saw move either, both values are unchanged after it,",
    "     and the next reading at 0 CONFIRMS (the hypothesis ends arrived_no_clear). OFF: System 0.",
    "  H2 no holding action known, and one action planted as the platform's (provenance",
    "     platform-universal) and left untried -- vc33's RESET at c4: ON it is withheld (System 0",
    "     acts with another) and the repeat row says why; OFF System 0 takes it (untried first).",
    "", ""])
open(p, "w", encoding="utf-8", newline="").write(s[:i] + doc + s[j:])
print("ok")
