import os
import sys
import tempfile

sys.path.insert(0, "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv")
import test_store_key_memo as t

tmp = tempfile.mkdtemp()
a, b = os.path.join(tmp, "x"), os.path.join(tmp, "y")
os.makedirs(a)
os.makedirs(b)
t._run("write", a, "2", env_extra={"TETHER_STORE_KEY_MEMO": "0"})
t._run("write", b, "2", env_extra={"TETHER_STORE_KEY_MEMO": "0"})
fa, fb = t._files(a), t._files(b)
print("OFF vs OFF same:", fa == fb)
print("names A:", sorted(fa)[:8])
print("names B:", sorted(fb)[:8])
print("differ:", [k for k in set(fa) | set(fb) if fa.get(k) != fb.get(k)][:8])
