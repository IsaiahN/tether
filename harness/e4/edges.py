"""THE LEDGER LEVEL CHECK over every E4a game (the reviewer 2026-10-18 23:21 item 2; 04:18:18Z ruling): per game, the
rows that carry one of the ledger's edge words (ledger.WIN, DEATH, RESET, ADVANCE), counted two ways so a miss in
one shows in the other: STRUCTURED (the row's detail.how or detail.ending equals the word) and RAW (the quoted word
appears anywhere in the line). READ ONLY. argv: e4_dir repo"""
import glob
import json
import os
import sys

sys.dont_write_bytecode = True
E4, REPO = sys.argv[1], sys.argv[2]
sys.path.insert(0, REPO)
import ledger  # noqa: E402

WORDS = (ledger.WIN, ledger.DEATH, ledger.RESET, ledger.ADVANCE)
CTRL = ledger.CAP        # the NON-ZERO CONTROL: the same two counters on the end word every finished game writes
print("# words", WORDS, "control", CTRL)
print("idx\tgame\trows\tstructured\traw\tby_word\tctrl_structured\tctrl_raw")
n_games = n_any = 0
for d in sorted(glob.glob(os.path.join(E4, "public", "[0-9][0-9]_*"))):
    idx, g = os.path.basename(d).split("_", 1)
    p = os.path.join(d, f"{g}.jsonl")
    if not os.path.exists(p):
        print(f"{idx}\t{g}\tNO LEDGER")
        continue
    rows = st = raw = cst = craw = 0
    by = dict.fromkeys(WORDS, 0)
    with open(p, encoding="utf-8") as fh:
        for ln in fh:
            rows += 1
            hit = [w for w in WORDS if f'"{w}"' in ln]
            raw += bool(hit)
            craw += f'"{CTRL}"' in ln
            for w in hit:
                by[w] += 1
            try:
                det = json.loads(ln).get("detail") or {}
            except ValueError:
                continue
            st += det.get("how") in WORDS or det.get("ending") in WORDS
            cst += det.get("how") == CTRL or det.get("ending") == CTRL
    n_games += 1
    n_any += bool(st or raw)
    print(f"{idx}\t{g}\t{rows}\t{st}\t{raw}\t{by}\t{cst}\t{craw}")
print(f"# games with any edge row: {n_any}/{n_games}")
