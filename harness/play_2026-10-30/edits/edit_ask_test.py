"""Whole-line edits to tests/test_ask.py: PROBE takes a step count; hold_no_gap runs 10 gridworld steps."""
import sys
sys.dont_write_bytecode = True
p = "c:/Users/Admin/Documents/GitHub/tether/tests/test_ask.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
pairs = [
    ("tree, which = sys.argv[1], sys.argv[2]", "tree, which, n = sys.argv[1], sys.argv[2], int(sys.argv[3])"),
    ("    n = 16" + nl + "else:", "else:"),
    ("    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=\"g\"), tether.Config(), ledger.Ledger())" + nl + "    n = 24" + nl,
     "    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=\"g\"), tether.Config(), ledger.Ledger())" + nl),
    ("def _child(tree: str, which: str, extra: dict | None = None) -> list:",
     "def _child(tree: str, which: str, extra: dict | None = None, n: int | None = None) -> list:"),
    ("    out = subprocess.run([sys.executable, \"-B\", \"-c\", PROBE, tree, which], env=env,",
     "    n = n or {\"fake\": 16, \"grid\": 24}[which]" + nl
     + "    out = subprocess.run([sys.executable, \"-B\", \"-c\", PROBE, tree, which, str(n)], env=env,"),
    ("    on = _child(root, \"grid\")", "    on = _child(root, \"grid\", n=HOLD)"),
    ("    off = _child(root, \"grid\", {\"TETHER_ASK\": \"0\"})", "    off = _child(root, \"grid\", {\"TETHER_ASK\": \"0\"}, n=HOLD)"),
    ("    print(f\"  MUST-HOLD: gridworld 24 steps, no gap with two survivors: ON = OFF, {len(on)} rows\")",
     "    print(f\"  MUST-HOLD: gridworld {HOLD} steps, no ask yet: ON = OFF, {len(on)} rows\")"),
    ("BASE = \"dad9d2b\"      # general-agent after 1a, the tree before the arm",
     "BASE = \"dad9d2b\"      # general-agent after 1a, the tree before the arm" + nl
     + "HOLD = 10             # gridworld default seed 0 first asks at cycle 12 under bargain S1 (r327)"),
    ("  check_hold_no_gap       MUST-HOLD: gridworld, 24 steps, where no gap holds two survivors: ON",
     "  check_hold_no_gap       MUST-HOLD: gridworld, the steps before its first ask: ON"),
]
for a, b in pairs:
    assert s.count(a) == 1, ("not exactly once", a[:70], s.count(a))
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok", len(pairs))
