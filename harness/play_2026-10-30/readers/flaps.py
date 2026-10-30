"""Read-only: the stop_rule rows a stop_smoke output printed, one line each with the r340 fields."""
import ast
import sys

sys.dont_write_bytecode = True
for ln in open(sys.argv[1], encoding="utf-8"):
    if not ln.startswith("  ") or " stop_rule " not in ln:
        continue
    head, _, rest = ln.strip().partition(" stop_rule ")
    d = ast.literal_eval(rest)
    br = d.get("bound_rose") or {}
    print(head, d["rule"], d.get("cause"), "last", d.get("last_survivors"), "rose", len(br),
          "reached", len(d.get("reached_bar") or []), "invalid", d.get("invalid_cells"),
          "low", d.get("low_before"), "->", d.get("low_after"), "bar", d.get("bar_before"), "->",
          d.get("bar_after"), "e.g.", list(br.items())[:2])
