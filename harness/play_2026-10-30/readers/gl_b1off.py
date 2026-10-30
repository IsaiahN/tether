"""Diagnostic only: test_gate_ledger.main() with B1 (tether._STEP_MINT) switched OFF in-process."""
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, "C:/Users/Admin/Documents/GitHub/tether/tests")
sys.path.insert(0, "C:/Users/Admin/Documents/GitHub/tether")
import tether  # noqa: E402
import test_gate_ledger  # noqa: E402
tether._STEP_MINT = False
print("B1 _STEP_MINT =", tether._STEP_MINT)
sys.exit(test_gate_ledger.main())
