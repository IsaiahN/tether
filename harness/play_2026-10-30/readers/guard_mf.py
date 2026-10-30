import subprocess
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, "C:/Users/Admin/Documents/GitHub/tether/tests")
sys.path.insert(0, "C:/Users/Admin/Documents/GitHub/tether")
import test_step_mint as t  # noqa: E402
R = "C:/Users/Admin/Documents/GitHub/tether"
src = lambda c: subprocess.run(["git", "-C", R, "show", f"{c}:tether.py"], capture_output=True, text=True, encoding="utf-8").stdout  # noqa: E731
base, bad = t._decorated(src("ae028d6")), t._decorated(src("47972ad"))
print("decorated at ae028d6:", len(base), sorted(base.items())[:6])
print("MUST-FAIL at 47972ad, moved:", {k: (v, bad.get(k)) for k, v in base.items() if bad.get(k) != v})
