import sys
sys.dont_write_bytecode = True
sys.path[:0] = ["C:/TETHER_RUNS/S6_2026-10-19/wt_ivv"]
import test_k1
test_k1.in_process()
print("in_process OK")
