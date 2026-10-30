"""Carry auto_play23.ps1 -> auto_play24.ps1 and want23.sh -> want24.sh by ordered replacements (r440 item 4)."""
import sys

sys.dont_write_bytecode = True
SP = sys.argv[1]
src = open(f"{SP}/auto_play23.ps1", encoding="utf-8").read()
s = src.replace("PLAY23", "@@P24@@").replace("PLAY22", "PLAY23").replace("PLAY21", "PLAY22").replace("@@P24@@", "PLAY24")
s = s.replace("fresh_r29", "@@R30@@").replace("fresh_r28", "fresh_r29").replace("@@R30@@", "fresh_r30")
s = s.replace("want23.sh", "want24.sh")
s = s.replace("$oldG = 'e7a1c8ebe4a5e1eca3ce0b9978221cfcc1a0f6fb'; $oldH = 'a3ad3eff6a738c4e057afb613bde9b638b7fe55c'",
              "$oldG = 'eadee1aa0c5c6f7e24381099d8573f28be254e04'; $oldH = '26a68e0e23bef27a622ccfa5f86bb01d83f04126'")
open(f"{SP}/auto_play24.ps1", "w", encoding="utf-8", newline="").write(s)
w = open(f"{SP}/want23.sh", encoding="utf-8").read()
w = w.replace("PLAY23", "PLAY24").replace("fresh_r29", "fresh_r30")
open(f"{SP}/want24.sh", "w", encoding="utf-8", newline="").write(w)
print("ok")
