"""MF for the seat fix: an UNDECLARED raw value read is red; the declared one is not."""
import sys
sys.dont_write_bytecode = True
sys.path[:0] = ["C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/conform", "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv"]
import arms
und = arms.bypasses({"x.py": 'v = os.environ.get("TETHER_SOME_UNDECLARED_CEILING") or ""\n'})
dec = arms.bypasses({"x.py": 'v = os.environ.get("TETHER_CONSOLIDATE_CEILING") or ""\n'})
print("undeclared ->", und)
print("declared ->", dec)
assert len(und) == 1 and "TETHER_SOME_UNDECLARED_CEILING" in und[0] and dec == []
print("MF ok")
