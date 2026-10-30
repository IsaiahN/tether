import sys
sys.dont_write_bytecode = True
for p, pairs in {
 "c:/Users/Admin/Documents/GitHub/tether/tether.py": [
  ("        a risky settle on this slot: the gap leaves 1b; (ii) MECHANISM BROKEN -- the space had\n",
   "        a risky settle on this slot under the current key: the gap leaves 1b; (ii) NONE SURVIVE --\n"),
  ("        survivors and has none, judged only where the record is current: the slot owes. And (iii)'s\n"
   "        aims leave when their owner's readings change or their space closes. A stop_rule row on\n",
   "        the space had survivors and has none, judged only where the record is current: the slot\n"
   "        owes, and the import route refits held terms before a mint (r338). And (iii)'s aims leave\n"
   "        once probed, when their owner reads anew, or when their space closes. A stop_rule row on\n"),
 ],
 "c:/Users/Admin/Documents/GitHub/tether/conform/arms.py": [
  ("                         \"HELD -- one S1 survivor and a risky settle of it on this slot \"\n"
   "                         \"(_settle_pred's code space) -- takes the gap out of 1b's eligible gaps; \"\n"
   "                         \"MECHANISM BROKEN -- the space had survivors and has none, judged only \"\n"
   "                         \"where the record is current -- puts the slot in owed_import; each \"\n",
   "                         \"HELD -- one S1 survivor and a risky settle of it on this slot under \"\n"
   "                         \"the space's current key (_settle_pred's code space) -- takes the gap \"\n"
   "                         \"out of 1b's eligible gaps; NONE SURVIVE -- the space had survivors and \"\n"
   "                         \"has none, judged only where the record is current -- puts the slot in \"\n"
   "                         \"owed_import, whose route refits before a mint (r338); each \"\n"),
  ("                         \"(_aims) until its owner reads anew or its space closes \"\n"
   "                         \"(split_aim_left). Nothing binds. Needs TETHER_ASK. OFF: as before. \"\n",
   "                         \"(_aims), spent once the probe presses at the owner, or left when the \"\n"
   "                         \"owner reads anew or the space closes (split_aim_left); a spent gap \"\n"
   "                         \"re-enters only on a new refusal key. Nothing binds. Needs TETHER_ASK. \"\n"
   "                         \"OFF: as before. \"\n"),
 ]}.items():
    s = open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in s else "\n"
    for a, b in pairs:
        a, b = a.replace("\n", nl), b.replace("\n", nl)
        assert s.count(a) == 1, (p[-12:], a[:70], s.count(a))
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
