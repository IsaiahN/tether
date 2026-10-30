import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
old = '''_k32, _ps = ctypes.windll.kernel32, ctypes.windll.psapi
_k32.GetCurrentProcess.restype = wt.HANDLE'''
new = '''# its OWN handles: ctypes.windll shares function objects, and game_one sets argtypes on the shared one with its own PMC
_k32, _ps = ctypes.WinDLL("kernel32"), ctypes.WinDLL("psapi")
_k32.GetCurrentProcess.restype = wt.HANDLE'''
assert s.count(old) == 1
s = s.replace(old, new)
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("ok")
