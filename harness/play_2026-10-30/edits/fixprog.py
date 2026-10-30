import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
reps = [
('''             seq range [seq0, seq1): minted''', '''             seq range [seq0, the next slice's seq0) (switch.tsv's seq1 closes after the first step only): minted'''),
('''             (books rows lag a cycle); confirmed / ruled_out = PERCEIVE/bet rows with predicted == actual % alphabet / not (residues,
             the row carries its alphabet); furthest_level''', '''             (books rows lag a cycle); confirmed / ruled_out = SCORED PERCEIVE/bet rows (actual and alphabet present) with
             predicted == actual % alphabet / not (residues); suspended = bet rows carrying "suspended" (the seam, unscored);
             furthest_level'''),
('''    python progress.py''', '''             library_files_after / store_bytes_end = the round's WRITE_CHECK line.
    python progress.py'''),
('"minted", "reused",\n             "confirmed", "ruled_out"]', '"minted", "reused",\n             "confirmed", "ruled_out", "suspended"]'),
('"library_files_after", "store_bytes_start",', '"library_files_after", "store_bytes_start", "store_bytes_end",'),
('''        after = re.search(rf"ROUND {n} AFTER (\d+) names|ROUND {n} .*?names after (\d+)", log)''',
 '''        after = re.search(rf"^\S+ ROUND {n} WRITE_CHECK rc \d+ .*?names (\d+) .*?store_bytes (\d+)", log, re.M)'''),
('''        for ln in sw:
            if ln[0].startswith("#") or len(ln) < 13:
                continue
            idx, game, ws, _c0, wall, _steps, lv, ending, endings = ln[:9]
            acts, seq0, seq1 = ln[13], int(ln[10]), int(ln[12])
            sl = [r for r in rows if seq0 <= r.get("seq", -1) < seq1]''',
'''        sl_rows = [ln for ln in sw if not ln[0].startswith("#") and len(ln) >= 14]
        for j, ln in enumerate(sl_rows):
            idx, game, ws, _c0, wall, _steps, lv, ending, endings = ln[:9]
            acts, seq0 = ln[13], int(ln[10])
            seq_end = int(sl_rows[j + 1][10]) if j + 1 < len(sl_rows) else len(rows) + 10**9
            sl = [r for r in rows if seq0 <= r.get("seq", -1) < seq_end]'''),
('''            bets = [r["detail"] for r in sl if r.get("event") == "bet" and "predicted" in r.get("detail", {})
                    and isinstance(r["detail"].get("actual"), int) and r["detail"].get("alphabet")]''',
'''            allb = [r["detail"] for r in sl if r.get("event") == "bet"]
            bets = [b for b in allb if "predicted" in b and isinstance(b.get("actual"), int) and b.get("alphabet")
                    and not b.get("suspended")]
            susp = sum(bool(b.get("suspended")) for b in allb)'''),
('''                              "confirmed": conf, "ruled_out": len(bets) - conf})''',
 '''                              "confirmed": conf, "ruled_out": len(bets) - conf, "suspended": susp})'''),
('''            "library_files_after": next((g for g in (after.groups() if after else ()) if g), ""),
            "store_bytes_start": m.group(2) if m else "",''',
 '''            "library_files_after": after.group(1) if after else "",
            "store_bytes_start": m.group(2) if m else "", "store_bytes_end": after.group(2) if after else "",'''),
]
for a, b in reps:
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s); print('ok', len(reps))
